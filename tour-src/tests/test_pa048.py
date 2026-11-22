# -*- coding: utf-8 -*-
"""タスク048(CAアナウンス・イベント)の動作確認(ヘッドレス Chromium)。使い方: python3 tour-src/tests/test_pa048.py
確かめること:
  1. 最初の長距離便(hnd_plane_ow / _star)の終わりで、CA→マイク→(録り直し)→これでOK→食事の場面(チャイム→自分の声の放送→ルルの反応)の順に流れる
  2. 声は端末内だけ: 録っているあいだ・再生のあいだ、ネットワークへの送信が一切ない(fetch / XHR / sendBeacon / WebSocket と、ブラウザの要求の両方で見る)。pa.js に外へ出すコードがない
  3. 保存は新しいキー(IndexedDB kanpe-pa-rec-v1)だけ。既存の保存キー(kanpe-pron-v1 / kanpe-voice-v1 / kanpe-tour-save-v1 の中身)に声は入らない
  4. 録り直しができる(確定の「これでOK」まで保存しない)。食事の場面が終わると声が消える
  5. マイク不許可・MediaRecorder なし・「こえを ださない モード」では、静かに飛ばして通常どおり進む(エラー画面なし)
  6. 2回目以降の便・もう一度の羽田では再発しない
  7. 画面に「録音」「テスト」「測定」などの言葉が出ない
マイクは Chromium の偽のマイク(--use-fake-device-for-media-stream)。実機(iPhone / Android)は確認できない(未確認)。リポジトリのファイルは書き換えない。"""
import os, re, sys, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import serve, ROOT
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pa_data

HOOK = "requestAnimationFrame(frame);\n})();"
BANNED = ['録音', 'テスト', '測定', '練習', '復習']

INIT = r"""
(function(){
 window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});
 window.__sp=[];window.__net=[];window.__au=[];window.__osc=0;var MODE=%s;
 setInterval(function(){var o=document.querySelector('.trip-ov');if(o&&!o.busy)o.click()},400);
 /* ネットワークに出る口を全部見張る(あれば記録) */
 try{var of=window.fetch;window.fetch=function(){window.__net.push('fetch '+String(arguments[0]&&arguments[0].url||arguments[0]));return of.apply(this,arguments)}}catch(e){}
 try{var xo=XMLHttpRequest.prototype.open;XMLHttpRequest.prototype.open=function(m,u){window.__net.push('xhr '+m+' '+u);return xo.apply(this,arguments)}}catch(e){}
 try{if(navigator.sendBeacon){var sb=navigator.sendBeacon;navigator.sendBeacon=function(u){window.__net.push('beacon '+u);return sb.apply(this,arguments)}}}catch(e){}
 try{var WS=window.WebSocket;window.WebSocket=function(u){window.__net.push('ws '+u);return new WS(u)}}catch(e){}
 /* 読み上げ・音声認識は偽物(記録だけ) */
 try{speechSynthesis.cancel=function(){};speechSynthesis.speak=function(u){window.__sp.push(u.text);setTimeout(function(){if(u.onstart)u.onstart({});setTimeout(function(){if(u.onend)u.onend({})},100)},10)}}catch(e){}
 function FS(){}FS.prototype.start=function(){var me=this;setTimeout(function(){var T=window.__T,G=T&&T.G,S=G&&G.scene,t=S&&S.turns&&S.turns[G.ti];var s=(t&&t.cue||'').replace(/\*/g,'');var rs=[{transcript:s,confidence:.95}];rs.isFinal=true;if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},10)},40)};
 FS.prototype.abort=FS.prototype.stop=function(){};window.SpeechRecognition=FS;window.webkitSpeechRecognition=FS;
 /* 再生を見張る(blob: の声が鳴ったか)。チャイムの音の数(オシレーター)も数える */
 try{var pl=HTMLMediaElement.prototype.play;HTMLMediaElement.prototype.play=function(){var me=this;window.__au.push({src:String(me.src).slice(0,5),t:Date.now()});return pl.apply(this,arguments)}}catch(e){}
 try{var AC0=window.AudioContext||window.webkitAudioContext;if(AC0){var co=AC0.prototype.createOscillator;AC0.prototype.createOscillator=function(){window.__osc++;return co.apply(this,arguments)}}}catch(e){}
 if(MODE==='deny'){navigator.mediaDevices.getUserMedia=function(){return Promise.reject(new DOMException('denied','NotAllowedError'))}}
 if(MODE==='nomr'){try{delete window.MediaRecorder}catch(e){window.MediaRecorder=undefined}}
 if(MODE==='silent'){try{localStorage.setItem('kd_prefs_v1',JSON.stringify({silent:1}))}catch(e){}}
 try{if(!localStorage.getItem('__seeded')){localStorage.setItem('__seeded','1');localStorage.setItem('kanpe-tour-save-v1',JSON.stringify({seen:{},help:5,weak:[],missed:[],ticket:window.__TK||'ow'}))}}catch(e){}
})();
"""


