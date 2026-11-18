# -*- coding: utf-8 -*-
"""タスク034 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_pa034.py
放送の場面(nbo_ev_e_gate / nbo_ev_f_captain / doh_ev_i_board)で、英語の読み上げが出るか・印が出て消えるか・
音オフ/声なしでも進むか・ふつうの会話は今までどおりか、を確かめる。読み上げは差し替え(記録だけ)。実機の声は確認できない(未確認)。
リポジトリのファイルは書き換えない。"""
import os, re, sys, json, threading, http.server, socketserver
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOOK = "requestAnimationFrame(frame);\n})();"

INIT = r"""
(function(){
 window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});
 window.__sp=[];var MODE=%s;
 setInterval(function(){var o=document.querySelector('.trip-ov');if(o&&!o.busy)o.click()},400);
 if(MODE==='novoice'){try{delete window.speechSynthesis}catch(e){}}
 else try{speechSynthesis.cancel=function(){};speechSynthesis.speak=function(u){var r={t:u.text,start:false,mid:false,end:null};window.__sp.push(r);
  setTimeout(function(){if(u.onstart){u.onstart({});r.start=true}setTimeout(function(){r.mid=!!document.querySelector('#msg .pa');if(u.onend)u.onend({});r.end=!document.querySelector('#msg .pa')},150)},10)}}catch(e){}
 function FS(){}
 FS.prototype.start=function(){var me=this;setTimeout(function(){var T=window.__T,G=T&&T.G,S=G&&G.scene,t=S&&S.turns&&S.turns[G.ti];
   var s=(t&&t.cue||'').replace(/\*/g,'');var rs=[{transcript:s,confidence:.95}];rs.isFinal=true;
   if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},10)},30)};
 FS.prototype.abort=FS.prototype.stop=function(){};
 window.SpeechRecognition=FS;window.webkitSpeechRecognition=FS;
 try{if(MODE==='off')localStorage.setItem('kd_snd','off');else localStorage.removeItem('kd_snd')}catch(e){}
 try{if(!localStorage.getItem('__seeded')){localStorage.setItem('__seeded','1');localStorage.setItem('kanpe-tour-save-v1',JSON.stringify({seen:{},help:5,weak:[],missed:[],ticket:'ow'}))}}catch(e){}
})();
"""


class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True


def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv


def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,PBY:PBY,startVid:startVid};" + HOOK, 1))


def run(base, br, path, vid, mode, pick):
    ctx = br.new_context(viewport={'width': 390, 'height': 780})
    ctx.add_init_script(INIT % json.dumps(mode))
    ctx.route(re.compile(r'.*/index\.html(\?.*)?$'), hooked)
    page = ctx.new_page(); errs = []
    page.on('pageerror', lambda e: errs.append(str(e)[:200]))
    page.goto(base + path + 'index.html?ev=off'); page.wait_for_timeout(800)
    page.evaluate("v=>{var T=window.__T;T.startVid(T.PBY[Object.keys(T.PBY)[0]],v,'ev')}", vid)
    shown = []; res = {'vid': vid, 'mode': mode, 'pick': pick, 'picked': False, 'cue_reached': False, 'finished': False}
    for _ in range(200):
        st = page.evaluate("""()=>{var G=window.__T.G;return {ph:G.phase,view:G.view,msg:document.getElementById('msgText').textContent,pa:!!document.querySelector('#msg .pa'),
          opts:[].slice.call(document.querySelectorAll('#panel .dq')).length}}""")
        if st['pa']: res['mark_seen'] = True
        if st['msg'] and (not shown or shown[-1] != st['msg']): shown.append(st['msg'])
        if st['ph'] == 'opts' and not res['picked']:
            res['cue_reached'] = True; res['picked'] = True
            page.evaluate("i=>document.querySelectorAll('#panel .dq')[i].click()", pick)
        if st['view'] == 'map' and res['picked']: res['finished'] = True; break
        page.wait_for_timeout(150)
    res['sp'] = page.evaluate("()=>window.__sp"); res['shown'] = shown; res['errors'] = errs + page.evaluate("()=>window.__errs")
    res['mark_after'] = page.evaluate("()=>!!document.querySelector('#msg .pa')")
    ctx.close(); return res


