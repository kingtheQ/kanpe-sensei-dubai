# -*- coding: utf-8 -*-
"""タスク064 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_doha064.py [--shots DIR]
(1) 素材の寸法 (2) 3場面(doh_immig1 / doh_immig2 / doh_dep_passport)で背景が実画・art id が dimmig/dimmig2・エラーなし
(3) 係官3人が正本プレビューと同じ画素(×0.93・top=511・clip=600。窓口の台の下は描かない) (4) 表示灯が1秒ごとに2コマで切り替わる
(5) 本編側・ドーハ側の artIdFor がドーハ以外の同名 bg(ナイロビの immig・羽田・vid が doh_ でない dimmig)に影響しない
マイク・実機の見え方は確認できない。"""
import os, sys, io, base64, threading, http.server, socketserver, re
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART = os.path.join(ROOT, 'tour/assets/art')
ZIPDIR = os.environ.get('DOHA064_PREVIEW', '')
SHOTS = sys.argv[sys.argv.index('--shots') + 1] if '--shots' in sys.argv else None
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,PBY:PBY,startVid:startVid,ART:ART,artIdFor:artIdFor,ARTFAIL:ARTFAIL,gt:function(){return t}};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "try{speechSynthesis.speak=function(u){setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));")
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
def snap(p):
    d = p.evaluate("()=>document.getElementById('sceneA').toDataURL('image/png')")
    return Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB')
bgim = Image.open(os.path.join(ART, 'doha-immigration-v1.png')).convert('RGB')
strip = Image.open(os.path.join(ART, 'doha-immigration-lights-strip.png')).convert('RGBA')
chk('素材 背景 1536x960', bgim.size == (1536, 960), bgim.size); chk('素材 表示灯 3072x64(2コマ)', strip.size == (3072, 64), strip.size)
off = Image.open(os.path.join(ART, 'npc/o-front-officer-blue.png')).convert('RGBA')
ow, oh = off.size; dw, dh = round(ow * .93), -(-oh * 93 // 100)
chk('係官の表示寸法 51x127(55x136 を ×0.93。高さは切り上げ)', (dw, dh) == (51, 127), (dw, dh))
with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(args=['--no-sandbox'])
    for vid, aid in [('doh_immig1', 'dimmig'), ('doh_immig2', 'dimmig2'), ('doh_dep_passport', 'dimmig')]:
        ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
        pg = ctx.new_page(); pg.route(re.compile(r'.*/tour/doha/index\.html.*'), hooked); pg.goto(base + '/tour/doha/index.html?ev=all'); pg.wait_for_timeout(1200); pg.mouse.click(215, 450); pg.wait_for_timeout(600)
        pg.evaluate("(v)=>{var T=window.__T;var pl=null;for(var k in T.PBY){if(T.PBY[k].v&&T.PBY[k].v.indexOf(v)>=0)pl=k}T.startVid(T.PBY[pl],v,'ev')}", vid)
        pg.wait_for_timeout(7000)
        r = pg.evaluate("()=>({id:__T.artIdFor(__T.G.scene),vid:__T.G.scene.vid,bg:__T.G.scene.d.bg,fail:JSON.stringify(__T.ARTFAIL),err:window.__errs.length,hidden:document.getElementById('sceneA').hidden})")
        chk('%s: art id %s・絵の読み込み失敗なし・エラーなし・sceneA 表示' % (vid, aid), r['id'] == aid and r['fail'] == '{}' and r['err'] == 0 and not r['hidden'], r)
        im = snap(pg)
        if SHOTS: os.makedirs(SHOTS, exist_ok=True); im.save(os.path.join(SHOTS, vid + '.png'))
        a = np.array(im).astype(int); b = np.array(bgim).astype(int)
        bt = b.copy()   # ガラスの薄い色(190,215,226 を 22%)を重ねた背景
        for gx in (128, 576, 1024): bt[380:600, gx:gx + 385] = np.rint(b[380:600, gx:gx + 385] * .78 + np.array([190, 215, 226]) * .22)
        # 係官の窓口: 窓口の台(y>=600)より下は背景のまま
        for x in (320, 768, 1216):
            lo = a[600:660, x - 40:x + 40]; ref = b[600:660, x - 40:x + 40]
            chk('%s: 窓口x%d 台の下(y600〜660)は背景のまま' % (vid, x), (lo == ref).all())
            hd = a[511:600, x - 26:x + 26]; rf = bt[511:600, x - 26:x + 26]
            chk('%s: 窓口x%d 頭と肩(y511〜600)が描かれている' % (vid, x), (hd != rf).any(axis=2).mean() > .15, round(float((hd != rf).any(axis=2).mean()), 3))
            above = a[490:508, x - 30:x + 30]; refa = bt[490:508, x - 30:x + 30]
            chk('%s: 窓口x%d 頭の上(y490〜508)は背景+ガラスの色のまま(±1)' % (vid, x), (np.abs(above - refa) <= 1).all())
        # 表示灯: 1秒ごとに切り替わる
        seen = []
        for _ in range(6):
            s = snap(pg).crop((300, 312, 340, 330)); seen.append(tuple(np.array(s).reshape(-1, 3).mean(axis=0).round()))
            pg.wait_for_timeout(1000)
        chk('%s: 表示灯が2状態で切り替わる' % vid, len(set(seen)) == 2, seen)
        ctx.close()
    # 同名 bg への影響なし
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
    pg = ctx.new_page(); pg.route(re.compile(r'.*/tour/doha/index\.html.*'), hooked); pg.goto(base + '/tour/doha/index.html'); pg.wait_for_timeout(1000)
    d = pg.evaluate("()=>{var f=__T.artIdFor;return [f({vid:'doh_city_h1',d:{bg:'x'}}),f({vid:'doh_immig1',d:{bg:'dimmig'}}),f({vid:'doh_immig2',d:{bg:'dimmig'}}),f({vid:'doh_dep_passport',d:{bg:'dimmig'}}),f({vid:'nbo_immig1',d:{bg:'immig'}}),f({vid:'doh_x',d:{bg:'immig'}}),f({vid:'hnd_exit',d:{bg:'dimmig'}}),f({vid:'doh_bag1',d:{bg:'dbag'}})]}")
    chk('ドーハ側 artIdFor', d == ['hotel', 'dimmig', 'dimmig2', 'dimmig', None, None, None, None], d)
    ctx.close()
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
    pg = ctx.new_page(); pg.route('**/tour/index.html', hooked); pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1000)
    m = pg.evaluate("()=>{var f=__T.artIdFor;return [f({vid:'nbo_immig1',d:{bg:'immig'}}),f({vid:'doh_immig1',d:{bg:'dimmig'}}),f({vid:'doh_immig2',d:{bg:'dimmig'}}),f({vid:'doh_dep_passport',d:{bg:'dimmig'}}),f({vid:'nbo_x',d:{bg:'dimmig'}}),f({vid:'hnd_exit',d:{bg:'immigH'}}),f({vid:'doh_x',d:{bg:'immig'}}),f({vid:'nbo_taxi1',d:{bg:'taxi'}})]}")
    chk('本編側 artIdFor', m == ['immig', 'dimmig', 'dimmig2', 'dimmig', None, 'hexit', 'immig', 'nairobi'], m)   # タスク067: 羽田の出国審査(hnd_exit・bg immigH)は実画 hexit に結んだ(ドーハの dimmig・ナイロビの immig は変わらない)
    ctx.close(); br.close()
print('NG: %d' % len(bad) if bad else 'ALL OK'); sys.exit(1 if bad else 0)
