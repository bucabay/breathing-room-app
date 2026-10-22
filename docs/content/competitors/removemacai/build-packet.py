"""Assemble retained evidence into a research packet, without further network access."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
PREFIX = str(ROOT.relative_to(APP))
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sources = json.loads((ROOT / 'sources/ledger.json').read_text())
baseline = next(p for p in json.loads((APP / 'docs/content/verification/batch-2.json').read_text())['records'] if p['id'] == 'removemacai')
for key, path, url, time in [
    ('baseline-home', baseline['sources'][0]['rawCapture'], baseline['officialUrl'], baseline['sources'][0]['retrievedAt']),
    ('discovery', baseline['discovery']['rawCapture'], baseline['discovery']['sourceUrl'], baseline['discovery']['retrievedAt']),
]:
    sources.append({'id': key, 'url': url, 'finalUrl': url, 'retrievedAtUtc': time,
                    'path': path, 'sha256': sha(APP / path), 'reuse': 'Existing verified record, not re-fetched.'})
sources.append({'id': 'br-capabilities', 'url': 'https://breathing-room.chatic.ai/',
                'path': 'docs/content/capabilities.md', 'sha256': sha(APP / 'docs/content/capabilities.md'),
                'retrievedAtUtc': None, 'checkedOn': '2026-10-21',
                'scope': 'Reused first-party source and public-page register; individual public URLs and code locators retained in the register. Not newly runtime-tested.'})
by_id = {s['id']: s for s in sources}
claims = []


def claim(key, wording, source, excerpt, scope='v1.1.4 documentation; not hands-on tested', location='comparison matrix', state='verified'):
    claims.append({'id': key, 'wording': wording, 'sourceIds': [source], 'sourceUrls': [by_id[source]['url']],
                   'excerpt': excerpt, 'checkedAtUtc': by_id[source].get('retrievedAtUtc'),
                   'checkedOn': by_id[source].get('checkedOn') or by_id[source]['retrievedAtUtc'][:10],
                   'evidenceClass': 'officially-documented' if source != 'br-capabilities' else 'reused-first-party-register',
                   'scope': scope, 'intendedLocation': location, 'state': state,
                   'reviewer': 'research-removemacai documentary worker', 'unresolvedQuestions': []})


claim('identity', 'RemoveMacAI is Om Lahore’s project at omlahore/RemoveMacAI, linked from its official homepage.', 'baseline-home', 'Made by\nOm Lahore\n·\nSource', 'Homepage identity and retained source link')
claim('function', 'RemoveMacAI documents turning off Apple Intelligence, removing its models and selectively keeping features enabled.', 'readme-release', 'The models are deleted and blocked from downloading again. Keep any feature you use.')
claim('platform-release', 'The v1.1.4 README requires Apple silicon and supports macOS 27; it says 26 and earlier are unsupported.', 'readme-release', '| 27 | Supported, tested on 27.0. On 27.0.1, use 0.2.3 or later. |\n| 26 and earlier | Not supported |')
claim('platform-main', 'The main-branch README separately says macOS 26 runs since 1.1.0 and 15.1+ is in testing using 1.2.0-beta.1.', 'readme-main', '| 26 | Runs since 1.1.0. Most of the testing has been on 27. |', 'Main-branch documentation only; conflicts with release-tag requirements. Do not market macOS 26/15 support for v1.1.4.')
claim('price', 'The official homepage describes RemoveMacAI as free and open source.', 'baseline-home', 'Free and open source.', 'Free advertised software; no paid tier, currency or subscription condition established. Optional sponsorship is not a purchase requirement.')
claim('license', 'The repository is MIT licensed, with copyright and permission notices required for copies/substantial portions.', 'license', 'Copyright (c) 2026 omlahore\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files', 'MIT scope includes associated documentation; retain full licence with copied documentation screenshot.')
release = json.loads((ROOT / 'sources/release.json').read_text())
claim('release', 'GitHub latest-release metadata identifies v1.1.4, published October 18, 2026, with app ZIP and arm64 CLI assets.', 'release', '"tag_name":"v1.1.4"', 'GitHub metadata only; binaries not downloaded, signatures and operation not tested.')
claim('review', 'The documented CLI asks before apply, undo, background and clean; --dry-run stops before changing, while --yes skips confirmation.', 'readme-release', '`apply`, `undo`, `background` and `clean` show the change first and ask. `--dry-run` shows it and stops, and `--yes` skips the question.')
claim('profile', 'Locked settings use a configuration profile approved in System Settings; other preferences have a previous-value journal.', 'readme-release', 'Removing the profile undoes all of them.', location='workflow / approval boundaries')
claim('trash-exceptions', 'Storage cleanup generally moves files to Trash, but unavailable simulators and Time Machine local snapshots are deleted immediately by simctl/tmutil.', 'readme-release', 'Unavailable simulators and Time Machine local snapshots are deleted right away by `simctl` and `tmutil`.', location='workflow / irreversible-action warning')
claim('timing', 'The README warns macOS deletes released model files on its own schedule, so Storage may continue counting them.', 'readme-release', "Apple's asset service releases the models right away, but macOS deletes the files on its own schedule.", location='workflow / measurement boundary')
claim('feature-loss', 'Turning Apple Intelligence off affects listed features and apps using the Foundation Models framework, Use Model in Shortcuts, Visual Intelligence and Calendar natural-language editing.', 'readme-release', 'apps that use Apple\'s on-device models (the Foundation Models framework and the Use Model action in Shortcuts), Visual Intelligence and natural-language editing in Calendar.', location='workflow / decision checklist')
claim('storage', 'Documented storage targets include installers, wallpaper videos, iOS update files, Xcode data, unavailable simulators, app caches and local Time Machine snapshots.', 'readme-release', '| Storage | Old macOS installers, aerial wallpaper videos, iPhone and iPad update files, Xcode build data and device support, unavailable simulators, app caches, Time Machine local snapshots,', location='comparison matrix / developer caches')
claim('background', 'RemoveMacAI documents listing other apps’ background updaters/helpers and switching them individually.', 'readme-release', "Updaters and helpers other apps install, such as Google's updater, shown with what they run and switched off one by one")
claim('local', 'The author says RemoveMacAI makes no network requests and collects no data; this is a vendor assertion, not an independent privacy audit.', 'readme-release', 'RemoveMacAI makes no network requests and collects no data.', 'Documented runtime claim; installation/download uses network. No blanket security guarantee.')
claim('install', 'The app README discloses it is not notarized; manual ZIP and Homebrew CLI distribution are documented.', 'readme-release', 'The app is not notarized', 'No installation performed. Do not reproduce remote-shell execution or advise disabling protections.')
claim('sip', 'The README says SIP stays on and nothing under /System is modified; sealed built-in apps are not removed.', 'readme-release', 'System Integrity Protection stays on, nothing under `/System` is modified', 'Vendor documentation, not verified execution.')
claim('pared', 'RemoveMacAI builds its Apple Intelligence work on pared by 4evy; this is an acknowledged upstream, not a verified same-product alias.', 'third-party', 'RemoveMacAI builds on [pared](https://github.com/4evy/pared) by 4evy.', 'Separate named upstream. Do not merge product identities merely because code/work is reused.')
claim('br-offer', 'Breathing Room is a free Apache-2.0 macOS preview; optional AI Care is advertised at $5 USD/month or $50 USD/year, renewing until cancelled, with applicable tax at checkout.', 'br-capabilities', 'Plans renew until cancelled; applicable tax shown at checkout.', 'Reused 2026-10-21 register §§ pricing/access/licence, not checkout testing.')
claim('br-caveats', 'Breathing Room preview identifies 0.1.0-preview.1, macOS 13+, advertised universal installer, Python 3.10+ prerequisite, and no Developer ID signing/notarization or physical-Intel runtime validation.', 'br-capabilities', 'Apple Development signed, not Developer ID signed or notarized', 'Reused register §§ preview/install; distributed binary parity remains unverified.')
claim('br-tools', 'Breathing Room source implements storage exploration, grouped CPU/memory sampling and activity history; this is not evidence it removes Apple Intelligence models.', 'br-capabilities', 'Source supports category, app/tool-owner, project, folder and large-file views.', 'Source implementation versus release behavior explicitly separated.')
claim('br-hosted', 'Breathing Room hosted AI needs internet/authentication and can receive relevant paths/process/storage data; local inspection is distinct from hosted AI.', 'br-capabilities', 'Hosted AI assistance requires internet access and authentication', 'Reused local/hosted register; no entirely-offline AI or blanket privacy promise.')
claim('br-approval', 'Breathing Room default investigation reviews exact actions; optional verified Ruff-cache automation and saved daily-care approvals have separate boundaries.', 'br-capabilities', 'only remembered exact approvals are eligible.', 'Reused approval exception section; app must remain running for scheduled care.')

screens = json.loads((APP / 'docs/content/screenshots.json').read_text())
br = next(a for a in screens['assets'] if a['id'] == 'current-space-browser-preview')
image = by_id['competitor-ui']
visuals = [
    {'id': 'removemacai-overview', 'productId': 'removemacai', 'view': 'Overview', 'kind': 'official-asset',
     'sourcePageUrl': 'https://github.com/omlahore/RemoveMacAI/blob/v1.1.4/README.md', 'assetUrl': image['url'],
     'capturedAtUtc': None, 'retrievedAtUtc': image['retrievedAtUtc'], 'capturedBy': None,
     'productVersion': None, 'buildOrCommit': 'Asset distributed in v1.1.4 tag; actual UI capture build unknown', 'osVersion': None,
     'dataMode': 'vendor-illustration', 'originalPath': image['path'], 'originalSha256': image['sha256'],
     'publishedPath': None, 'publishedSha256': None, 'widthPx': 2000, 'heightPx': 1400, 'edits': [],
     'privacyReview': {'status': 'reviewed', 'redactions': [], 'notes': 'App overview; no personal account, paths or inventory identifiers visible.'},
     'reuse': {'status': 'cleared', 'basis': 'Repository MIT grant expressly includes associated documentation files; screenshot is the README documentation asset. No separate screenshot restriction found in inspected notices. Preserve complete licence/notice with reuse; no trademark endorsement inferred.',
               'evidenceUrlOrPath': PREFIX + '/sources/LICENSE.txt', 'credit': 'RemoveMacAI by Om Lahore; MIT, copyright (c) 2026 omlahore.',
               'conditions': ['Carry complete MIT notice with distributed image.', 'Retain third-party notices conservatively.', 'Recheck context and attribution during independent review.']},
     'caption': 'Official RemoveMacAI Overview image distributed with v1.1.4 documentation. Vendor illustration, not our test; the displayed 16.1 GB is not measured savings or a guarantee.',
     'alt': 'RemoveMacAI Overview with Apple Intelligence status, background items, storage estimate and two reviewable presets.',
     'supportedClaimIds': ['function', 'review', 'background'], 'limitations': ['Actual capture time, OS and app build not provided.', 'Visible safe-by-design and undo claims are vendor UI copy, not our guarantee.', 'Snapshot/simulator exceptions still apply.'],
     'review': {'status': 'research-visually-inspected', 'reviewer': 'research-removemacai worker', 'reviewedAtUtc': now}},
    {'id': br['id'], 'productId': 'breathing-room', 'view': br['view'], 'kind': 'browser-preview',
     'sourcePageUrl': br['sourceUrl'], 'assetUrl': None, 'capturedAtUtc': br['capturedOn'], 'retrievedAtUtc': None,
     'capturedBy': 'screenshot-library worker (existing record)', 'productVersion': None, 'buildOrCommit': br['sourceCommit'],
     'osVersion': None, 'dataMode': 'example', 'originalPath': str(Path(br['sourcePath']).relative_to(APP)),
     'originalSha256': br['sha256'], 'publishedPath': None, 'publishedSha256': None,
     'widthPx': br['width'], 'heightPx': br['height'], 'edits': [], 'privacyReview': br['privacyReview'],
     'reuse': {'status': 'cleared', 'basis': br['reuseBasis'], 'evidenceUrlOrPath': 'docs/content/screenshots.json', 'credit': 'Breathing Room, which we build.'},
     'caption': br['caption'], 'alt': br['alt'], 'supportedClaimIds': ['br-tools'],
     'limitations': br['limitations'] + ['Keep both example-data notices visible. Current-source as captured October 21, not a claim of current binary parity.'],
     'review': {'status': 'research-visually-inspected', 'reviewer': 'research-removemacai worker', 'reviewedAtUtc': now}}
]
matrix = {
    'macOSCompatibility': ['platform-release', 'platform-main'], 'license': ['license'],
    'localOrHosted': ['local'], 'scanCleanupModel': ['function', 'storage', 'trash-exceptions'],
    'approvalControls': ['review', 'profile'], 'helperManagement': ['background'],
    'developerCaches': ['storage'], 'pricing': ['price'], 'installation': ['install', 'sip'], 'availability': ['release']
}
packet = {
    'schemaVersion': 1, 'jobId': 'research-removemacai', 'productId': 'removemacai', 'stage': 'research',
    'status': 'complete-research-not-publication-approval', 'assembledAtUtc': now,
    'identity': {'officialName': 'RemoveMacAI', 'author': 'Om Lahore / omlahore', 'homepage': baseline['officialUrl'],
                 'repository': 'https://github.com/omlahore/RemoveMacAI', 'canonicalOwnerId': 'removemacai',
                 'aliases': ['removemacai (CLI executable; same product)'], 'aliasSkipDecision': 'Do not skip: distinct canonical product. App and CLI share one packet and must not get separate doorway drafts. pared is acknowledged upstream, not a verified alias. No evidence links this product to PowerMyMac.',
                 'classification': 'adjacent', 'reason': 'Mac configuration/Apple Intelligence de-bloating plus targeted storage cleanup overlaps maintenance; not a like-for-like storage/activity investigation replacement.',
                 'platformIntent': 'Native Mac reader intent; no Windows/Linux replacement or compatibility claims.'},
    'ownership': {'allowedFolder': PREFIX, 'websiteEdits': False, 'queueEdits': False},
    'method': {'baselineReusedFirst': 'docs/content/verification/batch-2.json#removemacai',
               'homepageRefetched': False, 'directoryRefetched': False, 'browserUsed': False, 'productExecuted': False,
               'note': 'Public HTTP reads and image inspection only. UTC timestamps reflect actual clock; local task date is October 22. New official material retained as raw bytes; no installs or cleanup.'},
    'discovery': {**baseline['discovery'], 'sourceId': 'discovery', 'seedUrl': 'https://alternativeto.net/software/mole/',
                  'edgeUrl': 'https://alternativeto.net/software/mole/?p=2', 'edgeRetrievedAtUtc': '2026-10-21T18:37:09.298Z',
                  'edgeBasis': 'Reused docs/content/competitors.json record; raw edge response not independently retained here. About-page raw snapshot and hash retained by baseline.'},
    'sources': sources, 'claims': claims, 'matrix': matrix,
    'notVerifiedMatrixCells': {'groupedHelperCPUAndMemory': 'not verified; background toggles are not grouped resource monitoring',
                               'recurringGrowthMonitoring': 'not verified', 'runtimeDependencies': 'Exact prerequisites for CLI/source-build not verified; no Python requirement inferred.',
                               'allDeveloperCaches': 'Only documented Xcode data/app caches; npm/pnpm/etc support not verified.'},
    'sourceConflicts': [
        {'topic': 'macOS requirements', 'resolution': 'Scope v1.1.4 recommendation to documented macOS 27 Apple silicon. Main-branch macOS 26/15 claims are separate, not binary validation. No installation recommendation for older OSes.', 'claimIds': ['platform-release', 'platform-main']},
        {'topic': 'Reversible cleanup', 'resolution': 'README specific immediate simctl/tmutil deletion overrides broad homepage files-go-to-Trash/undo wording. Never promise all cleanup is reversible.', 'claimIds': ['trash-exceptions', 'review']}
    ],
    'visuals': visuals,
    'briefs': {
        'workflow': {'track': 'search-reference', 'title': 'Apple Intelligence models or ordinary clutter? Choose the cleanup scope first',
                     'slug': 'apple-intelligence-models-versus-mac-clutter',
                     'primaryIntent': 'Decide whether unwanted Apple Intelligence/configuration changes or broader disk growth is the actual Mac maintenance job.',
                     'description': 'RemoveMacAI addresses unwanted Apple Intelligence and selected macOS settings; broader disk growth needs a different investigation. Start with feature dependencies, OS support and cleanup reversibility, not a promised number of gigabytes.',
                     'sections': ['Decide which AI-dependent features you still need', 'Separate a settings/profile change from file cleanup', 'Check macOS 27 and Apple silicon before considering v1.1.4', 'Review exact changes and distinguish Trash from immediate deletion', 'Do not confuse released models with immediately available space', 'Use wider storage investigation when the source of growth is unknown'],
                     'interaction': 'Non-executing checklist: OS/architecture, features to retain, configuration vs storage goal, immediate-deletion acceptance. Do not generate removal commands or suggest bypassing security controls.',
                     'visualPlan': 'Official RemoveMacAI Overview after lead with vendor-data caveat; current-source Breathing Room Space later with full example-data banner/caption.',
                     'links': ['/comparisons/', '/comparisons/removemacai/', '/tools/'],
                     'mustNotClaim': ['Guaranteed GB recovery', 'Hands-on testing', 'Safe or fully reversible cleanup', 'Breathing Room removes Apple Intelligence', 'macOS 26/15 binary support resolved']},
        'comparison': {'title': 'Breathing Room vs RemoveMacAI: investigation or de-bloating?', 'slug': 'removemacai',
                       'primaryIntent': 'Select between adjacent tools by task, rather than rank them as interchangeable cleaners.',
                       'leadDecision': 'For selective Apple Intelligence/configuration changes on the documented supported platform, RemoveMacAI is the documented fit. For wider storage/app activity investigation, consider Breathing Room, which we build, with its preview, Python and hosted-AI caveats.',
                       'rows': list(matrix) + ['groupedHelperCPUAndMemory', 'recurringGrowthMonitoring'],
                       'links': ['/comparisons/', '/blog/apple-intelligence-models-versus-mac-clutter/'],
                       'format': 'Concise claim-linked matrix and two bounded decision paragraphs; no second alternatives route.'}
    },
    'advantagesAndTradeoffs': {
        'competitorAdvantages': ['Documents selective Apple Intelligence disable/model removal and profile export for MDM.', 'Free MIT app and CLI share undo history; review/dry-run controls are documented.', 'Documents configuration/background-updater controls beyond storage scanning.'],
        'competitorTradeoffs': ['v1.1.4 tagged requirements are macOS 27/Apple silicon; main docs differ.', 'Not notarized; no runtime or binary security audit performed.', 'AI-dependent features stop working; configuration undo is not guaranteed restoration of immediately deleted storage.', 'Disabling app updaters may trade background activity for responsibility to maintain updates (editorial caution, not tested outcome).'],
        'breathingRoomAdvantages': ['Source-based storage ownership/project views and grouped app/process monitoring suit a different investigation job.', 'Source includes activity history and constrained saved daily approvals, with limitations in capabilities.md.'],
        'breathingRoomTradeoffs': ['Preview, Python prerequisite, non-notarized release and unvalidated physical Intel runtime.', 'Hosted AI requires authentication/internet and may transmit relevant metadata; optional AI Care is paid.', 'No verified Apple Intelligence model-removal capability; do not recommend it for that specific task.']
    },
    'noncriticalUnknowns': ['Exact screenshot capture build/date/OS', 'Independent runtime/privacy/savings benchmarks', 'Grouped-helper resource reporting and recurring-growth features in RemoveMacAI', 'Older-OS release support conflict beyond the conservative macOS 27 scope', 'Source-build runtime prerequisites and installer success'],
    'draftGate': {'readyForBoundedDraft': True, 'criticalBlockers': [], 'conditions': ['Keep platform scope conservative and conflicts visible.', 'Carry screenshot MIT notice and credit into future asset distribution.', 'Preserve example-data and vendor-illustration disclosures.', 'Leave both pages draft and unpublished; independent current snapshot/browser/site QA still required.'],
                  'publicationApproved': False, 'independentReview': 'pending-separate-stage'},
    'validation': {'logPath': PREFIX + '/validation.json', 'siteChecks': 'Not applicable: no marketing content changed.', 'runtimeTests': 'Not performed; no product code executed.'}
}
(ROOT / 'research.json').write_text(json.dumps(packet, indent=2) + '\n')
print('Assembled', len(claims), 'claims and', len(sources), 'sources.')
