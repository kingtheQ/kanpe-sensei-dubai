# -*- coding: utf-8 -*-
"""タスク032 項目5(020-9): 何もない日の写真(変顔・寝顔・おやつ)。python3 tour-src/tests/test_raw032.py"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flow025'))
from play import *
ERR = []; bad = 0
def chk(name, ok, info=''):
    global bad
    print(('OK ' if ok else 'NG ') + name, info)
    if not ok: bad += 1
if __name__ == '__main__':
    with sync_playwright() as pw:
        srv = serve(ROOT); base = 'http://127.0.0.1:%d' % srv.server_address[1]
        br = pw.chromium.launch(args=['--no-sandbox'])
        ctx = br.new_context(viewport={'width': 390, 'height': 780}); ctx.add_init_script(INIT)
        q = ctx.new_page(); q.on('pageerror', lambda e: ERR.append(str(e)[:160]))
        q.goto(base + '/tour/'); q.wait_for_timeout(1500)
        chk('TRIP.RAWORDER が face,sleep,snack,nap', q.evaluate("()=>TRIP.RAWORDER.join(',')") == 'face,sleep,snack,nap')
        # 3枚とも 320x150 に描け、色が入り、ばらばら(同じ絵でない)
        r = q.evaluate("""()=>{var out={};['face','sleep','snack'].forEach(function(k){var cv=document.createElement('canvas');cv.width=320;cv.height=150;
          TRIP.drawPhoto(cv,{s:'raw',k:k});var d=cv.getContext('2d').getImageData(0,0,320,150).data,set={},bad=0;
          for(var i=0;i<d.length;i+=4){var key=d[i]+','+d[i+1]+','+d[i+2];set[key]=1;
            // 赤と緑の混在チェックはパレット側(ルルの青緑・キングの青)で担保。ここでは色数だけ
          }out[k]=Object.keys(set).length;out[k+'_sum']=Array.prototype.reduce.call(d,function(a,b){return (a+b)%1000003},0)});return out}""")
        print(r)
        chk('3枚とも色が6色以上(空でない)', all(r[k] >= 6 for k in ('face', 'sleep', 'snack')), str(r))
        chk('3枚の画素がそれぞれ違う', len({r['face_sum'], r['sleep_sum'], r['snack_sum']}) == 3)
        for k in ('face', 'sleep', 'snack'):
            q.evaluate("(k)=>{var cv=document.createElement('canvas');cv.id='rawcv';cv.style.cssText='position:fixed;left:10px;top:10px;width:380px;height:178px;z-index:99999;image-rendering:pixelated';document.body.appendChild(cv);TRIP.drawPhoto(cv,{s:'raw',k:k})}", k)
            q.screenshot(path='/tmp/t032_raw_%s.png' % k, clip={"x": 0, "y": 0, "width": 390, "height": 200})
            q.evaluate("()=>document.getElementById('rawcv').remove()")
        # 差し替え: setRaw で関数を換えると その絵になる。壊れた関数なら ドット絵に戻る(落ちない)
        r = q.evaluate("""()=>{TRIP.setRaw('face',function(g){g.fillStyle='#010203';g.fillRect(0,0,320,150)});var cv=document.createElement('canvas');TRIP.drawPhoto(cv,{s:'raw',k:'face'});
          var p=cv.getContext('2d').getImageData(5,5,1,1).data;var a=[p[0],p[1],p[2]];
          TRIP.setRaw('face',function(g){throw new Error('x')});var cv2=document.createElement('canvas');TRIP.drawPhoto(cv2,{s:'raw',k:'face'});return [a,cv2.width]}""")
        chk('setRaw で差し替えできる/壊れても落ちない', r[0] == [1, 2, 3] and r[1] == 320, str(r))
        # 選び方: 何もない日(場面なし)が続くと 変顔→寝顔→おやつ→昼寝 の順。休養日も同じ列に入る
        def seed(days, td, ph):
            return {'v': 1, 'trip': 1, 'tk': 'ow', 'day': td - 1, 'td': td, 'ph': ph, 'bun': 1, 'legs': [], 'days': days, 'cur': {'led': [], 'pick': []}}
        def d(n, ph): return {'d': n, 'td': n, 'ph': ph}
        q2 = ctx.new_page(); q2.add_init_script("localStorage.setItem('kanpe-trip-v1',%s)" % json.dumps(json.dumps(seed([], 3, 'night'))))
        q2.goto(base + '/tour/'); q2.wait_for_timeout(1200)
        pk = q2.evaluate("()=>TRIP.pickRaw?TRIP.pickRaw():null")
        # 公開関数が無ければ 夜を閉じて記録を見る(実フロー)
        t = q2.evaluate("()=>{var o=document.querySelector('.trip-ov');return o?o.innerText.replace(/\\s+/g,' ').slice(0,80):null}")
        print('夜', t)
        q2.wait_for_timeout(1800); q2.evaluate("()=>document.querySelector('.trip-ov').click()"); q2.wait_for_timeout(900)
        s = q2.evaluate("()=>JSON.parse(localStorage.getItem('kanpe-trip-v1'))")
        last = s['days'][-1] if s['days'] else None
        chk('場面のない日を閉じると 記録の写真は 素の瞬間(raw/face)', bool(last) and last['ph'].get('s') == 'raw' and last['ph'].get('k') == 'face', json.dumps(last))
        # 続けて(記録に raw が1つ入った状態から)閉じると 次は sleep
        sd = seed([{'d': 1, 'ph': {'s': 'raw', 'k': 'face', 'f': 0}}], 4, 'night')
        q3 = ctx.new_page(); q3.add_init_script("localStorage.setItem('kanpe-trip-v1',%s)" % json.dumps(json.dumps(sd)))
        q3.goto(base + '/tour/'); q3.wait_for_timeout(1200)
        q3.wait_for_timeout(1800); q3.evaluate("()=>document.querySelector('.trip-ov').click()"); q3.wait_for_timeout(900)
        s = q3.evaluate("()=>JSON.parse(localStorage.getItem('kanpe-trip-v1'))")
        chk('2回目は寝顔(sleep)', s['days'][-1]['ph'].get('k') == 'sleep', json.dumps(s['days'][-1]))
        # 旧い記録(raw のない days)でも 読めて アルバムに描ける
        q3.evaluate("()=>{var cv=document.createElement('canvas');TRIP.drawPhoto(cv,{s:'night',k:'night'})}")
        chk('旧い写真 {s:night,k:night} も描ける(例外なし)', not ERR, str(ERR))
        # 画面に出してはいけない語
        txt = q3.evaluate("()=>document.body.innerText")
        chk('画面に 復習/テスト/測定 が出ない', not any(w in txt for w in ('復習', 'テスト', '測定')))
        chk('ページエラー 0', not ERR, str(ERR))
        br.close()
    print('NG=%d' % bad); sys.exit(1 if bad else 0)
