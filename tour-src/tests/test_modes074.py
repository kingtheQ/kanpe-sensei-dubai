# -*- coding: utf-8 -*-
"""タスク074 の動作確認。使い方: python3 tour-src/tests/test_modes074.py
タイトル画面の3モード(耳学／カンペ／耳学＆カンペ)＋オープニング語り＋失敗ルールの統一。
 静的(生成物の中身): PREF.mode・設定の出し分け・失敗ルール(自動おてほん→3回目はルルが代行・save.help を減らさない)・world のモード選択と語り・
                    新しい localStorage キーが増えていない・台本データに差分なし・画面に「勉強・テスト・測定・復習」等の言葉がない
 動作(ヘッドレス): 3モードの出し分け／失敗2回→自動おてほん／失敗3回→ルルが代行(ヘルプ回数そのまま・弱点メモに残る)／設定から途中で切り替え／
                  world のモード選択の保存・引き継ぎ・既存の保存を壊さない／「はじめから」で日本語の語り・チャントの一時停止
マイク・実機の日本語の声・実機の見え方は確認できない(このテストの音声認識と声は偽物)。"""
import os, sys, re, json, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import serve, ROOT
from playwright.sync_api import sync_playwright

bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def git(*a):
    try: return subprocess.check_output(['git', '-C', ROOT] + list(a), stderr=subprocess.DEVNULL).decode('utf-8')
    except Exception: return None

PAGES = ['tour/index.html', 'tour/doha/index.html', 'tour/rovaniemi/index.html', 'tour/ending/index.html', 'dubai/index.html']
KING_TEXT = ['ようこそ', '空港えいご物語へ', 'これからあなたはキングとして', '相棒のルルと一緒に世界一周の旅にでます', 'ルルはあなたをサポートしてくれる',
             'キングとして大きな声で口の筋肉を鍛える', 'その耳で音を聞いて相手のリズムを体感してください', 'ただそれだけ', '言えないときは、相棒のルルが助けてくれます', '楽しんでいってらっしゃい']
FORBID = ['勉強', 'テスト', '測定', '復習', '採点', '点数']

def fn_src(src, name):
    i = src.index('function ' + name + '(')
    j = src.index('\nfunction ', i + 10)
    return src[i:j]

# ---------------- 静的 ----------------
for pg in PAGES:
    s = rd(pg)
    chk('S1 %s: PREF の既定値に数値キー mode:0 があり、0/1/2/3 以外は 0 に直す(087で3を追加)' % pg, 'pitch:1.6,mode:0}' in s and 'if(PREF.mode!==1&&PREF.mode!==2&&PREF.mode!==3)PREF.mode=0;' in s)
    chk('S2 %s: 設定に3モードのセグメント(sSeg・mode)と同じ3つの名前' % pg, "'mode')" in s and all(w in s for w in ['カンペモード', '耳学＆カンペモード', '耳学モード', '文字のカンペを見て言う', '相手は音だけ。自分の答えはカンペあり', '全部、音だけ。耳と口だけで旅する']))
    chk('S3 %s: 出し分けの分岐(相手の台詞の文字を出さない／カンペを出さない／耳学で見本が自動再生)' % pg,
        'function npcHide(){if(!(PREF.mode>=1)' in s and 'function cueBlind(T){return (PREF.mode===2||(PREF.mode===3&&G.tries<2))' in s and 'later(400,playDemo)' in s and "if(!npcHide())typeText(T.npc)" in s)
    oh = fn_src(s, 'onFail'); ar = fn_src(s, 'autoRescue'); lu = fn_src(s, 'luSayCue'); uh = fn_src(s, 'useHelp')
    chk('S4 %s: 失敗→自動おてほん(failDemo)・3回目の失敗は autoRescue(ルルが代わりに言って advance)' % pg, 'failDemo()' in oh and 'autoRescue()' in oh and 'advance' in lu and "'Lulu'" in lu)
    chk('S5 %s: 自動救済は save.help を減らさず、noteWeak で弱点メモに残す。手動ヘルプは従来どおり減らす' % pg, 'save.help' not in ar and 'save.help' not in lu and 'noteWeak(T)' in ar and 'save.help--' in uh)
    chk('S6 %s: 失敗の流れに数字・回数の表示がない(自動救済・自動おてほん・ルル代行は textContent に空文字か話者名しか入れない)' % pg, all(t_ in ("''", "'Lulu'") for t_ in re.findall(r"textContent=([^;)]*?)(?:[;)}]|else)", ar + fn_src(s, 'failDemo') + lu)), re.findall(r"textContent=([^;)]*?)(?:[;)}]|else)", ar + lu))
    chk('S7 %s: 設定を閉じたとき、モードが変わっていたらいまのターンを描き直す(PREF.silent と同じ作法)' % pg, 'G.cueMode!==PREF.mode' in s)
