"""Read-only public research; writes only this product's evidence folder."""
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
ID = 'cleaner-by-ciro-cesar-maciel'
SHA = '97a188398d18110a30d30a4bf9f57ad8843d5591'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
DAY = NOW[:10]
BASE = f'https://raw.githubusercontent.com/ciro-maciel/cleaner/{SHA}/'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


sources = []
texts = {}


def local_source(sid, path, url, retrieved):
    texts[sid] = json.loads(path.read_text())['text']
    sources.append(dict(id=sid, url=url, finalUrl=url, retrievedAtUtc=retrieved,
                        checkedAtUtc=NOW, reused=True, snapshotPath=str(path.relative_to(APP)),
                        sha256=digest(path), publisher='Ciro Cesar Maciel' if sid == 'official' else 'AlternativeTo',
                        sourceDate=None))


local_source('official', APP / 'docs/content/.runtime/verification-1' / f'{ID}-official.json',
             'https://ciromaciel.click/tools/cleaner', '2026-10-21T19:07:59.396261+00:00')
local_source('discovery', APP / 'docs/content/.runtime/verification-1' / f'{ID}-directory.json',
             f'https://alternativeto.net/software/{ID}/about/', '2026-10-21T19:05:46.325Z')
assert digest(APP / sources[0]['snapshotPath']) == 'fabcbe13dfbcf884fbd84df1d96d85e63e4705ea5ff99fcf9027498506169f70'
(ROOT / 'sources').mkdir(exist_ok=True)
# Retain immutable primary documents for missing release, repo and image-rights evidence.
# No binary, image, install script, credentials or user data is requested.
for sid, filename in [('readme', 'README.md'), ('notice', 'NOTICE'), ('license', 'LICENSE'), ('version', 'VERSION')]:
    url = BASE + filename
    path = ROOT / 'sources' / filename
    if path.exists():
        raw = path.read_bytes()
        final = url
    else:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'BreathingRoom-public-research'}), timeout=40) as response:
            raw = response.read()
            final = response.url
        path.write_bytes(raw)
    texts[sid] = raw.decode()
    sources.append(dict(id=sid, url=url, finalUrl=final, retrievedAtUtc=datetime.datetime.fromtimestamp(path.stat().st_mtime, datetime.timezone.utc).isoformat(),
                        reused=False, snapshotPath=str(path.relative_to(APP)), sha256=digest(path),
                        publisher='Ciro Cesar Maciel', sourceDate=None, scope=f'Repository commit {SHA}; not binary validation'))

# This is an explicitly labeled excerpt of the API response inspected with WebFetch,
# not a fabricated full raw response or an independent binary checksum measurement.
release = dict(tag_name='v0.4.0', name='Cleaner by Ciro Cesar Maciel 0.4.0',
               published_at='2026-10-19T19:17:45Z', draft=False, prerelease=False,
               target_commitish='8cd67e36dc3794f308108be34ae85aa4afa729a2',
               html_url='https://github.com/ciro-maciel/cleaner/releases/tag/v0.4.0',
               asset=dict(name='Cleaner-0.4.0-macos.dmg', size=2775786,
                          vendorReportedSha256='303991caf782308e4fda288db11f8adad9a87429da248d3164dcc65d9dfa8e0c',
                          url='https://github.com/ciro-maciel/cleaner/releases/download/v0.4.0/Cleaner-0.4.0-macos.dmg'),
               bodyExcerpt='Or download the .dmg and drag Cleaner to Applications: signed with Developer ID and notarized by Apple. Apple Silicon, macOS 14+.',
               retention='Selected fields transcribed from actual WebFetch API response; binary not downloaded.')
rp = ROOT / 'sources/release-excerpt.json'
write_json(rp, release)
texts['release'] = json.dumps(release)
sources.append(dict(id='release', url='https://api.github.com/repos/ciro-maciel/cleaner/releases/latest',
                    finalUrl='https://api.github.com/repos/ciro-maciel/cleaner/releases/latest',
                    checkedAtUtc=NOW, retrievedAtUtc=None, retrievalDate=DAY,
                    retrievalTimeNote='WebFetch performed in this job; exact transport timestamp unavailable.',
                    sourceDate=release['published_at'], snapshotPath=str(rp.relative_to(APP)), sha256=digest(rp),
                    retention='Selected-response excerpt, not full raw response', publisher='GitHub / Ciro Cesar Maciel'))
