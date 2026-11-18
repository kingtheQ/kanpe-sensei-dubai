# -*- coding: utf-8 -*-
"""タスク032 項目1(020-3): 場面の時刻は 旅の中の現地時刻。python3 tour-src/tests/test_time032.py
旅の中(その日を遊んでいる間)は TRIP.hourNow が場所ごとの旅の時刻を返し、nightNow / dohNight がそれで昼夜を決める。
旅の外(記録なし)・朝夜の1枚の間は、本当の時計のまま。ヘッドレス。"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *

def seed(tk, td, day, landed):
    legs = []
    return json.dumps({'v': 1, 'trip': 1, 'tk': tk, 'day': day, 'td': td, 'ph': 'day', 'bun': 1,
                       'legs': [{'i': i, 'fr': '', 'to': '', 'd': None, 'f': 1 if i < landed else 0, 'l': 1 if i < landed else 0, 'dt': ''} for i in range(13)],
                       'days': [], 'cur': {'led': [], 'pick': []}})

def run(p, base, page, tk, td, day, landed, places, probe):
    p.goto(base + '/world/'); p.evaluate("()=>localStorage.clear()")
    p.evaluate("(a)=>{localStorage.setItem('kanpe-trip-v1',a[0]);localStorage.setItem('kanpe-tour-save-v1',JSON.stringify({ticket:a[1],seen:{},v:1}))}", [seed(tk, td, day, landed), tk])
    p.goto(base + page); p.wait_for_timeout(900)
    out = {}
    for pid in places:
        out[pid] = p.evaluate("(a)=>{TRIP.hooks.at=function(){return a[0]};return [TRIP.hourNow(a[1]),%s]}" % probe, [pid, 'UTC'])
    return out

if __name__ == '__main__':
    bad = 0
    with sync_playwright() as pw:
        srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
        br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
        p = ctx.new_page(); errs = []; p.on('pageerror', lambda e: errs.append(str(e)[:160]))
        # ナイロビ(ow 2日目): 朝の到着
        r = run(p, base, '/tour/', 'ow', 2, 2, 1, ['immig', 'bag', 'sim', 'taxi', 'java', 'duty', 'qcheckin', 'gate', 'qplane'], "TRIP.hourNow(a[1])>=19||TRIP.hourNow(a[1])<5")
        print('NBO ow', r)
        exp = {'immig': (9, False), 'bag': (9, False), 'sim': (10, False), 'taxi': (10, False), 'java': (12, False), 'duty': (15, False),
               'qcheckin': (16, False), 'gate': (18, False), 'qplane': (19, True)}
        for k, (h, n) in exp.items():
            if r[k] != [h, n]: print('NG ow', k, r[k], (h, n)); bad += 1
        # スター 3日目: ナイロビ着は夜(01:25)
        r = run(p, base, '/tour/', 'star', 3, 3, 2, ['immig', 'bag', 'sim', 'taxi'], "TRIP.hourNow(a[1])>=19||TRIP.hourNow(a[1])<5")
        print('NBO star', r)
        for k, h in {'immig': 1, 'bag': 2, 'sim': 2, 'taxi': 3}.items():
            if r[k] != [h, True]: print('NG star', k, r[k]); bad += 1
        # ドーハ(ow 6〜9日)
        r = run(p, base, '/tour/doha/', 'ow', 7, 7, 3, ['dimmig', 'dride', 'calley', 'csouq', 'crest', 'cbreak', 'ccorn', 'dgate'], "[TRIP.hourNow(a[1])>=19||TRIP.hourNow(a[1])<5,TRIP.hourNow(a[1])>=18||TRIP.hourNow(a[1])<5]")
        print('DOH ow', r)
        exp = {'dimmig': (22, [True, True]), 'dride': (22, [True, True]), 'calley': (20, [True, True]), 'csouq': (19, [True, True]), 'crest': (20, [True, True]),
               'cbreak': (7, [False, False]), 'ccorn': (10, [False, False]), 'dgate': (15, [False, False])}
        for k, (h, nn) in exp.items():
            if r[k] != [h, nn]: print('NG doh', k, r[k], (h, nn)); bad += 1

        # 絵(dohNight)が 旅の時刻で昼夜を決めている: ドーハ市内 7日目。ccorn(朝10時)は昼の空、crest(20時)は夜の空
        sd = json.loads(seed('ow', 7, 7, 3))
        def sky(pid):
            q = ctx.new_page(); q.on('pageerror', lambda e: errs.append(str(e)[:160]))
            q.add_init_script("localStorage.setItem('kanpe-trip-v1',%s);localStorage.setItem('kanpe-tour-save-v1',%s)" % (json.dumps(json.dumps(sd)), json.dumps(json.dumps({'seen': {}, 'ticket': 'ow'}))))
            q.goto(base + '/tour/doha/'); q.wait_for_timeout(1200)
            q.evaluate("()=>{var b=document.querySelector('.mbtn[data-m=city]');if(b)b.click()}"); q.wait_for_timeout(500)
            q.evaluate("(id)=>document.querySelector('.node[data-id='+id+']').click()", pid); q.wait_for_timeout(2500)
            px = q.evaluate("()=>{var c=document.getElementById('scene');var d=c.getContext('2d').getImageData(6,6,1,1).data;return [d[0],d[1],d[2]]}")
            q.close(); return px
        a, b = sky('ccorn'), sky('crest')
        print('空の色 ccorn', a, 'crest', b)
        lum = lambda c: 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]
        if not (lum(a) > 120 and lum(b) < 90): print('NG 空の昼夜'); bad += 1
        # 旅の外(記録なし): 本当の時計(hourNow は tz の本当の時計と一致)
        p.goto(base + '/world/'); p.evaluate("()=>localStorage.clear()"); p.goto(base + '/tour/doha/'); p.wait_for_timeout(700)
        o = p.evaluate("()=>{TRIP.hooks.at=function(){return 'crest'};return [TRIP.hourNow('Asia/Qatar'),+new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Qatar',hour:'2-digit',hourCycle:'h23'}).format(new Date())]}")
        print('旅の外', o)
        if o[0] != o[1]: print('NG 旅の外'); bad += 1
        # 旅の中でも 朝の1枚・夜の1枚(ph が day でない)の間は本当の時計
        p.goto(base + '/world/'); p.evaluate("()=>localStorage.clear()")
        sd = json.loads(seed('ow', 7, 7, 3)); sd['ph'] = 'morning'
        p.evaluate("(a)=>{localStorage.setItem('kanpe-trip-v1',a);localStorage.setItem('kanpe-tour-save-v1',JSON.stringify({ticket:'ow',seen:{},v:1}))}", json.dumps(sd))
        p.goto(base + '/tour/doha/'); p.wait_for_timeout(700)
        o = p.evaluate("()=>{TRIP.hooks.at=function(){return 'crest'};return [TRIP.hourNow('Asia/Qatar'),+new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Qatar',hour:'2-digit',hourCycle:'h23'}).format(new Date())]}")
        print('朝の1枚の間', o)
        if o[0] != o[1]: print('NG 朝の1枚の間'); bad += 1
        print('JSエラー', errs); bad += len(errs)
        br.close()
    print('NG件数', bad); sys.exit(1 if bad else 0)
