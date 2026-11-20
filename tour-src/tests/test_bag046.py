# -*- coding: utf-8 -*-
"""タスク046 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_bag046.py
(1)荷物受け取り(nbo_bag1)が新しい会話文(5往復・旅行者)になっている (2)入国審査→荷物受け取り→SIM の順は変わらない・場面の数も同じ
(3)旅行者の声 pitch=1.0 が読み上げに使われる (4)専用スーツケース(青+黄タグ)がベルトに見え、3番目の台詞(緑の板のとなりの青いの)のあいだ板のとなりにいる
(5)4番目の台詞で取ったあと・荷物を受け取ったあとの場面(nbo_bag2)ではベルトから消える (6)雨もりの出来事は従来どおり起きて、ベルトが止まり、そのあとの会話の1行目が雨もりを受ける
マイク・実機の見え方・音は確認できない。"""
import os, sys, math, json, threading, http.server, socketserver
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
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,startVid:startVid,PBY:PBY,DLG:DLG,SP:SP,gt:function(){return t}};" + HOOK, 1))
INIT = ("window.__errs=[];window.__pitch=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "try{speechSynthesis.speak=function(u){window.__pitch.push([u.text,u.pitch]);setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));"
        "window.__fr=[];(function(){var o=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.drawImage=function(im){"
        "try{var s=im&&im.src||'';if(this.canvas&&this.canvas.id==='sceneA'){var a=arguments;"
        "if(s.indexOf('nairobi-baggage-base.png')>=0){window.__fr.push({te:window.__T?window.__T.gt():0,c:[]});if(window.__fr.length>4000)window.__fr.shift()}"
        "else if(s.indexOf('nairobi-baggage-bags.png')>=0&&window.__fr.length)window.__fr[window.__fr.length-1].c.push(['b',a[1]/112,a[2]/104,a[5],a[6]]);"
        "else if(s.indexOf('nairobi-baggage-island.png')>=0&&window.__fr.length)window.__fr[window.__fr.length-1].c.push(['i',a[1],a[2]])}}catch(e){}"
        "return o.apply(this,arguments)}})()")
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
# 緑の板の外わく(島の画像の緑の画素から。2倍の座標)
isl = np.array(Image.open(os.path.join(ROOT, 'tour/assets/art/nairobi-baggage-island.png')).convert('RGBA'))
gy, gx = np.where((isl[:, :, 0] == 30) & (isl[:, :, 1] == 110) & (isl[:, :, 2] == 76))
BX0, BX1, BY0, BY1 = gx.min() + 552, gx.max() + 552, gy.min() + 602, gy.max() + 602
def hero(p, secs=0.6):
    p.evaluate("()=>{window.__fr.length=0}"); p.wait_for_timeout(int(secs * 1000))
    fr = [f for f in p.evaluate("()=>window.__fr.slice()") if f['c']]
    out = []
    for f in fr:
        bs = [c for c in f['c'] if c[0] == 'b']; hs = [c for c in bs if c[2] == 1]
        out.append((len(bs), [(c[3] + 56, c[4] + 92, c[1]) for c in hs]))
    return out
