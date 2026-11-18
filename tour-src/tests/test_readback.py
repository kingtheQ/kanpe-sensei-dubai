# -*- coding: utf-8 -*-
"""タスク024: 窓口の読み返し(win_rb)に Azure を使う確認(ヘッドレス。マイクと本物の Azure は実機でしか確認できない)。
使い方: python3 tour-src/tests/test_readback.py
 A 同意あり+中継あり → Azure で読む(plog に src='az' と4つの値。kanpe-voice-v1 の旅の記録には入らない)
 B 同意なし → ブラウザの音声認識(src='sr')
 C 同意あり+通信できない → ブラウザの音声認識に切りかえ(src='sr')
 D 中継なし(今の公開状態) → ブラウザの音声認識(src='sr')"""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_routes as T
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.join(T.ROOT, 'tour-src'))
import window_data
PRICE = window_data.PRICE['star']
RB = window_data.readback(PRICE[0], PRICE[2])
HOOK = "window.__T={G:G,save:save,winStart:winStart,voiceSetConsent:voiceSetConsent,WSTEP:WSTEP};"

def run(pw, name, d, relay_on, consent, token_ok, az):
    srv = T.serve(d); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780})
    ctx.add_init_script(T.INIT % json.dumps({'sr': True, 'az': az, 'decl': RB}))
    if relay_on:
        if token_ok:
            ctx.route(T.RELAY + '/token', lambda r: r.fulfill(status=200, content_type='application/json', headers={'access-control-allow-origin': '*'}, body=json.dumps({'token': 'x', 'region': 'japaneast', 'expiresInSec': 600})))
        else:
            ctx.route(T.RELAY + '/**', lambda r: r.abort())
    def hook(route):
        r = route.fetch(); body = r.text(); assert T.HOOK_N in body
        route.fulfill(response=r, body=body.replace(T.HOOK_N, HOOK + T.HOOK_N, 1))
    ctx.route('**/tour/index.html', hook)
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
    pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(700)
    pg.evaluate("(c)=>{ if(c!==null) __T.voiceSetConsent(c); var i=__T.WSTEP.indexOf('win_rb'); __T.save.win={step:i,m:{},cont:5,pick:'star'}; __T.winStart(); }", consent)
    out = {'route': name, 'plog': None}
    for _ in range(120):
        p = pg.evaluate("()=>{try{return JSON.parse(localStorage.getItem('kanpe-pron-v1')||'[]')}catch(e){return []}}")
        rb = [x for x in p if x.get('diag') == 'readback']
        if rb: out['plog'] = rb[-1]; break
        T.click_text(pg, ['GO！', 'GO!'])
        pg.wait_for_timeout(250)
    out['voice'] = pg.evaluate("()=>{try{return JSON.parse(localStorage.getItem('kanpe-voice-v1')||'null')}catch(e){return 'bad'}}")
    out['errors'] = errs
    pg.screenshot(path=os.path.join(T.SHOTS, name + '_rb.png'))
    br.close(); srv.shutdown(); return out

if __name__ == '__main__':
    os.makedirs(T.SHOTS, exist_ok=True)
    d_off = T.build('off', None); d_on = T.build('on', T.RELAY)
    R = []; fails = []
    def ck(name, cond, info=''):
        R.append(('OK' if cond else 'NG', name, info))
        if not cond: fails.append(name)
    with sync_playwright() as pw:
        A = run(pw, 'rbA_az', d_on, True, True, True, True)
        B = run(pw, 'rbB_no', d_on, True, False, True, False)
        C = run(pw, 'rbC_offline', d_on, True, True, False, False)
        D = run(pw, 'rbD_norelay', d_off, False, None, False, False)
    pa = A['plog'] or {}
    ck('A: 読み返しが記録された', bool(A['plog']))
    ck('A: src=az', pa.get('src') == 'az', pa.get('src'))
    ck('A: 4つの値は Azure の値そのまま [総合,正確さ,流れ,言い切り度]', pa.get('sc') == [80, 80, 66, 100], pa.get('sc'))
    ck('A: nv=2', pa.get('nv') == 2, pa.get('nv'))
    n = pa.get('n') or 0; bits = pa.get('bits') or ''
    ck('A: bits の長さ = 単語数', len(bits) == n and n > 0, '%s/%s' % (len(bits), n))
    toks = [t for t in RB.split(' ')]
    low = [i for i, t in enumerate(toks) if re.search(r'th|r|l|v', re.sub(r"[^A-Za-z']", '', t), re.I)]
    ck('A: Azure の正確さが60未満の単語(th/r/l/v を含む語)が「言えなかった」', all(bits[i] == '0' for i in low) and len(low) > 0, '%d語' % len(low))
    ck('A: それ以外の単語は「言えた」', all(bits[i] == '1' for i in range(len(toks)) if i not in low))
    ck('A: ok = 単語数 − 言えなかった数', pa.get('ok') == n - bits.count('0'), '%s' % pa.get('ok'))
    ck('A: miss の k=az', any(m.get('k') == 'az' for m in pa.get('miss', [])))
    ck('A: 読み返しは kanpe-voice-v1 の旅の記録(始め/終わり)に入らない', not (A['voice'] and A['voice'].get('trips')), json.dumps(A['voice'])[:80])
    for X, nm, want in ((B, 'B', 'sr'), (C, 'C', 'sr'), (D, 'D', 'sr')):
        px = X['plog'] or {}
        ck('%s: 読み返しが記録された' % nm, bool(X['plog']))
        ck('%s: src=sr' % nm, px.get('src') == want, px.get('src'))
        ck('%s: 数字(sc)なし' % nm, 'sc' not in px)
    ck('JSエラー0', all(not x['errors'] for x in (A, B, C, D)), json.dumps([x['errors'] for x in (A, B, C, D)])[:100])
    for r in R: print('%-3s %s %s' % r)
    print('合計 %d 件 / NG %d 件' % (len(R), len(fails)))
    sys.exit(1 if fails else 0)
