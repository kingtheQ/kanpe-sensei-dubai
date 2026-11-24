# -*- coding: utf-8 -*-
"""タスク076 の動作確認(ヘッドレス)。使い方: python3 -I tour-src/tests/test_showtime076.py
プールサイドのショータイム格上げ: (1)歌詞表21行(昇順・0〜74.6・正本と一致) (2)再生中の切り替えに正面を挟む [歌う絵1→正面→歌う絵2→正面]
(3)呼びかけ台詞が曲より前に say() され、読み終わってから曲が始まる(読み上げが使えない環境では約1秒で先へ進む) (4)歌詞が曲の再生位置に連動して1行ずつ出る(止まれば追随して止まる・曲が止まれば消える)
(5)ステージ照明(光の円錐・足もとの光だまり・キラキラ)は曲が鳴っているあいだだけ描かれ、shadowBlur を使わない
実曲と歌詞の同期の聞こえ方・照明の実機での見え方・読み上げの聞こえ方は確認できない(未確認)。"""
import os, sys, re, json, base64, io, threading, http.server, socketserver
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tour-src'))
import song_data
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
# ---- 歌詞の正本(指示書076。declaration-song-suno.md パターン1) ----
CANON = ["Pack my bag, the sky is blue", "Every airport waits for you", "Step by step, and mile by mile", "I will say it with a smile",
 "This is my promise, Lulu", "We will travel around the world together", "And have fun every day", "My body is healthy, my mind is calm", "I eat good food, sleep well", "And never push too hard", "When I feel afraid", "I breathe and think of you", "We both help each other",
 "Let's see every village", "Hear every voice", "Share every little treasure", "Thank you for being here",
 "This is my promise, Lulu", "We will travel around the world together", "And have fun every day", "Let's go, let's go!"]
LY = song_data.SONG_SCENE['lyrics']
chk('歌詞表は21行', len(LY) == 21, len(LY))
chk('歌詞の時刻は昇順(重複なし)', all(LY[i][0] < LY[i + 1][0] for i in range(20)))
chk('歌詞の時刻は 0〜74.6 の範囲', all(0 <= t < 74.6 for t, _ in LY), (LY[0][0], LY[-1][0]))
chk('歌詞の文言は正本と一致(順序も)', [x[1] for x in LY] == CANON)
chk('歌詞は英語のみ(日本語を含まない)', all(re.search(r'[぀-ヿ一-鿿]', x[1]) is None for x in LY))
chk('節のまとまり: 各行の間隔は 1.5〜6 秒(詰め込み・間延びなし)', all(1.5 <= LY[i + 1][0] - LY[i][0] <= 6 for i in range(20)))
C = song_data.SONG_SCENE['call']
chk('呼びかけ台詞の文言', C['en'] == 'Come on, everybody — sing with me!', C)
src = open(os.path.join(ROOT, 'tour-src/art.js'), encoding='utf-8').read()
chk('artStage: 再生中の切り替えに正面(fi)が含まれる [ai,fi,bi,fi]', '[ai,fi,bi,fi]' in src)
sp = src[src.index('function artSpot('):src.index('/* 大きさを指定して描く artSway')]
chk('照明の描画コード(円錐・光だまり・キラキラ)が art.js にある', 'ca.lineTo' in sp and 'ca.ellipse' in sp and 'fillRect' in sp and 'if(H.spot)artSpot(sg,1)' in src and 'if(H.spot)artSpot(sg,2)' in src)
chk('照明はコードの描画だけ(shadowBlur・グラデーション・filter なし)', not re.search(r'shadowBlur|createLinearGradient|createRadialGradient|ca\.filter', sp))
sj = open(os.path.join(ROOT, 'tour-src/song.js'), encoding='utf-8').read()
a = sj.index('function onGo()'); body = sj[a:a + 4000]
bg_ = body.index('function begin()'); chk('呼びかけの say() の完了(gd(begin))から songStart する(begin の中で曲を始める)', "songStart('theme',onSong)" in body[bg_:body.index('var c=d.call')] and body.index('say(c.en') > body.index('function begin()'))
chk('曲は呼びかけの読み終わり(say の完了)から始まる(begin を完了に渡す)', 'say(c.en,.9,S.pitch,gd(begin))' in body)
# ---- 画面で ----
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,SONG:SONG,songBeatN:songBeatN,PBY:PBY,setMode:setMode,showMap:showMap,ART:ART};" + HOOK, 1))
# speak を手動で終わらせる版(HOLD): 読み上げが終わるまで曲が始まらないことを見る
INIT_HOLD = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
 "window.__au=[];(function(){var P=HTMLMediaElement.prototype,pl=P.play;P.play=function(){window.__au.push(['play',(this.src||'').split('/').pop().slice(0,22),+this.currentTime.toFixed(2)]);return pl.apply(this,arguments)}})();"
 "window.__say=[];window.__held=[];try{speechSynthesis.speak=function(u){window.__say.push(u.text);if(window.__hold){window.__held.push(u)}else setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
 "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
 "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));")
