#!/usr/bin/env python3
"""Read-only physical-volume inventory using df and du, with explicit gaps."""
import json
import os
from pathlib import Path
import pwd
import subprocess
import sys
import stat
import time

DATA = Path("/System/Volumes/Data")
HOME = Path(pwd.getpwuid(os.getuid()).pw_dir)

def display(path):
    value = str(path)
    return value.removeprefix(str(DATA)) or "/"

def category(path):
    text = display(path)
    lower = text.lower()
    if text.startswith(("/Applications", "/opt", "/usr/local")):
        return "apps", "Applications & installed tools"
    if text.startswith(("/Library", "/private", "/System", "/usr", "/.fseventsd")):
        return "system", "macOS & shared data"
    if any(part in lower for part in ("/code", "/projects", "/workspace", "/.npm", "/.cache", "/.cargo", "/.bun", "/.nvm", "/.yarn", "/.gradle", "/.m2", "/developer")):
        return "development", Path(text).name
    if "/pictures" in lower:
        return "images", "Photos & images"
    if "/movies" in lower:
        return "video", "Movies & video"
    if "/music" in lower:
        return "audio", "Music & audio"
    if "/downloads" in lower:
        return "downloads", "Downloads"
    if "/mobilesync" in lower or "/backup" in lower:
        return "backups", "Backups"
    if "/library/" in lower:
        return "app-data", Path(text).name
    return "documents", Path(text).name