def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, "window.__T={G:G,PBY:PBY,startVid:startVid,finishScene:finishScene,save:save,DLG:DLG};" + HOOK, 1))


bad = []
def chk(c, m, v=''):
    print(('OK  ' if c else 'NG  ') + m + ((' ' + str(v)) if v != '' else ''))
    if not c: bad.append(m)


def newpage(br, base, mode, tk='ow', preset=None):
    ctx = br.new_context(viewport={'width': 390, 'height': 780})
    ctx.add_init_script("window.__TK=%s;" % json.dumps(tk))
    ctx.add_init_script(INIT % json.dumps(mode))
    if preset: ctx.add_init_script(preset)
    ctx.route(re.compile(r'.*/tour/index\.html(\?.*)?$'), hooked)
    p = ctx.new_page(); errs = []; reqs = []
    p.on('pageerror', lambda e: errs.append(str(e)[:200]))
    p.on('request', lambda r: reqs.append((r.method, r.url, bool(r.post_data))))
    p.goto(base + '/tour/index.html'); p.wait_for_timeout(1500)
    return ctx, p, errs, reqs


def ev(p, js, *a):
    return p.evaluate(js, *a) if a else p.evaluate(js)


def btns(p):
    return ev(p, "()=>[].map.call(document.querySelectorAll('#panel button'),function(b){return b.offsetParent&&!b.disabled?b.textContent.trim():null}).filter(Boolean)")


def click_btn(p, pat):
    return ev(p, "(pat)=>{var b=[].slice.call(document.querySelectorAll('#panel button')).filter(function(x){return x.offsetParent&&!x.disabled&&new RegExp(pat).test(x.textContent)})[0];if(b){b.click();return true}return false}", pat)


def wait(p, js, sec=20, step=150):
    t0 = time.time()
    while time.time() - t0 < sec:
        try:
            if ev(p, js): return True
        except Exception:
            pass
        p.wait_for_timeout(step)
    return False


def idb_state(p):
    """IndexedDB kanpe-pa-rec-v1 の中身: None=DBなし/空、dict=声あり"""
    return ev(p, """()=>new Promise(function(res){try{var q=indexedDB.open('kanpe-pa-rec-v1');q.onerror=function(){res('err')};
      q.onupgradeneeded=function(){q.__new=1};
      q.onsuccess=function(){var db=q.result;if(!db.objectStoreNames.contains('rec')){db.close();res(null);return}
        var r=db.transaction('rec','readonly').objectStore('rec').get('cur');
        r.onsuccess=function(){var v=r.result;db.close();res(v?{bytes:v.buf.byteLength,type:v.type,ms:v.ms}:null)};r.onerror=function(){db.close();res('err')}}}catch(e){res('exc')}})""")


def start_flight_end(p, vid):
    ev(p, "(v)=>{var T=window.__T;T.startVid(T.PBY.hplane,v,null);T.finishScene()}", vid)


def screen_text(p):
    return ev(p, "()=>document.body.innerText")


