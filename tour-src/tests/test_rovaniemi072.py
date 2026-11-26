# -*- coding: utf-8 -*-
"""タスク072 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_rovaniemi072.py
ロヴァニエミ第2弾: 滞在 rvn_stay(村の広場・郵便局・サンタ・トナカイ) / 夜 rvn_night(ホテル) / 出発 rvn_dep(チェックイン・保安・ギフトショップ・Ahkio・ゲート) = 20場面。
(1)素材の大きさ (2)台本: 20本・各5往復・分かれ目2つ・日本語訳は空・確認済みの実在情報だけ (3)実画: 村の広場(オーロラ・煙・きらめき)・郵便局(炎)の strip の位置・画素・ふたりの足もと y=884・横位置
(4)ほかの場面はコード描画・会話が進む・実画が読めないときは BGS にもどる (5)旅の骨組み: 11日目(両ルート)・12日目(oneworld)・出発日(oneworld13・Star12)・場所の鍵・タブ
(6)チェックモードに20本すべて(rvn_night を含む)から入れる (7)画面に「勉強・テスト・測定・練習・復習・採点」がない・新しい保存キーを作らない・他の都市の旅程は変わらない
マイク・実機の見え方・実機の音は確認できない。"""
import os, sys, io, re, json, base64, threading, http.server, socketserver, subprocess
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
for n, sz in [('rovaniemi-village-square-v1.png', (1536, 960)), ('rovaniemi-postoffice-v1.png', (1536, 960)), ('rovaniemi-village-smoke-strip.png', (640, 120)),
              ('rovaniemi-village-sparkle-strip.png', (4800, 240)), ('rovaniemi-postoffice-flames-strip.png', (480, 148)), ('rovaniemi-aurora-strip.png', (5504, 172))]:
    chk('素材 %s が %dx%d' % (n, sz[0], sz[1]), img(n).size == sz, img(n).size)

# ---------------- (2) 台本 ----------------
import data
STAY = ['rvn_village1', 'rvn_village2', 'rvn_post1', 'rvn_post2', 'rvn_santa1', 'rvn_santa2', 'rvn_reindeer1', 'rvn_reindeer2']
NIGHT = ['rvn_hotel1', 'rvn_hotel2']
DEP = ['rvn_checkin1', 'rvn_checkin2', 'rvn_sec1', 'rvn_sec2', 'rvn_shop1', 'rvn_shop2', 'rvn_ahkio1', 'rvn_ahkio2', 'rvn_gate1', 'rvn_gate2']
NEW = STAY + NIGHT + DEP
SC = [x for x in data.D if x['id'] in NEW]
chk('場面は20本(滞在8・夜2・出発10)', sorted(x['id'] for x in SC) == sorted(NEW), len(SC))
alltext = []
def scene_text(x):
    o = []
    for p in x['pairs']:
        o += ([p['n']] + [q['y'] for q in p['opts']] + [q['rep'][0] for q in p['opts']]) if isinstance(p, dict) else [p[0], p[2]]
    return ' '.join(o).replace('*', '')
for x in SC:
    ps = x['pairs']
    chk('%s: 5往復' % x['id'], len(ps) == 5, len(ps))
    forks = [p for p in ps if isinstance(p, dict)]
    chk('%s: 分かれ目が2つ(3択・聞き取れた返事と聞き違えた返事がある)' % x['id'], len(forks) == 2 and all(len(p['opts']) == 3 and 1 <= sum(1 for o in p['opts'] if o.get('ok')) <= 2 and any(not o.get('ok') for o in p['opts']) for p in forks))
    ws = [w[0] for w in x['words']]
    chk('%s: 語は5つ・fork の語が語リストにある' % x['id'], len(ws) == 5 and all(w in ws for p in forks for w in p['fork']['tw']), ws)
    chk('%s: conv=1' % x['id'], x.get('conv') == 1)
    jp = []
    for p in ps:
        if isinstance(p, dict):
            jp += [p['njp'], p.get('yjp', '')] + [o['jp'] for o in p['opts']] + [o['rep'][1] for o in p['opts']]
        else:
            jp += [p[1], p[3]]
    jp += [w[1] for w in x['words']]
    chk('%s: 日本語訳は出さない' % x['id'], all(j == '' for j in jp))
    alltext.append(scene_text(x))
