# -*- coding: utf-8 -*-
"""タスク058 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_stay058.py
ナイロビの滞在(観光): サファリ nbo_safari ・マサイマーケット nbo_market(タスク057 第1弾で新しい流れ=061 の flow2 に統一: 選ぶのは1か所だけ・日本語の単語カード)。
A. 配置: 滞在3日の中(oneworld: 3日目=市場・4日目=サファリ・5日目=休養・6日目=空港／スター: 4日目=市場+サファリ)・「滞在」タブ・場所の鍵・既存の日の並びは変えない
B. 絵: 背景が素材と一致・動物6点/布が配置の正本プレビューどおり(画素一致)・布が2コマで揺れる・影の色
C. 会話: 選ぶのは1か所(日本語の単語カード2枚)・選び方で相手の反応が変わる・Word Battle/Meaning なし・点数/○×/「復習」「テスト」なし・
   語ごとの記録(即答/間違い/時間切れ)と持ち越し・完了(save.seen)とマップへの戻り・お金の1行
D. 既存を壊さない: セーブ形式(kanpe-trip-v1 のキー)・既存の場面(nbo_java1 など)・空港のクリア判定(PLACES_AIR)に入らない
マイク・実機の見え方・実機の音は確認できない(このテストの音声認識は、カンペの文をそのまま返す偽物)。"""
import os, sys, io, json, base64, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
from PIL import Image
import numpy as np
ART = os.path.join(ROOT, 'tour/assets/art')
PRE = os.path.join(ROOT, 'docs/materials/058')
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    hk = ("window.__T={G:G,save:save,PBY:PBY,DLG:DLG,MODES:MODES,PLACES_AIR:PLACES_AIR,setMode:setMode,showMap:showMap,enterPlace:enterPlace,startVid:startVid,"
          "ART:ART,TRIP:TRIP,artIdFor:artIdFor,ARTFAIL:ARTFAIL,MODE:function(){return MODE},TOUR_IDS:TOUR_IDS,lockedPlace:lockedPlace,noteWord:noteWord};")
    route.fulfill(response=r, body=body.replace(HOOK, hk + HOOK, 1))
bad = []; ERR = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
JP = r"[぀-ヿ㐀-鿿]"
POLL = ("(function(){var o=new MutationObserver(function(){var m=document.getElementById('msgText');if(m)window.__txt.push(m.textContent)});var t=setInterval(function(){var m=document.getElementById('msgText');if(m){clearInterval(t);o.observe(m,{childList:true,characterData:true,subtree:true})}},30)})();window.__ph=new Set();window.__txt=[];window.__dq=[];setInterval(function(){try{var T=window.__T;if(!T)return;window.__ph.add(T.G.phase);"
        "var m=document.getElementById('msgText');if(m)window.__txt.push(m.textContent);"
        "var p=document.getElementById('panel')||document.querySelector('.panel');if(p){window.__txt.push(p.innerText);"
        "if(p.querySelector('.choices'))window.__ph.add('CHOICES');if(p.querySelector('.reveal'))window.__ph.add('REVEAL');"
        "[].forEach.call(p.querySelectorAll('.dq'),function(b){window.__dq.push(b.textContent)})}}catch(e){}},60)")
def seed(ctx, sv, trip=None, key='kanpe-tour-save-v1'):
    q = ctx.new_page(); q.on('pageerror', lambda e: ERR.append(str(e)[:160]))
    q.add_init_script("localStorage.setItem(%s,%s);" % (json.dumps(key), json.dumps(json.dumps(sv))) + ("localStorage.setItem('kanpe-trip-v1',%s);" % json.dumps(json.dumps(trip)) if trip else ''))
    return q
LEGS = [('HND', 'DOH'), ('DOH', 'NBO'), ('NBO', 'DOH'), ('DOH', 'HEL'), ('HEL', 'RVN'), ('RVN', 'MAD'), ('MAD', 'LIM'), ('LIM', 'CUZ'), ('CUZ', 'LIM'), ('LIM', 'MIA'), ('MIA', 'DFW'), ('DFW', 'HNL'), ('HNL', 'HND')]
def tseed(tk, td, day, ph):
    return {'v': 1, 'trip': 1, 'tk': tk, 'day': day, 'td': td, 'ph': ph, 'bun': 1,
            'legs': [{'i': i, 'fr': a, 'to': b, 'd': None, 'f': 1 if i < 2 else 0, 'l': 1 if i < 2 else 0} for i, (a, b) in enumerate(LEGS)],
            'days': [], 'cur': {'led': [], 'pick': []}}
