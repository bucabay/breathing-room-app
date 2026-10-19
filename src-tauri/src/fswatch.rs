//! Public FSEvents bridge. Callback only enqueues; SQL/metadata work happens elsewhere.
use std::{ffi::{c_void, CStr, CString}, sync::{atomic::{AtomicBool, AtomicU64, Ordering}, mpsc::SyncSender, Arc}, time::Duration};

#[derive(Clone, Debug)]
pub struct Change { pub path: String, pub flags: u32, pub event_id: u64, pub at: u64 }
pub struct WatchState {
    pub enabled: AtomicBool,
    pub file_events: AtomicBool,
    pub running: AtomicBool,
    pub dropped: AtomicU64,
    pub error: std::sync::Mutex<String>,
    pub shutdown: AtomicBool,
}
impl Default for WatchState {
    fn default() -> Self { Self { enabled: AtomicBool::new(true), file_events: AtomicBool::new(true), running: AtomicBool::new(false), dropped: AtomicU64::new(0), error: std::sync::Mutex::new(String::new()), shutdown: AtomicBool::new(false) } }
}

#[cfg(target_os = "macos")]
mod mac {
    use super::*;
    type Object = *const c_void;
    #[repr(C)]
    struct Context { version: isize, info: *mut c_void, retain: Option<unsafe extern "C" fn(*const c_void) -> *const c_void>, release: Option<unsafe extern "C" fn(*const c_void)>, describe: Option<unsafe extern "C" fn(*const c_void) -> Object> }
    struct CallbackInfo { sender: SyncSender<Change>, state: Arc<WatchState> }
    #[link(name = "CoreServices", kind = "framework")]
    extern "C" {
        fn FSEventStreamCreate(allocator: Object, callback: unsafe extern "C" fn(Object, *mut c_void, usize, *mut c_void, *const u32, *const u64), context: *mut Context, paths: Object, since: u64, latency: f64, flags: u32) -> Object;
        fn FSEventStreamScheduleWithRunLoop(stream: Object, run_loop: Object, mode: Object);
        fn FSEventStreamStart(stream: Object) -> u8;
        fn FSEventStreamStop(stream: Object);
        fn FSEventStreamInvalidate(stream: Object);
        fn FSEventStreamRelease(stream: Object);
    }
    #[link(name = "CoreFoundation", kind = "framework")]
    extern "C" {
        fn CFStringCreateWithCString(allocator: Object, text: *const i8, encoding: u32) -> Object;
        fn CFArrayCreate(allocator: Object, values: *const Object, count: isize, callbacks: *const c_void) -> Object;
        fn CFRunLoopGetCurrent() -> Object;
        fn CFRunLoopRunInMode(mode: Object, seconds: f64, return_after_source: u8) -> i32;
        fn CFRelease(object: *mut c_void);
        static kCFTypeArrayCallBacks: [usize; 5];
        static kCFRunLoopDefaultMode: Object;
    }
    unsafe extern "C" fn callback(_stream: Object, info: *mut c_void, count: usize, paths: *mut c_void, flags: *const u32, ids: *const u64) {
        if info.is_null() || paths.is_null() || flags.is_null() || ids.is_null() { return; }
        let info = &*(info as *const CallbackInfo);
        if !info.state.enabled.load(Ordering::Relaxed) { return; }
        let paths = paths as *const *const i8;
        if count > 10000 { info.state.dropped.fetch_add((count - 10000) as u64, Ordering::Relaxed); }
        for i in 0..count.min(10000) {
            let raw = *paths.add(i);
            if raw.is_null() { continue; }
            let path = CStr::from_ptr(raw).to_string_lossy().into_owned();
            if path.contains("/app.breathingroom.mac/") { continue; }
            let event = Change { path, flags: *flags.add(i), event_id: *ids.add(i), at: crate::model::now() };
            if info.sender.try_send(event).is_err() { info.state.dropped.fetch_add(1, Ordering::Relaxed); }
        }
    }
    pub fn watch(root: String, sender: SyncSender<Change>, state: Arc<WatchState>) {
        while !state.shutdown.load(Ordering::Relaxed) {
            if !state.enabled.load(Ordering::Relaxed) { std::thread::sleep(Duration::from_millis(500)); continue; }
            let file_mode = state.file_events.load(Ordering::Relaxed);
            unsafe {
                let croot = match CString::new(root.as_str()) { Ok(v) => v, Err(_) => return };
                let string = CFStringCreateWithCString(std::ptr::null(), croot.as_ptr(), 0x08000100);
                let paths = CFArrayCreate(std::ptr::null(), &string, 1, &kCFTypeArrayCallBacks as *const _ as *const c_void);
                let mut info = Box::new(CallbackInfo { sender: sender.clone(), state: state.clone() });
                let mut context = Context { version: 0, info: &mut *info as *mut _ as *mut c_void, retain: None, release: None, describe: None };
                let stream = FSEventStreamCreate(std::ptr::null(), callback, &mut context, paths, u64::MAX, 2.0, 0x2 | 0x4 | 0x8 | if file_mode { 0x10 } else { 0 });
                CFRelease(paths as *mut c_void); CFRelease(string as *mut c_void);
                if stream.is_null() { if let Ok(mut e) = state.error.lock() { *e = "Filesystem stream could not be created".into(); } std::thread::sleep(Duration::from_secs(5)); continue; }
                FSEventStreamScheduleWithRunLoop(stream, CFRunLoopGetCurrent(), kCFRunLoopDefaultMode);
                if FSEventStreamStart(stream) == 0 { if let Ok(mut e) = state.error.lock() { *e = "Filesystem stream could not start; check folder access".into(); } FSEventStreamInvalidate(stream); FSEventStreamRelease(stream); std::thread::sleep(Duration::from_secs(5)); continue; }
                state.running.store(true, Ordering::Relaxed);
                if let Ok(mut e) = state.error.lock() { e.clear(); }
                while state.enabled.load(Ordering::Relaxed) && state.file_events.load(Ordering::Relaxed) == file_mode && !state.shutdown.load(Ordering::Relaxed) {
                    CFRunLoopRunInMode(kCFRunLoopDefaultMode, 0.5, 0);
                }
                state.running.store(false, Ordering::Relaxed);
                FSEventStreamStop(stream); FSEventStreamInvalidate(stream); FSEventStreamRelease(stream);
            }
        }
    }
}

