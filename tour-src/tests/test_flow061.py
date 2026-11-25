# -*- coding: utf-8 -*-
"""タスク061 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_flow061.py
対象は nbo_java1 だけ(d.flow2 のスイッチ)。新しい流れ:
 1 店員が英語で話す / 2 選ぶのは1場面に1回・日本語の短い単語カード(カード払い・現金・M-Pesa) / 3 M-Pesa は「What is M-Pesa?」と聞く→短い説明→支払い
 4 カードを押すと見本の英語が音声だけで流れる(文字なし) / 5 そのあとカンペ(文字)が出て声に出す / 6 間違えたら、おてほんボタンなしで自動でおてほん→言い直し
 7 発音の数値は出さない(通じたかは店員の反応) / 8 支払いは目に見える形(選んだ方法で払い、コーヒーとケーキが出る)
裏の反応時間の測定→持ち越し(053)は続く。ルルの代行回数・ポイント・スパルタ教室は入れない(詰んだときは今までのヘルプ)。
マイク・実機の音・見え方は確認できない(このテストの音声認識と声は偽物)。"""
import os, sys, json, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    hk = "window.__T={G:G,save:save,startVid:startVid,PBY:PBY,DLG:DLG,get PAYFX(){return typeof PAYFX!=='undefined'?PAYFX:null}};"
    route.fulfill(response=r, body=body.replace(HOOK, hk + HOOK, 1))
bad = []; ERR = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
JP = r"[぀-ヿ㐀-鿿]"
# 声(発話)と音声認識の記録・失敗の注入。INIT のあとに足す
SPY = """
(function(){var o=speechSynthesis.speak;window.__sp=[];
 speechSynthesis.speak=function(u){try{window.__sp.push({t:u.text,r:u.rate,ph:(window.__T&&__T.G.phase)||null,cue:!!document.querySelector('#panel .cue'),pan:(document.getElementById('panel')||{}).innerText||''})}catch(e){}o.call(speechSynthesis,u)};
 var P=window.SpeechRecognition.prototype,os=P.start;window.__srn=0;window.__bad=0;
 P.start=function(){window.__srn++;if(window.__bad>0){window.__bad--;var me=this;setTimeout(function(){var rs=[{transcript:'blah blah blah',confidence:.5}];rs.isFinal=true;if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},20)},60);return}return os.apply(this,arguments)}})();
"""
POLL = ("window.__ph=[];window.__pan=[];window.__btn=new Set();window.__cs=0;window.__csp=false;window.__msg=[];"
        "new MutationObserver(function(ms){ms.forEach(function(m){[].forEach.call(m.addedNodes,function(n){if(n.nodeType===1&&(n.classList.contains('jcards')||(n.querySelector&&n.querySelector('.jcards'))))window.__cs++})})}).observe(document.getElementById('panel'),{childList:true,subtree:true});"
        "setInterval(function(){try{var T=window.__T;if(!T)return;var ph=T.G.phase;var a=window.__ph;if(a[a.length-1]!==ph)a.push(ph);"
        "var p=document.getElementById('panel');var tx=p?p.innerText.replace(/\\s+/g,' '):'';window.__pan.push(ph+'|'+tx);"
        "[].forEach.call(document.querySelectorAll('#panel button'),function(b){window.__btn.add(b.textContent.trim())});"
        "var m=document.getElementById('msgText');if(m)window.__msg.push(m.textContent)}catch(e){}},40)")
LEGS = [('HND', 'DOH'), ('DOH', 'NBO'), ('NBO', 'DOH'), ('DOH', 'HEL'), ('HEL', 'RVN'), ('RVN', 'MAD'), ('MAD', 'LIM'), ('LIM', 'CUZ'), ('CUZ', 'LIM'), ('LIM', 'MIA'), ('MIA', 'DFW'), ('DFW', 'HNL'), ('HNL', 'HND')]
def tseed():
    return {'v': 1, 'trip': 1, 'tk': 'ow', 'td': 6, 'day': 6, 'ph': 'day', 'bun': 1,
            'legs': [{'i': i, 'fr': a, 'to': b, 'd': None, 'f': 1 if i < 2 else 0, 'l': 1 if i < 2 else 0} for i, (a, b) in enumerate(LEGS)],
            'days': [], 'cur': {'led': [], 'pick': []}}
