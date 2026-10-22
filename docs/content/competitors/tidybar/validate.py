"""Read-only packet checks. Run from the app repository root; no network or app actions."""
import hashlib
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
packet = json.loads((ROOT / "research.json").read_text())
checks = []


def check(label, passed):
    checks.append(bool(passed))
    print(("PASS " if passed else "FAIL ") + label)


def matches(path, digest):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


check("job/product/canonical ownership", packet["jobId"] == "research-tidybar"
      and packet["productId"] == packet["identity"]["canonicalOwnerId"] == "tidybar")
sources = {s["id"]: s for s in packet["sources"]}
claims = {c["id"] for c in packet["claims"]}
check("claim source references", all(set(c["sourceIds"]) <= sources.keys() for c in packet["claims"]))
check("matrix and figure claim references", all(
    set(row.get(key, [])) <= claims for row in packet["productMatrix"]
    for key in ("tidybarClaimIds", "breathingRoomClaimIds")) and all(
    set(v["supportedClaimIds"]) <= claims for v in packet["visuals"]))
texts = {}
for source in sources.values():
    if "snapshotPath" not in source:
        continue
    path = source["snapshotPath"]
    check("source hash " + source["id"], matches(path, source["sha256"]))
    if path.endswith(".html"):
        parser = VisibleText()
        parser.feed(Path(path).read_text())
        texts[source["id"]] = " ".join(" ".join(parser.parts).split())
    else:
        texts[source["id"]] = " ".join(json.loads(Path(path).read_text())["text"].split())

discovery = packet["discovery"]
check("discovery about-page hash", matches(discovery["snapshotPath"], discovery["sha256"]))
for edge in discovery["edges"]:
    check("edge hash " + edge["seedId"], matches(edge["rawCapture"], edge["sha256"]))
    check("edge contains TidyBar " + edge["seedId"], "tidybar" in Path(edge["rawCapture"]).read_text().lower())

for visual in packet["visuals"]:
    check("original asset hash " + visual["id"], matches(visual["originalPath"], visual["originalSha256"]))
    check("visual reuse/provenance " + visual["id"], visual["reuse"]["status"] == "cleared"
          and bool(visual["caption"]) and bool(visual["alt"]) and not visual["edits"])
    output = subprocess.check_output(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", visual["originalPath"]], text=True)
    dimensions = {key: int(value) for key, value in re.findall(r"(pixelWidth|pixelHeight): (\d+)", output)}
    check("image dimensions " + visual["id"], dimensions == {
        "pixelWidth": visual["widthPx"], "pixelHeight": visual["heightPx"]})

retrievals = json.loads((ROOT / "sources/retrievals.json").read_text())
check("seven successful hashed source/asset retrievals", len(retrievals) == 7 and all(
    r["httpStatus"] == 200 and matches(r["path"], r["sha256"]) for r in retrievals))
for claim in packet["claims"]:
    if not claim["id"].startswith("T"):
        continue
    haystack = " ".join(texts.get(source_id, "") for source_id in claim["sourceIds"])
    excerpt = " ".join(claim["excerpt"].split())
    # The identity quote is a table row, whose pipe is a Markdown rendering delimiter.
    passed = ("Maker" in haystack and "Wirecore GmbH (Germany)" in haystack
              if claim["id"] == "T01" else excerpt in haystack)
    check("supporting excerpt " + claim["id"], passed)

check("bounded drafting, no publication approval", packet["draftingAllowed"] and not packet["published"]
      and not packet["gates"]["criticalResearchBlockers"] and packet["gates"]["score"] is None)
check("briefs and unknowns", bool(packet["briefs"]["workflowArticle"]["interactionPass"])
      and bool(packet["briefs"]["comparison"]["excludedClaims"]) and len(packet["unknowns"]) >= 7)
print(f"SUMMARY {sum(checks)}/{len(checks)} checks passed")
raise SystemExit(0 if all(checks) else 1)
