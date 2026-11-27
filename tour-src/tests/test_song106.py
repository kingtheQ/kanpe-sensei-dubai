# -*- coding: utf-8 -*-
"""タスク106-A の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_song106.py
タイトルの「せつめいを きく」の下に「うたを うたう」。押すと歌詞パネル(英文のみ・21行・[開始秒,行]の表)。チャントは止めない・頭出ししない。
再生位置(currentTime)に合わせて1行ずつ強調。歌詞表の時刻は初版の近似(曲51秒の中)。発音課題・採点・マイクはなし。
実機の音・実機の自動再生・実際の歌との合い具合は確認できない(実機でキングが秒を調整する前提)。"""
import os, sys, re
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, 'flow025'))
from play import serve, ROOT
from playwright.sync_api import sync_playwright
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
LYR = """Hey, Lulu! (Hey, Lulu!)
Are you ready? (I am ready!)
One, two, three, go!
Pack my bag (Pack my bag!)
Sky is blue (Sky is blue!)
Every airport (Every airport!)
Waits for you (Waits for you!)
This is my promise, Lulu
We will travel around the world together
And have fun every day
My body is healthy, my mind is calm
I eat good food, sleep well
And never push too hard
When I feel afraid
I breathe and think of you
We both help each other
Let's see every village
Hear every voice
Share every little treasure
Thank you for being here
Let's go, let's go, let's go!""".split('\n')
# 再生を記録し、currentTime を外から動かせる偽の再生(本物のmp3のデコードに頼らない)
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "(function(){var P=HTMLMediaElement.prototype,pl=P.play,pa=P.pause;var L=[];window.__au=L;"
        "P.play=function(){L.push(['play',(this.src||'').split('/').pop().slice(0,22),+this.currentTime.toFixed(2),!!this.loop]);return pl.apply(this,arguments)};"
        "P.pause=function(){L.push(['pause',(this.src||'').split('/').pop().slice(0,22)]);return pa.apply(this,arguments)}})();"
        "window.__say=[];try{speechSynthesis.speak=function(u){window.__say.push(u.text);setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}")
def hl(pg):
    return pg.evaluate("()=>{var a=[].map.call(document.querySelectorAll('#sBox .sl'),function(d){return d.classList.contains('on')});var i=a.indexOf(true);return {n:a.length,on:a.filter(Boolean).length,i:i}}")
