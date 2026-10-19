use crate::gui::MonitorService;
use std::{sync::{Mutex, atomic::{AtomicBool, Ordering}}, time::Duration};
use tauri::{Emitter, Manager, WebviewUrl, WebviewWindowBuilder};

#[derive(Default)]
pub struct PanelState { pub pinned: AtomicBool, pub focused: AtomicBool, showing: AtomicBool, opened: Mutex<Option<std::time::Instant>>, dismissed:Mutex<Option<std::time::Instant>> }

pub fn dismiss(app:&tauri::AppHandle) {
    let state=app.state::<PanelState>();
    if state.showing.load(Ordering::Relaxed) {if let Ok(mut at)=state.dismissed.lock(){*at=Some(std::time::Instant::now());}}
    state.showing.store(false,Ordering::Relaxed);
    state.focused.store(false,Ordering::Relaxed);
    state.pinned.store(false,Ordering::Relaxed);
    if let Some(window)=app.get_webview_window("activity-panel") {let _=window.hide();}
    emit_state(app);
    if let Some(monitor)=&app.state::<MonitorService>().monitor {
        if let Ok(mut detector)=monitor.detector.lock() {detector.acknowledge();}
    }
}
pub fn toggle(app:&tauri::AppHandle) {
    let state=app.state::<PanelState>();
    if state.showing.load(Ordering::Relaxed) {dismiss(app);}
    else if !state.dismissed.lock().ok().and_then(|t|*t).is_some_and(|t|t.elapsed()<Duration::from_millis(300)) {
        if let Err(error)=show(app,true) {eprintln!("Activity panel: {error}");}
    }
}
pub fn show(app:&tauri::AppHandle, focus:bool) -> Result<(),String> {
    let window=app.get_webview_window("activity-panel").ok_or("Activity panel unavailable")?;
    let tray=app.tray_by_id("care").ok_or("Menu-bar icon unavailable")?;
    let rect=tray.rect().map_err(|e|e.to_string())?.ok_or("Menu-bar icon position unavailable")?;
    let monitors=window.available_monitors().map_err(|e|e.to_string())?;
    // Tray coordinates are physical on macOS. Choose the display containing its center.
    let position=rect.position.to_physical::<f64>(1.0);
    let monitor=monitors.iter().find(|m| {
        let p=m.position(); let s=m.size(); position.x>=p.x as f64 && position.x<(p.x as f64+s.width as f64)
            && position.y>=p.y as f64 && position.y<(p.y as f64+s.height as f64)
    }).or_else(||monitors.first()).ok_or("Display unavailable")?;
    let scale=monitor.scale_factor();
    let position=rect.position.to_physical::<f64>(scale); let size=rect.size.to_physical::<f64>(scale);
    let area=monitor.work_area(); let width=(440.0*scale).min(area.size.width as f64);
    let height=(620.0*scale).min(area.size.height as f64-16.0*scale).max(100.0);
    window.set_size(tauri::PhysicalSize::new(width as u32,height as u32)).map_err(|e|e.to_string())?;
    let x=(position.x+size.width/2.0-width/2.0).clamp(area.position.x as f64,area.position.x as f64+area.size.width as f64-width);
    let y=(position.y+size.height+6.0*scale).clamp(area.position.y as f64,area.position.y as f64+area.size.height as f64-height);
    window.set_position(tauri::PhysicalPosition::new(x,y)).map_err(|e|e.to_string())?;
    if focus {window.show().map_err(|e|e.to_string())?; window.set_focus().map_err(|e|e.to_string())?;}
    else {
        #[cfg(target_os="macos")]
        crate::native::show_activity_window(window.ns_window().map_err(|e|e.to_string())?);
        #[cfg(not(target_os="macos"))]
        window.show().map_err(|e|e.to_string())?;
    }
    let state=app.state::<PanelState>(); state.showing.store(true,Ordering::Relaxed);
    *state.opened.lock().map_err(|_|"Panel state unavailable")?=Some(std::time::Instant::now());
    emit_state(app);
    Ok(())
}
#[tauri::command]
pub fn dismiss_activity_panel(app:tauri::AppHandle) {dismiss(&app);}
#[tauri::command]
pub fn pin_activity_panel(app:tauri::AppHandle,pinned:bool) {app.state::<PanelState>().pinned.store(pinned,Ordering::Relaxed);emit_state(&app);}
#[tauri::command]
pub fn activity_panel_state(app:tauri::AppHandle)->serde_json::Value {
    let state=app.state::<PanelState>(); serde_json::json!({"pinned":state.pinned.load(Ordering::Relaxed),"visible":state.showing.load(Ordering::Relaxed)})
}
fn emit_state(app:&tauri::AppHandle) {
    if let Some(window)=app.get_webview_window("activity-panel") {let _=window.emit("activity-panel-state",activity_panel_state(app.clone()));}
}
#[tauri::command]
pub fn open_activity_main(app:tauri::AppHandle,destination:PanelNavigation)->Result<(),String> {
    destination.validate()?;
    let window=app.get_webview_window("main").ok_or("Main window unavailable")?;
    window.show().map_err(|e|e.to_string())?;window.unminimize().map_err(|e|e.to_string())?;window.set_focus().map_err(|e|e.to_string())?;
    window.emit("navigate-main",destination).map_err(|e|e.to_string())?;
    if !app.state::<PanelState>().pinned.load(Ordering::Relaxed) {dismiss(&app);}
    Ok(())
}
#[derive(Clone,serde::Deserialize,serde::Serialize)]
#[serde(rename_all="lowercase")]
pub enum PanelPage {Apps,Space,Activity}
#[derive(Clone,serde::Deserialize,serde::Serialize)]
#[serde(rename_all="camelCase")]
pub struct PanelNavigation {
    page:PanelPage,
    #[serde(default)] settings:bool,
    filter:Option<String>, search:Option<String>, app_id:Option<String>,
    event_id:Option<i64>, section:Option<String>,
}
impl PanelNavigation {
    fn validate(&self)->Result<(),String> {
        if self.search.as_ref().is_some_and(|s|s.len()>2000)
            || self.app_id.as_ref().is_some_and(|s|s.len()>4000)
            || self.event_id.is_some_and(|id|id<=0)
            || self.filter.as_ref().is_some_and(|s|!["all","files","processes"].contains(&s.as_str()))
            || self.section.as_ref().is_some_and(|s|!["writers","timeline","feed"].contains(&s.as_str())) {
            return Err("Invalid Activity navigation".into());
        }
        Ok(())
    }
}
pub fn setup(app:&tauri::App)->Result<(),Box<dyn std::error::Error>> {
    app.manage(PanelState::default());
    WebviewWindowBuilder::new(app,"activity-panel",WebviewUrl::App("index.html?panel=activity".into()))
        .title("Breathing Room Activity").inner_size(440.0,620.0).visible(false).focused(false)
        .decorations(false).resizable(false).skip_taskbar(true).always_on_top(true).build()?;
    let handle=app.handle().clone();
    std::thread::spawn(move || {
        let mut pressed=false; let mut escape_down=false; let mut ticks=0;
        loop {
            std::thread::sleep(Duration::from_millis(100)); ticks+=1;
            let app=handle.clone(); let check=ticks%10==0;
            #[cfg(target_os="macos")]
            let down=crate::native::mouse_pressed();
            #[cfg(not(target_os="macos"))]
            let down=false;
            let click=down&&!pressed; pressed=down;
            #[cfg(target_os="macos")]
            let escape=crate::native::escape_pressed();
            #[cfg(not(target_os="macos"))]
            let escape=false;
            let escape_click=escape&&!escape_down;escape_down=escape;
            let _=handle.run_on_main_thread(move || {
                let state=app.state::<PanelState>();
                let visible=state.showing.load(Ordering::Relaxed);
                if visible && escape_click {dismiss(&app);return;}
                if click && visible && !state.pinned.load(Ordering::Relaxed)
                    && state.opened.lock().ok().and_then(|t|*t).is_some_and(|t|t.elapsed()>Duration::from_millis(400)) {
                    if let Some(window)=app.get_webview_window("activity-panel") {
                        if let (Ok(cursor),Ok(position),Ok(size))=(app.cursor_position(),window.outer_position(),window.outer_size()) {
                            let in_tray=app.tray_by_id("care").and_then(|tray|tray.rect().ok().flatten()).is_some_and(|rect|{
                                let p=rect.position.to_physical::<f64>(1.0);let s=rect.size.to_physical::<f64>(1.0);
                                cursor.x>=p.x && cursor.x<=p.x+s.width && cursor.y>=p.y && cursor.y<=p.y+s.height
                            });
                            if !in_tray && (cursor.x<position.x as f64 || cursor.x>position.x as f64+size.width as f64 || cursor.y<position.y as f64 || cursor.y>position.y as f64+size.height as f64) {dismiss(&app);}
                        }
                    }
                }
                if check {
                    let service=app.state::<MonitorService>();
                    if let Some(monitor)=&service.monitor {
                        let config=monitor.config.lock().map(|c|c.clone()).unwrap_or_default();
                        if state.showing.load(Ordering::Relaxed) {
                            if let Ok(mut detector)=monitor.detector.lock(){detector.acknowledge();}
                        } else if config.enabled && config.alerts.enabled {
                            let at=crate::model::now();
                            let should=monitor.detector.lock().map(|mut d|{d.expire_stale(at,config.interval_seconds);d.can_open(at,config.alerts.cooldown_seconds)}).unwrap_or(false);
                            if should {
                                match show(&app,false) {
                                    Ok(())=>if let Ok(mut detector)=monitor.detector.lock(){detector.mark_opened(at);},
                                    Err(error)=>eprintln!("Activity panel: {error}"),
                                }
                            }
                        }
                    }
                }
            });
        }
    });
    Ok(())
}
