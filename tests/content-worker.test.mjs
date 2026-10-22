import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';

test('content queue validates and a dry-run admits only three independent jobs', () => {
  const source = `
import importlib.util, tempfile
from pathlib import Path
s = importlib.util.spec_from_file_location('worker', 'scripts/content-worker.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
with tempfile.TemporaryDirectory() as directory:
 m.RUNTIME = Path(directory)
 with m.database() as db:
  m.tick(db, m.sync(db), dry_run=True)
`;
  const result = spawnSync('python3', ['-c', source], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout.trim());
  assert.equal(output.dryRun, true);
  assert.ok(output.ready.length <= 3);
  assert.ok(!output.ready.includes('expand-queue'));
});

test('queue rejects duplicate IDs, missing dependencies and cycles', () => {
  const source = `
import importlib.util
s = importlib.util.spec_from_file_location('worker', 'scripts/content-worker.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
cases = [
 {'jobs':[{'id':'a','task':'x'},{'id':'a','task':'y'}]},
 {'jobs':[{'id':'a','task':'x','dependsOn':['missing']}]},
 {'jobs':[{'id':'a','task':'x','dependsOn':['b']},{'id':'b','task':'y','dependsOn':['a']}]},
 {'jobs':[{'id':'../escape','task':'x'}]},
]
for case in cases:
 try:
  m.validate_queue(case)
 except ValueError:
  continue
 raise Exception('invalid queue accepted')
print('ok')
`;
  const result = spawnSync('python3', ['-c', source], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.trim(), 'ok');
});

test('receipts reject false completion and require real scoped artifacts', () => {
  const source = `
import importlib.util, json, tempfile
from pathlib import Path
s = importlib.util.spec_from_file_location('worker', 'scripts/content-worker.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
with tempfile.TemporaryDirectory(dir=m.RUNTIME) as directory:
 p=Path(directory)/'receipt.json'
 bad = [
  {'jobId':'wrong','status':'done','artifacts':['README.md'],'validation':['checked']},
  {'jobId':'test','status':'blocked','diagnostic':'missing evidence'},
  {'jobId':'test','status':'done','artifacts':[],'validation':['checked']},
  {'jobId':'test','status':'done','artifacts':['README.md']},
  {'jobId':'test','status':'done','artifacts':['/etc/hosts'],'validation':['checked']},
  {'jobId':'test','status':'done','artifacts':['docs/content/nonexistent.md'],'validation':['checked']},
 ]
 for value in bad:
  p.write_text(json.dumps(value))
  try:
   m.validate_receipt(p,'test')
  except ValueError:
   continue
  raise Exception('invalid receipt accepted')
 p.write_text(json.dumps({'jobId':'test','status':'done','artifacts':['README.md'],'validation':['read README']}))
 assert m.validate_receipt(p,'test')['status']=='done'
print('ok')
`;
  const result = spawnSync('python3', ['-c', source], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.trim(), 'ok');
});

test('persistent slots claim disjoint jobs, serialize build resources and respect dependencies', () => {
  const source = `
import importlib.util, tempfile
from pathlib import Path
s=importlib.util.spec_from_file_location('worker','scripts/content-worker.py')
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
with tempfile.TemporaryDirectory() as directory:
 m.RUNTIME=Path(directory)
 jobs=[{'id':'a','task':'a','resources':['site-build']},{'id':'b','task':'b','resources':['site-build']},{'id':'c','task':'c'},{'id':'d','task':'d','dependsOn':['a']}]
 with m.database() as db:
  for j in jobs: db.execute("INSERT INTO jobs(id,state) VALUES(?,'pending')",(j['id'],))
  db.commit()
  assert m.claim_job(db,jobs,1)['id']=='a'
  assert m.claim_job(db,jobs,2)['id']=='c'
  assert m.claim_job(db,jobs,3) is None
  db.execute("UPDATE jobs SET state='done',slot=NULL WHERE id='a'"); db.commit()
  assert m.claim_job(db,jobs,1)['id']=='b'
  assert m.claim_job(db,jobs,3)['id']=='d'
  (m.RUNTIME/'PAUSED').touch()
  assert m.claim_job(db,jobs,1) is None
print('ok')
`;
  const result=spawnSync('python3',['-c',source],{encoding:'utf8'});
  assert.equal(result.status,0,result.stderr);
  assert.equal(result.stdout.trim(),'ok');
});

