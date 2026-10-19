import test from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { buildSync } from 'esbuild';
test('desktop sign-in offers Google, GitHub, and email with the same disabled state', () => {
  const { outputFiles } = buildSync({ stdin: { contents: `import {renderToStaticMarkup} from 'react-dom/server';import {AuthProviderButtons} from './src/components/auth-provider-buttons';export const render=disabled=>renderToStaticMarkup(<AuthProviderButtons disabled={disabled} onSelect={()=>{}}/>);export function select(){const selected=[];const node=AuthProviderButtons({disabled:false,onSelect:p=>selected.push(p)});node.props.children.forEach(child=>child.props.onClick());return selected;}`, loader: 'tsx', resolveDir: new URL('..', import.meta.url).pathname }, bundle: true, platform: 'node', format: 'cjs', jsx: 'automatic', write: false });
  const module = { exports: {} };
  new Function('require', 'module', 'exports', outputFiles[0].text)(createRequire(import.meta.url), module, module.exports);
  assert.deepEqual(module.exports.select(), ['google', 'github', 'email']);
  const enabled = module.exports.render(false);
  assert.equal((enabled.match(/<button /g) || []).length, 3);
  for (const provider of ['google', 'github', 'email']) assert.ok(enabled.includes(`data-provider-icon="${provider}"`));
  assert.equal((module.exports.render(true).match(/ disabled=""/g) || []).length, 3);
});
