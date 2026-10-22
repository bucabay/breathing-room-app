"""Assemble the owned research packet from retained evidence; no network calls."""
import datetime
import hashlib
import json
import re
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
OWNER = 'scheduled-research-storagerader (documentary research; not independent approval)'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    return str(path.relative_to(APP))


def load(path):
    return json.loads(path.read_text())


spec = importlib.util.spec_from_file_location('collector', ROOT / 'collect-evidence.py')
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)
baseline = load(APP / 'docs/content/verification/batch-2.json')
record = next(p for p in baseline['records'] if p['id'] == 'storagerader')
official_path = APP / record['sources'][0]['rawCapture']
directory_path = APP / record['discovery']['rawCapture']
official = load(official_path)
sources = [
    dict(id='S1', publisher='AlternativeTo', url=record['discovery']['sourceUrl'],
         finalUrl=record['discovery']['sourceUrl'], retrievedAtUtc=record['discovery']['retrievedAt'],
         rawPath=rel(directory_path), sha256=sha(directory_path), text=directory_path.read_text(),
         method='Reused batch-2 owned-tab rendered DOM; discovery only'),
    dict(id='S2', publisher='StorageRadar', url=official['url'], finalUrl=official['finalUrl'],
         retrievedAtUtc=official['retrievedAt'], rawPath=rel(official_path), sha256=sha(official_path),
         text=official['text'], method='Reused current batch-2 official rendered text; not refetched'),
]
for id_, name in [('S3', 'about'), ('S4', 'direct'), ('S5', 'changelog'), ('S6', 'privacy')]:
    p = ROOT / 'evidence' / (name + '.json')
    s = load(p)
    sources.append(dict(id=id_, publisher='StorageRadar', url=s['url'], finalUrl=s['finalUrl'],
                        retrievedAtUtc=s['retrievedAtUtc'], rawPath=rel(ROOT / s['rawPath']),
                        sha256=s['rawSha256'], text=s['text'], method='Public HTTP read; retained HTML'))

# Preserve the exact already-fetched App Store HTML instead of fetching it again.
apple_input = Path('/Users/gabe/.local/share/opencode/tool-output/tool_160865c43001qen4nK1kk01Q25')
apple_path = ROOT / 'evidence/app-store.html'
if not apple_path.exists():
    apple_path.write_bytes(apple_input.read_bytes())
parser = collector.Text()
parser.feed(apple_path.read_text())
apple_text = '\n'.join(parser.parts)
sources.append(dict(id='S7', publisher='Apple App Store / developer supplied listing',
                    url='https://apps.apple.com/us/app/storageradar/id6759776887',
                    finalUrl='https://apps.apple.com/us/app/storageradar-disk-space/id6759776887',
                    retrievedAtUtc=None, checkedAtUtc=NOW,
                    retrievalTimeNote='Read by WebFetch in this job before packet assembly; exact HTTP retrieval timestamp unavailable. checkedAtUtc is assembly/check time, not fabricated capture time.',
                    rawPath=rel(apple_path), sha256=sha(apple_path), text=apple_text,
                    method='Retained complete WebFetch HTML output; canonical URL from link rel=canonical, not an asserted redirect'))
sources_by_id = {s['id']: s for s in sources}
claims = []


def claim(id_, wording, source, excerpt, scope, location='comparison matrix / workflow brief'):
    assert excerpt in sources_by_id[source]['text'], (id_, excerpt)
    claims.append(dict(id=id_, wording=wording, state='verified', evidenceClass='officially-documented, not hands-on-tested',
                       sourceIds=[source], sourceUrls=[sources_by_id[source]['finalUrl']], excerpt=excerpt,
                       checkedAtUtc=sources_by_id[source].get('checkedAtUtc', sources_by_id[source]['retrievedAtUtc']),
                       scope=scope, intendedLocation=location, reviewer=OWNER, unresolvedQuestions=[]))


claim('C01', 'The directory name StorageRader resolves to official StorageRadar.', 'S2',
      'StorageRadar', 'Directory official link storageradar.chama.pro redirected to storageradar.app in retained batch-2 evidence; same listing identity, not a second product.')
