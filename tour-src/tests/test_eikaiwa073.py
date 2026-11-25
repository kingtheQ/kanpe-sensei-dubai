# -*- coding: utf-8 -*-
"""タスク073 の動作確認(ヘッドレス)。使い方: python3 tour-src/tests/test_eikaiwa073.py
英会話カフェ(場面 nbo_eikaiwa1)の台本パート(5往復)のあとに足した「5分自由会話」。声の聞き取り・先生の声・中継 /chat は全部にせもの(モック)。
(1) 誘い:   台本パートが終わると、先生が英語で誘い、「話す／帰る」の▶選択肢(英文だけ)が出る。断ると、先生の穏やかな台詞のあと通常どおり終わる(中継は呼ばない)
(2) 往復:   承諾 → 先生の最初の一言 → 声(モック)→ 吹き出しに認識結果 → /chat(モック)→ 先生の返事を読み上げ → もう一度…。「Bye」と言うと先生が返して終わる。
            /chat には API キー・システムプロンプトを送らない。履歴は直近だけ。カンペ・発音の数値・日本語・数字は画面に出ない
(3) カップ: 偽の時計で、コーヒーの画素が時間に連動して減る(0→1/300000 の刻み)。数字・タイマーの文字が画面にない。自由会話の外ではカップを描かない
(4) 締め:   時間切れ(聞いている最中・返事待ち・先生が話している最中)・途中で帰る(Bye ボタン・✕)・Bye と言う、のどれでも、先生の台詞のあと場面が終わる
(5) 失敗:   /chat が 503 not_configured・通信失敗・空の返事のとき、穏やかに締める(エラー画面・日本語・「error」の文字なし)。日本語まじりの返事は使わない。
            聞き取れない(3回で締め)・無音(軽い質問で助け、3回で締め)・マイク拒否
(6) 出さない環境: 音声認識がないとき・PREF.silent のときは、誘い自体を出さない(台本パートだけで終わる)
(7) 保存:   localStorage のキー一覧が増えない。自由会話の内容(会話の文)が、どの保存にも入らない
(8) 既存:   nbo_java1/2 の台本が変更前と同じ。台本パート(5往復)の中身が同じ。画面に「勉強・テスト・測定・復習・採点・点数・練習」が出ない
マイク・実際のAIの返事・iOS Safari は確認できない(未確認)。"""
import os, sys, re, json, subprocess, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import serve, ROOT
from playwright.sync_api import sync_playwright

HOOK = "requestAnimationFrame(frame);\n})();"
EXPOSE = ("window.__T={G:G,save:save,DLG:DLG,PREF:PREF,FT:FT,SP:SP,setSR:function(v){SR=v},get spSay(){return spSay}};")
INIT = """
window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(String(e.message))});
window.__spoken=[];window.__sayMs=8;window.__sr=[];window.__srStarts=0;window.__txt=[];
try{speechSynthesis.speak=function(u){window.__spoken.push(u.text);(window.__pitch=window.__pitch||[]).push([u.text,u.pitch]);setTimeout(function(){if(u.onend)u.onend({})},window.__sayMs)};speechSynthesis.cancel=function(){}}catch(e){}
(function(){function FS(){}
window.__cont=[];window.__finalAt=0;window.__pitch=[];
FS.prototype.start=function(){var me=this;me.__ab=false;window.__srStarts++;window.__cont.push(!!me.continuous);
 var cue=[].map.call(document.querySelectorAll('.cue .w'),function(x){return x.textContent}).join(' ');
 if(cue){setTimeout(function(){var rs=[{transcript:cue,confidence:.9}];rs.isFinal=true;if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},20)},60);return}
 var b=window.__sr.length?window.__sr.shift():{k:'silence'};
 function end(){if(!me.__ab&&me.onend)me.onend({})}
 me.__res=[];
 /* continuous の認識: results は積み上がる。途中経過(interim)は、あとの結果で置き換わる */
 function emit(t,fin){var rs=[{transcript:t,confidence:.9}];rs.isFinal=fin;var last=me.__res[me.__res.length-1];if(last&&!last.isFinal)me.__res.pop();
  var idx=me.__res.length;me.__res.push(rs);if(fin)window.__finalAt=performance.now();if(me.onresult)me.onresult({resultIndex:idx,results:me.__res.slice()})}
 if(b.k==='say')setTimeout(function(){if(me.__ab)return;if(me.onspeechstart)me.onspeechstart();emit(b.t,true);if(b.end!==undefined)setTimeout(end,b.end)},60);   /* 1つの final。そのあとセッションは開いたまま(continuous) */
 else if(b.k==='seq'){b.steps.forEach(function(s,i){setTimeout(function(){if(me.__ab)return;if(i===0&&me.onspeechstart)me.onspeechstart();emit(s.t,!!s.f)},s.at)});if(b.end!==undefined)setTimeout(end,b.end)}   /* 時間差の途中経過・final。end があればそのあとセッションを切る(Chrome の自動切断) */
 else if(b.k==='silence')setTimeout(function(){if(me.__ab)return;if(me.onerror)me.onerror({error:'no-speech'});end()},60);
 else if(b.k==='miss')setTimeout(function(){if(me.__ab)return;if(me.onspeechstart)me.onspeechstart();end()},60);
 else if(b.k==='deny')setTimeout(function(){if(me.onerror)me.onerror({error:'not-allowed'});end()},30);
 /* hang = 聞き続ける(abort されるまで終わらない) */};
FS.prototype.abort=function(){this.__ab=true};
FS.prototype.stop=function(){var me=this;setTimeout(function(){if(!me.__ab&&me.onend){me.__ab=true;me.onend({})}},10)};
if(!window.__noSR){window.SpeechRecognition=FS;window.webkitSpeechRecognition=FS}})();
"""
bad = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
JP = re.compile(r"[぀-ヿ㐀-鿿]")
FORBID = ['勉強', 'テスト', '測定', '復習', '採点', '点数', '練習', 'スコア']
ERRW = re.compile(r"error|エラー|失敗|503|502|not_configured|undefined|NaN|null|http", re.I)
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    route.fulfill(response=r, body=body.replace(HOOK, EXPOSE + HOOK, 1))
def hooked_head(route):
    body = subprocess.check_output(['git', '-C', ROOT, 'show', 'HEAD:tour/index.html']).decode('utf-8')
    assert HOOK in body
    route.fulfill(status=200, content_type='text/html; charset=utf-8', body=body.replace(HOOK, EXPOSE.replace('FT:FT,', '') + HOOK, 1))

srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
CORS = {'access-control-allow-origin': '*', 'access-control-allow-headers': 'content-type', 'access-control-allow-methods': 'POST, OPTIONS'}

