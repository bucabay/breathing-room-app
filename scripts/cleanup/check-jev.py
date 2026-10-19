#!/usr/bin/env python3
"""Explicit live API check using synthetic metadata, no real file reads/deletion."""
from cleanup import assess, home_dir
import json

home = home_dir()
plan = {"candidates": [
    {"ruleId": "npm", "name": "npm package downloads", "path": str(home / ".npm/_cacache"), "bytes": 200000000,
     "evidence": "Synthetic fixture: npm config confirms this location; complete inventory contains only downloaded package blobs, no credentials/symlinks/tracked files.",
     "impact": "Permanent supported-tool cache removal; packages download again.", "executable": True, "complete": True,
     "reason": "", "adapter": "tool-cache.py", "impactLevel": 2, "judgment": None},
    {"ruleId": "unknown", "name": "My original recordings", "path": str(home / "Documents/recordings"), "bytes": 500000000,
     "evidence": "Synthetic fixture: original personal audio files; no backup or reproducibility evidence.",
     "impact": "Unique recordings, not generated cache.", "executable": False, "complete": True, "reason": "Originals",
     "adapter": "inspect-only.py", "impactLevel": 5, "judgment": None}
]}
result = assess(plan, "Find reproducible cache files, preserve personal originals", home)
print(json.dumps({"mode": result["mode"], "usage": result.get("usage"), "results": [
    {"fixture": c["name"], "executable": c["executable"], "impact": c["impactLevel"], "judgment": c["judgment"]}
    for c in result["candidates"]]}, indent=2))
