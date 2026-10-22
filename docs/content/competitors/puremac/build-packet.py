"""Assemble this job's documentary packet from retained public evidence; no network."""
import datetime
import hashlib
import json
from pathlib import Path
import struct

APP = Path(__file__).resolve().parents[4]
ROOT = Path(__file__).resolve().parent
def load(p):
    return json.loads(p.read_text())
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
baseline = next(r for r in load(APP / 'docs/content/verification/batch-2.json')['records'] if r['id'] == 'puremac')
directory = APP / baseline['discovery']['rawCapture']
official = APP / baseline['sources'][0]['rawCapture']
assert digest(directory) == baseline['discovery']['sha256']
assert digest(official) == baseline['sources'][0]['sha256']
source_text = load(official)['text']
sources = [{'id': 'baseline', 'publisher': 'PureMac / momenbasel on GitHub', **baseline['sources'][0]},
           {'id': 'discovery', 'publisher': 'AlternativeTo', **baseline['discovery']}]
for name in ['latest-release', 'license', 'project', 'homepage', 'screenshots-tree', 'commit', 'cleaning-engine', 'image-license', 'space-explorer']:
    meta = load(ROOT / 'sources' / (name + '.meta.json'))
    assert digest(APP / meta['path']) == meta['sha256']
    sources.append({'id': name, 'publisher': 'PureMac project', **meta})
sources.append({'id': 'br-register', 'publisher': 'Breathing Room', 'path': 'docs/content/capabilities.md', 'checkedOn': '2026-10-21', 'sha256': digest(APP / 'docs/content/capabilities.md'), 'scope': 'Reused source/published verification; not native runtime certification.'})
claims = []
def claim(id, wording, source, excerpt, scope='Current repository documentation; not independently executed.', state='verified'):
    if source == 'baseline':
        assert excerpt in source_text, (id, excerpt)
    else:
        paths = {'latest-release': 'latest-release.txt', 'project': 'project.txt', 'homepage': 'homepage.txt', 'license': 'license.txt', 'cleaning-engine': 'cleaning-engine.txt'}
        if source in paths:
            assert excerpt in (ROOT / 'sources' / paths[source]).read_text(), (id, excerpt)
        elif source == 'br-register':
            assert excerpt in (APP / 'docs/content/capabilities.md').read_text(), (id, excerpt)
    s = next(s for s in sources if s['id'] == source)
    claims.append({'id': id, 'wording': wording, 'state': state, 'sourceIds': [source], 'sourceUrl': s.get('url', s.get('sourceUrl', 'https://breathing-room.chatic.ai/')), 'excerpt': excerpt, 'checkedAt': s.get('retrievedAtUtc', s.get('retrievedAt', s.get('checkedOn'))), 'evidenceClass': 'source-inspected' if source == 'cleaning-engine' else 'documented-not-tested', 'scope': scope, 'location': 'workflow article / comparison matrix', 'reviewer': 'research-puremac worker'})
