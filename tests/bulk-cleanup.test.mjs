import test from 'node:test';
import assert from 'node:assert/strict';
import { resolveCleanupBatch, validateBulkPlan } from '../scripts/bulk-cleanup.mjs';
const credentials = { groq: 'fixture-groq' };
const rows = count => Array.from({ length: count }, (_, i) => ({ id: `row-${i}`, path: `/fixture/cache-${i}`, name: `Cache ${i}`, kind: 'tool', methods: [{ id: 'tool-npm', argv: ['npm', 'cache', 'clean', '--force'] }] }));
const reply = locations => Response.json({ choices: [{ message: { content: JSON.stringify({ actions: locations.map(row => ({ id: row.id, action: 'method', methodId: 'tool-npm', detail: 'Use the owning cache command' })) }) } }], usage: { prompt_tokens: 100, completion_tokens: 50 } });
test('multiple locations use one bulk LLM request and never invoke typed decision models', async () => {
  const hits = [];
  const result = await resolveCleanupBatch({ mode: 'decision', model: 'decisions/auto', locations: rows(12) }, { getCredentials: async () => credentials, fetcher: async (url, options) => { hits.push(url); return reply(JSON.parse(JSON.parse(options.body).messages[1].content).locations); } });
  assert.equal(hits.length, 1); assert.match(hits[0], /api.groq.com/);
  assert.equal(result.actions.length, 12); assert.equal(result.telemetry.requestCount, 1);
});
test('larger selections use bounded bulk chunks rather than individual fan-out', async () => {
  const sizes = [];
  const result = await resolveCleanupBatch({ mode: 'platform', model: 'platform/auto', locations: rows(50) }, { getCredentials: async () => credentials, fetcher: async (_url, options) => { const locations = JSON.parse(JSON.parse(options.body).messages[1].content).locations; sizes.push(locations.length); return reply(locations); } });
  assert.deepEqual(sizes, [24, 24, 2]); assert.equal(result.actions.length, 50);
});
test('foreign IDs and duplicate rows cannot authorize an action', () => {
  assert.throws(() => validateBulkPlan({ actions: [{ id: 'other', action: 'method', methodId: 'tool-npm', detail: 'invalid' }] }, rows(1)), /invalid/);
  assert.throws(() => validateBulkPlan({ actions: [{ id: 'row-0', action: 'approval', detail: '' }, { id: 'row-0', action: 'approval', detail: '' }] }, rows(1)), /duplicate/);
});
test('omitted or unavailable methods produce individual follow-ups without losing other decisions', () => {
  const result = validateBulkPlan({ actions: [{ id: 'row-0', action: 'method', methodId: 'unregistered', detail: 'unsupported command' }] }, rows(2));
  assert.equal(result.length, 2); assert.ok(result.every(r => r.action === 'manual'));
});
test('quota errors are retained in telemetry and return follow-up rows', async () => {
  const result = await resolveCleanupBatch({ mode: 'platform', locations: rows(3) }, { getCredentials: async () => credentials, fetcher: async () => new Response('quota', { status: 429 }) });
  assert.equal(result.telemetry.requestCount, 1);
  assert.equal(result.actions.length, 3);
  assert.ok(result.actions.every(r => r.fallback));
  assert.match(result.telemetry.failures[0], /429/);
});
test('bulk planning waits for the reported Groq token reset instead of hammering the limit', async () => {
  let clock = 0, requests = 0;
  const pauses = [];
  const result = await resolveCleanupBatch({ mode: 'platform', locations: rows(25) }, {
    getCredentials: async () => credentials, now: () => clock,
    wait: async ms => { pauses.push(ms); clock += ms; },
    fetcher: async (_url, options) => {
      requests++;
      const locations = JSON.parse(JSON.parse(options.body).messages[1].content).locations;
      const response = reply(locations);
      if (requests === 1) { response.headers.set('x-ratelimit-remaining-tokens', '0'); response.headers.set('x-ratelimit-reset-tokens', '2s'); }
      return response;
    },
  });
  assert.deepEqual(pauses, [2000]); assert.equal(result.actions.length, 25); assert.equal(requests, 2);
});
