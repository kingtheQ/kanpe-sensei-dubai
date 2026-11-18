# -*- coding: utf-8 -*-
"""タスク023 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_doha023.py [--shots DIR]
ドーハ(tour/doha/)を、到着 → 市内 → 出発 → 機内 まで全部の場面を通す。音声認識は差し替え(カンペの文をそのまま返す)。
?ev=all で割りこみを全部起こす。持ち越しの種(ナイロビの場面)は、記録に「遊んだ」として入れておく。
マイクの実機の動きは確認できない(未確認)。リポジトリのファイルは書き換えない。"""
import os, re, sys, json, threading, http.server, socketserver, time
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHOTS = sys.argv[sys.argv.index('--shots') + 1] if '--shots' in sys.argv else None
SEEDS = ['nbo_lounge2', 'nbo_sec2', 'nbo_java2', 'nbo_art2', 'nbo_ev_f1_ribbon']

INIT = r"""
(function(){
 setInterval(function(){var o=document.querySelector('.trip-ov');if(o&&!o.busy)o.click()},400);   /* タスク030: 夜の1枚・朝の1枚は 自動で進める */
 window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});
 try{speechSynthesis.speak=function(u){setTimeout(function(){if(u.onend)u.onend({})},5)};speechSynthesis.cancel=function(){}}catch(e){}
 function FS(){}
 FS.prototype.start=function(){var me=this;setTimeout(function(){var T=window.__T,G=T&&T.G,S=G&&G.scene,t=S&&S.turns&&S.turns[G.ti];
   var s=(t&&t.cue||'').replace(/\*/g,'');var rs=[{transcript:s,confidence:.95}];rs.isFinal=true;
   if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},10)},30)};
 FS.prototype.abort=FS.prototype.stop=function(){};
 window.SpeechRecognition=FS;window.webkitSpeechRecognition=FS;
 try{if(!localStorage.getItem('__seeded')){localStorage.setItem('__seeded','1');
  var s={seen:{},help:5,weak:[],missed:[],ticket:'ow'};%s.forEach(function(k){s.seen[k]=1});localStorage.setItem('kanpe-tour-save-v1',JSON.stringify(s));localStorage.removeItem('kanpe-world-v1');localStorage.setItem('kanpe-trip-v1',JSON.stringify({v:1,trip:1,tk:'ow',day:6,td:9,ph:'day',bun:1,legs:[],days:[],cur:{led:[],pick:[]}}))}}catch(e){}
})();
""" % json.dumps(SEEDS)
HOOK = "requestAnimationFrame(frame);\n})();"


class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True


def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv


def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    hk = "window.__T={G:G,save:save,onNode:onNode,setMode:setMode,PBY:PBY,MODES:MODES};"
    route.fulfill(response=r, body=body.replace(HOOK, hk + HOOK, 1))


