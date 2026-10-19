import { build } from 'esbuild';
await build({ entryPoints: ['scripts/cleanup-agent.mjs'], outfile: 'scripts/cleanup/agent.mjs', bundle: true, platform: 'node', format: 'esm', target: 'node22' });