def chat_ok(replies):
    """/chat のモック: 順番に返事を返す。送られた本文を記録する"""
    box = {'reqs': [], 'i': 0, 'ts': []}
    def h(route, request):
        if request.method == 'OPTIONS': route.fulfill(status=204, headers=CORS); return
        box['reqs'].append(request.post_data_json); box['ts'].append(time.time())
        r = replies[min(box['i'], len(replies) - 1)]; box['i'] += 1
        body = dict(r) if isinstance(r, dict) else {'reply': r}; body['via'] = 'workers-ai'   # 文字列=旧形式(fix なし)・dict={reply,fix}
        route.fulfill(status=200, headers=CORS, content_type='application/json', body=json.dumps(body))
    return h, box
def chat_status(code, body='{"error":"not_configured"}'):
    box = {'reqs': []}
    def h(route, request):
        if request.method == 'OPTIONS': route.fulfill(status=204, headers=CORS); return
        box['reqs'].append(request.post_data_json); route.fulfill(status=code, headers=CORS, content_type='application/json', body=body)
    return h, box
def chat_fail():
    box = {'reqs': []}
    def h(route, request):
        if request.method == 'OPTIONS': route.fulfill(status=204, headers=CORS); return
        box['reqs'].append(request.post_data_json); route.abort()
    return h, box
def chat_hang():
    box = {'reqs': []}
    def h(route, request):
        if request.method == 'OPTIONS': route.fulfill(status=204, headers=CORS); return
        box['reqs'].append(request.post_data_json)   # 返さない
    return h, box

def mk(br, chat=None, init_extra='', prefs=None, route=hooked, vp=(430, 900)):
    ctx = br.new_context(viewport={'width': vp[0], 'height': vp[1]}); ctx.add_init_script(INIT + init_extra)
    ctx.add_init_script("localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}));" + ("localStorage.setItem('kd_prefs_v1',%s);" % json.dumps(json.dumps(prefs)) if prefs else ''))
    p = ctx.new_page()
    p.route('**/tour/index.html*', route)
    if chat: p.route(re.compile(r'https://kanpe-speech-relay\..*/chat$'), chat)
    return p
def enter(p):
    p.goto(base + '/tour/index.html?check=1'); p.wait_for_timeout(1500); p.mouse.click(215, 450); p.wait_for_timeout(600)
    p.evaluate("()=>document.getElementById('chkBtn').click()"); p.wait_for_timeout(150)
    p.evaluate("()=>{[].filter.call(document.querySelectorAll('#chkPan button'),function(b){return b.textContent==='nbo_eikaiwa1'})[0].click()}"); p.wait_for_timeout(600)
    p.evaluate("""()=>{window.__txt=[];setInterval(function(){try{var q=function(i){var e=document.getElementById(i);return e?e.innerText.replace(/\\s+/g,' '):''};window.__txt.push({ph:__T.G.phase,msg:(document.getElementById('msgText')||{}).textContent,who:q('who'),panel:q('panel'),heard:(document.querySelector('.ftheard')||{}).textContent||'',dq:[].map.call(document.querySelectorAll('.dq'),function(x){return x.textContent}),cue:!!document.querySelector('.cue')})}catch(e){}},40)}""")
    p.click('.btn.go')
def wait_free(p, timeout=60000):
    p.wait_for_function("()=>__T.G.phase==='free'&&document.querySelectorAll('.dq').length===2", timeout=timeout)
def wait_map(p, timeout=40000):
    p.wait_for_function("()=>__T.G.view==='map'", timeout=timeout)
def close(p):
    try: p.unroute_all(behavior='ignoreErrors')
    except Exception: pass
    p.context.close()
def view(p): return p.evaluate("()=>__T.G.view")
def accept(p, clock=True, sil=300):
    if clock: p.evaluate("()=>{window.__now=0;__T.FT.clock=function(){return window.__now}}")
    if sil: p.evaluate("(m)=>{__T.FT.silenceMs=m}", sil)   # 送信までの沈黙。既定(2800ms)は 9b/9c で確かめる。ほかのテストは速く進めるため短くする
    p.evaluate("()=>document.querySelectorAll('.dq')[0].click()")
def decline(p): p.evaluate("()=>document.querySelectorAll('.dq')[1].click()")
def spoken(p): return p.evaluate("()=>window.__spoken.slice()")
def keys(p): return p.evaluate("()=>Object.keys(localStorage).sort()")
def alltxt(p): return p.evaluate("()=>window.__txt")
def free_txt(p):
    return [t for t in alltxt(p) if t['ph'] == 'free']
def errs(p): return p.evaluate("()=>window.__errs.slice()")

