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

def run_card(pw, name, d, consent):
    """窓口の最初(win_decl の直前)で、同意の1枚が出るか・新しい文面か。consent は 前から入っている同意の記録"""
    res = {'route': name, 'errors': []}
    srv = T.serve(d); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780})
    ctx.add_init_script(T.INIT % json.dumps({'sr': True, 'az': True, 'decl': RB}))
    ctx.add_init_script("try{if(!localStorage.getItem('kanpe-voice-v1'))localStorage.setItem('kanpe-voice-v1',JSON.stringify({v:1,consent:%s,trips:[],next:null}))}catch(e){}" % json.dumps(consent))
    ctx.route(T.RELAY + '/token', lambda r: r.fulfill(status=200, content_type='application/json', headers={'access-control-allow-origin': '*'}, body=json.dumps({'token': 'x', 'region': 'japaneast', 'expiresInSec': 600})))
    ctx.route('**/tour/index.html', lambda r: T.hooked(r, 'tour'))
    page = ctx.new_page(); page.on('pageerror', lambda e: res['errors'].append(str(e)[:160]))
    page.goto(base + '/tour/index.html'); page.wait_for_timeout(700)
    page.evaluate("()=>{document.querySelectorAll('.trip-ov').forEach(function(o){o.remove()})}")
    page.evaluate("window.__PHASE='start';window.__T.save.win={step:0,m:{},cont:5,pick:null};window.__T.winStart()")
    t0 = time.time(); txt = ''
    while time.time() - t0 < 40:
        txt = page.evaluate("()=>document.getElementById('panel').innerText")
        if '発音をチェックしてみよう' in txt: break
        T.click_text(page, ['GO！', 'GO!']); time.sleep(.25)
    res['card_shown'] = '発音をチェックしてみよう' in txt
    res['card_text'] = txt[:400] if res['card_shown'] else ''
    if res['card_shown']:
        T.click_text(page, ['送ってOK']); page.wait_for_timeout(300)
        v = T.vstore(page); res['consent_after'] = v.get('consent') if v and v != 'bad' else None
    br.close(); srv.shutdown(); return res

if __name__ == '__main__':
    d_on = T.build('on', T.RELAY)
    ok = {'az': True, 'at': 1, 'ver': 2}
    with sync_playwright() as pw:
        R = [run(pw, 'A_yes_az', d_on, ok, True, True), run(pw, 'B_no', d_on, {'az': False, 'at': 1, 'ver': 2}, True, False),
             run(pw, 'C_yes_offline', d_on, ok, False, False)]
        R.append(run(pw, 'D_old_consent_v1', d_on, {'az': True, 'at': 1, 'ver': 1}, True, True))
        R.append(run_card(pw, 'E_old_yes_asked_again', d_on, {'az': True, 'at': 1, 'ver': 1}))
        R.append(run_card(pw, 'F_old_no_not_asked', d_on, {'az': False, 'at': 1, 'ver': 1}))
        R.append(run_card(pw, 'G_new_yes_not_asked', d_on, {'az': True, 'at': 1, 'ver': 2}))
    print(json.dumps(R, ensure_ascii=False, indent=1))
