//! Narrow AppKit bridge. Public native APIs, with no AppleScript or shell automation.
#[cfg(target_os = "macos")]
mod mac {
    use base64::Engine;
    use std::{
        ffi::{c_void, CString},
        mem::transmute,
    };
    type Object = *mut c_void;
    #[link(name = "AppKit", kind = "framework")]
    extern "C" {}
    #[link(name = "CoreGraphics", kind = "framework")]
    extern "C" { fn CGEventSourceKeyState(state_id:i32,key:u16)->bool; }
    #[link(name = "objc")]
    extern "C" {
        fn objc_getClass(name: *const i8) -> Object;
        fn sel_registerName(name: *const i8) -> Object;
        fn objc_msgSend();
        fn objc_autoreleasePoolPush() -> Object;
        fn objc_autoreleasePoolPop(pool: Object);
    }
    #[link(name = "IOKit", kind = "framework")]
    extern "C" {
        fn IOPSCopyPowerSourcesInfo() -> Object;
        fn IOPSCopyPowerSourcesList(info: Object) -> Object;
        fn IOPSGetPowerSourceDescription(info: Object, source: Object) -> Object;
    }
    #[link(name = "CoreFoundation", kind = "framework")]
    extern "C" {
        fn CFRelease(object: Object);
        fn CFBooleanGetValue(object: Object) -> u8;
        fn CFGetTypeID(object: Object) -> usize;
        fn CFBooleanGetTypeID() -> usize;
    }
    #[link(name = "Security", kind = "framework")]
    extern "C" {
        fn SecTaskCreateFromSelf(allocator: Object) -> Object;
        fn SecTaskCopyValueForEntitlement(
            task: Object,
            entitlement: Object,
            error: *mut Object,
        ) -> Object;
    }
    unsafe fn class(name: &str) -> Object {
        objc_getClass(CString::new(name).unwrap().as_ptr())
    }
    unsafe fn selector(name: &str) -> Object {
        sel_registerName(CString::new(name).unwrap().as_ptr())
    }
    unsafe fn get(object: Object, method: &str) -> Object {
        let send: unsafe extern "C" fn(Object, Object) -> Object =
            transmute(objc_msgSend as unsafe extern "C" fn());
        send(object, selector(method))
    }
    unsafe fn send_object(object: Object, method: &str, arg: Object) -> Object {
        let send: unsafe extern "C" fn(Object, Object, Object) -> Object =
            transmute(objc_msgSend as unsafe extern "C" fn());
        send(object, selector(method), arg)
    }
    unsafe fn string(object: Object) -> String {
        let utf8 = get(object, "UTF8String");
        if utf8.is_null() {
            String::new()
        } else {
            std::ffi::CStr::from_ptr(utf8 as *const i8)
                .to_string_lossy()
                .into_owned()
        }
    }
    unsafe fn ns_string(value: &str) -> Object {
        let send: unsafe extern "C" fn(Object, Object, *const i8) -> Object =
            transmute(objc_msgSend as unsafe extern "C" fn());
        send(
            class("NSString"),
            selector("stringWithUTF8String:"),
            CString::new(value).unwrap().as_ptr(),
        )
    }
    /// Order a floating activity window without activating this application.
    /// Call only on the AppKit main thread.
    pub fn show_activity_window(window: Object) {
        unsafe {
            let level: unsafe extern "C" fn(Object,Object,isize)=transmute(objc_msgSend as unsafe extern "C" fn());
            level(window,selector("setLevel:"),3);
            let order: unsafe extern "C" fn(Object,Object)=transmute(objc_msgSend as unsafe extern "C" fn());
            order(window,selector("orderFrontRegardless"));
        }
    }
    pub fn mouse_pressed() -> bool {
        unsafe {
            let send:unsafe extern "C" fn(Object,Object)->usize=transmute(objc_msgSend as unsafe extern "C" fn());
            send(class("NSEvent"),selector("pressedMouseButtons")) != 0
        }
    }
    pub fn escape_pressed() -> bool { unsafe { CGEventSourceKeyState(1,53) } }
    pub fn sandboxed() -> bool {
        unsafe {
            let pool = objc_autoreleasePoolPush();
            let task = SecTaskCreateFromSelf(std::ptr::null_mut());
            if task.is_null() {
                objc_autoreleasePoolPop(pool);
                return true;
            }
            let mut error = std::ptr::null_mut();
            let value = SecTaskCopyValueForEntitlement(
                task,
                ns_string("com.apple.security.app-sandbox"),
                &mut error,
            );
            let enabled = !value.is_null()
                && CFGetTypeID(value) == CFBooleanGetTypeID()
                && CFBooleanGetValue(value) != 0;
            if !value.is_null() {
                CFRelease(value);
            }
            if !error.is_null() {
                CFRelease(error);
            }
            CFRelease(task);
            objc_autoreleasePoolPop(pool);
            enabled
        }
    }
    pub fn trash(path: &str) -> Result<(), String> {
        unsafe {
            let pool = objc_autoreleasePoolPush();
            let url = send_object(class("NSURL"), "fileURLWithPath:", ns_string(path));
            let manager = get(class("NSFileManager"), "defaultManager");
            let send: unsafe extern "C" fn(Object, Object, Object, *mut Object, *mut Object) -> i8 =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let mut result = std::ptr::null_mut();
            let mut error = std::ptr::null_mut();
            let success = send(
                manager,
                selector("trashItemAtURL:resultingItemURL:error:"),
                url,
                &mut result,
                &mut error,
            );
            let message = if success != 0 {
                Ok(())
            } else {
                let description = string(get(error, "localizedDescription"));
                Err(if description.is_empty() {
                    "Could not move the file to Trash. Check folder access.".into()
                } else {
                    description
                })
            };
            objc_autoreleasePoolPop(pool);
            message
        }
    }
    pub fn in_package(path: &std::path::Path, home: &std::path::Path) -> bool {
        unsafe {
            let pool = objc_autoreleasePoolPush();
            let workspace = get(class("NSWorkspace"), "sharedWorkspace");
            let send: unsafe extern "C" fn(Object, Object, Object) -> i8 =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let mut packaged = false;
            for ancestor in path
                .ancestors()
                .skip(1)
                .take_while(|p| p.starts_with(home) && *p != home)
            {
                if send(
                    workspace,
                    selector("isFilePackageAtPath:"),
                    ns_string(&ancestor.to_string_lossy()),
                ) != 0
                {
                    packaged = true;
                    break;
                }
            }
            objc_autoreleasePoolPop(pool);
            packaged
        }
    }
    pub fn reveal(path: &str) {
        unsafe {
            let pool = objc_autoreleasePoolPush();
            let url = send_object(class("NSURL"), "fileURLWithPath:", ns_string(path));
            let urls = send_object(class("NSArray"), "arrayWithObject:", url);
            send_object(
                get(class("NSWorkspace"), "sharedWorkspace"),
                "activateFileViewerSelectingURLs:",
                urls,
            );
            objc_autoreleasePoolPop(pool);
        }
    }
    pub fn open_trash() -> Result<(), String> {
        unsafe {
            let pool = objc_autoreleasePoolPush();
            // Ask macOS for the user's Trash folder; `trash:` is not a portable
            // Launch Services URL scheme. Do not enumerate or delete its contents.
            let directories: unsafe extern "C" fn(Object, Object, usize, usize) -> Object =
                transmute(objc_msgSend as unsafe extern "C" fn());
            const NS_TRASH_DIRECTORY: usize = 102;
            const NS_USER_DOMAIN_MASK: usize = 1;
            let folders = directories(get(class("NSFileManager"), "defaultManager"), selector("URLsForDirectory:inDomains:"), NS_TRASH_DIRECTORY, NS_USER_DOMAIN_MASK);
            let url = get(folders, "firstObject");
            let open: unsafe extern "C" fn(Object, Object, Object) -> i8 =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let opened = !url.is_null() && open(get(class("NSWorkspace"), "sharedWorkspace"), selector("openURL:"), url) != 0;
            objc_autoreleasePoolPop(pool);
            if opened { Ok(()) } else { Err("Finder couldn't open Trash. Open Trash from the Dock instead; nothing has been deleted.".into()) }
        }
    }
    pub fn low_battery() -> bool {
        unsafe {
            let pool = objc_autoreleasePoolPush();
            let info = IOPSCopyPowerSourcesInfo();
            if info.is_null() {
                objc_autoreleasePoolPop(pool);
                return true;
            }
            let list = IOPSCopyPowerSourcesList(info);
            if list.is_null() {
                CFRelease(info);
                objc_autoreleasePoolPop(pool);
                return true;
            }
            let number: unsafe extern "C" fn(Object, Object) -> isize =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let at: unsafe extern "C" fn(Object, Object, usize) -> Object =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let count = number(list, selector("count"));
            // Desktop Macs have no battery power source.
            let mut low = false;
            for i in 0..count {
                let source = at(list, selector("objectAtIndex:"), i as usize);
                let description = IOPSGetPowerSourceDescription(info, source);
                if description.is_null() {
                    continue;
                }
                let state = string(send_object(
                    description,
                    "objectForKey:",
                    ns_string("Power Source State"),
                ));
                if state != "Battery Power" {
                    continue;
                }
                let current = number(
                    send_object(description, "objectForKey:", ns_string("Current Capacity")),
                    selector("integerValue"),
                );
                let maximum = number(
                    send_object(description, "objectForKey:", ns_string("Max Capacity")),
                    selector("integerValue"),
                );
                if maximum <= 0 || current * 100 / maximum < 40 {
                    low = true;
                }
            }
            CFRelease(list);
            CFRelease(info);
            objc_autoreleasePoolPop(pool);
            low
        }
    }
    pub fn running_apps() -> Result<Vec<crate::model::AppGroup>, String> {
        unsafe {
            let pool = objc_autoreleasePoolPush();
            let apps = get(
                get(class("NSWorkspace"), "sharedWorkspace"),
                "runningApplications",
            );
            let count_send: unsafe extern "C" fn(Object, Object) -> usize =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let count = count_send(apps, selector("count"));
            let at: unsafe extern "C" fn(Object, Object, usize) -> Object =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let pid_send: unsafe extern "C" fn(Object, Object) -> i32 =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let date_send: unsafe extern "C" fn(Object, Object) -> f64 =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let mut groups = std::collections::BTreeMap::<String, crate::model::AppGroup>::new();
            for i in 0..count {
                let app = at(apps, selector("objectAtIndex:"), i);
                let name = string(get(app, "localizedName"));
                let path = string(get(get(app, "bundleURL"), "path"));
                let executable = string(get(get(app, "executableURL"), "path"));
                let pid = pid_send(app, selector("processIdentifier"));
                let activation = pid_send(app, selector("activationPolicy"));
                let started = format!(
                    "launch:{:.6}",
                    date_send(get(app, "launchDate"), selector("timeIntervalSince1970"))
                );
                if pid <= 1 || name.is_empty() {
                    continue;
                }
                let protected = crate::processes::protected_executable(&executable)
                    || pid == std::process::id() as i32;
                let root_path = path
                    .find(".app/")
                    .map(|end| path[..end + 4].to_string())
                    .unwrap_or(path);
                let system = protected && executable.starts_with("/System/");
                let owner = if system {
                    "macOS & protected services".to_string()
                } else if root_path.ends_with(".app") {
                    root_path
                        .rsplit('/')
                        .next()
                        .unwrap_or(&name)
                        .trim_end_matches(".app")
                        .to_string()
                } else {
                    name.clone()
                };
                let id = if system {
                    "system".into()
                } else if root_path.is_empty() {
                    format!("app:{pid}")
                } else {
                    root_path.clone()
                };
                let main = !root_path.is_empty()
                    && executable.starts_with(&format!("{root_path}/Contents/MacOS/"));
                let group = groups.entry(id.clone()).or_insert(crate::model::AppGroup {
                    id,
                    name: owner.clone(),
                    bundle_path: if system || root_path.is_empty() {
                        None
                    } else {
                        Some(root_path)
                    },
                    cpu: 0.0,
                    memory_bytes: 0,
                    metrics_available: false,
                    can_quit: false,
                    coverage: "Main app only · metrics restricted".into(),
                    processes: vec![],
                });
                group.can_quit |= !protected && main && activation == 0;
                group.processes.push(crate::model::Process {
                    pid,
                    parent_pid: 0,
                    uid: libc::getuid(),
                    cpu: 0.0,
                    memory_bytes: 0,
                    started,
                    executable,
                    name,
                    app: owner,
                    protected: true,
                });
            }
            objc_autoreleasePoolPop(pool);
            let mut result: Vec<_> = groups.into_values().collect();
            for group in &mut result {
                if group.processes.len() > 1 {
                    group.coverage = "Observed app metadata · metrics restricted".into();
                }
            }
            result.sort_by(|a, b| {
                b.can_quit
                    .cmp(&a.can_quit)
                    .then(a.name.to_lowercase().cmp(&b.name.to_lowercase()))
            });
            Ok(result)
        }
    }
    pub struct Scope(Object);
    impl Drop for Scope {
        fn drop(&mut self) {
            unsafe {
                get(self.0, "stopAccessingSecurityScopedResource");
                get(self.0, "release");
            }
        }
    }
    pub fn scope(encoded: &str) -> Result<Scope, String> {
        let bytes = base64::engine::general_purpose::STANDARD
            .decode(encoded)
            .map_err(|_| "Invalid folder grant")?;
        unsafe {
            let pool = objc_autoreleasePoolPush();
            let data_send: unsafe extern "C" fn(Object, Object, *const u8, usize) -> Object =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let data = data_send(
                class("NSData"),
                selector("dataWithBytes:length:"),
                bytes.as_ptr(),
                bytes.len(),
            );
            let resolve: unsafe extern "C" fn(
                Object,
                Object,
                Object,
                usize,
                Object,
                *mut i8,
                *mut Object,
            ) -> Object = transmute(objc_msgSend as unsafe extern "C" fn());
            let mut stale = 0;
            let mut error = std::ptr::null_mut();
            let url = resolve(
                class("NSURL"),
                selector(
                    "URLByResolvingBookmarkData:options:relativeToURL:bookmarkDataIsStale:error:",
                ),
                data,
                1 << 10,
                std::ptr::null_mut(),
                &mut stale,
                &mut error,
            );
            let start: unsafe extern "C" fn(Object, Object) -> i8 =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let result = if url.is_null()
                || start(url, selector("startAccessingSecurityScopedResource")) == 0
            {
                Err("Folder grant unavailable. Choose the folder again.".into())
            } else {
                get(url, "retain");
                Ok(Scope(url))
            };
            objc_autoreleasePoolPop(pool);
            result
        }
    }
    pub fn pick_folder() -> Result<Option<(String, String)>, String> {
        unsafe {
            let pool = objc_autoreleasePoolPush();
            let panel = get(class("NSOpenPanel"), "openPanel");
            let set_bool: unsafe extern "C" fn(Object, Object, i8) =
                transmute(objc_msgSend as unsafe extern "C" fn());
            set_bool(panel, selector("setCanChooseDirectories:"), 1);
            set_bool(panel, selector("setCanChooseFiles:"), 0);
            set_bool(panel, selector("setAllowsMultipleSelection:"), 0);
            let modal: unsafe extern "C" fn(Object, Object) -> isize =
                transmute(objc_msgSend as unsafe extern "C" fn());
            if modal(panel, selector("runModal")) != 1 {
                objc_autoreleasePoolPop(pool);
                return Ok(None);
            }
            let url = get(panel, "URL");
            let path_string = get(get(url, "path"), "UTF8String");
            if path_string.is_null() {
                objc_autoreleasePoolPop(pool);
                return Err("Folder path unavailable".into());
            }
            let path = std::ffi::CStr::from_ptr(path_string as *const i8)
                .to_string_lossy()
                .into_owned();
            let make: unsafe extern "C" fn(
                Object,
                Object,
                usize,
                Object,
                Object,
                *mut Object,
            ) -> Object = transmute(objc_msgSend as unsafe extern "C" fn());
            let mut error = std::ptr::null_mut();
            let bookmark = make(
                url,
                selector(
                    "bookmarkDataWithOptions:includingResourceValuesForKeys:relativeToURL:error:",
                ),
                1 << 11,
                std::ptr::null_mut(),
                std::ptr::null_mut(),
                &mut error,
            );
            let length_send: unsafe extern "C" fn(Object, Object) -> usize =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let length = length_send(bookmark, selector("length"));
            let bytes = get(bookmark, "bytes");
            let result = if bytes.is_null() || length == 0 {
                Err("Could not persist this folder grant. Choose the folder again.".into())
            } else {
                Ok(Some((
                    path,
                    base64::engine::general_purpose::STANDARD
                        .encode(std::slice::from_raw_parts(bytes as *const u8, length)),
                )))
            };
            objc_autoreleasePoolPop(pool);
            result
        }
    }
    pub fn quit(pid: i32) -> Result<(), String> {
        unsafe {
            let pool = objc_autoreleasePoolPush();
            let running: unsafe extern "C" fn(Object, Object, i32) -> Object =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let app = running(
                class("NSRunningApplication"),
                selector("runningApplicationWithProcessIdentifier:"),
                pid,
            );
            let result = if app.is_null() {
                Err("The selected process is not a running GUI application.".into())
            } else {
                let send: unsafe extern "C" fn(Object, Object) -> i8 =
                    transmute(objc_msgSend as unsafe extern "C" fn());
                if send(app, selector("terminate")) != 0 {
                    Ok(())
                } else {
                    Err("The app could not be asked to quit. It may have unsaved work or permission restrictions.".into())
                }
            };
            objc_autoreleasePoolPop(pool);
            result
        }
    }
    pub fn icon(path: &str) -> Result<String, String> {
        unsafe {
            let pool = objc_autoreleasePoolPush();
            let utf8: unsafe extern "C" fn(Object, Object, *const i8) -> Object =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let path = CString::new(path).map_err(|_| "Invalid application path")?;
            let ns_path = utf8(
                class("NSString"),
                selector("stringWithUTF8String:"),
                path.as_ptr(),
            );
            let workspace = get(class("NSWorkspace"), "sharedWorkspace");
            let image = send_object(workspace, "iconForFile:", ns_path);
            let tiff = get(image, "TIFFRepresentation");
            let bitmap = send_object(class("NSBitmapImageRep"), "imageRepWithData:", tiff);
            let png_send: unsafe extern "C" fn(Object, Object, usize, Object) -> Object =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let png = png_send(
                bitmap,
                selector("representationUsingType:properties:"),
                4,
                get(class("NSDictionary"), "dictionary"),
            );
            let length_send: unsafe extern "C" fn(Object, Object) -> usize =
                transmute(objc_msgSend as unsafe extern "C" fn());
            let length = length_send(png, selector("length"));
            let bytes = get(png, "bytes");
            let result = if bytes.is_null() || length == 0 || length > 4_000_000 {
                Err("Application icon unavailable".into())
            } else {
                Ok(format!(
                    "data:image/png;base64,{}",
                    base64::engine::general_purpose::STANDARD
                        .encode(std::slice::from_raw_parts(bytes as *const u8, length))
                ))
            };
            objc_autoreleasePoolPop(pool);
            result
        }
    }
}
#[cfg(target_os = "macos")]
pub use mac::{
    icon, low_battery, pick_folder, quit, reveal, open_trash, running_apps, sandboxed, scope, trash, Scope, show_activity_window, mouse_pressed, escape_pressed,
};

#[cfg(test)]
mod tests {
    #[test]
    fn native_app_metadata_has_unique_groups_and_honest_metrics() {
        let apps = super::running_apps().unwrap();
        let unique: std::collections::HashSet<_> = apps.iter().map(|a| &a.id).collect();
        assert_eq!(apps.len(), unique.len());
        assert!(apps.iter().all(|a| !a.metrics_available));
    }
    #[test]
    fn appkit_icon_bridge_returns_a_real_png() {
        let image = super::icon("/System/Applications/Utilities/Terminal.app").unwrap();
        assert!(image.starts_with("data:image/png;base64,iVBOR"));
    }
}

#[cfg(target_os = "macos")]
pub use mac::in_package;
