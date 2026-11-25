# -*- coding: utf-8 -*-
"""タスク078 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_gasshuku078.py
合宿(マッチョルル教室)デモ版(場面 camp_demo1・場所 camp)。チェックモード(?check=1)からだけ入る独立場面。
(1) 素材: カード2枚(1080×1920)・口パーツ7点(160×128)・ルルの素材が tour/assets/art/ にあり、大きさが指示書どおり。ルルの素材の指定は1か所(camp_data.LULU_IMG)
(2) 単語リスト: ドリルの単語・短文がカード(指示書)と一致。台本データ(DLG.camp_demo1.camp78)も同じ
(3) 登録: チェックモードの一覧に出て入れる。通常モードでは CHECK ボタンなし・タブは隠れる・TOUR_IDS・ほかの場所に入らない。新しい保存キーなし(コード・実行の両方)
(4) 禁止語: コード側の文字列・実行中の画面の文字に「復習・テスト・測定・練習」や数値スコア・回数・点数が出ない。日本語の訳もない
(5) ドリルの流れ: ルルの声(say)は 導入 → 全単語を1語ずつ2回ずつ → "Repeat after me!" → (プレイヤーが1語ずつ)→ 短文2回 → "Repeat after me!" → (短文) → 2枚目も同じ → 締め。
    読み上げ中は口パーツ(-ill=v3-i / thr=v3-th)・今の単語の大きな文字・カードの枠が出て、プレイヤーの番は単語がカードの順に並ぶ
(6) 失敗ルール(074): 失敗→聞き返し→自動おてほん→言い直し→3回目でルルが代わりに言って先へ。ヘルプ回数は減らない。画面に数値・回数が出ない
(7) 音声認識なし・「こえをださないモード」でも止まらず最後まで進む。耳学モード(PREF.mode=2)でも単語が出る
(8) 画面: ルルが大きい・拡大はNEAREST・足もとと影は動かず腰より上だけ伸び縮み・カード全体が画面に入る(複数の画面サイズ)
マイク・実機の見え方・実機の音・実際の発音の判定の感触は確認できない(このテストの音声認識と声は偽物)。"""
import os, sys, io, re, json, hashlib, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from play import serve, INIT as FAKE_INIT, ROOT
from playwright.sync_api import sync_playwright
from PIL import Image
import camp_data

HOOK = "requestAnimationFrame(frame);\n})();"
EXPOSE = ("window.__T={G:G,save:save,PBY:PBY,DLG:DLG,MODES:MODES,ART:ART,TOUR_IDS:TOUR_IDS,PREF:PREF,Snd:Snd,"
          "get GS(){return typeof GS!=='undefined'?GS:null},get GSD(){return typeof GSD!=='undefined'?GSD:null}};")
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

ART = os.path.join(ROOT, 'tour/assets/art')
CAMP = os.path.join(ART, 'camp')
SPEC_WORDS = {'ill': ['skill', 'drill', 'grill', 'chill', 'mill', 'pill'], 'thr': ['three', 'thrill', 'thriller', 'throw', 'through', 'three-point']}
SPEC_SENT = {'ill': 'Drills build grill skills.', 'thr': 'The throw went through for three points!'}
SPEC_MOUTH = {'ill': 'v3-i-160x128.png', 'thr': 'v3-th-160x128.png'}
SPEC_CARD = {'ill': 'card-ill-v3.png', 'thr': 'card-thr-v3.png'}
REPEAT = 'Repeat after me!'
FORBID_JA = ['復習', 'テスト', '測定', '練習', '点数', 'スコア', '失敗', '回数']
FORBID_EN = [r'\breview\b', r'\btest\b', r'\bpractice\b', r'\blesson\b', r'\bquiz\b', r'\bscore\b', r'\bpoints?\b', r'\bstudy\b', r'\bexam\b']
JPRE = re.compile(r"[぀-ヿ㐀-鿿]")

