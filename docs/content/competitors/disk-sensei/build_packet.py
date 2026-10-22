"""Assemble a documentary packet from retained evidence, without network access."""
import datetime
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
PREFIX = 'docs/content/competitors/disk-sensei/'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load(path):
    return json.loads(Path(path).read_text())

baseline = next(p for p in load(APP / 'docs/content/verification/batch-2.json')['records'] if p['id'] == 'disk-sensei')
official = load(APP / baseline['sources'][0]['rawCapture'])
manifest = load(APP / 'docs/content/competitors.json')
product = next(p for p in manifest['competitors'] if p['id'] == 'disk-sensei')
sources = load(ROOT / 'sources/index.json')
for source in sources:
    source['snapshotPath'] = PREFIX + source['snapshotPath']
    source['publisher'] = 'Cindori AB'
    if source['id'] == 'vendor-comparison':
        source['publicationDate'] = '2026-08-14'
    elif source['id'] == 'release-1.6':
        source['publicationDate'] = '2025-05-17'
    if source['id'] != 'press-kit':
        source['textPath'] = source['snapshotPath'].replace('.html', '.txt')
        source['textSha256'] = sha(APP / source['textPath'])
        source['scope'] = 'Official published documentation; not hands-on validation.'
sources += [dict(id='baseline-official', publisher='Cindori AB',
    url=official['url'], finalUrl=official['finalUrl'], retrievedAtUtc=official['retrievedAt'],
    snapshotPath=baseline['sources'][0]['rawCapture'], sha256=sha(APP / baseline['sources'][0]['rawCapture']),
    reusedFrom='docs/content/verification/batch-2.json', scope='Current baseline reused, not re-fetched.'),
    dict(id='baseline-directory', publisher='AlternativeTo', url=baseline['discovery']['sourceUrl'],
    retrievedAtUtc=baseline['discovery']['retrievedAt'], snapshotPath=baseline['discovery']['rawCapture'],
    sha256=sha(APP / baseline['discovery']['rawCapture']), scope='Discovery only; no capability claims.'),
    dict(id='br-capabilities', publisher='Breathing Room', url='https://breathing-room.chatic.ai/',
    snapshotPath='docs/content/capabilities.md', sha256=sha(APP / 'docs/content/capabilities.md'),
    retrievedAtUtc=None, checkedDate='2026-10-21', scope='Reuse source/published verification register; binary parity not established.'),
    dict(id='br-readme', publisher='Breathing Room', url='https://github.com/bucabay/breathing-room-app',
    snapshotPath='README.md', sha256=sha(APP / 'README.md'), retrievedAtUtc=None,
    checkedDate=NOW[:10], scope='Current local README re-read; no app run or binary validation.'),
    dict(id='br-ui', publisher='Breathing Room', url=None, snapshotPath='src/components/cleanup-assistant.tsx',
    sha256=sha(APP / 'src/components/cleanup-assistant.tsx'), checkedDate=NOW[:10],
    scope='Current source, not distributed binary validation.')]
by_source = {s['id']: s for s in sources}
claims = []

def claim(cid, wording, sid, excerpt, scope, location='comparison matrix', state='verified'):
    source = by_source[sid]
    if state == 'verified' and sid not in ('br-capabilities', 'br-readme', 'br-ui'):
        text = official['text'] if sid == 'baseline-official' else (APP / source.get('textPath', source['snapshotPath'])).read_text()
        assert excerpt in text, (cid, excerpt)
    claims.append(dict(id=cid, wording=wording, sourceIds=[sid], sourceUrl=source.get('finalUrl', source.get('url')),
        excerpt=excerpt, checkedAtUtc=source.get('retrievedAtUtc') or NOW,
        checkedDate=source.get('checkedDate') or (source.get('retrievedAtUtc') or NOW)[:10],
        evidenceClass='officially-documented' if not sid.startswith('br-') else 'source-and-register-inspection',
        scope=scope, state=state, intendedLocation=location, reviewer='research-disk-sensei worker'))

claim('S01', 'Cindori markets Sensei as a Mac system monitoring utility.', 'baseline-official',
    'The All-in-One Mac System Performance Monitoring Tool.', 'Vendor positioning, not measured superiority.', 'identity/lead')
