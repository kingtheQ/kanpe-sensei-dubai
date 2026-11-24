# -*- coding: utf-8 -*-
"""タスク066 の動作確認(ヘッドレス)。使い方: python3 -I tour-src/tests/test_lobby066.py
(1)ロビーは通常版: 受付のスタッフが案内する場面(hub)・案内の3択(ショータイム/プール/Balcony Bar)・歌手は出ない
(2)ショータイムを選ぶと別場面のプールサイド(npool)で歌う。歌手は高さ250・観客・ルル・キングは指示書の座標・描いた絵を配置の正本プレビューと画素で比較
(1b)タスク077/077b: プールもバーも実在の場面へ
(3)照明ストリップ: 曲が鳴っているあいだは再生位置の拍に合わせて切りかえ(歌手の絵も)、鳴っていないときはゆっくり明滅
(4)049の歌・進行(曲→やりとり→マップ)は変わらない
マイク・実機の音・実機の見え方は確認できない。"""
import os, sys, json, re, base64, io, hashlib, subprocess, threading, http.server, socketserver
import numpy as np
from PIL import Image
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
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,SONG:SONG,songBeatN:songBeatN,PBY:PBY,ART:ART,setMode:setMode,showMap:showMap,artIdFor:artIdFor};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "window.__au=[];(function(){var P=HTMLMediaElement.prototype,pl=P.play;"
        "P.play=function(){window.__au.push(['play',(this.src||'').split('/').pop().slice(0,22),+this.currentTime.toFixed(2),!!(navigator.userActivation&&navigator.userActivation.isActive)]);return pl.apply(this,arguments)}})();"
        "window.__say=[];try{speechSynthesis.speak=function(u){window.__say.push(u.text);setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));")
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
def plays(p): return [a for a in p.evaluate("window.__au") if a[0] == 'play' and a[1].startswith('song-theme') and a[2] < 0.05]
def canvas(p): return Image.open(io.BytesIO(base64.b64decode(p.evaluate("document.getElementById('sceneA').toDataURL('image/png')").split(',')[1]))).convert('RGB')

REF = Image.open(os.path.join(ROOT, 'tour-src/art/ref-066/nairobi-pool-v2-preview.png')).convert('RGB')
def match(img):
    d = np.abs(np.array(img).astype(int) - np.array(REF).astype(int)).sum(2)
    return round(float((d <= 12).mean() * 100), 2), round(float((d[480:960, 380:1180] <= 12).mean() * 100), 2)
ART = os.path.join(ROOT, 'tour/assets/art')
BG = Image.open(os.path.join(ART, 'nairobi-pool-v2.png')).convert('RGBA'); LS = Image.open(os.path.join(ART, 'nairobi-pool-lights-strip.png')).convert('RGBA')
def top_expect(f):   # 背景+照明ストリップの f コマ目 の上の域(y0-300)。きらめき(y484〜)・人物は入らない域
    c = BG.copy(); c.alpha_composite(LS.crop((f * 1536, 0, f * 1536 + 1536, 960))); return np.array(c.convert('RGB'))[0:300, 0:400]   # タスク076: 光の円錐・キラキラは歌手のまわり(x 450〜)だけなので、左の x<400 で照明ストリップを比べる
def top_frame(img):
    a = np.array(img)[0:300, 0:400].astype(int); r = []
    for f in range(4): r.append(round(float((np.abs(a - top_expect(f).astype(int)).sum(2) <= 12).mean() * 100), 2))
    return r
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
def go(pg):
    pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1200); pg.mouse.click(215, 450); pg.wait_for_timeout(800)
    pg.evaluate("(function(){var T=__T;T.save.ticket='ow';['nbo_immig1','nbo_bag1','nbo_sim1','nbo_taxi1'].forEach(function(v){T.save.seen[v]=1});T.setMode('arr');T.showMap()})()"); pg.wait_for_timeout(400)
# ---- 素材 ----
for f, sz in [('nairobi-pool-v2.png', (1536, 960)), ('nairobi-pool-sparkle-strip-v2.png', (4592, 206)), ('nairobi-pool-lights-strip.png', (6144, 960))]:
    chk('素材の大きさ: ' + f, Image.open(os.path.join(ART, f)).size == sz, Image.open(os.path.join(ART, f)).size)
