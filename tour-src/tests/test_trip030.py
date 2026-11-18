# -*- coding: utf-8 -*-
"""タスク030: 旅の骨組みの通し(ヘッドレス)。python3 tour-src/tests/test_trip030.py
はじめから → DAY 1 の朝の1枚 → 賢者 → 窓口で券 → つづり → 夜の1枚 → 世界マップ(区間 n / 13)→ ナイロビ(DAY 2)。マイクは偽の音声認識。実機は未確認。"""
import os, sys, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
from auto import click_any
os.makedirs('/tmp/t030', exist_ok=True)
OV = """()=>{var o=document.querySelector('.trip-ov');if(!o)return null;return {t:o.innerText.replace(/\\s+/g,' ').slice(0,100),busy:!!o.busy,torn:!!o.querySelector('.trip-torn')}}"""
LOG = []
def ovstep(p):
    o = p.evaluate(OV)
    if not o: return False
    if not LOG or LOG[-1] != o['t']: LOG.append(o['t']); print('   OV', o['t'])
    if o['busy'] or o['torn']: p.wait_for_timeout(700); return True
    p.evaluate("()=>{var o=document.querySelector('.trip-ov');if(o&&!o.busy)o.click()}"); p.wait_for_timeout(500); return True
def play_until(p, secs, cond):
    t0 = time.time()
    while time.time() - t0 < secs:
        if cond(p): return True
        if ovstep(p): continue
        try: click_any(p)
        except Exception: pass
        p.wait_for_timeout(300)
    return False
def ev(p, js): return p.evaluate(js)
def trip(p): return ev(p, "()=>JSON.parse(localStorage.getItem('kanpe-trip-v1')||'null')")
def kind(): return os.environ.get('TK', 'ow')
if __name__ == '__main__':
    with sync_playwright() as pw:
        srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
        br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
        ctx.add_init_script("try{if(!localStorage.getItem('kanpe-set-v1'))localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}))}catch(e){}")
        p = ctx.new_page(); errs = []; p.on('pageerror', lambda e: errs.append(str(e)[:160]))
        p.goto(base + '/world/'); p.wait_for_timeout(700)
        p.click('#startBtn'); p.click('#cNew'); p.wait_for_timeout(1500)
        print('1 URL', p.url.replace(base, ''))
        ov = ev(p, OV); print('1 朝の1枚', ov); p.screenshot(path='/tmp/t030/a_day1.png')
        hub = lambda q: ev(q, "()=>[].slice.call(document.querySelectorAll('button')).some(function(x){return x.offsetParent&&x.textContent.indexOf('マップに もどる')>=0})")
        print('1 賢者の会話を終えた', play_until(p, 170, hub))
        print('1 trip', trip(p))
        ev(p, "()=>{var b=[].slice.call(document.querySelectorAll('button')).filter(function(x){return x.textContent.indexOf('マップに もどる')>=0});b[0].click()}"); p.wait_for_timeout(800)
        ev(p, "()=>document.querySelector('.node[data-id=ticket]').click()"); p.wait_for_timeout(1500)
        print('2 窓口→world', play_until(p, 450, lambda q: '/world/' in q.url), p.url.replace(base, ''))
        p.wait_for_timeout(1500)
        t = trip(p); print('2 trip', json.dumps(t)[:400], 'bytes', len(json.dumps(t)))
        print('2 world: ', ev(p, "()=>[document.getElementById('curName').textContent,document.getElementById('cntClear').textContent,document.getElementById('pips').children.length,!document.getElementById('mBundle').hidden]"))
        p.screenshot(path='/tmp/t030/b_world.png')
        p.click('#mBundle'); p.wait_for_timeout(900); p.screenshot(path='/tmp/t030/c_bundle.png'); print('2 bundle', ev(p, OV)); ev(p, "()=>document.querySelector('.trip-ov').click()")
        p.click('#mGate'); p.wait_for_timeout(700)
        print('3 gate', ev(p, "()=>[].map.call(document.querySelectorAll('#opts .opt'),function(x){return x.textContent.trim()})")); p.screenshot(path='/tmp/t030/d_gate.png')
        ev(p, "()=>{var o=[].slice.call(document.querySelectorAll('#opts .opt'));var t=o.filter(function(x){return x.textContent.indexOf('西へ')>=0})[0];t.click()}")
        # ちぎる→飛ぶ
        t0 = time.time()
        while time.time() - t0 < 25 and '/tour/' not in p.url:
            o = ev(p, OV)
            if o and not LOG.count(o['t']): LOG.append(o['t']); print('   OV', o['t'])
            p.wait_for_timeout(500)
        p.wait_for_timeout(2500)
        print('3 URL', p.url.replace(base, ''))
        print('3 着陸後', ev(p, OV)); p.screenshot(path='/tmp/t030/e_day2.png')
        print('3 trip', json.dumps(trip(p))[:500])
        print('errors', errs)
        br.close()
