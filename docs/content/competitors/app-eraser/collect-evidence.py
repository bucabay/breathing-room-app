"""Read-only public-source collection; never executes downloaded product code."""
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
COMMIT = "1b801bb3db4de54233d788e5f5866ce4f30f5da4"
SOURCES = {
    "controller": f"https://raw.githubusercontent.com/davunt/app-eraser/{COMMIT}/src/main/controller.js",
    "view": f"https://raw.githubusercontent.com/davunt/app-eraser/{COMMIT}/src/main/index.js",
    "locations": f"https://raw.githubusercontent.com/davunt/app-eraser/{COMMIT}/utils/pathLocations.js",
}

def collect(item):
    key, url = item
    try:
        with urllib.request.urlopen(url, timeout=40) as response:
            body = response.read()
            result = {"id": key, "url": url, "finalUrl": response.url,
                      "status": response.status, "retrievedAtUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      "sha256": hashlib.sha256(body).hexdigest(), "text": body.decode()}
    except Exception as error:
        result = {"id": key, "url": url, "error": str(error)}
    target = ROOT / "sources" / f"{key}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2) + "\n")
    return result

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(collect, SOURCES.items()):
            print(json.dumps(result, indent=2))
