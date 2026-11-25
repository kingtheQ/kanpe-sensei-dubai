/* ===== 英会話カフェの5分自由会話(タスク073) =====
   台本パート(5往復)が終わったあと、先生が英語で自由会話に誘う。承諾すると5分、先生と声で話す。
   ・入るのは場面データに freetalk=1 がある場面(nbo_eikaiwa1)だけ。音声認識のないブラウザと「こえをださないモード」(PREF.silent)では誘わない。
   ・聞き取り=ブラウザ標準の SpeechRecognition(en-US。既存エンジンの作法)。先生の読み上げ=既存の say()。返事=中継(relay/worker.js)の POST /chat。キーはゲームに置かない。
   ・自由会話中は、カンペを出さない・発音の数値判定(Azure評価)を使わない・日本語を出さない・数字や時間の文字を出さない。残り時間はカップのコーヒーが減る絵(art.js の artCup)だけ。
   ・新しい保存キーは作らない。会話の履歴・残り時間はこの中(メモリ)だけ。場面を出たら全部消える。
   ・/chat が未設定・失敗のとき、聞き取れない・無音が続くときは、エラーを出さず、先生の穏やかな締めの台詞で終える。
   タスク079(キングの実機フィードバック。カフェ=予行練習の場に限った設計変更):
   ・聞き取りは continuous=true。final を蓄積し、セッションが切れても(話し終わっていなければ)自動で再開する。送るのは「最後の発話から約2.8秒の沈黙」か「🎤タップ=言い終わり」のときだけ。言いかけの文は履歴に入れない。
   ・/chat の応答 {reply, fix}。fix(直した1文)があるときは会話を進めず、先生がお手本として読み上げ→本人が言い直す(ゆるい一致でOK・2回合わなければ先生がもう一度お手本を言って進む)。fix がない/旧形式の応答は今までどおり。
   ・聞き取り中は🎤が脈打つ。先生の考え中(/chat 待ち)は先生の吹き出しに「…」。 */