claims = []


def claim(cid, wording, sid, excerpt, scope, state='verified'):
    assert excerpt in texts[sid], (cid, excerpt)
    source = next(s for s in sources if s['id'] == sid)
    claims.append(dict(id=cid, wording=wording, sourceIds=[sid], sourceUrl=source['url'],
                       supportingExcerpt=excerpt, checkedAtUtc=NOW, checkedDate=DAY,
                       evidenceClass='documented-vendor' if sid != 'release' else 'published-release-metadata',
                       state=state, scope=scope, intendedLocation='workflow or comparison; cite beside claim',
                       reviewer='scheduled research worker; not independent publication approval'))


claim('identity', 'Cleaner by Ciro Cesar Maciel is the official name; Cleaner is its short form.', 'readme',
      '# Cleaner by Ciro Cesar Maciel', f'Official linked repository at {SHA}.')
claim('platform', 'Cleaner supports Apple Silicon Macs with macOS 14 or newer; Intel is not supported in the documented edition.',
      'official', 'Ainda não. O Cleaner é feito para Mac com Apple Silicon (M1 ou mais novo) e macOS 14 ou mais novo.',
      'Official FAQ; no Intel, Windows or Linux build inferred.')
claim('price', 'Cleaner is offered free, without an account, under MIT.', 'official',
      'Grátis, sem conta e com licença MIT.', 'Public offer checked 2026-10-21; no subscription, checkout or installation tested. No currency conversion needed.')
claim('license', 'The repository software and associated documentation carry MIT with notice-preservation conditions.', 'license',
      'The above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.',
      'Not blanket clearance for third-party art, fonts or maker marks; read NOTICE and README together.')
claim('version', 'The repository VERSION file identifies 0.4.0.', 'version', '0.4.0',
      f'Pinned main commit {SHA}; not proof latest vendor-blob DMG is byte-identical.')
claim('availability', 'GitHub publishes Cleaner v0.4.0 dated October 19, 2026 with a named DMG asset.', 'release',
      'Cleaner-0.4.0-macos.dmg', 'Latest-release endpoint observed; metadata only, no download/install test.')
claim('signing', 'The release publisher says the DMG is Developer ID signed and Apple notarized.', 'release',
      'signed with Developer ID and notarized by Apple.', 'Attributed vendor disclosure only; no independent signature, stapling or Gatekeeper inspection.')
claim('quarantine', 'Documented removal uses quarantine batches with original paths, one-click restore and automatic emptying after seven days.',
      'readme', 'Removal moves items to a quarantine batch that remembers each original path. Restore is one click; after 7 days the batch empties itself.',
      'Documented workflow, not tested recovery or a backup guarantee. Quarantine is not immediate reclaimed physical space.')
claim('approval', 'The documented workflow shows item paths, sizes and rules; running-app items start deselected and moving requires a three-second hold.',
      'official', 'Cada item mostra a pasta, o tamanho e a regra que o trouxe. Desmarque o que quiser manter. Itens de apps abertos já vêm desmarcados.',
      'Together with removal hold documented in README; no execution performed.')
claim('hold', 'Removal requires holding for three seconds according to README.', 'readme',
      '**Removal takes a 3-second hold.**', 'Documented guard, not proof accidental actions are impossible.')
claim('rules', 'Cleanup documents eight named rules for app caches, logs, Trash, old installers, Xcode, developer caches and Mail downloads.',
      'readme', 'The other seven are `logs`, `trash`, `installers`, `xcode-derived-data`, `dev-caches`, `xcode-device-support` and `mail-downloads`.',
      'app-caches is the preceding example; source inspection not adapter testing; rule counts are date-specific.')
claim('dev-caches', 'The homepage names npm, Bun, pnpm, Gradle and Cargo downloads among developer cleanup targets.', 'official',
      'pacotes baixados por npm, Bun, pnpm, Gradle e Cargo', 'Vendor documentation only; compatibility with individual tool versions not tested.')
claim('local', 'The vendor describes Cleaner as having no network code and no account or telemetry.', 'official',
      'Falar com a internet. Não há conta, telemetria nem envio de nada.', 'Attributed vendor claim, not a network audit; obtaining/updating the installer uses network access.')
