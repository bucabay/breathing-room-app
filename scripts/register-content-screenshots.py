#!/usr/bin/env python3
"""Register already captured and visually reviewed current browser-preview files."""
import datetime
import hashlib
import json
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "docs/content/screenshots.json"
VIEWS = {
    "home": "Home overview",
    "space": "Space",
    "apps": "Apps",
    "daily-care": "Daily care",
    "activity": "Activity",
    "assistant-review": "Assistant plan review",
    "activity-panel": "Menu bar",
}


def main():
    data = json.loads(PATH.read_text())
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    for slug, view in VIEWS.items():
        path = ROOT / f"docs/content/assets/breathing-room/{slug}-preview-2026-10-21.png"
        raw = path.read_bytes()
        width, height = struct.unpack(">II", raw[16:24])
        captured = datetime.datetime.fromtimestamp(path.stat().st_mtime, datetime.timezone.utc).isoformat()
        record = {
            "id": f"current-{slug}-browser-preview", "sourcePath": str(path), "view": view,
            "kind": "browser-preview", "dataOrigin": "illustrative-example-data", "actualNativeScan": False,
            "capturedOn": captured, "reviewedOn": "2026-10-21", "currentness": "verified-current-source-render",
            "sourceCommit": head, "sourceUrl": "http://127.0.0.1:1431/" + ("?panel=activity" if slug == "activity-panel" else ""),
            "reuseStatus": "first-party-example-ui-with-required-disclosure", "width": width, "height": height,
            "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "alt": f"Breathing Room {view} view rendered in a browser with illustrative example data.",
            "caption": f"Current-source Breathing Room {view} browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.",
            "privacyReview": {"status": "reviewed", "diagnostic": "Only built-in example names and paths; no real account, local inventory or personal files captured."},
            "reuseBasis": "App-owner-requested first-party UI capture; third-party app marks remain their owners' marks, no endorsement or blanket trademark licence inferred.",
            "edits": [],
            "visualReview": "Opened and read the actual PNG using the image-capable read tool; capture and disclosure text inspected, not inferred from file existence.",
            "limitations": ["Browser-only current source, not a distributed-release or native macOS behavior test.", "Floating assistant composer is part of the real UI and can overlap content in full-page captures; use contextual figures, not measurement evidence."],
        }
        if slug == "assistant-review":
            record["limitations"].append("Focused view hides the global preview banner; the preceding in-app answer visibly states interactive preview / no Mac inspection. Keep that disclosure and the caption; no approval button was clicked.")
        if slug == "activity-panel":
            record["caption"] = "Breathing Room Activity panel rendered in a browser with visible Example activity label. This is not a native macOS menu-bar screenshot or native interaction test."
            record["limitations"].append("Activity panel browser route only; native menu-bar placement/pinning remains unverified.")
        data["assets"] = [a for a in data["assets"] if a["id"] != record["id"]] + [record]
        for required in data["requiredViews"]:
            if required["view"] == view:
                required.update(status="verified-browser-preview", currentAssetId=record["id"], diagnostic=record["caption"])
    data["status"] = "done-browser-preview-scope"
    data["reusePolicy"]["rules"] = [rule for rule in data["reusePolicy"]["rules"] if "no assets were copied" not in rule.lower()]
    data["reusePolicy"]["rules"].append("Current browser captures can illustrate the current-source UI with explicit example-data captions; never represent them as native measurements.")
    data["inspection"].update(newCaptures=7, nativeTestingPerformed=False, cleanupPerformed=False)
    data["inspection"]["browserRecovery"] = "Existing authorized Chrome profile9333 restored; owned tab used against an owned app Vite preview on1431, existing user server1430 untouched. No cleanup approval, daily settings save, native scan, installation or external AI call performed."
    data["completionGate"] = {"requiredCurrentViews": 6, "verifiedCurrentViews": 6, "scope": "Current browser-preview illustrations only", "diagnostic": "All six view captures inspected, with explicit example-data/native limitations. Native menu-bar behavior remains unverified and cannot be claimed.", "nextStep": "Independent per-article visual/provenance review remains required; choose readable contextual crops while retaining disclosure."}
    PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print("Registered seven current-source browser previews; six required view illustrations covered; no native testing claimed.")


if __name__ == "__main__":
    main()