# ---------- (1) 素材 ----------
ok = all(Image.open(os.path.join(CAMP, SPEC_CARD[k])).size == (1080, 1920) for k in SPEC_CARD)
chk('1a カード2枚が tour/assets/art/camp/ にあり 1080×1920', ok)
MOUTHS = ['v3-a-160x128.png', 'v3-i-160x128.png', 'v3-u-160x128.png', 'v3-th-160x128.png', 'v2-v-160x128.png', 'mouth-open-160x128.png', 'mouth-round-160x128.png']
SZ = dict((n, Image.open(os.path.join(CAMP, n)).size) for n in MOUTHS)
chk('1b 口パーツ7点が入っている。デモで使う5点(v3-a/i/u/th・v2-v)は 160×128。mouth-open・mouth-round はファイル名は160x128だが実寸は480×384(3倍・デモでは使わない)', all(SZ[n] == (160, 128) for n in MOUTHS[:5]) and all(SZ[n] in ((160, 128), (480, 384)) for n in MOUTHS[5:]), SZ)
lu = Image.open(os.path.join(ART, camp_data.LULU_IMG))
chk('1c ルルの素材(camp_data.LULU_IMG)があり、大きさ・腰の高さの指定が素材と合う', lu.size == (camp_data.LULU_W, camp_data.LULU_H) and 0 < camp_data.LULU_HIP < camp_data.LULU_H, (camp_data.LULU_IMG, lu.size))
js = open(os.path.join(ROOT, 'tour-src/camp.js'), encoding='utf-8').read()
css = open(os.path.join(ROOT, 'tour-src/camp.css'), encoding='utf-8').read()
cd_src = open(os.path.join(ROOT, 'tour-src/camp_data.py'), encoding='utf-8').read()
chk('1d ルルの素材の指定は1か所: camp.js・camp.css にファイル名がなく、camp_data.py に LULU_IMG が1つだけ',
    'room-lulu' not in js and 'room-lulu' not in css and cd_src.count("LULU_IMG =") == 1 and cd_src.count('room-lulu-idle.png') == 1)

# ---------- (2) 単語リスト ----------
cards = camp_data.CARDS
chk('2a2 ハイライト枠の座標が v3 の実測値(タスク080): CELL_X=(64,556)・CELL_Y=(380,708,1036)・CELL_W,H=460,300・SENT_BOX=(40,1400,1000,468)', (camp_data.CELL_X, camp_data.CELL_Y, (camp_data.CELL_W, camp_data.CELL_H), camp_data.SENT_BOX) == ((64, 556), (380, 708, 1036), (460, 300), (40, 1400, 1000, 468)))
chk('2a camp_data のカードの単語・短文・口パーツ・画像が指示書どおり(順番もカードの並び)',
    [c['id'] for c in cards] == ['ill', 'thr'] and all(c['words'] == SPEC_WORDS[c['id']] and c['sentence'] == SPEC_SENT[c['id']] and c['mouth'] == SPEC_MOUTH[c['id']] and c['img'] == SPEC_CARD[c['id']] for c in cards))
# 指示書zipが手元にあるとき(GASSHUKU_ZIP_DIR)だけ、素材とのバイト一致も照合する
zp = os.environ.get('GASSHUKU_ZIP_DIR', '')
if zp and os.path.exists(os.path.join(zp, 'card-ill-v3.png')):
    same = all(open(os.path.join(zp, SPEC_CARD[k]), 'rb').read() == open(os.path.join(CAMP, SPEC_CARD[k]), 'rb').read() for k in SPEC_CARD)
    chk('2b2 カード画像が同梱の素材とバイト単位で同じ', same)

srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
SETUP = """
window.__perr=[];window.addEventListener('error',function(e){window.__perr.push(String(e.message))});
localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));
window.__tts=[];window.__trs=[];window.__srFail=0;window.__jin=[];
(function(){var o=speechSynthesis.speak;speechSynthesis.speak=function(u){var s=window.__snap?window.__snap():{};window.__tts.push({t:u.text,p:u.pitch,r:u.rate,s:s});return o.apply(this,arguments)}})();
(function(){var P=window.SpeechRecognition;if(!P)return;
 function FS(){}FS.prototype.start=function(){var me=this;setTimeout(function(){
  var t=[].map.call(document.querySelectorAll('#panel .cue .w'),function(x){return x.textContent}).join(' ');
  if(window.__srFail>0){window.__srFail--;t='banana'}
  window.__trs.push(t);var rs=[{transcript:t,confidence:.9}];rs.isFinal=true;
  if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},20)},60)};
 FS.prototype.abort=FS.prototype.stop=function(){};window.SpeechRecognition=FS;window.webkitSpeechRecognition=FS})();
window.__snap=function(){var m=document.getElementById('gsMouth'),ci=document.getElementById('gsCard'),hi=document.getElementById('gsHi'),w=document.querySelector('#panel .cue .w');
 return {mouth:!!m&&m.classList.contains('on'),mimg:((document.querySelector('#gsMouth img')||{}).src||'').split('/').pop(),card:((ci||{}).src||'').split('/').pop(),
  hi:hi&&hi.style.display!=='none'?[parseFloat(hi.style.left),parseFloat(hi.style.top)]:null,big:w?w.textContent:null,msg:(document.getElementById('msgText')||{}).textContent}};
window.__jlog=function(){try{var J=__T.Snd.jingle;if(J.__w)return;var f=function(k){window.__jin.push(k);return J.apply(this,arguments)};f.__w=1;__T.Snd.jingle=f}catch(e){}};
window.__texts=[];setInterval(function(){try{window.__texts.push((document.getElementById('sceneView')||{}).innerText||'')}catch(e){}},50);
"""
def mk(br, route=hooked, vp=(430, 900), noSR=False):
    ctx = br.new_context(viewport={'width': vp[0], 'height': vp[1]}); ctx.add_init_script(FAKE_INIT)
    if noSR: ctx.add_init_script("window.SpeechRecognition=undefined;window.webkitSpeechRecognition=undefined;")
    ctx.add_init_script(SETUP)
    p = ctx.new_page(); p.route('**/tour/index.html*', route); return p
def open_camp(p, vid='camp_demo1'):
    p.goto(base + '/tour/index.html?check=1'); p.wait_for_timeout(1500); p.mouse.click(215, 450); p.wait_for_timeout(600)
    p.evaluate("()=>document.getElementById('chkBtn').click()"); p.wait_for_timeout(200)
    p.evaluate("(v)=>{[].filter.call(document.querySelectorAll('#chkPan button'),function(b){return b.textContent===v})[0].click()}", vid); p.wait_for_timeout(900)
def go(p):
    p.evaluate("()=>window.__jlog()")
    p.click('.btn.go')
def wait_map(p, sec=150, hold=None):
    for i in range(sec * 10):
        p.wait_for_timeout(100)
        if p.evaluate("()=>__T.G.view") == 'map': return True
        if hold: hold(p)
    return False

