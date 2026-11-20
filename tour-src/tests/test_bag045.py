# -*- coding: utf-8 -*-
"""タスク045 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_bag045.py
(1)ナイロビの手荷物受け取り(nbo_bag1/2)が新しい絵で出る (2)荷物6個が楕円の経路を動く(式との一致・手前は左→右・奥は右→左)
(3)1周の長さを「動いて見えた時間」から測る(約24秒) (4)描く順: 奥の荷物 → 島 → 手前の荷物 (5)雨もりの出来事ではベルトが止まる
(6)島や荷物の画像が読めないとき、古い絵に落ちて会話は止まらない (7)ドーハの手荷物は今までどおり。リポジトリの生成物(tour/)は書き換えない。
マイク・実機の見え方は確認できない。"""
import os, sys, math, json, time, io, base64, threading, http.server, socketserver
from playwright.sync_api import sync_playwright
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
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,startVid:startVid,PBY:PBY,DLG:DLG,gt:function(){return t}};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "try{speechSynthesis.speak=function(u){setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));"
        # 描画の記録: 背景の描き直し(=1コマの始まり)ごとに、荷物・島の drawImage を順に残す
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
CX, CY, RX, RY, N, LV = 400, 330, 178, 28, 6, 13
def expect(ph):   # 式(素材のスクリプトと同じ): ph=経過/周期 → [(sin, design, x, y, level)]
    o = []
    for i in range(N):
        th = i * math.tau / N - math.tau * ph; sn = math.sin(th)
        o.append((sn, i, 2 * round(CX + RX * math.cos(th)), 2 * round(CY + RY * sn), max(0, min(LV - 1, round((sn + 1) / 2 * (LV - 1))))))
    return o
