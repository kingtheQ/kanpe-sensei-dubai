/* ---- 長いカンペ(宣言・読み上げ確認): 合否で止めない。点・色・音は出さず、最後に「きこえたこと」だけ見せる ---- */
function diagDone(){if(!G.scene)return;if(G.scene.end&&typeof endAfterRead==='function'){endAfterRead();return}G.phase='pass';G.tries=0;advance()}
function setupDiag(act,stat,toks,spans,T,card){
 var sid=G.sid,tg=toks.map(function(k){return k.txt}),heardEl=el('div','heard',''),rec=null,listening=false,fin=false,pend=false,got=false,segs=[],alts=[],lastInt='',silent=0,cfSum=0,cfN=0,t0=Date.now(),IDLE='🎤 もういちど';
 card.appendChild(heardEl);
 function alive(){return G.sid===sid&&G.view==='scene'&&!fin}
 function setIdle(){listening=false;act.classList.remove('down');act.textContent=IDLE}
 function hear(){return segs.join(' ')+(lastInt?' '+lastInt:'')}
 function hl(){var r=analyze(tg,hear()),last=-1;r.words.forEach(function(w,i){if(w.ok&&w.h!=null)last=i});spans.forEach(function(s,i){s.classList.toggle('on',i===last)})}
 function enough(){var r=analyze(tg,segs.join(' ')),n=r.words.length;return r.ratio>=.97||(r.okN>=n*.5&&r.words.slice(-3).every(function(w){return w.ok}))}  /* 最後の3語まで聞こえたら終わり。途中の一息では切らない */
 function fallback(msg){
  if(G.onBlocked){var ob=G.onBlocked;G.onBlocked=null;fin=true;ob(msg);return}  /* 終わりの場面: マイクが使えないときは、ルルが読む形にかえる */
  var a2=act.cloneNode(false);a2.className='btn';a2.textContent=IDLE;act.parentNode.replaceChild(a2,act);listening=false;
  setupActionTimer(a2,stat,toks,spans,T);card.appendChild(el('div','heard nomic',msg))}
 function finish(why){
  if(fin)return;fin=true;try{if(rec){var r0=rec;rec=null;r0.abort()}}catch(e){}Snd.duck(0);listening=false;act.disabled=true;
  var txt=segs.join(' ').trim(),res=analyze(tg,txt);
  /* 集計用の記録(004): 既存の発音記録 plog に、同じ形で残す。bits=紙の単語ごとの 合った(1)/ちがった(0)。alts=候補1〜3 */
  plogAdd({ts:Date.now(),v:G.scene?G.scene.vid:'',tg:tg.join(' '),hd:txt.slice(0,600),cf:cfN?cfSum/cfN:0,ok:res.okN,n:res.n,
   miss:res.words.filter(function(w){return !w.ok}).slice(0,40).map(function(w){return {t:missKey(w.t),h:w.h,k:w.k}}),
   diag:T.diag,why:why,seg:segs.length,bits:res.words.map(function(w){return w.ok?'1':'0'}).join(''),alts:alts.slice(0,12),src:'sr'});   /* src: sr=ブラウザの音声認識 / az=Azure(voice.js) */
  if(voiceCmpDiag(T.diag))voiceSaveSR(T.diag,tg,res,txt);  /* 始め・終わりの宣言は、比べるための別の記録(kanpe-voice-v1)にも残す */
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

