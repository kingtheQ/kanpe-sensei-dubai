# -*- coding: utf-8 -*-
"""タスク101(ホノルル10場面)の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_honolulu101.py
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
ARR = ['hnl_form1','hnl_bag1','hnl_lei1','hnl_trolley1']; CITY = ['hnl_cafe1','hnl_shop1','hnl_hotel1']; DEP = ['hnl_dep_board1','hnl_dep_ticket1','hnl_dep_gate1']
ALL = ARR + CITY + DEP
A = os.path.join(ROOT, 'tour/assets/art')
for n in ['arrival','street','hotel','departure']:
    p = os.path.join(A, 'honolulu-%s-v1.png' % n); chk('背景 %s は 1536x960' % n, os.path.exists(p) and Image.open(p).size == (1536, 960))
bs = Image.open(os.path.join(A, 'honolulu-board-rows-strip.png')); chk('案内板の重ね素材は 916x254(2コマ)', bs.size == (916, 254), bs.size)
hn = open(os.path.join(ROOT, 'tour/honolulu/index.html'), encoding='utf-8').read()
BG = {'honform':'arrival','honbag':'arrival','honlei':'arrival','hontrolley':'arrival','honcafe':'street','honshop':'street','honhotel':'hotel','honboard':'departure','honticket':'departure','hongate':'departure'}
for k, n in BG.items():
    m = re.search(r"ART\.%s=\{bg:'([^']+)'" % k, hn); chk('%s の背景は honolulu-%s-v1.png' % (k, n), m and m.group(1) == 'honolulu-%s-v1.png' % n)
chk('案内板の重ねは honboard の strips にある', 'honolulu-board-rows-strip.png' in re.search(r"ART\.honboard=\{[^\n]*", hn).group(0))
import data
SC = {x['id']: x for x in data.D if x['id'] in ALL}
chk('場面は10本', sorted(SC) == sorted(ALL), len(SC))
txt = {}
for i, x in SC.items():
    ps = x['pairs']
    chk('%s: 5往復・flow2・conv・語5つ' % i, len(ps) == 5 and x.get('flow2') == 1 and x.get('conv') == 1 and len(x['words']) == 5)
    forks = [p for p in ps if p.get('opts')]
    chk('%s: 選択は1回・カード式・2択' % i, len(forks) == 1 and forks[0].get('cards') == 1 and len(forks[0]['opts']) == 2, len(forks))
    t = []
    for p in ps:
        t += ([p['n']] + [q['y'] for q in p['opts']] + [q['rep'][0] for q in p['opts']]) if p.get('opts') else [p['n'], p['y']]
    txt[i] = ' '.join(t).replace('*', '')
T = ' '.join(txt.values()).lower()
chk('台詞に数字・記号($・%)がない', not re.search(r'[0-9$%€]', T))
chk('入国審査・税関の場面も語もない(国内線の到着)', not re.search(r'immigration|border|customs|visa', T))
chk('シドニー行きの航空会社名・便名・ターミナル名がない', not re.search(r'qantas|delta|hawaiian|united|jetstar|flight number|terminal|airlines', T))
chk('申告書の正式名称を台詞に出さない(this form で通す)', 'declaration' not in T and 'this form' in txt['hnl_form1'].lower())
chk('チップ・運賃・値段の割合や金額語がない', not re.search(r'tip|fare|dollar|cheap|expensive|percent', T))
chk('出発3場面は Sydney / Australia を扱う', 'sydney' in txt['hnl_dep_board1'].lower() and 'sydney' in txt['hnl_dep_ticket1'].lower() and 'australia' in txt['hnl_dep_ticket1'].lower())
chk('ワイキキ・トロリーは空港に行かないと言う(trolley1)', 'does not go to the airport' in txt['hnl_trolley1'].lower())
chk('スカイラインは空港に停まるがワイキキにはまだ(trolley1)', 'skyline' in txt['hnl_trolley1'].lower() and 'does not reach waikiki yet' in txt['hnl_trolley1'].lower())
chk('各場面に Aloha / Mahalo / No worries / No rush / Take your time のどれかがある(のんびり・明るい)', all(re.search(r'aloha|mahalo|no worries|no rush|take your time|enjoy', txt[i].lower()) for i in ALL))
chk('到着4場面は Aloha で始まる', all(SC[i]['pairs'][0]['n'].startswith('Aloha') for i in ARR))
chk('店名・ホテル名が台詞にない(先例どおり省く)', not re.search(r'hilton|hyatt|sheraton|marriott|matsumoto|ono|rainbow drive|duty free', T))
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
URL = re.compile(r'/tour/honolulu/index\.html(\?.*)?$')
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--no-sandbox'])
    for v in ALL:
        ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
        pg = ctx.new_page(); pg.route(URL, hooked)
        pg.goto(base + '/tour/honolulu/index.html?check=1'); pg.wait_for_timeout(1000)
        r = pg.evaluate("(v)=>{var T=window.__T,pl=null;Object.keys(T.PBY).forEach(function(k){if((T.PBY[k].v||[]).indexOf(v)>=0)pl=T.PBY[k]});if(!pl)return null;T.startVid(pl,v,'ev');return pl.id}", v)
        pg.wait_for_timeout(1800)
        i = pg.evaluate("(function(){var T=window.__T;return {art:T.artIdFor(T.G.scene),fail:Object.keys(T.ARTFAIL),vid:T.G.scene&&T.G.scene.vid}})()")
        chk('%s: チェックモードから入れる・実画あり・読み込み失敗なし・エラーなし' % v, r and i['vid'] == v and i['art'] and not i['fail'] and pg.evaluate('window.__errs') == [], (r, i))
        ctx.close()
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
    pg = ctx.new_page(); pg.route(URL, hooked); pg.goto(base + '/tour/honolulu/index.html?check=1'); pg.wait_for_timeout(1000)
    ids = pg.evaluate("(function(){var o=[];var M=window.__T.MODES;Object.keys(M).forEach(function(k){M[k].p.forEach(function(p){(p.v||[]).forEach(function(v){o.push(v)})})});return o})()")
    chk('MODES の場所に10場面すべてがある', sorted(set(ids)) == sorted(ALL), ids)
    cnt = pg.evaluate("(function(){var M=window.__T.MODES,o={};Object.keys(M).forEach(function(k){var s={};M[k].p.forEach(function(p){(p.v||[]).forEach(function(v){s[v]=1})});o[k]=Object.keys(s).length});return o})()")
    chk('モードごとの場面数 到着4・街3・出発3', sorted(cnt.values()) == [3, 3, 4], cnt)
    ctx.close()
    for path in ['/tour/index.html', '/tour/frankfurt/index.html', '/tour/honolulu/index.html', '/world/index.html']:
        ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT); pg = ctx.new_page(); pg.goto(base + path); pg.wait_for_timeout(900)
        chk('%s: エラーなし' % path, pg.evaluate('window.__errs') == [])
        ctx.close()
    br.close()
wd = open(os.path.join(ROOT, 'world/index.html'), encoding='utf-8').read()
chk('世界地図: ホノルルの点がある', "honolulu:{n:'ホノルル'" in wd and "../tour/honolulu/" in wd)
tj = open(os.path.join(ROOT, 'tour-src/trip.js'), encoding='utf-8').read()
chk('旅の表: IMPL.HNL・hnl_arr/hnl_city/hnl_dep', all(s in tj for s in ['HNL:1', 'hnl_arr', 'hnl_city', 'hnl_dep']))
chk('チェックモード: フランクフルトからホノルルへのリンク', 'honolulu/?check=1' in open(os.path.join(ROOT, 'tour/frankfurt/index.html'), encoding='utf-8').read())
chk('チェックモード: ホノルルからフランクフルトへのリンク', 'frankfurt/?check=1' in hn)
print('\nNG %d件' % len(bad) if bad else '\n全部OK'); sys.exit(1 if bad else 0)