claim('permissions', 'A full scan requires optional Full Disk Access; without it Trash, Mail and containers are hidden.', 'readme',
      'Without it, macOS hides the Trash, Mail and app containers, and Cleaner tells you so instead of pretending.',
      'No permission granted or machine setting changed. Vendor says system item moves can require admin password.')
claim('admin', 'The homepage says moving system items asks for an administrator password.', 'official',
      'Itens do sistema pedem a senha de administrador.', 'No credentials accessed or operation executed.')
claim('uninstaller', 'The documented uninstaller lists size and last use and searches 38 leftover locations including package receipts.', 'readme',
      'Lists apps with size and last use, then removes the app and its leftovers in 38 places, .pkg receipts included',
      'Vendor description, no completeness or safety guarantee.')
claim('disk-map', 'The documented disk map measures a folder and lets the user descend into larger parts.', 'readme',
      'Measures a whole folder in parallel and lets you walk into the biggest parts', 'No scan benchmark or access-completeness test.')
claim('startup', 'Startup controls are documented for LaunchAgents and LaunchDaemons without deleting their files.', 'readme',
      'Turns LaunchAgents and LaunchDaemons on and off without deleting the file', 'Documented only; no setting changed.')
claim('monitor', 'Menu-bar monitoring documents CPU, memory, network, disk and battery.', 'readme',
      'CPU, memory, network, disk and battery, live, plus how much you can free right now',
      'No app/helper grouping parity, recurring-growth history or measurement accuracy established.')
claim('limits', 'The README explicitly lists no duplicate finder, malware scan or app updater.', 'readme',
      'No duplicate finder, no malware scan and no app updater.', f'Vendor-stated limits at {SHA}; not inferred from silence.')
claim('languages', 'The documented interface follows the Mac language in English or Brazilian Portuguese.', 'readme',
      "The interface is in English and Brazilian Portuguese, following the Mac's language.", 'No locale runtime testing.')
claim('image-art', 'Official-build screen illustrations come from a licensed gallery and are not shipped with the source build.', 'readme',
      'The illustrations on each screen come from a licensed gallery and ship only in the official build;',
      'Critical screenshot redistribution uncertainty; source builds use Tabler icons instead.')
claim('image-mark', 'The logotype/maker mark is explicitly excluded from MIT.', 'notice',
      'It is the maker\'s mark and is not covered by the MIT License.',
      'No screenshot permission request authorized. Public display is not permission to republish.')

manifest = json.loads((APP / 'docs/content/competitors.json').read_text())


def find_product(obj):
    if isinstance(obj, dict):
        if obj.get('id') == ID and 'edges' in obj:
            return obj
        for value in obj.values():
            found = find_product(value)
            if found:
                return found
    if isinstance(obj, list):
        for value in obj:
            found = find_product(value)
            if found:
                return found


entry = find_product(manifest)
assert entry
library = json.loads((APP / 'docs/content/screenshots.json').read_text())
br = next(a for a in library['assets'] if a['id'] == 'current-space-browser-preview')
assert digest(Path(br['sourcePath'])) == br['sha256']
br = dict(br, productId='breathing-room', selectedFor='later figure: category size is not deletion permission',
          thisJobVisualReview='Opened and read the actual PNG; example banner, Space categories and composer visible. No native test.',
          originalSha256=br['sha256'], publishedPath=None, publishedSha256=None)
visual = dict(id='cleaner-official-cleanup', productId=ID, view='Cleanup item/rule/size view', kind='official-asset',
              sourcePageUrl=f'https://github.com/ciro-maciel/cleaner/blob/{SHA}/README.md',
              assetUrl=BASE + 'docs/cleanup.webp', alternateAssetUrl=BASE + 'docs/overview.webp',
              capturedAtUtc=None, retrievedAtUtc=None, capturedBy=None, productVersion=None,
              buildOrCommit=SHA, osVersion=None, dataMode='unknown', originalPath=None, originalSha256=None,
              publishedPath=None, publishedSha256=None, widthPx=None, heightPx=None, edits=[],
              privacyReview=dict(status='pending', redactions=[]),
              reuse=dict(status='link-only', basis='MIT covers software/docs subject to notice, but README discloses licensed gallery art and NOTICE excludes maker mark. Image-specific redistribution clearance is not established.',
                         evidenceUrlOrPath=[BASE + 'README.md', BASE + 'NOTICE', BASE + 'LICENSE'], credit='Cleaner by Ciro Cesar Maciel; official project screenshot.'),
              caption='Official Cleaner Cleanup screenshot linked by its author. Illustrates documented items, rules and sizes; not our test or measured savings. Capture date and app build unknown.',
              alt='Official Cleaner Cleanup view showing cleanup items, the rules that found them, and their sizes.',
              supportedClaimIds=['rules', 'approval'], review=dict(status='pending', reviewer=None, reviewedAtUtc=None),
              limitations=['Image URL verified from official README; image pixels not downloaded or visually inspected.',
                           'Unknown gallery-art and maker-mark redistribution terms block on-page reuse; link-only does not pass the visual gate.'])
