# -*- coding: utf-8 -*-
"""タスク067 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_haneda067.py
羽田出発の残り5場面(hnd_checkin_ow / hnd_sec / hnd_exit / hnd_plane_ow / hnd_plane_star)を実画に結んだ。
A. 結び(artIdFor): 本編側で 5場面が hcheckin_ow / hsec / hexit / hcabin_ow / hcabin_st に結ばれる。
   既存の結び(055 hcheckin_st・048 cabinseat・機内食 cabinmeal・054 ナイロビ出発・羽田のゲート)は変わらない
B. ドーハ側ビルド(tour/doha/index.html)の artIdFor は今までどおり(ホテルのフロントだけ)。羽田の結びを含まない
C. 通常モード: 5場面とも実画の背景(sceneA)が出る・読み込み失敗なし・エラーなし。別素材(荷物・トレイ・表示灯・機内の明滅)が読まれて描かれる
D. 配置: 同梱プレビューと見比べた画素の差(動く別素材・話す「…」の場所は除く)
E. 大きさ: 客室乗務員の高さ274・頭105px(この場面のキングの頭100pxの1.05倍)
F. チェックモード(?check=1): 同じ5場面を「CHECK」の一覧から始めて、5場面すべてに実画が出る
G. 画面に「勉強・テスト・測定」の言葉がない(新しく足した文字列)
マイク・実機の見え方は確認できない。"""
import os, sys, re, io, base64, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
import numpy as np
from PIL import Image
ART = os.path.join(ROOT, 'tour/assets/art')
PREV = os.environ.get('HND067_PREVIEWS', os.path.join(ROOT, 'tour-src/art/ref-haneda067'))   # 配置の正本プレビュー(素材パックのもの。リポジトリに入れてある)
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,startVid:startVid,PBY:PBY,DLG:DLG,ART:ART,ARTFAIL:ARTFAIL,artIdFor:artIdFor,OUT:OUT,gt:function(){return t},st:function(v){t=v}};" + HOOK, 1))
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
SC = {  # vid: (place, 期待する art id, 実画の背景, 別素材, 配置プレビュー, 別素材の領域(差から除く) [x0,y0,x1,y1])
    'hnd_checkin_ow': ('hcheckin', 'hcheckin_ow', 'haneda-checkin-qatar-v1.png', ['haneda-checkin-qatar-belt-bag.png'], 'haneda-checkin-qatar-preview.png', [(1120, 500, 1250, 620)]),
    'hnd_sec': ('hsec', 'hsec', 'haneda-security-v1.png', ['haneda-security-trays-strip.png'], 'haneda-security-preview.png', [(0, 500, 1536, 650)]),
    'hnd_exit': ('hexit', 'hexit', 'haneda-exit-immigration-v1.png', ['haneda-exit-lights-strip.png'], 'haneda-exit-immigration-preview.png', [(280, 300, 1260, 345), (230, 660, 410, 880)]),
    'hnd_plane_ow': ('hplane', 'hcabin_ow', 'haneda-cabin-qatar-v1.png', ['haneda-cabin-lights-strip.png'], 'haneda-cabin-qatar-preview.png', [(0, 240, 1536, 900)]),
    'hnd_plane_star': ('hplane', 'hcabin_st', 'haneda-cabin-turkish-v1.png', ['haneda-cabin-lights-strip.png'], 'haneda-cabin-turkish-preview.png', [(0, 240, 1536, 900)]),
}
CFG_BACK = ['hnd_checkin_star', 'hnd_gate_ow', 'hnd_gate_star']
src = open(os.path.join(ROOT, 'tour/index.html'), encoding='utf-8').read()
doha = open(os.path.join(ROOT, 'tour/doha/index.html'), encoding='utf-8').read()
def grab(p):
    d = p.evaluate("()=>document.getElementById('sceneA').toDataURL('image/png')")
    return Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB')
def settle(p, te):
    p.evaluate("(x)=>{var T=window.__T;T.st(T.G.scene.artT0+x)}", te); p.wait_for_timeout(160)
def info(p):
    return p.evaluate("()=>{var T=__T,S=T.G.scene,id=T.artIdFor(S);return {vid:S.vid,bg:S.d.bg,id:id,hid:document.getElementById('sceneA').hidden,fail:id?(T.ARTFAIL[id]||0):0,err:window.__errs.length}}")
