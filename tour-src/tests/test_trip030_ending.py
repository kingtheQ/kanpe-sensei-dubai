# -*- coding: utf-8 -*-
"""タスク030: 精算(29日目)とアルバムの1日1ページ。記録を仕込んで /tour/ending/ を開き、エラーなく進むか・画面の文字を見る。"""
import os, sys, json, time, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
os.makedirs('/tmp/t030', exist_ok=True)
SEED = {'v':1,'trip':1,'tk':'ow','day':8,'td':9,'ph':'morning','bun':1,
 'legs':[{'i':0,'fr':'HND','to':'DOH','d':1,'f':1,'l':1},{'i':1,'fr':'DOH','to':'NBO','d':2,'f':1,'l':1}],
 'days':[{'d':1,'td':1,'ph':{'s':'sage','k':'day','f':0},'led':[['ticket',1074300,'JPY']],'pick':[]},
         {'d':2,'td':2,'ph':{'s':'taxi','k':'day','f':0},'led':[['sim',1000,'KES'],['taxi',3000,'KES']],'pick':[]},
         {'d':3,'td':5,'ph':{'s':'nap','k':'nap','f':0},'led':[],'pick':[]},
         {'d':4,'td':6,'ph':{'s':'dgate','k':'day','f':0},'led':[['duty',24,'USD']],'pick':[]},
         {'d':5,'td':7,'ph':{'s':'csouq','k':'peak','f':0},'led':[['gift',22,'QAR'],['dinner',80,'QAR']],'pick':['metro']}],
 'cur':{'led':[],'pick':[]}}
with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
    ctx.add_init_script("try{if(!localStorage.getItem('kanpe-set-v1'))localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));if(!sessionStorage.getItem('seeded')){sessionStorage.setItem('seeded','1');localStorage.setItem('kanpe-trip-v1',%s)}}catch(e){}" % json.dumps(json.dumps(SEED)))
    p = ctx.new_page(); errs = []; p.on('pageerror', lambda e: errs.append(str(e)[:160]))
    p.goto(base + '/tour/ending/'); p.wait_for_timeout(500)
    print('settle:', p.evaluate("()=>JSON.stringify(TRIP.settle())"))
    print('album pages:', p.evaluate("()=>TRIP.albumPages().map(function(x){return x.d+'|'+x.stub+'|'+x.line})"))
    seen = []; t0 = time.time(); n = 0
    while time.time() - t0 < 110:
        m = p.evaluate("()=>(document.getElementById('msgText')||document.querySelector('.msg')||{}).textContent||''")
        if m and (not seen or seen[-1] != m):
            seen.append(m); print('  say:', m)
            if re.match(r'^Day [345]\.$', m) or m.startswith('We spent'): p.screenshot(path='/tmp/t030/end_%s.png' % re.sub(r'\W','',m)[:8])
        p.evaluate("()=>{var o=document.querySelector('.trip-ov');if(o&&!o.busy)o.click()}")
        p.wait_for_timeout(300)
    print('errors:', errs)
    br.close()
