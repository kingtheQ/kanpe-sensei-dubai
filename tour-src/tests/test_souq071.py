# -*- coding: utf-8 -*-
"""タスク071 の動作確認(ヘッドレス Chromium)。使い方: python3 tour-src/tests/test_souq071.py
ドーハ・スークの実画: bg calley(夜の路地)= doh_city_t1/t2/t3 と 割りこみ doh_ev_h_prayer、bg csouq(昼の広場)= doh_city_s1/s2/s3。
A. 結び: artIdFor が 7場面を dalley / dsouq に結ぶ。doh_city_h1→'hotel' は変わらない。対象外(crest・chotel の h2・ナイロビ側)は結ばない
B. 配置: ART の置き場が指示書どおり(別素材 {x,y,n,fw,fh,step}・ルル/キング/足もと)。素材のサイズが指示書どおり
C. 絵: 7場面すべて ?check=1 の「場面一覧」から始めて 実画の背景が出る(背景の画素が素材と一致)。動きの別素材は 2コマとも 背景+ストリップの合成と画素一致
D. 人物: キング(右)は全場面で出る。ルルは t3(いない場面)で出ない・ほかの場面で出る(既存の出し分け OUT.lvis のまま)
E. 既存: 対象外の場面は実画にならない(sceneA が隠れる)・ホテル(h1)は今までどおり実画・通常起動(?check なし)でも t1 に実画
マイク・実機の見え方は確認できない。台詞(doha_data.py)はこのタスクで変えていない(git diff で確認)。"""
import os, sys, io, json, base64, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
from PIL import Image
import numpy as np