with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome' if os.path.exists('/usr/bin/google-chrome') else None, args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
    p = ctx.new_page(); p.on('pageerror', lambda e: print('PAGEERR', str(e)[:160])); p.route('**/tour/index.html', hooked); p.goto(base + '/tour/index.html'); p.wait_for_timeout(1800)
    # ---------------- A. 結び ----------------
    r = p.evaluate("""()=>{var f=__T.artIdFor,o={};
      [['hnd_checkin_ow','checkinQ'],['hnd_sec','security'],['hnd_exit','immigH'],['hnd_plane_ow','cabinQ'],['hnd_plane_star','cabinT'],
       ['hnd_checkin_star','checkinT'],['hnd_gate_ow','hgateOW'],['hnd_gate_star','hgateST'],['hnd_ev_ca_ow','cabinQ'],['hnd_ev_ca_star','cabinT'],['hnd_ev_meal_ow','cabinQ'],['hnd_ev_meal_star','cabinT'],
       ['nbo_checkin1','checkinQ'],['nbo_checkin2','checkinQ'],['nbo_sec1','security'],['nbo_sec2','security'],['nbo_plane1','cabinQ'],['nbo_plane2','cabinQ'],['nbo_immig1','immig'],
       ['doh_x','checkinQ'],['doh_y','security'],['doh_z','immigH'],['doh_w','cabinQ']].forEach(function(a){o[a[0]]=f({vid:a[0],d:{bg:a[1]}})});return o}""")
    exp = {'hnd_checkin_ow': 'hcheckin_ow', 'hnd_sec': 'hsec', 'hnd_exit': 'hexit', 'hnd_plane_ow': 'hcabin_ow', 'hnd_plane_star': 'hcabin_st'}
    chk('A1 本編: 5場面の結び', all(r[k] == v for k, v in exp.items()), {k: r[k] for k in exp})
    chk('A2 055 ターキッシュ側・羽田のゲートは従来どおり', r['hnd_checkin_star'] == 'hcheckin_st' and r['hnd_gate_ow'] == 'hgate_ow' and r['hnd_gate_star'] == 'hgate_st', (r['hnd_checkin_star'], r['hnd_gate_ow'], r['hnd_gate_star']))
    chk('A3 048 cabinseat・機内食 cabinmeal は従来どおり(hnd_ev_ca_ / hnd_ev_meal_ は今回の機内の絵に取られない)', r['hnd_ev_ca_ow'] == 'cabinseat' and r['hnd_ev_ca_star'] == 'cabinseat' and r['hnd_ev_meal_ow'] == 'cabinmeal' and r['hnd_ev_meal_star'] == 'cabinmeal', (r['hnd_ev_ca_ow'], r['hnd_ev_meal_star']))
    chk('A4 054 ナイロビ出発は従来どおり(ncheckin1/2・nsec1/2・機内 nbo_plane は結ばれない)', (r['nbo_checkin1'], r['nbo_checkin2'], r['nbo_sec1'], r['nbo_sec2'], r['nbo_plane1'], r['nbo_plane2'], r['nbo_immig1']) == ('ncheckin1', 'ncheckin2', 'nsec1', 'nsec2', None, None, 'immig'), r)
    chk('A5 vid が hnd_ でない同名の bg(doh_ など)は今回の絵に結ばない', r['doh_x'] is None and r['doh_y'] is None and r['doh_z'] is None and r['doh_w'] is None, (r['doh_x'], r['doh_y'], r['doh_z'], r['doh_w']))
    # ---------------- B. ドーハ側 ----------------
    chk('B1 ドーハ側ビルドの artIdFor は ホテルのフロントだけ(変更なし)', "function artIdFor(S){return S&&S.vid==='doh_city_h1'?'hotel':null}" in doha)
    chk('B2 ドーハ側ビルドの artIdFor に 羽田の結びは入っていない', not re.search(r"function artIdFor\(S\)\{[^\n]*(hcheckin_ow|hsec|hexit|hcabin_)", doha))
    chk('B3 本編側の artIdFor に結びが入っている', all(('return\'' + x + '\'') in src for x in ('hcheckin_ow', 'hsec', 'hexit', 'hcabin_ow', 'hcabin_st')))
    # ---------------- C. 通常モード ----------------
    snaps = {}
    for vid, (pl, aid, bgf, extra, prev, mask) in SC.items():
        p.evaluate("(a)=>{var T=window.__T;T.startVid(T.PBY[a[0]],a[1],'ev')}", [pl, vid]); p.wait_for_timeout(1500)
        i0 = info(p); settle(p, 0.7)
        chk('C %s: 実画(%s)・art=%s・読み込み失敗なし・エラーなし' % (vid, bgf, i0['id']), i0['id'] == aid and not i0['hid'] and not i0['fail'] and i0['err'] == 0, i0)
        imgs = p.evaluate("()=>{var T=__T,c=T.ART['%s'];var o={bg:c.bg,strips:(c.strips||[]).map(function(s){return s.img}),fx:((c.dep&&c.dep.fx)||[]).map(function(s){return s.img})};return o}" % aid)
        chk('C %s: 背景と別素材が ART に結ばれている' % vid, imgs['bg'] == bgf and (set(imgs['strips'] + imgs['fx']) >= set(extra)), imgs)
        snaps[vid] = {}
        for k in (0, 1):
            settle(p, 0.7 + k); snaps[vid][k] = grab(p)
    if os.environ.get('HND067_DUMP'):
        for v, d in snaps.items():
            for k, im_ in d.items(): im_.save(os.path.join(os.environ['HND067_DUMP'], '%s-%d.png' % (v, k)))
    # ---------------- D. 配置(同梱プレビューとの画素差) ----------------
    if PREV:
        for vid, (pl, aid, bgf, extra, prev, mask) in SC.items():
            pv = np.array(Image.open(os.path.join(PREV, prev)).convert('RGB')).astype(int)
            best = None
            for k in (0, 1):
                a = np.array(snaps[vid][k]).astype(int); m = np.ones(a.shape[:2], bool)
                for (x0, y0, x1, y1) in mask: m[y0:y1, x0:x1] = False
                if vid in ('hnd_plane_ow', 'hnd_plane_star'):   # 機内は明滅の画面(座席の背面)を除き、人物(乗務員・ふたり)の周りだけ見る
                    m[:] = False; m[600:910, 500:1100] = True
                d = (np.abs(a - pv).sum(2) > 40) & m; fr = d.sum() / max(1, m.sum())
                if best is None or fr < best[0]: best = (fr, k, int(d.sum()), int(m.sum()))
            chk('D %s: 同梱プレビューとの差が小さい(差 %d / %d 画素 = %.2f%%)' % (vid, best[2], best[3], best[0] * 100), best[0] < 0.03, best)
    else:
        print('--  D 配置の画素差は HND067_PREVIEWS(プレビューのフォルダ)が無いので飛ばした')
    # ---------------- E. 客室乗務員の大きさ ----------------
    im = Image.open(os.path.join(ART, 'npc/ca-front-274.png')).convert('RGBA'); al = np.array(im)[:, :, 3]; rows = np.where(al.any(1))[0]
    chk('E1 乗務員の絵の高さは 274', im.size[1] == 274 and rows.min() == 0 and rows.max() == 273, im.size)
    # 頭(お団子の天辺=行0〜顎): 顔の肌色の行が細くなる手前(幅40画素以上の最後の行)を顎とみなして測る
    skin = (np.array(im)[:, :, 3] > 200) & (np.abs(np.array(im)[:, :, 0].astype(int) - 226) < 30) & (np.abs(np.array(im)[:, :, 1].astype(int) - 165) < 35) & (np.abs(np.array(im)[:, :, 2].astype(int) - 130) < 40)
    chin = max(y for y in range(0, 110) if skin[y].sum() >= 40) + 1
    chk('E2 乗務員の頭(お団子の天辺〜顎)= %dpx。キングの頭100pxの1.0〜1.1倍(100〜110px)・正本は105px' % chin, 103 <= chin <= 107, chin)
    # ---------------- F. チェックモード ----------------
    c2 = br.new_context(viewport={'width': 430, 'height': 900}); c2.add_init_script(INIT)
    q = c2.new_page(); q.on('pageerror', lambda e: print('PAGEERR', str(e)[:160])); q.route('**/tour/index.html*', hooked); q.goto(base + '/tour/index.html?check=1'); q.wait_for_timeout(1800)
    chk('F0 ?check=1 で CHECK ボタンが出る', q.evaluate("()=>!!document.getElementById('chkBtn')"))
    for vid, (pl, aid, bgf, extra, prev, mask) in SC.items():
        tk = 'star' if vid.endswith('star') else 'ow'
        q.evaluate("(t)=>{document.getElementById('chkBtn').click()}", tk); q.wait_for_timeout(120)
        q.evaluate("(t)=>{var b=[].slice.call(document.querySelectorAll('#chkPan button')).filter(function(x){return x.textContent===(t==='star'?'Star Alliance':'oneworld')})[0];if(b)b.click()}", tk); q.wait_for_timeout(120)
        ok = q.evaluate("(v)=>{var b=[].slice.call(document.querySelectorAll('#chkPan button')).filter(function(x){return x.textContent===v})[0];if(!b)return false;b.click();return true}", vid); q.wait_for_timeout(1500)
        i1 = info(q); settle(q, 0.7); cv = grab(q); sig = int(np.array(cv).astype(int).std())
        chk('F %s: チェックモードでも実画(art=%s・背景描画あり・失敗なし)' % (vid, i1['id']), ok and i1['id'] == aid and not i1['hid'] and not i1['fail'] and i1['err'] == 0 and sig > 20, (ok, i1, sig))
    # ---------------- G. 言葉 ----------------
    new = '\n'.join(l for l in src.split('\n') if ('hcheckin_ow:' in l or 'hsec:' in l or 'hexit:' in l or 'hcabin_ow:' in l or 'hcabin_st:' in l))
    chk('G 新しい ART 項目に「勉強・テスト・測定・練習」の言葉がない', not re.search(r'勉強|テスト|測定|練習', new))
    br.close()
print('\n結果: %s' % ('すべてOK' if not bad else 'NG %d件: %s' % (len(bad), bad)))
sys.exit(1 if bad else 0)
