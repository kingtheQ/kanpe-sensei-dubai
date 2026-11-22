/* ============================================================
   宣言文ソングの組み込み(タスク049)。ナイロビ(tour/)だけに入る。art.js のあと・エンジンと同じ場所に置かれる。
   - 掛け声チャント版(song-chant.mp3 / 51秒)=タイトル(スタート)画面の曲(タスク050で賢者の広間から移した)。再生は chant.js の1か所だけ(world/ のタイトルで開始・ループ、
     tour/ では続きから)。ここ(song.js)はテーマ曲の再生と、チャントとの背景音の受け渡し・マイク中の一時停止の連動・最初の会話が始まったらチャントを止める呼び出しだけを持つ。
   - メインテーマ(song-theme.mp3 / 1分15秒)=ホテルのロビーの「聴く」イベント(場所 hsong)専用。ほかの場面・タイトル・メニューでは流さない。
     発音の課題・採点・単語バトルはない。曲の途中でも出口ボタンでマップに戻れ、戻ったら止まる。
   - 再生はユーザーの操作(GOボタン・つぎへ)のあとだけ始める(自動再生の制限)。鳴らせなかったときは、曲なしで先へ進める。
   - 保存データ(kanpe-tour-save-v1 など)には何も書かない。再生の状態はこのファイルの変数だけ。
   ============================================================ */
var SONGBASE=ARTBASE.replace(/art\/$/,'song/');
var SONGFILE={theme:'song-theme.mp3'};
var SONGVOL={theme:.65};     /* テーマは聴くのが主役(チャントの音量 0.2 は chant.js) */
var SONGSC=/*SONGDATA*/null;
var ROOMSC=/*ROOMDATA*/null;   /* ホテルの部屋(タスク051) */
var SONG={el:null,key:null,ac:null,gn:null,want:null};
SP.singer={pitch:1.1,m:[[HJ,P(2,{x:'#2d8f8a',o:'#e0b040'})]]};   /* 絵が読めなかったときの、いつものドット */
BGS.nlobby=BGS.lobby;   /* 背景の絵が読めなかったときの、いつものドットのロビー */
/* 曲が鳴っているあいだは、場面の背景の音楽(Snd.go)を止めて重ならないようにする。曲が止まったら、いまの場面の音楽に戻す */
var SONGSNDGO=Snd.go;
Snd.go=function(k){SONG.want=k;return SONGSNDGO.call(Snd,(SONG.el||CHANT.has())?null:k)};
CHANT.hook={on:function(){SONGSNDGO.call(Snd,null)},off:function(){if(!SONG.el)songRestore()}};   /* チャントが鳴っているあいだも背景音を止め、止まったら戻す */
function songRestore(){SONGSNDGO.call(Snd,SONG.want||null)}
function songSndOn(){try{return localStorage.getItem('kd_snd')!=='off'}catch(e){return true}}
function songPlaying(){return !!(SONG.el&&SONG.key==='theme'&&!SONG.el.paused&&!SONG.el.ended)}
function songStop(){
 var e=SONG.el,k=SONG.key;SONG.el=null;SONG.key=null;
 if(e){try{e.onended=null;e.onerror=null;e.pause();e.removeAttribute('src');e.load()}catch(x){}songRestore()}
 if(SONG.ac){try{SONG.ac.close()}catch(x){}SONG.ac=null}
 return k}
