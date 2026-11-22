/* ===== CAアナウンス・イベント(タスク048): 自分の声が機内放送になる =====
   流れ: 羽田の機内(hnd_plane_*)の会話のあと → CA場面(hnd_ev_ca_*) → マイクを渡される画面(rec) → 食事のあと、チャイム→自分の声の放送(pre)→ルルの反応(hnd_ev_meal_*)
   声の扱い(必須・絶対):
     1. 声は端末の中だけ。MediaRecorder で録り、IndexedDB(DB名・保存キー kanpe-pa-rec-v1)に置く。ネットワークには一切出さない
        (このファイルに fetch / XMLHttpRequest / sendBeacon / WebSocket / 画像・スクリプトの外部読みこみは無い。再生は端末内の blob: URL)。
     2. 発音を調べる Azure の中継(voice.js)とは別系統。このファイルは voice.js の関数・保存(kanpe-voice-v1 / kanpe-pron-v1)を呼ばない・書かない。
     3. 保持はその便のあいだだけ。食事の場面が終わったとき・羽田の便が終わるとき(ナイロビへ飛ぶ前)・別の便が始まるとき・中断したとき・6時間たったとき に消す。
     4. 何度でも録り直せる(確定の「これでOK」まで、保存はしない)。
     5. マイクが許可されない・MediaRecorder が使えない・「こえを ださない モード」のときは、イベントを静かに飛ばして、通常どおり進む。
   画面に「録音」「テスト」「測定」などの言葉は出さない。 */
