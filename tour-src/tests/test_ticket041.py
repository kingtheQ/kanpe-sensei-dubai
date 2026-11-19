# -*- coding: utf-8 -*-
"""タスク041 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_ticket041.py
(1)窓口の全場面(宣言・同意・聞き取り5本・線を引く・おすすめ・値段・読み上げ・名前・搭乗券)が新しい絵で出る
(2)足と影は動かず、上半身だけ揺れる (3)線を引く会話で、航路が会話の進行に合わせて1区間ずつ増える
(4)アニメが描けないとき、航路入りの静止画に落ち、会話は止まらない。リポジトリの生成物(tour/)は書き換えない。マイク・実機の見え方は確認できない。"""
import os, sys, json, time, base64, io, threading, http.server, socketserver
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,winStart:winStart,startVid:startVid,PBY:PBY,DLG:DLG,OUT:OUT,onPass:onPass};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "try{speechSynthesis.speak=function(u){setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}))")
def grab(p):
    d = p.evaluate("()=>document.getElementById('sceneA').toDataURL('image/png')")
    return np.array(Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB')).astype(int)
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
def start(p, step, vid=None):
    p.evaluate("([s,v])=>{var T=window.__T;T.save.win={step:s,m:{},cont:5,pick:'ow'};if(v)T.startVid(T.PBY.ticket,v,'win');else T.winStart()}", [step, vid])
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
BGN = np.array(Image.open(os.path.join(ROOT, 'tour/assets/art/ticket-office-bg-clean-noroute.png')).convert('RGB')).astype(int)
BGR = np.array(Image.open(os.path.join(ROOT, 'tour/assets/art/ticket-office-bg-clean.png')).convert('RGB')).astype(int)
MAP = (slice(92, 415), slice(342, 1198))   # 係員の頭が重なる地図の下端(415より下)は比べない
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
    p = ctx.new_page(); p.route('**/tour/index.html', hooked); p.goto(base + '/tour/index.html'); p.wait_for_timeout(2000)
    # (1) 全場面
    vids = ['win_decl', 'win_c1', 'win_c2', 'win_c5', 'win_c7', 'win_c8', 'win_route', 'win_price_star', 'win_price_ow5', 'win_price_ow4',
            'win_rb_star', 'win_rb_ow5', 'win_rb_ow4', 'win_name', 'ticket_star', 'ticket_ow']
    for v in vids:
        start(p, 0, v); p.wait_for_timeout(900)
        r = p.evaluate("()=>({bg:__T.G.scene.d.bg,hid:document.getElementById('sceneA').hidden,err:window.__errs.length})")
        chk('場面 %s: 新しい絵(bg=%s)' % (v, r['bg']), r['bg'] in ('tdesk', 'rtmap') and not r['hid'] and r['err'] == 0)
    start(p, 0); p.wait_for_timeout(1200)   # 宣言(同意の1枚が先に出ることもある)
    r = p.evaluate("()=>({v:__T.G.scene&&__T.G.scene.vid,hid:document.getElementById('sceneA').hidden,err:window.__errs})")
    chk('窓口のはじめ(%s)も新しい絵' % r['v'], not r['hid'] and not r['err'], r['err'])
    # (2) 足と影は固定・上半身は揺れる
    start(p, 1, 'win_c1'); p.wait_for_timeout(1200)
    fr = []
    for i in range(24): fr.append(grab(p)); p.wait_for_timeout(100)
    def nchg(box):
        y0, y1, x0, x1 = box; s = set(f[y0:y1, x0:x1].tobytes() for f in fr); return len(s)
    chk('キング: 足もと・影 24回中 変化 %d種' % nchg((860, 940, 750, 920)), nchg((860, 940, 750, 920)) == 1)
    chk('ルル: 足もと・影 変化 %d種' % nchg((860, 940, 620, 780)), nchg((860, 940, 620, 780)) == 1)
    chk('キング: 上半身 変化 %d種' % nchg((692, 780, 770, 900)), nchg((692, 780, 770, 900)) >= 2)
    chk('係員: カウンター際(下) 変化 %d種' % nchg((560, 594, 700, 840)), nchg((560, 594, 700, 840)) == 1)
    chk('係員: 頭 変化 %d種' % nchg((420, 470, 730, 810)), nchg((420, 470, 730, 810)) >= 2)
    chk('背景の航路なし(地図が背景と同じ)', int(np.abs(fr[0][MAP] - BGN[MAP]).sum() > 0) == 0 or float((np.abs(fr[0][MAP] - BGN[MAP]).sum(axis=2) > 0).mean()) < 0.001)
    # (3) 線を引く: 1区間ずつ
    start(p, 6, 'win_route'); marks = []
    for k in range(3):
        p.wait_for_timeout(300); s0 = grab(p); p.wait_for_timeout(1000); s1 = grab(p); p.wait_for_timeout(3500); s2 = grab(p)
        info = p.evaluate("()=>({ph:__T.G.phase,ti:__T.G.ti,rf:__T.G.scene.rf,rn:__T.G.scene.rn})")
        def px(a): return int((np.abs(a[MAP] - BGN[MAP]).sum(axis=2) > 40).sum())
        marks.append((px(s0), px(s1), px(s2)))
        print('   turn', k, info, '航路の画素(0.3秒/1.3秒/4.8秒):', marks[-1])
        chk('ターン%d: 会話は止まらず進行中(phase=%s)' % (k, info['ph']), info['ph'] in ('cue', 'cuing', 'listen', 'npc', 'rep'))
        p.evaluate("()=>__T.onPass()")
    chk('航路は区間ごとに増える', marks[0][2] > marks[0][0] and marks[1][2] > marks[0][2] and marks[2][2] >= marks[1][2] * 0.85)
    # (4) 描けない → 静止画
    p2 = ctx.new_page(); p2.add_init_script("window.__artRouteBreak=1"); p2.route('**/tour/index.html', hooked); p2.goto(base + '/tour/index.html'); p2.wait_for_timeout(2000)
    start(p2, 6, 'win_route'); p2.wait_for_timeout(2500)
    f = grab(p2); d = float((np.abs(f[MAP] - BGR[MAP]).sum(axis=2) > 0).mean())
    ph = p2.evaluate("()=>__T.G.phase"); chk('描けないとき: 航路入りの静止画(地図の違い %.4f)' % d, d < 0.01 and ph in ('cue', 'cuing', 'listen', 'npc', 'rep'), ph)
    p2.evaluate("()=>__T.onPass()"); p2.wait_for_timeout(1500)
    chk('描けなくても会話は次へ進む(ti=%s)' % p2.evaluate("()=>__T.G.ti"), p2.evaluate("()=>__T.G.ti") == 1)
    chk('JSエラー 0', not p.evaluate("()=>window.__errs"), p.evaluate("()=>window.__errs"))
    br.close()
print('結果:', 'すべてOK' if not bad else 'NG=' + str(bad)); sys.exit(1 if bad else 0)
