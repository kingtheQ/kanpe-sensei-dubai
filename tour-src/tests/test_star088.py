# -*- coding: utf-8 -*-
"""タスク088 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_star088.py
(1) 窓口の分岐をどう選んでも(先頭・最後・oneworld寄り・古いセーブが ow)、価格・読み上げ・発券はスター版だけで、save.ticket==='star'
(2) ルール説明の場面(win_rules / win_count)が、おすすめのあと・値段の前に出る
(3) 数えた数字(寄港15・移動16・同じ国3回・30日)が、ルート表から計算した値とスターの決まりに合う
(4) ow4/ow5・ticket_ow のデータは残っている(2周目用)。リポジトリの生成物(tour/)は書き換えない。マイク・実機は確認できない。"""
import os, sys, re, json, threading, http.server, socketserver
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tour-src'))
import window_data as WD
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,winStart:winStart,startVid:startVid,PBY:PBY,DLG:DLG,onPass:onPass,WSTEP:WSTEP};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "try{speechSynthesis.speak=function(u){setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}))")
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)

# 窓口の分かれ目で選ぶ位置。'first' 先頭 / 'last' 最後
def run_flow(pg, strategy, old_pick, cont):
    pg.evaluate("([pk,ct])=>{var T=window.__T;try{localStorage.removeItem('kanpe-tour-save-v1')}catch(e){};delete T.save.ticket;T.save.win={step:1,m:{},cont:ct,pick:pk};T.winStart()}", [old_pick, cont])
    seq = []; last = None; idle = 0
    for i in range(1200):
        pg.wait_for_timeout(120)
        st = pg.evaluate("()=>({vid:__T.G.scene&&__T.G.scene.vid,ph:__T.G.phase,tk:__T.save.ticket||null,done:!!(__T.save.win&&__T.save.win.done),n:document.querySelectorAll('.dq').length,err:window.__errs.length})")
        if st['vid'] and st['vid'] != last: seq.append(st['vid']); last = st['vid']
        if st['tk'] and st['done'] and i > 5: break
        if st['ph'] == 'opts' and st['n']:
            pg.evaluate("([s,n])=>{var b=document.querySelectorAll('.dq');var i=s==='last'?n-1:0;"
                        "b[i].click()}", [strategy, st['n']])
        elif st['ph'] in ('cue', 'cuing', 'listen', 'rep', 'npc') and st['vid'] != 'win_decl':
            idle += 1
            if idle > 2: pg.evaluate("()=>__T.onPass()"); idle = 0
    fin = pg.evaluate("()=>({tk:__T.save.ticket||null,pick:(__T.save.win||{}).pick,done:!!(__T.save.win&&__T.save.win.done),err:window.__errs})")
    return seq, fin

srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
F = WD.route_facts()
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
    pg = ctx.new_page(); pg.route('**/tour/index.html', hooked); pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(2000)
    # (1)(2) 4とおりの流れ
    cases = [('先頭を選ぶ', 'first', 'star', 5), ('最後を選ぶ', 'last', 'star', 5), ('最後を選ぶ・大陸4つ・古いセーブが ow', 'last', 'ow', 4), ('先頭・古いセーブが ow', 'first', 'ow', 5)]
    for name, strat, pk, ct in cases:
        seq, fin = run_flow(pg, strat, pk, ct)
        print('   流れ:', ' > '.join(seq))
        chk('[%s] 発券はスター(ticket=%s)' % (name, fin['tk']), fin['tk'] == 'star' and fin['done'] and not fin['err'], fin['err'])
        chk('[%s] ow の値段・読み上げ・券の場面に入らない' % name, not [v for v in seq if re.search(r'ow[45]|ticket_ow', v)] and seq[-1] == 'ticket_star', seq[-4:])
        chk('[%s] 値段=star・読み上げ=star' % name, 'win_price_star' in seq and 'win_rb_star' in seq)
        i = {v: (seq.index(v) if v in seq else -1) for v in ['win_rec', 'win_rules', 'win_count', 'win_price_star']}
        chk('[%s] ルール→数える の順で、おすすめのあと・値段の前 %s' % (name, i), 0 <= i['win_rec'] < i['win_rules'] < i['win_count'] < i['win_price_star'])
    # (4) ow のデータが残っている
    r = pg.evaluate("()=>({t:!!__T.DLG.ticket_ow,p5:!!__T.DLG.win_price_ow5,p4:!!__T.DLG.win_price_ow4,r5:!!__T.DLG.win_rb_ow5,r4:!!__T.DLG.win_rb_ow4})")
    chk('ow4/ow5・ticket_ow の場面データは残っている %s' % r, all(r.values()))
    # ow の場面へは、窓口の流れからも「チケットの場所」からも行けない
    r = pg.evaluate("()=>{var pl=__T.PBY.ticket;return {v:pl.v.slice(),menu:!!pl.menu}}")
    chk('チケットの場所の場面一覧に ticket_ow がない %s' % r, r['v'] == ['ticket_star'])
    br.close()
# (3) 数字の確認(ルート表から計算した値と、スターの決まり)
R = WD.RULE
chk('寄港 %d <= %d' % (F['stops'], R['stops']), F['stops'] == 15 <= R['stops'])
chk('移動 %d <= %d(陸路 %d 区間を含む)' % (F['moves'], R['moves'], F['rail']), F['moves'] == 16 <= R['moves'] and F['rail'] == 3 and F['flights'] == 13)
chk('同じ国の最大 %d <= %d(%s)' % (F['max_same'], R['same_country'], F['us']), F['max_same'] == 3 <= R['same_country'])
chk('旅の長さ %d 日は %d〜%d 日の内' % (R['trip_days'], R['days_min'], R['days_max']), R['days_min'] <= R['trip_days'] <= R['days_max'])
D = []; WD.add(D); sc = {d['id']: d for d in D}
txt = ' '.join(t['n'] for t in sc['win_rules']['pairs'] + sc['win_count']['pairs'])
for w in ['fifteen', 'sixteen', 'thirteen', 'three times', 'thirty days', 'ten days at least', 'one year at most']:
    chk('台詞に「%s」' % w, w in txt.lower())
chk('台詞に「復習」「テスト」「測定」がない', not re.search(r'復習|テスト|測定', json.dumps(sc['win_rules']) + json.dumps(sc['win_count']), re.S))
print('結果:', 'すべてOK' if not bad else 'NG=' + str(bad)); sys.exit(1 if bad else 0)
