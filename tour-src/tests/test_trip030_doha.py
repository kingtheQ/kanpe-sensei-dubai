# -*- coding: utf-8 -*-
"""タスク030: ドーハのページで、日の鍵(到着の場所は開き、市内は7日目まで閉じる)を確かめる。"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
legs=[('HND','DOH'),('DOH','NBO'),('NBO','DOH'),('DOH','HEL'),('HEL','RVN'),('RVN','MAD'),('MAD','LIM'),('LIM','CUZ'),('CUZ','LIM'),('LIM','MIA'),('MIA','DFW'),('DFW','HNL'),('HNL','HND')]
SEED={'v':1,'trip':1,'tk':'ow','day':4,'td':6,'ph':'day','bun':1,
 'legs':[{'i':i,'fr':a,'to':b,'d':None,'f':1 if i<3 else 0,'l':1 if i<3 else 0} for i,(a,b) in enumerate(legs)],'days':[],'cur':{'led':[],'pick':[]}}
with sync_playwright() as pw:
    srv=serve(ROOT);base='http://127.0.0.1:%d'%srv.server_address[1]
    br=pw.chromium.launch(args=['--no-sandbox']);ctx=br.new_context(viewport={'width':390,'height':780});ctx.add_init_script(INIT)
    ctx.add_init_script("localStorage.setItem('kanpe-trip-v1',%s);localStorage.setItem('kanpe-tour-save-v1','{\"seen\":{},\"ticket\":\"ow\"}')"%json.dumps(json.dumps(SEED)))
    p=ctx.new_page();errs=[];p.on('pageerror',lambda e:errs.append(str(e)[:150]))
    p.goto(base+'/tour/doha/');p.wait_for_timeout(1500)
    print('overlay:',p.evaluate("()=>!!document.querySelector('.trip-ov')"))
    print('locked arr:',p.evaluate("()=>['dimmig','dbag','dsim','dride'].map(function(i){return i+':'+TRIP.lockedPlace(i)})"))
    print('locked city/dep:',p.evaluate("()=>['calley','chotel','cbreak','dcounter'].map(function(i){return i+':'+TRIP.lockedPlace(i)})"))
    print('tabs:',p.evaluate("()=>[].map.call(document.querySelectorAll('.mbtn'),function(b){return b.textContent+':'+b.hidden+':'+TRIP.lockedMode(b.dataset.m)})"))
    p.screenshot(path='/tmp/t030/doha_arr.png')
    print('errors',errs);br.close()