def newpage(ctx, base, vid='nbo_java1'):
    q = ctx.new_page(); q.on('pageerror', lambda e: ERR.append(str(e)[:160]))
    q.add_init_script("localStorage.setItem('kanpe-tour-save-v1',%s);localStorage.setItem('kanpe-trip-v1',%s);" % (json.dumps(json.dumps({'seen': {}, 'ticket': 'ow'})), json.dumps(json.dumps(tseed()))))
    q.route('**/tour/index.html', hooked); q.goto(base + '/tour/index.html'); q.wait_for_timeout(1700); q.evaluate(POLL)
    return q
PX = "(xy)=>{var cv=document.getElementById('sceneA'),g=cv.getContext('2d'),d=g.getImageData(380+xy[0]*3,324+xy[1]*3,1,1).data;return [d[0],d[1],d[2]]}"
def play(q, pick, wait_tap=150, vid='nbo_java1', cap=None):
    """場面を始め、カードの画面が出たら wait_tap ミリ秒おいて pick 番目を押し、マップに戻るまで進める。cap: 'pay' の最中の画素を調べる"""
    q.evaluate("(v)=>{var T=__T;T.save.missed=[];T.save.wrec={};T.save.seen={};window.__sp.length=0;window.__ph.length=0;window.__pan.length=0;window.__btn.clear();window.__cs=0;window.__srn=0;window.__msg.length=0;T.startVid(T.PBY.java,v,null)}", vid)
    q.wait_for_timeout(500); q.click('.btn.go'); tapped = False; out = {'px_before': None, 'px_after': None, 'kind': None}
    out['px_before'] = q.evaluate(PX, [176, 50])
    for i in range(500):
        q.wait_for_timeout(50)
        if not tapped and q.evaluate("()=>document.querySelectorAll('.jcard').length"):
            q.wait_for_timeout(wait_tap); q.evaluate("(i)=>document.querySelectorAll('.jcard')[i].click()", pick); tapped = True
        if q.evaluate("()=>__T.G.phase") == 'pay' and out['kind'] is None:
            out['kind'] = q.evaluate("()=>__T.PAYFX&&__T.PAYFX.k")
            q.wait_for_timeout(2400); out['px_after'] = q.evaluate(PX, [176, 50]); out['res'] = q.evaluate("()=>!!(__T.PAYFX&&__T.PAYFX.res)")
        if q.evaluate("()=>__T.G.view") == 'map': break
    return out
