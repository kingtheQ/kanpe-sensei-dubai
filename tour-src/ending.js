/* ===== 世界一周編: 終わりの場面(タスク016) =====
   帰国から1か月後のリビング。アルバムの最後の白いページを、旅の始めの約束(宣言文)をもう一度読んで埋める。
   設計の正本: docs/pm/deliverables/013-ending-scores-design-v1.md (E1〜E6・使えない場合 a〜e・記録 kanpe-voice-v1)。
   プレイ中は点数・判定を出さない原則(004-5)の例外は、この場面の E4(ふたつの声)と E5(音の変化)だけ。
   画面に日本語を足さない(同意の1枚とせっていを除く)。赤と緑は使わない(間違い・遠い単語は青)。 */
var DECL_TEXT=/*DECL*/'';
var END=null;
function endCtx(sp,who){return {bg:'album',who:who,sp:sp,hero:'blue',lulu:'plain',gold:0}}

/* ---------- 絵: リビング・アルバム・写真(ドット絵。グラデーションなし・赤と緑は使わない) ---------- */
function homeRoom(){
 R('#3b2f4a',0,0,VW,98);for(var x=0;x<VW;x+=20)R('#43365a',x,0,2,98);
 R('#2a1f36',0,92,VW,6);R('#6a4a34',0,98,VW,52);for(var y=106;y<150;y+=12)R('#5a3e2a',0,y,VW,1);
 R('#d9cfb0',10,6,48,54);R('#0e1630',14,10,40,46);R('#d9cfb0',33,10,2,46);R('#d9cfb0',14,31,40,2);
 for(var i=0;i<7;i++){if((i*5+Math.floor(t*2+i))%4)R('#fff',[18,24,40,46,20,44,28][i],[14,22,16,24,40,46,36][i],1,1)}
 for(i=0;i<6;i++)R('#ffcf6a',16+i*6,50+(i%2)*2,2,2);
 R('#8a7a60',300,4,2,36);R('#ffd36a',292,40,18,10);R('#fff3c0',296,42,10,4);
 c.globalAlpha=.1;R('#ffd36a',262,28,58,56);c.globalAlpha=1}
function pg(x,y,w,h){R('#cdbf9a',x-1,y-1,w+2,h+2);R('#f6efdc',x,y,w,h)}
function photoDep(x,y,w,h){
 var sk=Math.floor(h*.6);R('#8fd0f0',x,y,w,sk);R('#cdeaf7',x,y+sk,w,h-sk);R('#ffd36a',x+w-Math.floor(w*.2),y+3,Math.max(4,Math.floor(w*.09)),Math.max(4,Math.floor(w*.09)));
 R('#d8dde8',x+3,y+Math.floor(h*.32),Math.floor(w*.5),Math.floor(h*.42));for(var i=0;i<4;i++)R('#6aa0c8',x+6+i*Math.floor(w*.11),y+Math.floor(h*.4),Math.max(2,Math.floor(w*.07)),Math.max(2,Math.floor(h*.1)));
 R('#9a9aa6',x,y+h-Math.floor(h*.16),w,Math.floor(h*.16));
 if(w>60){sp2(BUDDYMAP,BPAL,x+Math.floor(w*.3),y+h-Math.floor(h*.16)-16,2);sp2(HEROMAP,HPAL,x+Math.floor(w*.55),y+h-Math.floor(h*.16)-24,2)}}
function photoHome(x,y,w,h){
 R('#e0b98a',x,y,w,h);R('#c99a6a',x,y+h-Math.floor(h*.2),w,Math.floor(h*.2));
 R('#7a5a3a',x+w-Math.floor(w*.3),y+3,Math.floor(w*.25),Math.floor(h*.45));R('#0e1630',x+w-Math.floor(w*.3)+2,y+5,Math.floor(w*.25)-4,Math.floor(h*.45)-4);
 c.globalAlpha=.25;R('#ffe9a8',x+3,y+3,Math.floor(w*.22),Math.floor(h*.32));c.globalAlpha=1;
 if(w>60){sp2(BUDDYMAP,BPAL,x+Math.floor(w*.22),y+h-Math.floor(h*.2)-16,2);sp2(HEROMAP,HPAL,x+Math.floor(w*.46),y+h-Math.floor(h*.2)-24,2)}}
