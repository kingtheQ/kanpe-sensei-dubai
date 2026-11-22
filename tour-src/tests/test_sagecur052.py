# -*- coding: utf-8 -*-
"""タスク052 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_sagecur052.py [ベースURLの代わりに--ROOT=別ディレクトリ]
賢者の質問リストを開いた時の▶初期位置を、完了(✓)の組み合わせごとに確認する。
 - 1つ完了→2番目 / 2つ完了→3番目 / 全部完了→1番目 / 完了なし→1番目 / 1番目だけ未完了(2,3完了)→1番目
 - 「マップに もどる」は初期位置にならない / ✓表示・項目・並びは変わらない
リポジトリの生成物は書き換えない。マイク・実機は確認できない。"""
import os, sys, threading, http.server, socketserver
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for a in sys.argv[1:]:
    if a.startswith('--ROOT='): ROOT = a[7:]
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,PBY:PBY,enterHub:enterHub,hubMenu:hubMenu};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "try{speechSynthesis.speak=function(u){setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}))")
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
IDS = ['sage_1', 'sage_2', 'sage_3']
CASES = [  # 完了の組み合わせ → 期待する初期位置(0始まり)
    ('完了なし', [], 0), ('1つ完了(1番目)', ['sage_1'], 1), ('2つ完了(1,2番目)', ['sage_1', 'sage_2'], 2),
    ('全部完了', IDS, 0), ('2,3番目だけ完了', ['sage_2', 'sage_3'], 0), ('1,3番目だけ完了', ['sage_1', 'sage_3'], 1)]
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
    p = ctx.new_page(); p.route('**/tour/index.html', hooked); p.goto(base + '/tour/index.html'); p.wait_for_timeout(2000)
    for name, done, want in CASES:
        r = p.evaluate("""([done])=>{var T=window.__T;T.save.seen={};done.forEach(function(v){T.save.seen[v]=1});
          T.enterHub(T.PBY.sage);var bs=[].slice.call(document.querySelectorAll('.dqbox .dq'));
          return {n:bs.length,sel:bs.map(function(b){return b.classList.contains('sel')}).indexOf(true),
                  nsel:bs.filter(function(b){return b.classList.contains('sel')}).length,
                  labels:bs.map(function(b){return b.children[1].textContent}),
                  ok:bs.map(function(b){return !!b.querySelector('.ok')}),err:window.__errs.length}}""", [done])
        chk('%s → ▶は%d番目(実測 %d番目 / 選択中%d個)' % (name, want + 1, r['sel'] + 1, r['nsel']), r['sel'] == want and r['nsel'] == 1 and r['err'] == 0)
        chk('  項目4つ・最後は「マップに もどる」・✓表示が完了と一致', r['n'] == 4 and r['labels'][3] == 'マップに もどる' and r['ok'] == [v in done for v in IDS] + [False], str(r['ok']))
        chk('  「マップに もどる」が初期位置ではない', r['sel'] != 3)
    # 他のメニュー(ドバイの部屋)は従来どおり先頭
    r = p.evaluate("""()=>{var T=window.__T;T.save.seen={};var pl=T.PBY.sage;var m=pl.menu;pl.menu=null;try{T.hubMenu('main')}catch(e){}
          var bs=[].slice.call(document.querySelectorAll('.dqbox .dq'));pl.menu=m;return bs.map(function(b){return b.classList.contains('sel')}).indexOf(true)}""")
    chk('menu無しのハブは従来どおり先頭(0番目)', r == 0, r)
    br.close()
srv.shutdown()
print('\nNG: %d' % len(bad)); sys.exit(1 if bad else 0)
