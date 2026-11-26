# -*- coding: utf-8 -*-
"""タスク096(チューリッヒ10場面)の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_zurich096.py
到着4・街3・出発3の場面データ・台詞の決まり・背景と発車標の別素材・チェックモードで10場面を選べること・世界地図と旅の骨組みへのつなぎ。
マイク・実機の見え方・実機の音は確認できない。"""
import os, sys, re, json, threading, http.server, socketserver
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
bad = []
def chk(n, ok, v=''):
    print(('OK  ' if ok else 'NG  ') + n, v if v != '' else '')
    if not ok: bad.append(n)
ARR = ['zur_arr1', 'zur_locker1', 'zur_tram1', 'zur_info1']; CITY = ['zur_cafe1', 'zur_shop1', 'zur_hotel1']; DEP = ['zur_dep_board1', 'zur_dep_ticket1', 'zur_dep_train1']
ALL = ARR + CITY + DEP
SIZE = {'zurich-arrival-v1.png': (1536, 960), 'zurich-street-v1.png': (1536, 960), 'zurich-hotel-v1.png': (1536, 960), 'zurich-departure-v1.png': (1536, 960), 'zurich-board-fra-v1.png': (432, 44)}
for n, sz in SIZE.items():
    p = os.path.join(ROOT, 'tour/assets/art', n); chk('素材 %s がある・大きさ %s' % (n, sz), os.path.exists(p) and Image.open(p).size == sz, Image.open(p).size if os.path.exists(p) else '')
# 背景の粒(2px)が崩れていない: 4枚とも 2x2 のブロックが同色(同梱の確認と同じ指標)
for n in ['arrival', 'street', 'hotel', 'departure']:
    im = Image.open(os.path.join(ROOT, 'tour/assets/art/zurich-%s-v1.png' % n)).convert('RGB'); px = im.load(); okc = tot = 0
    for y in range(0, 960, 2):
        for x in range(0, 1536, 2):
            tot += 1; okc += px[x, y] == px[x + 1, y] == px[x, y + 1] == px[x + 1, y + 1]
    chk('背景 %s: 粒2px(2x2ブロックが同色)の割合' % n, okc / tot > .97, '%.4f' % (okc / tot))
zu = open(os.path.join(ROOT, 'tour/zurich/index.html'), encoding='utf-8').read()
BGMAP = {'zurarr1': 'arrival', 'zurlock': 'arrival', 'zurinfo': 'arrival', 'zurboard': 'arrival', 'zurtram': 'street', 'zurcafe': 'street', 'zurshop': 'street', 'zurhotel': 'hotel', 'zurticket': 'departure', 'zurtrain': 'departure'}
for k, n in BGMAP.items():
    m = re.search(r"ART\.%s=\{bg:'([^']+)'" % k, zu)
    chk('%s の背景は zurich-%s-v1.png' % (k, n), m is not None and m.group(1) == 'zurich-%s-v1.png' % n, m.group(1) if m else None)
def art(k): return re.search(r"ART\.%s=\{[^\n]*" % k, zu).group(0)
chk('発車標の別素材(still)は zur_dep_board1 の絵(zurboard)だけに重ねる・位置は Fernverkehr の最初の行(232,226)', 'k:\'still\',img:\'zurich-board-fra-v1.png\',x:232,y:226' in art('zurboard') and all('board-fra' not in art(k) for k in BGMAP if k != 'zurboard'))
# 発車標の別素材: 背景の発車標の青を土台に、行き先の行だけを描いた重ね絵(時刻の欄に文字を描いていない)
ov = Image.open(os.path.join(ROOT, 'tour/assets/art/zurich-board-fra-v1.png')).convert('RGB'); bgi = Image.open(os.path.join(ROOT, 'tour/assets/art/zurich-arrival-v1.png')).convert('RGB')
chk('発車標の別素材: 重ね先(232,226)の背景は発車標の青の中(はみ出さない)', all(bgi.getpixel((232 + dx, 226 + dy))[2] > 120 and bgi.getpixel((232 + dx, 226 + dy))[0] < 60 or bgi.getpixel((232 + dx, 226 + dy))[0] < 60 for dx in (0, 431) for dy in (0, 43)))
bright = [(x, y) for y in range(44) for x in range(432) if sum(ov.getpixel((x, y))) > 600]
chk('発車標の別素材: 明るい字の画素がある(行き先と番号)・右端(Hinweis欄 x>=380)には字がない=時刻などを出していない', len(bright) > 100 and not any(x >= 380 for x, y in bright), (len(bright), max(x for x, y in bright)))
import data
SC = {x['id']: x for x in data.D if x['id'] in ALL}
chk('場面は10本', sorted(SC) == sorted(ALL), len(SC))
chk('入国審査・出国審査・搭乗口の場面を作っていない(ID に immig/depimmig/gate が無い・zur_ は10本だけ)', len([x for x in data.D if x['id'].startswith('zur_')]) == 10 and not any(re.search('immig|gate|passport', i) for i in ALL))
txt = {}
for i, x in SC.items():
    ps = x['pairs']
    chk('%s: 5往復・flow2・conv・語5つ' % i, len(ps) == 5 and x.get('flow2') == 1 and x.get('conv') == 1 and len(x['words']) == 5)
    forks = [p for p in ps if p.get('opts')]
    chk('%s: 選択は場面に1回だけ・カード式(2択)' % i, len(forks) == 1 and forks[0].get('cards') == 1 and len(forks[0]['opts']) == 2, len(forks))
    t = []
    for p in ps:
        t += ([p['n']] + [q['y'] for q in p['opts']] + [q['rep'][0] for q in p['opts']]) if p.get('opts') else [p['n'], p['y']]
    txt[i] = ' '.join(t).replace('*', '')
