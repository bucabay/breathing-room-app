"""Assemble this job's documentary packet from retained evidence; no network/actions."""
import datetime
import hashlib
import json
import pathlib
import struct

ROOT = pathlib.Path(__file__).resolve().parent
APP = ROOT.parents[3]


def load(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return str(path.relative_to(APP))


baseline = next(x for x in load(APP / 'docs/content/verification/batch-2.json')['records'] if x['id'] == 'purge')
manifest = load(APP / 'docs/content/competitors.json')
products = manifest.get('competitors', manifest.get('products', []))
entry = next(x for x in products if x['id'] == 'purge')
sources = []
for sid, record in [('official-homepage', baseline['sources'][0]), ('directory', baseline['discovery'])]:
    path = APP / record['rawCapture']
    assert digest(path) == record['sha256']
    sources.append({'id': sid, 'publisher': 'Purge / Jithin Sabu' if sid == 'official-homepage' else 'AlternativeTo',
                    'url': record['sourceUrl'], 'finalUrl': record.get('finalUrl', record['sourceUrl']),
                    'retrievedAtUtc': record['retrievedAt'], 'snapshotPath': record['rawCapture'],
                    'sha256': digest(path), 'method': 'Reused current batch-2 verification; not refetched',
                    'scope': 'Homepage documentary claims' if sid == 'official-homepage' else 'Discovery/identity only'})
for sid, name in [('readme', 'readme-v1.12.0'), ('license', 'license-v1.12.0'), ('release', 'release-latest'), ('safety', 'safety')]:
    meta = load(ROOT / 'sources' / (name + '.meta.json'))
    assert digest(APP / meta['path']) == meta['sha256']
    sources.append({'id': sid, 'publisher': 'Purge / Jithin Sabu', 'url': meta['url'], 'finalUrl': meta['finalUrl'],
                    'retrievedAtUtc': meta['retrievedAtUtc'], 'snapshotPath': meta['path'], 'sha256': meta['sha256'],
                    'scope': 'v1.12.0' if sid != 'release' else 'GitHub latest release API at retrieval',
                    'publicationDate': '2026-10-20T12:40:24Z' if sid == 'release' else None})
for sid, name in [('br-capabilities', 'capabilities.md'), ('br-visuals', 'screenshots.json')]:
    p = APP / 'docs/content' / name
    sources.append({'id': sid, 'publisher': 'Breathing Room (first-party evidence register)',
                    'url': 'https://breathing-room.chatic.ai/' if sid == 'br-capabilities' else 'http://127.0.0.1:1431/',
                    'snapshotPath': relative(p), 'sha256': digest(p), 'checkedOn': '2026-10-21',
                    'scope': 'Reused current 2026-10-21 source/public-page register; not native runtime verification'})
by_id = {s['id']: s for s in sources}
claims = []


def claim(cid, wording, sid, excerpt, locator, scope='Purge v1.12.0 documentary evidence; no hands-on test', state='verified', location='article and comparison'):
    s = by_id[sid]
    claims.append({'id': cid, 'wording': wording, 'sourceIds': [sid], 'sourceUrl': s['url'],
                   'excerpt': excerpt, 'locator': locator,
                   'checkedOn': s.get('checkedOn', s.get('retrievedAtUtc', '')[:10]),
                   'evidenceClass': 'documented-not-tested', 'state': state, 'scope': scope,
                   'intendedLocation': location, 'reviewer': 'research-purge worker; independent review pending'})


claim('P01', 'Purge is the Mac cleaner at purgemac.com, with official repository jithin-sabu/purge-app.', 'official-homepage',
      'Purge on GitHub', 'links: Purge on GitHub → https://github.com/jithin-sabu/purge-app', 'Identity cross-linked by directory, official homepage and repository')
claim('P02', 'Purge is advertised free, with no trial or paid tier.', 'official-homepage',
      'Yes. No license, no trial, no paid tier, nothing bundled in.', 'Is it really free?', 'Current advertised offer; no currency, billing period, device limit or checkout tested')
claim('P03', 'Purge documents macOS 13 or later.', 'official-homepage', 'macOS 13+', 'download version/platform line', 'Mac platform; architecture support not verified; no Windows/Linux support inferred')
claim('P04', 'The latest public release returned by GitHub was v1.12.0, published October 20, 2026.', 'release',
      'v1.12.0', 'tag_name; published_at=2026-10-20T12:40:24Z; draft=false; prerelease=false', 'As returned at retrieval; asset URLs listed, installer not downloaded or tested')
claim('P05', 'The repository is MIT licensed; retain the copyright and permission notice when reusing its documentation asset.', 'license',
      'Copyright (c) 2026 Jithin Sabu', 'Entire LICENSE; permission covers software and associated documentation files', 'Repository licence; not a blanket licence for third-party marks or external artwork')
claim('P06', 'Purge documents local scans and cleanup history, and says it does not use AI; its documented network exception is update checking.', 'readme',
      'Purge does not use AI. Nothing you scan or clean is sent to an AI service.', 'Privacy, lines 330–338', 'Vendor documentation, not packet-capture/source privacy audit; do not repeat blanket no-network or file-content claims')
claim('P07', 'Purge normally moves files to Trash and never empties it; simulators, simulator runtimes and Time Machine snapshots are permanent-removal exceptions. Apple Intelligence model removal uses Apple’s asset service.', 'readme',
      'Files and folders go to the Trash by default, and Purge never empties the Trash', 'Note line 47; Cleaning line 145', 'Model feature documented for macOS 27 / Apple silicon only (Overview line 62); not independently tested')
claim('P08', 'Clean Selected presents a confirmation sheet; Large Files and duplicate removal require review and confirmation.', 'readme',
      'Nothing is removed until you review and confirm', 'Large Files line 95; Cleaning line 142', 'Do not generalize manual confirmation to enabled automatic scheduled cleaning')
claim('P09', 'Optional scheduled cleaning targets Safe items; the documented schedule offers weekly, monthly, every three months or custom intervals and cleans when the app opens.', 'readme',
      'Purge sends a local reminder and cleans safe items when you open the app', 'Cleaning line 144', 'Homepage says scheduled cleaning and deleted-app review are off by default; no promise of background schedule execution while quit')
claim('P10', 'Purge documents Xcode, npm, pnpm, Homebrew and other tool caches, plus project artifacts such as node_modules and Rust target.', 'readme',
      '**Developer projects**: `node_modules`, Python virtual environments, Rust `target`', 'Dev Tools lines 78–84', 'Vendor says active projects are skipped; stale threshold one month to two years or Show all. No compatibility or savings test performed')
claim('P11', 'Purge documents an app uninstaller with per-item path/size review and an optional deleted-app leftover watcher.', 'readme',
      'review a per-app sheet that lists every item with its path and size and a safety label', 'App Uninstaller lines 118–123', 'Watcher is off by default; documented to work even if Purge is quit; this is distinct from scheduled cleanup')
claim('P12', 'Purge documents App Caches and Dev Tools scanning without Full Disk Access; Large Files and app scans require it.', 'readme',
      'Large Files and the app scans need Full Disk Access; without it only App Caches and Dev Tools scan', 'Overview line 60', 'Specific qualified description supersedes broad README installation wording at line 228; permission behavior not tested')
claim('P13', 'Official instructions offer Homebrew or a direct DMG, describe Apple notarization and Sparkle updates, and list optional Xcode command-line tools for full simulator listing.', 'readme',
      'Purge is notarized by Apple', 'Installation lines 184–245; Requirements lines 322–326', 'Vendor notarization statement only; no binary signature/notarization inspection. Xcode 16 and Node 18+ apply to source build/icon regeneration, not ordinary installed runtime')
claim('P14', 'Purge documents a read-only Everything else map for storage not listed as cleanup candidates.', 'release',
      'It is read only and moves nothing.', 'body / See what is in Everything else', 'v1.12.0 release notes, not observed behavior')
claim('P15', 'Purge’s safety labels are vendor classifications, not an independent guarantee that removal has no cost or data risk.', 'readme',
      'May be safe, but could cause inconvenience', 'Safety labels lines 125–138', 'Editorial interpretation; avoid calling arbitrary folders safe based on a label')
claim('B01', 'Breathing Room, which we build, is a free Apache-2.0 macOS maintenance preview, with advertised optional AI Care at $5 USD/month or $50 USD/year.', 'br-capabilities',
      'AI Care is advertised at **$5 USD/month or $50 USD/year**', 'Conclusion; pricing table lines 70–80', '0.1.0-preview.1 register; renewal/tax terms apply; no paid entitlement or payment test')
claim('B02', 'Breathing Room’s register documents grouped app/helper CPU and memory sampling and local activity history; sampled attribution is not forensic proof.', 'br-capabilities',
      'Path-derived ownership and sampled writes are not proof of the writer of a specific file', 'Capability matrix Apps and Activity', 'Source implementation, not distributed-binary/native performance verification')
claim('B03', 'Breathing Room requires macOS 13+ and Python 3.10+ for inventory; the identified preview is Apple Development signed, not Developer ID signed or notarized.', 'br-capabilities',
      '**Apple Development signed, not Developer ID signed or notarized**', 'Preview/runtime caveats lines 44–56', 'Universal installer advertised; clean-machine and physical Intel execution untested; do not advise protection bypass')
claim('B04', 'Breathing Room’s hosted AI needs authentication and internet and may send relevant paths, process and storage data; local inspection is a separate boundary.', 'br-capabilities',
      'relevant paths/process/storage data can reach the service and Cloudflare Workers AI', 'Local versus hosted boundary lines 58–68', 'Published policy/source register, not backend audit; never entirely offline AI or all-data-stays-on-Mac')
claim('B05', 'Breathing Room’s daily care reuses exact saved approvals while the app runs. Interactive cleanup has an explicit optional automatic verified-Ruff-cache mode.', 'br-capabilities',
      'Automatically move verified Ruff lint caches to Trash', 'Approval modes lines 36–42; Daily care row', 'Source architecture; not an unconditional never-deletes-without-asking promise or runtime test')

hero_meta = load(ROOT / 'assets/github-hero.meta.json')
hero = APP / hero_meta['path']
assert digest(hero) == hero_meta['sha256']
assert hero.read_bytes()[:8] == b'\x89PNG\r\n\x1a\n'
w, h = struct.unpack('>II', hero.read_bytes()[16:24])
br = next(x for x in load(APP / 'docs/content/screenshots.json')['assets'] if x['id'] == 'current-space-browser-preview')
assert digest(pathlib.Path(br['sourcePath'])) == br['sha256']
visuals = [
    {'id': 'purge-official-overview', 'productId': 'purge', 'view': 'Overview with storage categories', 'kind': 'official-asset',
     'sourcePageUrl': 'https://github.com/jithin-sabu/purge-app/blob/v1.12.0/README.md', 'assetUrl': hero_meta['url'],
     'retrievedAtUtc': hero_meta['retrievedAtUtc'], 'capturedAtUtc': None, 'capturedBy': None,
     'productVersion': 'Asset included at v1.12.0; actual capture version not supplied', 'buildOrCommit': 'v1.12.0 repository tag',
     'osVersion': None, 'dataMode': 'vendor-illustration', 'originalPath': hero_meta['path'], 'originalSha256': hero_meta['sha256'],
     'publishedPath': None, 'publishedSha256': None, 'widthPx': w, 'heightPx': h, 'edits': [],
     'privacyReview': {'status': 'reviewed', 'redactions': [], 'notes': 'Opened original PNG; no private paths/accounts visible.'},
     'reuse': {'status': 'cleared', 'basis': hero_meta['reuseBasis'], 'evidenceUrlOrPath': relative(ROOT / 'sources/license-v1.12.0.txt'),
               'credit': 'Purge / Copyright (c) 2026 Jithin Sabu, MIT licence; include full retained notice with published asset.'},
     'caption': 'Official Purge Overview image supplied in its v1.12.0 repository. Vendor illustration, not our scan or measured cleanup result. Purge / Jithin Sabu, MIT licence.',
     'alt': 'Purge Overview app window with App Caches, Dev Tools, Large Files, app removal and Everything else storage rows.',
     'supportedClaimIds': ['P14'], 'limitations': ['Real app view embedded in vendor hero artwork, not a landing-page capture.', 'Promotional safety headline is vendor wording, not our endorsement.', 'Numbers cannot substantiate savings or benchmarks.', 'Bottom of app window is cropped in vendor original; avoid inferring controls outside image.'],
     'review': {'status': 'research-visual-inspected; publication-context-independent-review-pending', 'reviewer': 'research-purge worker', 'reviewedAtUtc': datetime.datetime.now(datetime.timezone.utc).isoformat()}},
    {'id': br['id'], 'productId': 'breathing-room', 'view': br['view'], 'kind': 'browser-preview',
     'sourcePageUrl': br['sourceUrl'], 'assetUrl': None, 'capturedAtUtc': br['capturedOn'], 'retrievedAtUtc': None,
     'productVersion': 'current-source browser preview on 2026-10-21, not a binary', 'buildOrCommit': br['sourceCommit'], 'osVersion': None,
     'dataMode': 'example', 'originalPath': br['sourcePath'], 'originalSha256': br['sha256'], 'publishedPath': None, 'publishedSha256': None,
     'widthPx': br['width'], 'heightPx': br['height'], 'edits': [], 'privacyReview': br['privacyReview'],
     'reuse': {'status': 'cleared', 'basis': br['reuseBasis'], 'evidenceUrlOrPath': 'docs/content/screenshots.json', 'credit': 'Breathing Room, first-party browser preview'},
     'caption': br['caption'], 'alt': br['alt'], 'requiredVisibleLabels': ['Interactive preview · example data', 'This browser preview uses example data. Actions never change your Mac.'],
     'limitations': br['limitations'] + ['Asset URL inapplicable: existing first-party local capture, no new hosted asset created.', 'Source-current at capture only; recheck context/currentness before publication.'],
     'supportedClaimIds': [], 'review': {'status': 'original PNG opened and read in this research job; publication review pending', 'reviewer': 'research-purge worker'}}
]

packet = {
    'schemaVersion': 1, 'jobId': 'research-purge', 'stage': 'research', 'status': 'complete-research-not-publication-approved',
    'assembledAtUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'dateNote': 'Machine UTC retrieval/check date is October 21; scheduled local task date is October 22. Neither is a fabricated later check date.',
    'ownership': {'folder': relative(ROOT), 'websiteEdits': False, 'receiptException': 'docs/content/.runtime/research-purge.1792619917266646000.receipt.json'},
    'identity': {'productId': 'purge', 'officialName': 'Purge', 'canonicalOwnerId': 'purge', 'homepage': baseline['officialUrl'],
                 'repository': 'https://github.com/jithin-sabu/purge-app', 'author': 'Jithin Sabu',
                 'aliases': ['Purge for Mac'], 'aliasDecision': 'Same-product descriptive name, not a second draft. No evidence linking this repository to PowerMyMac; do not transfer facts from similarly named products or the macOS purge command.',
                 'skipSeparateAliasDraft': True, 'skipProductDraft': False, 'classification': 'direct-macos-storage-cleanup-overlap',
                 'classificationReason': 'Documented Mac caches, developer artifacts and reviewable cleanup overlap. App removal and non-AI operation are useful Purge decision factors; process/history investigation is a separately documented Breathing Room emphasis.',
                 'availability': 'Public GitHub non-prerelease v1.12.0 with DMG and checksum asset records; download/install execution untested', 'claimIds': ['P01', 'P03', 'P04', 'P05']},
    'discovery': {**baseline['discovery'], 'edges': entry['edges'], 'directoryCapabilityWarning': 'Directory discovery only. Its nothing-is-ever-lost wording is not usable against explicit official permanent-removal exceptions.'},
    'baselineReuse': {'path': 'docs/content/verification/batch-2.json', 'productId': 'purge', 'fieldsReused': ['identity', 'homepage', 'macOS minimum', 'free offer', 'MIT', 'discovery'], 'unnecessaryHomepageRefetch': False},
    'sources': sources, 'claims': claims,
    'productMatrix': [
        {'dimension': 'macOS / version / offer / licence', 'purgeClaimIds': ['P02','P03','P04','P05'], 'breathingRoomClaimIds': ['B01','B03']},
        {'dimension': 'local versus hosted', 'purgeClaimIds': ['P06'], 'breathingRoomClaimIds': ['B04']},
        {'dimension': 'scan and cleanup model', 'purgeClaimIds': ['P07','P10','P14'], 'breathingRoomClaimIds': ['B02','B05']},
        {'dimension': 'approval and schedule', 'purgeClaimIds': ['P08','P09'], 'breathingRoomClaimIds': ['B05']},
        {'dimension': 'process/helper CPU-memory grouping', 'purge': 'not verified', 'breathingRoomClaimIds': ['B02']},
        {'dimension': 'recurring-growth attribution', 'purge': 'not verified; cleaning history/schedule is not proof of growth attribution', 'breathingRoomClaimIds': ['B02','B04']},
        {'dimension': 'developer cache support', 'purgeClaimIds': ['P10'], 'breathingRoom': 'Source register capability matrix: discovery for npm, uv, pip, pnpm, Go, Bun, Yarn; adapters require installed tools and path validation; not native-tested', 'breathingRoomSourceId': 'br-capabilities'},
        {'dimension': 'install/runtime caveats', 'purgeClaimIds': ['P12','P13'], 'breathingRoomClaimIds': ['B03','B04']},
        {'dimension': 'app removal', 'purgeClaimIds': ['P11'], 'breathingRoom': 'full uninstaller not established; not a verified absence'}
    ],
    'screenshots': visuals,
    'sourceConflicts': [
        {'issue': 'Homepage says never deletes permanently elsewhere, but explicitly lists permanent exceptions.', 'resolution': 'Use qualified P07 and exact exception passage, never blanket reversibility. Directory nothing-is-ever-lost wording rejected.', 'draftBlocking': False},
        {'issue': 'README installation/requirements broadly require Full Disk Access, while Overview/homepage qualify categories that work without it.', 'resolution': 'Use specific P12 category boundary. Do not promise full scan without permission or claim permission needed just to start.', 'draftBlocking': False},
        {'issue': 'Safety page never-touch prose and bundled explanation labels include apparently overlapping protected categories; labels also contain data-loss caveats under generic nothing-is-lost prose.', 'resolution': 'Do not generalize never-touch coverage or no-loss guarantees. No claim that labels establish safety. Any detailed rule assertion needs tagged source inspection.', 'draftBlocking': False}
    ],
    'unknowns': [
        {'field': 'Purge CPU architectures and installer size', 'state': 'not-verified', 'draftBlocking': False, 'treatment': 'Omit architecture and size comparisons.'},
        {'field': 'Purge binary notarization, install, performance and runtime privacy', 'state': 'not-tested', 'draftBlocking': False, 'treatment': 'Attribute documentation; no tested/safe/faster/no-telemetry certification.'},
        {'field': 'Purge process grouping / growth attribution', 'state': 'not-verified', 'draftBlocking': False, 'treatment': 'Use not verified, not No.'},
        {'field': 'Breathing Room binary/source parity and paid service end-to-end behavior', 'state': 'not-tested', 'draftBlocking': False, 'treatment': 'Keep preview/source/hosted limitations and do not promise distributed feature parity.'},
        {'field': 'Vendor screenshot capture date/version and original OS', 'state': 'not-supplied', 'draftBlocking': False, 'treatment': 'Label vendor illustration contained in tag, not verified capture of v1.12.0.'}
    ],
    'briefs': {
        'workflow': {'track': 'search/reference', 'title': 'Review stale developer artifacts before clearing Mac storage', 'slug': 'purge-mac-workflow',
                     'primaryIntent': 'Decide whether an old project artifact is rebuildable, actively used, orphaned, or original data before acting on a cleaner result.',
                     'leadConclusion': 'Review project ownership and rebuild cost before selecting artifacts. Purge documents stale-project and orphaned-worktree rules; those are not permission to discard uncommitted work.',
                     'sections': ['Separate global tool caches from project output and original files', 'Use Purge’s documented stale-project and worktree boundaries without treating age as consent', 'Check rebuild access, offline requirements and unsaved work', 'Distinguish Trash moves from permanent simulator/snapshot operations and actual free-space change', 'Investigate repeat growth before choosing the next cleanup'],
                     'interactionPass': 'Plan a non-mutating checklist: known owner? active terminal/agent? original or reproducible? dependencies available? uncommitted work? Trash or permanent? No filesystem scanning, cleanup buttons, guaranteed savings or forced demo repo.',
                     'visualPlan': ['Official Purge Overview after lead; caption vendor illustration', 'Breathing Room Space later at the investigate-growth decision; retain example-data labels'],
                     'boundaries': 'No copied shell deletion commands or performed-cleanup narrative. Explain build/download costs and preserve backups; add no numeric savings.',
                     'links': ['existing /comparisons/ hub', 'planned /comparisons/purge/ counterpart; validate when created']},
        'comparison': {'title': 'Breathing Room vs Purge for Mac', 'slug': 'purge', 'primaryIntent': 'Choose between documented local non-AI cleaning and a preview that combines storage, activity and hosted assistance.',
                       'format': 'Concise sourced matrix, two bounded reader choices, caveats, link to distinct workflow article; not an expanded duplicate.',
                       'purgeAdvantages': ['Advertised free with no paid tier (P02)', 'Documented local non-AI model (P06)', 'Documented app removal, developer artifact and optional scheduling workflows (P09–P11)', 'Vendor documents notarization; unlike Breathing Room preview disclosure, not independently checked here (P13/B03)'],
                       'breathingRoomFit': 'Breathing Room, which we build, may fit readers investigating app/helper activity alongside storage. Describe source-backed grouping/history, not proven performance or automatic blame (B02).',
                       'tradeoffs': ['Do not sell Breathing Room as production-ready or entirely offline AI (B03/B04)', 'Purge also has schedules and cleanup history; never invent their absence (P09)', 'Neither Trash movement nor category size proves newly free space', 'Unknown Purge monitoring fields remain not verified, not No'],
                       'requiredDisclosures': ['We build Breathing Room', 'Breathing Room example-data browser preview, non-notarized release/Python caveats', 'Free local app versus advertised optional paid hosted AI', 'No installation or cleanup tests performed']}
    },
    'gates': {'identity': 'pass-documentary', 'alias': 'canonical-purge-no-product-skip', 'platformFit': 'direct-mac-overlap',
              'criticalClaimEvidence': 'pass-for-bounded-brief', 'competitorVisual': 'original-inspected-and-MIT-notice-retained',
              'breathingRoomVisual': 'existing-current-source-example-preview-inspected-hash-matched',
              'drafting': 'eligible-only-with-stated-boundaries', 'criticalBlockers': [], 'publication': 'not-approved-independent-review-required'},
    'safety': {'cleanup': False, 'installs': False, 'signups': False, 'credentialsRead': False, 'browserCookieExtraction': False,
               'commitsPushesDeployments': False, 'queueMutation': False, 'websiteEdits': False, 'subagents': False,
               'browser': 'Skill loaded; no Chrome interactions necessary. Reused directory evidence; missing official material retrieved read-only over public HTTP.'}
}
(ROOT / 'research.json').write_text(json.dumps(packet, indent=2, ensure_ascii=False) + '\n')
print('Wrote', relative(ROOT / 'research.json'), 'with', len(claims), 'claims,', len(sources), 'sources and', len(visuals), 'visuals')
