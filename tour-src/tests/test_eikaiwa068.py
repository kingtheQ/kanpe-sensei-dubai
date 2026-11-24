# -*- coding: utf-8 -*-
"""タスク068 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_eikaiwa068.py
ナイロビの英会話カフェ(場面 nbo_eikaiwa1・art id eikai)。チェックモード(?check=1)からだけ入る試作。
(1) 素材: 背景・別素材3点・先生9点が tour/assets/art/ にあり、大きさが指示書どおり。先生は ×0.791(アフロ幅156px)
(2) 通常モード: CHECKボタンなし・英会話のタブは隠れる・本編の場所の一覧/場面の数え(TOUR_IDS)に入らない・既存の場面(nbo_java1/2・nbo_bag1・nbo_sim1・nbo_taxi1・nbo_lounge1・nbo_art1)と既存の ART の中身が変わらない
(3) チェックモード: 一覧に nbo_eikaiwa1 が出て、押すと入れる。art id=eikai・背景が素材と一致・エラーなし
(4) 見た目: 同梱プレビューと、動く別素材の画素を除いて ≥99.9% 一致(先生 ×0.791・中心 x=800・底辺 y=706、下半身は y=648 から下が天板で隠れる・キング/ルルの位置と大きさ)
(5) 別素材: ランプ・窓の影・湯気が、それぞれ4コマとも実際に画面に出る(コマごとの画素が素材と一致)。コマの切り替えがゆっくり
(6) 会話: 5往復(挨拶・飲み物の注文・ひとこと雑談)が最後まで進み、先生の台詞が全部出て、自分の番を発音(声の認識)して、終わるとマップへ戻る。
    Word Battle・Meaning! は出ない。台本に日本語がない。「勉強・テスト・測定・復習」などの言葉が画面に出ない。聞き取りに失敗しても止まらない
(7) 先生が話しているあいだ、頭の上に「…」の吹き出しが出る
マイク・実機の見え方・実機の音は確認できない(このテストの音声認識と声は偽物)。"""
import os, sys, io, re, json, base64, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import serve, INIT as FAKE_INIT, ROOT
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np
ART = os.path.join(ROOT, 'tour/assets/art')
HOOK = "requestAnimationFrame(frame);\n})();"
EXPOSE = ("window.__T={G:G,save:save,PBY:PBY,DLG:DLG,MODES:MODES,ART:ART,ARTFAIL:ARTFAIL,artIdFor:artIdFor,TOUR_IDS:TOUR_IDS,"
          "get spSay(){return spSay},gt:function(){return t}};")
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, EXPOSE + HOOK, 1))
def hooked_head(route):   # 変更前(HEAD)の tour/index.html。既存の場面が変わっていないことの比較用
    body = subprocess.check_output(['git', '-C', ROOT, 'show', 'HEAD:tour/index.html']).decode('utf-8')
    assert HOOK in body
    route.fulfill(status=200, content_type='text/html; charset=utf-8', body=body.replace(HOOK, EXPOSE + HOOK, 1))
