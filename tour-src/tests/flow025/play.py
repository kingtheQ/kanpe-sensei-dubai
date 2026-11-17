import sys, json, time, threading, http.server, socketserver
from playwright.sync_api import sync_playwright
import os; ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads=True
def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s,*a,**k): super().__init__(*a,directory=d,**k)
        def log_message(s,*a): pass
    srv=Q(('127.0.0.1',0),H); threading.Thread(target=srv.serve_forever,daemon=True).start(); return srv
INIT="""
window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});
try{speechSynthesis.speak=function(u){setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}
(function(){function FS(){}
FS.prototype.start=function(){var me=this;setTimeout(function(){var t=[].map.call(document.querySelectorAll('.cue .w'),function(x){return x.textContent}).join(' ');var rs=[{transcript:t,confidence:.9}];rs.isFinal=true;
 if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},20)},60)};
FS.prototype.abort=FS.prototype.stop=function(){};window.SpeechRecognition=FS;window.webkitSpeechRecognition=FS})();
"""
def btns(p):
    return p.evaluate("""()=>{var b=[].slice.call(document.querySelectorAll('button, .opt'));
      return b.filter(function(x){return !x.disabled&&x.offsetParent}).map(function(x){return x.textContent.trim().slice(0,30)})}""")
if __name__=='__main__':
    srv=serve(ROOT); base='http://127.0.0.1:%d'%srv.server_address[1]
    with sync_playwright() as pw:
        br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
        ctx=br.new_context(viewport={'width':390,'height':780}); ctx.add_init_script(INIT)
        p=ctx.new_page(); p.on('pageerror',lambda e:print('PAGEERR',str(e)[:150]))
        p.goto(base+'/world/'); p.wait_for_timeout(800)
        print('title btns',btns(p))
        p.click('#startBtn'); p.wait_for_timeout(300); print(btns(p))
        p.click('#cNew'); p.wait_for_timeout(1500)
        print('URL after はじめから:',p.url)
        for i in range(25):
            print(i,p.url.replace(base,''),btns(p)[:8]); p.wait_for_timeout(1200)
            p.screenshot(path='/tmp/t025_shots/s%02d.png'%i)
            if i==3: break
        br.close()
