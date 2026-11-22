# -*- coding: utf-8 -*-
"""タスク062 の動作確認(ヘッドレス Chromium)。使い方: python3 tour-src/tests/test_check062.py
チェックモード(?check=1)のパネル「割りこみ・顔なじみ」に足した、CAアナウンス(048)の入口を確かめる。
  1. 通常(?check=1 なし): CHECK ボタンも入口もない。羽田の機内のあとの出方(CA場面)は従来どおり
  2. ?check=1: 入口のボタン(通し・機内食だけ)が出る。券を oneworld / Star に切りかえると、行き先が Doha / Istanbul に変わる
  3. 通し: CA場面 → 引き受ける → マイク画面 → はなす → これでOK → 機内食の場面で、自分の声(blob:)が再生される(チャイム・放送文つき)
  4. 機内食の場面だけ: 録ったあとの声が残っていれば再生される
  5. 専用の記録の中だけで動く: 通常のセーブ(localStorage)・通常の録音DB(kanpe-pa-rec-v1)は、作られず・変わらない
  6. 点検で何度試しても fired.pa1 を見ず、同じ入口から何度でも通しで試せる
マイクは Chromium の偽のマイク。実機(iPhone / Android)は確認できない(未確認)。リポジトリのファイルは書き換えない。"""
import os, re, sys, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import serve, ROOT
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pa_data

HOOK = "requestAnimationFrame(frame);\n})();"
EXPOSE = "window.__T={G:G,PBY:PBY,save:save,DLG:DLG,finishScene:finishScene,startVid:startVid};"
BANNED = ['録音', 'テスト', '測定', '練習', '復習']
INIT = r"""
(function(){
 window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});
 window.__au=[];window.__osc=0;window.__net=[];
 setInterval(function(){var o=document.querySelector('.trip-ov');if(o)o.click()},400);
 try{var of=window.fetch;window.fetch=function(){window.__net.push('fetch '+String(arguments[0]&&arguments[0].url||arguments[0]));return of.apply(this,arguments)}}catch(e){}
 try{speechSynthesis.cancel=function(){};speechSynthesis.speak=function(u){setTimeout(function(){if(u.onstart)u.onstart({});setTimeout(function(){if(u.onend)u.onend({})},60)},10)}}catch(e){}
 function FS(){}FS.prototype.start=function(){var me=this;setTimeout(function(){var T=window.__T,G=T&&T.G,S=G&&G.scene,t=S&&S.turns&&S.turns[G.ti];var s=(t&&t.cue||'').replace(/\*/g,'');var rs=[{transcript:s,confidence:.95}];rs.isFinal=true;if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},10)},40)};
 FS.prototype.abort=FS.prototype.stop=function(){};window.SpeechRecognition=FS;window.webkitSpeechRecognition=FS;
 try{var pl=HTMLMediaElement.prototype.play;HTMLMediaElement.prototype.play=function(){window.__au.push(String(this.src).slice(0,5));return pl.apply(this,arguments)}}catch(e){}
 try{var AC0=window.AudioContext||window.webkitAudioContext;if(AC0){var co=AC0.prototype.createOscillator;AC0.prototype.createOscillator=function(){window.__osc++;return co.apply(this,arguments)}}}catch(e){}
 try{if(!localStorage.getItem('__seeded')){localStorage.setItem('__seeded','1');
  localStorage.setItem('kanpe-tour-save-v1',JSON.stringify({seen:{nbo_immig1:1},ticket:'star',gold:1}));
  localStorage.setItem('kanpe-trip-v1','SENTINEL_TRIP');localStorage.setItem('kanpe-voice-v1','SENTINEL_VOICE')}}catch(e){}
})();
"""
bad = []
def chk(c, m, v=''):
    print(('OK  ' if c else 'NG  ') + m + ((' ' + str(v)) if v != '' else ''))
    if not c: bad.append(m)

def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, EXPOSE + HOOK, 1))

def ev(p, js, *a):
    return p.evaluate(js, *a) if a else p.evaluate(js)

def wait(p, js, sec=20, step=150):
    t0 = time.time()
    while time.time() - t0 < sec:
        try:
            if ev(p, js): return True
        except Exception:
            pass
        p.wait_for_timeout(step)
    return False

def panel_click(p, text):
    ev(p, "()=>document.getElementById('chkBtn').click()"); p.wait_for_timeout(80)
    return ev(p, "(t)=>{var b=[].slice.call(document.querySelectorAll('#chkPan button')).filter(function(x){return x.textContent===t})[0];if(!b)return false;b.click();return true}", text)