claim('S02', 'The product page documents Intel and Apple Silicon Mac support.', 'baseline-official',
    'Get in-depth insights into system performance and hardware health for Intel and Apple Silicon Macs.', 'No native compatibility testing performed.')
claim('S03', 'Sensei offers customizable status-bar/dropdown monitoring panels.', 'baseline-official',
    'Customize widgets for the status bar or dropdown panel, and create personalized monitoring dashboards with your own design and tracking preferences.', 'Documented feature; no performance test.')
claim('S04', 'Sensei documents removal of caches, logs, large downloads and leftover installation files.', 'baseline-official',
    'including old caches, system logs, large downloads, and leftover installation files.', 'Does not establish safety, completeness, exact current deletion semantics or measured savings.')
claim('S05', 'Sensei documents app uninstallation with related leftover files.', 'baseline-official',
    'Remove Apps and Their Leftover Files.', 'Vendor feature claim, not proof every leftover is removed.')
claim('S06', 'Sensei documents drive S.M.A.R.T. analysis.', 'baseline-official',
    'The Drive Health Report in Sensei will provide you with a S.M.A.R.T analysis of your storage.', 'No guarantee of failure prediction or support for every drive/enclosure.')
claim('S07', 'Sensei documents battery-health, thermal and disk-benchmark tools.', 'baseline-official',
    'Sensei’s Disk Benchmark tool measures the read and write speeds of your Mac’s storage with a single click.', 'Other supporting sections: MacBook Battery Health Monitoring; Real-Time Mac Thermal Monitoring. No benchmark executed.')
claim('S21', 'Sensei documents battery cycle count, capacity and real-time performance insights.', 'baseline-official',
    'including cycle count, capacity, and real-time performance.', 'Vendor documentation; not an observed battery-health measurement.')
claim('S22', 'Sensei documents CPU/GPU temperatures, fan speeds and system heat views.', 'baseline-official',
    'Monitor CPU and GPU temperatures, fan speeds, and system heat levels to diagnose hardware issues.', 'Documented monitoring, not proof of a diagnosis or fan control on all hardware.')
claim('S08', 'The store displays $29 billed annually for up to three Macs.', 'store',
    'Valid for up to 3 Macs.\n$29\nBilled annually.', 'Dollar symbol as displayed; ISO currency, taxes and checkout localization unverified. Not a free app.')
claim('S09', 'The store displays $59 as a one-time purchase for up to three Macs.', 'store',
    'Valid for up to 3 Macs.\n$59\nOne Time Purchase.', 'Do not call it lifetime updates or normalize to USD without evidence.')
claim('S10', 'The regular licence includes updates to versions 1 and 2; version 3 onward may be paid upgrades.', 'store',
    'The Regular License grants you access to all upcoming updates to the current major version of Sensei (1), as well as version 2. Version 3 and onwards may be a paid upgrade.',
    'Store still calls 1 current; newer vendor article discusses 2.1.2. Preserve explicit update entitlement, not the stale current-version label.')
claim('S11', 'The subscription licence key expires if the subscription expires without renewal.', 'store',
    'If your subscription expires and is not renewed, your license key will expire.', 'No paid subscription tested.')
claim('S12', 'The advertised refund window ends at activation even if fewer than fourteen days have elapsed.', 'store',
    'Refunds are available within 14 days of purchase before license activation.', 'Do not advertise an unconditional fourteen-day money-back guarantee.')
claim('S13', 'Licences are per user, up to three machines where that person is the primary user; businesses need enough licences for their users.', 'eula',
    'Licenses are per user and valid for use on all supported operating systems.', 'Supporting same paragraph limits to 3 unique machines and says businesses need at least as many licences as users. Not three unrestricted business seats.')
claim('S14', 'Cindori owns the software copyright and supplies a commercial EULA.', 'eula',
    'All title, including but not limited to copyrights, in and to SOFTWARE PRODUCT and any copies thereof are owned by CINDORI AB.', 'Treat as proprietary commercial licensing; no official open-source repository established.')
claim('S15', 'A vendor article dated August 14, 2026 identifies Sensei 2.1.2 and macOS 14+.', 'vendor-comparison',
    'Current Sensei 2.1.2 requires macOS 14 Sonoma or later', 'Version-specific vendor documentation, not proof of the latest downloadable build in October. Hardware/runtime not tested.')
