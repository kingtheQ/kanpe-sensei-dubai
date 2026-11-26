# -*- coding: utf-8 -*-
"""タスク070 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_corniche070.py [--shots DIR]
(1)ドーハの4場面(doh_city_c1/c2/c3・doh_ev_j_ask)で art id dcorn・背景が doha-corniche-v1.png(画素が素材と一致)
(2)ダウ舟: 2コマが0.8秒ごと・(700,258) / 水面のきらめき: 4コマが0.5秒ごと・(0,372)。キャンバスの画素が strip のコマと一致
(3)舟が二重に出ない: 実画の表示中は ドット描画のキャンバス(#scene)が隠れ、実画のキャンバス(#sceneA)だけが見える
(4)ふたりの足もと: ルル x=1060・キング x=1180・足もと y=884(止まったあとの描画が、素材のスプライトと一致)
(5)結び: ドーハ側 artIdFor は 4場面だけ dcorn・doh_city_h1 は hotel のまま・ほかの場面は null。ナイロビ側 artIdFor は dcorn を返さない
(6)実画が読めないときは ドット描画(BGS.ccorn)に落ちる(真っ暗にならない)・舟の二重表示なし
(7)台詞: 4場面の台詞は、このタスクの前(git HEAD)から変わらない  (8)?check=1 から4場面を始められ、実画が出る
(9)素材の大きさ。絵に文字を描いていないことは、素材の指定(文字なし)と shots の目視で確認する
マイク・実機の見え方は確認できない。"""
import os, sys, io, json, base64, threading, http.server, socketserver, subprocess, re
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART = os.path.join(ROOT, 'tour/assets/art')
SHOTS = sys.argv[sys.argv.index('--shots') + 1] if '--shots' in sys.argv else None
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv
HOOK = "requestAnimationFrame(frame);\n})();"
EXPOSE = ("window.__T={G:G,save:save,PBY:PBY,setMode:setMode,startVid:startVid,ART:ART,artIdFor:artIdFor,ARTFAIL:ARTFAIL,"
          "gt:function(){return t},TOURDLG:TOURDLG};")
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, EXPOSE + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "window.__say=[];try{speechSynthesis.speak=function(u){window.__say.push(u.text);setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));")
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
def boot(br, url='/tour/doha/index.html', route='**/tour/doha/index.html'):
    ctx = br.new_context(viewport={'width': 430, 'height': 900}, device_scale_factor=1)
    pg = ctx.new_page(); pg.add_init_script(INIT); pg.route(route, hooked)
    pg.goto(base + url); pg.wait_for_timeout(1200); pg.mouse.click(215, 450); pg.wait_for_timeout(800); return pg
