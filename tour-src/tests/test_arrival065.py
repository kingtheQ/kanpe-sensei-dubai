# -*- coding: utf-8 -*-
"""タスク065 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_arrival065.py
(1)素材: 到着ロビー背景 1536×960・オーロラ strip 5504×172(4コマ×1376×172)
(2)台本: 5場所×2場面=10本・各5往復・分かれ目(2つ)・日本語訳は空・語は5つ・fork の語が語リストにある・実在情報は確認済みのものだけ(Wi-Fi名・バス8番/Airport Express・北極圏ライン・Welcome to Rovaniemi Airport)・値段/時刻/所要時間/店名が台詞にない
(3)到着ロビー: art id rvnlobby・背景の画素が素材と一致(上部)・オーロラ strip が (80,128) に4コマ 1.2秒ごと・画素が composite と一致・ふたりは後ろ姿で足もと y=884(ルル700・キング836)・話し相手が右に立つ
(4)ほかの4場所はコード描画(art id なし・エラーなし・画面に出る)
(5)旅の骨組み: IMPL に RVN・oneworld/Star とも10日目に rvn_arr・場所の鍵(上から順)・世界マップの chain(ドーハ→ロヴァニエミ。ヘルシンキは乗り継ぎ)・「かいわ n / 10」
(6)世界マップに ロヴァニエミ(url ../tour/rovaniemi/)・ドーハの隣
(7)画面に「勉強・テスト・測定・練習・復習・採点」の言葉がない
マイク・実機の見え方・実機の音は確認できない。"""
import os, sys, io, re, json, base64, threading, http.server, socketserver
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART = os.path.join(ROOT, 'tour/assets/art')
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
def img(n): return Image.open(os.path.join(ART, n)).convert('RGBA')
def rgb(n): return np.array(img(n).convert('RGB')).astype(int)
def frac_same(a, b): return float((a == b).all(axis=2).mean())

# ---------------- (1) 素材 ----------------
chk('素材 rovaniemi-arrivals-v1.png が 1536×960', img('rovaniemi-arrivals-v1.png').size == (1536, 960), img('rovaniemi-arrivals-v1.png').size)
chk('素材 rovaniemi-aurora-strip.png が 5504×172(4コマ×1376×172)', img('rovaniemi-aurora-strip.png').size == (5504, 172), img('rovaniemi-aurora-strip.png').size)

# ---------------- (2) 台本 ----------------
import data
ARR_IDS = ['rvn_immig1', 'rvn_immig2', 'rvn_bag1', 'rvn_bag2', 'rvn_lobby1', 'rvn_lobby2', 'rvn_wifi1', 'rvn_wifi2', 'rvn_bus1', 'rvn_bus2']
SC = [x for x in data.D if x['id'] in ARR_IDS]   # 072 で滞在・夜・出発の20本が増えたので、到着の10本だけを対象にする(滞在・夜・出発は test_rovaniemi072.py)
ids = [x['id'] for x in SC]
chk('場面は10本(5場所×2)', ids == ['rvn_immig1', 'rvn_immig2', 'rvn_bag1', 'rvn_bag2', 'rvn_lobby1', 'rvn_lobby2', 'rvn_wifi1', 'rvn_wifi2', 'rvn_bus1', 'rvn_bus2'], ids)
alltext = []
for x in SC:
    ps = x['pairs']
    chk('%s: 5往復' % x['id'], len(ps) == 5, len(ps))
    forks = [p for p in ps if isinstance(p, dict)]
    chk('%s: 分かれ目が2つ(3択・聞き取れた返事と聞き違えた返事がある)' % x['id'], len(forks) == 2 and all(len(p['opts']) == 3 and 1 <= sum(1 for o in p['opts'] if o.get('ok')) <= 2 and any(not o.get('ok') for o in p['opts']) for p in forks))
    ws = [w[0] for w in x['words']]
    chk('%s: 語は5つ・fork の語が語リストにある' % x['id'], len(ws) == 5 and all(w in ws for p in forks for w in p['fork']['tw']), ws)
    chk('%s: conv=1(単語バトルを出さない)' % x['id'], x.get('conv') == 1)
    jp = []
    for p in ps:
        if isinstance(p, dict):
            jp += [p['njp'], p.get('yjp', '')] + [o['jp'] for o in p['opts']] + [o['rep'][1] for o in p['opts']]
        else:
            jp += [p[1], p[3]]
    jp += [w[1] for w in x['words']]
    chk('%s: 日本語訳は出さない(台詞・返事・語の日本語はすべて空)' % x['id'], all(j == '' for j in jp))
    for p in ps:
        if isinstance(p, dict):
            alltext += [p['n']] + [o['y'] for o in p['opts']] + [o['rep'][0] for o in p['opts']]
        else:
            alltext += [p[0], p[2]]
