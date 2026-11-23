# -*- coding: utf-8 -*-
"""タスク059 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_hnd059.py
28日目の羽田に戻った場面 hnd_return(1日目に拾った落とし物=木のおもちゃの飛行機を、持ち主に返す)。
A. 出る条件: 保存の keep.hnd1 があるセーブ(oneworld の28日目)だけ。ない人・スターには、場面も「羽田」タブも出ない。既存の1〜27日の並びは変えない
B. 会話: 分かれ目2か所・英語の返事だけ(日本語なし)・Word Battle/Meaning なし・点数/○×/「復習」「テスト」なし・聞き違えた返事で言い直してくれる・完了(save.seen)
C. 記録: 新しい保存キーを作らない(localStorage のキーの数)・keep.hnd1 は残る・カバンの記録帳が「ひろった」→「かえした」・「かいわ n / 全部」の分母が変わらない
D. 世界マップ: 羽田の「くうこうに もどる」が28日目だけ ../tour/ へ
マイク・実機の見え方・実機の音は確認できない(このテストの音声認識は、カンペの文をそのまま返す偽物)。"""
import os, sys, json, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    hk = ("window.__T={G:G,save:save,PBY:PBY,DLG:DLG,MODES:MODES,setMode:setMode,showMap:showMap,enterPlace:enterPlace,startVid:startVid,"
          "ART:ART,TRIP:TRIP,artIdFor:artIdFor,MODE:function(){return MODE},TOUR_IDS:TOUR_IDS,lockedPlace:lockedPlace,hretOn:hretOn};")
    route.fulfill(response=r, body=body.replace(HOOK, hk + HOOK, 1))
bad = []; ERR = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
JP = r"[぀-ヿ㐀-鿿]"
POLL = ("window.__txt=[];window.__ph=new Set();window.__dq=[];(function(){var t=setInterval(function(){var m=document.getElementById('msgText');if(m){clearInterval(t);new MutationObserver(function(){window.__txt.push(m.textContent)}).observe(m,{childList:true,characterData:true,subtree:true})}},30)})();setInterval(function(){try{"
        "var m=document.getElementById('msgText');if(m)window.__txt.push(m.textContent);"
        "var p=document.getElementById('panel')||document.querySelector('.panel');if(p){window.__txt.push(p.innerText);"
        "if(p.querySelector('.choices'))window.__ph.add('CHOICES');if(p.querySelector('.reveal'))window.__ph.add('REVEAL');"
        "[].forEach.call(p.querySelectorAll('.dq'),function(b){window.__dq.push(b.textContent)})}}catch(e){}},60)")
LEGS = [('HND', 'DOH'), ('DOH', 'NBO'), ('NBO', 'DOH'), ('DOH', 'HEL'), ('HEL', 'RVN'), ('RVN', 'MAD'), ('MAD', 'LIM'), ('LIM', 'CUZ'), ('CUZ', 'LIM'), ('LIM', 'MIA'), ('MIA', 'DFW'), ('DFW', 'HNL'), ('HNL', 'HND')]
def tseed(tk, td, day, ph):
    legs = LEGS if tk == 'ow' else LEGS
    return {'v': 1, 'trip': 1, 'tk': tk, 'day': day, 'td': td, 'ph': ph, 'bun': 1,
            'legs': [{'i': i, 'fr': a, 'to': b, 'd': None, 'f': 1, 'l': 1} for i, (a, b) in enumerate(legs)],
            'days': [], 'cur': {'led': [], 'pick': []}}
def seed(ctx, sv, trip):
    q = ctx.new_page(); q.on('pageerror', lambda e: ERR.append(str(e)[:160]))
    q.add_init_script("if(!localStorage.getItem('kanpe-tour-save-v1')){localStorage.setItem('kanpe-tour-save-v1',%s);localStorage.setItem('kanpe-trip-v1',%s)}" % (json.dumps(json.dumps(sv)), json.dumps(json.dumps(trip))))
    q.route('**/tour/index.html', hooked); return q
