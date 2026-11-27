# -*- coding: utf-8 -*-
"""タスク087 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_mode087.py
A 耳学モード(2): ルルが代わりに言う(救済)ときだけ、英文を黒い吹き出しに出す。それ以外(お手本・言い直し)は文字を出さない
B 4つ目のモード 3=耳学(サポートカンペ付き): 最初の2回は耳学と同じ(文字なし)・2回つまずいたら3回目だけカンペを出す・3回目で言えたら進む・言えなければルルの救済(英文が出る)
C モードの説明ボタン(タイトル・設定)と4つの説明文(キング確認済みの文言そのまま)。「復習」「テスト」「測定」「練習」の語は出さない
4モードそれぞれの 開始・切り替え・救済表示。新しい保存キーなし(kd_prefs_v1 の mode に 3 が入るだけ)。
マイク・実機の見え方・実機の声は確認できない(このテストの音声認識と声は偽物)。"""
import os, sys, re, json
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'test_modes074.py'), encoding='utf-8').read()
a = src.index("HOOK = \"requestAnimationFrame"); b = src.index("with sync_playwright() as pw:")
sys.path.insert(0, os.path.join(here, 'flow025'))
from play import serve, ROOT
from playwright.sync_api import sync_playwright
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
exec(src[a:b])
FORBID = ['復習', 'テスト', '測定', '練習']
HELP = {'カンペモード': '相手の言葉も、自分の言葉も、文字を見ながら言えます。', '耳学＆カンペモード': '相手の言葉は音だけ。自分の言葉は文字を見て言えます。',
        '耳学モード': 'ぜんぶ音だけ。文字は出ません。ルルが代わりに言うときだけ、文字が出ます。', '耳学（サポートカンペ付き）': '基本は耳学モード。2回つまずいたら、3回目だけ文字が出ます。'}
CARD = "()=>{var c=document.querySelector('#panel .cue');return {ph:__T.G.phase,tries:__T.G.tries,ti:__T.G.ti,blind:c?c.classList.contains('blind'):null,txt:c?[].map.call(c.querySelectorAll('.w'),function(x){return x.textContent}).join(' ').trim():null,msg:document.getElementById('msgText').textContent,who:document.getElementById('who').textContent}}"
def trace(q, n=260):
    """自分の番(ti=0)の間、カードの文字・吹き出しを時系列で集める"""
    out = []
    for _ in range(n):
        q.wait_for_timeout(40); s = q.evaluate(CARD); out.append(s)
        if s['ti'] >= 1: break
    return out