claim('identity', 'PureMac is the Mac-care project maintained at momenbasel/PureMac.', 'baseline', 'Free, open-source Mac care: cleanup, app management, storage exploration, and system checks. No subscription or telemetry.')
claim('free', 'PureMac is advertised as free, with no subscription, trial or account.', 'baseline', 'No subscription, no trial, no account.', 'Advertised core offer; no checkout, install or account testing. No currency conversion needed for a free offer.')
claim('license', 'The repository uses the MIT licence; preserve its copyright and permission notice on redistribution.', 'license', 'The above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.')
claim('platform', 'Source configuration targets macOS 13.0, arm64 and x86_64; current source version 3.1.0, build 30.', 'project', 'MARKETING_VERSION: "3.1.0"', 'Also MACOSX_DEPLOYMENT_TARGET 13.0, ARCHS arm64 x86_64 and CURRENT_PROJECT_VERSION 30 in the retained configuration. Not Windows/Linux support or runtime certification.')
claim('release', 'Latest stable GitHub API result is v3.1.0, published 2026-10-08; release offers DMG and ZIP.', 'latest-release', 'PureMac 3.1.0', 'API tag_name, published_at and assets fields retained. Installers were not downloaded or tested.')
claim('signing', 'The v3.1.0 release describes a universal binary signed with Developer ID, notarized and stapled by Apple.', 'latest-release', 'Universal binary (Intel + Apple Silicon). Signed with Developer ID + notarized + stapled by Apple.', 'Vendor release disclosure, not our binary-signature inspection. Source project Apple Development identity is a build setting, not contradiction of distribution signing.')
claim('install', 'Repository offers Homebrew and a release DMG for installation in /Applications.', 'baseline', 'brew install --cask puremac', 'Release notes use the qualified momenbasel/tap/puremac cask. Do not promise either command was executed or Gatekeeper always permits launch.')
claim('removal', 'Deletion method depends on workflow: user-level app, orphan and exact-duplicate removal use Trash; category, scheduled, admin and other documented cleanup can permanently delete.', 'baseline', 'App uninstalls, orphan removal, and exact-duplicate removal use the Trash at user level.', 'Read the following permanent-delete list in Our promise. Never generalize Trash recovery or per-run approval to all modes.')
claim('permanent-source', 'The inspected CleaningEngine has a removeItem path outside its special managed-DerivedData Trash branch.', 'cleaning-engine', 'try fileManager.removeItem(at: itemURL)', 'Pinned commit, lines 165–209. Source inspection only; no deletion executed.')
claim('approvals', 'Manual destructive workflows require confirmation; scheduled auto-clean is unattended after enablement.', 'baseline', 'Scheduled auto-clean remains unattended after enablement.')
claim('space', 'Space Explorer measures allocated space in a selected folder, supports drill-down and Finder reveal, and reports skipped/inaccessible items.', 'baseline', 'measures the allocated space inside a folder you choose.')
claim('developer', 'Documented cleanup includes Xcode, Homebrew, npm, Yarn classic, pnpm and Docker categories.', 'baseline', 'Node Cache\n- npm, yarn classic, pnpm content-addressable store', 'Categories have different removal consequences; do not imply every artifact is disposable. Xcode runtimes and MCP DerivedData are opt-in, with documented exceptions.')
claim('helpers', 'Performance documents live app/process CPU and memory with helper grouping.', 'baseline', 'with live app/process usage, app icons, sorting, search and helper grouping.', 'Do not claim Breathing Room uniquely groups helpers. Resident memory can double-count shared pages; CPU uses total machine capacity.')
claim('offline', 'Local scans/cleanup are documented to work offline; Homebrew update checking/installing requires a network connection.', 'baseline', 'Local scans and cleanup work offline. Checking for or installing Homebrew app updates requires a network connection.', 'No-telemetry is a vendor statement, not an independently audited network finding. Release checks also contact GitHub.')
claim('permissions', 'Without Full Disk Access, some categories and app-container scans are incomplete.', 'baseline', 'Without it, some cleanup categories and app-container scans will be incomplete.')
claim('visual', 'Repository says screenshots show the running macOS app; file-tool images use sample files/images.', 'baseline', 'Screenshots show the running macOS app. File tools use sample files and images.', 'Actual screenshot capture time, OS and exact app build are not supplied.')
claim('protection', 'Protection is documented as a configuration audit, not an antivirus or malware scanner.', 'baseline', 'This is a configuration audit, not an antivirus or malware scanner.')
claim('homepage-alias', 'Official homepage structured data gives PureMac Cleaner as an alternate name.', 'homepage', '"alternateName": "PureMac Cleaner"', 'Alias within this project, not evidence connecting it to PowerMyMac.')
claim('br-preview', 'Breathing Room is a free Apache-2.0 macOS maintenance preview; current identified release 0.1.0-preview.1, macOS 13+, Python 3.10+ prerequisite.', 'br-register', 'Breathing Room is a free, Apache-2.0 macOS maintenance **preview**', 'Reuse capabilities.md dated October 21; sections Current identified version, Python, License. Not native binary parity certification.')
claim('br-caveats', 'Breathing Room preview is Apple Development signed, not Developer ID signed or notarized; clean-machine and physical Intel validation are incomplete.', 'br-register', 'Apple Development signed, not Developer ID signed or notarized', 'Release disclosure retained in capabilities.md; no installation recommendation without these limitations.')
claim('br-pricing', 'Breathing Room local core is advertised free; optional AI Care is $5 USD/month or $50 USD/year, renewing until cancelled with applicable tax at checkout.', 'br-register', '$5 USD/month', 'capabilities.md Pricing/access rows; paid entitlement enforcement and exact allowances remain unverified.')
claim('br-hosted', 'Breathing Room hosted assistance requires authentication/internet and can send relevant paths, process and storage context to the service.', 'br-register', 'Hosted AI assistance requires internet access and authentication', 'capabilities.md Local versus hosted boundary; do not claim fully offline AI or all data stays on device.')
claim('br-workflow', 'Breathing Room source supports storage views, grouped processes, local activity history and daily care tied to saved exact approvals while the app runs.', 'br-register', 'Saved approvals bind account, API origin, action method/path and native rule', 'capabilities.md matrix and approval exceptions: optional verified Ruff-cache automatic Trash mode must be disclosed; not blanket per-item prompting.')
commit = load(ROOT / 'sources/commit.txt')['sha']
image_meta = load(ROOT / 'sources/space-explorer.meta.json')
image_path = APP / image_meta['path']
width, height = struct.unpack('>II', image_path.read_bytes()[16:24])
br = next(a for a in load(APP / 'docs/content/screenshots.json')['assets'] if a['id'] == 'current-space-browser-preview')
assert digest(Path(br['sourcePath'])) == br['sha256']
visuals = [{
    'id': 'puremac-space-explorer', 'productId': 'puremac', 'view': 'Space Explorer', 'kind': 'official-asset',
    'sourcePageUrl': f'https://github.com/momenbasel/PureMac/blob/{commit}/screenshots/space-explorer.png',
    'assetUrl': image_meta['url'], 'capturedAtUtc': None, 'retrievedAtUtc': image_meta['retrievedAtUtc'],
    'capturedBy': None, 'productVersion': None, 'buildOrCommit': commit, 'osVersion': None,
    'dataMode': 'vendor-illustration', 'originalPath': image_meta['path'], 'originalSha256': image_meta['sha256'],
    'publishedPath': None, 'publishedSha256': None, 'widthPx': width, 'heightPx': height, 'edits': [],
    'privacyReview': {'status': 'reviewed', 'redactions': [], 'notes': 'Visible /tmp/PureMac Samples/Projects and sample .bin filenames; no personal account visible.'},
    'reuse': {'status': 'cleared', 'basis': 'Repository MIT covers software and associated documentation; this screenshot is a tracked documentation asset. Preserve complete copyright/permission notice. No trademark endorsement implied.', 'evidenceUrlOrPath': 'sources/image-license.txt', 'credit': 'PureMac Contributors, MIT License; official repository screenshot.'},
    'caption': 'PureMac Space Explorer, official running-app screenshot using sample files. Allocated-space figures are vendor sample data, not our measurements. Source: PureMac Contributors (MIT).',
    'alt': 'PureMac Space Explorer showing two sample design-asset files, allocated folder size and skipped/inaccessible counters.',
    'supportedClaimIds': ['space', 'visual'], 'limitations': ['Vendor capture date, OS and exact screenshot version unknown; commit pins the asset, not the running app build.', 'Publication must include retained MIT notice and independent target-page review.'],
    'review': {'status': 'research-visual-inspection-complete', 'reviewer': 'research-puremac worker', 'notes': 'Actual PNG opened with image-capable read tool; not inferred from dimensions.'}
}, {'id': br['id'], 'productId': 'breathing-room', 'view': 'Space', 'kind': 'browser-preview',
    'sourcePageUrl': br['sourceUrl'], 'assetUrl': None, 'capturedAtUtc': br['capturedOn'], 'retrievedAtUtc': None,
    'capturedBy': 'screenshot-library job', 'productVersion': None, 'buildOrCommit': br['sourceCommit'], 'osVersion': None,
    'dataMode': 'example', 'originalPath': br['sourcePath'], 'originalSha256': br['sha256'], 'publishedPath': None, 'publishedSha256': None,
    'widthPx': br['width'], 'heightPx': br['height'], 'edits': [], 'privacyReview': br['privacyReview'],
    'reuse': {'status': 'cleared', 'basis': br['reuseBasis'], 'evidenceUrlOrPath': 'docs/content/screenshots.json', 'credit': 'Breathing Room; first-party browser preview.'},
    'caption': br['caption'], 'alt': br['alt'], 'supportedClaimIds': ['br-workflow'],
    'limitations': br['limitations'] + ['Retain visible Interactive preview / example data banner; full-height figure needs contextual responsive treatment.'],
    'review': {'status': 'research-visual-inspection-complete', 'reviewer': 'research-puremac worker', 'notes': 'Actual image opened and read again in this job. Independent rendered-page review still pending.'}}]