(function(){
 var DBN='kanpe-pa-rec-v1',STO='rec',RID='cur',MAXMS=40000,TTL=6*3600*1000;
 var DATA=/*PADATA*/null;   /* {ow:{chunks:[[..]],text:'..'},star:{..}} (pa_data.py) */
 var cur=null,R=null;       /* cur=確定した声 {buf,type,ms,ts} / R=いま録っている途中 */
 function kOf(v){var m=/_(ow|star)$/.exec(String(v||''));return m?m[1]:'ow'}
 /* ---- 端末内の保存(IndexedDB。最善努力。使えなくても、その場のメモリだけで進む) ---- */
 function idb(fn){try{var q=indexedDB.open(DBN,1);q.onupgradeneeded=function(){try{q.result.createObjectStore(STO)}catch(e){}};
  q.onsuccess=function(){var db=q.result;try{fn(db,function(){try{db.close()}catch(e){}})}catch(e){try{db.close()}catch(e2){}}};q.onerror=function(){}}catch(e){}}
 function idbPut(rec){idb(function(db,done){var tx=db.transaction(STO,'readwrite');tx.objectStore(STO).put(rec,RID);tx.oncomplete=tx.onerror=tx.onabort=done})}
 function idbDel(){idb(function(db,done){var tx=db.transaction(STO,'readwrite');tx.objectStore(STO).delete(RID);tx.oncomplete=tx.onerror=tx.onabort=done})}
 function idbGet(cb){var called=false;function once(v){if(!called){called=true;cb(v)}}
  idb(function(db,done){var tx=db.transaction(STO,'readonly'),r=tx.objectStore(STO).get(RID);r.onsuccess=function(){once(r.result||null)};r.onerror=function(){once(null)};tx.oncomplete=tx.onerror=tx.onabort=done});
  setTimeout(function(){once(null)},3000)}
 function fired(n){try{var e=evS();return !!e.fired[n]}catch(x){return false}}
 function discard(){cur=null;abortRec();idbDel()}
 /* 起動: 前のページで残った声があれば、食事の場面が済んでいる・古い(6時間)ときは消す。残すのは「声は録れたが、食事の場面がまだ」のときだけ */
 try{idbGet(function(r){if(!r)return;if(r.buf&&r.ts&&Date.now()-r.ts<TTL&&fired('pa1')&&!fired('pa2'))cur=r;else idbDel()})}catch(e){}
 /* ---- 使えるか ---- */
 function supported(){try{return typeof MediaRecorder!=='undefined'&&!!(navigator.mediaDevices&&navigator.mediaDevices.getUserMedia)&&!PREF.silent}catch(e){return false}}
 function typ(){var L=['audio/mp4','audio/webm;codecs=opus','audio/webm','audio/ogg;codecs=opus'];try{for(var i=0;i<L.length;i++)if(MediaRecorder.isTypeSupported(L[i]))return L[i]}catch(e){}return ''}
 /* ---- 録る(ボタンを押したときだけマイクを開く。録り終えたらすぐ閉じる) ---- */
 function relStream(r){try{if(r&&r.stream)r.stream.getTracks().forEach(function(t){try{t.stop()}catch(e){}})}catch(e){}}
 function abortRec(){var r=R;R=null;if(!r)return;try{r.mr.ondataavailable=null;r.mr.onstop=null;if(r.mr.state!=='inactive')r.mr.stop()}catch(e){}relStream(r)}
 function recStart(cb){
  try{navigator.mediaDevices.getUserMedia({audio:true}).then(function(stream){
   try{var ty=typ(),mr=ty?new MediaRecorder(stream,{mimeType:ty}):new MediaRecorder(stream),r={stream:stream,mr:mr,parts:[],t0:Date.now(),ty:mr.mimeType||ty||'audio/mp4'};
    mr.ondataavailable=function(e){if(e.data&&e.data.size)r.parts.push(e.data)};
    R=r;mr.start();cb(null)}catch(e){relStream({stream:stream});R=null;cb(e||'mr')}
  },function(e){cb(e||'denied')})}catch(e){cb(e||'gum')}}
 function toBuf(blob,cb){try{if(blob.arrayBuffer){blob.arrayBuffer().then(cb,function(){cb(null)});return}}catch(e){}
  try{var fr=new FileReader();fr.onload=function(){cb(fr.result)};fr.onerror=function(){cb(null)};fr.readAsArrayBuffer(blob)}catch(e){cb(null)}}
 function recStop(cb){var r=R;if(!r){cb(null);return}var fin=false;
  function done(){if(fin)return;fin=true;if(R===r)R=null;relStream(r);var blob=new Blob(r.parts,{type:r.ty}),ms=Date.now()-r.t0;
   if(!blob.size){cb(null);return}toBuf(blob,function(buf){cb(buf?{buf:buf,type:r.ty,ms:ms,ts:Date.now()}:null)})}
  r.mr.onstop=done;try{if(r.mr.state!=='inactive')r.mr.stop();else done()}catch(e){done()}
  setTimeout(done,2500)}
 /* ---- マイクを渡される画面。「カンペ」(意味のまとまりごとに区切る)・おてほん・はなす・もういちど・これでOK。done(true=声が決まった / false=飛ばす) ---- */
 function rec(S,done){
  var sid=G.sid,k=kOf(S.vid),D=DATA[k],who0=S.d.who,fin=false,state='idle',tmp=null,card,row,tm=null,wd=null;
  function alive(){return G.sid===sid&&G.view==='scene'&&!fin}
  function crew(t,cb){spSay=true;setMsg(t,who0);say(t,.95,(S.pitch||1.2),gd(function(){spSay=false;if(cb)cb()}))}
  function leave(ok){if(fin)return;fin=true;clearTimeout(tm);clearInterval(wd);try{Snd.duck(0)}catch(e){}if(!ok)discard();done(ok)}
  /* 中断(✕で地図へ・別の場面へ)したら、マイクを閉じて声を消す */
  wd=setInterval(function(){if(!fin&&(G.sid!==sid||G.view!=='scene')){fin=true;clearTimeout(tm);clearInterval(wd);try{Snd.duck(0)}catch(e){}discard()}},400);
  function btn(label,cls,fn){var b=el('button','btn'+(cls?' '+cls:''),label);b.type='button';b.addEventListener('click',fn);row.appendChild(b);return b}
  function show(st){state=st;row.textContent='';
   if(st==='idle'){btn('おてほん','sub',function(){if(!alive())return;stopSay();say(D.text,.8,1,function(){})});btn('🎤 はなす','',start)}
   else if(st==='rec'){var b=btn('■ きいてます…','down',stop);b.style.flex='1 1 100%'}
   else if(st==='review'){btn('もういちど','',function(){if(alive()&&state==='review'){tmp=null;start()}});btn('これでOK','',ok)}}
  function fit(){var ws=[].slice.call(card.querySelectorAll('.pac'));if(!ws.length)return;var f=34;
   function set(){ws.forEach(function(w){w.style.fontSize=f+'px'})}
   function over(){return card.scrollHeight>card.clientHeight+1||card.scrollWidth>card.clientWidth+1}
   set();for(var i=0;i<24&&over()&&f>14;i++){f-=1;set()}}
  function start(){
   if(!alive()||state!=='idle'&&state!=='review')return;state='wait';stopSay();try{Snd.duck(1)}catch(e){}
   recStart(function(err){
    if(!alive()){abortRec();try{Snd.duck(0)}catch(e){}return}
    if(err){try{Snd.duck(0)}catch(e){}abortRec();row.textContent='';crew("No problem. I will do it myself. Thank you!",function(){later(600,function(){leave(false)})});return}
    show('rec');tm=setTimeout(stop,MAXMS)})}
  function stop(){if(!alive()||state!=='rec')return;clearTimeout(tm);state='wait';
   recStop(function(r){try{Snd.duck(0)}catch(e){}if(!alive())return;
    if(!r||r.ms<700){tmp=null;show('idle');return}   /* 短すぎる・取れなかった: 静かに最初の状態へ */
    tmp=r;show('review')})}
  function ok(){if(!alive()||state!=='review'||!tmp)return;state='wait';cur=tmp;tmp=null;idbPut(cur);row.textContent='';
   crew("Perfect! Thank you so much!",function(){later(500,function(){leave(true)})})}
  G.phase='pa';clearPanel();clearInterval(G.typeTimer);spSay=false;$m('tapHint').textContent='';
  setMsgInstant('Here is the microphone. Please read this card.',who0);
  card=el('div','cue pacard');card.appendChild(el('span','lab','カンペ'));
  D.chunks.forEach(function(sn){var line=el('div','pal');sn.forEach(function(c){line.appendChild(el('span','pac',c))});card.appendChild(line)});
  panel.appendChild(card);row=el('div','row cuerow');panel.appendChild(row);show('idle');
  fit();requestAnimationFrame(fit)}
 /* ---- 食事の場面の始まり: チャイム → 自分の声の放送 → go()(ルルの反応へ)。音の設定がオフなら、声は出さず文だけ出して進む。再生できなくても止まらない ---- */
 function pre(S,go){
  var sid=G.sid,D=DATA[kOf(S.vid)],r=cur,fin=false,au=null,url=null,wd=null,snd=paOn();
  function end(){if(fin)return;fin=true;clearInterval(wd);paMark(0);try{if(au)au.pause()}catch(e){}try{if(url)URL.revokeObjectURL(url)}catch(e){}
   if(G.sid===sid)later(600,go)}
  wd=setInterval(function(){if(!fin&&G.sid!==sid){fin=true;clearInterval(wd);try{if(au)au.pause()}catch(e){}try{if(url)URL.revokeObjectURL(url)}catch(e){}paMark(0)}},300);
  G.phase='pa';clearPanel();spSay=false;$m('tapHint').textContent='';
  setMsgInstant(D.text,'Announcement');paMark(1);
  if(snd){try{Snd.fx('pachime')}catch(e){}}
  later(snd?2100:900,function(){
   if(!snd||!r){later(Math.min(D.text.length*26+900,4200),end);return}
   try{url=URL.createObjectURL(new Blob([r.buf],{type:r.type}));au=new Audio(url);au.volume=Math.max(0,Math.min(1,(PREF.voice==null?100:PREF.voice)/100));
    au.onended=end;au.onerror=end;var p=au.play();if(p&&p.catch)p.catch(end);
    setTimeout(end,(r.ms||15000)+3500)}catch(e){end()}})}
 /* ---- 差しこみ口: 羽田の機内の会話が終わったとき(finishScene のあと、ほかの出来事より先)。始めたら true ---- */
 function gate(S,cont){
  try{
   if(!S||!S.pl||S.pl.id!=='hplane'||(S.d&&S.d.ev)||EVQ==='off'||(TRIP.restToday&&TRIP.restToday()))return false;
   var m=/^hnd_plane_(ow|star)$/.exec(S.vid||'');if(!m)return false;var k=m[1],caId='hnd_ev_ca_'+k,mealId='hnd_ev_meal_'+k;
   if(!DLG[caId]||!DLG[mealId]||!DATA[k])return false;
   var e=evS(),f=e.fired;
   function meal(){f.pa2=1;e.streak=0;e.last='ev';storeSave();G.evCont=function(){discard();cont()};startVid(S.pl,mealId,'ev')}
   if(!f.pa1){   /* 最初の長距離便で1回だけ(以後の便・もう一度の旅でも勝手に再発しない) */
    if(!supported())return false;
    f.pa1=1;e.streak=0;e.last='ev';storeSave();
    G.evCont=function(){rec(G.scene,function(ok){if(ok&&cur)meal();else{discard();cont()}})};
    startVid(S.pl,caId,'ev');return true}
   if(!f.pa2&&cur){meal();return true}   /* 声は録れたのに食事の場面の前でページが切れたとき(再読みこみ)の続き */
  }catch(e){}
  return false}
 /* ---- 点検モード(?check=1)専用の入口(タスク062)。通常の出方(gate)は変えない。window.__CHK のときだけ動く ----
     from='ca': CA場面 → マイク画面 → 食事の場面(自分の声) まで通し / from='meal': 食事の場面だけ(声が残っていれば再生)。
     行き先は券(save.ticket)で決まる(oneworld=Doha / Star=Istanbul)。fired.pa1/pa2 は見ず・書かない(何度でも試せる)。
     声は check_shim.js により専用のDB名(chk1:…)に入る。終わりは地図へ戻る */
 function chk(pl,k,from){
  if(!window.__CHK||!pl)return false;
  k=(k==='star')?'star':'ow';var caId='hnd_ev_ca_'+k,mealId='hnd_ev_meal_'+k;
  if(!DLG[caId]||!DLG[mealId]||!DATA[k])return false;
  function back(){showMap()}
  function meal(){G.evCont=function(){discard();back()};startVid(pl,mealId,'ev')}
  if(from==='meal'){meal();return true}
  discard();
  G.evCont=function(){rec(G.scene,function(ok){if(ok&&cur)meal();else{discard();back()}})};
  startVid(pl,caId,'ev');return true}
 window.PA={gate:gate,pre:pre,discard:discard,supported:supported,chk:chk,has:function(){return !!cur}};
})();