claim('S16', 'Cindori provides Sensei 1.5.10 for older Macs and warns it may have more bugs.', 'older-versions',
    'Download Sensei 1.5.10', 'The same page says Catalina was supported at launch but minimum OS has since risen. Never apply 10.15 to current Sensei.')
claim('S17', 'Sensei 1.6 introduced an approved LaunchDaemon and integrated the menu-bar monitor into the main app.', 'release-1.6',
    'Sensei 1.6 replaces the helper tool with a modern LaunchDaemon.', 'May 17, 2025 release-specific architecture. Do not infer exact 2.x onboarding from this history.')
claim('S18', 'Disk Sensei and Sensei are related but separately introduced products in Cindori’s history.', 'about',
    'We released Disk Sensei, a comprehensive disk utility to monitor drive health, analyze storage usage, and optimize performance', 'About timeline: Disk Sensei 2015; Sensei 2019. Do not claim a simple rename or identical binaries.', 'alias resolution')
claim('S19', 'Cindori offers an upgrade from Disk Sensei or Trim Enabler to Sensei.', 'upgrade',
    'Purchased Trim Enabler or Disk Sensei in the past? Upgrade to Sensei at up to 50% off.', 'Separate predecessor/upgrade relationship, not proof Trim Enabler is the same product. Eligibility requires prior purchase verification; no form submitted.', 'alias resolution')
claim('S20', 'The vendor article says some Sensei cleaning features require Full Disk Access.', 'vendor-comparison',
    'Some Sensei cleaning features require Full Disk Access.', 'Attributed documentation; no permission changes made.')
claim('B01', 'Breathing Room is a free maintenance preview; AI Care is optional at $5 USD/month or $50 USD/year.', 'br-readme',
    '**AI Care is optional: $5 USD/month or $50 USD/year.**', 'Current README agrees with 2026-10-21 live verification register. No checkout test.')
claim('B02', 'Breathing Room requires macOS 13+, Python 3.10+ for disk inventory, and internet/sign-in for hosted agent features.', 'br-readme',
    '**Python 3.10+** for disk inventory and legacy cleanup scripts.', 'Universal Intel/Apple Silicon installer; physical Intel runtime remains untested. Local storage/process tools do not require AI Care.')
claim('B03', 'The Breathing Room preview is not notarized.', 'br-readme',
    'The preview is not notarized.', 'Release notes also disclose Apple Development, not Developer ID signing; never recommend disabling protections.')
claim('B04', 'Breathing Room documents category/app/project/folder/large-file views and grouped helper CPU/memory inspection.', 'br-readme',
    'Use **Apps** to inspect CPU and memory use across an app and its helpers.', 'Partial permissions and cached inventory possible; sampled ownership is not forensic writer attribution.')
claim('B05', 'Daily care reuses exact approved locations and methods while Breathing Room remains running.', 'br-readme',
    'Scheduled care cleans only exact locations and methods you\npreviously approved; newly discovered locations wait for review.', 'No wake-from-sleep/post-quit guarantee. Source architecture, not distributed-runtime certification.')
claim('B06', 'An explicit option can automatically Trash verified Ruff lint caches; other cleanup methods need approval.', 'br-ui',
    'Automatically move verified Ruff lint caches to Trash', 'Avoid unconditional “nothing ever changes without asking each time.”')
claim('B07', 'Hosted AI can receive questions, conversation and relevant inspection/tool data; this is not entirely offline AI.', 'br-capabilities',
    'question, conversation history and subsequent tool outputs', 'Register cites native request paths and public privacy policy. No backend audit or retention guarantee.')
claim('B08', 'Breathing Room source discovery includes named developer-tool cache queries, with owning-tool/path validation constraints.', 'br-capabilities',
    'npm, uv, pip, pnpm, Go build/module, Bun and Yarn caches', 'Source implementation, not certification of every cache version or distributed binary adapter.')

