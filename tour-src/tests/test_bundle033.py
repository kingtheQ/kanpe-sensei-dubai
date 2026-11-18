# -*- coding: utf-8 -*-
"""タスク033: つづり(チケットを みる)が静止して読めることの確認(ヘッドレス・Android Chrome 相当の画面)。
python3 tour-src/tests/test_bundle033.py
Star / oneworld の両方で、券の高さ・アニメの有無・画面の変化(3.6秒間に画面が何通りか)・DOMの書き換えを見る。実機は未確認。"""
import os, sys, json, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
STATE = {"v": 1, "trip": 1, "tk": "ow", "day": 1, "td": 1, "ph": "day", "bun": 1,
         "legs": [{"i": i, "fr": "", "to": "", "d": None, "f": 0, "l": 0, "dt": ""} for i in range(13)], "days": [], "cur": {"led": [], "pick": []}}
OBS = """()=>{window.__m={mut:0};new MutationObserver(function(ms){window.__m.mut+=ms.length}).observe(document.body,{childList:true,subtree:true,characterData:true,attributes:true});return 1}"""
UA = 'Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36'
bad = 0
with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(args=['--no-sandbox'])
    for tk in ('star', 'ow'):
        ctx = br.new_context(viewport={'width': 412, 'height': 780}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=UA)
        ctx.add_init_script(INIT)
        ctx.add_init_script("try{localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));localStorage.setItem('kanpe-trip-v1',%s);localStorage.setItem('kanpe-tour-save-v1',JSON.stringify({ticket:'%s'}))}catch(e){}" % (json.dumps(json.dumps(dict(STATE, tk=tk))), tk))
        p = ctx.new_page(); errs = []; p.on('pageerror', lambda e: errs.append(str(e)[:160]))
        p.goto(base + '/world/?map=1'); p.wait_for_timeout(1500)
        p.evaluate(OBS); p.tap('#mBundle'); p.wait_for_timeout(400)
        m0 = p.evaluate("()=>window.__m.mut"); hs = set()
        for i in range(30):
            hs.add(hashlib.md5(p.screenshot(clip={'x': 0, 'y': 150, 'width': 412, 'height': 300})).hexdigest()); p.wait_for_timeout(120)
        r = p.evaluate("()=>{var t=document.querySelector('.tp'),b=t.getBoundingClientRect();return {h:Math.round(b.height),anim:getComputedStyle(t).animationName,txt:document.querySelector('.trip-ov').innerText.replace(/\\s+/g,' '),ov:document.querySelectorAll('.trip-ov').length,mut:window.__m.mut}}")
        ok = r['h'] >= 120 and r['anim'] == 'none' and r['ov'] == 1 and r['mut'] == m0 and 'Landed 0 / 13' in r['txt'] and 'FLIGHT 1 / 13' in r['txt'] and not errs
        print(tk, 'OK' if ok else 'NG', '券の高さ', r['h'], 'アニメ', r['anim'], '画面の変化(通り)', len(hs), 'DOM書き換え', r['mut'] - m0, '|', r['txt'], errs)
        bad += 0 if ok else 1
        ctx.close()
sys.exit(1 if bad else 0)