def snap(p):
    d = p.evaluate("()=>document.getElementById('sceneA').toDataURL('image/png')")
    return np.array(Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB')).astype(int)
def img(n): return Image.open(os.path.join(ART, n)).convert('RGBA')
def rgb(n): return np.array(img(n).convert('RGB')).astype(int)
def play(p, vid):
    p.evaluate("(v)=>{var T=window.__T;T.startVid(T.PBY.ccorn,v,'ev')}", vid)
VIDS = ['doh_city_c1', 'doh_city_c2', 'doh_city_c3', 'doh_ev_j_ask']
bg = rgb('doha-corniche-v1.png'); dh = img('doha-corniche-dhow-strip.png'); sp = img('doha-corniche-sparkle-strip.png')
def frame_of(strip, i, fw, fh): return strip.crop((i * fw, 0, (i + 1) * fw, fh))
def region_match(snapA, x, y, fr):
    """ダウ舟のコマ fr(RGBA)の不透明な画素が、キャンバスの同じ位置と一致する割合"""
    a = np.array(fr); h, w = a.shape[:2]; m = a[:, :, 3] > 250
    if not m.any(): return 0.0
    cv = snapA[y:y + h, x:x + w]; exp = a[:, :, :3].astype(int)
    return float((cv[m] == exp[m]).all(axis=1).mean())
def blend_match(snapA, i):
    """きらめき(半透明の画素を含む)のコマ i を背景に重ねた期待画素と、キャンバス左半分(舟・人物と重ならない x0..690・y372..564)を比べる(±2)"""
    fr = np.array(frame_of(sp, i, 1536, 192)).astype(float)[:, :690]; al = fr[:, :, 3:4] / 255.
    exp = fr[:, :, :3] * al + bg[372:564, :690] * (1 - al)
    return float((np.abs(snapA[372:564, :690] - exp).max(axis=2) <= 2).mean())
with sync_playwright() as pw:
    br = pw.chromium.launch()
    # ---- (5) 結び ----
    pg = boot(br)
    r = pg.evaluate("()=>{var T=window.__T,f=T.artIdFor,o={};['doh_city_c1','doh_city_c2','doh_city_c3','doh_ev_j_ask','doh_city_h1','doh_city_t1','doh_city_s1','doh_city_b1','doh_immig1'].forEach(function(v){o[v]=f({vid:v})});o.none=f(null);return o}")
    chk('ドーハ側 artIdFor: 4場面は dcorn', all(r[v] == 'dcorn' for v in VIDS), {v: r[v] for v in VIDS})
    chk('ドーハ側 artIdFor: doh_city_h1 は hotel のまま', r['doh_city_h1'] == 'hotel', r['doh_city_h1'])
    SOUQ = ['doh_city_t1', 'doh_city_s1']   # タスク071 で スークの路地(dalley)・広場(dsouq)に結んだ場面。その結びは test_souq071.py が確かめる
    chk('ドーハ側 artIdFor: ほかの場面は null(スーク071の2場面は除く)', all(r[k] is None for k in r if k not in VIDS + ['doh_city_h1'] + SOUQ), {k: r[k] for k in r if k not in VIDS + ['doh_city_h1'] + SOUQ})
    chk('ドーハ側 artIdFor: スーク(071)の t1=dalley・s1=dsouq', (r['doh_city_t1'], r['doh_city_s1']) == ('dalley', 'dsouq'), (r['doh_city_t1'], r['doh_city_s1']))
    cf = pg.evaluate("()=>window.__T.ART.dcorn")
    chk('ART dcorn の置き場', cf['base'] == 884 and cf['lulu'] == 1060 and cf['king'] == 1180 and cf['mode'] == 'wide', {k: cf[k] for k in ('mode', 'base', 'lulu', 'king', 'dir')})
    chk('strips が指定どおり', cf['strips'] == [
        {'img': 'doha-corniche-sparkle-strip.png', 'x': 0, 'y': 372, 'n': 4, 'fw': 1536, 'fh': 192, 'step': .5},
        {'img': 'doha-corniche-dhow-strip.png', 'x': 700, 'y': 258, 'n': 2, 'fw': 512, 'fh': 256, 'step': .8}], cf['strips'])
    chk('doha: ページの異常なし(起動)', pg.evaluate("window.__errs") == [], pg.evaluate("window.__errs"))
    # ---- (1)(2)(3) 各場面 ----
    for vid in VIDS:
        play(pg, vid); pg.wait_for_timeout(3200)
        info = pg.evaluate("()=>{var T=window.__T,S=T.G.scene;return {id:T.artIdFor(S),hid:document.getElementById('scene').hidden,hidA:document.getElementById('sceneA').hidden,fail:!!T.ARTFAIL.dcorn}}")
        chk('%s: art id dcorn・実画のキャンバスだけ表示(ドット描画は隠れる=舟の二重なし)' % vid, info['id'] == 'dcorn' and info['hid'] and not info['hidA'] and not info['fail'], info)
        got = {'d': set(), 's': set()}
        for _ in range(26):
            s = snap(pg)
            dm = [region_match(s, 700, 258, frame_of(dh, i, 512, 256)) for i in range(2)]
            sm = [blend_match(s, i) for i in range(4)]
            got['d'].add(int(np.argmax(dm)) if max(dm) > .97 else -1); got['s'].add(int(np.argmax(sm)) if max(sm) > .97 else -1)
            pg.wait_for_timeout(137)
        chk('%s: ダウ舟の2コマが両方出る(その場で揺れる)' % vid, {0, 1} <= got['d'], sorted(got['d']))
        chk('%s: 水面のきらめき4コマが出る' % vid, {0, 1, 2, 3} <= got['s'], sorted(got['s']))
        s = snap(pg)
        ok = float((s[640:880, 0:1000] == bg[640:880, 0:1000]).all(axis=2).mean())
        chk('%s: 背景が doha-corniche-v1.png(舗道の画素が素材と一致)' % vid, ok > .9, round(ok, 3))
        dock = float((s[470:560, 610:850] == bg[470:560, 610:850]).all(axis=2).mean())
        chk('%s: ドック(舟のいない足場)は背景のまま' % vid, dock > .6, round(dock, 3))
        if SHOTS:
            os.makedirs(SHOTS, exist_ok=True); Image.fromarray(s.astype('uint8')).save(os.path.join(SHOTS, 'doha-%s.png' % vid))
        chk('%s: ページの異常なし' % vid, pg.evaluate("window.__errs") == [], pg.evaluate("window.__errs"))
    # ---- (4) ふたり ----
    play(pg, 'doh_city_c1'); pg.wait_for_timeout(5200)
    s = snap(pg)
    def sprite_hit(name, cx, by):
        a = np.array(img('wide-' + name + '.png')); h, w = a.shape[:2]; m = a[:, :, 3] > 250
        best = 0
        for dy in (-4, 0):   # 立ち絵は小さく上下にゆれる
            x0 = int(round(cx - w / 2)); y0 = int(round(by - h)) + dy
            cvv = s[y0:y0 + h, x0:x0 + w]
            if cvv.shape[:2] != (h, w): continue
            best = max(best, float((cvv[m] == a[:, :, :3][m]).all(axis=1).mean()))
        return best
    ks = sprite_hit('king-idle', 1180, 884); ls = sprite_hit('lulu-idle', 1060, 884)
    chk('キングが x=1180・足もと y=884 に立つ', ks > .9, round(ks, 3))
    chk('ルルが x=1060・足もと y=884 に立つ(ルルが左・キングが右)', ls > .9, round(ls, 3))
    pg.context.close()
    # ---- (6) 実画が読めないときのフォールバック ----
    ctx = br.new_context(viewport={'width': 430, 'height': 900}, device_scale_factor=1)
    pf = ctx.new_page(); pf.add_init_script(INIT); pf.route('**/tour/doha/index.html', hooked)
    pf.route('**/doha-corniche-v1.png', lambda r: r.abort())
    pf.goto(base + '/tour/doha/index.html'); pf.wait_for_timeout(1200); pf.mouse.click(215, 450); pf.wait_for_timeout(800)
    play(pf, 'doh_city_c2'); pf.wait_for_timeout(3000)
    info = pf.evaluate("()=>({hid:document.getElementById('scene').hidden,hidA:document.getElementById('sceneA').hidden,fail:!!window.__T.ARTFAIL.dcorn})")
    chk('背景が読めない: ドット描画(BGS.ccorn)に落ちる・実画のキャンバスは出ない', info['fail'] and not info['hid'] and info['hidA'], info)
    ctx.close()
    # ---- ナイロビ側は dcorn を返さない ----
    pn = boot(br, '/tour/index.html', '**/tour/index.html')
    r = pn.evaluate("()=>{var f=window.__T.artIdFor,o={};['doh_city_c1','doh_city_c2','doh_city_c3','doh_ev_j_ask'].forEach(function(v){o[v]=f({vid:v})});return o}")
    chk('ナイロビ側 artIdFor は 4場面で dcorn を返さない(触っていない)', all(v is None for v in r.values()), r)
    pn.context.close()
    # ---- (8) チェックモード ----
    pc = boot(br, '/tour/doha/index.html?check=1', '**/tour/doha/index.html*')
    pc.wait_for_timeout(600); pc.click('#chkBtn'); pc.wait_for_timeout(400)
    names = pc.evaluate("()=>Array.prototype.map.call(document.querySelectorAll('#chkPan button'),function(b){return b.textContent})")
    chk('チェックモードに4場面の入口がある', all(v in names for v in VIDS), [v for v in VIDS if v not in names])
    for vid in VIDS:
        if vid != VIDS[0]: pc.click('#chkBtn'); pc.wait_for_timeout(300)
        btn = pc.locator('#chkPan button', has_text=re.compile('^' + vid + '$'))
        if btn.count() == 0: chk('check: ' + vid, False, 'ボタンなし'); continue
        btn.first.click(); pc.wait_for_timeout(3200)
        info = pc.evaluate("()=>({id:window.__T.artIdFor(window.__T.G.scene),hidA:document.getElementById('sceneA').hidden})")
        chk('?check=1 から %s を始める: 実画(dcorn)が出る' % vid, info['id'] == 'dcorn' and not info['hidA'], info)
    br.close()
# ---- (7) 台詞の不変 ----
def dlg_of(txt):
    m = re.search(r'var TOURDLG=(\{.*?\});\n', txt, re.S); d = json.loads(m.group(1)); return {v: d[v] for v in VIDS}
before = subprocess.run(['git', 'show', 'HEAD:tour/doha/index.html'], cwd=ROOT, capture_output=True, text=True).stdout
now = open(os.path.join(ROOT, 'tour/doha/index.html'), encoding='utf-8').read()
# タスク092(057 第3弾)で街の c1〜c3 は新形式に変換した。ここでは「この任務(コルニーシュの絵)で台詞を変えていない」ことを、
# 変換の前後で変わらないもの(words の5語・ターン数)と、変換していない doh_ev_j_ask の完全一致で確かめる
_b, _n = dlg_of(before), dlg_of(now)
chk('4場面の台詞・単語は変わっていない(c1〜c3 は words とターン数が同じ・doh_ev_j_ask は HEAD と同一)',
    all(_b[v]['words'] == _n[v]['words'] and len(_b[v]['lines']) == len(_n[v]['lines']) for v in VIDS[:3]) and _b['doh_ev_j_ask'] == _n['doh_ev_j_ask'])
chk('素材の大きさ(背景1536×960・舟1024×256・きらめき6144×192)', img('doha-corniche-v1.png').size == (1536, 960) and dh.size == (1024, 256) and sp.size == (6144, 192))
print('\nNG:', bad if bad else 'なし')
sys.exit(1 if bad else 0)