function polaroid(x,y,w,h,fn,cap,al){
 R('#cfc3a0',x-1,y-1,w+2,h+2);R('#fffdf4',x,y,w,h);
 if(al!=null&&al<1)c.globalAlpha=Math.max(0,al);fn(x+4,y+4,w-8,h-15);c.globalAlpha=1;
 if(cap)T(cap,x+w/2,y+h-6,6.5,'#6a5a3a')}
function corners(x,y,w,h){[[x,y,1,1],[x+w-5,y,-1,1],[x,y+h-5,1,-1],[x+w-5,y+h-5,-1,-1]].forEach(function(q){R('#3a2a1c',q[0],q[1],5,2);R('#3a2a1c',q[0]+(q[2]>0?0:3),q[1],2,5*q[3]>0?5:5)})}
function albumCover(){
 R('#2a1c10',88,6,144,94);R('#6a4428',91,9,138,88);R('#d9a441',96,14,128,1);R('#d9a441',96,91,128,1);R('#d9a441',96,14,1,78);R('#d9a441',223,14,1,78);
 R('#c8452c',204,9,9,88);R('#a83a24',204,9,2,88);
 T('KING & LULU',150,38,11,'#ffd36a');T('WORLD JOURNEY',150,54,8,'#ffd36a');T('✈',150,74,13,'#ffd36a')}
BGS.album=function(ctx,S){
 homeRoom();var E=(S&&S.end)||{view:'one'},v=E.view;
 if(v==='cover'){albumCover();return}
 R('#2a1c10',38,8,244,90);R('#5a3a22',40,10,240,86);pg(46,15,112,76);pg(162,15,112,76);R('#b8a982',158,15,4,76);
 if(v==='one'){
  polaroid(52,19,100,68,photoDep,'Departure');
  R('#fff3b0',172,22,92,58);R('#cdbf80',172,22,92,1);R('#e8d98a',176,19,14,5);R('#e8d98a',246,19,14,5);
  T('PROMISE',218,31,7,'#6a5a3a');for(var i=0;i<6;i++)R('#b9ad82',178,38+i*6,78-(i%3)*10,2)}
 else if(v==='both'){polaroid(52,19,100,68,photoDep,'Departure');polaroid(168,19,100,68,photoHome,'Home')}
 else{ /* blank / develop: ひだりは旅の写真、みぎは まっ白なページ */
  polaroid(50,21,48,40,photoDep,null);polaroid(102,31,48,40,photoHome,null);R('#cfc3a0',60,70,34,1);R('#cfc3a0',110,78,30,1);
  corners(176,22,88,64);
  if(v==='develop'){var dv=Math.max(0,Math.min(1,(t-(E.devT||0))/5));polaroid(172,19,96,68,photoHome,'Home',dv)}}}

/* ---------- 進行 ---------- */
function endSay(who,sp,text,cb){
 applyCtx(endCtx(sp,who));spX=0;G.phase='endsay';
 setMsg(text,who);spSay=true;
 say(text,.92,sp==='lulu'?1.35:1,gd(function(){spSay=false;if(cb)later(750,cb)}))}
function endMicOK(){return !PREF.silent&&(!!SR||voiceAzureOn())}
function endingStart(){
 G.sid++;clearTimers();stopSay();G.camp=null;luHelp=false;resetOUT();speaker=null;spSay=false;
 G.view='scene';$m('mapView').hidden=true;$m('boothView').hidden=true;$m('sceneView').hidden=false;
 END={view:'one',devT:0,mic:true,plan:null,sndRows:null};
 G.scene={id:'end',vid:'end',pl:{id:'end',snd:'home',tip:['']},d:{who:'Lulu',story:0,words:[],lines:[],inter:[]},turns:[],words:[],pitch:1,from:null,anim:null,lastSp:null,tables:null,end:END,ctx:endCtx('lulu','Lulu')};
 applyCtx(G.scene.ctx);clearPanel();setMsgInstant('','');Snd.go('home');
 later(700,e1)}