def rgb(path): return np.array(Image.open(path).convert('RGB')).astype(int)
def rgba(path): return Image.open(path).convert('RGBA')
def snap(p):
    d = p.evaluate("()=>document.getElementById('sceneA').toDataURL('image/png')")
    return np.array(Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGB')).astype(int)
def comp(bg, strip, i, fw, fh, x, y):
    b = bg.convert('RGBA'); b.alpha_composite(strip.crop((i * fw, 0, i * fw + fw, fh)), (x, y)); return np.array(b.convert('RGB')).astype(int)

# ---------- (1) 素材 ----------
SIZES = {'nairobi-eikaiwa-cafe-v1.png': (1536, 960), 'nairobi-eikaiwa-cafe-steam-strip.png': (6144, 960), 'nairobi-eikaiwa-cafe-lamps-strip.png': (6144, 960),
         'nairobi-eikaiwa-cafe-window-strip.png': (800, 320), 'teacher-sit-front.png': (202, 360), 'teacher-sit-left-1.png': (203, 351), 'teacher-sit-left-2.png': (186, 352),
         'teacher-sit-back.png': (187, 359), 'teacher-stand-front.png': (217, 361), 'teacher-stand-left-1.png': (203, 352), 'teacher-stand-left-2.png': (181, 352),
         'teacher-stand-back.png': (194, 360), 'teacher-menu-icon.png': (97, 82)}
ok = all(os.path.exists(os.path.join(ART, n)) and Image.open(os.path.join(ART, n)).size == s for n, s in SIZES.items())
chk('1a 背景1・別素材3・先生9(ポーズ8＋宝箱アイコン)が tour/assets/art/ にあり、大きさが指示書どおり', ok and sum(1 for n in SIZES if n.startswith('teacher-')) == 9, len(SIZES))
ts = rgba(os.path.join(ART, 'teacher-sit-front.png')).resize((round(202 * .791), round(360 * .791)), Image.NEAREST)
aw = int((np.array(ts)[:, :, 3] > 0).sum(axis=1).max())
chk('1b 先生の ×0.791 表示(NEAREST)は 160×285、アフロ幅 156px', ts.size == (160, 285) and aw == 156, (ts.size, aw))

BG = rgba(os.path.join(ART, 'nairobi-eikaiwa-cafe-v1.png'))
LAMP = rgba(os.path.join(ART, 'nairobi-eikaiwa-cafe-lamps-strip.png')); STEAM = rgba(os.path.join(ART, 'nairobi-eikaiwa-cafe-steam-strip.png')); WIN = rgba(os.path.join(ART, 'nairobi-eikaiwa-cafe-window-strip.png'))
# 同梱プレビュー(正本)を、素材から組み立てなおす: 背景＋先生(×0.791・(720,421)・y<648)＋キング(148×248)・ルル(129×200)。動く別素材は含まない
bgnp = np.array(BG.convert('RGB')).astype(int)
pv = BG.copy(); t2 = ts.crop((0, 0, 160, 648 - 421)); pv.alpha_composite(t2, (720, 421))
kg = rgba(os.path.join(ART, 'npc/hall-king-back.png')).resize((148, 248), Image.NEAREST); lu = rgba(os.path.join(ART, 'npc/hall-lulu-back.png')).resize((129, 200), Image.NEAREST)
pv.alpha_composite(kg, (598, 684)); pv.alpha_composite(lu, (864, 732)); PV = np.array(pv.convert('RGB')).astype(int)
zp = os.environ.get('EIKAI_PREVIEW', '')   # 素材zipの teacher-cafe-preview.png のパス(あれば、組み立てなおしたプレビューとの一致も調べる)
if zp and os.path.exists(zp):
    real = rgb(zp); d = (real != PV).any(axis=2)
    chk('1c 同梱プレビュー(teacher-cafe-preview.png)と、組み立てなおしたプレビューの一致(先生・キング・ルル)', float((~d).mean()) >= .9995, round(float((~d).mean()), 5))
# 動く別素材のある画素(全コマの和)は比較から外す
ovl = np.zeros((960, 1536), bool)
for i in range(4):
    ovl |= np.array(LAMP.crop((i * 1536, 0, i * 1536 + 1536, 960)))[:, :, 3] > 0
    ovl |= np.array(STEAM.crop((i * 1536, 0, i * 1536 + 1536, 960)))[:, :, 3] > 0
    w = np.zeros((960, 1536), bool); w[172:492, 996:1196] = np.array(WIN.crop((i * 200, 0, i * 200 + 200, 320)))[:, :, 3] > 0; ovl |= w

srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    def mk(route=hooked, vp=(430, 900)):
        ctx = br.new_context(viewport={'width': vp[0], 'height': vp[1]}); ctx.add_init_script(FAKE_INIT)
        ctx.add_init_script("window.__perr=[];window.addEventListener('error',function(e){window.__perr.push(String(e.message))});localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));")
        p = ctx.new_page(); p.route('**/tour/index.html*', route); return p
    # ---------- (2) 通常モード ----------
    pn = mk(); pn.goto(base + '/tour/index.html'); pn.wait_for_timeout(1500); pn.mouse.click(215, 450); pn.wait_for_timeout(600)
    chk('2a 通常: CHECKボタンがない', pn.evaluate("()=>!document.getElementById('chkBtn')"))
    chk('2b 通常: 英会話のタブ(.mbtn[data-m=eikai])は隠れている', pn.evaluate("()=>{var b=document.querySelector('.mbtn[data-m=eikai]');return !!b&&b.hidden===true}"))
    chk('2c 通常: 本編の場面の数え(TOUR_IDS)に nbo_eikaiwa1 は入らない・場所 eikai は到着/空港/出発の場所一覧にない', pn.evaluate("()=>{var T=__T;var ids=T.TOUR_IDS.indexOf('nbo_eikaiwa1')<0;var inAny=['arr','stay','air','dep','hdep','hret','sage'].some(function(k){return T.MODES[k].p.some(function(p){return p.id==='eikai'||(p.v||[]).indexOf('nbo_eikaiwa1')>=0})});return ids&&!inAny}"))
    cur = pn.evaluate("()=>({old:Object.keys(__T.ART).filter(function(k){return k!=='eikai'}).map(function(k){return k+':'+JSON.stringify(__T.ART[k])}),dl:['nbo_java1','nbo_java2','nbo_art1','nbo_bag1','nbo_sim1','nbo_taxi1','nbo_lounge1','nbo_room'].map(function(v){return v+':'+JSON.stringify(__T.DLG[v]||null)})})")
    ph = br.new_context().new_page(); ph.route('**/tour/index.html*', hooked_head); ph.goto(base + '/tour/index.html'); ph.wait_for_timeout(1500)
    old = ph.evaluate("()=>({old:Object.keys(__T.ART).filter(function(k){return k!=='eikai'}).map(function(k){return k+':'+JSON.stringify(__T.ART[k])}),dl:['nbo_java1','nbo_java2','nbo_art1','nbo_bag1','nbo_sim1','nbo_taxi1','nbo_lounge1','nbo_room'].map(function(v){return v+':'+JSON.stringify(__T.DLG[v]||null)})})")
    chk('2d 既存の ART(%d項目)の中身が変更前(HEAD)と同じ' % len(old['old']), cur['old'] == old['old'])
    chk('2e 既存の場面(nbo_java1/2・art1・bag1・sim1・taxi1・lounge1・room)の台本が変更前と同じ', cur['dl'] == old['dl'])
    # ---------- (3) チェックモード ----------
    p = mk(); p.goto(base + '/tour/index.html?check=1'); p.wait_for_timeout(1500); p.mouse.click(215, 450); p.wait_for_timeout(600)
    p.evaluate("()=>document.getElementById('chkBtn').click()"); p.wait_for_timeout(200)
    chk('3a チェックモードの一覧に nbo_eikaiwa1 のボタンがある(場所 eikai・英会話カフェ)', p.evaluate("()=>[].some.call(document.querySelectorAll('#chkPan button'),function(b){return b.textContent==='nbo_eikaiwa1'})") and p.evaluate("()=>/英会話カフェ\\s+\\[eikai\\]/.test(document.getElementById('chkPan').innerText)"))
    p.evaluate("()=>{[].filter.call(document.querySelectorAll('#chkPan button'),function(b){return b.textContent==='nbo_eikaiwa1'})[0].click()}"); p.wait_for_timeout(2500)
    s = p.evaluate("()=>({view:__T.G.view,id:__T.artIdFor(__T.G.scene),fail:Object.keys(__T.ARTFAIL),errs:window.__perr})")
    chk('3b 一覧から入れる(場面の画面)・art id=eikai・絵の読み込みの失敗なし・エラーなし', s['view'] == 'scene' and s['id'] == 'eikai' and not s['fail'] and not s['errs'], s)
    # ---------- (4) 見た目: プレビューと比べる ----------
    best = 0; shots = []
    for i in range(36):
        a = snap(p); f = float((a == PV).all(axis=2)[~ovl].mean()); best = max(best, f); shots.append(a); p.wait_for_timeout(190)
    chk('4a 同梱プレビューと見た目が一致(動く別素材の画素を除く)≥99.9%', best >= .999, round(best, 5))
    a = shots[0]
    tab = (a == PV).all(axis=2)[648:706, 750:880] | ovl[648:706, 750:880]
    chk('4b 先生の下半身は天板で隠れている(y=648〜706・x=750〜880 は、プレビューと同じ=背景の天板のまま。左はしのキングの頭の揺れは除く)', float(tab.mean()) >= .999 and bool(((PV == bgnp).all(axis=2)[660:706, 760:880]).all()), float(tab.mean()))
    th = (a != bgnp).any(axis=2)[421:648, 720:880] & ~ovl[421:648, 720:880]
    ys, xs = np.where(th)
    chk('4c 先生が描かれている範囲(中心 x=800・上 y=421)と、アフロ幅 156px', 421 <= ys.min() + 421 <= 432 and abs((xs.min() + xs.max()) / 2 + 720 - 800) <= 1.5 and int(th[:70].sum(axis=1).max()) <= 156, (ys.min() + 421, xs.min() + 720, xs.max() + 720))
    # ---------- (5) 別素材 ----------
    lamp_ok = set(); win_ok = set(); st_a = set(); st_b = set(); times = {'lamp': [], 'win': [], 'steam': []}; prev = {}
    def which(a, strip, fw, fh, x, y, reg):   # 画面の区画が、素材のどのコマと(キャンバスの丸め誤差 ±3 以内で)一致するか
        (y0, y1, x0, x1) = reg; errs = [int(np.abs(a[y0:y1, x0:x1] - comp(BG, strip, i, fw, fh, x, y)[y0:y1, x0:x1]).max()) for i in range(4)]
        k = int(np.argmin(errs)); return k if errs[k] <= 3 and sorted(errs)[1] > 8 else None
    for k in range(80):
        a = snap(p); tt = p.evaluate("()=>__T.gt()")
        res = {'lamp': which(a, LAMP, 1536, 960, 0, 0, (130, 260, 160, 1420)), 'win': which(a, WIN, 200, 320, 996, 172, (172, 492, 996, 1196)), 'steam': which(a, STEAM, 1536, 960, 0, 0, (376, 666, 388, 450))}
        sb = which(a, STEAM, 1536, 960, 0, 0, (376, 666, 884, 910))
        if res['lamp'] is not None: lamp_ok.add(res['lamp'])
        if res['win'] is not None: win_ok.add(res['win'])
        if res['steam'] is not None: st_a.add(res['steam'])
        if sb is not None: st_b.add(sb)
        for nm in res:
            if res[nm] is not None and prev.get(nm) != res[nm]: times[nm].append(tt); prev[nm] = res[nm]
        p.wait_for_timeout(100)
    chk('5a ペンダントランプの4コマが実際に画面に出る(画素が素材と一致)', len(lamp_ok) == 4, sorted(lamp_ok))
    chk('5b 窓の外の影(996,172)の4コマが実際に画面に出る', len(win_ok) == 4, sorted(win_ok))
    chk('5c カップの湯気の4コマが実際に画面に出る(左のカウンターのカップ・右のカップ)', len(st_a) == 4 and len(st_b) == 4, (sorted(st_a), sorted(st_b)))
    cfg = p.evaluate("()=>__T.ART.eikai.strips.map(function(q){return [q.img,q.step,q.n,q.x,q.y,q.fw,q.fh,!!q.over]})")
    stp = dict((c[0].split('-')[-2], c[1]) for c in cfg)   # lamps / window / steam
    def gap(ts_): d_ = np.diff(ts_); return float(np.median(d_)) if len(d_) else 0
    g = dict((k, round(gap(v), 2)) for k, v in times.items())
    chk('5d 切り替えはゆっくり: ランプ(ゆるやかな明滅)%.1f秒・窓の影%.1f秒・湯気%.1f秒おき(いまの同種の strip は 0.5〜2.5 秒)。実測の間隔も設定より速くない' % (stp['lamps'], stp['window'], stp['steam']),
        .5 <= stp['lamps'] <= 1.0 and 1.0 <= stp['window'] <= 2.5 and .7 <= stp['steam'] <= 1.5 and g['lamp'] >= stp['lamps'] * .9 and g['win'] >= stp['window'] * .9 and g['steam'] >= stp['steam'] * .9, (stp, g))
    # ---------- (6) 会話 ----------
    p2 = mk(); p2.goto(base + '/tour/index.html?check=1'); p2.wait_for_timeout(1500); p2.mouse.click(215, 450); p2.wait_for_timeout(600)
    p2.evaluate("""()=>{window.__ph=[];window.__txt=[];window.__sp=[];var o=speechSynthesis.speak;speechSynthesis.speak=function(u){window.__sp.push(u.text);return o.apply(this,arguments)};
      setInterval(function(){try{var T=__T;var a=window.__ph;if(a[a.length-1]!==T.G.phase)a.push(T.G.phase);window.__txt.push((document.getElementById('msgText')||{}).textContent+'|'+((document.getElementById('panel')||{}).innerText||'').replace(/\\s+/g,' '))}catch(e){}},40)}""")
    dl = p2.evaluate("()=>__T.DLG.nbo_eikaiwa1")
    nturn = sum(1 for l in dl['lines'] if l.get('y') is not None and l.get('y') != '')
    JPRE = re.compile(r"[぀-ヿ㐀-鿿]")
    chk('6a 台本: 5往復・実在の店名なし・日本語の訳なし(jp は全部空)・単語の日本語の意味もなし(words 空)', nturn == 5 and all((l.get('jp') or '') == '' for l in dl['lines']) and dl['words'] == [] and dl.get('conv') == 1 and not JPRE.search(' '.join((l.get('n') or l.get('y') or '') for l in dl['lines'])), nturn)
    p2.evaluate("()=>document.getElementById('chkBtn').click()"); p2.wait_for_timeout(150)
    p2.evaluate("()=>{[].filter.call(document.querySelectorAll('#chkPan button'),function(b){return b.textContent==='nbo_eikaiwa1'})[0].click()}"); p2.wait_for_timeout(600)
    p2.evaluate("()=>{window.__bub=false;setInterval(function(){try{if(window.__bub||!__T.spSay)return;var d=document.getElementById('sceneA').getContext('2d').getImageData(836,400,34,24).data,n=0;for(var i=0;i<d.length;i+=4)if(d[i]===244&&d[i+1]===241&&d[i+2]===232)n++;if(n>100)window.__bub=true}catch(e){}},16)}")
    p2.click('.btn.go'); bub = 0; bubble_seen = False
    for i in range(900):
        p2.wait_for_timeout(50)
        if p2.evaluate("()=>__T.G.view") == 'map': break
    st = p2.evaluate("()=>({view:__T.G.view,ph:window.__ph,txt:window.__txt,sp:window.__sp,errs:window.__perr,seen:__T.save.seen})")
    npc = [l['n'] for l in dl['lines'] if l.get('n')]; cues = [re.sub(r'\*', '', l['y']) for l in dl['lines'] if l.get('y')]
    alltxt = ' '.join(st['txt'])
    chk('6b 5往復が最後まで進み、終わるとマップへ戻る(エラーなし)', st['view'] == 'map' and not st['errs'], (st['view'], st['errs']))
    chk('6c 先生の台詞5つが、画面に出て声で読まれる', all(any(n_ in t for t in st['txt']) for n_ in npc) and all(n_ in st['sp'] for n_ in npc), [n_ for n_ in npc if n_ not in st['sp']])
    chk('6d 自分の番(カンペ)が5つ出て、発音の流れ(聞き取り)を通って進む。見本が声で流れる', all(any(c in t for t in st['txt']) or any(c in s_ for s_ in st['sp']) for c in cues) and st['ph'].count('cue') >= 1, st['ph'][:12])
    chk('6e Word Battle・Meaning!(単語・意味の答え合わせ)の画面は出ない', not any(x in st['ph'] for x in ('words', 'reveal', 'meaning', 'wb')) and 'Meaning' not in alltxt, st['ph'])
    FORBID = ['勉強', 'テスト', '測定', '復習', '採点', '練習', '点数']
    chk('6f 画面に「勉強・テスト・測定・復習・採点・練習」の言葉が出ない', not any(w in alltxt for w in FORBID), [w for w in FORBID if w in alltxt])
    jp_screen = sorted(set(JPRE.findall(' '.join(re.sub(r'\|.*', '', t) for t in st['txt']))))
    chk('6g 先生と自分の台詞の表示に、日本語の訳が付かない(メッセージ欄に日本語の文字がない。場面の説明文を除く)', not [t for t in st['txt'] if JPRE.search(t.split('|')[0]) and not t.split('|')[0].startswith('ナイロビの小さな')], jp_screen)
    chk('7 先生が話しているあいだ、頭の上に「…」の吹き出しが出る', p2.evaluate('()=>window.__bub'))
    # 聞き取りに失敗したときの流れは既存の場面のまま: 2回失敗→3回目に通れば進む。3回失敗すると「ヘルプ」(ルルが代わりに言う)が出て、押すと進む
    def run_fail(nbad, use_help):
        q = mk(); q.goto(base + '/tour/index.html?check=1'); q.wait_for_timeout(1500); q.mouse.click(215, 450); q.wait_for_timeout(600)
        q.evaluate("(n)=>{var P=window.SpeechRecognition.prototype,os=P.start;window.__bad=n;window.__srn=0;P.start=function(){window.__srn++;if(window.__bad>0){window.__bad--;var me=this;setTimeout(function(){var rs=[{transcript:'blah blah blah',confidence:.5}];rs.isFinal=true;if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},20)},60);return}return os.apply(this,arguments)}}", nbad)
        q.evaluate("()=>document.getElementById('chkBtn').click()"); q.wait_for_timeout(150)
        q.evaluate("()=>{[].filter.call(document.querySelectorAll('#chkPan button'),function(b){return b.textContent==='nbo_eikaiwa1'})[0].click()}"); q.wait_for_timeout(600); q.click('.btn.go'); helped = False
        for i in range(1500):
            q.wait_for_timeout(50)
            if use_help and not helped and q.evaluate("()=>__T.G.phase") == 'assist':
                q.wait_for_timeout(300); q.evaluate("()=>{var b=document.querySelector('#panel .btn.help');b&&b.click()}"); helped = True
            if q.evaluate("()=>__T.G.view") == 'map': break
        return q.evaluate("()=>({view:__T.G.view,srn:window.__srn,errs:window.__perr})"), helped
    fs, _ = run_fail(2, False)
    chk('6h 聞き取りに2回失敗しても、3回目に通れば会話は最後まで進んでマップへ戻る', fs['view'] == 'map' and fs['srn'] >= 7 and not fs['errs'], fs)
    # タスク074: 3回失敗すると、ヘルプを押さなくてもルルが代わりに言って進む(自動救済・全モード共通)。ヘルプ回数は減らない
    fs, helped = run_fail(3, False)
    chk('6i 3回失敗すると、ボタンを押さなくてもルルが代わりに言って、最後まで進んでマップへ戻る(タスク074の自動救済)', fs['view'] == 'map' and not fs['errs'], (helped, fs))
    br.close()
print('\n%s  (NG %d件)' % ('すべて OK' if not bad else '失敗あり', len(bad)))
if bad: print(bad); sys.exit(1)
