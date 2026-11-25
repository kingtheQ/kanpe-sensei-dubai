# -*- coding: utf-8 -*-
"""タスク075 の動作確認(ヘッドレス)。使い方: python3 -I tour-src/tests/test_hotelroom075.py
ホテルの部屋(nbo_room・art nroom)の主人公を室内基準に拡大: キング 114→248px(148×248)・ルル 102→200px(129×200)=カフェ eikai の主人公と同値。
(1)art 設定: nroom の hall がキング w148/h248・ルル w129/h200・足もと by=884・eikai の dep と同値 (2)nbo_room→nroom の結び(artIdFor)・背景ファイルが不変(sha256)・台本が不変
(3)画面: 素材(68×114/66×102)を NEAREST で 148×248/129×200 に拡大した絵が足もと y=884 に描かれている・2人が重ならず絨毯(x396-1100)の上・影が拡大に追随・背景は人の外が不変・スーツケース(164px)との比率
(4)チェックモード(?check=1)から場所 hroom の nbo_room を開ける (5)他の art(eikai・nbar・ほかの hall)は不変・エラーなし・保存キーを増やさない
実機(スマホ)の見え方は確認できない(未確認)。"""
import os, sys, re, json, base64, io, hashlib, threading, http.server, socketserver
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tour-src'))
import song_data
ART = os.path.join(ROOT, 'tour/assets/art')
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
# ---- (2) 素材・台本が不変 ----
BG = os.path.join(ART, 'nairobi-hotel-room-v1.png')
chk('背景 nairobi-hotel-room-v1.png が不変(sha256 と 1536×960)', hashlib.sha256(open(BG, 'rb').read()).hexdigest() == 'e76cf4a75d84ba3694be2b43d472fc269dbabd781fc992d0d125336f06a2771f' and Image.open(BG).size == (1536, 960), hashlib.sha256(open(BG, 'rb').read()).hexdigest()[:16])
chk('主人公素材 hall-king-back 68×114・hall-lulu-back 66×102 は差し替えていない', Image.open(os.path.join(ART, 'npc/hall-king-back.png')).size == (68, 114) and Image.open(os.path.join(ART, 'npc/hall-lulu-back.png')).size == (66, 102))
sc = song_data.ROOM_SCENE
chk('台本 ROOM_SCENE が不変(6つの台詞・id nbo_room)', sc['id'] == 'nbo_room' and hashlib.sha256(json.dumps(sc, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest() == 'bee9191bbe7320aa7d5807f317fa460b1a41162d785bb8d7d79291f5532cddc9', hashlib.sha256(json.dumps(sc, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()[:16])
# ---- 画面 ----
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,ART:ART,setMode:setMode,showMap:showMap,artIdFor:artIdFor};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "window.__say=[];try{speechSynthesis.speak=function(u){window.__say.push(u.text);setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));")
def canvas(p): return np.array(Image.open(io.BytesIO(base64.b64decode(p.evaluate("document.getElementById('sceneA').toDataURL('image/png')").split(',')[1]))).convert('RGB')).astype(int)
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
def newpage(br):
    ctx = br.new_context(viewport={'width': 430, 'height': 900}, device_scale_factor=1); pg = ctx.new_page(); pg.add_init_script(INIT); pg.route(re.compile(r'/tour/index\.html'), hooked); return pg
def sprite(n, w, h):   # 素材を NEAREST で拡大(ページと同じ作り)
    im = Image.open(os.path.join(ART, 'npc', n + '.png')).convert('RGBA').resize((w, h), Image.NEAREST); return np.array(im)
def match(a, sp, x, by, tf):   # 腰から下(揺れない部分)の画素が、素材の拡大と一致する割合(%)
    h, w = sp.shape[:2]; x0 = int(x - w / 2 + .5); y0 = by - h; top = int(h * tf)
    c = a[y0 + top:y0 + h, x0:x0 + w]; s2 = sp[top:]; m = s2[..., 3] == 255
    return round(float((np.abs(c - s2[..., :3].astype(int)).sum(2)[m] <= 40).mean() * 100), 1)
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--autoplay-policy=document-user-activation-required'])
    pg = newpage(br); pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1200); pg.mouse.click(215, 450); pg.wait_for_timeout(800)
    cfg = pg.evaluate("JSON.parse(JSON.stringify(__T.ART.nroom))"); eik = pg.evaluate("JSON.parse(JSON.stringify(__T.ART.eikai.dep))")
    H = cfg['hall']
    # ---- (1) 設定 ----
    chk('nroom: キング h=248・w=148・ルル h=200・w=129(基準)', (H['king']['w'], H['king']['h'], H['lulu']['w'], H['lulu']['h']) == (148, 248, 129, 200), H)
    chk('nroom の大きさは eikai(カフェ)の主人公と同値(w/h が同じ)', (H['king']['w'], H['king']['h'], H['lulu']['w'], H['lulu']['h']) == (eik['king']['w'], eik['king']['h'], eik['lulu']['w'], eik['lulu']['h']), eik)
    chk('足もと by=884 は維持・素材は hall-*-back のまま・人(people)は置かない・TV の矩形も不変', H['king']['by'] == 884 and H['lulu']['by'] == 884 and H['king']['n'] == 'hall-king-back' and H['lulu']['n'] == 'hall-lulu-back' and not cfg.get('people') and cfg['tv'] == {'x': 1120, 'y': 216, 'w': 344, 'h': 176} and cfg['bg'] == 'nairobi-hotel-room-v1.png', cfg)
    kb = (H['king']['x'] - 74, H['king']['x'] + 74); lb = (H['lulu']['x'] - 64.5, H['lulu']['x'] + 64.5)
    chk('2人が重ならない・絨毯(x396-1100)の上に収まる', lb[1] < kb[0] and lb[0] >= 396 and kb[1] <= 1100, (lb, kb))
    # ---- (2) 結び・場面 ----
    pg.evaluate("(function(){var T=__T;T.save.ticket='ow';['nbo_immig1','nbo_bag1','nbo_sim1','nbo_taxi1'].forEach(function(v){T.save.seen[v]=1});T.setMode('arr');T.showMap()})()"); pg.wait_for_timeout(400)
    keys0 = sorted(pg.evaluate("Object.keys(localStorage)")); seen0 = pg.evaluate("JSON.stringify(__T.save.seen)")
    pg.click('.node[data-id=hroom]'); pg.wait_for_timeout(2200)
    info = pg.evaluate("[__T.G.view,__T.G.scene.d.id,__T.artIdFor(__T.G.scene)]")
    chk('hroom から nbo_room に入り、art id は nroom(結びは不変)', info == ['scene', 'nbo_room', 'nroom'], info)
    a = canvas(pg); bgp = np.array(Image.open(BG).convert('RGB')).astype(int)
    lu = sprite('hall-lulu-back', 129, 200); kg = sprite('hall-king-back', 148, 248)
    mlu = match(a, lu, H['lulu']['x'], 884, .6); mkg = match(a, kg, H['king']['x'], 884, .6)
    chk('表示サイズ: ルル 129×200・キング 148×248(腰から下の画素が素材の NEAREST 拡大と 90% 以上一致=その大きさで描かれている)', mlu >= 90 and mkg >= 90, (mlu, mkg))
    old_lu = sprite('hall-lulu-back', 66, 102); old_kg = sprite('hall-king-back', 68, 114)
    chk('旧サイズ(ルル66×102・キング68×114)では描かれていない(拡大された)', match(a, old_lu, 700, 884, .6) < 60 and match(a, old_kg, 836, 884, .6) < 60, (match(a, old_lu, 700, 884, .6), match(a, old_kg, 836, 884, .6)))
    # ぼかし拡大でない: 拡大後の色が素材の色だけ(補間の中間色が出ない)
    cols = lambda sp: {tuple(p[:3]) for p in sp.reshape(-1, 4) if p[3] == 255}
    kreg = a[884 - 248:884, H['king']['x'] - 74:H['king']['x'] + 74]; kc = {tuple(p) for p in kreg.reshape(-1, 3).tolist()}
    kb_cols = cols(kg) | {tuple(p) for p in bgp[884 - 248:884, H['king']['x'] - 74:H['king']['x'] + 74].reshape(-1, 3).tolist()}
    foreign = float(np.mean([tuple(p) not in kb_cols for p in kreg.reshape(-1, 3).tolist()]))
    chk('NEAREST 拡大(ぼかさない): キングの領域の色のうち、素材の色でも背景の色でもないもの(補間の中間色)が 1% 未満', foreign < .01, round(foreign, 4))
    # 頭の幅(キャップ): 素材の頭の幅 54px(68px幅中)→ 拡大後 約118px
    ks = np.array(Image.open(os.path.join(ART, 'npc/hall-king-back.png')).convert('RGBA')); top_rows = ks[:30, :, 3] == 255
    hw0 = int(max(r.sum() for r in top_rows)); hw1 = round(hw0 * 148 / 68)
    chk('頭(キャップ)の幅: 素材 %dpx → 拡大後 約%dpx(指示書: 54→≈118)' % (hw0, hw1), hw0 == 54 and 116 <= hw1 <= 120, (hw0, hw1))
    # 影: 足もとの下に影が描かれ、幅が拡大に追随(ルル57・キング78)
    def shadow_w(x0, x1, by):   # 足もとの下(by+1〜by+8)で、背景と違う画素の横の幅(窓 [x0,x1) の中)
        d = (np.abs(a[by + 1:by + 9, x0:x1] - bgp[by + 1:by + 9, x0:x1]).sum(2) > 40).any(0); xs = np.where(d)[0]
        return int(xs.max() - xs.min() + 1) if len(xs) else 0
    sl, sk = shadow_w(560, 758, 884), shadow_w(758, 980, 884)
    chk('影が足もとに描かれ、拡大に追随している(幅: ルル 57×2≈114・キング 78×2≈156 / 旧は 58・72。測定窓は±90px)', 100 <= sl <= 120 and 140 <= sk <= 165, (sl, sk))
    # 背景は人の外が不変: キングの頭(y≈636)より上
    same = float((a[0:630, :] == bgp[0:630, :]).all(axis=2).mean())
    chk('背景は人の外で不変(y<630 の画素が素材と一致 99.95% 以上。TV・ベッド・スーツケースの絵はそのまま)', same > .9995, same)
    # 比率: スーツケース(背景に描かれた高さ164px)とキングの比
    chk('比率: スーツケース(164px)はキング(248px)の約66%=腰〜胸の高さ・キングの頭は y≈636(ベッド上面 y≈604 の少し下)', abs(164 / 248 - .66) < .01 and 884 - 248 == 636, (round(164 / 248, 3), 884 - 248))
    sv = (round(164 / 114, 2), round(164 / 248, 2)); print('    スーツケース/キング: 旧 %.2f(スーツケースの方が高い) → 新 %.2f' % sv)
    txt = pg.evaluate("document.body.innerText"); chk('画面に「勉強・テスト・測定・練習」の言葉がない', not any(w in txt for w in ['勉強', 'テスト', '測定', '練習', '復習', '採点']))
    chk('エラーなし・保存の記録(save.seen)と保存キーを増やさない', pg.evaluate('window.__errs') == [] and pg.evaluate("JSON.stringify(__T.save.seen)") == seen0 and sorted(pg.evaluate("Object.keys(localStorage)")) == keys0, pg.evaluate('window.__errs'))
    pg.screenshot(path='/tmp/t075_room.png'); pg.context.close()
    # ---- (4) チェックモード ----
    pg = newpage(br); pg.goto(base + '/tour/index.html?check=1'); pg.wait_for_timeout(1500)
    try: pg.mouse.click(215, 450); pg.wait_for_timeout(800)
    except Exception: pass
    pg.click('#chkBtn'); pg.wait_for_timeout(400)
    ok = pg.evaluate("(function(){var rows=document.querySelectorAll('#chkPan .row');for(var i=0;i<rows.length;i++){var pn=rows[i].querySelector('.pn');if(pn&&pn.textContent.indexOf('[hroom]')>=0){var bs=rows[i].querySelectorAll('button');for(var j=0;j<bs.length;j++)if(bs[j].textContent==='開く'){bs[j].click();return true}}}return false})()")
    pg.wait_for_timeout(2200)
    inf = pg.evaluate("[__T.G.view,__T.G.scene&&__T.G.scene.d.id,__T.G.scene&&__T.artIdFor(__T.G.scene)]")
    chk('チェックモード(?check=1): 場所 hroom の「開く」から nbo_room(art nroom)に入れる', ok and inf == ['scene', 'nbo_room', 'nroom'], (ok, inf))
    ac = canvas(pg)
    chk('チェックモードでも拡大した2人が描かれている(ルル129×200・キング148×248)', match(ac, lu, H['lulu']['x'], 884, .6) >= 90 and match(ac, kg, H['king']['x'], 884, .6) >= 90, (match(ac, lu, H['lulu']['x'], 884, .6), match(ac, kg, H['king']['x'], 884, .6)))
    pg.screenshot(path='/tmp/t075_check.png'); pg.context.close()
    # ---- (5) ほかの art は不変 ----
    pg = newpage(br); pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1200); pg.mouse.click(215, 450); pg.wait_for_timeout(800)
    o = pg.evaluate("JSON.parse(JSON.stringify({eik:__T.ART.eikai.dep,nbar:__T.ART.nbar.hall,sage:__T.ART.sage.hall,hg:__T.ART.hgate_ow.hall}))")
    chk('他の art は不変: eikai(248/200)・nbar(248/200・x712/838)・sage/hgate_ow の hall は w/h を持たない', o['eik']['king']['h'] == 248 and o['nbar']['king']['h'] == 248 and o['nbar']['lulu']['x'] == 712 and 'h' not in o['sage']['king'] and 'h' not in o['hg']['king'], o)
    pg.context.close(); br.close()
print('\n不合格:', bad if bad else 'なし')
sys.exit(1 if bad else 0)
