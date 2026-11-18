# -*- coding: utf-8 -*-
"""タスク032 項目4(020-8): スパルタ時間の置き場所(休養の翌日の★)。python3 tour-src/tests/test_sparta032.py
枠だけ: (1) 表の置き方(前の日が休養・この日が★) (2) 入口(朝の1枚のあと 強化合宿が開く) (3) 終わり(合宿を終えたら その日が終わって夜の1枚)
(4) ふつうの日・休養日・ほかの合宿の入り方は 変わらない (5) 記録(kanpe-trip-v1)の互換。中身は いまある強化合宿のまま。ヘッドレス。"""
import os, sys, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
LEGS = [('HND', 'DOH'), ('DOH', 'NBO'), ('NBO', 'DOH'), ('DOH', 'HEL'), ('HEL', 'RVN'), ('RVN', 'MAD'), ('MAD', 'LIM'), ('LIM', 'CUZ'), ('CUZ', 'LIM'), ('LIM', 'MIA'), ('MIA', 'DFW'), ('DFW', 'HNL'), ('HNL', 'HND')]
def seed(landed, ph, td, day):
    return {'v': 1, 'trip': 1, 'tk': 'ow', 'day': day, 'td': td, 'ph': ph, 'bun': 1,
            'legs': [{'i': i, 'fr': a, 'to': b, 'd': None, 'f': 1 if i < landed else 0, 'l': 1 if i < landed else 0} for i, (a, b) in enumerate(LEGS)],
            'days': [], 'cur': {'led': [], 'pick': []}}
bad = 0; ERR = []
def chk(name, ok, info=''):
    global bad
    print(('OK ' if ok else 'NG ') + name, info)
    if not ok: bad += 1
OV = "()=>{var o=document.querySelector('.trip-ov');return o?o.innerText.replace(/\\s+/g,' ').slice(0,160):null}"
VIEWS = "()=>[].filter.call(document.querySelectorAll('[id$=View]'),function(x){return !x.hidden}).map(function(x){return x.id})"
def page(ctx, base, sd, url='/tour/'):
    q = ctx.new_page(); q.on('pageerror', lambda e: ERR.append(str(e)[:160]))
    q.add_init_script("localStorage.setItem('kanpe-trip-v1',%s);localStorage.setItem('kanpe-tour-save-v1','{\"seen\":{},\"ticket\":\"ow\"}');localStorage.setItem('kd_prefs_v1','{\"silent\":1}')" % json.dumps(json.dumps(sd)))
    q.goto(base + url); q.wait_for_timeout(1500); return q
if __name__ == '__main__':
    with sync_playwright() as pw:
        srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
        br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
        q = page(ctx, base, seed(12, 'morning', 24, 23), '/tour/')
        # (1) 置き方
        r = q.evaluate("()=>TRIP.spartaRule()"); chk('置き方: oneworld 24日目・スター 22日目は 前の日が休養・この日が★', r == {'ow': True, 'star': True}, r)
        chk('スパルタの日の判定 TRIP.isSparta(24)', q.evaluate("()=>[TRIP.isSparta(24),TRIP.isSparta(23),TRIP.isSparta(25)]") == [True, False, False])
        # (2) 入口: 朝の1枚 → タップ → 強化合宿(いまある合宿の画面)が開く
        o = q.evaluate(OV); print('朝', o); chk('朝の1枚 DAY 24', bool(o) and 'DAY 24' in o and 'Lulu has a plan' in o, o)
        q.evaluate("()=>document.querySelector('.trip-ov').click()"); q.wait_for_timeout(1500)
        v = q.evaluate(VIEWS); chk('タップのあと 強化合宿(phoView)が開く', v == ['phoView'], v)
        # (3) 終わり: 合宿を最後まで通す(声を出さないモード: おして よむ で通る)→ マップに戻り、夜の1枚
        t0 = time.time(); night = None
        while time.time() - t0 < 120:
            night = q.evaluate(OV)
            if night and 'Good night' in night: break
            q.evaluate("()=>{var b=document.getElementById('phoAct');if(b&&b.offsetParent&&!b.disabled)b.click();var n=document.getElementById('phoNext');if(n&&n.offsetParent)n.click()}")
            q.wait_for_timeout(450)
        print('合宿のあと', night, q.evaluate(VIEWS)); chk('合宿を終えると夜の1枚(DAY 24)', bool(night) and 'DAY 24' in night and 'Good night' in night, night)
        t = q.evaluate("()=>JSON.parse(localStorage.getItem('kanpe-trip-v1'))"); chk('夜のあいだ ph=night・cur.sp=1', t['ph'] == 'night' and t['cur'].get('sp') == 1, [t['ph'], t['cur']])
        q.wait_for_timeout(1600); q.evaluate("()=>document.querySelector('.trip-ov').click()"); q.wait_for_timeout(900)
        t = q.evaluate("()=>JSON.parse(localStorage.getItem('kanpe-trip-v1'))"); d = t['days'][-1] if t['days'] else {}
        chk('夜を閉じると 24日目の記録に sp=1', d.get('d') == 24 and d.get('td') == 24 and d.get('sp') == 1, d)
        # 次の日(25)は表では未実装の日(場所なし)。いまは 夜のあと 'wait'(未実装の日は飛ばす)になる
        print('その後', t['ph'], t['td']); q.close()
        # (4a) スパルタの日に 合宿を2回やっても その日の終わりは1回だけ(spartaDone は2回目は何もしない)
        q = page(ctx, base, seed(12, 'day', 24, 24)); r = q.evaluate("()=>{var a=TRIP.spartaDone(function(){}),b=TRIP.spartaDone(function(){});return [a,b]}")
        chk('spartaDone は 1回目だけ true', r == [True, False], r); q.close()
        # (4b) ふつうの日(6日目)に 合宿をやっても 何も起きない(夜の1枚が出ない)
        q = page(ctx, base, seed(2, 'day', 6, 6)); r = q.evaluate("()=>[TRIP.spartaDone(function(){}),!!document.querySelector('.trip-ov')]")
        chk('ふつうの日は spartaDone が何もしない', r == [False, False], r); q.close()
        # (5) 互換: sp のない古い記録(030 の形)を読んでも壊れない。保存キーは同じ
        old = seed(2, 'day', 6, 6); old['days'] = [{'d': 1, 'td': 1, 'ph': {'s': 'sage', 'k': 'day', 'f': 0}, 'led': [], 'pick': []}]
        q = page(ctx, base, old); t = q.evaluate("()=>{var s=TRIP.state();return [s.days.length,s.days[0].sp,TRIP.KEY]}")
        chk('古い記録を読める(sp は 0 になる・キーは kanpe-trip-v1)', t == [1, 0, 'kanpe-trip-v1'], t); q.close()
        chk('JSエラーなし', not ERR, ERR); br.close()
    print('NG件数', bad); sys.exit(1 if bad else 0)
