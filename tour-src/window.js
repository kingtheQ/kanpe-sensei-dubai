/* ===== 世界一周編: 窓口フロー(タスク012) =====
   宣言 → 聞き取り5本 → 線を引く → おすすめ → 値段 → 読み上げ確認 → 名前の確認 → 搭乗券(既存 ticket_star / ticket_ow)
   設計の正本: docs/pm/deliverables/003・004・011。build.py が tour/index.html に差しこむ。 */
var WSTEP=['win_decl','win_c1','win_c2','win_c5','win_c7','win_c8','win_route','win_rec','win_price','win_rb','win_name','win_pass'];
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
 var W=save.win,tk=W.pick==='ow'?('ow'+(W.cont===4?4:5)):'star';
 if(k==='win_price')return 'win_price_'+tk;if(k==='win_rb')return 'win_rb_'+tk;if(k==='win_pass')return 'ticket_'+(W.pick==='ow'?'ow':'star');return k}
function winRun(){
 var W=save.win,k=WSTEP[W.step];if(!k){showMap();return}
 if(k==='win_rec')winRecBuild();if(k==='win_decl')winDeclPrep();
 var vid=winVid(k),pl=PBY.ticket;
 if(k==='win_pass'){save.ticket=W.pick==='ow'?'ow':'star';W.done=1;storeSave();worldAt('nairobi');startVid(pl,vid,'hub');return}
 startVid(pl,vid,'win')}
function winAfter(S){var W=save.win;W.step++;storeSave();winRun()}

/* 次の旅のメモがあれば、係員が切り出す(2周目の窓口) */
function winDeclPrep(){
 var L=DLG.win_decl.lines[0];if(!L.n0)L.n0=L.n;var mm=memoLoad();
 L.n=mm.length?("Good morning. Last time, you wanted to see "+mm.join(' and ')+". I wrote it down for your next trip. Now, please make your promise to Lulu."):L.n0}

