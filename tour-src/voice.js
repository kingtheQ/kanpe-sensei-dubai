/* ===== 声(タスク016): 同意・記録(kanpe-voice-v1)・Azure 発音評価・設定 =====
   設計の正本: docs/pm/deliverables/013-ending-scores-design-v1.md
   声の行き先: ブラウザの音声認識(いつも) / Azure(同意した人の、旅の始めと終わりの宣言の2回だけ)。
   キーはゲームに置かない。中継(relay/)が10分だけ使えるトークンを渡す。中継の URL が空なら Azure は使わない。
   build.py が /*RELAY_URL*/'' の中身を tour-src/relay-url.txt から差しこむ(中継のURLは、そこ1か所だけ)。 */
var VOICEKEY='kanpe-voice-v1',VREF='decl-v1';
var RELAY_URL=/*RELAY_URL*/'';
var SDK_URL='https://cdn.jsdelivr.net/npm/microsoft-cognitiveservices-speech-sdk@1.45.0/distrib/browser/microsoft.cognitiveservices.speech.sdk.bundle-min.js';
var SDK_SRI='sha384-RrysmqdtkBJHdL3yBqslKJR4EMsU7hA1rz+HpC9qMY001mmfKeRcKisr+NyuyI6H';

/* ---- 保存: consent・旅ごとの始め/終わり・次の旅のメモ。「はじめから」でも消さない別のキー(苦手な音と同じ扱い) ---- */
function vLoad(){
 var v=null;try{v=JSON.parse(localStorage.getItem(VOICEKEY)||'null')}catch(e){}
 if(!v||typeof v!=='object'||v.v!==1)v={v:1,consent:null,trips:[],next:null};
 if(!Array.isArray(v.trips))v.trips=[];
 if(!v.consent||typeof v.consent!=='object'||typeof v.consent.az!=='boolean')v.consent=null;
 if(!v.next||typeof v.next!=='object')v.next=null;
 return v}
