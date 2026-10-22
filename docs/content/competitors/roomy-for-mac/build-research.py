"""Build this job's evidence packet; never installs or executes either app."""
import datetime
import hashlib
import json
from pathlib import Path
import struct
import subprocess

ROOT = Path('/Users/gabe/code/breathing-room-app')
OUT = ROOT / 'docs/content/competitors/roomy-for-mac'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def save(name, obj):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + '\n')
    return str(path.relative_to(ROOT))

batch_path = ROOT / 'docs/content/verification/batch-2.json'
batch = json.loads(batch_path.read_text())
def find_record(value):
    if isinstance(value, dict):
        if value.get('id') == 'roomy-for-mac' and 'facts' in value:
            return value
        for child in value.values():
            found = find_record(child)
            if found: return found
    if isinstance(value, list):
        for child in value:
            found = find_record(child)
            if found: return found
baseline = find_record(batch)
assert baseline
sources = []
for sid, item in [('directory', baseline['discovery']), ('homepage', baseline['sources'][0])]:
    path = ROOT / item['rawCapture']
    assert sha(path) == item['sha256'], f'Prior evidence changed: {path}'
    sources.append(dict(item, id=sid, reused=True, verifiedHash=sha(path)))
home = json.loads((ROOT / baseline['sources'][0]['rawCapture']).read_text())
save('evidence/reused-baseline.json', baseline)

# Excerpts read with WebFetch in this job, not fresh dates assigned to old evidence.
pages = [
 ('press', '/press', 'Press kit', [
  'Use them freely in articles, reviews and videos about Roomy.',
  'Taken from the app on a real Mac, with personal file and app names blurred.',
  'Screenshots may be cropped, resized and annotated.',
  'Roomy is an independent app by TSOFT LLC, not affiliated with or endorsed by Apple Inc.',
  '1.0.0, released October 13, 2026']),
 ('security', '/security', 'Security & Privacy', [
  'Roomy contacts our server only to activate and check a Pro license, and to load current prices for its Plans screen.',
  'Caches, logs and other rebuildable data are deleted, because apps recreate them.',
  'Downloads, backups, archives, large files, duplicates and uninstalled apps go to the Trash, so you can put them back.',
  'One setting sends everything to the Trash.',
  'Roomy doesn’t install launch agents, login items, system extensions or browser extensions.',
  'Quit it and nothing of it keeps running.',
  'Caches of apps that are open, macOS caches, unknown caches over 1 GB and app data are rated Review.',
  'Device backups and Xcode archives are rated Caution.',
  'None of them is ever preselected.']),
 ('changelog', '/changelog', 'What’s new in Roomy', [
  'October 13, 2026', 'First release',
  'Xcode DerivedData, device support, archives, SwiftUI previews and simulator caches, plus npm, Yarn, pnpm, Bun, Deno, Homebrew, pip, Poetry, uv, CocoaPods, Carthage, SwiftPM, Gradle, Maven, Cargo, Go, JetBrains, VS Code and Cursor caches.',
  'Activity Log of every clean, and exclusions for files and folders you never want cleaned.']),
 ('install', '/help/install', 'Install Roomy', [
  "You don't need an account or a license to start: the free version scans your whole Mac and cleans up to 500 MB.",
  'Roomy is sold directly by us, not through the Mac App Store or other download sites.',
  'Full Disk Access is optional.',
  'To update, quit Roomy, download the latest version from the download page, and drag it to Applications again.']),
 ('eula', '/legal/eula', 'End User License Agreement', [
  'Last updated October 13, 2026',
  'The Software is licensed, not sold.',
  'Free version. You may use the Software without a license key to scan your Mac and to clean up to 500 MB in total.',
  'For a Lifetime license, it lasts for the lifetime of the Roomy product, as described in our Terms of Service.',
  'It works offline for up to 21 days between checks; after that, Pro pauses until the Software can reach our server again.',
  'You are responsible for reviewing what you remove and for keeping backups'])
]
for sid, route, title, excerpts in pages:
    source = dict(id=sid, publisher='TSOFT LLC / Roomy', title=title,
        sourceUrl='https://roomymac.com'+route, finalUrl='https://roomymac.com'+route,
        checkedAtUtc=NOW, retrievedOn=NOW[:10], method='WebFetch rendered Markdown, read in this job',
        publicationDate='2026-10-13' if sid in ['changelog','eula'] else None,
        scope='Roomy 1.0.0 public documentation; vendor statements, not runtime verification',
        excerpts=excerpts, rawCapture=None)
    source['excerptRecord'] = save('evidence/'+sid+'-excerpts.json', source)
    sources.append(source)