T = ' '.join(alltext)
def scene_text(x):
    o = []
    for p in x['pairs']:
        o += ([p['n']] + [q['y'] for q in p['opts']] + [q['rep'][0] for q in p['opts']]) if isinstance(p, dict) else [p[0], p[2]]
    return ' '.join(o).replace('*', '')
chk('実在情報: Wi-Fi名 "Rovaniemi Airport Free Wi-Fi" が wifi1・wifi2 の両方にある(つづりどおり)', all('Rovaniemi Airport Free Wi-Fi' in scene_text(x) for x in SC if x['id'] in ('rvn_wifi1', 'rvn_wifi2')))
chk('実在情報: バス8番・Airport Express・サンタクロース村・2〜3km が bus にある', all(k in T for k in ['bus number eight', 'Airport Express', 'Santa Claus Village', 'two or three kilometers']))
chk('実在情報: 北極圏ライン・天窓の光・年のプレート・"Welcome to Rovaniemi Airport"', all(k in T for k in ['Arctic Circle line', 'skylight', 'plate', 'Welcome to Rovaniemi Airport']))
chk('未確認の情報を出さない: 値段・通貨・時刻・所要時間・店名・便名・番号付きの料金がない', not re.search(r'[€$¥]|euro|price|cost|how much|\bminutes?\b|\bhours?\b|o\'clock|\d|Ahkio|Napapiirin|Finnair|Iberia|Finavia|last bus|timetable', T, re.I), re.findall(r'[€$¥]|euro|price|cost|how much|\bminutes?\b|\bhours?\b|o\'clock|\d|Ahkio|Napapiirin|Finnair|Iberia|Finavia|last bus|timetable', T, re.I))
chk('個人名がない(Mr/Ms/Mrs・名乗り)', not re.search(r'\b(Mr|Ms|Mrs|my name is|I am called)\b', T, re.I))
# 画面の文字(背景のコード描画)に未確認の看板文言がない
src = open(os.path.join(ROOT, 'tour-src/build.py'), encoding='utf-8').read()
bg = src[src.index('BGR = r"""'):src.index('MAIN_RVN = r"""')]
texts = sorted(set(re.findall(r"T\('([^']+)'", bg)))
OKT = {'ROVANIEMI', 'Arrivals', 'Welcome to', 'Rovaniemi', 'Airport', 'Rovaniemi Airport', 'Free Wi-Fi', '8', 'AIRPORT EXPRESS', 'Napapiirin Lahja', 'Ahkio'}   # 072 の出発側の確認済みの店名(Finavia 公式)
chk('背景に描く文字は 確認済みのものだけ(ROVANIEMI / Arrivals / Welcome to Rovaniemi Airport / Wi-Fi名 / 8 / AIRPORT EXPRESS)', set(texts) <= OKT, texts)

