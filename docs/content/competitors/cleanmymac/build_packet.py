"""Assemble and validate the retained research packet; performs no network calls."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path):
    return json.loads(path.read_text())

batch = load(APP / 'docs/content/verification/batch-1.json')
record = next(r for r in batch['records'] if r['id'] == 'cleanmymac')
official_path = APP / record['sources'][0]['snapshotPath']
assert sha(official_path) == record['sources'][0]['sha256']
official = load(official_path)
directory_path = APP / record['discovery']['snapshotPath']
directory = load(directory_path)
sources = [
    dict(id='homepage', publisher='MacPaw', title='CleanMyMac homepage (reused verification snapshot)',
         url=official['officialUrl'], finalUrl=official['finalUrl'], retrievedAtUtc=official['retrievedAt'],
         snapshotPath=str(official_path.relative_to(APP)), sha256=sha(official_path),
         method='Inherited verified public-page extraction; not re-fetched', text=official['text'], scope='MacPaw direct homepage'),
    dict(id='discovery', publisher='AlternativeTo', title='CleanMyMac listing', url=directory['url'],
         finalUrl=directory['url'], retrievedAtUtc=directory['retrievedAt'],
         snapshotPath=str(directory_path.relative_to(APP)), sha256=sha(directory_path),
         method='Inherited directory DOM extraction; discovery only', text=directory['text'], scope='Directory, not official capability proof')
]
for name in ['press', 'smart-care', 'purchase', 'whats-new', 'eula', 'powermymac', 'purchase-options', 'editions', 'missing-features', 'current-eula']:
    p = ROOT / 'sources' / (name + '.json')
    d = load(p)
    s = dict(id=name, publisher='iMyMac' if name == 'powermymac' else 'MacPaw',
             title=d.get('text', name).split('\n')[0], url=d['url'], finalUrl=d.get('finalUrl'),
             retrievedAtUtc=d['retrievedAtUtc'], httpStatus=d.get('httpStatus'),
             snapshotPath=str(p.relative_to(APP)), sha256=sha(p), text=d.get('text', ''),
             method='Public HTTP GET; no cookies or authentication', error=d.get('error'), scope='Official public documentation; not runtime testing')
    raw = ROOT / 'sources' / (name + '.html')
    if raw.exists():
        assert sha(raw) == d['rawSha256']
        s.update(rawSnapshotPath=str(raw.relative_to(APP)), rawSha256=sha(raw))
    sources.append(s)
for name, path, url in [
    ('br-capabilities', 'docs/content/capabilities.md', 'https://breathing-room.chatic.ai/'),
    ('br-readme', 'README.md', 'https://github.com/bucabay/breathing-room-app'),
    ('br-screenshots', 'docs/content/screenshots.json', 'http://127.0.0.1:1431/')
]:
    p = APP / path
    sources.append(dict(id=name, publisher='Breathing Room', title=path, url=url, finalUrl=url,
                        retrievedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        snapshotPath=path, sha256=sha(p), text=p.read_text(),
                        method='Local file read; capabilities register reuses same-day source/public verification',
                        scope='First-party source/preview evidence, not installer validation'))
lookup = {s['id']: s for s in sources}
claims = []
def claim(id, wording, source, excerpt, scope, location='comparison matrix', state='verified', evidence='documented-vendor-behavior'):
    s = lookup[source]
    assert ' '.join(excerpt.split()) in ' '.join(s['text'].split()), (id, excerpt)
    claims.append(dict(id=id, proposedWording=wording, sourceIds=[source], sourceUrls=[s['url']],
                       supportingExcerpt=excerpt, checkedAtUtc=s['retrievedAtUtc'], evidenceClass=evidence,
                       scope=scope, intendedLocation=location, state=state, reviewer='research-cleanmymac worker; not independent publication reviewer'))

claim('c-identity', 'CleanMyMac is MacPaw’s Mac cleanup and maintenance product.', 'homepage',
      'This all-in-one Mac cleaner and maintenance app handles junk, duplicates, malware, and performance issues',
      'Official homepage; marketing describes intended functions, not measured effectiveness', 'identity')
claim('c-platform', 'The retained official homepage advertises macOS 11+, 320 MB and a minimum display size of 1200×800 px.', 'homepage',
      'macOS 11+, 320 MB\nMin. display size: 1200x800 px',
      'Homepage requirements; architecture-specific runtime compatibility not tested')
claim('c-home-version', 'The homepage snapshot labels 5.5.7 (22 July 2026) as latest; this conflicts with the newer dated changelog.', 'homepage',
      '5.5.7,\n            \n                          22 July 2026',
      'Do not use homepage latest-version label as current binary evidence', state='stale')
claim('c-version', 'MacPaw’s changelog documents update 5.7.2 dated October 15, 2026.', 'whats-new',
      'Update 5.7.2\n/\nOctober 15, 2026',
      'Newest dated release entry observed, not a downloaded binary or all-marketplace parity assertion')
claim('c-price-teaser', 'The homepage says “Starting at $3.33/month”; the exact offer conditions remain unverified.', 'homepage',
      '$3.33/month', 'Currency, billing period, device count, tax, discount and renewal amount not established; not a usable exact comparison price')
claim('c-purchase', 'Monthly and annual subscriptions and a one-time purchase are documented; subscriptions automatically renew.', 'purchase-options',
      'You can get either an annual or monthly CleanMyMac subscription.', 'MacPaw Store and App Store; no amounts verified')
claim('c-renewal', 'CleanMyMac subscriptions renew automatically.', 'purchase-options',
      'Subscription renewals occur automatically.', 'MacPaw Store/App Store subscriptions')
claim('c-one-time', 'A one-time purchase covers updates and fixes for the current major version, not future major-version upgrades.', 'purchase-options',
      'a one-time purchase includes only updates and fixes for your current major version of CleanMyMac.',
      'Documented entitlement, subject to compatibility; do not promise lifetime upgrades')
claim('c-editions', 'Pricing and features depend on marketplace; MacPaw says device count, upgrade possibilities and country-specific taxes affect price.', 'editions',
      'CleanMyMac pricing depends on factors like number of devices covered, upgrade possibilities, and country-specific taxes.',
      'MacPaw Store, App Store and Setapp; avoid mixing prices and feature sets')
claim('c-review', 'Smart Care scans, then lets users review results and click Run; tasks are selected by default, with Review and skip controls.', 'smart-care',
      'By default, CleanMyMac selects all Smart Care tasks. You can choose which tasks to skip by clearing the checkmark in the top-left corner of each tile.',
      'Knowledge base updated October 15, 2026; source-level workflow, not hands-on testing', 'workflow article')
claim('c-details', 'Use Review in a Smart Care tile to adjust its selected items before running tasks.', 'smart-care',
      'Click Review in a tile to adjust selections.', 'Default selections are not evidence of deletion safety', 'workflow article')
claim('c-duplicates', 'Smart Care’s My Clutter step scans Downloads for duplicate files; it is not documented here as an all-folder duplicate scan.', 'smart-care',
      'My Clutter — Scans for duplicate files in your Downloads folder.', 'Smart Care step only; other modules have different scope')
claim('c-xcode', 'MacPaw’s edition table lists Xcode Junk, user cache and system cache categories; App Store restrictions differ.', 'missing-features',
      'Xcode Junk\n✅\n✅\n✅', 'April 21, 2026 table; Xcode Junk listed for all three editions. Do not infer all developer caches or CLI parity.')
claim('c-monitoring', 'The edition table documents CPU, RAM and storage monitors and low-free-space alerts; do not say CleanMyMac lacks monitoring.', 'missing-features',
      'Storage Monitor\n✅\n✅\n✅', 'April 21, 2026 table; helper grouping and recurring-path attribution not established')
claim('c-alias', 'PowerMyMac is a separately branded iMyMac product, not a verified CleanMyMac alias.', 'powermymac',
      'Learn new skills and get help from  iMyMac', 'Combined with MacPaw CleanMyMac identity; separate vendors and products', 'identity')
claim('c-legacy', 'CleanMyMac X is a prior major version in the CleanMyMac family, not a second comparison target.', 'purchase-options',
      "a one-time purchase license of CleanMyMac X doesn't include an upgrade to the\nlatest CleanMyMac", 'Historical family name; no feature parity presumed', 'identity')
claim('b-fit', 'Breathing Room’s documented preview offers category, app/tool, project, folder and large-file storage views.', 'br-readme',
      'explore its category, app/tool,\nproject, folder, and large-file views.', 'Documentation/source, not distributed binary test')
claim('b-caveats', 'Breathing Room is a macOS 13+ preview requiring Python 3.10+ for inventory; hosted agent features require internet and sign-in.', 'br-readme',
      'Internet access and sign-in for hosted agent features.', 'README requirements also list macOS 13+ and Python 3.10+; see source; physical Intel not runtime-tested')
claim('b-pricing', 'Breathing Room’s core app is free; optional AI Care is advertised at $5 USD/month or $50 USD/year.', 'br-readme',
      '**AI Care is optional: $5 USD/month or $50 USD/year.**', 'Same-day capabilities public offer verification reused; no payment/entitlement test')
claim('b-preview', 'Breathing Room’s preview is not notarized; do not recommend disabling system protections.', 'br-readme',
      'The preview is not notarized.', 'Published preview caveat; not independent binary signature inspection')
claim('b-approval', 'Do not claim Breathing Room never cleans without a fresh prompt: optional narrowly verified Ruff automatic mode exists; daily care reuses saved exact approvals.', 'br-capabilities',
      'users can enable automatic Trash moves for narrowly verified Ruff caches during an investigation.', 'Same-day source register; scoped approval exception')

claim('b-platform', 'Breathing Room documents macOS 13+ and Python 3.10+ as requirements; physical Intel execution remains untested.', 'br-readme',
      '**Python 3.10+** for disk inventory and legacy cleanup scripts.', 'Requirements section; no compatible Python bundled')
claim('b-local-hosted', 'Inspection runs locally; hosted AI can receive relevant paths/process/storage data.', 'br-capabilities',
      'relevant paths/process/storage data can reach the service and Cloudflare Workers AI', 'Same-day policy/source verification reused; not backend audit')
claim('b-license', 'Breathing Room desktop source uses Apache License 2.0; that does not grant hosted-service entitlement.', 'br-capabilities',
      'Desktop source is Apache License 2.0 with NOTICE and preserved third-party attribution.', 'Desktop source only')
claim('b-activity', 'Breathing Room implements grouped helpers, CPU/memory sampling and local activity observations; source presence is not complete runtime QA.', 'br-capabilities',
      'Native sampling groups helpers through parent/app relationships and exposes CPU/memory.', 'Same-day source register; attribution and shared-memory limits remain')
claim('b-dev', 'Breathing Room source discovery queries npm, uv, pip, pnpm, Go, Bun and Yarn caches, with validation and installed-tool constraints.', 'br-capabilities',
      'Discovery includes queries for npm, uv, pip, pnpm, Go build/module, Bun and Yarn caches', 'Source adapters, not every cache/version tested')
claim('c-lens', 'CleanMyMac documentation lists a Space Lens storage module.', 'missing-features',
      'The\nSpace Lens module\nis available with the same scope of features in all editions of CleanMyMac.', 'Official edition table, April 21, 2026; no runtime test')
claim('c-notarization', 'The retained CleanMyMac homepage says “Notarized by Apple.”', 'homepage',
      'Notarized by Apple', 'Vendor assertion only; no binary signature inspection')

selected = next(a for a in load(APP / 'docs/content/screenshots.json')['assets'] if a['id'] == 'current-space-browser-preview')
assert sha(Path(selected['sourcePath'])) == selected['sha256']
br_visual = dict(selected)
br_visual.update(productId='breathing-room', originalPath=selected['sourcePath'], originalSha256=selected['sha256'],
                 publishedPath=None, publishedSha256=None, supportedClaimIds=['b-fit'],
                 review=dict(status='research-visual-inspected; independent-target-page-review-pending', reviewer='research-cleanmymac worker',
                             diagnostic='Opened actual PNG. Example-data labels visible; floating assistant overlaps chart. Full-size image is tall; contextual crop must preserve disclosure.'))
competitor_visual = dict(
    id='cleanmymac-smart-care-task-details', productId='cleanmymac', view='Smart Care task details', kind='official-asset',
    sourcePageUrl=lookup['smart-care']['url'],
    assetUrl='https://cms-assets-proxy.macpaw.com/cdn-cgi/image/format=auto,quality=90/f296b094-6321-4b20-b995-a16b07b456ae.webp',
    capturedAtUtc=None, retrievedAtUtc=None, sourcePageRetrievedAtUtc=lookup['smart-care']['retrievedAtUtc'],
    capturedBy=None, productVersion=None, buildOrCommit=None, osVersion=None, dataMode='vendor-illustration',
    originalPath=None, originalSha256=None, publishedPath=None, publishedSha256=None, widthPx=None, heightPx=None, edits=[],
    privacyReview=dict(status='pending', redactions=[]),
    reuse=dict(status='link-only', basis='Official support page links a real app UI asset with alt text Task details. Public availability is not a licence. Press room offers a kit but kit retrieval returned 403; no permission to republish this support asset established.',
               evidenceUrlOrPath='https://macpaw.com/press', credit='CleanMyMac screenshot: MacPaw; link to official Smart Care documentation.'),
    caption='Official MacPaw Smart Care task-details illustration. Vendor-provided UI, not our test or measured cleanup result. Exact build and capture date unknown.',
    alt='Official CleanMyMac Smart Care task-details screenshot linked from MacPaw’s review-results instructions.',
    supportedClaimIds=['c-review', 'c-details'], limitations=['Asset URL and app-view identity established by retained official HTML; image bytes not downloaded or visually approved.', 'Link-only research fallback does not satisfy on-page image gate.'],
    review=dict(status='blocked-rights-and-access', reviewer=None, reviewedAtUtc=None))

packet = dict(
    schemaVersion=1, jobId='research-cleanmymac', productId='cleanmymac', stage='research', status='blocked', published=False,
    reviewedOn='2026-10-21', generatedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    ownership=dict(appFolder='docs/content/competitors/cleanmymac/', websiteEdits=False, sharedFilesEdited=False, queueChanged=False),
    identity=dict(officialName='CleanMyMac', vendor='MacPaw', canonicalOwnerId='cleanmymac', homepage=official['officialUrl'],
                  repository=dict(url=None, state='not-verified', diagnostic='No official CleanMyMac application source repository established in checked official pages; do not invent a GitHub URL or open-source licence.'),
                  license=dict(value='Directory labels proprietary; exact current app EULA not verified', state='not-verified', sourceIds=['discovery','eula','current-eula'], diagnostic='Generic /eula expressly lists older CleanMyMac Classic/2/3, not proof of current 5.x terms. Guessed /legal/cleanmymac returned 404.'),
                  aliases=[dict(name='CleanMyMac X', canonicalOwnerId='cleanmymac', relationship='previous major version', skipSeparateDraft=True, claimIds=['c-legacy'])],
                  suspectedAliases=[dict(name='PowerMyMac', canonicalOwnerId='imymac--cleaner', relationship='distinct iMyMac product, not CleanMyMac alias', skipAsCleanMyMacAlias=False, createSeparateDraftInThisJob=False, claimIds=['c-alias','c-identity'])],
                  skipDecision=dict(skipProduct=False, reason='Relevant live Mac product; direct overlap in storage inspection and cleanup. Historical X name should not generate a duplicate draft. PowerMyMac stays separate; no other queue job edited.'),
                  fit=dict(classification='direct', platform='Mac', rationale='Shared cleanup/storage-maintenance intent; CleanMyMac also documents malware/app/duplicate/cloud tools beyond verified Breathing Room scope.', windowsSupport='not-verified; do not invent', macReplacementIntent='Mac user choosing reviewable cleanup versus an investigation-oriented preview')),
    discovery=dict(**record['discovery'], snapshotSha256=sha(directory_path), method='Reused corresponding batch-1 record and retained listing DOM snapshot',
                   seedUrl='https://alternativeto.net/software/cleanmymac/about/', pagination='Direct about page; no new pagination traversal', destinationUrl=official['officialUrl'], rawResponseLimit='Retained extracted DOM JSON, not original wire HTML', exclusions=['Ads and unrelated outbound links are not product evidence']),
    reuse=dict(verificationBatch='docs/content/verification/batch-1.json', batch2PresentAtIntake=False,
               currentFactsReused=['official identity/homepage','core function','homepage platform requirements','price teaser','download availability'],
               noNeedlessRefetch='Homepage and AlternativeTo listing were not fetched again; missing official workflow/pricing/version/rights evidence was checked.'),
    versions=dict(homepage='5.5.7, 22 July 2026', latestDocumentedChangelog='5.7.2, October 15, 2026', binaryTested=None,
                  resolution='Use latest documented changelog wording. Homepage version label is stale; do not claim installed or all-marketplace latest build.', claimIds=['c-home-version','c-version']),
    pricing=dict(exactAmount=None,currency=None,billingPeriod=None,deviceCount=None,tax=None,renewalAmount=None,trialPaymentConditions=None,
                 state='blocked-exact-offer', publicTeaser='$3.33/month starting price; currency/billing conditions not established',
                 verifiedOptions=['monthly subscription','annual subscription','one-time current-major purchase','Setapp subscription'],
                 claimIds=['c-price-teaser','c-purchase','c-renewal','c-one-time','c-editions'],
                 diagnostic='WebFetch store GET returned 403. Owned Chrome page33 displayed human-verification challenge; stopped, did not solve/bypass. No checkout created.'),
    sources=sources, claims=claims,
    productMatrix=[
        dict(dimension='macOS/platform', cleanMyMac='Homepage macOS 11+, 320 MB, 1200×800 minimum display; architecture runtime not verified', breathingRoom='macOS 13+, Python 3.10+, Intel runtime untested', claimIds=['c-platform','b-caveats']),
        dict(dimension='Licence/repository', cleanMyMac='Current exact EULA and official app repo not verified; directory says proprietary', breathingRoom='Apache-2.0 desktop source; not hosted-service entitlement', claimIds=[], sourceIds=['discovery','eula','br-capabilities'], state='qualified-unknown'),
        dict(dimension='Local versus hosted', cleanMyMac='Mac app; blanket offline operation/data boundary not verified', breathingRoom='Local inspection; hosted authenticated AI with relevant paths/tool data sent to service', claimIds=['b-caveats'], sourceIds=['br-capabilities'], state='qualified-unknown'),
        dict(dimension='Scan/cleanup/approval', cleanMyMac='Smart Care scan → default-selected tasks → Review/skip → Run', breathingRoom='Review exact native-validated actions; optional narrow Ruff automatic mode and saved approvals are distinct', claimIds=['c-review','c-details','b-approval']),
        dict(dimension='Storage inspection', cleanMyMac='Space Lens and clutter tools documented in edition table', breathingRoom='Category, app/tool, project, folder and large-file views', claimIds=['b-fit'], sourceIds=['missing-features']),
        dict(dimension='Process/helper grouping', cleanMyMac='CPU/RAM monitor documented; helper grouping not verified', breathingRoom='Grouped app/helper sampling implemented; memory and attribution caveats apply', claimIds=['c-monitoring'], sourceIds=['br-capabilities'], state='qualified-unknown'),
        dict(dimension='Recurring-growth monitoring', cleanMyMac='Storage monitor/alerts documented; path-level recurring growth attribution not verified', breathingRoom='Activity source records samples/events; incomplete attribution, app must run', claimIds=['c-monitoring'], sourceIds=['br-capabilities'], state='qualified-unknown'),
        dict(dimension='Developer caches', cleanMyMac='Xcode Junk listed; npm/pnpm/Ruff/CLI scope not verified', breathingRoom='Source adapters include npm/uv/pip/pnpm/Go/Bun/Yarn; tool/version validation limits apply', claimIds=['c-xcode'], sourceIds=['br-capabilities'], state='qualified-unknown'),
        dict(dimension='Pricing', cleanMyMac='Options verified, exact payable offer blocked', breathingRoom='Free core; optional AI Care $5 USD/month or $50 USD/year', claimIds=['c-price-teaser','c-purchase','b-pricing']),
        dict(dimension='Install/runtime', cleanMyMac='Vendor homepage says notarized; independent signature/runtime, permissions and architecture not tested', breathingRoom='Non-notarized preview; Python prerequisite; hosted login/network; partial permissions', claimIds=['b-preview','b-caveats'], sourceIds=['homepage'], state='qualified-vendor-assertion')
    ],
    visuals=[competitor_visual, br_visual],
    observations=dict(handsOnTesting=False, nativeAppLaunched=False, binariesDownloaded=False, cleanupPerformed=False, measuredSavings=None,
                      browser='Owned page33 only, about:blank health check then public store. Human-verification challenge retained in sources/store-browser.txt; owned page closed. Existing tabs not inspected or modified.'),
    briefs=dict(
        workflow=dict(track='search/LLM reference', title='Review CleanMyMac Smart Care selections before running cleanup', slug='review-cleanmymac-smart-care-selections',
                      intent='Help a Mac owner distinguish scan findings, selected tasks and actual removal before using a multi-module Run action.',
                      description='A documented review checklist for Smart Care’s default selections, per-tile details and exclusions. Not a hands-on test or a promise that every suggested file is disposable.',
                      structure=['Show official task-details visual after the lead, once cleared.', 'Explain the default-selected tasks and Review/skip controls.', 'Distinguish Downloads duplicate scan from other module scopes.', 'Classify originals, rebuildable data and unknown files before approving.', 'Use first-party Space example to explain size versus permission, with preview caveats.', 'Choose broad maintenance or investigation based on need, not unmeasured savings.'],
                      claimIds=['c-review','c-details','c-duplicates','b-fit','b-approval','b-preview'],
                      interactionPass='Proposed non-mutating decision checklist: which module, selected items, backup, rebuild/download cost, intended method, result versus free-space measure. No runnable deletion commands or forced demo repo.',
                      internalLinks=['/comparisons/cleanmymac/','/comparisons/'], toolLink='Only add relevant cache/rebuild tool after its route and implementation are verified.', wordBudget='900–1400 only if evidence earns it', draftingAllowed=False),
        comparison=dict(title='Breathing Room vs CleanMyMac: cleanup or investigation?',slug='cleanmymac',route='/comparisons/cleanmymac/',
                        intent='Concise Mac purchase/use decision, not a duplicate workflow tutorial.',
                        sections=['Bounded answer and affiliation: Breathing Room, which we build.', 'Claim-adjacent platform, cleanup, monitoring and price matrix with unknown cells.', 'Choose CleanMyMac for its documented broader maintenance tools; verify edition.', 'Consider Breathing Room for source-visible investigation if preview/runtime/hosted boundaries are acceptable.', 'Link deeper review checklist and official documentation.'],
                        linkToArticle='/blog/review-cleanmymac-smart-care-selections/',draftingAllowed=False)),
    judgments=dict(evidenceClass='editorial-judgment, not benchmark',
                   cleanMyMacAdvantages=['Documented multi-module maintenance including malware, app management and duplicates; edition scope matters.', 'Documented one-time current-major purchase option as well as subscriptions.', 'Documented monitors and alerts; do not frame it as blind one-shot cleanup.'],
                   breathingRoomAdvantages=['Source-visible storage/project/app investigation and grouped activity can fit readers wanting context before action.', 'Free local core with separately priced optional AI Care; not evidence of lowest total cost.'],
                   tradeoffs=['Breathing Room remains a non-notarized preview with Python/runtime and hosted-assistant requirements, not a like-for-like replacement for all CleanMyMac modules.', 'CleanMyMac default Smart Care selections require deliberate review; this is not evidence of inferior safety.', 'No speed, safety, savings, detection-rate or privacy superiority established.']),
    unknowns=[dict(field=x, critical=False) for x in ['CleanMyMac full offline/privacy boundaries','CleanMyMac helper grouping','CleanMyMac recurring-path attribution','CleanMyMac architecture-specific runtime and exact permissions','CleanMyMac current exact EULA/repository','CleanMyMac CLI/developer-cache parity; roadmap and directory news are not release proof','Breathing Room installer feature parity, clean-machine and physical-Intel runtime validation']],
    blockers=[
        dict(id='exact-pricing',critical=True,diagnostic='Cannot publish exact currency/term/device/tax/renewal comparison from $3.33/month teaser. Official store returned 403 and Chrome human-verification challenge.', resolution='Independent permitted review of actual public current offer, recording currency, billing term, device count, tax, promo and renewal conditions; no purchase required.'),
        dict(id='competitor-visual',critical=True,diagnostic='Real app screenshot URL identified, but reuse basis not cleared. Official press kit retrieval returned HTTP403; support asset intentionally link-only, not downloaded.', resolution='Obtain accessible vendor-authorized media kit with reuse terms, explicit permission, or an explicitly approved editorial policy decision. Then retain original hash and inspect actual image; no permission message authorized here.')
    ],
    draftingGate=dict(allowed=False, decision='blocked', productSkip=False, independentReview='pending separate stage', diagnostic='Do not create site drafts from this packet until exact pricing and on-page competitor visual rights/access are resolved. Noncritical unknown cells may remain qualified.'),
    validation=dict(command='python3 docs/content/competitors/cleanmymac/build_packet.py', checks=['Reused official snapshot SHA-256 matches verification record', 'Every retained raw official HTML hash matches its collection record', 'Every claim excerpt occurs in its source after whitespace normalization', 'Selected current-source Space PNG hash matches screenshots.json', 'All claim source IDs resolve'],
                    result='passed', marketingBuild='not applicable: no site files edited', browserResult='blocked at store human-verification; owned tab closed; no bypass', nativeTests='not run; research only')
)
extra_matrix_claims = {
    'macOS/platform': ['b-platform'], 'Licence/repository': ['b-license'],
    'Local versus hosted': ['b-local-hosted'], 'Storage inspection': ['c-lens','c-identity'],
    'Process/helper grouping': ['b-activity'], 'Recurring-growth monitoring': ['b-activity'],
    'Developer caches': ['b-dev'], 'Install/runtime': ['b-platform','c-notarization']
}
for row in packet['productMatrix']:
    row['claimIds'].extend(extra_matrix_claims.get(row['dimension'], []))
(ROOT / 'research.json').write_text(json.dumps(packet, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(dict(result='passed', claims=len(claims), sources=len(sources), status=packet['status'], researchSha256=sha(ROOT/'research.json')), indent=2))