claims = []
def claim(cid, wording, sid, excerpt, scope='', state='verified', checked=None):
    claims.append(dict(id=cid, wording=wording, sourceIds=[sid],
        sourceUrl=next(s.get('sourceUrl') for s in sources if s['id']==sid),
        excerpt=excerpt, checkedAtUtc=checked or NOW, state=state,
        evidenceClass='officially-documented; not hands-on', scope=scope,
        intendedLocation='workflow article / comparison matrix', reviewer='scheduled research worker',
        unresolvedQuestions=[]))
for i, fact in enumerate(baseline['facts']):
    claim('baseline-'+str(i+1), fact['value'], 'homepage', fact['excerpt'],
          'Reused current batch-2 verification; not re-fetched', checked=fact['retrievedAt'])
for cid, wording, passage in [
 ('review-workflow','Roomy documents Safe, Review and Caution ratings and confirmation before removal.', 'Every item shows what it is, how big it is, where it lives, and a Safe, Review or Caution rating.'),
 ('developer-scope','Roomy documents Xcode and package-manager cleanup.', 'Remove Xcode DerivedData, old device support files and simulator caches, plus npm, Yarn, pnpm, Homebrew, pip, Gradle, Cargo and Go caches.'),
 ('duplicates','Roomy advertises a content-based duplicate finder.', 'Find duplicate files on your Mac by comparing their contents, not their names. The oldest copy is kept.'),
 ('uninstaller','Roomy advertises an app uninstaller including caches, logs and helpers.', 'Uninstall apps on your Mac completely, with the caches, logs and helpers they leave behind.'),
 ('billing-conditions','Pro applies to one Mac; subscriptions renew automatically; lifetime includes future updates. USD, applicable tax included; advertised seven-day money-back guarantee.', 'All future updates included')]:
    assert passage in home['text']
    claim(cid, wording, 'homepage', passage, 'Vendor documentation; no cleanup, purchase or refund tested', checked=home['retrievedAt'])
claim('version','The official changelog identifies 1.0.0 as the first public release, dated October 13, 2026.', 'changelog', 'October 13, 2026 / First release', 'No binary downloaded or tested')
claim('local-hosted','Roomy says scanning stays on the Mac; it contacts its server for Pro checks and current prices.', 'security', pages[1][3][0], 'Policy statement, not network audit. License checks disclose key, hardware hash, Mac name, app version and IP visibility.')
claim('deletion','Roomy documents immediate deletion of rebuildable data, Trash for personal files, and an optional all-to-Trash setting.', 'security', 'Caches, logs and other rebuildable data are deleted, because apps recreate them.', 'Do not promise universal undo; backups and review still matter.')
claim('runtime','Roomy says it installs no background helpers and nothing keeps running after quit.', 'security', 'Quit it and nothing of it keeps running.', 'Not evidence of absence of every in-app monitoring feature.')
claim('install','Roomy is directly distributed; an account is not needed to start, and Full Disk Access is optional.', 'install', 'Full Disk Access is optional.', 'No installer execution; signing, notarization and additional runtime dependencies not independently verified.')
claim('license','Roomy uses a proprietary EULA, with Pro on one Mac and up to 21 days offline between checks.', 'eula', 'It works offline for up to 21 days between checks; after that, Pro pauses until the Software can reach our server again.', 'Lifetime means lifetime of product, not a guarantee of perpetual support. No official source repository identified in inspected links; absence not proven.')
for c in claims:
    if c['id'] == 'billing-conditions':
        c['supportingPassages'] = ['Use on 1 Mac', 'All future updates included', '7-day money-back guarantee',
            '$4.99/month. Renews automatically until you cancel. Cancel anytime.',
            'Prices in US dollars, tax included.']
        assert all(p in home['text'] for p in c['supportingPassages'])
    if c['id'] == 'install':
        c['supportingPassages'] = [pages[3][3][0], pages[3][3][1], pages[3][3][2]]