test('watchdog replenishes only missing slots and dry-run never starts workers', () => {
  const source = `
import importlib.util, tempfile
from pathlib import Path
from unittest.mock import patch
s=importlib.util.spec_from_file_location('worker','scripts/content-worker.py')
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
with tempfile.TemporaryDirectory() as directory:
 m.RUNTIME=Path(directory)
 with m.database() as db:
  with patch.object(m,'slot_active',side_effect=lambda slot:slot in (1,3)),patch.object(m,'coordinate',return_value={}),patch.object(m.subprocess,'Popen') as start:
   m.tick(db,[],dry_run=True)
   assert start.call_count==0
   m.tick(db,[])
   assert start.call_count==1
   assert start.call_args.args[0][-1]=='2'
print('ok')
`;
  const result=spawnSync('python3',['-c',source],{encoding:'utf8'});
  assert.equal(result.status,0,result.stderr);
  assert.ok(result.stdout.trim().endsWith('ok'));
});

test('disconnected jobs hold their slot until a validated terminal receipt arrives', () => {
  const source = `
import importlib.util, tempfile, json
from pathlib import Path
s=importlib.util.spec_from_file_location('worker','scripts/content-worker.py')
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
with tempfile.TemporaryDirectory() as directory:
 m.RUNTIME=Path(directory)
 receipt=m.RUNTIME/'attempt.receipt.json'
 (m.RUNTIME/'slot-1-attempt.json').write_text(json.dumps({'jobId':'a','receipt':str(receipt)}))
 with m.database() as db:
  db.execute("INSERT INTO jobs(id,state,slot) VALUES('a','uncertain',1)"); db.commit()
  assert m.recover_slot(db,1) is False
  assert db.execute("SELECT state FROM jobs WHERE id='a'").fetchone()[0]=='uncertain'
  receipt.write_text(json.dumps({'jobId':'a','status':'done','artifacts':['README.md'],'validation':['read actual artifact']}))
  assert m.recover_slot(db,1) is True
  assert db.execute("SELECT state,slot FROM jobs WHERE id='a'").fetchone()[0]=='done'
  assert db.execute("SELECT slot FROM jobs WHERE id='a'").fetchone()[0] is None
print('ok')
`;
  const result=spawnSync('python3',['-c',source],{encoding:'utf8'});
  assert.equal(result.status,0,result.stderr);
  assert.equal(result.stdout.trim(),'ok');
});

test('real slot locks identify live ownership and concurrent SQLite claims never duplicate jobs', () => {
  const source = `
import importlib.util, tempfile, fcntl
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
s=importlib.util.spec_from_file_location('worker','scripts/content-worker.py')
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
with tempfile.TemporaryDirectory() as directory:
 m.RUNTIME=Path(directory)
 with (m.RUNTIME/'slot-1.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  assert m.slot_active(1) is True
 assert m.slot_active(1) is False
 jobs=[{'id':str(n),'task':'isolated fixture'} for n in range(1,7)]
 with m.database() as db:
  for job in jobs: db.execute("INSERT INTO jobs(id,state) VALUES(?,'pending')",(job['id'],))
  db.commit()
 def claim(slot):
  with m.database() as db: return m.claim_job(db,jobs,slot)['id']
 with ThreadPoolExecutor(max_workers=3) as pool: claimed=list(pool.map(claim,[1,2,3]))
 assert len(set(claimed))==3
 with m.database() as db:
  assert db.execute("SELECT count(*) FROM jobs WHERE state='running'").fetchone()[0]==3
print('ok')
`;
  const result=spawnSync('python3',['-c',source],{encoding:'utf8'});
  assert.equal(result.status,0,result.stderr);
  assert.equal(result.stdout.trim(),'ok');
});