with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 375, 'height': 667}); ctx.add_init_script(INIT)
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
    pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800)
    pg.click('#startBtn'); pg.wait_for_timeout(500)
    # ---- ボタンの位置と文言 ----
    order = pg.evaluate("()=>[].map.call(document.querySelectorAll('#cmdMain > button'),function(b){return b.id+':'+b.textContent.replace('▶','')})")
    chk('A1 「せつめいを きく」の直下に「うたを うたう」(はじめから・つづきから・せつめいを きく・うたを うたう の順)', order[:4] == ['cNew:はじめから', 'cCont:つづきから', 'cNarr:せつめいを きく', 'cSong:うたを うたう'], order)
    # ---- 歌詞表(データ) ----
    T = pg.evaluate("()=>window.SONG_LYRICS")
    ts = [r[0] for r in T]
    chk('A2 歌詞表は [開始秒, 行] の21行で、指示書の歌詞の全文・順序どおり(括弧内の掛け声つき・節の見出しなし)', [r[1] for r in T] == LYR and len(T) == 21 and not any('[' in r[1] for r in T), len(T))
    chk('A3 歌詞表の時刻は昇順・0秒始まりで、すべて曲の長さ(51秒)の内側に収まっている', ts[0] == 0 and ts == sorted(ts) and len(set(ts)) == len(ts) and all(0 <= t < 51 for t in ts), (ts[0], ts[-1]))
    chk('A3b 最後の行にも1.5秒以上の表示時間がある(51秒の曲の終わりまで)', 51 - ts[-1] >= 1.5, 51 - ts[-1])
    # ---- チャント: 最初のタッチ(startBtn)で鳴っている ----
    au = pg.evaluate("()=>window.__au")
    chk('B0 タイトルの最初のタッチでチャントが先頭から鳴る(既存どおり)', any(a[0] == 'play' and 'song-chant' in a[1] for a in au) and pg.evaluate("()=>CHANT.has()"), au)
    n_before = len(pg.evaluate("()=>window.__au"))
    # ---- パネルを開く ----
    pg.evaluate("()=>{var e=[...document.querySelectorAll('audio')]}")
    pg.click('#cSong'); pg.wait_for_timeout(400)
    st = pg.evaluate("()=>({song:!document.getElementById('cmdSong').hidden,main:document.getElementById('cmdMain').hidden,txt:document.getElementById('cmdSong').innerText,close:document.getElementById('cSongClose').textContent.replace('▶','').trim()})")
    chk('A4 押すと歌詞パネルが開く(ほかの項目は隠れる)・「とじる」ボタンがある', st['song'] and st['main'] and st['close'] == 'とじる', st['close'])
    body = pg.evaluate("()=>[].map.call(document.querySelectorAll('#sBox .sl'),function(d){return d.textContent})")
    chk('A5 パネルの歌詞は21行の英文だけ(日本語・説明・見出しなし)・発音課題/採点/マイクの部品なし', body == LYR and not re.search(r'[぀-ヿ一-鿿]', ''.join(body)) and not pg.evaluate("()=>!!document.querySelector('#cmdSong .mic,#cmdSong .stat,#cmdSong .cue,#cmdSong [data-mic]')"), len(body))
    after = pg.evaluate("()=>window.__au")[n_before:]
    chk('B1 パネルを開いてもチャントは止めない・頭出ししない(pause も 先頭からの play も増えない)', not any(a[0] == 'pause' for a in after) and not any(a[0] == 'play' and a[2] < 0.05 for a in after) and pg.evaluate("()=>CHANT.has()"), after)
    # ---- 再生位置に合わせた強調: currentTime を動かして確認 ----
    def seek(t):
        pg.evaluate("(t)=>{var e=null;try{e=window.__chantEl}catch(x){}}", t)
    # 実際の Audio 要素を取り出せないので、CHANT.time を差し替えて検証(本体の時刻→行の対応を見る)
    pg.evaluate("()=>{window.__t=3;window.__ot=CHANT.time;CHANT.time=function(){return window.__t}}")
    res = []
    for t, want in [(0.0, 0), (1.9, 0), (2.0, 1), (4.5, 2), (9.0, 4), (15.0, 7), (30.0, 11), (31.0, 12), (47.6, 19), (50.9, 20), (-1, -1)]:
        pg.evaluate("(t)=>{window.__t=t}", t); pg.wait_for_timeout(260)
        h = hl(pg); res.append((t, h['i'], want))
    chk('A6 再生位置に合わせて、1行だけが強調される(表の秒の境界どおりに1行ずつ進む)', all(i == w for _, i, w in res) and all(True for _ in res), res)
    pg.evaluate("()=>{window.__t=-1}"); pg.wait_for_timeout(260)
    h = hl(pg)
    chk('A7 鳴っていない(再生位置なし)ときは、どの行も強調しない', h['on'] == 0, h)
    # 表を直すだけで時刻が変わる: SONG_LYRICS の1行の秒を変えると強調の切り替わりが変わる
    pg.evaluate("()=>{window.SONG_LYRICS[1][0]=3;window.__t=2.5}"); pg.wait_for_timeout(260)
    chk('A8 直すのは表の秒だけ: 表の秒を変えると、強調の切り替わりも変わる', hl(pg)['i'] == 0, hl(pg))
    pg.evaluate("()=>{window.SONG_LYRICS[1][0]=2}")
    # 強調中の行が見えている(パネル内にスクロールされる)
    pg.evaluate("()=>{window.__t=47.6}"); pg.wait_for_timeout(300)
    vis = pg.evaluate("()=>{var b=document.getElementById('sBox').getBoundingClientRect(),e=document.querySelector('#sBox .sl.on').getBoundingClientRect();return e.top>=b.top-1&&e.bottom<=b.bottom+1}")
    chk('A9 強調している行は、パネルの中で見えている位置にスクロールされる', vis)
    r = pg.evaluate("()=>{var w=document.getElementById('cmdSong').getBoundingClientRect();return {top:Math.round(w.top),bottom:Math.round(w.bottom),H:innerHeight}}")
    chk('A10 パネルは画面(375×667)の中に収まる', r['top'] >= 0 and r['bottom'] <= r['H'], r)
    pg.screenshot(path='/tmp/song106-panel.png')
    # ---- 閉じる ----
    pg.evaluate("()=>{CHANT.time=window.__ot}")
    pg.click('#cSongClose'); pg.wait_for_timeout(300)
    st = pg.evaluate("()=>({song:document.getElementById('cmdSong').hidden,main:document.getElementById('cmdMain').hidden})")
    after2 = pg.evaluate("()=>window.__au")[n_before:]
    chk('A11 「とじる」で元のメニューに戻る・チャントは流れ続ける(止めない)', st['song'] and not st['main'] and not any(a[0] == 'pause' for a in after2) and pg.evaluate("()=>CHANT.has()"), after2)
    chk('A12 エラーなし', not errs and not pg.evaluate("()=>window.__errs"), errs)
    pg.screenshot(path='/tmp/song106-menu.png')
    ctx.close()
    # ---- 最初のタッチ前にパネルを開く(チャントがまだ鳴っていない) ----
    ctx = br.new_context(viewport={'width': 375, 'height': 667}); ctx.add_init_script(INIT)
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
    pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{document.getElementById('startBtn').hidden=true;document.getElementById('cmd').hidden=false}")   # タッチなしでメニューを出す(自動再生制限の再現)
    pg.wait_for_timeout(200)
    pre = pg.evaluate("()=>[window.__au.length,CHANT.has()]")
    pg.click('#cSong'); pg.wait_for_timeout(500)
    au = pg.evaluate("()=>window.__au")
    chk('B2 最初のタッチ前は鳴っていない→「うたを うたう」のタッチをきっかけに、先頭から鳴り始める(1つだけ)', pre == [0, False] and len([a for a in au if a[0] == 'play']) == 1 and pg.evaluate("()=>CHANT.has()"), (pre, au))
    chk('B3 エラーなし', not errs and not pg.evaluate("()=>window.__errs"), errs)
    ctx.close()
    # ---- 音オフのとき: 鳴らさない(既存の扱いを壊さない)・パネルは開ける ----
    ctx = br.new_context(viewport={'width': 375, 'height': 667}); ctx.add_init_script(INIT + "localStorage.setItem('kd_snd','off');")
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
    pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800); pg.click('#startBtn'); pg.wait_for_timeout(300); pg.click('#cSong'); pg.wait_for_timeout(400)
    chk('B4 音オフ: パネルは開くが、チャントは鳴らさない・どの行も強調しない・エラーなし', not pg.evaluate("()=>document.getElementById('cmdSong').hidden") and not any(a[0] == 'play' for a in pg.evaluate("()=>window.__au")) and hl(pg)['on'] == 0 and not errs, errs)
    ctx.close()
    # ---- 既存の動き: 「せつめいを きく」・モード選択は変わらない ----
    ctx = br.new_context(viewport={'width': 375, 'height': 667}); ctx.add_init_script(INIT)
    pg = ctx.new_page(); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800); pg.click('#startBtn'); pg.wait_for_timeout(300)
    pg.click('#cNarr'); pg.wait_for_timeout(400)
    chk('B5 「せつめいを きく」は従来どおり語りが流れる(歌詞パネルは開かない)', pg.evaluate("()=>window.__say.length>0") and pg.evaluate("()=>document.getElementById('cmdSong').hidden"))
    ctx.close()
    # ---- 「復習」「テスト」「測定」の語 ----
    w = open(os.path.join(ROOT, 'world/index.html'), encoding='utf-8').read()
    i0, i1 = w.index('id="cmdSong"'), w.index('id="cmdAsk"')
    chk('B6 歌詞パネルの表示に「復習」「テスト」「測定」「練習」の語がない', not any(k in w[i0:i1] for k in ['復習', 'テスト', '測定', '練習']))
print()
print('すべて OK  (NG 0件)' if not bad else '失敗あり  (NG %d件)' % len(bad)); sys.exit(1 if bad else 0)
