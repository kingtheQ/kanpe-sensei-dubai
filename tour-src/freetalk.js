/* ===== 英会話カフェの5分自由会話(タスク073) =====
   台本パート(5往復)が終わったあと、先生が英語で自由会話に誘う。承諾すると5分、先生と声で話す。
   ・入るのは場面データに freetalk=1 がある場面(nbo_eikaiwa1)だけ。音声認識のないブラウザと「こえをださないモード」(PREF.silent)では誘わない。
   ・聞き取り=ブラウザ標準の SpeechRecognition(en-US。既存エンジンの作法)。先生の読み上げ=既存の say()。返事=中継(relay/worker.js)の POST /chat。キーはゲームに置かない。
   ・自由会話中は、カンペを出さない・発音の数値判定(Azure評価)を使わない・日本語を出さない・数字や時間の文字を出さない。残り時間はカップのコーヒーが減る絵(art.js の artCup)だけ。
   ・新しい保存キーは作らない。会話の履歴・残り時間はこの中(メモリ)だけ。場面を出たら全部消える。
   ・/chat が未設定・失敗のとき、聞き取れない・無音が続くときは、エラーを出さず、先生の穏やかな締めの台詞で終える。 */
var FT=(function(){
 var LIMIT=300000,MAXTURN=30,SILMAX=3,MISSMAX=3,CHATWAIT=15000,LISTENWAIT=14000;
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
  reask:['Sorry, I did not catch that. Could you say it once more?','One more time, please. A little slowly is fine.','Hmm, I missed that. What did you say?'],
  nudge:['Take your time. What kind of food do you like?','Let me ask you something. Do you like tea or coffee?','Here is an easy one. Where would you like to travel next?','Tell me about your day. What did you eat today?','Do you like sunny days or rainy days?']};
 var BYE=/\b(good\s?bye|bye|see you|see ya|i have to go|i must go|i should go|gotta go|i have to leave|talk to you later)\b/i;
 var st=null,self={lines:L,limit:LIMIT};
 self.clock=function(){return Date.now()};   /* 時計はここ1か所(テストは偽の時計に差し替える) */
 function chatUrl(){return (typeof RELAY_URL==='string'&&/^https:\/\//.test(RELAY_URL))?RELAY_URL.replace(/\/+$/,'')+'/chat':''}
 function canTalk(){return !!SR&&!PREF.silent}
 self.want=function(S){return !!(S&&S.d&&S.d.freetalk&&canTalk())};
 /* カップの残り(1→0)。自由会話の最中だけ数を返す(それ以外は null=カップを描かない) */
 self.cup=function(){if(!st||!st.on||st.dead)return null;return Math.max(0,Math.min(1,1-(self.clock()-st.t0)/LIMIT))};
 function alive(){return !!st&&!st.dead&&G.sid===st.sid&&G.view==='scene'&&G.phase==='free'}
 function pick(a){return a[Math.floor(Math.random()*a.length)]}
 function pushHist(role,text){var h=st.hist,last=h[h.length-1];text=String(text||'').replace(/\s+/g,' ').trim();if(!text)return;
  if(last&&last.role===role)last.content=(last.content+' '+text).slice(0,200);else h.push({role:role,content:text.slice(0,200)});
  if(h.length>40)h.splice(0,h.length-40)}
 function killRec(){if(st&&st.rec){var r=st.rec;st.rec=null;try{r.abort()}catch(e){}}if(st&&st.mic)st.mic.classList.remove('down')}
 function killNet(){if(st){st.tok++;if(st.ac){try{st.ac.abort()}catch(e){}st.ac=null}}}
 function cleanup(s){s=s||st;if(!s)return;s.dead=1;s.on=0;if(s.rec){try{s.rec.abort()}catch(e){}s.rec=null}s.tok++;if(s.ac){try{s.ac.abort()}catch(e){}s.ac=null}s.hist=[];if(s.guard)clearInterval(s.guard);if(st===s)st=null}
 /* 先生の台詞を出して読み上げる。読み終わったら done */
 function teacherSays(text,done,noHist){
  if(!alive())return;st.mode='say';if(!noHist)pushHist('assistant',text);
  clearInterval(G.typeTimer);npcMsg(text,whoNow());spSay=true;
  say(text,.95,st.S.pitch,gd(function(){spSay=false;if(!alive())return;if(done)done()}))}
 /* ---- 誘い(台本パートが終わったあと) ---- */
 self.end=function(){
  var S=G.scene;if(!self.want(S)){finishScene();return}
  clearPanel();G.phase='free';G.kick=null;G.mute=null;
  var me=st={sid:G.sid,S:S,hist:[],on:0,t0:0,mode:'offer',tok:0,sil:0,miss:0,turns:0,closing:0,expired:0,rec:null,ac:null,mic:null,heard:null,dead:0};
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
  clearPanel();var box=el('div','ftbox'),hb=el('div','ftheard',''),row=el('div','row'),mic=el('button','btn','🎤'),by=el('button','btn sub','Bye');
  mic.type='button';mic.setAttribute('aria-label','Speak');by.type='button';by.setAttribute('aria-label','Bye');
  mic.addEventListener('click',function(){if(!alive()||st.closing)return;
   if(st.mode==='listen'){if(st.rec){try{st.rec.stop()}catch(e){}}return}
   if(st.mode==='say'){stopSay();spSay=false;listen()}});
  by.addEventListener('click',function(){byeFlow()});
  row.appendChild(mic);row.appendChild(by);box.appendChild(hb);box.appendChild(row);panel.appendChild(box);st.heard=hb;st.mic=mic}
 function expired(){return !!st&&st.on&&self.clock()-st.t0>=LIMIT}
 function tick(){
  if(!alive())return;
  if(!st.closing&&expired()){if(st.mode==='listen'||st.mode==='think')closeTime();else st.expired=1}
  later(500,tick)}
 function closeTime(){closeWith(pick(L.time))}
 /* 聞く(自動で聞き始める。🎤 でも聞き直せる) */
 function listen(){
  if(!alive()||st.closing)return;
  if(st.expired||expired()||st.turns>=MAXTURN){closeTime();return}
  stopSay();spSay=false;killRec();st.mode='listen';st.heard.className='ftheard live';st.heard.textContent='…';
  var r;try{r=new SR()}catch(e){closeWith(L.soft);return}
  st.rec=r;var got=false,spoke=false,err='',last='',finalTxt='',my=r;
  r.lang='en-US';r.interimResults=true;r.maxAlternatives=1;r.continuous=false;
  try{r.onspeechstart=function(){spoke=true}}catch(e){}
  r.onresult=function(ev){
   if(st&&st.rec!==my)return;if(!alive()){try{my.abort()}catch(e){}return}
   var rs=ev.results[ev.results.length-1],alt=rs[0];spoke=true;
   if(rs.isFinal){got=true;finalTxt=alt.transcript}else{last=alt.transcript;st.heard.textContent=last}};
  r.onerror=function(ev){err=(ev&&ev.error)||'error'};
  function ended(){
   if(!alive()||st.rec!==my)return;st.rec=null;if(st.mic)st.mic.classList.remove('down');
   var txt=String(got?finalTxt:last).replace(/\s+/g,' ').trim();
   if(err==='not-allowed'||err==='service-not-allowed'||err==='audio-capture'){closeWith(L.soft);return}
   if(txt&&/[A-Za-z0-9]/.test(txt)){heard(txt);return}
   if(!spoke||err==='no-speech')silent();else missed()}
  r.onend=ended;
  if(st.mic)st.mic.classList.add('down');
  try{r.start()}catch(e){st.rec=null;if(st.mic)st.mic.classList.remove('down');closeWith(L.soft);return}
  later(LISTENWAIT,function(){if(alive()&&st.rec===my){try{my.abort()}catch(e){}ended()}})}
 function afterReask(){if(!alive())return;later(250,listen)}
 /* 無音が続く: 先生から軽い質問を投げ直す。数回続けば穏やかに締める */
 function silent(){
  if(!alive())return;st.heard.className='ftheard';st.heard.textContent='';st.sil++;
  if(st.sil>=SILMAX){closeWith(L.soft);return}
  teacherSays(pick(L.nudge),afterReask)}
 /* 聞き取れなかった: 先生が自然な英語で聞き返す。数回続けば穏やかに締める */
 function missed(){
  if(!alive())return;st.heard.className='ftheard';st.heard.textContent='';st.miss++;
  if(st.miss>=MISSMAX){closeWith(L.soft);return}
  teacherSays(L.reask[Math.min(st.miss-1,L.reask.length-1)],afterReask)}
 /* 聞こえた: 認識結果をそのまま吹き出しで見せる(日本語訳は出さない・数値の判定もしない) */
 function heard(txt){
  txt=txt.slice(0,200);st.sil=0;st.miss=0;st.heard.className='ftheard done';st.heard.textContent=txt;
  pushHist('user',txt);
  if(txt.split(' ').length<=6&&BYE.test(txt)){st.closing=1;killRec();killNet();teacherSays(L.bye,function(){later(700,fin)},1);return}   /* 「Bye」と言われたら、先生が自然に返して終わる(AIは呼ばない) */
  st.turns++;ask()}
 /* 返事を作る(中継の POST /chat)。失敗したら穏やかに締める */
 function ask(){
  if(!alive())return;st.mode='think';var url=chatUrl();
  if(!url){closeWith(L.busy);return}
  setMsgInstant('…',whoNow());spSay=false;
  var my=++st.tok,ac=(typeof AbortController!=='undefined')?new AbortController():null;st.ac=ac;
  later(CHATWAIT,function(){if(alive()&&st.tok===my&&st.mode==='think'){if(ac){try{ac.abort()}catch(e){}}closeWith(L.busy)}});
  var h=st.hist.slice(-12).map(function(m){return {role:m.role,content:m.content}});
  fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:h}),cache:'no-store',signal:ac?ac.signal:undefined})
   .then(function(r){if(!r.ok)throw new Error('http');return r.json()})
   .then(function(j){
    if(!alive()||st.tok!==my||st.closing)return;
    var rep=tidy(j&&j.reply);if(!rep)throw new Error('empty');
    if(expired()){closeTime();return}
    teacherSays(rep,function(){if(st.expired||expired())closeTime();else later(250,listen)})})
   .catch(function(){if(alive()&&st.tok===my&&!st.closing)closeWith(L.busy)})}
 /* 先生の返事を整える: 日本語が混ざっていたら使わず(先生の軽い質問に差し替える)、絵文字や記号は落とす。空なら失敗として扱う */
 function tidy(t){
  if(typeof t!=='string')return '';
  if(/[　-鿿豈-﫿＀-￯]/.test(t))return pick(L.nudge);
  t=t.replace(/[^\x20-\x7e‘’“”–—…]/g,'').replace(/\s+/g,' ').trim();
  return t.length>=2?t.slice(0,360):''}
 /* ---- 終わり方(どれも先生の穏やかな台詞のあと、場面が終わる) ---- */
 function closeWith(line){
  if(!alive()||st.closing)return;st.closing=1;killRec();killNet();clearPanel();
  teacherSays(line,function(){later(700,fin)},1)}
 function fin(){if(!alive())return;var s=st;cleanup(s);spSay=false;finishScene()}
 function byeFlow(){if(!alive()||st.closing||!st.on)return;st.hist.length=0;closeWith(L.bye)}
 /* 場面を出る ✕ ボタン: 自由会話の最中は、先生が「バイバイ」に返してから出る。誘いの最中・締めの最中は、いつもどおりすぐ出る */
 self.exit=function(){if(alive()&&st.on&&!st.closing){byeFlow();return true}return false};
 return self})();
