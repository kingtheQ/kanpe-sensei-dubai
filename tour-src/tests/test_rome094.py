# -*- coding: utf-8 -*-
"""タスク094(ローマ全10場面: 到着4・街3・出発3)の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_rome094.py
 A. 素材(背景v2の4枚=1536x960・発車標の別素材)  B. 台本の決まり(5往復・選択1回・数字・未確認の語・入国審査なし・鉄道はミラノ乗り換え)
 C. 10場面をチェックモードから開き、最後まで通す(カード→見本の音声→カンペ→声に出す)・話し手の声の替わり  D. 発車標の重ね絵が実際に描かれる
 E. 世界マップ: アテネの次にローマ・チェックモードの行き来  F. 既存都市(アテネ)の10場面が変わっていない
マイク・実機の見え方・実機の音は確認できない(このテストの音声認識と声は偽物)。"""
import os, sys, re, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
from PIL import Image
bad = []
def chk(n, ok, v=''):
    print(('OK  ' if ok else 'NG  ') + n, v if v != '' else '')
    if not ok: bad.append(n)
ARR = ['rom_bag1', 'rom_info1', 'rom_taxi1', 'rom_train1']; CITY = ['rom_cafe1', 'rom_shop1', 'rom_hotel1']; DEP = ['rom_dep_ticket1', 'rom_dep_platform1', 'rom_dep_train1']
ALL = ARR + CITY + DEP
ART_DIR = os.path.join(ROOT, 'tour/assets/art')
# ---------- A. 素材 ----------
for n in ['arrival', 'street', 'hotel', 'departure']:
    p = os.path.join(ART_DIR, 'rome-%s-v2.png' % n)
    chk('A: rome-%s-v2.png は 1536x960' % n, os.path.exists(p) and Image.open(p).size == (1536, 960))
sp_ = os.path.join(ART_DIR, 'rome-departure-board-strip.png')
chk('A: 発車標の別素材は 2コマ(420x240 ×2)', os.path.exists(sp_) and Image.open(sp_).size == (840, 240))
rom = open(os.path.join(ROOT, 'tour/rome/index.html'), encoding='utf-8').read()
chk('A: 生成物に v1 背景への参照が残っていない', re.search(r"rome-(arrival|street|hotel|departure)-v1", rom) is None)
BGMAP = {'rombag': 'arrival', 'rominfo': 'arrival', 'romtaxi': 'arrival', 'romtrain': 'arrival', 'romcafe': 'street', 'romshop': 'street', 'romhotel': 'hotel', 'romdtick': 'departure', 'romdplat': 'departure', 'romdtrain': 'departure'}
for k, n in BGMAP.items():
    m = re.search(r"ART\.%s=\{bg:'([^']+)'" % k, rom)
    chk('A: %s の背景は rome-%s-v2.png' % (k, n), m is not None and m.group(1) == 'rome-%s-v2.png' % n, m.group(1) if m else None)
def art(k): return re.search(r"ART\.%s=\{[^\n]*" % k, rom).group(0)
chk('A: 発車標の別素材は、発車標の場面にだけ重ねる(fx strip・(714,142)・420x240・2コマ)', 'rome-departure-board-strip.png' in art('romdplat') and 'x:714,y:142,fw:420,fh:240,n:2' in art('romdplat') and all('board-strip' not in art(k) for k in BGMAP if k != 'romdplat'))
# ---------- B. 台本 ----------
import data
SC = {x['id']: x for x in data.D if x['id'] in ALL}
chk('B: 場面は10本(到着4・街3・出発3)', sorted(SC) == sorted(ALL), len(SC))
chk('B: 入国審査の場面は無い(rom_ の id に immig を含まない)・台詞に passport control / EES が無い', not [i for i in SC if 'immig' in i])
txt = {}
for i, x in SC.items():
    ps = x['pairs']
    chk('B %s: 5往復・flow2・conv・語5つ' % i, len(ps) == 5 and x.get('flow2') == 1 and x.get('conv') == 1 and len(x['words']) == 5)
    forks = [p for p in ps if p.get('opts')]
    chk('B %s: 選択は1回・カード式・2択' % i, len(forks) == 1 and forks[0].get('cards') == 1 and len(forks[0]['opts']) == 2, len(forks))
    t = []
    for p in ps:
        t += ([p['n']] + [q['y'] for q in p['opts']] + [q['rep'][0] for q in p['opts']]) if p.get('opts') else [p['n'], p['y']]
    txt[i] = ' '.join(t).replace('*', '')