/* iPhone / iPad(Safari)は audio.volume が効かない(いつも最大)ので、控えめな音量にするため Web Audio のゲインを通す。通せなければ、そのまま鳴らす */
function songIOS(){try{return /iP(hone|ad|od)/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1)}catch(x){return false}}
/* 曲を鳴らす。必ずユーザー操作(クリック)のなかで呼ぶ。鳴らせない(音オフ・ブロック・読み込み失敗)なら cb('off'|'blocked'|'error') */
function songStart(key,cb){
 songStop();
 if(!songSndOn()){if(cb)cb('off');return false}
 var e=new Audio(SONGBASE+SONGFILE[key]);e.preload='auto';e.loop=false;e.volume=SONGVOL[key];SONG.el=e;SONG.key=key;SONGSNDGO.call(Snd,null);
 if(songIOS()){try{var AC0=window.AudioContext||window.webkitAudioContext,ac=new AC0(),gn=ac.createGain();gn.gain.value=SONGVOL[key];gn.connect(ac.destination);ac.createMediaElementSource(e).connect(gn);e.volume=1;SONG.ac=ac;SONG.gn=gn;if(ac.resume)ac.resume()}catch(x){}}
 e.onended=function(){if(SONG.el!==e)return;var k=SONG.key;SONG.el=null;SONG.key=null;if(SONG.ac){try{SONG.ac.close()}catch(x){}SONG.ac=null}songRestore();if(cb)cb('end',k)};
 e.onerror=function(){if(SONG.el!==e)return;songStop();if(cb)cb('error')};
 var p;try{p=e.play()}catch(x){p=null}
 if(p&&p.catch)p.catch(function(){if(SONG.el===e){songStop();if(cb)cb('blocked')}});
 return true}
/* マイクで聞いているあいだ・タブが見えないあいだ・音オフのあいだは止め、戻ったら続きから */
window.__songSync=function(){CHANT.sync();var e=SONG.el;if(!e)return;
 var hold=(typeof ambDuck!=='undefined'&&ambDuck)||document.hidden||!songSndOn();
 if(hold){if(!e.paused){try{e.pause()}catch(x){}}}
 else if(e.paused&&!e.ended){var p;try{p=e.play()}catch(x){}if(p&&p.catch)p.catch(function(){})}};
document.addEventListener('visibilitychange',function(){window.__songSync()});
/* 場面を離れたら止める: テーマは聴く場面のあいだだけ(チャントは場面の遷移では止めない。最初の会話が始まったら止める) */
function songWatch(){
 if(!SONG.el)return;var S=G.scene,inside;
 inside=G.view==='scene'&&!!S&&!!S.d&&S.d.listen===1;
 if(!inside)songStop()}
window.__songWatch=songWatch;setInterval(songWatch,250);
/* ---- チャントは、最初の会話が始まった(「GO！」でたがいの会話に入る)ときに止める。そのあとは再開しない。始めるのは chant.js だけ(タスク050) ---- */
window.__songGo=function(S){CHANT.stop()};
/* ---- ホテルのロビーの「聴く」イベント ---- */
function songListen(pl){
 var d=SONGSC;
 G.sid++;clearTimers();stopSay();Snd.go(null);resetOUT();
 G.scene={id:pl.id,vid:null,pl:pl,d:d,turns:[],words:[],pitch:1,from:null,anim:null,lastSp:null,tables:null};
 speaker=null;applyCtx({bg:d.bg,who:d.who,sp:d.sp,hero:'blue',lulu:'plain',gold:0});
 cam=0;spX=360;spSay=false;luTalk=false;G.view='scene';G.ti=0;G.tries=0;$m('mapView').hidden=true;$m('sceneView').hidden=false;
 clearPanel();G.phase='listen';setMsgInstant(d.intro,'');$m('tapHint').textContent='';
 var S=G.scene,sid=G.sid;
 var go=el('button','btn go','GO！');go.type='button';panel.appendChild(go);
 go.addEventListener('click',function(){
  if(G.sid!==sid||S.songGo)return;S.songGo=1;
  clearPanel();setMsgInstant('♪','');
  function next(){if(G.sid!==sid||S.songAfter)return;S.songAfter=1;songLine(0)}
  function nextBtn(){if(G.sid!==sid||S.songAfter||panel.querySelector('.songnext'))return;
   var b=el('button','btn sub songnext','つぎへ ▶');b.type='button';panel.appendChild(b);
   b.addEventListener('click',function(){if(G.sid!==sid)return;songStop();next()})}
  var ok=songStart('theme',function(why){
   if(G.sid!==sid)return;
   if(why==='end')next();                        /* 曲が終わった */
   else{nextBtn()}                               /* 音オフ・ブロック・読み込み失敗: 曲なしで先へ進める */
  });
  if(!ok)nextBtn();
  else later(20000,nextBtn);                     /* 十分聴いたら、先へ進めるボタンを出す(曲の途中でも出口ボタンでマップに戻れる) */
  });
 /* 歌手・ルル・キングの短いやりとり。読み上げて表示するだけ(マイクなし・採点なし)。タップで早送りできる */
 function songLine(i){
  var L=d.after[i];
  if(!L){speaker=null;luTalk=false;spSay=false;later(700,function(){showMap()});return}
  clearPanel();G.phase='listen';
  if(L.w==='singer'){speaker=SP.singer;luTalk=false}
  else if(L.w==='lulu'){speaker=null;luTalk=true}
  else{speaker=null;luTalk=false}
  S.pitch=L.w==='lulu'?1.35:(L.w==='singer'?SP.singer.pitch:1);
  setMsgInstant(L.en,L.who);
  var adv=false;function go2(){if(adv||G.sid!==sid)return;adv=true;spSay=false;stopSay();songLine(i+1)}
  var sk=el('button','btn sub','つぎへ ▶');sk.type='button';panel.appendChild(sk);sk.addEventListener('click',go2);
  spSay=true;say(L.en,.9,S.pitch,gd(function(){spSay=false;later(900,go2)}))}}

