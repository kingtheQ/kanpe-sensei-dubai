// 手元テスト：本物のキーは使わず、Azure の返事をにせものに差し替えて、中継の動きだけを確かめる。
// 実行：node relay/test/worker.test.mjs
import worker from '../worker.js';
import assert from 'node:assert/strict';

let calls = [];
globalThis.fetch = async (url, init) => {
  calls.push({ url, init });
  if (init.headers['Ocp-Apim-Subscription-Key'] === 'BAD') return new Response('denied', { status: 401 });
  return new Response('FAKE.TOKEN.VALUE', { status: 200 });
};
const env = { ALLOWED_ORIGINS: 'https://kingtheq.github.io', AZURE_SPEECH_REGION: 'eastus', AZURE_SPEECH_KEY: 'TESTKEY' };
const req = (path, o = {}) => new Request('https://relay.example.workers.dev' + path, { method: o.method || 'GET', headers: Object.assign({ 'CF-Connecting-IP': o.ip || '1.1.1.1' }, o.headers || {}) });
const results = [];
async function t(name, fn) { try { await fn(); results.push([name, 'OK']); } catch (e) { results.push([name, 'NG ' + e.message]); process.exitCode = 1; } }

await t('許可された場所から：トークンが返り、キーは本文に含まれない', async () => {
  const r = await worker.fetch(req('/token', { headers: { Origin: 'https://kingtheq.github.io' } }), env);
  assert.equal(r.status, 200);
  const body = await r.text();
  assert.ok(!body.includes('TESTKEY'));
  const j = JSON.parse(body);
  assert.equal(j.token, 'FAKE.TOKEN.VALUE'); assert.equal(j.region, 'eastus'); assert.ok(j.expiresInSec > 0 && j.expiresInSec <= 540);
  assert.equal(r.headers.get('Access-Control-Allow-Origin'), 'https://kingtheq.github.io');
  assert.equal(calls[0].url, 'https://eastus.api.cognitive.microsoft.com/sts/v1.0/issueToken');
  assert.equal(calls[0].init.method, 'POST');
});
await t('2回目はAzureに聞き直さず使い回す', async () => {
  const n = calls.length;
  await worker.fetch(req('/token', { headers: { Origin: 'https://kingtheq.github.io' } }), env);
  assert.equal(calls.length, n);
});
await t('知らない場所（Origin）は403で、Azureを呼ばない', async () => {
  const n = calls.length;
  const r = await worker.fetch(req('/token', { headers: { Origin: 'https://evil.example' } }), env);
  assert.equal(r.status, 403); assert.equal(r.headers.get('Access-Control-Allow-Origin'), null); assert.equal(calls.length, n);
});
await t('Originなし（ブラウザ以外）も403', async () => {
  assert.equal((await worker.fetch(req('/token'), env)).status, 403);
});
await t('事前確認（OPTIONS）：許可は204、不許可は403', async () => {
  assert.equal((await worker.fetch(req('/token', { method: 'OPTIONS', headers: { Origin: 'https://kingtheq.github.io' } }), env)).status, 204);
  assert.equal((await worker.fetch(req('/token', { method: 'OPTIONS', headers: { Origin: 'https://evil.example' } }), env)).status, 403);
});
await t('/token 以外は404、POSTは405', async () => {
  const h = { Origin: 'https://kingtheq.github.io' };
  assert.equal((await worker.fetch(req('/', { headers: h }), env)).status, 404);
  assert.equal((await worker.fetch(req('/token', { method: 'POST', headers: h }), env)).status, 405);
});
await t('キー未登録は503', async () => {
  const r = await worker.fetch(req('/token', { ip: '2.2.2.2', headers: { Origin: 'https://kingtheq.github.io' } }), { ...env, AZURE_SPEECH_KEY: '' });
  assert.equal(r.status, 503);
});
await t('1分に13回目は429', async () => {
  let last;
  for (let i = 0; i < 13; i++) last = await worker.fetch(req('/token', { ip: '3.3.3.3', headers: { Origin: 'https://kingtheq.github.io' } }), env);
  assert.equal(last.status, 429);
});
for (const [n, s] of results) console.log((s === 'OK' ? '✓ ' : '✗ ') + n + (s === 'OK' ? '' : ' → ' + s));
console.log(results.filter((r) => r[1] === 'OK').length + ' / ' + results.length + ' 通過');