import base64
def snap(p, path):   # 場面の絵(canvas)をそのまま保存(画面の上に重なる表示に隠れないように)
    d = p.evaluate("()=>document.getElementById('sceneA').toDataURL('image/png')")
    open(path, 'wb').write(base64.b64decode(d.split(',')[1]))
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
gen0 = open(os.path.join(ROOT, 'tour/index.html'), 'rb').read()
def start(p, vid): p.evaluate("(v)=>{var T=window.__T;T.startVid(T.PBY.bag,v,'ev')}", vid)
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
    p = ctx.new_page(); p.route('**/tour/index.html', hooked); p.goto(base + '/tour/index.html'); p.wait_for_timeout(1800)
    # (1) 会話文
    d = p.evaluate("()=>{var d=__T.DLG.nbo_bag1;return {who:d.who,sp:d.sp,bg:d.bg,n:d.lines.filter(function(l){return l.n}).length,l2:d.lines.filter(function(l){return l.n})[2].n,w:d.words.map(function(w){return w[0]})}}")
    print(d)
    chk('nbo_bag1 は旅行者との5往復・背景baggage', d['sp'] == 'traveler' and d['n'] == 5 and d['bg'] == 'baggage' and '旅行者' in d['who'], d)
    chk('3番目の台詞に「緑の板のとなりの青いの」', 'next to the green board' in d['l2'])
    chk('単語5つ(belt/suitcase/tag/heavy/help)', d['w'] == ['belt', 'suitcase', 'tag', 'heavy', 'help'], d['w'])
    # (2) 並び(入国審査→荷物受取→SIM)と場面の数
    arr = p.evaluate("()=>{var g=null;try{g=__T.PBY}catch(e){}return Object.keys(g||{})}")
    src = open(os.path.join(ROOT, 'tour-src/trip.js'), encoding='utf-8').read()
    chk("trip.js の割り当て表は 入国審査→荷物受取→SIM→タクシー の4場面のまま", "nbo_arr:[['nbo_immig1','nbo_immig2'],['nbo_bag1','nbo_bag2'],['nbo_sim1','nbo_sim2'],['nbo_taxi1','nbo_taxi2']]" in src)
    chk('場所の並び(build.py)の bag は nbo_bag1, nbo_bag2 のまま', "['nbo_bag1', 'nbo_bag2']" in open(os.path.join(ROOT, 'tour-src/build.py'), encoding='utf-8').read())
    # (3) 声と見た目
    start(p, 'nbo_bag1'); p.wait_for_timeout(1500)
    r = p.evaluate("()=>({tp:__T.G.scene.turns.map(function(T){return T.pitch}),sp:!!__T.SP.traveler,pp:__T.SP.traveler&&__T.SP.traveler.pitch,err:window.__errs.length})")
    chk('旅行者の声 pitch=1.0(全ターンに反映)', r['pp'] == 1 and r['tp'] == [1] * 5 and r['err'] == 0, r)
    p.evaluate("()=>{var b=document.querySelector('button.go');if(b)b.click()}"); p.wait_for_timeout(2500)
    ps = p.evaluate("()=>window.__pitch.filter(function(x){return /Tokyo/.test(x[0])})")
    chk('読み上げの pitch(Tokyoの台詞)', len(ps) >= 1 and all(abs(x[1] - 1.0) < 1e-6 for x in ps), ps[:3])
    sps = p.evaluate("()=>({a:JSON.stringify(__T.SP.traveler.m),o:['bag_staff2','ev_wet','ev_trav3','ev_ribbon','sim_staff','sim_staff2','taxi_staff','officer','officer2'].map(function(k){return JSON.stringify(__T.SP[k].m)}),pit:['bag_staff2','ev_wet','sim_staff','sim_staff2','taxi_staff','officer','officer2'].map(function(k){return __T.SP[k].pitch})})")
    chk('見た目の定義がある(ナイロビ到着の係員・雨もりの旅行者などの見た目とは別)', sps['a'] and sps['a'] not in sps['o'])
    chk('声が係員・ルル(1.35)と被らない', 1 not in sps['pit'], sps['pit'])
    # (4) 専用スーツケース: 台詞 0,1 では動いて見える。台詞2(3番目)で緑の板のとなり。
    h0 = hero(p, 0.8)
    chk('ベルト上に荷物6個(うち専用1個)', all(n == 6 for n, h in h0) and all(len(h) == 1 for n, h in h0), len(h0))
    snap(p, '/tmp/t046_line0.png')
    p.evaluate("()=>{__T.G.ti=2}"); p.wait_for_timeout(2500)
    ok = 0; xs = []; tot = 0
    for k in range(5):
        h = hero(p, 0.5)
        for n, hh in h:
            tot += 1
            if n == 6 and len(hh) == 1:
                X, Y, lv = hh[0]; xs.append(X)
                # 板のとなり: 板の右端より右、すぐ(150画素=2倍の座標)以内。手前の縁(y が板より下)。専用の絵(行1)の手前の段階
                if BX1 - 40 < X - 33 and X - 33 < BX1 + 110 and Y > BY1 and lv >= 9: ok += 1
    chk('3番目の台詞のあいだ、専用スーツケースは緑の板のとなり(板の右端 %d の -40〜+110 画素)' % BX1, tot > 40 and ok == tot, '%d/%d x=%s..%s' % (ok, tot, min(xs), max(xs)))
    snap(p, '/tmp/t046_line2.png')
    p.evaluate("()=>{__T.G.ti=3}"); p.wait_for_timeout(600)
    h = hero(p, 0.5)
    chk('4番目の台詞(重いですよ)のあいだもベルト上にある', all(n == 6 and len(hh) == 1 for n, hh in h) and len(h) > 5)
    p.evaluate("()=>{__T.G.ti=4}"); p.wait_for_timeout(600)
    h = hero(p, 0.5)
    chk('5番目の台詞(取れました!のあと)では専用スーツケースがベルトから消える(荷物5個)', all(n == 5 and len(hh) == 0 for n, hh in h) and len(h) > 5, (len(h), set((n, len(hh)) for n, hh in h)))
    snap(p, '/tmp/t046_line4.png')
    # (5) 荷物を受け取ったあとの場面
    start(p, 'nbo_bag2'); p.wait_for_timeout(1200)
    h = hero(p, 0.5)
    chk('nbo_bag2(受け取ったあと)では専用スーツケースは出ない(荷物5個)', all(n == 5 and len(hh) == 0 for n, hh in h) and len(h) > 5)
    # (6) 雨もり
    start(p, 'nbo_ev_b_leak'); p.wait_for_timeout(1200)
    h = hero(p, 1.5)
    pos = {tuple(hh) for n, hh in h}
    chk('雨もりの出来事: ベルトが止まる・専用スーツケースも止まって見える(6個)', len(h) > 30 and len(pos) == 1 and all(n == 6 for n, hh in h), (len(h), len(pos)))
    snap(p, '/tmp/t046_leak.png')
    # 雨もりを遊んだあとの nbo_bag1 の1行目が雨もりを受ける(VARIANTS)
    sv = p.evaluate("()=>{var T=__T;T.save.seen=T.save.seen||{};T.save.seen['nbo_ev_b_leak']=1;return 1}")
    start(p, 'nbo_bag1'); p.wait_for_timeout(1200); p.evaluate("()=>{var b=document.querySelector('button.go');if(b)b.click()}"); p.wait_for_timeout(1500)
    t0 = p.evaluate("()=>{var S=__T.G.scene;return S.turns[0].npc}")
    chk('雨もりを遊んだあとは、1行目が雨もりを受ける', 'rain' in t0 and 'Tokyo' in t0, t0)
    chk('エラーなし', p.evaluate("()=>window.__errs.length") == 0, p.evaluate("()=>window.__errs"))
    br.close()
chk('tour/index.html を書き換えていない', open(os.path.join(ROOT, 'tour/index.html'), 'rb').read() == gen0)
print('NG', bad) if bad else print('すべてOK')
sys.exit(1 if bad else 0)
