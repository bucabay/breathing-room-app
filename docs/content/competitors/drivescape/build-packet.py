"""Assemble the owned packet from retained evidence; does not fetch or publish."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
batch = load(APP / 'docs/content/verification/batch-1.json')
baseline = next(x for x in batch['products'] if x['id'] == 'drivescape') if 'products' in batch else None
if baseline is None:
    for value in batch.values():
        if isinstance(value, list):
            baseline = next((x for x in value if isinstance(x, dict) and x.get('id') == 'drivescape'), None)
            if baseline: break
assert baseline
manifest = next(x for x in load(APP / 'docs/content/competitors.json')['competitors'] if x['id'] == 'drivescape')
retrievals = load(ROOT / 'source-retrievals.json')
sources = []
for s in retrievals:
    s = dict(s)
    if 'path' in s: s['snapshotPath'] = 'docs/content/competitors/drivescape/' + s.pop('path')
    sources.append(s)
for sid, name in [('baseline-home', 'official'), ('baseline-directory', 'directory')]:
    p = APP / f'docs/content/.runtime/verification-1/drivescape-{name}.json'
    d = load(p)
    sources.append({'id': sid, 'url': d.get('officialUrl') if name == 'official' else d['url'],
                    'finalUrl': d.get('finalUrl', d.get('url')), 'retrievedAtUtc': d['retrievedAt'],
                    'snapshotPath': str(p.relative_to(APP)), 'sha256': sha(p), 'reuse': 'Existing same-day verification; not re-fetched for already-verified facts.'})
for sid, path in [('br-capabilities','docs/content/capabilities.md'), ('br-visuals','docs/content/screenshots.json')]:
    p = APP / path
    sources.append({'id':sid,'url':None,'snapshotPath':path,'sha256':sha(p),'checkedOn':'2026-10-21','reuse':'Same-day first-party evidence register; source implementation is not binary testing.'})
for name in ['listing-visuals-browser.json','listing-visuals-snapshot.txt']:
    p = ROOT / 'sources' / name
    sources.append({'id':name,'url':baseline['discovery']['sourceUrl'],'snapshotPath':str(p.relative_to(APP)), 'sha256':sha(p),'retrievedAtUtc':now,'timestampNote':'Recorded at packet assembly after owned-tab DOM inspection; not vendor capture date.'})
byid = {s['id']:s for s in sources}
claims = []
def claim(cid, wording, source, excerpt, scope, location='comparison matrix', evidence='vendor-documented'):
    s = byid[source]
    claims.append({'id':cid,'wording':wording,'state':'verified','evidenceClass':evidence,
                   'sourceIds':[source],'sourceUrl':s['url'],'excerpt':excerpt,
                   'checkedAtUtc':s.get('retrievedAtUtc',s.get('checkedOn')),
                   'scope':scope,'intendedLocation':location,'reviewer':'research-drivescape worker; not independent publication review'})
claim('identity','DriveScape is published by BrickLogic (Vadym Kovalsky).','press','BrickLogic — Vadym Kovalsky, solo developer, Ukraine','Official product identity; no relationship to PowerMyMac established.')
claim('license','DriveScape is proprietary; its public repository hosts releases, not app source.','press',"“Open source” — it's proprietary; the releases repo on GitHub hosts binaries, not source.",'Do not infer open-source rights from GitHub availability.')
claim('repo','The official release/issue repository is BrickLogic/ChartyDriveReleases.','repository','DriveScape — Releases & Issues','Official press kit links here; README links back to drivescape.dev. Repository spelling is not proof of a historical product rename.')
claim('mac','DriveScape advertises macOS 11+ on Apple Silicon, not Intel Macs.','press','macOS 11+ (Apple Silicon)','Not runtime-tested; do not turn native cross-platform marketing into Intel support.')
claim('other-platforms','DriveScape advertises Windows 10/11 x64 and Linux x64 AppImage builds.','press','Windows 10/11 x64 (code-signed) · Linux x64 (AppImage)','Advertised support only; latest GitHub release queried here lists Mac assets only. Windows/Linux current installer availability and parity unverified.')
claim('version','The official changelog identifies v1.11.0, dated September 20, 2026, as latest.','changelog','v1.11.0 Latest 20 September 2026','GitHub latest-release API agrees: v1.11.0, published 2026-09-20T18:22:14Z; no binary installed.')
claim('pricing','DriveScape Pro costs US$8 once for every machine the buyer owns or controls, for personal or business use.','eula','DriveScape Pro is a one-time purchase of US$8','EULA sections 2, 5 and 7: perpetual current-major-version licence; future major versions may cost extra. Paddle handles taxes; tax-inclusive final total not checked.')
claim('major-upgrades','The licence covers the current major version plus minor updates and bug fixes; future major versions may be sold separately.','eula','A future major version may be offered as a separate purchase.','Do not promise all future versions for $8; marketing use-forever wording must carry this condition.')
claim('free-trial','Scanning, sunburst, lists, Trends and duplicate finding remain free; Pro actions have a seven-day trial then an $8 unlock.','baseline-home','The entire visual side is\nfree forever\n: scanning, the sunburst, the largest-files lists, trends and the duplicate finder','Trial activation asks for email; no card/account advertised. Deduplication actions are paid after trial, unlike finding duplicates.')
claim('trial-data','Requesting the trial sends an email address and a hash of a hardware identifier; the vendor uses these to enforce one trial per person/device.','privacy','the email address you enter, and a one-way cryptographic hash of a hardware identifier','Policy disclosure, not a privacy/network audit; do not equate no account with no data sent.')
claim('local','DriveScape documents local scans and cleanup without an account or cloud AI.','privacy','All of that work happens locally, on your computer.','Vendor policy only. Launch-time licence checks transmit a token containing purchase email/order reference; update checks send version/OS/architecture; optional bug reports become public issues. Do not say zero network traffic.')
claim('sunburst','DriveScape documents selecting a folder or disk, then exploring a clickable sunburst.','how-it-works','Click any ring to zoom in; the biggest wedges are the biggest space hogs.','Documented UI, not speed/completeness benchmark.')
claim('approval','DriveScape documents staging/review, risk labels and a Trash-first cleanup workflow.','how-it-works',"You confirm before anything happens.",'No execution tested. Homepage also mentions optional permanent deletion with confirmation; do not state all actions are always reversible, or that emptying Trash preserves undo.')
claim('dev','DriveScape documents identifying developer caches/build artifacts including node_modules, Docker, Xcode DerivedData and cargo/npm/pip.','press','caches, build artifacts (node_modules, Xcode DerivedData, cargo/npm/pip)','Risk tiers are vendor labels, not permission to delete personal data or guarantees that rebuilding succeeds.')
claim('duplicates-sweep','DriveScape documents APFS-clone-aware duplicates, a leftovers uninstaller, Sweep Downloads triage and Trends.','press','Includes a duplicate finder that understands APFS clones','Feature documentation, not hands-on validation; uninstaller is macOS-only per same-day homepage/changelog.')
claim('trends','DriveScape documents a snapshot for each scan and comparison with the previous scan.','baseline-home','Every scan becomes a snapshot - see whether the disk is growing and what changed since last time.','Do not claim it lacks growth history. Background/continuous process ownership tracking is not established by this passage.')
claim('shields','Shields is described as an optional subscription coming with DriveScape 2.0; its price is not yet announced.','press','optional subscription coming with DriveScape 2.0 - price announced at launch','Planned, not verified shipped. Press boilerplate sounds present-tense; explicit Facts/FAQ release conditions take precedence. Exclude security comparisons from this Mac storage article.')
claim('install','The official release README advertises a notarized Apple Silicon DMG.','repository','macOS — notarized .dmg (Apple Silicon)','Vendor disclosure only: no signature/notarization inspection or installation. Press says direct-download only; Full Disk Access may be relevant, do not change permissions.')
claim('br-preview','Breathing Room is a macOS 13+ maintenance preview, identified as 0.1.0-preview.1, with Apple Silicon/Intel universal installer advertised.','br-capabilities','macOS 13+; universal Apple Silicon/Intel installer advertised.','Same-day evidence register: physical Intel and clean-machine runtime untested; Apple Development signed, not Developer ID signed or notarized; Python 3.10+ prerequisite. Source does not prove installer feature parity.',evidence='reused-first-party-register')
claim('br-workflow','Breathing Room source implements storage exploration, helper-grouped CPU/memory monitoring, activity history and approval-bound daily care.','br-capabilities','Source supports category, app/tool-owner, project, folder and large-file views.','Source-level only; permission-limited inventories and inferred ownership. Daily care requires app running; exact saved approvals; optional narrowly verified Ruff automatic mode is an exception to blanket approval language.',evidence='reused-first-party-register')
claim('br-pricing-hosted','Breathing Room advertises a free core app and optional AI Care at $5 USD/month or $50 USD/year; AI uses authentication and a hosted service.','br-capabilities','Confirmed advertised $5 USD/month, $50 USD/year.','Same-day register and cited live pages; renewals/tax apply. Hosted service allowance/enforcement not verified. Website download account gate differs from direct public GitHub downloads.',evidence='reused-first-party-register')
claim('br-license','Breathing Room desktop source is Apache-2.0; this does not licence its hosted service.','br-capabilities','Desktop source is Apache License 2.0 with NOTICE and preserved third-party attribution.','No free hosted-service entitlement inferred.',evidence='reused-first-party-register')
claim('br-dev','Breathing Room source discovery includes npm, uv, pip, pnpm, Go, Bun and Yarn caches.','br-capabilities','Discovery includes queries for npm, uv, pip, pnpm, Go build/module, Bun and Yarn caches','Source implementation only; installed tools, native path/method validation and permissions constrain availability.',evidence='reused-first-party-register')
matrix = {
 'macOS compatibility': ['mac','br-preview'], 'licence': ['license','pricing','major-upgrades','br-license'],
 'local versus hosted': ['local','trial-data','br-pricing-hosted'], 'scan and cleanup': ['sunburst','approval','br-workflow'],
 'approval controls': ['approval','br-workflow'], 'helper CPU/memory grouping': {'drivescape':'not verified','breathingRoomClaimIds':['br-workflow']},
 'recurring growth': ['trends','br-workflow'], 'developer caches': ['dev','br-dev'],
 'pricing': ['pricing','major-upgrades','free-trial','shields','br-pricing-hosted'],
 'runtime/install caveats': ['install','mac','other-platforms','br-preview'],
 'duplicate finder and uninstaller': {'drivescapeClaimIds':['duplicates-sweep'],'breathingRoom':'not verified as equivalent in capability register'}
}
preview = next(x for x in load(APP / 'docs/content/screenshots.json')['assets'] if x['id']=='current-space-browser-preview')
assert sha(Path(preview['sourcePath'])) == preview['sha256']
visual = {'id':'drivescape-listing-app-ui','productId':'drivescape','kind':'listing-asset',
 'view':'Listing labels it DriveScape screenshot 1; exact view/version not independently visually reviewed',
 'sourcePageUrl':baseline['discovery']['sourceUrl'],
 'assetUrl':'https://img.alternativeto.net/s/618x394/avif/drivescape_348518_full.png',
 'alternativeAssetUrls':['https://img.alternativeto.net/s/618x394/avif/drivescape_303678_full.png','https://img.alternativeto.net/s/618x394/avif/drivescape_261023_full.png'],
 'capturedAtUtc':None,'retrievedAtUtc':None,'sourcePageInspectedAtUtc':now,'capturedBy':None,'productVersion':None,
 'dataMode':'unknown','originalPath':None,'originalSha256':None,'publishedPath':None,'publishedSha256':None,
 'edits':[],'privacyReview':{'status':'pending','redactions':[]},
 'reuse':{'status':'link-only','basis':'No explicit screenshot republication licence established. Public availability and listing upload do not grant rights. Press kit supplies logo/social assets, not app screenshots or permission covering these listing assets. No image bytes downloaded.', 'evidenceUrlOrPath':'https://drivescape.dev/press','credit':'DriveScape / BrickLogic; screenshot reference via AlternativeTo'},
 'caption':'DriveScape app screenshot supplied on AlternativeTo. Vendor/listing image; version, capture date and example-versus-measured data are unverified. Link only pending reuse clearance.',
 'alt':'DriveScape app screenshot linked from its AlternativeTo listing; view requires visual verification.',
 'supportedClaimIds':[],'limitations':['Not an approved on-page visual. No inferred screenshot rights, source dimensions, native capture or hands-on experience.','Homepage animated/example marketing UI and press logo/social card are not substitutes for a real app screenshot.'],
 'review':{'status':'pending','reviewer':None,'reviewedAtUtc':None}}
brvisual = dict(preview)
brvisual.update(productId='breathing-room',originalPath=preview['sourcePath'],originalSha256=preview['sha256'],publishedPath=None,publishedSha256=None,
 review={'status':'research-visually-inspected','reviewer':'research-drivescape worker','reviewedAtUtc':now},
 requiredLabels=['Current-source browser preview','Example data only','Not a native scan, measured activity or cleanup result'],
 visualDiagnostic='Opened actual PNG: example-data banner visible, category and project views illustrated; floating composer overlaps chart. Keep disclosure; assess contextual crop and mobile readability in draft review.')
brief = {'track':'search/LLM reference; workflow-first','status':'blocked-not-a-draft',
 'title':'Review node_modules and build caches before reclaiming Mac storage',
 'slug':'review-node-modules-build-caches-mac','primaryIntent':'Decide which generated project artifacts are rebuildable before using tiered cleanup, then check whether growth returns.',
 'audience':'Apple Silicon Mac developers investigating project/build-cache growth; not a Windows replacement article.',
 'distinctMechanism':'Use DriveScape risk-tiered staging and scan snapshots to distinguish project outputs, shared package stores and potentially irreplaceable Docker/virtual-environment data. Contrast Breathing Room owner/project views and ongoing investigation without claiming it implements the same sunburst or duplicate engine.',
 'proposedLead':'Start by separating rebuildable project outputs from shared stores and original data. DriveScape documents a tiered, review-first workflow; labels and file sizes do not establish that a folder is disposable.',
 'sections':['Locate a heavy project with a disk map; numbers in vendor demos are examples, not our results.', 'Classify project output versus shared store versus original data; check manifests, backups and rebuild/download cost.', 'Review exact locations and Trash versus permanent-delete behavior; do not execute cleanup for article research.', 'Re-scan to compare snapshots; history is not writer attribution.', 'Choose one-off visual cleanup or continuing app/activity investigation; disclose Breathing Room affiliation and preview/hosted caveats.'],
 'visualPlacement':['Cleared real DriveScape app UI immediately after lead; currently blocked.','Selected Breathing Room Space browser preview later, with example/native disclosure.'],
 'interactionPass':'Hand off a local checklist/decision aid: manifest present? backup? rebuild cost? shared store/volume? Answer unknown routes to review, never automatic deletion. No filesystem access or invented size estimates.',
 'links':['/comparisons/','/comparisons/drivescape/','/tools/ (select an existing relevant tool only after route verification)'],
 'avoid':['Measured scan speed/savings','All SAFE-tier files universally disposable','No DriveScape history','All Breathing Room data stays local','Universal Intel compatibility for DriveScape','Claims of testing either binary']}
comparison = {'status':'blocked-not-a-draft','title':'Breathing Room vs DriveScape: Mac storage workflows','slug':'drivescape',
 'primaryIntent':'Choose between a documented sunburst/staged-cleanup workflow and a broader Mac maintenance preview with app/activity investigation.',
 'format':'Concise conclusion, sourced matrix, when to choose each, preview/pricing/install caveats, deeper workflow link.',
 'claimIds':[c['id'] for c in claims], 'matrix':matrix,
 'disclosure':'Breathing Room, which we build. Source/documentation comparison only; no hands-on competitor test.',
 'links':['/comparisons/','/blog/review-node-modules-build-caches-mac/'],
 'notAReplacementFor':'Do not imply Breathing Room runs on Windows/Linux or duplicates every DriveScape tool.'}
blockers = [{'id':'competitor-visual-rights','severity':'critical','blocks':['drafting','publication'],
 'diagnostic':'Real DriveScape screenshot URLs are recorded from the authoritative listing, but no explicit reuse basis, image-byte provenance, version or visual/privacy approval is established. Press kit contains logos/social card only. Link-only fallback does not satisfy EDITORIAL.md image gate.',
 'resolution':'Obtain explicit authorised reuse permission/licence for a real app screenshot (with source/capture provenance), or an explicit policy decision permitting another approach. Do not contact vendor in this job. Then download only permitted asset bytes, hash originals, inspect UI/privacy and review captions.'}]
packet = {'schemaVersion':1,'jobId':'research-drivescape','productId':'drivescape','checkedAtUtc':now,
 'status':'blocked','stage':'research','draftingAllowed':False,'published':False,
 'identity':{'officialName':'DriveScape','homepage':'https://drivescape.dev/','publisher':'BrickLogic','repository':'https://github.com/BrickLogic/ChartyDriveReleases','repositoryType':'release binaries and issues, not app source','canonicalOwnerId':'drivescape','aliases':[],
 'aliasDecision':{'status':'keep-distinct','skipSeparateAliasDrafts':True,'verifiedDuplicateIds':[], 'rationale':'Official press and repository identify DriveScape consistently. ChartyDriveReleases is the linked repository name, not verified as a separate product or former marketing name. PowerMyMac has no evidenced relationship; no merger or separate alias article authorised.'},
 'classification':'direct-storage-cleanup-overlap','platformFit':'Mac eligible; macOS 11+ Apple Silicon. Broader app/process/AI workflows are adjacent, not feature-equivalent.',
 'skipDecision':{'skipProduct':False,'reason':'Live official product and Mac storage/cleanup overlap verified; block drafting for rights rather than invent doorway content.'}},
 'ownership':['docs/content/competitors/drivescape/'],
 'baselineReuse':{'path':'docs/content/verification/batch-1.json','sha256':sha(APP / 'docs/content/verification/batch-1.json'),'recordId':'drivescape','reusedFields':['officialName','officialUrl','platforms','pricing','availability','discovery'],'newResearchReason':'Resolve missing licence conditions, exact Mac platform/version, repo identity and screenshot rights.'},
 'discovery':{**baseline['discovery'],'edges':manifest['edges'],'rawSnapshotSha256':sha(APP / baseline['discovery']['snapshotPath']),'method':'Reused same-day rendered discovery; owned Chrome tab inspected only for missing screenshot URLs after HTTP 403. No CAPTCHA bypass, cookies or hidden state extracted.'},
 'sources':sources,'claims':claims,'productMatrix':matrix,'visuals':[visual,brvisual],
 'briefs':{'workflowArticle':brief,'comparison':comparison},
 'advantagesAndTradeoffs':{'drivescape':['Documented sunburst, clone-aware duplicates, Sweep and leftover-app cleanup; useful for one-off visual storage review.','US$8 current-major-version licence across owned/controlled machines; free visual exploration. Optional future Shields subscription is separate.','Apple Silicon only on Mac. Trial requires email and hashed device identifier. No independent performance, safety, install or privacy audit performed.'],
 'breathingRoom':['Source-level app/helper CPU/memory and local activity investigation may suit continuing maintenance; not proof a process wrote a particular file.','Free core with optional recurring AI Care; authenticated hosted reasoning is not fully offline.','Non-notarized preview with Python prerequisite and untested clean-machine/Intel behavior; not a production-readiness recommendation.']},
 'unknowns':['No distributed-binary tests, timing, recovered-space measurements, privacy audit or permissions changes performed.','DriveScape helper/process grouping and continuous background attribution not verified; do not mark No.','Latest GitHub release lists Mac-only assets; current Windows/Linux downloads and feature parity unverified.','No independent notarization/signature inspection for DriveScape.','Shields 2.0 availability and price unverified/planned; exclude from shipped-feature rows.','Final checkout tax-inclusive total, payment/activation/refund execution and future upgrade prices not tested.','Competitor screenshot version/date/rights and narrow-screen legibility pending.','Breathing Room source-versus-release feature parity remains unverified per same-day capabilities register.'],
 'sourceQualifications':['Marketing says use forever; EULA limits included upgrades to current major version. Preserve both scope and price.','Homepage says Trash-first but also optional permanent deletion. Describe default review/Trash flow, not guaranteed reversibility.','Press mentions Shields network downloads; privacy/EULA describe existing disk tools. Treat Shields as planned rather than silently importing future behavior.','Homepage numbers, scan animations, safety-verifier illustration and mock typical-cleaner comparison are marketing examples, not our tests.'],
 'blockers':blockers,'independentReview':{'status':'pending','score':None},
 'safety':{'nativeAppLaunched':False,'cleanupPerformed':False,'imageBytesDownloaded':False,'signupsPurchasesMessages':False,'siteEdited':False,'queueEdited':False,'agentsSpawned':False}}
(ROOT / 'research.json').write_text(json.dumps(packet,indent=2,ensure_ascii=False)+'\n')
lines = ['# DriveScape research packet', '',
    '**Research retained; drafting BLOCKED. Not a draft, review approval or publication.**', '',
    f'Checked: {now}. Job: `research-drivescape`. Only this competitor folder and the required runtime receipt are owned.', '',
    '## Decision and identity', '',
    'DriveScape is a live BrickLogic product with direct Mac storage-analysis/cleanup overlap. Keep canonical owner `drivescape`; do not skip the product as dead or irrelevant. The official homepage is https://drivescape.dev/ and its official binary/issue repository is https://github.com/BrickLogic/ChartyDriveReleases. It is proprietary, not open source.', '',
    'No verified separate alias. The repository name is not enough to assert a former ChartyDrive product identity. Skip separate alias drafts; no evidence connects PowerMyMac to DriveScape. No other competitor was researched or changed.', '',
    'Mac fit: macOS 11+ Apple Silicon only (vendor documentation). Breathing Room is Mac-only here; no Windows/Linux support is invented. Broader process/activity investigation is adjacent, not full feature equivalence.', '',
    '## Critical blocker', '',blockers[0]['diagnostic'], '', '**Required next action:** '+blockers[0]['resolution'], '',
    '## Reused verification and discovery', '',
    '`docs/content/verification/batch-1.json` record `drivescape` was read first. Same-day official homepage/discovery snapshots were reused, not fetched again to repeat name, headline, price or platform verification. New requests cover missing licence/version/repository/privacy detail and visual provenance; raw responses are retained and hashed in research.json.', '',
    f"Discovery: {baseline['discovery']['sourceUrl']} at {baseline['discovery']['retrievedAt']}. The listing's official link points to https://drivescape.dev/.", '',
    'Traversal edges: CleanMyMac page 5 and Mole page 4, retained with exact URLs/timestamps in research.json. The directory proves discovery, not capabilities. An ordinary HTTP request for missing listing visuals returned 403; an owned existing-profile Chrome tab rendered the public listing without login/CAPTCHA bypass. DOM-visible image URLs were retained; the owned tab was closed, other tabs untouched.', '',
    '## Claim ledger', '', 'All passages below are source/documentation evidence, not our runtime tests. Every claim has its actual checked time and scope in research.json. Local register claims inherit same-day verification; they were not re-certified against binaries.', '']
for c in claims:
    lines += [f"### {c['id']}", '',c['wording'], '',f"Source: {c['sourceUrl'] or byid[c['sourceIds'][0]]['snapshotPath']} · checked {c['checkedAtUtc']} · {c['evidenceClass']}", '', '> '+c['excerpt'].replace('\n',' '), '', '**Conditions:** '+c['scope'], '']
lines += ['## Comparison matrix handoff', '', '| Dimension | Evidence / treatment |','| --- | --- |']
for key,val in matrix.items():
    lines.append('| '+key+' | '+((', '.join(val)) if isinstance(val,list) else json.dumps(val))+' |')
lines += ['', 'Unknown is not No. Every factual row must cite the corresponding claim IDs beside the claim, not only in a bibliography.', '',
    '## Visuals', '',
    '**Competitor, link-only:** '+visual['assetUrl'], '',
    'Source page: '+visual['sourcePageUrl']+'. Other app-image URLs are in research.json. The listing labels these as DriveScape screenshots; exact app view, version, capture date and data mode have not been independently inspected. No bytes downloaded, no original hash invented. The press kit offers a logo and social card, neither satisfies the app-UI gate. Public availability does not establish republication rights.', '',
    '**Selected Breathing Room view:** `'+preview['sourcePath']+'`', '',
    'SHA-256: `'+preview['sha256']+'`. Existing PNG opened and visually inspected; hash matches screenshots.json. Retained first-party source, build commit, timestamp and reuse basis are copied into research.json; no duplicate asset or site record was created.', '',
    '**Required caption:** '+preview['caption'], '',
    '**Alt:** '+preview['alt'], '',
    'Keep the example-data banner and disclosure. This is the current-source browser preview captured October 21, not a current native-release screenshot or measured result. Floating composer overlaps part of the chart: crop/context and mobile readability require later review. No image changes made.', '',
    '## Distinct workflow article brief', '',f"**Working title:** {brief['title']}\n\n**Proposed slug:** `{brief['slug']}`\n\n**Track:** {brief['track']}\n\n**Intent:** {brief['primaryIntent']}", '',
    '**Mechanism:** '+brief['distinctMechanism'], '', '**Lead direction (not article copy):** '+brief['proposedLead'], '']
lines += [f'{i}. {section}' for i,section in enumerate(brief['sections'],1)]
lines += ['', '**Visual placement:** '+' '.join(brief['visualPlacement']), '', '**Interaction handoff:** '+brief['interactionPass'], '',
    'No forced demo repo, commands that delete data, artificial FAQ, benchmark quota or invented hands-on narrative. Include contextual comparison/hub links; verify any tool route before linking.', '',
    '## Concise comparison brief', '',f"**Title:** {comparison['title']}\n\n**Route:** `/comparisons/drivescape/`\n\n**Intent:** {comparison['primaryIntent']}", '',
    'Use a short conclusion, claim-linked matrix and two bounded decision cases. DriveScape may fit visual map/duplicate/Sweep review without hosted AI; Breathing Room, which we build, may fit continuing Mac app/activity investigation, subject to preview/runtime and hosted-service limits. Do not claim superiority or that either tool replaces every function of the other. Link the deeper workflow article rather than expanding its checklist into duplicate content.', '',
    '## Advantages and trade-offs', '']
for product,items in packet['advantagesAndTradeoffs'].items():
    lines += ['### '+product,''] + ['- '+x for x in items]+['']
lines += ['## Conflicts and unknowns','']+['- '+x for x in packet['sourceQualifications']]+['']+['- '+x for x in packet['unknowns']]+['',
    '## Safety, validation and handoff', '',
    'No native app launch/install, cleanup, binary download, signup, purchase, message, permission request, credentials read, hidden browser extraction, commit, push or deployment. No site/queue/database edits and no agents. Source responses and research outputs remain local to this folder. No publication quality score is awarded and independent review remains pending.', '',
    'Actual structural, hash and source-excerpt validation outcomes are retained in `validation.json`; the final job receipt reports blocked. Site builds were not run because no site content changed. Clearing the screenshot gate requires independent subsequent work; a link-only source is not a waiver.', '']
(ROOT / 'research.md').write_text('\n'.join(lines))
print('Wrote research.json:',len(claims),'claims;',len(sources),'sources; drafting blocked by competitor image gate.')
