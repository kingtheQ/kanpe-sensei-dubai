# -*- coding: utf-8 -*-
"""タスク106-B の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_mode106.py
5つ目のモード 4=耳学(サポートカンペ付き)2: 基本は耳学。1回つまずいたら2回目からカンペを出し、3回目も出したまま。3回目も失敗ならルルの救済(英文が黒い吹き出しに出る)。
タイトルと設定の両方で選べる。説明(あそびかた)に1項目。既存4モードの挙動・既存の保存値は変えない(kd_prefs_v1 の mode に 4 が入るだけ)。
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
NAME4 = '耳学（サポートカンペ付き）2'; DESC4 = '基本は耳学モード。1回つまずいたら、2回目から文字が出ます。'
CARD = "()=>{var c=document.querySelector('#panel .cue');return {ph:__T.G.phase,tries:__T.G.tries,ti:__T.G.ti,blind:c?c.classList.contains('blind'):null,txt:c?[].map.call(c.querySelectorAll('.w'),function(x){return x.textContent}).join(' ').trim():null,msg:document.getElementById('msgText').textContent,who:document.getElementById('who').textContent}}"
def trace(q, n=500):
    out = []
    for _ in range(n):
        q.wait_for_timeout(40); s = q.evaluate(CARD); out.append(s)
        if s['ti'] >= 1: break
    return out
def run(br, base, mode, nbad):
    ctx = newctx(br, {'mode': mode}); q = open_scene(ctx, base); wait_phase(q, 'cue'); q.wait_for_timeout(400)
    cue0 = q.evaluate("()=>__T.G.scene.turns[__T.G.ti].cue.replace(/\\*/g,'')")
    q.evaluate("()=>{window.__bad=%d;window.__sayph.length=0}" % nbad)
    tr = trace(q); errs = list(q.errs) + (q.evaluate("()=>window.__errs") or [])
    ctx.close(); return cue0, tr, errs
def shown(tr, tries, cue0):   # その失敗回数のときに、カンペ(英文)が出ていたか(言えたあとの pass は数えない)
    return [x['txt'] for x in tr if x['txt'] is not None and x['ph'] in ('cue', 'retry') and x['tries'] == tries]

with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    # ---- 開始: モード4は最初は耳学と同じ(文字なし) ----
    ctx = newctx(br, {'mode': 4}, nomic=True); q = open_scene(ctx, base); wait_phase(q, 'cue'); q.wait_for_timeout(1200)
    s = q.evaluate(SNAP); pm = q.evaluate("()=>__T.PREF.mode")
    chk('M1 モード4の開始: PREF.mode=4・1回目はカンペなし・相手の文字も出ない(耳学と同じ)', pm == 4 and s['cardBlind'] and s['cardText'].strip() == '' and s['msg'] == '' and not q.errs, (pm, s['cardText'], s['msg']))
    ctx.close()
    # ---- 1回つまずく → 2回目はカンペ表示 → 言えて進む ----
    cue0, tr, errs = run(br, base, 4, 1)
    t0, t1 = shown(tr, 0, cue0), shown(tr, 1, cue0)
    chk('M2 1回目(失敗0回)はカンペなし', t0 != [] and all(t == '' for t in t0), sorted(set(t0)))
    chk('M3 1回つまずいたあとの2回目はカンペ(英文)が出る', any(t == cue0 for t in t1), sorted(set(t1)))
    chk('M4 2回目で言えると、ルルの救済なしで次の台詞へ進む・弱点メモ(自動救済)に残らない', tr[-1]['ti'] >= 1 and not any(x['ph'] == 'help' for x in tr), tr[-1])
    chk('M4b エラーなし', not errs, errs)
    # ---- 2回つまずく → 3回目もカンペ表示のまま ----
    cue0, tr, errs = run(br, base, 4, 2)
    t2 = shown(tr, 2, cue0)
    chk('M5 2回つまずいたあとの3回目も、カンペ(英文)を出したまま', any(t == cue0 for t in t2) and all(t == cue0 for t in t2 if t), sorted(set(t2)))
    chk('M5b 3回目で言えると進む・救済なし・エラーなし', tr[-1]['ti'] >= 1 and not any(x['ph'] == 'help' for x in tr) and not errs, (tr[-1], errs))
    # ---- 3回とも失敗 → ルルの救済(英文が黒い吹き出し) ----
    cue0, tr, errs = run(br, base, 4, 3)
    resc = [x for x in tr if x['ph'] == 'help' and x['who'] == 'Lulu']
    chk('M6 3回目もカンペ付きで失敗すると、ルルが代わりに言い、その英文が黒い吹き出しに出て、物語が進む', bool(resc) and all(x['msg'] == cue0 for x in resc) and tr[-1]['ti'] >= 1 and any(t == cue0 for t in shown(tr, 1, cue0)) and any(t == cue0 for t in shown(tr, 2, cue0)), (len(resc), cue0))
    leak = [x for x in tr if not (x['ph'] == 'help' and x['who'] == 'Lulu') and x['msg'] and re.search(r'[A-Za-z]{3,}', x['msg']) and x['ph'] in ('cue', 'retry')]
    chk('M6b 救済のとき以外は、吹き出し(相手の文字)に英文が出ない', not leak and not errs, leak[:2])
    # ---- 次の自分の番は、また文字なしから ----
    ctx = newctx(br, {'mode': 4}); q = open_scene(ctx, base); wait_phase(q, 'cue'); q.wait_for_timeout(400)
    q.evaluate("()=>{window.__bad=1;window.__sayph.length=0}"); tr = trace(q); wait_phase(q, 'cue'); q.wait_for_timeout(600); nx = q.evaluate(CARD)
    chk('M7 次の自分の番は、また文字なしから始まる(カンペは「そのターンで1回つまずいたあと」だけ)', nx['ti'] >= 1 and nx['blind'] and nx['txt'] == '' and nx['tries'] == 0, nx)
    ctx.close()
    # ---- 既存モードに変化なし: モード3は1回つまずいても2回目はカンペなし・モード2は常にカンペなし ----
    cue0, tr, errs = run(br, base, 3, 1)
    chk('N1 モード3(087): 1回つまずいても2回目はカンペなし(変わらない)', all(t == '' for t in shown(tr, 1, cue0)) and shown(tr, 1, cue0) != [], sorted(set(shown(tr, 1, cue0))))
    cue0, tr, errs = run(br, base, 2, 2)
    chk('N2 モード2(耳学): 2回つまずいても3回目までカンペなし(変わらない)', all(t == '' for t in shown(tr, 1, cue0) + shown(tr, 2, cue0)), sorted(set(shown(tr, 2, cue0))))
    cue0, tr, errs = run(br, base, 0, 1)
    chk('N3 モード0(カンペ): いつもカンペあり(変わらない)', all(t == cue0 for t in shown(tr, 0, cue0) + shown(tr, 1, cue0)) and shown(tr, 0, cue0) != [], sorted(set(shown(tr, 0, cue0))))
    # ---- 設定から5つ目に切り替え ----
    ctx = newctx(br, {'mode': 0}, nomic=True); q = open_scene(ctx, base); wait_phase(q, 'cue'); q.wait_for_timeout(500)
    q.click('#sceneView .setbtn:not(.wb)'); q.wait_for_timeout(300)
    seg = q.evaluate("()=>[].map.call(document.querySelectorAll('#setBody .sseg')[0].querySelectorAll('button'),function(b){return b.textContent})")
    chk('C1 設定に5つのモード名(5つ目=%s)' % NAME4, len(seg) == 5 and seg[4] == NAME4 and seg[:4] == ['カンペモード', '耳学＆カンペモード', '耳学モード', '耳学（サポートカンペ付き）'], seg)
    q.evaluate("()=>document.querySelectorAll('#setBody .sseg')[0].querySelectorAll('button')[4].click()"); q.wait_for_timeout(200)
    saved = q.evaluate("()=>JSON.parse(localStorage.getItem('kd_prefs_v1'))")
    chk('C2 5つ目を選ぶと kd_prefs_v1 に mode:4 が保存され、ほかのキーはそのまま(新しい保存キーなし)', saved.get('mode') == 4 and saved.get('bgm') == 70 and set(saved) <= {'bgm', 'beat', 'voice', 'rate', 'silent', 'big', 'pitch', 'mode'}, saved)
    q.evaluate("()=>[].filter.call(document.querySelectorAll('#setBody button'),function(b){return b.textContent==='モードの説明'})[0].click()"); q.wait_for_timeout(150)
    txt = q.evaluate("()=>{var p=document.querySelector('#setBody .mhelp');return p&&!p.hidden?p.innerText:null}")
    chk('C3 設定の「モードの説明」に、見出し・説明が指示書どおりの文言で1項目増えている・既存の4つはそのまま・禁止語なし', txt is not None and NAME4 in txt and DESC4 in txt and '基本は耳学モード。2回つまずいたら、3回目だけ文字が出ます。' in txt and not any(w in txt for w in FORBID), txt)
    q.evaluate("()=>[].filter.call(document.querySelectorAll('#setBody .mhelp button'),function(b){return b.textContent==='とじる'})[0].click()"); q.wait_for_timeout(100)
    q.evaluate("()=>{window.__say.length=0}"); q.click('#setBack'); q.wait_for_timeout(1200)
    s = q.evaluate(SNAP)
    chk('C4 設定を閉じると、いまの番がモード4で描き直される(文字なし・お手本が自動で流れる)', s['cardBlind'] and s['cardText'].strip() == '' and s['msg'] == '', (s['cardText'], s['msg']))
    chk('C5 エラーなし', not q.errs and not q.evaluate("()=>window.__errs"), q.errs)
    ctx.close()
    # ---- タイトル画面(world) ----
    ctx = br.new_context(viewport={'width': 375, 'height': 667}); ctx.add_init_script("try{if(!sessionStorage.getItem('__pf')){sessionStorage.setItem('__pf','1');localStorage.setItem('kd_prefs_v1',JSON.stringify({bgm:55,silent:1,mode:2}))}}catch(e){}")
    pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:160])); pg.goto(base + '/world/index.html'); pg.wait_for_timeout(800); pg.click('#startBtn'); pg.wait_for_timeout(300)
    st = pg.evaluate("()=>[].map.call(document.querySelectorAll('#mSel .mopt'),function(b){return b.querySelector('b').textContent+':'+b.getAttribute('aria-checked')})")
    chk('T1 タイトル: 5つのモード名(5つ目=%s)・前回(耳学=2)が選ばれている' % NAME4, st == ['カンペモード:false', '耳学＆カンペモード:false', '耳学モード:true', '耳学（サポートカンペ付き）:false', NAME4 + ':false'], st)
    pg.click('#mSel .mopt[data-m="4"]'); pg.wait_for_timeout(200)
    sv = pg.evaluate("()=>JSON.parse(localStorage.getItem('kd_prefs_v1'))")
    chk('T2 5つ目を選ぶと kd_prefs_v1 に mode:4 だけ足される(bgm・silent は壊さない)', sv == {'bgm': 55, 'silent': 1, 'mode': 4}, sv)
    pg.reload(); pg.wait_for_timeout(800); pg.click('#startBtn'); pg.wait_for_timeout(200)
    chk('T3 再訪時も5つ目が選ばれている(引き継ぎ)', pg.evaluate("()=>[].map.call(document.querySelectorAll('#mSel .mopt'),function(b){return b.getAttribute('aria-checked')})") == ['false', 'false', 'false', 'false', 'true'])
    pg.click('#mHelpBtn'); pg.wait_for_timeout(150)
    ht = pg.evaluate("()=>document.getElementById('mHelp').innerText")
    chk('T4 タイトルの「モードの説明」に、見出し・説明が指示書どおりの文言で出る・既存の4つはそのまま・禁止語なし', NAME4 in ht and DESC4 in ht and '基本は耳学モード。2回つまずいたら、3回目だけ文字が出ます。' in ht and not any(w in ht for w in FORBID), ht)
    r = pg.evaluate("()=>{var w=document.getElementById('cmdMain').getBoundingClientRect();return {wb:Math.round(w.bottom),H:innerHeight,top:Math.round(w.top)}}")
    chk('T5 説明を開いても、ウィンドウ全体が画面の中に収まる(375×667)', r['top'] >= 0 and r['wb'] <= r['H'], r)
    chk('T6 エラーなし', not errs, errs)
    ctx.close()
print()
print('すべて OK  (NG 0件)' if not bad else '失敗あり  (NG %d件)' % len(bad)); sys.exit(1 if bad else 0)
