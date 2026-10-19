import test from 'node:test';
import assert from 'node:assert/strict';
import { requestDecision, resolveDecisionCleanup } from '../scripts/typed-decisions.mjs';
const credentials = { jev: 'fixture-jev', cloudflare: 'fixture-cloud', account: 'a'.repeat(32) };
const input = { state: { fixture: true }, questions: { disposable: { type: 'noul', instructions: 'Is this reproducible?' } } };
const response = (questions, model = 'jev-1.13.0') => Response.json({ model, answers: Object.fromEntries(Object.keys(questions).map(id => [id, { type: 'noul', noul: .99 }])), usage: { input_tokens: 10, output_tokens: 1 } });
test('Jev is attempted first and Clef receives the identical state/questions after failure', async () => {
  const hits = [];
  const result = await requestDecision(input, { getCredentials: async () => credentials, fetcher: async (url, options) => {
    const body = JSON.parse(options.body); hits.push(url);
    assert.deepEqual(body.state, input.state); assert.deepEqual(body.questions, input.questions);
    if (url.includes('typesafe')) return new Response('rate limited', { status: 429 });
    assert.equal(options.headers.Authorization, 'Bearer fixture-cloud');
    assert.equal(body.model, 'clef-flash'); return response(body.questions, 'clef-flash');
  } });
  assert.equal(result.provider, 'clef'); assert.equal(hits.length, 2);
  assert.match(hits[1], /ai\/run\/@cf\/cloudflare\/clef-flash$/);
});
test('invalid Jev typed answers trigger Clef fallback', async () => {
  const result = await requestDecision(input, { getCredentials: async () => credentials, fetcher: async url => url.includes('typesafe') ? Response.json({ model: 'jev', answers: { disposable: { type: 'noul', noul: true } } }) : response(input.questions, 'clef-flash') });
  assert.equal(result.provider, 'clef');
});
test('96 questions are batched within the compatible 64-question limit', async () => {
  const counts = [];
  const questions = Object.fromEntries(Array.from({ length: 96 }, (_, i) => [`q_${i}`, { type: 'noul', instructions: 'Fixture' }]));
  const result = await requestDecision({ state: {}, questions }, { getCredentials: async () => credentials, fetcher: async (_url, options) => { const body = JSON.parse(options.body); counts.push(Object.keys(body.questions).length); return response(body.questions); } });
  assert.deepEqual(counts, [64, 32]); assert.equal(Object.keys(result.answers).length, 96);
  assert.equal(result.usage.input_tokens, 20);
});
test('only a confident listed method can become argv; unique-data decisions preserve', async () => {
  const argv = ['cargo', 'clean', '--target-dir', '/fixture/target'];
  const call = async unique => resolveDecisionCleanup({ supportedMethods: [{ argv }], location: {} }, {
    getCredentials: async () => credentials,
    fetcher: async () => Response.json({ model: 'jev', answers: {
      action: { type: 'choice', choice: 'method_0', confidence: .99, probabilities: { method_0: .99, approval: .01, preserve: 0, research: 0 } },
      unique: { type: 'noul', noul: unique },
    } }),
  });
  assert.deepEqual((await call(.01)).argv, argv);
  const preserved = await call(.9); assert.deepEqual(preserved.argv, []); assert.equal(preserved.disposition, 'preserve');
});
test('Jev-only selection never silently switches to Clef', async () => {
  const hits = [];
  await assert.rejects(requestDecision({ ...input, selection: 'jev' }, { getCredentials: async () => credentials, fetcher: async url => { hits.push(url); return new Response('unauthorized', { status: 401 }); } }), /typed decisions unavailable/);
  assert.equal(hits.length, 1);
});
