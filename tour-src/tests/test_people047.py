# -*- coding: utf-8 -*-
"""タスク047 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_people047.py
(1)荷物受取 nbo_bag1: 金髪バックパッカーが、配置の正本プレビュー(1536×960)と同じ位置・大きさ(66×126、左上 1032,582)で出る — 立ちの絵の画素が正本と一致
(2)足元の楕円の影が正本と合う (3)5往復のあいだ同じ位置(足と影は固定・全体は上下しない。動くのは腰から上の揺れ最大3px) (4)nbo_bag2・雨もりでは出ない
(5)絵が読めないときは SP.traveler のドット絵で同じ場所に出る(場面は落ちない) (6)人の置き方の部品(artPeople/artShadowP)がある・24点の素材がある
マイク・実機の見え方は確認できない。"""
import os, sys, io, base64, threading, http.server, socketserver
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACK = os.environ.get('PACK047', '/home/claude/t047')   # 配置の正本プレビューのある場所(同梱パック)
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,startVid:startVid,PBY:PBY,SP:SP,artPeople:artPeople,artShadowP:artShadowP,gt:function(){return t}};" + HOOK, 1))
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
    return np.array(Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB')).astype(int)
def start(p, vid): p.evaluate("(v)=>{var T=window.__T;T.startVid(T.PBY.bag,v,'ev')}", vid)
prev = np.array(Image.open(os.path.join(PACK, 'nbo-bag1-traveler-preview.png')).convert('RGB')).astype(int)
sp = np.array(Image.open(os.path.join(ROOT, 'tour/assets/art/npc/t-backpacker-front.png')).convert('RGBA'))
H, W = sp.shape[:2]; X0, Y0 = 1032, 582; CUT = round(H * .58)
chk('縮めた素材は 66×126', (W, H) == (66, 126), (W, H))
M = sp[:, :, 3] > 200
def sprite_diff(img, rows):   # 絵の画素(不透明)だけ、正本プレビューと比べる。rows=(開始,終了)
    m = M.copy(); m[:rows[0]] = False; m[rows[1]:] = False
    a = img[Y0:Y0 + H, X0:X0 + W]; b = prev[Y0:Y0 + H, X0:X0 + W]
    return np.abs(a - b)[m].sum(axis=1), int(m.sum())
# 影: 正本の 703〜708 行・1030〜1099 列(703行より上・709行より下は、正本では画面の会話枠の影が重なって約8%暗い)で、絵の画素以外を比べる
SH = (slice(703, 709), slice(1030, 1100))
SM = np.zeros(prev.shape[:2], bool); SM[Y0:Y0 + H, X0:X0 + W] = sp[:, :, 3] > 0
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
gen0 = open(os.path.join(ROOT, 'tour/index.html'), 'rb').read()
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
    p = ctx.new_page(); p.route('**/tour/index.html', hooked)
    # 画素比べのコマでは、まわる荷物を透明にする(荷物は足元の影の上を通るため。旅行者の描き方だけを比べる。荷物のある普通の画面は最後に撮る)
    bi = Image.open(os.path.join(ROOT, 'tour/assets/art/nairobi-baggage-bags.png')); tb = io.BytesIO(); Image.new('RGBA', bi.size, (0, 0, 0, 0)).save(tb, 'PNG')
    p.route('**/nairobi-baggage-bags.png', lambda r: r.fulfill(status=200, body=tb.getvalue(), content_type='image/png'))
    p.goto(base + '/tour/index.html'); p.wait_for_timeout(1800)
    start(p, 'nbo_bag1'); p.wait_for_timeout(1500)
    frames = {}
    for ti in range(5):
        p.evaluate("(k)=>{__T.G.ti=k}", ti); p.wait_for_timeout(700)
        frames[ti] = [snap(p) for _ in range(8) if (p.wait_for_timeout(137) or True)]
    allf = [f for v in frames.values() for f in v]
    # (1) 下半身(腰から下=動かない所)は全部のコマで正本と一致。上半身は揺れの0のコマで一致
    lo = [sprite_diff(f, (CUT, H)) for f in allf]; lo_max = max(d.max() for d, n in lo)
    chk('立ちの絵(腰から下)が正本と全コマで画素一致(%d画素×%dコマ)' % (lo[0][1], len(allf)), lo_max == 0, '最大差 %d' % lo_max)
    up = [sprite_diff(f, (0, CUT)) for f in allf]; best = min(d.sum() for d, n in up)
    chk('立ちの絵(腰から上)は、揺れが0のコマで正本と画素一致(%d画素)' % up[0][1], best == 0, '最小差 %d' % best)
    # (2) 影
    dsh = []
    for f in allf:
        m = ~SM[SH]; dsh.append(int((np.abs(f[SH] - prev[SH]).sum(axis=2)[m] > 40).sum()))
    chk('足元の影が正本と一致(703〜708行・%d画素のうち差のある画素 最大 %d)' % (int((~SM[SH]).sum()), max(dsh)), max(dsh) <= 4, dsh[:8])
    # (3) 位置の固定: 足と影(絵の腰から下+影の行)は5往復の全コマで同じ
    low = [np.concatenate([f[Y0 + CUT:Y0 + H, X0:X0 + W].ravel(), f[SH].ravel()]) for f in allf]; same = all((x == low[0]).all() for x in low)
    chk('5往復・%dコマのあいだ、足(腰から下)と影の画素が1つも動かない' % len(allf), same)
    # 頭の上端: 絵の一番上の行の色(輪郭)が、画面のどの行に出るか。全体が上下するなら 3px を超える/足も動く。揺れなら 0〜3px 上に伸びるだけ
    r0 = int(np.where(M.any(axis=1))[0][0]); ext = []   # 絵の一番上の行は、ほぼ黒の輪郭が22画素
    for f in allf:
        r = None
        for yy in range(Y0 + r0 - 8, Y0 + r0 + 8):
            if (f[yy, X0:X0 + W].sum(axis=1) <= 24).sum() >= 10: r = Y0 + r0 - yy; break
        ext.append(r)
    chk('頭の上端の動きは 0〜3px の範囲(全体の上下なし)。観測 %s' % sorted(set(ext)), None not in ext and min(ext) >= 0 and max(ext) <= 3 and max(ext) >= 1, sorted(set(ext)))
    # (4) bag2・雨もりでは出ない
    for vid in ('nbo_bag2', 'nbo_ev_b_leak'):
        start(p, vid); p.wait_for_timeout(1500); f = snap(p)
        d, n = sprite_diff(f, (CUT, H))
        chk('%s では旅行者を出さない(絵の画素の一致が %d/%d 画素)' % (vid, int((d == 0).sum()), n), (d == 0).mean() < .5)
    chk('エラーなし', p.evaluate("()=>window.__errs.length") == 0, p.evaluate("()=>window.__errs"))
    # (5) フォールバック: 素材が読めないとき
    ctx2 = br.new_context(viewport={'width': 390, 'height': 780}); ctx2.add_init_script(INIT)
    q = ctx2.new_page(); q.route('**/tour/index.html', hooked); q.route('**/npc/t-backpacker-front.png', lambda r: r.abort())
    q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800); start(q, 'nbo_bag1'); q.wait_for_timeout(2000)
    f = snap(q); shown = q.evaluate("()=>document.getElementById('sceneA').hidden===false")
    jc = (f[560:712, 1020:1112] == np.array([58, 90, 138])).all(axis=2).sum()   # SP.traveler の服の色。素材の絵では出ない
    sh = int((np.abs(f[708, 1026:1105] - np.array([117, 121, 131])).sum(axis=1) <= 8).sum())
    chk('素材が読めなくても、場面は出て(新しい絵のまま)、SP.traveler のドット絵(服の色 %d画素)と影(%d画素)が足元に出る' % (jc, sh), shown and jc >= 150 and sh >= 30, (shown, jc, sh))
    j0 = int((np.abs(allf[0][560:712, 1020:1112] - np.array([58, 90, 138])).sum(axis=2) == 0).sum())
    chk('ふだんの絵のときは SP.traveler の服の色は出ない(%d画素)' % j0, j0 == 0)
    snap_path = '/tmp/t047_fallback.png'; Image.fromarray(f.astype('uint8')).save(snap_path)
    chk('フォールバックのエラーなし', q.evaluate("()=>window.__errs.length") == 0, q.evaluate("()=>window.__errs"))
    # (6) 部品
    chk('部品 artPeople / artShadowP がある', p.evaluate("()=>typeof __T.artPeople==='function'&&typeof __T.artShadowP==='function'"))
    br.close()
n = len([f for f in os.listdir(os.path.join(ROOT, 'tour/assets/art/npc')) if f.startswith('t-') and f.endswith('.png')])
chk('旅行者の素材が24点(6人×4ポーズ)', n == 24, n)
chk('tour/index.html を書き換えていない', open(os.path.join(ROOT, 'tour/index.html'), 'rb').read() == gen0)
print('NG', bad) if bad else print('すべてOK')
sys.exit(1 if bad else 0)
