# -*- coding: utf-8 -*-
"""タスク032 項目3(020-10): 29日目の読み上げ5項目のうち 手数料・別切符 と 選んだ重さ。python3 tour-src/tests/test_settle032.py
(1) 別切符の区間をちぎると、記録帳(kanpe-trip-v1)に 1回だけ ['sep',95,'USD'] が載る(tearNow と fly の両方)  (2) 手数料は addFee で載る
(3) settle / settleExtra が その記録を数える  (4) 精算の読み上げ(ending ページ)に 5項目が順に出る。ヘッドレス。"""
import os, sys, json, re, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
LEGS = [('HND', 'DOH'), ('DOH', 'NBO'), ('NBO', 'DOH'), ('DOH', 'HEL'), ('HEL', 'RVN'), ('RVN', 'MAD'), ('MAD', 'LIM'), ('LIM', 'CUZ'), ('CUZ', 'LIM'), ('LIM', 'MIA'), ('MIA', 'DFW'), ('DFW', 'HNL'), ('HNL', 'HND')]
def seed(landed, ph, td, days=None):
    return {'v': 1, 'trip': 1, 'tk': 'ow', 'day': 17, 'td': td, 'ph': ph, 'bun': 1,
            'legs': [{'i': i, 'fr': a, 'to': b, 'd': None, 'f': 1 if i < landed else 0, 'l': 1 if i < landed else 0} for i, (a, b) in enumerate(LEGS)],
            'days': days or [], 'cur': {'led': [], 'pick': []}}
bad = 0; ERR = []
def chk(name, ok, info=''):
    global bad
    print(('OK ' if ok else 'NG ') + name, info)
    if not ok: bad += 1
def page(ctx, base, sd, url='/tour/ending/'):
    q = ctx.new_page(); q.on('pageerror', lambda e: ERR.append(str(e)[:160]))
    q.add_init_script("if(!sessionStorage.getItem('s')){sessionStorage.setItem('s','1');localStorage.setItem('kanpe-trip-v1',%s)}" % json.dumps(json.dumps(sd)))
    q.goto(base + url); q.wait_for_timeout(600); return q