function vSave(v){try{localStorage.setItem(VOICEKEY,JSON.stringify(v))}catch(e){}}
function voiceRelayOn(){return /^https:\/\//.test(RELAY_URL)}
function voiceConsent(){var c=vLoad().consent;return c?c.az:null}
function voiceNeedConsent(){return voiceRelayOn()&&voiceConsent()===null}      /* 中継がなければ、送る先がないので聞かない */
function voiceAzureOn(){return voiceRelayOn()&&voiceConsent()===true}
/* Azure で読む長いカンペ: 旅の始めの宣言・終わりの宣言・窓口の読み返し(タスク024)。始め/終わりの2つだけが kanpe-voice-v1 の比べに入る */
function voiceAzDiag(k){return k==='decl'||k==='decl_end'||k==='readback'}
function voiceCmpDiag(k){return k==='decl'||k==='decl_end'}
/* 読み返しの判定: 聞き取れた単語でも、Azure の単語の正確さが AZ_BAD(60)未満なら「言えなかった」に数える(仮。false にすると、聞き取れたかどうかだけ) */
var RB_AZ_JUDGE=true;
function voiceSetConsent(b){var v=vLoad();v.consent={az:!!b,at:Date.now(),ver:1};vSave(v)}
function voiceClear(){var v=vLoad();v.trips=[];v.next=null;vSave(v)}              /* 同意の選びは残す(切り替えは別) */
function voiceSetNext(o){var v=vLoad();v.next=o;vSave(v)}
function voiceTripCur(){var v=vLoad();return v.trips.length?v.trips[v.trips.length-1]:null}
/* kind: 'decl'=旅の始め / 'decl_end'=旅の終わり。2周目の始めは、前の旅に終わりがあれば新しい旅として測り直す */
function voiceSetM(kind,M){
 var v=vLoad(),tr=v.trips.length?v.trips[v.trips.length-1]:null;
 if(kind==='decl'){if(!tr||tr.end)v.trips.push(tr={id:tr?tr.id+1:1,ref:VREF,start:null,end:null});tr.ref=VREF;tr.start=M}
 else{if(!tr)v.trips.push(tr={id:1,ref:VREF,start:null,end:null});tr.end=M}
 if(v.trips.length>20)v.trips=v.trips.slice(-20);
 vSave(v)}
/* ブラウザの音声認識だけで読んだとき(同意なし・通信なし)の記録。数字は null、単語ごとは bits だけ */
function voiceSaveSR(kind,tg,res,txt){
 voiceSetM(kind,{ts:Date.now(),src:'sr',tot:null,acc:null,flu:null,cmp:null,w:null,
  bits:res.words.map(function(w){return w.ok?'1':'0'}).join(''),heard:String(txt||'').slice(0,600)})}

/* ---- 中継からトークンをもらう(8秒で見切る)・Speech SDK を読みこむ(同意した人が読むときだけ) ---- */
var _vt=null,_sdkP=null;
function voiceToken(){
 if(_vt&&_vt.exp>Date.now())return Promise.resolve(_vt);
 return new Promise(function(res,rej){
  var done=false,ac=(typeof AbortController!=='undefined')?new AbortController():null;
  var tm=setTimeout(function(){if(done)return;done=true;try{if(ac)ac.abort()}catch(e){}rej('token_timeout')},8000);
  var fail=function(e){if(done)return;done=true;clearTimeout(tm);rej(String(e))};
  try{fetch(RELAY_URL.replace(/\/+$/,'')+'/token',{cache:'no-store',signal:ac?ac.signal:undefined}).then(function(r){if(!r.ok)throw 'http'+r.status;return r.json()}).then(function(j){
   if(done)return;if(!j||typeof j.token!=='string'||!j.token)throw 'bad_token';
   done=true;clearTimeout(tm);_vt={token:j.token,region:String(j.region||'eastus'),exp:Date.now()+Math.max(60,+j.expiresInSec||60)*1000-20000};res(_vt)}).catch(fail)}
  catch(e){fail(e)}})}
function voiceSdk(){
 if(window.SpeechSDK)return Promise.resolve(window.SpeechSDK);
 if(_sdkP)return _sdkP;
 _sdkP=new Promise(function(res,rej){
  var s=document.createElement('script');s.src=SDK_URL;s.integrity=SDK_SRI;s.crossOrigin='anonymous';s.async=true;
  var tm=setTimeout(function(){rej('sdk_timeout')},12000);
  s.onload=function(){clearTimeout(tm);if(window.SpeechSDK)res(window.SpeechSDK);else rej('sdk_missing')};
  s.onerror=function(){clearTimeout(tm);rej('sdk_error')};
  document.head.appendChild(s)});
 _sdkP.catch(function(){_sdkP=null});
 return _sdkP}

/* ---- Azure の発音評価(連続認識。70語は約40秒なので、30秒を超える音声は連続で扱う) ----
   cb: started() / live(文字) / seg({text,pa,words}) / canceled(エラー文) / fail(理由)。返す H.stop(done) で止めて、まだ来る最後の結果も待つ。
   抑揚(prosody)は別料金なので使わない。 */
function voiceAzStart(ref,cb){
 var H={dead:false,rec:null,segs:[]};
 H.abort=function(){H.dead=true;try{if(H.rec)H.rec.close()}catch(e){}H.rec=null};
 H.stop=function(done){
  var fin=false,r=H.rec;function f(){if(fin)return;fin=true;H.abort();if(done)done()}
  if(!r){f();return}
  var tm=setTimeout(f,4000);
  try{r.stopContinuousRecognitionAsync(function(){clearTimeout(tm);f()},function(){clearTimeout(tm);f()})}catch(e){clearTimeout(tm);f()}};
 Promise.all([voiceToken(),voiceSdk()]).then(function(r){
  if(H.dead)return;
  var tk=r[0],S=r[1],rec;
  try{
   var cfg=S.SpeechConfig.fromAuthorizationToken(tk.token,tk.region);cfg.speechRecognitionLanguage='en-US';
   var pa=new S.PronunciationAssessmentConfig(ref,S.PronunciationAssessmentGradingSystem.HundredMark,S.PronunciationAssessmentGranularity.Phoneme,true);
   try{pa.phonemeAlphabet='IPA'}catch(e){}
   rec=new S.SpeechRecognizer(cfg,S.AudioConfig.fromDefaultMicrophoneInput());pa.applyTo(rec)}
  catch(e){cb.fail('init');return}
  H.rec=rec;
  rec.recognizing=function(s,e){if(!H.dead&&e&&e.result)cb.live(String(e.result.text||''))};
  rec.recognized=function(s,e){
   if(H.dead||!e||!e.result)return;var res=e.result;
   if(res.reason!==S.ResultReason.RecognizedSpeech)return;
   var j=null;try{j=JSON.parse(res.properties.getProperty(S.PropertyId.SpeechServiceResponse_JsonResult))}catch(x){}
   var nb=j&&j.NBest&&j.NBest[0];
   var sg={text:String(res.text||''),pa:(nb&&nb.PronunciationAssessment)||null,words:(nb&&nb.Words)||[]};
   H.segs.push(sg);cb.seg(sg)};
  rec.canceled=function(s,e){if(H.dead)return;cb.canceled(e&&e.reason===S.CancellationReason.Error?String(e.errorDetails||'error'):'')};
  rec.startContinuousRecognitionAsync(function(){if(!H.dead)cb.started()},function(err){if(!H.dead)cb.fail(String(err))})
 },function(e){if(!H.dead)cb.fail(String(e))});
 return H}

/* ---- 結果を、紙の単語(宣言文70語)の順にそろえて持つ。Azure の言葉と紙の言葉を、近い順に対応づける ---- */
function vnorm(s){return String(s).toLowerCase().replace(/[^a-z0-9']/g,'')}
function valign(rn,an){
 var n=rn.length,m=an.length,D=[],B=[],i,j;
 for(i=0;i<=n;i++){D.push([]);B.push([]);for(j=0;j<=m;j++){D[i].push(0);B[i].push(0)}}
 for(i=1;i<=n;i++){D[i][0]=i;B[i][0]=1}for(j=1;j<=m;j++){D[0][j]=j;B[0][j]=2}
 for(i=1;i<=n;i++)for(j=1;j<=m;j++){
  var sub=D[i-1][j-1]+(rn[i-1]===an[j-1]?0:1.2),del=D[i-1][j]+1,ins=D[i][j-1]+1;
  if(sub<=del&&sub<=ins){D[i][j]=sub;B[i][j]=0}else if(del<=ins){D[i][j]=del;B[i][j]=1}else{D[i][j]=ins;B[i][j]=2}}
 var map=[];for(i=0;i<n;i++)map.push(-1);i=n;j=m;
 while(i>0||j>0){var b=B[i][j];if(i>0&&j>0&&b===0){map[i-1]=j-1;i--;j--}else if(i>0&&(j===0||b===1)){i--}else{j--}}
 return map}
/* ---- 4つの数字(タスク024): 独自の計算式はやめ、Azure が返した値そのものを使う ----
   総合=PronScore / 正確さ=AccuracyScore / 流れ=FluencyScore / 言い切り度=CompletenessScore。
   長い宣言は連続認識で、Azure は「区切りごと」に4つの値を返す(全体で1つの値は返らない)。
   ・区切りが1つのとき: その区切りの4つの値を、そのまま使う(PronScore も Azure の値)。
   ・区切りが2つ以上のとき: Azure の区切りごとの値を、Microsoft の連続認識の例(Speech SDK サンプル)の考え方で合わせる
       正確さ=区切りの AccuracyScore を単語数で平均 / 流れ=区切りの FluencyScore を長さ(Duration)で平均
       言い切り度=紙の単語のうち、聞き取れて正確さ60以上の割合(Microsoft のサンプルが「誤発音」とする区切りと同じ。連続認識では区切りごとの値が全体の紙と比べた値か分からないため)
       総合=Microsoft Learn の式を、この3つにあてる(下の vPron)
   記録には、区切りごとの Azure の値(az)も そのまま残す。合わせ方を変えても、古い記録を計算しなおせる。 */
var AZ_BAD=60;                                   /* 単語の正確さがこれ未満=「遠い」(013 の3段の下の区切りと同じ。仮) */
var NUMV=2;                                      /* 数字の意味の版。2=Azure の値そのもの。印がない(nv なし)古い記録は、独自の式で計算した数字 */
function vr1(x){return Math.round(x*10)/10}
function vShow(x){return typeof x==='number'?String(Math.round(x)):'-'}      /* 画面には整数で出す */
/* PronScore(読み上げ・抑揚なし): Microsoft Learn「Use pronunciation assessment」の式。3つを小さい順に s0,s1,s2 として 0.6*s0+0.2*s1+0.2*s2 */
function vPron(a,f,c){var s=[a,f,c].sort(function(x,y){return x-y});return s[0]*.6+s[1]*.2+s[2]*.2}
/* raw=区切りごと [PronScore|null, Accuracy, Fluency, Completeness, 単語数, 長さ]。w=紙の単語の順の結果, refN=紙の単語数 */
function voiceWhole(raw,w,refN){
 if(!raw||!raw.length)return null;
 if(raw.length===1){var r=raw[0];return {tot:typeof r[0]==='number'?r[0]:vPron(r[1],r[2],r[3]),acc:r[1],flu:r[2],cmp:r[3]}}
 var an=0,as=0,fd=0,fs=0;
 raw.forEach(function(r){as+=r[1]*r[4];an+=r[4];fs+=r[2]*r[5];fd+=r[5]});
 if(!an||!fd)return null;
 var good=0;(w||[]).forEach(function(x){if(x&&x[1]!=null&&x[1]>=AZ_BAD&&x[2]!=='Omission')good++});
 var acc=as/an,flu=fs/fd,cmp=refN?Math.min(100,good*100/refN):0;
 return {tot:vPron(acc,flu,cmp),acc:acc,flu:flu,cmp:cmp}}
/* tg=紙の単語, segs=Azure の区切りごとの結果, txt=聞こえた文, res=analyze の結果。
   単語の半分以上が対応づかなければ、Azure の結果は使わない(src='sr'。数字なし) */
function voiceBuildM(tg,segs,txt,res){
 var rn=tg.map(vnorm),aw=[],raw=[];
 segs.forEach(function(sg){
  var pa=sg.pa,wd=0,wn=0;
  (sg.words||[]).forEach(function(w){
   var a=w.PronunciationAssessment||{};wd+=+w.Duration||0;
   if(a.ErrorType==='Insertion'||a.ErrorType==='Omission')return;wn++;
   aw.push({n:vnorm(w.Word),a:typeof a.AccuracyScore==='number'?a.AccuracyScore:null,e:a.ErrorType||'None',
    p:(w.Phonemes||[]).map(function(p){var q=p.PronunciationAssessment||{};return [String(p.Phoneme||''),Math.round(typeof q.AccuracyScore==='number'?q.AccuracyScore:0)]})})});
  if(pa&&typeof pa.AccuracyScore==='number'&&typeof pa.FluencyScore==='number'&&typeof pa.CompletenessScore==='number'&&wn>0)
   raw.push([typeof pa.PronScore==='number'?pa.PronScore:null,pa.AccuracyScore,pa.FluencyScore,pa.CompletenessScore,wn,wd||1])});
 var map=valign(rn,aw.map(function(x){return x.n})),w=[],matched=0;
 rn.forEach(function(r,i){
  var j=map[i],x=j>=0?aw[j]:null,ok=x&&x.a!=null&&(x.n===r||lev(x.n,r)<=Math.max(1,Math.floor(r.length*.5)));
  if(ok){matched++;w.push([tg[i],Math.round(x.a),x.e,x.p])}else w.push([tg[i],null,'Omission',[]])});
 var cov=tg.length?matched/tg.length:0,W=cov>=.5?voiceWhole(raw,w,tg.length):null,usable=!!W;
 var M={ts:Date.now(),src:usable?'az':'sr',nv:usable?NUMV:undefined,tot:null,acc:null,flu:null,cmp:null,w:null,
  bits:res.words.map(function(x){return x.ok?'1':'0'}).join(''),heard:String(txt||'').slice(0,600)};
 if(usable){
  M.tot=vr1(W.tot);M.acc=vr1(W.acc);M.flu=vr1(W.flu);M.cmp=vr1(W.cmp);M.w=w;
  M.nseg=raw.length;M.az=raw.map(function(r){return [r[0]==null?null:vr1(r[0]),vr1(r[1]),vr1(r[2]),vr1(r[3]),r[4],Math.round(r[5])]})}
 return M}

/* ---- 同意の1枚(ゲーム内の紙)。ボタンは同じ大きさ。ここだけ日本語(013 3-4) ---- */
function consentCard(done){
 clearPanel();G.phase='consent';
 var card=el('div','vcons');card.appendChild(el('div','vh','声を送ってもいい？'));
 card.appendChild(el('p','','旅のはじめと、おわりに、同じ文を言います。そのときの声だけを、発音を調べるために Microsoft のサービス（Azure）に送ります。'));
 var ul=el('ul');
 ['送るのは、この2回だけ。ほかの場面の声は、このサービスには送りません。（ほかの場面では、ブラウザの音声認識が声を文字にします。Chrome なら Google、Safari なら Apple のサービスです。）',
  'ゲームは声を保存しません。Microsoft は、この方法では声を保存しないと説明しています。',
  '結果は、この端末の中だけに残ります。',
  '送らなくても、ゲームは最後まで同じように遊べます。いつでも、設定で変えられます。'].forEach(function(t){ul.appendChild(el('li','',t))});
 card.appendChild(ul);panel.appendChild(card);
 var row=el('div','row cuerow'),ok=el('button','btn sub','送ってOK'),no=el('button','btn sub','送らない'),used=false;
 [ok,no].forEach(function(b){b.type='button'});
 function pick(v){if(used)return;used=true;voiceSetConsent(v);done()}
 ok.addEventListener('click',function(){pick(true)});no.addEventListener('click',function(){pick(false)});
 row.appendChild(ok);row.appendChild(no);panel.appendChild(row)}

/* ---- せってい: 「こえの おくりさき」(切り替え・記録を消す) ---- */
function voiceSetSection(b){
 var s=sSec('こえの おくりさき');
 if(voiceRelayOn()){
  var r=el('div','stg'),tx=el('div','tx');tx.appendChild(el('div','tt','こえを Microsoft に おくる'));
  tx.appendChild(el('div','dd','はじめと おわりの せんげん(2かい)だけ。ほかの ばめんでは おくりません'));
  var tg=el('button','tgl');tg.type='button';tg.setAttribute('aria-label','こえを おくる');tg.setAttribute('aria-pressed',voiceConsent()===true?'true':'false');
  tg.addEventListener('click',function(){var nv=voiceConsent()!==true;voiceSetConsent(nv);tg.setAttribute('aria-pressed',nv?'true':'false')});
  r.appendChild(tx);r.appendChild(tg);s.appendChild(r)}
 var cl=el('button','btn sub','こえの きろくを けす'),armed=false;cl.type='button';
 cl.addEventListener('click',function(){
  if(!armed){armed=true;cl.textContent='ほんとうに けす？ もういちど おす';setTimeout(function(){if(armed){armed=false;cl.textContent='こえの きろくを けす'}},4000);return}
  voiceClear();armed=false;cl.textContent='けしました'});
 s.appendChild(cl);s.appendChild(el('div','dd2','はじめと おわりを くらべる きろくだけ けします。ほかの はつおんの きろくは そのままです'));
 b.appendChild(s)}

/* ---- Azure で読む長いカンペ(宣言)。見た目と進み方は setupDiag(ブラウザの音声認識)と同じ。使えないときは、そちらにかえる ---- */
function setupDiagAz(act,stat,toks,spans,T,card){
 var sid=G.sid,tg=toks.map(function(k){return k.txt}),ref=tg.join(' '),heardEl=el('div','heard',''),IDLE='🎤 もういちど',
  H=null,listening=false,starting=false,fin=false,segs=[],lastInt='',lastAt=0,silent=0,t0=Date.now(),tick=0;
 card.appendChild(heardEl);
 function alive(){return G.sid===sid&&G.view==='scene'&&!fin}
 function setIdle(){listening=false;act.classList.remove('down');act.textContent=IDLE}
 function segTxt(){return segs.map(function(s){return s.text}).join(' ')}
 function heardTxt(){return segTxt()+(lastInt?' '+lastInt:'')}
 function hl(){var r=analyze(tg,heardTxt()),last=-1;r.words.forEach(function(w,i){if(w.ok&&w.h!=null)last=i});spans.forEach(function(s,i){s.classList.toggle('on',i===last)})}
 function enough(){var r=analyze(tg,segTxt()),n=r.words.length;return r.ratio>=.97||(r.okN>=n*.5&&r.words.slice(-3).every(function(w){return w.ok}))}
 function kill(){clearInterval(tick);if(H){var h0=H;H=null;h0.abort()}Snd.duck(0)}
 function toSR(why){   /* Azure をやめて、ブラウザの音声認識で続ける(通信できない・SDKが読めない・認証が通らない) */
  if(fin)return;fin=true;kill();listening=false;starting=false;G.azFail=String(why||1).slice(0,40);
  var a2=act.cloneNode(false);a2.className='btn';a2.textContent=IDLE;if(act.parentNode)act.parentNode.replaceChild(a2,act);
  if(heardEl.parentNode)heardEl.parentNode.removeChild(heardEl);
  if(SR){setupDiag(a2,stat,toks,spans,T,card);if(G.kick)later(300,G.kick);return}
  if(G.onBlocked){var ob=G.onBlocked;G.onBlocked=null;ob('azure');return}
  setupActionTimer(a2,stat,toks,spans,T);card.appendChild(el('div','heard nomic','マイクが使えません'))}
 function finish(why){
  if(fin)return;fin=true;listening=false;act.disabled=true;clearInterval(tick);var h0=H;H=null;
  function go(){
   Snd.duck(0);
   var txt=segTxt().trim(),res=analyze(tg,txt),M=voiceBuildM(tg,segs,txt,res);
   /* 判定。始め・終わりの宣言は今までどおり(聞き取れたか)。窓口の読み返しだけ、Azure の単語ごとの正確さも使う */
   var judge=T.diag==='readback'&&RB_AZ_JUDGE&&M.src==='az'&&M.w&&M.w.length===res.words.length,bits=M.bits,okN=res.okN,miss=[];
   if(judge){bits='';res.words.forEach(function(w,i){
    var low=w.ok&&M.w[i][1]!=null&&M.w[i][1]<AZ_BAD,ok=w.ok&&!low;bits+=ok?'1':'0';if(low)okN--;
    if(!ok&&miss.length<40)miss.push({t:missKey(w.t),h:w.h,k:low?'az':w.k})})}
   else miss=res.words.filter(function(w){return !w.ok}).slice(0,40).map(function(w){return {t:missKey(w.t),h:w.h,k:w.k}});
   var rec={ts:M.ts,v:G.scene?G.scene.vid:'',tg:tg.join(' '),hd:txt.slice(0,600),cf:0,ok:okN,n:res.n,miss:miss,
    diag:T.diag,why:why,seg:segs.length,bits:bits,alts:[],src:M.src};
   if(M.src==='az'){rec.nv=M.nv;rec.sc=[M.tot,M.acc,M.flu,M.cmp]}   /* Azure の4つの値(総合・正確さ・流れ・言い切り度) */
   plogAdd(rec);
   if(voiceCmpDiag(T.diag))voiceSetM(T.diag,M);
   card.classList.add('shown');heardEl.className='heard fin';heardEl.textContent=txt||'…';
   later(Math.min(6500,2600+txt.length*16),diagDone)}
  if(h0)h0.stop(go);else go()}
 function start(){
  if(fin||listening||starting)return;stopSay();starting=true;heardEl.className='heard live';heardEl.textContent='…';stat.className='stat';stat.textContent='';
  Snd.duck(1);lastAt=Date.now();
  H=voiceAzStart(ref,{
   started:function(){starting=false;if(!alive())return;listening=true;lastAt=Date.now();act.classList.add('down');act.textContent='きいてます…'},
   live:function(tx){if(!alive())return;lastInt=tx;lastAt=Date.now();heardEl.textContent=heardTxt();hl()},
   seg:function(sg){if(!alive())return;segs.push(sg);lastInt='';lastAt=Date.now();silent=0;heardEl.textContent=heardTxt();hl();if(enough())finish('enough')},
   canceled:function(){if(!alive())return;if(segs.length)finish('cancel');else toSR('canceled')},
   fail:function(e){starting=false;if(!alive())return;toSR(e)}});
  clearInterval(tick);
  tick=setInterval(function(){
   if(!alive()||!listening)return;var now=Date.now();
   if(now-t0>110000||(segs.length&&now-lastAt>9000)){finish(segs.length?'silence':'none');return}
   if(!segs.length&&now-lastAt>15000){silent++;kill();setIdle();starting=false;if(silent>=2){finish('none');return}later(300,function(){if(alive())start()})}},500)}
 G.kick=function(){if(G.phase==='cue'&&alive()&&!listening&&!starting&&act.isConnected)start()};
 G.mute=function(){kill();listening=false;starting=false;segs=[];lastInt='';silent=0;t0=Date.now();if(act.isConnected)setIdle();heardEl.textContent=''};
 act.addEventListener('click',function(){
  if(fin)return;
  if(listening||starting){
   if(segs.length||lastInt){if(!segs.length)segs.push({text:String(lastInt).trim(),pa:null,words:[]});lastInt='';finish('manual')}
   else{kill();starting=false;setIdle()}
   return}
  start()});
 act.addEventListener('contextmenu',function(e){e.preventDefault()});
 stat.className='stat';stat.textContent=''}
