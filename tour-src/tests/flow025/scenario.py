# -*- coding: utf-8 -*-
"""タスク025 の動作確認(ヘッドレス)。python3 tour-src/tests/flow025/scenario.py
初回(はじめから→賢者→窓口で購入→羽田のマップ→搭乗ゲート→機内→ナイロビ到着)、券なしのゲート、グアム行き、記録消去の導線を通す。マイクは偽の音声認識。実機のマイクは未確認。"""
import os; os.makedirs("/tmp/t025_shots", exist_ok=True)
import sys, json, time
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from play import *
from auto import click_any, BATTLE
base=None
def ev(p,js): return p.evaluate(js)
def mk(pw):
    br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
    ctx=br.new_context(viewport={'width':390,'height':780}); ctx.add_init_script(INIT)
    ctx.add_init_script("try{if(!localStorage.getItem('kanpe-set-v1'))localStorage.setItem('kanpe-set-v1',JSON.stringify({v:1,vmode:'pick'}))}catch(e){}")
    return br,ctx
def play_until(p,secs,cond,stepfn=None):
    t0=time.time()
    while time.time()-t0<secs:
        if cond(p): return True
        if stepfn and stepfn(p): p.wait_for_timeout(400); continue
        click_any_safe(p); p.wait_for_timeout(350)
    return False
def click_any_safe(p):
    try: return click_any(p)
    except Exception as e: return None