def panel_buttons(p):
    ev(p, "()=>document.getElementById('chkBtn').click()"); p.wait_for_timeout(80)
    r = ev(p, "()=>[].map.call(document.querySelectorAll('#chkPan button'),function(b){return b.textContent})")
    ev(p, "()=>{var x=document.querySelector('#chkPan .x');if(x)x.click()}")
    return r

def panel_text(p):
    ev(p, "()=>document.getElementById('chkBtn').click()"); p.wait_for_timeout(80)
    r = ev(p, "()=>document.getElementById('chkPan').innerText")
    ev(p, "()=>{var x=document.querySelector('#chkPan .x');if(x)x.click()}")
    return r

def pbtn(p, pat):
    return ev(p, "(pat)=>{var b=[].slice.call(document.querySelectorAll('#panel button')).filter(function(x){return x.offsetParent&&!x.disabled&&new RegExp(pat).test(x.textContent)})[0];if(b){b.click();return true}return false}", pat)

def real_state(pg2):
    return pg2.evaluate("()=>{var o={};for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k.indexOf('chk1:')!==0)o[k]=localStorage.getItem(k)}return o}")

def idb_names(pg2):
    return pg2.evaluate("()=>indexedDB.databases().then(function(a){return a.map(function(d){return d.name}).sort()})")

