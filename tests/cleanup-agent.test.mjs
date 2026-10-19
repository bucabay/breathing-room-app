import test from 'node:test';
import assert from 'node:assert/strict';
import { resolveCleanup, status } from '../scripts/cleanup-agent.mjs';

function fixture(output = { argv: [], detail: 'Use owning app controls', source: '' }) {
  const calls = [];
  return { calls, getConnections: async () => [{ id: 'openai', authentication: 'subscription' }], launch: async () => ({
    close: async () => calls.push('close'), client: {
      config: { providers: async () => ({ data: { providers: [{ id: 'openai', models: { fixture: {} } }] } }) },
      session: {
        create: async () => ({ data: { id: 'test-session' } }),
        prompt: async input => { calls.push(input.model); return { data: { info: { structured: output }, parts: [] } }; },
        abort: async () => calls.push('abort'), delete: async () => calls.push('delete'),
      },
    },
  }) };
}
test('subscription uses the explicitly selected model and releases the SDK session', async () => {
  const hooks = fixture();
  const result = await resolveCleanup({ mode: 'subscription', model: 'openai/fixture', location: {}, supportedMethods: [] }, hooks);
  assert.deepEqual(result.argv, []);
  assert.deepEqual(hooks.calls, [{ providerID: 'openai', modelID: 'fixture' }, 'abort', 'delete', 'close']);
});
test('API mode never silently uses an OAuth subscription', async () => {
  const hooks = fixture();
  await assert.rejects(resolveCleanup({ mode: 'api', model: 'openai/fixture' }, hooks), /not connected in api mode/);
  assert.deepEqual(hooks.calls, []);
});
test('malformed agent output is rejected and the session is still closed', async () => {
  const hooks = fixture({ argv: 'rm -rf /' });
  await assert.rejects(resolveCleanup({ mode: 'subscription', model: 'openai/fixture' }, hooks), /structured cleanup output/);
  assert.deepEqual(hooks.calls.slice(-3), ['abort', 'delete', 'close']);
});

function freeFixture(cost = { input: 0, output: 0, cache: { read: 0, write: 0 } }) {
  const hooks = fixture();
  const launch = hooks.launch;
  hooks.getConnections = async () => [];
  hooks.launch = async options => {
    const runtime = await launch(options);
    runtime.client.config.providers = async () => ({ data: { providers: [{ id: 'opencode', name: 'OpenCode Zen', models: { fixture: { id: 'fixture', name: 'Free fixture', cost } } }] } });
    return runtime;
  };
  return hooks;
}
test('free mode works without a configured API credential and pins the selected model', async () => {
  const hooks = freeFixture();
  await resolveCleanup({ mode: 'free', model: 'opencode/fixture', location: {}, supportedMethods: [] }, hooks);
  assert.deepEqual(hooks.calls, [{ providerID: 'opencode', modelID: 'fixture' }, 'abort', 'delete', 'close']);
});
test('free mode refuses a paid model before creating a session or buying inference', async () => {
  const hooks = freeFixture({ input: 0.1, output: 0.5 });
  await assert.rejects(resolveCleanup({ mode: 'free', model: 'opencode/fixture' }, hooks), /not a zero-cost/);
  assert.deepEqual(hooks.calls, ['close']);
});
test('status includes models without auth-list entries', async () => {
  const hooks = freeFixture();
  const result = await status({ ...hooks, getCredentials: async () => ({}), getDecisionCredentials: async () => ({}) });
  assert.equal(result.providers.find(p => p.id === 'opencode').models[0].mode, 'free');
  assert.deepEqual(hooks.calls, ['close']);
});