R=[]
def rec(k,v): R.append((k,v)); print(k,'=>',v)
with sync_playwright() as pw:
    srv=serve(ROOT); base='http://127.0.0.1:%d'%srv.server_address[1]
    br,ctx=mk(pw); p=ctx.new_page(); errs=[]
    p.on('pageerror',lambda e:errs.append(str(e)[:150]))
    # ===== 初回 =====
    p.goto(base+'/world/'); p.wait_for_timeout(700)
    p.click('#startBtn'); p.click('#cNew'); p.wait_for_timeout(1500)
    rec('1 はじめから→URL',p.url.replace(base,''))
    rec('1 賢者の広間 見出し',ev(p,"()=>(document.querySelector('.mapbar h1')||{}).textContent"))
    # 賢者の会話(sage_1)を最後まで → 広間のメニューで マップに もどる
    def hub_menu(p):
        return ev(p,"()=>{var b=[].slice.call(document.querySelectorAll('button')).filter(function(x){return x.offsetParent&&x.textContent.indexOf('マップに もどる')>=0});return b.length>0}")
    ok=play_until(p,160,hub_menu)
    rec('1 賢者の会話を終えて広間メニューに到達',ok)
    p.screenshot(path='/tmp/t025_shots/f1_hub.png')
    ev(p,"()=>{var b=[].slice.call(document.querySelectorAll('button')).filter(function(x){return x.textContent.indexOf('マップに もどる')>=0});b[0].click()}")
    p.wait_for_timeout(800)
    rec('1 購入前 tour記録 ticket',ev(p,"()=>{var t=JSON.parse(localStorage.getItem('kanpe-tour-save-v1')||'null');return t&&t.ticket||null}"))
    p.screenshot(path='/tmp/t025_shots/f2_map.png')
    ev(p,"()=>document.querySelector('.node[data-id=ticket]').click()")
    p.wait_for_timeout(1500)
    # 窓口フローを最後まで → world に戻る
    t_log=[]
    def left(p): return '/world/' in p.url
    seen=set()
    def lg(p):
        b=tuple(btns(p)); t=ev(p,"()=>(document.getElementById('panel')||{innerText:''}).innerText.replace(/\\n/g,' | ').slice(0,90)")
        k=(b,t)
        if k not in seen: seen.add(k); print('   W',round(time.time()),list(b)[:6],t)
        return False
    ok=play_until(p,420,left,lg)
    rec('2 窓口で購入し終えたあと world へ戻った',ok)
    rec('2 戻り先URL',p.url.replace(base,''))
    p.wait_for_timeout(1200)
    rec('2 tour記録 ticket',ev(p,"()=>{var t=JSON.parse(localStorage.getItem('kanpe-tour-save-v1')||'null');return t&&t.ticket||null}"))
    rec('2 world記録 at',ev(p,"()=>{var w=JSON.parse(localStorage.getItem('kanpe-world-v1')||'null');return w?w.at:null}"))
    rec('2 world画面 現在地',ev(p,"()=>(document.getElementById('curName')||{}).textContent"))
    p.screenshot(path='/tmp/t025_shots/f3_world_after_buy.png')
    # 搭乗ゲート → ナイロビ
    p.click('#mGate'); p.wait_for_timeout(800)
    rec('3 ゲートの選択肢',ev(p,"()=>[].map.call(document.querySelectorAll('#opts .opt'),function(x){return x.textContent.trim()})"))
    p.screenshot(path='/tmp/t025_shots/f4_gate.png')
    ev(p,"()=>{var o=[].slice.call(document.querySelectorAll('#opts .opt'));var t=o.filter(function(x){return x.textContent.indexOf('西へ')>=0})[0];t.click()}")
    p.wait_for_timeout(1500)
    rec('3 機内の文言',ev(p,"()=>[(document.querySelector('#sFlight .note')||{}).textContent,(document.getElementById('flRoute')||{}).textContent]"))
    p.screenshot(path='/tmp/t025_shots/f5_flight.png')
    p.wait_for_url('**/tour/**',timeout=20000); p.wait_for_timeout(2500)
    rec('3 着陸後URL',p.url.replace(base,''))
    rec('3 着陸後 見出し',ev(p,"()=>(document.querySelector('.mapbar h1')||{}).textContent||document.title"))
    rec('3 着陸後 ボタン',btns(p)[:8])
    rec('3 着陸後 world.at',ev(p,"()=>JSON.parse(localStorage.getItem('kanpe-world-v1')).at"))
    p.screenshot(path='/tmp/t025_shots/f6_landing.png')
    rec('errors',errs)
    br.close()
    # ===== 券なしでゲート =====
    br,ctx=mk(pw); p=ctx.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)[:150]))
    p.goto(base+'/world/?map=1'); p.wait_for_timeout(600)
    p.click('#mGate'); p.wait_for_timeout(500)
    ev(p,"()=>{var o=[].slice.call(document.querySelectorAll('#opts .opt'));o.filter(function(x){return x.textContent.indexOf('西へ')>=0})[0].click()}")
    p.wait_for_timeout(700)
    rec('4 券なし: 画面',ev(p,"()=>[document.getElementById('sGate').hidden,[].map.call(document.querySelectorAll('#gSay p'),function(x){return x.textContent}),[].map.call(document.querySelectorAll('#opts .opt'),function(x){return x.textContent.trim()})]"))
    rec('4 券なし: 飛行画面にならない',ev(p,"()=>document.getElementById('sFlight').hidden"))
    p.screenshot(path='/tmp/t025_shots/g1_noticket.png')
    p.click('#opts .opt'); p.wait_for_timeout(1500)
    rec('4 案内ボタンのあとURL',p.url.replace(base,''))
    # グアム行きは従来どおり
    p.goto(base+'/world/?map=1'); p.wait_for_timeout(500); p.click('#mGate'); p.wait_for_timeout(400)
    ev(p,"()=>{var o=[].slice.call(document.querySelectorAll('#opts .opt'));o.filter(function(x){return x.textContent.indexOf('南へ')>=0})[0].click()}")
    p.wait_for_timeout(800)
    rec('4 グアム行き: 飛行画面',ev(p,"()=>!document.getElementById('sFlight').hidden"))
    rec('errors',errs)
    br.close()
    # ===== 記録消去への導線 =====
    br,ctx=mk(pw); p=ctx.new_page(); errs=[]; p.on('pageerror',lambda e:errs.append(str(e)[:150]))
    p.goto(base+'/world/'); p.wait_for_timeout(500)
    ev(p,"()=>{localStorage.setItem('kanpe-world-v1',JSON.stringify({v:1,at:'nairobi',seen:{haneda:1,nairobi:1},cleared:{haneda:1}}));localStorage.setItem('kanpe-tour-save-v1',JSON.stringify({seen:{sage_1:1},ticket:'star',help:5,weak:[],missed:[]}));localStorage.setItem('kanpe-tour-memo-v1','[\"a\"]');localStorage.setItem('kanpe-voice-v1','{\"v\":1}');sessionStorage.setItem('kw-started',String(Date.now()))}")
    p.goto(base+'/world/'); p.wait_for_timeout(700)
    rec('5 30分以内: 最初の画面(マップ)',ev(p,"()=>!document.getElementById('sMap').hidden"))
    p.click('#mTitle'); p.wait_for_timeout(600)
    rec('5 タイトルへ戻った+選択表示',ev(p,"()=>[!document.getElementById('sTitle').hidden,!document.getElementById('cmd').hidden]"))
    p.screenshot(path='/tmp/t025_shots/h1_title.png')
    p.click('#cNew'); p.wait_for_timeout(300)
    rec('5 確認文',ev(p,"()=>document.querySelector('#cmdAsk .ask').textContent"))
    p.click('#cYes'); p.wait_for_timeout(1500)
    rec('5 消去後URL',p.url.replace(base,''))
    rec('5 消えた/残った',ev(p,"()=>({world:localStorage.getItem('kanpe-world-v1'),tour:localStorage.getItem('kanpe-tour-save-v1'),memo:localStorage.getItem('kanpe-tour-memo-v1'),voice:localStorage.getItem('kanpe-voice-v1')})"))
    rec('errors',errs)
    br.close()