claim('C02', 'StorageRadar identifies its founder as Vladimir Chemeris.', 'S3',
      'Vladimir Chemeris', 'Also corroborated by App Store seller. Do not substitute country or company inferred from a directory.')
claim('C03', 'The App Store edition requires macOS 15.0 or later.', 'S7',
      'Requires macOS 15.0 or later.', 'US Mac listing; no Windows/Linux or processor compatibility claim established.')
claim('C04', 'Vendor release history lists version 3.0.8, build 308, dated 2026-10-21.', 'S5',
      '3.0.8', 'Vendor release history, not proof this is the version in every distribution channel.')
claim('C05', 'The US App Store page checked in this job displays version 3.0.6.', 'S7',
      '3.0.6', 'Channel-specific listing observation; do not call 3.0.8 the current App Store version. No installer downloaded.')
claim('C06', 'StorageRadar documents Treemap and Sunburst, large files, exact duplicate review and batch cleanup review.', 'S2',
      'Treemap & Sunburst visualization\nLarge Files with filters & search\nDuplicate Review for exact file copies\nCleanup List for batch operations', 'Vendor documentation; no coverage, accuracy or performance benchmark.')
claim('C07', 'Free includes scanning, previews, dry run and local snapshot capture/history; applying cleanup and report compare/export are excluded.', 'S2',
      'Move to Trash / Delete\nApp Uninstaller apply\nDev Cleanup apply\nReports compare & export', 'These lines are under Free / Not included. Snapshot capture is not the same entitlement as comparison/export.')
claim('C08', 'The homepage advertises Core at $9.99 USD, Developer at $19.99 USD and Core-to-Developer upgrade at $9.99, one-time rather than subscription.', 'S2',
      'Free keeps preview access across all main workspaces · Upgrade from Core to Developer is $9.99 · USD pricing shown; regional App Store pricing may vary · No subscription · Family Sharing supported where available', 'Core/Developer amounts in adjacent pricing cards. Region and Family Sharing conditions apply; no checkout tested.')
claim('C09', 'Core unlocks file cleanup and App Uninstaller apply; Developer adds Dev Cleanup apply and report compare/export.', 'S2',
      'Dev Cleanup apply\nEcosystem profiles (Xcode, npm…)\nStep-by-step pre-apply review\nReports compare over time\nJSON / Markdown / CSV export', 'Developer includes Core. Do not present paid apply actions as free.')
claim('C10', 'StorageRadar says removal follows review, with Trash/undo distinguished from permanent deletion.', 'S2',
      'Move to Trash supports a quick undo window: you can restore items from Trash via Finder afterward. Delete Permanently does not support undo.', 'Documented controls, not a safety guarantee. No cleanup run. Trash movement is not immediate free-space recovery.')
claim('C11', 'Developer profiles cover Apple, Web, Backend, Android, Data and Containers ecosystems.', 'S2',
      'Dev Cleanup covers six groups: Apple (Xcode DerivedData, Archives, simulators, device support, SwiftPM, CocoaPods, Carthage), Web (npm, pnpm, Yarn, Corepack, and node-gyp caches), Backend (Homebrew, JetBrains, Composer, Go, and Rust Cargo caches), Android (Gradle caches, the Android SDK cache, emulator artifacts), Data (pip and pytest caches), and Containers (Docker, Colima, Podman).', 'Vendor catalogue; profile presence does not establish compatibility with every tool version or permission state.')
claim('C12', 'StorageRadar documents local snapshot history and Developer-tier diff/export for growth comparisons.', 'S2',
      "Free and Core can capture snapshots and review that history; Developer unlocks diff and export to answer 'what grew, shrank, appeared, or disappeared?'", 'Point-in-time comparisons; do not infer a continuous watcher, process attribution or scheduled cleanup.')
claim('C13', 'Vendor documentation says core storage data stays local, with opt-out analytics and diagnostics enabled by default.', 'S6',
      'this analytics delivery is enabled by default and can be turned off in Settings.', 'Aptabase analytics and Sentry diagnostics are documented remote channels; policy assertions, not an audit. Never say no network traffic or no telemetry.')
claim('C14', 'The optional MCP endpoint is documented as local and read-only without file-content or mutation access.', 'S6',
      'It does not provide remote cloud processing, file-content access, delete operations, or move operations.', 'Describes StorageRadar endpoint, not any external assistant client privacy policy.')
