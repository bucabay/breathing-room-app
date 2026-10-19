// Docs: docs/cleanup-agent.md. Shared secret and bounded JSON transport for AI providers.
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
const exec = promisify(execFile);
export async function readSecret(name) {
  try { return (await exec('seal', ['get', name], { timeout: 5000, maxBuffer: 16384 })).stdout.trim(); }
  catch { return ''; }
}
export async function readJson(response) {
  if (!response.body) throw new Error('Provider returned no body');
  const reader = response.body.getReader(), decoder = new TextDecoder();
  let size = 0, text = '';
  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > 128000) throw new Error('Provider response exceeded its limit');
      text += decoder.decode(value, { stream: true });
    }
    return JSON.parse(text + decoder.decode());
  } finally { await reader.cancel().catch(() => {}); }
}
