# -*- coding: utf-8 -*-
"""タスク016 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_routes.py
中継URLあり/なしの2種類のページを一時フォルダに作り、(0)中継なし (1)同意する+Azure(偽のSDK) (2)同意しない
(3)同意する+通信なし (4)マイクなし の5経路を、始めの宣言 → 終わりの場面まで通す。マイクと本物の Azure は実機でしか確認できない。
リポジトリの tour/ は書き換えない(出力は /tmp)。"""
import os, sys, json, shutil, subprocess, threading, http.server, socketserver, time, re
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = '/tmp/kanpe016'
RELAY = 'https://relay.example.test'
SHOTS = os.path.join(OUT, 'shots')

def build(variant, relay):
    d = os.path.join(OUT, variant)
    shutil.rmtree(d, ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env['KANPE_RELAY_URL'] = relay if relay is not None else ''   # None=中継なし。relay-url.txt に公開用のURLが入った後も、「中継なし」の経路を作れるように空を渡す
    keep = {}
    for f in ('tour/index.html', 'tour/doha/index.html', 'tour/ending/index.html'):
        keep[f] = open(os.path.join(ROOT, f), 'rb').read()
    try:
        subprocess.check_call([sys.executable, os.path.join(ROOT, 'tour-src', 'build.py')], env=env, stdout=subprocess.DEVNULL)
        for f in ('tour/index.html', 'tour/ending/index.html'):
            os.makedirs(os.path.dirname(os.path.join(d, f)), exist_ok=True)
            shutil.copy(os.path.join(ROOT, f), os.path.join(d, f))
    finally:
        for f, b in keep.items(): open(os.path.join(ROOT, f), 'wb').write(b)   # リポジトリの生成物は元に戻す
    return d

DECL = re.search(r'DECL = \((.*?)\)\n', open(os.path.join(ROOT, 'tour-src', 'window_data.py'), encoding='utf-8').read(), re.S)
DECL = ''.join(re.findall(r'"((?:[^"\\]|\\.)*)"', DECL.group(1)))

INIT = r"""
(function(){
 var cfg=%s;
 window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});
 window.addEventListener('unhandledrejection',function(e){window.__errs.push('rej:'+String(e.reason))});
 try{speechSynthesis.speak=function(u){setTimeout(function(){if(u.onend)u.onend({})},8)};speechSynthesis.cancel=function(){}}catch(e){}
 if(cfg.sr){
  var say=function(){return window.__SAY||cfg.decl};
  function FS(){}
  FS.prototype.start=function(){var me=this;setTimeout(function(){var rs=[{transcript:say(),confidence:.9}];rs.isFinal=true;
    if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},20)},60)};
  FS.prototype.abort=FS.prototype.stop=function(){};
  window.SpeechRecognition=FS;window.webkitSpeechRecognition=FS;
 }else{try{delete window.SpeechRecognition;delete window.webkitSpeechRecognition}catch(e){}}
 if(cfg.az){
  var WORDS=cfg.decl.split(' ');
  function mk(phase){var bad=/th|r|l|v/i;
   var ws=WORDS.map(function(w){var core=w.replace(/[^A-Za-z']/g,'');var a=bad.test(core)?(phase==='start'?52:86):94;
    return {Word:core,Duration:3000000,PronunciationAssessment:{AccuracyScore:a,ErrorType:'None'},Phonemes:core.split('').map(function(ch){return {Phoneme:ch==='r'?'ɹ':(/th/i.test(core)&&ch.toLowerCase()==='t'?'θ':ch.toLowerCase()),PronunciationAssessment:{AccuracyScore:a}}})}});
   return {NBest:[{PronunciationAssessment:{AccuracyScore:80,FluencyScore:phase==='start'?66:84,CompletenessScore:100,PronScore:80},Words:ws}]}}
  window.SpeechSDK={
   SpeechConfig:{fromAuthorizationToken:function(){return {}}},
   PronunciationAssessmentGradingSystem:{HundredMark:1},PronunciationAssessmentGranularity:{Phoneme:1},
   PronunciationAssessmentConfig:function(){this.applyTo=function(){}},
   AudioConfig:{fromDefaultMicrophoneInput:function(){return {}}},
   ResultReason:{RecognizedSpeech:3},PropertyId:{SpeechServiceResponse_JsonResult:9},CancellationReason:{Error:1},
   SpeechRecognizer:function(){var me=this;
    me.close=function(){};me.stopContinuousRecognitionAsync=function(ok){setTimeout(ok,5)};
    me.startContinuousRecognitionAsync=function(ok){setTimeout(ok,5);setTimeout(function(){
      var j=JSON.stringify(mk((location.pathname.indexOf('ending')>=0?'end':'start')));
      me.recognized(me,{result:{reason:3,text:cfg.decl,properties:{getProperty:function(){return j}}}})},600)}}};
 }
})();
"""

class Q(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True
def serve(d):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=d, **k)
        def log_message(s, *a): pass
    srv = Q(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv

HOOK_N = "requestAnimationFrame(frame);\n})();"
def hooked(route, kind):
    r = route.fetch(); body = r.text()
    hk = "window.__T={G:G,save:save,winStart:%s};" % ('winStart' if kind == 'tour' else 'null')
    assert HOOK_N in body
    route.fulfill(response=r, body=body.replace(HOOK_N, hk + HOOK_N, 1))

def drive(page, secs, until, log):
    """見えているボタンを、人のように押していく。until(page)が真になったら終わる"""
    t0 = time.time(); last = ''
    while time.time() - t0 < secs:
        if until(page): return True
        info = page.evaluate("""()=>{var o={};var b=[].slice.call(document.querySelectorAll('#panel button, #panel .opt'));
          o.btns=b.filter(function(x){return !x.disabled&&x.offsetParent}).map(function(x){return x.textContent.trim()});
          o.msg=(document.getElementById('msgText')||{}).textContent||'';o.phase=window.__T&&window.__T.G?window.__T.G.phase:'';return o}""")
        sig = json.dumps(info, ensure_ascii=False)
        if sig != last: log.append(sig[:200]); last = sig
        for want in log_buttons:
            if want(info['btns']): break
        time.sleep(.25)
    return False
log_buttons = []

def click_text(page, texts):
    return page.evaluate("""(tx)=>{var b=[].slice.call(document.querySelectorAll('#panel button, #panel .opt'));
      for(var i=0;i<b.length;i++){var x=b[i];if(x.disabled||!x.offsetParent)continue;var s=x.textContent.trim();
       for(var j=0;j<tx.length;j++){if(s===tx[j]||s.indexOf(tx[j])===0){x.click();return s}}}return null}""", texts)

def vstore(page):
    return page.evaluate("()=>{try{return JSON.parse(localStorage.getItem('kanpe-voice-v1')||'null')}catch(e){return 'bad'}}")

def run_route(pw, name, d, relay_on, consent_btn, sr, az, token_ok, phase_says=None):
    res = {'route': name, 'errors': [], 'shots': []}
    srv = serve(d); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 780})
    cfg = {'sr': sr, 'az': az, 'decl': DECL}
    ctx.add_init_script(INIT % json.dumps(cfg))
    if relay_on:
        if token_ok:
            ctx.route(RELAY + '/token', lambda r: r.fulfill(status=200, content_type='application/json', headers={'access-control-allow-origin': '*'}, body=json.dumps({'token': 'x', 'region': 'japaneast', 'expiresInSec': 600})))
        else:
            ctx.route(RELAY + '/**', lambda r: r.abort())
    ctx.route('**/tour/index.html', lambda r: hooked(r, 'tour'))
    ctx.route('**/tour/ending/index.html', lambda r: hooked(r, 'end'))
    page = ctx.new_page(); logs = []
    page.on('pageerror', lambda e: res['errors'].append('pageerror:' + str(e)[:160]))
    # ---- 始めの宣言(窓口の最初の場面) ----
    page.goto(base + '/tour/index.html'); page.wait_for_timeout(700)
    page.evaluate("window.__PHASE='start';window.__T.winStart()")
    seen_consent = False; clicked = []
    def tick(p):
        nonlocal seen_consent
        v = vstore(p)
        if v and v != 'bad' and v.get('trips') and v['trips'][0].get('start'): return True
        txt = p.evaluate("()=>document.getElementById('panel').innerText")
        if '声を送ってもいい' in txt: seen_consent = True
        for t in ([consent_btn] if '声を送ってもいい' in txt and consent_btn else []) + ['GO！', 'GO!']:
            r = click_text(p, [t])
            if r: clicked.append(r); break
        return False
    ok = drive(page, 70, tick, logs)
    res['consent_card_shown'] = seen_consent; res['clicked'] = clicked[:6]
    v = vstore(page); res['after_start'] = v
    res['start_recorded'] = bool(v and v != 'bad' and v.get('trips') and v['trips'][0].get('start'))
    page.screenshot(path=os.path.join(SHOTS, name + '_1start.png')); res['shots'].append(name + '_1start.png')
    res['errors'] += page.evaluate("window.__errs")
    # ---- 終わりの場面 ----
    page.evaluate("window.__PHASE='end';window.__SAY=%s" % json.dumps(DECL if phase_says is None else phase_says))
    page.goto(base + '/tour/ending/index.html'); page.wait_for_timeout(600)
    stages = []
    def tick2(p):
        txt = p.evaluate("()=>document.getElementById('panel').innerText")
        st = p.evaluate("()=>window.__T&&window.__T.G&&window.__T.G.scene&&window.__T.G.scene.end?window.__T.G.scene.end.view:''")
        key = st + '|' + ('E4' if 'Departure' in txt and 'Home' in txt and 'Voice' in txt or ('Home' in txt and 'Departure' not in txt and '✦' in txt) else '')
        if '声を送ってもいい' in txt:
            click_text(p, [consent_btn]); return False
        if st+'|'+txt[:20] != getattr(tick2, 'last', None):
            tick2.last = st+'|'+txt[:20]; tick2.n = getattr(tick2, 'n', 0) + 1
            p.wait_for_timeout(500); p.screenshot(path=os.path.join(SHOTS, '%s_e%d.png' % (name, tick2.n)))
        if 'Voice' in txt and 'Words' in txt and not res.get('e4_text'): res['e4_text'] = txt[:400]   # E4 の数字(タスク024)
        if 'Close the album' in txt: return True
        for t in ['We went!', '›']:
            if click_text(p, [t]): break
        return False
    ok2 = drive(page, 90, tick2, logs)
    res['reached_E6'] = ok2
    res['errors'] += page.evaluate("window.__errs")
    res['final_panel'] = page.evaluate("()=>document.getElementById('panel').innerText")[:300]
    v = vstore(page); res['final_store'] = {'consent': v.get('consent') if v and v != 'bad' else None, 'trips': [{'id': t['id'], 'start_src': (t.get('start') or {}).get('src'), 'end_src': (t.get('end') or {}).get('src'), 'start_tot': (t.get('start') or {}).get('tot'), 'end_tot': (t.get('end') or {}).get('tot'), 'start_nv': (t.get('start') or {}).get('nv'), 'end_nv': (t.get('end') or {}).get('nv'), 'end_nseg': (t.get('end') or {}).get('nseg')} for t in (v or {}).get('trips', [])] if v and v != 'bad' else None, 'next': v.get('next') if v and v != 'bad' else None, 'bytes': len(json.dumps(v)) if v else 0}
    page.screenshot(path=os.path.join(SHOTS, name + '_6end.png')); res['shots'].append(name + '_6end.png')
    br.close(); srv.shutdown(); return res

def e45_shots(pw, d, name='yes'):
    """E4・E5 の見た目を撮る(同意あり+Azure の経路を、E4・E5 で止めて撮影)"""
    pass

if __name__ == '__main__':
    os.makedirs(SHOTS, exist_ok=True)
    d_off = build('off', None)
    d_on = build('on', RELAY)
    sizes = {'tour/index.html(off)': os.path.getsize(os.path.join(d_off, 'tour/index.html')), 'tour/ending/index.html(off)': os.path.getsize(os.path.join(d_off, 'tour/ending/index.html'))}
    with sync_playwright() as pw:
        R = []
        R.append(run_route(pw, 'r0_norelay', d_off, False, None, True, False, False))
        R.append(run_route(pw, 'r1_yes_az', d_on, True, '送ってOK', True, True, True))
        R.append(run_route(pw, 'r2_no', d_on, True, '送らない', True, False, True))
        R.append(run_route(pw, 'r3_yes_offline', d_on, True, '送ってOK', True, False, False))
        R.append(run_route(pw, 'r4_nomic', d_off, False, None, False, False, False))
    print(json.dumps({'sizes': sizes, 'routes': R}, ensure_ascii=False, indent=1))
