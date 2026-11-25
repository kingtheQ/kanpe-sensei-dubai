# -*- coding: utf-8 -*-
"""タスク086 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_noresult086.py
合宿デモ(camp_demo1)と通常の会話で、「聞き取れなかった(認識結果なし)」と「言ったけれど違った(認識結果あり・不一致)」を分けて扱うこと。
(1) 合宿・聞き取れなかった: ブザー・シェイクなし・自分の声の再生なし・失敗に数えない(it.fails=0・G.tries=0)・お手本を1回流して言い直し(上限なし)。その回の録音は捨て、同じ項目では録り直さない
(2) 合宿・不一致: 従来の失敗の流れ(ブザー→自分の声→お手本→言い直し)。自分の声の再生が判定から遅れない
(3) 聞き取れなかったことが合計2回あったら、合宿の残りは録音しない(判定を優先)。そのあとの不一致では自分の声は流れないが、流れは進む
(4) 通常の会話(合宿以外): 聞き取れなかった→失敗に数えず(G.tries 不変)・ブザーなし・お手本1回→また聞く。何回聞き取れなくても自動救済に入らない。不一致は従来どおり G.tries が増える
実機のマイク(Android の同時利用)は確認できない(このテストの音声認識とマイクは偽物)。"""
import os, sys, re, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import serve, INIT as FAKE_INIT, ROOT
from playwright.sync_api import sync_playwright
HOOK = "requestAnimationFrame(frame);\n})();"
EXPOSE = ("window.__T={G:G,save:save,PBY:PBY,DLG:DLG,PREF:PREF,Snd:Snd,"
          "get GS(){return typeof GS!=='undefined'?GS:null},startVid:startVid};")
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, EXPOSE + HOOK, 1))
SETUP = """
window.__perr=[];window.addEventListener('error',function(e){window.__perr.push(String(e.message))});
localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));
window.__ev=[];window.__srq=[];window.__srn=0;window.__t0={};
(function(){var o=speechSynthesis.speak;speechSynthesis.speak=function(u){window.__ev.push({k:'say',t:u.text,r:u.rate,ts:performance.now()});return o.apply(this,arguments)}})();
(function(){var P=window.SpeechRecognition;if(!P)return;
 function FS(){}FS.prototype.start=function(){var me=this;window.__srn++;var mode=window.__srq.length?window.__srq.shift():'ok';setTimeout(function(){
  var t=[].map.call(document.querySelectorAll('#panel .cue .w'),function(x){return x.textContent}).join(' ');
  window.__ev.push({k:'sr',m:mode,ts:performance.now()});
  if(mode==='none'){setTimeout(function(){if(me.onend)me.onend({})},30);return}
  if(mode==='err'){if(me.onerror)me.onerror({error:'no-speech'});setTimeout(function(){if(me.onend)me.onend({})},30);return}
  if(mode==='empty'){var r0=[{transcript:'  ',confidence:0}];r0.isFinal=true;if(me.onresult)me.onresult({results:[r0]});setTimeout(function(){if(me.onend)me.onend({})},20);return}
  if(mode==='bad')t='banana';
  var rs=[{transcript:t,confidence:.9}];rs.isFinal=true;
  if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},20)},60)};
 FS.prototype.abort=FS.prototype.stop=function(){};window.SpeechRecognition=FS;window.webkitSpeechRecognition=FS})();
window.__rec={gum:0,start:0,stop:0,own:0};window.__jin=[];window.__shake=0;
(function(){try{navigator.mediaDevices.getUserMedia=function(){window.__rec.gum++;return Promise.resolve({getTracks:function(){return [{stop:function(){}}]}})}}catch(e){}
 function MR(st,o){this.state='inactive';this.mimeType=(o&&o.mimeType)||'audio/webm'}MR.isTypeSupported=function(){return true};
 MR.prototype.start=function(ts){this.state='recording';window.__rec.start++;this.ts=ts;var me=this;if(ts)setTimeout(function(){if(me.state==='recording'&&me.ondataavailable)me.ondataavailable({data:new Blob(['xxxx'],{type:'audio/webm'})})},ts)};
 MR.prototype.stop=function(){var me=this;if(this.state==='inactive')return;this.state='inactive';window.__rec.stop++;setTimeout(function(){if(me.ondataavailable)me.ondataavailable({data:new Blob(['yyyy'],{type:'audio/webm'})});if(me.onstop)me.onstop()},300)};
 window.MediaRecorder=MR;
 HTMLMediaElement.prototype.play=function(){var me=this;if(/^blob:/.test(me.src||'')){window.__rec.own++;window.__ev.push({k:'own',ts:performance.now()});setTimeout(function(){if(me.onended)me.onended()},60)}return Promise.resolve()};
 setInterval(function(){try{var J=__T.Snd.jingle;if(!J.__w){var f=function(k){window.__jin.push(k);return J.apply(this,arguments)};f.__w=1;__T.Snd.jingle=f}}catch(e){}},20)})();
"""
srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
def mk(br):
    ctx = br.new_context(viewport={'width': 430, 'height': 900}); ctx.add_init_script(FAKE_INIT); ctx.add_init_script(SETUP)
    p = ctx.new_page(); p.route('**/tour/index.html*', hooked); return p