blocker = 'Required competitor app screenshot is link-only: official README discloses licensed-gallery screen art; NOTICE excludes the maker mark from MIT. No image-specific redistribution permission/clearance or approved alternative exists. Obtain documented clearance (no outreach authorized here) or an explicitly approved policy decision, then download/hash/inspect the image and independently review both visuals before drafting.'
unknowns = ['Binary signature/notarization, successful installation, actual restore, quarantine-expiry scheduling and cleanup results were not tested.',
            'Latest vendor-blob DMG identity versus GitHub v0.4.0 asset is not verified.',
            'Cleaner process/helper grouping and recurring-growth history are not verified, not absent.',
            'Python/runtime dependency of distributed Cleaner not independently audited; native Swift vendor description is not a full dependency inventory.',
            'Official image capture date, version, dimensions, pixels and redistribution clearance remain unknown.',
            'No measured space recovery, speed, accuracy, security, complete app-remnant detection or safety superiority claim is authorized.']
matrix = [
    ('macOS', 'Apple Silicon M1+, macOS 14+; Intel explicitly unsupported', ['platform']),
    ('pricing/licence', 'Free, no account; MIT software/docs with third-party and mark exceptions', ['price', 'license', 'image-art', 'image-mark']),
    ('operation', 'Vendor describes local app with no network code or telemetry; installation uses downloads', ['local']),
    ('scan/cleanup', 'Rule-based candidate review, folder map, app uninstalling', ['rules', 'disk-map', 'uninstaller']),
    ('approval/recovery', 'Review selections, three-second hold, seven-day quarantine then emptying', ['approval', 'hold', 'quarantine']),
    ('permissions', 'Optional Full Disk Access for complete coverage; admin password for system item moves', ['permissions', 'admin']),
    ('developer caches', 'npm, Bun, pnpm, Gradle, Cargo named by homepage', ['dev-caches']),
    ('monitoring', 'Menu-bar CPU/memory/network/disk/battery; grouping and recurring growth not verified', ['monitor']),
    ('installation/version', 'Published GitHub v0.4.0; drag DMG app to Applications documented; signing/notarization vendor-reported', ['availability', 'version', 'signing']),
    ('limits', 'No duplicate finder, malware scan or app updater per README', ['limits'])]