# ---------------- ブラウザ ----------------
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,PBY:PBY,PLACES_RARR:PLACES_RARR,setMode:setMode,showMap:showMap,enterPlace:enterPlace,startVid:startVid,"
        "ART:ART,TRIP:TRIP,artIdFor:artIdFor,ARTFAIL:ARTFAIL,DLG:DLG,TOUR_IDS:TOUR_IDS,worldSync:worldSync,storeSave:storeSave,MODES:MODES,lockedPlace:lockedPlace,gt:function(){return t}};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "window.__say=[];try{speechSynthesis.speak=function(u){window.__say.push(u.text);setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));")
LEGS = [('HND', 'DOH'), ('DOH', 'NBO'), ('NBO', 'DOH'), ('DOH', 'HEL'), ('HEL', 'RVN'), ('RVN', 'MAD'), ('MAD', 'LIM'), ('LIM', 'CUZ'), ('CUZ', 'LIM'), ('LIM', 'MIA'), ('MIA', 'DFW'), ('DFW', 'HNL'), ('HNL', 'HND')]
def seed(landed, td, day):
    return {'v': 1, 'trip': 1, 'tk': 'ow', 'day': day, 'td': td, 'ph': 'day', 'bun': 1,
            'legs': [{'i': i, 'fr': a, 'to': b, 'd': None, 'f': 1 if i < landed else 0, 'l': 1 if i < landed else 0} for i, (a, b) in enumerate(LEGS)], 'days': [], 'cur': {'led': [], 'pick': []}}
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
FORBID = ['勉強', 'テスト', '測定', '練習', '復習', '採点']
def snap(p):
    d = p.evaluate("()=>document.getElementById('sceneA').toDataURL('image/png')")
    return np.array(Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB')).astype(int)
def newpage(br, sd, path='/tour/rovaniemi/index.html', hook=True):
    ctx = br.new_context(viewport={'width': 430, 'height': 900}, device_scale_factor=1)
    ctx.add_init_script(INIT)
    ctx.add_init_script("if(!localStorage.getItem('__seeded')){localStorage.setItem('__seeded','1');localStorage.setItem('kanpe-trip-v1',%s);localStorage.setItem('kanpe-tour-save-v1','{\"seen\":{},\"ticket\":\"ow\"}')}" % json.dumps(json.dumps(sd)))
    pg = ctx.new_page()
    if hook: pg.route('**' + path, hooked)
    pg.goto(base + path); pg.wait_for_timeout(1300); return pg
def dismiss(pg): pg.mouse.click(215, 450); pg.wait_for_timeout(900)
def play(p, pl, vid): p.evaluate("(a)=>{var T=window.__T;T.startVid(T.PBY[a[0]],a[1],'ev')}", [pl, vid])
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--no-sandbox'])
    # ---------------- (5) 旅の骨組み(ロヴァニエミのページ。10日目・ヘルシンキまで着いた) ----------------
    pg = newpage(br, seed(5, 10, 10)); dismiss(pg)
    r = pg.evaluate("(function(){var T=TRIP;return {impl:T.IMPL.RVN,ow:T.ROWS.ow[9][5],star:T.ROWS.star[9][5],grp:T.GROUPS.rvn_arr,pg:T.PLACEGRP.rimmig+T.PLACEGRP.rbus,"
                    "lock:['rimmig','rbag','rlobby','rwifi','rbus'].map(function(i){return __T.lockedPlace(i)}),tot:__T.TOUR_IDS.length,places:__T.PLACES_RARR.map(function(p){return p.id}),hour:T.HOUR.rbus}})()")
    chk('IMPL に RVN', r['impl'] == 1)
    chk('oneworld 10日目・Star 10日目とも rvn_arr を載せている', r['ow'] == ['rvn_arr'] and r['star'] == ['rvn_arr'], (r['ow'], r['star']))
    chk('rvn_arr は5場所×2場面(場所ごとにどちらか1本あそべば終わり)', r['grp'] == [['rvn_immig1', 'rvn_immig2'], ['rvn_bag1', 'rvn_bag2'], ['rvn_lobby1', 'rvn_lobby2'], ['rvn_wifi1', 'rvn_wifi2'], ['rvn_bus1', 'rvn_bus2']])
    chk('場所の並び: 入国審査→手荷物→到着ロビー→無料Wi-Fi→バス乗り場', r['places'] == ['rimmig', 'rbag', 'rlobby', 'rwifi', 'rbus'], r['places'])
    chk('場所の鍵: 入国審査だけ開き、あとは上から順に閉じている', r['lock'] == [False, True, True, True, True], r['lock'])
    chk('TOUR_IDS は30本(到着10+滞在・夜・出発20。「かいわ n / 30」)', r['tot'] == 30, r['tot'])
    chk('場所→まとまりの対応(PLACEGRP)が rvn_arr', r['pg'] == 'rvn_arrrvn_arr', r['pg'])
    chk('ページが開く(エラーなし)', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    # 1本ずつ遊ぶと、次の場所が開く
    seen = {}
    for pl, vid in [('rimmig', 'rvn_immig1'), ('rbag', 'rvn_bag2'), ('rlobby', 'rvn_lobby2'), ('rwifi', 'rvn_wifi1')]:
        pg.evaluate("(a)=>{__T.save.seen[a]=1;__T.storeSave();__T.worldSync()}", vid)
    r = pg.evaluate("['rimmig','rbag','rlobby','rwifi','rbus'].map(function(i){return __T.lockedPlace(i)})")
    chk('入国→荷物→ロビー→Wi-Fi をあそぶと、バス乗り場が開く', r == [False, False, False, False, False], r)
    w0 = pg.evaluate("JSON.parse(localStorage.getItem('kanpe-world-v1')||'{}').cleared||{}")
    chk('到着の場所を全部あそぶまで、世界マップに印はつかない(4/5)', 'rovaniemi' not in w0, w0)
    pg.evaluate("(a)=>{__T.save.seen[a]=1;__T.storeSave();__T.worldSync()}", 'rvn_bus2')
    w1 = pg.evaluate("JSON.parse(localStorage.getItem('kanpe-world-v1')||'{}').cleared||{}")
    chk('5場所をあそぶと 世界マップに ロヴァニエミの印', w1.get('rovaniemi') == 1, w1)
    pg.context.close()

    # ---------------- (3) 到着ロビー(実画) ----------------
    pg = newpage(br, seed(5, 10, 10)); dismiss(pg)
    play(pg, 'rlobby', 'rvn_lobby1'); pg.wait_for_timeout(8500)
    cf = pg.evaluate("(function(){var T=__T;var c=T.ART.rvnlobby;return {id:T.artIdFor(T.G.scene),bg:c.bg,strips:c.strips,dep:c.dep,fail:T.ARTFAIL.rvnlobby||0,vid:T.G.scene.vid}})()")
    chk('rvn_lobby1: art id rvnlobby・背景 rovaniemi-arrivals-v1.png', cf['id'] == 'rvnlobby' and cf['bg'] == 'rovaniemi-arrivals-v1.png' and not cf['fail'], cf['id'])
    bgS = rgb('rovaniemi-arrivals-v1.png'); sn = snap(pg)
    chk('背景の画素が素材と一致(窓帯より上の天井。人も動きもない領域)', frac_same(sn[0:120, :], bgS[0:120, :]) > .999, frac_same(sn[0:120, :], bgS[0:120, :]))
    st = cf['strips'][0]
    chk('オーロラ: 左上(80,128)・4コマ・1コマ 1376×172・1.2秒ごと', (st['img'], st['x'], st['y'], st['n'], st['fw'], st['fh'], st['step']) == ('rovaniemi-aurora-strip.png', 80, 128, 4, 1376, 172, 1.2), st)
    ss = img('rovaniemi-aurora-strip.png')
    def comp(k):
        b = Image.fromarray(bgS.astype('uint8')).convert('RGBA'); b.alpha_composite(ss.crop((k * 1376, 0, k * 1376 + 1376, 172)), (80, 128)); return np.array(b.convert('RGB')).astype(int)
    comps = [comp(k)[128:300, 80:1456] for k in range(4)]
    seen_k, order = set(), []
    for i in range(60):
        a = snap(pg)[128:300, 80:1456]
        ds = [float(np.abs(a - comps[k]).mean()) for k in range(4)]; k0 = int(np.argmin(ds))
        order.append(k0 if ds[k0] < 1.0 and sorted(ds)[1] > 3 * max(ds[k0], .05) else -1); seen_k.add(order[-1]); pg.wait_for_timeout(120)
    chk('オーロラの4コマがすべて、位置(80,128)の画素どおりに出る(半透明の縁の丸め誤差は平均1以下)', seen_k == {0, 1, 2, 3}, order)
    ch = [i for i in range(1, len(order)) if order[i] != order[i - 1] and order[i] >= 0 and order[i - 1] >= 0]
    chk('オーロラは順に切り替わる(0→1→2→3→0)', all((order[i] - order[i - 1]) % 4 == 1 for i in ch), order)
    d = cf['dep']
    chk('ふたりは後ろ姿で足もと y=884(ルル x=700・キング x=836)', (d['lulu']['n'], d['lulu']['x'], d['lulu']['by'], d['king']['n'], d['king']['x'], d['king']['by']) == ('hall-lulu-back', 700, 884, 'hall-king-back', 836, 884), d)
    sn = snap(pg)
    lb = Image.open(os.path.join(ART, 'npc/hall-lulu-back.png')).size; kb = Image.open(os.path.join(ART, 'npc/hall-king-back.png')).size
    def region(x, by, sz): return (slice(by - sz[1], by), slice(x - sz[0] // 2, x - sz[0] // 2 + sz[0]))
    for nm, (x, by, sz) in {'ルル': (700, 884, lb), 'キング': (836, 884, kb)}.items():
        rs = region(x, by, sz); chk('%s が描かれている(その矩形の画素が背景と変わっている)' % nm, frac_same(sn[rs], bgS[rs]) < .9)
    chk('ルルが左・キングが右', d['lulu']['x'] < d['king']['x'])
    pr = d['npcS']['r_greeter']; rs = region(pr['x'], pr['by'], Image.open(os.path.join(ART, 'npc', pr['n'] + '.png')).size)
    chk('話し相手(lobby1 の旅行者)がふたりの右に立っている・描かれている', pr['x'] > d['king']['x'] + 100 and frac_same(sn[rs], bgS[rs]) < .9, pr)
    chk('相手がトロリー(904..994×636..738)とウェルカム看板(1112..)に重ならない', pr['x'] + 40 < 1112 and pr['by'] - 126 > 738)
    pg.screenshot(path='/tmp/rt/final_lobby1.png')
    chk('lobby1: エラーなし', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    pg.context.close()
    pg = newpage(br, seed(5, 10, 10)); dismiss(pg)
    play(pg, 'rlobby', 'rvn_lobby2'); pg.wait_for_timeout(8500)
    c2 = pg.evaluate("[__T.artIdFor(__T.G.scene),__T.G.scene.vid,__T.G.scene.d.bg]"); s2 = snap(pg)
    chk('rvn_lobby2 も art id rvnlobby・背景は実画', c2 == ['rvnlobby', 'rvn_lobby2', 'rlobby'] and frac_same(s2[0:120, :], bgS[0:120, :]) > .999, c2)
    pr = cf['dep']['npcS']['r_local']; rs = region(pr['x'], pr['by'], Image.open(os.path.join(ART, 'npc', pr['n'] + '.png')).size)
    chk('lobby2: 話し相手(職員)が描かれている', frac_same(s2[rs], bgS[rs]) < .9)
    pg.context.close()

    # ---------------- (4) ほかの4場所(コード描画)・会話が進む ----------------
    for pl, vid in [('rimmig', 'rvn_immig1'), ('rimmig', 'rvn_immig2'), ('rbag', 'rvn_bag1'), ('rbag', 'rvn_bag2'), ('rwifi', 'rvn_wifi1'), ('rwifi', 'rvn_wifi2'), ('rbus', 'rvn_bus1'), ('rbus', 'rvn_bus2')]:
        pg = newpage(br, seed(5, 10, 10)); dismiss(pg)
        play(pg, pl, vid); pg.wait_for_timeout(2500)
        aid = pg.evaluate("__T.artIdFor(__T.G.scene)")
        vis = pg.evaluate("(function(){var a=document.getElementById('scene'),b=document.getElementById('sceneA');return [!a.hidden,b.hidden]})()")
        pg.evaluate("document.querySelector('button.btn.go').click()"); pg.wait_for_timeout(5000)
        ph = pg.evaluate("[__T.G.scene.vid,__T.G.phase,!!document.querySelector('.cue'),document.querySelector('#msgText').textContent]")
        txt = pg.evaluate("document.body.innerText")
        chk('%s: コード描画(art id なし・ドット画の canvas が出る)' % vid, aid is None and vis == [True, True], (aid, vis))
        chk('%s: 会話が進む(相手の台詞のあとカンペが出る)' % vid, ph[0] == vid and ph[2] is True and len(ph[3]) > 10, ph)
        chk('%s: 画面に「勉強・テスト・測定・練習」の言葉がない・エラーなし' % vid, not any(w in txt for w in FORBID) and pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
        pg.context.close()
    # 分かれ目: 2つ目の台詞で▶の返事が3つ出る(英語のみ)
    pg = newpage(br, seed(5, 10, 10)); dismiss(pg)
    play(pg, 'rwifi', 'rvn_wifi1'); pg.wait_for_timeout(2500)
    chk('wifi1: 2番目の台詞に分かれ目(3つの返事)が入っている', pg.evaluate("(function(){var L=__T.G.scene.d.lines;return L[3].opts&&L[3].opts.length===3&&L[3].opts.every(function(o){return /^[\\x00-\\x7f*]+$/.test(o.y)})})()"))
    pg.context.close()

    # ---------------- (6) 世界マップ ----------------
    pg = newpage(br, seed(3, 9, 9), path='/world/index.html', hook=False); pg.mouse.click(215, 450); pg.wait_for_timeout(600)
    wm = pg.evaluate("(function(){return {ap:window.__AP?1:0}})()")
    html = open(os.path.join(ROOT, 'world/index.html'), encoding='utf-8').read()
    chk('世界マップ: ロヴァニエミ(url ../tour/rovaniemi/)がドーハの隣', "rovaniemi:{n:'ロヴァニエミ'" in html and "url:'../tour/rovaniemi/'" in html and "doha:['nairobi','dubai','rovaniemi'],rovaniemi:['doha']" in html)
    ch = pg.evaluate("(function(){var c=TRIP.chain('RVN');return c&&c.map(function(j){return TRIP.legInfo(j).fr+'>'+TRIP.legInfo(j).to})})()")
    chk('ドーハにいる10日目前: chain(RVN) = DOH>HEL→HEL>RVN(ヘルシンキは乗り継ぎだけ)', ch == ['DOH>HEL', 'HEL>RVN'], ch)
    chk('canFly(rovaniemi) が true・ヘルシンキ(場面なし)は飛べない', pg.evaluate("[TRIP.canFly('rovaniemi'),TRIP.canFly('helsinki')]") == [True, False])
    pg.context.close()
    br.close()
print('\nNG:', bad if bad else 'なし')
sys.exit(1 if bad else 0)
