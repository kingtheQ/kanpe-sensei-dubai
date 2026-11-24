# -*- coding: utf-8 -*-
"""タスク077b の動作確認(ヘッドレス)。使い方: python3 -I tour-src/tests/test_lobby077b.py
バルコニーバルの素材結び: (1)ART.nbar の確定値(strips 2点の座標・ルル/キングの大きさ指定・バーテンダー n/x/top/clip) (2)素材ファイルの存在と大きさ
(3)画面で: ロビー → バーで場面 nbo_bar1(絵 nbar)・ルル129×200/キング148×248で描かれる・バーテンダーはカウンター上面(y500)で切れて描かれる・ストリップが動く
(4)チェックモード(?check=1)でもロビー hub からバー場面まで辿れる (5)背景が読めなくても詰まらない (6)台詞・保存キーを増やさない。
実機の見え方・カーテンと明滅の動きの感触・読み上げの聞こえ方は確認できない(未確認)。"""
import os, sys, re, json, base64, io, threading, http.server, socketserver
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tour-src'))
import song_data
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
ART = os.path.join(ROOT, 'tour/assets/art')
# ---- 素材ファイル ----
sizes = {'nairobi-balcony-bar-v1.png': (1536, 960), 'nairobi-balcony-bar-lights-strip.png': (6144, 960), 'nairobi-balcony-bar-curtain-strip.png': (384, 490), 'npc/tk-bartender.png': (135, 278)}
chk('素材ファイルが tour/assets/art 配下にあり大きさが仕様どおり(背景1536×960・lights 6144×960・curtain 384×490・バーテンダー135×278)', all(os.path.exists(os.path.join(ART, f)) and Image.open(os.path.join(ART, f)).size == sz for f, sz in sizes.items()), {f: Image.open(os.path.join(ART, f)).size for f in sizes if os.path.exists(os.path.join(ART, f))})
# ---- 画面で ----
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,ART:ART,SONGSC:SONGSC,setMode:setMode,showMap:showMap,artIdFor:artIdFor};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "window.__say=[];try{speechSynthesis.speak=function(u){window.__say.push(u.text);setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));")
def canvas(p): return np.array(Image.open(io.BytesIO(base64.b64decode(p.evaluate("document.getElementById('sceneA').toDataURL('image/png')").split(',')[1]))).convert('RGB')).astype(int)
def msgt(p): return p.evaluate("document.querySelector('#msgText').innerText").strip()
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
def newpage(br):
    ctx = br.new_context(viewport={'width': 430, 'height': 900}, device_scale_factor=1); pg = ctx.new_page(); pg.add_init_script(INIT); pg.route(re.compile(r'/tour/index\.html'), hooked); return pg
def go(pg):
    pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(1200); pg.mouse.click(215, 450); pg.wait_for_timeout(800)
    pg.evaluate("(function(){var T=__T;T.save.ticket='ow';['nbo_immig1','nbo_bag1','nbo_sim1','nbo_taxi1'].forEach(function(v){T.save.seen[v]=1});T.setMode('arr');T.showMap()})()"); pg.wait_for_timeout(400)
    pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1700)