packet = dict(schemaVersion=1, jobId='research-' + ID, productId=ID, checkedAtUtc=NOW,
              status='blocked', draftingAllowed=False, published=False,
              identity=dict(officialName='Cleaner by Ciro Cesar Maciel', homepage='https://ciromaciel.click/tools/cleaner',
                            repository='https://github.com/ciro-maciel/cleaner', canonicalOwnerId=ID,
                            aliases=['Cleaner', 'ciro-cleaner (Homebrew cask identifier)'],
                            aliasDecision=dict(skip=False, reason='Own author domain links ciro-maciel/cleaner and repository links back, uses full name and lists this as its own Mac app. No verified alternate manifest identity; do not merge generic Cleaner names or infer a PowerMyMac relationship.'),
                            classification='direct-mac-cleanup-overlap', classificationReason='Both address Mac storage inspection/reviewable cleanup; not full-suite interchangeability. Cleaner additionally documents uninstaller/startup tools; Breathing Room preview focuses on investigation and approved care.'),
              discovery=dict(listingUrl=sources[1]['url'], sourceId='discovery', method='Reused batch-1 official-link browser record and existing traversal edges; no directory refetch.',
                             edges=entry['edges'], snapshotPath=sources[1]['snapshotPath'], sha256=sources[1]['sha256'],
                             exclusions='No exclusion/dead-product/alias skip justified; a published release exists. Listing is discovery only.'),
              reusedBaseline=dict(path='docs/content/verification/batch-1.json', recordId=ID, originalStatus='partial',
                                  originalUnverifiedFields=['availability'], result='Reused current identity, platform, price, licence and core workflow. Filled repository/release/rights evidence; no homepage refetch.'),
              sources=sources, claims=claims, productMatrix=[dict(dimension=d, value=v, claimIds=c) for d, v, c in matrix],
              versionScope=dict(repositoryCommit=SHA, repositoryVersion='0.4.0', publishedRelease=release,
                                warning='Main README evidence and release metadata are separate scopes; no distributed binary parity certification.'),
              breathingRoom=dict(evidenceRegister='docs/content/capabilities.md', checked='2026-10-21',
                                 rule='Reuse current primary-source register; source implementation is not proof of binary parity. Recheck affected primary claims before publication if changed/stale.',
                                 comparisonClaims=[
                                     dict(id='br-preview', wording='0.1.0-preview.1, macOS 13+, universal Intel/Apple Silicon advertised; physical Intel/clean-machine execution unvalidated, not Developer ID signed or notarized.', registerSections=['Preview, installation and runtime caveats'], sourceUrls=['https://github.com/bucabay/breathing-room-app/releases/tag/v0.1.0-preview.1'], localEvidence=['RELEASE_NOTES.md:3-15,43-46', 'src-tauri/tauri.conf.json:49-51']),
                                     dict(id='br-price', wording='Free Apache-2.0 core; optional AI Care $5 USD/month or $50 USD/year, renews until cancelled, applicable taxes at checkout; no unlimited allowance verified.', registerSections=['Pricing, access and paid-feature claims'], sourceUrls=['https://breathing-room.chatic.ai/#pricing', 'https://breathing-room.chatic.ai/checkout/monthly/'], localEvidence=['README.md:141-150', 'src/billing-config.json:4-7']),
                                     dict(id='br-care', wording='Local inspection/execution with hosted authenticated AI; exact saved daily approvals require app running; optional automatic verified Ruff-cache Trash mode is an exception to blanket manual-approval language. Python 3.10+ needed for inventory, not bundled.', registerSections=['Approval exception', 'Local versus hosted boundary', 'Preview, installation and runtime caveats'], sourceUrls=['https://breathing-room.chatic.ai/privacy/', 'https://breathing-room.chatic.ai/download/'], localEvidence=['README.md:64-72,120-128', 'src-tauri/src/cleanup_session.rs:400,469-478', 'src/components/cleanup-assistant.tsx:198']),
                                     dict(id='br-investigation', wording='Source supports storage context, grouped app/helper CPU and memory, activity history and recurring-growth investigation; sampled/inferred observations do not prove exact file writers or measured savings.', registerSections=['Current capability matrix'], sourceUrls=['https://breathing-room.chatic.ai/'], localEvidence=['src-tauri/src/processes.rs:57-164', 'src-tauri/src/monitor.rs:12-25,218-230'])],
                                 evidenceClass='reused-source-and-published register, not new runtime verification'),
              visuals=[visual, br],
              briefs=dict(track='search/LLM reference; Breathing Room editorial adaptation, not MailKite code-demo workflow',
                          workflow=dict(title='Reviewing Mac cleanup rules before a seven-day quarantine expires',
                                        slug='cleaner-by-ciro-cesar-maciel-mac-workflow',
                                        primaryIntent='Help Apple Silicon Mac owners distinguish a reviewable cleanup candidate, reversible quarantine and actual free-space recovery.',
                                        description='Cleaner documents public cleanup rules and a seven-day quarantine. Use those boundaries to decide what to leave alone, what needs a rebuild plan, and when recurring-growth investigation is the more useful next step.',
                                        outline=['Top official Cleanup figure only after reuse clearance', 'Read the rule and exclusion, not just the size; close or defer active-project items', 'Plan restoration before quarantine expires; seven days is not a backup', 'Explain that on-volume quarantine retains data; do not calculate savings from candidate sizes', 'Contrast one-time review with recurring-growth investigation using labeled Space preview', 'Decision checklist and source-linked limits; one disclosed Breathing Room recommendation at most'],
                                        guardrails=['Documentation-led, not a tested tutorial; no removal commands or fabricated restoration experiment.', 'Do not repeat vendor language that every proposed cache is safe; rebuild costs and important data still require judgment.', 'No invented support question or forced FAQ.']),
                          comparison=dict(title='Breathing Room vs Cleaner by Ciro Cesar Maciel', slug=ID,
                                          primaryIntent='Choose between a documented free local rule/quarantine workflow and a qualified preview with hosted investigation/approved care.',
                                          contents=['Concise claim-linked matrix above', 'Cleaner strengths: free/no-account documented offer, inspectable rules, quarantine, uninstaller/startup controls', 'Breathing Room fit: source-supported storage context, grouped helpers and recurring investigation; retain preview/hosted/paid/runtime caveats', 'Cleaner and Breathing Room limitations without inferred negative cells', 'Link to workflow and existing comparisons hub'],
                                          disclosure='Breathing Room, which we build; no objective winner or measured superiority established.'),
                          interactionPass=dict(proposed='Non-executing decision checklist: supported Mac? known rebuild cost? backup for original data? restore before seven days? recurring growth?',
                                               scope='Draft-stage handoff only; no runnable cleanup, no forced demo repo, no site changes.'),
                          internalLinks=['/comparisons/'],
                          linkPolicy='Only hub confirmed by PLAN; validate counterpart route/tool existence before draft links.'),
              advantagesAndTradeoffs=dict(cleaner=['Documented free/no-account local workflow and published MIT source.', 'Public rules, seven-day quarantine, app-remnant/startup tools and menu bar monitoring documented.', 'Apple Silicon/macOS 14 only; Full Disk Access for complete scan; recovery window is finite; no binary validation performed.'],
                                          breathingRoom=['Source-supported project/tool storage context, grouped helper monitoring and recurring-growth investigation can fit ongoing diagnosis.', 'Free core is a preview, Python-dependent inventory; hosted AI authentication/data transfer and optional paid Care must be disclosed.', 'No supported claim here for a full uninstaller, malware removal or duplicate-photo parity.']),
              unknowns=unknowns, blockers=[dict(id='competitor-image-clearance', diagnostic=blocker)],
              gates=dict(identity='pass', aliasResolution='distinct product; no alias skip', platformFit='pass', offer='pass-documented',
                         release='pass-metadata-only', competitorVisual='blocked-link-only', breathingRoomVisual='selected-hash-checked-visually-read-example-only',
                         independentReview='pending', drafting='blocked'),
              safety=dict(publicPages='Untrusted source data only.', agentsSpawned=0, imagesDownloaded=0, binariesDownloaded=0,
                          installs=0, cleanupRuns=0, credentialsRead=False, websiteEdited=False, queueEdited=False,
                          note='No browser automation required for source-only research. Browser skill loaded; no tabs, profiles or settings touched.'),
              diagnostic=blocker)
