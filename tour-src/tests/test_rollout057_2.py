# -*- coding: utf-8 -*-
"""タスク057 第2弾(羽田の出発11場面を新しい会話の流れ=061 flow2 へ)の確認。使い方: python3 tour-src/tests/test_rollout057_2.py
静的(生成物の台本): 11場面すべて conv=1・flow2=1・カードの1ターンだけ(ほかは固定文)・5往復(10行)のまま・単語5語のまま・日本語の単語カード2〜3枚・fork が付く・ターンの順番は元のまま(相手の台詞の頭を元の台本と照合)
  keep='hnd1' が hnd_gate_ow / hnd_gate_star に残り、ほかの羽田の場面には付かない。hnd_return は keep なし・分かれ目(カード)は1か所だけ。ow/star の出し分け(PBY の tkv)・hreturn の結びは不変
動作(ヘッドレス。声と音声認識は偽物): 11場面×カードの全部の選び方
  カード(日本語の単語)は1場面に1回だけ → 見本の英語が音声だけ(文字なし) → カンペ(文字) → 声に出す → 相手の反応(rep) → マップへ戻る(save.seen +1)
  英語の選択肢(▶の枠)・Word Battle・Meaning!・おてほんボタン・発音の数値は出ない / 反応時間の記録(forkNote→noteWord)は061と同じ経路 / 両ゲート場面を終えると save.keep.hnd1 が立つ
  失敗: 自動おてほん→言い直し、3回目の失敗でルルが代わりに言って物語が進む(074) / 3モード(カンペ・耳学＆カンペ・耳学)
マイク・実機の音・見え方は確認できない(音声認識と声は偽物)。"""
import os, sys, json, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
SCN = """hnd_checkin_ow hnd_checkin_star hnd_sec hnd_exit hnd_gate_ow hnd_gate_star hnd_board_ow hnd_board_star hnd_plane_ow hnd_plane_star hnd_return""".split()
FIRST = """sage_1 sage_2 sage_3 nbo_immig1 nbo_immig2 nbo_bag1 nbo_bag2 nbo_sim1 nbo_sim2 nbo_taxi1 nbo_taxi2
nbo_java2 nbo_art1 nbo_art2 nbo_lounge1 nbo_lounge2 nbo_duty1 nbo_duty2 nbo_safari nbo_market
nbo_checkin1 nbo_checkin2 nbo_sec1 nbo_sec2 nbo_gate1 nbo_gate2 nbo_plane1 nbo_plane2""".split()   # 第1弾(test_rollout057_1.py)
NPC_OLD = {"hnd_checkin_ow": ["Good evening. Welcome to", "Passports, please. Do yo", "Please put it on the sca", "Yes, a window seat. Your", "About forty minutes befo"], "hnd_checkin_star": ["Good evening. Welcome to", "Passports, please. Do yo", "Please put it on the sca", "Yes, a window seat. Your", "About forty minutes befo"], "hnd_sec": ["Next, please. Please put", "Yes, please. Put it in a", "Jackets off, please. Do ", "That is fine. Please wal", "Yes, all clear. Thank yo"], "hnd_exit": ["Passport and boarding pa", "Thank you. Where are you", "Nairobi, nice. Is this a", "Wonderful. Please look a", "Perfect. All done. Enjoy"], "hnd_gate_ow": ["Good evening. Is this yo", "Yes, this is Gate 141. B", "Of course. Please sit on", "Yes, it is a late flight", "Good idea. I will call y"], "hnd_gate_star": ["Good evening. Is this yo", "Yes, this is Gate 141. B", "Of course. Please sit on", "Yes, it is a late flight", "Good idea. I will call y"], "hnd_board_ow": ["Attention, please. Fligh", "May I see your boarding ", "Thank you. Please go dow", "It is a long flight. Ple", "My pleasure. Have a safe"], "hnd_board_star": ["Attention, please. Fligh", "May I see your boarding ", "Thank you. Please go dow", "It is a long flight. Ple", "My pleasure. Have a safe"], "hnd_plane_ow": ["Good evening. Welcome ab", "Thank you. Your seat is ", "In the overhead bin. Let", "Of course. It is a night", "Good night. Sleep well. "], "hnd_plane_star": ["Good evening. Welcome ab", "Thank you. Your seat is ", "In the overhead bin. Let", "Of course. It is a night", "Good night. Sleep well. "], "hnd_return": ["Excuse me, I am sorry to", "It is a wooden airplane ", "Please, may I see it? I ", "It is the same one! It t", "Welcome home, travelers."]}   # 元の台本の相手の台詞の頭24字(順番の照合用)
CARD_AT = {'hnd_return': 3}   # カードにしたターン(0始まり)。ほかの10場面は 2
ADJ = {}   # カードの直後の相手の一言を最小限だけ整えた6か所(どのカードでも筋が通るよう、rep と重なる頭の「Yes, a window seat.」「Yes,」「Of course.」を外した)
for _s in ('hnd_checkin_ow', 'hnd_checkin_star'): ADJ[(_s, 3)] = 'Your flight leaves late '
for _s in ('hnd_gate_ow', 'hnd_gate_star'): ADJ[(_s, 3)] = 'It is a late flight. Mos'
for _s in ('hnd_plane_ow', 'hnd_plane_star'): ADJ[(_s, 3)] = 'It is a night flight, so'
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
bad = []; ERR = []
def chk(name, ok, val=''):
    print(('OK  ' if ok else 'NG  ') + name, val if val != '' else '')
    if not ok: bad.append(name)