claim('C15', 'The Direct build is documented as outside App Store sandboxing and uses a separately activated licence key.', 'S4',
      'The Direct build gets broader macOS access for advanced and developer cleanup that sandboxing limits on the App Store.', 'Broader access is vendor-described; macOS permissions still apply. Signing/notarization not independently checked.')
claim('C16', 'The Direct page currently labels the Core-to-Developer upgrade $10.', 'S4',
      'Upgrade Core → Developer — $10', 'Different channel/page from homepage $9.99 upgrade. Preserve both; do not silently round or assert one universal upgrade price.')
claim('C17', 'App Store metadata labels the download free with in-app purchases.', 'S7',
      'Free · In‑App Purchases', 'Free download does not mean paid apply/report actions are free; actual purchases and availability in other storefronts untested.')

matrix = [
    ('macOS compatibility', 'macOS 15.0+ App Store edition; architecture not verified', ['C03']),
    ('versions', 'Vendor history 3.0.8 build 308 (2026-10-21); US App Store displays 3.0.6', ['C04', 'C05']),
    ('licence', 'Paid one-time unlocks; source-code licence not verified', ['C08', 'C09']),
    ('local / hosted', 'Local scan data and no required app account documented; analytics/diagnostics are remote and opt-out', ['C13']),
    ('scan / cleanup model', 'Treemap/Sunburst, large files, duplicates; review then paid apply', ['C06', 'C07', 'C09']),
    ('approval controls', 'Dry run / pre-apply review; Trash undo differs from irreversible permanent deletion', ['C10']),
    ('helper grouping', 'CPU/memory app-helper grouping not verified; do not write No', []),
    ('recurring growth', 'Local snapshots; Developer diff/export. Continuous watcher not verified', ['C12']),
    ('developer caches', 'Six documented ecosystem groups; Developer apply; build/access restrictions', ['C11', 'C15']),
    ('pricing', 'Free previews; Core $9.99 USD; Developer $19.99 USD; homepage upgrade $9.99 / Direct upgrade $10', ['C07', 'C08', 'C09', 'C16']),
    ('runtime / installation', 'App Store and Direct build differ in sandbox scope; external runtime requirements and native signature/notarization not verified', ['C15']),
    ('AI', 'Local read-only MCP, not deletion authority; no parity claim with hosted Breathing Room assistant', ['C14']),
]

inventory = load(APP / 'docs/content/screenshots.json')
preview = next(a for a in inventory['assets'] if a['id'] == 'current-space-browser-preview')
assert sha(Path(preview['sourcePath'])) == preview['sha256']
asset_matches = re.findall(r'https://is1-ssl\.mzstatic\.com/[^\s"<>]+', apple_path.read_text())
asset_url = next(u for u in asset_matches if '/2_see-your-disk-clearly.png/1286x804bb.webp' in u)
visuals = [
    dict(id='storageradar-app-store-disk-map', productId='storagerader', view='Disk Map listing screenshot candidate',
         kind='listing-asset', sourcePageUrl=sources_by_id['S7']['finalUrl'], assetUrl=asset_url,
         capturedAtUtc=None, retrievedAtUtc=None, capturedBy=None, productVersion=None,
         dataMode='vendor-illustration', originalPath=None, originalSha256=None,
         publishedPath=None, publishedSha256=None, widthPx=None, heightPx=None, edits=[],
         reuse=dict(status='link-only', basis='No licence or permission grant established. Public App Store display is not republication permission.',
                    evidenceUrlOrPath=sources_by_id['S7']['rawPath'], credit='StorageRadar / Vladimir Chemeris; source: Mac App Store'),
         caption='StorageRadar app screenshot supplied on its Mac App Store listing. Vendor illustration; version and capture date unknown; not our test.',
         alt='StorageRadar disk visualization screenshot linked from its Mac App Store listing; visual description pending inspection.',
         privacyReview=dict(status='pending', redactions=[]), supportedClaimIds=['C06'],
         limitations=['URL found inside Mac App Previews and Screenshots shelf, not the social card or icon.',
                      'No competitor image downloaded because reuse rights are unclear; dimensions in URL are not measured file dimensions.',
                      'Image contents not independently opened or visually approved. Candidate alt/caption must be refined after rights-cleared inspection.'],
         review=dict(status='pending', reviewer=None, reviewedAtUtc=None)),
    dict(id=preview['id'], productId='breathing-room', kind='browser-preview', view='Space',
         sourcePageUrl=preview['sourceUrl'], assetUrl=None, capturedAtUtc=preview['capturedOn'],
         retrievedAtUtc=None, capturedBy='screenshot-library job (reused, not recaptured)',
         productVersion=None, buildOrCommit=preview['sourceCommit'], osVersion=None,
         dataMode='example', originalPath=preview['sourcePath'], originalSha256=preview['sha256'],
         publishedPath=None, publishedSha256=None, widthPx=preview['width'], heightPx=preview['height'], edits=[],
         reuse=dict(status='cleared', basis=preview['reuseBasis'], evidenceUrlOrPath='docs/content/screenshots.json', credit='Breathing Room, which we build'),
         caption=preview['caption'], alt=preview['alt'], privacyReview=preview['privacyReview'],
         supportedClaimIds=[], limitations=preview['limitations'] + ['Current-source means captured source commit, not a certification of every subsequent change. Retain both example-data banners; no numerical result claims.'],
         review=dict(status='research-visual-inspected', reviewer=OWNER, reviewedAtUtc=NOW)),
]

