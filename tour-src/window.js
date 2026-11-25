/* ===== 世界一周編: 窓口フロー(タスク012) =====
   宣言 → 聞き取り5本 → 線を引く → おすすめ(いつもスター) → スターの決まり → ルートを数える → 値段 → 読み上げ確認 → 名前の確認 → 搭乗券(ticket_star だけ)
   タスク088: 発券はスターに統一(1周目)。ow4/ow5・ticket_ow のデータは2周目用に残し、この流れからは行かない。
   設計の正本: docs/pm/deliverables/003・004・011。build.py が tour/index.html に差しこむ。 */
var WSTEP=['win_decl','win_c1','win_c2','win_c5','win_c7','win_c8','win_route','win_rec','win_rules','win_count','win_price','win_rb','win_name','win_pass'];
var ORD=['','first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth','eleventh','twelfth','thirteenth','fourteenth','fifteenth','sixteenth','seventeenth','eighteenth','nineteenth','twentieth','twenty first','twenty second','twenty third','twenty fourth','twenty fifth','twenty sixth','twenty seventh','twenty eighth','twenty ninth','thirtieth','thirty first'];
var WSTOP={a:1,an:1,the:1,to:1,of:1,'in':1,on:1,at:1,and:1,or:1,'for':1,'with':1,from:1,as:1,is:1,am:1,are:1,be:1,it:1,that:1,'this':1,my:1,your:1,our:1,so:1};
/* カンペの強調(＊): 冠詞・前置詞などのほかを太字にする(data 側の star() と同じ規則) */
function wst(s){return s.split(' ').map(function(tok){var m=/^([^A-Za-z0-9]*)(.*?[A-Za-z0-9])([^A-Za-z0-9]*)$/.exec(tok);if(!m||WSTOP[m[2].toLowerCase()])return tok;return m[1]+'*'+m[2]+'*'+m[3]}).join(' ')}

/* ---- 次の旅のメモ(はじめからでも消えない別のキー。端末の中だけ) ---- */
var MEMOKEY='kanpe-tour-memo-v1';
function memoLoad(){try{var a=JSON.parse(localStorage.getItem(MEMOKEY)||'[]');return Array.isArray(a)?a.filter(function(x){return typeof x==='string'&&x.length<40}).slice(0,12):[]}catch(e){return[]}}
function winMemo(en){var a=memoLoad();if(a.indexOf(en)<0)a.push(en);try{localStorage.setItem(MEMOKEY,JSON.stringify(a))}catch(e){}}

/* ---- 状態: save.win = {step, m:{場面:{t,why}}, cont:大陸の数, pick:'star'|'ow', done} ---- */
function winStart(){
 var W=save.win;if(!W||typeof W!=='object'||W.done)W=save.win={step:0,m:{},cont:5,pick:null};
 if(!W.m||typeof W.m!=='object')W.m={};if(typeof W.step!=='number'||W.step<0||W.step>=WSTEP.length)W.step=0;
 storeSave();winRun()}
function winVid(k){
 /* 088: どの分岐でも券はスター。save.win.pick が ow でも(古いセーブ・点検モード)、ここで無視する */
 if(k==='win_price')return 'win_price_star';if(k==='win_rb')return 'win_rb_star';if(k==='win_pass')return 'ticket_star';return k}
function winRun(){
 var W=save.win,k=WSTEP[W.step];if(!k){showMap();return}
 if(k==='win_decl'&&voiceNeedConsent()){winConsent();return}   /* 宣言の直前に、声を送ってよいかを一度だけ聞く(013 3-3) */
 if(k==='win_rec')winRecBuild();if(k==='win_decl')winDeclPrep();
 var vid=winVid(k),pl=PBY.ticket;
 if(k==='win_pass'){save.ticket='star';W.pick='star';W.done=1;storeSave();startVid(pl,vid,'hub');return}
 startVid(pl,vid,'win')}
function winAfter(S){var W=save.win;W.step++;storeSave();winRun()}

/* 同意の1枚: 賢者の見送りのあと、宣言の直前。ルルが紙をわたす。選んだら宣言へ進む */
function winConsent(){
 DLG.win_consent=DLG.win_consent||{who:'Lulu',story:0,bg:'tdesk',sp:'',hero:'blue',lulu:'plain',nogold:1,inter:[],intro:'',lines:[],words:[],win:1,auto:1,hook:'consent'};
 startVid(PBY.ticket,'win_consent','win')}