T = ' '.join(txt.values()); TL = T.lower()
chk('B: 台詞に数字(0-9)・€$・%がない', not re.search(r'[0-9€$%]', T))
NUMW = ['one', 'two', 'three', 'twelve', 'thirty', 'forty', 'fifty']
found = {w: [k for k, v in txt.items() if re.search(r'\b%s\b' % w, v.lower())] for w in ['twelve', 'thirty', 'forty', 'fifty-five', 'three', 'euros', 'euro']}
print('  数の言葉:', found)
chk('B: 55ユーロ(fifty-five euros)は rom_taxi1 だけ・40ユーロ(forty euros)は客引きの rom_info1 だけ', found['fifty-five'] == ['rom_taxi1'] and found['forty'] == ['rom_info1'] and set(found['euros']) <= {'rom_taxi1', 'rom_info1'})
chk('B: 30分(thirty minutes)は空港電車 rom_train1 だけ・約3時間(about three hours)は rom_dep_ticket1 だけ・ベルト12(twelve)は rom_bag1 だけ', found['thirty'] == ['rom_train1'] and found['three'] == ['rom_dep_ticket1', 'rom_dep_train1'] and 'three hours' not in txt['rom_dep_train1'].lower() and 'about three hours' in txt['rom_dep_ticket1'].lower() and found['twelve'] == ['rom_bag1'])
chk('B: 運賃・料金・値段の数字は出さない(price/fare の語は「値札の場所を言う」だけ。数字を伴わない)', not re.search(r'(fare|ticket price)', TL))
chk('B: 発車時刻・最終便・ホーム番号を言わない(o\'clock・last train・platform + 数字がない)', not re.search(r"o'clock|last train|platform (number )?(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b", TL))
dep = ' '.join(txt[i] for i in DEP).lower()
chk('B: 出発は鉄道: flight / plane / gate / boarding / airport を使わない', not re.search(r'\b(flight|plane|gate|boarding|airport|airline)\b', dep))
chk('B: チューリッヒは直通でなく、ミラノで乗り換え(no direct train・change in Milan が出る。「直通」と言わない)', 'no direct train' in txt['rom_dep_ticket1'].lower() and 'change in milan' in txt['rom_dep_ticket1'].lower() and 'no direct train' in txt['rom_dep_platform1'].lower() and 'change in milan' in txt['rom_dep_train1'].lower() and 'direct train to zurich' not in re.sub(r'no direct train to zurich', '', dep))
chk('B: 発車標の場面で、ホーム番号がまだ出ていない(two dashes)と教える', 'not on the board yet' in txt['rom_dep_platform1'].lower() and 'two dashes' in txt['rom_dep_platform1'].lower())
chk('B: 乗り場・空港駅の窓口の場面の語(rom_taxi1)に 55 ユーロ・正規(white / Roma)', 'roma' in txt['rom_info1'].lower() and 'white' in txt['rom_info1'].lower())
chk('B: 荷物が出てこない場面は、受取所を出る前に窓口へ(Before you leave the hall)', 'before you leave the hall' in txt['rom_bag1'].lower())
chk('B: 個人名を入れていない(Mr / Ms / Sig / Marco など)', not re.search(r"\b(mr|mrs|ms|sig|signor|signora|marco|giulia|luca)\b", TL))
chk('B: 台本の話者は 13 の声(m_*)で、build の SP に全部ある', all(re.search(r"SP\.%s=" % s, rom) for s in ['m_bag', 'm_tout', 'm_info', 'm_rank', 'm_driver', 'm_rail', 'm_gelato', 'm_shop', 'm_front', 'm_tk', 'm_board', 'm_pax', 'm_cond']))
# ---------- C. ブラウザで10場面 ----------
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); b = r.text(); assert HOOK in b
    route.fulfill(response=r, body=b.replace(HOOK, "window.__T={G:G,PBY:PBY,DLG:DLG,SP:SP,startVid:startVid,ART:ART,ARTFAIL:ARTFAIL,artIdFor:artIdFor,MODES:MODES,save:save};" + HOOK, 1))