article = dict(status='brief-only-blocked', track='search/LLM reference',
               title='Compare two Mac storage scans without mistaking permission gaps for growth',
               proposedSlug='compare-mac-storage-scans-permission-gaps',
               primaryIntent='Use baseline/target snapshots to investigate growth while holding scan root and permission coverage constant.',
               audience='Mac developers whose storage keeps growing between work sessions',
               distinctMechanism='StorageRadar snapshots, Developer compare/export, and visible blocked paths; contrast point-in-time diff with ongoing sampled activity.',
               conclusion='Choose snapshot comparisons for a bounded before/after question; do not treat a new permission grant, mounted volume or changed scan root as proof an app generated new data.',
               outline=['Define one scan root and record build, time, scope and access coverage.',
                        'Review blocked paths before interpreting a baseline; unknown size is not zero.',
                        'Capture a second local snapshot of the same root; compare/export requires Developer.',
                        'Separate grew/new/removed from changed visibility and mounted-volume handling (3.0.8 release note).',
                        'Inspect exact paths and rebuild/download cost; review before any removal. No cleanup instructions executed here.',
                        'When repeated activity rather than two snapshots is the question, consider Breathing Room, which we build, with preview/hosted/paid caveats.'],
               interactionHandoff='A no-upload checklist with scan root, version, permissions changed?, and baseline/target timestamps. If scope/access changed, return incomparable, not a fabricated GB delta. No filesystem access or deletion.',
               visualPlan='Rights-cleared StorageRadar Disk Map after lead, selected Breathing Room Space preview later with both example-data warnings; do not imply these show the same scan.',
               internalLinks=['/comparisons/', '/comparisons/storagerader/'],
               unknownLinks='Confirm counterpart route and suitable local tool route at draft stage; do not invent working links.',
               noHandsOn='Documented workflow brief, not a claim that two scans were executed.')
comparison = dict(status='brief-only-blocked', title='Breathing Room vs StorageRadar: snapshots or ongoing activity?',
                  proposedSlug='storagerader', primaryIntent='Choose between review-first storage snapshots and a maintenance preview with ongoing activity and optional hosted assistance.',
                  classification='direct for storage analysis/reviewed cleanup; partial overlap, not whole-product equivalents',
                  rows=matrix, disclosure='Breathing Room, which we build',
                  decision='StorageRadar suits local snapshot/diff and documented duplicate/uninstall workflows with one-time paid unlocks. Breathing Room may suit sampled activity/process investigation and approval-based care, if preview and hosted-service caveats are acceptable.',
                  caveats='No measured speed, savings, safety, coverage or parity claims. No invented Windows support. Unknown competitor monitoring/helper grouping is not No.')

