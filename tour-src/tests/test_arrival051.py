# -*- coding: utf-8 -*-
"""タスク051 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_arrival051.py
(1)SIM(nbo_sim1/2): 背景が nairobi-sim-v1.png(画素が素材と一致)・art id simshop・既存の会話が進む
(2)回転台: 4コマが 1コマ0.5秒で切り替わる(キャンバスの画素が strip のコマと一致)・左上(1204,596)=足もと中心(1264,896)。OPEN看板: 2コマが1秒ごと・(704,524)から128×48
(3)タクシー(nbo_taxi1/2): 背景が nairobi-taxi-v1.png・既存の会話が進む・fx は無し
(4)旅行者: SIM2人・タクシー2人。相手・ふたり・回転台と重ならない・絵が描かれている
(5)ホテルの部屋 hroom: 到着タブの hsong の次・v 空(場面の数・完了条件・save.seen に入らない)・タクシーのあとに開く
(6)nbo_room: 背景 nairobi-hotel-room-v1.png・後ろ姿のふたり(足もと y=884、ルル x=700・キング x=836)・人なし・発音課題/マイク/採点なし・6つの台詞が読み上げ+表示で進む・マップへ戻る
(7)TV画面の矩形(x1120-1464 / y216-392)が art 設定にあり、画面には何も映っていない
(8)絵が読めないときは今までのドット描画に落ちる(真っ暗にならない)
(9)ドーハ側の art 設定の入口(artIdFor)・049/050 の場面は変わらない  (10)画面に「勉強・テスト・測定・練習」の言葉がない
マイク・実機の見え方・実機の音は確認できない。"""
import os, sys, io, json, base64, threading, http.server, socketserver
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART = os.path.join(ROOT, 'tour/assets/art')
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,PBY:PBY,PLACES_NARR:PLACES_NARR,setMode:setMode,showMap:showMap,enterPlace:enterPlace,startVid:startVid,"
        "ART:ART,TRIP:TRIP,artIdFor:artIdFor,ARTFAIL:ARTFAIL,TOTALV:function(){return TOTALV},gt:function(){return t}};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "window.__say=[];try{speechSynthesis.speak=function(u){window.__say.push(u.text);setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));")
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
def newpage(br, init=INIT):
    ctx = br.new_context(viewport={'width': 430, 'height': 900}, device_scale_factor=1)
    pg = ctx.new_page(); pg.add_init_script(init); pg.route('**/tour/index.html', hooked); return pg
def boot(br, init=INIT):
    pg = newpage(br, init); pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1200); pg.mouse.click(215, 450); pg.wait_for_timeout(800); return pg
