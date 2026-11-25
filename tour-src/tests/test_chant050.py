# -*- coding: utf-8 -*-
"""タスク050 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_chant050.py
(1)タイトル(world/): 起動直後(無操作)は鳴らない・エラーなし。最初のタッチで song-chant.mp3 が先頭から・音量0.2で鳴る(ユーザー操作の中)。
    最初のタッチが「はじめる」ボタンでも同じ。タッチを何回しても1つだけ(二重に鳴らない)。タイトルにいるあいだはループ
(2)「はじめから」で tour/ へ進んでも先頭に戻らず続きから鳴る→DAY 1→賢者の広間(sage_1)でも同じ再生が続く→最初の会話(GO！)で止まり、そのあと再開しない
(3)sage_1 の「GO！」ではチャントが新たに始まらない(タイトルを通らずに広間へ来た場合は、最初から鳴らない)
(4)マイク中(duck)は止まり、終わると続きから(最初の会話の前だけ)。音オフなら鳴らさない
(5)「つづきから」(地図)ではチャントが止まる。タイトルを通らない開き方(?map=1)では鳴らない
(6)049の歌手イベントとテーマ曲に変更なし: タイトル・広間でテーマ曲は鳴らない。画面に「勉強・テスト・測定・練習」の言葉がない。保存データにチャントの状態を書かない
マイク・実機の音・実機の自動再生の可否は確認できない。"""
import os, sys, json, threading, http.server, socketserver
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "(function(){var P=HTMLMediaElement.prototype,pl=P.play,pa=P.pause;var L=JSON.parse(sessionStorage.getItem('__au')||'[]');window.__au=L;"
        "function sv(){try{sessionStorage.setItem('__au',JSON.stringify(L))}catch(e){}}"
        "P.play=function(){L.push(['play',(this.src||'').split('/').pop().slice(0,22),+this.volume.toFixed(2),!!(navigator.userActivation&&navigator.userActivation.isActive),+this.currentTime.toFixed(2),!!this.loop]);sv();return pl.apply(this,arguments)};"
        "P.pause=function(){L.push(['pause',(this.src||'').split('/').pop().slice(0,22),+this.currentTime.toFixed(1)]);sv();return pa.apply(this,arguments)}})();"
        "window.__say=[];try{speechSynthesis.speak=function(u){window.__say.push(u.text);setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "if(!sessionStorage.getItem('__set')){sessionStorage.setItem('__set','1');}")
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
def au(p): return p.evaluate("JSON.parse(sessionStorage.getItem('__au')||'[]')")
def plays(p, f='song-chant'): return [a for a in au(p) if a[0] == 'play' and a[1].startswith(f)]
def has(p): return p.evaluate("!!(window.CHANT&&CHANT.has())")
def playing(p): return p.evaluate("!!(window.CHANT&&CHANT.playing())")
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
def newpage(br):
    ctx = br.new_context(viewport={'width': 430, 'height': 900}, device_scale_factor=1)
    pg = ctx.new_page(); pg.add_init_script(INIT); return pg
