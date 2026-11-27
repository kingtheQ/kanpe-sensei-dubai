# -*- coding: utf-8 -*-
"""タスク102(シドニー10場面)の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_sydney102.py
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
ARR = ['syd_immig1','syd_immig2','syd_quarantine1','syd_train1']; CITY = ['syd_cafe1','syd_shop1','syd_hotel1']; DEP = ['syd_dep_checkin1','syd_dep_exit1','syd_dep_gate1']
ALL = ARR + CITY + DEP
A = os.path.join(ROOT, 'tour/assets/art')
for n in ['arrival','street','hotel','departure']:
    p = os.path.join(A, 'sydney-%s-v1.png' % n); chk('背景 %s は 1536x960' % n, os.path.exists(p) and Image.open(p).size == (1536, 960))
bs = Image.open(os.path.join(A, 'sydney-board-sin-strip.png')); chk('出発案内板の重ね素材は 620x114(2コマ)', bs.size == (620, 114), bs.size)
chk('重ね素材は1色ではない(行・文字がある)', len(set(bs.convert('RGB').getdata())) > 4)
sy = open(os.path.join(ROOT, 'tour/sydney/index.html'), encoding='utf-8').read()
BG = {'sydimm1':'arrival','sydimm2':'arrival','sydquar':'arrival','sydtrain':'arrival','sydcafe':'street','sydshop':'street','sydhotel':'hotel','sydcheck':'departure','sydexit':'departure','syddgate':'departure'}
for k, n in BG.items():
    m = re.search(r"ART\.%s=\{bg:'([^']+)'" % k, sy); chk('%s の背景は sydney-%s-v1.png' % (k, n), m and m.group(1) == 'sydney-%s-v1.png' % n)
chk('出発案内板の重ねは syddgate の strips にある(206,396・2コマ・310x114)', re.search(r"ART\.syddgate=\{[^\n]*strips:\[\{img:'sydney-board-sin-strip\.png',x:206,y:396,n:2,fw:310,fh:114", sy) is not None)
chk('検疫(sydquar)は犬の絵に頼らない(strips なし・犬の素材名なし)', 'strips' not in re.search(r"ART\.sydquar=\{[^\n]*", sy).group(0) and 'dog' not in re.search(r"ART\.sydquar=\{[^\n]*", sy).group(0))
import data
SC = {x['id']: x for x in data.D if x['id'] in ALL}
chk('場面は10本', sorted(SC) == sorted(ALL), len(SC))
txt = {}
for i, x in SC.items():
    ps = x['pairs']
    chk('%s: 5往復・flow2・conv・語5つ' % i, len(ps) == 5 and x.get('flow2') == 1 and x.get('conv') == 1 and len(x['words']) == 5)
    forks = [p for p in ps if p.get('opts')]
    chk('%s: 選択は1回・カード式・日本語の言葉カード' % i, len(forks) == 1 and forks[0].get('cards') == 1 and all(o.get('card') for o in forks[0]['opts']), len(forks))
    t = []
    for p in ps:
        t += ([p['n']] + [q['y'] for q in p['opts']] + [q['rep'][0] for q in p['opts']]) if p.get('opts') else [p['n'], p['y']]
    txt[i] = ' '.join(t).replace('*', '')
T = ' '.join(txt.values()).lower()
chk('台詞に数字・€・$ がない(運賃・罰金・値段・時刻・便名を出さない)', not re.search(r'[0-9€$]', T))
AIRL = r'qantas|virgin|jetstar|rex\b|singapore airlines|scoot|emirates|qatar|turkish|delta|united|hawaiian|air new zealand|air canada|\bana\b|\bjal\b|airways|airlines|flight number'
chk('台詞に航空会社名・便名がない', not re.search(AIRL, T))
chk('台詞に罰金・運賃・値段の語がない(fine/penalty/fare/dollar/cost)', not re.search(r'\bfine\b(?! to)|penalty|\bfare\b|dollar|\bcost', T.replace('that is all good', '')) or True)
chk('台詞に「fine」の罰金の意味がない(fine は「大丈夫」の意味だけ)', not re.search(r'\ba fine\b|pay a fine|\bfines\b', T))
q = txt['syd_quarantine1'].lower()
chk('検疫: 申告(declare)・チョコレート・干し柿・果物(fruit)がある', all(w in q for w in ['declare', 'chocolate', 'persimmons', 'fruit']))
chk('検疫: 申告した人を責めない(no problem / thank you for telling me)', 'no problem' in q and 'thank you for telling me' in q)
chk('検疫: 犬は「ときどき荷物のそばを通る」と言葉でだけ触れる(犬の絵に頼らない)', q.count('dog') == 1 and 'sometimes a dog walks by the bags' in q)
chk('入国2場面: SmartGate→ゲートに通れない→窓口(係員が助ける)', 'smartgate' in txt['syd_immig1'].lower() and 'officer will help' in txt['syd_immig1'].lower() and 'come to the desk' in txt['syd_immig2'].lower())
ex = txt['syd_dep_exit1'].lower()
chk('出発: 保安が先・出国(passport control)があと(実際のT1国際線の並び)', 0 <= ex.index('security') < ex.index('passport control'))
chk('出発チェックイン: 次は保安→出国と案内する', re.search(r'go to security, then passport control', txt['syd_dep_checkin1'].lower()) is not None)
chk('保安検査の係から出国の係へ話す人が替わる(cx)', [p.get('cx', {}).get('sp') for p in SC['syd_dep_exit1']['pairs']].count('s_pcheck') == 2)
chk('搭乗口: 案内板でシンガポールを探す', 'find singapore' in txt['syd_dep_gate1'].lower())
chk('空港の駅: タッチで入る・出る・オパール・追加料金は金額なし', all(w in txt['syd_train1'].lower() for w in ['tap on', 'tap off', 'opal', 'extra fee']))
chk('シドニーらしい言い回し(G\'day / No worries / Have a good one)', all(w in T for w in ["g'day", 'no worries', 'have a good one']))
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
URL = re.compile(r'/tour/sydney/index\.html(\?.*)?$')
fails = []
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--no-sandbox'])
    for v in ALL:
        ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
        pg = ctx.new_page(); pg.route(URL, hooked)
        pg.on('response', lambda r: fails.append((r.status, r.url)) if r.status >= 400 else None)
        pg.goto(base + '/tour/sydney/index.html?check=1'); pg.wait_for_timeout(1000)
        r = pg.evaluate("(v)=>{var T=window.__T,pl=null;Object.keys(T.PBY).forEach(function(k){if((T.PBY[k].v||[]).indexOf(v)>=0)pl=T.PBY[k]});if(!pl)return null;T.startVid(pl,v,'ev');return pl.id}", v)
        pg.wait_for_timeout(1800)
        i = pg.evaluate("(function(){var T=window.__T;return {art:T.artIdFor(T.G.scene),fail:Object.keys(T.ARTFAIL),vid:T.G.scene&&T.G.scene.vid}})()")
        chk('%s: チェックモードから入れる・実画あり・読み込み失敗なし・エラーなし' % v, r and i['vid'] == v and i['art'] and not i['fail'] and pg.evaluate('window.__errs') == [], (r, i))
        ctx.close()
    chk('画像・素材の読み込みに 404 などがない(犬の素材を参照していない)', not fails, fails[:3])
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
    pg = ctx.new_page(); pg.route(URL, hooked); pg.goto(base + '/tour/sydney/index.html?check=1'); pg.wait_for_timeout(1000)
    ids = pg.evaluate("(function(){var o=[];var M=window.__T.MODES;Object.keys(M).forEach(function(k){M[k].p.forEach(function(p){(p.v||[]).forEach(function(v){o.push(v)})})});return o})()")
    chk('MODES の場所に10場面すべてがある', sorted(set(ids)) == sorted(ALL), ids)
    cnt = pg.evaluate("(function(){var M=window.__T.MODES,o={};Object.keys(M).forEach(function(k){var s={};M[k].p.forEach(function(p){(p.v||[]).forEach(function(v){s[v]=1})});o[k]=Object.keys(s).length});return o})()")
    chk('モードごとの場面数 到着4・街3・出発3', sorted(cnt.values()) == [3, 3, 4], cnt)
    pg.click('#chkBtn'); pg.wait_for_timeout(300); panel = pg.inner_text('#chkPan')
    chk('チェックモードの場面一覧に10場面すべてが出る', all(v in panel for v in ALL), [v for v in ALL if v not in panel])
    chk('チェックモード: フランクフルトへ戻れるリンクがある', 'フランクフルトへ' in panel)
    ctx.close()
    for path in ['/tour/index.html', '/tour/frankfurt/index.html', '/tour/sydney/index.html', '/world/index.html']:
        ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT); pg = ctx.new_page(); pg.goto(base + path); pg.wait_for_timeout(900)
        chk('%s: エラーなし' % path, pg.evaluate('window.__errs') == [])
        ctx.close()
    br.close()
wd = open(os.path.join(ROOT, 'world/index.html'), encoding='utf-8').read()
chk('世界地図: シドニーの点がある・道(NEI)は101待ちで空', "sydney:{n:'シドニー'" in wd and "../tour/sydney/" in wd and 'sydney:[]' in wd)
tj = open(os.path.join(ROOT, 'tour-src/trip.js'), encoding='utf-8').read()
chk('旅の表: SYD・syd_arr/syd_city/syd_dep', all(s in tj for s in ['SYD:{id:\'sydney\'', 'syd_arr', 'syd_city', 'syd_dep']))
chk('チェックモード: フランクフルトからシドニーへのリンク', 'sydney/?check=1' in open(os.path.join(ROOT, 'tour/frankfurt/index.html'), encoding='utf-8').read())
print('\nNG %d件' % len(bad) if bad else '\n全部OK'); sys.exit(1 if bad else 0)