function consentScene(S){
 applyCtx({bg:'tdesk',who:'Lulu',sp:'lulu',hero:'blue',lulu:'plain',gold:0});
 var en='King, one question before we start.';setMsgInstant(en,'Lulu');spSay=false;say(en,.95,1.35);
 consentCard(function(){winRun()})}

/* 次の旅のメモがあれば、係員が切り出す(2周目の窓口) */
function winDeclPrep(){
 var L=DLG.win_decl.lines[0];if(!L.n0)L.n0=L.n;var mm=memoLoad();
 var nx=vLoad().next,sn=nx&&nx.k?(" Last time, the \""+nx.k+"\" sound was a little hard. Let's meet it again on the road."):"";
 L.n=mm.length?("Good morning. Last time, you wanted to see "+mm.join(' and ')+". I wrote it down for your next trip."+sn+" Now, please make your promise to Lulu."):(sn?("Good morning."+sn+" Now, please make your promise to Lulu."):L.n0)}

/* 分かれ目(▶): 英文だけを出して読み上げる。選んだ文をそのまま言う */
function winOpts(T){
 G.phase='opts';clearPanel();clearInterval(G.typeTimer);msgText.textContent=npcHide()?'':T.npc;var S=G.scene,sid=G.sid;
 var box=el('div','dqbox'),bs=[];
 T.opts.forEach(function(o){var b=el('button','dq');b.type='button';b.appendChild(el('span','cur','▶'));b.appendChild(el('span','',cueText(o.y)));
  b.addEventListener('click',function(){pickOpt(T,o)});box.appendChild(b);bs.push(b)});
 panel.appendChild(box);
 function sel(i){bs.forEach(function(b,j){b.classList.toggle('sel',j===i)})}
 bs.forEach(function(b,i){['focus','pointerenter','pointerdown'].forEach(function(ev){b.addEventListener(ev,function(){sel(i)})})});
 sel(0);
 (function rd(i){if(G.sid!==sid||G.phase!=='opts'||i>=T.opts.length)return;sel(i);say(cueText(T.opts[i].y),.9,1,gd(function(){later(300,function(){if(G.phase==='opts')rd(i+1)})}))})(0)}
function pickOpt(T,o){
 if(G.phase!=='opts')return;stopSay();var S=G.scene;
 S.pick=o.k;T.pk=o.k;T.cue=o.y;T.cueJp=o.jp;if(o.rep)T.rep=o.rep;
 winMark(S.vid,o);if(o.memo)winMemo(o.memo);
 showCue()}
function winMark(vid,o){
 var W=save.win;if(!W)return;if(!W.m)W.m={};delete W.m[vid];
 if(o.mt)W.m[vid]={t:o.mt,why:o.why||''};if(o.cont)W.cont=o.cont;if(o.tk)W.pick=o.tk;storeSave()}

/* おすすめ(088): 印の多い券の理由は聞いたうえで、最後はいつもスター。選ぶ分岐はなく、係員が「スターが合います」と寄せる */
function winRecBuild(){
 var W=save.win,m=W.m||{},cnt={star:0,ow:0},why={star:[],ow:[]};
 Object.keys(m).forEach(function(k){var x=m[k];if(cnt[x.t]!=null){cnt[x.t]++;if(x.why)why[x.t].push(x.why)}});
 var intro;
 if(cnt.star===0&&cnt.ow===0)intro="You are still deciding, so I recommend Star Alliance. The rules are simple, and it has the most routes.";
 else if(cnt.star>cnt.ow)intro="Let me look at your answers. "+why.star.slice(0,2).join(' ')+" So I recommend Star Alliance.";
 else intro="Let me look at your answers. "+why.ow.slice(0,1).join(' ')+" oneworld is a good ticket for another trip. But your route goes one way, around the world, and home. Star Alliance fits your route best, and its rules are simple.";
 DLG.win_rec={who:'世界一周の窓口係',story:1,bg:'tdesk',sp:'desk_rtw',hero:'blue',lulu:'plain',nogold:1,inter:[],intro:'The Round the World desk.',win:1,auto:1,words:[],
  lines:[{n:intro,jp:''},{y:wst("Thank you. That makes sense."),jp:'ありがとうございます。なるほど。'},
   {n:"Shall I prepare the Star Alliance ticket for you?",jp:'スターアライアンスの券を用意しましょうか。'},
   {y:wst("Yes, please. I'll take Star Alliance."),jp:'はい、お願いします。スターアライアンスにします。'}]}}

