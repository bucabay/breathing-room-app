// OpenCode's runtime catalog is the source of truth, as in Shipherd.
export function isFreeModel(providerID, model) {
  if (providerID !== 'opencode' || !model?.cost || model.cost.input !== 0 || model.cost.output !== 0) return false;
  const prices = [model.cost, ...(model.cost.tiers ?? []), ...(model.cost.experimentalOver200K ? [model.cost.experimentalOver200K] : [])];
  return prices.every(price => price.input === 0 && price.output === 0 && (price.cache?.read ?? 0) === 0 && (price.cache?.write ?? 0) === 0);
}

export function cleanupCompatible(model) {
  return model.capabilities?.toolcall !== false && model.capabilities?.input?.text !== false && model.capabilities?.output?.text !== false;
}

export function modelCatalog(data, connections = []) {
  return data.providers.map(provider => {
    const connection = connections.find(c => c.id === provider.id || c.name?.toLowerCase() === provider.name?.toLowerCase());
    const authentication = connection?.authentication ?? 'api';
    const models = Object.values(provider.models).map(model => ({
      id: model.id, name: model.name, cost: model.cost, status: model.status,
      mode: isFreeModel(provider.id, model) ? 'free' : authentication,
      cleanupCompatible: cleanupCompatible(model),
    }));
    const defaults = models.filter(m => m.cleanupCompatible && m.status !== 'deprecated');
    const preferred = provider.id === 'opencode' ? defaults.find(m => m.mode === 'free') : defaults.find(m => m.id === data.default?.[provider.id]);
    return { id: provider.id, name: provider.name, authentication, models, defaultModel: preferred?.id ?? defaults[0]?.id ?? models[0]?.id ?? '' };
  }).sort((a, b) => Number(b.authentication === 'subscription') - Number(a.authentication === 'subscription'));
}