JP = re.compile(r"[぀-ヿ㐀-鿿]")
assert len(SCN) == 11 and len(set(SCN)) == 11
# ---------------- 静的 ----------------
html = open(os.path.join(ROOT, 'tour/index.html'), encoding='utf-8').read()
m = re.search(r"var DLG=(\{.*?\});\n", html, re.S) or re.search(r"DLG\s*=\s*(\{.*?\});\s*\n", html, re.S)
def dlg_of(vid):
    i = html.index('"%s":{"who"' % vid) if ('"%s":{"who"' % vid) in html else html.index("%s:{who" % vid)
    return i
import subprocess
j = subprocess.run([sys.executable, '-I', '-c', """
import sys, json; sys.path.insert(0, %r); sys.argv=['x']
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    import runpy
    g = runpy.run_path(%r)
print(json.dumps(g['dl'], ensure_ascii=False))
""" % (os.path.join(ROOT, 'tour-src'), os.path.join(ROOT, 'tour-src/build.py'))], capture_output=True, text=True, cwd=ROOT)
dl = json.loads(j.stdout.strip().split('\n')[-1])
cnt_flow2 = sorted(k for k, v in dl.items() if v.get('flow2') and not k.startswith(('ath_', 'rom_', 'fra_', 'rvn_')))   # アテネ(090・091)・ローマ(094)・フランクフルト(097)・ロヴァニエミ(095=057第4弾。test_rollout057_4.py)は新形式の別の弾

