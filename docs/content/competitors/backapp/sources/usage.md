# Usage

## Installed Apps

When you open BackApp, you see the list of apps discovered under `/Applications` and `~/Applications`. Each row shows the icon, name, path, and version. Badges mark App Store and iPhone (Designed for iPhone) apps.

The trailing **inspector** has categories (with counts) and source filters.

![Main window](screenshots/1-main.png)

### Filters

| Filter | Meaning |
|--------|---------|
| **App Store** | Apps with an App Store receipt |
| **iPhone** | iOS / Designed for iPhone apps |
| **System** | Include `/System/Applications` (default **off** — turning it on rescans) |
| **Other** | Everything else (not System / iPhone / App Store) |
| **Updates Available** | Apps where a newer App Store version is known from cache |

![Categories and filters](screenshots/2-filters.png)

Use **Clear All Filters** to reset toggles and category selection. Search (`⌘F`) filters by name, bundle ID, or version.

!!! tip "Sidebar"
    The left sidebar (Installed Apps + snapshots) appears only after you have at least one snapshot. Until then the window is list + inspector only.

### Toolbar

| Control | Action |
|---------|--------|
| Create snapshot (`camera.viewfinder`) | Capture the current list |
| Import (`tray.and.arrow.down`) | Import a snapshot JSON file |
| Refresh (`⌘R`) | Rescan installed apps |

## Create a snapshot

Choose **Create snapshot** or **File → New Snapshot…** (`⌘N`). Name the snapshot and review counts by source and category, then **Create**.

![Create Snapshot](screenshots/3-snapshot.png)

Snapshots are stored locally as JSON. The sidebar lists them with date, device name, and app count.

## Compare to a snapshot

Select a snapshot in the sidebar. The detail list shows each app from the snapshot compared to what’s on this Mac:

- **Same version** — installed and matches
- **Not installed** — missing on this Mac
- **Different version** — installed, but version differs (newer/older indicators when comparable)

Status filters in the inspector let you focus on one of these groups. Source and category filters work here too.

![Snapshot compare](screenshots/4-snapshot-compare.png)

Toolbar on a snapshot: **Export**, **Delete**, **Refresh** (rescans the machine for comparison).

## App detail

Click an installed app (or a snapshot row that still exists on this Mac) to open detail.

### Without App Store data

Non–App Store apps show local metadata: provider, bundle ID, version, path, compatibility.

![App detail without App Store](screenshots/5-app-detail.png)

### With App Store data

When lookup succeeds: developer, category, versions, release date, What’s New, and preview screenshots. Use **View in App Store** to open the store page. **Refresh** (`⌘R` on this screen) re-fetches App Store info for this app.

![App detail with App Store](screenshots/6-appstore-details.png)

## Export and import

**Export** (`⌘⇧E` when a snapshot is selected, or the export toolbar button) opens a Save panel and writes a JSON file (for example `snapshot-24 Aug 2026.json`).

![Export snapshot](screenshots/7-export-import.png)

**Import** (`⌘⇧I` or the import toolbar button) opens a file picker, shows a preview sheet (name, stats, device), then adds the snapshot with a new ID so it never overwrites an existing one.

Share export files with another Mac or keep them as backups of your app set.

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| `⌘N` | New Snapshot… |
| `⌘⇧I` | Import Snapshot… |
| `⌘⇧E` | Export Snapshot… |
| `⌘⌫` | Delete Snapshot |
| `⌘R` | Refresh (list / snapshot compare, or App Store on app detail) |
| `⌘F` | Focus search |
| `⌘1` | Go to Installed Apps |

Also: **BackApp → About BackApp** for version, author, and the GitHub link.

## About

**BackApp → About BackApp** opens a small window with the app icon, version, author (Markus Lind), repository link, and copyright.