DEP = {k: 1 for k in ['hnd_checkin_ow', 'hnd_sec', 'hnd_exit', 'hnd_gate_ow', 'hnd_board_ow', 'hnd_plane_ow']}   # 1日目の羽田の出発は遊び終えている(出発の途中ではない)
SV_KEEP = {'seen': dict(DEP), 'ticket': 'ow', 'keep': {'hnd1': 1}}
SV_NONE = {'seen': dict(DEP), 'ticket': 'ow'}
with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
    # ---------------- A. 出る条件 ----------------
    info = {}
    for name, sv, tk, ph in [('keep', SV_KEEP, 'ow', 'morning'), ('none', SV_NONE, 'ow', 'morning'), ('star', dict(SV_KEEP, ticket='star'), 'star', 'morning')]:
        ctx2 = br.new_context(viewport={'width': 430, 'height': 900}); ctx2.add_init_script(INIT)
        q = seed(ctx2, sv, tseed(tk, 28, 27, ph)); q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800)
        info[name] = q.evaluate("""()=>{var T=__T.TRIP,r=T.rowOf(28),o={};o.gt=T.groupTd('hnd_ret');o.reach=T.reachable(28);o.next27=T.nextTd(27);o.max=T.maxTd();
          var st=T.state();o.st=[st.ph,st.td,st.day];o.mode=__T.MODE();o.modes=Object.keys(__T.MODES);o.lock=__T.lockedPlace('hreturn');o.hret=__T.hretOn();
          o.rest=[1,2,3,27].map(function(d){return T.rowOf(d)[5].join('+')});return o}""")
        q.close(); ctx2.close()
    k, n, st = info['keep'], info['none'], info['star']
    chk('A1 keep あり(oneworld): 28日目に hnd_ret が載り、朝の1枚で日が開く(ph=day・td=28・Day 28)', k['gt'] == 28 and k['reach'] and k['st'] == ['day', 28, 28], (k['gt'], k['reach'], k['st']))
    chk('A2 keep なし: 28日目は今までどおり「まだ作っていない日」(載らない・開かない・朝のまま・最終日=27のまま)', n['gt'] == 0 and not n['reach'] and n['st'][0] != 'day' and n['max'] != 28, (n['gt'], n['reach'], n['st'], n['max']))
    chk('A3 スター券: 28日目はグアム(羽田ではない)。keep があっても場面は載らない', st['gt'] == 0 and not st['reach'], st['gt'])
    chk('A4 「羽田」タブ(hret)は keep ありの28日目をあそぶ最中だけ出て、朝の1枚のあとそのタブへ移る。keep なし・スターでは出ない・移らない', k['hret'] and k['mode'] == 'hret' and not n['hret'] and n['mode'] != 'hret' and not st['hret'] and st['mode'] != 'hret', (k['hret'], k['mode'], n['hret'], n['mode'], st['hret']))
    chk('A5 モードの並び: hret は hdep のあと・arr の前', k['modes'] == ['sage', 'hdep', 'hret', 'arr', 'stay', 'air', 'dep'], k['modes'])
    chk('A6 既存の日の並びは変わらない(1・2・3・27日目)', k['rest'] == n['rest'] and k['rest'][0] == 'hnd+hnd_dep' and k['rest'][1] == 'nbo_arr', k['rest'])
    # ---------------- B・C. 会話と記録 ----------------
    def go(sv, tk='ow'):
        c = br.new_context(viewport={'width': 430, 'height': 900}); c.add_init_script(INIT)
        q = seed(c, sv, tseed(tk, 28, 27, 'morning')); q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800); q.evaluate(POLL); return q, c
    def play(q, picks, waits=(200, 200)):
        q.evaluate("()=>{__T.save.missed=[];__T.save.wrec={};window.__ph.clear();window.__txt.length=0;window.__dq.length=0}")
        q.evaluate("()=>{__T.startVid(__T.PBY['hreturn'],'hnd_return',null)}")
        q.wait_for_timeout(500); q.evaluate("()=>{document.querySelectorAll('.trip-ov').forEach(function(o){o.remove()})}"); q.click('.btn.go', force=True); k = 0; seenq = []
        for step in range(300):
            q.wait_for_timeout(200)
            n = q.evaluate("()=>document.querySelectorAll('.dq').length")
            if n and k < 2:
                q.wait_for_timeout(waits[k]); seenq.append(q.evaluate("()=>[].map.call(document.querySelectorAll('.dq'),function(b){return b.textContent})"))
                q.evaluate("(i)=>{document.querySelectorAll('.dq')[i].click()}", picks[k]); k += 1; q.wait_for_timeout(600)
            if k >= 2 and q.evaluate("()=>__T.save.seen['hnd_return']>0"): q.wait_for_timeout(700); break
        return k, seenq
    q, c = go(SV_KEEP)
    keys0 = q.evaluate("()=>Object.keys(localStorage).sort()")
    ids = q.evaluate("()=>({ids:__T.TOUR_IDS.length,has:__T.TOUR_IDS.indexOf('hnd_return')>=0,dlg:!!__T.DLG.hnd_return,bg:__T.DLG.hnd_return&&__T.DLG.hnd_return.bg,conv:__T.DLG.hnd_return&&__T.DLG.hnd_return.conv,keep:__T.DLG.hnd_return&&__T.DLG.hnd_return.keep||null,art:__T.artIdFor({d:__T.DLG.hnd_return,vid:'hnd_return'})})")
    chk('B0 場面の形: 既存の背景(hgateOW)・既存の出発ゲートの絵(hgate_ow)・conv=1(Word Battle なし)・keep は付けない(新しい拾い物を作らない)', ids['dlg'] and ids['bg'] == 'hgateOW' and ids['art'] == 'hgate_ow' and ids['conv'] == 1 and ids['keep'] is None, ids)
    chk('C1 「かいわ n / 全部」の分母(TOUR_IDS)に入れない(出ない人の分母を変えない)', not ids['has'], ids['ids'])
    # 通じた返事(ok=1)を選ぶ: 1つめ=0番(plane)・2つめ=0番(home)
    k, sq = play(q, [0, 0])
    s = q.evaluate("()=>({seen:__T.save.seen,keep:__T.save.keep,w:__T.save.wrec,m:__T.save.missed,ph:Array.from(window.__ph),txt:window.__txt.join('\\n'),view:__T.G.view})")
    alltxt = '\n'.join(sum(sq, []))
    chk('B1 分かれ目は2か所(▶の英語の返事を3つから選ぶ)', k == 2 and all(len(x) == 3 for x in sq), [len(x) for x in sq])
    chk('B2 選択肢は英語だけ(日本語なし)・点数/○×/「復習」「テスト」なし', not re.search(JP, alltxt) and not any(w in s['txt'] for w in ['復習', 'テスト', '点', '○', '×', '正解']), alltxt[:90])
    chk('B3 Word Battle・Meaning!・3択の答え合わせは出ない', 'words' not in s['ph'] and 'REVEAL' not in s['ph'] and 'CHOICES' not in s['ph'], s['ph'])
    chk('B4 終わると場面の完了(save.seen.hnd_return=1)', s['seen'].get('hnd_return') == 1, s['seen'])
    chk('B5 通じた返事をすぐ選ぶと「即答」(持ち越しに入らない)', all(s['w'].get(w, {}).get('o') == 'fast' for w in ['airplane', 'thank']) and not s['m'], dict((a, b['o']) for a, b in s['w'].items()))
    chk('B6 台詞の英語は出る(相手の最初の一言・最後の一言)', 'A month ago, I lost a small toy' in s['txt'] and 'Welcome home, travelers' in s['txt'], '')
    keys1 = q.evaluate("()=>Object.keys(localStorage).sort()")
    new = sorted(set(keys1) - set(keys0) - {'kanpe-pron-v1'})   # kanpe-pron-v1 は どの会話場面でも書く 既存の発音の記録(この場面が作ったものではない)
    chk('C2 新しい保存キーを作らない(既存の発音の記録 kanpe-pron-v1 を除いて、localStorage のキーが増えない)', not new, new)
    chk('C3 keep.hnd1 はそのまま残る(拾った記録を消さない)・keep に新しいキーは増えない', s['keep'] == {'hnd1': 1}, s['keep'])
    # 28日目はその日の最後の場面 → 夜の1枚へ
    ov = q.evaluate("()=>({day:__T.TRIP.dayDone(28),ov:!!document.querySelector('.trip-ov'),view:__T.G.view})")
    chk('C4 この場面で28日目が終わる(dayDone)・マップか夜の1枚へ戻る', ov['day'] and (ov['view'] == 'map' or ov['ov']), ov)
    # 記録帳の1行
    line = q.evaluate("""()=>{var f=document.getElementById('setView');var tt=[].map.call(document.querySelectorAll('.tt'),function(e){return e.textContent});return tt.filter(function(t){return /わすれもの|かいわ/.test(t)})}""")
    print('   記録帳(設定を開く前):', line)
    q.evaluate("()=>{var b=document.getElementById('setBtn')||document.querySelector('[data-set],.setbtn');if(b)b.click()}")
    q.wait_for_timeout(500)
    lines = q.evaluate("()=>[].map.call(document.querySelectorAll('.tt'),function(e){return e.textContent}).filter(function(t){return /わすれもの|かいわ/.test(t)})")
    chk('C5 カバンの記録帳: 返したあとは「かえした もの：ちいさな わすれもの」(拾っただけの間は「ひろった」)', any(t.startswith('かえした') for t in lines) and not any(t.startswith('ひろった') for t in lines), lines)
    q.close(); c.close()
    # 拾っただけの間(返す前): 「ひろった」のまま
    q, c = go(SV_KEEP)
    q.evaluate("()=>{var b=document.getElementById('setBtn')||document.querySelector('[data-set],.setbtn');if(b)b.click()}"); q.wait_for_timeout(500)
    lines0 = q.evaluate("()=>[].map.call(document.querySelectorAll('.tt'),function(e){return e.textContent}).filter(function(t){return /わすれもの/.test(t)})")
    chk('C6 返す前は「ひろった もの：ちいさな わすれもの」のまま', any(t.startswith('ひろった') for t in lines0), lines0)
    q.close(); c.close()
    # 聞き違えた返事(ok なし): 1つめ=1番(plain)・2つめ=1番(tank)
    q, c = go(SV_KEEP)
    k, sq = play(q, [1, 1])
    s = q.evaluate("()=>({seen:__T.save.seen,m:__T.save.missed,txt:window.__txt.join('\\n')})")
    why = dict((m[0], m[3]) for m in s['m'])
    chk('B7 聞き違えた返事を選ぶと「間違い」で持ち越し。物語は止まらず終わる', why == {'airplane': '間違い', 'thank': '間違い'} and s['seen'].get('hnd_return') == 1, why)
    chk('B8 選び方で相手の反応が変わる(聞き違え→言い直してくれる)', 'Not a plain' in s['txt'] and 'not a tank' in s['txt'] and 'wonderful news' not in s['txt'], [x for x in ['Not a plain', 'not a tank', 'wonderful news'] if x in s['txt']] or s['txt'][:200])
    q.close(); c.close()
    # D. 28日目の途中(day)で「羽田」タブが出る・初期のタブが hret
    q, c = go(SV_KEEP)
    d = q.evaluate("()=>({on:__T.hretOn(),mode:__T.MODE(),tab:[].map.call(document.querySelectorAll('[data-m]'),function(b){return [b.dataset.m,b.hidden]})})")
    hv = dict(d['tab'])
    chk('D1 28日目をあそぶ最中は「羽田」タブが出て、そのタブへ移る(朝の1枚を開いたあと)', d['on'] and d['mode'] == 'hret' and hv.get('hret') is False, d)
    chk('D2 同じ日、ほかのタブの出し隠しは今までどおり(hdep は隠れる)', hv.get('hdep') is True, hv)
    q.close(); c.close()
    # E. 世界マップ: 羽田の「くうこうに もどる」
    c = br.new_context(viewport={'width': 430, 'height': 900}); c.add_init_script(INIT)
    q = c.new_page(); q.on('pageerror', lambda e: ERR.append(str(e)[:160]))
    q.add_init_script("if(!localStorage.getItem('kanpe-tour-save-v1')){localStorage.setItem('kanpe-tour-save-v1',%s);localStorage.setItem('kanpe-trip-v1',%s);localStorage.setItem('kanpe-world-v1',%s)}" % (
        json.dumps(json.dumps(SV_KEEP)), json.dumps(json.dumps(dict(tseed('ow', 28, 28, 'day')))), json.dumps(json.dumps({'v': 1, 'at': 'haneda', 'seen': {'haneda': 1}, 'cleared': {'haneda': 1}}))))
    q.goto(base + '/world/index.html'); q.wait_for_timeout(1800)
    mb = q.evaluate("()=>{var b=document.getElementById('mBack');return b?b.hidden:'none'}")
    q.close(); c.close()
    c = br.new_context(viewport={'width': 430, 'height': 900}); c.add_init_script(INIT)
    q = c.new_page(); q.on('pageerror', lambda e: ERR.append(str(e)[:160]))
    q.add_init_script("if(!localStorage.getItem('kanpe-tour-save-v1')){localStorage.setItem('kanpe-tour-save-v1',%s);localStorage.setItem('kanpe-trip-v1',%s);localStorage.setItem('kanpe-world-v1',%s)}" % (
        json.dumps(json.dumps(SV_NONE)), json.dumps(json.dumps(dict(tseed('ow', 28, 28, 'day')))), json.dumps(json.dumps({'v': 1, 'at': 'haneda', 'seen': {'haneda': 1}, 'cleared': {'haneda': 1}}))))
    q.goto(base + '/world/index.html'); q.wait_for_timeout(1800)
    mb0 = q.evaluate("()=>{var b=document.getElementById('mBack');return b?b.hidden:'none'}")
    chk('E1 世界マップ(羽田)の「くうこうに もどる」: 28日目をあそぶ日(keep あり)だけ出る。keep なしの同じ日は出ない(今までどおり)', mb is False and mb0 is True, (mb, mb0))
    q.close(); c.close()
    chk('Z ページのエラーなし', not ERR, ERR[:3])
print('NG:', bad if bad else 'なし')
sys.exit(1 if bad else 0)
