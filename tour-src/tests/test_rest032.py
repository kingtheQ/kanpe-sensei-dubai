# -*- coding: utf-8 -*-
"""タスク032 項目2(020-7): 休養日は 単語バトル・合宿の入口を出さない。来るのは「知らせ」だけ。飽きたサインを数えない。
python3 tour-src/tests/test_rest032.py   ヘッドレス。ナイロビ(oneworld 5日目=休養日)で確かめる。"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
LEGS = [('HND', 'DOH'), ('DOH', 'NBO'), ('NBO', 'DOH'), ('DOH', 'HEL'), ('HEL', 'RVN'), ('RVN', 'MAD'), ('MAD', 'LIM'), ('LIM', 'CUZ'), ('CUZ', 'LIM'), ('LIM', 'MIA'), ('MIA', 'DFW'), ('DFW', 'HNL'), ('HNL', 'HND')]
def seed(tk, td, day, ph):
    return {'v': 1, 'trip': 1, 'tk': tk, 'day': day, 'td': td, 'ph': ph, 'bun': 1,
            'legs': [{'i': i, 'fr': a, 'to': b, 'd': None, 'f': 1 if i < 2 else 0, 'l': 1 if i < 2 else 0} for i, (a, b) in enumerate(LEGS)],
            'days': [], 'cur': {'led': [], 'pick': []}}
OV = "()=>{var o=document.querySelector('.trip-ov');return o?o.innerText.replace(/\\s+/g,' ').slice(0,160):null}"
def page(ctx, base, sd):
    q = ctx.new_page(); q.on('pageerror', lambda e: ERR.append(str(e)[:160]))
    q.add_init_script("localStorage.setItem('kanpe-trip-v1',%s);localStorage.setItem('kanpe-tour-save-v1',%s)" % (json.dumps(json.dumps(sd)), json.dumps(json.dumps({'seen': {}, 'ticket': 'ow'}))))
    q.goto(base + '/tour/'); q.wait_for_timeout(1500); return q
ERR = []; bad = 0
def chk(name, ok, info=''):
    global bad
    print(('OK ' if ok else 'NG ') + name, info)
    if not ok: bad += 1
if __name__ == '__main__':
    with sync_playwright() as pw:
        srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
        br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
        # A. 休養日の朝の1枚(5日目 ナイロビ): 知らせが出る。タップ→夜の1枚→(場面のない日なので)次の日の朝
        q = page(ctx, base, seed('ow', 5, 4, 'morning'))
        o = q.evaluate(OV); print('朝', o); q.screenshot(path='/tmp/t032_rest_morning.png')
        chk('朝の1枚に DAY 5 と NOTICE と知らせの文', bool(o) and 'DAY 5' in o and 'NOTICE' in o and 'strike' in o, o)
        chk('休養日の知らせのあいだ restToday が true', q.evaluate("()=>TRIP.restToday()") is True)
        q.evaluate("()=>document.querySelector('.trip-ov').click()"); q.wait_for_timeout(700)
        o = q.evaluate(OV); print('夜', o); chk('朝のあと夜の1枚(DAY 5 / Good night)', bool(o) and 'DAY 5' in o and 'Good night' in o, o)
        q.wait_for_timeout(1600); q.evaluate("()=>document.querySelector('.trip-ov').click()"); q.wait_for_timeout(900)
        o = q.evaluate(OV); print('次の朝', o); chk('夜のあと 6日目の朝(DAY 6、知らせなし)', bool(o) and 'DAY 6' in o and 'NOTICE' not in o, o)
        chk('夜を閉じたあと 合宿ボタンが戻る', q.evaluate("()=>document.getElementById('boothBtn').hidden") is False)
        t = q.evaluate("()=>JSON.parse(localStorage.getItem('kanpe-trip-v1'))")
        chk('記録: 5日目が日の記録に入り、その日の写真は昼寝', any(d['d'] == 5 and d['ph']['k'] == 'nap' for d in t['days']), json.dumps(t['days'])[:200]); q.close()
        # B. 休養日の途中(朝の1枚のあと閉じて開き直し=ph が day): 場面に入らず夜の1枚へ。マップのボタンは隠れ、場所は全部閉じ、合宿は始まらない
        q = page(ctx, base, seed('ow', 5, 5, 'day'))
        o = q.evaluate(OV); chk('開き直し: 夜の1枚(DAY 5)', bool(o) and 'DAY 5' in o and 'Good night' in o, o)
        s = q.evaluate("""()=>({booth:document.getElementById('boothBtn').hidden,rest:TRIP.restToday(),
          locks:['immig','bag','java','qcheckin'].map(function(i){return TRIP.lockedPlace(i)}),
          tabs:[].map.call(document.querySelectorAll('.mbtn'),function(b){return b.dataset.m+':'+TRIP.lockedMode(b.dataset.m)})})""")
        print('休養日の状態', s)
        chk('合宿ボタンは隠れる', s['booth'] is True); chk('場所は全部閉じる', all(s['locks']), s['locks'])
        q.evaluate("()=>{var o=document.querySelector('.trip-ov');if(o)o.remove()}")
        q.evaluate("()=>document.getElementById('boothBtn').click()"); q.wait_for_timeout(900)
        v = q.evaluate("()=>[].map.call(document.querySelectorAll('[id$=View]'),function(x){return x.id+':'+(x.hidden?'h':'v')+':'+(x.offsetParent?'show':'off')})")
        print('合宿ボタンを押したあとの画面', v)
        chk('合宿は始まらない(マップのまま)', any(x.startswith('mapView:') and x.endswith(':show') for x in v) and not any((x.startswith('phoView') or x.startswith('boothView') or x.startswith('sceneView')) and x.endswith(':show') for x in v), v)
        q.close()
        # C. 休養日でない日(6日目)は今までどおり: ボタンが出て、その日の場所が開く
        q = page(ctx, base, seed('ow', 6, 6, 'day'))
        s = q.evaluate("()=>({booth:document.getElementById('boothBtn').hidden,rest:TRIP.restToday(),lk:['java','qcheckin'].map(function(i){return TRIP.lockedPlace(i)})})")
        chk('6日目は合宿ボタンが出て、場所が開く', s['booth'] is False and s['rest'] is False and s['lk'] == [False, False], s); q.close()
        # D. 飽きたサインを休養日は数えない(コードの印)
        h = open(os.path.join(ROOT, 'tour', 'index.html'), encoding='utf-8').read()
        chk('evNote/evBored/evGate に休養日の除外', "S.d.win||TRIP.restToday())return;var e=evS()" in h and "if(TRIP.restToday())return false;return EVQ==='all'" in h and "if(EVQ==='off'||TRIP.restToday())return false" in h)
        chk('JSエラーなし', not ERR, ERR)
        br.close()
    print('NG件数', bad); sys.exit(1 if bad else 0)