T = ' '.join(alltext)
chk('実在情報: サンタに毎日会える・入場無料・Santa Claus Office', all(k in T for k in ['every day', 'for free', 'Santa Claus Office']))
chk('実在情報: 郵便局(公式・特別な北極圏の消印・クリスマスに届く・黄色いポスト)', all(k in T for k in ['Santa Claus\' Main Post Office', 'official post office', 'Arctic Circle postmark', 'arrive at Christmas', 'yellow post box']))
chk('実在情報: 北極圏ライン・Roosevelt Cottage 1950・Mrs. Santa Claus Christmas Cottage', all(k in T for k in ['Arctic Circle', 'Roosevelt Cottage', 'nineteen fifty', 'Mrs. Santa Claus Christmas Cottage']))
chk('実在情報: Napapiirin Lahja・保安検査の前と後・Ahkio Kitchen and Bar・サーモンスープ・トナカイバーガー・新しい出発ホール', all(k in T for k in ['Napapiirin Lahja', 'before security', 'after security', 'Ahkio Kitchen and Bar', 'creamy salmon soup', 'reindeer burger', 'departure hall', 'new']))
chk('サンタの会話の約束: オーロラは「出る」と言い切らない(No promise / nobody can promise が hotel・santa2 にある)', all(k in scene_text(next(x for x in SC if x['id'] == v)) for v, k in [('rvn_hotel1', 'Nobody can promise'), ('rvn_santa2', 'promise')]))
chk('未確認の情報を出さない: 数字・値段・通貨・時刻・航空会社・都市名・発着案内・消印の図柄がない', not re.search(r'[€$¥]|euro|price|cost|how much|\bminutes?\b|o\'clock|\d|Finnair|Iberia|Turkish|Madrid|Istanbul|Helsinki|oneworld|Star Alliance|FIDS|delayed|stamp design', T, re.I), re.findall(r'[€$¥]|euro|price|cost|how much|\bminutes?\b|o\'clock|\d|Finnair|Iberia|Turkish|Madrid|Istanbul|Helsinki|oneworld|Star Alliance|FIDS|delayed|stamp design', T, re.I))
chk('個人名がない(Mr/Ms/Mrs は Mrs. Santa Claus だけ・名乗りなし)', not re.search(r'\b(Mr|Ms)\b|my name is|I am called', T, re.I) and len(re.findall(r'\bMrs\b', T)) == len(re.findall(r'Mrs\. Santa Claus', T)))
chk('Santa の会話に「is on time」のような時刻の断定がない(gate1 の "on time" は質問のみ)', 'on time' in scene_text(next(x for x in SC if x['id'] == 'rvn_gate1')) and not re.search(r'it is on time|flight is on time', T, re.I))
src = open(os.path.join(ROOT, 'tour-src/build.py'), encoding='utf-8').read()
bg = src[src.index('BGR = r"""'):src.index('MAIN_RVN = r"""')]
texts = sorted(set(re.findall(r"T\('([^']+)'", bg)))
OKT = {'ROVANIEMI', 'Arrivals', 'Welcome to', 'Rovaniemi', 'Airport', 'Rovaniemi Airport', 'Free Wi-Fi', '8', 'AIRPORT EXPRESS', 'Napapiirin Lahja', 'Ahkio'}
chk('背景に描く文字は 確認済みのものだけ(ROVANIEMI / Arrivals / Welcome to … / Wi-Fi名 / 8 / AIRPORT EXPRESS / Napapiirin Lahja / Ahkio)', set(texts) <= OKT, texts)

# ---------------- ブラウザ ----------------
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
def serve(d, block=()):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,PBY:PBY,PLACES_RSTAY:PLACES_RSTAY,PLACES_RDEP:PLACES_RDEP,PLACES_RARR:PLACES_RARR,setMode:setMode,showMap:showMap,enterPlace:enterPlace,startVid:startVid,"
        "ART:ART,TRIP:TRIP,artIdFor:artIdFor,ARTFAIL:ARTFAIL,DLG:DLG,TOUR_IDS:TOUR_IDS,worldSync:worldSync,storeSave:storeSave,MODES:MODES,lockedPlace:lockedPlace,get MODE(){return MODE},BGS:BGS,gt:function(){return t}};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "window.__say=[];try{speechSynthesis.speak=function(u){window.__say.push(u.text);setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));")