/* 分かれ目(▶): 英文だけを出して読み上げる。選んだ文をそのまま言う */
function winOpts(T){
 G.phase='opts';clearPanel();clearInterval(G.typeTimer);msgText.textContent=T.npc;var S=G.scene,sid=G.sid;
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

/* おすすめ: 印の多い券と理由。同数ならキングが▶で決める。印がなければスター(003 2-3) */
function winRecBuild(){
 var W=save.win,m=W.m||{},cnt={star:0,ow:0},why={star:[],ow:[]};
 Object.keys(m).forEach(function(k){var x=m[k];if(cnt[x.t]!=null){cnt[x.t]++;if(x.why)why[x.t].push(x.why)}});
 var NM={star:'Star Alliance',ow:'oneworld Explorer'},tie=cnt.star===cnt.ow&&cnt.star>0,none=cnt.star===0&&cnt.ow===0,lead=cnt.ow>cnt.star?'ow':'star',oth=lead==='ow'?'star':'ow',intro,ans;
 if(none){intro="You are still deciding, so I recommend Star Alliance. The rules are simple, and it has the most routes.";ans="Thank you. That makes sense."}
 else if(tie){intro="Your dreams point to two tickets. "+why.ow.slice(0,1).concat(why.star.slice(0,1)).join(' ')+" Both are good.";ans="Two tickets. I see."}
 else{intro="Let me look at your answers. "+why[lead].slice(0,2).join(' ')+" So I recommend "+NM[lead]+".";ans="Thank you. That makes sense."}
 var order=tie||none?['star','ow']:[lead,oth];
 function op(k){return {k:k,y:wst("I'll take "+NM[k]+", please."),jp:'',tk:k}}
 DLG.win_rec={who:'世界一周の窓口係',story:1,bg:'tdesk',sp:'desk_rtw',hero:'blue',lulu:'plain',nogold:1,inter:[],intro:'The Round the World desk.',win:1,auto:1,words:[],
  lines:[{n:intro,jp:''},{y:wst(ans),jp:''},{n:"Which ticket will you take?",jp:'どちらの券にしますか。'},{y:'',jp:'',opts:order.map(op)}]}}

/* ---- 長いカンペ(宣言・読み上げ確認): 合否で止めない。点・色・音は出さず、最後に「きこえたこと」だけ見せる ---- */
function diagDone(){if(!G.scene)return;G.phase='pass';G.tries=0;advance()}
function setupDiag(act,stat,toks,spans,T,card){
 var sid=G.sid,tg=toks.map(function(k){return k.txt}),heardEl=el('div','heard',''),rec=null,listening=false,fin=false,pend=false,got=false,segs=[],alts=[],lastInt='',silent=0,cfSum=0,cfN=0,t0=Date.now(),IDLE='🎤 もういちど';
 card.appendChild(heardEl);
 function alive(){return G.sid===sid&&G.view==='scene'&&!fin}
 function setIdle(){listening=false;act.classList.remove('down');act.textContent=IDLE}
 function hear(){return segs.join(' ')+(lastInt?' '+lastInt:'')}
 function hl(){var r=analyze(tg,hear()),last=-1;r.words.forEach(function(w,i){if(w.ok&&w.h!=null)last=i});spans.forEach(function(s,i){s.classList.toggle('on',i===last)})}
 function enough(){var r=analyze(tg,segs.join(' ')),n=r.words.length;return r.ratio>=.97||(r.okN>=n*.5&&r.words.slice(-3).every(function(w){return w.ok}))}  /* 最後の3語まで聞こえたら終わり。途中の一息では切らない */
 function fallback(msg){
  var a2=act.cloneNode(false);a2.className='btn';a2.textContent=IDLE;act.parentNode.replaceChild(a2,act);listening=false;
  setupActionTimer(a2,stat,toks,spans,T);card.appendChild(el('div','heard nomic',msg))}
 function finish(why){
  if(fin)return;fin=true;try{if(rec){var r0=rec;rec=null;r0.abort()}}catch(e){}Snd.duck(0);listening=false;act.disabled=true;
  var txt=segs.join(' ').trim(),res=analyze(tg,txt);
  /* 集計用の記録(004): 既存の発音記録 plog に、同じ形で残す。bits=紙の単語ごとの 合った(1)/ちがった(0)。alts=候補1〜3 */
  plogAdd({ts:Date.now(),v:G.scene?G.scene.vid:'',tg:tg.join(' '),hd:txt.slice(0,600),cf:cfN?cfSum/cfN:0,ok:res.okN,n:res.n,
   miss:res.words.filter(function(w){return !w.ok}).slice(0,40).map(function(w){return {t:missKey(w.t),h:w.h,k:w.k}}),
   diag:T.diag,why:why,seg:segs.length,bits:res.words.map(function(w){return w.ok?'1':'0'}).join(''),alts:alts.slice(0,12)});
  card.classList.add('shown');heardEl.className='heard fin';heardEl.textContent=txt||'…';
  later(Math.min(6500,2600+txt.length*16),diagDone)}
 function start(){
  if(fin||listening)return;stopSay();
  var r;try{r=new SR()}catch(e){fallback('マイクが使えません');return}
  rec=r;r.lang='en-US';r.interimResults=true;r.maxAlternatives=3;r.continuous=false;got=false;lastInt='';
  var errCode='';
  r.onresult=function(ev){
   if(rec!==r)return;if(!alive()){try{r.abort()}catch(e){}return}
   var rs=ev.results[ev.results.length-1],a0=rs[0];
   if(rs.isFinal){got=true;segs.push(String(a0.transcript).trim());cfSum+=a0.confidence||0;cfN++;var al=[];for(var q=0;q<rs.length&&q<3;q++)al.push(String(rs[q].transcript).slice(0,120));alts.push(al);lastInt='';silent=0;hl()}
   else{lastInt=a0.transcript;hl()}};
  r.onerror=function(ev){errCode=(ev&&ev.error)||'error'};
  r.onend=function(){Snd.duck(0);
   if(rec!==r)return;rec=null;listening=false;if(!alive())return;
   if(errCode==='not-allowed'||errCode==='service-not-allowed'){fallback('マイクが許可されていません');return}
   if(errCode==='audio-capture'){fallback('マイクが見つかりません');return}
   if(!got&&lastInt){segs.push(String(lastInt).trim());alts.push([String(lastInt).slice(0,120)]);got=true;lastInt=''}
   if(got)silent=0;else silent++;
   if(segs.length&&enough()){finish('enough');return}
   if(silent>=(segs.length?2:3)||Date.now()-t0>110000){setIdle();finish(segs.length?'silence':'none');return}
   pend=true;later(150,function(){pend=false;if(alive())start()})};
  try{Snd.duck(1);r.start();listening=true;act.classList.add('down');act.textContent='きいてます…'}catch(e){Snd.duck(0);fallback('マイクが使えません')}}
 G.kick=function(){if(G.phase==='cue'&&alive()&&!listening&&!pend&&!rec&&act.isConnected)start()};
 G.mute=function(){if(rec){var r0=rec;rec=null;try{r0.abort()}catch(e){}}listening=false;pend=false;Snd.duck(0);segs=[];alts=[];lastInt='';silent=0;t0=Date.now();if(act.isConnected)setIdle();heardEl.textContent=''};
 act.addEventListener('click',function(){
  if(fin)return;
  if(listening||pend){
   if(segs.length||lastInt){if(!got&&lastInt){segs.push(String(lastInt).trim());lastInt=''}finish('manual')}
   else{if(rec){var r0=rec;rec=null;try{r0.abort()}catch(e){}}pend=false;Snd.duck(0);setIdle()}
   return}
  start()});
 act.addEventListener('contextmenu',function(e){e.preventDefault()});
 stat.className='stat';stat.textContent=''}

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
