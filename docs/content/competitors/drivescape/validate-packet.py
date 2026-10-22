"""Structural/provenance checks only; not editorial or publication approval."""
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
class Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'): self.skip+=1
    def handle_endtag(self,tag):
        if tag in ('script','style'): self.skip=max(0,self.skip-1)
    def handle_data(self,data):
        if not self.skip: self.parts.append(data)
def norm(s): return re.sub(r'[^a-z0-9]+','',s.lower())
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((ROOT/'research.json').read_text()); checks=[]; failures=[]
def check(name,ok,detail):
    checks.append({'check':name,'outcome':'pass' if ok else 'fail','detail':detail})
    if not ok: failures.append(name)
sources={s['id']:s for s in d['sources']}
for s in sources.values():
    if 'snapshotPath' not in s: continue
    p=APP/s['snapshotPath']
    check('source-hash:'+s['id'],p.exists() and digest(p)==s['sha256'],str(p.relative_to(APP)))
for c in d['claims']:
    s=sources[c['sourceIds'][0]]; p=APP/s['snapshotPath']
    if p.suffix=='.json':
        text=json.loads(p.read_text()).get('text','')
    elif p.suffix=='.html':
        parser=Text(); parser.feed(p.read_text()); text=' '.join(parser.parts)
    else: text=p.read_text()
    check('supporting-excerpt:'+c['id'],norm(c['excerpt']) in norm(text),c['sourceUrl'] or s['snapshotPath'])
check('unique-claim-ids',len({c['id'] for c in d['claims']})==len(d['claims']),str(len(d['claims']))+' claim IDs')
check('canonical-and-fit',d['identity']['canonicalOwnerId']=='drivescape' and not d['identity']['skipDecision']['skipProduct'],'Distinct Mac storage competitor; no verified duplicate')
v=d['visuals'][0]
check('link-only-not-downloaded',v['reuse']['status']=='link-only' and v['originalSha256'] is None and v['originalPath'] is None,'Rights unresolved; no image bytes downloaded or hashes invented')
visuals=json.loads((ROOT/'sources/listing-visuals-browser.json').read_text())
check('screenshot-url-in-public-dom',any(i['src']==v['assetUrl'] and 'screenshot' in i['alt'].lower() for i in visuals['images']),'Source DOM identifies selected screenshot URL')
b=d['visuals'][1]
check('breathing-room-original-hash',digest(Path(b['originalPath']))==b['originalSha256'],'Selected existing Space PNG unchanged; example-data caption retained')
check('required-block',d['status']=='blocked' and not d['draftingAllowed'] and bool(d['blockers']),'Missing competitor image rights blocks drafting')
check('briefs-present',all(d['briefs'][x]['status']=='blocked-not-a-draft' for x in ('workflowArticle','comparison')),'Workflow and comparison are briefs, not published drafts')
check('markdown-present',(ROOT/'research.md').exists() and 'drafting BLOCKED' in (ROOT/'research.md').read_text(),'Human-readable packet explicitly blocked')
result={'status':'pass' if not failures else 'fail','scope':'Research structure, source excerpts and retained-byte integrity, not runtime QA or reuse clearance','checks':checks,'failures':failures,'notRun':['Site builds/tests (no site edits)','Native app/binary tests','Independent publication/visual review']}
(ROOT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(bool(failures))