def main():
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required', '--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream'])
        ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
        ctx.route(re.compile(r'.*/tour/index\.html(\?.*)?$'), hooked)
        pg2 = ctx.new_page(); pg2.goto(base + '/README.md'); pg2.wait_for_timeout(300)
        p = ctx.new_page(); errs = []
        p.on('pageerror', lambda e: errs.append(str(e)[:200]))
        # ---------- 1. 通常 ----------
        p.goto(base + '/tour/index.html'); p.wait_for_timeout(1200)
        real0 = real_state(pg2)
        chk(ev(p, "()=>!document.getElementById('chkBtn')&&!window.__CHK"), '通常: CHECKボタンも入口もない')
        dbs0 = idb_names(pg2)
        # 通常の出方: 羽田の機内(oneworld)のあとにCA場面が割りこむ(従来どおり)
        ev(p, "()=>{__T.save.ticket='ow';var T=__T;T.startVid(T.PBY.hplane,'hnd_plane_ow',null);T.finishScene()}")
        chk(wait(p, "()=>__T.G.scene&&__T.G.scene.vid==='hnd_ev_ca_ow'", 10), '通常: 機内会話の直後にCA場面が割りこむ(従来どおり)')
        chk(ev(p, "()=>__T.save.ev.fired.pa1===1"), '通常: 最初の便で1回きり(fired.pa1)を記録')
        ev(p, "()=>{localStorage.clear()}")   # 通常の見本は消して、点検側の確認から始める(以降は別の新しい環境)
        ctx.close()
        # ---------- 2〜6. 点検 ----------
        for tk, label, dest in (('ow', 'oneworld', 'Doha'), ('star', 'Star Alliance', 'Istanbul')):
            tag = '[%s] ' % tk
            c2 = br.new_context(viewport={'width': 390, 'height': 780}); c2.add_init_script(INIT)
            c2.route(re.compile(r'.*/tour/index\.html(\?.*)?$'), hooked)
            q2 = c2.new_page(); q2.goto(base + '/README.md'); q2.wait_for_timeout(300)
            p = c2.new_page(); errs = []
            p.on('pageerror', lambda e: errs.append(str(e)[:200]))
            p.goto(base + '/tour/index.html'); p.wait_for_timeout(800)   # 通常で開いて見本を入れる
            real0 = real_state(q2); dbs0 = idb_names(q2)
            p.goto(base + '/tour/index.html?check=1'); p.wait_for_timeout(1500)
            bs = panel_buttons(p)
            chk('CAアナウンス 通し' in bs and '機内食の場面だけ' in bs, tag + '割りこみ・顔なじみの欄に入口(通し・機内食だけ)が出る')
            txt = panel_text(p)
            i_ev = txt.find('割りこみ・顔なじみ'); i_pa = txt.find('CAアナウンス(048)'); i_win = txt.find('窓口の流れ')
            chk(0 <= i_ev < i_pa and (i_win < 0 or i_pa < i_win), tag + '入口は「割りこみ・顔なじみ」の欄にある')
            panel_click(p, label)
            txt = panel_text(p)
            chk(('→ ' + dest) in txt.split('CAアナウンス(048)')[1][:80], tag + '券を%sにすると行き先が %s と出る' % (label, dest))
            chk(ev(p, "()=>__T.save.ticket==='%s'" % ('star' if tk == 'star' else 'ow')), tag + '券の切りかえが効く')
            for rnd in (1, 2):   # 何度でも通しで試せる(fired を見ない)
                r = '[%s/%d回目] ' % (tk, rnd)
                panel_click(p, 'CAアナウンス 通し')
                chk(wait(p, "()=>__T.G.scene&&__T.G.scene.vid==='hnd_ev_ca_%s'" % tk, 8), r + 'CA場面が始まる')
                wait(p, "()=>document.querySelectorAll('#panel .dq').length>0", 20)
                ev(p, "()=>document.querySelectorAll('#panel .dq')[0].click()")
                chk(wait(p, "()=>__T.G.phase==='pa'", 40), r + 'マイクを渡される画面になる')
                chk(pbtn(p, 'はなす'), r + 'はなす を押せる')
                chk(wait(p, "()=>[].some.call(document.querySelectorAll('#panel button'),function(b){return /きいてます/.test(b.textContent)})", 8), r + 'マイクが開く(きいてます)')
                p.wait_for_timeout(1600)
                pbtn(p, 'きいてます')
                chk(wait(p, "()=>[].some.call(document.querySelectorAll('#panel button'),function(b){return /これでOK/.test(b.textContent)})", 8), r + '録り終わると もういちど・これでOK が出る')
                pbtn(p, 'これでOK')
                chk(wait(p, "()=>__T.G.scene&&__T.G.scene.vid==='hnd_ev_meal_%s'" % tk, 15), r + '機内食の場面に進む')
                chk(wait(p, "()=>document.getElementById('msgText').textContent.indexOf('%s')>=0" % dest, 10), r + '放送文に行き先 %s が出る' % dest)
                chk(wait(p, "()=>window.__au.indexOf('blob:')>=0", 12), r + '自分の声(blob:)が再生される', ev(p, "()=>window.__au"))
                chk(ev(p, "()=>window.__osc")>0, r + 'チャイムが鳴る')
                body = ev(p, "()=>document.body.innerText")
                chk(not any(w in body for w in BANNED), r + '画面に禁止語(録音・テスト等)が出ない')
                ev(p, "()=>__T.finishScene()")
                chk(wait(p, "()=>__T.G.view==='map'", 10), r + '終わると地図へ戻る')
                ev(p, "()=>{window.__au=[]}")
            # 機内食だけ(声は通しで録ったもの。終わりで消えるので、無ければ文だけで進む)
            panel_click(p, '機内食の場面だけ')
            chk(wait(p, "()=>__T.G.scene&&__T.G.scene.vid==='hnd_ev_meal_%s'" % tk, 15), tag + '機内食の場面だけも始まる')
            ev(p, "()=>__T.finishScene()"); wait(p, "()=>__T.G.view==='map'", 10)
            # 専用の記録の範囲
            real1 = real_state(q2); dbs1 = idb_names(q2)
            chk(real1 == real0, tag + '通常のセーブ(localStorage)は読み書きされず変わらない', [k for k in real1 if real1[k] != real0.get(k)])
            chk('kanpe-pa-rec-v1' not in dbs1 or 'kanpe-pa-rec-v1' in dbs0, tag + '通常の録音DB(kanpe-pa-rec-v1)は作られない', dbs1)
            chk('chk1:kanpe-pa-rec-v1' in dbs1, tag + '声は専用のDB(chk1:kanpe-pa-rec-v1)へ', dbs1)
            ks = ev(p, "()=>{var a=[];for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k.indexOf('chk1:')===0)a.push(k)}return a}")
            chk('chk1:kanpe-trip-v1' not in ks, tag + '旅の骨組み(kanpe-trip-v1)は動かない', ks)
            chk(ev(p, "()=>window.__net.length")==0, tag + 'ネットワークへの送信なし')
            chk(not errs, tag + 'ページのエラーなし', errs[:2])
            c2.close()
        br.close()
    print('\n結果:', 'NG %d件' % len(bad) if bad else 'NG 0件')
    sys.exit(1 if bad else 0)

main()
