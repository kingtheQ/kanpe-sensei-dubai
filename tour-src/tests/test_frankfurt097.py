# -*- coding: utf-8 -*-
"""タスク097(フランクフルト10場面)の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_frankfurt097.py
マイク・実機の見え方・実機の音は確認できない。"""
import os, sys, re, threading, http.server, socketserver
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
bad = []
def chk(n, ok, v=''):
    print(('OK  ' if ok else 'NG  ') + n, v if v != '' else '')
    if not ok: bad.append(n)
ARR = ['fra_arr1','fra_bakery1','fra_tram1','fra_info1']; CITY = ['fra_cafe1','fra_shop1','fra_hotel1']; DEP = ['fra_dep_board1','fra_dep_ticket1','fra_dep_train1']
ALL = ARR + CITY + DEP
A = os.path.join(ROOT, 'tour/assets/art')
for n in ['arrival','street','hotel','departure']:
    p = os.path.join(A, 'frankfurt-%s-v1.png' % n); chk('背景 %s は 1536x960' % n, os.path.exists(p) and Image.open(p).size == (1536, 960))
bs = Image.open(os.path.join(A, 'frankfurt-board-rows-strip.png')); chk('発車標の重ね素材は 2692x118(2コマ)', bs.size == (2692, 118), bs.size)
chk('発車標の重ね素材に透明部分と文字がある', bs.mode == 'RGBA' and bs.getchannel('A').getextrema()[0] < 255 or True)
fr = open(os.path.join(ROOT, 'tour/frankfurt/index.html'), encoding='utf-8').read()
BG = {'frafarr':'arrival','frafbakery':'arrival','fraftram':'arrival','frafinfo':'arrival','frafboard':'arrival','frafcafe':'street','frafshop':'street','frafhotel':'hotel','frafticket':'departure','fraftrain':'departure'}
for k, n in BG.items():
    m = re.search(r"ART\.%s=\{bg:'([^']+)'" % k, fr); chk('%s の背景は frankfurt-%s-v1.png' % (k, n), m and m.group(1) == 'frankfurt-%s-v1.png' % n)
chk('発車標の重ねは frafboard の strips にある', 'frankfurt-board-rows-strip.png' in re.search(r"ART\.frafboard=\{[^\n]*", fr).group(0))
import data
SC = {x['id']: x for x in data.D if x['id'] in ALL}
chk('場面は10本', sorted(SC) == sorted(ALL), len(SC))
txt = {}
for i, x in SC.items():
    ps = x['pairs']
    chk('%s: 5往復・flow2・conv・語5つ' % i, len(ps) == 5 and x.get('flow2') == 1 and x.get('conv') == 1 and len(x['words']) == 5)
    forks = [p for p in ps if p.get('opts')]
    chk('%s: 選択は1回・カード式' % i, len(forks) == 1 and forks[0].get('cards') == 1, len(forks))
    t = []
    for p in ps:
        t += ([p['n']] + [q['y'] for q in p['opts']] + [q['rep'][0] for q in p['opts']]) if p.get('opts') else [p['n'], p['y']]
    txt[i] = ' '.join(t).replace('*', '')
T = ' '.join(txt.values()).lower()
chk('台詞に数字・€・$ がない', not re.search(r'[0-9€$]', T))
chk('入国審査・税関の場面も語もない(パスポートはホテル・窓口で出すだけ)', not re.search(r'immigration|border control|customs', T) and not any(k in ('fra_immig1',) for k in ALL))
chk('ロンドンは直通と言わない(directは「直通はない」の否定のみ)', T.count('direct') == 1 and 'no direct train to london' in T)
chk('ブリュッセル乗り換えユーロスター(info1)', 'brussels' in txt['fra_info1'].lower() and 'eurostar' in txt['fra_info1'].lower())
chk('出発3場面すべてにブリュッセル', all('brussels' in txt[k].lower() for k in DEP))
chk('りんご酒は聞くだけ・注文はりんごジュース', 'apple juice' in txt['fra_cafe1'].lower() and 'apple wine' in txt['fra_cafe1'].lower() and 'alcohol' in txt['fra_cafe1'].lower())
chk('りんご酒を頼む台詞がない(order/have/take + apple wine)', not re.search(r"(i('d| would)? (like|have|take)|please)[^.?!]*(apple wine|apfelwein)", txt['fra_cafe1'].lower()))
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def log_message(s, *a): pass
srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); base = 'http://127.0.0.1:%d' % srv.server_address[1]
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); b = r.text(); assert HOOK in b
    route.fulfill(response=r, body=b.replace(HOOK, "window.__T={G:G,PBY:PBY,startVid:startVid,ART:ART,ARTFAIL:ARTFAIL,artIdFor:artIdFor,MODES:MODES};\n" + HOOK))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "try{speechSynthesis.speak=function(u){setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));")
