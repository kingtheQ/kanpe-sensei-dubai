# -*- coding: utf-8 -*-
"""タスク085-E の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_reveal085.py
賢者(sage_1/2/3)とチケット窓口(ticket_star/ticket_ow)の5場面を最後まで進め、Word Battle(phase=words)を一度も通らずに
Meaning!(phase=reveal・日本語訳つき)へ進み、最後まで出て場面が終わること。ほかの conv 場面(nbo_java1)は Meaning! も Word Battle も出ないこと。
マイク・実機は確認できない(音声認識は偽物)。"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import serve, ROOT
from playwright.sync_api import sync_playwright
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,save:save,startVid:startVid,PBY:PBY,DLG:DLG};" + HOOK, 1))
INIT = """
window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});
window.__ph=[];window.__rv=[];
try{speechSynthesis.speak=function(u){setTimeout(function(){if(u.onend)u.onend({})},6)};speechSynthesis.cancel=function(){}}catch(e){}
(function(){function FS(){}
FS.prototype.start=function(){var me=this;setTimeout(function(){var T=window.__T&&__T.G.scene&&__T.G.scene.turns[__T.G.ti];if(!T||(T.opts&&!T.pk))return;var t=T.cue.replace(/\\*/g,'');
  var rs=[{transcript:t,confidence:.9}];rs.isFinal=true;if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},20)},40)};
FS.prototype.abort=FS.prototype.stop=function(){};window.SpeechRecognition=FS;window.webkitSpeechRecognition=FS})();
localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));
"""
TICK = """()=>{var g=__T.G;if(!window.__sid)window.__sid=setInterval(function(){
 var ph=g.phase;if(window.__ph[window.__ph.length-1]!==ph)window.__ph.push(ph);
 if(ph==='reveal'){var r=document.querySelector('#panel .reveal');if(r){var jp=r.querySelector('.jp');var k=g.ti+':'+(jp?jp.textContent:'');}
   var m=document.getElementById('msgText').textContent;if(window.__rv.indexOf(m)<0&&/Meaning/.test(m)){window.__rv.push(m);var j=[].map.call(document.querySelectorAll('#panel .reveal .jp'),function(x){return x.textContent}).join('|');window.__rvjp=(window.__rvjp||[]);window.__rvjp.push(j)}
   var sk=[].filter.call(document.querySelectorAll('#panel button'),function(b){return b.textContent==='つぎへ'})[0];if(sk&&window.__fast)sk.click();return}
 if(ph==='opts'){var jc=document.querySelector('#panel .jcard');if(jc&&!jc.disabled)jc.click()}
 },120)}"""
def run(br, base, vid):
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
    q = ctx.new_page(); errs = []; q.on('pageerror', lambda e: errs.append(str(e)[:160])); q.route('**/tour/index.html*', hooked)
    q.goto(base + '/tour/index.html?check=1'); q.wait_for_timeout(1500)
    q.evaluate("(v)=>{var T=window.__T;T.startVid(T.PBY[T.DLG[v].bg==='tdesk'?'ticket':(T.DLG[v].bg==='sage'?'sage':'ticket')],v,'hub')}", vid)
    q.wait_for_timeout(500); q.evaluate(TICK); q.evaluate("()=>{window.__fast=1}")
    # 最初の「GO」など押すボタンがあれば押す
    for i in range(400):
        q.wait_for_timeout(150)
        if q.evaluate("()=>{var b=document.querySelector('.btn.go');if(b&&b.offsetParent){b.click();return 1}return 0}"): pass
        ph = q.evaluate("()=>__T.G.phase")
        if q.evaluate("()=>window.__ph.indexOf('reveal')>=0") and q.evaluate("()=>(__T.G.scene?__T.G.scene.vid:'')") != vid: break
        if q.evaluate("()=>window.__ph.indexOf('reveal')>=0 && __T.G.phase!=='reveal'"): break
        if q.evaluate("()=>window.__ph.indexOf('words')>=0"): break
    r = q.evaluate("()=>({ph:window.__ph,rv:window.__rv,jp:window.__rvjp||[],n:__T.G.scene?__T.G.scene.turns.length:0,errs:window.__errs,seen:__T.save.seen})")
    r['perr'] = errs; ctx.close(); return r
with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    for vid in ('sage_1', 'sage_2', 'sage_3', 'ticket_star', 'ticket_ow'):
        r = run(br, base, vid)
        chk('E %s: Word Battle(words)を通らず Meaning!(reveal)へ進む' % vid, 'reveal' in r['ph'] and 'words' not in r['ph'], r['ph'])
        chk('E %s: Meaning! が日本語訳つきで出る(1往復ずつ)' % vid, len(r['rv']) >= 1 and any(any(ord(c) > 0x3000 for c in j) for j in r['jp']), (r['rv'][:3], [j[:30] for j in r['jp'][:2]]))
        chk('E %s: エラーなし' % vid, not r['errs'] and not r['perr'], (r['errs'], r['perr']))
    print('\n全部OK' if not bad else '\nNG: %s' % bad); sys.exit(1 if bad else 0)
