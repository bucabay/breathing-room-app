"""Assemble documentary evidence, not article copy or publication approval."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
now = datetime.now(timezone.utc).isoformat()
manifest = json.loads((ROOT / 'sources/manifest.json').read_text())
visual = json.loads((ROOT / 'sources/visual-download.json').read_text())
release = json.loads((ROOT / 'sources/release.json').read_text())
batch = json.loads((APP / 'docs/content/verification/batch-2.json').read_text())

def find_product(value):
    if isinstance(value, dict):
        if value.get('id') == 'cleanmylinux' and 'facts' in value:
            return value
        for child in value.values():
            found = find_product(child)
            if found:
                return found
    if isinstance(value, list):
        for child in value:
            found = find_product(child)
            if found:
                return found

baseline = find_product(batch)
assert baseline
(ROOT / 'sources/baseline-record.json').write_text(json.dumps(baseline, indent=2) + '\n')
for name in ['official', 'directory']:
    src = APP / f'docs/content/.runtime/verification-2/cleanmylinux-{name}.json'
    expected = baseline['sources'][0]['sha256'] if name == 'official' else baseline['discovery']['sha256']
    assert hashlib.sha256(src.read_bytes()).hexdigest() == expected
    (ROOT / f'sources/baseline-{name}.json').write_bytes(src.read_bytes())

sources = [{'id': s['id'], 'publisher': 'Better Linux / GitHub', **s} for s in manifest['sources']]
sources += [
    {'id': 'baseline-home', 'publisher': 'Better Linux', 'url': baseline['officialUrl'],
     'finalUrl': baseline['finalUrl'], 'retrievedAtUtc': baseline['sources'][0]['retrievedAt'],
     'path': 'sources/baseline-official.json', 'sha256': baseline['sources'][0]['sha256'],
     'reusedFrom': 'docs/content/verification/batch-2.json#cleanmylinux'},
    {'id': 'discovery', 'publisher': 'AlternativeTo', 'url': baseline['discovery']['sourceUrl'],
     'retrievedAtUtc': baseline['discovery']['retrievedAt'], 'path': 'sources/baseline-directory.json',
     'sha256': baseline['discovery']['sha256'], 'evidenceClass': 'discovery-only'},
    {'id': 'br-capabilities', 'publisher': 'Breathing Room', 'url': 'https://breathing-room.chatic.ai/',
     'path': 'docs/content/capabilities.md', 'retrievedAtUtc': '2026-10-21',
     'scope': 'Reused same-day public release/pricing/privacy review, not newly fetched or runtime-tested.'},
]
for name in ['README.md', 'src-tauri/tauri.conf.json', 'src/billing-config.json', 'src/components/cleanup-assistant.tsx']:
    data = (APP / name).read_bytes()
    dest = 'sources/br-' + name.replace('/', '-')
    (ROOT / dest).write_bytes(data)
    sources.append({'id': 'br-' + name, 'publisher': 'Breathing Room',
                    'url': 'https://github.com/bucabay/breathing-room-app',
                    'localSourcePath': name, 'path': dest, 'retrievedAtUtc': now,
                    'sha256': hashlib.sha256(data).hexdigest(),
                    'scope': 'Current working-tree source; not a release-binary certification.'})

claims = []
def claim(id, wording, source, excerpt, locator, state='verified', conditions=None):
    s = next(x for x in sources if x['id'] == source)
    claims.append({'id': id, 'wording': wording, 'sourceIds': [source], 'sourceUrl': s['url'],
                   'excerpt': excerpt, 'locator': locator, 'checkedAtUtc': s['retrievedAtUtc'],
                   'evidenceClass': 'documented-not-hands-on', 'state': state,
                   'conditions': conditions, 'intendedLocation': 'Brief and comparison matrix',
                   'reviewer': 'research-cleanmylinux worker; independent review pending'})

claim('identity', 'CleanMyLinux is a Better Linux project; the official site links the Better-Linux/CleanMyLinux repository.',
      'baseline-home', 'View on GitHub → https://github.com/Better-Linux/CleanMyLinux', 'links[2] and footer © 2026 Better Linux')
claim('platform', 'CleanMyLinux is designed exclusively for Linux desktops, not a native Mac replacement on the same OS.',
      'baseline-home', 'designed exclusively for modern Linux desktops.', 'text footer', conditions='No macOS or Windows support is inferred from Tauri.')
claim('scope', 'The homepage advertises cache cleaning, app resets and package-update checks.',
      'baseline-home', 'Clean caches, reset app states, and check for package updates with complete peace of mind.',
      'text footer', conditions='Attribute to vendor. Do not repeat safety, speed or risk-free wording as tested fact.')
claim('license', 'The repository is MIT licensed, with copyright/permission-notice retention required.',
      'LICENSE', 'Copyright (c) 2026 Better Linux\nPermission is hereby granted, free of charge', 'lines 1–13',
      conditions='Licence covers software and associated documentation; not an endorsement or trademark licence.')
claim('apps', 'The README documents application discovery, disk-usage analysis, uninstallation and app resetting under completed Phase 2.',
      'README.md', 'Per-application disk usage analysis (binary size + local caches + configurations).',
      'Project Roadmap / Phase 2, lines 92–96', conditions='Current main documentation, not proof of feature parity in beta.2 binary.')
claim('updates', 'The README documents APT, Pacman, DNF, Flatpak and Snap update management.',
      'README.md', 'Native Packages: Support for Debian/Ubuntu (`APT`), Arch Linux (`Pacman`), and Fedora/Red Hat (`DNF`).',
      'Universal Updates, lines 47–50', conditions='No update executed. No claim this updates every app or fixes every package.')
claim('auth', 'The README says the GUI runs unprivileged and requests PolicyKit authentication for administrative tasks.',
      'README.md', 'The main graphical interface runs entirely as a standard unprivileged user.',
      'Uncompromising Security, line 53', conditions='Authentication design is not a guarantee against destructive actions or per-path cleanup approval.')
claim('roadmap', 'The README places junk cleaning in Current Focus and disk analysis/real-time resource monitors in later roadmap phases.',
      'README.md', 'Phase 3: System Junk Cleaner (Current Focus)', 'Project Roadmap, lines 97–108',
      conditions='Do not treat roadmap as shipped, or claim these capabilities are absent; release packaging already exists despite a later packaging roadmap item.')
claim('compatibility-conflict', 'Exact minimum binary-compatible Linux distribution versions are unresolved.',
      'README.md', 'Ubuntu | `22.04 LTS` ... GLIBC version older than `2.39` ... pre-compiled binary will fail to launch.',
      'Supported Distributions, lines 25–36', 'not-verified',
      'The listed older distro minimums and GLIBC requirement are not reconciled. Do not recommend a specific minimum or certify installation. Arch is explicitly not tested yet.')
claim('version', 'The GitHub latest-release endpoint returns v1.0.0-beta.2, published May 25, 2026.',
      'release.json', '"tag_name": "v1.0.0-beta.2"; "published_at": "2026-05-25T05:19:04Z"; "prerelease": false',
      'tag_name/published_at/prerelease', conditions='Version name says beta even though GitHub prerelease flag is false. Do not call this production-stable.')
claim('downloads', 'Public release metadata lists x86_64 RPM, amd64 AppImage and amd64 DEB downloads.',
      'release.json', '; '.join(x['name'] for x in release['assets']), 'assets[].name/browser_download_url',
      conditions='Only metadata retrieved; no executables downloaded, installed or checksum-tested. No ARM/macOS/Windows support inferred.')
claim('pricing', 'MIT permission is granted free of charge and public release download links are listed; no commercial price or plan was verified.',
      'LICENSE', 'Permission is hereby granted, free of charge', 'lines 5–10',
      conditions='Licence permission is not a $0 commercial offer or guarantee of support, lifetime updates or hosted entitlement. “Premium” is not a price.')
claim('br-install', 'Breathing Room is a non-notarized macOS 13+ preview requiring Python 3.10+ for disk inventory; physical Intel runtime testing remains unverified.',
      'br-README.md', 'The preview is not notarized. ... macOS 13 or later ... Python 3.10+ ... release has not been runtime-tested on physical Intel hardware.',
      'lines 59–72', conditions='Published release caveats reused from capabilities.md; no new installation or binary test.')
claim('br-version', 'Current Breathing Room config identifies 0.1.0-preview.1.',
      'br-src-tauri/tauri.conf.json', '"version": "0.1.0-preview.1"', 'line 4', conditions='Source config, not a latest-channel guarantee.')
claim('br-workflow', 'Breathing Room documents Space inventory, grouped Apps CPU/memory and Activity investigation.',
      'br-README.md', 'Use Apps to inspect CPU and memory use across an app and its helpers.',
      'lines 76–84,102–118', conditions='Inventories may be partial; sampled I/O and path ownership are not proof a process wrote a particular file.')
claim('br-price', 'Breathing Room advertises a free core app and optional AI Care at $5 USD/month or $50 USD/year.',
      'br-README.md', 'AI Care is optional: $5 USD/month or $50 USD/year.', 'lines 141–150',
      conditions='Same-day public pricing reused from capabilities.md: recurring, cancelable, applicable tax at checkout; no unlimited-AI promise. Legacy appAmount field is not a purchase offer.')
claim('br-hosted', 'Agent-assisted workflows need authentication and a hosted service connection, unlike local storage/process tools.',
      'br-README.md', 'Agent-assisted workflows require an authenticated hosted service connection.', 'lines 64–70,143–145',
      conditions='Relevant paths/process/storage/tool data can leave the Mac per public privacy policy in capabilities.md. Never describe all AI as offline.')
claim('br-approval', 'Ordinary cleanup requires action review, but optional automatic verified Ruff-cache mode must be disclosed.',
      'br-src/components/cleanup-assistant.tsx', 'Automatically move verified Ruff lint caches to Trash', 'line 198',
      conditions='Do not claim blanket “never changes anything without asking each time”. Scheduled care reuses exact prior approvals, must remain running; README lines 120–128.')

br = next(x for x in json.loads((APP / 'docs/content/screenshots.json').read_text())['assets'] if x['id'] == 'current-space-browser-preview')
assert hashlib.sha256(Path(br['sourcePath']).read_bytes()).hexdigest() == br['sha256']
image = {
    'id': 'cleanmylinux-applications-preview', 'productId': 'cleanmylinux', 'view': 'Applications start screen',
    'kind': 'official-asset', 'sourcePageUrl': f'https://github.com/Better-Linux/CleanMyLinux/blob/{manifest["commit"]}/README.md#preview',
    'assetUrl': visual['url'], 'capturedAtUtc': None, 'retrievedAtUtc': visual['retrievedAtUtc'],
    'capturedBy': None, 'productVersion': None, 'buildOrCommit': manifest['commit'], 'osVersion': None,
    'dataMode': 'vendor-illustration', 'originalPath': visual['path'], 'originalSha256': visual['sha256'],
    'publishedPath': None, 'publishedSha256': None, 'widthPx': visual['widthPx'], 'heightPx': visual['heightPx'],
    'edits': [], 'privacyReview': {'status': 'reviewed', 'redactions': [], 'notes': 'No account, filenames or inventory results visible.'},
    'reuse': {'status': 'cleared', 'basis': visual['reuseBasis'], 'evidenceUrlOrPath': 'sources/LICENSE',
              'credit': 'CleanMyLinux / Better Linux. Copyright (c) 2026 Better Linux. MIT License; include complete licence notice.'},
    'caption': 'CleanMyLinux official repository preview of the Applications screen. Vendor-provided image; app version, capture date and OS are not supplied. No scan or cleanup was performed for this article.',
    'alt': 'CleanMyLinux Applications start screen with app-management description and a Scan button.',
    'supportedClaimIds': ['apps'], 'limitations': ['No results shown; not proof of scan accuracy, safety, performance or release-version parity.', 'Do not label the generic window controls as evidence of Windows support.'],
    'review': {'status': 'research-visual-inspected', 'reviewer': 'research-cleanmylinux worker', 'reviewedAtUtc': now,
               'notes': 'Opened actual 1194×797 PNG with image read tool: Applications title, sidebar app icon, settings and Scan button; no fabricated UI.'}}

matrix = {
    'platform': {'cleanmylinux': 'Linux desktops; exclusive official positioning', 'claims': ['platform', 'downloads'], 'breathingRoomClaims': ['br-install']},
    'licence': {'cleanmylinux': 'MIT', 'claims': ['license'], 'breathingRoom': 'Apache-2.0 desktop source, per capabilities.md; hosted service distinct'},
    'operation': {'cleanmylinux': 'Desktop app / native package tools documented; comprehensive network/telemetry model not verified', 'claims': ['auth', 'updates'], 'breathingRoomClaims': ['br-hosted']},
    'scanCleanup': {'cleanmylinux': 'App management documented; cache-cleaner scope/current release parity unresolved', 'claims': ['apps', 'scope', 'roadmap'], 'breathingRoomClaims': ['br-workflow', 'br-approval']},
    'approval': {'cleanmylinux': 'PolicyKit for admin actions documented; exact-location cleanup approval not verified', 'claims': ['auth'], 'breathingRoomClaims': ['br-approval']},
    'helperGrouping': {'cleanmylinux': 'not verified', 'claims': ['roadmap'], 'breathingRoomClaims': ['br-workflow']},
    'recurringGrowth': {'cleanmylinux': 'not verified; later monitoring roadmap is not an absence claim', 'claims': ['roadmap'], 'breathingRoomClaims': ['br-workflow']},
    'developerCaches': {'cleanmylinux': 'Specific npm/pnpm/uv/etc adapter support not verified', 'claims': ['scope'], 'breathingRoom': 'Source-level cache discovery recorded in capabilities.md; not universal runtime certification'},
    'pricing': {'cleanmylinux': 'MIT free-of-charge permission; public assets; commercial price/conditions not verified', 'claims': ['pricing', 'downloads'], 'breathingRoomClaims': ['br-price']},
    'installation': {'cleanmylinux': 'x86 Linux release formats observed; distro/GLIBC minimum conflict; no executable test', 'claims': ['downloads', 'compatibility-conflict'], 'breathingRoomClaims': ['br-install', 'br-version']}
}
packet = {
    'schemaVersion': 1, 'jobId': 'research-cleanmylinux', 'productId': 'cleanmylinux', 'officialName': 'CleanMyLinux',
    'canonicalOwnerId': 'cleanmylinux', 'vendor': 'Better Linux', 'homepage': baseline['finalUrl'],
    'repository': 'https://github.com/Better-Linux/CleanMyLinux', 'aliases': [],
    'aliasDecision': {'skipSeparateDraft': False, 'status': 'distinct-official-identity-verified',
                      'rationale': 'Official site and repository reciprocally identify CleanMyLinux / Better Linux. No verified alternate product identity; CleanMyMac and PowerMyMac are not inferred aliases from naming similarity.'},
    'classification': 'adjacent-platform-specific', 'platformFit': 'Linux-to-Mac replacement intent only; not a same-platform substitute or Linux-capable Breathing Room.',
    'decision': {'researchStatus': 'complete-with-bounded-unknowns', 'skip': False, 'drafting': 'eligible-only-for-bounded-Mac-transition-brief',
                 'publicationApproved': False, 'criticalBlockers': [],
                 'blockedClaims': ['Exact minimum Linux binary compatibility: README distro table conflicts with GLIBC 2.39 warning.', 'Any runtime, performance, savings, stable-release, complete-offline, or feature-parity claim without new evidence.'],
                 'diagnostic': 'Identity, platform, release metadata and two authentic visual sources established. Unknown commercial terms and minimum Linux compatibility are explicitly excluded from recommendation claims; do not draft a Linux installation guide.'},
    'timePolicy': 'Actual retrieval timestamps are UTC from tools/system clock (2026-10-21); local scheduled date is October 22. Do not invent later retrieval dates.',
    'researchedAtUtc': now, 'sourceCommit': manifest['commit'], 'release': {
        'tag': release['tag_name'], 'publishedAtUtc': release['published_at'], 'apiPrereleaseFlag': release['prerelease'],
        'labelPolicy': 'Preserve beta in version name; false API prerelease flag does not certify production stability.',
        'url': release['html_url'], 'assets': [{'name': a['name'], 'url': a['browser_download_url'], 'vendorDigest': a.get('digest'), 'downloaded': False} for a in release['assets']]},
    'discovery': {**baseline['discovery'], 'ownedRetainedCopy': 'sources/baseline-directory.json',
                  'edges': next(x for x in json.loads((APP / 'docs/content/competitors.json').read_text())['competitors'] if x['id'] == 'cleanmylinux')['edges']},
    'sources': sources, 'claims': claims, 'matrix': matrix,
    'visuals': [image, {'id': br['id'], 'productId': 'breathing-room', 'kind': 'browser-preview',
                      'sourceManifest': 'docs/content/screenshots.json', 'sourcePath': br['sourcePath'],
                      'originalSha256': br['sha256'], 'publishedPath': None, 'publishedSha256': None,
                      'capturedAtUtc': br['capturedOn'], 'sourcePageUrl': br['sourceUrl'], 'assetUrl': None,
                      'buildOrCommit': br['sourceCommit'], 'widthPx': br['width'], 'heightPx': br['height'],
                      'caption': br['caption'], 'alt': br['alt'], 'dataMode': 'example', 'actualNativeScan': False,
                      'reuse': {'status': 'cleared-first-party-context', 'basis': br['reuseBasis']},
                      'edits': [], 'privacyReview': br['privacyReview'],
                      'review': {'status': 'research-visual-inspected', 'reviewedAtUtc': now,
                                 'notes': 'Opened actual PNG; visible Interactive preview · example data and no-Mac-changes banner. Keep these labels. Tall full image needs responsive/contextual treatment; independent page review pending.'},
                      'limitations': br['limitations']}],
    'briefs': {
        'article': {'track': 'search-reference', 'title': 'Moving from Linux app cleanup to Mac storage review',
                    'slug': 'linux-app-cleanup-to-mac-storage-review',
                    'intent': 'Help a CleanMyLinux user moving to a Mac separate package/app removal, app reset, rebuildable cache and original project data before choosing a workflow.',
                    'outline': ['Start with the target OS, not a list of interchangeable cleaners', 'Separate uninstalling an app from resetting its local state', 'Review project data and cache rebuild costs on the Mac', 'Inspect a Mac inventory before authorizing changes', 'Choose Linux package management or Mac investigation according to the machine'],
                    'openingBoundary': 'CleanMyLinux is for Linux. Breathing Room, which we build, is a Mac preview, not a port of its uninstaller/updater.',
                    'interactionHandoff': 'A non-destructive decision checklist: target OS → package/app removal vs storage investigation → original vs rebuildable data → review permission and rebuild cost. No deletion buttons or invented savings.',
                    'visualOrder': ['Official CleanMyLinux Applications start screen immediately after lead', 'Current-source Breathing Room Space example-data view beside inventory discussion'],
                    'notAllowed': ['Linux command transplantation to macOS', 'Claiming Breathing Room replaces APT/DNF/Flatpak/Snap updating', 'Invented macOS/Windows CleanMyLinux build', 'Untested installation instructions', 'Measured savings from sample figures']},
        'comparison': {'title': 'CleanMyLinux vs Breathing Room: Linux and Mac roles', 'slug': 'cleanmylinux',
                       'intent': 'Short OS-first decision, not a universal winner table.',
                       'rows': list(matrix), 'linkToArticle': '/blog/linux-app-cleanup-to-mac-storage-review/',
                       'links': ['/comparisons/', '/tools/'], 'linkPolicy': 'Verify counterpart/tool routes at drafting; no invented specific tool route.',
                       'conclusion': 'Stay with a Linux-native package workflow on Linux. On a Mac, evaluate a Mac storage/process workflow separately, including preview and hosted-service caveats.'}},
    'advantagesAndTradeoffs': {
        'cleanmylinux': ['Documented Linux package/app management across native formats, Flatpak and Snap; useful when that is the actual job.', 'MIT source and public beta download metadata can be inspected without an account.', 'Not a native Mac choice; unresolved distro minimums, beta naming and source/release feature boundaries must remain visible.'],
        'breathingRoom': ['Documented Mac storage exploration and grouped process/activity investigation; a different job from Linux package updating.', 'Free local core with optional paid hosted AI Care; neither all-local AI nor unlimited AI.', 'Non-notarized preview, Python prerequisite, untested physical Intel execution and incomplete clean-machine/binary parity evidence limit recommendations.']},
    'unknowns': ['CleanMyLinux commercial prices, paid services/support and guarantees', 'CleanMyLinux ARM support and exact tested distro/GLIBC matrix', 'CleanMyLinux full network/telemetry behavior, per-path approval and developer-cache adapters', 'CleanMyLinux screenshot capture date, app build and OS', 'Source roadmap versus beta binary feature parity', 'Native runtime outcomes for either product'],
    'validation': {'handsOnTests': False, 'browserSessionUsed': False, 'siteChanged': False,
                   'independentReview': 'pending separate stage', 'checksLog': 'validation.json'}
}
(ROOT / 'research.json').write_text(json.dumps(packet, indent=2) + '\n')
print(f'Assembled {len(claims)} claims, {len(sources)} sources and 2 visual records.')