def run():
    df = subprocess.check_output(["/bin/df", "-k", "/", str(DATA)], text=True, timeout=8)
    lines = [line.split() for line in df.splitlines()[1:] if line.strip()]
    total = int(lines[-1][1]) * 1024
    available = int(lines[-1][3]) * 1024
    data_used = int(lines[-1][2]) * 1024
    system_used = int(lines[0][2]) * 1024
    system_volumes = [("macOS system volume", system_used)]
    try:
        info = disk_info(["info", "-plist", str(DATA)])
        containers = disk_info(["apfs", "list", "-plist"])
        container = next(c for c in containers["Containers"] if c["ContainerReference"] == info["APFSContainerReference"])
        total, available = container["CapacityCeiling"], container["CapacityFree"]
        system_volumes = [("macOS " + v["Name"] + " volume", v["CapacityInUse"]) for v in container["Volumes"] if v["DeviceIdentifier"] != info["DeviceIdentifier"]]
    except (OSError, ValueError, KeyError, StopIteration, subprocess.SubprocessError):
        pass
    start = time.monotonic()
    # One traversal, one filesystem: do not scan firmlink aliases or other volumes twice.
    process = subprocess.Popen(["/usr/bin/du", "-k", "-x", "-d", "6", str(DATA)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timed_out = False
    try:
        out, err = process.communicate(timeout=180)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        out, err = process.communicate()
    measured = {}
    large_files = []
    for line in out.decode(errors="replace").splitlines():
        number, separator, path = line.partition("\t")
        if separator and number.isdigit():
            size = int(number) * 1024
            try:
                metadata = os.lstat(path)
                if stat.S_ISDIR(metadata.st_mode):
                    measured[path] = size
                elif stat.S_ISREG(metadata.st_mode) and size >= 100_000_000:
                    large_files.append({"path": display(Path(path)), "bytes": size, "identity": "", "removable": False})
            except OSError:
                pass
    # BSD du cannot combine -a with -d. A separate worker provides a real deadline
    # even when a file-provider folder blocks inside scandir/stat.
    sampled, files_checked, sample_timed_out = sample_large_files(sorted(measured, key=lambda p: measured[p], reverse=True))
    large_files.extend(sampled)
    large_files.sort(key=lambda f: f["bytes"], reverse=True)
    errors = err.decode(errors="replace").splitlines()
    partial_paths = [line.split(": ", 2)[1] for line in errors if line.startswith("du: ") and ": " in line[4:]]
    partial_ancestors = set()
    for denied in partial_paths:
        current = Path(denied)
        while str(current).startswith(str(DATA)):
            partial_ancestors.add(str(current))
            if current == DATA:
                break
            current = current.parent
    def partial(path):
        return timed_out or path in partial_ancestors
    # Non-overlapping accounting frontier: drill into Users/home/Library and apps.
    children_by_parent = {}
    for path in measured:
        children_by_parent.setdefault(os.path.dirname(path), []).append(path)
    for children in children_by_parent.values():
        children.sort(key=lambda p: measured[p], reverse=True)
    groups = []
    def add(path, amount):
        cat, owner = category(Path(path))
        groups.append({"id": path, "name": owner, "category": cat, "owner": owner, "project": "", "bytes": amount, "files": 0})
    def split(path, levels):
        children = children_by_parent.get(path, [])
        amount = measured.get(path, 0)
        if not children or levels <= 0:
            add(path, amount)
            return
        assigned = 0
        for child in children:
            assigned += measured[child]
            split(child, levels - 1)
        if amount > assigned:
            add(path + "/[files in this folder]", amount - assigned)
    for root in sorted(children_by_parent.get(str(DATA), [])):
        split(root, 3 if Path(root).name == "Users" else 1 if Path(root).name in ("Applications", "opt") else 0)
    data_measured = measured.get(str(DATA), sum(g["bytes"] for g in groups))
    identified = min(data_used, sum(g["bytes"] for g in groups)) + sum(size for _, size in system_volumes)
    used = total - available
    remaining = max(0, used - identified)
    for name, size in system_volumes:
        groups.append({"id": "system-volume-" + name, "name": name, "category": "system", "owner": name, "project": "", "bytes": size, "files": 0})
    if remaining:
        groups.append({"id": "unattributed", "name": "Unmapped storage", "category": "unmapped", "owner": "Unmapped storage", "project": "", "bytes": remaining, "files": 0})
    directories = [{"path": display(Path(p)), "name": Path(p).name or "Disk", "bytes": size, "partial": partial(p),
                    "parent": display(Path(p).parent)} for p, size in measured.items() if p != str(DATA)]
    directories.sort(key=lambda d: d["bytes"], reverse=True)
    warnings = [f"Read-only du traversal completed in {time.monotonic() - start:.0f}s. Folder totals are allocated estimates; APFS clones and snapshots can differ from df.",
                "File categorization is based on owning folders; folder totals include all descendant files, including hidden files.",
                f"Large-file discovery sampled {files_checked} entries within 15 seconds; this shortlist is not exhaustive. Browse any folder for its actual files."]
    if errors:
        warnings.append(f"{len(errors)} access errors. Full Disk Access may improve protected-folder coverage.")
        warnings.extend(errors[:15])
    if timed_out:
        warnings.append("Scan reached its 180-second limit; unfinished paths remain unmapped.")
    if sample_timed_out:
        warnings.append("Large-file sampling reached its 15-second limit; measured folder totals are retained.")
    gap = max(0, data_used - min(data_used, data_measured))
    warnings.append(f"Unmapped Data volume bytes: {gap}. Remaining container use includes APFS metadata, snapshots and other volumes; not assumed disposable.")
    return {"totalBytes": total, "availableBytes": available, "scannedBytes": identified, "fileCount": 0,
            "partial": bool(errors) or timed_out, "skipped": len(errors), "scannedAt": int(time.time()),
            "roots": ["/System/Volumes/Data"], "groups": sorted(groups, key=lambda g: g["bytes"], reverse=True),
            "candidates": [], "warnings": warnings, "largeFiles": large_files[:50], "directories": directories,
            "usedBytes": used, "identifiedBytes": identified, "unmappedBytes": remaining,
            "coveragePercent": min(100, identified / max(used, 1) * 100), "inventoryMethod": "df + du + diskutil APFS volumes"}

def disk_info(args):
    raw = subprocess.check_output(["/usr/sbin/diskutil", *args], timeout=8)
    # Native plutil avoids external Python XML-library dependencies.
    result = subprocess.run(["/usr/bin/plutil", "-convert", "json", "-o", "-", "--", "-"], input=raw, capture_output=True, timeout=8, check=True)
    return json.loads(result.stdout)

def sample_large_files(directories):
    worker = subprocess.Popen([sys.executable, "-B", __file__, "large-files"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    timed_out = False
    try:
        out, _ = worker.communicate(input=json.dumps(directories).encode(), timeout=15)
    except subprocess.TimeoutExpired:
        timed_out = True
        worker.kill()
        out, _ = worker.communicate()
    files, checked = [], 0
    for line in out.decode(errors="replace").splitlines():
        try:
            item = json.loads(line)
            if "checked" in item:
                checked = item["checked"]
            elif "path" in item and "bytes" in item:
                files.append(item)
        except (ValueError, TypeError):
            pass
    return files, checked, timed_out

def large_file_rows(directories):
    deadline = time.monotonic() + 15
    checked = 0
    for directory in directories:
        if time.monotonic() >= deadline or checked >= 200000:
            break
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    if time.monotonic() >= deadline or checked >= 200000:
                        break
                    checked += 1
                    if checked % 1000 == 0:
                        yield {"checked": checked}
                    if entry.is_file(follow_symlinks=False):
                        info = entry.stat(follow_symlinks=False)
                        if info.st_blocks * 512 >= 100_000_000:
                            yield {"path": display(Path(entry.path)), "bytes": info.st_blocks * 512, "identity": "", "removable": False}
        except OSError:
            pass
    yield {"checked": checked}

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2 and sys.argv[1] == "large-files":
            for row in large_file_rows(json.load(sys.stdin)):
                print(json.dumps(row), flush=True)
        elif len(sys.argv) == 3 and sys.argv[1] == "browse":
            path = Path(sys.argv[2])
            if not path.is_absolute() or ".." in path.parts:
                raise ValueError("Invalid folder")
            resolved = path.resolve()
            allowed = (str(DATA), "/Users", "/Applications", "/Library", "/private", "/opt", "/usr/local")
            if not any(str(resolved) == p or str(resolved).startswith(p + "/") for p in allowed):
                raise ValueError("Outside inventory roots")
            entries = []
            with os.scandir(path) as children:
                for entry in children:
                    if len(entries) >= 5000:
                        break
                    info = entry.stat(follow_symlinks=False)
                    entries.append({"path": entry.path, "name": entry.name, "directory": stat.S_ISDIR(info.st_mode),
                                    "symlink": stat.S_ISLNK(info.st_mode), "bytes": info.st_blocks * 512,
                                    "logicalBytes": info.st_size})
            print(json.dumps({"path": str(path), "entries": entries, "partial": len(entries) >= 5000}))
        else:
            print(json.dumps(run()))
    except (OSError, ValueError, subprocess.SubprocessError):
        print(json.dumps({"error": "Volume inventory could not complete. Check disk access and retry."}))