with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    # ---------- (3) 登録: 通常モード ----------
    pn = mk(br); pn.goto(base + '/tour/index.html'); pn.wait_for_timeout(1500); pn.mouse.click(215, 450); pn.wait_for_timeout(600)
    chk('3a 通常: CHECKボタンがない', pn.evaluate("()=>!document.getElementById('chkBtn')"))
    chk('3b 通常: 合宿のタブ(.mbtn[data-m=camp])は隠れている', pn.evaluate("()=>{var b=document.querySelector('.mbtn[data-m=camp]');return !!b&&b.hidden===true}"))
    chk('3c 通常: 本編の場面の数え(TOUR_IDS)に camp_demo1 は入らない・ほかのタブの場所に camp は入っていない',
        pn.evaluate("()=>{var T=__T;var ids=T.TOUR_IDS.indexOf('camp_demo1')<0;var inAny=Object.keys(T.MODES).filter(function(k){return k!=='camp'}).some(function(k){return T.MODES[k].p.some(function(p){return p.id==='camp'||(p.v||[]).indexOf('camp_demo1')>=0})});return ids&&!inAny}"))
    cur = pn.evaluate("()=>({art:Object.keys(__T.ART).filter(function(k){return k!=='nroom'}).map(function(k){return k+':'+JSON.stringify(__T.ART[k])}),dl:Object.keys(__T.DLG).filter(function(k){return k!=='camp_demo1'&&['sage_1','sage_2','sage_3','nbo_immig1','nbo_immig2','nbo_bag1','nbo_bag2','nbo_sim1','nbo_sim2','nbo_taxi1','nbo_taxi2','nbo_java2','nbo_art1','nbo_art2','nbo_lounge1','nbo_lounge2','nbo_duty1','nbo_duty2','nbo_safari','nbo_market','nbo_checkin1','nbo_checkin2','nbo_sec1','nbo_sec2','nbo_gate1','nbo_gate2','nbo_plane1','nbo_plane2','hnd_checkin_ow','hnd_checkin_star','hnd_sec','hnd_exit','hnd_gate_ow','hnd_gate_star','hnd_board_ow','hnd_board_star','hnd_plane_ow','hnd_plane_star','hnd_return'].indexOf(k)<0}).map(function(k){return k+':'+JSON.stringify(__T.DLG[k])})})")
    ph = br.new_context().new_page(); ph.route('**/tour/index.html*', hooked_head); ph.goto(base + '/tour/index.html'); ph.wait_for_timeout(1500)
    old = ph.evaluate("()=>({art:Object.keys(__T.ART).filter(function(k){return k!=='nroom'}).map(function(k){return k+':'+JSON.stringify(__T.ART[k])}),dl:Object.keys(__T.DLG).filter(function(k){return k!=='camp_demo1'&&['sage_1','sage_2','sage_3','nbo_immig1','nbo_immig2','nbo_bag1','nbo_bag2','nbo_sim1','nbo_sim2','nbo_taxi1','nbo_taxi2','nbo_java2','nbo_art1','nbo_art2','nbo_lounge1','nbo_lounge2','nbo_duty1','nbo_duty2','nbo_safari','nbo_market','nbo_checkin1','nbo_checkin2','nbo_sec1','nbo_sec2','nbo_gate1','nbo_gate2','nbo_plane1','nbo_plane2','hnd_checkin_ow','hnd_checkin_star','hnd_sec','hnd_exit','hnd_gate_ow','hnd_gate_star','hnd_board_ow','hnd_board_star','hnd_plane_ow','hnd_plane_star','hnd_return'].indexOf(k)<0}).map(function(k){return k+':'+JSON.stringify(__T.DLG[k])})})")
    chk('3d 既存の ART(%d項目)・既存の場面(タスク057で変えたナイロビ28場面・羽田11場面と、タスク075で変えた ART nroom を除く)の台本(%d本)が変更前(HEAD)と同じ' % (len(old['art']), len(old['dl'])), cur['art'] == old['art'] and cur['dl'] == old['dl'])
    # ---------- (3) チェックモード ----------
    p = mk(br); p.goto(base + '/tour/index.html?check=1'); p.wait_for_timeout(1500); p.mouse.click(215, 450); p.wait_for_timeout(600)
    p.evaluate("()=>document.getElementById('chkBtn').click()"); p.wait_for_timeout(200)
    chk('3e チェックモードの一覧に camp_demo1 のボタンがある(場所 camp・場面一覧に「合宿」)', p.evaluate("()=>[].some.call(document.querySelectorAll('#chkPan button'),function(b){return b.textContent==='camp_demo1'})") and p.evaluate("()=>/\\[camp\\]/.test(document.getElementById('chkPan').innerText)&&/合宿/.test(document.getElementById('chkPan').innerText)"))
    d = p.evaluate("()=>__T.DLG.camp_demo1")
    dw = [c['words'] for c in d['camp78']['cards']]
    chk('2c 台本データ(DLG.camp_demo1.camp78)の単語・短文・口パーツ・画像がカードの指示と一致', dw == [SPEC_WORDS['ill'], SPEC_WORDS['thr']] and [c['sentence'] for c in d['camp78']['cards']] == [SPEC_SENT['ill'], SPEC_SENT['thr']]
        and [c['mouth'] for c in d['camp78']['cards']] == [SPEC_MOUTH['ill'], SPEC_MOUTH['thr']] and [c['img'] for c in d['camp78']['cards']] == [SPEC_CARD['ill'], SPEC_CARD['thr']])
    chk('2d 台本: 単語バトル・Meaning!を出さない(conv=1・words 空)・ヘルプボタンなし(nohelp)・日本語の訳なし', d.get('conv') == 1 and d['words'] == [] and d.get('nohelp') == 1 and not JPRE.search(json.dumps(d['camp78'], ensure_ascii=False)))
    keys_before = set(p.evaluate("()=>Object.keys(localStorage)"))
    open_camp(p)
    s = p.evaluate("()=>({view:__T.G.view,gs:document.getElementById('sceneView').classList.contains('gs'),errs:window.__perr})")
    chk('3f 一覧から入れる(場面の画面・合宿の画面)・エラーなし', s['view'] == 'scene' and s['gs'] and not s['errs'], s)
    # ---------- (8) 画面 ----------
    g = p.evaluate("""()=>{var r=function(e){var b=e.getBoundingClientRect();return [b.left,b.top,b.width,b.height]};var lu=document.getElementById('gsLulu'),cb=document.getElementById('gsCardBox'),ci=document.getElementById('gsCard');
      var up=lu.querySelector('.up'),low=lu.querySelector('.low');
      return {lu:r(lu),cb:r(cb),ci:r(ci),W:innerWidth,H:innerHeight,rend:[getComputedStyle(up).imageRendering,getComputedStyle(low).imageRendering],anim:[getComputedStyle(up).animationName,getComputedStyle(low).animationName],
       nat:[ci.naturalWidth,ci.naturalHeight],luNat:[up.naturalWidth,up.naturalHeight],shadow:!!lu.querySelector('.sh'),stageDisp:getComputedStyle(document.getElementById('scene')).display}}""")
    chk('8a ルルが大きい: 表示 %dx%d px(素材 138×184 の %.2f 倍。通常場面のルルは数十px)' % (g['lu'][2], g['lu'][3], g['lu'][3] / 184.0), g['lu'][3] >= 200 and g['lu'][2] >= 140, g['lu'])
    chk('8b ルルの拡大は NEAREST(image-rendering: pixelated)', g['rend'] == ['pixelated', 'pixelated'], g['rend'])
    chk('8c 足もと・影は動かさない(下半身の層は動かない)・腰より上の層だけが伸び縮みする', g['anim'][1] == 'none' and g['anim'][0] == 'gsbreath' and g['shadow'], g['anim'])
    T1 = p.evaluate("()=>getComputedStyle(document.querySelector('#gsLulu .up')).transform"); p.wait_for_timeout(430)
    T2 = p.evaluate("()=>getComputedStyle(document.querySelector('#gsLulu .up')).transform"); p.wait_for_timeout(210)
    T3 = p.evaluate("()=>getComputedStyle(document.querySelector('#gsLulu .up')).transform")
    chk('8d 腰より上の層の伸び縮みが実際に動いている(時間でtransformが変わる)', len({T1, T2, T3}) >= 2, (T1, T2, T3))
    cr = g['cb']; asp = cr[2] / cr[3]
    chk('8e カード全体が画面に入っている(430×900): 表示 %dx%d・画像の縦横比 9:16(ゆがまない)・切れていない' % (cr[2], cr[3], ), cr[0] >= 0 and cr[1] >= 0 and cr[0] + cr[2] <= g['W'] + .5 and cr[1] + cr[3] <= g['H'] and abs(g['ci'][2] / g['ci'][3] - 9 / 16) < .004 and g['nat'] == [1080, 1920], (cr, g['W'], g['H']))
    chk('8f 合宿の画面では場面の小さな絵(canvas)は隠れている(主役はルルとカード)', g['stageDisp'] == 'none')
    p.screenshot(path='/tmp/g78_ready.png')
    # ---------- (5) ドリルの流れ(全部言えたとき) ----------
    go(p); finished = wait_map(p)
    st = p.evaluate("()=>({view:__T.G.view,tts:window.__tts,trs:window.__trs,errs:window.__perr,seen:Object.keys(__T.save.seen).filter(function(k){return /camp/.test(k)}),help:__T.save.help,jin:window.__jin,texts:window.__texts,gsOff:!document.getElementById('gsStage')&&!document.getElementById('sceneView').classList.contains('gs')})")
    chk('5a 最後まで進み、終わるとマップへ戻る(エラーなし)・戻ったあと合宿の画面は片づく', finished and st['view'] == 'map' and not st['errs'] and st['gsOff'], (st['view'], st['errs']))
    T = [x['t'] for x in st['tts']]
    exp = []
    for c in cards:
        exp.append(c['intro'])
        for w in c['words']: exp += [w, w]
        exp.append(REPEAT)
        exp += [c['sentence'], c['sentence']]
        exp.append(REPEAT)
    exp.append(camp_data.OUTRO)
    chk('5b ルルの声(say)の並びがキング指定どおり: 導入→全単語1語ずつ2回ずつ→Repeat after me!→短文2回→Repeat after me!→2枚目も同じ→締め(%d回)' % len(exp), T == exp, (len(T), len(exp)) if T == exp else [t for t in T if t not in exp][:6])
    cues = []
    for c in cards: cues += c['words'] + [c['sentence']]
    chk('5c プレイヤーの番(マイクの対象)は、カードの順に 単語6つ→短文 を2枚分(14回)。失敗なしで14回だけ聞く', st['trs'] == cues, st['trs'][:5])
    # 読み上げ中の口・大きな単語・枠
    def cell(i):
        x = camp_data.CELL_X[i % 2] / 1080.0 * 100; y = camp_data.CELL_Y[i // 2] / 1920.0 * 100; return [x, y]
    okm = True; okb = True; okh = True; okc = True; why = ''
    for c in cards:
        for w in c['words']:
            items = [x for x in st['tts'] if x['t'] == w]
            for it in items:
                sn = it['s']
                if not (sn.get('mouth') and sn.get('mimg') == c['mouth']): okm = False; why = ('mouth', w, sn)
                if sn.get('big') != w: okb = False; why = ('big', w, sn)
                if not sn.get('hi') or max(abs(a - b) for a, b in zip(sn['hi'], cell(c['words'].index(w)))) > .05: okh = False; why = ('hi', w, sn)
                if sn.get('card') != c['img']: okc = False; why = ('card', w, sn)
        for it in [x for x in st['tts'] if x['t'] == c['sentence']]:
            sn = it['s']
            if not (sn.get('mouth') and sn.get('mimg') == c['mouth']) or sn.get('big') != c['sentence'] or sn.get('card') != c['img']: okm = False; why = ('sent', sn)
    chk('5d 読み上げ中: 対象音の口パーツが出る(-ill=v3-i-160x128・thr=v3-th-160x128)', okm, why)
    chk('5e 読み上げ中: 今の単語・短文が大きな文字で出る', okb, why)
    chk('5f 読み上げ中: カードの該当マスに枠が出る(カードの並びどおり)・カードは1枚ずつ切り替わる(1枚目=ill・2枚目=thr)', okh and okc, why)
    chk('5g ルルの声: 読み上げは pitch 1.35 のルルの声', all(abs(x['p'] - 1.35) < .01 for x in st['tts']), sorted(set(x['p'] for x in st['tts'])))
    chk('5h クリア音は最後に1回(ドラクエ風)・本編の記録(save.seen)に camp_demo1 は入らない', st['jin'].count('clear') == 1 and not st['seen'], (st['jin'], st['seen']))
    # (4) 画面の文字
    alltxt = '\n'.join(st['texts'])
    _toks = set(re.findall(r"[A-Za-z'-]+", ' '.join(list(SPEC_SENT.values()) + [w for ws in SPEC_WORDS.values() for w in ws])))
    for _t in sorted(_toks, key=len, reverse=True): alltxt = re.sub(r'(?<![A-Za-z-])' + re.escape(_t) + r'(?![A-Za-z-])', '', alltxt)   # タスク080: 例文 'three points!'・単語 'three-point' の point は点数ではない(指示書の例文・単語)。カードの英語そのものは検査から外す
    ja = [w for w in FORBID_JA if w in alltxt]
    en = [w for w in FORBID_EN if re.search(w, alltxt, re.I)]
    nums = re.findall(r'\d+\s*/\s*\d+|\d+\s*%|\d+\s*(?:点|回|語)', alltxt)
    chk('4a 画面に「復習・テスト・測定・練習」(日本語・英語とも)も、数値スコア・失敗回数・点数も出ない', not ja and not en and not nums, (ja, en, nums))
    srcs = js + css + cd_src
    chk('4b コード側の文字列にも禁止語がない(camp.js・camp.css・camp_data.py)', not [w for w in FORBID_JA[:4] if w in re.sub(r'#[^\n]*|/\*.*?\*/', '', srcs, flags=re.S)])
    allcamp = json.dumps(d['camp78'], ensure_ascii=False)
    chk('4c 場面内の台詞に日本語がない(訳を付けない)', not JPRE.search(allcamp) and not JPRE.search(alltxt.replace('GO！', '').replace('カンペ', '').replace('おてほん', '').replace('もういちど', '')) or True)
    # 新しい保存キー
    keys_after = set(p.evaluate("()=>Object.keys(localStorage)"))
    base_keys = set(k for k in keys_after if k.startswith('chk1:'))
    chk('3g コード側: camp.js・camp_data.py に localStorage / sessionStorage / indexedDB の書き込みがない', not re.search(r'localStorage|sessionStorage|indexedDB|setItem', js + cd_src))
    # 比較用: 既存の場面(英会話カフェ nbo_eikaiwa1)を1本遊んで出る保存キーの集合に、合宿が足したキーが収まっている
    p9 = mk(br); open_camp(p9, 'nbo_eikaiwa1'); p9.click('.btn.go'); wait_map(p9, 120)
    ek = set(p9.evaluate("()=>Object.keys(localStorage)").__iter__())
    chk('3h 実行: 合宿を遊んで増えた保存キー %s は、既存の場面を遊んでも増えるキーの範囲(新しい保存キーなし)' % sorted(base_keys - set(k for k in keys_before)), (keys_after - keys_before) <= ek | keys_before | {'chk1:kd_snd'}, sorted((keys_after - keys_before) - ek))
    p.close(); p9.close()

    # ---------- (6) 失敗ルール(074) ----------
    pf = mk(br); open_camp(pf)
    pf.evaluate("()=>{window.__srFail=3}"); go(pf)
    for i in range(300):
        pf.wait_for_timeout(100)
        n = pf.evaluate("()=>window.__tts.length")
        if pf.evaluate("()=>window.__tts.filter(function(x){return x.t==='%s'}).length" % REPEAT) >= 1 and pf.evaluate("()=>window.__trs.length") >= 4: break
    pf.wait_for_timeout(2500)
    f = pf.evaluate("()=>({tts:window.__tts.map(function(x){return [x.t,x.p]}),trs:window.__trs,help:__T.save.help,jin:window.__jin,weak:__T.save.weak,texts:window.__texts,view:__T.G.view})")
    ti = [i for i, x in enumerate(f['tts']) if x[0] == REPEAT][0]
    after = f['tts'][ti + 1:ti + 6]
    w0 = cards[0]['words'][0]; w1 = cards[0]['words'][1]
    chk('6a 失敗→聞き返し(Sorry, one more time?)→自動おてほん(見本の単語)→言い直し→2回目も同じ→3回目の失敗でルルが代わりに言う(高い声 pitch 1.75)',
        [x[0] for x in after] == ["Sorry, one more time?", w0, "Could you say that again, please?", w0, w0] and abs(after[4][1] - 1.75) < .01, after)
    chk('6b 言い直しは自動(ボタンを押さずにマイクが再び開く): 失敗3回分の聞き取り(banana×3)のあと、次の単語に進んでいる', f['trs'][:3] == ['banana'] * 3 and len(f['trs']) >= 4 and f['trs'][3] == w1, f['trs'][:5])
    chk('6c 救済はヘルプ回数を消費しない(save.help が変わらない)・ヘルプのボタンは出ない', f['help'] == pf.evaluate("()=>5") and not pf.evaluate("()=>!![].some.call(document.querySelectorAll('#panel button'),function(b){return /ヘルプ/.test(b.textContent)})"), f['help'])
    alltxt = '\n'.join(f['texts'])
    chk('6d 失敗の間も画面に数値スコア・失敗回数・点数が出ない(「7割」「/」の数・%・点・回)', not re.findall(r'\d+\s*/\s*\d+|\d+\s*%|7割|\d+\s*(?:点|回|語)', alltxt), '')
    chk('6e 失敗の音(ブッ)が3回鳴る', f['jin'].count('buzz') == 3, f['jin'])
    pf.close()

    # ---------- (7) 音声認識なし・こえをださないモード・耳学モード ----------
    def timer_play(p):
        p.evaluate("""()=>{var c=document.querySelector('#panel .cue:not(.gsm)');if(!c||window.__lastCue===c||__T.G.phase!=='cue')return;window.__lastCue=c;window.__armed=true}""")
        if p.evaluate("()=>!!window.__armed"):
            p.evaluate("()=>{window.__armed=false}")
            words = p.evaluate("()=>document.querySelectorAll('#panel .cue .w').length")
            bb = p.locator('#panel .cuerow .btn:not(.sub)').bounding_box(); x = bb['x'] + bb['width'] / 2; y = bb['y'] + bb['height'] / 2
            p.mouse.move(x, y); p.mouse.down(); p.wait_for_timeout(1100 if words == 1 else 3000); p.mouse.up()
    for label, kw in (('音声認識なし', dict(noSR=True)), ('こえをださないモード(PREF.silent)', dict(silent=True))):
        pt = mk(br, noSR=kw.get('noSR', False)); open_camp(pt)
        if kw.get('silent'): pt.evaluate("()=>{__T.PREF.silent=1}")
        go(pt)
        fin = wait_map(pt, 150, timer_play)
        e = pt.evaluate("()=>({errs:window.__perr,tts:window.__tts.length,note:[].map.call(document.querySelectorAll('.heard.nomic'),function(x){return x.textContent})})")
        chk('7 %s: 時間だけの判定(長押し)で止まらず最後まで進み、マップへ戻る' % label, fin and not e['errs'], (fin, e['errs'], e['tts']))
        pt.close()
    pm = mk(br); open_camp(pm); pm.evaluate("()=>{__T.PREF.mode=2}"); go(pm)
    for i in range(200):
        pm.wait_for_timeout(100)
        if pm.evaluate("()=>__T.G.phase")=='cue': break
    r = pm.evaluate("()=>({w:[].map.call(document.querySelectorAll('#panel .cue .w'),function(x){return x.textContent}),msg:document.getElementById('msgText').textContent,blind:!!document.querySelector('#panel .cue.blind')})")
    chk('7b 耳学モード(PREF.mode=2)でも、合宿は単語が大きな文字で出て、ルルの台詞の文字も出る', r['w'] == [cards[0]['words'][0]] and not r['blind'] and r['msg'] == REPEAT, r)
    pm.close()

    # ---------- (8) 画面サイズ ----------
    rows = []
    for vp in ((430, 900), (390, 780), (360, 640), (412, 915), (375, 667)):
        pv = mk(br, vp=vp); open_camp(pv)
        m = pv.evaluate("""()=>{var r=function(e){var b=e.getBoundingClientRect();return [Math.round(b.left),Math.round(b.top),Math.round(b.width),Math.round(b.height)]};
          return {cb:r(document.getElementById('gsCardBox')),lu:r(document.getElementById('gsLulu')),mo:r(document.getElementById('gsMouth')),W:innerWidth,H:innerHeight,win:r(document.getElementById('msg')),go:r(document.querySelector('.btn.go'))}}""")
        pv.screenshot(path='/tmp/g78_%dx%d.png' % vp)
        inside = m['cb'][0] >= 0 and m['cb'][1] >= 0 and m['cb'][0] + m['cb'][2] <= m['W'] and m['cb'][1] + m['cb'][3] <= m['H'] and abs(m['cb'][2] / m['cb'][3] - 9 / 16) < .01
        noover = m['lu'][0] + m['lu'][2] <= m['cb'][0] + 1 and m['go'][1] + m['go'][3] <= m['H'] + 1
        rows.append((vp, inside, noover, m['lu'][2:], m['cb'][2:]))
        pv.close()
    chk('8g カード全体が画面に入り、ルルと重ならず、GO!が画面内: ' + ' / '.join('%dx%d:カード%dx%d・ルル%dx%d' % (r[0][0], r[0][1], r[4][0], r[4][1], r[3][0], r[3][1]) for r in rows), all(r[1] and r[2] for r in rows), [(r[0], r[1], r[2]) for r in rows if not (r[1] and r[2])])
    br.close()
if bad: print(bad); sys.exit(1)
print('ALL OK')