def snap(p):
    d = p.evaluate("()=>document.getElementById('sceneA').toDataURL('image/png')")
    return np.array(Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB')).astype(int)
def img(n): return Image.open(os.path.join(ART, n)).convert('RGBA')
def rgb(n): return np.array(img(n).convert('RGB')).astype(int)
def play(p, pl, vid): p.evaluate("(a)=>{var T=window.__T;T.startVid(T.PBY[a[0]],a[1],'ev')}", [pl, vid])
def frac_same(a, b): return float((a == b).all(axis=2).mean())
# 区画の画素のしるし(ページ内と同じ式)
SUMJS = ("(function(x,y,w,h){var d=document.getElementById('sceneA').getContext('2d').getImageData(x,y,w,h).data,s=0;"
         "for(var p=0;p<w*h;p++){s+=(d[4*p]*3+d[4*p+1]*5+d[4*p+2]*7)*((p%97)+1)}return s})")
def csum(arr):
    h, w = arr.shape[:2]; f = arr.reshape(-1, 3); p = np.arange(w * h)
    return int(((f[:, 0] * 3 + f[:, 1] * 5 + f[:, 2] * 7) * ((p % 97) + 1)).sum())
def composite(bg, strip, fi, fw, fh, x, y):
    out = bg.copy(); fr = strip.crop((fi * fw, 0, fi * fw + fw, fh)); base_ = Image.fromarray(bg.astype('uint8')).convert('RGBA'); base_.alpha_composite(fr, (x, y))
    return np.array(base_.convert('RGB')).astype(int)
FORBID = ['勉強', 'テスト', '測定', '練習', '復習', '採点']
with sync_playwright() as pw:
    br = pw.chromium.launch()
    # ---------------- 素材 ----------------
    for f, sz in [('nairobi-sim-v1.png', (1536, 960)), ('nairobi-taxi-v1.png', (1536, 960)), ('nairobi-hotel-room-v1.png', (1536, 960)), ('nairobi-sim-spinner-strip.png', (480, 300)), ('nairobi-sim-blink-strip.png', (256, 48))]:
        chk('素材 %s が %s で置かれている' % (f, sz), img(f).size == sz, img(f).size)
    # ---------------- (1)(2) SIM ----------------
    pg = boot(br); play(pg, 'sim', 'nbo_sim1'); pg.wait_for_timeout(8500)
    cf = pg.evaluate("(function(){var T=__T;var c=T.ART.simshop;return {id:T.artIdFor(T.G.scene),bg:c.bg,strips:c.strips,people:c.people,npc:c.npc,npcS:c.npcS,base:c.base,lulu:c.lulu,king:c.king,suit:c.suit,vid:T.G.scene.vid,fail:T.ARTFAIL.simshop||0}})()")
    chk('nbo_sim1: art id simshop・背景 nairobi-sim-v1.png', cf['id'] == 'simshop' and cf['bg'] == 'nairobi-sim-v1.png' and not cf['fail'], cf['id'])
    bgS = rgb('nairobi-sim-v1.png'); sn = snap(pg)
    chk('SIMの背景の画素が素材と一致(上の天井・看板の帯。人も動きもない領域)', frac_same(sn[0:120, :], bgS[0:120, :]) > .999, frac_same(sn[0:120, :], bgS[0:120, :]))
    chk('相手(店員)の絵が中央のカウンターの向こうにある(npc 方式。x=768・カウンターの高さ y=500 で切る)', cf['npc']['x'] == 768 and cf['npc']['clip'] == 500 and cf['npcS'] == {'sim_staff': 'w-front-man-suit-1', 'sim_staff2': 'w-front-man-dashiki'}, cf['npc'])
    sx0, sx1 = 768 - 28, 768 + 28
    chk('店員が描かれている(その矩形の画素が背景と変わっている)', frac_same(sn[372:500, sx0:sx1], bgS[372:500, sx0:sx1]) < .9)
    chk('2人と荷物の立つ足もとは y=900・カウンターの手前(ルル700・キング860・荷物965)', (cf['base'], cf['lulu'], cf['king'], cf['suit']) == (900, 700, 860, 965))
    # 回転台・OPEN の位置と数値
    st = {s['img']: s for s in cf['strips']}
    sp, bl = st['nairobi-sim-spinner-strip.png'], st['nairobi-sim-blink-strip.png']
    chk('回転台: 左上(1204,596)・4コマ・1コマ 120×300・0.5秒ごと', (sp['x'], sp['y'], sp['n'], sp['fw'], sp['fh'], sp['step']) == (1204, 596, 4, 120, 300, .5), sp)
    chk('OPEN看板: (704,524)・2コマ・128×48・1秒ごと', (bl['x'], bl['y'], bl['n'], bl['fw'], bl['fh'], bl['step']) == (704, 524, 2, 128, 48, 1), bl)
    spS = img('nairobi-sim-spinner-strip.png'); al = np.array(spS.crop((0, 0, 120, 300)))[:, :, 3]
    ys = np.where(al.max(axis=1) > 0)[0]; bot = ys.max(); xs = np.where(al[bot] > 0)[0]
    chk('回転台の足もと中心が (1264,896)(コマの最下段の中心 x=1204+60、下端 y=596+300)', 1204 + 60 == 1264 and 596 + 300 == 896 and bot >= 295, (bot, 1204 + int((xs.min() + xs.max()) / 2)))
    # アニメ: キャンバスの画素が strip のコマと一致(位置の確認)・切り替わり
    exp_sp = [csum(composite(bgS, spS, k, 120, 300, 1204, 596)[596:896, 1204:1324]) for k in range(4)]
    blS = img('nairobi-sim-blink-strip.png'); exp_bl = [csum(composite(bgS, blS, k, 128, 48, 704, 524)[524:572, 704:832]) for k in range(2)]
    seen_sp, seen_bl, order_sp, order_bl = set(), set(), [], []
    for i in range(34):
        a = pg.evaluate(SUMJS + "(1204,596,120,300)"); b = pg.evaluate(SUMJS + "(704,524,128,48)")
        ka = exp_sp.index(a) if a in exp_sp else -1; kb = exp_bl.index(b) if b in exp_bl else -1
        seen_sp.add(ka); seen_bl.add(kb); order_sp.append(ka); order_bl.append(kb); pg.wait_for_timeout(100)
    chk('回転台の4コマがすべて、位置(1204,596)の画素どおりに出る(NEARESTの粒のまま)', seen_sp == {0, 1, 2, 3}, order_sp)
    chk('OPEN看板の2コマ(点灯/消灯)が、位置(704,524)の画素どおりに出る', seen_bl == {0, 1}, order_bl)
    ch = [i for i in range(1, len(order_sp)) if order_sp[i] != order_sp[i - 1]]
    chk('回転台は 順に切り替わる(0→1→2→3→0)', all((order_sp[i] - order_sp[i - 1]) % 4 == 1 for i in ch if order_sp[i] >= 0 and order_sp[i - 1] >= 0), order_sp)
    chk('切り替えの間隔: 回転台 約0.5秒(100ms間隔の観測で4〜6回に1回)・OPEN 約1秒', 3 <= (len(order_sp) / max(1, len(ch))) <= 7 and 5 <= (len(order_bl) / max(1, len([i for i in range(1, len(order_bl)) if order_bl[i] != order_bl[i - 1]]))) <= 14, [len(ch)])
    # 旅行者(SIM)
    pe = cf['people']
    chk('SIMの旅行者は2人(t-safari-front・t-woman-hijab-front)', [q['n'] for q in pe] == ['t-safari-front', 't-woman-hijab-front'], pe)
    def box(q):
        w, h = Image.open(os.path.join(ART, 'npc', q['n'] + '.png')).size; return (q['x'] - w // 2, q['by'] - h, q['x'] + w - w // 2, q['by'])
    def hit(a, b): return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])
    others = {'店員': (768 - 41, 372, 768 + 41, 500), 'ルル': (700 - 40, 900 - 124, 700 + 40, 900), 'キング': (860 - 40, 900 - 124, 860 + 40, 900), '荷物': (965 - 30, 900 - 110, 965 + 30, 900), '回転台': (1204, 596, 1324, 896)}
    for q in pe:
        for nm, ob in others.items(): chk('SIM旅行者 %s は %s と重ならない' % (q['n'], nm), not hit(box(q), ob), (box(q), ob))
        b = box(q); chk('SIM旅行者 %s が描かれている' % q['n'], frac_same(sn[b[1]:b[3], b[0]:b[2]], bgS[b[1]:b[3], b[0]:b[2]]) < .85)
    chk('SIMの旅行者は左右の他キャリア(Telkom/airtel)の前の端(x<400 と x>1350)', pe[0]['x'] < 400 and pe[1]['x'] > 1350, [q['x'] for q in pe])
    txt = pg.evaluate("document.body.innerText"); chk('SIM: 画面に「勉強・テスト・測定・練習」の言葉がない', not any(w in txt for w in FORBID))
    chk('SIM: エラーなし', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    # 既存の会話が進む(1往復: 相手→カンペ)
    pg.evaluate("document.querySelector('button.btn.go').click()"); pg.wait_for_timeout(4500)
    ph = pg.evaluate("[__T.G.scene.vid,__T.G.phase,!!document.querySelector('.cue')]")
    chk('nbo_sim1 の会話は今までどおり進む(相手の台詞のあとカンペが出る)', ph[0] == 'nbo_sim1' and ph[2] is True, ph)
    n_sim1 = pg.evaluate("__T.G.scene.d.lines.length"); lines1 = pg.evaluate("__T.G.scene.d.lines[0].en||__T.G.scene.d.lines[0][0]||JSON.stringify(__T.G.scene.d.lines[0]).slice(0,80)")
    chk('nbo_sim1 の台詞の数は変わらない(5往復=10行)', n_sim1 == 10, n_sim1)
    pg.context.close()
    pg = boot(br); play(pg, 'sim', 'nbo_sim2'); pg.wait_for_timeout(8500)
    c2 = pg.evaluate("[__T.artIdFor(__T.G.scene),__T.G.scene.vid,__T.G.scene.d.bg]"); s2 = snap(pg)
    chk('nbo_sim2 も art id simshop・背景は新しい絵', c2 == ['simshop', 'nbo_sim2', 'sim'] and frac_same(s2[0:120, :], bgS[0:120, :]) > .999, c2)
    chk('nbo_sim2: 店員(sim_staff2=ダシキの人)が描かれている', frac_same(s2[372:500, 768 - 28:768 + 28], bgS[372:500, 768 - 28:768 + 28]) < .9)
    chk('nbo_sim2: エラーなし', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs')); pg.context.close()
    # ---------------- (3)(4) タクシー ----------------
    bgT = rgb('nairobi-taxi-v1.png')
    pg = boot(br); play(pg, 'taxi', 'nbo_taxi1'); pg.wait_for_timeout(8500)
    ct = pg.evaluate("(function(){var T=__T,c=T.ART.nairobi;return {id:T.artIdFor(T.G.scene),bg:c.bg,fx:c.fx,people:c.people,npcS:c.npcS,base:c.base,lulu:c.lulu,king:c.king,suit:c.suit,npc:c.npc}})()"); sn = snap(pg)
    chk('nbo_taxi1: art id nairobi・背景 nairobi-taxi-v1.png', ct['id'] == 'nairobi' and ct['bg'] == 'nairobi-taxi-v1.png', ct['id'])
    chk('タクシーの背景の画素が素材と一致(空・ガラスの壁。人のいない領域)', frac_same(sn[0:700, :], bgT[0:700, :]) > .999, frac_same(sn[0:700, :], bgT[0:700, :]))
    chk('fx は無し(朝の屋外の絵なので、夜の星・ガラスのきらめきは出さない)', ct['fx'] == '', ct['fx'])
    chk('npcS の対応は維持(taxi_staff→ダシキ、driver→スーツ)', ct['npcS'] == {'taxi_staff': 'w-front-man-dashiki', 'driver': 'w-front-man-suit-1'}, ct['npcS'])
    pe = ct['people']; chk('タクシーの旅行者は2人(t-backpacker-front・t-man-thobe-front)', [q['n'] for q in pe] == ['t-backpacker-front', 't-man-thobe-front'], pe)
    others = {'係員': (1060 - 45, 926 - 136, 1060 + 45, 926), 'ルル': (300 - 40, 926 - 124, 300 + 40, 926), 'キング': (470 - 40, 926 - 124, 470 + 40, 926), '荷物': (575 - 30, 926 - 110, 575 + 30, 926)}
    for q in pe:
        for nm, ob in others.items(): chk('タクシー旅行者 %s は %s と重ならない' % (q['n'], nm), not hit(box(q), ob))
        b = box(q); chk('タクシー旅行者 %s が描かれている' % q['n'], frac_same(sn[b[1]:b[3], b[0]:b[2]], bgT[b[1]:b[3], b[0]:b[2]]) < .85)
        chk('タクシー旅行者 %s は歩道の上(足もと y≥775)で、右の端寄り(x>1200)' % q['n'], q['by'] >= 775 and q['x'] > 1200)
    pg.evaluate("document.querySelector('button.btn.go').click()"); pg.wait_for_timeout(4500)
    ph = pg.evaluate("[__T.G.scene.vid,__T.G.phase,!!document.querySelector('.cue'),__T.G.scene.d.lines.length]")
    chk('nbo_taxi1 の会話は今までどおり進む(カンペが出る・10行)', ph[0] == 'nbo_taxi1' and ph[2] is True and ph[3] == 10, ph)
    txt = pg.evaluate("document.body.innerText"); chk('タクシー: 画面に「勉強・テスト・測定・練習」の言葉がない', not any(w in txt for w in FORBID))
    chk('タクシー: エラーなし', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs')); pg.context.close()
    pg = boot(br); play(pg, 'taxi', 'nbo_taxi2'); pg.wait_for_timeout(8500); c2 = pg.evaluate("[__T.artIdFor(__T.G.scene),__T.G.scene.vid]"); s2 = snap(pg)
    chk('nbo_taxi2 も art id nairobi・背景は新しい絵', c2 == ['nairobi', 'nbo_taxi2'] and frac_same(s2[0:700, :], bgT[0:700, :]) > .999, c2)
    chk('nbo_taxi2: エラーなし', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs')); pg.context.close()
    # ---------------- (5) ホテルの部屋(場所) ----------------
    pg = boot(br)
    ids = pg.evaluate("__T.PLACES_NARR.map(function(p){return p.id})")
    chk('到着タブは immig,bag,sim,taxi,hsong,hroom の順(ホテルの部屋が hsong の次)', ids == ['immig', 'bag', 'sim', 'taxi', 'hsong', 'hroom'], ids)
    pl = pg.evaluate("(function(){var p=__T.PBY.hroom;return [p.v.length,p.rest,p.name,p.tip,p.x,p.y,p.ico,p.snd]})()")
    chk('hroom: v は空・rest=nbo_room・名前「ホテルの部屋」・実名のホテル・座標(48,88)', pl[0] == 0 and pl[1] == 'nbo_room' and pl[2] == 'ホテルの部屋' and pl[3] == ['Villa Rosa Kempinski', '部屋で休む'] and (pl[4], pl[5]) == (48, 88), pl)
    pg.evaluate("(function(){var T=__T;T.save.ticket='ow';T.setMode('arr');T.showMap()})()"); pg.wait_for_timeout(400)
    lk = lambda i: pg.evaluate("document.querySelector('.node[data-id=%s]').classList.contains('lock')" % i)
    chk('入国審査〜タクシーを遊ぶ前は、ホテルの部屋に鍵がかかっている', lk('hroom') is True)
    pg.evaluate("(function(){var T=__T;['nbo_immig1','nbo_bag1','nbo_sim1'].forEach(function(v){T.save.seen[v]=1});T.showMap()})()"); pg.wait_for_timeout(300)
    chk('タクシーの前(SIMまで)では、ホテルの部屋はまだ閉じている', lk('hroom') is True and lk('hsong') is True)
    tv0 = pg.evaluate("__T.TOTALV()")
    pg.evaluate("(function(){var T=__T;T.save.seen['nbo_taxi1']=1;T.showMap()})()"); pg.wait_for_timeout(400)
    chk('タクシーまで遊ぶと、ホテルのロビーとホテルの部屋が開く(hsong の次=タクシーのあと)', lk('hsong') is False and lk('hroom') is False)
    chk('場面の数(TOTALV)は変わらない(ホテルの部屋は数に入らない)', pg.evaluate("__T.TOTALV()") == tv0 == 8, tv0)
    chk('ホテルの部屋に「済」の印は出ない・場所の点(dots)もない', pg.evaluate("(function(){var n=document.querySelector('.node[data-id=hroom]');return !n.classList.contains('done')&&n.querySelectorAll('i').length===0})()"))
    gp = pg.evaluate("(function(){var Tp=__T.TRIP;return [JSON.stringify(Tp.GROUPS.nbo_arr),Tp.PLACEGRP.hroom===undefined]})()")
    chk('到着の完了条件(GROUPS nbo_arr)は4場所のまま・PLACEGRP に hroom は入っていない', gp == [json.dumps([['nbo_immig1', 'nbo_immig2'], ['nbo_bag1', 'nbo_bag2'], ['nbo_sim1', 'nbo_sim2'], ['nbo_taxi1', 'nbo_taxi2']], separators=(',', ':')), True], gp)
    # 地図の座標が重ならない(ノード同士の矩形)
    rs = pg.evaluate("(function(){var o={};['immig','bag','sim','taxi','hsong','hroom'].forEach(function(i){var r=document.querySelector('.node[data-id='+i+']').getBoundingClientRect();o[i]=[r.left,r.top,r.right,r.bottom]});return o})()")
    ov = [(a, b) for a in rs for b in rs if a < b and hit(rs[a], rs[b])]
    chk('地図のノードどうしが重ならない(hroom は (48,88) のまま)', ov == [], ov)
    seen0 = pg.evaluate("JSON.stringify(__T.save.seen)")
    # ---------------- (6)(7) nbo_room ----------------
    pg.click('.node[data-id=hroom]'); pg.wait_for_timeout(1800)
    sc = pg.evaluate("[__T.G.view,__T.G.phase,__T.G.scene.d.id,!!document.querySelector('.cue'),__T.G.scene.turns.length,__T.artIdFor(__T.G.scene)]")
    chk('部屋の場面に入る(nbo_room・art id nroom・カンペ/会話の型ではない)', sc[0] == 'scene' and sc[2] == 'nbo_room' and sc[3] is False and sc[4] == 0 and sc[5] == 'nroom', sc)
    bgR = rgb('nairobi-hotel-room-v1.png'); sn = snap(pg)
    chk('部屋の背景の画素が素材と一致(上半分・TVも含む。人のいない領域)', frac_same(sn[0:760, :], bgR[0:760, :]) > .9995, frac_same(sn[0:760, :], bgR[0:760, :]))
    tv = pg.evaluate("__T.ART.nroom.tv")
    chk('art 設定に TV画面の矩形 tv:{x:1120,y:216,w:344,h:176}(= x1120-1464 / y216-392)が記録されている', tv == {'x': 1120, 'y': 216, 'w': 344, 'h': 176}, tv)
    chk('TVには何も映っていない(その矩形の画素が背景のまま)', frac_same(sn[216:392, 1120:1464], bgR[216:392, 1120:1464]) == 1.0)
    hl = pg.evaluate("(function(){var h=__T.ART.nroom.hall;return [h.lulu.n,h.lulu.x,h.lulu.by,h.king.n,h.king.x,h.king.by,!!h.sage,(__T.ART.nroom.people||[]).length]})()")
    chk('ふたりは後ろ姿(hall-lulu-back/hall-king-back)・足もと y=884・ルル x=700・キング x=836・人は置かない', hl == ['hall-lulu-back', 700, 884, 'hall-king-back', 836, 884, False, 0], hl)
    for nm, n, x in [('ルル', 'hall-lulu-back', 700), ('キング', 'hall-king-back', 836)]:
        w, h = Image.open(os.path.join(ART, 'npc', n + '.png')).size; b = (x - w // 2, 884 - h, x - w // 2 + w, 884)
        chk('%s が描かれている(足もと y=884)' % nm, frac_same(sn[b[1]:b[3], b[0]:b[2]], bgR[b[1]:b[3], b[0]:b[2]]) < .85)
    txt = pg.evaluate("document.body.innerText"); chk('部屋の入り: 画面に「勉強・テスト・測定・練習」の言葉がない', not any(w in txt for w in FORBID))
    chk('部屋の入り: マイク・カンペ・単語バトルの画面は出ない', pg.evaluate("[!!document.querySelector('.cue'),__T.G.phase]") == [False, 'listen'])
    pg.click('button.btn.go'); pg.wait_for_timeout(300)
    LINES = ['We made it. This is our room at the Villa Rosa Kempinski.', 'It is so quiet. Look at the moon.', 'Nairobi is beautiful at night.', 'My blue suitcase is here. I am so tired.', 'Rest well, King. Tomorrow is a new day.', 'Lala salama, Lulu.']
    def waitmsg(k, ms=6000):
        try: pg.wait_for_function("(function(){var m=document.querySelector('#msg');return m&&m.innerText.indexOf(%s)>=0})()" % json.dumps(k), timeout=ms); return True
        except Exception: return False
    for i, k in enumerate(LINES):
        chk('台詞(%d)が表示される(英語・読み上げ): %s' % (i + 1, k), waitmsg(k))
        if i == 1:
            chk('会話中も マイク・カンペ・採点の画面は出ない', pg.evaluate("[!!document.querySelector('.cue'),__T.G.phase,!!document.querySelector('.mic')]") == [False, 'listen', False])
            tx = pg.evaluate("document.body.innerText"); chk('会話中: 画面に「勉強・テスト・測定・練習」の言葉がない', not any(w in tx for w in FORBID))
    try: pg.wait_for_function("__T.G.view==='map'", timeout=8000)
    except Exception: pass
    chk('やりとりが終わるとマップに戻る', pg.evaluate("__T.G.view") == 'map')
    say = [x for x in pg.evaluate("window.__say") if x in LINES]; chk('6つの台詞がすべて読み上げられた', say == LINES, say)
    chk('部屋の場面は保存の記録(save.seen)を変えない', pg.evaluate("JSON.stringify(__T.save.seen)") == seen0)
    chk('発音の保存(kanpe-pron-v1)を作っていない', pg.evaluate("localStorage.getItem('kanpe-pron-v1')") is None)
    chk('エラーなし(部屋)', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs')); pg.context.close()
    # ---------------- (8) 絵が読めないとき: 今までのドット描画に落ちる ----------------
    for what, f, pl_, vid in [('SIM', 'nairobi-sim-v1.png', 'sim', 'nbo_sim1'), ('タクシー', 'nairobi-taxi-v1.png', 'taxi', 'nbo_taxi1'), ('部屋', 'nairobi-hotel-room-v1.png', 'hroom', None)]:
        ctx = br.new_context(viewport={'width': 430, 'height': 900}); pg = ctx.new_page(); pg.add_init_script(INIT); pg.route('**/tour/index.html', hooked)
        pg.route('**/' + f, lambda r: r.abort()); pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1200); pg.mouse.click(215, 450); pg.wait_for_timeout(800)
        if vid: play(pg, pl_, vid)
        else: pg.evaluate("(function(){var T=__T;T.enterPlace('hroom')})()")
        pg.wait_for_timeout(2500)
        r = pg.evaluate("(function(){var c=document.getElementById('scene'),g=c.getContext('2d').getImageData(0,0,c.width,c.height).data,s={},n=0;for(var i=0;i<g.length;i+=4*37){s[g[i]+','+g[i+1]+','+g[i+2]]=1}return [document.getElementById('sceneA').hidden,c.hidden,Object.keys(s).length]})()")
        chk('%s: 背景の絵が読めないとき、いつものドット描画に落ちる(絵のキャンバスは隠れ、色の数が多い=真っ暗ではない)' % what, r[0] is True and r[1] is False and r[2] > 6, r)
        chk('%s: 絵が読めなくてもエラーなし' % what, pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs')); ctx.close()
    # 動きの絵(strip)だけ読めないときは、動きだけ出さず背景と人は出る
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); pg = ctx.new_page(); pg.add_init_script(INIT); pg.route('**/tour/index.html', hooked)
    pg.route('**/nairobi-sim-spinner-strip.png', lambda r: r.abort()); pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1200); pg.mouse.click(215, 450); pg.wait_for_timeout(800)
    play(pg, 'sim', 'nbo_sim1'); pg.wait_for_timeout(2500); sn = snap(pg)
    chk('回転台の絵だけ読めないとき: 場面は出て(背景は新しい絵)、回転台の位置は背景のまま', frac_same(sn[0:120], bgS[0:120]) > .999 and frac_same(sn[596:896, 1204:1324], bgS[596:896, 1204:1324]) > .99 and pg.evaluate("document.getElementById('sceneA').hidden") is False)
    ctx.close()
    # ---------------- (9) ドーハ側・049/050 は変わらない ----------------
    dh = open(os.path.join(ROOT, 'tour/doha/index.html'), encoding='utf-8').read()
    chk("ドーハ側の artIdFor は ホテルのフロント(doh_city_h1)・070 のコルニーシュ4場面(dcorn)・064 の入国審査(dimmig)だけ。SIMの店などナイロビの絵は入らない", "if(/^doh_/.test(v)&&g==='dimmig')return v==='doh_immig2'?'dimmig2':'dimmig';return v==='doh_city_h1'?'hotel':(v==='doh_city_c1'||v==='doh_city_c2'||v==='doh_city_c3'||v==='doh_ev_j_ask')?'dcorn':null}" in dh and 'simshop' not in dh.split("function artIdFor(S){")[1][:420])
    th = open(os.path.join(ROOT, 'tour/index.html'), encoding='utf-8').read()
    chk("ナイロビ側の artIdFor に sim→simshop・nroom→nroom が足された(nlobby・taxi などは残る)", "g==='nroom'?'nroom':g==='sim'?'simshop'" in th and "g==='nlobby'?'nlobby'" in th and "(g==='taxi'?'nairobi'" in th)
    chk('049 の歌手の場面データ(SONGSC)・チャントは変わらない(nbo_song・nlobby が残る)', "'id': 'nbo_song'" in open(os.path.join(ROOT, 'tour-src/song_data.py'), encoding='utf-8').read().replace('"', "'") and 'nlobby:{bg:' in th)
    br.close()
print('\n失敗:', bad if bad else 'なし'); sys.exit(1 if bad else 0)