/* E1: 1ページ目(出発の日の写真と約束の紙)→ ページをめくって、最後の白いページ */
function e1(){
 END.view='one';
 endSay('Lulu','lulu','Page one. The day we promised.',function(){
  Snd.fx('page');END.view='blank';
  endSay('Lulu','lulu','And the last page is still empty.',e2)})}
/* 同意が まだなら ここで一度だけ聞く(中継があるときだけ)。そのあと、宣言文をもう一度読む */
function e2(){
 if(voiceNeedConsent()){applyCtx(endCtx('lulu','Lulu'));setMsgInstant('King, one question first.','Lulu');consentCard(function(){clearPanel();e2b()});return}
 e2b()}
function e2b(){
 var S=G.scene;
 if(!endMicOK()){endLuluReads();return}                              /* d: マイクが使えない */
 S.turns=[{npc:"Read it with me, King. Let's fill it.",npcJp:'',cue:DECL_TEXT,cueJp:'',diag:'decl_end',ctx:endCtx('lulu','Lulu'),pitch:1.35}];
 G.ti=0;G.tries=0;G.azFail=null;
 G.onBlocked=function(){G.onBlocked=null;END.mic=false;G.sid++;clearTimers();stopSay();clearPanel();endLuluReads()};
 npcTurn()}
function endLuluReads(){                                              /* d: ルルが先に読み、キングは最後の一言だけ */
 END.mic=false;clearPanel();
 var card=el('div','vcons');card.appendChild(el('p','',DECL_TEXT));panel.appendChild(card);
 applyCtx(endCtx('lulu','Lulu'));setMsgInstant("I'll read it first. Listen.",'Lulu');spSay=true;
 say(DECL_TEXT,.9,1.35,gd(function(){spSay=false;later(700,function(){clearPanel();e3()})}))}
function endAfterRead(){G.onBlocked=null;clearPanel();e3()}          /* diag.js の diagDone から呼ばれる(合格音・クリア音は鳴らさない) */
/* E3: 現像(白いページに今日の写真がゆっくり現れる)→ キングの最後の一言(採点に入れない) */
function e3(){
 END.view='develop';END.devT=t;
 later(4600,function(){Snd.fx('sparkle')});
 endSay('Lulu','lulu','There. Look how the picture comes up.',function(){
  later(2200,function(){
   endSay('Lulu','lulu',"Now it's a whole album.",function(){
    clearPanel();var b=el('button','btn','We went!');b.type='button';panel.appendChild(b);
    b.addEventListener('click',function(){
     if(b.disabled)return;b.disabled=true;
     applyCtx(endCtx('king','King'));spX=0;setMsg('We went!','King');
     say('We went!',1,1,gd(function(){later(900,function(){clearPanel();e4()})}))})})})})}

/* ---------- 比べるための組み立て(013 第2・4章) ---------- */
function endToks(){return DECL_TEXT.split(' ')}
function endPlan(){
 var tr=voiceTripCur()||{},st=tr.start||null,en=tr.end||null;
 if(!END.mic||!en||!en.heard||!en.heard.trim())return {show:false};                       /* d・何も聞こえなかった: E4・E5 は出さない */
 var three=!!(st&&st.src==='az'&&en.src==='az'&&st.w&&en.w&&st.w.length===en.w.length);   /* 同じ測り方どうしだけ、数字と3段の色で比べる */
 return {show:true,st:st,en:en,cmp:three,one:!st}}
