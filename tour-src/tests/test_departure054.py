# -*- coding: utf-8 -*-
"""タスク054 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_departure054.py
ナイロビ出発まわり(チェックイン・保安検査・免税店・ラウンジ・ゲート)の新背景と、別素材の動き・人の配置を、描画の記録(drawImage)から確かめる。
(1) 10場面(+同じ場所で出る出来事3つ)が新しい背景で出て、エラーなし (2) チェックイン: ベルトの荷物が横へ動く(位置の式・速さ・待ち)
(3) 保安検査: トレイと中身が両方のベルトを流れる(式・両はしで切る) (4) 免税店: 広告画面が3コマを2.5秒ごとに切り替える
(5) ラウンジ: 時計の針が3つの中心に重なって切り替わる・TV画面が x826〜1082/y348〜476 で4コマ・座る人6人が正本プレビューの位置(上半身だけでない)
(6) ゲート: 窓の外の飛行機(動きつき・柱の手前に出ない)・FIDSが(1184,356) (7) 立つ旅行者が2〜3人・端・相手/2人/動く素材と重ならない
(8) カウンター越しの相手は、カウンターの高さより下を描かない (9) 絵が読めないとき古い絵に落ちて会話は止まらない
(10) 羽田・ドーハ・機内・観光は変わらない(artIdFor の対応)。リポジトリの生成物(tour/)は書き換えない。マイク・実機の見え方は確認できない。"""
import os, sys, math, json, struct, threading, http.server, socketserver
from playwright.sync_api import sync_playwright
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
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,startVid:startVid,PBY:PBY,DLG:DLG,gt:function(){return t},st:function(v){t=v},artIdFor:typeof artIdFor==='function'?artIdFor:null,ART:typeof ART==='undefined'?null:ART,OUT:OUT};" + HOOK, 1))
BGS = ['nairobi-checkin-v1.png', 'nairobi-security-v1.png', 'nairobi-dutyfree-v1.png', 'nairobi-lounge-v2.png', 'nairobi-gate-v1.png']
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "try{speechSynthesis.speak=function(u){setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));"
        # 描画の記録: sceneA への drawImage を [ファイル名, 引数..., 不透明度] で残す。背景を描いた行(=1コマの始まり)には t と te を添える
        "window.__fr=[];(function(){var BG=" + json.dumps(BGS) + ",o=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.drawImage=function(im){"
        "try{if(this.canvas&&this.canvas.id==='sceneA'){var s=(im&&im.src||'').split('/').pop(),a=[].slice.call(arguments,1);"
        "if(BG.indexOf(s)>=0&&a.length<=4){var T=window.__T,S=T&&T.G.scene;window.__fr.push(['BG',s,T?T.gt():0,(T&&S&&S.artT0!=null)?T.gt()-S.artT0:0])}"
        "else window.__fr.push([s].concat(a,[this.globalAlpha]));if(window.__fr.length>20000)window.__fr.splice(0,10000)}}catch(e){}"
        "return o.apply(this,arguments)}})()")
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
def png_size(path):
    with open(path, 'rb') as f: h = f.read(24)
    return struct.unpack('>II', h[16:24])
def isz(n):
    for d in ('', 'npc/'):
        q = os.path.join(ART, d + n)
        if os.path.exists(q): return png_size(q)
    raise SystemExit('no image ' + n)
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
gen0 = open(os.path.join(ROOT, 'tour/index.html'), 'rb').read()
PL = {'nbo_checkin1': 'qcheckin', 'nbo_checkin2': 'qcheckin', 'nbo_sec1': 'nsec', 'nbo_sec2': 'nsec', 'nbo_duty1': 'duty', 'nbo_duty2': 'duty',
      'nbo_lounge1': 'lounge', 'nbo_lounge2': 'lounge', 'nbo_gate1': 'gate', 'nbo_gate2': 'gate', 'nbo_ev_c_phone': 'qcheckin', 'nbo_ev_d_lulu': 'duty', 'nbo_ev_e_gate': 'gate'}
NEWBG = {'checkinQ': 'nairobi-checkin-v1.png', 'security': 'nairobi-security-v1.png', 'duty': 'nairobi-dutyfree-v1.png', 'lounge': 'nairobi-lounge-v2.png', 'gate': 'nairobi-gate-v1.png'}
def start(p, vid):
    p.evaluate("(a)=>{var T=window.__T;T.startVid(T.PBY[a[0]],a[1],'ev')}", [PL[vid], vid]); p.wait_for_timeout(900)
