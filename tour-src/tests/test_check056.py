# -*- coding: utf-8 -*-
"""タスク056 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_check056.py
?check=1 の点検モードを確かめる。(1) パラメータなし=従来どおり(CHECKボタンなし・専用キーなし・鍵は従来の判定)
(2) ?check=1: 全場所ロックなし・場面一覧から全場面(ナイロビ・ドーハ)を直接始められる・窓口の各段・割りこみの場面も始まる
(3) 通常のセーブ(kanpe-…)は、点検中に何をしても読まれず・書かれず・消えない(あらかじめ入れた見本の値が最後まで同じ)
(4) 点検の進行は専用キー chk1: にだけ入る (5) 旅の骨組み(TRIP)は動かない=夜の1枚・場所の鍵が出ない
(6) ページのエラーなし。リポジトリの生成物(tour/)は書き換えない。マイク・実機の見え方は確認できない。"""
import os, re, sys, json, threading, http.server, socketserver
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def log_message(s, *a): pass
srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
PORT = srv.server_address[1]
HOOK = "requestAnimationFrame(frame);\n})();"
EXPOSE = ("window.__T={G:G,save:save,MODES:MODES,PBY:PBY,DLG:DLG,TRIP:TRIP,finishScene:finishScene,lockedPlace:lockedPlace,"
          "get MODE(){return MODE},EVSLOTS:typeof EVSLOTS!=='undefined'?EVSLOTS:[],WSTEP:typeof WSTEP!=='undefined'?WSTEP:[]};")
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "try{speechSynthesis.speak=function(u){setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        # 通常のセーブの見本(点検中に変わってはいけない)。ページ読み込みのたびに入れ直さないよう、1度だけ
        "if(!localStorage.getItem('__seeded')){localStorage.setItem('__seeded','1');"
        "localStorage.setItem('kanpe-tour-save-v1',JSON.stringify({seen:{nbo_immig1:1},ticket:'star',gold:1}));"
        "localStorage.setItem('kanpe-trip-v1','SENTINEL_TRIP');localStorage.setItem('kanpe-world-v1','SENTINEL_WORLD');"
        "localStorage.setItem('kanpe-voice-v1','SENTINEL_VOICE')}")
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
def hk(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, EXPOSE + HOOK))
def real_state(_pg):
    # 点検ページの中では getItem が専用キーへ向くため、本物の記録は別のタブ(スクリプトなしの静的ページ)から読む
    return PG2.evaluate("()=>{var o={};for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k.indexOf('chk1:')!==0)o[k]=localStorage.getItem(k)}return o}")
