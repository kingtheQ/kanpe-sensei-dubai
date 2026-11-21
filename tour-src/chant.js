/* ============================================================
   タイトル(スタート)画面の掛け声チャント(タスク050)。world/(タイトル)と tour/(賢者の広間)の両方にビルドが入れる。チャントの再生はこの1か所だけ。
   - song-chant.mp3(51秒)。音量 0.2。タイトル画面のどこかを最初にタッチしたとき、先頭から鳴らす(自動再生の制限のため、起動直後の無操作では鳴らさない・エラーにもしない)。
   - タイトル画面にいるあいだはループ。すでに鳴っていれば新たに始めない(二重に鳴らない)。
   - 「はじめる」で tour/ へページが変わるため、離れる瞬間の再生位置を sessionStorage(kw-chant。保存データではない・15秒で無効)に置き、
     tour/ の最初に、その続きから鳴らす(先頭に戻さない)。tour/ ではループしない。賢者の広間の最初の会話が始まったら止め、そのあとは再開しない。
   - マイクで聞いているあいだ・タブが見えないあいだ・音オフのあいだは止め、戻ったら続きから(最初の会話が始まる前だけ)。
   - 保存データ(kanpe-tour-save-v1 など)には何も書かない。
   ============================================================ */
var CHANT=(function(){
 var BASE='/*CHANTBASE*/',FILE='song-chant.mp3',VOL=.2,KEY='kw-chant',WIN=15000;
 var st={el:null,ac:null,loop:0,done:0,armed:0,evs:['pointerup','touchend','click','keydown'],hook:null};
 function sndOn(){try{return localStorage.getItem('kd_snd')!=='off'}catch(e){return true}}
 function ios(){try{return /iP(hone|ad|od)/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1)}catch(x){return false}}
 function hook(k){try{if(st.hook&&st.hook[k])st.hook[k]()}catch(x){}}
 function clean(){
  var e=st.el;st.el=null;
  if(e){try{e.onended=null;e.onerror=null;e.pause();e.removeAttribute('src');e.load()}catch(x){}}
  if(st.ac){try{st.ac.close()}catch(x){}st.ac=null}
  if(e)hook('off')}
 /* 鳴らす。すでに鳴っていれば何もしない。必ずユーザー操作の中から呼ぶ(鳴らせなければ、そっと諦める) */
 function start(at,loop,blocked){
  if(st.el||st.done||!sndOn())return false;
  var e=new Audio(BASE+FILE);e.preload='auto';e.loop=!!loop;e.volume=VOL;st.el=e;st.loop=loop?1:0;
  if(at>0){try{e.currentTime=at}catch(x){}}
  /* iPhone / iPad(Safari)は audio.volume が効かないので、Web Audio のゲインを通す */
  if(ios()){try{var C=window.AudioContext||window.webkitAudioContext,ac=new C(),gn=ac.createGain();gn.gain.value=VOL;gn.connect(ac.destination);ac.createMediaElementSource(e).connect(gn);e.volume=1;st.ac=ac;if(ac.resume)ac.resume()}catch(x){}}
  e.onended=function(){if(st.el===e)clean()};
  e.onerror=function(){if(st.el===e)clean()};
  hook('on');
  var p;try{p=e.play()}catch(x){p=null}
  if(p&&p.catch)p.catch(function(){if(st.el===e){clean();if(blocked)blocked()}});
  return true}
 /* 止める。そのあとは再開しない(done) */
 function stop(){st.done=1;unbind();try{sessionStorage.removeItem(KEY)}catch(x){}clean()}
 /* マイクで聞いているあいだ・タブが見えないあいだ・音オフのあいだは止め、戻ったら続きから */
 function sync(){var e=st.el;if(!e)return;
  var hold=(typeof ambDuck!=='undefined'&&ambDuck)||document.hidden||!sndOn();
  if(hold){if(!e.paused){try{e.pause()}catch(x){}}}
  else if(e.paused&&!e.ended){var p;try{p=e.play()}catch(x){}if(p&&p.catch)p.catch(function(){})}}
 document.addEventListener('visibilitychange',sync);
 /* ---- タイトル画面(world/): 最初のタッチで先頭から。ループ ---- */
 function onTouch(){
  if(st.el){unbind();return}
  if(start(0,true,function(){if(st.armed)bind()}))unbind()}
 function bind(){if(st.bound)return;st.bound=1;st.evs.forEach(function(n){document.addEventListener(n,onTouch,true)})}
 function unbind(){if(!st.bound)return;st.bound=0;st.evs.forEach(function(n){document.removeEventListener(n,onTouch,true)})}
 function arm(){st.armed=1;st.done=0;bind()}
 function leave(){st.armed=0;st.done=0;unbind();clean()}      /* タイトルを離れる(続きから・地図へ): 止める */
 /* ページが変わる瞬間(はじめる→tour/)の再生位置を渡す。タイトルで鳴らしているときだけ */
 window.addEventListener('pagehide',function(){var e=st.el;if(e&&st.loop){try{sessionStorage.setItem(KEY,JSON.stringify({t:e.currentTime,at:Date.now()}))}catch(x){}}});
 /* ---- tour/: ページの最初に、続きから。初回(賢者の広間へ行くとき)だけ。ループしない ---- */
 function resume(ok){
  var raw=null,o=null;try{raw=sessionStorage.getItem(KEY);sessionStorage.removeItem(KEY)}catch(x){}
  if(!ok||!raw)return;
  try{o=JSON.parse(raw)}catch(x){return}
  if(!o||typeof o.t!=='number'||typeof o.at!=='number'||!isFinite(o.t)||!isFinite(o.at))return;
  function pos(){return Math.max(0,o.t+(Date.now()-o.at)/1000)}
  if(Date.now()-o.at>WIN||o.at>Date.now()+1000)return;
  if(start(pos(),false,retry))return;
  function retry(){   /* 開いた直後に鳴らせなかったとき: この画面での最初のタッチで、続きから */
   function again(){if(st.done||st.el){off();return}if(start(pos(),false,null))off()}
   function off(){['pointerup','touchend','click','keydown'].forEach(function(n){document.removeEventListener(n,again,true)})}
   ['pointerup','touchend','click','keydown'].forEach(function(n){document.addEventListener(n,again,true)})}
 }
 return {start:start,stop:stop,sync:sync,arm:arm,leave:leave,resume:resume,has:function(){return !!st.el},
  playing:function(){return !!(st.el&&!st.el.paused&&!st.el.ended)},set hook(h){st.hook=h},get hook(){return st.hook}}
})();
window.CHANT=CHANT;
