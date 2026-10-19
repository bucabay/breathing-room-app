use crate::{
    model::{now, Candidate, LargeFile, Settings, StorageGroup, StorageReport},
    system,
};
use std::{
    collections::{BTreeMap, HashSet},
    fs,
    os::unix::fs::MetadataExt,
    path::{Path, PathBuf},
    sync::atomic::{AtomicBool, Ordering},
    time::{Duration, Instant},
};

struct Rule {
    id: &'static str,
    name: &'static str,
    relative: &'static str,
    method: &'static str,
    description: &'static str,
}
const RULES: &[Rule] = &[
    Rule { id: "npm", name: "npm download cache", relative: ".npm/_cacache", method: "npm cache clean --force", description: "Removes downloaded packages, not project dependencies. Packages download again when needed." },
    Rule { id: "uv", name: "Unused Python cache", relative: ".cache/uv", method: "uv cache prune", description: "Uses uv's locking and supported pruning. Measured cache size is not a promise of recovered space." },
    Rule { id: "pip", name: "pip download cache", relative: "Library/Caches/pip", method: "python3 -m pip cache purge", description: "Removes cached wheels and downloads. Installed Python packages remain available." },
];

pub fn valid_root(home: &Path, path: &Path) -> Result<PathBuf, String> {
    let canonical = path
        .canonicalize()
        .map_err(|_| "Folder is unavailable or permission is missing")?;
    let home = home.canonicalize().map_err(|_| "Home folder unavailable")?;
    if !canonical.starts_with(&home) {
        return Err(
            "Choose a folder within your home directory for this development build.".into(),
        );
    }
    if !canonical.is_dir() {
        return Err("Choose a folder, not a file.".into());
    }
    Ok(canonical)
}

