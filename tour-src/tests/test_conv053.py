# -*- coding: utf-8 -*-
"""タスク053 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_conv053.py
A. 手順0: 語ごとの記録(即答/遅い/間違い/時間切れ・ms)と選別(即答=卒業・それ以外=持ち越し・理由つき・上限16)。即答の線は WB.fastFrac の1か所。画面(Word Battle)は今のまま
B. 手順2〜3: 試行の場面 nbo_java1(会話に溶かす。タスク061で新しい流れに作り替え済み: 日本語カードで選ぶのは1回)。Word Battle も Meaning! も出ない／選び方で相手の反応が変わる／
   選ぶまでの時間が語ごとに記録される／時間切れでも物語は進み、場面の完了(save.seen)とマップへの戻りは今までどおり／点数が画面に出ない
C. 手順1: 夢(夜の1枚のあと)。持ち越しの上位5語が夢の会話に出る(3択にしない)。通じた語は持ち越しから外れ、通じなかった語は残る。夢のあとは次の朝の1枚へ
マイクの実機・音・見え方は確認できない(このテストの音声認識は、カンペの文をそのまま返す偽物)。"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
HOOK = "requestAnimationFrame(frame);\n})();"
OPT = lambda *ns: ",".join("%s:typeof %s!=='undefined'?%s:null" % (n, n, n) for n in ns)
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    hk = "window.__T={G:G,save:save,startVid:startVid,PBY:PBY,DLG:DLG,PLACES:typeof PLACES!=='undefined'?PLACES:null,startWords:startWords,noteWord:noteWord,fastMs:fastMs,WB:WB,LIMIT:LIMIT," + OPT('dreamStart', 'dreamWords', 'TRIP', 'forkOpts', 'enterPlace', 'showMap') + "};"
    route.fulfill(response=r, body=body.replace(HOOK, hk + HOOK, 1))
bad = []; ERR = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
JP = r"[぀-ヿ㐀-鿿]"
POLL = ("window.__ph=new Set();window.__txt=[];setInterval(function(){try{var T=window.__T;if(!T)return;window.__ph.add(T.G.phase);"
        "var m=document.getElementById('msgText');if(m)window.__txt.push(m.textContent);"
        "var p=document.getElementById('panel')||document.querySelector('.panel');if(p){window.__txt.push(p.innerText);"
        "if(p.querySelector('.choices'))window.__ph.add('CHOICES');if(p.querySelector('.reveal'))window.__ph.add('REVEAL');"
        "[].forEach.call(p.querySelectorAll('.dq'),function(b){window.__txt.push('DQ:'+b.textContent)})}}catch(e){}},60)")
def seed(ctx, key, sv, trip=None):
    q = ctx.new_page(); q.on('pageerror', lambda e: ERR.append(str(e)[:160]))
    q.add_init_script("localStorage.setItem(%s,%s);" % (json.dumps(key), json.dumps(json.dumps(sv))) + ("localStorage.setItem('kanpe-trip-v1',%s);" % json.dumps(json.dumps(trip)) if trip else ''))
    return q
LEGS = [('HND', 'DOH'), ('DOH', 'NBO'), ('NBO', 'DOH'), ('DOH', 'HEL'), ('HEL', 'RVN'), ('RVN', 'MAD'), ('MAD', 'LIM'), ('LIM', 'CUZ'), ('CUZ', 'LIM'), ('LIM', 'MIA'), ('MIA', 'DFW'), ('DFW', 'HNL'), ('HNL', 'HND')]
def tseed(tk, td, day, ph):
    return {'v': 1, 'trip': 1, 'tk': tk, 'day': day, 'td': td, 'ph': ph, 'bun': 1,
            'legs': [{'i': i, 'fr': a, 'to': b, 'd': None, 'f': 1 if i < 2 else 0, 'l': 1 if i < 2 else 0} for i, (a, b) in enumerate(LEGS)],
            'days': [], 'cur': {'led': [], 'pick': []}}
with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
    # ---------------- A. 手順0 ----------------
    q = ctx.new_page(); q.on('pageerror', lambda e: ERR.append(str(e)[:160])); q.route('**/dubai/index.html', hooked)
    q.goto(base + '/dubai/index.html'); q.wait_for_timeout(1500)
    r = q.evaluate("()=>({f:__T.fastMs(),fr:__T.WB.fastFrac,lim:__T.WB.limit,L:__T.LIMIT,w:Object.prototype.toString.call(__T.save.wrec)})")
    chk('A1 即答の線 = 制限時間の前半(5000ms → 2500ms)。WB.fastFrac の1か所', r['f'] == 2500 and r['fr'] == .5 and r['lim'] == 5000, r)
    q.evaluate("()=>{__T.WB.fastFrac=.4}"); chk('A1b 線は WB.fastFrac を変えるだけで動く(0.4 → 2000ms)', q.evaluate("()=>__T.fastMs()") == 2000)
    q.evaluate("()=>{__T.WB.fastFrac=.5;var T=__T;T.save.missed=[];T.save.wrec={};"
               "T.noteWord(['alpha','/a/','ア'],'slow',3100);T.noteWord(['beta','/b/','ベ'],'wrong',900);T.noteWord(['gamma','/g/','ガ'],'timeout',5000);T.noteWord(['delta','/d/','デ'],'fast',800)}")
    s = q.evaluate("()=>({m:__T.save.missed,w:__T.save.wrec})")
    why = dict((m[0], m[3]) for m in s['m'])
    chk('A2 遅い・間違い・時間切れは持ち越し(理由つき)、即答は持ち越しに入れない', why == {'alpha': '遅い', 'beta': '間違い', 'gamma': '時間切れ'}, why)
    chk('A2b 語ごとの記録に結果とミリ秒が残る', s['w']['alpha'] == dict(s['w']['alpha'], o='slow', ms=3100) and s['w']['delta']['o'] == 'fast' and s['w']['delta']['ms'] == 800 and s['w']['beta']['o'] == 'wrong', json.dumps(s['w'])[:200])
    chk('A2c 意味(日本語)は保存だけ: 持ち越しの形は [単語, 発音記号, 意味, 理由]', s['m'][0][2] == 'ガ' and len(s['m'][0]) == 4, s['m'][0])
    q.evaluate("()=>{__T.noteWord(['alpha','/a/','ア'],'fast',500)}")
    chk('A3 持ち越しの語を即答したら卒業(持ち越しから外れる)', 'alpha' not in [m[0] for m in q.evaluate("()=>__T.save.missed")])
    q.evaluate("()=>{for(var i=0;i<20;i++)__T.noteWord(['w'+i,'/w/','わ'],'wrong',100)}")
    n = q.evaluate("()=>[__T.save.missed.length,Object.keys(__T.save.wrec).length,__T.save.missed[0][0]]")
    chk('A4 持ち越しの上限16・新しい順', n[0] == 16 and n[2] == 'w19', n)
    q.evaluate("()=>{var T=__T;T.save.missed=[];T.save.wrec={};T.save.seen={}}")
    # 実際の Word Battle(今の画面のまま)で、即答・遅い・間違い・時間切れを起こす
    vid = q.evaluate("()=>{var L=[];__T.PLACES.forEach(function(p){p.v.forEach(function(v){if(__T.DLG[v]&&__T.DLG[v].words.length>=6)L.push(v)})});return L[0]}")
    q.evaluate("(v)=>{var T=__T,pl=T.PLACES.filter(function(p){return p.v.indexOf(v)>=0})[0];T.startVid(pl,v,null);T.startWords()}", vid)
    q.wait_for_timeout(400)
    def cur():
        return q.evaluate("()=>{var e=document.querySelector('.prompt .en');return e?e.textContent:null}")
    def jp_of(w): return q.evaluate("(w)=>{var ws=__T.G.scene.words;for(var i=0;i<ws.length;i++)if(ws[i][0]===w)return ws[i][2]}", w)
    def click_text(t): q.evaluate("(t)=>{[].forEach.call(document.querySelectorAll('.choices .ch'),function(b){if(b.textContent===t&&!b.disabled)b.click()})}", t)
    def click_wrong(w):
        q.evaluate("(t)=>{var d=0;[].forEach.call(document.querySelectorAll('.choices .ch'),function(b){if(b.textContent!==t&&!d&&!b.disabled){d=1;b.click()}})}", jp_of(w))
    seen = []
    w0 = cur(); seen.append(w0); click_text(jp_of(w0)); q.wait_for_timeout(1500)                       # 即答
    w1 = cur(); seen.append(w1); q.wait_for_timeout(3000); click_text(jp_of(w1)); q.wait_for_timeout(1500)   # 遅い(3秒)
    w2 = cur(); seen.append(w2); click_wrong(w2); q.wait_for_timeout(2000)                               # 間違い
    w3 = cur(); seen.append(w3); q.wait_for_timeout(5700); q.wait_for_timeout(1500)                       # 時間切れ
    s = q.evaluate("()=>({m:__T.save.missed,w:__T.save.wrec})"); why = dict((m[0], m[3]) for m in s['m']); wr = s['w']
    print('  語:', seen, why, dict((k, (v['o'], v['ms'])) for k, v in wr.items()))
    chk('A5 実画面: 即答は卒業(持ち越しなし・記録 fast)', wr.get(w0.lower(), {}).get('o') == 'fast' and w0 not in why and wr[w0.lower()]['ms'] < 2500, wr.get(w0.lower()))
    chk('A5b 実画面: 3秒の正解は「遅い」(持ち越し・記録 slow・ms 約3000)', why.get(w1) == '遅い' and wr[w1.lower()]['o'] == 'slow' and 2500 < wr[w1.lower()]['ms'] < 5000, (why.get(w1), wr.get(w1.lower())))
    chk('A5c 実画面: 間違いは「間違い」', why.get(w2) == '間違い' and wr[w2.lower()]['o'] == 'wrong', why.get(w2))
    chk('A5d 実画面: 時間切れは「時間切れ」(ms=制限時間)', why.get(w3) == '時間切れ' and wr[w3.lower()]['o'] == 'timeout' and wr[w3.lower()]['ms'] == 5000, why.get(w3))
    q.close()
    # ---------------- B. 試行の場面 nbo_java1 ----------------
    q = seed(ctx, 'kanpe-tour-save-v1', {'seen': {}, 'ticket': 'ow'}, tseed('ow', 6, 6, 'day')); q.route('**/tour/index.html', hooked)
    q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800); q.evaluate(POLL)
    # タスク061: nbo_java1 は新しい流れ(日本語カードで選ぶのは1回だけ)に作り替えた。裏の計測と持ち越しは同じ仕組み。詳しい確認は test_flow061.py
    def run_java(pick, wait):
        q.evaluate("()=>{var T=__T;T.save.missed=[];T.save.wrec={};T.save.seen={};window.__ph.clear();window.__txt.length=0;T.startVid(T.PBY.java,'nbo_java1',null)}")
        q.wait_for_timeout(500); q.click('.btn.go'); forks = 0
        for step in range(120):
            q.wait_for_timeout(250)
            n = q.evaluate("()=>document.querySelectorAll('.jcard').length")
            if n:
                forks += 1; q.wait_for_timeout(wait); q.evaluate("(i)=>{document.querySelectorAll('.jcard')[i].click()}", pick)
            if q.evaluate("()=>__T.G.view") == 'map': break
        return forks
    f = run_java(0, 0)   # すぐ カード → 即答
    s = q.evaluate("()=>({w:__T.save.wrec,m:__T.save.missed,seen:__T.save.seen,view:__T.G.view,ph:Array.from(window.__ph)})"); why = dict((m[0], m[3]) for m in s['m']); print('  run1', json.dumps(s['w'])[:300], why, s['ph'])
    chk('B1 選ぶのは1場面に1回(日本語カード。タスク061)', f == 1, f)
    chk('B2 Word Battle も Meaning! も出ない(phase に words/reveal なし・3択の選択肢画面なし)', 'words' not in s['ph'] and 'reveal' not in s['ph'] and 'CHOICES' not in s['ph'] and 'REVEAL' not in s['ph'], s['ph'])
    chk('B3 会話が終わるとマップへ戻り、場面の完了(save.seen)が +1', s['view'] == 'map' and s['seen'].get('nbo_java1') == 1, (s['view'], s['seen']))
    chk('B4 すぐ押すと shillings は即答(fast)で卒業。持ち越しに入らない', s['w'].get('shillings', {}).get('o') == 'fast' and 'shillings' not in why, s['w'])
    f = run_java(0, 3200)   # 3.2秒のあと カード → 遅い
    s = q.evaluate("()=>({w:__T.save.wrec,m:__T.save.missed,seen:__T.save.seen,view:__T.G.view})"); why = dict((m[0], m[3]) for m in s['m'])
    chk('B5 3.2秒で選ぶと「遅い」→持ち越し(shillings)・ms が記録される', why.get('shillings') == '遅い' and 3000 < s['w']['shillings']['ms'] < 5000, s['w'].get('shillings'))
    txt = q.evaluate("()=>window.__txt.join('\\n')"); import re
    chk('B6 画面に「復習」「テスト」「間違い」「Word Battle」「Meaning」「点」が出ない(日本語は選ぶカードの単語だけ)', not any(w in txt for w in ['復習', 'テスト', 'Word Battle', 'Meaning!', '間違い', '点']), '')
    chk('B7 選んだ方法で相手の反応が変わる(カード→"Card is fine")', 'Of course. Card' in txt)
    f = run_java(1, 5600)   # 時間切れのあと 現金
    s = q.evaluate("()=>({w:__T.save.wrec,m:__T.save.missed,seen:__T.save.seen,view:__T.G.view})"); why = dict((m[0], m[3]) for m in s['m'])
    txt = q.evaluate("()=>window.__txt.join('\\n')")
    chk('B8 現金を選ぶと、相手の反応は "Cash is fine"', 'Cash is fine' in txt)
    chk('B9 制限時間をこえて選ぶと「時間切れ」(ms=制限時間)・物語は進んで終わる', why.get('shillings') == '時間切れ' and s['w']['shillings']['ms'] == 5000 and s['view'] == 'map' and s['seen'].get('nbo_java1') == 1, (why.get('shillings'), s['view']))
    # 場面のスイッチ: conv のない場面は今までどおり Word Battle が出る(タスク057 第1弾でナイロビの nbo_java2 も新しい流れになったので、まだ変えていない羽田の hnd_sec で確かめる)
    q.evaluate("(v)=>{var T=__T;T.save.missed=[];T.save.wrec={};window.__ph.clear();var pl=null;for(var k in T.PBY){var p=T.PBY[k];if(p&&p.v&&p.v.indexOf(v)>=0){pl=p;break}} T.startVid(pl,v,null)}", 'hnd_sec'); q.wait_for_timeout(400); q.click('.btn.go')
    for i in range(60):
        q.wait_for_timeout(300)
        if 'words' in q.evaluate("()=>Array.from(window.__ph)"): break
    chk('B10 場面ごとのスイッチ: 会話に溶かしていない hnd_sec(羽田・第2弾で変える予定)は今までどおり Word Battle へ進む', 'words' in q.evaluate("()=>Array.from(window.__ph)"))
    q.close()
    # ---------------- C. 夢 ----------------
    q = seed(ctx, 'kanpe-tour-save-v1', {'seen': {}, 'ticket': 'ow'}, tseed('ow', 6, 6, 'day')); q.route('**/tour/index.html', hooked)
    q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800); q.evaluate(POLL)
    chk('C0 夢の入口(TRIP.hooks.dream)がある', q.evaluate("()=>typeof __T.TRIP.hooks.dream")  == 'function')
    miss = [['latte', '/l/', 'ラテ', '遅い'], ['iced', '/i/', '冷たい', '間違い'], ['slice', '/s/', 'ひと切れ', '時間切れ'], ['carrot cake', '/c/', 'キャロットケーキ', '遅い'],
            ['shillings', '/s/', 'シリング', '遅い'], ['aisle', '/a/', '通路', '間違い'], ['receipt', '/r/', 'レシート', '遅い']]
    q.evaluate("(m)=>{var T=__T;T.save.missed=m;T.save.wrec={};window.__done=0;window.__ph.clear();window.__txt.length=0;T.dreamStart(function(){window.__done=1})}", miss)
    q.wait_for_timeout(1200)
    d = q.evaluate("()=>{var d=__T.DLG.dream_1;return {n:d.lines.filter(function(l){return l.n}).map(function(l){return l.n}),dw:d.lines.filter(function(l){return l.dw}).map(function(l){return l.dw}),bg:d.bg,view:__T.G.view}}")
    print('  夢の語:', d['dw'])
    chk('C1 夢に出る語は持ち越しの上位5語(重い=間違い・時間切れが先)', d['dw'] == ['iced', 'slice', 'aisle', 'latte', 'carrot cake'] and len(d['n']) == 5, d['dw'])
    q.screenshot(path='/tmp/t053_dream.png')
    for i in range(80):
        q.wait_for_timeout(500)
        if q.evaluate("()=>window.__done") == 1: break
    s = q.evaluate("()=>({m:__T.save.missed.map(function(x){return x[0]}),w:__T.save.wrec,done:window.__done,view:__T.G.view,ph:Array.from(window.__ph)})")
    txt = q.evaluate("()=>window.__txt.join('\\n')")
    print('  夢のあと 持ち越し:', s['m'], 'wrec', dict((k, v['o']) for k, v in s['w'].items()), 'view', s['view'])
    chk('C2 夢の中は3択にしない(選択肢・Word Battle・Meaning なし)', 'CHOICES' not in s['ph'] and 'words' not in s['ph'] and 'reveal' not in s['ph'] and 'opts' not in s['ph'], s['ph'])
    chk('C3 自然に通じた語(台本のある語)は持ち越しから外れ、夢で通じた記録が残る', all(k not in s['m'] for k in ['iced', 'slice', 'latte', 'carrot cake']) and s['w'].get('iced', {}).get('o') == 'dream', s['m'])
    chk('C4 台本のない語(aisle)も夢に出て、言えれば外れる。上位5語に入らなかった語(shillings・receipt)は残る', 'aisle' not in s['m'] and s['m'] == ['shillings', 'receipt'], s['m'])
    chk('C5 夢が終わると、元の流れ(done)に戻る', s['done'] == 1 and s['view'] == 'map', (s['done'], s['view']))
    chk('C6 夢の画面に点数・○×・日本語・「復習」「テスト」が出ない(カンペ画面そのものの既存の文字=カンペ・おてほん・ヘルプ・発音の結果は除く)', not any(w in txt for w in ['復習', 'テスト', '点', '○', '×']) and not re.search(JP, re.sub('カンペ|おてほん|もういちど|ヘルプ|残り|達人賢者|強化合宿|回|きいてます|語|7割未満', '', txt)), re.findall(JP + '+', re.sub('カンペ|おてほん|もういちど|ヘルプ|残り|達人賢者|回|きいてます|語|7割未満', '', txt))[:5])
    # 通じなかった語は残る(音声認識がちがう言葉を返す)
    q.evaluate("(m)=>{var T=__T;T.save.missed=m;T.save.wrec={};window.__done=0;window.__wrong=1;"
               "var F=window.SpeechRecognition;F.prototype.start=function(){var me=this;setTimeout(function(){var rs=[{transcript:'zzz qqq',confidence:.5}];rs.isFinal=true;if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},20)},60)};"
               "T.dreamStart(function(){window.__done=1})}", miss[:2])
    for i in range(100):
        q.wait_for_timeout(500)
        if q.evaluate("()=>window.__done") == 1: break
    s = q.evaluate("()=>({m:__T.save.missed.map(function(x){return x[0]}),done:window.__done})")
    chk('C7 通じなかった(言えなかった)語は持ち越しに残り、夢は止まらずに終わる', sorted(s['m']) == ['iced', 'latte'] and s['done'] == 1, s)
    q.close()
    # 夜の1枚 → 夢 → 次の朝の1枚(休む流れ)
    sv = {'seen': {}, 'ticket': 'ow', 'missed': [['latte', '/l/', 'ラテ', '遅い'], ['iced', '/i/', '冷たい', '間違い']]}
    q = seed(ctx, 'kanpe-tour-save-v1', sv, tseed('ow', 5, 5, 'night')); q.route('**/tour/index.html', hooked)
    q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800)
    OV = "()=>{var o=document.querySelector('.trip-ov');return o?o.innerText.replace(/\\s+/g,' ').slice(0,120):null}"
    o = q.evaluate(OV); chk('C8 夜の1枚(Good night)が出る', bool(o) and 'Good night' in o, o)
    q.wait_for_timeout(1600); q.evaluate("()=>document.querySelector('.trip-ov').click()"); q.wait_for_timeout(1200)
    v = q.evaluate("()=>({sc:__T.G.scene&&__T.G.scene.vid,view:__T.G.view})"); chk('C9 夜の1枚を閉じると、夢の場面が始まる(持ち越しの語があるとき)', v['sc'] == 'dream_1' and v['view'] == 'scene', v)
    q.screenshot(path='/tmp/t053_night_dream.png')
    for i in range(60):
        q.wait_for_timeout(500)
        o = q.evaluate(OV)
        if o and 'DAY' in o and 'Good night' not in o: break
    chk('C10 夢のあと、次の日の朝の1枚(DAY)へ続く', bool(o) and 'DAY' in o, o)
    chk('C11 夢で通じた語が持ち越しから外れている', q.evaluate("()=>JSON.parse(localStorage.getItem('kanpe-tour-save-v1')).missed.length") == 0)
    q.close()
    # 持ち越しがなければ夢は出ない
    q = seed(ctx, 'kanpe-tour-save-v1', {'seen': {}, 'ticket': 'ow'}, tseed('ow', 5, 5, 'night')); q.route('**/tour/index.html', hooked)
    q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800); q.wait_for_timeout(1600); q.evaluate("()=>document.querySelector('.trip-ov').click()"); q.wait_for_timeout(1200)
    o = q.evaluate(OV); chk('C12 持ち越しがないときは夢を挟まず、そのまま次の朝へ', q.evaluate("()=>__T.G.scene&&__T.G.scene.vid")!='dream_1' and bool(o) and 'DAY' in o, o); q.close()
    # D. ドーハ版でも夢が動く(夜の1枚のあとの入口は trip.js 共通)
    q = seed(ctx, 'kanpe-tour-save-v1', {'seen': {}, 'ticket': 'ow'}, tseed('ow', 7, 7, 'day')); q.route('**/tour/doha/index.html', hooked)
    q.goto(base + '/tour/doha/index.html'); q.wait_for_timeout(1800)
    chk('D1 ドーハ版にも夢の入口がある', q.evaluate("()=>typeof __T.TRIP.hooks.dream") == 'function')
    q.evaluate("()=>{var T=__T;T.save.missed=[['passport','/p/','パスポート','遅い'],['aisle','/a/','通路','間違い']];window.__done=0;T.dreamStart(function(){window.__done=1})}")
    for i in range(60):
        q.wait_for_timeout(500)
        if q.evaluate("()=>window.__done") == 1: break
    chk('D2 ドーハ版: 夢が終わり、通じた語は持ち越しから外れる', q.evaluate("()=>window.__done") == 1 and q.evaluate("()=>__T.save.missed.length") == 0)
    q.close()
    # E. 夢の置き場所: 051の nbo_room(ホテルの部屋)の最後 → 夢 → 地図。同じ夜に二度は見ない
    q = seed(ctx, 'kanpe-tour-save-v1', {'seen': {}, 'ticket': 'ow'}, tseed('ow', 4, 4, 'day')); q.route('**/tour/index.html', hooked)
    q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800)
    q.evaluate("()=>{var T=__T;T.save.missed=[['latte','/l/','ラテ','遅い'],['iced','/i/','冷たい','間違い']];T.enterPlace('hroom')}")
    q.wait_for_timeout(500); q.evaluate("()=>document.querySelector('.btn.go').click()")
    for i in range(40):
        q.wait_for_timeout(500)
        if q.evaluate("()=>__T.G.scene&&__T.G.scene.vid")=='dream_1': break
        q.evaluate("()=>{var b=document.querySelector('#panel .btn.sub');if(b)b.click()}")
    chk('E1 nbo_room の6行のあと、持ち越しがあれば夢の場面に入る', q.evaluate("()=>__T.G.scene&&__T.G.scene.vid")=='dream_1')
    q.close()
    q = seed(ctx, 'kanpe-tour-save-v1', {'seen': {}, 'ticket': 'ow'}, tseed('ow', 4, 4, 'day')); q.route('**/tour/index.html', hooked)
    q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800)
    q.evaluate("()=>{var T=__T;T.save.missed=[];T.enterPlace('hroom')}")
    q.wait_for_timeout(500); q.evaluate("()=>document.querySelector('.btn.go').click()")
    for i in range(40):
        q.wait_for_timeout(500)
        if q.evaluate("()=>__T.G.view")=='map': break
        q.evaluate("()=>{var b=document.querySelector('#panel .btn.sub');if(b)b.click()}")
    chk('E2 持ち越しがなければ、夢を挟まず地図へ戻る', q.evaluate("()=>__T.G.view")=='map')
    q.close()
    chk('JSエラーなし', not ERR, ERR)
    br.close()
print('NG:', bad if bad else 'なし'); sys.exit(1 if bad else 0)
