# -*- coding: utf-8 -*-
"""タスク024: 同意文の版(ver)の確認。使い方: python3 tour-src/tests/test_consent.py
 1 まだ聞いていない人 → 新しい文面の1枚が出る(窓口の宣言の直前)
 2 古い文面(ver 1)で「送ってOK」と答えた人 → 新しい文面で もう一度聞く。聞くまでは Azure に送らない
 3 古い文面(ver 1)で「送らない」と答えた人 → 聞き直さない(送らないままを守る)
 4 新しい文面で答えた人 → 聞き直さない
 5 「送ってOK」を押すと ver が新しくなる
 6 文面に、送る場面(はじめの宣言・窓口の読み返し・おわりの宣言)が全部ある。「この2回」の言い方が残っていない"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_routes as T
from playwright.sync_api import sync_playwright
HOOK = "window.__T={G:G,save:save,winStart:winStart,voiceAzureOn:voiceAzureOn,voiceNeedConsent:voiceNeedConsent,voiceConsent:voiceConsent,CV:CONSENT_VER};"

def probe(pw, d, stored):
    srv = T.serve(d); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780})
    ctx.add_init_script("try{speechSynthesis.speak=function(u){setTimeout(function(){if(u.onend)u.onend({})},8)}}catch(e){}")
    def hook(route):
        r = route.fetch(); body = r.text(); assert T.HOOK_N in body
        route.fulfill(response=r, body=body.replace(T.HOOK_N, HOOK + T.HOOK_N, 1))
    ctx.route('**/tour/index.html', hook)
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
    pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(600)
    if stored is not None:
        pg.evaluate("(s)=>localStorage.setItem('kanpe-voice-v1',JSON.stringify(s))", {'v': 1, 'consent': stored, 'trips': [], 'next': None})
    pg.evaluate("()=>__T.winStart()"); pg.wait_for_timeout(900)
    o = pg.evaluate("()=>({phase:__T.G.phase,txt:document.getElementById('panel').innerText,az:__T.voiceAzureOn(),need:__T.voiceNeedConsent(),cv:__T.CV})")
    o['errors'] = errs; o['pg'] = pg; o['br'] = br; o['srv'] = srv
    return o

if __name__ == '__main__':
    os.makedirs(T.SHOTS, exist_ok=True)
    d_on = T.build('on', T.RELAY)
    R = []; fails = []
    def ck(name, cond, info=''):
        R.append(('OK' if cond else 'NG', name, info))
        if not cond: fails.append(name)
    with sync_playwright() as pw:
        o = probe(pw, d_on, None)
        cv = o['cv']
        ck('1 まだ聞いていない → 同意の1枚が出る', o['phase'] == 'consent' and '声を送ってもいい' in o['txt'], o['phase'])
        txt = o['txt']
        ck('6 はじめの宣言・窓口の読み返し・おわりの宣言が書いてある', all(k in txt for k in ('はじめの宣言', '読み返し', 'おわりの宣言')))
        ck('6 「この3回」で、「この2回」は残っていない', 'この3回' in txt and '2回' not in txt)
        ck('6 送らなくても最後まで遊べる・設定で変えられる', '送らなくても' in txt and '設定' in txt)
        o['pg'].screenshot(path=os.path.join(T.SHOTS, 'consent_v2.png'))
        T.click_text(o['pg'], ['送ってOK']); o['pg'].wait_for_timeout(400)
        st = T.vstore(o['pg'])
        ck('5 「送ってOK」で ver が新しくなる', st and st['consent']['az'] is True and st['consent']['ver'] == cv, json.dumps(st['consent']) if st else '')
        o['br'].close(); o['srv'].shutdown()
        o = probe(pw, d_on, {'az': True, 'at': 1, 'ver': 1})
        ck('2 古い文面で OK した人 → もう一度聞く', o['phase'] == 'consent', o['phase'])
        ck('2 聞くまでは Azure に送らない', o['az'] is False)
        o['br'].close(); o['srv'].shutdown()
        o = probe(pw, d_on, {'az': False, 'at': 1, 'ver': 1})
        ck('3 古い文面で「送らない」の人 → 聞き直さない', o['phase'] != 'consent' and o['need'] is False, o['phase'])
        ck('3 送らないまま', o['az'] is False)
        o['br'].close(); o['srv'].shutdown()
        o = probe(pw, d_on, {'az': True, 'at': 1, 'ver': cv})
        ck('4 新しい文面で OK した人 → 聞き直さない', o['phase'] != 'consent' and o['need'] is False, o['phase'])
        ck('4 Azure を使う', o['az'] is True)
        ck('JSエラー0', not o['errors'])
        o['br'].close(); o['srv'].shutdown()
    for r in R: print('%-3s %s %s' % r)
    print('合計 %d 件 / NG %d 件' % (len(R), len(fails)))
    sys.exit(1 if fails else 0)
