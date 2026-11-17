import sys, json, time
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from play import *
PREF=['GO！','送ってOK','送らない','これでOK','This is OK']
BATTLE="""()=>{var ch=[].slice.call(document.querySelectorAll('.choices .ch'));if(!ch.length)return null;window.__MAP=window.__MAP||{};
 var en=(document.querySelector('.prompt .en')||{}).textContent;var good=ch.filter(function(x){return x.classList.contains('good')})[0];
 if(good){window.__MAP[en]=good.textContent;return 'learn'}
 if(ch.every(function(x){return x.disabled}))return 'wait';
 var k=window.__MAP[en];var pick=ch.filter(function(x){return x.textContent===k})[0]||ch[0];pick.click();return 'battle:'+en+'>'+pick.textContent}"""
def click_any(p, avoid=('✕','🌏','もういちど','おてほん','ヘルプ','')):
    r=p.evaluate(BATTLE)
    if r: return r
    r=p.evaluate("""()=>{var b=[].slice.call(document.querySelectorAll('button')).filter(function(x){return !x.disabled&&x.offsetParent&&x.textContent.indexOf('マップに もどる')>=0});if(b.length){b[0].click();return 'MAPBACK'}return null}""")
    if r:
        p.wait_for_timeout(800); print('MAPDOM',p.evaluate("()=>document.getElementById('mapView').innerHTML")[:1500]); raise SystemExit
    return p.evaluate("""(av)=>{var pref=%s;var b=[].slice.call(document.querySelectorAll('#panel button, #panel .opt, .wmodal button, button')).filter(function(x){return !x.disabled&&x.offsetParent});
      var t=function(x){return x.textContent.trim()};
      for(var k=0;k<pref.length;k++)for(var i=0;i<b.length;i++)if(t(b[i]).indexOf(pref[k])===0){b[i].click();return t(b[i])}
      var c=b.filter(function(x){var s=t(x);return s&&av.every(function(a){return a===''||s.indexOf(a)<0})});if(c.length){c[0].click();return t(c[0])}return null}"""%json.dumps(PREF), list(avoid))
def run(p, base, secs, until, log):
    t0=time.time(); last=None
    while time.time()-t0<secs:
        if until(p): return True
        b=btns(p); u=p.url.replace(base,'')
        sig=(u,tuple(b))
        if sig!=last: log.append((round(time.time()-t0),u,b[:7])); last=sig
        r=click_any(p)
        p.wait_for_timeout(400)
    return False
if __name__=='__main__':
    srv=serve(ROOT); base='http://127.0.0.1:%d'%srv.server_address[1]
    with sync_playwright() as pw:
        br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
        ctx=br.new_context(viewport={'width':390,'height':780}); ctx.add_init_script(INIT); ctx.add_init_script("try{if(!localStorage.getItem('kanpe-set-v1'))localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}))}catch(e){}")
        p=ctx.new_page(); p.on('pageerror',lambda e:print('PAGEERR',str(e)[:150]))
        p.goto(base+'/world/'); p.wait_for_timeout(800)
        p.click('#startBtn'); p.click('#cNew'); p.wait_for_timeout(1200)
        log=[]
        ok=run(p,base,150,lambda q:'/world/' in q.url,log)
        for l in log: print(l)
        print('reached world:',ok,p.url)
        print('tour save:',p.evaluate("localStorage.getItem('kanpe-tour-save-v1')")[:300])
        print('world save:',p.evaluate("localStorage.getItem('kanpe-world-v1')"))
        p.screenshot(path='/tmp/t025_shots/after_buy.png')
        br.close()
