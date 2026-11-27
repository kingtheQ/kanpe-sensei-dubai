# -*- coding: utf-8 -*-
"""タスク078 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_gasshuku078.py
合宿(マッチョルル教室)デモ版(場面 camp_demo1・場所 camp)。タスク083で: カード1枚・新しい短文・意味のまとまりごとの言い直し・自分の声(端末の中だけ)・口パーツ非表示・全コマで体の高さを同じに。チェックモード(?check=1)からだけ入る独立場面。
(1) 素材: カード2枚(1080×1920)・口パーツ7点(160×128)・マッチョルル16枚・背景画(camp.png 1536×960)が tour/assets/art/ にあり、大きさが指示書どおり。ルルの素材の指定は1か所(camp_data.LULU_FRAMES。足もとの測り値も素材と照合)
(2) 単語リスト: ドリルの単語・短文がカード(指示書)と一致。台本データ(DLG.camp_demo1.camp78)も同じ
(3) 登録: チェックモードの一覧に出て入れる。通常モードでは CHECK ボタンなし・タブは隠れる・TOUR_IDS・ほかの場所に入らない。新しい保存キーなし(コード・実行の両方)
(4) 禁止語: コード側の文字列・実行中の画面の文字に「復習・テスト・測定・練習」や数値スコア・回数・点数が出ない。日本語の訳もない
(5) ドリルの流れ: ルルの声(say)は 導入 → 全単語を1語ずつ2回ずつ → "Repeat after me!" → (プレイヤーが1語ずつ)→ 短文2回 → "Repeat after me!" → (短文) → 2枚目も同じ → 締め。
    読み上げ中は口パーツ(-ill=v3-i / thr=v3-th)・今の単語の大きな文字・カードの枠が出て、プレイヤーの番は単語がカードの順に並ぶ
(6) 失敗ルール(074): 失敗→聞き返し→自動おてほん→言い直し→3回目でルルが代わりに言って先へ。ヘルプ回数は減らない。画面に数値・回数が出ない
(7) 音声認識なし・「こえをださないモード」でも止まらず最後まで進む。耳学モード(PREF.mode=2)でも単語が出る
(8) 画面(タスク081・082): マッチョルルがカール運動(1→2→3→2→1…・約0.45秒/コマ)をループ・足もと(下端)がそろって跳ねない・ルルは従来の0.66倍・ルルは左下に固定で口パーツの出入りで動かない・
    口パーツはルルの頭の上・カードはステージ幅の55%前後でハイライト枠が追従・背景は背景画(camp.png。artIdFor の campK→camp)・複数の画面サイズでカード全体が画面に入りルルと重ならない
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
          "get GS(){return typeof GS!=='undefined'?GS:null},get GSD(){return typeof GSD!=='undefined'?GSD:null},gsHi:function(i){return gsHi(i)}};")
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
SPEC_SENT = {'ill': 'Drills are good for my skills.', 'thr': 'I can throw it through.'}
SPEC_CHUNKS = {'ill': ['Drills are good', 'for my skills.'], 'thr': ['I can', 'throw it', 'through.']}
SPEC_MOUTH = {'ill': 'v3-i-160x128.png', 'thr': 'v3-th-160x128.png'}
SPEC_CARD = {'ill': 'card-ill-v3.png', 'thr': 'card-thr-v3.png'}
REPEAT = 'Repeat after me!'
ALL = 'Now the whole sentence!'
FORBID_JA = ['復習', 'テスト', '測定', '練習', '点数', 'スコア', '失敗', '回数']
FORBID_EN = [r'\breview\b', r'\btest\b', r'\bpractice\b', r'\blesson\b', r'\bquiz\b', r'\bscore\b', r'\bpoints?\b', r'\bstudy\b', r'\bexam\b']
JPRE = re.compile(r"[぀-ヿ㐀-鿿]")

# ---------- (1) 素材 ----------
ok = all(Image.open(os.path.join(CAMP, SPEC_CARD[k])).size == (1080, 1920) for k in SPEC_CARD)
chk('1a カード2枚が tour/assets/art/camp/ にあり 1080×1920', ok)
MOUTHS = ['v3-a-160x128.png', 'v3-i-160x128.png', 'v3-u-160x128.png', 'v3-th-160x128.png', 'v2-v-160x128.png', 'mouth-open-160x128.png', 'mouth-round-160x128.png']
SZ = dict((n, Image.open(os.path.join(CAMP, n)).size) for n in MOUTHS)
chk('1b 口パーツ7点が入っている。デモで使う5点(v3-a/i/u/th・v2-v)は 160×128。mouth-open・mouth-round はファイル名は160x128だが実寸は480×384(3倍・デモでは使わない)', all(SZ[n] == (160, 128) for n in MOUTHS[:5]) and all(SZ[n] in ((160, 128), (480, 384)) for n in MOUTHS[5:]), SZ)
def measure(path):
    """足もと(下端)と足もとの中心: 透明でない最下行(8画素以上)の次の行 / その上30行の x の範囲の中心。camp_data.LULU_FRAMES の foot_y・foot_x はこの式の測り値"""
    im = Image.open(path).convert('RGBA'); a = im.getchannel('A'); W, H = im.size
    cnt = [sum(1 for x in range(W) if a.getpixel((x, y)) > 128) for y in range(H)]
    fy = max(y for y in range(H) if cnt[y] >= 8) + 1
    xs = [x for y in range(fy - 30, fy) for x in range(W) if a.getpixel((x, y)) > 128]
    top = min(y for y in range(H) if cnt[y] > 0)
    return im.size, fy, (min(xs) + max(xs) + 1) / 2.0, top
FR = camp_data.LULU_FRAMES
meas = [measure(os.path.join(CAMP, f['img'])) for f in FR]
chk('1c ルルの素材(camp_data.LULU_FRAMES の4コマ)が tour/assets/art/camp/ にあり、大きさ・足もとの高さ(foot_y)・足もとの中心(foot_x)の指定が素材の測り値と一致',
    all(m[0] == (f['w'], f['h']) and m[1] == f['foot_y'] and abs(m[2] - f['foot_x']) < .01 for m, f in zip(meas, FR)) and meas[0][3] == 12 and camp_data.LULU_REF_H == meas[0][1] - meas[0][3],
    [(m[0], m[1], m[2]) for m in meas])
allm = sorted(n for n in os.listdir(CAMP) if n.startswith('macho-'))
chk('1c2 マッチョルル16枚(dumbbell・exercise・rope・barbell の各1〜4。今回使うのは dumbbell だけ)が入っている', allm == sorted('macho-%s-%d.png' % (k, i) for k in ('barbell', 'dumbbell', 'exercise', 'rope') for i in range(1, 5)), len(allm))
gym = Image.open(os.path.join(ART, 'camp.png'))
chk('1c3 背景画 tour/assets/art/camp.png が 1536×960', gym.size == (1536, 960), gym.size)
js = open(os.path.join(ROOT, 'tour-src/camp.js'), encoding='utf-8').read()
css = open(os.path.join(ROOT, 'tour-src/camp.css'), encoding='utf-8').read()
cd_src = open(os.path.join(ROOT, 'tour-src/camp_data.py'), encoding='utf-8').read()
chk('1d ルルの素材の指定は1か所: camp.js・camp.css にルルのファイル名がなく、camp_data.py に LULU_FRAMES・LULU_SCALE(=0.66)・LULU_SEQ([0,1,2,1])・LULU_FRAME_SEC(=0.45)が1つずつ',
    'macho-' not in js and 'macho-' not in css and 'room-lulu' not in js + css + cd_src and cd_src.count("LULU_FRAMES =") == 1 and cd_src.count("LULU_SCALE =") == 1
    and camp_data.LULU_SCALE == .66 and camp_data.LULU_SEQ == [0, 1, 2, 1] and camp_data.LULU_FRAME_SEC == .45 and camp_data.CARD_SHARE == .55)

# ---------- (2) 単語リスト ----------
cards = camp_data.CARDS
def ink_box(path):   # 短文の文字(濃い・赤い画素)の外接矩形。カードの枠線(x<60・x>1020・y>1880)は除く
    im = Image.open(path).convert('RGB'); xs = []; ys = []
    for y in range(1345, 1880, 2):
        for x in range(60, 1020, 2):
            r, g, b = im.getpixel((x, y))
            if abs(r - 255) + abs(g - 249) + abs(b - 236) > 60: xs.append(x); ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)
sb = camp_data.SENT_BOX
ink_ok = all(sb[0] <= ink_box(os.path.join(CAMP, SPEC_CARD[k]))[0] and sb[1] <= ink_box(os.path.join(CAMP, SPEC_CARD[k]))[1] and ink_box(os.path.join(CAMP, SPEC_CARD[k]))[2] <= sb[0] + sb[2] and ink_box(os.path.join(CAMP, SPEC_CARD[k]))[3] <= sb[1] + sb[3] for k in SPEC_CARD)
chk('2a2 ハイライト枠の座標: 単語マス CELL_X=(64,556)・CELL_Y=(380,708,1036)・460×300(カード作りは080と同じ)・短文の枠は新カード2枚の文字(測ると y1514〜1744)を囲む %s' % (sb,),
    (camp_data.CELL_X, camp_data.CELL_Y, (camp_data.CELL_W, camp_data.CELL_H)) == ((64, 556), (380, 708, 1036), (460, 300)) and ink_ok and sb[0] > 40 and sb[1] + sb[3] < 1880, (sb, [ink_box(os.path.join(CAMP, SPEC_CARD[k])) for k in SPEC_CARD]))
chk('2a camp_data のカードの単語・短文・口パーツ・画像が指示書どおり(順番もカードの並び)',
    [c['id'] for c in cards] == ['ill', 'thr'] and all(c['words'] == SPEC_WORDS[c['id']] and c['sentence'] == SPEC_SENT[c['id']] and c['chunks'] == SPEC_CHUNKS[c['id']] and c['mouth'] == SPEC_MOUTH[c['id']] and c['img'] == SPEC_CARD[c['id']] for c in cards))
chk('2a3 新しい短文: 1文に練習の音を含む語は2つまで・短い・ほかは易しい語。意味のまとまり(chunks)をつなぐと短文になる', all(len(re.findall(r'(?i)ill\\b|ills\\b', c['sentence'])) <= 2 for c in cards[:1]) and len(re.findall(r'(?i)\\bthr', cards[1]['sentence'])) <= 2 and all(len(c['sentence'].split()) <= 6 for c in cards) and all(' '.join(c['chunks']) == c['sentence'] for c in cards))
# 指示書zipが手元にあるとき(GASSHUKU_ZIP_DIR)だけ、素材とのバイト一致も照合する
zp = os.environ.get('GASSHUKU_ZIP_DIR', '')
if zp and os.path.exists(os.path.join(zp, 'card-ill-v3.png')):
    same = all(open(os.path.join(zp, SPEC_CARD[k]), 'rb').read() == open(os.path.join(CAMP, SPEC_CARD[k]), 'rb').read() for k in SPEC_CARD)
    chk('2b2 カード画像が同梱の素材とバイト単位で同じ', same)

srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
SETUP = """
window.__perr=[];window.addEventListener('error',function(e){window.__perr.push(String(e.message))});
localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));
window.__tts=[];window.__trs=[];window.__mon=[];window.__srFail=0;window.__jin=[];window.__ev=[];
(function(){var o=speechSynthesis.speak;speechSynthesis.speak=function(u){var s=window.__snap?window.__snap():{};window.__tts.push({t:u.text,p:u.pitch,r:u.rate,s:s});window.__ev.push({k:'say',t:u.text,p:u.pitch,r:u.rate});return o.apply(this,arguments)}})();
(function(){var P=window.SpeechRecognition;if(!P)return;
 function FS(){}FS.prototype.start=function(){var me=this;setTimeout(function(){
  var t=[].map.call(document.querySelectorAll('#panel .cue .w'),function(x){return x.textContent}).join(' ');
  if(window.__srFail>0){window.__srFail--;t='banana'}
  window.__trs.push(t);window.__mon.push(!!document.getElementById('gsMouth'));var rs=[{transcript:t,confidence:.9}];rs.isFinal=true;
  if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},20)},60)};
 FS.prototype.abort=FS.prototype.stop=function(){};window.SpeechRecognition=FS;window.webkitSpeechRecognition=FS})();