function endCls(M,i,three){
 if(three&&M.w&&M.w[i]){var a=M.w[i][1];return a==null?2:(a>=80?0:(a>=60?1:2))}      /* 近い／おしい／遠い(80・60 は仮の区切り) */
 return M.bits&&M.bits.charAt(i)==='1'?0:2}
function endMarks(st,en,three){
 var c=[],tk=endToks();
 tk.forEach(function(k,i){
  var a=endCls(st,i,three),b=endCls(en,i,three);if(!(b<a))return;
  var d=1;if(three){var sa=st.w[i][1]==null?0:st.w[i][1],sb=en.w[i][1]==null?0:en.w[i][1];d=sb-sa;if(d<5)return}   /* 5点未満の差は「同じ」(仮) */
  c.push({i:i,d:d,k:vnorm(k)})});
 c.sort(function(x,y){return y.d-x.d||x.i-y.i});
 var seen={},out=[];c.forEach(function(x){if(seen[x.k]||out.length>=3)return;seen[x.k]=1;out.push(x.i)});
 return out}
function endTier(label,M,three,nums,marks){
 var box=el('div','ert'),h=el('div','erh');h.appendChild(el('b','',label));
 if(nums)h.appendChild(el('span','enum','Voice '+M.tot+' · Words '+M.acc+' · Flow '+M.flu+' · Finish '+M.cmp));
 box.appendChild(h);var ws=el('div','ewords');
 endToks().forEach(function(k,i){
  var s=el('span','ew c'+endCls(M,i,three),k);
  if(marks&&marks.indexOf(i)>=0)s.appendChild(el('i','',' ✦'));
  ws.appendChild(s);ws.appendChild(document.createTextNode(' '))});
 box.appendChild(ws);return box}
function endNav(back,fwd){
 var row=el('div','row cuerow');
 if(back){var b=el('button','btn sub','‹');b.type='button';b.setAttribute('aria-label','back');b.addEventListener('click',back);row.appendChild(b)}
 var f=el('button','btn sub','›');f.type='button';f.setAttribute('aria-label','next');f.addEventListener('click',fwd);row.appendChild(f);
 panel.appendChild(row)}
