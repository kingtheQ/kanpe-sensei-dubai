# -*- coding: utf-8 -*-
"""タスク077 の動作確認(ヘッドレス)。使い方: python3 -I tour-src/tests/test_lobby077.py
ロビーの3択を行き先につなぐ: (1)プール=実在の場面 nbo_pool1(聞くだけ型・静かなプール npoolq・歌手と観客なし・終わるとマップへ)(2)既存 npool の定義は不変
(3)バー=枠組みのみ(nbo_bar1・nbar・台本データ・PLACEHOLDER)。素材待ち(BAR_READY=False)の間は一言→メニューに戻り、壊れた場面へは行かない。印を True にすると nbo_bar1 が最後まで動く(枠組みの確認)
(4)メニューは3択+「マップに もどる」の4ボタンのまま (5)チェックモード(?check=1)でもロビーからプール場面まで辿れる (6)保存キー・保存の記録を増やさない
実機の見え方・読み上げの聞こえ方は確認できない(未確認)。"""
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
JA = re.compile(r'[぀-ヿ一-鿿]')
# ---- データ ----
P = song_data.POOL_SCENE
chk('プール場面 nbo_pool1: 絵は npoolq・聞くだけ(マイク等の設定なし)', P['id'] == 'nbo_pool1' and P['bg'] == 'npoolq' and not any(k in P for k in ('mic', 'cue', 'words', 'battle')), P['id'])
chk('プール台本: 入り(日本語1行)+英語4行・指示書077どおり', P['intro'] == '夜のプールサイド。ショーのない時間は静かで、水が光っている。' and [(l['w'], l['en']) for l in P['lines']] == [('lulu', 'Look at the water. It is so quiet now.'), ('king', 'The pool looks beautiful at night.'), ('lulu', "Let's sit here for a while."), ('king', 'Good idea. What a long day.')])
chk('プール台本: 日本語は入りの1行だけ(台詞は英語のみ)', all(JA.search(l['en']) is None for l in P['lines']))
B = song_data.BAR_SCENE
chk('バー場面 nbo_bar1 の定義・台本(指示書077どおり)', B['id'] == 'nbo_bar1' and B['bg'] == 'nbar' and B['intro'] == 'ホテルのバルコニーバル。街の明かりが見える。' and [(l['w'], l['en']) for l in B['lines']] == [('bartender', 'Good evening. What can I get you?'), ('king', 'A mango juice, please.'), ('bartender', 'Here you are. Enjoy the view.'), ('lulu', 'Look at the city lights, King.'), ('king', 'Thank you. What a beautiful night.')])
chk('バー台本: 値段なし・酒でなくジュース・日本語は入りだけ', all(not re.search(r'\d|\$|KES|beer|wine|cocktail', l['en'], re.I) and JA.search(l['en']) is None for l in B['lines']) and 'juice' in B['lines'][1]['en'])
chk('バーの切り替えの印は1か所(song_data.BAR_READY)・いまは False(素材待ち)', song_data.BAR_READY is False)
chk('メニューは3択のまま(英文だけ)・行き先の名前も変えていない', [m[0] for m in song_data.LOBBY_HUB['menu']] == ['See the evening show', 'The swimming pool', 'The Balcony Bar'] and [m[1] for m in song_data.LOBBY_HUB['menu']] == ['nbo_show', 'nbo_pool', 'nbo_bbar'])
chk('スタッフの一言: バーは素材待ちの仮置きとして残る・プールの一言は使わない(場面ができた)', 'nbo_bbar' in song_data.LOBBY_HUB['lines'] and 'nbo_pool' not in song_data.LOBBY_HUB['lines'])
ar = open(os.path.join(ROOT, 'tour-src/art.js'), encoding='utf-8').read()
nb = ar[ar.index(' nbar:{'):ar.index('/* 機内の対面アップ(タスク048)')]
chk('art nbar: 背景は予定名 nairobi-balcony-bar-v1.png・PLACEHOLDER の印・バーテンダー座標は決め打ちしない(null)', "bg:'nairobi-balcony-bar-v1.png'" in nb and 'PLACEHOLDER' in nb and re.search(r'bartender:\{n:null,x:null,top:null,clip:null\}', nb) is not None)
chk('バーの背景ファイルはまだ存在しない(素材待ち)・リポジトリに仮の絵を置いていない', not os.path.exists(os.path.join(ROOT, 'tour/assets/art/nairobi-balcony-bar-v1.png')))
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
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,SONG:SONG,PBY:PBY,ART:ART,SONGSC:SONGSC,setMode:setMode,showMap:showMap,artIdFor:artIdFor};" + HOOK, 1))
INIT = ("window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});"
        "window.__au=[];(function(){var P=HTMLMediaElement.prototype,pl=P.play;P.play=function(){window.__au.push(['play',(this.src||'').split('/').pop().slice(0,22)]);return pl.apply(this,arguments)}})();"
        "window.__say=[];try{speechSynthesis.speak=function(u){window.__say.push(u.text);setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}"
        "try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}"
        "localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));")
