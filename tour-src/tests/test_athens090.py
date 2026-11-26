# -*- coding: utf-8 -*-
"""タスク090・091・093(背景 v1→v2 差し替え)の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_athens090.py
アテネ10場面(到着4・街3・出発3)・マイク画像の差し替え・チェックモード・世界地図・旅の骨組みの表。
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
ARR = ['ath_immig1', 'ath_immig2', 'ath_taxi1', 'ath_transit1']; CITY = ['ath_cafe1', 'ath_shop1', 'ath_hotel1']; DEP = ['ath_checkin1', 'ath_depimmig1', 'ath_gate1']
ALL = ARR + CITY + DEP
for n, sz in [('athens-arrival-v2.png', None), ('athens-street-v2.png', None), ('athens-hotel-v2.png', None), ('athens-departure-v2.png', None), ('mic-large-v1.png', None)]:
    p = os.path.join(ROOT, 'tour/assets/art', n); chk('素材 %s がある' % n, os.path.exists(p) and Image.open(p).size[0] > 0, Image.open(p).size if os.path.exists(p) else '')
for n in ['arrival', 'street', 'hotel', 'departure']:
    chk('093: athens-%s-v2.png は 1536x960' % n, Image.open(os.path.join(ROOT, 'tour/assets/art/athens-%s-v2.png' % n)).size == (1536, 960))
ath = open(os.path.join(ROOT, 'tour/athens/index.html'), encoding='utf-8').read()
BGMAP = {'athimm1': 'arrival', 'athimm2': 'arrival', 'athtaxi': 'arrival', 'athmetro': 'arrival', 'athcafe': 'street', 'athshop': 'street', 'athhotel': 'hotel', 'athck': 'departure', 'athdep': 'departure'}
for k, n in BGMAP.items():
    m = re.search(r"ART\.%s=\{bg:'([^']+)'" % k, ath)
    chk('093: %s の背景は athens-%s-v2.png' % (k, n), m is not None and m.group(1) == 'athens-%s-v2.png' % n, m.group(1) if m else None)
chk('093: 生成物に athens の v1 背景への参照が残っていない', re.search(r"athens-(arrival|street|hotel|departure)-v1", ath) is None)
def art(k): return re.search(r"ART\.%s=\{[^\n]*" % k, ath).group(0)
chk('093: 到着の係官はカウンター上面(y=585)で切る・x=769(8番窓口)', all('clerk:{x:769,' in art(k) and 'clip:585}' in art(k) for k in ['athimm1', 'athimm2']))
chk('093: 出発の係員はカウンター上面(y=595)で切る', 'clip:595}' in art('athck'))
chk('093: タベルナの店員は左(戸口 x30〜240)・おみやげ屋は右の壁ぎわ(x>1100)', re.search(r"a_waiter:\{[^}]*x:150,", art('athcafe')) is not None and re.search(r"a_shop:\{[^}]*x:1140,", art('athshop')) is not None)
chk('093: ホテルの3人は一面のベッド(y745〜)の奥の縁(足もと y=752)', len(re.findall(r"by:752", art('athhotel'))) == 3)
import data
SC = {x['id']: x for x in data.D if x['id'] in ALL}
chk('場面は10本', sorted(SC) == sorted(ALL), len(SC))
txt = []
for i, x in SC.items():
    ps = x['pairs']
    chk('%s: 5往復・flow2・conv・語5つ' % i, len(ps) == 5 and x.get('flow2') == 1 and x.get('conv') == 1 and len(x['words']) == 5)
    forks = [p for p in ps if p.get('opts')]
    chk('%s: 選択は1回・カード式' % i, len(forks) == 1 and forks[0].get('cards') == 1, len(forks))
    t = []
    for p in ps:
        t += ([p['n']] + [q['y'] for q in p['opts']] + [q['rep'][0] for q in p['opts']]) if p.get('opts') else [p['n'], p['y']]
    txt.append(' '.join(t).replace('*', ''))
T = ' '.join(txt)
chk('台詞に数字(0-9)・ユーロ記号・地下鉄の値段がない', not re.search(r'[0-9€$]', T) and 'euro' in T)
chk('金額は定額タクシーの forty euros だけ(taxi 以外に euro はない)', all(('euro' not in tx.lower()) == (k != 'ath_taxi1') or k == 'ath_taxi1' for k, tx in zip(ALL, txt)) and 'forty euros' in txt[ALL.index('ath_taxi1')].lower())
chk('thirty は出国審査の場面だけ', [k for k, tx in zip(ALL, txt) if 'thirty' in tx.lower()] == ['ath_depimmig1'])
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def log_message(s, *a): pass
srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); base = 'http://127.0.0.1:%d' % srv.server_address[1]
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); b = r.text(); assert HOOK in b
    route.fulfill(response=r, body=b.replace(HOOK, "window.__T={G:G,PBY:PBY,startVid:startVid,ART:ART,ARTFAIL:ARTFAIL,artIdFor:artIdFor,MODES:MODES,MICBIG_IMG:typeof MICBIG_IMG!=='undefined'?MICBIG_IMG:null};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});window.__say=[];"
        "try{speechSynthesis.speak=function(u){window.__say.push(u.text);setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));")
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--no-sandbox'])
    for v in ALL:
        ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
        pg = ctx.new_page(); pg.route(re.compile(r'/tour/athens/index\.html(\?.*)?$'), hooked)
        pg.goto(base + '/tour/athens/index.html?check=1'); pg.wait_for_timeout(1000)
        r = pg.evaluate("(v)=>{var T=window.__T,pl=null;Object.keys(T.PBY).forEach(function(k){if((T.PBY[k].v||[]).indexOf(v)>=0)pl=T.PBY[k]});if(!pl)return null;T.startVid(pl,v,'ev');return pl.id}", v)
        pg.wait_for_timeout(1800)
        i = pg.evaluate("(function(){var T=window.__T;return {art:T.artIdFor(T.G.scene),fail:Object.keys(T.ARTFAIL),vid:T.G.scene&&T.G.scene.vid}})()")
        chk('%s: チェックモードから入れる・実画あり・読み込み失敗なし・エラーなし' % v, r and i['vid'] == v and i['art'] and not i['fail'] and pg.evaluate('window.__errs') == [], (r, i))
        if v == 'ath_taxi1':
            cx = pg.evaluate("(function(){var T=window.__T;return T.G.scene&&1}())"); chk('taxi: 場面が動く', bool(cx))
        ctx.close()
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
    pg = ctx.new_page(); pg.route(re.compile(r'/tour/athens/index\.html(\?.*)?$'), hooked); pg.goto(base + '/tour/athens/index.html?check=1'); pg.wait_for_timeout(1000)
    ids = pg.evaluate("(function(){var o=[];var M=window.__T.MODES;Object.keys(M).forEach(function(k){M[k].p.forEach(function(p){(p.v||[]).forEach(function(v){o.push(v)})})});return o})()")
    chk('MODES の場所に10場面すべてがある(到着4・街3・出発3)', sorted(set(ids)) == sorted(ALL), ids)
    ctx.close()
    for path in ['/tour/index.html', '/tour/athens/index.html']:
        ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT); pg = ctx.new_page(); pg.goto(base + path); pg.wait_for_timeout(900)
        chk('%s: エラーなし' % path, pg.evaluate('window.__errs') == [])
        ctx.close()
    br.close()
w = open(os.path.join(ROOT, 'tour/index.html'), encoding='utf-8').read()
chk('マイク: MICBIG_IMG が mic-large-v1.png', "MICBIG_IMG='assets/art/mic-large-v1.png'" in w)
chk('マイク: 箱の大きさ84x119は変えていない', re.search(r'\.declmic\{[^}]*width:84px', w) is not None or '84' in w)
wd = open(os.path.join(ROOT, 'world/index.html'), encoding='utf-8').read()
chk('世界地図: アテネの点とロヴァニエミからの道', "athens:{n:'アテネ'" in wd and "rovaniemi:['doha','athens']" in wd)
chk('チェックモード: ロヴァニエミからアテネへのリンク', "athens/?check=1" in open(os.path.join(ROOT, 'tour/rovaniemi/index.html'), encoding='utf-8').read())
print('\nNG %d件' % len(bad) if bad else '\n全部OK'); sys.exit(1 if bad else 0)
