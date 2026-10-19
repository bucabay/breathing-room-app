import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { randomBytes } from 'node:crypto';

test('device API requires authentication and rejects invalid cleanup requests before execution', async () => {
  const port = 45000 + Math.floor(Math.random() * 10000);
  const token = randomBytes(32).toString('hex');
  const child = spawn(process.execPath, ['scripts/cleanup-agent.mjs', '--serve'], {
    env: { ...process.env, BREATHING_ROOM_AGENT_PORT: String(port), BREATHING_ROOM_AGENT_API_TOKEN: token }, stdio: ['ignore', 'pipe', 'ignore'],
  });
  try {
    await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('API startup timed out')), 5000);
      child.once('error', error => { clearTimeout(timer); reject(error); });
      child.once('exit', () => { clearTimeout(timer); reject(new Error('API exited before startup')); });
      child.stdout.once('data', () => { clearTimeout(timer); resolve(); });
    });
    const url = `http://127.0.0.1:${port}`;
    assert.equal((await fetch(url + '/agent/status')).status, 401);
    const response = await fetch(url + '/cleanup/execute', { method: 'POST', headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }, body: JSON.stringify({ planId: '../../other', ids: ['item'], mode: 'subscription', model: 'openai/fixture' }) });
    assert.equal(response.status, 400);
    assert.ok((await response.json()).error);
  } finally { child.kill('SIGTERM'); }
});