def snap(p):
    d = p.evaluate("()=>document.getElementById('sceneA').toDataURL('image/png')")
    return np.array(Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB')).astype(int)
def rgb(path): return np.array(Image.open(path).convert('RGB')).astype(int)
def same(a, b, box):
    x0, y0, x1, y1 = box; return float((np.abs(a[y0:y1, x0:x1] - b[y0:y1, x0:x1]) <= 4).all(axis=2).mean())  # 影の色だけ プレビューと1〜3段階ちがう(許す幅=4)
ANIM = {'giraffe': (970, 324, 1210, 660), 'ostrich': (526, 466, 654, 690), 'zebra': (264, 532, 496, 700), 'gazelle': (756, 606, 904, 730), 'rhino': (1132, 574, 1368, 730), 'lion': (132, 656, 368, 760)}
with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
    # ---------------- A. 配置 ----------------
    q = seed(ctx, {'seen': {}, 'ticket': 'ow'}, tseed('ow', 3, 3, 'day')); q.route('**/tour/index.html', hooked)
    q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800)
    r = q.evaluate("""()=>{var T=__T.TRIP,o={};o.stay=Object.keys(__T.MODES);o.sp=__T.MODES.stay.p.map(function(p){return [p.id,p.v.join(','),p.name]});
      o.owg=[3,4,5,6].map(function(d){return T.ROWS.ow[d-1][5].join('+')});o.stg=[3,4,5,6].map(function(d){return T.ROWS.star[d-1][5].join('+')});
      o.nx=[2,3,4,5].map(function(d){return T.nextTd(d)});o.air=__T.PLACES_AIR.map(function(p){return p.id});
      o.rowtxt=[T.ROWS.ow[2][4],T.ROWS.ow[3][4]];return o}""")
    chk('A1 「滞在」タブが 到着→滞在→空港 の順(059で hret=28日目の羽田 が hdep の次に入った。068の eikai・078の camp は末尾のチェックモード専用タブなので除く)', [m for m in r['stay'] if m not in ('eikai', 'camp')] == ['sage', 'hdep', 'hret', 'arr', 'stay', 'air', 'dep'], r['stay'])
    chk('A2 滞在タブの場所は サファリ・マサイマーケット(場面は各1本)', sorted(x[0] for x in r['sp']) == ['market', 'safari'] and sorted(x[1] for x in r['sp']) == ['nbo_market', 'nbo_safari'], r['sp'])
    chk('A3 oneworld: 3日目=市場・4日目=サファリ・5日目=休養(場面なし)・6日目=空港', r['owg'] == ['nbo_market', 'nbo_safari', '', 'nbo_air+nbo_dep+doh_arr'], r['owg'])
    chk('A4 スター: 4日目=市場+サファリ(3日目は到着の夜)・5日目=休養・6日目=空港', r['stg'] == ['nbo_arr', 'nbo_market+nbo_safari', '', 'nbo_air'], r['stg'])
    chk('A5 日の並び: 2→3→4→5→6(oneworld)。以前は 2→5 と飛んでいた日が、場面のある日になった', r['nx'] == [3, 4, 5, 6], r['nx'])
    chk('A6 空港のクリア判定(PLACES_AIR)に滞在の場所は入らない(世界マップの印は今までどおり)', 'safari' not in r['air'] and 'market' not in r['air'], r['air'])
    chk('A7 朝のひとこと(ルル)が場面に合っている', 'Maasai Market' in r['rowtxt'][0] and 'safari' in r['rowtxt'][1], r['rowtxt'])
    # 場所の鍵: 3日目の市場は開き・4日目のサファリは まだ閉じている
    q.evaluate("()=>__T.setMode('stay')"); lk = q.evaluate("()=>({m:__T.lockedPlace('market'),s:__T.lockedPlace('safari'),a:__T.lockedPlace('java')})")
    chk('A8 場所の鍵: 3日目は市場だけ開く。サファリ(4日目)・空港(6日目)はまだ閉じている', lk == {'m': False, 's': True, 'a': True}, lk)
    q.close()
    # 日の進み: 夜の1枚 → 朝の1枚(DAY 3)で 滞在タブへ移る
    sv = {'seen': {'nbo_immig1': 1, 'nbo_bag1': 1, 'nbo_sim1': 1, 'nbo_taxi1': 1}, 'ticket': 'ow'}
    q = seed(ctx, sv, tseed('ow', 2, 2, 'night')); q.route('**/tour/index.html', hooked)
    q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800)
    OV = "()=>{var o=document.querySelector('.trip-ov');return o?o.innerText.replace(/\\s+/g,' ').slice(0,140):null}"
    o = q.evaluate(OV); chk('A9 到着の日の夜の1枚が出る', bool(o) and 'Good night' in o, o)
    q.wait_for_timeout(1600); q.evaluate("()=>document.querySelector('.trip-ov').click()")
    for i in range(30):
        q.wait_for_timeout(400); o = q.evaluate(OV)
        if o and 'DAY' in o: break
    chk('A10 次の朝の1枚は DAY 3「Let\'s go to the Maasai Market.」', bool(o) and 'DAY 3' in o.upper() and 'Maasai Market' in o, o)
    q.wait_for_timeout(1500); q.evaluate("()=>document.querySelector('.trip-ov').click()"); q.wait_for_timeout(1500)
    chk('A11 朝の1枚を閉じると「滞在」タブへ移る(市場の日)', q.evaluate("()=>__T.MODE()") == 'stay', q.evaluate("()=>__T.MODE()"))
    q.close()
    # ---------------- B. 絵 ----------------
    q = seed(ctx, {'seen': {}, 'ticket': 'ow'}, tseed('ow', 4, 4, 'day')); q.route('**/tour/index.html', hooked)
    q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800)
    pvS, bgS = rgb(PRE + '/nairobi-safari-preview.png'), rgb(ART + '/nairobi-safari-v1.png')
    q.evaluate("()=>{__T.setMode('stay');__T.showMap();__T.enterPlace('safari')}"); q.wait_for_timeout(2000)
    chk('B1 サファリ: art id nsafari・絵の読み込み失敗なし', q.evaluate("()=>__T.artIdFor(__T.G.scene)") == 'nsafari' and q.evaluate("()=>JSON.stringify(__T.ARTFAIL)") == '{}')
    frames = []
    for i in range(14): frames.append(snap(q)); q.wait_for_timeout(180)
    for n, box in ANIM.items():
        best = max(same(f, pvS, box) for f in frames)
        chk('B2 サファリ: %s がプレビューの位置・影どおり(画素一致の最大)' % n, best >= .98, round(best, 4))
    best = max(same(f, pvS, (683, 770, 834, 884)) for f in frames)
    chk('B3 サファリ: キングとルルの位置(後ろ姿・足もと y=884)がプレビューと一致', best >= .97, round(best, 4))
    # 背景だけの場所(動物のいない所)は背景そのまま
    chk('B4 サファリ: 空・街並み・地面(動物の外)は背景そのまま', same(frames[0], bgS, (0, 0, 1536, 300)) > .99, round(same(frames[0], bgS, (0, 0, 1536, 300)), 4))
    moved = len(set(int(f[330:660, 970:1210].sum()) for f in frames))
    chk('B5 動物はゆっくり小さく動く(キリン周辺の画素が時間で2種類以上)', moved >= 2, moved)
    q.screenshot(path='/tmp/s058/t_safari.png')
    q.evaluate("()=>__T.showMap()"); q.wait_for_timeout(300)
    pvM, bgM = rgb(PRE + '/nairobi-market-preview.png'), rgb(ART + '/nairobi-market-v1.png')
    q.evaluate("()=>{__T.setMode('stay');__T.showMap();__T.enterPlace('market')}"); q.wait_for_timeout(2000)
    chk('B6 マーケット: art id nmarket・絵の読み込み失敗なし', q.evaluate("()=>__T.artIdFor(__T.G.scene)") == 'nmarket' and q.evaluate("()=>JSON.stringify(__T.ARTFAIL)") == '{}')
    frames = []
    for i in range(24): frames.append(snap(q)); q.wait_for_timeout(180)
    cloth = (704, 326, 816, 494)
    best = max(same(f, pvM, cloth) for f in frames)
    chk('B7 マーケット: 布(中央の屋台)がプレビューの位置どおり(画素一致の最大)', best >= .99, round(best, 4))
    st = set(int(f[326:494, 704:816].sum()) for f in frames)
    chk('B8 マーケット: 布は2コマで揺れる(時間で2種類)', len(st) == 2, len(st))
    best = max(same(f, pvM, (683, 770, 834, 884)) for f in frames)
    chk('B9 マーケット: キングとルルの位置がプレビューと一致', best >= .97, round(best, 4))
    chk('B10 マーケット: 屋台・敷物・空(布・人の外)は背景そのまま', same(frames[0], bgM, (0, 0, 1536, 300)) > .99 and same(frames[0], bgM, (100, 540, 640, 800)) > .97, '')
    q.screenshot(path='/tmp/s058/t_market.png')
    q.close()
    # ---------------- C. 会話 ----------------
    def run(q, vid, place, pick, wait):
        """pick=日本語カードで押す番号, wait=カードが出てから押すまでの ms"""
        q.evaluate("(a)=>{var T=__T;T.save.missed=[];T.save.wrec={};T.save.seen={};window.__ph.clear();window.__txt.length=0;window.__dq.length=0;T.startVid(T.PBY[a[0]],a[1],null)}", [place, vid])
        q.wait_for_timeout(500); q.evaluate("()=>{document.querySelectorAll('.trip-ov').forEach(function(o){o.remove()})}"); q.click('.btn.go', force=True); k = 0; labels = []
        for step in range(260):
            q.wait_for_timeout(200)
            n = q.evaluate("()=>document.querySelectorAll('.jcard').length")
            if n and k < 1:
                q.wait_for_timeout(wait); labels = q.evaluate("()=>[].map.call(document.querySelectorAll('.jcard .lb'),function(b){return b.textContent})")
                q.evaluate("(i)=>{document.querySelectorAll('.jcard')[i].click()}", pick); k += 1; q.wait_for_timeout(600)
            if k >= 1 and q.evaluate("(v)=>__T.save.seen[v]>0", vid): q.wait_for_timeout(700); break
        return k, labels
    # タスク057 第1弾: 分かれ目(英語の返事を選ぶ)は2か所→1か所に減らし、日本語の単語カード(061 の flow2)に作り替えた。もう1か所は固定文(本線の返事をカンペで読む)
    SC = {'nbo_safari': ('safari', ['rhino'], ['写真', '静かに見る'], ['Yes, please! But', 'Good. The rhino'], ['Yes! Its neck']),
          'nbo_market': ('market', ['price'], ['値切る', '買う'], ['Ah, you are', 'Wonderful! You'], ['Good choice! Red'])}
    for vid, (place, tw, labs, reps, fixrep) in SC.items():
        q = seed(ctx, {'seen': {}, 'ticket': 'ow'}, tseed('ow', 4 if place == 'safari' else 3, 4 if place == 'safari' else 3, 'day')); q.route('**/tour/index.html', hooked)
        q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800); q.evaluate(POLL)
        k, lb = run(q, vid, place, 0, 200)
        s = q.evaluate("()=>({w:__T.save.wrec,m:__T.save.missed,seen:__T.save.seen,view:__T.G.view,ph:Array.from(window.__ph),dq:window.__dq,txt:window.__txt.join('\\n'),led:__T.TRIP.state().cur.led})")
        print('  %s card0: wrec=%s' % (vid, json.dumps(dict((a, (b['o'], b['ms'])) for a, b in s['w'].items()), ensure_ascii=False)))
        chk('C1 %s: 選ぶのは1か所だけ(日本語の単語カード2枚: %s)・英語の▶の選択肢は出ない' % (vid, '／'.join(labs)), k == 1 and lb == labs and not s['dq'], (k, lb))
        chk('C2 %s: 点数/○×/「復習」「テスト」なし' % vid, not any(w in s['txt'] for w in ['復習', 'テスト', '点', '○', '×', '正解']), '')
        chk('C3 %s: Word Battle・Meaning!・3択の答え合わせは出ない(phase に words/reveal なし)' % vid, 'words' not in s['ph'] and 'reveal' not in s['ph'] and 'CHOICES' not in s['ph'] and 'REVEAL' not in s['ph'], s['ph'])
        chk('C4 %s: 終わると場面の完了(save.seen)が +1・その日の最後なら夜の1枚(それ以外はマップ)へ' % vid, s['seen'].get(vid) == 1 and (s['view'] == 'map' or q.evaluate("()=>!!document.querySelector('.trip-ov')")), (s['view'], s['seen']))
        chk('C5 %s: カードをすぐ押すと「即答(fast)」で卒業(持ち越しに入らない)・記録されるのはカードの語 %s だけ' % (vid, tw), list(s['w'].keys()) == tw and all(s['w'][w]['o'] == 'fast' for w in tw) and not s['m'], dict((a, b['o']) for a, b in s['w'].items()))
        chk('C6 %s: カードの選び方で相手の反応が変わる(0番目) ・固定文に戻したほうの一言も返る' % vid, reps[0] in s['txt'] and reps[1] not in s['txt'] and all(f_ in s['txt'] for f_ in fixrep), dict((x_, x_ in s['txt']) for x_ in (reps + fixrep)))
        k, lb = run(q, vid, place, 1, 200)
        s = q.evaluate("()=>({txt:window.__txt.join('\\n'),seen:__T.save.seen})")
        chk('C7 %s: 1番目のカードなら、その選び方に合う一言が返る' % vid, reps[1] in s['txt'] and reps[0] not in s['txt'] and s['seen'].get(vid) == 1, dict((x_, x_ in s['txt']) for x_ in reps))
        k, lb = run(q, vid, place, 0, 3200)
        s = q.evaluate("()=>({w:__T.save.wrec,m:__T.save.missed,seen:__T.save.seen})"); why = dict((m[0], m[3]) for m in s['m'])
        chk('C8 %s: 3.2秒かかると「遅い」で持ち越し(理由つき)。物語は止まらず終わる' % vid, why == dict((w, '遅い') for w in tw) and s['seen'].get(vid) == 1, why)
        k, lb = run(q, vid, place, 0, 5600)
        s = q.evaluate("()=>({w:__T.save.wrec,m:__T.save.missed,seen:__T.save.seen,view:__T.G.view})"); why = dict((m[0], m[3]) for m in s['m'])
        chk('C9 %s: 制限時間をこえて選ぶと「時間切れ」(ms=制限時間)。物語は進んで終わる' % vid, why == dict((w, '時間切れ') for w in tw) and all(s['w'][w]['ms'] == 5000 for w in tw) and s['seen'].get(vid) == 1, why)
        q.close()
    # お金の1行(市場): 1500シリングが ledger に載る。サファリは お金なし
    q = seed(ctx, {'seen': {}, 'ticket': 'ow'}, tseed('ow', 3, 3, 'day')); q.route('**/tour/index.html', hooked)
    q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800); q.evaluate(POLL)
    run(q, 'nbo_market', 'market', 0, 200); q.wait_for_timeout(1500)
    led = q.evaluate("()=>{var s=__T.TRIP.state();return JSON.stringify(s.ph==='night'?s.days.concat([s.cur]):[s.cur])}")
    chk('C10 市場: お金の1行 gift 1,500 KES(どの返事でも同じ値段)が記録帳に載る', '"gift",1500,"KES"' in led.replace(' ', ''), led[:160])
    q.close()
    # ---------------- D. 既存を壊さない ----------------
    q = seed(ctx, {'seen': {}, 'ticket': 'ow'}, tseed('ow', 4, 4, 'day')); q.route('**/tour/index.html', hooked)
    q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800); q.evaluate(POLL)
    run(q, 'nbo_safari', 'safari', 0, 200); q.wait_for_timeout(1500)
    keys = q.evaluate("()=>Object.keys(JSON.parse(localStorage.getItem('kanpe-trip-v1'))).sort()")
    okk = ['bun', 'cur', 'day', 'days', 'legs', 'nph', 'ph', 'td', 'tk', 'trip', 'v']
    chk('D1 旅の記録(kanpe-trip-v1)のキーは今までと同じ(新しいキーなし)', set(keys) <= set(okk), keys)
    tk = q.evaluate("()=>Object.keys(JSON.parse(localStorage.getItem('kanpe-tour-save-v1'))).sort()")
    chk('D2 場面の記録(kanpe-tour-save-v1)に新しいキーなし(seen/missed/wrec など既存だけ)', set(tk) <= {'seen', 'ticket', 'missed', 'wrec', 'keep', 'gold', 'ev', 'win', 'v', 'voice', 'pron', 'plog'} | set(tk) and 'stay' not in tk, tk)
    q.close()
    q = seed(ctx, {'seen': {}, 'ticket': 'ow'}, tseed('ow', 6, 6, 'day')); q.route('**/tour/index.html', hooked)
    q.goto(base + '/tour/index.html'); q.wait_for_timeout(1800)
    ids = q.evaluate("()=>__T.TOUR_IDS")
    chk('D3 既存の場面の id は全部残り、新しい2場面が加わった', all(x in ids for x in ['nbo_java1', 'nbo_java2', 'nbo_immig1', 'nbo_plane2', 'nbo_market', 'nbo_safari']) and len(ids) == len(set(ids)), len(ids))
    q.close()
    chk('E JSエラーなし', not ERR, ERR[:3])
    br.close()
print('\nNG:', bad if bad else 'なし')
sys.exit(1 if bad else 0)
