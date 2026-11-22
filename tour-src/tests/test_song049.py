# -*- coding: utf-8 -*-
"""タスク049 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_song049.py [OLDROOT=変更前の作業コピー]
(1)オープニング: 最初の画面(DAY 1)をタップ→賢者の最初の会話の「GO！」を押しても曲(チャント)は鳴らない(タスク050でチャントはタイトル画面の曲へ。再生・ループ・継続・停止は test_chant050.py)
(2)会話はふつうに進む
(3)ホテルのロビー(hsong): 到着タブの最後にある・到着の完了条件には入らない(場面の数・済の印・保存の記録 save.seen が変わらない)・タクシーのあとに開く
(4)歌手の場面: 「GO！」のあとテーマ曲が鳴る(操作の中で)・発音/採点/単語バトルの画面にならない・音符が出る・曲の途中でも出口ボタンでマップに戻れて曲が止まる
(5)曲が最後まで鳴ると歌手・ルル・キングの短いやりとり→マップへ。音オフのときは曲なしで先へ進める
(6)テーマ曲はこの場面でしか鳴らない(オープニング・ほかの場面で song-theme.mp3 は一度も鳴らない)/画面に「勉強・テスト・測定・練習」の言葉がない/保存データに曲の状態を書かない
マイク・実機の音・実機の見え方は確認できない。"""
import os, sys, json, threading, http.server, socketserver
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
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,SONG:SONG,PBY:PBY,PLACES_NARR:PLACES_NARR,setMode:setMode,showMap:showMap,enterPlace:enterPlace,startVid:startVid,"
        "DLG:DLG,TOTALV:function(){return TOTALV},gt:function(){return t}};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "window.__au=[];(function(){var P=HTMLMediaElement.prototype,pl=P.play,pa=P.pause;"
        "P.play=function(){window.__au.push(['play',(this.src||'').split('/').pop().slice(0,22),+this.volume.toFixed(2),!!(navigator.userActivation&&navigator.userActivation.isActive),+this.currentTime.toFixed(2)]);return pl.apply(this,arguments)};"
        "P.pause=function(){window.__au.push(['pause',(this.src||'').split('/').pop().slice(0,22),+this.currentTime.toFixed(1)]);return pa.apply(this,arguments)}})();"
        "window.__say=[];try{speechSynthesis.speak=function(u){window.__say.push(u.text);setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));")
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
def plays(p, f):   # 曲ファイルを新しく鳴らした記録 [(音量, 操作の中か)](0秒からの再生だけ。マイクのあとの続きからの再生は数えない)
    return [(a[2], a[3]) for a in p.evaluate("window.__au") if a[0] == 'play' and a[1].startswith(f) and a[4] < 0.05]
def pauses(p, f): return [a for a in p.evaluate("window.__au") if a[0] == 'pause' and a[1].startswith(f)]
def paused(p): return p.evaluate("(function(){var e=__T.SONG.el;return e?e.paused:null})()")
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
def newpage(br, init=INIT):
    ctx = br.new_context(viewport={'width': 430, 'height': 900}, device_scale_factor=1)
    pg = ctx.new_page(); pg.add_init_script(init); pg.route('**/tour/index.html', hooked); return pg
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--autoplay-policy=document-user-activation-required'])
    # ---------------- (1)(2) オープニング: チャントはタイトルの曲(タスク050)。賢者の広間の「GO！」では鳴らない ----------------
    pg = newpage(br); pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1200)
    chk('オープニングは最初の画面(DAY 1)から始まる(まだ曲は鳴らない)', pg.evaluate("__T.G.view") == 'map' and plays(pg, 'song-chant') == [], plays(pg, 'song-chant'))
    pg.mouse.click(215, 450); pg.wait_for_timeout(900)
    chk('最初の操作のあと、賢者の広間の最初の会話(sage_1)が開く・曲は鳴らない', pg.evaluate("__T.G.scene&&__T.G.scene.vid") == 'sage_1' and plays(pg, 'song-chant') == [])
    pg.click('button.btn.go'); pg.wait_for_timeout(1500)
    chk('「GO！」を押してもチャントは鳴らない(050でタイトルへ移した。再生は test_chant050.py)', plays(pg, 'song-chant') == [] and pg.evaluate("__T.SONG.el") is None, plays(pg, 'song-chant'))
    # 会話がふつうに進む: 相手の台詞→カンペ(画面にカンペが出る)
    pg.wait_for_timeout(1500)
    ph = pg.evaluate("[__T.G.phase,!!document.querySelector('.cue'),__T.G.scene.pl.id]")
    chk('会話がふつうに進む(相手の台詞のあとカンペが出る)', ph[1] is True and ph[2] == 'sage', ph)
    chk('オープニングでテーマ曲は鳴らない', plays(pg, 'song-theme') == [])
    chk('エラーなし(オープニング)', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    pg.context.close()
    # ---------------- (3)(4)(5) ホテルのロビーの歌手 ----------------
    pg = newpage(br); pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1200)
    pg.mouse.click(215, 450); pg.wait_for_timeout(800)
    ids = pg.evaluate("__T.PLACES_NARR.map(function(p){return p.id})")
    chk('到着タブのタクシーのあとにホテルのロビー hsong がある(タスク051でそのあとにホテルの部屋 hroom が増えた)', ids == ['immig', 'bag', 'sim', 'taxi', 'hsong', 'hroom'], ids)
    pl = pg.evaluate("(function(){var p=__T.PBY.hsong;return [p.v.length,p.listen,p.name,p.tip[0]]})()")
    chk('場面の数は空(完了条件・場面の数に入らない)・実名のホテル名', pl[0] == 0 and pl[1] == 'nbo_song' and pl[3] == 'Villa Rosa Kempinski', pl)
    # 順に開く: 入国審査を遊ぶ前は鍵がかかっている(到着のあと)
    pg.evaluate("(function(){var T=__T;T.save.ticket='ow';T.setMode('arr');T.showMap()})()"); pg.wait_for_timeout(400)
    lk = pg.evaluate("document.querySelector('.node[data-id=hsong]').classList.contains('lock')")
    chk('入国審査〜タクシーを遊ぶ前は、ロビーに鍵がかかっている(到着のあとに開く)', lk is True)
    tv0 = pg.evaluate("__T.TOTALV()")
    pg.evaluate("(function(){var T=__T;['nbo_immig1','nbo_bag1','nbo_sim1','nbo_taxi1'].forEach(function(v){T.save.seen[v]=1});T.showMap()})()"); pg.wait_for_timeout(400)
    lk = pg.evaluate("document.querySelector('.node[data-id=hsong]').classList.contains('lock')")
    chk('タクシーまで遊ぶとロビーが開く', lk is False)
    chk('場面の数(TOTALV)は変わらない(ロビーは数に入らない)', pg.evaluate("__T.TOTALV()") == tv0 == 8, [tv0])
    chk('ロビーに「済」の印は出ない(任意の場所)', pg.evaluate("document.querySelector('.node[data-id=hsong]').classList.contains('done')") is False)
    seen0 = pg.evaluate("JSON.stringify(__T.save.seen)")
    pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1800)
    sc = pg.evaluate("[__T.G.view,__T.G.phase,__T.G.scene.d.id,!!document.querySelector('.cue'),__T.G.scene.turns.length]")
    chk('歌手の場面に入る(カンペ・会話の型ではない)', sc[0] == 'scene' and sc[2] == 'nbo_song' and sc[3] is False and sc[4] == 0, sc)
    chk('入ってすぐは曲は鳴らない(操作のあとだけ)', plays(pg, 'song-theme') == [])
    txt = pg.evaluate("document.body.innerText")
    for w in ['勉強', 'テスト', '測定', '練習', '復習', '採点']:
        chk('画面に「%s」の言葉がない(入口)' % w, w not in txt)
    pg.click('#songNotice'); pg.wait_for_timeout(500)   # タスク060: 入り→「つぎへ」でルルの一言→「GO！」
    pg.click('button.btn.go'); pg.wait_for_timeout(2000)
    pt = plays(pg, 'song-theme')
    chk('「GO！」のあと song-theme.mp3 が鳴りはじめる(1回・ユーザー操作の中)', len(pt) == 1 and pt[0][1] is True, pt)
    st = pg.evaluate("(function(){var e=__T.SONG.el;return [__T.SONG.key,e.paused,+e.currentTime.toFixed(1),+e.duration.toFixed(1)]})()")
    chk('テーマが実際に再生されている(約75秒の曲)', st[0] == 'theme' and st[1] is False and st[2] > 0.5 and abs(st[3] - 74.6) < 0.5, st)
    chk('聴くだけ: カンペ・マイク・単語バトルの画面は出ない', pg.evaluate("[!!document.querySelector('.cue'),__T.G.phase]") == [False, 'listen'])
    chk('チャントは鳴っていない・ロビーでテーマだけ鳴る', plays(pg, 'song-chant') == [])
    txt = pg.evaluate("document.body.innerText")
    chk('曲のあいだ「勉強・テスト・測定・練習」の言葉がない', not any(w in txt for w in ['勉強', 'テスト', '測定', '練習', '復習', '採点']))
    # 曲の途中でも出口ボタンで離れられる→止まる
    pg.click('#exitBtn'); pg.wait_for_timeout(500)
    chk('曲の途中でも出口ボタンでマップに戻れる', pg.evaluate("__T.G.view") == 'map')
    chk('場面を離れたらテーマが止まる', pg.evaluate("__T.SONG.el") is None and len(pauses(pg, 'song-theme')) >= 1, pauses(pg, 'song-theme'))
    chk('歌手の場面は保存の記録(save.seen)を変えない', pg.evaluate("JSON.stringify(__T.save.seen)") == seen0)
    # もう一度入って、最後まで聴く(終わり近くへ飛ばす)→歌手・ルル・キングのやりとり→マップ
    pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1500); pg.click('#songNotice'); pg.wait_for_timeout(400); pg.click('button.btn.go'); pg.wait_for_timeout(1200)
    chk('もう一度入ると、また最初から聴ける(任意・何度でも)', len(plays(pg, 'song-theme')) == 2)
    pg.evaluate("(function(){var e=__T.SONG.el;e.playbackRate=16})()"); pg.wait_for_timeout(100)   # 16倍速で自然に最後まで鳴らす(試験用の簡易サーバーは途中からの読み込みに対応しないため)
    def waitmsg(k, ms=9000):
        try: pg.wait_for_function("(function(){var m=document.querySelector('#msg');return m&&m.innerText.indexOf(%s)>=0})()" % json.dumps(k), timeout=ms); return True
        except Exception: return False
    chk('曲が終わると歌手のあいさつ(英語・読み上げ)に進む', waitmsg('Thank you for listening', 9000))
    for i, k in enumerate(['That was beautiful', 'Asante! It was a wonderful song', 'Sleep well']):
        chk('つづく台詞(%d): %s' % (i + 1, k), waitmsg(k, 5000))
    try: pg.wait_for_function("__T.G.view==='map'", timeout=8000)
    except Exception: pass
    chk('やりとりが終わるとマップに戻る', pg.evaluate("__T.G.view") == 'map')
    say = [x for x in pg.evaluate("window.__say") if x.startswith(('Thank you for', 'That was', 'Asante'))]
    chk('台詞は読み上げられた(4つ)', len(say) == 4, say)
    chk('歌手の場面でマイク・発音の保存(kanpe-pron-v1)を作っていない', pg.evaluate("localStorage.getItem('kanpe-pron-v1')") is None)
    keys = pg.evaluate("Object.keys(localStorage)")
    chk('曲の状態を保存データに書いていない(保存キーに song の名前がない)', not any('song' in k.lower() for k in keys), keys)
    chk('エラーなし(ロビー)', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    pg.context.close()
    # ---------------- 音オフ・再生が止められたとき: 曲なしで先へ進める ----------------
    pg = newpage(br, INIT + "localStorage.setItem('kd_snd','off');")
    pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1200); pg.mouse.click(215, 450); pg.wait_for_timeout(800)
    pg.evaluate("(function(){var T=__T;T.save.ticket='ow';['nbo_immig1','nbo_bag1','nbo_sim1','nbo_taxi1'].forEach(function(v){T.save.seen[v]=1});T.setMode('arr');T.showMap()})()"); pg.wait_for_timeout(400)
    pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1500); pg.click('#songNotice'); pg.wait_for_timeout(400); pg.click('button.btn.go'); pg.wait_for_timeout(800)
    chk('音オフのときは曲を鳴らさない', plays(pg, 'song-theme') == [])
    chk('音オフでも「つぎへ」で先へ進める(曲なしで詰まらない)', pg.evaluate("!!document.querySelector('.songnext')") is True)
    pg.click('.songnext'); pg.wait_for_timeout(600)
    chk('「つぎへ」で歌手のあいさつへ', 'Thank you for listening' in pg.evaluate("document.querySelector('#msg').innerText"))
    pg.context.close()
    # ---------------- 画像・音の素材が読めている ----------------
    pg = newpage(br); pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(500)
    for f in ['assets/art/nairobi-hotel-lobby-v1.png', 'assets/art/npc/hall-singer.png', 'assets/song/song-chant.mp3', 'assets/song/song-theme.mp3']:
        code = pg.evaluate("fetch('%s').then(function(r){return r.status})" % f)
        chk('素材が読める: ' + f, code == 200, code)
    br.close()
print('FAILED: %s' % bad if bad else 'ALL OK')
sys.exit(1 if bad else 0)