/* E4: ふたつの声(旅の始めと、いま) */
function e4(){
 var P=END.plan=endPlan();
 if(!P.show){e6();return}
 END.view='both';Snd.fx('page');
 var line=P.one?"Let's keep this page.":'Here is the day we left, and here is today.';
 endSay('Lulu','lulu',line,null);
 clearPanel();var box=el('div','eres');
 var three=P.cmp,marks=[];
 if(P.st&&P.st.bits&&P.en.bits)marks=endMarks(P.st,P.en,three);
 if(P.st)box.appendChild(endTier('Departure',P.st,three,three,null));
 box.appendChild(endTier('Home',P.en,P.cmp||(!P.st&&P.en.src==='az'&&!!P.en.w),false,marks));
 if(marks.length){var tk=endToks(),jl=el('div','ejoy');jl.textContent=marks.map(function(i){return '✦ '+tk[i].replace(/[^A-Za-z']/g,'')}).join('   ');box.appendChild(jl)}
 panel.appendChild(box);endNav(null,function(){e5()})}
/* E5: 音の変化(いちばんむずかしかった音 上位3つ。数字は出さず、棒の長さだけ) */
var KMAP={'θ':'th','ð':'th','f':'f','v':'v','l':'l','r':'r','ɹ':'r','b':'b','ʃ':'sh','s':'s','w':'w','ŋ':'ng'};
function sndAz(st,en){
 function agg(M){var o={};M.w.forEach(function(x){(x[3]||[]).forEach(function(p){var k=String(p[0]).replace(/[ˈˌː]/g,'');if(k==='ɹ')k='r';if(!KMAP[k])return;var e=o[k]||(o[k]={s:0,n:0,ws:{}});e.s+=p[1];e.n++;var wk=vnorm(x[0]);if(e.ws[wk]==null||p[1]<e.ws[wk])e.ws[wk]=p[1]})});return o}
 var a=agg(st),b=agg(en),rows=[];
 Object.keys(a).forEach(function(k){
  var x=a[k],y=b[k];if(!y||Object.keys(x.ws).length<2||Object.keys(y.ws).length<2)return;
  var sm=x.s/x.n,em=y.s/y.n;if(sm>=85)return;
  var ex='',lo=999;Object.keys(x.ws).forEach(function(w){if(x.ws[w]<lo){lo=x.ws[w];ex=w}});
  rows.push({sk:KMAP[k],k:KMAP[k],ex:ex,a:sm,b:em})});
 rows.sort(function(p,q){return p.a-q.a});return rows.slice(0,3)}
function sndBits(st,en){
 var tk=endToks(),rows=[];
 SNDORDER.forEach(function(id){
  var idx=[];tk.forEach(function(k,i){var w=vnorm(k);if(w.length>1&&hasSnd(id,w))idx.push(i)});
  var seen={},ws=0;idx.forEach(function(i){var w=vnorm(tk[i]);if(!seen[w]){seen[w]=1;ws++}});if(ws<2)return;
  var ms=0,me=0,ex='';idx.forEach(function(i){if(st.bits.charAt(i)!=='1'){ms++;if(!ex)ex=vnorm(tk[i])}if(en.bits.charAt(i)!=='1')me++});
  if(!ms)return;rows.push({sk:SND[id].chip,k:KMAP[id]?id:'',ex:ex,a:100-ms*100/idx.length,b:100-me*100/idx.length})});
 rows.sort(function(p,q){return p.a-q.a});return rows.slice(0,3)}
function e5(){
 var P=END.plan;if(END.sndRows==null)END.sndRows=P.cmp?sndAz(P.st,P.en):((P.st&&P.st.bits&&P.en.bits)?sndBits(P.st,P.en):[]);
 var rows=END.sndRows;if(!rows.length){e6();return}
 endSay('Lulu','lulu','These are the sounds we met on the road.',null);
 clearPanel();var box=el('div','eres');
 var lg=el('div','esl');lg.appendChild(el('span','','Departure ▬ (top)'));lg.appendChild(el('span','','Home ▬ (bottom)'));box.appendChild(lg);
 rows.forEach(function(r){
  var row=el('div','esr');row.appendChild(el('div','sk',r.sk));
  var bars=el('div','bars');bars.appendChild(el('div','sx',r.ex));
  [['a',r.a],['b',r.b]].forEach(function(q){var tr=el('div','eb '+q[0]),i=el('i');i.style.width=Math.max(4,Math.min(100,Math.round(q[1])))+'%';tr.appendChild(i);bars.appendChild(tr)});
  row.appendChild(bars);box.appendChild(row)});
 panel.appendChild(box);endNav(function(){e4()},function(){e6()})}
/* E6: 次の旅のメモ(いちばん残った音を1つ)と、アルバムの表紙 */
function e6(){
 END.view='cover';Snd.fx('page');clearPanel();
 var rows=END.sndRows||[],memo=null;
 if(rows.length){var w=rows.slice().sort(function(p,q){return p.b-q.b})[0];memo={k:w.k,snd:w.sk,w:w.ex,ts:Date.now()};voiceSetNext(memo)}
 var box=el('div','eres emem');
 if(memo){box.appendChild(el('div','erh')).appendChild(el('b','','Next trip memo'));
  var big=el('div','esk',memo.snd);box.appendChild(big);box.appendChild(el('div','sx',memo.w))}
 panel.appendChild(box);
 var go=el('button','btn sub','Close the album');go.type='button';go.addEventListener('click',function(){location.href='../../world/?map=1'});
 var row=el('div','row cuerow');row.appendChild(go);panel.appendChild(row);
 endSay('Lulu','lulu',memo?"Next time, let's meet that sound on the road.":'Until the next trip.',null)}