pub fn start(root: String, sender: SyncSender<Change>, state: Arc<WatchState>) {
    #[cfg(target_os = "macos")]
    std::thread::spawn(move || mac::watch(root, sender, state));
}

#[cfg(all(test, target_os = "macos"))]
mod tests {
    use super::*;
    #[test]
    fn public_watcher_observes_owned_fixture_without_scanning() {
        let root=std::env::temp_dir().join(format!("breathing-fsevents-{}",std::process::id()));
        std::fs::create_dir_all(&root).unwrap();
        let root=root.canonicalize().unwrap();
        let (send,receive)=std::sync::mpsc::sync_channel(100);
        let state=Arc::new(WatchState::default());
        start(root.to_string_lossy().into_owned(),send,state.clone());
        for _ in 0..50 { if state.running.load(Ordering::Relaxed) {break;} std::thread::sleep(Duration::from_millis(100)); }
        assert!(state.running.load(Ordering::Relaxed),"FSEvents did not start");
        // IgnoreSelf is intentional; use an owned child to produce a file change.
        let file=root.join("fixture.txt");
        std::process::Command::new("/usr/bin/touch").arg(&file).status().unwrap();
        let deadline=std::time::Instant::now()+Duration::from_secs(8);
        let mut found=false;
        while std::time::Instant::now()<deadline {
            if let Ok(change)=receive.recv_timeout(Duration::from_millis(500)) { if change.path.ends_with("fixture.txt") { found=true;break;} }
        }
        state.shutdown.store(true,Ordering::Relaxed);
        state.enabled.store(false,Ordering::Relaxed);
        std::thread::sleep(Duration::from_millis(600));
        std::fs::remove_dir_all(root).unwrap();
        assert!(found,"No notification for owned test file");
    }
}