var FT=(function(){
 var LIMIT=300000,MAXTURN=30,SILMAX=3,MISSMAX=3,CHATWAIT=15000,LISTENWAIT=14000,SILENCE=2800,CAPMS=45000,RESTARTMAX=40;
 /* 先生の台詞(全部、簡単な英語。日本語は出さない) */
 var L={
  invite:'We still have some time. Would you like to chat a little more?',
  yes:"Yes, let's chat.",no:'No, I should go now.',
  open:"Great! Let's talk. What did you do today?",
  decline:"That's okay. Thank you for coming today. Please come again!",
  time:['Oh, look at the time. The coffee is almost gone, and so is our time. I really enjoyed this. See you again!',
        'Oh, the cup is empty now. That was a lot of fun. Thank you for the nice talk. See you again!'],
  bye:'Bye-bye! It was so nice talking with you. See you again!',
  soft:'Oh, it is a little hard to hear today. Thank you for the nice talk. See you again!',
  busy:'Oh, the café is getting busy now. Thank you for the nice talk. See you again!',
  reask:['Sorry, I did not catch that. Could you say it once more?','One more time, please. A little slowly is fine.','Hmm, I missed that. What did you say?',
         'Sorry, the café is a bit noisy. Can you say that again?','I did not hear you well. Please try again.','Pardon me? Say it one more time, please.',
         'Oh, I lost you for a moment. Could you repeat that?','Sorry, say that again for me? Take your time.'],
  nudge:['Take your time. What kind of food do you like?','Let me ask you something. Do you like tea or coffee?','Here is an easy one. Where would you like to travel next?','Tell me about your day. What did you eat today?','Do you like sunny days or rainy days?',
         'No hurry. What do you like to do on weekends?','Here is a small question. What is your favorite drink?','Let me ask you this. Have you ever been on a safari?'],
  /* 言い直しの流れ(タスク079): 合わなかったときの一言・言い直せたときの一言(「正解」「点数」の言葉は使わない) */
  again:['Once more, please.','Try it one more time.','One more time. Take your time.','Your turn again. Say it slowly.','Let us try again.'],
  ack:["That's it.","Yes, that's it!",'Right, like that.','Yes, just like that.','There you go.',"That's the way."]};
 var BYE=/\b(good\s?bye|bye|see you|see ya|i have to go|i must go|i should go|gotta go|i have to leave|talk to you later)\b/i;
 var st=null,self={lines:L,limit:LIMIT,silenceMs:SILENCE,swaps:0};
 self.clock=function(){return Date.now()};   /* 時計はここ1か所(テストは偽の時計に差し替える) */
 function chatUrl(){return (typeof RELAY_URL==='string'&&/^https:\/\//.test(RELAY_URL))?RELAY_URL.replace(/\/+$/,'')+'/chat':''}
 function canTalk(){return !!SR&&!PREF.silent}
 self.want=function(S){return !!(S&&S.d&&S.d.freetalk&&canTalk())};
 /* カップの残り(1→0)。自由会話の最中だけ数を返す(それ以外は null=カップを描かない) */
 self.cup=function(){if(!st||!st.on||st.dead)return null;return Math.max(0,Math.min(1,1-(self.clock()-st.t0)/LIMIT))};
 function alive(){return !!st&&!st.dead&&G.sid===st.sid&&G.view==='scene'&&G.phase==='free'}
 function pick(a){return a[Math.floor(Math.random()*a.length)]}
 /* 直近に使った文を避けて選ぶ(聞き返し・無音の質問・言い直しの一言。連続で同じ文を出さない)。使った文はこの中(メモリ)だけに置く */
 function fresh(a){
  var u=st?st.used:[],n=Math.min(4,a.length-1),rc=u.slice(-n),c=a.filter(function(x){return rc.indexOf(x)<0}),v=pick(c.length?c:a);
  if(st){u.push(v);if(u.length>12)u.shift()}return v}
 self.fresh=fresh;
 function pushHist(role,text){var h=st.hist,last=h[h.length-1];text=String(text||'').replace(/\s+/g,' ').trim();if(!text)return;
  if(last&&last.role===role)last.content=(last.content+' '+text).slice(0,200);else h.push({role:role,content:text.slice(0,200)});
  if(h.length>40)h.splice(0,h.length-40)}
 /* 聞き取りの部品。micOff=🎤の脈打ちを止める / abortRec=認識を捨てる(画面の表示は触らない=再開で「聞いてない」ように見えない) / clearSil=沈黙の計時を全部止める */
 function micOff(){if(st&&st.mic){st.mic.classList.remove('down');st.mic.classList.remove('ftlisten')}}
 function clearSil(){if(!st)return;if(st.sT){clearTimeout(st.sT);st.sT=0}if(st.capT){clearTimeout(st.capT);st.capT=0}if(st.noT){clearTimeout(st.noT);st.noT=0}}
 function abortRec(){if(st&&st.rec){var r=st.rec;st.rec=null;try{r.abort()}catch(e){}}}
 function killRec(){clearSil();abortRec();micOff()}
 function killNet(){if(st){st.tok++;if(st.ac){try{st.ac.abort()}catch(e){}st.ac=null}}}
 function cleanup(s){s=s||st;if(!s)return;s.dead=1;s.on=0;if(s.rec){try{s.rec.abort()}catch(e){}s.rec=null}s.tok++;if(s.ac){try{s.ac.abort()}catch(e){}s.ac=null}
  if(s.sT)clearTimeout(s.sT);if(s.capT)clearTimeout(s.capT);if(s.noT)clearTimeout(s.noT);s.sT=s.capT=s.noT=0;s.hist=[];s.used=[];s.redo=null;s.buf='';s.interim='';if(s.guard)clearInterval(s.guard);if(st===s)st=null}
 /* 先生の台詞を出して読み上げる。読み終わったら done */
 function teacherSays(text,done,noHist){
  if(!alive())return;st.mode='say';if(!noHist)pushHist('assistant',text);
  clearInterval(G.typeTimer);npcMsg(text,whoNow());spSay=true;
  say(text,.95,st.S.pitch,gd(function(){spSay=false;if(!alive())return;if(done)done()}))}
 /* ---- 誘い(台本パートが終わったあと) ---- */
 self.end=function(){
  var S=G.scene;if(!self.want(S)){finishScene();return}
  clearPanel();G.phase='free';G.kick=null;G.mute=null;self.swaps=0;
  var me=st={sid:G.sid,S:S,hist:[],used:[],on:0,t0:0,mode:'offer',tok:0,sil:0,miss:0,turns:0,closing:0,expired:0,rec:null,ac:null,mic:null,heard:null,fixEl:null,dead:0,
   buf:'',interim:'',spoke:false,restarts:0,sT:0,capT:0,noT:0,redo:null,seq:0};
  me.guard=setInterval(function(){if(st!==me||!alive())cleanup(me)},400);   /* 場面を出たら、聞き取り・通信・履歴を全部捨てる */
  teacherSays(L.invite,function(){later(250,showChoice)},1)};
 function showChoice(){
  if(!alive())return;st.mode='offer';clearPanel();
  var box=el('div','dqbox'),bs=[],sid=G.sid;
  [[L.yes,go],[L.no,declined]].forEach(function(o){var b=el('button','dq');b.type='button';b.appendChild(el('span','cur','▶'));b.appendChild(el('span','',o[0]));
   b.addEventListener('click',function(){if(!alive()||st.mode!=='offer')return;st.mode='picked';stopSay();spSay=false;o[1]()});box.appendChild(b);bs.push(b)});
  panel.appendChild(box);
  function sel(i){bs.forEach(function(b,j){b.classList.toggle('sel',j===i)})}
  bs.forEach(function(b,i){['focus','pointerenter','pointerdown'].forEach(function(ev){b.addEventListener(ev,function(){sel(i)})})});
  sel(0);
  (function rd(i){if(G.sid!==sid||!alive()||st.mode!=='offer'||i>=bs.length)return;sel(i);say(i?L.no:L.yes,.9,1,gd(function(){later(300,function(){if(alive()&&st.mode==='offer')rd(i+1)})}))})(0)}
 function declined(){closeWith(L.decline)}
 /* ---- 5分の自由会話 ---- */
 function go(){
  st.on=1;st.t0=self.clock();ui();tick();
  teacherSays(L.open,function(){later(200,listen)})}
 function ui(){
  clearPanel();var box=el('div','ftbox'),hb=el('div','ftheard',''),fx=el('div','ftfix',''),row=el('div','row'),mic=el('button','btn','🎤'),by=el('button','btn sub','Bye');
  mic.type='button';mic.setAttribute('aria-label','Speak');by.type='button';by.setAttribute('aria-label','Bye');
  mic.addEventListener('click',function(){if(!alive()||st.closing)return;
   /* 聞いている最中のタップ=「言い終わり」。たまった言葉があればすぐ送る。何も話していなければ聞き直す(最初から) */
   if(st.mode==='listen'){if(!submitNow()){abortRec();clearSil();st.buf='';st.interim='';st.heard.textContent='…';armNo();startRec()}return}
   if(st.mode==='say'&&!st.seq){stopSay();spSay=false;listen()}});
  by.addEventListener('click',function(){byeFlow()});
  row.appendChild(mic);row.appendChild(by);box.appendChild(hb);box.appendChild(fx);box.appendChild(row);panel.appendChild(box);st.heard=hb;st.fixEl=fx;st.mic=mic}
 function expired(){return !!st&&st.on&&self.clock()-st.t0>=LIMIT}
 function tick(){
  if(!alive())return;
  if(!st.closing&&expired()){if(st.mode==='listen'||st.mode==='think')closeTime();else st.expired=1}
  later(500,tick)}
 function closeTime(){closeWith(pick(L.time))}
 /* ---- 聞く(タスク079: continuous。自動で聞き始める。話している途中は送らない) ---- */
 function curText(){return String((st.buf||'')+' '+(st.interim||'')).replace(/\s+/g,' ').trim()}
 function showHeard(){st.heard.className='ftheard live';st.heard.textContent=curText()||'…'}
 function listen(){
  if(!alive()||st.closing)return;
  if(st.expired||expired()||st.turns>=MAXTURN){closeTime();return}
  stopSay();spSay=false;killRec();st.mode='listen';st.seq=0;st.buf='';st.interim='';st.spoke=false;st.restarts=0;
  st.heard.className='ftheard live';st.heard.textContent='…';
  if(st.mic){st.mic.classList.add('down');st.mic.classList.add('ftlisten')}
  armNo();startRec()}
 /* 何も話さないまま長く続いたら、無音として扱う(話し始めたら止める) */
 function armNo(){if(st.noT)clearTimeout(st.noT);st.noT=later(LISTENWAIT,function(){if(alive()&&st.mode==='listen'&&!curText()){var sp=st.spoke;abortRec();clearSil();if(sp)missed();else silent()}})}
 /* 沈黙の計時: 話が続いている間(途中経過も含む)は伸ばし続け、止まって約2.8秒たったら送る */
 function armSil(){
  if(st.sT)clearTimeout(st.sT);
  st.sT=setTimeout(function(){st.sT=0;submitNow()},self.silenceMs);
  if(!st.capT)st.capT=setTimeout(function(){st.capT=0;submitNow()},CAPMS)}   /* 話し続けて45秒たったら、そこまでを送る */
 /* たまった言葉を送る。送れる言葉がなければ false */
 function submitNow(){
  if(!alive()||st.mode!=='listen'||st.closing)return false;
  var txt=curText();if(!txt||!/[A-Za-z0-9]/.test(txt))return false;
  killRec();gotText(txt);return true}
 function startRec(){
  if(!alive()||st.closing||st.mode!=='listen')return;
  var r;try{r=new SR()}catch(e){closeWith(L.soft);return}
  st.rec=r;var err='',my=r;
  r.lang='en-US';r.interimResults=true;r.maxAlternatives=1;r.continuous=true;
  try{r.onspeechstart=function(){if(st&&st.rec===my)st.spoke=true}}catch(e){}
  r.onresult=function(ev){
   if(!st||st.rec!==my)return;if(!alive()){try{my.abort()}catch(e){}return}
   var i,it='';st.spoke=true;
   for(i=ev.resultIndex||0;i<ev.results.length;i++){
    var rs=ev.results[i],t=String(rs[0]&&rs[0].transcript||'').replace(/\s+/g,' ').trim();if(!t)continue;
    if(rs.isFinal)addFinal(t);else it+=(it?' ':'')+t}
   st.interim=it;
   if(curText()){if(st.noT){clearTimeout(st.noT);st.noT=0}showHeard();armSil()}};
  r.onerror=function(ev){err=(ev&&ev.error)||'error'};
  r.onend=function(){
   if(!alive()||st.rec!==my)return;st.rec=null;
   if(err==='not-allowed'||err==='service-not-allowed'||err==='audio-capture'){closeWith(L.soft);return}
   if(st.mode!=='listen')return;
   /* セッションが切れただけ(Chrome は短い沈黙で切る)。言葉がたまっていれば、本人はまだ話し終わっていない → 表示はそのまま、すぐ聞き直す */
   if(curText()){
    if(++st.restarts>RESTARTMAX){submitNow();return}
    later(80,function(){if(alive()&&st.mode==='listen'&&!st.rec)startRec()});return}
   if(!st.spoke||err==='no-speech')silent();else missed()};
  try{r.start()}catch(e){st.rec=null;closeWith(L.soft)}}
 /* final を足す。端末によっては final が「ここまで全部」の形で重ねて届く(Android の Chrome)ので、同じ文を二度足さない */
 function addFinal(t){
  var b=st.buf||'',lb=b.toLowerCase(),lt=t.toLowerCase();
  if(b&&lt.indexOf(lb)===0&&lt.length>lb.length){st.buf=t;return}
  if(b&&(lb===lt||lb.slice(-lt.length)===lt))return;
  st.buf=(b?b+' ':'')+t}
 function afterReask(){if(!alive())return;later(250,listen)}
 /* 無音が続く: 先生から軽い質問を投げ直す。数回続けば穏やかに締める。言い直しの最中は、質問ではなく「もう一度」と促す */
 function silent(){
  if(!alive()||st.closing)return;st.heard.className='ftheard';st.heard.textContent='';
  if(st.redo){redoQuiet();return}
  st.sil++;
  if(st.sil>=SILMAX){closeWith(L.soft);return}
  teacherSays(fresh(L.nudge),afterReask)}
 /* 聞き取れなかった: 先生が自然な英語で聞き返す(毎回ちがう文)。数回続けば穏やかに締める */
 function missed(){
  if(!alive()||st.closing)return;st.heard.className='ftheard';st.heard.textContent='';
  if(st.redo){redoQuiet();return}
  st.miss++;
  if(st.miss>=MISSMAX){closeWith(L.soft);return}
  teacherSays(fresh(L.reask),afterReask)}
 /* 聞こえた: 認識結果をそのまま吹き出しで見せる(日本語訳は出さない・数値の判定もしない) */
 function gotText(txt){
  txt=txt.slice(0,200);st.sil=0;st.miss=0;st.heard.className='ftheard done';st.heard.textContent=txt;micOff();
  if(st.redo){judgeRedo(txt);return}
  pushHist('user',txt);st.said=txt;
  if(txt.split(' ').length<=6&&BYE.test(txt)){st.closing=1;killRec();killNet();teacherSays(L.bye,function(){later(700,fin)},1);return}   /* 「Bye」と言われたら、先生が自然に返して終わる(AIは呼ばない) */
  st.turns++;ask()}
 /* 返事を作る(中継の POST /chat)。失敗したら穏やかに締める。先生の考え中は吹き出しに「…」(🎤の脈打ちは止まっている) */
 function ask(){
  if(!alive())return;st.mode='think';var url=chatUrl();micOff();
  if(!url){closeWith(L.busy);return}
  clearInterval(G.typeTimer);setMsgInstant('…',whoNow());spSay=false;
  var my=++st.tok,ac=(typeof AbortController!=='undefined')?new AbortController():null;st.ac=ac;
  later(CHATWAIT,function(){if(alive()&&st.tok===my&&st.mode==='think'){if(ac){try{ac.abort()}catch(e){}}closeWith(L.busy)}});
  var h=st.hist.slice(-12).map(function(m){return {role:m.role,content:m.content}});
  fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:h}),cache:'no-store',signal:ac?ac.signal:undefined})
   .then(function(r){if(!r.ok)throw new Error('http');return r.json()})
   .then(function(j){
    if(!alive()||st.tok!==my||st.closing)return;
    var rep=tidy(j&&j.reply);if(!rep)throw new Error('empty');
    var fx=tidyFix(j&&j.fix,st.said);   /* 旧形式(fix なし)・fix が空・使えない fix は、今までどおりすぐ会話を進める */
    if(expired()){closeTime();return}
    if(fx)startRedo(fx,rep);else speakReply(rep)})
   .catch(function(){if(alive()&&st.tok===my&&!st.closing)closeWith(L.busy)})}
 function speakReply(rep){
  if(!alive()||st.closing)return;
  if(expired()){closeTime();return}
  st.seq=0;hideFix();
  teacherSays(rep,function(){if(st.expired||expired())closeTime();else later(250,listen)})}
 /* ---- 言い直し(タスク079): はっきりした間違いのときだけ。お手本(先生が読む)→本人が言い直す→先生が短く受けて、reply で会話が続く ----
    ・ゆるい一致でOK(単語の7割ほど。1文字ちがいの聞き間違いは同じ語とみなす)。2回合わなければ、先生がもう一度お手本を言って会話を進める。点数・「間違い」の言葉・ラベルは出さない。 */
 function startRedo(fx,rep){
  st.redo={fix:fx,rep:rep,tries:0,quiet:0};
  if(st.fixEl)st.fixEl.textContent=fx;
  teacherSays(fx,function(){later(300,listen)},1)}
 function hideFix(){if(st&&st.fixEl)st.fixEl.textContent=''}
 function judgeRedo(txt){
  var R=st.redo;
  if(self.match(R.fix,txt)){   /* 言い直せた: 先生が短く受けて、reply から会話が続く */
   st.redo=null;st.seq=1;teacherSays(fresh(L.ack),function(){later(200,function(){speakReply(R.rep)})},1);return}
  R.tries++;
  if(R.tries>=2){giveModel();return}
  teacherSays(fresh(L.again),function(){later(250,listen)},1)}
 /* 2回合わない・声が出ない: 止めずに、先生がもう一度お手本を言って、そのまま会話を進める */
 function giveModel(){
  var R=st.redo;st.redo=null;st.seq=1;
  teacherSays(R.fix,function(){later(300,function(){speakReply(R.rep)})},1)}
 function redoQuiet(){
  var R=st.redo;R.quiet++;
  if(R.quiet>=2){giveModel();return}
  teacherSays(fresh(L.again),function(){later(250,listen)},1)}
 /* 言い直しの一致判定(ゆるい): 直した文の単語の7割ほど(短い文は全部)が、言った言葉の中にあればよい。冠詞の抜け・前置き・1文字の聞き違いは許す。完全一致は求めない */
 function words(t){return String(t||'').toLowerCase().replace(/[’‘]/g,"'").replace(/[^a-z0-9' ]+/g,' ').replace(/'/g,'').split(/\s+/).filter(Boolean)}
 function lev(a,b){var m=a.length,n=b.length,d=[],i,j;for(i=0;i<=m;i++){d[i]=[i]}for(j=1;j<=n;j++)d[0][j]=j;
  for(i=1;i<=m;i++)for(j=1;j<=n;j++)d[i][j]=Math.min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+(a.charAt(i-1)===b.charAt(j-1)?0:1));return d[m][n]}
 function sameWord(a,b){return a===b||(a.length>=4&&b.length>=4&&lev(a,b)<=1)}
 self.match=function(fix,said){
  var f=words(fix),s=words(said);if(!f.length||!s.length)return false;
  var used=[],hit=0;
  f.forEach(function(w){for(var i=0;i<s.length;i++){if(!used[i]&&sameWord(w,s[i])){used[i]=1;hit++;return}}});
  var need=f.length<=3?f.length:Math.ceil(f.length*.7-1e-9);   /* 3語以下は全部・それより長い文は7割(切り上げ) */
  return hit>=need&&hit/s.length>=.5};
 /* 先生の返事を整える: 日本語が混ざっていたら使わず(先生の軽い質問に差し替える。差し替えた回数は FT.swaps に残す)、絵文字や記号は落とす。空なら失敗として扱う */
 function tidy(t){
  if(typeof t!=='string')return '';
  if(/[　-鿿豈-﫿＀-￯]/.test(t)){self.swaps++;return fresh(L.nudge)}
  t=t.replace(/[^\x20-\x7e‘’“”–—…]/g,'').replace(/\s+/g,' ').trim();
  return t.length>=2?t.slice(0,360):''}
 /* 直した文を整える: 日本語・記号・短すぎ・本人の発言と同じ、のものは「なし」にする(=すぐ会話を進める) */
 function tidyFix(t,said){
  if(typeof t!=='string')return '';
  if(/[　-鿿豈-﫿＀-￯]/.test(t))return '';
  t=t.replace(/[^\x20-\x7e‘’“”–—…]/g,'').replace(/\s+/g,' ').trim();
  if(t.length<3||words(t).length<2)return '';
  if(words(t).join(' ')===words(said).join(' '))return '';
  return t.slice(0,200)}
 /* ---- 終わり方(どれも先生の穏やかな台詞のあと、場面が終わる) ---- */
 function closeWith(line){
  if(!alive()||st.closing)return;st.closing=1;st.redo=null;killRec();killNet();clearPanel();
  teacherSays(line,function(){later(700,fin)},1)}
 function fin(){if(!alive())return;var s=st;cleanup(s);spSay=false;finishScene()}
 function byeFlow(){if(!alive()||st.closing||!st.on)return;st.hist.length=0;closeWith(L.bye)}
 /* 場面を出る ✕ ボタン: 自由会話の最中は、先生が「バイバイ」に返してから出る。誘いの最中・締めの最中は、いつもどおりすぐ出る */
 self.exit=function(){if(alive()&&st.on&&!st.closing){byeFlow();return true}return false};
 return self})();