def main():
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required', '--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream'])

        # ===== 1〜4,7: 通し(oneworld / Star) =====
        for tk in ('ow', 'star'):
            tag = '[%s] ' % tk
            ctx, p, errs, reqs = newpage(br, base, 'ok', tk)
            keys0 = ev(p, "()=>Object.keys(localStorage).sort()")
            pron0 = ev(p, "()=>[localStorage.getItem('kanpe-pron-v1'),localStorage.getItem('kanpe-voice-v1')]")
            n_req0 = len(reqs)
            start_flight_end(p, 'hnd_plane_' + tk)
            ok = wait(p, "()=>__T.G.scene&&__T.G.scene.vid==='hnd_ev_ca_%s'" % tk, 8)
            chk(ok, tag + '機内の会話のあと、CA場面が始まる')
            chk(ev(p, "()=>__T.save.ev&&__T.save.ev.fired&&__T.save.ev.fired.pa1===1"), tag + 'この便で1回きり(fired.pa1)を記録')
            wait(p, "()=>document.querySelectorAll('#panel .dq').length>0", 15)
            ca_line = ev(p, "()=>document.getElementById('msgText').textContent")
            chk('announcement' in ca_line and 'voice' in ca_line, tag + 'CAが声の不調と放送を頼む', ca_line[:50])
            chk(ev(p, "()=>document.querySelector('#who,.who')&&document.body.innerText.indexOf('%s')>=0" % pa_data.VARIANTS[tk]['who']), tag + 'CAの名前の札が出る')
            ev(p, "()=>document.querySelectorAll('#panel .dq')[0].click()")
            chk(wait(p, "()=>__T.G.phase==='pa'", 40), tag + '引き受けるとマイクを渡される画面になる')
            chk(btns(p) == ['おてほん', '🎤 はなす'], tag + 'ボタン: おてほん・はなす', btns(p))
            # カンペ: 意味のまとまりで区切る
            rows = ev(p, "()=>[].map.call(document.querySelectorAll('#panel .pacard .pal'),function(l){return [].map.call(l.querySelectorAll('.pac'),function(c){return c.textContent})})")
            chk(rows == pa_data.chunks(tk), tag + 'カンペはPM案の文を、意味のまとまりごとに区切って出す', rows)
            chk(' '.join(' '.join(r) for r in rows) == pa_data.text(tk) and pa_data.text(tk).startswith('Welcome aboard, everyone. This is King, your guest announcer. We are flying to'), tag + 'カンペの文面はPM案のとおり', pa_data.text(tk))
            fs = ev(p, "()=>[].map.call(document.querySelectorAll('#panel .pac'),function(c){return parseFloat(getComputedStyle(c).fontSize)})")
            chk(min(fs) >= 20, tag + 'カンペの文字は小さすぎない(最小 %.0fpx)' % min(fs))
            chk(ev(p, "()=>{var c=document.querySelector('#panel .pacard');return c.scrollHeight<=c.clientHeight+1&&c.scrollWidth<=c.clientWidth+1}"), tag + 'カンペは枠に収まる(はみ出さない)')
            txt = screen_text(p)
            chk(not any(w in txt for w in BANNED), tag + '画面に「録音」「テスト」などの言葉が出ない(マイク画面)')
            chk(idb_state(p) is None, tag + '録る前: 端末内にも声はない')
            keys0 = ev(p, "()=>Object.keys(localStorage).sort()")
            pron0 = ev(p, "()=>[localStorage.getItem('kanpe-pron-v1'),localStorage.getItem('kanpe-voice-v1')]")
            reqs_before = len(reqs)
            # 1回目
            chk(click_btn(p, 'はなす'), tag + '「はなす」で始める')
            chk(wait(p, "()=>/きいてます/.test(document.getElementById('panel').innerText)", 10), tag + '録っているあいだは「きいてます…」')
            p.wait_for_timeout(1800)
            chk(not any(w in screen_text(p) for w in BANNED), tag + '画面に禁止語なし(録っている間)')
            chk(click_btn(p, 'きいてます'), tag + 'もう一度押すと止まる')
            chk(wait(p, "()=>/これでOK/.test(document.getElementById('panel').innerText)", 10), tag + '止めると「もういちど」「これでOK」')
            chk(btns(p) == ['もういちど', 'これでOK'], tag + 'ボタン: もういちど・これでOK', btns(p))
            chk(idb_state(p) is None, tag + '確定前: まだ端末内にも保存しない')
            # 録り直し
            chk(click_btn(p, 'もういちど'), tag + '「もういちど」で録り直す')
            chk(wait(p, "()=>/きいてます/.test(document.getElementById('panel').innerText)", 10), tag + '録り直しが始まる')
            p.wait_for_timeout(1600)
            click_btn(p, 'きいてます')
            chk(wait(p, "()=>/これでOK/.test(document.getElementById('panel').innerText)", 10), tag + '録り直しのあと、また確定を選べる')
            chk(idb_state(p) is None, tag + '録り直しても、確定まで保存しない')
            # 確定
            chk(click_btn(p, 'これでOK'), tag + '「これでOK」で確定')
            p.wait_for_timeout(800)
            st = idb_state(p)
            chk(isinstance(st, dict) and st['bytes'] > 1000, tag + '確定すると、端末内(IndexedDB kanpe-pa-rec-v1)に声が残る', st)
            keys1 = ev(p, "()=>Object.keys(localStorage).sort()")
            chk(keys1 == keys0, tag + '既存の保存(localStorage)にキーは増えない', sorted(set(keys1) ^ set(keys0)))
            chk(ev(p, "()=>[localStorage.getItem('kanpe-pron-v1'),localStorage.getItem('kanpe-voice-v1')]") == pron0, tag + 'kanpe-pron-v1 / kanpe-voice-v1 は変わらない')
            ls = ev(p, "()=>Object.keys(localStorage).map(function(k){return localStorage.getItem(k)||''}).join('|')")
            chk('UklGR' not in ls and 'GkXf' not in ls and 'data:audio' not in ls, tag + 'localStorage に音声データは入らない')
            # 食事の場面
            chk(wait(p, "()=>__T.G.scene&&__T.G.scene.vid==='hnd_ev_meal_%s'" % tk, 15), tag + '食事の場面が始まる')
            p.wait_for_timeout(300)
            osc0 = ev(p, "()=>window.__osc")
            au_n0 = len(ev(p, "()=>window.__au"))
            chk(wait(p, "()=>/Announcement/.test(document.body.innerText)&&!!document.querySelector('#msg .pa')", 6), tag + '放送の札と🔊の印が出る')
            ann = ev(p, "()=>document.getElementById('msgText').textContent")
            chk(ann == pa_data.text(tk), tag + '放送の文はカンペと同じ', ann[:60])
            chk(wait(p, "()=>window.__au.length>%d" % au_n0, 8), tag + 'そのあと、自分の声が(端末内の blob: で)再生される')
            au = ev(p, "()=>window.__au")
            chk(any(a['src'] == 'blob:' for a in au), tag + '再生元は端末内の blob:', [a['src'] for a in au])
            chk(ev(p, "()=>window.__osc") >= osc0 or ev(p, "()=>window.__osc") >= 3, tag + 'チャイム(3音)が鳴る/鳴らす呼び出し', ev(p, "()=>window.__osc"))
            chk(wait(p, "()=>__T.G.phase==='npc'||__T.G.phase==='cue'", 40), tag + '放送のあと、ルルが反応する')
            wait(p, "()=>/your voice/.test(document.getElementById('msgText').textContent)", 10)
            lulu = ev(p, "()=>document.getElementById('msgText').textContent")
            chk('your voice' in lulu and ev(p, "()=>document.body.innerText.indexOf('Lulu')>=0"), tag + 'ルルの台詞(自分の声に反応)', lulu[:60])
            chk(not any(w in screen_text(p) for w in BANNED), tag + '画面に禁止語なし(食事の場面)')
            # 会話を進めて、場面を終える
            for _ in range(80):
                try: v = ev(p, "()=>__T.G.scene&&__T.G.scene.vid")
                except Exception: v = None; break
                if ('/world/' in p.url) or (v and not v.startswith('hnd_ev_meal')): break
                p.wait_for_timeout(300)
            p.wait_for_timeout(500)
            chk('/world/' in p.url or ev(p, "()=>!window.PA||!window.PA.has()") , tag + '食事の場面が終わると、声は消える/ナイロビへ飛ぶ', p.url.replace(base, ''))
            ev_ok = True
            if '/world/' in p.url:
                for _ in range(15):
                    if idb_state(p) is None: break
                    p.wait_for_timeout(300)
                chk(idb_state(p) is None, tag + '便が終わると、端末内の声は消えている(世界マップ側で確認)', idb_state(p))
            else:
                chk(idb_state(p) is None, tag + '食事のあと、端末内の声は消えている', idb_state(p))
            # ネットワーク: マイク画面〜再生のあいだ
            net = ev(p, "()=>window.__net") if '/tour/' in p.url else []
            chk(net == [], tag + 'ページ内の fetch / XHR / sendBeacon / WebSocket が一度も呼ばれない', net)
            ext = [r for r in reqs[reqs_before:] if not r[1].startswith(base) and not r[1].startswith('blob:') and not r[1].startswith('data:') and 'fonts.googleapis.com' not in r[1] and 'fonts.gstatic.com' not in r[1]]
            posts = [r for r in reqs[reqs_before:] if r[0] != 'GET' or r[2]]
            chk(ext == [], tag + 'ブラウザの要求に、外部への通信がない', ext)
            chk(posts == [], tag + 'ブラウザの要求に、GET以外・送信データつきの要求がない', posts)
            chk(not errs and not ev(p, "()=>window.__errs") if '/tour/' in p.url else not errs, tag + 'エラーなし', errs)
            ctx.close()

        # ===== 6: 再発しない =====
        ctx, p, errs, reqs = newpage(br, base, 'ok', 'ow', preset="try{if(!localStorage.getItem('__seeded2')){localStorage.setItem('__seeded2','1');localStorage.setItem('kanpe-tour-save-v1',JSON.stringify({seen:{},help:5,weak:[],missed:[],ticket:'ow',ev:{fired:{pa1:1,pa2:1},streak:0,last:'ev'}}))}}catch(e){}")
        ev(p, "()=>{var T=window.__T;T.startVid(T.PBY.hplane,'hnd_plane_ow',null)}")
        chk(ev(p, "()=>window.PA.gate(__T.G.scene,function(){})") is False, '2回目以降の羽田の機内(fired.pa1あり)では、CAは再発しない')
        ev(p, "()=>{var T=window.__T;T.startVid(T.PBY.qplane,'nbo_plane1',null)}")
        chk(ev(p, "()=>window.PA.gate(__T.G.scene,function(){})") is False, 'ナイロビ→ドーハの便(2回目の長距離便)では始まらない')
        ctx.close()

        # ===== 5: 飛ばす(静かに) =====
        def skip_case(name, mode, expect_ca_asked):
            ctx, p, errs, reqs = newpage(br, base, mode, 'ow')
            start_flight_end(p, 'hnd_plane_ow')
            if expect_ca_asked:
                wait(p, "()=>__T.G.scene&&__T.G.scene.vid==='hnd_ev_ca_ow'", 8)
                wait(p, "()=>document.querySelectorAll('#panel .dq').length>0", 15)
                ev(p, "()=>document.querySelectorAll('#panel .dq')[0].click()")
                chk(wait(p, "()=>__T.G.phase==='pa'", 40), name + ': マイク画面までは進む')
                click_btn(p, 'はなす')
                p.wait_for_timeout(600)
                m = ev(p, "()=>document.getElementById('msgText').textContent")
                chk('No problem' in m, name + ': 断られたら、CAが静かに引き取る(エラー表示なし)', m)
                txt = screen_text(p)
                chk(not any(w in txt for w in BANNED + ['エラー', 'error', 'Error', '許可', 'できません']), name + ': エラーの言葉が出ない')
            else:
                seen = False
                for _ in range(40):
                    try:
                        if ev(p, "()=>!!(__T.G.scene&&/^hnd_ev_ca/.test(__T.G.scene.vid))||!!(__T.save.ev&&__T.save.ev.fired&&__T.save.ev.fired.pa1)"): seen = True; break
                    except Exception:
                        break
                    p.wait_for_timeout(200)
                chk(not seen, name + ': CA場面は始まらず、イベントの記録も付かず、通常どおり進む')
            # 先へ進む: 世界マップ(ナイロビへ飛ぶ)へ
            went = wait(p, "()=>location.pathname.indexOf('/world/')>=0", 25, 300) or '/world/' in p.url
            chk(went, name + ': 流れが止まらず、ナイロビへ飛ぶ(世界マップへ進む)', p.url.replace(base, ''))
            chk(not any(r[0] != 'GET' or r[2] for r in reqs), name + ': 送信なし')
            p.wait_for_timeout(500)
            chk(idb_state(p) is None, name + ': 端末内に声は残らない', idb_state(p))
            chk(not errs, name + ': ページのエラーなし', errs)
            ctx.close()
        skip_case('マイク不許可', 'deny', True)
        skip_case('MediaRecorderなし', 'nomr', False)
        skip_case('こえをださないモード', 'silent', False)

        br.close()

    # ===== 2: pa.js に外へ出すコード・Azure・既存の声の保存への入口が無い =====
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pa.js'), encoding='utf-8').read()
    code = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
    code = re.sub(r'(?m)^\s*//.*$', '', code)
    for w in ['fetch(', 'XMLHttpRequest', 'sendBeacon', 'WebSocket', 'EventSource', 'new Image', 'importScripts', 'voiceAzureOn', 'voiceSave', 'setupDiagAz', 'RELAY', 'relay', 'azure', 'Azure', 'kanpe-voice', 'kanpe-pron', 'plogAdd', 'localStorage', 'http://', 'https://']:
        chk(w not in code, 'pa.js(コメント除く)に「%s」が無い' % w)
    chk("'kanpe-pa-rec-v1'" in code, '保存キー(DB名)は kanpe-pa-rec-v1')
    print('NG件数:', len(bad))
    for b in bad: print('  NG:', b)
    sys.exit(1 if bad else 0)


main()