def wait_map(pg, ms=20000):
    try: pg.wait_for_function("__T.G.view==='map'", timeout=ms); return True
    except Exception: return False
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--autoplay-policy=document-user-activation-required'])
    pg = newpage(br); go(pg)
    nb = pg.evaluate("JSON.parse(JSON.stringify(__T.ART.nbar))")
    chk('nbar: strips 2点が指示どおり(lights 0,0・4コマ・1536×960・step1.1／curtain 1120,88・4コマ・96×490・step1.4)', nb['strips'] == [{'img': 'nairobi-balcony-bar-lights-strip.png', 'x': 0, 'y': 0, 'n': 4, 'fw': 1536, 'fh': 960, 'step': 1.1}, {'img': 'nairobi-balcony-bar-curtain-strip.png', 'x': 1120, 'y': 88, 'n': 4, 'fw': 96, 'fh': 490, 'step': 1.4}], nb['strips'])
    chk('nbar: ストリップの1コマの大きさが実ファイルと合う(6144=1536×4・384=96×4・高さ960/490)', Image.open(os.path.join(ART, 'nairobi-balcony-bar-lights-strip.png')).size == (nb['strips'][0]['fw'] * nb['strips'][0]['n'], nb['strips'][0]['fh']) and Image.open(os.path.join(ART, 'nairobi-balcony-bar-curtain-strip.png')).size == (nb['strips'][1]['fw'] * nb['strips'][1]['n'], nb['strips'][1]['fh']))
    chk('nbar: バーテンダーの確定値(tk-bartender・x784・top350・clip500)', nb['bartender'] == {'n': 'tk-bartender', 'x': 784, 'top': 350, 'clip': 500}, nb['bartender'])
    chk('nbar: ルル 129×200(x712・足もと908)・キング 148×248(x838・足もと912)・placeholder の印なし・背景名', nb['hall']['lulu'] == {'n': 'tk-lulu-back', 'x': 712, 'by': 908, 'w': 129, 'h': 200} and nb['hall']['king'] == {'n': 'tk-king-back', 'x': 838, 'by': 912, 'w': 148, 'h': 248} and 'placeholder' not in nb and nb['bg'] == 'nairobi-balcony-bar-v1.png', nb['hall'])
    keys0 = sorted(pg.evaluate("Object.keys(localStorage)")); seen0 = pg.evaluate("JSON.stringify(__T.save.seen)")
    pg.click('button.dq:nth-child(3)'); pg.wait_for_timeout(1200)
    chk('ロビーでバーを選ぶと場面 nbo_bar1(絵 nbar・hub ではない)に入る', pg.evaluate("[__T.G.view,__T.G.scene.d.id,__T.G.scene.d.bg,!!__T.G.scene.hub,__T.artIdFor(__T.G.scene)]") == ['scene', 'nbo_bar1', 'nbar', False, 'nbar'])
    # ---- 画素: 背景・ストリップ・バーテンダー・ルル・キング ----
    bgp = np.array(Image.open(os.path.join(ART, 'nairobi-balcony-bar-v1.png')).convert('RGB')).astype(int)
    prev = np.array(Image.open(os.path.join(ROOT, 'tour-src/tests/fixtures/nairobi-balcony-bar-preview.png')).convert('RGB')).astype(int) if os.path.exists(os.path.join(ROOT, 'tour-src/tests/fixtures/nairobi-balcony-bar-preview.png')) else None
    a = canvas(pg)
    chk('画面は 1536×960 の背景として描かれる(キャンバスの大きさ)', a.shape[:2] == (960, 1536), a.shape)
    def sprite(n, w=None, h=None):
        s = Image.open(os.path.join(ART, 'npc', n + '.png')).convert('RGBA')
        if w: s = s.resize((w, h), Image.NEAREST)
        return np.array(s)
    def match(a, sp, x, by, tf=0.0, tol=12):
        h, w = sp.shape[:2]; x0 = int(x - w / 2 + .5); y0 = by - h; top = int(h * tf)
        c = a[y0 + top:y0 + h, x0:x0 + w]; s2 = sp[top:]; m = s2[..., 3] == 255
        return round(float((np.abs(c - s2[..., :3].astype(int)).sum(2)[m] <= tol).mean() * 100), 1)
    lu = sprite('tk-lulu-back', 129, 200); kg = sprite('tk-king-back', 148, 248)
    mlu = match(a, lu, 712, 908, .6); mkg = match(a, kg, 838, 912, .6)
    chk('主人公の表示サイズ: ルル 129×200・キング 148×248(腰から下の画素が素材の拡大と 90% 以上一致=その大きさで描かれている)', mlu >= 90 and mkg >= 90, (mlu, mkg))
    # 075(nroom)基準: 室内基準 = キング248・ルル200 を、素材の高さ(229/205)から決まる拡大率で置く
    chk('室内基準の高さ(ルル200・キング248)で、影を描かない(足もとの下の画素が背景のまま)', float((np.abs(a[909:914, 690:735] - bgp[909:914, 690:735]).sum(2) <= 40).mean()) > .9, 0)
    # バーテンダー: top350〜clip500 だけ・腰から下(y500より下)は描かない(背景のまま)
    bt = Image.open(os.path.join(ART, 'npc/tk-bartender.png')).convert('RGBA'); btn = np.array(bt)
    x0 = int(784 - btn.shape[1] / 2 + .5)
    upper = a[352:498, x0:x0 + 135]; sp_up = btn[2:148]; m = sp_up[..., 3] == 255
    mb = round(float((np.abs(upper - sp_up[..., :3].astype(int)).sum(2)[m] <= 12).mean() * 100), 1)
    chk('バーテンダー: 頭〜肩(top350〜カウンター上面)が素材どおりに描かれている(一致 90% 以上。上半身は小さく揺れるので 2px 内側で比較)', mb >= 90, mb)
    below = a[502:560, x0:x0 + 135]; bg_below = bgp[502:560, x0:x0 + 135]
    chk('バーテンダー: カウンター上面(y500)より下は描かない(背景のまま 97% 以上)', float((np.abs(below - bg_below).sum(2) <= 40).mean()) > .97, float((np.abs(below - bg_below).sum(2) <= 40).mean()))
    if prev is not None:
        pm = float((np.abs(a - prev).sum(2) <= 40).mean() * 100)   # 揺れ(上半身3px)とストリップのコマ違いの分だけ差が出る
        def vsprev(sp, x, by, tf):   # 主人公の絵の画素(腰から下=揺れない)だけを、同梱プレビューと比べる(ストリップの明滅は含めない)
            h, w = sp.shape[:2]; x0 = int(x - w / 2 + .5); y0 = by - h; top = int(h * tf); m = sp[top:, :, 3] == 255
            return float((np.abs(a[y0 + top:y0 + h, x0:x0 + w] - prev[y0 + top:y0 + h, x0:x0 + w]).sum(2)[m] <= 40).mean() * 100)
        foot = min(vsprev(lu, 712, 908, .6), vsprev(kg, 838, 912, .6))
        chk('同梱プレビュー(配置の正本)との一致: 画面全体 99% 以上(揺れ・ストリップのコマ違い分を除く)・主人公の腰から下の絵 97% 以上(プレビューと同じ画素)', pm >= 99 and foot >= 97, (round(pm, 2), round(foot, 2)))
    # ストリップが動く: 時間をおくと、明かり(全画面)とカーテンの領域が変わる
    cs = [canvas(pg)]
    for _ in range(5): pg.wait_for_timeout(1200); cs.append(canvas(pg))
    curt = lambda im: im[88:578, 1120:1216]
    lights = lambda im: im[0:300, 0:1536]
    chg_c = max(int((np.abs(curt(x) - curt(cs[0])).sum(2) > 30).sum()) for x in cs[1:])
    chg_l = max(int((np.abs(lights(x) - lights(cs[0])).sum(2) > 30).sum()) for x in cs[1:])
    chk('ストリップが動く: カーテン領域・上部の明かり領域が時間で変わる(画素数)', chg_c > 50 and chg_l > 50, (chg_c, chg_l))
    pg.click('button.btn.go'); pg.wait_for_timeout(500)
    chk('GO！のあと台詞(英語)が表示・読み上げ(バーテンダーの1行目)', msgt(pg) == 'Good evening. What can I get you?' and 'Good evening. What can I get you?' in pg.evaluate("window.__say"))
    chk('場面が終わるとマップに戻る', wait_map(pg))
    said = [s_ for s_ in pg.evaluate("window.__say") if s_ in [l['en'] for l in song_data.BAR_SCENE['lines']]]
    chk('台詞は5つ・台本どおり順に読み上げられた(変更なし)', said == [l['en'] for l in song_data.BAR_SCENE['lines']], said)
    chk('エラーなし・保存の記録(save.seen)と保存キーを増やさない', pg.evaluate('window.__errs') == [] and pg.evaluate("JSON.stringify(__T.save.seen)") == seen0 and sorted(pg.evaluate("Object.keys(localStorage)")) == keys0, (seen0, keys0))
    pg.context.close()
    # ---- チェックモード ----
    pg = newpage(br); pg.goto(base + '/tour/index.html?check=1'); pg.wait_for_timeout(1500)
    try: pg.mouse.click(215, 450); pg.wait_for_timeout(800)
    except Exception: pass
    pg.click('#chkBtn'); pg.wait_for_timeout(400)
    ok = pg.evaluate("(function(){var rows=document.querySelectorAll('#chkPan .row');for(var i=0;i<rows.length;i++){var pn=rows[i].querySelector('.pn');if(pn&&pn.textContent.indexOf('[hsong]')>=0){var bs=rows[i].querySelectorAll('button');for(var j=0;j<bs.length;j++)if(bs[j].textContent==='開く'){bs[j].click();return true}}}return false})()")
    pg.wait_for_timeout(1700)
    pg.click('button.dq:nth-child(3)'); pg.wait_for_timeout(1200)
    chk('チェックモード: ロビー(hsong)からバーを選ぶと nbo_bar1(絵 nbar)に入る', ok and pg.evaluate("[__T.G.scene.d.id,__T.artIdFor(__T.G.scene)]") == ['nbo_bar1', 'nbar'])
    pg.click('button.btn.go'); pg.wait_for_timeout(400)
    chk('チェックモード: 台詞も進む・終わるとマップ・エラーなし', msgt(pg).startswith('Good evening') and wait_map(pg) and pg.evaluate('window.__errs') == [])
    pg.context.close()
    # ---- 背景が読めなくても詰まらない(いつものドットのロビーに戻る保険) ----
    pg = newpage(br); pg.route('**/nairobi-balcony-bar-v1.png', lambda r: r.abort()); go(pg); pg.click('button.dq:nth-child(3)'); pg.wait_for_timeout(1000); pg.click('button.btn.go'); pg.wait_for_timeout(400)
    chk('バーの背景が読めなくても、台詞が出て最後まで進みマップに戻る(エラーなし)', msgt(pg).startswith('Good evening') and wait_map(pg) and pg.evaluate('window.__errs') == [])
    pg.context.close()
    # ---- バーテンダーの絵だけ読めなくても詰まらない ----
    pg = newpage(br); pg.route('**/tk-bartender.png', lambda r: r.abort()); go(pg); pg.click('button.dq:nth-child(3)'); pg.wait_for_timeout(1000); pg.click('button.btn.go'); pg.wait_for_timeout(400)
    chk('バーテンダーの絵が読めなくても、台詞が出て最後まで進みマップに戻る(エラーなし)', msgt(pg).startswith('Good evening') and wait_map(pg) and pg.evaluate('window.__errs') == [])
    pg.context.close(); br.close()
print('FAILED: %s' % bad if bad else 'ALL OK')
sys.exit(1 if bad else 0)