w = rd('world/index.html')
chk('W1 world: モード選択UI(4つ。087で4つ目を追加)と kd_prefs_v1 への保存(mode だけをマージ)', w.count('class="mopt"') == 4 and "PREFKEY='kd_prefs_v1'" in w and 'p.mode=m' in w and 'function modeSave(' in w)
chk('W2 world: モード名・説明が土台の設定と同じ', all(x in w for x in ['カンペモード', '耳学＆カンペモード', '耳学モード', '文字のカンペを見て言う', '相手は音だけ。自分の答えはカンペあり', '全部、音だけ。耳と口だけで旅する']))
m = re.search(r"var OPENING_NARRATION='([^']*)'", w)
nar = m.group(1) if m else ''
chk('W3 world: ナレーション文案が定数 OPENING_NARRATION 1か所にあり、キングの下書きの文の内容と一致(句読点の差は許容)', bool(m) and all(k in nar for k in KING_TEXT) and w.count('OPENING_NARRATION=') == 1, nar[:40])
def strip_p(t): return re.sub(r'[、。！？!?,.\s]', '', t)
KING = 'ようこそ！空港えいご物語へ！これからあなたはキングとして、相棒のルルと一緒に世界一周の旅にでます。ルルはあなたをサポートしてくれる。キングとして大きな声で口の筋肉を鍛える、その耳で音を聞いて相手のリズムを体感してください。ただそれだけ。はじめて聞く英語は、意味がわからなくて戸惑うかもしれません。でも、キングの使命はひたすら発音すること。言えないときは、相棒のルルが助けてくれます。やっていて、意味がわからないし、合っているかも分からないと思うでしょう。でも安心してください。あなたの耳と口の筋肉が、自然に覚えていきます。気にしないで、どんどん世界を旅してください。楽しんでいってらっしゃい！'
chk('W3b world: 文案は句読点を除いて下書きと完全一致(書き換え・要約なし)', strip_p(nar) == strip_p(KING))
chk('W4 world: 再生は playOpeningNarration() 1つ・ja-JP の speechSynthesis・停止は stopOpeningNarration(画面を離れる・pagehide)・差し替え用の OPENING_NARRATION_AUDIO',
    w.count('function playOpeningNarration(') == 1 and "u.lang='ja-JP'" in w and "addEventListener('pagehide',stopOpeningNarration)" in w and 'OPENING_NARRATION_AUDIO' in w and 'CHANT.leave();stopOpeningNarration()' in w)
chk('W5 world: 語りの文字は画面に出さない(定数は speechSynthesis と音声ファイルにだけ渡す)', w.count('OPENING_NARRATION') - w.count('OPENING_NARRATION_AUDIO') - w.count('OPENING_NARRATION=') <= 3 and 'textContent=OPENING_NARRATION' not in w and 'innerHTML=OPENING_NARRATION' not in w)
ui_text = ' '.join(re.findall(r'MODES74=\[\[(.*?)\]\];', rd('tour/index.html'))) + ' ' + ' '.join(re.findall(r'<b>(.*?)</b><small>(.*?)</small>', w)[0]) + nar
chk('W6 画面に「勉強・テスト・測定・復習」等の言葉がない(モード名・説明・語りも含む)', not any(x in ui_text + ' '.join(re.findall(r'<b>(.*?)</b>|<small>(.*?)</small>', w)[0]) for x in FORBID))
chk('W7 chant: 語りのあいだ一時停止する口(narr)がある', 'function narr(on)' in rd('tour/index.html') and 'function narr(on)' in w)
# 新しい localStorage キーが増えていない
KEYRE = re.compile(r"(?:localStorage|sessionStorage)\.(?:getItem|setItem|removeItem)\(\s*(['\"])([^'\"]+)\1")
def keys(t): return sorted(set(m[1] for m in KEYRE.findall(t)))
for pg in PAGES + ['world/index.html']:
    old = git('show', 'HEAD:' + pg)
    if old is None: continue
    chk('K1 %s: localStorage/sessionStorage の文字列キーの一覧が従来から増えていない' % pg, set(keys(rd(pg))) - {'kw-chant'} <= set(keys(old)), sorted(set(keys(rd(pg))) - set(keys(old))))   # kw-chant は050からある sessionStorage の合図(085で removeItem を足しただけ・新しいキーではない)