for n in ['s-stand-front', 's-stand-sing1', 's-stand-sing2', 'b-back-safari', 'b-back-thobe', 'b-back-backpacker', 'b-back-maasai', 'b-back-dashiki']:
    chk('高さ250: ' + n, Image.open(os.path.join(ART, 'npc', n + '.png')).height == 250)
for f in ['nairobi-hotel-lobby-song-v1.png', 'npc/hall-singer-stage.png', 'npc/a-back-maasai.png']: chk('060のファイルは消していない: ' + f, os.path.exists(os.path.join(ART, f)))
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--autoplay-policy=document-user-activation-required'])
    ctx = br.new_context(viewport={'width': 430, 'height': 900}, device_scale_factor=1); pg = ctx.new_page(); pg.add_init_script(INIT); pg.route('**/tour/index.html', hooked)
    go(pg); seen0 = pg.evaluate("JSON.stringify(__T.save.seen)")
    A = pg.evaluate("JSON.parse(JSON.stringify(__T.ART.npool))"); st = A['stage']
    chk('歌手: 中心x=790・足もと y=734', (st['singer']['x'], st['singer']['by']) == (790, 734), st['singer'])
    P = {q['n']: (q['x'], q['by']) for q in st['people']}
    chk('観客の座標(指示書どおり)', P == {'b-back-maasai': (1142, 856), 'b-back-safari': (462, 864), 'b-back-backpacker': (1064, 868), 'b-back-thobe': (585, 900), 'b-back-dashiki': (960, 906)}, P)
    chk('ルル(712,886)・キング(838,890)', (st['lulu']['x'], st['lulu']['by'], st['king']['x'], st['king']['by']) == (712, 886, 838, 890))
    chk('照明ストリップは(0,0)・曲に同期(beat)・きらめきは(56,484)', [(q['x'], q['y'], q.get('sync')) for q in A['strips']] == [(56, 484, None), (0, 0, 'beat')], A['strips'])
    # ---- ロビー(通常版) ----
    hs = pg.evaluate("(function(){var p=__T.PBY.hsong;return [!!p.hub,!!p.listen,p.menu.map(function(m){return m[0]}),p.hubBg]})()")
    chk('ロビーは案内の3択(hub)・歌の場面そのものではない', hs[0] is True and hs[1] is False and hs[2] == ['See the evening show', 'The swimming pool', 'The Balcony Bar'], hs)
    chk('ロビーの選択肢は英文だけ(日本語を足さない)', all(re.search(r'[぀-ヿ一-鿿]', m) is None for m in hs[2]))
    pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1800)
    chk('ロビー: 絵の設定は nlobby・歌手(singer)は出ない・スタッフ(tk-clerk)が立つ', pg.evaluate("[__T.artIdFor(__T.G.scene),!!__T.ART.nlobby.hall.sage,__T.ART.nlobby.hall.clerk.n]") == ['nlobby', False, 'tk-clerk'], pg.evaluate("__T.artIdFor(__T.G.scene)"))
    lob = canvas(pg); lob.save('/tmp/lobby066.png'); a = np.array(lob).astype(int); bgl = np.array(Image.open(os.path.join(ART, 'nairobi-hotel-lobby-v1.png')).convert('RGB')).astype(int)
    chk('ロビー: 背景の絵が描かれている(受付まわりの画素の一致 80% 以上)', float((np.abs(a - bgl).sum(2)[0:480] <= 12).mean()) > .8)
    chk('ロビー: 案内の一言を読み上げ・メニュー3つ+もどる', 'Welcome to the Villa Rosa Kempinski. What would you like to see?' in pg.evaluate("window.__say") and pg.evaluate("document.querySelectorAll('button.dq').length") == 4)
    chk('ロビー: 曲は鳴らない・日本語の選択肢なし', plays(pg) == [])
    # タスク077b: バーも実在の場面 nbo_bar1(絵 nbar)へ(詳しくは test_lobby077.py・test_lobby077b.py)。プールは実在の場面 nbo_pool1 へ(test_lobby077.py)
    pg.click('button.dq:nth-child(3)'); pg.wait_for_timeout(900)
    chk('「The Balcony Bar」: 場面 nbo_bar1(バルコニーバル)に入る・絵は nbar', pg.evaluate("[__T.G.view,__T.G.scene.d.id,__T.artIdFor(__T.G.scene)]") == ['scene', 'nbo_bar1', 'nbar'], pg.evaluate("[__T.G.view,__T.G.scene.d.id,__T.artIdFor(__T.G.scene)]"))
    pg.click('#exitBtn'); pg.wait_for_timeout(500); pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1500)
    pg.click('button.dq:nth-child(2)'); pg.wait_for_timeout(700)
    chk('「The swimming pool」: 場面 nbo_pool1(静かなプール)に入る・絵は npoolq', pg.evaluate("[__T.G.view,__T.G.scene.d.id,__T.artIdFor(__T.G.scene)]") == ['scene', 'nbo_pool1', 'npoolq'], pg.evaluate("[__T.G.view,__T.G.scene.d.id,__T.artIdFor(__T.G.scene)]"))
    pg.click('#exitBtn'); pg.wait_for_timeout(500); pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1500)
    # ---- ショータイム → プールサイド ----
    pg.click('button.dq:nth-child(1)'); pg.wait_for_timeout(2500)
    chk('ショータイム: 別場面(nbo_song)・絵は npool(プールサイド)', pg.evaluate("[__T.G.scene.id,__T.G.scene.d.id,__T.G.scene.d.bg,__T.artIdFor(__T.G.scene)]") == ['hsong', 'nbo_song', 'npool', 'npool'], pg.evaluate("[__T.G.scene.d.bg,__T.artIdFor(__T.G.scene)]"))
    chk('入ってすぐは曲が鳴らない・入りの1行(日本語)', plays(pg) == [] and 'プールサイド' in pg.evaluate("document.querySelector('#msg').innerText"))
    im1 = canvas(pg); im1.save('/tmp/pool066-entry.png'); m1 = match(im1)
    chk('絵: 全体の一致率が 95% 以上(配置の正本プレビューと画素で比較。差12以下の画素)', m1[0] >= 95.0, m1)
    chk('絵: 人物の域(x380-1180・y480-960)の一致率が 75% 以上', m1[1] >= 75.0, m1)
    tf = top_frame(im1); chk('曲が鳴っていないとき、照明は背景+ストリップのどれかのコマ(上の域の一致 99% 以上)', max(tf) >= 99.0, tf)
    f0 = tf.index(max(tf)); pg.wait_for_timeout(1900); tf2 = top_frame(canvas(pg)); f1 = tf2.index(max(tf2))
    chk('曲が鳴っていないとき、ゆっくり明滅する(1.9秒でコマが変わる)', max(tf2) >= 99.0 and f1 != f0, (f0, f1))
    pg.click('#songNotice'); pg.wait_for_timeout(400); pg.wait_for_timeout(600)
    pg.click('button.btn.go'); pg.wait_for_timeout(1500)
    pt = plays(pg); chk('「GO！」のあと song-theme.mp3 が鳴りはじめる(1回・ユーザー操作の中)', len(pt) == 1 and pt[0][3] is True, pt)
    # ---- 曲の再生位置に同期 ----
    pg.evaluate("(function(){var e=__T.SONG.el;e.pause();window.__fake=e})()")
    B = pg.evaluate("JSON.parse(JSON.stringify(window.__T.G.scene.d.beats))"); chk('拍のデータ: 100個以上・昇順・曲の長さ(74.6秒)以内', len(B) >= 100 and B == sorted(B) and B[-1] < 74.6, (len(B), B[-1]))
    res = []
    for ct in [B[10] + .05, B[11] + .05, B[12] + .05, B[13] + .05, B[14] + .05]:
        pg.evaluate("(function(ct){var e=window.__fake;Object.defineProperty(e,'currentTime',{get:function(){return ct},configurable:true});Object.defineProperty(e,'paused',{get:function(){return false},configurable:true})})(%f)" % ct)
        pg.wait_for_timeout(250); n = pg.evaluate("__T.songBeatN()"); tf = top_frame(canvas(pg)); res.append((n, tf.index(max(tf)), max(tf)))
    chk('曲の再生位置の拍の数 = 数えた拍(11,12,13,14,15)', [r[0] for r in res] == [11, 12, 13, 14, 15], res)
    chk('照明のコマ = 拍の数 mod 4(拍ごとに切りかわる)', all(r[1] == r[0] % 4 and r[2] >= 99.0 for r in res), res)
    # 歌手の絵: 拍ごとに 歌う絵 a/b を切りかえる(足もとは固定・頭の高さの域を比べる)
    def sing_frac(img, n):
        s = Image.open(os.path.join(ART, 'npc', n + '.png')).convert('RGBA'); x0 = int(790 - s.width / 2 + .5); y0 = 734 - 250
        a = np.array(img.crop((x0, y0, x0 + s.width, y0 + 120))).astype(int); sp = np.array(s)[:120].astype(int); m = sp[..., 3] > 0
        return round(float((np.abs(a - sp[..., :3]).sum(2)[m] <= 12).mean() * 100), 1)
    ims = []
    for ct in [B[11] + .05, B[12] + .05, B[13] + .05, B[14] + .05]:   # 拍の数 12,13,14,15 → タスク076: [歌う絵1 → 正面 → 歌う絵2 → 正面]
        pg.evaluate("(function(ct){Object.defineProperty(window.__fake,'currentTime',{get:function(){return ct},configurable:true})})(%f)" % ct); pg.wait_for_timeout(250); ims.append(canvas(pg))
    sg = [[sing_frac(i, n) for n in ('s-stand-sing1', 's-stand-front', 's-stand-sing2')] for i in ims]
    chk('歌手: 拍ごとに [歌う絵1 → 正面 → 歌う絵2 → 正面] を切りかえる(高さ250・足もと y=734)', [r.index(max(r)) for r in sg] == [0, 1, 2, 1] and all(max(r) >= 95 for r in sg), sg)
    chk('聴くだけ: カンペ・マイク・単語バトルの画面は出ない', pg.evaluate("[!!document.querySelector('.cue'),__T.G.phase]") == [False, 'listen'])
    chk('場面は保存の記録(save.seen)を変えない', pg.evaluate("JSON.stringify(__T.save.seen)") == seen0)
    ims[0].save('/tmp/pool066-singing.png')
    chk('エラーなし', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    ctx.close()
    # ---- 曲が終わるとやりとり→マップ(049のまま) ----
    ctx = br.new_context(viewport={'width': 430, 'height': 900}, device_scale_factor=1); pg = ctx.new_page(); pg.add_init_script(INIT); pg.route('**/tour/index.html', hooked)
    go(pg); pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1500); pg.click('button.dq:nth-child(1)'); pg.wait_for_timeout(1500)
    pg.click('#songNotice'); pg.wait_for_timeout(500); pg.click('button.btn.go'); pg.wait_for_timeout(1200); pg.evaluate("__T.SONG.el.playbackRate=16")
    def waitmsg(k, ms=9000):
        try: pg.wait_for_function("(function(){var m=document.querySelector('#msg');return m&&m.innerText.indexOf(%s)>=0})()" % json.dumps(k), timeout=ms); return True
        except Exception: return False
    chk('曲が終わると歌手のあいさつ(049のまま)', waitmsg('Thank you for listening', 12000))
    for i, k in enumerate(['That was beautiful', 'Asante! It was a wonderful song', 'Sleep well']): chk('つづく台詞(%d): %s' % (i + 1, k), waitmsg(k, 5000))
    try: pg.wait_for_function("__T.G.view==='map'", timeout=8000)
    except Exception: pass
    chk('やりとりが終わるとマップに戻る', pg.evaluate("__T.G.view") == 'map')
    chk('エラーなし(通し)', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    ctx.close()
    # ---- 絵が読めなかったとき ----
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); pg = ctx.new_page(); pg.add_init_script(INIT); pg.route('**/tour/index.html', hooked); pg.route('**/nairobi-pool-v2.png', lambda r: r.abort())
    go(pg); pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1500); pg.click('button.dq:nth-child(1)'); pg.wait_for_timeout(1500); pg.click('#songNotice'); pg.wait_for_timeout(500)
    chk('プールの背景が読めなくても、ルルの一言→GO！まで進める', pg.evaluate("!!document.querySelector('button.btn.go')"))
    chk('エラーなし(背景が読めないとき)', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    ctx.close(); br.close()
print('FAILED: %s' % bad if bad else 'ALL OK')
sys.exit(1 if bad else 0)