def take(p, secs, tick=0.1):
    p.evaluate("()=>{window.__fr.length=0}"); t0 = time.time(); p.wait_for_timeout(int(secs * 1000))
    return p.evaluate("()=>window.__fr.slice()")
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
gen0 = open(os.path.join(ROOT, 'tour/index.html'), 'rb').read()
def start(p, vid):
    p.evaluate("(v)=>{var T=window.__T;T.startVid(T.PBY.bag,v,'ev')}", vid)
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
    p = ctx.new_page(); p.route('**/tour/index.html', hooked); p.goto(base + '/tour/index.html'); p.wait_for_timeout(1800)
    # (1) 場面
    for v in ('nbo_bag1', 'nbo_bag2'):
        start(p, v); p.wait_for_timeout(1500)
        r = p.evaluate("()=>({bg:__T.G.scene.d.bg,hid:document.getElementById('sceneA').hidden,err:window.__errs.length})")
        chk('場面 %s: 新しい絵(bg=%s)・エラーなし' % (v, r['bg']), r['bg'] == 'baggage' and not r['hid'] and r['err'] == 0)
    start(p, 'nbo_bag1'); p.wait_for_timeout(1200)
    p.screenshot(path='/tmp/t045_a.png')
    # (2)(4) 長く動かして記録する(26秒)
    fr = take(p, 26.5); fr = [f for f in fr if f['c']]
    chk('コマを記録', len(fr) > 200, len(fr))
    p.screenshot(path='/tmp/t045_b.png')
    t0 = fr[0]['te']
    # 経過 te は S.artT0 からの値。S.artT0 は場面の始まりなので、記録した te−t0 を位相の差に使い、位相の原点は荷物0番の位置から求める
    def decode(f):
        bs = [c for c in f['c'] if c[0] == 'b']; isl = [i for i, c in enumerate(f['c']) if c[0] == 'i']
        return bs, isl
    okcount = okorder = okell = 0; samples = []
    for f in fr:
        bs, isl = decode(f)
        if len(bs) != N or len(isl) != 1: continue
        okcount += 1
        # 描く順: 奥(sin<0)→島→手前。sin は y から逆算
        ys = [(c[4] - 330 * 2) / (RY * 2) for c in bs]   # 接地点 y=2*(cy+ry*sin)=ay下げ前。描画先の y は 接地y-92
        sins = [((c[4] + 92) / 2 - CY) / RY for c in bs]
        pos = f['c'].index(['i'] + [c for c in f['c'] if c[0] == 'i'][0][1:])
        before = [((c[4] + 92) / 2 - CY) / RY for c in f['c'][:pos] if c[0] == 'b']
        after = [((c[4] + 92) / 2 - CY) / RY for c in f['c'][pos + 1:] if c[0] == 'b']
        if all(s < 0.02 for s in before) and all(s > -0.02 for s in after) and before == sorted(before) and after == sorted(after) and len(before) + len(after) == N: okorder += 1
        for c in bs:
            X, Y = c[3] + 56, c[4] + 92   # 接地点(2倍の座標)
            e = ((X / 2 - CX) / RX) ** 2 + ((Y / 2 - CY) / RY) ** 2
            if abs(e - 1) < 0.08: okell += 1
        samples.append((f['te'], {int(round(c[2])): (c[3] + 56, c[4] + 92) for c in bs}, {int(round(c[2])): c[1] for c in bs}))
    chk('毎コマ 荷物6個＋島1つ', okcount == len(fr), '%d/%d' % (okcount, len(fr)))
    chk('描く順: 奥の荷物(奥の順) → 島 → 手前の荷物(奥の順)', okorder == okcount, '%d/%d' % (okorder, okcount))
    chk('接地点が楕円(rx=178,ry=28の2倍)の上', okell == okcount * N, '%d/%d' % (okell, okcount * N))
    # 大きさの段階: 手前ほど大きい(段階が上がる)
    lvl_front = max(c[1] for f in fr[:50] for c in f['c'] if c[0] == 'b'); lvl_min = min(c[1] for f in fr[:50] for c in f['c'] if c[0] == 'b')
    # (3) 1周の長さ: 種類2(赤)の経路を追って、最初の位置にもどるまでの te
    tr = [(s[0], s[1].get(0)) for s in samples]   # 注意: key は後で design で引く
    des = {}
    for f in fr:
        for c in f['c']:
            if c[0] == 'b' and int(round(c[2])) == 2: des.setdefault(id(f), (f['te'], c[3] + 56, c[4] + 92))
    path = sorted(des.values())
    x0, y0 = path[0][1], path[0][2]; te0 = path[0][0]
    back = [(te - te0) for (te, x, y) in path if te - te0 > 12 and abs(x - x0) <= 6 and abs(y - y0) <= 2]
    per = (min(back)) if back else None
    # 戻りの代表は、もどった区間の中央(最初の位置を通過する中心)
    if back:
        grp = [b for b in back if abs(b - min(back)) < 1.0]; per = sum(grp) / len(grp)
    chk('1周 約24秒(測定値)', per is not None and abs(per - 24.0) <= 0.35, 'per=%s' % (round(per, 2) if per else None))
    # 向き: 手前(y が大きいとき)は x が増える、奥は減る
    pm = [(te, x, y) for (te, x, y) in path]
    fw = bk = fa = ba = 0
    for (a, b) in zip(pm, pm[1:]):
        if b[0] - a[0] > .2 or b[1] == a[1]: continue
        if a[2] > 660 * 2 // 2 + 700: pass
        if a[2] > 2 * CY + 20: fa += 1; fw += b[1] > a[1]
        elif a[2] < 2 * CY - 20: ba += 1; bk += b[1] < a[1]
    chk('手前の縁では左→右・奥の縁では右→左', fa > 20 and ba > 20 and fw == fa and bk == ba, 'front %d/%d back %d/%d' % (fw, fa, bk, ba))
    # 式との一致(位相は荷物0番の最初の位置から決める)
    # (5) 雨もりの出来事ではベルトが止まる
    start(p, 'nbo_ev_b_leak'); p.wait_for_timeout(1200)
    s1 = take(p, 2.0); s1 = [f for f in s1 if f['c']]
    allpos = {tuple(sorted((c[3], c[4]) for c in f['c'] if c[0] == 'b')) for f in s1}
    chk('雨もり(nbo_ev_b_leak)ではベルトが止まる', len(s1) > 30 and len(allpos) == 1, 'コマ%d 位置の種類%d' % (len(s1), len(allpos)))
    p.screenshot(path='/tmp/t045_leak.png')
    # ふたりが描かれる・話すと「…」
    # (6) 画像が読めない
    p2 = ctx.new_page(); p2.route('**/tour/index.html', hooked); p2.route('**/nairobi-baggage-island.png', lambda r: r.abort()); p2.goto(base + '/tour/index.html'); p2.wait_for_timeout(1800)
    p2.evaluate("()=>{var T=window.__T;T.startVid(T.PBY.bag,'nbo_bag1','ev')}"); p2.wait_for_timeout(2500)
    r = p2.evaluate("()=>({hid:document.getElementById('sceneA').hidden,vid:__T.G.scene.vid,err:window.__errs.length,btn:document.querySelectorAll('button').length})")
    chk('島が読めないとき古い絵に落ち、場面は続く', r['hid'] is True and r['vid'] == 'nbo_bag1' and r['err'] == 0, r)
    p2.screenshot(path='/tmp/t045_fallback.png')
    # (7) ドーハの手荷物は今までどおり(新しい絵を使わない)
    p3 = ctx.new_page(); p3.route('**/tour/doha/index.html', lambda r: r.continue_()); p3.goto(base + '/tour/doha/index.html'); p3.wait_for_timeout(2000)
    r = p3.evaluate("()=>{var v=null;try{v=typeof artIdFor==='function'?artIdFor({d:{bg:'baggage'}}):'(none)'}catch(e){v='err'}return v}")
    chk('ドーハ側は荷物受取の新しい絵に結ばれない', r != 'bagclaim', r)
    chk('エラーなし', p.evaluate("()=>window.__errs.length") == 0, p.evaluate("()=>window.__errs"))
    br.close()
chk('tour/index.html を書き換えていない', open(os.path.join(ROOT, 'tour/index.html'), 'rb').read() == gen0)
print('NG', bad) if bad else print('すべてOK')
sys.exit(1 if bad else 0)