def open_camp(p):
    p.goto(base + '/tour/index.html?check=1'); p.wait_for_timeout(1500); p.mouse.click(215, 450); p.wait_for_timeout(600)
    p.evaluate("()=>document.getElementById('chkBtn').click()"); p.wait_for_timeout(200)
    p.evaluate("(v)=>{[].filter.call(document.querySelectorAll('#chkPan button'),function(b){return b.textContent===v})[0].click()}", 'camp_demo1'); p.wait_for_timeout(900)
def first_turn(p, q):
    """GO のあと、最初のプレイヤーの番(1語目)に入る直前に、偽の認識の結果の順番 q を入れる"""
    p.evaluate("(q)=>{window.__srq=q}", q); p.click('.btn.go')
def snap(p): return p.evaluate("()=>({ev:window.__ev,rec:window.__rec,jin:window.__jin,tries:__T.G.tries,fails:(__T.GS&&__T.GS.cur)?__T.GS.cur.fails:null,txt:(__T.GS&&__T.GS.cur)?__T.GS.cur.text:null,i:(__T.GS&&__T.GS.cur)?__T.GS.cur.i:null,noRec:__T.GS&&__T.GS.noRec,recOff:__T.GS&&__T.GS.recOff,srn:window.__srn,phase:__T.G.phase,errs:window.__perr})")
def wait_sr(p, n, sec=40):
    for _ in range(sec * 10):
        p.wait_for_timeout(100)
        if p.evaluate("window.__srn") >= n: return True
    return False
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    # ---- (1) 合宿: 聞き取れなかった(1回)→お手本1回→言い直しで合格 ----
    p = mk(br); open_camp(p); first_turn(p, ['none'])
    wait_sr(p, 2); p.wait_for_timeout(1500)
    s = snap(p); ev = s['ev']
    i_sr = [i for i, e in enumerate(ev) if e['k'] == 'sr'][0]
    after = [e for e in ev[i_sr + 1:i_sr + 4]]
    w0 = s['txt']
    chk('1a 聞き取れなかった: ブザーなし・自分の声の再生なし・失敗に数えない(fails=0・G.tries=0)', 'buzz' not in s['jin'] and s['rec']['own'] == 0 and s['fails'] in (0, None) and s['tries'] == 0, [s['jin'], s['rec'], s['fails'], s['tries']])
    chk('1b 聞き取れなかったあと、お手本が1回(ふつうの速さ rate 1)流れて、また聞く(認識が2回目に入る)', after and after[0]['k'] == 'say' and abs(after[0]['r'] - 1) < .01 and s['srn'] >= 2 and (len(after) < 2 or after[1]['k'] != 'say' or after[1]['t'] != after[0]['t']), after)
    chk('1d エラーなし', s['errs'] == [], s['errs'])
    p.close()
    # ---- (1b) 聞き取れなかったが何回続いても、数えず・止まらず続く(上限なし) ----
    p = mk(br); open_camp(p); first_turn(p, ['none', 'err', 'empty', 'none'] + ['none'] * 20)
    wait_sr(p, 6); p.wait_for_timeout(800)
    s = snap(p)
    chk('1e 聞き取れなかった(無音・no-speech・空の結果)を4回続けても、失敗に数えない・ブザー・自分の声なし・救済に入らない(ルルの代行 pitch 1.75 なし)', 'buzz' not in s['jin'] and s['rec']['own'] == 0 and s['fails'] in (0, None) and s['tries'] == 0 and s['srn'] >= 5, [s['jin'], s['srn'], s['fails']])
    chk('1c その回の録音は捨て、同じ項目では録り直さない(noRec=1・何度聞き取れなくても getUserMedia は最初の1回だけ)', s['noRec'] == 1 and s['rec']['gum'] == 1, [s['noRec'], s['rec']])
    p.close()
    # ---- (2) 合宿: 不一致は従来の失敗の流れ・自分の声が遅れない ----
    p = mk(br); open_camp(p); first_turn(p, ['bad'])
    wait_sr(p, 2); p.wait_for_timeout(2000)
    s = snap(p); ev = s['ev']
    i_sr = [i for i, e in enumerate(ev) if e['k'] == 'sr'][0]
    own = [e for e in ev if e['k'] == 'own']
    dt = (own[0]['ts'] - ev[i_sr]['ts']) if own else 9999
    chk('2a 言ったけれど違った(認識結果あり): ブザーが鳴る・自分の声が1回・そのあとお手本→言い直し(従来の流れ)', 'buzz' in s['jin'] and s['rec']['own'] == 1 and s['srn'] >= 2, [s['jin'], s['rec'], s['srn']])
    chk('2b 自分の声の再生は判定から遅れない(判定→再生まで %d ms・目安 900ms 以内。以前は止まりの待ちで最大2秒)' % dt, dt < 900, dt)
    p.close()
    # ---- (3) 聞き取れなかったことが2回 → 録音をやめる。そのあとの不一致でも流れは進む ----
    p = mk(br); open_camp(p); first_turn(p, ['none', 'ok', 'none', 'ok', 'bad'])
    wait_sr(p, 6, 60); p.wait_for_timeout(2500)
    s = snap(p)
    chk('3a 聞き取れなかったことが2回あったら、合宿の残りは録音しない(recOff=1)・自分の声は流れない・不一致のあとも止まらず進む(エラーなし)', s['recOff'] == 1 and s['rec']['own'] == 0 and s['srn'] >= 6 and s['errs'] == [], [s['recOff'], s['rec'], s['srn'], s['errs']])
    p.close()
    # ---- (4) 通常の会話 ----
    p = mk(br); p.goto(base + '/tour/index.html'); p.wait_for_timeout(1500); p.mouse.click(215, 450); p.wait_for_timeout(600)
    p.evaluate("()=>{var T=__T;T.save.missed=[];window.__srq=['none','none','none'];T.startVid(T.PBY.java,'nbo_java1',null)}"); p.wait_for_timeout(1200)
    p.click('.btn.go') if p.evaluate("!!document.querySelector('.btn.go')") else None
    wait_sr(p, 5, 60); p.wait_for_timeout(1200)
    s = snap(p)
    chk('4a 通常の会話: 聞き取れなかった3回でも、失敗に数えない(G.tries=0)・ブザーなし・自動救済に入らない(phase が help でない)・また聞いている', s['tries'] == 0 and 'buzz' not in s['jin'] and s['phase'] != 'help' and s['srn'] >= 4, [s['tries'], s['jin'], s['phase'], s['srn']])
    chk('4b 通常の会話: 聞き取れなかったあとはお手本が流れる(say が出る)・エラーなし', any(e['k'] == 'say' and e['ts'] > [x for x in s['ev'] if x['k'] == 'sr'][0]['ts'] for e in s['ev']) and s['errs'] == [], s['errs'])
    p.close()
    p = mk(br); p.goto(base + '/tour/index.html'); p.wait_for_timeout(1500); p.mouse.click(215, 450); p.wait_for_timeout(600)
    p.evaluate("()=>{var T=__T;T.save.missed=[];window.__srq=['bad','none','none','none','none'];T.startVid(T.PBY.java,'nbo_java1',null)}"); p.wait_for_timeout(1200)
    p.click('.btn.go') if p.evaluate("!!document.querySelector('.btn.go')") else None
    wait_sr(p, 4, 60); p.wait_for_timeout(600)
    s = snap(p)
    chk('4c 通常の会話: 言ったけれど違った(不一致)は従来どおり(ブザー・G.tries が増える)', 'buzz' in s['jin'] and s['tries'] == 1, [s['jin'], s['tries']])
    br.close()
print('NG=%d' % len(bad)); sys.exit(1 if bad else 0)
