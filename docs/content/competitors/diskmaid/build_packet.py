"""Assemble the owned evidence packet from retained sources, without network access."""
import hashlib
import json
from pathlib import Path
from html.parser import HTMLParser

APP = Path(__file__).resolve().parents[4]
ROOT = Path(__file__).resolve().parent
DATE = '2026-10-21'
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):
    return str(p.relative_to(APP))
def load(p):
    return json.loads(p.read_text())
batch = load(APP / 'docs/content/verification/batch-1.json')
def find_product(x):
    if isinstance(x, dict):
        if x.get('id') == 'diskmaid' and 'facts' in x:
            return x
        for v in x.values():
            r = find_product(v)
            if r: return r
    if isinstance(x, list):
        for v in x:
            r = find_product(v)
            if r: return r
record = find_product(batch)
assert record
competitor_manifest = load(APP / 'docs/content/competitors.json')
def find_edges(x):
    if isinstance(x, dict):
        if x.get('id') == 'diskmaid' and 'edges' in x: return x['edges']
        for v in x.values():
            r = find_edges(v)
            if r: return r
    if isinstance(x, list):
        for v in x:
            r = find_edges(v)
            if r: return r
edges = find_edges(competitor_manifest)
assert edges
official_path = APP / record['sources'][0]['snapshotPath']
official = load(official_path)
discovery_path = APP / record['discovery']['snapshotPath']
app_path = ROOT / 'sources/app-store.html'
app_html = app_path.read_text()
manifest = load(ROOT / 'sources/manifest.json')
store = next(s for s in manifest if s['id'] == 'app-store')
sources = [
    {'id': 'discovery', 'url': record['discovery']['sourceUrl'], 'finalUrl': record['discovery']['sourceUrl'], 'retrievedAtUtc': record['discovery']['retrievedAt'], 'snapshotPath': rel(discovery_path), 'sha256': digest(discovery_path), 'publisher': 'AlternativeTo', 'use': 'Discovery only; Free tag does not establish free full functionality.'},
    {'id': 'official', 'url': record['officialUrl'], 'finalUrl': record['officialFinalUrl'], 'retrievedAtUtc': official['retrievedAt'], 'snapshotPath': rel(official_path), 'sha256': digest(official_path), 'publisher': 'Nalarin', 'use': 'Reused current batch-1 record; vendor-documented capabilities, not measured results.'},
    {**store, 'snapshotPath': rel(app_path), 'publisher': 'Apple App Store / Nalarin', 'scope': 'US storefront; version 1.6 dated 2026-06-01'},
    {'id': 'terms', 'url': 'https://nalarin.com/mymacmaid/terms', 'finalUrl': 'https://nalarin.com/mymacmaid/terms', 'checkedOn': DATE, 'retrievedAtUtc': None, 'method': 'Successful WebFetch text; exact tool retrieval clock not provided. urllib retention request returned 403.', 'publisher': 'Nalarin', 'publishedOrUpdatedOn': '2026-02-09'},
    {'id': 'privacy', 'url': 'https://nalarin.com/mymacmaid/privacy', 'finalUrl': 'https://nalarin.com/mymacmaid/privacy', 'checkedOn': DATE, 'retrievedAtUtc': None, 'method': 'Successful WebFetch text; exact tool retrieval clock not provided. urllib retention request returned 403.', 'publisher': 'Nalarin', 'publishedOrUpdatedOn': '2026-02-09'},
    {'id': 'br-capabilities', 'url': 'https://breathing-room.chatic.ai/', 'snapshotPath': 'docs/content/capabilities.md', 'sha256': digest(APP / 'docs/content/capabilities.md'), 'checkedOn': DATE, 'method': 'Reuse same-day source and live-page verification register; no repeated public fetch.', 'publisher': 'Breathing Room'},
    {'id': 'br-screenshots', 'url': 'http://127.0.0.1:1431/', 'snapshotPath': 'docs/content/screenshots.json', 'sha256': digest(APP / 'docs/content/screenshots.json'), 'checkedOn': DATE, 'publisher': 'Breathing Room', 'scope': 'Current-source browser preview, not native release evidence'},
]
claims = []
def claim(id, wording, source, excerpt, scope, state='verified', location='comparison matrix / workflow'):
    s = next(s for s in sources if s['id'] == source)
    claims.append({'id': id, 'wording': wording, 'sourceIds': [source], 'sourceUrl': s['url'], 'excerpt': excerpt, 'checkedOn': DATE, 'evidenceClass': 'documented-not-hands-on', 'scopeAndConditions': scope, 'state': state, 'intendedLocation': location, 'reviewer': 'research-diskmaid worker; independent review pending'})