test('coordinator advances evidenced research handoffs but never unknown identity or publication', () => {
  const source = `
import importlib.util, tempfile, json
from pathlib import Path
s=importlib.util.spec_from_file_location('worker','scripts/content-worker.py')
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
with tempfile.TemporaryDirectory() as directory:
 root=Path(directory); m.RUNTIME=root/'runtime'; m.CONTENT=root/'content'; m.SITE=root/'site'
 m.CONTENT.mkdir(); m.RUNTIME.mkdir()
 facts=[{'field':field,'value':'documented','sourceUrl':'https://vendor.example/docs','excerpt':'retained evidence'} for field in ('officialName','coreFunction','platforms')]
 product={'id':'known','baselineVerification':{'officialUrl':'https://vendor.example','facts':facts}}
 unknown={'id':'unknown','baselineVerification':{'officialUrl':None,'facts':[]}}
 (m.CONTENT/'competitors.json').write_text(json.dumps({'competitors':[product,unknown]}))
 for slug in ('known','unknown'):
  folder=m.CONTENT/'competitors'/slug; folder.mkdir(parents=True)
  (folder/'research.json').write_text(json.dumps({'status':'blocked','draftingAllowed':False}))
  (folder/'research.md').write_text('Retained evidence and unresolved image rights.')
 with m.database() as db:
  for slug in ('known','unknown'): db.execute("INSERT INTO jobs(id,state,diagnostic) VALUES(?,'blocked','Image or identity unresolved')",('research-'+slug,))
  db.commit(); result=m.coordinate(db,[])
  assert result['admittedResearchHandoffs']==['research-known']
  assert db.execute("SELECT state FROM jobs WHERE id='research-known'").fetchone()[0]=='done'
  assert db.execute("SELECT state FROM jobs WHERE id='research-unknown'").fetchone()[0]=='blocked'
  assert db.execute("SELECT count(*) FROM transitions").fetchone()[0]==1
  assert json.loads((m.CONTENT/'competitors/known/research.json').read_text())['draftingAllowed'] is False
  assert all(family['publicationFlagApproved']==0 for family in result['pages'].values())
print('ok')
`;
  const result=spawnSync('python3',['-c',source],{encoding:'utf8'});
  assert.equal(result.status,0,result.stderr);
  assert.equal(result.stdout.trim(),'ok');
});

test('queue expansion assigns four distinct page families, five roundups and independent reviews idempotently', () => {
  const source = `
import importlib.util, tempfile, json
from pathlib import Path
s=importlib.util.spec_from_file_location('expand','scripts/expand-content-queue.py')
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
with tempfile.TemporaryDirectory() as directory:
 m.CONTENT=Path(directory)
 base=[{'id':name,'task':'fixture','dependsOn':[]} for name in ('sources','editorial','capabilities','expand-queue','foundation-review','screenshot-library')]
 (m.CONTENT/'queue.json').write_text(json.dumps({'version':1,'jobs':base}))
 products=[{'id':slug,'name':slug.title(),'listingUrl':'https://alternativeto.net/software/'+slug+'/about/'} for slug in ('alpha','beta')]
 (m.CONTENT/'competitors.json').write_text(json.dumps({'competitors':products}))
 m.expand(); first=(m.CONTENT/'queue.json').read_text(); m.expand(); assert (m.CONTENT/'queue.json').read_text()==first
 jobs=json.loads(first)['jobs']; by_id={j['id']:j for j in jobs}; assert len(by_id)==len(jobs)
 assert len([j for j in jobs if j['id'].startswith('draft-roundup-')])==5
 assert len([j for j in jobs if j['id'].startswith('review-roundup-')])==5
 for product in products:
  for kind,(collection,intent) in m.KINDS.items():
   draft,review=m.page_ids(product['id'],kind)
   assert by_id[draft]['pageKind']==kind
   assert 'src/content/'+collection+'/' in by_id[draft]['task']
   assert by_id[review]['dependsOn']==[draft]
   assert by_id[review]['resources']==['site-build']
 assert len(by_id['content-final-audit']['dependsOn'])==13
 assert not (m.CONTENT/'queue.pending.json').exists()
print('ok')
`;
  const result=spawnSync('python3',['-c',source],{encoding:'utf8'});
  assert.equal(result.status,0,result.stderr);
  assert.ok(result.stdout.trim().endsWith('ok'));
});
