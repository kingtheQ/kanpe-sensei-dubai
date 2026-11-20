# -*- coding: utf-8 -*-
"""タスク043: 羽田の出発の場面(チェックイン→保安検査→出国→出発ゲート→搭乗→機内)の通し(ヘッドレス)。
TK=ow|star python3 tour-src/tests/test_hnd043.py  マイクは偽の音声認識。実機は未確認。"""
import os, sys, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
from auto import click_any
from test_trip030 import ovstep, play_until, ev, trip, OV
TK = os.environ.get('TK', 'ow')
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text()
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save};" + HOOK, 1) if HOOK in body else body)
bad = []
def chk(n, ok, v=''):
    print(('OK  ' if ok else 'NG  ') + n, v)
    if not ok: bad.append(n)
if __name__ == '__main__':
    with sync_playwright() as pw:
        srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
        br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT);
        ctx.add_init_script("try{if(!localStorage.getItem('kanpe-set-v1'))localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}))}catch(e){}")
        p = ctx.new_page(); errs = []; p.on('pageerror', lambda e: errs.append(str(e)[:160]))
        p.route('**/tour/index.html', hooked); p.route('**/tour/', hooked); p.route('**/tour/?*', hooked); p.route('**/tour/#*', hooked)
        keys0 = None
        ctx.add_init_script("try{if(!localStorage.getItem('kanpe-tour-save-v1'))localStorage.setItem('kanpe-tour-save-v1',JSON.stringify({v:1,ticket:'%s',seen:%s}))}catch(e){}" % (TK, json.dumps({k+'_'+TK if k in ('hnd_checkin','hnd_gate','hnd_board','ticket') else k:1 for k in ['hnd_checkin','hnd_sec','hnd_exit','hnd_gate','hnd_board','ticket']}) if os.environ.get('SEEDED') else '{}'))
        p.goto(base + '/tour/'); p.wait_for_timeout(2500)
        print('TRIP?', ev(p, "()=>typeof TRIP"))
        ev(p, "()=>{TRIP.setTicket('%s',0);TRIP.save()}" % TK); p.reload(); p.wait_for_timeout(2500)
        keys0 = ev(p, "()=>Object.keys(localStorage).sort()")
        print('trip', json.dumps(trip(p))[:200])
        seq = []
        def hdep(q):
            return ev(q, "()=>{var G=__T.G;var v=G.scene&&G.scene.vid;return {v:v||null,bg:G.scene&&G.scene.d&&G.scene.d.bg||null,url:location.pathname}}")
        T0 = time.time(); LASTP = [0]
        def cond(q):
            if time.time() - LASTP[0] > 25:
                LASTP[0] = time.time(); print('   t=%d' % (time.time() - T0), btns(q)[:6], q.url.replace(base, ''))
            if '/world/' in q.url: return True
            try:
                r = hdep(q)
                if r['v'] and (not seq or seq[-1][0] != r['v']): seq.append((r['v'], r['bg'])); print('   scene', r['v'], r['bg'])
                if not r['v']:
                    ids = ['hcheckin','hsec','hexit','hgate','hboard','hplane']
                    ev(q, "(ids)=>{for(var i=0;i<ids.length;i++){var n=document.querySelector('.node[data-id='+ids[i]+']');if(n&&!n.classList.contains('lock')&&!n.classList.contains('done')){n.click();return}}}".replace('(ids)=>','()=>').replace('ids.length','%d' % 6).replace('ids[i]',"['hcheckin','hsec','hexit','hgate','hboard','hplane'][i]"))
            except Exception as e: print('ERR', str(e)[:100])
            return False
        print('チケット', ev(p, "()=>__T.save.ticket"), 'モード', ev(p, "()=>document.querySelector('.tab.on,.mtab.on')&&document.querySelector('.tab.on,.mtab.on').textContent"))
        p.screenshot(path='/tmp/t043_after_ticket.png')
        ok = play_until(p, 60, cond); p.screenshot(path='/tmp/t043_scene.png'); print('btns', btns(p)); ok = play_until(p, 1500, cond)
        print('終点', ok, p.url.replace(base, ''))
        print('場面の並び', [s[0] for s in seq])
        print('背景', [s[1] for s in seq])
        print('keep(世界側の保存):', ev(p, "()=>JSON.parse(localStorage.getItem('kanpe-tour-save-v1')||'{}').keep"))
        print('keys 増減', sorted(set(ev(p, "()=>Object.keys(localStorage)")) ^ set(keys0)))
        print('trip legs', json.dumps((trip(p) or {}).get('legs'))[:300])
        if ok and '/world/' in p.url:
            t0 = time.time()
            while time.time() - t0 < 90 and '/tour/' not in p.url: p.wait_for_timeout(500)
            p.wait_for_timeout(3000)
            print('着陸後 URL', p.url.replace(base, ''), 'OV', ev(p, OV))
            t = trip(p) or {}
            print('着陸後 here/legs', [(l['fr'], l['to'], l['f'], l['l']) for l in t.get('legs', [])[:3]], 'day', t.get('day'), 'ph', t.get('ph'))
            p.screenshot(path='/tmp/t043_arrive.png')
        print('errors', errs)
        br.close()