sources.append(dict(id='br-register', sourceUrl='https://breathing-room.chatic.ai/',
    publisher='Breathing Room first-party evidence register', title='Capabilities evidence register',
    reused=True, checkedOn='2026-10-21', rawCapture='docs/content/capabilities.md',
    verifiedHash=sha(ROOT/'docs/content/capabilities.md'), scope='Source and published disclosures, not native runtime QA'))
for cid, wording, excerpt, locator in [
 ('br-preview', 'Breathing Room is a macOS 13+ preview with Python 3.10+ prerequisite; published release discloses no Developer ID signing or notarization.',
  'Apple Development signed, not Developer ID signed or notarized', 'capabilities.md:46–55; public v0.1.0-preview.1 release'),
 ('br-price', 'Breathing Room has a free local core; advertised AI Care is USD 5/month or 50/year with renewal and applicable-tax caveats.',
  '$5 USD/month', 'capabilities.md:70–86; homepage pricing'),
 ('br-monitor', 'Breathing Room source groups app/helpers and records sampled activity; daily care needs a running app and exact saved approvals.',
  'Saved approvals bind account, API origin, action method/path and native rule', 'capabilities.md:25–32; source code citations retained there'),
 ('br-hosted', 'Breathing Room hosted assistance requires authentication/internet and can send relevant paths/process/storage data.',
  'relevant paths/process/storage data can reach the service and Cloudflare Workers AI', 'capabilities.md:58–68; public privacy policy')]:
    assert excerpt in (ROOT/'docs/content/capabilities.md').read_text()
    claim(cid, wording, 'br-register', excerpt, 'Reused 2026-10-21 evidence; no new runtime verification. '+locator, checked='2026-10-21')

assets = []
for view in ['developer-cleanup', 'clean-confirmation']:
    url = 'https://roomymac.com/images/press/screenshots/'+view+'.png'
    path = OUT / 'assets' / (view+'-original.png')
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        subprocess.run(['curl', '--fail', '--location', '--max-time', '40', '--output', str(path), url], check=True)
    data = path.read_bytes()
    final = url
    content_type = 'image/png (validated PNG signature)'
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    path.write_bytes(data)
    width, height = struct.unpack('>II', data[16:24])
    assets.append(dict(id='roomy-'+view, productId='roomy-for-mac', view=view,
      kind='official-asset', sourcePageUrl='https://roomymac.com/press', assetUrl=url,
      finalAssetUrl=final, retrievedAtUtc=datetime.datetime.fromtimestamp(path.stat().st_mtime, datetime.timezone.utc).isoformat(),
      capturedAtUtc=None, capturedBy='Vendor; exact photographer unknown', productVersion=None,
      buildOrCommit=None, osVersion=None, dataMode='unknown',
      originalPath=str(path.relative_to(ROOT)), originalSha256=sha(path),
      publishedPath=None, publishedSha256=None, widthPx=width, heightPx=height,
      bytes=len(data), contentType=content_type, edits=[],
      privacyReview={'status':'research-reviewed','redactions':[],
        'diagnostic':'Opened actual PNG with image-capable read tool; no account, license key or personal path visible. Confirmation item names are already vendor-blurred; no edits made.'},
      reuse={'status':'cleared','basis':pages[0][3][0], 'evidenceUrlOrPath':'https://roomymac.com/press',
             'credit':'Roomy screenshot courtesy of TSOFT LLC; https://roomymac.com/press'},
      caption='Roomy '+view.replace('-', ' ')+' view, supplied in the official press kit. Vendor capture; exact version, capture date and measurement conditions not supplied. Not our test results.',
      alt=('Roomy Developer view showing Gradle, pnpm, npm, Xcode and Swift Package Manager entries with Safe or Review ratings.' if view=='developer-cleanup' else 'Roomy Clean Safe Items confirmation warning that selected rebuildable data is deleted immediately, with vendor-blurred item names.'),
      supportedClaimIds=['developer-scope' if view=='developer-cleanup' else 'review-workflow'],
      limitations=['Vendor describes real-Mac capture with personal names blurred; not independently reproduced.', 'Publication-specific visual review remains required.'],
      review={'status':'research-visually-inspected; independent page review pending','reviewer':'scheduled research worker','reviewedAtUtc':NOW}))