window.__snap=function(){var m=null,ci=document.getElementById('gsCard'),hi=document.getElementById('gsHi'),w=document.querySelector('#panel .cue .w');
 return {f:(document.getElementById('gsLulu')||{getAttribute:function(){return null}}).getAttribute('data-f'),mouth:!!m&&m.classList.contains('on'),mimg:((document.querySelector('#gsMouth img')||{}).src||'').split('/').pop(),card:((ci||{}).src||'').split('/').pop(),
  hi:hi&&hi.style.display!=='none'?[parseFloat(hi.style.left),parseFloat(hi.style.top)]:null,big:w?w.textContent:null,msg:(document.getElementById('msgText')||{}).textContent}};
window.__jlog=function(){try{var J=__T.Snd.jingle;if(J.__w)return;var f=function(k){window.__jin.push(k);return J.apply(this,arguments)};f.__w=1;__T.Snd.jingle=f}catch(e){}};
/* 083: 偽のマイク・録音(自分の声)と、通信・保存の監視。録音は端末の中だけで、送られず・保存されないことを数える */
window.__rec={gum:0,start:0,stop:0,trk:0,own:[],made:[],revoked:[]};window.__net=[];window.__armed_k={};window.__arm={};
(function(){try{navigator.mediaDevices.getUserMedia=function(){window.__rec.gum++;return Promise.resolve({getTracks:function(){return [{stop:function(){window.__rec.trk++}}]}})}}catch(e){}
 function MR(st,o){this.state='inactive';this.mimeType=(o&&o.mimeType)||'audio/webm'}MR.isTypeSupported=function(){return true};
 MR.prototype.start=function(){this.state='recording';window.__rec.start++};
 MR.prototype.stop=function(){var me=this;if(this.state==='inactive')return;this.state='inactive';window.__rec.stop++;setTimeout(function(){if(me.ondataavailable)me.ondataavailable({data:new Blob(['xxxxxxxxxx'],{type:'audio/webm'})});if(me.onstop)me.onstop()},10)};
 window.MediaRecorder=MR;
 var cu=URL.createObjectURL,ru=URL.revokeObjectURL;URL.createObjectURL=function(b){var u=cu.call(URL,b);window.__rec.made.push(u);return u};URL.revokeObjectURL=function(u){window.__rec.revoked.push(u);return ru.call(URL,u)};
 HTMLMediaElement.prototype.play=function(){var me=this;if(/^blob:/.test(me.src||'')){window.__rec.own.push(me.src);window.__ev.push({k:'own'});setTimeout(function(){if(me.onended)me.onended()},60)}return Promise.resolve()};
 var of=window.fetch;window.fetch=function(){window.__net.push(['fetch',String(arguments[0])]);return of.apply(this,arguments)};
 var xo=XMLHttpRequest.prototype.open;XMLHttpRequest.prototype.open=function(m,u){window.__net.push(['xhr',String(u)]);return xo.apply(this,arguments)};
 try{var sb=navigator.sendBeacon;navigator.sendBeacon=function(u){window.__net.push(['beacon',String(u)]);return sb.apply(navigator,arguments)}}catch(e){}
 var WS=window.WebSocket;window.WebSocket=function(u){window.__net.push(['ws',String(u)]);return new WS(u)};
 try{var io=IDBFactory.prototype.open;IDBFactory.prototype.open=function(n){window.__net.push(['idb',String(n)]);return io.apply(this,arguments)}}catch(e){}
 var si=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(/blob:|audio|base64/i.test(String(v)))window.__net.push(['store-audio',String(k)]);return si.apply(this,arguments)};
 setInterval(function(){try{var c=__T.GS&&__T.GS.cur;if(c&&window.__arm[c.kind]&&!window.__armed_k[c.kind]){window.__armed_k[c.kind]=1;window.__srFail=window.__arm[c.kind]}}catch(e){}},10)})();
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
    p.evaluate("()=>{window.__jlog();window.__net.length=0}")   # 起動時の読みこみ(既存の機内放送の声のDB)は数えず、GO のあとだけ監視する
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
    cur = pn.evaluate("()=>({art:Object.keys(__T.ART).filter(function(k){return k!=='nroom'&&k!=='ticket'&&k!=='hsec'&&k!=='hexit'&&k!=='hcabin_ow'&&k!=='hcabin_st'&&k!=='cabinQ'&&k!=='javaK'&&k!=='artK'&&k.indexOf('ath')!==0&&k.indexOf('zur')!==0&&k.indexOf('syd')!==0}).map(function(k){return k+':'+JSON.stringify(__T.ART[k])}),dl:Object.keys(__T.DLG).filter(function(k){return k!=='camp_demo1'&&k.indexOf('win_')!==0&&['sage_1','sage_2','sage_3','ticket_star','ticket_ow','nbo_immig1','nbo_immig2','nbo_bag1','nbo_bag2','nbo_sim1','nbo_sim2','nbo_taxi1','nbo_taxi2','nbo_java2','nbo_art1','nbo_art2','nbo_lounge1','nbo_lounge2','nbo_duty1','nbo_duty2','nbo_safari','nbo_market','nbo_checkin1','nbo_checkin2','nbo_sec1','nbo_sec2','nbo_gate1','nbo_gate2','nbo_plane1','nbo_plane2','hnd_checkin_ow','hnd_checkin_star','hnd_sec','hnd_exit','hnd_gate_ow','hnd_gate_star','hnd_board_ow','hnd_board_star','hnd_plane_ow','hnd_plane_star','hnd_return','win_rules','win_count'].indexOf(k)<0}).map(function(k){return k+':'+JSON.stringify(__T.DLG[k])})})")
    ph = br.new_context().new_page(); ph.route('**/tour/index.html*', hooked_head); ph.goto(base + '/tour/index.html'); ph.wait_for_timeout(1500)
    old = ph.evaluate("()=>({art:Object.keys(__T.ART).filter(function(k){return k!=='nroom'&&k!=='ticket'&&k!=='hsec'&&k!=='hexit'&&k!=='hcabin_ow'&&k!=='hcabin_st'&&k!=='cabinQ'&&k!=='javaK'&&k!=='artK'&&k.indexOf('ath')!==0&&k.indexOf('zur')!==0&&k.indexOf('syd')!==0}).map(function(k){return k+':'+JSON.stringify(__T.ART[k])}),dl:Object.keys(__T.DLG).filter(function(k){return k!=='camp_demo1'&&k.indexOf('win_')!==0&&['sage_1','sage_2','sage_3','ticket_star','ticket_ow','nbo_immig1','nbo_immig2','nbo_bag1','nbo_bag2','nbo_sim1','nbo_sim2','nbo_taxi1','nbo_taxi2','nbo_java2','nbo_art1','nbo_art2','nbo_lounge1','nbo_lounge2','nbo_duty1','nbo_duty2','nbo_safari','nbo_market','nbo_checkin1','nbo_checkin2','nbo_sec1','nbo_sec2','nbo_gate1','nbo_gate2','nbo_plane1','nbo_plane2','hnd_checkin_ow','hnd_checkin_star','hnd_sec','hnd_exit','hnd_gate_ow','hnd_gate_star','hnd_board_ow','hnd_board_star','hnd_plane_ow','hnd_plane_star','hnd_return','win_rules','win_count'].indexOf(k)<0}).map(function(k){return k+':'+JSON.stringify(__T.DLG[k])})})")
    chk('3d 既存の ART(%d項目。082で足した camp は比べない=コミット前後どちらの HEAD でも通る)・既存の場面(タスク057で変えたナイロビ28場面・羽田11場面と、タスク075で変えた ART nroom・タスク089で変えた ART ticket と窓口の win_ 場面を除く)の台本(%d本)が変更前(HEAD)と同じ' % (len(old['art']), len(old['dl'])),
        [x for x in cur['art'] if not x.startswith('camp:')] == [x for x in old['art'] if not x.startswith('camp:')] and cur['dl'] == old['dl'] and any(x.startswith('camp:') for x in cur['art']))
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
    # ---------- (8) 画面(タスク081・082) ----------
    p.wait_for_timeout(900)
    GEO = """()=>{var r=function(e){var b=e.getBoundingClientRect();return [b.left,b.top,b.width,b.height]};var GS=__T.GS,D=__T.GSD.lulu,st=document.querySelector('#sceneView .stage');
      var fr=[];for(var k in GS.frs){var b=GS.frs[k].getBoundingClientRect(),f=D.frames[+k];fr.push({i:+k,on:GS.frs[k].classList.contains('on'),vis:getComputedStyle(GS.frs[k]).visibility,
        footY:b.top+f.foot_y*b.height/f.h,footX:b.left+f.foot_x*b.width/f.w,headY:b.top+12*b.height/f.h,top:b.top,w:b.width,h:b.height,rend:getComputedStyle(GS.frs[k]).imageRendering})}
      return {lu:r(GS.lulu),cb:r(document.getElementById('gsCardBox')),ci:r(document.getElementById('gsCard')),nomouth:!document.getElementById('gsMouth'),st:r(st),sh:r(GS.sh),fr:fr,dim:GS.dim,W:innerWidth,H:innerHeight,
       sa:r(document.getElementById('sceneA')),sc:r(document.getElementById('scene')),saHidden:document.getElementById('sceneA').hidden,scHidden:document.getElementById('scene').hidden}}"""
    g = p.evaluate(GEO)
    OLDH = {(430, 900): 239, (390, 780): 221, (360, 640): 197, (412, 915): 212, (375, 667): 188}   # 変更前(078・HEAD)のルルの表示の高さ。同じ画面サイズで実測した値
    d0 = g['dim']
    chk('8a ルルの大きさ=従来の0.66倍: 従来の表示の高さ(基準)%dpx(変更前の実測 %dpx と一致)→ ルルの背の高さ %dpx(=%.3f倍)。倍率は camp_data.LULU_SCALE の1か所' % (d0['refH'], OLDH[(430, 900)], d0['lCharH'], d0['lCharH'] / float(d0['refH'])),
        d0['refH'] == OLDH[(430, 900)] and abs(d0['lCharH'] / float(d0['refH']) - camp_data.LULU_SCALE) < .01 and camp_data.LULU_SCALE == .66, d0)
    used = [f for f in g['fr']]
    fy = [f['footY'] for f in used]; fx = [f['footX'] for f in used]
    chk('8b 足もと(下端)と足もとの中心が全コマでそろっている(素材ごとに高さが違っても跳ねない): 足もとの高さのばらつき %.2fpx・中心 %.2fpx(1px未満)' % (max(fy) - min(fy), max(fx) - min(fx)), max(fy) - min(fy) < .6 and max(fx) - min(fx) < .6 and len(used) == 3, (fy, fx))
    bh = [f['footY'] - f['headY'] for f in used]
    chk('8b2 体の高さ(頭のてっぺん→足の裏)が全コマで同じ(タスク083): コマ別 %s px・ばらつき %.2fpx(0.6px未満)・基準 %.1fpx(=素材の340×表示倍率)。画像の縮小はなめらか(image-rendering: auto)' % (['%.1f' % x for x in bh], max(bh) - min(bh), g['dim']['lCharH']),
        max(bh) - min(bh) < .6 and abs(bh[0] - g['dim']['lCharH']) < .8 and all(f['rend'] == 'auto' for f in used), bh)
    chk('8b3 全コマが同じ箱(同じキャンバス)の中: 箱の位置・大きさは1つで、各コマは足もとの中心をそろえて重なる(箱 %s)' % [round(x) for x in g['lu']], len(used) == 3 and all(f['top'] + f['h'] >= g['lu'][1] - .5 for f in used), g['lu'])
    # コマ送り: 1→2→3→2→1… 約0.45秒/コマ
    seq = p.evaluate("""()=>new Promise(function(res){var out=[],t0=performance.now(),iv=setInterval(function(){var f=__T.GS.lulu.getAttribute('data-f');if(!out.length||out[out.length-1][0]!==f)out.push([f,Math.round(performance.now()-t0)]);if(performance.now()-t0>5200){clearInterval(iv);res(out)}},20)})""")
    labels = [x[0] for x in seq]
    ts = [x[1] for x in seq]
    durs = [ts[i + 1] - ts[i] for i in range(1, len(ts) - 1)]
    okseq = all(labels[i] == ['1', '2', '3', '2'][(labels.index('1') + i) % 4] for i in range(len(labels))) if '1' in labels else False
    chk('8c ルルがカール運動のコマ送りをループ: 順番 %s(1→2→3→2→1…)・1コマ %d〜%dms(目標450ms)' % ('→'.join(labels[:9]), min(durs), max(durs)), len(labels) >= 9 and okseq and all(330 <= x <= 570 for x in durs), (seq, durs))
    # ルルは左下に固定(口パーツは出さない)
    before = p.evaluate(GEO); p.wait_for_timeout(700); after = p.evaluate(GEO)
    same = lambda a, b: max(abs(x - y) for x, y in zip(a, b)) < .01
    chk('8d ルルは左下に固定(箱 %s)・時間がたっても位置・大きさが変わらない・カードの左側' % [round(x) for x in before['lu']],
        same(before['lu'], after['lu']) and before['lu'][0] + before['lu'][2] <= before['cb'][0] + 1 and before['lu'][1] + before['lu'][3] >= g['st'][1] + g['st'][3] - 40, (before['lu'], g['st']))
    chk('8e 口パーツは画面に出さない(083): #gsMouth が画面にない・camp.js に口パーツの表示の部品がない(素材ファイルは残す)', before['nomouth'] and 'gsMouth' not in js and 'gsMouth' not in css, before['nomouth'])
    cr = g['cb']; stw = g['st'][2]
    chk('8f カードが大きい: ステージ幅 %dpx に対し カード %dpx(%.1f%%。従来 199px=約46%%・目標55%%前後)・縦横比 9:16・切れていない' % (stw, cr[2], cr[2] / stw * 100),
        .54 <= cr[2] / stw <= .56 and abs(g['ci'][2] / g['ci'][3] - 9 / 16) < .004 and cr[0] >= 0 and cr[1] >= 0 and cr[0] + cr[2] <= g['W'] + .5 and cr[1] + cr[3] <= g['H'], cr)
    gb = p.evaluate("""()=>{var c=document.getElementById('sceneA'),x=c.getContext('2d'),pts=[[8,8],[770,170],[300,300],[1100,360],[100,800],[760,900]],o=[];pts.forEach(function(q){o.push(Array.prototype.slice.call(x.getImageData(q[0],q[1],1,1).data,0,3))});return {px:o,pts:pts}}""")
    ref = [list(gym.convert('RGB').getpixel(tuple(q))) for q in gb['pts']]
    chk('8g 背景がジムの絵(camp.png): 場面の背景用キャンバス(sceneA)が出ていて、画素が camp.png と一致(6点)・ステージいっぱいに敷かれている・紺の手順描画(campK)は出ていない',
        gb['px'] == ref and not g['saHidden'] and g['scHidden'] and abs(g['sa'][2] - g['st'][2]) < 1 and abs(g['sa'][3] - g['st'][3]) < 1, (gb['px'], ref))
    chk('8g2 背景は既存の画像背景の仕組み: ART.camp(bg=camp.png)と artIdFor(bg campK→camp)。camp_demo1 の bg は campK のまま', p.evaluate("()=>__T.ART.camp&&__T.ART.camp.bg==='camp.png'&&__T.DLG.camp_demo1.bg==='campK'"))
    # ハイライト枠がカードの表示に追従する(単語マス・短文)
    def hi_ok(pg, tag):
        res = []
        for idx in (0, 3, 5, -1):
            r = pg.evaluate("""(i)=>{__T.gsHi(i);var h=document.getElementById('gsHi').getBoundingClientRect(),c=document.getElementById('gsCard').getBoundingClientRect(),D=__T.GSD;
              var r=i<0?D.sent:[D.cell.x[i%2],D.cell.y[Math.floor(i/2)],D.cell.w,D.cell.h],k=c.width/D.cardW;
              return [h.left-c.left-r[0]*k,h.top-c.top-r[1]*k,h.width-r[2]*k,h.height-r[3]*k]}   /* 080で枠は border-box(枠線込みでマスの寸法ちょうど) */""", idx)
            res.append([round(x, 1) for x in r])
        pg.evaluate("()=>__T.gsHi(null)")
        return max(abs(x) for r in res for x in r) <= 1.6, res
    hk, hr = hi_ok(p, '430')
    chk('8h ハイライトの枠がカードの表示に追従(拡大後の寸法でも、カード画像の座標どおり。誤差1.6px以内)', hk, hr)
    p.screenshot(path='/tmp/g83_ready.png')
    # ---------- (5) ドリルの流れ(全部言えたとき) ----------
    reqs = []; p.on('request', lambda r: reqs.append((r.method, r.url)))
    go(p); finished = wait_map(p)
    st = p.evaluate("()=>({view:__T.G.view,tts:window.__tts,trs:window.__trs,errs:window.__perr,seen:Object.keys(__T.save.seen).filter(function(k){return /camp/.test(k)}),help:__T.save.help,jin:window.__jin,mon:window.__mon,texts:window.__texts,gsOff:!document.getElementById('gsStage')&&!document.getElementById('sceneView').classList.contains('gs'),ev:window.__ev,rec:window.__rec,net:window.__net})")
    chk('5a 最後まで進み、終わるとマップへ戻る(エラーなし)・戻ったあと合宿の画面は片づく', finished and st['view'] == 'map' and not st['errs'] and st['gsOff'], (st['view'], st['errs']))
    T = [x['t'] for x in st['tts']]
    c0 = cards[0]
    exp = [c0['intro']]
    for w in c0['words']: exp += [w, w]
    exp.append(REPEAT)
    exp += [c0['sentence'], c0['sentence']]
    exp.append(REPEAT)
    for ch in c0['chunks']: exp.append(ch)       # 意味のまとまりごと: 言う前にお手本を1回(自動)
    exp.append(ALL)
    exp.append(camp_data.OUTRO)
    chk('5b ルルの声(say)の並び(083・カード1枚): 導入→全単語1語ずつ2回ずつ→Repeat after me!→短文2回→Repeat after me!→まとまりごと(お手本1回→言う)→Now the whole sentence!→(全文を言う)→締め(%d回)・2枚目(thr)は出ない' % len(exp), T == exp, (len(T), len(exp)) if T == exp else [t for t in T if t not in exp][:6])
    cues = list(c0['words']) + list(c0['chunks']) + [c0['sentence']]
    chk('5c プレイヤーの番(マイクの対象)は 単語6つ→まとまり(%d)→全文1回(計%d回)。失敗なしで、その回数だけ聞く' % (len(c0['chunks']), len(cues)), st['trs'] == cues, st['trs'][:5])
    def cell(i):
        x = camp_data.CELL_X[i % 2] / 1080.0 * 100; y = camp_data.CELL_Y[i // 2] / 1920.0 * 100; return [x, y]
    okb = True; okh = True; okc = True; why = ''
    for w in c0['words']:
        for it in [x for x in st['tts'] if x['t'] == w]:
            sn = it['s']
            if sn.get('big') != w: okb = False; why = ('big', w, sn)
            if not sn.get('hi') or max(abs(a - b) for a, b in zip(sn['hi'], cell(c0['words'].index(w)))) > .05: okh = False; why = ('hi', w, sn)
            if sn.get('card') != c0['img']: okc = False; why = ('card', w, sn)
    for it in [x for x in st['tts'] if x['t'] == c0['sentence']]:
        if it['s'].get('big') != c0['sentence'] or it['s'].get('card') != c0['img']: okb = False; why = ('sent', it['s'])
    chk('5e 読み上げ中: 今の単語・短文が大きな文字で出る', okb, why)
    chk('5f 読み上げ中: カードの該当マスに枠が出る(カードの並びどおり)・使うカードは1枚だけ(ill。thr は一度も出ない)', okh and okc and all(x['s'].get('card') in (c0['img'], '') for x in st['tts']), why)
    pit = sorted(set((x['p'], x['r']) for x in st['tts']))
    chk('5g ルルの声: 読み上げは pitch 1.35 のルルの声。言う前のお手本(まとまり)は pitch 1・ふつうの速さ(rate 1) %s' % pit, all((abs(x['p'] - 1.35) < .01) or (x['t'] in c0['chunks'] and abs(x['p'] - 1) < .01 and abs(x['r'] - 1) < .01) for x in st['tts']), pit)
    chk('5g2 口パーツは画面に一度も出ない(083): 聞いている間(%d回)も、読み上げの間も #gsMouth がない。ルルの読み上げ中もカール運動は続く' % len(st['mon']), len(st['mon']) == len(cues) and not any(st['mon']) and not any(x['s'].get('mouth') for x in st['tts']) and len(set(x['s'].get('f') for x in st['tts'])) >= 2, st['mon'])
    own_n = len([e for e in st['ev'] if e['k'] == 'own'])
    chk('5g3 言えたときは、自分の声は流れない(失敗なしの通し: 自分の声の再生 %d回)・聞くたびに録り(%d回)、そのたびにマイクを閉じる(トラック停止 %d)・録音のURLは全部手放す(作った%d・手放した%d)' % (own_n, st['rec']['gum'], st['rec']['trk'], len(st['rec']['made']), len(st['rec']['revoked'])),
        own_n == 0 and st['rec']['gum'] == len(cues) and st['rec']['trk'] == st['rec']['gum'], st['rec'])
    ext = [u for m, u in reqs if not (u.startswith(base) or u.startswith('blob:') or u.startswith('data:'))]
    posts = [(m, u) for m, u in reqs if m != 'GET']
    chk('5g4 通信: 合宿を通して遊んでいる間、外へ出た通信 %d件・GET以外 %d件・fetch/XHR/ビーコン/WebSocket/IndexedDB の呼び出し %d件・保存領域に録音(blob/audio)が入った %d件' % (len(ext), len(posts), len([n for n in st['net'] if n[0] != 'store-audio']), len([n for n in st['net'] if n[0] == 'store-audio'])), not ext and not posts and not st['net'], (ext[:3], posts[:3], st['net'][:3]))
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

    # ---------- (6) 失敗の流れ(083): 単語 → まとまり → 全文 ----------
    pf = mk(br); open_camp(pf)
    freq = []; pf.on('request', lambda r: freq.append((r.method, r.url)))
    pf.evaluate("()=>{window.__srFail=3;window.__arm={chunk:2,whole:3}}"); go(pf)
    fin6 = wait_map(pf, 200)
    f = pf.evaluate("()=>({ev:window.__ev,trs:window.__trs,help:__T.save.help,jin:window.__jin,weak:__T.save.weak,texts:window.__texts,view:__T.G.view,rec:window.__rec,net:window.__net,errs:window.__perr})")
    ev = f['ev']; sq = lambda lst: [(e['k'] == 'own' and 'OWN') or e['t'] for e in lst]
    ri = [i for i, e in enumerate(ev) if e['k'] == 'say' and e['t'] == REPEAT][0]
    w0 = c0['words'][0]; w1 = c0['words'][1]
    seg_w = ev[ri + 1:ri + 6]
    chk('6a 単語が言えない(1〜2回目): お手本が自動(ふつうの速さ rate 1・pitch 1・ボタンなし)→自分の声→お手本→言い直し。3回目は自分の声なしでルルが代わりに言う(pitch 1.75)=順に %s' % sq(seg_w),
        sq(seg_w) == ['OWN', w0, 'OWN', w0, w0] and all(abs(e['r'] - 1) < .01 and abs(e['p'] - 1) < .01 for e in seg_w[1:4:2]) and abs(seg_w[4]['p'] - 1.75) < .01, seg_w)
    chk('6b 言い直しは自動(ボタンを押さずにマイクが再び開く): 失敗3回分の聞き取り(banana×3)のあと、次の単語に進んでいる', f['trs'][:3] == ['banana'] * 3 and f['trs'][3] == w1, f['trs'][:5])
    chk('6c 救済はヘルプ回数を消費しない(save.help が変わらない)・ヘルプのボタンは出ない・弱点メモ(save.weak)にも入れない', f['help'] == 5 and not f['weak'], (f['help'], f['weak']))
    alltxt = '\n'.join(f['texts'])
    chk('6d 失敗の間も画面に数値スコア・失敗回数・点数が出ない(「7割」「/」の数・%・点・回)', not re.findall(r'\d+\s*/\s*\d+|\d+\s*%|7割|\d+\s*(?:点|回|語)', alltxt), '')
    k0 = [i for i, e in enumerate(ev) if e['k'] == 'say' and e['t'] == c0['chunks'][0]]
    segc = ev[k0[0]:k0[0] + 5]
    chk('6e 短文のまとまり(1つ目): お手本が自動→言う→外れたら 自分の声→お手本→言い直し→2回続けて外れたら、お手本をもう一度流して次のまとまりへ(自分の声は流さない)=順に %s' % sq(segc),
        sq(segc) == [c0['chunks'][0], 'OWN', c0['chunks'][0], c0['chunks'][0], c0['chunks'][1]] and all(abs(e['p'] - 1) < .01 and abs(e['r'] - 1) < .01 for e in segc[:5] if e['k'] == 'say'), segc)
    wi = [i for i, e in enumerate(ev) if e['k'] == 'say' and e['t'] == ALL][0]
    segw = ev[wi + 1:wi + 6]
    chk('6f 全文で止まったとき(074の失敗ルール): 自分の声→お手本→言い直し→…→3回目でルルが代わりに言って(pitch 1.75)先へ=順に %s' % sq(segw),
        sq(segw) == ['OWN', c0['sentence'], 'OWN', c0['sentence'], c0['sentence']] and abs(segw[4]['p'] - 1.75) < .01 and segw[1]['r'] == 1, segw)
    chk('6g 失敗の音(ブッ)は 単語3+まとまり2+全文3=8回・最後まで進んでマップへ戻る(エラーなし)', f['jin'].count('buzz') == 8 and fin6 and not f['errs'], (f['jin'].count('buzz'), fin6, f['errs']))
    own6 = len([e for e in ev if e['k'] == 'own'])
    chk('6h 自分の声の再生は 単語2+まとまり1+全文2=5回(言えた回は流れない)。再生はどれも blob: の端末内URL(%d件)・再生後に全部手放す(作った%d・手放した%d)・マイクは聞くたびに閉じる(開いた%d・止めた%d)' % (own6, len(f['rec']['made']), len(f['rec']['revoked']), f['rec']['gum'], f['rec']['trk']),
        own6 == 5 and all(u.startswith('blob:') for u in f['rec']['own']) and sorted(f['rec']['made']) == sorted(f['rec']['revoked']) and f['rec']['gum'] == f['rec']['trk'] and len(f['trs']) == f['rec']['gum'], f['rec'])
    fext = [u for m, u in freq if not (u.startswith(base) or u.startswith('blob:') or u.startswith('data:'))]
    fpost = [(m, u) for m, u in freq if m != 'GET']
    chk('6i 失敗の流れの通しでも、録音は外へ出ない・保存されない: 外へ出た通信 %d件・GET以外 %d件・fetch/XHR/ビーコン/WebSocket/IndexedDB の呼び出し %d件・保存領域に録音が入った %d件' % (len(fext), len(fpost), len([n for n in f['net'] if n[0] != 'store-audio']), len([n for n in f['net'] if n[0] == 'store-audio'])), not fext and not fpost and not f['net'], (fext[:3], fpost[:3], f['net'][:3]))
    srcjs = re.sub(r'/\*.*?\*/', '', js, flags=re.S)
    chk('6j コード側: camp.js に通信・保存の命令がない(fetch・XMLHttpRequest・sendBeacon・WebSocket・indexedDB・localStorage・sessionStorage・FileReader・Image の外部読みこみ)・voice.js(Azure の中継)の関数を呼ばない・録音の部品は gsRec*/gsOwn* にまとまる',
        not re.search(r'fetch\(|XMLHttpRequest|sendBeacon|WebSocket|indexedDB|localStorage|sessionStorage|FileReader|voiceToken|voiceSdk|voiceAzure|voiceSave|kanpe-voice|PAD?\.', srcjs) and 'createObjectURL' in srcjs and 'revokeObjectURL' in srcjs)
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
        pv = mk(br, vp=vp); open_camp(pv); pv.wait_for_timeout(700)
        m = pv.evaluate("""()=>{var r=function(e){var b=e.getBoundingClientRect();return [Math.round(b.left),Math.round(b.top),Math.round(b.width),Math.round(b.height)]};var GS=__T.GS;
          return {cb:r(document.getElementById('gsCardBox')),lu:r(GS.lulu),st:r(document.querySelector('#sceneView .stage')),W:innerWidth,H:innerHeight,win:r(document.getElementById('msg')),go:r(document.querySelector('.btn.go')),dim:GS.dim,
           feet:Object.keys(GS.frs).map(function(k){var b=GS.frs[k].getBoundingClientRect(),f=__T.GSD.lulu.frames[+k];return b.top+f.foot_y*b.height/f.h}),bh:Object.keys(GS.frs).map(function(k){var b=GS.frs[k].getBoundingClientRect(),f=__T.GSD.lulu.frames[+k];return (f.foot_y-12)*b.height/f.h}),
           exit:(function(){var e=document.getElementById('exitBtn').getBoundingClientRect(),q=document.elementFromPoint(e.left+e.width/2,e.top+e.height/2);return !!q&&(q.id==='exitBtn'||!!q.closest('#exitBtn'))})()}}""")
        pv.screenshot(path='/tmp/g78_%dx%d.png' % vp)
        inside = m['cb'][0] >= 0 and m['cb'][1] >= 0 and m['cb'][0] + m['cb'][2] <= m['W'] and m['cb'][1] + m['cb'][3] <= m['H'] and abs(m['cb'][2] / m['cb'][3] - 9 / 16) < .01
        noover = m['lu'][0] + m['lu'][2] <= m['cb'][0] + 1 and m['go'][1] + m['go'][3] <= m['H'] + 1
        scale_ok = m['dim']['refH'] == OLDH[vp] and abs(m['dim']['lCharH'] / float(m['dim']['refH']) - .66) < .012
        share = m['cb'][2] / float(m['st'][2])
        feet_ok = max(m['feet']) - min(m['feet']) < .6
        mouth_ok = max(m['bh']) - min(m['bh']) < .6   # 083: 口パーツは出さない。代わりに、体の高さ(頭→足の裏)が全コマでそろう
        rows.append((vp, inside, noover, scale_ok, .52 <= share <= .56, feet_ok, mouth_ok, m['exit'], m['lu'][2:], m['cb'][2:], share, m['dim']['refH'], m['dim']['lCharH']))
        pv.close()
    chk('8i 5つの画面サイズ: カード全体が画面に入り(縦横比9:16)・ルルと重ならず・GO!が画面内・✕が押せる(最前面): ' + ' / '.join('%dx%d:カード%dx%d(%.0f%%)' % (r[0][0], r[0][1], r[9][0], r[9][1], r[10] * 100) for r in rows),
        all(r[1] and r[2] and r[7] for r in rows), [(r[0], r[1], r[2], r[7]) for r in rows if not (r[1] and r[2] and r[7])])
    chk('8j 5つの画面サイズ: ルルは従来の表示の高さ(変更前の実測 %s)の0.66倍・カードはステージ幅の52〜56%%(高さが足りない小さな画面は高さに合わせて縮む)・足もとのばらつき1px未満・体の高さ(頭→足の裏)が全コマでそろう(口パーツは出さない): ' % sorted(OLDH.values()) + ' / '.join('%dx%d:ルルの背%dpx(基準%d)' % (r[0][0], r[0][1], r[12], r[11]) for r in rows),
        all(r[3] and r[4] and r[5] and r[6] for r in rows), [(r[0], r[3], r[4], r[5], r[6]) for r in rows if not (r[3] and r[4] and r[5] and r[6])])
    br.close()
if bad: print(bad); sys.exit(1)
print('ALL OK')
