# -*- coding: utf-8 -*-
"""タスク035: 鍛える音の集計と反映(ヘッドレス)。python3 tour-src/tests/test_train035.py
ページの中の関数(IIFEの内側)を、テストの中だけで取り出す(本番のHTMLには何も足さない)。マイク・実機は未確認。"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
HOOK = "window.__t={ts:trainSounds,pick:pickLessons,plog:plogLoad};"
def rec(tg, miss, v, hd='x', **kw):
    r = {'ts': 1, 'v': v, 'tg': tg, 'hd': hd, 'cf': 0, 'n': len(tg.split()), 'ok': len(tg.split()) - len(miss),
         'miss': [{'t': t, 'h': h, 'k': 'diff'} for t, h in miss]}
    r.update(kw); return r
def run(pw, base, path, seed, js):
    br = pw.chromium.launch(args=['--no-sandbox'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
    def patch(route):
        resp = route.fetch(); body = resp.text()
        if 'function trainSounds(){' in body: body = body.replace('function trainSounds(){', HOOK + 'function trainSounds(){', 1)
        route.fulfill(response=resp, body=body)
    ctx.route('**/*.html', patch); ctx.route('**/', patch)
    p = ctx.new_page(); errs = []; p.on('pageerror', lambda e: errs.append(str(e)[:200]))
    p.goto(base + path); p.wait_for_timeout(1200)
    if seed is not None:
        p.evaluate("(s)=>localStorage.setItem('kanpe-pron-v1',JSON.stringify(s))", seed)
    out = p.evaluate(js); br.close(); return out, errs
if __name__ == '__main__':
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    TS = "()=>JSON.parse(JSON.stringify(window.__t.ts().map(function(t){return {k:t.k,weak:Math.round(t.weak*1000)/1000,n:t.n,x:t.x,words:t.words}})))"
    fails = 0
    def check(name, cond, info=''):
        global fails
        print(('OK  ' if cond else 'NG  ') + name, info)
        if not cond: fails += 1
    with sync_playwright() as pw:
        for path in ['/dubai/', '/tour/', '/tour/doha/']:
            print('==', path)
            # 1 記録なし → 空
            r, e = run(pw, base, path, [], TS); check('記録なし→空', r == [] and not e, (r, e))
            # 2 記録が少ない(1単語・1場面だけ失敗) → 空
            s = [rec('think about it', [('think', 'sink')], 'a', hd='sink about it')]
            r, e = run(pw, base, path, s, TS); check('1単語1場面→空', r == [], r)
            # 3 2単語だが1場面だけ → 空
            s = [rec('think thank this', [('think', 'sink'), ('thank', 'sank')], 'a', hd='sink sank this')]
            r, e = run(pw, base, path, s, TS); check('2単語1場面→空(場面条件)', [t for t in r if t['k'] == 'th'] == [], r)
            # 4 2単語・2場面 → th が入る。弱さの式を手計算と突き合わせる
            s = [rec('think thank this', [('think', 'sink')], 'a', hd='sink thank this'),
                 rec('thirty three thing', [('thirty', 'dirty')], 'b', hd='dirty three thing')]
            r, e = run(pw, base, path, s, TS)
            th = [t for t in r if t['k'] == 'th']
            check('2単語2場面→th', len(th) == 1, r)
            if th:
                t = th[0]; exp = (t['x'] + 0.5) / (t['n'] + 2)
                check('式 (X+0.5)/(N+2)', abs(t['weak'] - round(exp, 3)) < 0.0011, (t['x'], t['n'], t['weak']))
                check('失敗した単語が入っている', set(['think', 'thirty']) <= set(t['words']), t['words'])
            # 5 上位は3つまで、弱さの大きい順(弱い音が4つ以上そろうデータ)
            s = [rec('think thirty five fine right red water window', [('think', 'sink'), ('five', 'hive'), ('right', 'light'), ('water', 'ater')], 'sA', hd='x'),
                 rec('think thirty five fine right red water window', [('thirty', 'dirty'), ('fine', 'hine'), ('red', 'led'), ('window', 'indow')], 'sB', hd='x')]
            r, e = run(pw, base, path, s, TS)
            check('上位ちょうど3つ', len(r) == 3, [(t['k'], t['weak']) for t in r])
            check('弱さは降順', all(r[i]['weak'] >= r[i + 1]['weak'] for i in range(len(r) - 1)), [(t['k'], t['weak']) for t in r])
            # 5b 合宿で言えた記録(camp、hdは空)は「出た回数」に入り、弱さが下がる。場面の数には入らない
            camp = [dict(rec('think', [], 'camp', hd='', camp=1, sok=1), okw=['think']) for _ in range(6)]
            r0, _ = run(pw, base, path, s, TS); r1, _ = run(pw, base, path, s + camp, TS)
            w0 = [t for t in r0 if t['k'] == 'th'][0]['weak']; w1 = [t for t in r1 if t['k'] == 'th'][0]['weak']
            check('合宿で言えるほど弱さが下がる', w1 < w0, (w0, w1))
            only_camp_fail = [rec('think thank', [('think', 'sink'), ('thank', 'sank')], 'camp', hd='', camp=1), rec('thirty thing', [('thirty', 'dirty'), ('thing', 'sing')], 'sA', hd='x')]
            r2, _ = run(pw, base, path, only_camp_fail, TS)
            check('合宿の失敗は「2場面」に数えない', [t for t in r2 if t['k'] == 'th'] == [], r2)
            # 6 何も聞こえなかった回(hd空)は数えない
            s = [rec('think thank this', [('think', None), ('thank', None)], 'a', hd=''), rec('thirty thing', [('thirty', None), ('thing', None)], 'b', hd='')]
            r, e = run(pw, base, path, s, TS); check('hd空は数えない', r == [], r)
            # 7 src の印(az/sr)があっても、無くても、同じ結果(024が入っても壊れない)
            base_s = [rec('think thank this', [('think', 'sink')], 'a', hd='sink thank this'), rec('thirty three thing', [('thirty', 'dirty')], 'b', hd='dirty three thing')]
            r0, _ = run(pw, base, path, base_s, TS)
            r1, _ = run(pw, base, path, [dict(x, src='az') for x in base_s], TS)
            r2, _ = run(pw, base, path, [dict(x, src='sr', bits='011', alts=[], diag='decl', why='ok', seg=1) for x in base_s], TS)
            r3, e3 = run(pw, base, path, [dict(x, src='az', ph=[['th', 40]], extra={'z': 1}) for x in base_s], TS)
            check('src=az/sr/未知の項目でも同じ', r0 == r1 == r2 == r3 and not e3, (r0, r1, r2, r3))
            # 8 壊れた記録が混ざっても落ちない
            r, e = run(pw, base, path, [None, 5, 'x', {'tg': 3, 'miss': 'x'}, {}, {'tg': 'think', 'hd': 'y', 'miss': [None, {'t': 5}]}] + base_s, TS)
            check('壊れた記録でも落ちない', not e and [t['k'] for t in r] == [t['k'] for t in r0], (r, e))
    print('FAILS', fails); sys.exit(1 if fails else 0)