DOH3 = ['doh_immig1','doh_immig2','doh_bag1','doh_bag2','doh_sim1','doh_sim2','doh_taxi','doh_metro','doh_city_t1','doh_city_t2','doh_city_t3','doh_city_h1','doh_city_h2','doh_city_h3','doh_city_h4','doh_city_s1','doh_city_s2','doh_city_s3','doh_city_r1','doh_city_r2','doh_city_r3','doh_city_c1','doh_city_c2','doh_city_c3','doh_dep_checkin','doh_dep_passport','doh_dep_bear','doh_dep_train','doh_dep_orchard','doh_dep_lounge','doh_dep_gate','doh_dep_plane']   # タスク092(第3弾)
chk('S0 flow2 の場面は nbo_java1 + 第1弾28 + 第2弾11 + 第3弾のドーハ32 = 72(イベントには付いていない。ロヴァニエミ30場面は第4弾=095でこの一覧の外)', cnt_flow2 == sorted(SCN + FIRST + ['nbo_java1'] + DOH3), len(cnt_flow2))
for sid in SCN:
    d_ = dl[sid]; L = d_['lines']; cards = [i for i, l in enumerate(L) if l.get('cards')]
    opts = L[cards[0]]['opts'] if cards else []
    ok = (d_.get('conv') == 1 and d_.get('flow2') == 1 and len(L) == 10 and len(cards) == 1 and len(d_['words']) == 5 and 2 <= len(opts) <= 3
          and all(JP.search(o['card']) for o in opts) and L[cards[0]].get('fork', {}).get('tw')
          and not any(l.get('opts') for i, l in enumerate(L) if i != cards[0]))
    chk('S1 %s: conv=1・flow2=1・5往復(10行)・カードは1ターンだけ(%d番目)・カード%d枚・単語5語・fork あり' % (sid, cards[0] // 2 if cards else -1, len(opts)), ok, [o['card'] for o in opts])
    tw = L[cards[0]]['fork']['tw'][0]
    chk('S2 %s: fork の語(%s)は場面の単語5語の中にある' % (sid, tw), tw in [w['w'] if isinstance(w, dict) else w[0] for w in d_['words']], d_['words'][:2])
# 既存フラグが残る
chk('S3 keep: hnd_gate_ow・hnd_gate_star は keep=hnd1(秘密イベントの下地。hnd_return の出現条件)を維持。ほかの羽田の10場面には keep が付いていない(新しい拾い物を作らない)', dl['hnd_gate_ow'].get('keep') == 'hnd1' and dl['hnd_gate_star'].get('keep') == 'hnd1' and not any(dl[k].get('keep') for k in SCN if k not in ('hnd_gate_ow', 'hnd_gate_star')), [(k, dl[k].get('keep')) for k in SCN if dl[k].get('keep')])
for sid in SCN:
    npcs = [l['n'][:24] for l in dl[sid]['lines'] if 'n' in l]
    ci_ = CARD_AT.get(sid, 2); cl = [i for i, l in enumerate(dl[sid]['lines']) if l.get('cards')]
    chk('S3b %s: ターンの数(5)と相手の台詞の順番が元の台本のまま(整えた6か所を除く)・カードは %d 番目のターン(0始まり)' % (sid, ci_), len(npcs) == 5 and npcs == [ADJ.get((sid, i), h) for i, h in enumerate(NPC_OLD[sid])] and cl == [2 * ci_ + 1], (npcs, cl))
    chk('S3c %s: 場面の既存の属性(who・bg・sp・intro)が残っている' % sid, bool(dl[sid]['who']) and bool(dl[sid]['bg']) and bool(dl[sid]['sp']) and bool(dl[sid]['intro']))
chk('S3d hnd_return: 分かれ目(カード)は1か所だけ・木の飛行機の側は固定文(opts なし)・rep つき・keep なし', bool(dl['hnd_return']['lines'][3].get('rep')) and not dl['hnd_return']['lines'][3].get('opts') and bool(dl['hnd_return']['lines'][7].get('cards')) and dl['hnd_return'].get('keep') is None, dl['hnd_return']['lines'][3].get('rep'))
import event_data, doha_data
chk('S3e VARIANTS(持ち越しの差しかえ)が参照する場面は羽田にない・参照が壊れていない(build.py の assert が通っている)', not any(v[0].startswith('hnd_') for v in event_data.VARIANTS + doha_data.VARIANTS) and all(v[0] in dl and 'n' in dl[v[0]]['lines'][2 * v[1]] for v in event_data.VARIANTS + doha_data.VARIANTS))
chk('S4 窓口・ドーハのイベント・羽田のイベント・ナイロビのイベントの場面は変えていない(ロヴァニエミは第4弾=095で変えた。test_rollout057_4.py)(flow2 なし)', not any(dl[k].get('flow2') for k in dl if k.startswith(('win_', 'ticket_', 'doh_ev_', 'hnd_ev_', 'nbo_ev_', 'nbo_eikaiwa'))))
# ---------------- 動作 ----------------
HOOK = "requestAnimationFrame(frame);\n})();"
def hooked(route):
    r = route.fetch(); body = r.text(); assert HOOK in body
    hk = "window.__T={G:G,save:save,startVid:startVid,PBY:PBY,DLG:DLG,PREF:PREF,get PAYFX(){return typeof PAYFX!=='undefined'?PAYFX:null}};"
    route.fulfill(response=r, body=body.replace(HOOK, hk + HOOK, 1))
INITM = INIT + """
window.__sp=[];window.__srn=0;window.__bad=0;window.__nomic=0;
(function(){var o=speechSynthesis.speak;speechSynthesis.speak=function(u){try{window.__sp.push({t:u.text,r:u.rate,ph:(window.__T&&__T.G.phase)||null,cue:!!document.querySelector('#panel .cue'),pan:(document.getElementById('panel')||{}).innerText||'',who:(document.getElementById('who')||{}).textContent||''})}catch(e){}o.call(speechSynthesis,u)};
 function FS(){}FS.prototype.start=function(){var me=this;window.__srn++;if(window.__nomic)return;setTimeout(function(){var T=window.__T&&__T.G.scene&&__T.G.scene.turns[__T.G.ti];var t=T&&T.cue?T.cue.replace(/\\*/g,''):'';
  if(window.__bad>0){window.__bad--;t='blah blah blah'}
  var rs=[{transcript:t,confidence:.9}];rs.isFinal=true;if(me.onresult)me.onresult({results:[rs]});setTimeout(function(){if(me.onend)me.onend({})},20)},60)};
 FS.prototype.abort=FS.prototype.stop=function(){};window.SpeechRecognition=FS;window.webkitSpeechRecognition=FS})();
"""
SNAPJS = "function(){var T=window.__T;return {view:T.G.view,seen:T.save.seen,sp:window.__sp,ph:window.__ph,cs:window.__cs,btn:Array.from(window.__btn),pan:window.__pan,msg:window.__msg,lb:window.__lb,dq:window.__dq,wrec:T.save.wrec,missed:T.save.missed,help:T.save.help,h0:window.__h0,srn:window.__srn,keep:T.save.keep||null}}"
POLL = ("window.__snap=" + SNAPJS + ";window.addEventListener('beforeunload',function(){try{var o=window.__snap();o.view='nav';sessionStorage.setItem('__mir',JSON.stringify(o))}catch(e){}});"
        "window.__ph=[];window.__pan=[];window.__btn=new Set();window.__cs=0;window.__msg=[];window.__lb=[];window.__dq=0;"
        "new MutationObserver(function(ms){ms.forEach(function(m){[].forEach.call(m.addedNodes,function(n){if(n.nodeType===1&&(n.classList.contains('jcards')||(n.querySelector&&n.querySelector('.jcards'))))window.__cs++})})}).observe(document.getElementById('panel'),{childList:true,subtree:true});"
        "setInterval(function(){try{var T=window.__T;if(!T)return;var ph=T.G.phase;var a=window.__ph;if(a[a.length-1]!==ph)a.push(ph);"
        "var p=document.getElementById('panel');var tx=p?p.innerText.replace(/\\s+/g,' '):'';window.__pan.push(ph+'|'+tx);"
        "[].forEach.call(document.querySelectorAll('#panel button'),function(b){window.__btn.add(b.textContent.trim())});"
        "if(document.querySelector('#panel .dq'))window.__dq++;"
        "if(!window.__lb.length){var l=[].map.call(document.querySelectorAll('.jcard .lb'),function(x){return x.textContent});if(l.length)window.__lb=l}"
        "var m=document.getElementById('msgText');if(m)window.__msg.push(m.textContent)}catch(e){}},40)")
LEGS = [('HND', 'DOH'), ('DOH', 'NBO'), ('NBO', 'DOH'), ('DOH', 'HEL'), ('HEL', 'RVN'), ('RVN', 'MAD'), ('MAD', 'LIM'), ('LIM', 'CUZ'), ('CUZ', 'LIM'), ('LIM', 'MIA'), ('MIA', 'DFW'), ('DFW', 'HNL'), ('HNL', 'HND')]
def tseed():
    return {'v': 1, 'trip': 1, 'tk': 'ow', 'td': 6, 'day': 6, 'ph': 'day', 'bun': 1,
            'legs': [{'i': i, 'fr': a, 'to': b, 'd': None, 'f': 1 if i < 2 else 0, 'l': 1 if i < 2 else 0} for i, (a, b) in enumerate(LEGS)],
            'days': [], 'cur': {'led': [], 'pick': []}}
def newctx_(br, mode=0):
    ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INITM)
    ctx.add_init_script("localStorage.setItem('kanpe-tour-save-v1',%s);localStorage.setItem('kanpe-trip-v1',%s);" % (json.dumps(json.dumps({'seen': {}, 'ticket': 'ow'})), json.dumps(json.dumps(tseed()))))
    ctx.add_init_script("try{if(!sessionStorage.getItem('__pf')){sessionStorage.setItem('__pf','1');localStorage.setItem('kd_prefs_v1',%s)}}catch(e){}" % json.dumps(json.dumps({'mode': mode})))
    return ctx
def newpage(ctx, base):
    q = ctx.new_page(); q.on('pageerror', lambda e: ERR.append(str(e)[:160]))
    q.route('**/tour/index.html*', hooked); q.goto(base + '/tour/index.html?ev=off'); q.wait_for_timeout(1500); q.evaluate(POLL)
    return q
def reset(q):
    q.evaluate("()=>{var T=__T;T.save.missed=[];T.save.wrec={};T.save.seen={};T.save.keep={};window.__sp.length=0;window.__ph.length=0;window.__pan.length=0;window.__btn.clear();window.__cs=0;window.__srn=0;window.__msg.length=0;window.__lb=[];window.__dq=0;window.__bad=0;window.__nomic=0;window.__h0=T.save.help}")
def run(q, vid, pick, wait_tap=150, bad_after=0, maxit=700):
    """場面を始め、カードの画面が出たら wait_tap ミリ秒おいて pick 番目を押し、マップへ戻るまで進める"""
    reset(q)
    q.evaluate("(v)=>{var T=__T,pl=null;for(var k in T.PBY){var p=T.PBY[k];if(p&&p.v&&p.v.indexOf(v)>=0){pl=p;break}}T.startVid(pl,v,null)}", vid)
    q.wait_for_timeout(450); q.click('.btn.go'); tapped = False
    try:
        for i in range(maxit):
            q.wait_for_timeout(50)
            if not tapped and q.evaluate("()=>document.querySelectorAll('.jcard').length"):
                q.wait_for_timeout(wait_tap); q.evaluate("(i)=>document.querySelectorAll('.jcard')[i].click()", pick); tapped = True
                if bad_after: q.evaluate("(n)=>{window.__bad=n}", bad_after)
            if q.evaluate("()=>__T.G.view") == 'map': break
        return q.evaluate("()=>window.__snap()")
    except Exception:   # 乗る飛行機の場面(nbo_plane2)を終えると次の街のページへ移る。移る直前(beforeunload)に控えた状態を読む
        q.wait_for_timeout(1200)
        o = json.loads(q.evaluate("()=>sessionStorage.getItem('__mir')")); o['view'] = 'map' if o['seen'] else o['view']; return o
def strip(s): return s.replace('*', '')
with sync_playwright() as pw:
    srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    br = pw.chromium.launch(args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
    ctx = newctx_(br, 0); q = newpage(ctx, base)
    n_runs = 0
    # ---------- A. 11場面 × カードの全部の選び方 ----------
    for sid in [x for x in SCN if x in os.environ.get('ONLY', '').split(',') or not os.environ.get('ONLY')]:   # ONLY=nbo_plane1,nbo_plane2 のように絞って早く回せる(省略=全11場面)
        L = dl[sid]['lines']; ci = [i for i, l in enumerate(L) if l.get('cards')][0]; T = L[ci]; opts = T['opts']; tw = T['fork']['tw'][0]
        for pk, o in enumerate(opts):
            q.close(); q = newpage(ctx, base)
            r = run(q, sid, pk); n_runs += 1; tag = '%s/%s' % (sid, o['card'])
            ph = r['ph']; sp = r['sp']
            ok_flow = r['view'] == 'map' and r['seen'].get(sid) == 1
            chk('A1 %s: 最後まで通り、マップへ戻る(save.seen=1)' % tag, ok_flow, (r['view'], r['seen']))
            kp = r.get('keep') or {}
            chk('A1b %s: keep=hnd1 の扱い(両ゲート場面を終えると save.keep.hnd1=1 が立つ。ほかの場面では立たない)' % tag, (kp.get('hnd1') == 1) == (sid in ('hnd_gate_ow', 'hnd_gate_star')), kp)
            chk('A2 %s: 日本語カードの画面は1回だけ・カードの文字は台本どおり' % tag, r['cs'] == 1 and r['lb'] == [x['card'] for x in opts], (r['cs'], r['lb']))
            chk('A3 %s: 英語の選択肢(▶の枠)・Word Battle・Meaning!・おてほんボタンは出ない' % tag, r['dq'] == 0 and 'words' not in ph and 'reveal' not in ph and 'おてほん' not in ' '.join(r['btn']), (r['dq'], ph, r['btn']))
            sm = [x for x in sp if x['t'] == strip(o['y'])]
            i_s = ph.index('sample') if 'sample' in ph else -1
            chk('A4 %s: カードを押すと見本の英語が声だけで流れ(画面にカンペの文字なし)、そのあとカンペ(cue)が出る' % tag, bool(sm) and sm[0]['ph'] == 'sample' and not sm[0]['cue'] and strip(o['y']) not in sm[0]['pan'] and i_s >= 0 and 'cue' in ph[i_s:], (sm[:1], ph[:8]))
            chk('A5 %s: 順番は カード(opts)→見本(sample)→カンペ(cue)' % tag, 'opts' in ph and ph.index('opts') < i_s < ph.index('cue', i_s), ph)
            want = (o['then']['rep']['n'] if o.get('then') else (o['rep']['n'] if o.get('rep') else None))
            chk('A6 %s: 相手の反応(rep)が返る' % tag, want is None or any(x['t'] == want for x in sp), want)
            if o.get('then'):
                chk('A6b %s: 知らない現地カードは、まず自分が「What is 〜?」と聞き → 相手の短い説明 → 本線に戻る' % tag, any(x['t'] == o['then']['n'] for x in sp) and any(p_.startswith('cue|') and strip(o['then']['y']) in p_ for p_ in r['pan']), o['then']['n'][:30])
            nums = [p for p in r['pan'] if re.search(r'\d+\s*%|7割|\d+\s*/\s*\d+\s*語|\d+/\d+|Nice|Too ', p)]
            jpm = [m_ for m_ in r['msg'] if JP.search(m_) and m_ != dl[sid]['intro']]   # 場面の導入文(日本語)は従来どおり出る。相手の台詞の日本語訳は出ない
            chk('A7 %s: 発音の数値・判定の文字・日本語の台詞訳は画面に出ない' % tag, not nums and not jpm, (nums[:1], jpm[:1]))
            w = r['wrec'].get(tw) or r['wrec'].get(tw.lower())
            chk('A8 %s: 反応時間の記録(forkNote→noteWord)が語「%s」に残る(すぐ押す=fast)・持ち越しに入らない' % (tag, tw), bool(w) and w.get('o') == 'fast' and not any(m_[0].lower() == tw.lower() for m_ in r['missed']), (w, r['missed'][:1]))
            txt = ' '.join(r['pan'])
            chk('A9 %s: 「復習」「テスト」「点」「ポイント」「スパルタ」は出ない' % tag, not any(x in txt for x in ['復習', 'テスト', '点', 'ポイント', 'スパルタ']))
    chk('A0 通した回数', True, '%d 回(11場面の全カード)' % n_runs)
    # ---------- B. 反応時間(遅い→持ち越し・時間切れ) ----------
    sid = 'hnd_sec'; tw = 'liquids'
    q.close(); q = newpage(ctx, base); r = run(q, sid, 0, wait_tap=3200)
    why = dict((m_[0], m_[3]) for m_ in r['missed'])
    chk('B1 3.2秒かかると「遅い」→ 持ち越し(夢の材料)に入る(hnd_sec の liquids)', why.get(tw) == '遅い' or why.get(tw.lower()) == '遅い' and 3000 < (r['wrec'].get(tw) or r['wrec'].get(tw.lower()))['ms'] < 5000, r['wrec'].get(tw))
    # ---------- C. 失敗ルール(074): 自動おてほん→言い直し、3回目でルルが代わりに言う ----------
    for sid, pk in (('hnd_exit', 0), ('hnd_plane_ow', 1), ('hnd_gate_ow', 1), ('hnd_return', 1)):
        L = dl[sid]['lines']; ci = [i for i, l in enumerate(L) if l.get('cards')][0]; o = L[ci]['opts'][pk]; cue = strip(o['y'])
        q.close(); q = newpage(ctx, base); r = run(q, sid, pk, bad_after=2); sp_t = [x['t'] for x in r['sp']]
        k = sp_t.index('Sorry, one more time?') if 'Sorry, one more time?' in sp_t else -1
        chk('C1 %s: 言えなかったら店員が聞き返し(Sorry, one more time?)→自動で見本(おてほん)が流れ→言い直せる(ボタンなし)' % sid, k >= 0 and sp_t[k + 1] == cue and r['view'] == 'map' and 'おてほん' not in ' '.join(r['btn']), sp_t[:8])
        q.close(); q = newpage(ctx, base); r = run(q, sid, pk, bad_after=3)
        lulu = [x for x in r['sp'] if x['t'] == cue and x['ph'] == 'help']
        chk('C2 %s: 3回目の失敗でルルが代わりに言い、物語が進んで終わる(ヘルプ回数は減らない・数値なし)' % sid, bool(lulu) and r['view'] == 'map' and r['help'] == r['h0'] and not [p for p in r['pan'] if re.search(r'\d+\s*%|7割|\d+/\d+', p)], (len(lulu), r['view']))
    # ---------- D. 3モード(074): 変換した場面から hnd_gate_ow(keep)・hnd_exit・hnd_return・hnd_checkin_star ----------
    def snap(q): return q.evaluate("()=>{var c=document.querySelector('#panel .cue');return {ph:__T.G.phase,msg:document.getElementById('msgText').textContent,cards:[].map.call(document.querySelectorAll('.jcard .lb'),function(x){return x.textContent}),blind:c?c.classList.contains('blind'):null,ctext:c?[].map.call(c.querySelectorAll('.w'),function(x){return x.textContent}).join(' '):null,btns:[].map.call(document.querySelectorAll('#panel button'),function(b){return b.textContent.trim()}),jc:document.querySelectorAll('.jcard').length}}")
    modes = {}
    for sid, pk in (('hnd_gate_ow', 0), ('hnd_exit', 1), ('hnd_return', 1), ('hnd_checkin_star', 1)):
        L = dl[sid]['lines']; ci = [i for i, l in enumerate(L) if l.get('cards')][0]; T = L[ci]; o = T['opts'][pk]; cue = strip(o['y']); npc = L[ci - 0]['n'] if False else L[ci - 1 + 0]['n'] if False else None
        for mode in (0, 1, 2):
            ctx2 = newctx_(br, mode); q2 = newpage(ctx2, base); reset(q2)
            q2.evaluate("(v)=>{var T=__T,pl=null;for(var k in T.PBY){var p=T.PBY[k];if(p&&p.v&&p.v.indexOf(v)>=0){pl=p;break}}T.startVid(pl,v,null)}", sid); q2.wait_for_timeout(450); q2.click('.btn.go')
            for i in range(300):
                q2.wait_for_timeout(50)
                if q2.evaluate("()=>document.querySelectorAll('.jcard').length"): break
            q2.wait_for_timeout(900); a = snap(q2)
            q2.evaluate("(i)=>document.querySelectorAll('.jcard')[i].click()", pk)
            smp = None
            for i in range(200):
                q2.wait_for_timeout(30)
                p_ = q2.evaluate("()=>({ph:__T.G.phase,pan:document.getElementById('panel').innerText})")
                if p_['ph'] == 'sample': smp = p_; break
            for i in range(300):
                q2.wait_for_timeout(50)
                if q2.evaluate("()=>__T.G.phase") == 'cue': break
            q2.wait_for_timeout(1200); b = snap(q2)
            say_cue = q2.evaluate("(c)=>window.__sp.filter(function(x){return x.t===c}).map(function(x){return x.ph})", cue)
            srn = q2.evaluate("()=>window.__srn")
            try:
                for i in range(500):
                    q2.wait_for_timeout(50)
                    if q2.evaluate("()=>__T.G.view") == 'map': break
                end = q2.evaluate("()=>({v:__T.G.view,seen:__T.save.seen})")
            except Exception:   # 場面が終わって次の街のページへ移った(乗る飛行機)。移る直前に控えた状態を読む
                q2.wait_for_timeout(1200); mir = json.loads(q2.evaluate("()=>sessionStorage.getItem('__mir')")); end = {'v': 'map' if mir['seen'] else mir['view'], 'seen': mir['seen']}
            modes[(sid, mode)] = dict(a=a, smp=smp, b=b, say_cue=say_cue, srn=srn, end=end)
            ctx2.close()
        m0, m1, m2 = modes[(sid, 0)], modes[(sid, 1)], modes[(sid, 2)]
        labs = [x['card'] for x in T['opts']]
        chk('D1 %s: 3モードとも、カード(日本語の単語)は同じように出る・英語の選択肢は出ない' % sid, all(modes[(sid, m)]['a']['cards'] == labs for m in (0, 1, 2)), [modes[(sid, m)]['a']['cards'] for m in (0, 1, 2)])
        chk('D2 %s: カンペモード(0)は相手の台詞の文字が出る / 耳学＆カンペ(1)・耳学(2)は相手の台詞の文字が出ない(声だけ)' % sid, m0['a']['msg'] != '' and m1['a']['msg'] == '' and m2['a']['msg'] == '', (m0['a']['msg'][:25], m1['a']['msg'], m2['a']['msg']))
        chk('D3 %s: 全モードで、カードを押した直後の見本は音声だけ(🔊・文字なし)' % sid, all(modes[(sid, m)]['smp'] and '🔊' in modes[(sid, m)]['smp']['pan'] and cue not in modes[(sid, m)]['smp']['pan'] for m in (0, 1, 2)), [modes[(sid, m)]['smp'] for m in (0, 1, 2)])
        chk('D4 %s: カンペ(0)・耳学＆カンペ(1)は、見本のあとカンペ(文字)が出る' % sid, (m0['b']['ctext'] == cue or (o.get('then') and m0['b']['ctext'] == strip(o['then']['y']))) and (m1['b']['ctext'] == cue or (o.get('then') and m1['b']['ctext'] == strip(o['then']['y']))) and not m0['b']['blind'] and not m1['b']['blind'], (m0['b']['ctext'], m1['b']['ctext']))
        chk('D5 %s: 耳学(2)は、見本のあとカンペの文字が出ない(🎤だけ)。見本が自動でもう一度流れて重ならず(見本は1回だけ)、マイクが開く' % sid, m2['b']['blind'] and (m2['b']['ctext'] or '').strip() == '' and m2['say_cue'].count('sample') == 1 and m2['say_cue'].count('cue') == 0 and m2['srn'] >= 1, (m2['b']['blind'], m2['say_cue'], m2['srn']))
        chk('D6 %s: 3モードとも最後まで通る(マップへ戻る・save.seen=1)' % sid, all(modes[(sid, m)]['end']['v'] == 'map' and modes[(sid, m)]['end']['seen'].get(sid) == 1 for m in (0, 1, 2)), [modes[(sid, m)]['end'] for m in (0, 1, 2)])
    # ---------- E. 3モードでの失敗(耳学・カード後) ----------
    ctx2 = newctx_(br, 2); q2 = newpage(ctx2, base); sid = 'hnd_board_star'; L = dl[sid]['lines']; ci = [i for i, l in enumerate(L) if l.get('cards')][0]; cue = strip(L[ci]['opts'][1]['y'])
    r = run(q2, sid, 1, bad_after=3); lulu = [x for x in r['sp'] if x['t'] == cue and x['ph'] == 'help']
    chk('E1 耳学(2)でカードのあとに3回失敗 → ルルが声で代わりに言い(吹き出しは文字なし)、物語が進む', bool(lulu) and r['view'] == 'map' and all(x['pan'].find(cue) < 0 for x in lulu), (len(lulu), r['view']))
    ctx2.close()
    chk('Z ページのエラーなし', not ERR, ERR[:3])
    br.close()
print('\n結果: NG %d 件' % len(bad), bad[:10])
sys.exit(1 if bad else 0)
