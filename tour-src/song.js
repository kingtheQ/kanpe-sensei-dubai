/* ============================================================
   宣言文ソングの組み込み(タスク049)。ナイロビ(tour/)だけに入る。art.js のあと・エンジンと同じ場所に置かれる。
   - 掛け声チャント版(song-chant.mp3 / 51秒)=オープニング(賢者の広間の最初の会話 sage_1)。再生は、最初のGOを押したあと。音量は控えめ。
     賢者の広間にいるあいだだけ鳴り、広間を離れたら止まる(または自然に終わる)。マイクで聞いているあいだは止まる。会話はふつうに進む。
   - メインテーマ(song-theme.mp3 / 1分15秒)=ホテルのロビーの「聴く」イベント(場所 hsong)専用。ほかの場面・タイトル・メニューでは流さない。
     発音の課題・採点・単語バトルはない。曲の途中でも出口ボタンでマップに戻れ、戻ったら止まる。
   - 再生はユーザーの操作(GOボタン・つぎへ)のあとだけ始める(自動再生の制限)。鳴らせなかったときは、曲なしで先へ進める。
   - 保存データ(kanpe-tour-save-v1 など)には何も書かない。再生の状態はこのファイルの変数だけ。
   ============================================================ */
var SONGBASE=ARTBASE.replace(/art\/$/,'song/');
var SONGFILE={chant:'song-chant.mp3',theme:'song-theme.mp3'};
var SONGVOL={chant:.2,theme:.65};     /* チャントは会話の読み上げ・効果音の邪魔にならない控えめな音量。テーマは聴くのが主役 */
var SONGSC=/*SONGDATA*/null;
var SONG={el:null,key:null,ac:null,gn:null,opened:0,open:0,want:null};
SP.singer={pitch:1.1,m:[[HJ,P(2,{x:'#2d8f8a',o:'#e0b040'})]]};   /* 絵が読めなかったときの、いつものドット */
BGS.nlobby=BGS.lobby;   /* 背景の絵が読めなかったときの、いつものドットのロビー */
/* 曲が鳴っているあいだは、場面の背景の音楽(Snd.go)を止めて重ならないようにする。曲が止まったら、いまの場面の音楽に戻す */
var SONGSNDGO=Snd.go;
Snd.go=function(k){SONG.want=k;return SONGSNDGO.call(Snd,SONG.el?null:k)};
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
window.__songSync=function(){var e=SONG.el;if(!e)return;
 var hold=(typeof ambDuck!=='undefined'&&ambDuck)||document.hidden||!songSndOn();
 if(hold){if(!e.paused){try{e.pause()}catch(x){}}}
 else if(e.paused&&!e.ended){var p;try{p=e.play()}catch(x){}if(p&&p.catch)p.catch(function(){})}};
document.addEventListener('visibilitychange',function(){window.__songSync()});
/* 場面を離れたら止める: チャントは賢者の広間のあいだだけ。テーマは聴く場面のあいだだけ */
function songWatch(){
 if(!SONG.el)return;var S=G.scene,inside;
 if(SONG.key==='chant')inside=G.view==='scene'&&!!S&&!!S.pl&&S.pl.id==='sage';
 else inside=G.view==='scene'&&!!S&&!!S.d&&S.d.listen===1;
 if(!inside)songStop()}
window.__songWatch=songWatch;setInterval(songWatch,250);
/* ---- オープニングのチャント: 賢者の広間の最初の会話(sage_1)の「GO！」を押したあと、1回だけ ---- */
window.__songGo=function(S){
 if(!SONG.open||SONG.opened||!S||S.vid!=='sage_1')return;
 SONG.opened=1;songStart('chant',null)};
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
