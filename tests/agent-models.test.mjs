import test from 'node:test';
import assert from 'node:assert/strict';
import { isFreeModel, modelCatalog } from '../scripts/agent-models.mjs';

test('catalog retains every runtime provider and model, including custom, image and deprecated models', () => {
  const providers = [{ id: 'custom-provider', name: 'Custom Provider', models: {
    custom: { id: 'custom', name: 'Custom Text' },
    image: { id: 'image', name: 'Image model', capabilities: { toolcall: false, output: { text: false } } },
    retired: { id: 'retired', name: 'Retired model', status: 'deprecated' },
  } }];
  const catalog = modelCatalog({ providers, default: { 'custom-provider': 'custom' } }, []);
  assert.deepEqual(catalog[0].models.map(m => m.id), ['custom', 'image', 'retired']);
  assert.equal(catalog[0].models[1].cleanupCompatible, false);
  assert.equal(catalog[0].defaultModel, 'custom');
});
test('free classification requires zero pricing, including cache and higher-context tiers', () => {
  const cost = { input: 0, output: 0, cache: { read: 0, write: 0 } };
  assert.equal(isFreeModel('opencode', { cost }), true);
  assert.equal(isFreeModel('openai', { cost }), false, 'OAuth zero-price metadata is a subscription, not a free model');
  assert.equal(isFreeModel('opencode', {}), false);
  assert.equal(isFreeModel('opencode', { cost: { ...cost, cache: { read: 0.1 } } }), false);
  assert.equal(isFreeModel('opencode', { cost: { ...cost, tiers: [{ input: 1, output: 0 }] } }), false);
});
test('subscription detection uses provider metadata names for custom IDs', () => {
  const catalog = modelCatalog({ providers: [{ id: 'new-oauth-provider', name: 'New Provider', models: { model: { id: 'model', name: 'Model' } } }] }, [{ name: 'New Provider', authentication: 'subscription' }]);
  assert.equal(catalog[0].models[0].mode, 'subscription');
});