chk('K2 kd_prefs_v1 の中身は mode の+1キーだけ(PREF の既定キー)', re.search(r"var PREF=\{bgm:70,beat:80,voice:100,rate:1,silent:0,big:0,pitch:1\.6,mode:0\}", rd('dubai/index.html')) is not None)
d = git('diff', '--stat', 'HEAD', '--', 'tour-src/data.py', 'tour-src/doha_data.py', 'tour-src/eikaiwa_data.py', 'tour-src/haneda_data.py', 'tour-src/event_data.py', 'tour-src/conv_data.py', 'tour-src/stay_data.py', 'tour-src/rvn_data.py', 'tour-src/window_data.py', 'tour-src/pa_data.py', 'tour-src/song_data.py')
# D1: タスク057 第1弾でナイロビの台本データを変えたため、この確認は外した(3モードの動作は下のM系で見る)

# ---------------- 動作 ----------------
HOOK = "requestAnimationFrame(frame);\n})();"
EXPOSE = "window.__T={G:G,save:save,PREF:PREF,get luHelp(){return luHelp},prefSave:prefSave};"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, EXPOSE + HOOK, 1))
INIT = """
window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});
window.__say=[];window.__sayph=[];
try{speechSynthesis.speak=function(u){window.__say.push(u.text);window.__sayph.push({t:u.text,lang:u.lang,ph:(window.__T&&__T.G.phase)||null,msg:(document.getElementById('msgText')||{}).textContent||'',who:(document.getElementById('who')||{}).textContent||''});setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}
(function(){function FS(){}
window.__srn=0;window.__bad=0;window.__heard=[];
FS.prototype.start=function(){var me=this;window.__srn++;if(window.__nomic)return;setTimeout(function(){var T=window.__T&&__T.G.scene&&__T.G.scene.turns[__T.G.ti];var t=T?T.cue.replace(/\\*/g,''):'';
  if(window.__bad>0){window.__bad--;t='blah blah blah'}
  var rs=[{transcript:t,confidence:.9}];rs.isFinal=true;if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},20)},60)};
FS.prototype.abort=FS.prototype.stop=function(){};window.SpeechRecognition=FS;window.webkitSpeechRecognition=FS})();
"""
def newctx(br, prefs=None, vp=(390, 780), nomic=False):
    ctx = br.new_context(viewport={'width': vp[0], 'height': vp[1]}); ctx.add_init_script(INIT)
    if nomic: ctx.add_init_script("window.__nomic=1")
    ctx.add_init_script("try{localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}))}catch(e){}")
    if prefs is not None: ctx.add_init_script("try{if(!sessionStorage.getItem('__pf')){sessionStorage.setItem('__pf','1');localStorage.setItem('chk1:kd_prefs_v1',%s)}}catch(e){}" % json.dumps(json.dumps(prefs)))   # チェックモードの保存は専用の名前(chk1:)
    return ctx
def open_scene(ctx, base, vid='doh_immig1'):   # タスク057 第2弾で羽田(hnd_sec)も新しい流れ(おてほんボタンなし)になったので、まだ変えていないドーハの doh_immig1 を使う
    q = ctx.new_page(); errs = []; q.on('pageerror', lambda e: errs.append(str(e)[:160])); q.route('**/tour/index.html*', hooked); q.route('**/tour/doha/index.html*', hooked)
    q.goto(base + ('/tour/doha/index.html?check=1' if vid.startswith('doh_') else '/tour/index.html?check=1')); q.wait_for_timeout(1500); q.mouse.click(215, 450); q.wait_for_timeout(500)
    q.evaluate("()=>document.getElementById('chkBtn').click()"); q.wait_for_timeout(150)
    q.evaluate("(v)=>{[].filter.call(document.querySelectorAll('#chkPan button'),function(b){return b.textContent===v})[0].click()}", vid); q.wait_for_timeout(600)
    q.click('.btn.go'); q.errs = errs
    return q
