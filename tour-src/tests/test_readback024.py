# -*- coding: utf-8 -*-
"""タスク024: 窓口の読み返し(win_rb)の発音評価の確認(ヘッドレス。マイクと本物の Azure は実機でしか確認できない)。
使い方: python3 tour-src/tests/test_readback024.py
3経路: (A)同意済み+Azure(偽SDK) → plog に src=az と az=[…] が残り、比べる記録(kanpe-voice-v1)の旅は増えない
       (B)同意しない → src=sr  (C)同意済みだが中継に届かない → src=sr(SRに落ちる)  (D)旧い同意(ver1)→ src=sr(取り直しまで送らない。ver が上がったあと)"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_routes as T
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.join(T.ROOT, 'tour-src'))
import window_data as WD
RB = WD.readback(WD.PRICE['star'][0], WD.PRICE['star'][2])

def run(pw, name, d, consent, token_ok, az):
    res = {'route': name, 'errors': []}
    srv = T.serve(d); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780})
    ctx.add_init_script(T.INIT % json.dumps({'sr': True, 'az': az, 'decl': RB}))
    if consent is not None:
        ctx.add_init_script("try{if(!localStorage.getItem('kanpe-voice-v1'))localStorage.setItem('kanpe-voice-v1',JSON.stringify({v:1,consent:%s,trips:[],next:null}))}catch(e){}" % json.dumps(consent))
    if token_ok:
        ctx.route(T.RELAY + '/token', lambda r: r.fulfill(status=200, content_type='application/json', headers={'access-control-allow-origin': '*'}, body=json.dumps({'token': 'x', 'region': 'japaneast', 'expiresInSec': 600})))
    else:
        ctx.route(T.RELAY + '/**', lambda r: r.abort())
    ctx.route('**/tour/index.html', lambda r: T.hooked(r, 'tour'))
    page = ctx.new_page(); page.on('pageerror', lambda e: res['errors'].append(str(e)[:160]))
    page.goto(base + '/tour/index.html'); page.wait_for_timeout(700)
    page.evaluate("()=>{document.querySelectorAll('.trip-ov').forEach(function(o){o.remove()})}")
    page.evaluate("window.__PHASE='start';window.__T.save.win={step:9,m:{},cont:5,pick:'star'};window.__T.winStart()")
    t0 = time.time(); plog = None; logs = []
    while time.time() - t0 < 60:
        plog = page.evaluate("()=>{try{return JSON.parse(localStorage.getItem('kanpe-pron-v1')||'[]').filter(function(x){return x.diag==='readback'})}catch(e){return []}}")
        if plog: break
        T.click_text(page, ['GO！', 'GO!']); time.sleep(.25)
    res['plog'] = [{k: x.get(k) for k in ('diag', 'src', 'az', 'ok', 'n', 'seg')} for x in plog or []]
    v = T.vstore(page); res['trips'] = len(v['trips']) if v and v != 'bad' else None
    res['errors'] += page.evaluate("window.__errs"); br.close(); srv.shutdown(); return res

if __name__ == '__main__':
    d_on = T.build('on', T.RELAY)
    ok = {'az': True, 'at': 1, 'ver': 2}
    with sync_playwright() as pw:
        R = [run(pw, 'A_yes_az', d_on, ok, True, True), run(pw, 'B_no', d_on, {'az': False, 'at': 1, 'ver': 2}, True, False),
             run(pw, 'C_yes_offline', d_on, ok, False, False)]
        if len(sys.argv) > 1 and sys.argv[1] == 'old': R.append(run(pw, 'D_old_consent_v1', d_on, {'az': True, 'at': 1, 'ver': 1}, True, True))
    print(json.dumps(R, ensure_ascii=False, indent=1))
