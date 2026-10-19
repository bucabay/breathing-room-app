import test from 'node:test';
import assert from 'node:assert/strict';
import { resolvePlatformCleanup, platformCredentials } from '../scripts/platform-ai.mjs';
const credentials = { account: 'a'.repeat(32), cloudflare: 'fixture-cloud', groq: 'fixture-groq' };
const input = { location: { path: '/fixture/cache' }, supportedMethods: [] };
const reply = () => Response.json({ choices: [{ message: { content: JSON.stringify({ argv: [], detail: 'Use app cache controls', source: '' }) } }], usage: { prompt_tokens: 3000, completion_tokens: 500 } });
test('Workers AI is primary and returns measured-token neuron estimates', async () => {
  const hits = [];
  const result = await resolvePlatformCleanup(input, { getCredentials: async () => credentials, fetcher: async (url, options) => { hits.push(url); assert.equal(JSON.parse(options.body).chat_template_kwargs.enable_thinking, false); return reply(); } });
  assert.equal(result.provider, 'workers-ai');
  assert.equal(result.estimatedNeurons, 205);
  assert.equal(hits.length, 1);
});
test('quota and capacity failures fall back to Groq, without sending it the Cloudflare token', async () => {
  const hits = [];
  const result = await resolvePlatformCleanup(input, { getCredentials: async () => credentials, fetcher: async (url, options) => { hits.push(url); if (url.includes('cloudflare')) return new Response('quota', { status: 429 }); assert.equal(options.headers.Authorization, 'Bearer fixture-groq'); return reply(); } });
  assert.equal(result.provider, 'groq');
  assert.equal(hits.length, 2);
});
test('missing credentials cause no network requests and expose no secret values', async () => {
  let called = false;
  await assert.rejects(resolvePlatformCleanup(input, { getCredentials: async () => ({}), fetcher: async () => { called = true; return reply(); } }), /setup required/);
  assert.equal(called, false);
});
test('explicit Groq selection stays pinned even when Workers AI is configured', async () => {
  const hits = [];
  const result = await resolvePlatformCleanup({ ...input, model: 'platform/groq' }, { getCredentials: async () => credentials, fetcher: async url => { hits.push(url); return reply(); } });
  assert.equal(result.provider, 'groq');
  assert.deepEqual(hits, ['https://api.groq.com/openai/v1/chat/completions']);
});
test('missing token usage does not incorrectly report zero neurons consumed', async () => {
  const result = await resolvePlatformCleanup(input, { getCredentials: async () => credentials, fetcher: async () => Response.json({ response: JSON.stringify({ argv: [], detail: 'Use app controls', source: '' }) }) });
  assert.equal(result.estimatedNeurons, undefined);
});
test('environment credentials take precedence over Seal and are never persisted', async () => {
  const result = await platformCredentials({ CLOUDFLARE_ACCOUNT_ID: credentials.account, CLOUDFLARE_AI_API_TOKEN: 'env-token', GROQ_API_KEY: 'env-groq' }, async () => { throw new Error('Must not read Seal'); });
  assert.equal(result.cloudflare, 'env-token');
  assert.equal(result.groq, 'env-groq');
});
test('the user-supplied grok/api-key Seal entry is the preferred Groq credential', async () => {
  const names = [];
  const result = await platformCredentials({ CLOUDFLARE_ACCOUNT_ID: credentials.account, CLOUDFLARE_AI_API_TOKEN: 'env-token' }, async name => { names.push(name); return name === 'grok/api-key' ? 'fixture-saved-groq' : ''; });
  assert.equal(result.groq, 'fixture-saved-groq'); assert.deepEqual(names, ['grok/api-key']);
});
test('default routing tries typed decisions before generative inference for known methods', async () => {
  let fetched = false;
  const result = await resolvePlatformCleanup({ model: 'platform/auto', location: {}, supportedMethods: [{ argv: ['fixture'] }] }, {
    decide: async () => ({ argv: ['fixture'], model: 'clef-flash' }),
    getCredentials: async () => credentials,
    fetcher: async () => { fetched = true; return reply(); },
  });
  assert.equal(result.model, 'clef-flash'); assert.equal(fetched, false);
});