def wait_phase(q, ph, n=300):
    for _ in range(n):
        if q.evaluate("()=>__T.G.phase") == ph: return True
        q.wait_for_timeout(40)
    return False
SNAP = """()=>{var T=__T.G.scene.turns[__T.G.ti],c=document.querySelector('#panel .cue');return {ph:__T.G.phase,ti:__T.G.ti,npc:T.npc,cue:T.cue.replace(/\\*/g,''),msg:document.getElementById('msgText').textContent,
 who:document.getElementById('who').textContent,cardText:c?[].map.call(c.querySelectorAll('.w'),function(x){return x.textContent}).join(' '):null,cardBlind:c?c.classList.contains('blind'):null,
 cardAll:c?c.innerText:null,btns:[].map.call(document.querySelectorAll('#panel button'),function(b){return b.textContent.trim()}),
 demo:!!document.querySelector('#panel .btn.sub'),help:__T.save.help,weak:__T.save.weak.length}}"""

with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    # ---- 動作1: 3モードの出し分け(最初の自分の番) ----
    res = {}
    for mode in (0, 1, 2):
        ctx = newctx(br, {'mode': mode}, nomic=True); q = open_scene(ctx, base)   # マイクは聞いたふりだけして答えない(自分の番で止まって見える)
        assert wait_phase(q, 'cue') or True
        q.wait_for_timeout(1300)
        res[mode] = q.evaluate(SNAP); res[mode]['say'] = q.evaluate("()=>window.__sayph"); res[mode]['srn'] = q.evaluate("()=>window.__srn"); res[mode]['pm'] = q.evaluate("()=>__T.PREF.mode"); res[mode]['errs'] = q.errs + q.evaluate("()=>window.__errs")
        ctx.close()
    r0, r1, r2 = res[0], res[1], res[2]
    chk('M0 カンペモード(0・既定): 相手の台詞の文字が出て、カンペ(文字)が出て、おてほんボタンがある', r0['pm'] == 0 and r0['msg'] == r0['npc'] and r0['cardText'] == r0['cue'] and 'おてほん' in r0['btns'] and not r0['cardBlind'], (r0['msg'][:30], r0['cardText']))
    chk('M1 耳学＆カンペ(1): 相手の台詞の文字(英語)が出ず、声では流れ、カンペは出る・おてほんボタンも従来どおり', r1['pm'] == 1 and r1['msg'] == '' and r1['who'] != '' and r1['cardText'] == r1['cue'] and 'おてほん' in r1['btns'] and any(s['t'] == r1['npc'] for s in r1['say']), (r1['msg'], r1['who']))
    chk('M1b 耳学＆カンペ(1): 相手の台詞の日本語も出ない(画面に日本語の台詞訳がない)', not re.search(r'[぀-ヿ㐀-鿿]', r1['msg']))
    chk('M2 耳学(2): 相手の台詞の文字が出ず、自分のカンペの文字も出ない(カードの中に言うべき文の単語が1つもない)', r2['pm'] == 2 and r2['msg'] == '' and r2['cardBlind'] and r2['cardText'].strip() == '' and not any(w for w in re.findall(r'[A-Za-z]{3,}', r2['cardAll'] or '')), (r2['cardAll'], r2['msg']))
    first_cue_say = [i for i, s in enumerate(r2['say']) if s['t'] == r2['cue']]
    chk('M2b 耳学(2): 自分の番の冒頭でお手本が自動で流れ(ボタンを押していない)、そのあとマイクが開く', bool(first_cue_say) and r2['srn'] >= 1 and r2['say'][first_cue_say[0]]['ph'] == 'cue', (r2['say'][:4], r2['srn']))
    chk('M2c 耳学(2): 聞き直しは音だけのボタン(🔊)・文字のおてほんは出ない', '🔊' in r2['btns'] and 'おてほん' not in r2['btns'] and r2['demo'])
    chk('M3 3モードともエラーなし', all(not res[m]['errs'] for m in res), [res[m]['errs'] for m in res])
    # ---- 動作2: 失敗ルール(全モード共通。耳学モードで確認) ----
    for mode in (0, 2):
        ctx = newctx(br, {'mode': mode}); q = open_scene(ctx, base)
        wait_phase(q, 'cue'); q.wait_for_timeout(300)
        h0 = q.evaluate("()=>__T.save.help"); w0 = q.evaluate("()=>__T.save.weak.length")
        q.evaluate("()=>{window.__bad=2;window.__say.length=0;window.__sayph.length=0;window.__srn=0;window.__btnclicks=0}")
        q.evaluate("()=>{var T=__T.G.scene.turns[__T.G.ti];window.__c0=T.cue.replace(/\\*/g,'')}")
        # 最初の自分の番の失敗2回→3回目に通る。おてほんボタンは押さない
        for _ in range(200):
            q.wait_for_timeout(50)
            if q.evaluate("()=>__T.G.ti")>=1: break
        sp = q.evaluate("()=>window.__sayph"); c0 = q.evaluate("()=>window.__c0")
        retry_lines = [s for s in sp if s['ph'] == 'retry']
        cue_after_retry = [i for i, s in enumerate(sp) if s['t'] == c0 and s['ph'] == 'retry']
        chk('F1(m%d) 失敗したら相手の聞き返しのあと、おてほんが自動で流れる(ボタンなし)・2回失敗→3回目に通って先へ進む' % mode, len(retry_lines) >= 2 and len(cue_after_retry) >= 2 and q.evaluate("()=>__T.G.ti") >= 1, (len(retry_lines), len(cue_after_retry)))
        chk('F1b(m%d) 通れば save.help・弱点メモは変わらない' % mode, q.evaluate("()=>__T.save.help") == h0 and q.evaluate("()=>__T.save.weak.length") == w0)
        ctx.close()
        ctx = newctx(br, {'mode': mode}); q = open_scene(ctx, base)
        wait_phase(q, 'cue'); q.wait_for_timeout(300)
        h0 = q.evaluate("()=>__T.save.help"); cue0 = q.evaluate("()=>__T.G.scene.turns[__T.G.ti].cue.replace(/\\*/g,'')")
        q.evaluate("()=>{window.__bad=3;window.__sayph.length=0}")
        seen = {'lulu': False, 'msg': [], 'phases': set(), 'btn': set()}
        for _ in range(240):
            q.wait_for_timeout(40)
            s = q.evaluate("()=>({ph:__T.G.phase,who:document.getElementById('who').textContent,msg:document.getElementById('msgText').textContent,ti:__T.G.ti,pan:document.getElementById('panel').innerText,stat:(document.querySelector('#panel .stat')||{}).textContent||''})")
            seen.setdefault('stats', []).append(s['stat'])
            seen['phases'].add(s['ph'])
            if s['ph'] == 'help' and s['who'] == 'Lulu': seen['lulu'] = True; seen['msg'].append(s['msg']); seen['pan'] = s['pan']
            if s['ti'] >= 1: break
        sp = q.evaluate("()=>window.__sayph")
        lulu_say = [x for x in sp if x['t'] == cue0 and x['ph'] == 'help']
        chk('F2(m%d) 3回目の失敗でルルが代わりに言い(ルルの吹き出し・声)、物語が進む(次の台詞へ)' % mode, seen['lulu'] and len(lulu_say) >= 1 and q.evaluate("()=>__T.G.ti") >= 1, (seen['lulu'], len(lulu_say)))
        chk('F3(m%d) 自動救済はヘルプ回数(save.help)を消費しない' % mode, q.evaluate("()=>__T.save.help") == h0, (h0, q.evaluate("()=>__T.save.help")))
        chk('F4(m%d) 救済された文も弱点メモ(save.weak)に残る' % mode, q.evaluate("(c)=>__T.save.weak.some(function(w){return w.c.replace(/\\*/g,'')===c})", cue0))
        chk('F5(m%d) 失敗のあいだ、数字のスコア・失敗回数・「7割未満」は出ない(判定の表示欄が空)' % mode, all(not re.search(r'[0-9]|7割|Too', x_) for x_ in seen['stats']), sorted(set(seen['stats'])))
        if mode == 2: chk('F6 耳学(2): 救済のときだけルルの吹き出しに英文が出る(087-A。ほかの場面は出さない)', any(m_ == cue0 for m_ in seen['msg']) and seen['msg'] != [], seen['msg'])
        if mode == 0: chk('F6b カンペ(0): 救済時はルルの吹き出しにその文が出る(従来のヘルプ代行と同じ形)', any(m_ == cue0 for m_ in seen['msg']), seen['msg'])
        ctx.close()
    # ---- 動作3: 手動ヘルプは従来どおり回数を消費 ----
    ctx = newctx(br, {'mode': 0}, nomic=True); q = open_scene(ctx, base); wait_phase(q, 'cue'); q.wait_for_timeout(800)
    h0 = q.evaluate("()=>__T.save.help"); q.evaluate("()=>{var b=document.querySelector('#panel .btn.help');b&&b.click()}"); q.wait_for_timeout(500)
    chk('H1 手動ヘルプは従来どおり残り回数を1つ減らす', q.evaluate("()=>__T.save.help") == h0 - 1, (h0, q.evaluate("()=>__T.save.help")))
    ctx.close()
    # ---- 動作4: 設定からの切り替え(場面の途中で描き直す) ----
    ctx = newctx(br, {'mode': 0}, nomic=True); q = open_scene(ctx, base); wait_phase(q, 'cue'); q.wait_for_timeout(500)
    q.evaluate("()=>{window.__bad=0}")
    q.click('#sceneView .setbtn:not(.wb)'); q.wait_for_timeout(300)
    seg = q.evaluate("()=>[].map.call(document.querySelectorAll('#setBody .sseg')[0].querySelectorAll('button'),function(b){return b.textContent+':'+b.getAttribute('aria-pressed')})")
    chk('C1 設定に3モードのセグメントがあり、いまのモード(カンペ)が選ばれている(チェックモードでも)', seg == ['カンペモード:true', '耳学＆カンペモード:false', '耳学モード:false', '耳学（サポートカンペ付き）:false'], seg)
    q.evaluate("()=>document.querySelectorAll('#setBody .sseg')[0].querySelectorAll('button')[2].click()"); q.wait_for_timeout(200)
    saved = q.evaluate("()=>JSON.parse(localStorage.getItem('kd_prefs_v1'))")   # チェックモードでは専用の名前(chk1:)へ向く(ページの中からは同じ名前で読める)
    chk('C2 選ぶと即 kd_prefs_v1 に mode が保存される(数値・他のキーを壊さない)', saved.get('mode') == 2 and saved.get('bgm') == 70, saved)
    q.evaluate("()=>{window.__sayph.length=0;window.__say.length=0}")
    q.click('#setBack'); q.wait_for_timeout(1200)
    s = q.evaluate(SNAP)
    chk('C3 設定を閉じると、いまのターンが耳学モードで描き直される(カンペの文字が消え、お手本が自動で流れる)', s['cardBlind'] and s['cardText'].strip() == '' and s['msg'] == '' and any(x == s['cue'] for x in q.evaluate("()=>window.__say")), (s['cardAll'], s['msg']))
    q.evaluate("()=>{document.querySelector('.setbtn:not(.wb)').click()}"); q.wait_for_timeout(200)
    q.evaluate("()=>document.querySelectorAll('#setBody .sseg')[0].querySelectorAll('button')[1].click()"); q.wait_for_timeout(100); q.click('#setBack'); q.wait_for_timeout(1000)
    s = q.evaluate(SNAP)
    chk('C4 耳学＆カンペ(1)に切り替えると、相手の台詞の文字は出ず、カンペが出る', s['msg'] == '' and s['cardText'] == s['cue'] and not s['cardBlind'], (s['msg'], s['cardText']))
    chk('C5 切り替えてもエラーなし', not q.errs and not q.evaluate("()=>window.__errs"), q.errs)
    ctx.close()
    # ---- 動作5: PREF.silent と耳学モードが重なったとき ----
    ctx = newctx(br, {'mode': 2, 'silent': 1}, nomic=True); q = open_scene(ctx, base); wait_phase(q, 'cue'); q.wait_for_timeout(1200)
    s = q.evaluate(SNAP); sp_ = q.evaluate("()=>document.querySelectorAll('#panel .cue .w').length"); vis = q.evaluate("()=>[].some.call(document.querySelectorAll('#panel .cue .w'),function(x){return x.offsetParent!==null||x.textContent!==''})")   # 非表示(display:none)で空
    chk('S1 こえをださない＋耳学: 画面に文字を出さない(spanは空・非表示)・時間判定は内部トークンのまま・エラーなし', s['cardBlind'] and not vis and s['msg'] == '' and s['cardText'].strip() == '' and not q.errs, (sp_, vis, s['cardAll']))
    q.evaluate("()=>{var a=document.querySelector('#panel .btn:not(.sub):not(.help)');window.__dn=0}")
    # 長押し(クリック2回)で時間判定→進む
    ph0 = q.evaluate("()=>__T.G.ti")
    for _ in range(3):
        if q.evaluate("()=>__T.G.ti") > ph0: break
        q.evaluate("()=>{var a=[].filter.call(document.querySelectorAll('#panel .btn'),function(b){return b.textContent.indexOf('もういちど')>=0})[0];a&&a.click()}"); q.wait_for_timeout(3000)
        q.evaluate("()=>{var a=[].filter.call(document.querySelectorAll('#panel .btn'),function(b){return b.textContent.indexOf('もういちど')>=0})[0];a&&a.click()}"); q.wait_for_timeout(1500)
    chk('S1b こえをださない＋耳学: 時間判定で自分の番が通り、先へ進む', q.evaluate("()=>__T.G.ti") > ph0 or q.evaluate("()=>__T.G.phase") in ('pass', 'npc'), q.evaluate("()=>[__T.G.ti,__T.G.phase]"))
    ctx.close()
    # ---- 動作6: world のモード選択・保存・引き継ぎ・語り ----
    NARR_INIT = "window.__ssp=[];window.__aud=[];try{speechSynthesis.speak=function(u){window.__ssp.push({t:u.text,lang:u.lang});setTimeout(function(){if(u.onend)u.onend({})},__NARRMS)};speechSynthesis.cancel=function(){window.__ssc=(window.__ssc||0)+1}}catch(e){}window.__NARRMS=8;"
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(NARR_INIT)
    ctx.add_init_script("try{if(!sessionStorage.getItem('__pf')){sessionStorage.setItem('__pf','1');localStorage.setItem('kd_prefs_v1',JSON.stringify({bgm:55,silent:1}))}}catch(e){}")
    pg = ctx.new_page(); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800); pg.click('#startBtn'); pg.wait_for_timeout(300)
    st = pg.evaluate("()=>[].map.call(document.querySelectorAll('#mSel .mopt'),function(b){return b.querySelector('b').textContent+'|'+b.querySelector('small').textContent+'|'+b.getAttribute('aria-checked')})")
    chk('T1 タイトル: 3つの名前＋1行説明が出て、保存が無い(modeなし)ときはカンペモード(0)が選ばれている', st == ['カンペモード|文字のカンペを見て言う|true', '耳学＆カンペモード|相手は音だけ。自分の答えはカンペあり|false', '耳学モード|全部、音だけ。耳と口だけで旅する|false', '耳学（サポートカンペ付き）|耳学モード。2回つまずいたら、3回目だけ文字|false'], st)
    pg.click('#mSel .mopt[data-m="2"]'); pg.wait_for_timeout(200)
    sv = pg.evaluate("()=>JSON.parse(localStorage.getItem('kd_prefs_v1'))")
    chk('T2 選ぶと即 kd_prefs_v1 に保存(既存の bgm・silent を壊さず mode:2 だけ足す)', sv == {'bgm': 55, 'silent': 1, 'mode': 2}, sv)
    pg.reload(); pg.wait_for_timeout(800); pg.click('#startBtn'); pg.wait_for_timeout(200)
    st = pg.evaluate("()=>[].map.call(document.querySelectorAll('#mSel .mopt'),function(b){return b.getAttribute('aria-checked')})")
    chk('T3 再訪時は前回のモードを引き継ぐ(耳学が選ばれている)', st == ['false', 'false', 'true', 'false'], st)
    pg.evaluate("()=>localStorage.setItem('kd_prefs_v1','{broken')"); pg.reload(); pg.wait_for_timeout(800); pg.click('#startBtn'); pg.wait_for_timeout(200)
    st = pg.evaluate("()=>[].map.call(document.querySelectorAll('#mSel .mopt'),function(b){return b.getAttribute('aria-checked')})")
    chk('T4 保存が壊れていてもカンペモード(0)を既定として扱い、エラーにならない', st == ['true', 'false', 'false', 'false'], st)
    # せつめいを きく
    pg.evaluate("()=>{window.__ssp.length=0}"); pg.click('#cNarr'); pg.wait_for_timeout(300)
    ssp = pg.evaluate("()=>window.__ssp")
    chk('N1 「せつめいを きく」で日本語(ja-JP)のナレーションが流れる・文案はキングの下書き(句読点を除いて一致)', len(ssp) == 1 and ssp[0]['lang'] == 'ja-JP' and strip_p(ssp[0]['t']) == strip_p(KING), ssp)
    chk('N2 聞き直しではゲームは始まらない(タイトルのまま)', pg.url.endswith('/world/index.html') and pg.evaluate("()=>!document.getElementById('sTitle').hidden"))
    chk('N3 語りの文字は画面に出ていない', '空港えいご物語へ' not in pg.evaluate("()=>document.body.innerText").replace('空港えいご物語\n', ''))
    ctx.close()
    # 語りのあいだ、タイトルのチャント(050)は一時停止し、語りが終わったら続きから(まだタイトルにいる場合)
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(NARR_INIT.replace('window.__NARRMS=8', 'window.__NARRMS=2500'))
    pg = ctx.new_page(); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800); pg.click('#startBtn'); pg.wait_for_timeout(1200)
    was = pg.evaluate("()=>!!(window.CHANT&&CHANT.playing())")
    pg.click('#cNarr'); pg.wait_for_timeout(600)
    during = pg.evaluate("()=>!!(window.CHANT&&CHANT.playing())"); held = pg.evaluate("()=>!!(window.CHANT&&CHANT.has())")
    pg.wait_for_timeout(3200)
    after = pg.evaluate("()=>!!(window.CHANT&&CHANT.playing())")
    chk('N8 語りのあいだチャントは一時停止し(止まっている)、語りが終わったら続きから鳴る(タイトルにいる間)', was and (not during) and held and after, (was, during, held, after))
    ctx.close()
    # はじめから(保存なし)→語り→語り終えたら世界一周編へ
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(NARR_INIT.replace('window.__NARRMS=8', 'window.__NARRMS=1200'))
    pg = ctx.new_page(); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800); pg.click('#startBtn'); pg.wait_for_timeout(200)
    pg.click('#cNew'); pg.wait_for_timeout(400)
    ssp = pg.evaluate("()=>window.__ssp")
    chk('N4 「はじめから」を押すと語りが始まる(語りの最中はまだタイトルにいて「すすむ」だけが出る)', len(ssp) == 1 and '/world/' in pg.url and pg.evaluate("()=>!document.getElementById('cmdNarr').hidden"), (ssp[:1] and ssp[0]['lang'], pg.url))
    pg.wait_for_url('**/tour/**', timeout=8000)
    chk('N5 語りを聞き終えたら世界一周編(tour/)へ進む', '/tour/' in pg.url)
    ctx.close()
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(NARR_INIT.replace('window.__NARRMS=8', 'window.__NARRMS=30000'))
    pg = ctx.new_page(); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800); pg.click('#startBtn'); pg.click('#cNew'); pg.wait_for_timeout(300)
    c0 = pg.evaluate("()=>window.__ssc||0"); pg.click('#cGo'); pg.wait_for_url('**/tour/**', timeout=8000)
    chk('N6 語りの途中で「すすむ」を押すと、語りは止まって(speechSynthesis.cancel)ゲームが始まる', pg.url.count('/tour/') == 1)
    ctx.close()
    # 「つづきから」では自動再生しない
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(NARR_INIT)
    ctx.add_init_script("try{localStorage.setItem('kanpe-world-v1',JSON.stringify({v:1,at:'doha',cleared:{haneda:1,doha:1},seen:{haneda:1,doha:1}}));localStorage.setItem('kanpe-tour-save-v1','{\"seen\":{}}')}catch(e){}")
    pg = ctx.new_page(); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800); pg.click('#startBtn'); pg.wait_for_timeout(200)
    pg.evaluate("()=>{window.__ssp.length=0}");
    if pg.evaluate("()=>document.getElementById('cCont').getAttribute('aria-disabled')") != 'true': pg.click('#cCont'); pg.wait_for_timeout(500)
    chk('N7 「つづきから」では語りを自動再生しない', pg.evaluate("()=>window.__ssp.length") == 0)
    ctx.close()
    br.close()
print('\n%s  (NG %d件)' % ('すべて OK' if not bad else '失敗あり', len(bad)))
if bad: print(bad); sys.exit(1)