register = APP / 'docs/content/capabilities.md'
register_text = register.read_text()
sources.append(dict(id='br-register', url=None, finalUrl=None, retrievedAtUtc=None,
                    checkedAtUtc=NOW, reused=True, sourceDate='2026-10-21',
                    publisher='Breathing Room capability verification worker',
                    snapshotPath='docs/content/capabilities.md', sha256=digest(register),
                    scope='Existing primary-source inspection register, reused without claiming a new native test.'))
br_excerpts = {
    'br-preview': 'Apple Development signed, not Developer ID signed or notarized',
    'br-price': 'Plans renew until cancelled; applicable tax shown at checkout.',
    'br-care': 'Python **3.10+** is a disclosed prerequisite for disk inventory and legacy scripts, not bundled.',
    'br-investigation': 'Native sampling groups helpers through parent/app relationships and exposes CPU/memory.',
}
for item in packet['breathingRoom']['comparisonClaims']:
    excerpt = br_excerpts[item['id']]
    assert excerpt in register_text
    item.update(sourceIds=['br-register'], supportingExcerpt=excerpt, checkedAtUtc=NOW,
                state='verified-register-reuse', evidenceClass='reused-source-and-published-documentation',
                limitations='Full statement support is in the named register sections and primary file/URL references; not a new runtime observation.')
write_json(ROOT / 'research.json', packet)
print(json.dumps(dict(packet=str(ROOT / 'research.json'), claims=len(claims), sources=len(sources), status='blocked'), indent=2))