fn classify(path: &Path, home: &Path, project: &str) -> (String, String) {
    let relative = path.strip_prefix(home).unwrap_or(path).to_string_lossy();
    for (prefix, owner) in [
        (".npm/", "npm"),
        (".yarn/", "Yarn"),
        (".cache/uv/", "Python / uv"),
        ("Library/Caches/pip/", "Python / pip"),
        ("Library/Caches/Homebrew/", "Homebrew"),
        ("Library/Developer/Xcode/", "Xcode"),
        (".cargo/", "Rust"),
        (".nvm/", "Node.js"),
        (".bun/", "Bun"),
        (".pub-cache/", "Dart / Flutter"),
        (".cache/codex-runtimes/", "Codex"),
    ] {
        if relative.starts_with(prefix) {
            return ("development".into(), owner.into());
        }
    }
    if relative.starts_with("Library/Application Support/MobileSync/") {
        return ("backups".into(), "Device backups".into());
    }
    if let Some(end) = relative.find(".app/") {
        let name = relative[..end].rsplit('/').next().unwrap_or("Application");
        return ("apps".into(), name.into());
    }
    if relative.starts_with("Library/Caches/")
        || relative.starts_with("Library/Application Support/")
    {
        let owner = relative.split('/').nth(2).unwrap_or("Other apps");
        let friendly = if owner == "Google" {
            "Google Chrome"
        } else if owner.contains("VSCode") || owner == "Code" {
            "Visual Studio Code"
        } else if owner.contains("Slack") {
            "Slack"
        } else {
            owner
        };
        return ("app-data".into(), friendly.into());
    }
    if !project.is_empty()
        || relative.starts_with("code/")
        || relative.starts_with("workspace/")
        || relative.starts_with(".cache/")
    {
        return ("development".into(), "Projects & tools".into());
    }
    let ext = path
        .extension()
        .and_then(|v| v.to_str())
        .unwrap_or("")
        .to_ascii_lowercase();
    let category = match ext.as_str() {
        "jpg" | "jpeg" | "png" | "heic" | "gif" | "webp" | "tiff" | "raw" | "dng" | "psd" => {
            "images"
        }
        "mp4" | "mov" | "mkv" | "avi" | "m4v" => "video",
        "mp3" | "wav" | "m4a" | "flac" | "aiff" => "audio",
        "dmg" | "pkg" | "zip" | "tar" | "gz" | "xip" | "iso" => "downloads",
        _ if relative.starts_with("Downloads/") => "downloads",
        _ => "documents",
    };
    (category.into(), "Personal files".into())
}
struct Walker<'a> {
    home: &'a Path,
    cancel: &'a AtomicBool,
    deadline: Instant,
    seen: HashSet<(u64, u64)>,
    groups: BTreeMap<String, StorageGroup>,
    rule_sizes: BTreeMap<&'static str, u64>,
    files: u64,
    skipped: u64,
    partial: bool,
    large_files: Vec<LargeFile>,
}
pub fn file_identity(metadata: &fs::Metadata) -> String {
    format!(
        "{}:{}:{}:{}:{}",
        metadata.dev(),
        metadata.ino(),
        metadata.mtime(),
        metadata.mtime_nsec(),
        metadata.len()
    )
}
pub fn personal_file(home: &Path, path: &Path) -> bool {
    let relative = path.strip_prefix(home).unwrap_or(path).to_string_lossy();
    [
        "Downloads/",
        "Desktop/",
        "Documents/",
        "Pictures/",
        "Movies/",
        "Music/",
    ]
    .iter()
    .any(|prefix| relative.starts_with(prefix))
        && ![
            ".app/",
            ".photoslibrary/",
            ".imovielibrary/",
            ".fcpbundle/",
            ".band/",
            ".logicx/",
            ".sparsebundle/",
            ".bundle/",
            ".framework/",
            ".pages/",
            ".numbers/",
            ".key/",
            ".rtfd/",
            ".pvm/",
            ".vmwarevm/",
            "/.git/",
        ]
        .iter()
        .any(|part| relative.contains(part))
}
impl Walker<'_> {
    fn walk(&mut self, path: &Path, project: &str, depth: usize) {
        if self.cancel.load(Ordering::Relaxed)
            || Instant::now() > self.deadline
            || self.files >= 200_000
            || depth > 40
        {
            self.partial = true;
            return;
        }
        let Ok(metadata) = fs::symlink_metadata(path) else {
            self.skipped += 1;
            self.partial = true;
            return;
        };
        if metadata.file_type().is_symlink() {
            if depth == 0 {
                self.skipped += 1;
                self.partial = true;
            }
            return;
        }
        if metadata.is_dir() {
            let relative = path
                .strip_prefix(self.home)
                .unwrap_or(path)
                .to_string_lossy();
            let project = if project.is_empty()
                && !relative.starts_with('.')
                && !relative.starts_with("Library/")
                && [
                    "package.json",
                    "Cargo.toml",
                    "pyproject.toml",
                    ".git",
                    "pubspec.yaml",
                ]
                .iter()
                .any(|f| path.join(f).exists())
            {
                relative.to_string()
            } else {
                project.into()
            };
            let Ok(entries) = fs::read_dir(path) else {
                self.skipped += 1;
                self.partial = true;
                return;
            };
            for entry in entries {
                match entry {
                    Ok(entry) => self.walk(&entry.path(), &project, depth + 1),
                    Err(_) => {
                        self.skipped += 1;
                        self.partial = true;
                    }
                }
                if self.cancel.load(Ordering::Relaxed)
                    || Instant::now() > self.deadline
                    || self.files >= 200_000
                {
                    self.partial = true;
                    break;
                }
            }
        } else if metadata.is_file() {
            // Hardlinks are counted once. APFS cloned extents require additional accounting;
            // these are allocated estimates, never a promise of reclaimable space.
            if !self.seen.insert((metadata.dev(), metadata.ino())) {
                return;
            }
            let bytes = metadata.blocks().saturating_mul(512);
            if bytes >= 10_000_000 {
                self.large_files.push(LargeFile {
                    path: path.to_string_lossy().into(),
                    bytes,
                    identity: file_identity(&metadata),
                    removable: personal_file(self.home, path)
                        && metadata.uid() == unsafe { libc::getuid() },
                });
                self.large_files.sort_by(|a, b| b.bytes.cmp(&a.bytes));
                self.large_files.truncate(20);
            }
            let (category, owner) = classify(path, self.home, project);
            let id = format!("{category}\t{owner}\t{project}");
            let group = self.groups.entry(id.clone()).or_insert(StorageGroup {
                id,
                name: owner.clone(),
                category,
                owner,
                project: project.into(),
                bytes: 0,
                files: 0,
            });
            group.bytes += bytes;
            group.files += 1;
            self.files += 1;
            for rule in RULES {
                if path.starts_with(self.home.join(rule.relative)) {
                    *self.rule_sizes.entry(rule.id).or_default() += bytes;
                }
            }
        }
    }
}
pub fn scan(settings: &Settings, cancel: &AtomicBool) -> Result<StorageReport, String> {
    let home = system::user_home()?;
    let (total, available) = system::disk_space()?;
    let mut warnings = Vec::new();
    let mut roots: Vec<PathBuf> = if settings.scan_paths.is_empty() {
        [
            "Downloads",
            "Documents",
            "Desktop",
            "Pictures",
            "Movies",
            "Music",
            "code",
            "workspace",
            "Library/Caches",
            "Library/Application Support",
            "Applications",
            "Library/Developer",
            ".npm",
            ".yarn",
            ".cache",
            ".cargo",
            ".nvm",
            ".bun",
        ]
        .iter()
        .map(|p| home.join(p))
        .filter(|p| !matches!(fs::symlink_metadata(p), Err(ref error) if error.kind() == std::io::ErrorKind::NotFound))
        .collect()
    } else {
        settings
            .scan_paths
            .iter()
            .filter_map(|p| match valid_root(&home, Path::new(p)) {
                Ok(path) => Some(path),
                Err(error) => {
                    warnings.push(format!("{p}: {error}"));
                    None
                }
            })
            .collect()
    };
    if settings.scan_paths.is_empty()
        && !matches!(fs::symlink_metadata("/Applications"), Err(ref error) if error.kind() == std::io::ErrorKind::NotFound)
    {
        roots.push(PathBuf::from("/Applications"));
    }
    roots.sort_by_key(|p| p.components().count());
    let mut distinct = Vec::<PathBuf>::new();
    for root in roots {
        if !distinct.iter().any(|parent| root.starts_with(parent)) {
            distinct.push(root);
        }
    }
    let mut walker = Walker {
        home: &home,
        cancel,
        deadline: Instant::now() + Duration::from_secs(15),
        seen: HashSet::new(),
        groups: BTreeMap::new(),
        rule_sizes: BTreeMap::new(),
        files: 0,
        skipped: 0,
        partial: !warnings.is_empty(),
        large_files: vec![],
    };
    let overall_deadline = walker.deadline;
    for (index, root) in distinct.iter().enumerate() {
        // Fair-share time across roots so a huge code tree cannot starve app/cache
        // discovery. This is intentionally partial rather than an unbounded crawl.
        let remaining = overall_deadline.saturating_duration_since(Instant::now());
        let share = remaining / (distinct.len() - index) as u32;
        walker.deadline = (Instant::now() + share).min(overall_deadline);
        walker.walk(root, "", 0);
    }
    if walker.skipped > 0 {
        warnings.push(format!(
            "{} paths were unreadable. Grant folder access to improve coverage.",
            walker.skipped
        ));
    }
    if walker.partial {
        warnings
            .push("This is a bounded, partial scan. Unscanned space is not empty space.".into());
    }
    warnings.push("Allocated sizes exclude duplicate hardlinks; APFS clone sharing can still overstate totals. Available-space change is measured after cleanup.".into());
    let candidates = RULES
        .iter()
        .filter_map(|r| {
            let bytes = *walker.rule_sizes.get(r.id)?;
            if bytes == 0 {
                return None;
            }
            Some(Candidate {
                id: r.id.into(),
                name: r.name.into(),
                path: home.join(r.relative).to_string_lossy().into(),
                bytes,
                description: r.description.into(),
                method: r.method.into(),
                executable: {
                    #[cfg(feature = "gui")]
                    {
                        !crate::native::sandboxed()
                    }
                    #[cfg(not(feature = "gui"))]
                    {
                        true
                    }
                },
            })
        })
        .collect();
    let scanned = walker.groups.values().map(|g| g.bytes).sum();
    let mut groups: Vec<_> = walker.groups.into_values().collect();
    groups.sort_by(|a, b| b.bytes.cmp(&a.bytes));
    Ok(StorageReport {
        total_bytes: total,
        available_bytes: available,
        scanned_bytes: scanned,
        file_count: walker.files,
        partial: walker.partial,
        skipped: walker.skipped,
        scanned_at: now(),
        roots: distinct
            .iter()
            .map(|p| p.to_string_lossy().into())
            .collect(),
        groups,
        candidates,
        warnings,
        large_files: walker.large_files,
    })
}
pub fn cleanup(id: &str) -> Result<String, String> {
    #[cfg(feature = "gui")]
    if crate::native::sandboxed() {
        return Err("Command-based cache cleanup is unavailable in this sandbox build. Use the owning tool's supported controls.".into());
    }
    let (program, args): (&str, &[&str]) = match id {
        "npm" => ("npm", &["cache", "clean", "--force"]),
        "uv" => ("uv", &["cache", "prune"]),
        "pip" => ("python3", &["-m", "pip", "cache", "purge"]),
        _ => return Err("Unknown cleanup rule. No files were changed.".into()),
    };
    let processes = crate::processes::sample()?;
    if processes.iter().any(|p| {
        p.pid != std::process::id() as i32
            && (p.name == program
                || p.name.starts_with(&format!("{program} "))
                || (id == "pip" && p.name.contains("pip")))
    }) {
        return Err(format!(
            "{program} is running. Try again when it has finished."
        ));
    }
    let home = system::user_home()?;
    let (query, expected): (&[&str], PathBuf) = match id {
        "npm" => (&["config", "get", "cache"], home.join(".npm")),
        "uv" => (&["cache", "dir"], home.join(".cache/uv")),
        "pip" => (
            &["-m", "pip", "cache", "dir"],
            home.join("Library/Caches/pip"),
        ),
        _ => unreachable!(),
    };
    let actual = system::output(program, query, 8)?;
    let actual = valid_root(&home, Path::new(actual.trim()))?;
    if actual
        != expected
            .canonicalize()
            .map_err(|_| "Cache no longer exists")?
    {
        return Err(
            "The tool uses a custom cache location. Scan and verify that location before cleaning."
                .into(),
        );
    }
    system::output(program, args, 45).map(|text| text.chars().take(1000).collect())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn classification_distinguishes_packages_and_personal_images() {
        let home = Path::new("/Users/test");
        assert_eq!(
            classify(Path::new("/Users/test/.npm/_cacache/image.png"), home, "").0,
            "development"
        );
        assert_eq!(
            classify(Path::new("/Users/test/Pictures/image.png"), home, "").0,
            "images"
        );
    }
    #[test]
    fn unknown_cleanup_is_rejected_without_execution() {
        assert!(cleanup("../../Documents").is_err());
    }
    #[test]
    fn protected_roots_are_rejected() {
        assert!(valid_root(Path::new("/Users"), Path::new("/System")).is_err());
    }
    #[test]
    fn personal_selection_excludes_package_internals_and_tool_data() {
        let home = Path::new("/Users/test");
        assert!(personal_file(
            home,
            Path::new("/Users/test/Downloads/old.zip")
        ));
        assert!(!personal_file(
            home,
            Path::new("/Users/test/Pictures/Photos.photoslibrary/original.jpg")
        ));
        assert!(!personal_file(
            home,
            Path::new("/Users/test/Documents/Backup.sparsebundle/bands/0")
        ));
        assert!(!personal_file(
            home,
            Path::new("/Users/test/.npm/_cacache/file")
        ));
    }
    #[test]
    fn scanner_deduplicates_hardlinks_and_does_not_follow_symlinks() {
        let root = std::env::temp_dir().join(format!(
            "breathing-room-fixture-{}-{}",
            std::process::id(),
            std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_nanos()
        ));
        fs::create_dir(&root).unwrap();
        fs::write(root.join("one.txt"), vec![1_u8; 10_000]).unwrap();
        fs::hard_link(root.join("one.txt"), root.join("copy.txt")).unwrap();
        std::os::unix::fs::symlink("/Users", root.join("outside")).unwrap();
        let cancel = AtomicBool::new(false);
        let mut walker = Walker {
            home: &root,
            cancel: &cancel,
            deadline: Instant::now() + Duration::from_secs(2),
            seen: HashSet::new(),
            groups: BTreeMap::new(),
            rule_sizes: BTreeMap::new(),
            files: 0,
            skipped: 0,
            partial: false,
            large_files: vec![],
        };
        walker.walk(&root, "", 0);
        assert_eq!(walker.files, 1);
        assert!(!walker.partial);
        fs::remove_dir_all(root).unwrap();
    }
}
