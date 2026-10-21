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