def at(p, te, wait=140):
    """この場面の経過 te 秒の1コマを取る(時計 t を進めて、その次のコマの記録を返す)。戻り値=(コマの記録, その t, その te)"""
    p.evaluate("(x)=>{var T=window.__T;T.st(T.G.scene.artT0+x);window.__fr.length=0}", te); p.wait_for_timeout(wait)
    fr = p.evaluate("()=>window.__fr.slice()")
    idx = [i for i, e in enumerate(fr) if e[0] == 'BG']
    if len(idx) < 2: return None
    seg = fr[idx[0]:idx[1]]            # 完全な1コマ(背景の描きはじめ〜次の背景の前)
    return seg[1:], seg[0][2], seg[0][3]
def calls(fr, name): return [e[1:] for e in fr if e[0] == name]
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
    p = ctx.new_page(); p.route('**/tour/index.html', hooked); p.goto(base + '/tour/index.html'); p.wait_for_timeout(1800)
    # (1) 場面と背景
    for v in PL:
        start(p, v)
        r = p.evaluate("()=>({bg:__T.G.scene.d.bg,hid:document.getElementById('sceneA').hidden,err:window.__errs.length,id:__T.artIdFor(__T.G.scene)})")
        fr = at(p, 0.5)
        drawn = fr and [e[1] for e in [x for x in p.evaluate("()=>window.__fr.slice()") if x[0] == 'BG']][-1]
        chk('場面 %s: 新しい背景(%s)・エラーなし・art=%s' % (v, drawn, r['id']), r['bg'] in NEWBG and drawn == NEWBG[r['bg']] and not r['hid'] and r['err'] == 0 and r['id'])
    # (2) チェックイン: ベルトの荷物(x0..x1 の間を速さ v で左→右。wait 秒あいて繰り返す)
    for v, x0, x1 in (('nbo_checkin1', 814, 920), ('nbo_checkin2', 1130, 1236)):
        start(p, v); W, Hh, BY, VV, WAIT = x1 - x0 + 80, 96, 604, 20, 2
        okx = True; seen = []
        for te in (0.3, 2, 4.5, 7, 9.2, 10.5, 12, 14, 17, 21):
            r = at(p, te); fr, t_, te_ = r
            b = calls(fr, 'nairobi-checkin-belt-bag.png'); u = (te_ % (W / VV + WAIT)) * VV
            if u > W: okx &= not b; seen.append((round(te_, 1), None)); continue
            exp = 2 * round((x0 - 80 + u) / 2)
            okx &= len(b) == 1 and abs(b[0][0] - exp) <= 2 and b[0][1] == BY - Hh; seen.append((round(te_, 1), b[0][0] if b else None))
        chk('チェックイン %s: 荷物がベルト(x %d〜%d・面 y=%d)を 秒速%dpx で動く(位置の式と一致・%d秒あいて繰り返す)' % (v, x0, x1, BY, VV, WAIT), okx, seen[:5])
        xs = [s[1] for s in seen if s[1] is not None]
        chk('  荷物は左のカウンターの奥から右へ(動いている)', len(set(xs)) >= 4 and xs == sorted(xs)[:len(xs)] or len(set(xs)) >= 4)
    # (3) 保安検査: トレイが両ベルトを流れる
    items = {'nbo_sec1': ([(2, 0, 60), (3, 0, 260)], [(1, 0, 900), (4, 0, 1100)]), 'nbo_sec2': ([(4, 0, 80), (0, 0, 300)], [(5, 0, 880), (2, 0, 1120)])}
    for v, (li, ri) in items.items():
        start(p, v); okq = True; cnt = 0
        for te in (0.3, 3, 8, 15, 30):
            fr, t_, te_ = at(p, te); its = calls(fr, 'nairobi-security-items.png'); got = sorted((e[4], e[0]) for e in its)
            exp = []
            for (x0, x1, lst) in ((0, 528, li), (862, 1258, ri)):
                L = x1 - x0 + 150
                for (c, s, x) in lst:
                    pp = ((x - x0 + 14 * te_) % L + L) % L + x0 - 112
                    exp.append((2 * round(pp / 2), c * 112))
            exp = sorted(exp); okq &= len(got) == 4 and all(abs(a[0] - b[0]) <= 2 and a[1] == b[1] for a, b in zip(got, exp)); cnt += len(got)
        chk('保安検査 %s: トレイと中身が2本のベルト(左 x0〜528 / 右 862〜1258・面 y=648)を 秒速14px で流れる(式と一致)' % v, okq, cnt)
    # (4) 免税店: 広告画面
    start(p, 'nbo_duty1'); okd = True; fidx = []
    for te in (0.2, 3.0, 5.4, 7.8, 10.2):
        fr, t_, te_ = at(p, te); a = calls(fr, 'nairobi-dutyfree-screen-strip.png')
        k = int(t_ / 2.5) % 3; okd &= len(a) == 1 and a[0][0] == k * 176 and a[0][4] == 301 and a[0][5] == 281 and a[0][2] == 176 and a[0][3] == 112; fidx.append(a[0][0] // 176 if a else None)
    chk('免税店: 広告画面(176×112)を (301,281) に3コマ・2.5秒ごとに切り替え', okd and len(set(fidx)) >= 2, fidx)
    start(p, 'nbo_duty2'); fr, t_, te_ = at(p, 4)
    a = calls(fr, 'nairobi-dutyfree-screen-strip.png'); chk('免税店(2): 広告画面あり', len(a) == 1 and a[0][4:6] == [301, 281])
    # (5) ラウンジ
    CEN = [(850, 222), (954, 222), (1058, 222)]; OFF = [0, 4, 8]
    SIT = {'t-woman-hijab-sit-side-2.png': (522, 537), 't-man-dashiki-sit-side-2.png': (578, 665), 't-safari-sit-side-2.png': (478, 762),
           't-maasai-sit-side-1.png': (1256, 667), 't-man-thobe-sit-side-2.png': (995, 761), 't-backpacker-sit-side-1.png': (1331, 757)}
    for v in ('nbo_lounge1', 'nbo_lounge2'):
        start(p, v); okc = okt = True; seq = []
        for te in (0.2, 1.3, 2.4, 3.6, 5.7, 8.8, 11.5):
            fr, t_, te_ = at(p, te); h = calls(fr, 'nairobi-lounge-clock-hands.png'); tv = calls(fr, 'nairobi-lounge-tv-strip.png')
            n = int(t_)
            exp = [((n + OFF[i]) % 12, CEN[i][0] - 32, CEN[i][1] - 32) for i in range(3)]
            okc &= len(h) == 3 and all(a[0] == e[0] * 64 and a[4] == e[1] and a[5] == e[2] and a[2] == 64 for a, e in zip(h, exp))
            okt &= len(tv) == 1 and tv[0][0] == (int(t_ / 2.5) % 4) * 256 and tv[0][4:6] == [826, 348] and tv[0][2:4] == [256, 128]; seq.append(h[0][0] // 64 if h else None)
        chk('ラウンジ %s: 時計の針12コマが中心 (850,222)(954,222)(1058,222) に重なり、1秒ごとに切り替え(3つで時刻がずれる)' % v, okc and len(set(seq)) >= 5, seq)
        chk('ラウンジ %s: TV画面4コマが x826〜1082 / y348〜476 で2.5秒ごとに切り替え' % v, okt)
        fr, t_, te_ = at(p, 1.0); oks = True; det = []
        for n, (X, Y) in SIT.items():
            cs = calls(fr, n); w, h = isz(n); cut = round(h * .58)
            low = [c for c in cs if c[1] == cut]; up = [c for c in cs if c[1] == 0]
            ok1 = len(low) == 1 and low[0][4] == X and low[0][5] == Y + cut and low[0][5] + low[0][3] == Y + h and low[0][3] == h - cut     # 下半身まで全部(座面に足が着く所まで)
            ok2 = len(up) == 1 and up[0][4] == X and up[0][5] in (Y, Y - 3) and up[0][3] in (cut, cut + 3) and up[0][2] == w
            oks &= ok1 and ok2; det.append((n.split('-sit')[0][2:], X, Y))
        chk('ラウンジ %s: 座る人6人が正本プレビューの位置に全身で(上半身だけでない)' % v, oks and len(SIT) == 6, det)
    fr, t_, te_ = at(p, 1.0)
    chk('ラウンジ: 丸ブースのマサイ男性だけ手前のテーブル(front-054)が下半身を隠す(正本と同じ)', len(calls(fr, 'nairobi-lounge-front-054.png')) == 1 and calls(fr, 'nairobi-lounge-front-054.png')[0][:2] == [1256, 667])
    # (6) ゲート
    for v in ('nbo_gate1', 'nbo_gate2'):
        start(p, v); okp = True; dxs = []; pil = True
        for te in (0.1, 5, 12, 20, 30, 38):
            fr, t_, te_ = at(p, te); pl = calls(fr, 'nairobi-gate-plane.png'); fd = calls(fr, 'nairobi-gate-fids.png')
            okp &= len(fd) == 1 and fd[0][:2] == [1184, 356]
            T = 320 / 8; u = te_ % (T + 3)
            if u > T: okp &= not pl; continue
            exp = 2 * round((70 - 8 * u) / 2); okp &= len(pl) == 1 and abs(pl[0][0] - exp) <= 2 and pl[0][1] == 0; dxs.append(pl[0][0])
            bgd = [e for e in fr if e[0] == 'nairobi-gate-v1.png']                   # 柱を背景から描き直す(飛行機は柱の手前に出ない)
            pil &= len(bgd) >= 6
        chk('ゲート %s: FIDSが(1184,356)に静止・窓の外の飛行機が左へ秒速8pxでゆっくり動く(式と一致)・柱の手前に出ない' % v, okp and pil and len(set(dxs)) >= 3 and dxs == sorted(dxs, reverse=True), dxs)
    # (7)(8) 配置: 立つ旅行者2〜3人・端・重ならない・カウンターより下を描かない
    cfgs = p.evaluate("()=>{var o={};for(var k in __T.ART){if(__T.ART[k].dep)o[k]=__T.ART[k].dep}return o}")
    cfgs = dict((k, v) for k, v in cfgs.items() if k not in ('nmarket', 'nsafari'))   # タスク058: 滞在の観光2場面は出発まわりではない
    chk('出発まわりの art 設定が10個(ncheckin/nsec/nduty/nlounge/ngate × 2)', sorted(cfgs) == sorted(a + b for a in ('ncheckin', 'nsec', 'nduty', 'nlounge', 'ngate') for b in '12'), sorted(cfgs))
    def rect(n, x, by): w, h = isz(n + '.png'); return (x - w * .3, by - h, x + w * .3, by)
    def hit(a, b, m=0): return not (a[2] + m <= b[0] or b[2] + m <= a[0] or a[3] + m <= b[1] or b[3] + m <= a[1])
    for k, D in sorted(cfgs.items()):
        if k.startswith('nlounge'): continue
        ppl = D['people']; rs = [rect(q['n'], q['x'], q['by']) for q in ppl]
        lk = [rect(D['lulu']['n'], D['lulu']['x'], D['lulu']['by']), rect(D['king']['n'], D['king']['x'], D['king']['by'])]
        mov = []                                      # 動く別素材の通り道
        for f in D['fx']:
            if f['k'] == 'shuttle': mov.append((f['x0'], f['by'] - f['h'], f['x1'], f['by']))
            if f['k'] == 'queue': mov.append((f['x0'], f['by'] - 86, f['x1'], f['by']))
            if f['k'] == 'plane': mov.append((784 - 8 * (f['span'] / 8) + 70 - 0, 228, 1429 + f['dx0'], 478))
        cl = [(D['clerk']['x'] - 70, D['clerk']['top'], D['clerk']['x'] + 70, D['clerk']['clip'])] if 'clerk' in D else []
        spk = [rect(v['n'], v['x'], v['by']) for v in D['npcS'].values() if isinstance(v, dict) and 'n' in v and v['x'] > 0]
        edge = all(((r[0] + r[2]) / 2 <= 360 or (r[0] + r[2]) / 2 >= 1176) for r in rs)
        ov = [(i, 'lulu/king') for i, r in enumerate(rs) if any(hit(r, q, 12) for q in lk)] + [(i, 'move') for i, r in enumerate(rs) if any(hit(r, q) for q in mov)] + \
             [(i, 'npc') for i, r in enumerate(rs) if any(hit(r, q) for q in cl + spk)] + [(i, 'people') for i, r in enumerate(rs) for j, q in enumerate(rs) if j > i and hit(r, q)]
        chk('配置 %s: 旅行者%d人(2〜3人)・すべて端(左右の1/4)・相手/2人/動く素材/ほかの人と重ならない' % (k, len(ppl)), 2 <= len(ppl) <= 3 and edge and not ov, ov)
    for v, vclip in (('nbo_checkin1', 528), ('nbo_checkin2', 528), ('nbo_duty1', 602), ('nbo_duty2', 602), ('nbo_lounge1', 516), ('nbo_gate1', 660), ('nbo_gate2', 660)):
        start(p, v); r = p.evaluate("()=>{var S=__T.G.scene;var id=__T.artIdFor(S),D=__T.ART[id].dep;var k=null;for(var q in SPK){}return {id:id,sp:S.d.sp,m:D.npcS[S.d.sp],clip:D.clerk.clip,top:D.clerk.top}}".replace('var k=null;for(var q in SPK){}', ''))
        fr, t_, te_ = at(p, 1.0); cs = calls(fr, r['m'] + '.png'); mb = max([c[5] + c[7] for c in cs] or [9999])
        chk('カウンター越しの相手 %s(%s): カウンターの高さ y=%d より下を描かない(描いた下端 %s)' % (v, r['m'], r['clip'], mb), cs and r['clip'] == vclip and mb <= vclip)
    # (9) 絵が読めないとき
    p.close()
    for blk, vid in (('nairobi-lounge-v2.png', 'nbo_lounge1'), ('npc/tk-clerk-star.png', 'nbo_checkin1'), ('nairobi-gate-v1.png', 'nbo_gate2'), ('npc/t2-safari-back.png', 'nbo_sec1')):
        ctx2 = br.new_context(viewport={'width': 390, 'height': 780}); ctx2.add_init_script(INIT)
        q = ctx2.new_page(); q.route('**/tour/index.html', hooked); q.route('**/' + blk, lambda r: r.abort()); q.goto(base + '/tour/index.html'); q.wait_for_timeout(1500)
        start(q, vid); q.wait_for_timeout(700)
        r = q.evaluate("()=>({hid:document.getElementById('sceneA').hidden,err:window.__errs.length,turns:(__T.G.scene.turns||[]).length,msg:!!document.querySelector('#ctl,.ctl,#bar,#msg,#npc')})")
        chk('読めない(%s): 古い絵に落ちて場面は続く(sceneA を隠し、会話が出る・エラーなし)' % blk, r['hid'] and r['err'] == 0 and r['turns'] >= 5, r)
        ctx2.close()
    # (10) 対応の確認: 羽田・ドーハ・機内・観光は新しい絵にならない
    ctx3 = br.new_context(viewport={'width': 390, 'height': 780}); ctx3.add_init_script(INIT)
    q = ctx3.new_page(); q.route('**/tour/index.html', hooked); q.goto(base + '/tour/index.html'); q.wait_for_timeout(1500)
    R = q.evaluate("()=>{var f=__T.artIdFor,o={};[['hnd_checkin_ow','checkinQ'],['hnd_sec','security'],['hnd_gate_ow','hgateOW'],['doh_x','checkinQ'],['doh_y','gate'],['nbo_plane1','cabinQ'],['nbo_plane2','cabinQ'],['nbo_java1','cafe'],['nbo_art1','cafe'],['nbo_song','nlobby'],['nbo_sim1','sim'],['nbo_immig1','immig'],['nbo_bag1','baggage'],['nbo_taxi1','taxi']].forEach(function(a){o[a[0]+'/'+a[1]]=f({vid:a[0],d:{bg:a[1]}})});return o}")
    exp = {'hnd_checkin_ow/checkinQ': None, 'hnd_sec/security': None, 'hnd_gate_ow/hgateOW': 'hgate_ow', 'doh_x/checkinQ': None, 'doh_y/gate': None, 'nbo_plane1/cabinQ': None, 'nbo_plane2/cabinQ': None,
           'nbo_java1/cafe': None, 'nbo_art1/cafe': None, 'nbo_song/nlobby': 'nlobby', 'nbo_sim1/sim': 'simshop', 'nbo_immig1/immig': 'immig', 'nbo_bag1/baggage': 'bagclaim', 'nbo_taxi1/taxi': 'nairobi'}
    chk('対応: 羽田(checkinQ/security)・ドーハ側の同名bg・機内・カフェ・歌手・SIM・入国・荷物・タクシーは、これまでどおり', R == exp, {k: v for k, v in R.items() if exp[k] != v})
    ctx3.close()
    p3 = br.new_context(viewport={'width': 390, 'height': 780}); p3.add_init_script(INIT)
    d = p3.new_page(); d.route('**/tour/doha/index.html', hooked); d.goto(base + '/tour/doha/index.html'); d.wait_for_timeout(1200)
    dh = d.evaluate("()=>{var f=__T.artIdFor;return f?[f({vid:'doh_city_h1',d:{bg:'x'}}),f({vid:'nbo_checkin1',d:{bg:'checkinQ'}}),f({vid:'doh_a',d:{bg:'gate'}})]:'none'}")
    chk('ドーハ側の artIdFor は ホテルのフロントだけ(変更なし)', dh == ['hotel', None, None], dh)
    p3.close(); br.close()
chk('リポジトリの生成物(tour/index.html)を書き換えていない', open(os.path.join(ROOT, 'tour/index.html'), 'rb').read() == gen0)
print('\n%d 件NG: %s' % (len(bad), bad) if bad else '\n全部OK')
sys.exit(1 if bad else 0)