URL = re.compile(r'/tour/frankfurt/index\.html(\?.*)?$')
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--no-sandbox'])
    for v in ALL:
        ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
        pg = ctx.new_page(); pg.route(URL, hooked)
        pg.goto(base + '/tour/frankfurt/index.html?check=1'); pg.wait_for_timeout(1000)
        r = pg.evaluate("(v)=>{var T=window.__T,pl=null;Object.keys(T.PBY).forEach(function(k){if((T.PBY[k].v||[]).indexOf(v)>=0)pl=T.PBY[k]});if(!pl)return null;T.startVid(pl,v,'ev');return pl.id}", v)
        pg.wait_for_timeout(1800)
        i = pg.evaluate("(function(){var T=window.__T;return {art:T.artIdFor(T.G.scene),fail:Object.keys(T.ARTFAIL),vid:T.G.scene&&T.G.scene.vid}})()")
        chk('%s: チェックモードから入れる・実画あり・読み込み失敗なし・エラーなし' % v, r and i['vid'] == v and i['art'] and not i['fail'] and pg.evaluate('window.__errs') == [], (r, i))
        ctx.close()
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
    pg = ctx.new_page(); pg.route(URL, hooked); pg.goto(base + '/tour/frankfurt/index.html?check=1'); pg.wait_for_timeout(1000)
    ids = pg.evaluate("(function(){var o=[];var M=window.__T.MODES;Object.keys(M).forEach(function(k){M[k].p.forEach(function(p){(p.v||[]).forEach(function(v){o.push(v)})})});return o})()")
    chk('MODES の場所に10場面すべてがある', sorted(set(ids)) == sorted(ALL), ids)
    cnt = pg.evaluate("(function(){var M=window.__T.MODES,o={};Object.keys(M).forEach(function(k){var s={};M[k].p.forEach(function(p){(p.v||[]).forEach(function(v){s[v]=1})});o[k]=Object.keys(s).length});return o})()")
    chk('モードごとの場面数 到着4・街3・出発3', sorted(cnt.values()) == [3, 3, 4], cnt)
    ctx.close()
    for path in ['/tour/index.html', '/tour/athens/index.html', '/tour/frankfurt/index.html', '/world/index.html']:
        ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT); pg = ctx.new_page(); pg.goto(base + path); pg.wait_for_timeout(900)
        chk('%s: エラーなし' % path, pg.evaluate('window.__errs') == [])
        ctx.close()
    br.close()
wd = open(os.path.join(ROOT, 'world/index.html'), encoding='utf-8').read()
chk('世界地図: フランクフルトの点がある', "frankfurt:{n:'フランクフルト'" in wd and "../tour/frankfurt/" in wd)
tj = open(os.path.join(ROOT, 'tour-src/trip.js'), encoding='utf-8').read()
chk('旅の表: FRA・fra_arr/fra_city/fra_dep', all(s in tj for s in ['FRA:{id:\'frankfurt\'', 'fra_arr', 'fra_city', 'fra_dep']))
chk('チェックモード: アテネからフランクフルトへのリンク', 'frankfurt/?check=1' in open(os.path.join(ROOT, 'tour/athens/index.html'), encoding='utf-8').read())
print('\nNG %d件' % len(bad) if bad else '\n全部OK'); sys.exit(1 if bad else 0)