claim('identity', 'DiskMaid is Nalarin’s Mac storage-cleanup app; its linked App Store name is DiskMaid: Clean Your Computer.', 'app-store', 'DiskMaid: Clean Your Computer', 'Homepage snapshot links App Store ID 6758129723; store developer Nalarin, seller PT KERJA AKAL DIGITAL. No installation performed.')
claim('platform-version', 'The US listing shows version 1.6, dated June 1, 2026, requiring macOS 14.6 or later.', 'app-store', 'Requires macOS 14.6 or later.', 'Version/date confirmed from HTML Version 1.6 and time datetime=2026-06-01. Architecture compatibility not established; no Windows support inferred.')
claim('price', 'Free download with a Lifetime in-app purchase listed at $19.99 in the US storefront; the description says all described features require a one-time purchase.', 'app-store', 'All features described above requires one time purchase', 'HTML In-App Purchases: Lifetime / $19.99. US dollar storefront display, not a checkout/tax/refund or entitlement test. Do not call the full cleaner free.')
claim('license', 'The published terms grant a personal, non-exclusive, non-transferable licence on macOS devices.', 'terms', 'We grant you a personal, non-exclusive, non-transferable license to use DiskMaid on your macOS devices in accordance with these terms.', 'Commercial licence terms; no open-source licence or public repository verified.')
claim('scan', 'Nalarin documents Smart Scan for user caches, log files, local/external Trash and browser history/cache.', 'official', 'User caches & log files\nLocal & external trash bins\nBrowser history & cache', 'Vendor documentation, not tested removability, coverage, safety or speed.')
claim('large-files', 'DiskMaid documents large/old file discovery and preview before deleting.', 'official', 'Visual file size breakdown\nFind forgotten movies & installers\nPreview before deleting', 'Large/old does not mean expendable; no workflow executed.')
claim('duplicates', 'DiskMaid documents exact-duplicate detection using multi-stage hashing and smart selection.', 'official', 'Our precise hashing algorithm\n                        finds exact duplicates, even with different filenames.', 'Vendor claim; no independent hash/collision, selection or recovery test. Do not equate duplicate bytes with disposable copies.')
claim('uninstaller', 'DiskMaid documents app removal and searching for support files, preferences and caches left behind.', 'official', 'Complete app removal\nDeep library folder scan\nClean zombie app data', 'Not proof of complete removal for every app or privileged location.')
claim('approval', 'Nalarin says DiskMaid shows what will be deleted before deletion.', 'official', 'We show you exactly what will be deleted before it happens.', 'Vendor control claim, not proof of exact-method approval, Trash behavior or scheduled authority.')
claim('history', 'The website labels an Activity History view as tracking and undoing past cleanups.', 'official', 'Activity History\nTrack and undo past cleanups', 'Recovery coverage, retention and irreversible exceptions unverified. Not proof of recurring-growth/process monitoring.')
claim('developer', 'The App Store description includes intermediate build files and package-manager caches.', 'app-store', 'Developer Files: Safely remove your intermediate build files and package manager caches.', 'Do not repeat safely as a verified safety claim. Exact tools, paths and rebuild costs not documented here; do not claim no developer support.')
claim('local-scan', 'Nalarin describes scans as local; its privacy policy also discloses a device identifier for licence management.', 'privacy', 'The only information we collect is a unique device-level identifier.', 'Do not generalize local scans into zero network use or no data collection.')
claim('privacy-conflict', 'The homepage says no usage tracking, while the App Store declares identifiers used to track users and identifiers not linked to identity.', 'app-store', 'Data Used to Track You', 'Unresolved developer-disclosure conflict. No network audit. Block blanket no-tracking/no-data-leaves claims.', state='contradicted')
claim('sandbox', 'Nalarin describes the app as sandboxed.', 'official', 'Runs within the secure macOS sandbox, respecting your system\'s permissions.', 'Vendor disclosure only, not binary entitlement or permission-scope inspection.')
claim('br-preview', 'Breathing Room, which we build, is a macOS 13+ preview identified as 0.1.0-preview.1; its release discloses no Developer ID signing or notarization and Python 3.10+ for inventory.', 'br-capabilities', 'Apple Development signed, not Developer ID signed or notarized', 'Reuse capabilities.md preview table and release URL https://github.com/bucabay/breathing-room-app/releases/tag/v0.1.0-preview.1; source implementation is not distributed-binary QA.')
claim('br-price-hosted', 'Breathing Room advertises free local tools and optional hosted AI Care at $5 USD/month or $50 USD/year; hosted assistance needs authentication/internet.', 'br-capabilities', '$5 USD/month', 'capabilities.md pricing and local/hosted sections; not an account/payment/entitlement test; renewal and applicable taxes disclosed. Local inspection differs from hosted tool-output sharing.')
claim('br-workflow', 'Breathing Room source implements category/app/project storage views, app/helper grouping, activity history and exact saved approvals for daily care while the app runs.', 'br-capabilities', 'Daily care', 'capabilities.md matrix and approval exception: explicitly enabled automatic Ruff-cache Trash mode exists; never say every action always needs a new click. Sampled ownership is not forensic attribution.')
for c in claims:
    if c['sourceIds'] == ['official']:
        assert c['excerpt'] in official['text'], c['id']
    if c['sourceIds'] == ['app-store']:
        assert c['excerpt'] in app_html, c['id']

