/* ===== 会話に溶かす分かれ目と、夢(タスク053 / 設計 015 案2＋夢) =====
   1. 分かれ目(forkOpts): 相手の一言に「今日の語」が入り、プレイヤーは▶で英語の返事を2〜3個から選んで声に出す。
      選ぶまでの時間(ms)を裏で測って、語ごとの記録(noteWord)に入れる。日本語の選択肢・○×・点数は出さない。計時は画面に出さない。
      即答の線は WB(fastFrac)の1か所。時間切れ(LIMIT をこえても選ばない)は裏で記録するだけで、物語は止めない。
   2. 夢(dreamStart): 寝る場面(夜の1枚のあと)で、持ち越し(save.missed)の語が上位5語まで夢の会話に出る。3択にしない。
      自然に通じたら(発音が7割以上で、その語が言えていたら)持ち越しから外れる。通じなかった語は残す(会話は止めない)。 */
var DREAMBANK=DREAMBANK_JSON,DREAMFB=DREAMFB_JSON;
function forkWord(S,w){var ws=(S&&S.words)||[];for(var i=0;i<ws.length;i++)if(ws[i][0]===w)return ws[i];return [w,'','']}
function forkNote(T,why,ms){var S=G.scene;((T.fork&&T.fork.tw)||[]).forEach(function(w){noteWord(forkWord(S,w),why,ms)})}
function forkOpts(T){
 G.phase='opts';clearPanel();clearInterval(G.typeTimer);msgText.textContent=npcHide()?'':T.npc;var S=G.scene,sid=G.sid;
 var box=el('div','dqbox'),bs=[],t0=performance.now();
 T.opts.forEach(function(o){var b=el('button','dq');b.type='button';b.appendChild(el('span','cur','▶'));b.appendChild(el('span','',cueText(o.y)));
  b.addEventListener('click',function(){forkPick(T,o,performance.now()-t0)});box.appendChild(b);bs.push(b)});
 panel.appendChild(box);
 function sel(i){bs.forEach(function(b,j){b.classList.toggle('sel',j===i)})}
 bs.forEach(function(b,i){['focus','pointerenter','pointerdown'].forEach(function(ev){b.addEventListener(ev,function(){sel(i)})})});
 sel(0);
 /* 制限時間をこえても選ばれなければ、裏で「時間切れ」を記録する(画面には何も出さない・物語は止めない) */
 later(LIMIT,function(){if(G.sid===sid&&G.phase==='opts'&&!T.fk){T.fk=1;forkNote(T,'timeout',LIMIT)}});
 (function rd(i){if(G.sid!==sid||G.phase!=='opts'||i>=T.opts.length)return;sel(i);say(cueText(T.opts[i].y),.9,1,gd(function(){later(300,function(){if(G.phase==='opts')rd(i+1)})}))})(0)}
function forkPick(T,o,ms){
 if(G.phase!=='opts')return;
 if(!T.fk){T.fk=1;forkNote(T,o.ok?(ms<=fastMs()?'fast':(ms<=LIMIT?'slow':'timeout')):'wrong',ms)}
 evPick(T,o)}
/* ---- 夢 ---- */
var DREAMW={'時間切れ':2,'間違い':2,'遅い':1};
function dreamWords(){   /* 持ち越しの上位5語: 重い(間違い・時間切れ)を先に、同じ重さなら新しい順 */
 var idx=(save.missed||[]).map(function(r,i){return {r:r,i:i}});
 idx.sort(function(a,b){return (DREAMW[b.r[3]]||1)-(DREAMW[a.r[3]]||1)||a.i-b.i});
 return idx.slice(0,5).map(function(x){return x.r})}
function dreamLine(r){var b=DREAMBANK[String(r[0]).toLowerCase()];if(b)return b;
 var tk=String(r[0]).split(' ').map(function(x){return '*'+x+'*'}).join(' ');return [DREAMFB[0],DREAMFB[1],tk+'.','']}