with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT); ctx.add_init_script(SPY)
    q = newpage(ctx, base)
    # ---------- A. カードで払う(1番目) ----------
    o = play(q, 0)
    s = q.evaluate("()=>({view:__T.G.view,seen:__T.save.seen,sp:window.__sp,ph:window.__ph,cs:window.__cs,btn:Array.from(window.__btn),pan:window.__pan,msg:window.__msg,turns:0})")
    print('  phases:', s['ph']); print('  ボタン:', s['btn'])
    chk('A1 選ぶのは1場面に1回(日本語カードの画面は1回だけ)', s['cs'] == 1, s['cs'])
    chk('A1b 英語の選択肢(▶の枠 .dq)は出ない', not any('dq' in p for p in []) and q.evaluate("()=>document.querySelectorAll('.dq').length") == 0)
    cards = [p.split('|', 1)[1] for p in s['pan'] if '|' in p and p.startswith('opts|')]
    ctxt = cards[0] if cards else ''
    chk('A2 カードは日本語の短い単語(カード払い・現金・M-Pesa)', all(w in ctxt for w in ['カード払い', '現金', 'M-Pesa']) and len(ctxt) < 30, ctxt)
    chk('A3 店員が先に英語で話す(支払いをたずねる文が、カードの画面の上に出ている)', any('How would you like to pay' in m for m in s['msg']))
    sm = [x for x in s['sp'] if x['t'] == 'Can I pay by card?']
    chk('A4 カードを押すと見本の英語(Can I pay by card?)が声で流れる。そのとき画面にカンペ(文字)はない', bool(sm) and sm[0]['ph'] == 'sample' and not sm[0]['cue'] and 'Can I pay' not in sm[0]['pan'], sm[:1])
    chk('A5 そのあとカンペ(文字)が出て、声に出す(音声認識が走る)', any(p.startswith('cue|') and 'Can I pay by card?' in p for p in s['pan']) and s['sp'].index(sm[0]) < len(s['sp']))
    i_sample = s['ph'].index('sample'); i_cue = s['ph'].index('cue', i_sample)
    chk('A5b 順番: カード(opts)→ 見本の音声(sample)→ カンペ(cue)→ 店員の反応(rep)→ 支払い(pay)', s['ph'].index('opts') < i_sample < i_cue < s['ph'].index('rep') < s['ph'].index('pay'), s['ph'])
    chk('A6 おてほんボタンは、この場面のどの画面にも置かない', 'おてほん' not in ' '.join(s['btn']), s['btn'])
    nums = [p for p in s['pan'] if re.search(r'\d+\s*%|7割|\d+\s*/\s*\d+\s*語|\d+/\d+|Nice|Too ', p)]
    chk('A7 発音の数値(%・語数・7割)や判定の文字は、どの画面にも出ない', not nums, nums[:2])
    chk('A8 店員の反応で返す(カード→ "Of course. Card is fine." / ふつうの返事の "Okay.")', any('Of course. Card is fine.' in m for m in s['msg']))
    chk('A9 支払い: 選んだ方法=カード。払ったあと、コーヒー(茶色)が出る(画素が変わる)', o['kind'] == 'card' and o['res'] and o['px_before'] != o['px_after'] and o['px_after'][0] < 140, o)
    chk('A10 会話が終わるとマップへ戻り、場面の完了(save.seen)が +1。Word Battle・Meaning! は出ない', s['view'] == 'map' and s['seen'].get('nbo_java1') == 1 and 'words' not in s['ph'] and 'reveal' not in s['ph'], (s['view'], s['seen']))
    txt = ' '.join(s['pan'])
    chk('A11 「復習」「テスト」「点」「ポイント」「スパルタ」は出ない', not any(w in txt for w in ['復習', 'テスト', '点', 'ポイント', 'スパルタ']))
    # ---------- B. 現金(2番目) ----------
    o = play(q, 1)
    s = q.evaluate("()=>({view:__T.G.view,sp:window.__sp,ph:window.__ph,msg:window.__msg,btn:Array.from(window.__btn)})")
    chk('B1 現金: 見本が先に音声で流れ、返事は店員の反応(Cash is fine)で返り、現金の払いになる', any(x['t'] == 'Okay. I will pay in cash.' and x['ph'] == 'sample' and not x['cue'] for x in s['sp']) and any('Cash is fine' in m for m in s['msg']) and o['kind'] == 'cash' and o['px_before'] != o['px_after'], o)
    # ---------- C. M-Pesa(3番目): 分からないまま進ませない ----------
    o = play(q, 2)
    s = q.evaluate("()=>({view:__T.G.view,sp:window.__sp,ph:window.__ph,msg:window.__msg,btn:Array.from(window.__btn),pan:window.__pan,seen:__T.save.seen})")
    sp_t = [x['t'] for x in s['sp']]
    chk('C1 M-Pesa を押したら、まず見本の音声(What is M-Pesa?)→ カンペ → プレイヤーが店員に聞く', any(x['t'] == 'What is M-Pesa?' and x['ph'] == 'sample' and not x['cue'] for x in s['sp']) and any(p.startswith('cue|') and 'What is M-Pesa?' in p for p in s['pan']), sp_t)
    i_q = sp_t.index('What is M-Pesa?'); i_exp = next(i for i, t_ in enumerate(sp_t) if t_.startswith('It is money on your phone'))
    pp = s['pan']; i_cue2 = next(i for i, p_ in enumerate(pp) if p_.startswith('cue|') and 'Yes, I will pay with M-Pesa.' in p_); i_pay = next(i for i, p_ in enumerate(pp) if p_.startswith('pay|'))
    chk('C2 聞いたあと、店員が短く説明し(phone・Kenya)、そのあとで「M-Pesaで払います」を言い、支払いに進む', i_q < i_exp and 'phone' in sp_t[i_exp] and 'Kenya' in sp_t[i_exp] and i_cue2 < i_pay, sp_t[i_q:i_exp + 1])
    chk('C3 M-Pesa の支払い(スマホをかざす)が出て、コーヒーが出る。マップへ戻る', o['kind'] == 'mpesa' and o['res'] and o['px_before'] != o['px_after'] and s['view'] == 'map' and s['seen'].get('nbo_java1') == 1, o)
    chk('C4 M-Pesa でも、選ぶのは1回・おてほんボタンなし・数値なし', 'おてほん' not in ' '.join(s['btn']) and not [p for p in s['pan'] if re.search(r'\d+\s*%|7割|\d+/\d+', p)])
    # ---------- D. 間違えたら、ボタンなしで自動でおてほん→言い直し ----------
    q.evaluate("()=>{window.__bad=2}")
    o = play(q, 0)
    s = q.evaluate("()=>({view:__T.G.view,sp:window.__sp,ph:window.__ph,btn:Array.from(window.__btn),pan:window.__pan,srn:window.__srn,msg:window.__msg})")
    sp_t = [x['t'] for x in s['sp']]; cue1 = "I'd like a latte, please."
    k = sp_t.index('Sorry, one more time?') if 'Sorry, one more time?' in sp_t else -1
    chk('D1 言えなかったら、店員が聞き返し(Sorry, one more time?)、そのあと自動で見本(おてほん)が流れる(ボタンを押していない)', k >= 0 and sp_t[k + 1] == cue1 and s['sp'][k + 1]['r'] < s['sp'][k]['r'] + .2, sp_t[:8])
    chk('D2 おてほんのあと、自動で聞き取りにもどり、言い直せる(認識が3回走り、最後は通る)', s['srn'] >= 6 and s['view'] == 'map', (s['srn'], s['view']))
    chk('D3 失敗のときも、おてほんボタン・数値(7割未満・語数)は出ない', 'おてほん' not in ' '.join(s['btn']) and not [p for p in s['pan'] if re.search(r'7割|\d+/\d+語|\d+\s*%', p)], [p for p in s['pan'] if re.search(r'7割|語|%', p)][:2])
    chk('D4 失敗のあいだ、ヘルプ(今までのまま)は残っている', any('ヘルプ' in b for b in s['btn']), s['btn'])
    # ---------- E. 裏の反応時間(053)は続く ----------
    play(q, 0, 150); w = q.evaluate("()=>({w:__T.save.wrec,m:__T.save.missed})")
    chk('E1 すぐ押すと shillings は即答(fast・持ち越しに入らない)・msが記録される', w['w'].get('shillings', {}).get('o') == 'fast' and w['w']['shillings']['ms'] < 2500 and not w['m'], w)
    play(q, 0, 3200); w = q.evaluate("()=>({w:__T.save.wrec,m:__T.save.missed})"); why = dict((m[0], m[3]) for m in w['m'])
    chk('E2 3.2秒かかると「遅い」→ 持ち越し(夢の材料)に入る', why.get('shillings') == '遅い' and 3000 < w['w']['shillings']['ms'] < 5000, w['w'].get('shillings'))
    q.evaluate("(v)=>{var T=__T;T.save.missed=[];T.save.wrec={};T.save.seen={};T.startVid(T.PBY.java,v,null)}", 'nbo_java1'); q.wait_for_timeout(500); q.click('.btn.go')
    for i in range(200):
        q.wait_for_timeout(100)
        if q.evaluate("()=>document.querySelectorAll('.jcard').length"): break
    q.wait_for_timeout(5600); ph = q.evaluate("()=>__T.G.phase"); w = q.evaluate("()=>__T.save.wrec.shillings"); why = dict((m[0], m[3]) for m in q.evaluate("()=>__T.save.missed"))
    chk('E3 制限時間をこえても物語は止まらず待つ(カードのまま)。裏で「時間切れ」(ms=5000)が記録され、持ち越しに入る', ph == 'opts' and w and w['o'] == 'timeout' and w['ms'] == 5000 and why.get('shillings') == '時間切れ', (ph, w, why))
    q.evaluate("()=>document.querySelectorAll('.jcard')[0].click()")
    for i in range(200):
        q.wait_for_timeout(100)
        if q.evaluate("()=>__T.G.view") == 'map': break
    chk('E4 時間切れのあと押しても、物語は先へ進んで終わる(記録は時間切れのまま)', q.evaluate("()=>__T.G.view") == 'map' and q.evaluate("()=>__T.save.wrec.shillings.o") == 'timeout')
    # ---------- F. 詰んだときは今までのヘルプ(ルルの代行)のまま ----------
    q.evaluate("()=>{__T.save.help=5;window.__bad=0}")
    q.evaluate("(v)=>{var T=__T;T.save.missed=[];T.save.wrec={};T.save.seen={};window.__ph.length=0;T.startVid(T.PBY.java,v,null)}", 'nbo_java1'); q.wait_for_timeout(500); q.click('.btn.go'); used = False
    for i in range(400):
        q.wait_for_timeout(100)
        if q.evaluate("()=>document.querySelectorAll('.jcard').length"):
            q.evaluate("()=>{window.__bad=99;document.querySelectorAll('.jcard')[0].click()}")
        if not used and q.evaluate("()=>{var c=document.querySelector('#panel .cue'),h=document.querySelector('#panel .btn.help');return !!(c&&h&&[].map.call(c.querySelectorAll('.w'),function(x){return x.textContent}).join(' ').indexOf('Can I pay')>=0)}"):
            q.wait_for_timeout(400); q.evaluate("()=>{window.__bad=0;var b=document.querySelector('#panel .btn.help');b&&b.click()}"); used = True
        if q.evaluate("()=>__T.G.view") == 'map': break
    chk('F1 詰んだとき: ヘルプ(ルルが代わりに言う)を使うと、残り回数が減り、そのまま支払いまで進んで終わる(今までのヘルプのまま)', used and q.evaluate("()=>__T.save.help") == 4 and q.evaluate("()=>__T.G.view") == 'map' and 'pay' in q.evaluate("()=>window.__ph"), (used, q.evaluate("()=>__T.save.help"), q.evaluate("()=>window.__ph")))
    # ---------- G. ほかの場面は今のまま(タスク057 第1弾・第2弾でナイロビ・賢者・羽田にも広げたので、まだ変えていないドーハの doh_immig1 で確かめる) ----------
    q.close(); q = ctx.new_page(); q.on('pageerror', lambda e: ERR.append(str(e)[:160]))   # 第2弾で羽田も新しい流れになったので、まだ変えていないドーハ(tour/doha/)の doh_immig1 で確かめる
    q.add_init_script("localStorage.setItem('kanpe-tour-save-v1',%s);localStorage.setItem('kanpe-trip-v1',%s);" % (json.dumps(json.dumps({'seen': {}, 'ticket': 'ow'})), json.dumps(json.dumps(tseed()))))
    q.route('**/tour/doha/index.html', hooked); q.goto(base + '/tour/doha/index.html'); q.wait_for_timeout(1700); q.evaluate(POLL)
    q.evaluate("()=>{window.__bad=0}")
    q.evaluate("(v)=>{var T=__T;T.save.missed=[];T.save.wrec={};T.save.seen={};window.__btn.clear();window.__pan.length=0;var pl=null;for(var k in T.PBY){var p=T.PBY[k];if(p&&p.v&&p.v.indexOf(v)>=0){pl=p;break}} T.startVid(pl,v,null)}", 'doh_immig1'); q.wait_for_timeout(500); q.click('.btn.go')
    for i in range(60):
        q.wait_for_timeout(150)
        if q.evaluate("()=>__T.G.phase") == 'cue': break
    q.wait_for_timeout(1600)
    s = q.evaluate("()=>({btn:Array.from(window.__btn),pan:window.__pan.join('\\n')})")
    # タスク074: 数字のスコア(語数・%)は全場面で出さない(キング決定)。おてほんボタンは新しい流れではない場面に今までどおり残る
    chk('G1 doh_immig1(新しい流れではない場面)は、おてほんボタンが今までどおり出る。発音の数値(語数・%)は出ない(タスク074で全場面共通になった)', 'おてほん' in ' '.join(s['btn']) and re.search(r'\d+/\d+語', s['pan']) is None, (s['btn'], re.findall(r'\d+/\d+語[^\n]{0,12}', s['pan'])[:1]))
    for i in range(150):
        q.wait_for_timeout(200)
        if 'words' in q.evaluate("()=>window.__ph"): break
    chk('G2 doh_immig1 は今までどおり Word Battle へ進む', 'words' in q.evaluate("()=>window.__ph"))
    q.close()
    chk('Z ページのエラーなし', not ERR, ERR[:3])
    br.close()
print('FAIL' if bad else 'ALL OK', bad)
sys.exit(1 if bad else 0)