class AssetParser(HTMLParser):
    def __init__(self): super().__init__(); self.urls = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'source' and 'srcset' in d:
            for part in d['srcset'].split(','):
                url = part.strip().split(' ')[0]
                if 'App_Store_Screenshot_1.png/1286x804bb.webp' in url and url not in self.urls:
                    self.urls.append(url)
parser = AssetParser(); parser.feed(app_html)
assert parser.urls
br = next(a for a in load(APP / 'docs/content/screenshots.json')['assets'] if a['id'] == 'current-space-browser-preview')
assert digest(Path(br['sourcePath'])) == br['sha256']
visuals = [
    {'id': 'diskmaid-app-store-screenshot-1', 'productId': 'diskmaid', 'view': 'App Store Mac app screenshot 1; actual pixels not reviewed', 'kind': 'official-asset', 'sourcePageUrl': store['finalUrl'], 'assetUrl': parser.urls[0], 'locator': '#product_media_mac_ source srcset; exact URL from public HTML, not inferred', 'capturedAtUtc': None, 'retrievedAtUtc': None, 'sourcePageRetrievedAtUtc': store['retrievedAtUtc'], 'capturedBy': None, 'productVersion': None, 'dataMode': 'vendor-illustration', 'originalPath': None, 'originalSha256': None, 'publishedPath': None, 'publishedSha256': None, 'widthPx': None, 'heightPx': None, 'edits': [], 'privacyReview': {'status': 'pending'}, 'reuse': {'status': 'link-only', 'basis': 'Authoritative store listing provides source link, not permission to copy. No reusable image licence or permission established; no image downloaded.', 'evidenceUrlOrPath': 'https://nalarin.com/mymacmaid/terms', 'credit': 'DiskMaid / Nalarin, via Apple App Store'}, 'caption': 'DiskMaid vendor-supplied Mac screenshot on its App Store listing; linked reference only. Not our test or a measured cleanup result.', 'alt': 'DiskMaid Mac app screenshot supplied by Nalarin on the App Store; detailed view description pending pixel review.', 'supportedClaimIds': [], 'limitations': ['Exact URL retained, but image pixels, dimensions, version, capture date and privacy not verified.', 'No on-page embedding or hotlinking; rights gate remains blocked.'], 'review': {'status': 'pending'}},
    {**br, 'productId': 'breathing-room', 'originalPath': br['sourcePath'], 'originalSha256': br['sha256'], 'publishedPath': None, 'publishedSha256': None, 'reviewThisJob': 'Opened and read actual PNG; visible Interactive preview · example data banner and no-Mac-change disclosure. No edits or copy.', 'requiredLabels': ['Current-source browser preview', 'Example data only', 'Not a native scan, measured activity or cleanup result'], 'supportedClaimIds': ['br-workflow']},
]
matrix = {
    'macOS': {'value': '14.6+', 'claimIds': ['platform-version']},
    'licence': {'value': 'Personal, non-exclusive, non-transferable', 'claimIds': ['license']},
    'localHosted': {'value': 'Vendor says local scans; identifier disclosure and tracking conflict must be retained', 'claimIds': ['local-scan', 'privacy-conflict']},
    'scanCleanup': {'value': 'Caches/logs/Trash/browser data, large/old files, duplicates and app remnants documented', 'claimIds': ['scan', 'large-files', 'duplicates', 'uninstaller']},
    'approval': {'value': 'Pre-deletion visibility documented; exact mutation/recovery semantics not verified', 'claimIds': ['approval', 'history']},
    'developerCaches': {'value': 'Build files/package-manager caches documented; exact adapters not verified', 'claimIds': ['developer']},
    'pricing': {'value': 'Free download; Lifetime $19.99 US listing; described features require one-time purchase', 'claimIds': ['price']},
    'helperGrouping': {'value': 'not verified', 'claimIds': [], 'state': 'not-verified'},
    'recurringGrowth': {'value': 'not verified; cleanup history is not evidence of growth monitoring', 'claimIds': ['history'], 'state': 'not-verified'},
    'runtimeInstall': {'value': 'Mac App Store; sandbox vendor disclosure; architecture, external runtime and permissions scope not verified', 'claimIds': ['platform-version', 'sandbox']},
}
packet = {
    'schemaVersion': 1, 'jobId': 'research-diskmaid', 'productId': 'diskmaid', 'checkedOn': DATE,
    'status': 'blocked', 'draftingAllowed': False, 'published': False,
    'ownership': 'docs/content/competitors/diskmaid/ only, plus required receipt; no website records/assets changed',
    'identity': {'name': 'DiskMaid', 'officialHomepage': record['officialUrl'], 'officialRepository': None, 'repositoryStatus': 'No official repository linked in retained homepage/terms/store; existence not established, not proof no repository exists.', 'publisher': 'Nalarin', 'seller': 'PT KERJA AKAL DIGITAL', 'appStoreId': '6758129723', 'canonicalOwnerId': 'diskmaid', 'aliases': [{'name': 'DiskMaid: Clean Your Computer', 'state': 'verified-store-title', 'evidence': 'Retained homepage App Store ID matches linked store title.'}], 'historicalNameClues': [{'name': 'MyMacMaid', 'state': 'not-verified-as-former-product-name', 'evidence': 'Legal paths /mymacmaid/ and store bundleId Nalarin.MyMacMaid; neither alone proves a separate/former app.'}], 'aliasSkipDecision': {'skipSeparateDraft': False, 'reason': 'DiskMaid canonical record retained; only one DiskMaid identity in manifest. Store subtitle is same app ID, not another draft. No PowerMyMac alias evidence; unrelated unresolved pair not investigated or merged.', 'skipAnyMyMacMaidDraftUntilResolved': True}, 'fit': 'direct', 'fitReason': 'Documented native Mac cleanup/storage workflow overlaps; this is not a Windows-tool replacement scenario.', 'platformFit': 'Mac-to-Mac only; no Windows/Linux support claim'},
    'discovery': {**record['discovery'], 'snapshotSha256': digest(discovery_path), 'method': 'Reused batch-1, no directory re-fetch', 'edges': edges, 'edgeProvenancePath': 'docs/content/competitors.json'},
    'verificationReuse': {'batchPath': 'docs/content/verification/batch-1.json', 'recordId': 'diskmaid', 'reusedFields': ['identity', 'homepage', 'coreFunction', 'macOS design', 'free download CTA'], 'newChecks': ['App Store version/OS/full-function purchase terms/seller', 'licence', 'privacy conflict', 'public screenshot locator'], 'datePolicy': 'Same-day verified material reused; volatile offers refresh within 30 days and before publication.'},
    'sources': sources, 'claims': claims, 'productMatrix': matrix, 'visuals': visuals,
    'unknowns': ['Exact CPU architecture compatibility and required permissions', 'Actual cleanup/deletion/undo implementation and coverage', 'Official source repository and exact developer-cache adapters', 'Native/runtime behavior, benchmarks, measured savings and battery impact', 'Lifetime entitlement scope, checkout tax, regional availability, trial/free limits, current subscription SKU availability', 'Process/helper grouping and recurring-growth monitoring', 'Vendor screenshot capture date/version/pixels and reuse permission'],
    'blockers': [
        {'id': 'visual-rights', 'diagnostic': 'Competitor app image URL found in App Store HTML, but reuse permission and pixel/privacy review absent. No permitted image downloaded. Required two-product on-page visual gate not met.', 'unblock': 'Obtain documented permission/licence or explicit editorial policy approval via separately authorized work, then retrieve/hash original and visually/privacy review; do not send a permission request in this job.'},
        {'id': 'privacy-conflict', 'diagnostic': 'Official no-usage-tracking language conflicts with App Store tracking-identifiers disclosure; privacy policy admits device identifier collection.', 'unblock': 'Keep conflict explicit and omit blanket privacy/safety conclusions; current vendor clarification or independent authorized audit is needed before a stronger privacy claim.'},
    ],
    'articleBrief': {'track': 'search/reference workflow', 'proposedSlug': 'review-mac-app-remnants-and-duplicate-files', 'title': 'Review Mac app remnants without deleting shared files', 'primaryIntent': 'Decide what to retain when app leftovers and exact duplicate files appear in a Mac storage audit.', 'distinctAngle': 'Separate app-related support data from original/shared files; exact duplicate content does not establish which copy should be removed. DiskMaid documents both remnants and hashing; Breathing Room is the alternate investigate-owner workflow, not a claimed duplicate finder.', 'outline': ['Lead with retention-first decision and backups; top real product visual after lead when rights clear', 'App relationship versus identical contents: two different reasons a file appears', 'Review candidate path, active projects and backup/restore cost before selecting', 'Use documented DiskMaid preview/selection with paid-feature boundary; do not invent click steps', 'If source/ownership remains unclear, investigate rather than delete; bounded Breathing Room alternative and preview/runtime/hosted caveats', 'Record scan totals separately from actual available-space changes; no recovery guarantee'], 'interactionPass': 'Handoff a local, non-scanning keep/investigate checklist: active app/project? sole original? shared/synced copy? backup? rebuild cost known? Any unknown means keep/investigate, not delete. No filesystem access, upload or fake savings calculation.', 'internalLinks': ['/comparisons/', '/comparisons/diskmaid/'], 'visualPlan': 'Breathing Room Space preview directly after lead with example-data disclosure; DiskMaid app view later only after rights and pixel review.'},
    'comparisonBrief': {'proposedSlug': 'diskmaid', 'title': 'Breathing Room vs DiskMaid', 'primaryIntent': 'Choose a Mac cleanup/storage approach, not a speed/safety winner.', 'rows': list(matrix), 'conclusion': 'DiskMaid documents App Store-distributed cleanup, duplicate detection and app-remnant removal; Breathing Room, which we build, offers a preview investigation/approval workflow with local tools and optional hosted AI. Choose by documented task and release caveats, not unsupported superiority.', 'linkToWorkflow': '/blog/review-mac-app-remnants-and-duplicate-files/', 'lengthPolicy': 'Concise sourced matrix and decision criteria; do not duplicate workflow article or create alternatives doorway.'},
    'advantagesAndTradeoffs': {'diskmaid': ['Documented exact-duplicate finder and app uninstaller/remnant workflow; neither is verified as equivalent in Breathing Room.', 'Mac App Store distribution and native SwiftUI positioning; this is not proof of faster/safer operation.', 'Purchase-gated described functionality, macOS 14.6+ requirement, unspecified adapters and unresolved privacy-disclosure conflict.'], 'breathingRoom': ['Source-documented owner/project views, grouped app/helper monitoring and reviewable saved approvals; source presence is not binary/runtime QA.', 'Free local tools versus optional paid hosted assistance; hosted tool data is not all-local processing.', 'Preview 0.1.0-preview.1, macOS 13+, Python 3.10+ inventory prerequisite, non-notarized release and physical-Intel validation limitations must be disclosed.']},
    'testing': {'handsOnCompetitor': False, 'cleanupRun': False, 'browserUsed': False, 'imageDownloaded': False, 'siteChanged': False, 'independentReview': 'pending', 'notes': 'Research only. No build/test of unchanged website; no product, payment, safety or performance tests claimed.'},
    'accessDiagnostics': {'firstRetentionAttempt': 'urllib App Store HTTP 403; later ordinary retry succeeded. No anti-bot bypass.', 'laterRetention': manifest, 'fallback': 'Terms/privacy successfully read with WebFetch; official capabilities retained from existing same-day snapshot. No browser/CDP/profile recovery needed.'},
}
(ROOT / 'research.json').write_text(json.dumps(packet, indent=2, ensure_ascii=False) + '\n')
print(f'Assembled {len(claims)} claims, {len(sources)} sources, {len(visuals)} visuals; status blocked.')