with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    # ================= (1) 誘いと、断る =================
    p = mk(br); enter(p); wait_free(p)
    p.wait_for_timeout(2600)   # 打ち字(1文字26ms)が終わるのを待つ。本物の声は数秒かかるので、実機では自然にそろう
    sp0 = spoken(p); dl = p.evaluate("()=>__T.DLG.nbo_eikaiwa1"); npc = [l['n'] for l in dl['lines'] if l.get('n')]
    T = free_txt(p); T = [t for t in T if t['dq']][0]
    L = p.evaluate("()=>__T.FT.lines")
    chk('1a 台本パートが終わると、先生が英語で誘う(声で読まれ、画面にも出る)。5往復の先生の台詞が先に全部読まれている', L['invite'] in sp0 and all(n in sp0 for n in npc) and sp0.index(L['invite']) > max(sp0.index(n) for n in npc), sp0[-3:])
    chk('1b 選択肢は英文だけ(▶ の2行・日本語なし)。見た目は既存の▶選択肢(.dqbox/.dq)。先生の誘いは画面にも出ている', len(T['dq']) == 2 and all(re.search(r'[A-Za-z]', d) and not JP.search(d) for d in T['dq']) and any(t['msg'] == L['invite'] for t in alltxt(p) if t['ph'] == 'free'), T['dq'])
    chk('1c 誘いの画面にカンペ(.cue)は出ない。カップはまだ描かれない(FT.cup()=null)', not any(t['cue'] for t in alltxt(p) if t['ph'] == 'free') and p.evaluate("()=>__T.FT.cup()") is None)
    pre_keys = keys(p)
    decline(p); wait_map(p)
    sp1 = spoken(p)
    chk('1d 断ると、先生の穏やかな台詞(英語)のあと、通常どおりマップへ戻る。エラーなし', L['decline'] in sp1 and view(p) == 'map' and not errs(p), (sp1[-2:], errs(p)))
    chk('1e 断ったとき、中継(/chat)は呼ばない・マイクを聞き始めない(台本パートの5回のあと増えない)', p.evaluate("()=>window.__srStarts") == 5, p.evaluate("()=>window.__srStarts"))
    base_keys = keys(p)
    close(p)

    # ================= (2) 承諾 → 往復 → Bye =================
    h, box = chat_ok(['Oh, nice! You went to the zebra market. What did you buy?', 'That sounds good! Do you like fresh fruit?'])
    p = mk(br, h); enter(p); wait_free(p)
    p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'say',t:'I went to the zebra market yesterday'},{k:'say',t:'I bought mango and banana'},{k:'hang'})}")
    accept(p)
    p.wait_for_function("()=>document.querySelector('.ftbox')", timeout=10000)
    sp = spoken(p)
    chk('2a 承諾すると、先生の最初の一言(英語)が読まれ、🎤 と Bye のボタンが出る。聞き取りが自動で始まる', L['open'] in sp and p.evaluate("()=>[].map.call(document.querySelectorAll('.ftbox button'),function(b){return b.textContent}).join('|')") == '🎤|Bye', sp[-2:])
    p.wait_for_function("()=>window.__spoken.indexOf('That sounds good! Do you like fresh fruit?')>=0", timeout=15000)
    p.wait_for_timeout(300); p.screenshot(path='/tmp/ft073_listening.png')
    chk('2b /chat に2回送られ、先生の返事が声で読まれる(1回目・2回目とも)', len(box['reqs']) == 2 and 'Oh, nice! You went to the zebra market. What did you buy?' in spoken(p), len(box['reqs']))
    r1, r2 = box['reqs']
    chk('2c 送る本文は {messages:[{role,content}]} だけ。APIキー・system・モデル名・先生の設定を送らない。履歴は先生の最初の一言から', list(r1.keys()) == ['messages'] and r1['messages'][0] == {'role': 'assistant', 'content': L['open']} and r1['messages'][-1] == {'role': 'user', 'content': 'I went to the zebra market yesterday'} and all(m['role'] in ('user', 'assistant') for m in r1['messages']) and not re.search(r'key|system|model|prompt|Bearer', json.dumps(r1), re.I), r1)
    chk('2d 2回目の送信には、1回目のやりとり(先生の返事も)が履歴として入り、最後はプレイヤーの発言。交互になっている', [m['role'] for m in r2['messages']] == ['assistant', 'user', 'assistant', 'user'] and r2['messages'][2]['content'].startswith('Oh, nice!') and r2['messages'][-1]['content'] == 'I bought mango and banana', r2['messages'])
    T = free_txt(p)
    chk('2e 認識結果がそのまま吹き出し(.ftheard)に出る。日本語訳・カンペ・数値の判定は出ない', any(t['heard'] == 'I went to the zebra market yesterday' for t in T) and not any(t['cue'] for t in T) and not any(JP.search(t['msg'] or '') or JP.search(t['heard']) or any(JP.search(d) for d in t['dq']) for t in T), [t['heard'] for t in T][-1])
    chk('2f 先生の返事が画面(メッセージ欄)にも出る(打ち字の途中まででも、返事の頭が出ている)', any((t['msg'] or '').startswith('Oh, nice!') for t in T))
    # Bye と言う → 先生が返して終わる(AIを呼ばない)
    n = len(box['reqs']); p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'say',t:'ok, bye bye'})}")
    p.evaluate("()=>{var m=document.querySelector('.ftbox button');m.click()}")   # いま聞いている最中(hang)の聞き直し=止める→何も聞こえず→聞き直し
    p.wait_for_function("()=>window.__spoken.indexOf(%s)>=0" % json.dumps(L['bye']), timeout=15000); wait_map(p)
    chk('2g 「bye」と言うと、先生が「バイバイ」に返して、場面が終わる(マップへ。AIは呼ばない・エラーなし)', len(box['reqs']) == n and view(p) == 'map' and not errs(p), (len(box['reqs']), errs(p)))
    chk('2h 終わったあと、FT のカップは null(自由会話の内容は残らない)', p.evaluate("()=>__T.FT.cup()") is None)
    full_keys = keys(p)
    mark = p.evaluate("()=>{var s=[];for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);var v=localStorage.getItem(k);if(/zebra|mango|banana|fresh fruit|What did you buy/i.test(v))s.push(k)}for(var j=0;j<sessionStorage.length;j++){if(/zebra|mango|banana/i.test(sessionStorage.getItem(sessionStorage.key(j))))s.push('session:'+sessionStorage.key(j))}return s}")
    chk('7a 新しい保存キーを作らない(自由会話をしたあとの localStorage のキー一覧が、断って台本パートだけで終えたときと同じ)', full_keys == base_keys, (set(full_keys) ^ set(base_keys)))
    chk('7b 自由会話の中身(プレイヤーの英語・先生の返事)が、どの保存(localStorage・sessionStorage)にも入っていない', mark == [], mark)
    allp = ' '.join((t['msg'] or '') + ' ' + t['panel'] + ' ' + t['heard'] for t in alltxt(p))
    chk('8a 画面に「勉強・テスト・測定・復習・採点・点数・練習」の言葉が出ない', not any(w in allp for w in FORBID), [w for w in FORBID if w in allp])
    close(p)

    # ================= (3) カップ: 偽の時計で、時間に連動 =================
    h, box = chat_ok(['Nice!'])
    p = mk(br, h); enter(p); wait_free(p)
    def coffee(p):
        return p.evaluate("""()=>{var d=document.getElementById('sceneA').getContext('2d').getImageData(757,656,96,64).data,n=0,hl=0;for(var i=0;i<d.length;i+=4){if(d[i]===107&&d[i+1]===63&&d[i+2]===35)n++;if(d[i]===143&&d[i+1]===90&&d[i+2]===52)hl++}return [n,hl]}""")
    chk('3a 自由会話の前(誘いの最中)は、カップのコーヒーの画素がない(カップを描かない)', coffee(p) == [0, 0], coffee(p))
    p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'hang'},{k:'hang'})}")
    accept(p); p.wait_for_function("()=>document.querySelector('.ftheard.live')", timeout=10000)
    exp = lambda f: 80 * max(0, int(f * 10 + 0.5) * 4 - 4)   # 水面の1段(4px)はハイライト色
    seq = []
    for now, f in [(0, 1.0), (30000, .9), (120000, .6), (210000, .3), (288000, .04)]:
        p.evaluate("(n)=>{window.__now=n}", now); p.wait_for_timeout(250)
        c = coffee(p); seq.append((now, c[0], exp(f), c[1]))
    chk('3b コーヒーの画素が、偽の時計の進みに連動して減る(経過 0・30・120・210・288秒 → 水面を除くコーヒー 2880・2560・1600・640・0 画素＋水面の1段 320・320・320・320・0)', [s[1] for s in seq] == [s[2] for s in seq] == [2880, 2560, 1600, 640, 0] and [s[3] for s in seq] == [320, 320, 320, 320, 0], seq)
    chk('3c 単調に減っていて、増えない', all(seq[i][1] >= seq[i + 1][1] for i in range(len(seq) - 1)))
    p.evaluate("(n)=>{window.__now=n}", 150000); p.wait_for_timeout(250); p.screenshot(path='/tmp/ft073_cup_half.png')
    T = free_txt(p)
    digit = [t for t in T if re.search(r'[0-9０-９]', (t['msg'] or '') + t['panel'] + t['heard'] + t['who'].replace('英会話カフェの先生', ''))]
    chk('3d 数字・タイマーの文字が画面(メッセージ欄・パネル・吹き出し)に出ない', not digit and not any(re.search(r'\d\s*[:：]\s*\d', (t['msg'] or '') + t['panel']) for t in T), digit[:1])
    p.evaluate("(n)=>{window.__now=n}", 0)
    close(p)

    # ================= (4) 締め: 時間切れ(3つの状態)・途中で帰る =================
    for label, setup in [('聞いている最中', 'listen'), ('返事待ちの最中', 'think'), ('先生が話している最中', 'say')]:
        if setup == 'think': h, box = chat_hang()
        else: h, box = chat_ok(['Oh, I see. What do you like to eat?'])
        p = mk(br, h); enter(p); wait_free(p)
        if setup == 'say': p.evaluate("()=>{window.__sayMs=1800}")
        p.evaluate("()=>{window.__sr.length=0;" + ("window.__sr.push({k:'say',t:'I like rice'});" if setup == 'think' else "window.__sr.push({k:'hang'});") + "}")
        accept(p)
        if setup == 'listen': p.wait_for_function("()=>document.querySelector('.ftheard.live')&&window.__srStarts>=6", timeout=15000)
        if setup == 'think': p.wait_for_function("()=>window.__spoken.length>0&&window.__srStarts>=6", timeout=15000); p.wait_for_timeout(800)
        if setup == 'say': p.wait_for_timeout(300)   # 最初の一言(1.8秒)を話している最中
        n0 = len(spoken(p)); p.evaluate("()=>{window.__now=300000}")
        wait_map(p, 30000); sp = spoken(p); closing = [s for s in sp if s in L['time']]
        chk('4%s 時間切れ(%s): 先生の締めの台詞(英語)のあと、場面が終わる。エラー・日本語なし' % ('abc'[['listen', 'think', 'say'].index(setup)], label), len(closing) == 1 and view(p) == 'map' and not errs(p), (sp[-2:], errs(p)))
        close(p)
    # 途中で帰る: Bye ボタン / ✕
    for label, how in [('Bye ボタン', 'bye'), ('✕ ボタン', 'x')]:
        h, box = chat_ok(['Oh, nice! Where do you live?'])
        p = mk(br, h); enter(p); wait_free(p)
        p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'say',t:'I am a traveler'},{k:'hang'})}"); accept(p)
        p.wait_for_function("()=>window.__spoken.indexOf('Oh, nice! Where do you live?')>=0", timeout=15000); p.wait_for_timeout(500)
        if how == 'bye': p.evaluate("()=>document.querySelectorAll('.ftbox button')[1].click()")
        else: p.evaluate("()=>document.getElementById('exitBtn').click()")
        p.wait_for_function("()=>window.__spoken.indexOf(%s)>=0" % json.dumps(L['bye']), timeout=10000); wait_map(p)
        chk('4%s 途中で出る(%s): 先生が「バイバイ」に自然に返し、そのあと場面が終わる。会話は捨てられる(FT のカップ null・以後の通信なし)' % ('de'[['bye', 'x'].index(how)], label), view(p) == 'map' and p.evaluate("()=>__T.FT.cup()") is None and not errs(p), errs(p))
        n = len(box['reqs']); p.wait_for_timeout(800)
        chk('4%s2 場面を出たあと、聞き取りも通信も続かない(通信は増えない)' % 'de'[['bye', 'x'].index(how)], len(box['reqs']) == n)
        close(p)

    # ================= (5) 失敗: /chat と聞き取り =================
    for label, mkh in [('503 not_configured', lambda: chat_status(503)), ('502', lambda: chat_status(502, '{"error":"upstream_error"}')), ('通信失敗(接続できない)', chat_fail),
                       ('空の返事', lambda: chat_ok(['   '])), ('返事が返らない(15秒の上限)', chat_hang)]:
        h, box = mkh()
        p = mk(br, h); enter(p); wait_free(p)
        p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'say',t:'I like tea'})}"); accept(p)
        if '15秒' in label:
            p.wait_for_function("()=>window.__srStarts>=6", timeout=15000); p.wait_for_timeout(500)
        wait_map(p, 40000); sp = spoken(p); T = alltxt(p)
        shown = ' '.join((t['msg'] or '') + ' ' + t['panel'] + ' ' + t['heard'] for t in T if t['ph'] == 'free')
        chk('5 /chat %s: 先生の穏やかな締めの台詞(英語)で終わり、場面が終わる。エラーの文字・日本語を出さない' % label, L['busy'] in sp and view(p) == 'map' and not ERRW.search(shown) and not JP.search(shown) and not errs(p), (sp[-1:], shown[-80:], errs(p)))
        close(p)
    # 日本語まじりの返事は使わない
    h, box = chat_ok(['こんにちは! Nice to meet you.', 'Great! What is your favorite food?'])
    p = mk(br, h); enter(p); wait_free(p)
    p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'say',t:'Hello teacher'},{k:'hang'})}"); accept(p)
    p.wait_for_function("(n)=>window.__spoken.some(function(s){return n.indexOf(s)>=0})", arg=L['nudge'], timeout=15000); p.wait_for_timeout(300)
    T = free_txt(p); sp = spoken(p)
    chk('5b 返事に日本語が混ざっていたら、それは出さず・読まず、先生の軽い質問(英語)に差し替えて会話を続ける。差し替えが起きたことは FT.swaps(=1)で検出できる', not any(JP.search((t['msg'] or '')) for t in T) and not any(JP.search(s) for s in sp) and sp[-1] in L['nudge'] and view(p) == 'scene' and p.evaluate("()=>__T.FT.swaps") == 1, sp[-1:])
    close(p)
    # 聞き取れない: 3回で締め(2回までは聞き返し)
    h, box = chat_ok(['Nice!'])
    p = mk(br, h); enter(p); wait_free(p)
    p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'miss'},{k:'miss'},{k:'miss'})}"); accept(p)
    wait_map(p, 40000); sp = spoken(p)
    chk('5c 聞き取れないことが3回続くと、先生が聞き返し(2回・毎回ちがう文)→ 穏やかに締めて終わる。AIは呼ばない・エラーなし', sp[-3] in L['reask'] and sp[-2] in L['reask'] and sp[-3] != sp[-2] and sp[-1] == L['soft'] and len(box['reqs']) == 0 and not errs(p), sp[-4:])
    close(p)
    # 無音: 軽い質問で助ける。1回だけなら続く。3回で締め
    h, box = chat_ok(['Oh, I see. Do you like coffee?'])
    p = mk(br, h); enter(p); wait_free(p)
    p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'silence'},{k:'say',t:'I like coffee'},{k:'hang'})}"); accept(p)
    p.wait_for_function("()=>window.__spoken.indexOf('Oh, I see. Do you like coffee?')>=0", timeout=15000)
    sp = spoken(p); i = sp.index(L['open'])
    chk('5d 無音が続いたら、先生から軽い質問を投げ直す(英語・会話は続く)。そのあと話せば普通に往復する', sp[i + 1] in L['nudge'] and len(box['reqs']) == 1 and view(p) == 'scene', sp[i:i + 3])
    close(p)
    p = mk(br, chat_ok(['x'])[0]); enter(p); wait_free(p)
    p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'silence'},{k:'silence'},{k:'silence'})}"); accept(p)
    wait_map(p, 40000); sp = spoken(p)
    chk('5e 無音が3回続くと、先生が穏やかに締めて終わる', sp[-1] == L['soft'] and view(p) == 'map' and not errs(p), sp[-3:])
    close(p)
    p = mk(br, chat_ok(['x'])[0]); enter(p); wait_free(p)
    p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'deny'})}"); accept(p)
    wait_map(p, 30000); sp = spoken(p)
    chk('5f マイクが使えない(拒否)とき、エラー画面を出さず、先生が穏やかに締めて終わる', sp[-1] == L['soft'] and view(p) == 'map' and not errs(p), sp[-2:])
    close(p)

    # ================= (6) 出さない環境 =================
    p = mk(br, chat_ok(['x'])[0]); enter(p)
    p.wait_for_function("()=>__T.G.phase==='clear'", timeout=60000); p.evaluate("()=>{__T.PREF.silent=1}")
    p.wait_for_timeout(2500)
    chk('6a こえをださないモード(PREF.silent)では、自由会話の誘いを出さない(台本パートだけで終わり、マップへ)', view(p) == 'map' and not [t for t in alltxt(p) if t['ph'] == 'free'] and p.evaluate("()=>__T.FT.want({d:{freetalk:1}})") is False, view(p))
    close(p)
    p = mk(br, chat_ok(['x'])[0]); enter(p)
    p.wait_for_function("()=>__T.G.phase==='clear'", timeout=60000); p.evaluate("()=>{__T.setSR(null)}")
    p.wait_for_timeout(2500)
    chk('6b 音声認識がないブラウザ(SR なし)では、誘いを出さない(台本パートだけで終わり、マップへ)', view(p) == 'map' and not [t for t in alltxt(p) if t['ph'] == 'free'] and p.evaluate("()=>__T.FT.want({d:{freetalk:1}})") is False, view(p))
    close(p)

    # ================= (9) タスク079: 聞き取り(continuous・蓄積・送信タイミング) =================
    # 9a/9b: 考えて間があいても先に進まない。final を蓄積し、最後の発話から約2.8秒の沈黙で、全文を1回だけ送る(既定の時間で確かめる)
    h, box = chat_ok(['Mombasa sounds nice. Did you swim there?'])
    p = mk(br, h); enter(p); wait_free(p)
    p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'seq',steps:[{t:'I went to',f:1,at:60},{t:'the zebra',f:0,at:1500},{t:'the zebra market',f:1,at:1800}]},{k:'hang'})}")
    accept(p, sil=0)   # 沈黙の待ちは既定のまま
    chk('9a-0 FT の沈黙の待ちの既定は約2.8秒(2.5〜3秒の範囲)', 2500 <= p.evaluate("()=>__T.FT.silenceMs") <= 3000, p.evaluate("()=>__T.FT.silenceMs"))
    p.wait_for_function("()=>document.querySelector('.ftheard.live')&&window.__srStarts>=6", timeout=15000)
    p.wait_for_timeout(1000)   # 1つ目の final(I went to)から約1秒: まだ送らない
    chk('9a continuous=true で聞いている(聞き取りの開始すべて)', p.evaluate("()=>window.__cont.slice(5).length>0&&window.__cont.slice(5).every(function(x){return x===true})"), p.evaluate("()=>window.__cont"))
    chk('9b 考えて間があいても(約1.5秒)先に進まない: 言いかけの文は先生に送られない・履歴にも入らない。heard 欄には途中経過がそのまま出ている', len(box['reqs']) == 0 and p.evaluate("()=>document.querySelector('.ftheard').textContent") == 'I went to', (len(box['reqs']), p.evaluate("()=>document.querySelector('.ftheard').textContent")))
    p.wait_for_timeout(1400)   # 2つ目の途中経過(the zebra)が出ている頃
    chk('9b2 話している途中の途中経過(interim)が、蓄積した言葉のあとにリアルタイムで出る', p.evaluate("()=>document.querySelector('.ftheard').textContent") in ('I went to the zebra', 'I went to the zebra market'), p.evaluate("()=>document.querySelector('.ftheard').textContent"))
    p.wait_for_function("()=>window.__finalAt>0&&performance.now()-window.__finalAt>1500", timeout=8000)
    chk('9b3 最後の発話から1.5秒たっても、まだ送らない(沈黙の待ち 約2.8秒の途中)', len(box['reqs']) == 0)
    for _ in range(80):
        if box['reqs']: break
        p.wait_for_timeout(100)
    fa = p.evaluate("()=>window.__finalAt"); now_ms = p.evaluate("()=>performance.now()")
    chk('9c 送信は「最後の final から約2.5〜3秒の沈黙」のあと。送られた発言は蓄積した全文を1回だけ(言いかけの "I went to" は単独で送られない)', len(box['reqs']) == 1 and box['reqs'][0]['messages'][-1] == {'role': 'user', 'content': 'I went to the zebra market'} and [m['content'] for m in box['reqs'][0]['messages'] if m['role'] == 'user'] == ['I went to the zebra market'], box['reqs'][:1])
    sent_after = (now_ms - fa) / 1000.0
    chk('9c2 送られた時刻は最後の final から約2.8秒後(2.4〜3.6秒の間。測定: 送信を確認した時点で最後の final から %.2f 秒)' % sent_after, 2.4 <= sent_after <= 3.9, sent_after)
    close(p)

    # 9d: 🎤タップ=言い終わり → 沈黙を待たずに即送信
    h, box = chat_ok(['Rice is great. I like it too.'])
    p = mk(br, h); enter(p); wait_free(p)
    p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'say',t:'I like rice'},{k:'hang'})}")
    accept(p, sil=0)
    p.wait_for_function("()=>document.querySelector('.ftheard.live')&&document.querySelector('.ftheard').textContent==='I like rice'", timeout=15000)
    p.wait_for_timeout(300)
    chk('9d-0 タップ前は送られていない', len(box['reqs']) == 0)
    t_tap = time.time(); p.evaluate("()=>document.querySelector('.ftbox button').click()")
    for _ in range(40):
        if box['reqs']: break
        p.wait_for_timeout(50)
    chk('9d 🎤タップ=言い終わり: 沈黙(2.8秒)を待たずに、すぐ(1秒以内)送られる。送る本文は聞こえた言葉', len(box['reqs']) == 1 and box['reqs'][0]['messages'][-1]['content'] == 'I like rice' and box['ts'][0] - t_tap < 1.0, (len(box['reqs']), box['ts'][0] - t_tap if box['ts'] else None))
    close(p)

    # 9e: 認識のセッションが途中で切れても、自動で再開し、表示は初期化されない(「聞いてない」ように見えない)。🎤の脈打ちも途切れない
    h, box = chat_ok(['Mombasa has lovely beaches. Did you swim there?'])
    p = mk(br, h); enter(p); wait_free(p)
    p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'seq',steps:[{t:'I went to Mombasa',f:1,at:60}],end:150},{k:'seq',steps:[{t:'with my friend',f:1,at:100}],end:250},{k:'hang'})}")
    accept(p, sil=0); p.evaluate("()=>{__T.FT.silenceMs=1500}")
    p.evaluate("""()=>{window.__samp=[];setInterval(function(){var m=document.querySelector('.ftbox .row .btn'),hb=document.querySelector('.ftheard');if(m&&hb)window.__samp.push({c:m.className,h:hb.textContent,mode:window.getComputedStyle(m).animationName})},25)}""")
    p.wait_for_function("()=>window.__srStarts>=8", timeout=15000)
    p.wait_for_function("()=>(document.querySelector('.ftheard')||{}).textContent==='I went to Mombasa with my friend'", timeout=8000)
    smp = p.evaluate("()=>window.__samp.slice()")
    i0 = next(i for i, x in enumerate(smp) if x['h'] == 'I went to Mombasa')
    i1 = next(i for i, x in enumerate(smp) if x['h'] == 'I went to Mombasa with my friend')
    after = smp[i0:i1 + 1]   # 最初の言葉が出てから、全文が出るまで(再開をまたぐ間)
    chk('9e1 セッションが2回切れても自動で再開した(認識の開始が増えた)。蓄積は続き、全文が heard 欄に出る', p.evaluate("()=>window.__srStarts") >= 8 and after[-1]['h'] == 'I went to Mombasa with my friend', p.evaluate("()=>window.__srStarts"))
    chk('9e2 再開のたびに heard 欄が空・「…」に戻らない(最初の言葉が出てから、全文が出るまで、表示は途切れない)', all(x['h'] and x['h'] != '…' and x['h'].startswith('I went to Mombasa') for x in after), [x['h'] for x in after if not x['h'].startswith('I went')][:3])
    chk('9e3 🎤の脈打ち(ftlisten・アニメーション ftpulse)が、再開をまたいで途切れない', all('ftlisten' in x['c'] and x['mode'] == 'ftpulse' for x in after), [x['c'] for x in after if 'ftlisten' not in x['c']][:2])
    p.wait_for_timeout(2300)
    chk('9e4 そのあと沈黙が続くと、全文が1回だけ送られる(再開で言葉がなくなったり重複したりしない)', len(box['reqs']) == 1 and box['reqs'][0]['messages'][-1]['content'] == 'I went to Mombasa with my friend', box['reqs'][:1])
    close(p)

    # 9f: 状態表示 — 聞き取り中は🎤が脈打つ。先生の考え中(/chat 待ち)は🎤の脈打ちが止まり、先生の吹き出しに「…」。先生が話す間も脈打たない。画面に日本語なし
    h, box = chat_hang()
    p = mk(br, h); enter(p); wait_free(p)
    p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'say',t:'I like tea'},{k:'hang'})}")
    p.evaluate("()=>{window.__sayMs=900}")
    accept(p); st = {}
    p.wait_for_function("()=>document.querySelector('.ftbox')", timeout=10000)
    st['say'] = p.evaluate("()=>document.querySelector('.ftbox .row .btn').className")   # 先生の最初の一言を話している最中
    p.wait_for_function("()=>document.querySelector('.ftheard.live')&&document.querySelector('.ftbox .row .btn').classList.contains('ftlisten')", timeout=10000)
    st['listen'] = p.evaluate("()=>({c:document.querySelector('.ftbox .row .btn').className,a:getComputedStyle(document.querySelector('.ftbox .row .btn')).animationName})")
    p.wait_for_function("()=>window.__txt.length&&document.getElementById('msgText').textContent==='…'", timeout=10000); p.wait_for_timeout(200)
    st['think'] = p.evaluate("()=>({c:document.querySelector('.ftbox .row .btn').className,m:document.getElementById('msgText').textContent,a:getComputedStyle(document.querySelector('.ftbox .row .btn')).animationName})")
    chk('9f1 聞き取り中: 🎤が脈打つ(ftlisten・アニメーション ftpulse)。先生が話している最中は脈打たない', 'ftlisten' not in st['say'] and 'ftlisten' in st['listen']['c'] and st['listen']['a'] == 'ftpulse', st)
    chk('9f2 先生の考え中(/chat 待ち): 先生の吹き出しに「…」が出て、🎤の脈打ちは止まる', st['think']['m'] == '…' and 'ftlisten' not in st['think']['c'] and st['think']['a'] != 'ftpulse', st['think'])
    T = free_txt(p); allf = ' '.join((t['msg'] or '') + ' ' + t['panel'] + ' ' + t['heard'] for t in T)
    chk('9f3 状態表示に日本語・数字・ラベルを出さない', not JP.search(allf) and not any(w in allf for w in FORBID), allf[-60:])
    close(p)

    # ================= (10) タスク079: fix(直した文)と言い直し =================
    FIX = 'I went to Mombasa yesterday.'
    REP = 'Mombasa has lovely beaches! Did you swim there?'
    REP2 = 'That sounds like a good day. What did you eat?'
    def fixrun(replies, srs, extra=''):
        h, box = chat_ok(replies)
        p = mk(br, h); enter(p); wait_free(p)
        p.evaluate("(a)=>{window.__sr.length=0;a.forEach(function(x){window.__sr.push(x)})}", srs)
        accept(p); return p, box
    def idx(sp, s, start=0):
        try: return sp.index(s, start)
        except ValueError: return -1
    # 10a: fix があると、会話を進めず、先生がお手本を読み上げ(音声＋文字)→本人が言い直す→先生が短く受ける→reply から会話が続く
    p, box = fixrun([{'reply': REP, 'fix': FIX}, REP2],
                    [{'k': 'say', 't': 'I go to Mombasa yesterday'}, {'k': 'say', 't': 'I went to Mombasa yesterday'}, {'k': 'say', 't': 'We ate fish and chips'}, {'k': 'hang'}])
    p.wait_for_function("()=>document.querySelector('.ftfix')&&document.querySelector('.ftfix').textContent!==''", timeout=15000)
    p.wait_for_timeout(200)
    sp = spoken(p); T = free_txt(p)
    fixtxt = p.evaluate("()=>document.querySelector('.ftfix').textContent")
    chk('10a1 fix があると、本人の発言(.ftheard)の下に、直した文だけが出る(ラベル・日本語・数字・「間違い」の言葉なし)', fixtxt == FIX and p.evaluate("()=>document.querySelector('.ftheard').nextElementSibling.className") == 'ftfix' and not JP.search(fixtxt) and not re.search(r'mistake|wrong|error|score|point|correct', fixtxt, re.I), fixtxt)
    chk('10a2 先生がまずお手本(直した文)を読み上げ、reply は先生が言い直しを聞いたあとまで言わない(この時点で reply は読まれていない・画面にもない)', FIX in sp and REP not in sp and not any((t['msg'] or '').startswith('Mombasa has') for t in T), sp[-2:])
    p.wait_for_function("()=>window.__spoken.indexOf(%s)>=0" % json.dumps(REP), timeout=15000)
    sp = spoken(p); i_fix = sp.index(FIX); i_rep = sp.index(REP); mid = sp[i_fix + 1:i_rep]
    chk('10a3 言い直せたら、先生が短く受ける(That\'s it. などの一言)→ そのあと reply から会話が続く。順番: お手本 → 受け → reply', len(mid) == 1 and mid[0] in L['ack'], mid)
    chk('10a4 言い直しの間は /chat を呼ばない(言い直し前は1回だけ)。reply のあとの本人の発言で2回目', len(box['reqs']) >= 1)
    p.wait_for_function("()=>window.__spoken.indexOf(%s)>=0" % json.dumps(REP2), timeout=15000)
    r2 = box['reqs'][1]['messages']
    chk('10a5 履歴: お手本・言い直し・先生の受けの一言は入らない。本人の元の発言 → 先生の reply → 次の発言 の順', [m['role'] for m in r2] == ['assistant', 'user', 'assistant', 'user'] and r2[1]['content'] == 'I go to Mombasa yesterday' and r2[2]['content'] == REP and r2[3]['content'] == 'We ate fish and chips' and not any(FIX in m['content'] or m['content'] in L['ack'] for m in r2), r2)
    chk('10a6 reply を言うときに、お手本の表示は消える(次の会話に残らない)', p.evaluate("()=>document.querySelector('.ftfix').textContent") == '')
    allp = ' '.join((t['msg'] or '') + ' ' + t['panel'] + ' ' + t['heard'] for t in free_txt(p))
    chk('10a7 画面に日本語・「間違い」「テスト」等の言葉・点数が出ない。マイク入力は /chat に言い直しを送っていない', not JP.search(allp) and not any(w in allp for w in FORBID) and not any('I went to Mombasa yesterday' == m['content'] for r in box['reqs'] for m in r['messages'] if m['role'] == 'user'), '')
    close(p)

    # 10b: 言い直しはゆるい一致でよい(完全一致を求めない)。判定の単体
    M = lambda f, s: p0.evaluate("([f,s])=>__T.FT.match(f,s)", [f, s])
    p0 = mk(br); p0.goto(base + '/tour/index.html'); p0.wait_for_timeout(1200)
    cases = [(FIX, 'I went to Mombasa yesterday', True), (FIX, 'i went mombasa yesterday', True), (FIX, 'I went to Mombasa yesterdays', True), (FIX, 'I went to Mombassa yesterday', True),
             (FIX, 'well I went to Mombasa yesterday', True), (FIX, 'I go to Mombasa yesterday', True), (FIX, 'I like pizza', False), (FIX, 'Mombasa', False), (FIX, '', False),
             ('I like tea.', 'I like tea', True), ('I like tea.', 'I like coffee', False), ('She is my friend.', 'She is my friend very much and a lot of other things', False)]
    res = [(f, s, M(f, s), e) for f, s, e in cases]
    close(p0)
    chk('10b ゆるい一致の判定: 大きく違わなければ通る(冠詞抜け・1文字の聞き違い・前置きは可)・まったく別の文・1語だけ・空は通らない', all(r[2] == r[3] for r in res), [r for r in res if r[2] != r[3]])

    # 10c: 2回言い直しても合わなければ、止まらず、先生がもう一度お手本を言って会話を進める。1回目の失敗では「もう一度」の一言
    p, box = fixrun([{'reply': REP, 'fix': FIX}, REP2],
                    [{'k': 'say', 't': 'I go to Mombasa yesterday'}, {'k': 'say', 't': 'I like pizza'}, {'k': 'say', 't': 'banana banana'}, {'k': 'say', 't': 'We ate fish'}, {'k': 'hang'}])
    p.wait_for_function("()=>window.__spoken.indexOf(%s)>=0" % json.dumps(REP), timeout=20000)
    sp = spoken(p); i1 = sp.index(FIX); seq = sp[i1:sp.index(REP) + 1]
    chk('10c 合わないまま2回: お手本 → (1回目の失敗)「もう一度」の一言 → (2回目の失敗)先生がもう一度お手本 → reply。そこで止まらず会話が進む', len(seq) == 4 and seq[1] in L['again'] and seq[2] == FIX and seq[3] == REP, seq)
    p.wait_for_function("()=>window.__spoken.indexOf(%s)>=0" % json.dumps(REP2), timeout=15000)
    chk('10c2 そのあと普通に往復が続く(次の発言が /chat に送られる・言い直しの失敗は履歴に入らない)', len(box['reqs']) == 2 and box['reqs'][1]['messages'][-1]['content'] == 'We ate fish' and not any('pizza' in m['content'] or 'banana' in m['content'] for m in box['reqs'][1]['messages']), box['reqs'][-1:])
    close(p)

    # 10d: 言い直しの最中に声が出ない → 2回目の無音で、止まらずお手本を言って進む(エラー・締めにしない)
    p, box = fixrun([{'reply': REP, 'fix': FIX}, REP2], [{'k': 'say', 't': 'I go to Mombasa yesterday'}, {'k': 'silence'}, {'k': 'silence'}, {'k': 'hang'}])
    p.wait_for_function("()=>window.__spoken.indexOf(%s)>=0" % json.dumps(REP), timeout=20000)
    sp = spoken(p)
    chk('10d 言い直しで声が出ないまま: 「もう一度」→ もう一度お手本 → reply で進む。会話は締めない(場面は続く)', sp[sp.index(FIX) + 1] in L['again'] and sp[sp.index(FIX) + 2] == FIX and view(p) == 'scene' and not errs(p), sp[-5:])
    close(p)

    # 10e: 後方互換 — fix なし(旧形式の {reply} だけ・fix が空・日本語・本人の発言と同じ・短すぎ)は、今までどおりすぐ会話が進む(お手本・言い直しなし)
    for label, rb in [('旧形式(fix の項目なし)', {'reply': REP}), ('fix が空文字', {'reply': REP, 'fix': ''}), ('fix が日本語', {'reply': REP, 'fix': 'こんにちは。'}),
                      ('fix が本人の発言と同じ', {'reply': REP, 'fix': 'I went to Mombasa'}), ('fix が短すぎる', {'reply': REP, 'fix': 'Hi'}), ('fix が文字でない', {'reply': REP, 'fix': 7})]:
        p, box = fixrun([rb], [{'k': 'say', 't': 'I went to Mombasa'}, {'k': 'hang'}])
        p.wait_for_function("()=>window.__spoken.indexOf(%s)>=0" % json.dumps(REP), timeout=15000)
        sp = spoken(p); shown = p.evaluate("()=>document.querySelector('.ftfix').textContent")
        chk('10e %s: お手本・言い直しは出さず、reply がすぐ読まれる(エラーなし・fix の表示なし)' % label, shown == '' and sp[-1] == REP and len(box['reqs']) == 1 and not errs(p), (shown, sp[-2:]))
        close(p)

    # 10f: 時間切れ・Bye ボタンは、言い直しの最中でも穏やかに終わる
    p, box = fixrun([{'reply': REP, 'fix': FIX}], [{'k': 'say', 't': 'I go to Mombasa yesterday'}, {'k': 'hang'}])
    p.wait_for_function("()=>document.querySelector('.ftfix').textContent!==''&&window.__srStarts>=7", timeout=15000)
    p.evaluate("()=>{window.__now=300000}"); wait_map(p, 30000); sp = spoken(p)
    chk('10f 言い直しの聞き取り中に時間切れ: 先生の締めの台詞のあと場面が終わる(エラーなし・reply は言わない)', any(s in L['time'] for s in sp) and REP not in sp and not errs(p), sp[-2:])
    close(p)

    # 10g: 先生の台詞の同じ文が連続しない(聞き返し・無音の質問は毎回ちがう)。各8種以上
    p = mk(br, chat_ok(['x'])[0]); enter(p); wait_free(p)
    p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'hang'},{k:'hang'})}"); accept(p)
    p.wait_for_function("()=>document.querySelector('.ftheard.live')", timeout=10000)
    out = {}
    for key in ('reask', 'nudge'):
        seqs = p.evaluate("(k)=>{var a=[];for(var i=0;i<200;i++)a.push(__T.FT.fresh(__T.FT.lines[k]));return a}", key)
        out[key] = (len(L[key]), all(seqs[i] != seqs[i + 1] for i in range(len(seqs) - 1)), all(len(set(seqs[i:i + 4])) == 4 for i in range(len(seqs) - 3)), set(seqs) == set(L[key]))
    chk('10g 聞き返し(reask)・無音の質問(nudge)は各8種以上。200回選んでも、連続で同じ文が出ず・直近4つは全部ちがい・8種すべてが使われる', all(v[0] >= 8 and v[1] and v[2] and v[3] for v in out.values()), out)
    close(p)

    # ================= (11) タスク079: 先生の声(男性・低い pitch) =================
    p = mk(br); p.goto(base + '/tour/index.html'); p.wait_for_timeout(1200)
    pit = p.evaluate("()=>{var o={};Object.keys(__T.SP).forEach(function(k){if(__T.SP[k]&&typeof __T.SP[k].pitch==='number')o[k]=__T.SP[k].pitch});return o}")
    others = {k: v for k, v in pit.items() if k != 'eikai_teacher'}
    close(p)
    chk('11a 先生(eikai_teacher)の pitch は %s。ほかの全キャラの最低(%s=%s)より0.1以上低い。ルル(1.35)・キングと聞き分けられ、既存の pitch と衝突しない' % (pit.get('eikai_teacher'), min(others, key=others.get), min(others.values())), pit.get('eikai_teacher') == 0.6 and min(abs(v - pit['eikai_teacher']) for v in others.values()) >= 0.1 and pit['eikai_teacher'] < min(others.values()) - 0.09, pit.get('eikai_teacher'))
    h, box = chat_ok(['Good!'])
    p = mk(br, h); enter(p); wait_free(p)
    p.wait_for_timeout(2600)
    pitches = p.evaluate("()=>window.__pitch.slice()")
    dl = p.evaluate("()=>__T.DLG.nbo_eikaiwa1"); npc = [l['n'] for l in dl['lines'] if l.get('n')]
    sc = [x[1] for x in pitches if x[0] in npc]
    p.evaluate("()=>{window.__sr.length=0;window.__sr.push({k:'hang'})}"); accept(p)
    p.wait_for_function("()=>window.__spoken.indexOf(%s)>=0" % json.dumps(L['open']), timeout=10000)
    ft = [x[1] for x in p.evaluate("()=>window.__pitch.slice()") if x[0] in (L['invite'], L['open'])]
    chk('11b 台本パート(068の5往復の先生の台詞)も自由会話(誘い・最初の一言)も、同じ pitch 0.6 で読まれる(片方だけ変わる不整合なし)', len(sc) >= 5 and set(round(x, 3) for x in sc) == {0.6} and set(round(x, 3) for x in ft) == {0.6}, (sc, ft))
    close(p)

    # ================= (8) 既存の場面・台本パートが変わっていない =================
    p = mk(br); p.goto(base + '/tour/index.html'); p.wait_for_timeout(1500)
    now = p.evaluate("()=>({j:['nbo_java1','nbo_java2','nbo_art1','nbo_bag1','nbo_sim1','nbo_taxi1','nbo_lounge1','nbo_room'].map(function(v){return v+':'+JSON.stringify(__T.DLG[v]||null)}),e:JSON.stringify(__T.DLG.nbo_eikaiwa1.lines),ef:__T.DLG.nbo_eikaiwa1.freetalk||0})")
    ph = mk(br, route=hooked_head); ph.goto(base + '/tour/index.html'); ph.wait_for_timeout(1500)
    old = ph.evaluate("()=>({j:['nbo_java1','nbo_java2','nbo_art1','nbo_bag1','nbo_sim1','nbo_taxi1','nbo_lounge1','nbo_room'].map(function(v){return v+':'+JSON.stringify(__T.DLG[v]||null)}),e:JSON.stringify(__T.DLG.nbo_eikaiwa1.lines)})")
    chk('8b 既存の場面(nbo_java1/2・art1・bag1・sim1・taxi1・lounge1・room)の台本が変更前と同じ(nbo_java=061 は変更なし)', now['j'] == old['j'])
    chk('8c 台本パート(068の5往復)の台詞・カンペが変更前と同じ。自由会話の印(freetalk)は nbo_eikaiwa1 だけにある', now['e'] == old['e'] and now['ef'] == 1 and p.evaluate("()=>Object.keys(__T.DLG).filter(function(k){return __T.DLG[k].freetalk}).join(',')") == 'nbo_eikaiwa1')
    close(p); ph.context.close()
    br.close()
print('\n%s  (NG %d件)' % ('すべて OK' if not bad else '失敗あり', len(bad)))
if bad: print(bad); sys.exit(1)