def tr(q): return q.evaluate("()=>JSON.parse(localStorage.getItem('kanpe-trip-v1'))")
if __name__ == '__main__':
    with sync_playwright() as pw:
        srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
        br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
        ctx.add_init_script("try{if(!localStorage.getItem('kanpe-set-v1'))localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}))}catch(e){}")
        # (1) 別切符をちぎる(tearNow): 7=リマ→クスコ(別切符)。2回ちぎっても 1回だけ載る。別切符でない区間(6)は載らない
        q = page(ctx, base, seed(6, 'day', 17), '/tour/')
        a = q.evaluate("()=>[TRIP.tearNow(6),JSON.stringify(TRIP.state().cur.led)]"); b = q.evaluate("()=>[TRIP.tearNow(7),JSON.stringify(TRIP.state().cur.led)]"); c2 = q.evaluate("()=>[TRIP.tearNow(7),JSON.stringify(TRIP.state().cur.led)]")
        print('tearNow', a, b, c2)
        chk('別切符でない区間は載らない', a[1] == '[]', a); chk('別切符は 1回だけ載る', b[1] == '[["sep",95,"USD"]]' and c2[0] is False and c2[1] == b[1], (b, c2))
        t = tr(q); chk('記録(kanpe-trip-v1)に残る', t['cur']['led'] == [['sep', 95, 'USD']], t['cur']); q.close()
        # (1b) 飛ぶ(fly)でも 同じ: クスコだけ「ある」ことにして、世界マップの飛ぶ経路を通す
        q = page(ctx, base, seed(7, 'day', 17), '/world/')
        r = q.evaluate("()=>{TRIP.IMPL.CUZ=1;var r=TRIP.fly('cusco');return [r&&r.tear,JSON.stringify(TRIP.state().cur.led)]}"); print('fly', r)
        chk('fly でも別切符が載る(1回)', r[0] == [7] and r[1] == '[["sep",95,"USD"]]', r); q.close()
        # (2) 夜のあいだ(ph night)は 直前の日の記録に足す。手数料(addFee)
        days = [{'d': 16, 'td': 16, 'ph': {'s': 'nap', 'k': 'nap', 'f': 0}, 'led': [['taxi', 3000, 'KES']], 'pick': ['taxi']}]
        q = page(ctx, base, seed(7, 'night', 17, days), '/tour/')
        r = q.evaluate("()=>{TRIP.IMPL.CUZ=1;TRIP.tearNow(7);var a=TRIP.addFee(6,'USD');var z=TRIP.addFee(0,'USD');return [a,z,JSON.stringify(TRIP.state().days[0].led),JSON.stringify(TRIP.state().cur.led)]}"); print('night', r)
        chk('夜のあいだは 直前の日の記録に載る', r[2] == '[["taxi",3000,"KES"],["sep",95,"USD"],["fee",6,"USD"]]' and r[3] == '[]' and r[0] is True and r[1] is False, r); q.close()
        # (3) settle / settleExtra
        days = [{'d': 1, 'td': 1, 'ph': {'s': 'sage', 'k': 'day', 'f': 0}, 'led': [['ticket', 1074300, 'JPY']], 'pick': []},
                {'d': 2, 'td': 2, 'ph': {'s': 'taxi', 'k': 'day', 'f': 0}, 'led': [['sim', 1000, 'KES'], ['fee', 6, 'USD'], ['sep', 95, 'USD']], 'pick': ['taxi', 'taxi', 'metro']},
                {'d': 3, 'td': 5, 'ph': {'s': 'nap', 'k': 'nap', 'f': 0}, 'led': [], 'pick': ['metro']}]
        q = page(ctx, base, seed(2, 'wait', 9, days))
        R = q.evaluate("()=>{var r=TRIP.settle();return {total:r.total,fee:r.fee,sep:r.sep,picks:r.picks,extra:TRIP.settleExtra(r)}}"); print('settle', R)
        chk('手数料 6USD=900円、別切符 95USD=14250円', R['fee'] == 900 and R['sep'] == 14250, R)
        chk('合計は ticket 1074300 + sim 1200 + fee 900 + sep 14250', R['total'] == 1074300 + 1200 + 900 + 14250, R['total'])
        chk('読み上げ4(手数料・別切符)', R['extra'][0] == 'Fees and separate tickets cost us 15,150 yen.', R['extra'])
        chk('読み上げ5(選んだ重さ: Taxi 2 / Metro 2)', R['extra'][1] == 'Taxi 2 times, metro 2 times.', R['extra'])
        # 手数料・別切符が 0 のとき / 選んだ記録が 0 のとき
        q2 = page(ctx, base, seed(2, 'wait', 9, [days[0]]))
        R2 = q2.evaluate("()=>TRIP.settleExtra(TRIP.settle())"); print('none', R2)
        chk('なかったときは「なかった」と読み、選んだ記録がなければ5は読まない', R2 == ['No fees this time. No separate tickets, either.'], R2); q2.close(); q.close()
        # (4) 精算の読み上げ: ending ページで 5項目が順に出る
        q = page(ctx, base, seed(2, 'wait', 9, days)); seen = []; t0 = time.time()
        while time.time() - t0 < 75:
            m = q.evaluate("()=>(document.getElementById('msgText')||document.querySelector('.msg')||{}).textContent||''")
            if m and (not seen or seen[-1] != m): seen.append(m); print('  say:', m)
            if q.evaluate("()=>!!document.querySelector('.trip-ov')"): break
            q.wait_for_timeout(250)
        want = ['We spent 1,090,650 yen on this trip.', 'The biggest day was day 2.', 'The metro saved us 2,009 yen that day.', 'Fees and separate tickets cost us 15,150 yen.', 'Taxi 2 times, metro 2 times.']
        # 文字は1字ずつ出るので、途中の文字列でも 7字以上なら その文の先頭と一致で数える
        idx = [next((i for i, m in enumerate(seen) if len(m) >= 7 and w.startswith(m)), -1) for w in want]
        chk('読み上げ5項目が この順で出る', all(i >= 0 for i in idx) and idx == sorted(idx), idx)
        chk('JSエラーなし', not ERR, ERR); q.close(); br.close()
    print('NG件数', bad); sys.exit(1 if bad else 0)