record = next(r for r in load(APP / 'docs/content/competitors.json')['competitors'] if r['id'] == 'puremac') if isinstance(load(APP / 'docs/content/competitors.json'), dict) and 'competitors' in load(APP / 'docs/content/competitors.json') else None
packet = {'schemaVersion': 1, 'jobId': 'research-puremac', 'status': 'research-complete', 'publicationStatus': 'not-approved', 'assembledAtUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'identity': {'id': 'puremac', 'officialName': 'PureMac', 'canonicalOwnerId': 'puremac', 'officialHomepage': 'https://www.moamenbasel.com/PureMac/', 'officialRepository': 'https://github.com/momenbasel/PureMac', 'maintainer': 'momenbasel / Moamen Basel', 'aliases': ['PureMac Cleaner'], 'aliasSkipDecision': {'skip': False, 'reason': 'Verified independent repository identity; homepage alternateName belongs to same PureMac owner. PowerMyMac baseline resolves to TechyCub, not this project; no basis to merge or create a separate PureMac Cleaner article.'}, 'classification': 'direct-overlapping-mac-maintenance', 'fit': 'Mac storage review and cleanup overlap directly; capabilities and approval models differ. Not Windows/Linux software.'},
    'discovery': {**baseline['discovery'], 'edges': record['edges'] if record else [], 'pagination': 'Retained manifest edge URLs identify seed pages; no more-specific pagination is asserted.', 'reuse': 'Existing baseline hashes checked, not refetched.'},
    'sources': sources, 'claims': claims, 'visuals': visuals,
    'productMatrix': {'macOS': ['platform', 'release'], 'license': ['license'], 'pricing': ['free'], 'localHosted': ['offline'], 'scanModel': ['space', 'developer'], 'approvalControls': ['removal', 'approvals', 'permanent-source'], 'helperGrouping': ['helpers'], 'recurringGrowth': 'not verified; scheduled cleanup does not establish growth attribution/history', 'developerCaches': ['developer'], 'runtimeInstall': ['install', 'signing', 'permissions']},
    'conflicts': [{'topic': 'Homepage blanket Trash-only / no network claims', 'sources': ['homepage', 'baseline', 'cleaning-engine'], 'resolution': 'Reject blanket homepage wording. Retained repository describes workflow-specific permanent deletion and networked Homebrew/GitHub checks; pinned CleaningEngine confirms removeItem. Use only scoped repository claims. No generic safety, complete recoverability or never-network claim is draftable.', 'status': 'resolved-for-bounded-comparison'}],
    'unknowns': ['Independent binary signing/notarization and install/runtime results', 'Feature parity of all main-branch documentation with v3.1.0 binary', 'Screenshot capture date, exact app build and OS', 'PureMac recurring-growth history/attribution, hosted AI behavior and other unlisted features: not verified, never No', 'Breathing Room exact hosted AI allowance/paid gating and release feature parity'],
    'briefs': {'workflow': {'title': 'Inspect allocated folder space before choosing a Mac cleanup method', 'slug': 'inspect-folder-space-before-mac-cleanup', 'intent': 'Use PureMac Space Explorer to separate a folder-size inspection from a later destructive workflow; understand sample size versus recoverable space.', 'track': 'search-reference', 'outline': ['Inspect the selected folder and access limits', 'Allocated bytes are not promised free-space gains', 'Choose the specific removal workflow, not a blanket Trash assumption', 'Decide whether manual inspection or recurring investigation fits'], 'interaction': 'A non-mutating decision checklist: inspect only / app or duplicate removal / category cleanup / scheduled cleanup. Show method, confirmation and permanent-deletion caveats; no fake scanner or predicted savings.'},
    'comparison': {'title': 'Breathing Room vs PureMac: reviewable care or a free native toolkit', 'slug': 'puremac', 'intent': 'Concise product choice, not a second expanded workflow essay.', 'rows': ['macOS/release and runtime', 'local inspection versus hosted assistance', 'cleanup method and approval boundaries', 'storage and grouped processes', 'scheduled cleanup versus saved exact approvals', 'price and installation limitations'], 'disclosure': 'Breathing Room, which we build.', 'links': ['/comparisons/', '/blog/inspect-folder-space-before-mac-cleanup/', '/tools/']}},
    'advantagesAndTradeoffs': {'puremac': ['Free MIT native toolkit with documented uninstaller, duplicate review and configuration audit; do not claim Breathing Room implements equivalent tools.', 'Vendor-disclosed signed/notarized stable release, unlike Breathing Room preview disclosures; not our binary audit.', 'Local scans documented offline; category/scheduled cleanup may permanently delete and unattended scheduling needs deliberate selection.'], 'breathingRoom': ['Source-evidenced activity history and hosted investigation may suit recurring questions; PureMac absence not established.', 'Saved exact approvals constrain daily care; optional interactive Ruff automatic Trash exception must remain explicit.', 'Preview, Python prerequisite, incomplete native QA and non-notarized distribution are material costs; hosted AI requires authentication/internet and optional paid AI Care.']},
    'gates': {'drafting': 'ready-for-bounded-documentary-draft', 'criticalResearchBlockers': [], 'independentReview': 'pending', 'nativeTesting': 'not-performed', 'websiteChanged': False, 'publication': 'blocked-until-draft-site-and-independent-review', 'restrictions': ['Do not recommend guaranteed safety/recovery/speed/savings.', 'Keep all eventual content draft/unpublished.', 'Do not copy vendor comparison-table claims about other products.']}}
(ROOT / 'research.json').write_text(json.dumps(packet, indent=2) + '\n')
print(f'Wrote research.json: {len(claims)} claims, {len(sources)} sources, {len(visuals)} inspected visuals')