ART = os.path.join(ROOT, 'tour/assets/art')
HOOK = "requestAnimationFrame(frame);\n})();"
EXPOSE = "window.__T={G:G,save:save,DLG:DLG,PBY:PBY,startVid:startVid,ART:ART,artIdFor:artIdFor,ARTFAIL:ARTFAIL,OUT:OUT};"
bad = []; ERR = []
DOHA = re.compile(r'/tour/doha/(index\.html)?(\?.*)?$')
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, EXPOSE + HOOK, 1))
def snap(p):
    d = p.evaluate("()=>document.getElementById('sceneA').toDataURL('image/png')")
    return np.array(Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB')).astype(int)
def img(n): return Image.open(os.path.join(ART, n)).convert('RGBA')
def comp(bg, layers, box):
    """bg(RGB)の上に layers=[(RGBAの1コマ, x, y)] を順に重ねた結果の box 部分(NEARESTのまま・拡大なし)"""
    im = bg.convert('RGBA')
    for fr, x, y in layers: im.alpha_composite(fr, (x, y))
    x0, y0, x1, y1 = box
    return np.array(im.convert('RGB')).astype(int)[y0:y1, x0:x1]
def frame(strip, i, fw): return strip.crop((i * fw, 0, (i + 1) * fw, strip.size[1]))
def match(a, b, tol=4): return float((np.abs(a - b) <= tol).all(axis=2).mean())

ALLEY = {'bg': 'doha-souq-alley-v1.png', 'lan': 'doha-souq-alley-lanterns-strip.png', 'clo': 'doha-souq-alley-cloth-strip.png'}
SQ = {'bg': 'doha-souq-square-v1.png', 'clo': 'doha-souq-square-cloth-strip.png', 'bird': 'doha-souq-square-birds-strip.png'}
SCENES = [('doh_city_t1', 'dalley'), ('doh_city_t2', 'dalley'), ('doh_city_t3', 'dalley'), ('doh_ev_h_prayer', 'dalley'),
          ('doh_city_s1', 'dsouq'), ('doh_city_s2', 'dsouq'), ('doh_city_s3', 'dsouq')]

# ---- B(素材): サイズ ----
for n, sz in [('doha-souq-alley-v1.png', (1536, 960)), ('doha-souq-alley-lanterns-strip.png', (3072, 960)), ('doha-souq-alley-cloth-strip.png', (3072, 960)),
              ('doha-souq-square-v1.png', (1536, 960)), ('doha-souq-square-cloth-strip.png', (3072, 176)), ('doha-souq-square-birds-strip.png', (3072, 120))]:
    chk('B0 素材 %s が %dx%d' % (n, sz[0], sz[1]), img(n).size == sz, img(n).size)

bgA = Image.open(os.path.join(ART, ALLEY['bg'])).convert('RGB'); bgS = Image.open(os.path.join(ART, SQ['bg'])).convert('RGB')
lanS, cloA = img(ALLEY['lan']), img(ALLEY['clo']); cloS, birdS = img(SQ['clo']), img(SQ['bird'])

with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(INIT)
    p = ctx.new_page(); p.on('pageerror', lambda e: ERR.append(str(e)[:160])); p.route(DOHA, hooked)
    p.goto(base + '/tour/doha/?check=1'); p.wait_for_timeout(1800)

    # ---------------- A. 結び ----------------
    r = p.evaluate("""()=>{var o={};['doh_city_t1','doh_city_t2','doh_city_t3','doh_ev_h_prayer','doh_city_s1','doh_city_s2','doh_city_s3','doh_city_h1','doh_city_h2','doh_city_r1','doh_city_c1','doh_immig1','doh_dep_gate'].forEach(function(v){o[v]=__T.artIdFor({vid:v})});o.none=__T.artIdFor(null);o.nov=__T.artIdFor({});return o}""")
    for v, a in SCENES: chk('A1 %s → %s' % (v, a), r[v] == a, r[v])
    chk("A2 既存の doh_city_h1 → 'hotel'(壊れていない)", r['doh_city_h1'] == 'hotel', r['doh_city_h1'])
    chk('A3 対象外(h2・r1・入国審査・出発ゲート・S無し)は結ばない', all(r[k] is None for k in ['doh_city_h2', 'doh_city_r1', 'doh_immig1', 'doh_dep_gate', 'none', 'nov']), {k: r[k] for k in ['doh_city_h2', 'doh_city_r1', 'doh_immig1', 'doh_dep_gate']})
    chk("A4 既存(タスク070)の doh_city_c1 → 'dcorn'(壊れていない)", r['doh_city_c1'] == 'dcorn', r['doh_city_c1'])

    # ---------------- B. 置き場 ----------------
    art = p.evaluate("()=>JSON.parse(JSON.stringify({a:__T.ART.dalley,s:__T.ART.dsouq}))")
    a, s = art['a'], art['s']
    chk('B1 路地 背景・ルル700・キング806・足もと856', (a['bg'], a['lulu'], a['king'], a['base'], a['mode']) == (ALLEY['bg'], 700, 806, 856, 'wide'), (a['bg'], a['lulu'], a['king'], a['base']))
    chk('B2 路地 ランタン {0,0,n2,1536x960,step1}', a['strips'][0] == {'img': ALLEY['lan'], 'x': 0, 'y': 0, 'n': 2, 'fw': 1536, 'fh': 960, 'step': 1}, a['strips'][0])
    chk('B3 路地 吊り布 {0,0,n2,1536x960,step0.8}', a['strips'][1] == {'img': ALLEY['clo'], 'x': 0, 'y': 0, 'n': 2, 'fw': 1536, 'fh': 960, 'step': .8}, a['strips'][1])
    chk('B4 広場 背景・ルル660・キング770・足もと836', (s['bg'], s['lulu'], s['king'], s['base'], s['mode']) == (SQ['bg'], 660, 770, 836, 'wide'), (s['bg'], s['lulu'], s['king'], s['base']))
    chk('B5 広場 屋台布 {0,452,n2,1536x176,step0.8}', s['strips'][0] == {'img': SQ['clo'], 'x': 0, 'y': 452, 'n': 2, 'fw': 1536, 'fh': 176, 'step': .8}, s['strips'][0])
    chk('B6 広場 鳥 {0,36,n2,1536x120,step0.4}(横スクロールなし=stripsだけ)', s['strips'][1] == {'img': SQ['bird'], 'x': 0, 'y': 36, 'n': 2, 'fw': 1536, 'fh': 120, 'step': .4}, s['strips'][1])

    # ---------------- C・D. 7場面(?check=1 の場面一覧から始める) ----------------
    p.evaluate("()=>document.getElementById('chkBtn').click()"); p.wait_for_timeout(150)
    def start_scene(vid, p=p):
        p.evaluate("()=>document.getElementById('chkBtn').click()") if p.evaluate("()=>document.getElementById('chkPan').hidden") else None
        p.wait_for_timeout(100)
        ok = p.evaluate("""v=>{var b=[].filter.call(document.querySelectorAll('#chkPan button'),function(x){return x.textContent.trim()===v})[0];if(!b)return false;b.click();return true}""", vid)
        return ok
    # 割りこみ(祈り)は自動で進み、偽の音声認識だと2〜3秒で終わってしまう。絵を確かめるため、声を返さない偽物の別ページで開く
    ctx2 = br.new_context(viewport={'width': 430, 'height': 900}); ctx2.add_init_script(INIT.replace('FS.prototype.start=function(){', 'FS.prototype.start=function(){return;'))
    p2 = ctx2.new_page(); p2.on('pageerror', lambda e: ERR.append(str(e)[:160])); p2.route(DOHA, hooked); p2.goto(base + '/tour/doha/?check=1'); p2.wait_for_timeout(1800)
    for vid, aid in SCENES:
        pg = p2 if vid == 'doh_ev_h_prayer' else p
        P = ALLEY if aid == 'dalley' else SQ; bgI = bgA if aid == 'dalley' else bgS
        ok = start_scene(vid, pg); chk('C0 %s: 場面一覧のボタンから始まる' % vid, ok)
        pg.wait_for_timeout(7200)   # 入って来る歩き(約6秒)が終わるまで
        cur = pg.evaluate("()=>({vid:__T.G.scene&&__T.G.scene.vid,id:__T.artIdFor(__T.G.scene),hid:document.getElementById('sceneA').hidden,fail:Object.keys(__T.ARTFAIL),lvis:__T.OUT.lvis})")
        chk('C1 %s: 実画が出ている(sceneA 表示・読み込み失敗なし・結び=%s)' % (vid, aid), cur['vid'] == vid and cur['id'] == aid and not cur['hid'] and not cur['fail'], cur)
        # 背景の画素一致(足もとより下・人物も strip も無い帯)
        bot = (0, 900, 1536, 960) if aid == 'dalley' else (0, 880, 1536, 960)
        s0 = snap(pg); ref = np.array(bgI).astype(int)
        m = match(s0[bot[1]:bot[3], bot[0]:bot[2]], ref[bot[1]:bot[3], bot[0]:bot[2]])
        chk('C2 %s: 背景が素材と画素一致(下の帯 %s)' % (vid, str(bot)), m >= .999, round(m, 4))
        # D 人物: ルルの箱(足もと中心 ±45・高さ110)が背景のままか。キングの箱
        B = 856 if aid == 'dalley' else 836; lx = 700 if aid == 'dalley' else 660; kx = 806 if aid == 'dalley' else 770
        lb = (lx - 40, B - 100, lx + 40, B - 6); kb = (kx - 40, B - 100, kx + 40, B - 6)
        lm = match(s0[lb[1]:lb[3], lb[0]:lb[2]], ref[lb[1]:lb[3], lb[0]:lb[2]]); km = match(s0[kb[1]:kb[3], kb[0]:kb[2]], ref[kb[1]:kb[3], kb[0]:kb[2]])
        chk('D1 %s: キングが右に出ている(背景とは違う)' % vid, km < .8, round(km, 3))
        if vid == 'doh_city_t3':
            chk('D2 doh_city_t3: ルルがいない(ルルの位置は背景のまま。出し分け lvis=0 を保つ)', lm >= .999 and cur['lvis'] == 0, (round(lm, 4), cur['lvis']))
        else:
            chk('D3 %s: ルルが左に出ている(背景とは違う)' % vid, lm < .8 and cur['lvis'] == 1, (round(lm, 3), cur['lvis']))
        # C 動き: 2コマとも 背景+ストリップの合成と画素一致(人物の上=y<680の帯)
        box = (0, 0, 1536, 680)
        seen = {'lan': set(), 'clo': set(), 'bird': set()}; best = []
        for k in range(10):
            sn = snap(pg)[box[1]:box[3], box[0]:box[2]]
            if aid == 'dalley':
                for fl in (0, 1):
                    for fc in (0, 1):
                        e = comp(bgI, [(frame(lanS, fl, 1536), 0, 0), (frame(cloA, fc, 1536), 0, 0)], box)
                        if match(sn, e) >= .999: seen['lan'].add(fl); seen['clo'].add(fc)
            else:
                for fc in (0, 1):
                    for fb in (0, 1):
                        e = comp(bgI, [(frame(cloS, fc, 1536), 0, 452), (frame(birdS, fb, 1536), 0, 36)], box)
                        if match(sn, e) >= .999: seen['clo'].add(fc); seen['bird'].add(fb)
            pg.wait_for_timeout(430)
        if aid == 'dalley':
            chk('C3 %s: ランタンの明滅 2コマとも合成と一致' % vid, seen['lan'] == {0, 1}, sorted(seen['lan']))
            chk('C4 %s: 吊り布の揺れ 2コマとも合成と一致' % vid, seen['clo'] == {0, 1}, sorted(seen['clo']))
        else:
            chk('C3 %s: 屋台布の揺れ 2コマとも合成と一致' % vid, seen['clo'] == {0, 1}, sorted(seen['clo']))
            chk('C4 %s: 鳥の羽ばたき 2コマとも合成と一致' % vid, seen['bird'] == {0, 1}, sorted(seen['bird']))
        if vid == 'doh_city_t1':
            pg.screenshot(path='/tmp/souq071_alley_t1.png')
            Image.fromarray(snap(pg).astype('uint8')).save('/tmp/souq071_alley_t1_canvas.png')
        if vid == 'doh_city_s1':
            Image.fromarray(snap(pg).astype('uint8')).save('/tmp/souq071_square_s1_canvas.png')
        if vid == 'doh_city_t3':
            Image.fromarray(snap(pg).astype('uint8')).save('/tmp/souq071_alley_t3_canvas.png')
        if vid == 'doh_ev_h_prayer':
            Image.fromarray(snap(pg).astype('uint8')).save('/tmp/souq071_alley_prayer_canvas.png')

    # ---------------- E. 既存 ----------------
    for vid, want_hidden in [('doh_city_r1', True), ('doh_city_h2', True), ('doh_city_h1', False), ('doh_city_c1', False)]:
        ok = start_scene(vid); p.wait_for_timeout(1500)
        st = p.evaluate("()=>({vid:__T.G.scene&&__T.G.scene.vid,id:__T.artIdFor(__T.G.scene),hid:document.getElementById('sceneA').hidden})")
        chk('E1 %s: %s' % (vid, '実画にならない(今までの描画)' if want_hidden else "今までどおり実画(%s)" % ('hotel' if vid == 'doh_city_h1' else 'dcorn')), ok and st['vid'] == vid and st['hid'] == want_hidden and (want_hidden or st['id'] == ('hotel' if vid == 'doh_city_h1' else 'dcorn')), st)

    # 通常起動(?check なし)でも t1 に実画(開く手段: 場所に入る)
    q = ctx.new_page(); q.on('pageerror', lambda e: ERR.append(str(e)[:160])); q.route(DOHA, hooked)
    q.goto(base + '/tour/doha/'); q.wait_for_timeout(1500)
    q.evaluate("()=>{__T.startVid(__T.PBY.calley,'doh_city_t1',null)}"); q.wait_for_timeout(1500)
    st = q.evaluate("()=>({id:__T.artIdFor(__T.G.scene),hid:document.getElementById('sceneA').hidden})")
    chk('E2 通常起動(?check なし)でも doh_city_t1 に実画(dalley)', st['id'] == 'dalley' and not st['hid'], st)
    # ナイロビ側(本編)は 対象場面を持たない=結ばない
    n = ctx.new_page(); n.route('**/tour/index.html', hooked); n.goto(base + '/tour/index.html'); n.wait_for_timeout(1200)
    rn = n.evaluate("()=>['doh_city_t1','doh_city_s1','doh_ev_h_prayer'].map(function(v){return __T.artIdFor({vid:v})})")
    chk('E3 ナイロビ(本編)の artIdFor は対象外のまま触っていない(null)', rn == [None, None, None], rn)
    chk('Z ページエラーなし', not ERR, ERR)
    br.close()
print('\n結果: NG=%d' % len(bad), bad)
sys.exit(1 if bad else 0)