packet = dict(schemaVersion=1, jobId='research-storagerader', stage='research', status='blocked',
              assembledAtUtc=NOW, timeBasis='Actual UTC system clock; check timestamps preserved, not rewritten to harness calendar date.',
              draftingAllowed=False, published=False,
              ownership='Only docs/content/competitors/storagerader/ plus required runtime receipt; no site edits.',
              identity=dict(id='storagerader', officialName='StorageRadar', directoryName='StorageRader',
                            homepage='https://storageradar.app/', formerHomepage='https://storageradar.chama.pro/',
                            developer='Vladimir Chemeris', appStoreId='6759776887', canonicalOwnerId='storagerader',
                            aliases=['StorageRader', 'StorageRadar: Disk Space'],
                            aliasDecision=dict(verified=True, skipSeparateAliasDrafts=True, skipThisCanonicalProduct=False,
                                               evidence=['S1', 'S2', 'S3', 'S7'],
                                               rationale='Keep existing stable queue owner storagerader for official StorageRadar. Do not create a second StorageRadar packet/article. No evidence connecting this product to PowerMyMac.'),
                            repository=dict(url=None, state='not-verified', rationale='No official source repository linked in inspected official homepage/about/direct pages; do not infer open source or invent GitHub URL.'),
                            fit='direct-overlap-mac', fitReason='macOS disk analysis, review-first cleanup and developer storage. No non-Mac replacement framing needed.',
                            productSkipDecision='do-not-skip-relevant-canonical-product; block drafting for missing visual rights'),
              discovery=dict(**record['discovery'], seedId='mole', seedUrl='https://alternativeto.net/software/mole/',
                             edgeUrl='https://alternativeto.net/software/mole/?p=7', edgeRetrievedAtUtc='2026-10-21T18:37:22.582Z',
                             edgeSource='docs/content/competitors.json, storagerader.edges; no new traversal',
                             currentRawSha256=sha(directory_path)),
              baselineReuse=dict(path='docs/content/verification/batch-2.json', recordId='storagerader',
                                 reused=['Identity/redirect', 'macOS platform', 'core workflow', 'pricing', 'all retained homepage text'],
                                 added=['Developer/about', 'Direct-build conditions', 'channel-specific release history', 'privacy policy', 'App Store identity/version and screenshot URL'],
                                 homepageRefetched=False),
              sources=sources, claims=claims, productMatrix=[dict(dimension=a, value=b, claimIds=c) for a,b,c in matrix],
              breathingRoomEvidence=dict(path='docs/content/capabilities.md', checkedOn='2026-10-21', refetched=False,
                                          method='Reused current first-party evidence register, source/published distinctions retained; not new runtime validation.',
                                          homepage='https://breathing-room.chatic.ai/',
                                          releaseUrl='https://github.com/bucabay/breathing-room-app/releases/tag/v0.1.0-preview.1',
                                          claims=[dict(id='BR01', wording='0.1.0-preview.1 preview, macOS 13+, universal installer advertised; physical Intel and clean-machine behavior unvalidated.', locator='capabilities.md:48-54'),
                                                  dict(id='BR02', wording='Apple Development signed preview, not Developer ID signed/notarized; Python 3.10+ disclosed, not bundled.', locator='capabilities.md:50-52'),
                                                  dict(id='BR03', wording='Free local inspection/monitoring, optional AI Care advertised at $5 USD/month or $50/year; renews until cancelled, tax may apply.', locator='capabilities.md:74-79'),
                                                  dict(id='BR04', wording='Hosted AI needs network/authentication and can send relevant paths/process/storage information; do not describe all-local AI.', locator='capabilities.md:60-66'),
                                                  dict(id='BR05', wording='Source implements grouped helper CPU/memory, local activity history and saved exact daily approvals while running; not proof of installer parity.', locator='capabilities.md:24-40'),
                                                  dict(id='BR06', wording='Optional automatic Ruff-cache mode is an exception to ordinary interactive approvals; daily care uses exact saved approvals.', locator='capabilities.md:36-42')],
                                          requiredBeforePublication='Recheck if material source/release changes; refresh volatile offers within 30 days. Retain native-runtime caveats.'),
              visuals=visuals, workflowArticleBrief=article, comparisonBrief=comparison,
              truthfulAdvantagesAndTradeoffs=dict(
                  storageRadar=['Documented Treemap/Sunburst, exact-duplicate review and App Uninstaller; not verified capabilities of Breathing Room in current register.',
                                'Free local scanning and snapshot capture; Developer compare/export and developer cleanup require paid unlock.',
                                'One-time offers; core data local, but analytics and diagnostics default on. App Store sandbox limits differ from Direct.',
                                'Requires macOS 15+ on App Store, versus advertised macOS 13+ Breathing Room preview. Not a runtime compatibility test.'],
                  breathingRoom=['Source-backed grouped process monitoring/activity/care may fit ongoing investigation rather than just point-in-time diff.',
                                 'Free core and Apache-2.0 desktop source, but hosted AI Care is separately advertised and not entirely offline.',
                                 'Non-notarized preview, Python prerequisite and unvalidated installation/Intel behavior are real trade-offs. Do not declare winner from source alone.']),
              noncriticalUnknowns=['Official source-code repository/licence', 'StorageRadar processor architectures and external-runtime requirements',
                                  'StorageRadar native signature/notarization inspection', 'Exact screenshot build/capture date/data authenticity',
                                  'Continuous monitoring, helper CPU/memory grouping and scheduled care in StorageRadar',
                                  'Exact Direct currently downloadable binary version; no installer fetched', 'Actual checkout, activation, refunds and Family Sharing behavior'],
              sourceDiscrepancies=['Homepage upgrade $9.99 vs Direct page $10: retain channel-specific labels; do not assert universal upgrade cost.',
                                   'Vendor 3.0.8 history vs US Store 3.0.6: distinguish channel/listing, not an unsupported parity claim.',
                                   'About page calls one unlock User while pricing calls it Core; use pricing-page labels, no invented fourth plan.'],
              blockers=[dict(id='VISUAL-RIGHTS', severity='critical', gate='drafting',
                             diagnostic='Real competitor app screenshot URL found in App Store shelf, but no republication licence/permission established. Kept link-only, not downloaded. Required on-page competitor visual gate is unsatisfied.',
                             resolution='Provide documented rights/permission for that app image or another permitted official/listing app screenshot, then download original, retain hash/provenance and visually inspect. Do not send permission requests in this scheduled job.')],
              review=dict(status='not-independent-review', score=None, publicationApproval=False),
              safety=dict(browserUsed=False, imagesDownloaded=0, binariesDownloaded=0, installed=False, cleanup=False,
                          signup=False, purchase=False, messages=False, credentialsRead=False, queueChanged=False, siteEdited=False))
