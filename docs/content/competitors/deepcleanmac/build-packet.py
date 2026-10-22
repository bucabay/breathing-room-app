"""Build a research-only packet from retained public evidence; no network or app execution."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()


def load(path):
    return json.loads((ROOT / path).read_text())


def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def relative(path):
    return str(path.relative_to(ROOT))


baseline = next(p for p in load('docs/content/verification/batch-1.json')['records']
                if p['id'] == 'deepcleanmac')
sources = []
texts = {}


def source(id, path, publisher, reused=False, updated=None):
    d = load(path)
    texts[id] = d['text']
    sources.append(dict(id=id, publisher=publisher, title=d.get('title', id),
                        url=d.get('url', d.get('officialUrl')),
                        finalUrl=d.get('url', d.get('finalUrl')),
                        retrievedAtUtc=d.get('retrievedAtUtc', d.get('retrievedAt')),
                        sourceUpdated=updated, snapshotPath=path,
                        sha256=digest(path), reused=reused,
                        evidenceClass='publisher-documentation-not-runtime-test'))


source('S1', baseline['discovery']['snapshotPath'], 'AlternativeTo', True)
source('S2', baseline['sources'][0]['snapshotPath'], 'DeepCleanMac', True)
for id, name, updated in [('S3', 'terms', '2026-04-13'),
                          ('S4', 'privacy', '2026-04-13'),
                          ('S5', 'changelog', '2026-10-19'),
                          ('S6', 'homepage', None),
                          ('S7', 'directory-visual', None)]:
    source(id, relative(OUT / 'sources' / (name + '-browser.json')),
           'AlternativeTo' if id == 'S7' else 'DeepCleanMac', updated=updated)

claims = []


def claim(id, wording, sid, excerpt, scope, state='verified', location='comparison matrix'):
    assert excerpt in texts[sid], (id, 'excerpt not found')
    s = next(s for s in sources if s['id'] == sid)
    claims.append(dict(id=id, wording=wording, intendedLocation=location,
                       sourceIds=[sid], sourceUrl=s['url'], excerpt=excerpt,
                       checkedAtUtc=s['retrievedAtUtc'], scope=scope, state=state,
                       evidenceClass='documented-vendor-claim' if sid != 'S1' else 'directory-discovery',
                       reviewer='research-deepcleanmac worker; not independent review'))


claim('C01', 'The listing identifies DeepCleanMac and links deepcleanmac.com as its official site.',
      'S1', 'Official Website\ndeepcleanmac.com', 'Identity/discovery only', location='identity')
claim('C02', 'DeepCleanMac advertises macOS Sonoma 14.0 or later on Apple Silicon and Intel.',
      'S2', 'DeepCleanMac supports macOS Sonoma (14.0) and later, on both Apple Silicon and Intel Macs.',
      'Advertised requirements; neither architecture installed/tested')
claim('C03', 'The documented cleanup workflow is scan, review file sizes/locations/types, then clean.',
      'S2', "See exactly what will be cleaned from your Mac - file sizes, locations, and types. You're always in control.",
      'Homepage describes user review; not evidence of every deletion guard or reversibility')
claim('C04', 'The homepage advertises an updater for App Store, Homebrew and Sparkle apps.',
      'S2', 'Detects updates from the App Store, Homebrew, and Sparkle automatically.',
      'Vendor description; update execution not tested')
claim('C05', 'The homepage advertises an app uninstaller, duplicate finder, resetter and disk treemap.',
      'S2', 'Eight powerful tools in one app - clean, update, uninstall, deduplicate, reset, shred, analyze, and monitor.',
      'Documented suite breadth; no guarantee of complete uninstall or irreversible shredding')
claim('C06', 'The advertised health dashboard monitors CPU, memory and disk usage.',
      'S2', 'Monitor CPU, memory, and disk usage in real-time with a clear health score.',
      'Vendor description; no inference of complete process attribution or historical monitoring')
claim('C07', 'The homepage advertises $5/year with automatic renewal and $9 one-time lifetime.',
      'S2', '1-Year License\nFull access for one year with automatic renewal.\n$5\n/year',
      'Homepage offer, not confirmed transaction price; conflicts with historical changelog')
claim('C08', 'The homepage lifetime offer is $9 one-time with lifetime updates.',
      'S2', 'Lifetime License\nPay once, use forever. Best value for long-term users.\n$9\none-time',
      'Advertised offer only; historical price conflict retained')
claim('C09', 'The terms grant a paid non-exclusive, non-transferable licence for one Mac.',
      'S3', 'non-exclusive, non-transferable license to use the Software on one (1) Mac computer',
      'Terms dated April 13, 2026; commercial proprietary-use conditions, not an open-source licence')
claim('C10', 'The annual licence renews unless cancelled; lifetime includes future updates for one Mac.',
      'S3', 'The license renews automatically unless cancelled.',
      'Annual renewal term; lifetime separately stated in same terms section')
claim('C11', 'Prices are stated in USD and may incur tax; the terms offer a 14-day refund window.',
      'S3', 'Prices are listed in USD and may be subject to applicable taxes.',
      'Published terms; checkout, refund and cancellation not exercised')
claim('C12', 'The terms offer a full refund when contacted within 14 days of purchase.',
      'S3', 'contact us within 14 days of purchase',
      'Published policy only; no support contact or refund test')
claim('C13', 'The privacy policy discloses cleanup statistics tied to a licence key.',
      'S4', 'Anonymous cleanup statistics (files cleaned count, space freed) tied to your license key.',
      'Policy assertion, not network audit; do not repeat directory No Tracking as fact')
claim('C14', 'The policy also discloses machine identifier/app version and approximate country/city analytics.',
      'S4', 'Machine identifier and app version, used for license activation and update checks.',
      'Policy assertion; approximate-location wording recorded in C15')
claim('C15', 'The policy says country and city are derived from IP for analytics and IP is not stored.',
      'S4', 'Country and city derived from your IP address for analytics purposes. We do not store your IP address.',
      'Vendor policy statement; no independent retention verification')
claim('C16', 'The policy says cleaned filenames and paths are not collected.',
      'S4', 'We do not collect filenames or paths of files that are cleaned.',
      'Vendor policy statement; does not establish all-offline operation')
claim('C17', 'The newest entry shown in the inspected changelog is version 1.7.3, October 19, 2026.',
      'S5', 'October 19, 2026\n\nVersion 1.7.3',
      'Latest listed changelog entry, not binary version verification')
claim('C18', 'Version 1.7.1 documents keeping Git-committed build folders and skipping cloud-only project folders.',
      'S5', 'Those folders are now kept like any other folder with committed files.',
      'October 13 release note; source/binary protection behavior not tested', location='workflow brief')
claim('C19', 'Version 1.7.0 describes keeping build folders when a Git/deploy-key check cannot finish.',
      'S5', "It's also kept whenever DeepCleanMac can't finish checking it.",
      'October 7 release note; vendor assertion, not a safety certification', location='workflow brief')
claim('C20', 'Version 1.6.7 records a fix for double-counted cache sizes and leaves Poetry virtual environments alone.',
      'S5', 'some cache folders were counted twice, so a scan could report far more space than it would actually free.',
      'September 28 historical fix; do not imply present versions retain that defect', location='workflow brief')
claim('C21', 'The July 22 version 1.5.2 note announces $9/year and $19 lifetime, unlike the current homepage offer.',
      'S5', '1-Year License now $9/year, Lifetime License now $19 one-time',
      'Historical changelog vs current homepage; reduction/promotion/transaction amount unresolved')
claim('C22', 'The homepage offers a public DMG link, but free-download wording does not establish a free full licence.',
      'S2', 'Download Free', 'Link https://deepcleanmac.com/DeepCleanMac.dmg; no binary retrieval/installation')
claim('C23', 'The changelog documents Full Disk Access detection and skipped protected paths when not granted.',
      'S5', 'Protected paths are automatically skipped when not granted',
      'Version 1.3.0, April 23; not proof of sandbox/signing/notarization state')

# Current same-day first-party evidence is reused, not re-fetched or promoted to native QA.
cap_path = 'docs/content/capabilities.md'
cap_text = (ROOT / cap_path).read_text()
sources.append(dict(id='BR1', publisher='Breathing Room evidence register',
                    url='https://breathing-room.chatic.ai/', finalUrl=None,
                    retrievedAtUtc=None, reviewedOn='2026-10-21', snapshotPath=cap_path,
                    sha256=digest(cap_path), reused=True,
                    evidenceClass='same-day-first-party-register-with-source-and-public-URL-references'))
for id, wording, excerpt, locator, urls in [
    ('B01', 'Breathing Room is a free Apache-2.0 macOS maintenance preview; optional hosted AI is not all-offline.',
     'Hosted AI assistance requires internet access and authentication; this is not an entirely offline AI product.',
     'Conclusion; Local versus hosted boundary', ['https://breathing-room.chatic.ai/privacy/']),
    ('B02', 'AI Care is advertised at $5 USD/month or $50 USD/year; local core tools require no app purchase.',
     '**$5 USD/month**, **$50 USD/year**', 'Pricing rows 74–79', ['https://breathing-room.chatic.ai/#pricing']),
    ('B03', 'Identified preview is 0.1.0-preview.1, macOS 13+, with a universal installer advertised; physical Intel untested.',
     'Physical Intel behavior remains explicitly untested.', 'Preview table rows 48–49',
     ['https://github.com/bucabay/breathing-room-app/releases/tag/v0.1.0-preview.1']),
    ('B04', 'Preview disclosures say Apple Development signed, not Developer ID signed/notarized, and Python 3.10+ required.',
     'Python **3.10+** is a disclosed prerequisite', 'Preview table rows 50–51',
     ['https://breathing-room.chatic.ai/download/', 'https://github.com/bucabay/breathing-room-app/releases/tag/v0.1.0-preview.1']),
    ('B05', 'Source includes grouped helpers, activity observations, developer-cache discovery and constrained cleanup approvals.',
     'Native sampling groups helpers through parent/app relationships', 'Capability matrix rows 24–32; approval exception 36–42',
     ['https://github.com/bucabay/breathing-room-app']),
    ('B06', 'Daily care requires the app to remain running and saved exact approvals; optional automatic Ruff-cache mode is separate.',
     'only remembered exact approvals are eligible.', 'Daily care and approval exception sections',
     ['https://github.com/bucabay/breathing-room-app']),
]:
    assert excerpt in cap_text, id
    claims.append(dict(id=id, wording=wording, intendedLocation='comparison / bounded recommendation',
                       sourceIds=['BR1'], sourceUrl=urls[0], supportingUrls=urls,
                       excerpt=excerpt, locator=locator, checkedOn='2026-10-21',
                       evidenceClass='reused-current-register; source/publication-not-binary-QA',
                       state='verified', scope='Register limitations apply; not newly tested in this job',
                       reviewer='research-deepcleanmac worker; inherited capabilities verification'))

screens = load('docs/content/screenshots.json')
br = next(a for a in screens['assets'] if a['id'] == 'current-space-browser-preview')
assert digest(br['sourcePath']) == br['sha256']
visual_meta = load(relative(OUT / 'sources/competitor-visual-inspection.json'))
asset = visual_meta['images'][0]
visuals = [dict(id='deepcleanmac-dashboard-listing', productId='deepcleanmac',
                view='Dashboard — System health overview', kind='listing-asset',
                sourcePageUrl=baseline['discovery']['sourceUrl'], assetUrl=asset['src'],
                capturedAtUtc=None, retrievedAtUtc=visual_meta['retrievedAtUtc'], capturedBy=None,
                productVersion=None, buildOrCommit=None, osVersion=None,
                dataMode='unknown', originalPath=None, originalSha256=None,
                publishedPath=None, publishedSha256=None, widthPx=asset['width'], heightPx=asset['height'],
                edits=[], privacyReview={'status':'pending','redactions':[]},
                reuse={'status':'link-only','basis':'No explicit image redistribution licence or permission verified. Public visibility is not permission.',
                       'evidenceUrlOrPath':baseline['discovery']['sourceUrl'],
                       'credit':'DeepCleanMac app image via AlternativeTo; rights remain with respective owners.'},
                caption='DeepCleanMac Dashboard app image published on AlternativeTo. Version, capture date and underlying measurement conditions are unknown; not our test results.',
                alt='DeepCleanMac Dashboard showing health, available disk space, CPU and memory cards, with cleanup tools in a sidebar.',
                supportedClaimIds=['C06'], limitations=[
                    'Visually inspected in owned browser tab; real app UI, not just logo/landing page.',
                    '618 × 394 rendition has soft small text; publication needs a cleared legible source.',
                    'Viewed read-only; no third-party original copied to repository, so original hash is inapplicable, not invented.',
                    'Screenshot has lifetime cleanup figures; they are unknown-source image data, never verified savings.',
                    'Link-only fallback does not satisfy required on-page competitor-image gate.'],
                review={'status':'research-visual-inspection-only','reviewer':'research-deepcleanmac worker','reviewedAtUtc':NOW}),
           dict(id=br['id'], productId='breathing-room', view=br['view'], kind=br['kind'],
                sourcePageUrl=br['sourceUrl'], assetUrl=None, capturedAtUtc=br['capturedOn'],
                retrievedAtUtc=None, capturedBy='screenshot-library worker (inherited manifest)',
                productVersion=None, buildOrCommit=br['sourceCommit'], osVersion=None,
                dataMode='example', originalPath=br['sourcePath'], originalSha256=br['sha256'],
                publishedPath=None, publishedSha256=None, widthPx=br['width'],heightPx=br['height'],
                edits=[], privacyReview=br['privacyReview'], reuse={'status':'cleared',
                    'basis':br['reuseBasis'],'evidenceUrlOrPath':'docs/content/screenshots.json',
                    'credit':'Breathing Room current-source browser preview; example data.'},
                caption=br['caption'],alt=br['alt'],supportedClaimIds=['B05'],
                limitations=br['limitations']+['No current native claim; independent page-context review still pending. Keep example-data banners visible.'],
                review={'status':'research-inspected','reviewer':'research-deepcleanmac worker','reviewedAtUtc':NOW})]

unknowns = [
    {'field':'repository','value':None,'state':'not-verified','diagnostic':'No official source-repository link in retained homepage/terms/changelog. Do not invent a GitHub project or infer no repository exists.'},
    {'field':'publisherLegalIdentity','value':None,'state':'not-verified','diagnostic':'Public sources identify DeepCleanMac, but no incorporated entity/person independently established.'},
    {'field':'trialLimits','value':None,'state':'not-verified','diagnostic':'Download Free / Start for Free does not state free scan/cleanup quota, trial duration or activation rules.'},
    {'field':'exactTransactionPrice','value':None,'state':'not-verified','diagnostic':'Homepage $5/$9 vs dated changelog $9/$19; no checkout opened and no promotion duration established.'},
    {'field':'signingNotarizationRuntime','value':None,'state':'not-verified','diagnostic':'No binary fetched; signing, notarization, runtime dependencies and actual DMG build unknown.'},
    {'field':'helperGroupingRecurringGrowth','value':None,'state':'not-verified','diagnostic':'Dashboard documented, but ownership-grouping and persistent growth history equivalence to Breathing Room not verified.'},
    {'field':'cleanupMechanism','value':None,'state':'not-verified','diagnostic':'Review workflow documented; Trash vs permanent deletion, complete guard rules and undo scope not verified.'},
    {'field':'offlineAndHosted','value':None,'state':'not-verified','diagnostic':'Privacy policy documents network-related licence/update/analytics data; no code or traffic audit, all-offline unsupported.'},
]
matrix = [
    ('platform','macOS 14+; Apple Silicon/Intel advertised',['C02'],'macOS 13+ universal preview; Intel untested',['B03']),
    ('version','Latest listed 1.7.3, Oct 19, not inspected binary',['C17'],'0.1.0-preview.1 identified, not all-channel latest certified',['B03']),
    ('licence','Commercial, single-Mac, non-transferable use licence',['C09','C10'],'Apache-2.0 source; hosted service separate',['B01']),
    ('price','Homepage $5 USD/year auto-renew or $9 lifetime; historical discrepancy unresolved',['C07','C08','C11','C21'],'Free core; AI Care $5 USD/month or $50 USD/year advertised',['B02']),
    ('operation','Native Mac utility marketed; network-related analytics/licensing documented',['C02','C13','C14','C15','C16'],'Local inspection and constrained execution; authenticated hosted AI',['B01','B05']),
    ('scanCleanup','Review sizes, locations, types before cleaning; deletion/undo details not verified',['C03'],'Source-backed discovery and approval architecture, not runtime-certified',['B05','B06']),
    ('suiteBreadth','Updater/uninstaller/duplicates/resetter/treemap advertised',['C04','C05'],'Do not position as equivalent full suite; corresponding full modules not established',['B05']),
    ('monitoring','CPU/memory/disk dashboard documented; grouping/history unknown',['C06'],'Grouped helpers/activity source implementation; attribution limitations',['B05']),
    ('developerFiles','Git-aware build-folder exclusions and Xcode changes documented',['C18','C19','C20'],'Developer cache adapters source-backed, not every version certified',['B05']),
    ('installation','FDA detection documented; signing/notarization/runtime unknown',['C23'],'Non-notarized preview; Python 3.10+ prerequisite',['B04']),
]

packet = dict(schemaVersion=1,jobId='research-deepcleanmac',productId='deepcleanmac',
    stage='research',status='blocked',checkedAtUtc=NOW,canonicalOwnerId='deepcleanmac',
    identity={'officialName':'DeepCleanMac','homepage':'https://deepcleanmac.com/',
              'repository':None,'aliases':[], 'aliasDecision':{
                  'status':'no-verified-alias','skipSeparateDraft':False,
                  'rationale':'Directory and official pages consistently identify DeepCleanMac. No alias evidence in retained official sources. PowerMyMac ambiguity is a separate group in alias-decisions.json; no relation to this product established. Do not merge by shared cleaner category or similar DeepClean spelling.'},
              'classification':'direct-with-scope-differences',
              'fitRationale':'Native Mac cleanup/storage and CPU/memory dashboard overlap; broader documented updater/uninstaller/duplicates suite is not a one-to-one replacement for activity/approval investigation.',
              'platformIntent':'Mac-to-Mac comparison only; no invented Windows/Linux support.',
              'deadOrIrrelevant':False,'skipDecision':'Do not skip a live relevant identity; block drafting for visual rights and price reconciliation instead.'},
    ownership={'ownedFolder':relative(OUT),'websiteEdits':False,'queueMutation':False},
    reuse={'baseline':'docs/content/verification/batch-1.json#deepcleanmac',
           'reasonForHomepageRevisit':'Baseline lacked image URLs. Browser visit was for public image/repository-link discovery after direct HTTP 403, not a needless fact refresh.',
           'otherReusedEvidence':['docs/content/capabilities.md','docs/content/screenshots.json','docs/content/verification/alias-decisions.json']},
    discovery={**baseline['discovery'],'sha256':digest(baseline['discovery']['snapshotPath']),
               'seedEdges':[
                   {'seedId':'cleanmymac','url':'https://alternativeto.net/software/cleanmymac/?p=6','retrievedAtUtc':'2026-10-21T18:36:42.517Z'},
                   {'seedId':'mole','url':'https://alternativeto.net/software/mole/?p=6','retrievedAtUtc':'2026-10-21T18:37:21.311Z'}],
               'edgeEvidencePath':'docs/content/competitors.json#deepcleanmac',
               'method':'Inherited browser-rendered discovery; raw retained directory JSON hashed. Listing tags/prices not primary capability evidence.'},
    sources=sources, claims=claims,
    productMatrix=[{'dimension':r[0],'competitor':r[1],'competitorClaimIds':r[2],
                    'breathingRoom':r[3],'breathingRoomClaimIds':r[4]} for r in matrix],
    unknowns=unknowns, visuals=visuals,
    conflicts=[
        {'id':'price-conflict','claimIds':['C07','C08','C21'],
         'diagnostic':'Current homepage advertises $5/year and $9 lifetime; July changelog says $9/year and $19 lifetime; directory says $19–$39. Official terms settle USD/tax/one-Mac conditions, not amounts. No transaction amount or sale duration established.',
         'resolution':'Publish only as dated attributed homepage offer if independently approved; do not assert current final price or cheapest comparison. Exact-price drafting remains blocked pending reconciliation.'},
        {'id':'privacy-tag-conflict','claimIds':['C13','C14','C15','C16'],
         'diagnostic':'Directory No Tracking/Works Offline labels are not proof; official policy discloses licence-linked analytics/device/location information.',
         'resolution':'Use attributed official policy, never a blanket no-tracking/offline claim.'},
        {'id':'safety-marketing','claimIds':['C18','C19','C20'],
         'diagnostic':'Homepage absolute safety/recovery/speed language is not independent evidence. Dated changelog records protection and counting fixes.',
         'resolution':'Describe fixes by exact version/date without implying present defects, risk-free deletion, guaranteed SSD shredding or reproduced failures.'}],
    briefs={
        'workflow':{'state':'planning-only-blocked-not-a-draft','track':'search/reference',
                    'title':'Review developer build folders before cleaning a Mac',
                    'slug':'review-developer-build-folders-before-cleaning-mac',
                    'primaryIntent':'Distinguish disposable generated output from committed project data, environments and cloud-only files before approving cleanup.',
                    'angle':'Use DeepCleanMac 1.7.0/1.7.1 Git-aware exclusions and 1.6.7 counting fix as concrete documented reasons not to treat a scan total as permission to delete.',
                    'claimIds':['C18','C19','C20','B05','B06'],
                    'sections':['Start with a keep/rebuild/unknown decision, not a cleanup target.',
                                'Separate committed project content, regenerable output and environment state.',
                                'Explain the dated vendor protection changes without pretending to test them.',
                                'Review exact location, permissions, rebuild cost and backup before approval.',
                                'Show Breathing Room, which we build, as an optional review/investigation preview, not a replacement for every suite tool.'],
                    'visualPlan':['Cleared DeepCleanMac app UI required; current link-only dashboard is not enough.',
                                  'Selected current-source Space preview, example data banners and caption intact.'],
                    'interactionHandoff':'A non-destructive decision checklist: committed/unknown → keep; generated → confirm reproducible rebuild, owner and exact location before review. No shell deletion demo, scan, upload or invented saved-byte calculator.',
                    'internalLinks':['/comparisons/deepcleanmac/','/comparisons/','/tools/'],
                    'limitations':'No SERP-volume evidence collected; title uniqueness across future drafts needs independent review; no hands-on claims.'},
        'comparison':{'state':'planning-only-blocked-not-a-draft',
                      'title':'Breathing Room vs DeepCleanMac: review workflow or utility suite?',
                      'slug':'deepcleanmac','primaryIntent':'Choose between a documented Mac utility suite and an open-source maintenance/investigation preview.',
                      'structure':['Conclusion with audience and affiliation disclosure.',
                                   'Compact cited matrix: platform, scope, review controls, monitoring, network/privacy, pricing and install caveats.',
                                   'When each product fits, what remains unverified, link to workflow and comparison hub.'],
                      'boundedConclusion':'DeepCleanMac may fit someone needing the documented updater/uninstaller/duplicate tools. Breathing Room, which we build, may fit someone willing to use a non-notarized Python-dependent preview for source-backed investigation and exact approval workflows. Neither was benchmarked here.',
                      'noClaims':['No measured speed/savings/safety winner','No blanket no-tracking or offline AI claim','No unknown-as-No checkmarks','No full-feature parity','No final transaction price until resolved']}},
    advantagesAndTradeoffs={
        'deepcleanmac':['Documented updater/uninstaller/duplicates/resetter/treemap breadth may serve suite buyers (C04–C05).',
                        'Published annual and lifetime single-Mac licensing options; amounts require reconciliation (C07–C12,C21).',
                        'Versioned release notes disclose concrete protection changes; this is documentation, not our certification (C17–C20).',
                        'Licence-linked analytics/device/location policy and unknown deletion/undo details need explicit qualification (C13–C16).'],
        'breathingRoom':['Source-backed grouped activity and exact-approval investigation can suit developers (B05–B06).',
                         'Free local core and inspectable Apache-2.0 desktop source (B01–B02); hosted AI separate.',
                         'Non-notarized preview, Python dependency, untested physical Intel and hosted-auth boundary are material trade-offs (B01–B04).',
                         'Do not claim full uninstaller/updater/duplicate-suite equivalence or guaranteed cleanup outcomes.']},
    blockers=[
        {'id':'competitor-image-rights','severity':'critical','diagnostic':'Real Dashboard listing asset found and visually inspected, but reuse permission/licence unknown. Link-only fallback does not satisfy EDITORIAL visual gate. No asset downloaded for publication.',
         'unblock':'Obtain verifiable image reuse permission/licence and a legible app screenshot, or explicit authorized editorial policy decision; retain original bytes/hash/provenance when permitted.'},
        {'id':'exact-price-discrepancy','severity':'critical-for-price-comparison','diagnostic':'Official current homepage and historical changelog amounts differ without verified explanation; actual payable amount unknown.',
         'unblock':'Read-only official price reconciliation or independent approval of explicit dated homepage-offer-only wording; no purchase/signup/contact permitted.'}],
    draftingGate={'ready':False,'publicationReady':False,'independentReview':'pending','score':None,
                  'diagnostic':'Research evidence retained; missing critical visual reuse basis and unresolved exact-price evidence block drafting. Noncritical unknowns are explicit, not fabricated.'},
    safety={'installedOrExecutedCompetitor':False,'cleanup':False,'accountsOrPurchasesOrMessages':False,
            'credentialsOrCookiesRead':False,'thirdPartyImageDownloadedForPublication':False,
            'browser':'Only task-created tab 89 used and closed; no existing tabs inspected/navigated. No browser recovery needed.',
            'fetchFailures':[{'url':'https://deepcleanmac.com/'+p,'method':'Python urllib public GET','result':'HTTP 403 Forbidden'} for p in ['terms','privacy','changelog','']],
            'recovery':'WebFetch read source text; normal owned browser navigation retained public DOM snapshots. No challenge bypass, hidden extraction or alternate profile.'})
(OUT / 'research.json').write_text(json.dumps(packet, indent=2, ensure_ascii=False) + '\n')
print('Wrote', relative(OUT / 'research.json'), 'with',len(claims),'claims and',len(sources),'sources')