function dreamPass(){
 var S=G.scene,T=S&&S.turns&&S.turns[G.ti];if(!(S&&S.d&&S.d.dream&&T&&T.dw))return;
 var ks=String(T.dw).split(' ').map(missKey),a=plogLoad(),last=a[a.length-1],bad=false;
 if(last&&last.v==='dream_1'&&last.ts>=(T.dts||0))(last.miss||[]).forEach(function(m){if(ks.indexOf(m.t)>=0)bad=true});
 if(!bad)noteWord([T.dw,'',''],'dream',0)}
function dreamGiveUp(){   /* 夢は止めない: 2回言えなければ、そのまま先へ(その語は持ち越しに残る) */
 var S=G.scene,T=S&&S.turns&&S.turns[G.ti];if(!(S&&S.d&&S.d.dream&&T&&T.dw)||G.tries<2)return false;
 G.phase='pass';G.tries=0;var m='Never mind. It is only a dream.';setMsg(m,whoNow());spSay=true;
 say(m,.9,S.pitch,gd(function(){spSay=false;later(350,advance)}));return true}
var DREAMED=0;   /* 部屋(nbo_room)で夢を見たあとの夜は、もう一度見ない(1回の眠りに夢は1回) */
function dreamStart(done,fromRoom){
 if(!fromRoom&&DREAMED){DREAMED=0;done();return}
 var ws=dreamWords();if(!ws.length){done();return}
 if(fromRoom)DREAMED=1;
 var lines=[];ws.forEach(function(r){var b=dreamLine(r);lines.push({n:b[0],jp:b[1],dw:r[0]});lines.push({y:b[2],jp:b[3]})});
 DLG.dream_1={who:'達人賢者',story:1,bg:'dream',sp:'dream',hero:'blue',lulu:'plain',nogold:1,inter:[],intro:'Zzz…',lines:lines,
  words:ws.map(function(r){return [r[0],r[1],r[2]]}),ev:1,auto:1,kind:'ev',dream:1};
 var pl={id:'dream',name:'Dream',snd:'dream',tip:['Zzz…',''],v:[]};
 G.evCont=function(){try{done()}finally{if(G.view==='scene'&&G.scene&&G.scene.vid==='dream_1')showMap()}};
 startVid(pl,'dream_1','ev')}
(function(){try{if(typeof TRIP!=='undefined'&&TRIP.hooks)TRIP.hooks.dream=function(done){dreamStart(done)};window.__dreamRoom=function(done){dreamStart(done,1)}}catch(e){}})();
SP.dream={pitch:.8,m:[[trav({}),P(4,{o:'#5a3a8a',p:'#3a2a5a',h:'#d9d4c6'})]]};
BGS.dream=function(){grad(0,98,'#1b1646','#4a3a8a',16);
 for(var i=0;i<30;i++){var sx=(i*53)%320,sy=(i*31)%70;if((Math.floor(t*2)+i)%6)R('#ffe9a8',sx,sy,2,2);else R('#fff',sx,sy,1,1)}
 for(var dy=0;dy<22;dy++){var w=Math.floor(Math.sqrt(121-(dy-11)*(dy-11)));R('#fff3c0',212-w,10+dy,w*2,1)}
 for(dy=0;dy<22;dy++){w=Math.floor(Math.sqrt(100-(dy-10)*(dy-10)));R('#2c2563',216-w,9+dy,w*2,1)}
 R('#6a5aa8',20,58,70,10);R('#8a7ac8',34,52,44,8);R('#6a5aa8',200,66,86,10);R('#8a7ac8',214,60,52,8);
 R('#d9d2f0',0,98,VW,52);for(var x=0;x<VW;x+=22)R('#c7bee6',x+((x/22)%2)*8,104+((x/22)%3)*12,16,3);R('#bdb2e0',0,98,VW,2);
 for(i=0;i<7;i++){var by=96-((t*12+i*23)%70),bx=24+i*42+Math.sin(t+i)*6;c.globalAlpha=.5;R('#e8e2ff',bx,by,5,5);R('#fff',bx+1,by+1,2,2);c.globalAlpha=1}
 R('#9a8ad0',120,96,80,6);R('#7a6ab0',124,102,6,14);R('#7a6ab0',190,102,6,14);R('#fff',150,88,10,8);R('#caa06a',152,90,6,4)};