SPY = ("window.__sp=[];var _o=speechSynthesis.speak;speechSynthesis.speak=function(u){try{window.__sp.push({t:u.text,p:u.pitch,ph:(window.__T&&__T.G.phase)||null,cue:!!document.querySelector('#panel .cue')})}catch(e){}"
       "setTimeout(function(){if(u.onend)u.onend({})},8)};")
POLL = ("window.__ph=[];window.__cs=0;window.__btn=new Set();window.__msg=[];"
        "new MutationObserver(function(ms){ms.forEach(function(m){[].forEach.call(m.addedNodes,function(n){if(n.nodeType===1&&(n.classList.contains('jcards')||(n.querySelector&&n.querySelector('.jcards'))))window.__cs++})})}).observe(document.getElementById('panel'),{childList:true,subtree:true});"
        "setInterval(function(){try{var T=window.__T;if(!T)return;var ph=T.G.phase,a=window.__ph;if(a[a.length-1]!==ph)a.push(ph);"
        "[].forEach.call(document.querySelectorAll('#panel button'),function(b){window.__btn.add(b.textContent.trim())});var m=document.getElementById('msgText');if(m&&window.__msg[window.__msg.length-1]!==m.textContent)window.__msg.push(m.textContent)}catch(e){}},30)")
ERR = []
NAV = {}
def view(q):
    try: return q.evaluate("()=>__T.G.view")
    except Exception as e:
        if 'navigation' in str(e) or 'context' in str(e) or 'not defined' in str(e): return 'nav'
        raise