T = ' '.join(txt.values())
chk('台詞に数字(0-9)・通貨記号・通貨名がない(運賃・ロッカー料金・値段・時刻・ホーム番号・トラム番号を出さない)', not re.search(r'[0-9€$¥]|franc|CHF|euro|dollar', T, re.I))
chk('four hours は切符の窓口(zur_dep_ticket1)だけ。直通・乗り換えなしを係員が教える', [k for k, v in txt.items() if 'four hours' in v] == ['zur_dep_ticket1'] and 'direct train' in txt['zur_dep_ticket1'] and 'No. It is a direct' in txt['zur_dep_ticket1'] and 'straight to Frankfurt' in txt['zur_dep_train1'])
chk('乗り換えありとして描いていない(change trains を聞くだけで、乗り換え駅・乗り換え時間が無い)', not re.search(r'transfer|change at|connection|switch', T, re.I))
chk('店名・ホテル名・個人名を出していない(Migros/Coop/Hotel名/Dolder など)', not re.search(r'Migros|Coop|Sprüngli|Sprungli|Läderach|Laderach|Dolder|Marriott|Baur|Hilton', T))
chk('発車標: 長距離列車は赤い側・Gleis の欄でホームを読む(番号は言わない)', 'red side' in txt['zur_dep_board1'] and 'Gleis' in txt['zur_dep_board1'])
chk('入国審査の台詞が無い(passport は ホテルの記入だけ。control/immigration/visa が無い)', not re.search(r'passport control|immigration|visa|customs', T, re.I) and 'passport' in txt['zur_hotel1'])
chk('車掌への切符(zur_dep_train1): となりの乗客→車掌に話し手が替わる(cx が2本)', sum(1 for p in SC['zur_dep_train1']['pairs'] if p.get('cx', {}).get('sp') == 'z_conductor') == 2)
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def log_message(s, *a): pass
srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); base = 'http://127.0.0.1:%d' % srv.server_address[1]
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); b = r.text(); assert HOOK in b
    route.fulfill(response=r, body=b.replace(HOOK, "window.__T={G:G,PBY:PBY,startVid:startVid,ART:ART,ARTFAIL:ARTFAIL,artIdFor:artIdFor,MODES:MODES,SP:SP,DLG:DLG};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});window.__say=[];"
        "try{speechSynthesis.speak=function(u){window.__say.push(u.text);setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));")
SHOT = os.environ.get('ZUR_SHOT')   # 画面の保存先(確認用)。指定したときだけ撮る
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--no-sandbox'])
    for v in ALL:
        ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
        pg = ctx.new_page(); pg.route(re.compile(r'/tour/zurich/index\.html(\?.*)?$'), hooked)
        pg.goto(base + '/tour/zurich/index.html?check=1'); pg.wait_for_timeout(1000)
        r = pg.evaluate("(v)=>{var T=window.__T,pl=null;Object.keys(T.PBY).forEach(function(k){if((T.PBY[k].v||[]).indexOf(v)>=0)pl=T.PBY[k]});if(!pl)return null;T.startVid(pl,v,'ev');return pl.id}", v)
        pg.wait_for_timeout(1800)
        i = pg.evaluate("(function(){var T=window.__T;return {art:T.artIdFor(T.G.scene),fail:Object.keys(T.ARTFAIL),vid:T.G.scene&&T.G.scene.vid,sp:T.G.scene&&T.G.scene.d&&T.G.scene.d.sp,known:!!(T.G.scene&&T.G.scene.d&&T.SP[T.G.scene.d.sp])}})()")
        chk('%s: チェックモードから入れる・実画あり・読み込み失敗なし・エラーなし・話者の声が定義済み' % v, r and i['vid'] == v and i['art'] and not i['fail'] and pg.evaluate('window.__errs') == [] and i['known'], (r, i))
        if SHOT: pg.screenshot(path=os.path.join(SHOT, v + '.png'))
        ctx.close()
    # 話者の切り替え(zur_dep_train1): 乗客 → 車掌 の声と絵が出る
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
    pg = ctx.new_page(); pg.route(re.compile(r'/tour/zurich/index\.html(\?.*)?$'), hooked); pg.goto(base + '/tour/zurich/index.html?check=1'); pg.wait_for_timeout(1000)
    ids = pg.evaluate("(function(){var o=[];var M=window.__T.MODES;Object.keys(M).forEach(function(k){M[k].p.forEach(function(p){(p.v||[]).forEach(function(v){o.push(v)})})});return o})()")
    chk('チェックモード: MODES の場所に10場面すべてがある(到着4・街3・出発3)', sorted(set(ids)) == sorted(ALL) and len(ids) == 10, ids)
    nm = pg.evaluate("(function(){var M=window.__T.MODES;return Object.keys(M).map(function(k){return k+':'+M[k].p.length})})()")
    chk('チェックモード: タブは 到着4・街3・出発3 の場所', sorted(nm) == ['arr:4', 'city:3', 'dep:3'], nm)
    ctx.close()
    for path in ['/tour/index.html', '/tour/athens/index.html', '/tour/zurich/index.html']:
        ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT); pg = ctx.new_page(); pg.goto(base + path); pg.wait_for_timeout(900)
        chk('%s: エラーなし' % path, pg.evaluate('window.__errs') == [])
        ctx.close()
    br.close()