def chk_keys(pg):
    return pg.evaluate("()=>{var a=[];for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k.indexOf('chk1:')===0)a.push(k)}return a}")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    ctx = b.new_context(viewport={'width': 390, 'height': 800}); ctx.add_init_script(INIT)
    PG2 = ctx.new_page(); PG2.goto('http://127.0.0.1:%d/README.md' % PORT)
    pg = ctx.new_page(); pg.route(re.compile(r'/index\.html'), hk)
    def go(path):
        pg.goto('http://127.0.0.1:%d/%s' % (PORT, path)); pg.wait_for_timeout(1200)
    # ---------- (1) 通常: 従来どおり ----------
    go('tour/index.html')
    pg.evaluate("()=>{localStorage.setItem('__before',JSON.stringify(Object.keys(localStorage).sort()))}")
    chk('通常: CHECKボタンがない', pg.evaluate("()=>!document.getElementById('chkBtn')&&!window.__CHK"))
    chk('通常: 専用キー(chk1:)を作らない', chk_keys(pg) == [])
    norm_lock = pg.evaluate("()=>{var T=window.__T,n=0;T.MODES.arr.p.forEach(function(p){if(T.lockedPlace(p.id))n++});return n}")
    chk('通常: 場所の鍵は従来どおり(到着の2つ目以降が閉じる)', norm_lock >= 1, norm_lock)
    # ---------- (2)〜(5) ナイロビ ?check=1 ----------
    real0 = real_state(pg)
    go('tour/index.html?check=1')
    chk('点検: CHECKボタンが出る', pg.evaluate("()=>!!document.getElementById('chkBtn')&&window.__CHK===true"))
    chk('点検: 通常のセーブの見本が同じ(読み込みだけでは変わらない)', real_state(pg) == real0, [(k, real_state(pg).get(k), real0.get(k)) for k in set(real_state(pg)) | set(real0) if real_state(pg).get(k) != real0.get(k)])
    chk('点検: 専用の記録は空から始まる(通常の seen/ticket を読まない)', pg.evaluate("()=>JSON.stringify(window.__T.save.seen)==='{}'"))
    for mode in ['sage', 'hdep', 'arr', 'air', 'dep']:
        r = pg.evaluate("(m)=>{var T=window.__T;T.G.view==='map'||0;var ps=T.MODES[m].p,n=0;ps.forEach(function(p){if(T.lockedPlace(p.id))n++});return [ps.length,n]}", mode)
        chk('点検: %s の場所は全部ロックなし' % mode, r[1] == 0, r)
    tabs = pg.evaluate("()=>[].slice.call(document.querySelectorAll('#modeBar .mbtn')).map(function(b){return [b.dataset.m,b.hidden]})")
    chk('点検: 全タブが見える(賢者・羽田の出発も)', all(not h for m, h in tabs) and len(tabs) >= 5, tabs)
    pg.evaluate("()=>document.getElementById('chkBtn').click()"); pg.wait_for_timeout(200)
    nb = pg.evaluate("()=>document.querySelectorAll('#chkPan button').length")
    chk('点検: 場面一覧のボタンが出る', nb > 60, nb)
    # 一覧の全場面を、1つずつ直接始める(前提なし)
    allv = pg.evaluate("""()=>{var T=window.__T,a=[];Object.keys(T.MODES).forEach(function(k){T.MODES[k].p.forEach(function(p){
        var s=[];(p.v||[]).forEach(function(v){s.push(v)});if(p.tkv)Object.keys(p.tkv).forEach(function(t){p.tkv[t].forEach(function(v){if(s.indexOf(v)<0)s.push(v)})});
        if(p.menu)p.menu.forEach(function(m){if(s.indexOf(m[1])<0)s.push(m[1])});s.forEach(function(v){if(T.DLG[v])a.push([p.id,v])})})});return a}""")
    chk('点検: 一覧の場面を数えた', len(allv) >= 35, len(allv))
    fails = []
    for pid, v in allv:
        pg.evaluate("()=>document.getElementById('chkBtn').click()"); pg.wait_for_timeout(60)
        ok = pg.evaluate("""(v)=>{var bs=[].slice.call(document.querySelectorAll('#chkPan button')).filter(function(b){return b.textContent===v});if(!bs.length)return 'nobtn';bs[0].click();return 'clicked'}""", v)
        pg.wait_for_timeout(120)
        r = pg.evaluate("()=>{var G=window.__T.G;return [G.view,G.scene&&G.scene.vid]}")
        if ok != 'clicked' or r[0] != 'scene' or r[1] != v: fails.append((v, ok, r))
    chk('点検: 一覧のどの場面も直接始まる(%d)' % len(allv), not fails, fails[:5])
    # 割りこみ・窓口の各段
    evv = pg.evaluate("()=>window.__T.EVSLOTS.map(function(s){return s.vid}).filter(function(v,i,a){return a.indexOf(v)===i&&window.__T.DLG[v]})")
    efails = []
    for v in evv:
        pg.evaluate("()=>document.getElementById('chkBtn').click()"); pg.wait_for_timeout(60)
        pg.evaluate("(v)=>{[].slice.call(document.querySelectorAll('#chkPan button')).filter(function(b){return b.textContent===v})[0].click()}", v); pg.wait_for_timeout(120)
        r = pg.evaluate("()=>{var G=window.__T.G;return [G.view,G.scene&&G.scene.vid]}")
        if r != ['scene', v]: efails.append((v, r))
    chk('点検: 割りこみ・顔なじみの場面も始まる(%d)' % len(evv), evv and not efails, efails[:3])
    wsteps = pg.evaluate("()=>window.__T.WSTEP")
    wf = []
    for k in wsteps:
        if k == 'win_decl': continue   # 声の同意の1枚が先に出る(別の場面)。別に確かめる
        pg.evaluate("()=>document.getElementById('chkBtn').click()"); pg.wait_for_timeout(60)
        pg.evaluate("(k)=>{[].slice.call(document.querySelectorAll('#chkPan button')).filter(function(b){return b.textContent===k})[0].click()}", k); pg.wait_for_timeout(150)
        r = pg.evaluate("()=>{var G=window.__T.G;return [G.view,G.scene&&G.scene.vid]}")
        if r[0] != 'scene': wf.append((k, r))
    chk('点検: 窓口の各段から始まる(%d段)' % (len(wsteps) - 1), not wf, wf)
    pg.evaluate("()=>document.getElementById('chkBtn').click()"); pg.wait_for_timeout(60)
    pg.evaluate("()=>{[].slice.call(document.querySelectorAll('#chkPan button')).filter(function(b){return b.textContent==='win_decl'})[0].click()}"); pg.wait_for_timeout(200)
    chk('点検: 宣言の段も開く(同意の1枚か宣言の場面)', pg.evaluate("()=>window.__T.G.view==='scene'"))
    # 券を切りかえると、羽田の出発の場面が券ごとに選べる
    pg.evaluate("()=>document.getElementById('chkBtn').click()"); pg.evaluate("()=>{[].slice.call(document.querySelectorAll('#chkPan button')).filter(function(b){return b.textContent==='Star Alliance'})[0].click()}")
    chk('点検: 券をStarに切りかえられる', pg.evaluate("()=>window.__T.save.ticket==='star'"))
    # 場面を終えても 旅の骨組みは動かず、通常のセーブは変わらない
    pg.evaluate("()=>{var b=[].slice.call(document.querySelectorAll('#chkPan button')).filter(function(b){return b.textContent==='nbo_gate1'})[0];b.click()}"); pg.wait_for_timeout(150)
    pg.evaluate("()=>{window.__T.finishScene()}"); pg.wait_for_timeout(400)
    chk('点検: 場面のあと地図に戻る(夜の1枚などは出ない)', pg.evaluate("()=>window.__T.G.view==='map'&&!document.querySelector('.trip-ov,.trip-night,.trip-mor')"))
    ck = chk_keys(pg)
    chk('点検: 進行は専用キー chk1:kanpe-tour-save-v1 に入る', 'chk1:kanpe-tour-save-v1' in ck, ck)
    chk('点検: 旅の骨組み(kanpe-trip-v1)は作られない', 'chk1:kanpe-trip-v1' not in ck, ck)
    chk('点検: 通常のセーブ(見本)は最後まで同じ', real_state(pg) == real0, [k for k in real_state(pg) if real_state(pg)[k] != real0.get(k)])
    # 再読み込み: 進行は専用キーから戻る・通常は不変
    go('tour/index.html?check=1')
    chk('点検: 再読み込みで進行が戻る(専用キーから)', pg.evaluate("()=>window.__T.save.seen.nbo_gate1>0"))
    chk('点検: 再読み込み後も通常のセーブは不変', real_state(pg) == real0)
    # 通常に戻ると、点検の進行は見えない
    go('tour/index.html')
    chk('通常に戻る: 点検の進行は混ざらない(nbo_gate1 なし・見本の seen のまま)', pg.evaluate("()=>!window.__T.save.seen.nbo_gate1&&window.__T.save.seen.nbo_immig1>0&&window.__T.save.ticket==='star'"))
    chk('通常に戻る: 通常のセーブ(見本)は同じ', real_state(pg) == real0)
    # ---------- ドーハ ----------
    go('tour/doha/index.html?check=1')
    for mode in ['arr', 'city', 'dep']:
        r = pg.evaluate("(m)=>{var T=window.__T,n=0,ps=T.MODES[m].p;ps.forEach(function(p){if(T.lockedPlace(p.id))n++});return [ps.length,n]}", mode)
        chk('ドーハ点検: %s の場所は全部ロックなし' % mode, r[1] == 0, r)
    dv = pg.evaluate("""()=>{var T=window.__T,a=[];Object.keys(T.MODES).forEach(function(k){T.MODES[k].p.forEach(function(p){var s=(p.v||[]).slice();if(p.menu)p.menu.forEach(function(m){if(s.indexOf(m[1])<0)s.push(m[1])});s.forEach(function(v){if(T.DLG[v])a.push([p.id,v])})})});return a}""")
    df = []
    for pid, v in dv:
        pg.evaluate("()=>document.getElementById('chkBtn').click()"); pg.wait_for_timeout(50)
        pg.evaluate("(v)=>{[].slice.call(document.querySelectorAll('#chkPan button')).filter(function(b){return b.textContent===v})[0].click()}", v); pg.wait_for_timeout(110)
        r = pg.evaluate("()=>{var G=window.__T.G;return [G.view,G.scene&&G.scene.vid]}")
        if r != ['scene', v]: df.append((v, r))
    chk('ドーハ点検: 一覧のどの場面も直接始まる(%d)' % len(dv), len(dv) >= 20 and not df, df[:5])
    chk('ドーハ点検: 通常のセーブは不変', real_state(pg) == real0)
    ck0 = sorted(chk_keys(pg))
    go('tour/doha/index.html')
    chk('ドーハ通常: CHECKボタンなし・専用キーを増やさない・通常のセーブ不変', pg.evaluate("()=>!document.getElementById('chkBtn')") and sorted(chk_keys(pg)) == ck0)
    errs = pg.evaluate("()=>window.__errs")
    chk('ページのエラーなし', not errs, errs[:3])
    b.close()
print('\n結果:', 'すべてOK' if not bad else 'NG あり: %s' % bad)
sys.exit(1 if bad else 0)
