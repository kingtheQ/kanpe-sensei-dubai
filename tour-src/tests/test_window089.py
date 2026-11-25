# -*- coding: utf-8 -*-
"""タスク089 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_window089.py
(1) 初回の流れ: 宣言 → はじめての人 → 地図とルール(win_route) → 値段 → 読み上げ → 名前 → 発券。c2/c5/c7/c8・おすすめ・旧ルール・旧数え は通らない
(2) 宣言: 係員の導入1つ → ルルのお手本→プレイヤーが言う を9文。係員・ルルの吹き出しは1文まで。話す番(cue)のときだけ大きいマイクが出る(幅・高さを測る)
(3) 地図: 区間の番号 1〜16 がすべて地図に描かれる。「Round-the-world ticket rules!」が最初の係員の言葉。移動16/寄港15のカウンターが出る
(4) 2回目に窓口へ来たら、宣言・はじめての人・地図とルールを飛ばし、win_back の挨拶から値段へ(初回と流れが変わる)
(5) 前の旅のメモは、宣言とは別の短いやり取り(win_memo)で、初回の人には出ない
(6) 区切って言った宣言の記録は、これまでと同じ1件(70語ぶんの bits)に戻る
(7) c2/c5/c7/c8・旧ルール・旧数え・ow のデータは消えていない(2周目用)。リポジトリの生成物(tour/)は書き換えない。マイク・実機は確認できない。"""
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
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,winStart:winStart,startVid:startVid,PBY:PBY,DLG:DLG,onPass:onPass,WSTEP:WSTEP,vLoad:vLoad,voiceSetMPart:voiceSetMPart,showMap:showMap,storeSave:storeSave};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "window.__txt={};(function(){var f=CanvasRenderingContext2D.prototype.fillText;CanvasRenderingContext2D.prototype.fillText=function(t){window.__txt[String(t)]=Date.now();return f.apply(this,arguments)}})();"
        "try{speechSynthesis.speak=function(u){setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}))")
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
def sents(t):
    return len([x for x in re.split(r'(?<=[.!?])\s+', t.strip()) if x])

SNAP = ("()=>{var G=__T.G,S=G.scene,T=S&&S.turns&&S.turns[G.ti],m=document.querySelector('.declmic'),r=m?m.getBoundingClientRect():null,"
        "st=document.querySelector('#sceneView .stage').getBoundingClientRect();"
        "return {vid:S&&S.vid,ph:G.phase,ti:G.ti,npc:T&&T.npc,cue:T&&T.cue,who:T&&T.ctx&&T.ctx.who,dp:T&&T.dp?1:0,rn:S&&S.rn,stp:S&&S.stp,tk:__T.save.ticket||null,"
        "done:!!(__T.save.win&&__T.save.win.done),n:document.querySelectorAll('.dq').length,mic:!!m,mw:r?r.width:0,mh:r?r.height:0,sw:st.width,sh:st.height,view:G.view,err:window.__errs.length}}")

def drive(pg, stop_at=None, limit=2500, rec=None):
    """窓口の流れを進める。分かれ目は先頭を選び、宣言の文・会話は onPass で進める。stop_at の場面が出たら止める。"""
    seq = []; last = None; idle = 0; log = []
    for i in range(limit):
        pg.wait_for_timeout(60)
        st = pg.evaluate(SNAP)
        if st['vid'] and st['vid'] != last:
            last = st['vid']
            if st['vid'] != 'win_consent': seq.append(st['vid'])
            if stop_at and st['vid'] == stop_at: return seq, st, log
        if rec: rec(st, log)
        if st['tk'] and st['done'] and i > 5: break
        if st['view'] != 'scene' and not (st['tk'] and st['done']):
            if st['view'] == 'map': break
        if st['vid'] == 'win_consent':
            pg.evaluate("()=>{[].slice.call(document.querySelectorAll('#panel .btn')).filter(function(b){return b.textContent==='送らない'}).forEach(function(b){b.click()})}")
        elif st['ph'] == 'opts' and st['n']:
            pg.evaluate("()=>{document.querySelectorAll('.dq')[0].click()}")
        elif pg.query_selector('.btn.go'):
            pg.click('.btn.go')
        elif st['ph'] == 'cue':
            idle += 1
            if idle > 3: pg.evaluate("()=>__T.onPass()"); idle = 0
        else:
            idle = 0
    return seq, pg.evaluate(SNAP), log

srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
F = WD.route_facts()
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    def newpage(memo=None):
        ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
        if memo: ctx.add_init_script("localStorage.setItem('kanpe-tour-memo-v1',%s)" % json.dumps(json.dumps(memo)))
        pg = ctx.new_page(); pg.route('**/tour/index.html', hooked); pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1800)
        for _ in range(3):
            pg.mouse.click(195, 486); pg.wait_for_timeout(350)   # 旅の1日目カードを閉じる
        return pg
    # ---------- (1)(2)(3)(4) 初回 → 途中で窓口を出る → 2回目 ----------
    pg = newpage()
    pg.evaluate("()=>{var T=__T;try{localStorage.removeItem('kanpe-tour-save-v1')}catch(e){};delete T.save.ticket;delete T.save.win;T.winStart()}")
    mic_log = {'cue_dp': [], 'npc_dp': [], 'cue_other': [], 'turns': []}
    route_txt = {}
    def rec(st, log):
        if st['vid'] == 'win_decl':
            if st['dp']:
                (mic_log['cue_dp'] if st['ph'] == 'cue' else mic_log['npc_dp'] if st['ph'] == 'npc' else []).append((st['ti'], st['mic'], st['mw'], st['mh'], st['sw'], st['sh'], st['who']))
            else:
                if st['ph'] == 'cue': mic_log['cue_other'].append(st['mic'])
            if st['ph'] == 'npc': mic_log['turns'].append((st['ti'], st['who'], st['npc']))
        if st['vid'] and st['ph'] == 'cue' and st['vid'] != 'win_decl': mic_log['cue_other'].append(st['mic'])
    # 初回: 値段(win_price_star)の場面が出たところで止める(=窓口を途中で出る)
    seq1, st1, _ = drive(pg, stop_at='win_price_star', rec=rec)
    print('   初回の流れ:', ' > '.join(seq1))
    chk('初回: 宣言→はじめての人→地図とルール→値段 の順', seq1 == ['win_decl', 'win_c1', 'win_route', 'win_price_star'], seq1)
    chk('初回: c2/c5/c7/c8・おすすめ・旧ルール・旧数え を通らない', not [v for v in seq1 if re.search(r'win_c[2578]|win_rec|win_rules|win_count|win_memo', v)])
    # (2) 宣言
    d = pg.evaluate("()=>{var d=__T.DLG.win_decl,ts=[];for(var i=0;i<d.lines.length;i+=2)ts.push([d.lines[i].n,d.lines[i+1].y,d.lines[i+1].dp||0]);return ts}")
    chk('宣言は 係員の導入1つ＋9文(%d番)' % len(d), len(d) == 10 and sum(1 for x in d if x[2]) == 9)
    chk('宣言の9文を つなぐと DECL(70語)と同じ', ' '.join(x[1] for x in d[1:]) == WD.DECL and len(WD.DECL.split()) == 70)
    chk('導入は短い1文: %r' % d[0][0], sents(d[0][0]) == 1 and len(d[0][0].split()) <= 8, d[0][0])
    chk('宣言の係員・ルルの吹き出しは どれも1文まで(最大%d文)' % max(sents(x[0]) for x in d), all(sents(x[0]) == 1 for x in d))
    whos = {}
    for x in mic_log['cue_dp']: whos[x[0]] = x[6]
    chk('宣言のルルのお手本の番(9文)の話す人は Lulu: %s' % whos, sorted(whos) == list(range(1, 10)) and set(whos.values()) == {'Lulu'})
    cd = mic_log['cue_dp']
    chk('話す番(宣言9文)では、毎回 大きいマイクが出ている(%d回観測)' % len(cd), len(cd) > 0 and all(x[1] for x in cd))
    ws = [x[2] for x in cd]; hs = [x[3] for x in cd]; sw = cd[0][4] if cd else 0
    chk('マイクの大きさ: 幅 %.0fpx(ステージ幅 %.0fpx の %.0f%%)・高さ %.0fpx' % (min(ws), sw, min(ws) / sw * 100, min(hs)), min(ws) >= 80 and min(hs) >= 110 and min(ws) / sw >= .2)
    chk('ルルが話している間(npc)は、マイクは出ていない(%d回観測)' % len(mic_log['npc_dp']), len(mic_log['npc_dp']) > 0 and not any(x[1] for x in mic_log['npc_dp']))
    chk('宣言のほかの話す番(導入の返事・窓口の会話)では、マイクは出ない', mic_log['cue_other'] and not any(mic_log['cue_other']))
    # (3) 地図とルール
    rd = pg.evaluate("()=>{var d=__T.DLG.win_route,ts=[];for(var i=0;i<d.lines.length;i+=2)ts.push([d.lines[i].n,d.lines[i+1].y,d.lines[i].route,d.lines[i].stp]);return ts}")
    chk('ルールの最初の係員の言葉は「Round-the-world ticket rules!」(%d番)' % len(rd), rd[0][0] == 'Round-the-world ticket rules!', rd[0][0])
    chk('地図とルールの係員の吹き出しは どれも1文まで(最大%d文)' % max(sents(x[0]) for x in rd), all(sents(x[0]) == 1 for x in rd))
    chk('区間を引く番の route は 1,3,5,8,10,12,14,16 と増え、16で止まる', [x[2] for x in rd if x[2] is not None] == [1, 3, 5, 8, 10, 12, 14, 16], [x[2] for x in rd if x[2] is not None])
    chk('寄港を数える番の stp は 5,10,15', [x[3] for x in rd if x[3] is not None] == [5, 10, 15])
    alltxt = ' '.join(x[0] for x in rd).lower()
    for w in ['rules!', 'rule one', 'same way', 'come home', 'sixteen moves', 'train', 'fifteen times', 'twenty-four hours', 'thirteen flights', 'three train rides', 'three times', 'ten days at least', 'one year at most', 'thirty-day']:
        chk('ルール説明の台詞に「%s」がある' % w, w in alltxt)
    # 描画: 番号の札 1〜16 と カウンター を、ルールの場面を最後まで流して集める
    pg2 = newpage()
    pg2.evaluate("()=>{var T=__T;delete T.save.ticket;T.save.win={step:0,m:{},cont:5,pick:null,ver:2,dd:1,rr:0,vis:1};T.storeSave();T.winStart()}")
    drawn = set(); lastv = None
    for i in range(3000):
        pg2.wait_for_timeout(60)
        st = pg2.evaluate(SNAP)
        if st['vid'] == 'win_route' and st['ph'] in ('cue', 'npc', 'cuing', 'listen', 'rep'):
            pg2.wait_for_timeout(700)   # 線を引く動きを待つ
            drawn |= set(pg2.evaluate("()=>Object.keys(window.__txt)"))
        if st['vid'] == 'win_price_star': break
        if st['ph'] == 'opts' and st['n']: pg2.evaluate("()=>{document.querySelectorAll('.dq')[0].click()}")
        elif pg2.query_selector('.btn.go'): pg2.click('.btn.go')
        elif st['ph'] == 'cue': pg2.evaluate("()=>__T.onPass()")
    nums = sorted(int(x) for x in drawn if re.fullmatch(r'\d{1,2}', x))
    chk('地図に区間の番号 1〜16 が すべて描かれた %s' % nums, nums == list(range(1, 17)))
    chk('地図に「MOVES」「STOPS」と 16/16・15/15 が描かれた', {'MOVES', 'STOPS', '16/16', '15/15'} <= drawn)
    chk('ルールの途中の数 1/16 … も数えている(例: 8/16, 5/15)', {'1/16', '8/16', '5/15', '10/15'} <= drawn)
    pg2.context.close()
    # (4) 2回目: 窓口を出て、また来る
    pg.evaluate("()=>{__T.showMap()}"); pg.wait_for_timeout(400)
    w = pg.evaluate("()=>JSON.parse(JSON.stringify(__T.save.win))")
    chk('途中で出たときのセーブ: 宣言済み(dd)・説明済み(rr) が残る', w.get('dd') == 1 and w.get('rr') == 1 and w.get('ver') == 2, w)
    pg.evaluate("()=>{__T.winStart()}")
    seq2, fin2, _ = drive(pg)
    print('   2回目の流れ:', ' > '.join(seq2))
    chk('2回目: 挨拶(win_back)→値段→読み上げ→名前→発券。宣言・はじめての人・地図とルールは飛ばす', seq2 == ['win_back', 'win_price_star', 'win_rb_star', 'win_name', 'ticket_star'], seq2)
    chk('2回目も 発券はスター(ticket=%s)・エラーなし' % fin2['tk'], fin2['tk'] == 'star' and fin2['done'] and fin2['err'] == 0)
    chk('初回と2回目で流れが変わる(初回 %d 場面 / 2回目 %d 場面)' % (len(seq1) + 4, len(seq2)), seq1[:3] == ['win_decl', 'win_c1', 'win_route'] and seq2[0] == 'win_back')
    # 続けて最後まで通した初回(窓口を出ずに)も 発券まで通る
    pg3 = newpage()
    pg3.evaluate("()=>{var T=__T;try{localStorage.removeItem('kanpe-tour-save-v1')}catch(e){};delete T.save.ticket;delete T.save.win;T.winStart()}")
    seq3, fin3, _ = drive(pg3)
    chk('初回を通しで: %s' % ' > '.join(seq3), seq3 == ['win_decl', 'win_c1', 'win_route', 'win_price_star', 'win_rb_star', 'win_name', 'ticket_star'] and fin3['tk'] == 'star' and fin3['err'] == 0)
    pg3.context.close()
    # ---------- (5) 前の旅のメモ ----------
    pm = newpage(memo=['Tahiti', 'Canada'])
    pm.evaluate("()=>{var T=__T;try{localStorage.removeItem('kanpe-tour-save-v1')}catch(e){};delete T.save.ticket;delete T.save.win;T.winStart()}")
    seqm, stm, _ = drive(pm, stop_at='win_c1')
    print('   メモあり:', ' > '.join(seqm))
    chk('メモあり: 前の旅のメモ(win_memo)が、宣言の前に別の場面として出る', seqm[:2] == ['win_memo', 'win_decl'], seqm)
    mm = pm.evaluate("()=>{var d=__T.DLG.win_memo,ts=[];for(var i=0;i<d.lines.length;i+=2)ts.push(d.lines[i].n);return ts}")
    chk('メモの台詞(%d番): 1文ずつ・Tahiti と Canada を言う' % len(mm), all(sents(x) == 1 for x in mm) and any('Tahiti and Canada' in x for x in mm), mm)
    dd = pm.evaluate("()=>__T.DLG.win_decl.lines[0].n")
    chk('メモあり: 宣言の係員の言葉にメモは混ざらない: %r' % dd, 'Tahiti' not in dd and 'Last time' not in dd)
    pm.context.close()
    chk('メモなし(初回)では、win_memo に入らない', 'win_memo' not in seq1)
    # ---------- (6) 区切って言った宣言の記録 ----------
    pv = newpage()
    r = pv.evaluate("""()=>{
      var S=%s,tg=S.map(function(s){return s.split(' ').length});
      try{localStorage.removeItem('kanpe-voice-v1')}catch(e){}
      for(var i=0;i<S.length;i++){var b='';for(var k=0;k<tg[i];k++)b+=(i===3&&k===0)?'0':'1';
        __T.voiceSetMPart('decl',{ts:1000+i,src:'sr',tot:null,acc:null,flu:null,cmp:null,w:null,bits:b,heard:S[i]},{dp:1,df:i===0?1:0,dl:i===S.length-1?1:0});
        if(i<S.length-1){var v=__T.vLoad(),t=v.trips.length?v.trips[v.trips.length-1]:null;if(t&&t.start)return {early:1}}}
      var v=__T.vLoad(),t=v.trips[v.trips.length-1];return {n:v.trips.length,bits:t.start.bits,heard:t.start.heard,src:t.start.src}}""" % json.dumps(WD.DECL_SENT))
    chk('区切った宣言は、最後の文のあとで1件に戻る(早く保存されない・trips=%s)' % r.get('n'), not r.get('early') and r.get('n') == 1)
    chk('まとめた記録: bits は70語ぶん・4文目の1語目だけ0(%s)' % (r.get('bits') or '')[:12], r.get('bits') and len(r['bits']) == 70 and r['bits'][sum(len(x.split()) for x in WD.DECL_SENT[:3])] == '0' and r['bits'].count('0') == 1)
    chk('まとめた記録: 聞こえた文は9文をつないだもの', r.get('heard') == WD.DECL[:600])
    pv.context.close()
    br.close()
# ---------- (7) データが残っている ----------
D = []; WD.add(D); ids = [d['id'] for d in D]
for k in ['win_c2', 'win_c5', 'win_c7', 'win_c8', 'win_rules', 'win_count', 'win_price_ow5', 'win_price_ow4', 'win_rb_ow5', 'win_rb_ow4']:
    chk('データは消えていない: %s' % k, k in ids)
chk('窓口の流れ(WSTEP)に c2/c5/c7/c8・おすすめ・旧ルール・旧数え は入っていない', True)
src = open(os.path.join(ROOT, 'tour-src', 'window.js'), encoding='utf-8').read()
ws = re.search(r"var WSTEP=\[(.*?)\];", src).group(1)
chk('WSTEP=%s' % ws, not re.search(r'win_c[2578]|win_rec|win_rules|win_count', ws))
print('\n結果: %s' % ('すべて OK' if not bad else 'NG %d件: %s' % (len(bad), bad)))
sys.exit(1 if bad else 0)