wd = open(os.path.join(ROOT, 'world/index.html'), encoding='utf-8').read()
chk('世界地図: チューリッヒの点(url ../tour/zurich/)がある・既存のアテネ(ロヴァニエミからの道)は変えていない', "zurich:{n:'チューリッヒ'" in wd and "url:'../tour/zurich/'" in wd and "rovaniemi:['doha','athens']" in wd and "athens:['rovaniemi']" in wd)
chk('世界地図: ローマ(094)が無い間は zurich:[] (ローマの後ろにつなぐ2行は094のマージ時)', "zurich:[]" in wd)
tj = open(os.path.join(ROOT, 'tour-src/trip.js'), encoding='utf-8').read()
chk('旅の骨組み: ZRH を空港に・IMPL に入れた', "ZRH:{id:'zurich'" in tj and re.search(r"var IMPL=\{[^}]*ZRH:1", tj) is not None)
chk('旅の骨組み: まとまり zur_arr/zur_city/zur_dep が10場面すべて', all("'%s'" % v in tj for v in ALL) and "zur_arr:[['zur_arr1'],['zur_locker1'],['zur_tram1'],['zur_info1']]" in tj)
chk('旅の骨組み: 場所10か所が PLACEGRP・THEME・HOUR に入っている', all(re.search(r'\b%s:' % p, tj) for p in ['zarr', 'zlock', 'ztram', 'zinfo', 'zcafe', 'zshop', 'zhotel', 'zboard', 'zticket', 'ztrain']) and tj.count('zboard:') >= 3)
chk('旅の骨組み: MODEGRP の arr/dep/city に zurich', "zurich:'zur_arr'" in tj and "zurich:'zur_dep'" in tj and "zurich:'zur_city'" in tj)
chk('旅の骨組み: LEGS/ROWS は変えていない(アテネ・ローマの便は PM確認待ち)', 'ZRH' not in re.search(r"var LEGS=\{.*?\n var ROWS", tj, re.S).group(0))
chk('チェックモード: アテネのページからチューリッヒへ・チューリッヒのページからアテネへ', "zurich/?check=1" in open(os.path.join(ROOT, 'tour/athens/index.html'), encoding='utf-8').read() and "athens/?check=1" in zu)
chk('トラム・カフェ・おみやげ・ホテルの環境音の対応(AMBBG)と snd zur', "ztram:'outdoor'" in zu and "zur:'airport'" in zu and "snd:'zur'" in zu)
print('\nNG %d件' % len(bad) if bad else '\n全部OK'); sys.exit(1 if bad else 0)