INIT_NOTTS = INIT_HOLD + "try{delete window.SpeechSynthesisUtterance}catch(e){}window.SpeechSynthesisUtterance=undefined;"
def plays(p): return [a for a in p.evaluate("window.__au") if a[0] == 'play' and a[1].startswith('song-theme')]
def canvas(p): return Image.open(io.BytesIO(base64.b64decode(p.evaluate("document.getElementById('sceneA').toDataURL('image/png')").split(',')[1]))).convert('RGB')
def msg(p): return p.evaluate("document.querySelector('#msgText').innerText").strip()
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
def newpage(br, init):
    ctx = br.new_context(viewport={'width': 430, 'height': 900}, device_scale_factor=1); pg = ctx.new_page(); pg.add_init_script(init); pg.route('**/tour/index.html', hooked); return pg
def go(pg):
    pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1200); pg.mouse.click(215, 450); pg.wait_for_timeout(800)
    pg.evaluate("(function(){var T=__T;T.save.ticket='ow';['nbo_immig1','nbo_bag1','nbo_sim1','nbo_taxi1'].forEach(function(v){T.save.seen[v]=1});T.setMode('arr');T.showMap()})()"); pg.wait_for_timeout(400)
    pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1500); pg.click('button.dq:nth-child(1)'); pg.wait_for_timeout(1500); pg.click('#songNotice'); pg.wait_for_timeout(500)
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--autoplay-policy=document-user-activation-required'])
    # ---- 呼びかけ → 読み終わってから曲 ----
    pg = newpage(br, INIT_HOLD); go(pg)
    pg.evaluate("window.__hold=1"); pg.click('button.btn.go'); pg.wait_for_timeout(700)
    chk('「GO！」のあと、歌手の呼びかけが表示される(話者=ラウンジの歌手)', msg(pg) == C['en'] and pg.evaluate("document.querySelector('#who').innerText").strip() == 'ラウンジの歌手', msg(pg))
    chk('呼びかけが say() で読み上げられた', C['en'] in pg.evaluate("window.__say"))
    chk('読み上げのあいだ(読み終わる前)は曲が始まっていない', plays(pg) == [] and pg.evaluate("__T.SONG.el") is None)
    pg.evaluate("(function(){window.__hold=0;var h=window.__held.splice(0);h.forEach(function(u){if(u.onend)u.onend({})})})()"); pg.wait_for_timeout(600)
    chk('読み終わってから song-theme.mp3 が1回だけ鳴りはじめる', len(plays(pg)) == 1, plays(pg))
    sayidx = pg.evaluate("window.__say").index(C['en']); chk('呼びかけ以外の読み上げ(ルルの一言)が先に1つある=流れは 入り→ルル→GO→呼びかけ→曲', sayidx == pg.evaluate("window.__say").index(C['en']) and pg.evaluate("window.__say")[sayidx - 1].startswith('Look, King'), pg.evaluate("window.__say"))
    # ---- 歌詞: 再生位置に連動 ----
    pg.evaluate("(function(){var e=__T.SONG.el;e.pause();window.__fake=e;window.__ct=0;Object.defineProperty(e,'currentTime',{get:function(){return window.__ct},configurable:true});Object.defineProperty(e,'paused',{get:function(){return false},configurable:true})})()")
    def at(ct, wait=350):
        pg.evaluate("window.__ct=%f" % ct); pg.wait_for_timeout(wait); return msg(pg)
    chk('最初の行の前は「♪」のまま', at(1.0) == '♪')
    res = [(ct, at(ct)) for ct in [LY[0][0] + .1, LY[4][0] + .1, LY[5][0] + 1, LY[12][0] + .5, LY[16][0] + .5, LY[20][0] + .5, 74.0]]
    exp = [CANON[0], CANON[4], CANON[5], CANON[12], CANON[16], CANON[20], CANON[20]]
    chk('再生位置ごとに、その時刻の歌詞が1行ずつ画面下のメッセージ欄に出る', [r[1] for r in res] == exp, res)
    held = at(LY[8][0] + .2); chk('曲が一時停止のとき(位置が動かない)は、表示も同じ行のまま', held == CANON[8] and at(LY[8][0] + .2, 600) == CANON[8])
    chk('位置が進めば、続きから追随する', at(LY[9][0] + .2) == CANON[9])
    chk('歌詞の表示は英語のみ・話者名は空', not re.search(r'[぀-ヿ一-鿿]', msg(pg)) and pg.evaluate("document.querySelector('#who').innerText").strip() == '')
    # ---- 照明: 曲が鳴っているあいだだけ ----
    pg.evaluate("window.__ct=%f" % (LY[2][0] + .2)); pg.wait_for_timeout(1800); on = canvas(pg); on.save('/tmp/showtime076-on.png')
    chk('エラーなし(曲の最中)', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    # 曲をやめる(出口ボタン)→ 表示が消え、照明が消える。もう一度入って鳴らさずに撮る
    pg.click('#exitBtn'); pg.wait_for_timeout(500)
    chk('場面を離れると曲が止まる(歌詞表示も出ない)', pg.evaluate("__T.SONG.el") is None and pg.evaluate("__T.G.view") == 'map')
    pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1500); pg.click('button.dq:nth-child(1)'); pg.wait_for_timeout(2500); off = canvas(pg); off.save('/tmp/showtime076-off.png')
    A = np.array(on).astype(int); Bm = np.array(off).astype(int)
    def lift(box):  # 範囲内で、鳴っているときのほうが明るい画素の平均の差(R+G+B)
        x0, y0, x1, y1 = box; return float((A[y0:y1, x0:x1].sum(2) - Bm[y0:y1, x0:x1].sum(2)).mean())
    cone_lift = lift((740, 200, 840, 440))
    dd = (A[704:764, 620:960].sum(2) - Bm[704:764, 620:960].sum(2)); pool_px = int((dd > 12).sum())
    chk('足もとの光だまり: 曲が鳴っているときだけ足もと(楕円の域)が明るい(明るくなった画素が 1500 以上)', pool_px >= 1500, pool_px)
    chk('光の円錐: 曲が鳴っているときだけ歌手の上方が明るい', cone_lift > 4, round(cone_lift, 1))
    # 観客・ルル・キングは光に隠れない: 曲が鳴っている絵(on)で、各人物の足もとの側(腰から下は揺れない)の素材の画素が、そのまま描かれている
    st = pg.evaluate("JSON.parse(JSON.stringify(__T.ART.npool.stage))"); AR = os.path.join(ROOT, 'tour/assets/art/npc')
    figs = [(q['n'], q['x'], q['by']) for q in st['people']] + [(st['lulu']['n'], st['lulu']['x'], st['lulu']['by']), (st['king']['n'], st['king']['x'], st['king']['by'])]
    fr = []
    for n, x, by in figs:   # 曲が鳴っていないとき(off)と比べる。腰から下は揺れないので、光だけが違いを生む
        sp_ = Image.open(os.path.join(AR, n + '.png')).convert('RGBA'); x0 = int(x - sp_.width / 2 + .5); y0 = by - sp_.height; h0 = int(sp_.height * .7)
        a_ = A[y0 + h0:by, x0:x0 + sp_.width]; b_ = Bm[y0 + h0:by, x0:x0 + sp_.width]; m_ = np.array(sp_)[h0:][..., 3] == 255
        fr.append(round(float((np.abs(a_ - b_).sum(2)[m_] <= 12).mean() * 100), 1) if m_.any() else 100.0)
    chk('観客5人・ルル・キング: 曲が鳴っていないときと腰から下の画素が同じ(98% 以上=光に隠れない・色を変えない)', min(fr) >= 98, fr)
    xs = re.findall(r'\[(-?\d+),(-?\d+),[\d.]+\]', re.search(r'var S0=(\[.*?\]\]);', sp).group(1) + ']')
    pts = [(790 + int(a), 734 + int(b) - 60) for a, b in xs]
    chk('キラキラの位置は歌手の体(x±110・y484〜734)に重ならない', all(not (680 <= px <= 900 and 480 <= py <= 740) for px, py in pts), pts)
    chk('キラキラは観客の頭(y>600)より上の空の側だけ', all(py < 640 for px, py in pts), max(py for px, py in pts))
    pg.context.close()
    # ---- 読み上げが使えない環境: 約1秒で曲に進む(止まらない) ----
    pg = newpage(br, INIT_NOTTS); go(pg); pg.click('button.btn.go'); pg.wait_for_timeout(400)
    chk('読み上げなし: 呼びかけは表示され、まだ曲は始まっていない(短い待ち)', msg(pg) == C['en'] and plays(pg) == [], msg(pg))
    pg.wait_for_timeout(1400)
    chk('読み上げなし: 約1秒の待ちのあと曲が始まる(止まらない)', len(plays(pg)) == 1, plays(pg))
    chk('エラーなし(読み上げなし)', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    pg.context.close()
    # ---- 音オフ: 曲なしで先へ(既存どおり) ----
    pg = newpage(br, INIT_HOLD + "localStorage.setItem('kd_snd','off');"); go(pg); pg.click('button.btn.go'); pg.wait_for_timeout(1200)
    chk('音オフ: 曲は鳴らず「つぎへ」で先へ進める', plays(pg) == [] and pg.evaluate("!!document.querySelector('.songnext')") is True)
    pg.context.close(); br.close()
print('FAILED: %s' % bad if bad else 'ALL OK')
sys.exit(1 if bad else 0)