br_register = (APP / 'docs/content/capabilities.md').read_text()
br_support = [
    ('https://github.com/bucabay/breathing-room-app/releases/tag/v0.1.0-preview.1', 'macOS 13+; universal Apple Silicon/Intel installer advertised.'),
    ('https://github.com/bucabay/breathing-room-app/releases/tag/v0.1.0-preview.1', 'Apple Development signed, not Developer ID signed or notarized'),
    ('https://breathing-room.chatic.ai/#pricing', '$5 USD/month'),
    ('https://breathing-room.chatic.ai/privacy/', 'relevant paths/process/storage data can reach the service and Cloudflare Workers AI'),
    ('https://github.com/bucabay/breathing-room-app', 'Native sampling groups helpers through parent/app relationships and exposes CPU/memory.'),
    ('https://github.com/bucabay/breathing-room-app', 'Automatically move verified Ruff lint caches to Trash.'),
]
for br_claim, (url, excerpt) in zip(packet['breathingRoomEvidence']['claims'], br_support):
    assert excerpt in br_register
    br_claim.update(sourceUrls=[url], excerpt=excerpt, checkedOn='2026-10-21',
                    evidenceClass='Reused first-party capability register; source/published evidence, not runtime test',
                    supportingRegister='docs/content/capabilities.md', reviewer=OWNER)
packet['breathingRoomEvidence']['registerSha256'] = sha(APP / 'docs/content/capabilities.md')
(ROOT / 'research.json').write_text(json.dumps(packet, indent=2, ensure_ascii=False) + '\n')
print('Wrote research.json:', len(claims), 'verified documentary claims,', len(sources), 'sources; blocked visual rights')
