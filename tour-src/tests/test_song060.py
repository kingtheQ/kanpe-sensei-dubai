# -*- coding: utf-8 -*-
"""タスク060 の動作確認(ヘッドレス)。使い方: python3 -I tour-src/tests/test_song060.py
ホテルの歌場面(hsong=nbo_song)の改善:
(1)背景が歌場面版(nairobi-hotel-lobby-song-v1.png)・通常のロビー(nlobby・nairobi-hotel-lobby-v1.png)は変わらない
(2)歌手は台の上(中心x=790・足もと y=734)・観客5人の半円・ルルとキングは観客の中央(座標=配置の正本プレビューの実測)
(3)描いた絵を配置の正本プレビューと画素で比べる(人物の域の一致率)
(4)入り: 観客が集まった絵+入りの1行→「つぎへ」でルルの一言(英語だけ・読み上げ・日本語訳なし)→「GO！」で歌が始まる(曲はGO！の操作の中だけ)
(5)049の歌・進行(曲→歌手・ルル・キングのやりとり→マップ)・対象外の場面は変わらない
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
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,SONG:SONG,PBY:PBY,ART:ART,setMode:setMode,showMap:showMap,artIdFor:artIdFor};" + HOOK, 1))
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
REF = Image.open(os.path.join(ROOT, 'tour-src/art/ref-song060/nairobi-hotel-lobby-song-preview.png')).convert('RGB')
def match(img):
    d = np.abs(np.array(img).astype(int) - np.array(REF).astype(int)).sum(2)
    return round(float((d <= 12).mean() * 100), 2), round(float((d[480:960, 380:1180] <= 12).mean() * 100), 2)
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
# ---- (1) 素材・通常のロビーは変わらない(ファイルの中身が main の変更前と同じ) ----
def git_sha(path):
    try: return subprocess.check_output(['git', 'rev-parse', 'HEAD:' + path], cwd=ROOT, stderr=subprocess.DEVNULL).decode().strip()
    except Exception: return None
def blob_sha(path):
    d = open(os.path.join(ROOT, path), 'rb').read(); return hashlib.sha1(b'blob %d\0' % len(d) + d).hexdigest()
for f in ['tour/assets/art/nairobi-hotel-lobby-v1.png', 'tour/assets/art/npc/hall-singer.png', 'tour/assets/art/npc/hall-lulu-back.png', 'tour/assets/art/npc/hall-king-back.png']:
    h = git_sha(f); chk('通常のロビーまわりの素材は変えていない: ' + f.split('/')[-1], h is not None and h == blob_sha(f), h)
bg = Image.open(os.path.join(ROOT, 'tour/assets/art/nairobi-hotel-lobby-song-v1.png')); chk('歌場面の背景(1536×960)が置かれている', bg.size == (1536, 960), bg.size)
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--autoplay-policy=document-user-activation-required'])
    ctx = br.new_context(viewport={'width': 430, 'height': 900}, device_scale_factor=1); pg = ctx.new_page(); pg.add_init_script(INIT); pg.route('**/tour/index.html', hooked)
    pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1200); pg.mouse.click(215, 450); pg.wait_for_timeout(800)
    pg.evaluate("(function(){var T=__T;T.save.ticket='ow';['nbo_immig1','nbo_bag1','nbo_sim1','nbo_taxi1'].forEach(function(v){T.save.seen[v]=1});T.setMode('arr');T.showMap()})()"); pg.wait_for_timeout(400)
    seen0 = pg.evaluate("JSON.stringify(__T.save.seen)")
    # ---- (2) 設定の数値 ----
    A = pg.evaluate("JSON.parse(JSON.stringify(__T.ART.nsong))")
    chk('歌場面は歌場面版の背景を使う(nsong)・通常のロビー(nlobby)の設定は別に残る', A['bg'] == 'nairobi-hotel-lobby-song-v1.png' and pg.evaluate("__T.ART.nlobby.bg") == 'nairobi-hotel-lobby-v1.png', A['bg'])
    chk('場面→絵の対応: 歌場面(bg=nsong)は nsong・ほかは変わらない', pg.evaluate("[__T.artIdFor({vid:'nbo_song',d:{bg:'nsong'}}),__T.artIdFor({vid:'nbo_song',d:{bg:'nlobby'}}),__T.artIdFor({vid:'nbo_room',d:{bg:'nroom'}}),__T.artIdFor({vid:'nbo_sim1',d:{bg:'sim'}})]") == ['nsong', 'nlobby', 'nroom', 'simshop'])
    s = A['hall']['sage']; chk('歌手は台の上: 中心x=790・足もと y=734(1536×960換算)', (s['x'], s['by']) == (790, 734), s)
    chk('ルルとキングは観客の中央(ルル708・キング844。足もと948)', A['hall']['lulu']['x'] == 708 and A['hall']['king']['x'] == 844 and A['hall']['lulu']['by'] == A['hall']['king']['by'] == 948)
    P = {q['n']: q for q in A['people']}
    chk('観客は5人(safari・thobe・backpacker・maasai・dashiki)', sorted(P) == sorted(['a-back-safari', 'a-back-thobe', 'a-back-backpacker', 'a-back-maasai', 'a-back-dashiki']), sorted(P))
    chk('観客の座標(正本プレビューの実測): safari(494,872) thobe(584,898) backpacker(990,888) maasai(1075,862)', all((P[k]['x'], P[k]['by']) == v for k, v in {'a-back-safari': (494, 872), 'a-back-thobe': (584, 898), 'a-back-backpacker': (990, 888), 'a-back-maasai': (1075, 862)}.items()))
    # ---- (4) 入り ----
    pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(2500)
    chk('入ってすぐ: 曲は鳴らない・GO！はまだない・「つぎへ」がある', plays(pg) == [] and pg.evaluate("!document.querySelector('button.btn.go')") and pg.evaluate("!!document.querySelector('#songNotice')"))
    msg = pg.evaluate("document.querySelector('#msg').innerText")
    chk('入りの1行(日本語)が出ている', '人が集まっている' in msg, msg)
    # ---- (3) 入りの絵(観客が集まった状態)を正本プレビューと比べる ----
    im1 = canvas(pg); m1 = match(im1); chk('絵: 全体の一致率が 93% 以上(正本プレビューと画素で比較。差12以下の画素)', m1[0] >= 93.0, m1)
    chk('絵: 人物の域(x380-1180・y480-960)の一致率が 70% 以上', m1[1] >= 70.0, m1)
    pg.click('#songNotice'); pg.wait_for_timeout(500)
    msg = pg.evaluate("document.querySelector('#msg').innerText")
    chk('ルルの一言(英語): Look, King! Someone is going to sing.', 'Look, King! Someone is going to sing.' in msg and 'ルル' in msg, msg)
    body = msg.replace('ルル', '', 1)
    chk('ルルの一言に日本語(訳)を出さない', re.search(r'[぀-ヿ一-鿿]', body) is None, body)
    chk('ルルの一言が読み上げられた', 'Look, King! Someone is going to sing.' in pg.evaluate("window.__say"))
    chk('一言のあと GO！が出る・まだ曲は鳴らない(歌を始める前)', pg.evaluate("!!document.querySelector('button.btn.go')") and plays(pg) == [])
    pg.wait_for_timeout(600)
    pg.click('button.btn.go'); pg.wait_for_timeout(2000)
    pt = plays(pg); chk('「GO！」のあと song-theme.mp3 が鳴りはじめる(1回・ユーザー操作の中)', len(pt) == 1 and pt[0][3] is True, pt)
    chk('聴くだけ: カンペ・マイク・単語バトルの画面は出ない', pg.evaluate("[!!document.querySelector('.cue'),__T.G.phase]") == [False, 'listen'])
    im2 = canvas(pg); m2 = match(im2); chk('歌っているあいだも観客・歌手の配置は同じ(一致率 93% 以上。♪が出るぶん少し下がる)', m2[0] >= 92.0, m2)
    chk('歌手の場面は保存の記録(save.seen)を変えない', pg.evaluate("JSON.stringify(__T.save.seen)") == seen0)
    Image.open(io.BytesIO(base64.b64decode(pg.evaluate("document.getElementById('sceneA').toDataURL('image/png')").split(',')[1]))).save('/tmp/song060-singing.png')
    im1.save('/tmp/song060-entry.png')
    # ---- (5) 曲が終わるとやりとり→マップ(049のまま) ----
    pg.evaluate("(function(){var e=__T.SONG.el;e.playbackRate=16})()")
    def waitmsg(k, ms=9000):
        try: pg.wait_for_function("(function(){var m=document.querySelector('#msg');return m&&m.innerText.indexOf(%s)>=0})()" % json.dumps(k), timeout=ms); return True
        except Exception: return False
    chk('曲が終わると歌手のあいさつ(049のまま)', waitmsg('Thank you for listening', 9000))
    for i, k in enumerate(['That was beautiful', 'Asante! It was a wonderful song', 'Sleep well']): chk('つづく台詞(%d): %s' % (i + 1, k), waitmsg(k, 5000))
    try: pg.wait_for_function("__T.G.view==='map'", timeout=8000)
    except Exception: pass
    chk('やりとりが終わるとマップに戻る', pg.evaluate("__T.G.view") == 'map')
    chk('エラーなし', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    ctx.close()
    # ---- 背景の絵が読めなかったとき: いつものドットのロビーに落ちて、流れは止まらない ----
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); pg = ctx.new_page(); pg.add_init_script(INIT); pg.route('**/tour/index.html', hooked)
    pg.route('**/nairobi-hotel-lobby-song-v1.png', lambda r: r.abort())
    pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1200); pg.mouse.click(215, 450); pg.wait_for_timeout(800)
    pg.evaluate("(function(){var T=__T;T.save.ticket='ow';['nbo_immig1','nbo_bag1','nbo_sim1','nbo_taxi1'].forEach(function(v){T.save.seen[v]=1});T.setMode('arr');T.showMap()})()"); pg.wait_for_timeout(400)
    pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1500); pg.click('#songNotice'); pg.wait_for_timeout(500)
    chk('背景が読めなくても、ルルの一言→GO！まで進める', pg.evaluate("!!document.querySelector('button.btn.go')") and 'Look, King!' in pg.evaluate("document.querySelector('#msg').innerText"))
    chk('エラーなし(背景が読めないとき)', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    ctx.close()
    # ---- 素材が読める ----
    ctx = br.new_context(); pg = ctx.new_page(); pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(300)
    for f in ['assets/art/nairobi-hotel-lobby-song-v1.png', 'assets/art/npc/hall-singer-stage.png'] + ['assets/art/npc/a-back-%s.png' % n for n in ['safari', 'thobe', 'backpacker', 'maasai', 'dashiki']]:
        code = pg.evaluate("fetch('%s').then(function(r){return r.status})" % f); chk('素材が読める: ' + f, code == 200, code)
    br.close()
print('FAILED: %s' % bad if bad else 'ALL OK')
sys.exit(1 if bad else 0)