br = next(a for a in json.loads((ROOT/'docs/content/screenshots.json').read_text())['assets'] if a['id']=='current-space-browser-preview')
assert sha(Path(br['sourcePath'])) == br['sha256']
assets.append(dict(br, selectedFor='Storage classification and size-versus-disposability explanation',
                  inspectedInThisJob=True, publishedPath=None, publishedSha256=None))

unknowns = [
 'Roomy exact screenshot version, OS and capture date: vendor did not supply these.',
 'Roomy Developer ID signing/notarization, executable behavior and performance: not independently verified; do not claim.',
 'Roomy public source repository: none identified in inspected official pages; do not invent a GitHub URL or claim none exists.',
 'Roomy live CPU/helper grouping and recurring storage-growth investigation: not verified, never label No.',
 'Roomy external runtime requirements beyond documented macOS requirement: not verified.',
 '500 MB is total allowance, not a daily/monthly reset. MB unit convention and accounting details not verified.',
 'No purchase, refund, activation, installation, cleanup, native scan or end-to-end comparison performed.',
 'Breathing Room binary parity and runtime caveats remain as documented in capabilities.md; source/UI evidence is not distributed binary QA.'
]
matrix = [
 ('macOS','macOS 14+; Apple silicon and Intel','baseline-3'),
 ('license','Proprietary EULA; no verified official repository','license'),
 ('operation','Local scanning; licensing/pricing requests to vendor','local-hosted'),
 ('scan / cleanup','Caches, build data, app leftovers, duplicates, large files','baseline-2'),
 ('approval','Ratings, review and confirmation','review-workflow'),
 ('helper grouping','not verified',None),
 ('recurring-growth monitoring','not verified',None),
 ('developer caches','Xcode and package-manager categories documented','developer-scope'),
  ('pricing','Free scans + total 500 MB cleanup; USD 4.99/month, 29.99/year or 59.99 once, one Mac','baseline-4'),
 ('removal / undo','Rebuildable data deleted by default; personal files to Trash; optional all-to-Trash','deletion'),
 ('runtime / installation','Direct DMG distribution; optional Full Disk Access; no account needed to start','install')
]
packet = dict(schemaVersion=1, jobId='research-roomy-for-mac', stage='research',
  status='complete-research-pending-independent-review', researchedAtUtc=NOW,
  identity=dict(id='roomy-for-mac', officialName='Roomy', publisher='TSOFT LLC',
    homepage='https://roomymac.com/', repositoryUrl=None, canonicalOwnerId='roomy-for-mac',
    aliases=['Roomy for Mac'], aliasDecision='same product display-name variant; retain one canonical owner',
    skipDecision=False, skipReason=None, powerMyMacRelationship='No alias evidence in corresponding batch record or inspected official identity; do not conflate.',
    classification='direct', rationale='Mac storage cleaner with developer-cache and review-before-removal workflow overlap; not feature-for-feature parity.'),
  ownership=['docs/content/competitors/roomy-for-mac/'],
  discovery=dict(baseline['discovery'], seedUrl='https://alternativeto.net/software/cleanmymac/',
     edgeUrl='https://alternativeto.net/software/cleanmymac/?p=7',
     edgeRetrievedAtUtc='2026-10-21T18:36:45.366Z', edgeRecord='docs/content/competitors.json#roomy-for-mac'),
  reusedVerification=dict(path=str(batch_path.relative_to(ROOT)),sha256=sha(batch_path), unnecessaryRefetch=False),
  sources=sources, claims=claims,
  matrix=[dict(dimension=k,value=v,claimIds=(['baseline-4','baseline-5','baseline-6','baseline-7','billing-conditions','license'] if k=='pricing' else ['baseline-2','developer-scope','duplicates','uninstaller'] if k=='scan / cleanup' else [c] if c else []),state='verified' if c else 'not-verified') for k,v,c in matrix],
  breathingRoomEvidence=dict(register='docs/content/capabilities.md', checkedOn='2026-10-21',
    version='0.1.0-preview.1', limitations=['macOS 13+, universal installer advertised; physical Intel untested',
      'Apple Development signed; not Developer ID signed or notarized per release disclosure',
      'Python 3.10+ required for inventory/legacy scripts; not bundled',
      'Free local core; hosted authenticated AI Care advertised USD 5/month or 50/year',
      'Hosted assistant sends relevant context/tool outputs; not entirely offline',
      'Daily care needs running app and exact saved approvals; optional automatic verified Ruff mode must be qualified'],
    sourceUrls=['https://breathing-room.chatic.ai/','https://breathing-room.chatic.ai/privacy/',
      'https://github.com/bucabay/breathing-room-app/releases/tag/v0.1.0-preview.1']),
  visuals=assets, unknowns=unknowns, criticalBlockers=[],
  draftGate=dict(eligibleForBoundedDraft=True, publicationApproved=False,
     conditions=['Use only documented claims with adjacent citations.', 'Keep unknown cells not verified.',
       'Refresh volatile facts if older than 30 days; independent draft/render review required.',
       'Never present screenshots or vendor language as our tests or guaranteed savings.']),
  briefs={'workflow':dict(title='Review developer caches before deleting: Roomy’s ratings and the rebuild cost',
    slug='review-developer-caches-roomy', primaryIntent='Decide which developer-cache candidates need review before a Mac cleanup',
    track='search/LLM reference', distinctMechanism='Safe/Review/Caution ratings, open-app caches, Xcode archives and immediate deletion versus Trash',
    outline=['Start with rebuildability, not folder size', 'Read Roomy’s rating and removal method',
      'Keep backups and archives distinct from caches', 'Account for rebuild/download cost without invented timings',
      'Choose a local categorized cleanup or a hosted investigation workflow'],
    topVisual='roomy-developer-cleanup', laterVisual='current-space-browser-preview',
    interactionHandoff='A static checklist: data type, open app, rebuild/download cost, backup status, removal method, explicit approval. No filesystem mutation or fake savings estimator.'),
   'comparison':dict(title='Breathing Room vs Roomy: investigation or categorized Mac cleanup',
    slug='roomy-for-mac', primaryIntent='Choose between two Mac maintenance approaches',
    scope='Concise sourced matrix, not a second copy of the developer-cache guide',
    decision='Roomy for documented local categorized cleanup, duplicate finding and uninstalling; Breathing Room for source-documented app/activity investigation and optional hosted assistance, with preview caveats.',
    requiredDisclosure='Breathing Room, which we build',
    internalLinks=['/comparisons/', '/comparisons/roomy-for-mac/', '/blog/review-developer-caches-roomy/'],
    linkStatus='Proposed routes only; verify existence during drafting, no site edits in research.')},
  advantagesAndTradeoffs=[
    'Roomy documents local scan data, no-account free scanning, duplicate finding and app uninstalling; do not invent equivalent Breathing Room capabilities.',
    'Roomy offers a one-time option but limits free cleanup to 500 MB total and Pro to one Mac; lifetime is product lifetime.',
    'Breathing Room source documents helper grouping, sampled activity and saved-approval daily care; not proof of binary parity or forensic attribution.',
    'Breathing Room has a free local core but hosted AI has authentication, data-sharing and advertised paid-care boundaries; preview signing and Python prerequisites matter.',
    'Neither product’s documented approval or Trash model establishes risk-free deletion or measured performance gains.'],
  execution=dict(browserUsed=False, reason='Existing verified discovery plus read-only public documentation and permitted asset downloads were sufficient.',
    assetDownloadDiagnostic='Initial urllib request returned HTTP 403; ordinary curl succeeded for both public press PNGs without authentication/cookies. WebFetch recognized PNG but could not render it.',
    installations=False, cleanup=False, credentialsAccessed=False, websiteChanged=False, independentReview='pending separate stage'))
save('research.json', packet)
print(json.dumps({'claims':len(claims),'sources':len(sources),'visuals':len(assets),'output':str(OUT/'research.json')},indent=2))
