// 空港えいご物語：Azure Speech 用の中継（Cloudflare Workers）
// やること：キーをこの中に隠したまま、短時間だけ使える「トークン」を配る。
// キーはコードに書かない。Cloudflare の「シークレット」（AZURE_SPEECH_KEY）に、持ち主が自分の手で登録する。

const TOKEN_LIFETIME_MS = 9 * 60 * 1000; // Azure のトークンは10分有効。余裕を見て9分で使い回しを止める
const MAX_PER_MIN_PER_IP = 12; // 1つの端末あたり、1分に配る回数の上限（この Worker の1つの実行場所の中での目安）

let cache = null; // { token, exp }
const hits = new Map(); // ip -> { n, reset }

function allowedOrigins(env) {
  return String(env.ALLOWED_ORIGINS || '')
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);
}

function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '600',
    Vary: 'Origin',
  };
}

function json(body, status, extra) {
  return new Response(JSON.stringify(body), {
    status,
    headers: Object.assign(
      { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
      extra || {}
    ),
  });
}

function tooMany(ip, now) {
  if (hits.size > 500) {
    for (const [k, v] of hits) if (v.reset <= now) hits.delete(k);
  }
  const h = hits.get(ip);
  if (!h || h.reset <= now) {
    hits.set(ip, { n: 1, reset: now + 60000 });
    return false;
  }
  h.n += 1;
  return h.n > MAX_PER_MIN_PER_IP;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin') || '';
    const ok = allowedOrigins(env).includes(origin);
    const cors = ok ? corsHeaders(origin) : {};

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: ok ? 204 : 403, headers: cors });
    }
    if (url.pathname !== '/token') return json({ error: 'not_found' }, 404, cors);
    if (request.method !== 'GET') return json({ error: 'method_not_allowed' }, 405, cors);
    // ブラウザから来た求めだけ通す（Origin が許可リストにあるものだけ）
    if (!ok) return json({ error: 'forbidden' }, 403);

    const key = env.AZURE_SPEECH_KEY;
    const region = env.AZURE_SPEECH_REGION || 'eastus';
    if (!key) return json({ error: 'not_configured' }, 503, cors);

    const now = Date.now();
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    if (tooMany(ip, now)) return json({ error: 'rate_limited' }, 429, Object.assign({ 'Retry-After': '60' }, cors));

    if (!cache || cache.exp <= now) {
      let res;
      try {
        res = await fetch('https://' + region + '.api.cognitive.microsoft.com/sts/v1.0/issueToken', {
          method: 'POST',
          headers: { 'Ocp-Apim-Subscription-Key': key, 'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': '0' },
        });
      } catch (e) {
        return json({ error: 'upstream_unreachable' }, 502, cors);
      }
      if (!res.ok) return json({ error: 'upstream_error', status: res.status }, 502, cors); // キーや本文は返さない
      cache = { token: (await res.text()).trim(), exp: now + TOKEN_LIFETIME_MS };
    }
    const secsLeft = Math.max(1, Math.floor((cache.exp - now) / 1000));
    return json({ token: cache.token, region, expiresInSec: secsLeft }, 200, cors);
  },
};