for cid, topic in [('U01','Sensei process/helper grouping'), ('U02','Sensei recurring folder-growth attribution and exact-path scheduled cleanup'),
                   ('U03','Sensei current cleanup approval/deletion/Trash/rollback semantics'), ('U04','Sensei named npm/pnpm/uv/Ruff cache adapters'),
                   ('U05','Sensei complete offline/network behavior and telemetry'), ('U06','Sensei latest downloadable patch, signing/notarization and precise runtime prerequisites'),
                   ('U07','Sensei trial duration today and ISO checkout currency/tax treatment')]:
    claims.append(dict(id=cid, wording=topic + ': not verified.', state='not-verified', sourceIds=[], sourceUrl=None,
        excerpt=None, checkedDate=NOW[:10], evidenceClass='unknown', scope='Do not render as No, absent, free, private or tested.',
        intendedLocation='matrix/limitations', reviewer='research-disk-sensei worker'))

kit = by_source['press-kit']
visuals = []
for item, vid, view, caption, alt in [
    (kit['selectedAssets'][2], 'sensei-clean', 'Clean / Large Files',
     'Earlier Sensei Clean interface supplied in Cindori’s press kit. Vendor illustration; capture date and app version unknown. Sizes are not our test results.',
     'Earlier Sensei Clean window with file categories, selectable large files and a Delete control.'),
    (kit['selectedAssets'][3], 'sensei-drive-health', 'Storage / Drive Health',
     'Earlier Sensei drive-health interface from Cindori’s press kit. Vendor illustration, not our drive-health test or a current-version capture.',
     'Earlier Sensei storage-health window with drive temperature and S.M.A.R.T. attributes.')]:
    p = ROOT / item['path']
    width,height=struct.unpack('>II',p.read_bytes()[16:24])
    visuals.append(dict(id=vid, productId='disk-sensei', view=view, kind='official-asset',
        sourcePageUrl='https://cindori.com/press', assetUrl=kit['url'], archiveMember=item['member'],
        retrievedAtUtc=kit['retrievedAtUtc'], capturedAtUtc=None, capturedBy='Cindori (press-kit provider; actual capturer unknown)',
        productVersion=None, buildOrCommit=None, osVersion=None, dataMode='vendor-illustration',
        originalPath=PREFIX+item['path'], originalSha256=item['sha256'], publishedPath=None, publishedSha256=None,
        widthPx=width, heightPx=height, edits=[], privacyReview=dict(status='reviewed',redactions=[],note='Vendor-provided examples; no local user inventory.'),
        reuse=dict(status='cleared',basis='Official press-kit Artwork explicitly described as ready to go for web publishing in Welcome.pdf, page 1.',
            evidenceUrlOrPath=PREFIX+'sources/Welcome.pdf',credit='Sensei screenshot courtesy of Cindori AB.',
            conditions='Editorial depiction of Sensei only; no endorsement, blanket trademark licence or current-version representation.'),
        caption=caption,alt=alt,supportedClaimIds=['S04'] if vid=='sensei-clean' else ['S06'],
        limitations=['Historical UI; exact capture version/date unknown.','Not hands-on testing or evidence of measured results.','Needs contextual legibility review in the eventual draft.'],
        review=dict(status='visually-inspected-research-only',reviewer='research-disk-sensei worker',reviewedAtUtc=NOW)))

br = next(a for a in load(APP/'docs/content/screenshots.json')['assets'] if a['id']=='current-space-browser-preview')
assert sha(br['sourcePath']) == br['sha256']
visuals.append(dict(id=br['id'],productId='breathing-room',view='Space',kind='browser-preview',
    sourcePageUrl=br['sourceUrl'],assetUrl=None,capturedAtUtc=br['capturedOn'],retrievedAtUtc=None,
    capturedBy='screenshot-library worker (existing manifest)',productVersion=None,buildOrCommit=br['sourceCommit'],osVersion=None,
    dataMode='example',originalPath=br['sourcePath'],originalSha256=br['sha256'],publishedPath=None,publishedSha256=None,
    widthPx=br['width'],heightPx=br['height'],edits=[],privacyReview=br['privacyReview'],
    reuse=dict(status='cleared',basis=br['reuseBasis'],evidenceUrlOrPath='docs/content/screenshots.json',credit='Breathing Room example-data browser preview.'),
    caption=br['caption'],alt=br['alt'],supportedClaimIds=['B04'],
    limitations=br['limitations']+['Current-source as captured October 21, not a claim of native or latest binary parity. Keep example-data banner.'],
    review=dict(status='visually-inspected-research-only',reviewer='research-disk-sensei worker',reviewedAtUtc=NOW)))

