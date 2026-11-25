# -*- coding: utf-8 -*-
"""タスク085 A・B・C・D の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_narr085.py
A: タイトルのチャントは、ゲーム開始(はじめから→tour/)で止まり、tour/ でも鳴らない・kw-chant を残さない
B: 「せつめいを きく」を聞いた回は「はじめから」で説明を流さない(ボタンからは何度でも聞ける)。流れている最中に「はじめから」→二重に始めず、語り終えてから進む。保存データに何も書かない
C: OPENING_NARRATION が指示書C項の全文と一字一句同じ
D: 速さ 1.12・高さ 1.05(定数 NARR_RATE/NARR_PITCH)"""
import os, sys, re, threading, http.server, socketserver
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv
C_TEXT = 'ようこそ！空港えいご物語へ！これからあなたはキングとして、相棒のルルと一緒に世界一周の旅にでます。ルルはあなたをサポートしてくれる。キングとして大きな声で口の筋肉を鍛える、その耳で音を聞いて相手のリズムを体感してください。ただそれだけ。はじめて聞く英語は、意味がわからなくて戸惑うかもしれません。でも、キングの使命はひたすら発音すること。言えないときは、相棒のルルが助けてくれます。やっていて、意味がわからないし、合っているかも分からないと思うでしょう。でも安心してください。あなたの耳と口の筋肉が、自然に覚えていきます。気にしないで、どんどん世界を旅してください。楽しんでいってらっしゃい！'
# 発話は SLOW ミリ秒かけて終わる(「流れている最中」を作るため)
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
 "(function(){var P=HTMLMediaElement.prototype,pl=P.play;var L=JSON.parse(sessionStorage.getItem('__au')||'[]');"
 "P.play=function(){L.push(['play',(this.src||'').split('/').pop().slice(0,22)]);try{sessionStorage.setItem('__au',JSON.stringify(L))}catch(e){}return pl.apply(this,arguments)}})();"
 "window.__say=[];window.SLOW=600;try{speechSynthesis.speak=function(u){window.__say.push({t:u.text,r:u.rate,p:u.pitch,l:u.lang});try{sessionStorage.setItem('__sc',String(+(sessionStorage.getItem('__sc')||0)+1))}catch(e){};window.__cur=u;setTimeout(function(){if(window.__cur===u&&u.onend){window.__cur=null;u.onend({})}},window.SLOW)};speechSynthesis.cancel=function(){window.__cur=null}}catch(e){}"
 "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}")
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
def plays(p): return [a for a in p.evaluate("JSON.parse(sessionStorage.getItem('__au')||'[]')") if a[0] == 'play' and a[1].startswith('song-chant')]
def newpage(br):
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); pg = ctx.new_page(); pg.add_init_script(INIT); return pg
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
w = open(os.path.join(ROOT, 'world/index.html'), encoding='utf-8').read()
m = re.search(r"var OPENING_NARRATION='([^']*)'", w)
chk('C 説明文が指示書C項の全文と一字一句同じ', bool(m) and m.group(1) == C_TEXT and w.count('OPENING_NARRATION=') == 1)
chk('D 定数 NARR_RATE=1.12 / NARR_PITCH=1.05 を使う(voice の選び方は変えない)', 'NARR_RATE=1.12' in w and 'NARR_PITCH=1.05' in w and 'u.rate=NARR_RATE' in w and 'u.pitch=NARR_PITCH' in w)
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--autoplay-policy=document-user-activation-required'])
    # --- シナリオ1: 説明を聞かずに「はじめから」→ 説明1回 → tour/ ---
    pg = newpage(br); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800)
    pg.mouse.click(215, 300); pg.wait_for_timeout(800)
    n0 = len(plays(pg)); chk('A0 タイトルでチャントが鳴っている', n0 == 1, plays(pg))
    pg.click('#cNew'); pg.wait_for_url('**/tour/**', timeout=10000); pg.wait_for_timeout(1200)
    say = pg.evaluate("window.__say")   # tour/ では新しいページ(聞き取りの発話は別)
    chk('A1 tour/ に進んだあと、チャントは鳴らない・kw-chant を残さない', len(plays(pg)) == n0 and pg.evaluate("!!(window.CHANT&&CHANT.has())") is False and pg.evaluate("sessionStorage.getItem('kw-chant')") is None, plays(pg))
    pg.close()
    # --- シナリオ2: 「せつめいを きく」→ 聞き終わる → 「はじめから」: 二重に流さない ---
    pg = newpage(br); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800)
    pg.mouse.click(215, 300); pg.wait_for_timeout(500)
    pg.click('#cNarr'); pg.wait_for_timeout(1500)   # 600ms で語り終わる
    s1 = pg.evaluate("window.__say")
    chk('B1 「せつめいを きく」で説明が1回流れる(ja-JP・速さ1.12・高さ1.05)', len(s1) == 1 and s1[0]['l'] == 'ja-JP' and abs(s1[0]['r'] - 1.12) < 0.001 and abs(s1[0]['p'] - 1.05) < 0.001 and s1[0]['t'] == C_TEXT, s1[:1] and {k: s1[0][k] for k in 'rpl'})
    pg.click('#cGo') if pg.evaluate("!document.getElementById('cmdNarr').hidden") else None
    pg.wait_for_timeout(300)
    pg.click('#cNew'); pg.wait_for_url('**/tour/**', timeout=6000)
    chk('B2 聞いたあとの「はじめから」では説明を流さず、すぐ tour/ へ(二重再生なし・発話は通しで1回のまま)', pg.evaluate("sessionStorage.getItem('__sc')") == '1', pg.evaluate("sessionStorage.getItem('__sc')"))
    pg.close()
    pg = newpage(br); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800)
    pg.mouse.click(215, 300); pg.wait_for_timeout(500)
    pg.click('#cNarr'); pg.wait_for_timeout(1500)
    pg.evaluate("window.SLOW=60000")
    pg.click('#cNew') if pg.evaluate("!document.getElementById('cmdMain').hidden") else None
    pg.wait_for_timeout(500)
    cnt = int(pg.evaluate("sessionStorage.getItem('__sc')"))
    chk('B2b 聞いたあとの「はじめから」で、説明をもう一度は流さない(発話の数が増えない・URLは tour/)', cnt == 1 and '/tour/' in pg.url, [cnt, pg.url])
    pg.close()
    # --- シナリオ3: ボタンから何度でも ---
    pg = newpage(br); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800)
    pg.mouse.click(215, 300); pg.wait_for_timeout(500)
    for i in range(3):
        pg.click('#cNarr'); pg.wait_for_timeout(1200)
        if pg.evaluate("!document.getElementById('cmdNarr').hidden"): pg.click('#cGo'); pg.wait_for_timeout(200)
    chk('B3 「せつめいを きく」は何度でも聞ける(3回押して3回流れる)', pg.evaluate("window.__say.length") == 3, pg.evaluate("window.__say.length"))
    pg.close()
    # --- シナリオ4: 流れている最中に「はじめから」→ 二重に始めず、語り終えてから進む ---
    pg = newpage(br); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800)
    pg.mouse.click(215, 300); pg.wait_for_timeout(500)
    pg.evaluate("window.SLOW=1500"); pg.click('#cNarr'); pg.wait_for_timeout(300)
    pg.evaluate("document.getElementById('cmdMain').hidden=false"); pg.click('#cNew'); pg.wait_for_timeout(300)
    chk('B4 流れている最中の「はじめから」は説明をもう一度始めない(発話1つ)・まだ tour/ に進まない', pg.evaluate("window.__say.length") == 1 and '/tour/' not in pg.url, [pg.evaluate("window.__say.length"), pg.url])
    pg.wait_for_url('**/tour/**', timeout=6000)
    chk('B4b 語り終えたあとに tour/ へ進み、発話は通しで1回のまま', pg.evaluate("sessionStorage.getItem('__sc')") == '1', pg.evaluate("sessionStorage.getItem('__sc')"))
    pg.close()
    pg = newpage(br); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800)
    pg.mouse.click(215, 300); pg.wait_for_timeout(500); pg.click('#cNarr'); pg.wait_for_timeout(1200)
    ks = pg.evaluate("JSON.stringify(Object.keys(localStorage))+JSON.stringify(Object.keys(sessionStorage))")
    chk('B5 保存データ・セッションに説明の既聴を書かない', 'narr' not in ks.lower() and 'heard' not in ks.lower(), ks)
    chk('Z エラーなし', pg.evaluate("window.__errs") == [], pg.evaluate("window.__errs"))
    br.close()
print('NG=%d' % len(bad)); sys.exit(1 if bad else 0)