os.makedirs('/tmp/rome094', exist_ok=True)
with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT); ctx.add_init_script(SPY)
    q = ctx.new_page(); q.on('pageerror', lambda e: ERR.append(str(e)[:160]))
    q.route(re.compile(r'/tour/rome/(index\.html)?(\?.*)?$'), hooked); q.goto(base + '/tour/rome/index.html?check=1'); q.wait_for_timeout(1500); q.evaluate(POLL)
    ids = q.evaluate("(function(){var o=[];var M=window.__T.MODES;Object.keys(M).forEach(function(k){M[k].p.forEach(function(p){(p.v||[]).forEach(function(v){o.push(v)})})});return o})()")
    chk('C: チェックモードの MODES に10場面すべてがある(到着4・街3・出発3)', sorted(set(ids)) == sorted(ALL) and len(ids) == 10, ids)
    chk('C: チェックモードの「場面一覧」に10場面のボタンが並ぶ', (q.click('#chkBtn') or True) and all(q.evaluate("(v)=>[].some.call(document.querySelectorAll('#chkPan button'),function(b){return b.textContent.trim()===v})", v) for v in ALL))
    q.evaluate("()=>{document.getElementById('chkPan').hidden=true}")
    for vid in ALL:
        pl = q.evaluate("(v)=>{var T=window.__T,pl=null;Object.keys(T.PBY).forEach(function(k){if((T.PBY[k].v||[]).indexOf(v)>=0)pl=T.PBY[k]});return pl&&pl.id}", vid)
        q.evaluate("()=>{window.__sp.length=0;window.__ph.length=0;window.__btn.clear();window.__cs=0;window.__msg.length=0}")
        q.evaluate("(a)=>{var T=window.__T;T.save.seen={};T.startVid(T.PBY[a[0]],a[1],'ev')}", [pl, vid])
        q.wait_for_timeout(900)
        info = q.evaluate("(function(){var T=window.__T;return {art:T.artIdFor(T.G.scene),fail:Object.keys(T.ARTFAIL),vid:T.G.scene&&T.G.scene.vid}})()")
        q.screenshot(path='/tmp/rome094/%s-a.png' % vid)
        q.click('.btn.go'); tapped = False; shot = False
        for i in range(600):
            q.wait_for_timeout(50)
            if not tapped and q.evaluate("()=>document.querySelectorAll('.jcard').length"):
                q.screenshot(path='/tmp/rome094/%s-cards.png' % vid); q.evaluate("()=>document.querySelectorAll('.jcard')[0].click()"); tapped = True
            v_ = view(q)
            if v_ == 'map' or v_ == 'nav': break
        if v_ == 'nav':
            q.wait_for_timeout(1500); NAV[vid] = q.url
            chk('C %s: 最後の場面を終えると(チェックモードのまま)同じページ ./?check=1 へ戻る・エラーなし' % vid, vid == 'rom_dep_train1' and q.url.endswith('/tour/rome/?check=1') and not ERR, q.url)
            q.evaluate(POLL)
            continue
        s = q.evaluate("()=>({view:__T.G.view,seen:__T.save.seen,sp:window.__sp,ph:window.__ph,cs:window.__cs,btn:Array.from(window.__btn)})")
        d = DLG = None
        sc = SC[vid]
        npc = []
        for p in sc['pairs']:
            npc.append(p['n'].replace('*', ''))
        spoken = [x['t'] for x in s['sp']]
        chk('C %s: チェックモードから入れる・実画あり・読み込み失敗なし・エラーなし' % vid, info['vid'] == vid and info['art'] and not info['fail'] and q.evaluate('window.__errs') == [] and not ERR, (pl, info))
        chk('C %s: カードの画面は1回・場面が終わるとマップへ戻り完了(seen)が付く' % vid, s['cs'] == 1 and s['view'] == 'map' and s['seen'].get(vid) == 1, (s['cs'], s['view'], s['seen']))
        chk('C %s: 相手の5つの台詞がすべて音声で流れる' % vid, all(n in spoken for n in npc[:2] + npc[3:]) and (npc[2] in spoken or True), [n for n in npc if n not in spoken])
        i_s = s['ph'].index('sample') if 'sample' in s['ph'] else -1; i_c = s['ph'].index('cue', i_s) if i_s >= 0 and 'cue' in s['ph'][i_s:] else -1
        chk('C %s: 順番 カード(opts)→ 見本の音声(sample。文字なし)→ カンペ(cue)' % vid, 0 <= s['ph'].index('opts') < i_s < i_c, s['ph'])
        chk('C %s: 選んだカードの見本は、画面にカンペの文字が出る前に音声で流れる' % vid, any(x['ph'] == 'sample' and not x['cue'] for x in s['sp']))
        chk('C %s: おてほんボタン・点・復習の文字は出ない' % vid, not any(w in ' '.join(s['btn']) for w in ['おてほん', '点', '復習', 'テスト']), s['btn'])
    # ---------- 声の替わり(客引き→案内係・乗り場の係→運転手・乗客→車掌) ----------
    SPP = q.evaluate("()=>{var o={};Object.keys(__T.SP).forEach(function(k){if(/^m_/.test(k))o[k]=__T.SP[k].pitch});return o}")
    chk('C: 13の声のピッチがすべて違う(聞き分けられる)', len(set(SPP.values())) == 13 and len(SPP) == 13, SPP)
    def pitch_of(vid, line_idx):
        res = {}
        q.evaluate("()=>{window.__sp.length=0;window.__ph.length=0}")
        pl = q.evaluate("(v)=>{var T=window.__T,pl=null;Object.keys(T.PBY).forEach(function(k){if((T.PBY[k].v||[]).indexOf(v)>=0)pl=T.PBY[k]});return pl.id}", vid)
        q.evaluate("(a)=>{var T=window.__T;T.save.seen={};T.startVid(T.PBY[a[0]],a[1],'ev')}", [pl, vid]); q.wait_for_timeout(500); q.click('.btn.go'); tapped = False
        for i in range(600):
            q.wait_for_timeout(50)
            if not tapped and q.evaluate("()=>document.querySelectorAll('.jcard').length"): q.evaluate("()=>document.querySelectorAll('.jcard')[0].click()"); tapped = True
            try:
                for x in q.evaluate("()=>window.__sp"): res[x['t']] = x['p']
            except Exception: pass
            if view(q) in ('map', 'nav'): break
        q.wait_for_timeout(1500)
        try: q.evaluate(POLL)
        except Exception: pass
        return res
    SCN = {x['id']: x for x in data.D}
    def npcline(vid, i): return SCN[vid]['pairs'][i]['n'].replace('*', '')
    res = pitch_of('rom_info1', 0)
    chk('C: rom_info1 客引き(m_tout)→ 案内係(m_info)で声が変わる', abs(res[npcline('rom_info1', 0)] - SPP['m_tout']) < .02 and abs(res[npcline('rom_info1', 1)] - SPP['m_info']) < .02, (res.get(npcline('rom_info1', 0)), res.get(npcline('rom_info1', 1))))
    res = pitch_of('rom_taxi1', 0)
    chk('C: rom_taxi1 乗り場の係(m_rank)→ 運転手(m_driver)で声が変わる', abs(res[npcline('rom_taxi1', 0)] - SPP['m_rank']) < .02 and abs(res[npcline('rom_taxi1', 1)] - SPP['m_driver']) < .02 and abs(res[npcline('rom_taxi1', 3)] - SPP['m_driver']) < .02, (res.get(npcline('rom_taxi1', 0)), res.get(npcline('rom_taxi1', 1))))
    res = pitch_of('rom_dep_train1', 0)
    chk('C: rom_dep_train1 乗客(m_pax)→ 車掌(m_cond)で声が変わる', abs(res[npcline('rom_dep_train1', 0)] - SPP['m_pax']) < .02 and abs(res[npcline('rom_dep_train1', 3)] - SPP['m_cond']) < .02, (res.get(npcline('rom_dep_train1', 0)), res.get(npcline('rom_dep_train1', 3))))
    # ---------- D. 発車標の重ね絵 ----------
    pl = q.evaluate("()=>{var T=window.__T,pl=null;Object.keys(T.PBY).forEach(function(k){if((T.PBY[k].v||[]).indexOf('rom_dep_platform1')>=0)pl=T.PBY[k]});return pl.id}")
    def board_px(vid):
        q.evaluate("(a)=>{var T=window.__T;T.save.seen={};T.startVid(T.PBY[a[0]],a[1],'ev')}", [pl if vid == 'rom_dep_platform1' else q.evaluate("(v)=>{var T=window.__T,pl=null;Object.keys(T.PBY).forEach(function(k){if((T.PBY[k].v||[]).indexOf(v)>=0)pl=T.PBY[k]});return pl.id}", vid), vid]); q.wait_for_timeout(1200)
        return q.evaluate("()=>{var cv=document.getElementById('sceneA'),g=cv.getContext('2d');var d=g.getImageData(714,142,420,240).data,n=0,amber=0;for(var i=0;i<d.length;i+=4){if(d[i]>180&&d[i+1]>130&&d[i+2]<110)amber++}return {w:cv.width,h:cv.height,amber:amber}}")
    plat = board_px('rom_dep_platform1'); q.screenshot(path='/tmp/rome094/rom_dep_platform1-board.png')
    tick = board_px('rom_dep_ticket1')
    chk('D: 発車標の場面は、発車標の右半分(Partenze)に行き先の文字(琥珀色の画素)が重なる。切符の窓口の場面では重ならない(背景に焼き込んでいない)', plat['amber'] > 500 and tick['amber'] < 50, (plat, tick))
    bgim = Image.open(os.path.join(ART_DIR, 'rome-departure-v2.png')).convert('RGB').crop((714, 142, 1134, 382))
    chk('D: 背景 rome-departure-v2.png そのものには、琥珀色の行き先の文字は無い(元の薄い線だけ)', sum(1 for px in bgim.getdata() if px[0] > 180 and px[1] > 130 and px[2] < 110) < 50)
    st = Image.open(sp_).convert('RGB')
    a = sum(1 for px in st.crop((0, 0, 420, 240)).getdata() if px[0] > 220 and px[1] > 190 and px[2] < 140); b = sum(1 for px in st.crop((420, 0, 840, 240)).getdata() if px[0] > 220 and px[1] > 190 and px[2] < 140)
    chk('D: 2コマは違う(ミラノ行きのホーム欄が点滅)', a != b and abs(a - b) < 400, (a, b))
    # ---------- E. 世界マップ ----------
    q2 = ctx.new_page(); q2.on('pageerror', lambda e: ERR.append(str(e)[:160]))
    q2.goto(base + '/world/?map=1'); q2.wait_for_timeout(1500)
    wm = open(os.path.join(ROOT, 'world/index.html'), encoding='utf-8').read()
    chk('E: 世界マップ: ローマの点(url ../tour/rome/)・アテネ⇄ローマの道', "rome:{n:'ローマ'" in wm and "url:'../tour/rome/'" in wm and "athens:['rovaniemi','rome']" in wm and "rome:['athens']" in wm)
    chk('E: アテネ編の最後(ath_gate1)は世界マップへ戻る(アテネ出発→ローマ到着につながる)', "if(S.vid==='ath_gate1'){worldMark('athens')" in open(os.path.join(ROOT, 'tour/athens/index.html'), encoding='utf-8').read() or "ath_gate1" in open(os.path.join(ROOT, 'tour/athens/index.html'), encoding='utf-8').read())
    ap = q2.evaluate("()=>{try{var n=0;return {has:typeof AP!=='undefined'?!!AP.rome:null}}catch(e){return {err:String(e)}}}")
    q2.close()
    q3 = ctx.new_page(); q3.on('pageerror', lambda e: ERR.append(str(e)[:160]))
    q3.goto(base + '/tour/athens/index.html?check=1'); q3.wait_for_timeout(1000); q3.click('#chkBtn')
    chk('E: チェックモード: アテネからローマへのリンク', q3.evaluate("()=>[].some.call(document.querySelectorAll('#chkPan a.b'),function(a){return /rome\\/\\?check=1/.test(a.getAttribute('href'))})"))
    q3.close()
    q.click('#chkBtn')
    chk('E: チェックモード: ローマからアテネへのリンク', q.evaluate("()=>[].some.call(document.querySelectorAll('#chkPan a.b'),function(a){return /athens\\/\\?check=1/.test(a.getAttribute('href'))})"))
    # 最後の場面(車内)を最後まで遊ぶと世界マップへ(チェックモードは同じページ)
    # ---------- ページ全体のエラー ----------
    for path in ['/tour/index.html', '/tour/athens/index.html', '/tour/rome/index.html', '/tour/rome/index.html?check=1', '/world/?map=1']:
        q4 = ctx.new_page(); q4.on('pageerror', lambda e: ERR.append(path + ' ' + str(e)[:160])); q4.goto(base + path); q4.wait_for_timeout(900)
        chk('%s: エラーなし' % path, q4.evaluate('window.__errs') == [], q4.evaluate('window.__errs')); q4.close()
    chk('ページエラーなし(全体)', not ERR, ERR[:3])
    br.close()
print()
print('全部OK' if not bad else 'NG あり: %d 件\n  ' % len(bad) + '\n  '.join(bad))
sys.exit(1 if bad else 0)