packet = dict(schemaVersion=1,jobId='research-disk-sensei',stage='research',status='complete-documentary-research',
    createdAtUtc=NOW,clockNote='Retrieval/check dates use actual UTC machine clock (2026-10-21); harness calendar says October 22. No artificial date bump.',
    publicationApproved=False,draftingDecision=dict(status='ready-with-bounded-claims',criticalBlockers=[],
        conditions=['Use historical screenshot captions; do not call the press-kit UI current.',
                    'Attribute version/macOS requirements to August vendor documentation; do not claim latest installer tested.',
                    'Keep dollar prices as displayed, ISO currency unverified; no normalized cheapest-price comparison.',
                    'Unknown matrix cells remain not verified; independent draft/render review still required.']),
    ownership=dict(ownedDirectory=PREFIX,websiteEdits=False,queueEdits=False),
    identity=dict(id='disk-sensei',officialName='Sensei',vendor='Cindori AB',canonicalHomepage='https://cindori.com/sensei',
        canonicalOwnerId='disk-sensei',officialRepository=None,repositoryStatus='No official source repository established from inspected official pages; do not use similarly named unaffiliated GitHub downloads.',
        aliases=[dict(name='Disk Sensei',relationship='Legacy predecessor/upgrade source, not a proven simple rename.',sourceIds=['about','upgrade']),
                 dict(name='Sensei Monitor',relationship='Feature/component of Sensei, not a separate comparison owner.',sourceIds=['release-1.6'])],
        aliasDecision=dict(skipSeparateAliasDraft=True,skipThisJob=False,canonicalOwnerId='disk-sensei',
            rationale='AlternativeTo disk-sensei slug currently names Sensei and links to its homepage. One Sensei packet under assigned stable ID. Legacy Disk Sensei deserves no second current-product doorway page; Trim Enabler remains a distinct product, not an alias. No evidence links this product to PowerMyMac.'),
        fit=dict(classification='direct-overlap',platform='macOS',reason='Both document Mac storage inspection/cleanup and monitoring. Hardware diagnostics is Sensei’s adjacent strength; not full feature parity.'),
        excluded=False,dead=False),
    discovery=dict(**baseline['discovery'],edges=product['edges'],baselineRecord='docs/content/verification/batch-2.json#disk-sensei',
        rawCaptureHashVerified=True,notRefetched=True,limitation='Baseline about-page snapshot retains official link only. Seed pagination provenance reused from manifest, not newly replayed.'),
    sources=sources,claims=claims,
    matrix=[dict(dimension=d,senseiClaimIds=s,breathingRoomClaimIds=b) for d,s,b in [
        ('macOS/version/architecture',['S02','S15','S16','U06'],['B02','B03']),
        ('licence/pricing',['S08','S09','S10','S11','S12','S13','S14','U07'],['B01']),
        ('local versus hosted',['S17','U05'],['B07']),
        ('scan/cleanup/app uninstall',['S04','S05','U03'],['B04','B05','B06']),
        ('process/helper grouping',['U01'],['B04']),('recurring growth/scheduling',['U02'],['B04','B05']),
        ('developer caches',['U04'],['B08']),('hardware health',['S06','S07','S21','S22'],[]),
        ('runtime/installation',['S15','S16','S17','S20','U06'],['B02','B03'])]],
    visuals=visuals,
    currentCompetitorVisualLinks=[dict(sourcePageUrl=by_source['vendor-comparison']['url'],
        assetUrl='https://cindori.com/images/blog/sensei/sensei-2-clean.png',reuseStatus='link-only',downloaded=False,
        scope='Exact image path observed in current vendor article; not downloaded because press-kit permission does not automatically cover other website images.')],
    sourceConflicts=[dict(topic='OS and version',resolution='Legacy kit says Catalina; support says minimum increased; August 2026 vendor article specifies 2.1.2/macOS14+. Never use launch-era requirement for current builds.'),
        dict(topic='architecture',resolution='Press-kit Q/A describes Monitor as standalone in 1.5; 1.6 release says unified app. Use version-scoped history only.'),
        dict(topic='price/update terms',resolution='Legacy kit calls licence lifetime; current store limits future major upgrades and calls 1 current despite August article naming 2.1.2. Quote current entitlement wording, not unlimited lifetime updates.')],
    noncriticalUnknowns=['Latest downloadable patch and actual installer minimum/signing/runtime have not been inspected.',
        'ISO currency/tax and trial duration today unverified; do not invent.',
        'No official repo found; exact offline/telemetry behavior unverified.',
        'Historical vendor artwork capture dates/builds unknown; labelled explicitly.'],
    observations=dict(installed=False,handsOn=False,benchmarks=False,cleanup=False,browserUsed=False,
        method='Reused current verification first; read-only official HTTP pages and explicitly distributed press artwork. No browser/cookie extraction or accounts.'),
    briefs=dict(workflow=dict(track='search-reference',slug='mac-storage-pressure-or-drive-health-sensei',
        title='Mac storage pressure or drive trouble? Choose the right investigation',
        primaryIntent='Separate lack of capacity from drive-health questions before choosing a cleanup action.',
        description='Capacity and drive-health indicators answer different questions. Use Sensei’s documented hardware views or Breathing Room’s storage workflow without treating either as a diagnosis or a cleanup guarantee.',
        outline=['Start with the reader’s symptom: full storage versus a drive-health warning; neither proves the other.',
                 'Check capacity and identify known files before considering removal; a large file is not permission.',
                 'Explain Sensei’s documented S.M.A.R.T., thermal and benchmark tools without promising prediction or a repair.',
                 'Use Breathing Room, which we build, for storage categories/app/project investigation and reviewable cleanup; disclose preview/Python/hosted constraints.',
                 'Preserve backup and app-native management options; no destructive tests or TRIM/security-setting tutorial.',
                 'Finish with a decision checklist: capacity, hardware concern, or both.'],
        visuals=['sensei-drive-health immediately after lead with historical caption','current-space-browser-preview alongside capacity discussion; preserve example banner'],
        interactionPass='Propose a static three-path decision aid (capacity / health warning / both), not a simulated scanner or unsupported numeric score.',
        exclusion='Not another generic cleaner list or CPU troubleshooting post; no fabricated diagnosis, hands-on trial, savings or performance claims.',
        links=['/comparisons/','/comparisons/disk-sensei/'],wordCount='Earned length, approximately 900–1400 words; no padding.'),
        comparison=dict(slug='disk-sensei',title='Breathing Room vs Sensei: storage workflows or hardware diagnostics',
            primaryIntent='Choose between overlapping Mac maintenance products by documented workflow and deployment caveats.',
            structure=['Disclosure and bounded recommendation','Concise sourced matrix with unknowns','Who should choose Sensei','Who should consider the Breathing Room preview','Pricing/update/refund/version limits','Link to distinct storage-versus-health workflow'],
            visuals=['sensei-clean','current-space-browser-preview'],
            links=['/comparisons/','/blog/mac-storage-pressure-or-drive-health-sensei/'])),
    advantagesAndTradeoffs=dict(sensei=['Documented S.M.A.R.T., thermal, battery and benchmark tools; choose for hardware-oriented investigation, not guaranteed diagnosis.',
        'Configurable menu-bar panels and app uninstallation documented; subscription or one-time licence for up to three Macs subject to per-user/update terms.',
        'Latest build verification, cleanup semantics, detailed developer adapters and network behavior remain unknown.'],
        breathingRoom=['Source/register documents category/app/project storage views, grouped helper inspection and exact saved approvals; potential fit for recurring investigation, not proof of superiority.',
        'Free local core with optional paid hosted AI Care; preview not notarized, Python prerequisite and physical Intel untested. Hosted AI is not offline.',
        'No verified equivalence to Sensei’s hardware diagnostics or app uninstaller; do not imply either parity or an unsupported absence.']),
    validation=dict(status='see-separate-validation-record',recordPath=PREFIX+'validation.json',independentReview='pending separate review stage',siteBuild='not applicable: no site files edited',
        reviewScore=None,prohibitedActionsPerformed=False))
(ROOT/'research.json').write_text(json.dumps(packet,indent=2,ensure_ascii=False)+'\n')
print('Wrote research.json:',len(claims),'claims;',len(sources),'sources;',len(visuals),'visuals')