def main():
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]; bad = []
    def chk(c, m):
        print(('OK  ' if c else 'NG  ') + m)
        if not c: bad.append(m)
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        cases = [('/tour/', 'nbo_ev_e_gate', 0, "Attention, please. Qatar Airways"), ('/tour/', 'nbo_ev_f_captain', 0, "Ladies and gentlemen, this is your captain"),
                 ('/tour/doha/', 'doh_ev_i_board', 0, "Attention, please. Passengers to Helsinki")]
        for path, vid, pick, head in cases:
            r = run(base, br, path, vid, 'on', pick)
            sp0 = r['sp'][0] if r['sp'] else {}
            chk(sp0.get('t', '').startswith(head), '%s: 放送の文を読み上げた(%s…)' % (vid, sp0.get('t', '')[:30]))
            chk(sp0.get('mid') is True and sp0.get('end') is True, '%s: 読み上げ中に印が出て、終わると消えた' % vid)
            chk(r['finished'] and not r['mark_after'] and not r['errors'], '%s: 最後まで進んだ・印は残らない・エラーなし %s' % (vid, r['errors']))
        # あとの一言: 放送(Announcement)は印つき、Travelerは印なし
        r = run(base, br, '/tour/', 'nbo_ev_e_gate', 'on', 0)
        ts = [(x['t'], x['mid']) for x in r['sp']]
        chk(any(t.startswith('Thank you. Boarding will begin soon') and m for t, m in ts), 'あとの一言(Announcement)も放送の声と印')
        r = run(base, br, '/tour/', 'nbo_ev_e_gate', 'on', 1)
        ts = [(x['t'], x['mid']) for x in r['sp']]
        chk(any(t.startswith('Gate fourteen, not forty') for t, m in ts) and not any(t.startswith('Gate fourteen, not forty') and m for t, m in ts), 'あとの一言(Traveler)はふつうの声・印なし')
        r = run(base, br, '/tour/', 'nbo_ev_e_gate', 'on', 2)
        chk(any(x['t'].startswith('Attention, please. Your gate has changed') and x['mid'] for x in r['sp']), '「もう一度」で放送がもう一度流れる')
        # 音オフ
        r = run(base, br, '/tour/', 'nbo_ev_f_captain', 'off', 0)
        chk(not any(x['t'].startswith('Ladies and gentlemen') for x in r['sp']) and not r.get('mark_seen') and r['cue_reached'] and r['finished'], '音オフ: 放送は読まない・印なし・文は出て進む')
        chk(any('captain' in s for s in r['shown']), '音オフ: 文は画面に残る')
        # 声なし
        r = run(base, br, '/tour/', 'nbo_ev_e_gate', 'novoice', 0)
        chk(r['cue_reached'] and r['finished'] and not r.get('mark_seen') and not r['errors'], '声なし環境: 無音で進む・印なし・エラーなし %s' % r['errors'])
        # ふつうの会話(放送ではない割りこみ)は印なし・今までどおり読む
        r = run(base, br, '/tour/', 'nbo_ev_a_dropped', 'on', 0)
        chk(len(r['sp']) > 0 and not r.get('mark_seen'), 'ふつうの会話(nbo_ev_a_dropped): 今までどおり読む・放送の印なし')
        # nbo_gate2: 最初の台詞(放送)だけ放送の声と印。2つ目からは係員の会話でふつうの声
        ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT % json.dumps('on'))
        ctx.route(re.compile(r'.*/index\.html(\?.*)?$'), hooked); pg = ctx.new_page(); pe = []
        pg.on('pageerror', lambda e: pe.append(str(e)[:200]))
        pg.goto(base + '/tour/index.html?ev=off'); pg.wait_for_timeout(800)
        pg.evaluate("()=>{var T=window.__T;T.startVid(T.PBY[Object.keys(T.PBY)[0]],'nbo_gate2','x')}"); pg.wait_for_timeout(500)
        for _ in range(60):
            pg.evaluate("()=>{var b=[].slice.call(document.querySelectorAll('#panel button')).filter(function(x){return x.offsetParent&&!x.disabled});for(var i=0;i<b.length;i++)if(/^GO/.test(b[i].textContent)){b[i].click();return}}")
            sp = pg.evaluate("()=>window.__sp")
            if any(q['t'].startswith('Which group') for q in sp): break
            pg.wait_for_timeout(200)
        g0 = [q for q in sp if q['t'].startswith('Attention please. Flight boarding')]; g1 = [q for q in sp if q['t'].startswith('Which group')]
        chk(bool(g0) and g0[0]['mid'] is True, 'nbo_gate2 最初の台詞: 放送の声と印')
        chk(bool(g1) and g1[0]['mid'] is False and g1[0]['start'] is False, 'nbo_gate2 2つ目(係員の会話): ふつうの声・印なし')
        chk(not pe, 'nbo_gate2: エラーなし %s' % pe)
        ctx.close()
        br.close()
    print('NG件数:', len(bad)); sys.exit(1 if bad else 0)


main()