def main():
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    out = {'errors': [], 'scenes': {}, 'npc_lines': {}, 'order': []}
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        ctx = br.new_context(viewport={'width': 390, 'height': 780})
        ctx.add_init_script(INIT)
        ctx.route(re.compile(r'.*/tour/doha/(index\.html)?(\?.*)?$'), hooked)
        page = ctx.new_page()
        page.on('pageerror', lambda e: out['errors'].append(str(e)[:200]))
        page.goto(base + '/tour/doha/index.html?ev=all'); page.wait_for_timeout(800)
        modes = page.evaluate("()=>Object.keys(window.__T.MODES)"); out['tabs'] = modes
        if SHOTS: os.makedirs(SHOTS, exist_ok=True)

        def wait_map(limit=90):
            t0 = time.time(); lines = []
            while time.time() - t0 < limit:
                st = page.evaluate("""()=>{var G=window.__T.G;var S=G.scene;var r={view:G.view,phase:G.phase,vid:S&&S.vid,msg:(document.getElementById('msgText')||{}).textContent};
                  var b=[].slice.call(document.querySelectorAll('#panel button')).filter(function(x){return !x.disabled&&x.offsetParent});r.btns=b.map(function(x){return x.textContent.trim()});return r}""")
                if st['view'] == 'map': return lines
                if st['vid'] and st['msg'] and (not lines or lines[-1] != (st['vid'], st['msg'])): lines.append((st['vid'], st['msg']))
                if st['phase'] == 'hub' and not st['vid']: return lines
                page.evaluate("""()=>{var b=[].slice.call(document.querySelectorAll('#panel button')).filter(function(x){return !x.disabled&&x.offsetParent});
                  var pref=['GO','つぎ','すすむ','OK','▶'];for(var i=0;i<b.length;i++){var s=b[i].textContent;for(var j=0;j<pref.length;j++)if(s.indexOf(pref[j])===0){b[i].click();return}}
                  var ph=window.__T.G.phase;if(b.length&&(ph==='words'||ph==='reveal'||ph==='clear'||ph==='opts'))b[0].click()}""")
                page.wait_for_timeout(120)
            raise SystemExit('timeout: ' + json.dumps(st, ensure_ascii=False))

        for m in ['arr', 'city', 'dep']:
            page.evaluate("m=>window.__T.setMode(m)", m); page.wait_for_timeout(300)
            if SHOTS: page.screenshot(path=os.path.join(SHOTS, 'map_%s.png' % m))
            places = page.evaluate("()=>window.__T.MODES[%s].p.map(function(p){return {id:p.id,v:p.v,hub:!!p.hub,menu:p.menu||null}})" % json.dumps(m))
            for p in places:
                for k, vid in enumerate(p['v']):
                    if p['hub']:
                        page.evaluate("id=>window.__T.onNode(id)", p['id']); page.wait_for_timeout(300)
                        out['order'] += [x[0] for x in wait_map() if x[0]]
                        label = [mm[0] for mm in p['menu'] if mm[1] == vid][0]
                        page.evaluate("""l=>{var b=[].slice.call(document.querySelectorAll('#panel button'));for(var i=0;i<b.length;i++)if(b[i].textContent.indexOf(l)>=0){b[i].click();return}}""", label)
                    else:
                        page.evaluate("id=>window.__T.onNode(id)", p['id'])
                    page.wait_for_timeout(300)
                    if SHOTS and k == 0:
                        page.wait_for_timeout(700); page.screenshot(path=os.path.join(SHOTS, 'scene_%s.png' % vid))
                    if vid == 'doh_dep_plane':
                        try:
                            with page.expect_navigation(timeout=120000): lines = wait_map(120)
                        except SystemExit:
                            raise
                        except Exception:
                            pass
                        out['after_plane_url'] = page.url
                        out['world'] = page.evaluate("()=>JSON.parse(localStorage.getItem('kanpe-world-v1')||'null')")
                        out['save'] = page.evaluate("()=>JSON.parse(localStorage.getItem('kanpe-tour-save-v1')||'null')")
                        break
                    lines = wait_map()
                    for (v, msg) in lines: out['npc_lines'].setdefault(v, []).append(msg)
                    out['order'] += sorted(set(x[0] for x in lines if x[0]), key=[x[0] for x in lines].index)
                    if m == 'arr' and p['id'] == 'dride':
                        out['mode_after_ride'] = page.evaluate("()=>window.__T.MODES&&document.querySelector('.mbtn.on').dataset.m")
                        page.evaluate("()=>window.__T.setMode('arr')")
        out['errors'] += page.evaluate("()=>window.__errs||[]") if 'world' not in page.url else []
        br.close()
    s = out.get('save') or {}
    out['seen_new'] = sorted(k for k in (s.get('seen') or {}) if k.startswith('doh_'))
    out['ev_fired'] = sorted(((s.get('ev') or {}).get('fired') or {}).keys())
    print(json.dumps({k: out[k] for k in ('tabs', 'errors', 'mode_after_ride', 'after_plane_url', 'world', 'ev_fired')}, ensure_ascii=False, indent=1))
    print('seen doh_* :', len(out['seen_new']))
    print('order:', ' '.join(dict.fromkeys(out['order'])))
    json.dump(out, open('/tmp/doha023_result.json', 'w'), ensure_ascii=False, indent=1)


main()