/* ---- 線を引く地図(窓口の壁): 西まわりに 羽田→ナイロビ→ロヴァニエミ→クスコ→ホノルル→羽田。もどる線は止まる ---- */
var WM=/*WMAP*/[];
var WP={tok:[139.8,35.5,'HANEDA',0,8],nbo:[36.8,-1.3,'NAIROBI',0,7],rov:[25.7,66.5,'ROVANIEMI',-26,0],cus:[-72,-13.5,'CUSCO',0,7],hon:[-157.9,21.3,'HONOLULU',6,7]};
var WSG=[['tok','nbo',0],['nbo','rov',0],['rov','cus',0],['cus','hon',0],['hon','tok',-360]];
function wmx(lon){return 22+(lon+180)/360*276}function wmy(lat){return 40+(75-lat)/130*48}
function wmPt(a,b,sh,f){var A=WP[a],B=WP[b],lon=A[0]+(B[0]+sh-A[0])*f,lat=A[1]+(B[1]-A[1])*f,x=wmx(lon),y=wmy(lat);while(x<22)x+=276;while(x>=298)x-=276;return [x,y]}
function wmN(a,b,sh){var A=WP[a],B=WP[b];return Math.max(2,Math.round(Math.sqrt(Math.pow((B[0]+sh-A[0])*.77,2)+Math.pow((B[1]-A[1])*.37,2))/2.2))}
function wmSeg(i,f,col){var sg=WSG[i],n=wmN(sg[0],sg[1],sg[2]);for(var k=0;k<=n*f;k++){var q=wmPt(sg[0],sg[1],sg[2],k/n);R(col,q[0]-1,q[1]-1,2,2)}}
BGS.rtmap=function(ctx,S){
 airWall('#e9edf3');floorAir('#d8dce6','#c4c8d4');
 R('#0b1d33',17,36,286,56);R('#f4f1e8',17,36,286,1);R('#f4f1e8',17,91,286,1);R('#1c4a78',22,40,276,48);
 for(var r=0;r<WM.length;r++){var row=WM[r];for(var c0=0;c0<row.length;c0++)if(row.charAt(c0)==='#')R(((r+c0)%5===0)?'#4f9a5c':'#3f8450',22+c0*3,40+r*3,3,3)}
 var rf=(S&&S.rf)||0,rn=(S&&S.rn)||0,e=(S&&S.rt!=null)?t-S.rt:0,D=1.1;
 for(var i=0;i<5;i++){if(i<rf)wmSeg(i,1,'#ffd36a');else if(i<rn){var f=Math.max(0,Math.min(1,(e-(i-rf)*D)/D));if(f>0)wmSeg(i,f,'#ffd36a')}}
 if(rn>=6){ /* もどる線: ホノルルからペルーへ。少し進んで止まる(青。赤は使わない) */
  var f6=Math.max(0,Math.min(1,e/1.2)),n6=wmN('hon','cus',0),lim=Math.floor(n6*.28*f6),ex=null;
  for(var k=0;k<=lim;k++){var q=wmPt('hon','cus',0,k/n6);if(k%2===0)R('#5aa0ff',q[0]-1,q[1]-1,2,2);ex=q}
  if(f6>=1&&ex&&Math.floor(t*3)%2){R('#fff',ex[0]-4,ex[1]-4,9,9);R('#2f6ad8',ex[0]-3,ex[1]-3,7,7);T('✕',ex[0],ex[1],7,'#fff')}}
 Object.keys(WP).forEach(function(k){var p=WP[k],x=wmx(p[0]),y=wmy(p[1]);R('#0b1d33',x-3,y-3,6,6);R('#ffd36a',x-2,y-2,4,4);T(p[2],x+p[3],y+p[4],5,'#fff')})};