/* ---- ホテルの部屋(タスク051): 到着の夜、部屋で休む場面 nbo_room。読み上げて表示するだけ(マイク・発音の課題・採点・単語バトルなし)。曲は鳴らさない。
   v が空の場所なので、保存の記録(save.seen)・到着の完了条件・場面の数には何も足さない。タップ(つぎへ)で早送りできる ---- */
BGS.nroom=function(){R('#dccbaa',0,0,VW,98);R('#c4ae8a',0,0,VW,6);R('#0f1630',22,16,70,50);R('#e8dcc4',56,16,3,50);R('#e8dcc4',22,40,70,3);
 R('#99674a',0,98,VW,52);R('#a5623f',100,128,120,16);R('#f4f1e8',130,84,90,16);R('#b3322f',200,88,46,12);R('#2a2c34',224,26,70,36);R('#6a4a30',224,86,84,14)};   /* 背景の絵が読めなかったときの、いつものドットの部屋 */
function roomRest(pl){
 var d=ROOMSC;
 G.sid++;clearTimers();stopSay();Snd.go(null);resetOUT();
 G.scene={id:pl.id,vid:null,pl:pl,d:d,turns:[],words:[],pitch:1,from:null,anim:null,lastSp:null,tables:null};
 speaker=null;applyCtx({bg:d.bg,who:d.who,sp:null,hero:'blue',lulu:'plain',gold:0});
 cam=0;spX=360;spSay=false;luTalk=false;G.view='scene';G.ti=0;G.tries=0;$m('mapView').hidden=true;$m('sceneView').hidden=false;
 clearPanel();G.phase='listen';setMsgInstant(d.intro,'');$m('tapHint').textContent='';
 var S=G.scene,sid=G.sid;
 var go=el('button','btn go','GO！');go.type='button';panel.appendChild(go);
 go.addEventListener('click',function(){if(G.sid!==sid||S.roomGo)return;S.roomGo=1;Snd.go('hotel');roomLine(0)});
 function roomLine(i){
  var L=d.lines[i];
  if(!L){speaker=null;luTalk=false;spSay=false;later(700,function(){showMap()});return}
  clearPanel();G.phase='listen';
  speaker=null;luTalk=(L.w==='lulu');
  S.pitch=L.w==='lulu'?1.35:1;
  setMsgInstant(L.en,L.who);
  var adv=false;function go2(){if(adv||G.sid!==sid)return;adv=true;spSay=false;stopSay();roomLine(i+1)}
  var sk=el('button','btn sub','つぎへ ▶');sk.type='button';panel.appendChild(sk);sk.addEventListener('click',go2);
  spSay=true;say(L.en,.9,S.pitch,gd(function(){spSay=false;later(900,go2)}))}}