def canvas(p): return Image.open(io.BytesIO(base64.b64decode(p.evaluate("document.getElementById('sceneA').toDataURL('image/png')").split(',')[1]))).convert('RGB')
def msgt(p): return p.evaluate("document.querySelector('#msgText').innerText").strip()
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
ART = os.path.join(ROOT, 'tour/assets/art')
def newpage(br, init=INIT):
    ctx = br.new_context(viewport={'width': 430, 'height': 900}, device_scale_factor=1); pg = ctx.new_page(); pg.add_init_script(init); pg.route(re.compile(r'/tour/index\.html'), hooked); return pg
def go(pg, url='/tour/index.html'):
    pg.goto(base + url); pg.wait_for_timeout(1200); pg.mouse.click(215, 450); pg.wait_for_timeout(800)
    pg.evaluate("(function(){var T=__T;T.save.ticket='ow';['nbo_immig1','nbo_bag1','nbo_sim1','nbo_taxi1'].forEach(function(v){T.save.seen[v]=1});T.setMode('arr');T.showMap()})()"); pg.wait_for_timeout(400)
    pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1700)
def nbtn(pg): return pg.evaluate("document.querySelectorAll('button.dq').length")
def wait_map(pg, ms=15000):
    try: pg.wait_for_function("__T.G.view==='map'", timeout=ms); return True
    except Exception: return False
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--autoplay-policy=document-user-activation-required'])
    pg = newpage(br); go(pg)
    seen0 = pg.evaluate("JSON.stringify(__T.save.seen)"); keys0 = sorted(pg.evaluate("Object.keys(localStorage)"))
    chk('メニューは3択+「マップに もどる」の4ボタン', nbtn(pg) == 4 and pg.evaluate("Array.from(document.querySelectorAll('button.dq')).map(function(b){return b.innerText.replace('▶','').replace('✓','').trim()})") == ['See the evening show', 'The swimming pool', 'The Balcony Bar', 'マップに もどる'])
    # 既存 npool の定義は不変
    npool = pg.evaluate("JSON.parse(JSON.stringify(__T.ART.npool))")
    chk('既存 npool の定義は変えていない(stage の歌手 x=790・by=734、観客5人、ルル・キング、2ストリップ)', npool['stage']['singer']['x'] == 790 and npool['stage']['singer']['by'] == 734 and len(npool['stage']['people']) == 5 and (npool['stage']['lulu']['x'], npool['stage']['king']['x']) == (712, 838) and len(npool['strips']) == 2 and npool['bg'] == 'nairobi-pool-v2.png')
    # ---- バー(素材待ち): 一言→メニュー ----
    pg.click('button.dq:nth-child(3)'); pg.wait_for_timeout(600)
    chk('バー(素材待ち): スタッフの一言(英文)を表示・読み上げ・メニューに戻る(場面には入らない)', 'Balcony Bar has a lovely view' in msgt(pg) and any('Balcony Bar has a lovely view' in s_ for s_ in pg.evaluate("window.__say")) and nbtn(pg) == 4 and pg.evaluate("[__T.G.view,!!__T.G.scene.hub,__T.G.scene.d.id||null]") == ['scene', True, None])
    chk('バー(素材待ち): エラーなし・もう一度選んでも同じ(壊れた場面に遷移しない)', (pg.click('button.dq:nth-child(3)'), pg.wait_for_timeout(500))[0] is None and pg.evaluate('window.__errs') == [] and nbtn(pg) == 4 and not pg.evaluate("__T.G.scene.d.id"))
    # ---- プール: 実在の場面 ----
    pg.click('button.dq:nth-child(2)'); pg.wait_for_timeout(900)
    chk('プール: 場面 nbo_pool1 に入る(ロビーの hub のままではない)', pg.evaluate("[__T.G.view,__T.G.scene.d.id,__T.G.scene.d.bg,!!__T.G.scene.hub,__T.G.phase]") == ['scene', 'nbo_pool1', 'npoolq', False, 'listen'], pg.evaluate("[__T.G.scene.d.id,__T.G.scene.hub]"))
    chk('プール: 入りの1行(日本語)が出て、曲・歌手の場面ではない', '夜のプールサイド' in msgt(pg) and pg.evaluate("__T.SONG.el") is None and pg.evaluate("__T.artIdFor(__T.G.scene)") == 'npoolq')
    q = pg.evaluate("JSON.parse(JSON.stringify(__T.ART.npoolq))")
    chk('art npoolq: 歌手・観客(stage)なし・ルルとキングだけ(npool の足もと基準 712/886・838/890)・2ストリップ・背景は同じ', 'stage' not in q and 'sage' not in q['hall'] and set(q['hall'].keys()) == {'lulu', 'king'} and (q['hall']['lulu']['x'], q['hall']['lulu']['by'], q['hall']['king']['x'], q['hall']['king']['by']) == (712, 886, 838, 890) and q['bg'] == 'nairobi-pool-v2.png' and q['strips'] == npool['strips'], q)
    im = canvas(pg); im.save('/tmp/pool077.png'); a_ = np.array(im).astype(int)
    def frac(n, x, by, tf=0.0):   # tf = 素材の上から何割より下を比べるか(0.8 = 足もと側の2割。腰から下は揺れない)
        s_ = Image.open(os.path.join(ART, 'npc', n + '.png')).convert('RGBA'); x0 = int(x - s_.width / 2 + .5); y0 = by - s_.height; top = int(s_.height * tf); h = s_.height - top
        c = a_[y0 + top:y0 + top + h, x0:x0 + s_.width]; sp_ = np.array(s_)[top:top + h]; m = sp_[..., 3] == 255
        return round(float((np.abs(c - sp_[..., :3].astype(int)).sum(2)[m] <= 12).mean() * 100), 1)
    sing = frac('s-stand-front', 790, 734); aud = [frac(n, x, by) for n, x, by in [('b-back-maasai', 1142, 856), ('b-back-safari', 462, 864), ('b-back-backpacker', 1064, 868), ('b-back-thobe', 585, 900), ('b-back-dashiki', 960, 906)]]
    lu = frac('tk-lulu-back', 712, 886, .8); kg = frac('tk-king-back', 838, 890, .8)   # 足もとの側(腰から下は揺れない)
    chk('絵: 歌手・観客は描かれず(素材との一致 30% 未満)、ルルとキングは描かれている(腰から下で 95% 以上)', sing < 30 and max(aud) < 30 and lu >= 95 and kg >= 95, (sing, aud, lu, kg))
    pg.wait_for_timeout(100)
    pg.click('button.btn.go'); pg.wait_for_timeout(500)
    chk('GO！のあと台詞(英語)が表示・読み上げ。カンペ・マイク・単語バトルの画面は出ない', msgt(pg) == 'Look at the water. It is so quiet now.' and 'Look at the water. It is so quiet now.' in pg.evaluate("window.__say") and pg.evaluate("[!!document.querySelector('.cue'),__T.G.phase]") == [False, 'listen'])
    chk('場面が終わるとマップに戻る', wait_map(pg))
    said = [s_ for s_ in pg.evaluate("window.__say") if s_ in [l['en'] for l in P['lines']]]
    chk('台詞は4つ・順に読み上げられた', said == [l['en'] for l in P['lines']], said)
    chk('曲は鳴らない・エラーなし・保存の記録(save.seen)と保存キーを増やさない', [a for a in pg.evaluate("window.__au") if a[1].startswith('song')] == [] and pg.evaluate('window.__errs') == [] and pg.evaluate("JSON.stringify(__T.save.seen)") == seen0 and sorted(pg.evaluate("Object.keys(localStorage)")) == keys0, (seen0, keys0))
    # ---- もう一度ロビーに入り、メニュー・もどる・ショーは従来どおり ----
    pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1500)
    chk('ロビーにもどれる(4ボタン)', nbtn(pg) == 4)
    pg.click('button.dq:nth-child(2)'); pg.wait_for_timeout(700); pg.click('#exitBtn'); pg.wait_for_timeout(500)
    chk('プール場面の途中でも出口ボタンでマップに戻れる', pg.evaluate("__T.G.view") == 'map')
    pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1500); pg.click('button.dq:nth-child(4)'); pg.wait_for_timeout(500)
    chk('「マップに もどる」は従来どおりマップへ', pg.evaluate("__T.G.view") == 'map')
    pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1500); pg.click('button.dq:nth-child(1)'); pg.wait_for_timeout(1500)
    chk('ショー(nbo_show)は従来どおり歌場面 nbo_song(npool)へ', pg.evaluate("[__T.G.scene.d.id,__T.artIdFor(__T.G.scene)]") == ['nbo_song', 'npool'])
    pg.click('#exitBtn'); pg.wait_for_timeout(400)
    # ---- バーの枠組み: 印を True にすると nbo_bar1 が最後まで動く(背景は素材待ちなのでドットのロビーで描く・エラーなし) ----
    pg.click('.node[data-id=hsong]'); pg.wait_for_timeout(1500); pg.evaluate("__T.SONGSC.barReady=1")
    pg.click('button.dq:nth-child(3)'); pg.wait_for_timeout(800)
    chk('(枠組みの確認)印を有効にすると、バー → 場面 nbo_bar1(絵 nbar)に入る', pg.evaluate("[__T.G.scene.d.id,__T.artIdFor(__T.G.scene)]") == ['nbo_bar1', 'nbar'] and 'バルコニーバル' in msgt(pg))
    pg.click('button.btn.go'); pg.wait_for_timeout(500)
    chk('(枠組みの確認)バーの台詞が順に出て、終わるとマップに戻る', msgt(pg) == 'Good evening. What can I get you?' and wait_map(pg, 20000))
    chk('(枠組みの確認)エラーなし', pg.evaluate('window.__errs') == [], pg.evaluate('window.__errs'))
    pg.context.close()
    # ---- チェックモードでもロビー → プール場面まで辿れる ----
    pg = newpage(br); pg.goto(base + '/tour/index.html?check=1'); pg.wait_for_timeout(1500)
    try: pg.mouse.click(215, 450); pg.wait_for_timeout(800)
    except Exception: pass
    pg.click('#chkBtn'); pg.wait_for_timeout(400)
    ok = pg.evaluate("(function(){var rows=document.querySelectorAll('#chkPan .row');for(var i=0;i<rows.length;i++){var pn=rows[i].querySelector('.pn');if(pn&&pn.textContent.indexOf('[hsong]')>=0){var bs=rows[i].querySelectorAll('button');for(var j=0;j<bs.length;j++)if(bs[j].textContent==='開く'){bs[j].click();return true}}}return false})()")
    pg.wait_for_timeout(1700)
    chk('チェックモード: 場面一覧からロビー(hsong)を開ける・3択+もどるの4ボタン', ok and nbtn(pg) == 4, ok)
    pg.click('button.dq:nth-child(2)'); pg.wait_for_timeout(900)
    chk('チェックモード: ロビーからプール場面(nbo_pool1)まで辿れる', pg.evaluate("[__T.G.scene.d.id,__T.artIdFor(__T.G.scene)]") == ['nbo_pool1', 'npoolq'])
    pg.click('button.btn.go'); pg.wait_for_timeout(400)
    chk('チェックモード: 台詞も進む・終わるとマップ・エラーなし', msgt(pg).startswith('Look at the water') and wait_map(pg) and pg.evaluate('window.__errs') == [])
    pg.context.close()
    # ---- プールの背景が読めなくても詰まらない ----
    pg = newpage(br); pg.route('**/nairobi-pool-v2.png', lambda r: r.abort()); go(pg); pg.click('button.dq:nth-child(2)'); pg.wait_for_timeout(900); pg.click('button.btn.go'); pg.wait_for_timeout(400)
    chk('プールの背景が読めなくても、台詞が出て最後まで進みマップに戻る(エラーなし)', msgt(pg).startswith('Look at the water') and wait_map(pg) and pg.evaluate('window.__errs') == [])
    pg.context.close(); br.close()
print('FAILED: %s' % bad if bad else 'ALL OK')
sys.exit(1 if bad else 0)