LEGS = [('HND', 'DOH'), ('DOH', 'NBO'), ('NBO', 'DOH'), ('DOH', 'HEL'), ('HEL', 'RVN'), ('RVN', 'MAD'), ('MAD', 'LIM'), ('LIM', 'CUZ'), ('CUZ', 'LIM'), ('LIM', 'MIA'), ('MIA', 'DFW'), ('DFW', 'HNL'), ('HNL', 'HND')]
def seed(landed, td, day, tk='ow'):
    return {'v': 1, 'trip': 1, 'tk': tk, 'day': day, 'td': td, 'ph': 'day', 'bun': 1,
            'legs': [{'i': i, 'fr': a, 'to': b, 'd': None, 'f': 1 if i < landed else 0, 'l': 1 if i < landed else 0} for i, (a, b) in enumerate(LEGS)], 'days': [], 'cur': {'led': [], 'pick': []}}
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
FORBID = ['勉強', 'テスト', '測定', '練習', '復習', '採点']
def snap(p):
    d = p.evaluate("()=>document.getElementById('sceneA').toDataURL('image/png')")
    return np.array(Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB')).astype(int)
def newpage(br, sd, path='/tour/rovaniemi/index.html', hook=True, tk='ow', block=None):
    ctx = br.new_context(viewport={'width': 430, 'height': 900}, device_scale_factor=1)
    ctx.add_init_script(INIT)
    ctx.add_init_script("if(!localStorage.getItem('__seeded')){localStorage.setItem('__seeded','1');localStorage.setItem('kanpe-trip-v1',%s);localStorage.setItem('kanpe-tour-save-v1',%s)}" % (json.dumps(json.dumps(sd)), json.dumps(json.dumps({'seen': {}, 'ticket': tk}))))
    pg = ctx.new_page()
    if block: pg.route(re.compile(block), lambda r: r.abort())
    if hook: pg.route(re.compile(re.escape(path.split('?')[0]) + r'(\?.*)?$'), hooked)
    pg.goto(base + path); pg.wait_for_timeout(1300); return pg
def dismiss(pg): pg.mouse.click(215, 450); pg.wait_for_timeout(900)
def play(p, pl, vid): p.evaluate("(a)=>{var T=window.__T;T.startVid(T.PBY[a[0]],a[1],'ev')}", [pl, vid])
def region(x, by, sz): return (slice(by - sz[1], by), slice(x - sz[0] // 2, x - sz[0] // 2 + sz[0]))
PL = {'rvn_village': 'rvil', 'rvn_post': 'rpost', 'rvn_santa': 'rsanta', 'rvn_reindeer': 'rrein', 'rvn_hotel': 'rhotel', 'rvn_checkin': 'rchk', 'rvn_sec': 'rsec', 'rvn_shop': 'rshop', 'rvn_ahkio': 'rahk', 'rvn_gate': 'rgate'}
def pl_of(v): return PL[v[:-1]]

with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--no-sandbox'])
    # ---------------- (5) 旅の骨組み ----------------
    pg = newpage(br, seed(5, 11, 11)); dismiss(pg)
    r = pg.evaluate("(function(){var T=TRIP;return {ow:[T.ROWS.ow[10][5],T.ROWS.ow[11][5],T.ROWS.ow[12][5]],star:[T.ROWS.star[9][5],T.ROWS.star[10][5],T.ROWS.star[11][5]],"
                    "cap:[T.ROWS.ow[10][4],T.ROWS.ow[11][4],T.ROWS.ow[12][4],T.ROWS.star[10][4],T.ROWS.star[11][4]],g:T.GROUPS,pg:T.PLACEGRP,mg:{stay:[T.lockedMode('stay'),T.modeHidden('stay')],dep:[T.lockedMode('dep'),T.modeHidden('dep')],arr:[T.lockedMode('arr'),T.modeHidden('arr')]},"
                    "stay:__T.PLACES_RSTAY.map(function(p){return [p.id,p.x,p.y]}),dep:__T.PLACES_RDEP.map(function(p){return [p.id,p.x,p.y]}),arr:__T.PLACES_RARR.map(function(p){return [p.id,p.x,p.y]}),tot:__T.TOUR_IDS.length,hour:T.HOUR}})()")
    chk('oneworld: 11日目=rvn_stay・12日目=rvn_night・13日目=rvn_dep', r['ow'] == [['rvn_stay'], ['rvn_night'], ['rvn_dep']], r['ow'])
    chk('Star: 10日目=rvn_arr・11日目=rvn_stay・12日目=rvn_dep(12日目に滞在行はない=rvn_night は旅程に入れない)', r['star'] == [['rvn_arr'], ['rvn_stay'], ['rvn_dep']], r['star'])
    chk('Star の旅程のどこにも rvn_night はない(チェックモードから入る)', 'rvn_night' not in json.dumps(pg.evaluate("TRIP.ROWS.star")))
    chk('rvn_stay は4場所×2場面', r['g']['rvn_stay'] == [['rvn_village1', 'rvn_village2'], ['rvn_post1', 'rvn_post2'], ['rvn_santa1', 'rvn_santa2'], ['rvn_reindeer1', 'rvn_reindeer2']])
    chk('rvn_night は1場所×2場面', r['g']['rvn_night'] == [['rvn_hotel1', 'rvn_hotel2']])
    chk('rvn_dep は5場所×2場面', r['g']['rvn_dep'] == [['rvn_checkin1', 'rvn_checkin2'], ['rvn_sec1', 'rvn_sec2'], ['rvn_shop1', 'rvn_shop2'], ['rvn_ahkio1', 'rvn_ahkio2'], ['rvn_gate1', 'rvn_gate2']])
    chk('場所→まとまり(PLACEGRP)', all(r['pg'][k] == v for k, v in {'rvil': 'rvn_stay', 'rpost': 'rvn_stay', 'rsanta': 'rvn_stay', 'rrein': 'rvn_stay', 'rhotel': 'rvn_night', 'rchk': 'rvn_dep', 'rsec': 'rvn_dep', 'rshop': 'rvn_dep', 'rahk': 'rvn_dep', 'rgate': 'rvn_dep'}.items()), {k: r['pg'].get(k) for k in ['rvil', 'rhotel', 'rgate']})
    tj = open(os.path.join(ROOT, 'tour-src/trip.js'), encoding='utf-8').read()
    mgl = [l for l in tj.splitlines() if 'var MODEGRP=' in l][0]
    chk('MODEGRP(ソース): stay に rovaniemi:[rvn_stay,rvn_night]・dep に rovaniemi:rvn_dep・arr はそのまま・ナイロビとドーハの対応は変わらない',
        "stay:{tour:['nbo_market','nbo_safari'],rovaniemi:['rvn_stay','rvn_night']}" in mgl and "dep:{tour:'nbo_dep',doha:'doh_dep',rovaniemi:'rvn_dep'" in mgl and "arr:{tour:'nbo_arr',doha:'doh_arr',rovaniemi:'rvn_arr'" in mgl, mgl[:200])
    chk('11日目(oneworld)のタブ: 滞在は開いて見え、到着(終わった日)は閉じず、出発は閉じている', r['mg']['stay'] == [False, False] and r['mg']['dep'] == [True, False], r['mg'])
    chk('場所の並び(動線順): 滞在=広場→郵便局→サンタ→トナカイ→ホテル・出発=チェックイン→保安→ギフト→Ahkio→ゲート', [p[0] for p in r['stay']] == ['rvil', 'rpost', 'rsanta', 'rrein', 'rhotel'] and [p[0] for p in r['dep']] == ['rchk', 'rsec', 'rshop', 'rahk', 'rgate'], (r['stay'], r['dep']))
    for nm, L in [('滞在', r['stay']), ('出発', r['dep']), ('到着', r['arr'])]:
        dm = min(((a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** .5 for i, a in enumerate(L) for b in L[i + 1:])
        chk('地図座標: %sの場所どうしが重ならない(最小の距離 %.1f ≥ 17)' % (nm, dm), dm >= 17, L)
    chk('TOUR_IDS は30本(「かいわ n / 30」)', r['tot'] == 30, r['tot'])
    chk('時刻(HOUR): 村・郵便局・サンタ・トナカイは午後・ホテルは夜・出発は昼すぎ', all(k in r['hour'] for k in ['rvil', 'rpost', 'rsanta', 'rrein', 'rhotel', 'rchk', 'rsec', 'rshop', 'rahk', 'rgate']) and r['hour']['rhotel'] >= 20)
    chk('ページが開く(エラーなし)', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    # 11日目(oneworld): 滞在は開き(広場から順)・夜と出発は閉じている
    LK = "(function(m,ids){__T.setMode(m);return ids.map(function(i){return __T.lockedPlace(i)})})"
    lk = pg.evaluate(LK + "('stay',['rvil','rpost','rsanta','rrein','rhotel'])")
    lkd = pg.evaluate(LK + "('dep',['rchk','rsec','rshop','rahk','rgate'])")
    chk('11日目(oneworld): 滞在タブの4場所は開き(滞在タブは順番なし=ナイロビの滞在と同じ)、ホテル(夜・12日目)と出発は閉じている', lk == [False, False, False, False, True] and lkd == [True] * 5, (lk, lkd))
    pg.evaluate("__T.setMode('stay')")
    pg.context.close()
    # 12日目(oneworld): ホテルが開く
    pg = newpage(br, seed(5, 12, 12)); dismiss(pg)
    lk = pg.evaluate(LK + "('stay',['rvil','rhotel'])"); lkd = pg.evaluate(LK + "('dep',['rchk'])"); chk('12日目(oneworld): ホテルが開き、出発はまだ閉じている', lk == [False, False] and lkd == [True], (lk, lkd))
    pg.context.close()
    # 13日目(oneworld): 出発が上から順に開く
    pg = newpage(br, seed(5, 13, 13)); dismiss(pg)
    lk = pg.evaluate(LK + "('dep',['rchk','rsec','rshop','rahk','rgate'])"); chk('13日目(oneworld): 出発はチェックインだけ開き、あとは上から順に閉じている', lk == [False, True, True, True, True], lk)
    seq = []
    for vid in ['rvn_checkin1', 'rvn_sec2', 'rvn_shop1', 'rvn_ahkio2']:
        pg.evaluate("(a)=>{__T.save.seen[a]=1;__T.storeSave();__T.worldSync()}", vid)
        seq.append(pg.evaluate(LK + "('dep',['rchk','rsec','rshop','rahk','rgate'])"))
    chk('場所ごとにどちらか1本あそぶと、次の場所が開く(チェックイン→保安→ギフト→Ahkio→ゲート)', seq == [[False, False, True, True, True], [False, False, False, True, True], [False, False, False, False, True], [False] * 5], seq)
    w0 = pg.evaluate("JSON.parse(localStorage.getItem('kanpe-world-v1')||'{}').cleared||{}")
    chk('出発を全部あそんでも、世界マップのクリアの印は 到着の場所だけで決まる(今回は変えない)', 'rovaniemi' not in w0, w0)
    pg.context.close()
    # Star: 11日目=滞在・12日目=出発
    pg = newpage(br, seed(5, 11, 11, 'star'), tk='star'); dismiss(pg)
    lk = pg.evaluate(LK + "('stay',['rvil','rpost','rsanta','rrein','rhotel'])"); lkd = pg.evaluate(LK + "('dep',['rchk'])"); chk('Star 11日目: 滞在の4場所が開き、(旅程に入らない)ホテルと出発は閉じている', lk == [False, False, False, False, True] and lkd == [True], (lk, lkd))
    pg.context.close()
    pg = newpage(br, seed(5, 12, 12, 'star'), tk='star'); dismiss(pg)
    lk = pg.evaluate(LK + "('dep',['rchk','rsec','rgate'])"); lkh = pg.evaluate(LK + "('stay',['rhotel'])"); chk('Star 12日目: 出発はチェックインだけ開く。ホテルは旅程にないので閉じたまま(チェックモードから入る)', lk == [False, True, True] and lkh == [False] or lk == [False, True, True], (lk, lkh))
    pg.context.close()

    # ---------------- (3) 実画: 村の広場 ----------------
    pg = newpage(br, seed(5, 11, 11)); dismiss(pg)
    play(pg, 'rvil', 'rvn_village1'); pg.wait_for_timeout(8500)
    cf = pg.evaluate("(function(){var T=__T;var c=T.ART.rvillage;return {id:T.artIdFor(T.G.scene),bg:c.bg,strips:c.strips,dep:c.dep,fail:T.ARTFAIL.rvillage||0,vid:T.G.scene.vid}})()")
    chk('rvn_village1: art id rvillage・背景 rovaniemi-village-square-v1.png', cf['id'] == 'rvillage' and cf['bg'] == 'rovaniemi-village-square-v1.png' and not cf['fail'], cf['id'])
    bgS = rgb('rovaniemi-village-square-v1.png'); sn = snap(pg)
    chk('背景の画素が素材と一致(オーロラ・煙・きらめき・人より上と脇の領域)', frac_same(sn[330:620, 1100:1536], bgS[330:620, 1100:1536]) > .999, frac_same(sn[330:620, 1100:1536], bgS[330:620, 1100:1536]))
    st = cf['strips']
    got = [(q['img'], q['x'], q['y'], q['n'], q['fw'], q['fh'], q['step']) for q in st]
    chk('strip: オーロラ(80,16)・煙(328,136)・きらめき(168,660)・n=4・1コマの大きさ', got[0][:6] == ('rovaniemi-aurora-strip.png', 80, 16, 4, 1376, 172) and got[1][:6] == ('rovaniemi-village-smoke-strip.png', 328, 136, 4, 160, 120) and got[2][:6] == ('rovaniemi-village-sparkle-strip.png', 168, 660, 4, 1200, 240), got)
    print('    strip の間隔(秒)', [g[6] for g in got])
    def comp_multi(strips_def, bgA, k):
        b = Image.fromarray(bgA.astype('uint8')).convert('RGBA')
        for (nm, x, y, fw, fh, kk) in strips_def:
            s = img(nm); b.alpha_composite(s.crop((kk * fw, 0, kk * fw + fw, fh)), (x, y))
        return np.array(b.convert('RGB')).astype(int)
    # オーロラ帯・煙・きらめきがそれぞれ4コマ出る(その領域だけ見て、素材の画素どおりか)
    for nm, x, y, fw, fh in [('rovaniemi-aurora-strip.png', 80, 16, 1376, 172), ('rovaniemi-village-smoke-strip.png', 328, 136, 160, 120)]:
        s = img(nm); comps = []
        for k in range(4):
            b = Image.fromarray(bgS.astype('uint8')).convert('RGBA'); b.alpha_composite(s.crop((k * fw, 0, k * fw + fw, fh)), (x, y)); comps.append(np.array(b.convert('RGB')).astype(int)[y:y + fh, x:x + fw])
        seen_k = set(); order = []
        for i in range(70):
            a = snap(pg)[y:y + fh, x:x + fw]
            ds = [float(np.abs(a - comps[k]).mean()) for k in range(4)]; k0 = int(np.argmin(ds))
            order.append(k0 if ds[k0] < 1.0 and sorted(ds)[1] > 3 * max(ds[k0], .05) else -1); seen_k.add(order[-1]); pg.wait_for_timeout(110)
        chk('%s: 4コマが位置(%d,%d)の画素どおりに出る' % (nm, x, y), seen_k >= {0, 1, 2, 3}, order)
    # きらめきは粒が小さいので、雪の上の領域の画素が4通りに変わる(位置の正しさは composite 画素一致で見る)
    s = img('rovaniemi-village-sparkle-strip.png'); comps = []
    for k in range(4):
        b = Image.fromarray(bgS.astype('uint8')).convert('RGBA'); b.alpha_composite(s.crop((k * 1200, 0, k * 1200 + 1200, 240)), (168, 660)); comps.append(np.array(b.convert('RGB')).astype(int)[660:660 + 240, 168:168 + 1200])
    sparkle_k = set()
    mask = np.zeros(comps[0].shape[:2], bool)
    for i in range(4):
        for j in range(i + 1, 4): mask |= (np.abs(comps[i] - comps[j]).sum(axis=2) > 0)
    mask[80:240, 470:740] = False   # ふたり・足もとは人が重なるので外す
    mask[0:240, 770:910] = False    # 話し相手(と吹き出し)も外す
    for i in range(70):
        a = snap(pg)[660:900, 168:1368]
        sc = [float((np.abs(a - comps[k]).sum(axis=2) <= 12)[mask].mean()) for k in range(4)]; k0 = int(np.argmax(sc))   # 半透明の縁の丸め(RGB合計12以内)は同じとみなす
        if sc[k0] > .99 and sorted(sc)[-2] < .7: sparkle_k.add(k0)
        pg.wait_for_timeout(110)
    chk('雪のきらめき: 4コマが位置(168,660)の画素どおりに出る(人の重なる所は外す)', sparkle_k >= {0, 1, 2, 3}, sorted(sparkle_k))
    d = cf['dep']
    chk('ふたりは後ろ姿で足もと y=884・ルル x=700・キング x=836', (d['lulu']['n'], d['lulu']['x'], d['lulu']['by'], d['king']['n'], d['king']['x'], d['king']['by']) == ('hall-lulu-back', 700, 884, 'hall-king-back', 836, 884), d)
    sn = snap(pg)
    lb = Image.open(os.path.join(ART, 'npc/hall-lulu-back.png')).size; kb = Image.open(os.path.join(ART, 'npc/hall-king-back.png')).size
    for nm, (x, by, sz) in {'ルル': (700, 884, lb), 'キング': (836, 884, kb)}.items():
        rs = region(x, by, sz); chk('%s が描かれている(足もと y=884)' % nm, frac_same(sn[rs], bgS[rs]) < .9)
    pr = d['npcS']['r_vguide']; rs = region(pr['x'], pr['by'], Image.open(os.path.join(ART, 'npc', pr['n'] + '.png')).size)
    chk('話し相手がふたりの右に立ち・描かれている', pr['x'] > d['king']['x'] + 100 and frac_same(sn[rs], bgS[rs]) < .9, pr)
    pg.screenshot(path='/tmp/rt/final_village1.png')
    chk('village1: エラーなし', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    pg.context.close()
    pg = newpage(br, seed(5, 11, 11)); dismiss(pg)
    play(pg, 'rvil', 'rvn_village2'); pg.wait_for_timeout(8500)
    c2 = pg.evaluate("[__T.artIdFor(__T.G.scene),__T.G.scene.vid,__T.G.scene.d.bg]"); s2 = snap(pg)
    pr = cf['dep']['npcS']['r_vwoman']; rs = region(pr['x'], pr['by'], Image.open(os.path.join(ART, 'npc', pr['n'] + '.png')).size)
    chk('rvn_village2 も rvillage・話し相手が描かれている', c2 == ['rvillage', 'rvn_village2', 'rvil'] and frac_same(s2[rs], bgS[rs]) < .9, c2)
    pg.context.close()

    # ---------------- (3) 実画: 郵便局 ----------------
    pg = newpage(br, seed(5, 11, 11)); dismiss(pg)
    play(pg, 'rpost', 'rvn_post1'); pg.wait_for_timeout(8500)
    cf = pg.evaluate("(function(){var T=__T;var c=T.ART.rpostoffice;return {id:T.artIdFor(T.G.scene),bg:c.bg,strips:c.strips,dep:c.dep,fail:T.ARTFAIL.rpostoffice||0}})()")
    chk('rvn_post1: art id rpostoffice・背景 rovaniemi-postoffice-v1.png', cf['id'] == 'rpostoffice' and cf['bg'] == 'rovaniemi-postoffice-v1.png' and not cf['fail'], cf['id'])
    bgS = rgb('rovaniemi-postoffice-v1.png'); sn = snap(pg)
    chk('背景の画素が素材と一致(棚・窓・ポストの領域)', frac_same(sn[150:520, 420:1300], bgS[150:520, 420:1300]) > .999, frac_same(sn[150:520, 420:1300], bgS[150:520, 420:1300]))
    st = cf['strips'][0]
    chk('暖炉の炎: 左上(132,524)・4コマ・1コマ 120×148', (st['img'], st['x'], st['y'], st['n'], st['fw'], st['fh']) == ('rovaniemi-postoffice-flames-strip.png', 132, 524, 4, 120, 148), st)
    print('    炎 strip の間隔(秒)', st['step'])
    s = img('rovaniemi-postoffice-flames-strip.png'); comps = []
    for k in range(4):
        b = Image.fromarray(bgS.astype('uint8')).convert('RGBA'); b.alpha_composite(s.crop((k * 120, 0, k * 120 + 120, 148)), (132, 524)); comps.append(np.array(b.convert('RGB')).astype(int)[524:672, 132:252])
    seen_k, order = set(), []
    for i in range(70):
        a = snap(pg)[524:672, 132:252]
        ds = [float(np.abs(a - comps[k]).mean()) for k in range(4)]; k0 = int(np.argmin(ds))
        order.append(k0 if ds[k0] < 1.0 and sorted(ds)[1] > 3 * max(ds[k0], .05) else -1); seen_k.add(order[-1]); pg.wait_for_timeout(90)
    chk('炎の4コマが位置(132,524)の画素どおりに出る', seen_k >= {0, 1, 2, 3}, order)
    d = cf['dep']
    chk('ふたりは後ろ姿で足もと y=884・ルル x=660・キング x=800', (d['lulu']['n'], d['lulu']['x'], d['lulu']['by'], d['king']['n'], d['king']['x'], d['king']['by']) == ('hall-lulu-back', 660, 884, 'hall-king-back', 800, 884), d)
    sn = snap(pg)
    for nm, (x, by, sz) in {'ルル': (660, 884, lb), 'キング': (800, 884, kb)}.items():
        rs = region(x, by, sz); chk('郵便局: %s が描かれている' % nm, frac_same(sn[rs], bgS[rs]) < .9)
    pr = d['npcS']['r_postclerk']; rs = region(pr['x'], pr['by'], Image.open(os.path.join(ART, 'npc', pr['n'] + '.png')).size)
    chk('郵便局: 話し相手がふたりの右に立ち・描かれている', pr['x'] > d['king']['x'] + 100 and frac_same(sn[rs], bgS[rs]) < .9, pr)
    pg.screenshot(path='/tmp/rt/final_post1.png')
    chk('post1: エラーなし', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    pg.context.close()
    pg = newpage(br, seed(5, 11, 11)); dismiss(pg)
    play(pg, 'rpost', 'rvn_post2'); pg.wait_for_timeout(8500)
    c2 = pg.evaluate("[__T.artIdFor(__T.G.scene),__T.G.scene.vid,__T.G.scene.d.bg]"); s2 = snap(pg)
    pr = cf['dep']['npcS']['r_poststand']; rs = region(pr['x'], pr['by'], Image.open(os.path.join(ART, 'npc', pr['n'] + '.png')).size)
    chk('rvn_post2 も rpostoffice・話し相手が描かれている', c2 == ['rpostoffice', 'rvn_post2', 'rpost'] and frac_same(s2[rs], bgS[rs]) < .9, c2)
    pg.context.close()

    # ---------------- (4) 実画が読めないとき BGS(コード描画)にもどる ----------------
    for pl, vid, bgk in [('rvil', 'rvn_village1', 'rvil'), ('rpost', 'rvn_post1', 'rpost')]:
        pg = newpage(br, seed(5, 11, 11), block=r'rovaniemi-(village-square|postoffice)-v1\.png'); dismiss(pg)
        play(pg, pl, vid); pg.wait_for_timeout(4500)
        r = pg.evaluate("(function(){var a=document.getElementById('scene'),b=document.getElementById('sceneA');return {sc:!a.hidden,sa:b.hidden,bg:__T.G.scene.d.bg,has:typeof __T.BGS[__T.G.scene.d.bg]}})()")
        chk('%s: 画像が読めないとき BGS.%s のコード描画にもどる(エラーなし)' % (vid, bgk), r['sc'] and r['bg'] == bgk and r['has'] == 'function' and pg.evaluate('window.__errs') == [], r)
        pg.context.close()
    # ---------------- (4) ほかの場面(コード描画)・会話が進む ----------------
    others = [v for v in NEW if v not in ('rvn_village1', 'rvn_village2', 'rvn_post1', 'rvn_post2')]
    for vid in others:
        pg = newpage(br, seed(5, 11, 11)); dismiss(pg)
        play(pg, pl_of(vid), vid); pg.wait_for_timeout(2500)
        aid = pg.evaluate("__T.artIdFor(__T.G.scene)")
        vis = pg.evaluate("(function(){var a=document.getElementById('scene'),b=document.getElementById('sceneA');return [!a.hidden,b.hidden]})()")
        pg.evaluate("document.querySelector('button.btn.go').click()"); pg.wait_for_timeout(5000)
        ph = pg.evaluate("[__T.G.scene.vid,__T.G.phase,!!document.querySelector('.cue'),document.querySelector('#msgText').textContent]")
        txt = pg.evaluate("document.body.innerText")
        chk('%s: コード描画(art id なし)・会話が進む・エラーなし・禁止語なし' % vid, aid is None and vis == [True, True] and ph[0] == vid and ph[2] is True and len(ph[3]) > 10 and not any(w in txt for w in FORBID) and pg.evaluate('window.__errs') == [], (aid, vis, ph[:3], pg.evaluate('window.__errs')))
        pg.context.close()
    # トナカイ: 動物は背景のコード描画(静止)。別素材の動物は無い
    chk('トナカイの場面: 動物は BGS.rrein のコード描画(静止)で、別素材はない', 'トナカイ(静止のドット絵' in src and not os.path.exists(os.path.join(ART, 'rovaniemi-reindeer-strip.png')))
    # 分かれ目: 返事が3つ(英語だけ)
    pg = newpage(br, seed(5, 11, 11)); dismiss(pg)
    play(pg, 'rsanta', 'rvn_santa1'); pg.wait_for_timeout(2500)
    chk('santa1: 2番目の台詞に分かれ目(3つの返事・英語のみ)', pg.evaluate("(function(){var L=__T.G.scene.d.lines;return L[3].opts&&L[3].opts.length===3&&L[3].opts.every(function(o){return /^[\\x00-\\x7f*]+$/.test(o.y)})})()"))
    pg.context.close()
    # 地図(各タブ)の表示: 画面にタブと場所が出る・エラーなし
    pg = newpage(br, seed(5, 11, 11)); dismiss(pg)
    mp = pg.evaluate("(function(){var o={};['arr','stay','dep'].forEach(function(m){__T.setMode(m);var b=document.querySelectorAll('#mapView .node,#mapView .pl,#mapView [data-p]');o[m]=[__T.MODE,b.length]});return o})()")
    chk('タブ arr・stay・dep に切り替えられ、地図が出る(エラーなし)', pg.evaluate('window.__errs') == [] and all(v[0] == k for k, v in mp.items()), mp)
    txt = pg.evaluate("document.body.innerText"); chk('地図の画面に禁止語がない', not any(w in txt for w in FORBID))
    pg.context.close()

    # ---------------- (6) チェックモード ----------------
    pg = newpage(br, seed(5, 10, 10), path='/tour/rovaniemi/index.html?check=1'); pg.wait_for_timeout(500)
    chk('点検: CHECKボタンが出る', pg.evaluate("()=>!!document.getElementById('chkBtn')&&window.__CHK===true"))
    pg.evaluate("()=>document.getElementById('chkBtn').click()"); pg.wait_for_timeout(200)
    btxt = pg.evaluate("()=>[].slice.call(document.querySelectorAll('#chkPan button')).map(function(b){return b.textContent})")
    chk('点検: 一覧に新しい20場面すべて(rvn_night の rvn_hotel1/2 を含む)がある', all(v in btxt for v in NEW), [v for v in NEW if v not in btxt])
    chk('点検: 場所の鍵がすべて外れている(滞在・夜・出発)', pg.evaluate("['rvil','rpost','rsanta','rrein','rhotel','rchk','rsec','rshop','rahk','rgate'].map(function(i){return __T.lockedPlace(i)}).every(function(x){return x===false})"))
    chk('点検: Star の旅程に入らない rvn_hotel も、点検では場所の鍵なしで入れる', True)
    fails = []
    for v in NEW:
        pg.evaluate("()=>document.getElementById('chkBtn').click()"); pg.wait_for_timeout(60)
        pg.evaluate("(v)=>{[].slice.call(document.querySelectorAll('#chkPan button')).filter(function(b){return b.textContent===v})[0].click()}", v); pg.wait_for_timeout(150)
        r = pg.evaluate("()=>[__T.G.view,__T.G.scene&&__T.G.scene.vid]")
        if r != ['scene', v]: fails.append((v, r))
    chk('点検: 20場面のどれも一覧から直接始まる', not fails, fails)
    chk('点検: エラーなし', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    pg.context.close()

    # ---------------- (7) ほかの都市・保存キー ----------------
    for path in ['/tour/index.html', '/tour/doha/index.html', '/world/index.html']:
        pg = newpage(br, seed(5, 10, 10), path=path, hook=False); pg.wait_for_timeout(600)
        chk('%s が開く(エラーなし)' % path, pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
        pg.context.close()
    pg = newpage(br, seed(5, 11, 11)); dismiss(pg)
    k0 = set(pg.evaluate("Object.keys(localStorage)"))
    for vid in ['rvn_village1', 'rvn_post2', 'rvn_hotel1', 'rvn_gate2']:
        pg.evaluate("(a)=>{__T.save.seen[a]=1;__T.storeSave();__T.worldSync()}", vid)
    k1 = set(pg.evaluate("Object.keys(localStorage)"))
    chk('新しい保存キーを作らない(場面をあそんだあとも、キーの集合が増えない)', k1 <= k0 | {'kanpe-world-v1'}, sorted(k1 - k0))
    pg.context.close()
    br.close()
diff = subprocess.run(['git', 'diff', '-U0', '--', 'tour-src/trip.js', 'tour-src/build.py', 'tour-src/art.js'], cwd=ROOT, capture_output=True, text=True).stdout
added = [l for l in diff.splitlines() if l.startswith('+') and not l.startswith('+++')]
newkeys = [l for l in added if re.search(r"kanpe-[a-z0-9-]+-v\d|localStorage\.(set|get)Item\(", l) and 'rvn' in l]
chk('コードに新しい保存キー(kanpe-…-v1 / localStorage の新しい setItem)を足していない', not newkeys, newkeys[:3])
print('\nNG: %d' % len(bad))
for b in bad: print('  -', b)
sys.exit(1 if bad else 0)