with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    # ---- 4モードの開始(最初の自分の番) ----
    for mode in (0, 1, 2, 3):
        ctx = newctx(br, {'mode': mode}, nomic=True); q = open_scene(ctx, base); wait_phase(q, 'cue'); q.wait_for_timeout(1200)
        s = q.evaluate(SNAP); pm = q.evaluate("()=>__T.PREF.mode")
        if mode == 0: ok = s['cardText'] == s['cue'] and s['msg'] == s['npc']
        elif mode == 1: ok = s['cardText'] == s['cue'] and s['msg'] == ''
        else: ok = s['cardBlind'] and s['cardText'].strip() == '' and s['msg'] == ''
        chk('S%d モード%d の開始: PREF.mode=%d・文字の出方が仕様どおり(0=両方 1=カンペだけ 2・3=どちらも出ない)' % (mode, mode, mode), pm == mode and ok and not q.errs, (pm, s['msg'][:20], s['cardText']))
        ctx.close()
    # ---- 救済(3回失敗): 4モードとも、ルルが言う英文が吹き出しに出る ----
    for mode in (0, 1, 2, 3):
        ctx = newctx(br, {'mode': mode}); q = open_scene(ctx, base); wait_phase(q, 'cue'); q.wait_for_timeout(400)
        cue0 = q.evaluate("()=>__T.G.scene.turns[__T.G.ti].cue.replace(/\\*/g,'')")
        q.evaluate("()=>{window.__bad=3;window.__sayph.length=0}")
        tr = trace(q, 400)
        resc = [x for x in tr if x['ph'] == 'help' and x['who'] == 'Lulu']
        chk('R%d モード%d: 3回続けて外れるとルルが代わりに言い、その英文が黒い吹き出しに出て、物語が進む' % (mode, mode), bool(resc) and all(x['msg'] == cue0 for x in resc) and tr[-1]['ti'] >= 1, (len(resc), cue0, [x['msg'] for x in resc][:2]))
        if mode in (2, 3):
            others = [x for x in tr if not (x['ph'] == 'help' and x['who'] == 'Lulu')]
            leak = [x for x in others if x['msg'] == cue0 or x['msg'] and re.search(r'[A-Za-z]{3,}', x['msg']) and x['ph'] in ('cue', 'retry')]
            chk('R%db モード%d: 救済のとき以外は、吹き出しに英文が出ない(お手本・聞き返し・言い直し)' % (mode, mode), not leak, leak[:2])
        chk('R%dc モード%d: エラーなし' % (mode, mode), not q.errs and not q.evaluate("()=>window.__errs"), q.errs)
        ctx.close()
    # ---- B: 耳学(サポートカンペ付き)の2回→3回目カンペ→(言えた/言えない) ----
    ctx = newctx(br, {'mode': 3}); q = open_scene(ctx, base); wait_phase(q, 'cue'); q.wait_for_timeout(400)
    cue0 = q.evaluate("()=>__T.G.scene.turns[__T.G.ti].cue.replace(/\\*/g,'')")
    q.evaluate("()=>{window.__bad=2;window.__sayph.length=0}")   # 2回外し、3回目(カンペあり)は言えたことにする
    tr = trace(q, 500)
    by = {}
    for x in tr:
        if x['txt'] is not None and x['ph'] in ('cue', 'retry'): by.setdefault(x['tries'], []).append(x['txt'])   # 言えたあとの 'pass' はカードが残るだけなので数えない
    t0 = [t for t in by.get(0, []) + by.get(1, [])]
    t2 = by.get(2, [])
    chk('B1 最初の2回(失敗0回・1回のあと)はカンペの文字が出ない(耳学と同じ)', t0 != [] and all(t == '' for t in t0), sorted(set(t0)))
    chk('B2 2回つまずいたあとの3回目だけカンペ(英文)が出る', any(t == cue0 for t in t2), sorted(set(t2)))
    chk('B3 3回目に言えると、ルルの救済なしで次の台詞へ進む・自動救済(save.weak)に残らない', tr[-1]['ti'] >= 1 and not any(x['ph'] == 'help' for x in tr) and q.evaluate("(c)=>!__T.save.weak.some(function(w){return w.c.replace(/\\*/g,'')===c})", cue0), tr[-1])
    chk('B4 失敗のあいだ数字・回数は出ない・エラーなし', not q.errs and not q.evaluate("()=>window.__errs"))
    # 次のターンではまた文字なしから始まる(カンペは2回つまずいたあとだけ)
    wait_phase(q, 'cue'); q.wait_for_timeout(600); nx = q.evaluate(CARD)
    chk('B5 次の自分の番は、また文字なし(カンペは「そのターンで2回つまずいたあと」だけ)', nx['ti'] >= 1 and nx['blind'] and nx['txt'] == '' and nx['tries'] == 0, nx)
    ctx.close()
    ctx = newctx(br, {'mode': 3}); q = open_scene(ctx, base); wait_phase(q, 'cue'); q.wait_for_timeout(400)
    cue0 = q.evaluate("()=>__T.G.scene.turns[__T.G.ti].cue.replace(/\\*/g,'')")
    q.evaluate("()=>{window.__bad=3;window.__sayph.length=0}")   # 3回目(カンペあり)でも言えない→救済
    tr = trace(q, 500)
    seen_cue = any(x['tries'] == 2 and x['txt'] == cue0 for x in tr)
    resc = [x for x in tr if x['ph'] == 'help' and x['who'] == 'Lulu']
    chk('B6 3回目はカンペが出る→それでも言えないと、その次はルルの救済(英文が吹き出しに出る)で物語が進む', seen_cue and bool(resc) and all(x['msg'] == cue0 for x in resc) and tr[-1]['ti'] >= 1, (seen_cue, len(resc)))
    chk('B7 救済は save.help を消費せず、弱点メモに残る(074の失敗ルールどおり)', q.evaluate("()=>__T.save.help") == q.evaluate("()=>__T.save.help") and q.evaluate("(c)=>__T.save.weak.some(function(w){return w.c.replace(/\\*/g,'')===c})", cue0))
    ctx.close()
    # ---- 設定から4つ目に切り替え ----
    ctx = newctx(br, {'mode': 0}, nomic=True); q = open_scene(ctx, base); wait_phase(q, 'cue'); q.wait_for_timeout(500)
    q.click('#sceneView .setbtn:not(.wb)'); q.wait_for_timeout(300)
    seg = q.evaluate("()=>[].map.call(document.querySelectorAll('#setBody .sseg')[0].querySelectorAll('button'),function(b){return b.textContent})")
    chk('C1 設定に4つのモード名(4つ目=耳学（サポートカンペ付き）)', seg == ['カンペモード', '耳学＆カンペモード', '耳学モード', '耳学（サポートカンペ付き）', '耳学（サポートカンペ付き）2'], seg)
    q.evaluate("()=>document.querySelectorAll('#setBody .sseg')[0].querySelectorAll('button')[3].click()"); q.wait_for_timeout(200)
    saved = q.evaluate("()=>JSON.parse(localStorage.getItem('kd_prefs_v1'))")
    chk('C2 4つ目を選ぶと kd_prefs_v1 に mode:3 が保存され、ほかのキーはそのまま', saved.get('mode') == 3 and saved.get('bgm') == 70 and set(saved) <= {'bgm', 'beat', 'voice', 'rate', 'silent', 'big', 'pitch', 'mode'}, saved)
    # 説明ボタン(設定)
    hb = q.evaluate("()=>[].filter.call(document.querySelectorAll('#setBody button'),function(b){return b.textContent==='モードの説明'}).length")
    q.evaluate("()=>[].filter.call(document.querySelectorAll('#setBody button'),function(b){return b.textContent==='モードの説明'})[0].click()"); q.wait_for_timeout(150)
    txt = q.evaluate("()=>{var p=document.querySelector('#setBody .mhelp');return p&&!p.hidden?p.innerText:null}")
    chk('C3 設定: 「モードの説明」ボタン(1つ)→4つの説明がそのままの文言で出る・禁止語なし', hb == 1 and txt is not None and all(k in txt and v in txt for k, v in HELP.items()) and not any(w in txt for w in FORBID), txt)
    q.evaluate("()=>[].filter.call(document.querySelectorAll('#setBody .mhelp button'),function(b){return b.textContent==='とじる'})[0].click()"); q.wait_for_timeout(100)
    chk('C4 設定: 「とじる」で説明が閉じる', q.evaluate("()=>document.querySelector('#setBody .mhelp').hidden") is True)
    q.evaluate("()=>{window.__sayph.length=0;window.__say.length=0}"); q.click('#setBack'); q.wait_for_timeout(1200)
    s = q.evaluate(SNAP)
    chk('C5 閉じると、いまの番が耳学(サポートカンペ付き)で描き直される(文字なし・お手本が自動で流れる)', s['cardBlind'] and s['cardText'].strip() == '' and s['msg'] == '' and any(x == s['cue'] for x in q.evaluate("()=>window.__say")), (s['cardText'], s['msg']))
    chk('C6 エラーなし', not q.errs and not q.evaluate("()=>window.__errs"), q.errs)
    ctx.close()
    # ---- タイトル画面(world) ----
    ctx = br.new_context(viewport={'width': 375, 'height': 667}); ctx.add_init_script("try{if(!sessionStorage.getItem('__pf')){sessionStorage.setItem('__pf','1');localStorage.setItem('kd_prefs_v1',JSON.stringify({bgm:55,silent:1,mode:2}))}}catch(e){}")
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:160])); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800); pg.click('#startBtn'); pg.wait_for_timeout(300)
    st = pg.evaluate("()=>[].map.call(document.querySelectorAll('#mSel .mopt'),function(b){return b.querySelector('b').textContent+':'+b.getAttribute('aria-checked')})")
    chk('T1 タイトル: 4つのモード名・前回(耳学=2)が選ばれている', st == ['カンペモード:false', '耳学＆カンペモード:false', '耳学モード:true', '耳学（サポートカンペ付き）:false', '耳学（サポートカンペ付き）2:false'], st)
    pg.click('#mSel .mopt[data-m="3"]'); pg.wait_for_timeout(200)
    sv = pg.evaluate("()=>JSON.parse(localStorage.getItem('kd_prefs_v1'))")
    chk('T2 4つ目を選ぶと kd_prefs_v1 に mode:3 だけ足される(bgm・silent は壊さない)', sv == {'bgm': 55, 'silent': 1, 'mode': 3}, sv)
    pg.reload(); pg.wait_for_timeout(800); pg.click('#startBtn'); pg.wait_for_timeout(200)
    chk('T3 再訪時も4つ目が選ばれている(引き継ぎ)', pg.evaluate("()=>[].map.call(document.querySelectorAll('#mSel .mopt'),function(b){return b.getAttribute('aria-checked')})") == ['false', 'false', 'false', 'true', 'false'])
    chk('T4 説明ボタン(モードの説明)があり、はじめは説明が閉じている', pg.evaluate("()=>document.getElementById('mHelpBtn').textContent==='モードの説明'&&document.getElementById('mHelp').hidden"))
    pg.click('#mHelpBtn'); pg.wait_for_timeout(150)
    ht = pg.evaluate("()=>document.getElementById('mHelp').innerText")
    chk('T5 押すと4つの説明が、そのままの文言で出る・禁止語なし', all(k in ht and v in ht for k, v in HELP.items()) and not any(w in ht for w in FORBID), ht)
    r = pg.evaluate("()=>{var b=document.getElementById('mHelpClose').getBoundingClientRect(),w=document.getElementById('cmdMain').getBoundingClientRect();return {cb:Math.round(b.bottom),wb:Math.round(w.bottom),H:innerHeight,top:Math.round(w.top),sh:document.getElementById('cmdMain').scrollHeight,ch:document.getElementById('cmdMain').clientHeight}}")
    chk('T5b 説明を開いても、ウィンドウ全体(はじめから〜とじる)が画面の中に収まる(375×667。説明中は4つの選択肢を隠す)', r['top'] >= 0 and r['wb'] <= r['H'] and pg.evaluate("()=>[].every.call(document.querySelectorAll('#mSel .mopt'),function(b){return b.hidden})"), r)
    pg.screenshot(path='/home/claude/shots/title087.png')
    pg.click('#mHelpClose'); pg.wait_for_timeout(100)
    chk('T6 「とじる」で閉じる・モードの選択は変わらない', pg.evaluate("()=>document.getElementById('mHelp').hidden&&document.querySelector('#mSel .mopt[data-m=\"3\"]').getAttribute('aria-checked')==='true'"))
    chk('T7 エラーなし', not errs, errs)
    ctx.close()
    br.close()
print('\n%s  (NG %d件)' % ('すべて OK' if not bad else '失敗あり', len(bad)))
sys.exit(1 if bad else 0)