STORE = "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}))"
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--autoplay-policy=document-user-activation-required'])
    # ---------------- (1) タイトル ----------------
    pg = newpage(br); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(1200)
    chk('起動直後(無操作)はタイトル画面・チャントは鳴らない・エラーなし', pg.evaluate("!document.getElementById('sTitle').hidden") and plays(pg) == [] and not has(pg) and pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    pg.mouse.click(215, 300); pg.wait_for_timeout(1500)   # タイトルのどこか(ボタン以外)を最初にタッチ
    pc = plays(pg)
    chk('タイトルの最初のタッチで song-chant.mp3 が鳴りはじめる(1回・ユーザー操作の中・先頭から・ループ)', len(pc) == 1 and pc[0][3] is True and pc[0][4] < 0.05 and pc[0][5] is True, pc)
    chk('音量は 0.2', len(pc) == 1 and abs(pc[0][2] - 0.2) < 0.01, pc)
    chk('実際に再生されている', playing(pg) is True)
    pg.mouse.click(215, 300); pg.mouse.click(100, 200); pg.wait_for_timeout(300)
    chk('何回タッチしても1つだけ(二重に鳴らない)', len(plays(pg)) == 1, plays(pg))
    chk('タイトルの最初のタッチ(画面全体が「はじめる」)で、先頭からやり直しもしない(再生は1回のまま)', len(plays(pg)) == 1 and not [a for a in au(pg) if a[0] == 'pause'], au(pg))
    chk('コマンド(はじめから・つづきから)が出ている(通常操作が妨げられない)', pg.evaluate("!document.getElementById('cmd').hidden"))
    pg.close()
    # ---------------- (1b) 最初のタッチが「はじめる」ボタン ----------------
    pg = newpage(br); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(1000)
    pg.click('#startBtn'); pg.wait_for_timeout(1200)
    pc = plays(pg)
    chk('最初のタッチが「はじめる」ボタンでも、そのタッチで先頭から鳴る(1回)', len(pc) == 1 and pc[0][3] is True and pc[0][4] < 0.05, pc)
    chk('そのとき「はじめから/つづきから」も出る', pg.evaluate("!document.getElementById('cmd').hidden"))
    # ---------------- (2) はじめから→tour/ へ ----------------
    pg.wait_for_timeout(2500)   # タイトルで少し鳴らしてから進む(続きから鳴る位置が0でないことを見るため)
    n0 = len(plays(pg))
    pg.click('#cNew'); pg.wait_for_url('**/tour/**', timeout=8000); pg.wait_for_timeout(1500)
    pc = plays(pg)
    chk('tour/ に進んだあと、チャントは鳴らない(ゲーム開始でタイトルの曲は止まる・085)', len(pc) == n0, pc)
    chk('tour/ に進んだ直後、チャントは再生されていない(広間の前も)', has(pg) is False)
    chk('継続用の一時メモ(kw-chant)は残らない', pg.evaluate("sessionStorage.getItem('kw-chant')") is None)
    # DAY 1 → 賢者の広間
    pg.mouse.click(215, 450); pg.wait_for_timeout(1500)
    sc = pg.evaluate("[document.querySelector('button.btn.go')!==null, window.CHANT.has()]")
    chk('DAY 1 のあと賢者の広間(最初の会話の「GO！」の前)でも、チャントは鳴っていない(場面の音に切り替わる)', sc == [True, False] and len(plays(pg)) == n0, [sc, plays(pg)])
    pg.evaluate("window.__ambDuck(true)"); pg.evaluate("window.__ambDuck(false)"); pg.wait_for_timeout(500)
    chk('マイクの出入りでも、チャントは再開しない', has(pg) is False and len(plays(pg)) == n0, plays(pg))
    pg.click('button.btn.go'); pg.wait_for_timeout(800)
    chk('最初の会話(GO！)が始まってもチャントは鳴らない', has(pg) is False)
    n = len(plays(pg))
    pg.evaluate("window.__ambDuck(true)"); pg.evaluate("window.__ambDuck(false)"); pg.wait_for_timeout(800)
    chk('止まったあと、マイク終了で再開しない', has(pg) is False and len(plays(pg)) == n)
    n = len(plays(pg))
    pg.evaluate("window.__ambDuck(true)"); pg.evaluate("window.__ambDuck(false)"); pg.wait_for_timeout(800)
    chk('止まったあと、マイク終了で再開しない', has(pg) is False and len(plays(pg)) == n)
    pg.wait_for_timeout(1500)
    chk('そのあとも鳴らない・テーマ曲も鳴っていない・エラーなし', has(pg) is False and plays(pg, 'song-theme') == [] and pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    txt = pg.evaluate("document.body.innerText")
    for w in ['勉強', 'テスト', '測定', '練習']:
        chk('画面に「%s」の言葉がない' % w, w not in txt)
    sv = pg.evaluate("JSON.stringify(Object.keys(localStorage))")
    chk('保存データにチャントの状態を書かない(localStorageにchant/song関連のキーがない)', 'chant' not in sv.lower() and 'song' not in sv.lower(), sv)
    pg.context.close()
    # ---------------- (3) タイトルを通らずに tour/ を開く: 広間のGO！で新たに始まらない ----------------
    pg = newpage(br); pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1200)
    chk('タイトルを通らない tour/ では、開いた直後も鳴らない', plays(pg) == [] and not has(pg))
    pg.mouse.click(215, 450); pg.wait_for_timeout(900)
    chk('賢者の広間 sage_1 が開いても鳴らない', pg.evaluate("document.querySelector('button.btn.go')!==null") and plays(pg) == [])
    pg.click('button.btn.go'); pg.wait_for_timeout(1500)
    chk('sage_1 の「GO！」でもチャントは新たに始まらない(旧トリガーは外した)', plays(pg) == [] and not has(pg), plays(pg))
    chk('エラーなし', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    pg.context.close()
    # ---------------- (4) 音オフ・古い引き継ぎ・つづきから・?map=1 ----------------
    pg = newpage(br); pg.goto(base + '/world/index.html'); pg.evaluate("localStorage.setItem('kd_snd','off')"); pg.reload(); pg.wait_for_timeout(800)
    pg.mouse.click(215, 300); pg.wait_for_timeout(600)
    chk('音オフのときは鳴らさない(エラーなし)', plays(pg) == [] and not has(pg) and pg.evaluate('window.__errs') == [])
    pg.context.close()
    pg = newpage(br); pg.goto(base + '/tour/index.html'); pg.evaluate("sessionStorage.setItem('kw-chant',JSON.stringify({t:3,at:Date.now()-60000}))"); pg.reload(); pg.wait_for_timeout(1000)
    chk('古い引き継ぎ(15秒より前)は使わない・消える', plays(pg) == [] and pg.evaluate("sessionStorage.getItem('kw-chant')") is None)
    pg.context.close()
    pg = newpage(br); pg.goto(base + '/world/index.html?map=1'); pg.wait_for_timeout(1000); pg.mouse.click(215, 300); pg.wait_for_timeout(500)
    chk('タイトルを通らない開き方(?map=1)では鳴らない', plays(pg) == [] and not has(pg))
    pg.context.close()
    # つづきから: 記録がある状態でタイトル→つづきから→チャントが止まる
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); pg = ctx.new_page(); pg.add_init_script(INIT)
    pg.goto(base + '/world/index.html'); pg.evaluate("(function(){var k=Object.keys(localStorage);})()")
    pg.evaluate("localStorage.setItem('kanpe-world-v1',JSON.stringify({v:1,at:'haneda',cleared:{haneda:1,guam:1},seen:{a:1,b:1}}))"); pg.reload(); pg.wait_for_timeout(1000)
    pg.mouse.click(215, 300); pg.wait_for_timeout(1000)
    ok1 = has(pg)
    pg.evaluate("sessionStorage.removeItem('kw-started')")
    cc = pg.evaluate("document.getElementById('cCont').getAttribute('aria-disabled')")
    pg.click('#cCont'); pg.wait_for_timeout(600)
    chk('つづきから(地図へ)でチャントが止まる', ok1 is True and cc == 'false' and has(pg) is False, [ok1, cc])
    chk('エラーなし(つづきから)', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    ctx.close()
    # ---------------- ループ: タイトルで曲の終わりを過ぎても鳴っている ----------------
    pg = newpage(br); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(600)
    pg.evaluate("""(function(){var P=HTMLMediaElement.prototype,pl=P.play;window.__els=[];P.play=function(){window.__els.push(this);return pl.apply(this,arguments)}})()""")
    pg.mouse.click(215, 300); pg.wait_for_timeout(800)
    d = pg.evaluate("(function(){var e=window.__els[0];return [e.loop,+e.duration.toFixed(1)]})()")
    chk('タイトルではループする(loop=true・51秒の曲)', d[0] is True and abs(d[1] - 51.4) < 0.5, d)
    pg.evaluate("(function(){var e=window.__els[0];e.currentTime=e.duration-0.4})()"); pg.wait_for_timeout(1500)
    lp = pg.evaluate("(function(){var e=window.__els[0];return [e.paused,e.ended,+e.currentTime.toFixed(1),CHANT.playing()]})()")
    chk('曲の終わりを過ぎても止まらず先頭に戻って鳴っている', lp[0] is False and lp[1] is False and lp[2] < 5 and lp[3] is True, lp)
    pg.context.close()
    # ---------------- iPhone(Safari): audio.volume が効かないので Web Audio のゲイン(0.2)を通す(要素の音量は 1) ----------------
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1,
                         user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
    pg = ctx.new_page(); pg.add_init_script(INIT); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800); pg.mouse.click(195, 300); pg.wait_for_timeout(1000)
    pc = plays(pg)
    chk('iPhone: チャントは Web Audio のゲインを通して鳴る(要素の音量は1・タイトルで1回)', len(pc) == 1 and pc[0][2] == 1 and has(pg), pc)
    ctx.close()
    # ---------------- 素材が読める(world/ からも tour/ からも) ----------------
    pg = newpage(br); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(300)
    code = pg.evaluate("fetch('../tour/assets/song/song-chant.mp3').then(function(r){return r.status})")
    chk('素材が読める: ../tour/assets/song/song-chant.mp3(world/ から)', code == 200, code)
    br.close()
print('\nNG=%d' % len(bad)); sys.exit(1 if bad else 0)
