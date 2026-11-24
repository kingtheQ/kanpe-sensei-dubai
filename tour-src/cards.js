/* ===== 新しい会話の流れ(タスク061)。対象は d.flow2 の場面だけ(いまは nbo_java1)。他の場面は今のまま =====
   流れ: 店員が英語で話す → 選ぶのは1場面に1回(日本語の短い単語カード) → 見本の英語が音声だけで流れる(文字なし) → カンペ(文字)が出て声に出す
        → 間違えたら、ボタンなしで自動でおてほんが流れて言い直し → 発音の数値は出さず、通じたかは店員の反応で返す → 支払いは目に見える形で返す。
   M-Pesa(知らない現地のカード): タップしたら、プレイヤーが店員に「What is M-Pesa?」と聞く → 短い説明 → 支払い(分からないまま進ませない)。
   裏の反応時間(カードが出てからタップするまで)の測定と持ち越し→夢(053)は、conv.js の forkNote/noteWord をそのまま使う。画面には出さない。
   ルルの代行回数・ポイント・スパルタ教室は入れない(未決定)。詰んだときは今までのヘルプのまま。 */
function f2(){var S=G.scene;return !!(S&&S.d&&S.d.flow2&&!G.camp)}
if(typeof CT!=='undefined'){CT.mpesa=['m','pesa'];CT.empesa=['m','pesa']}   /* 音声認識が M-Pesa を1語に聞く場合の保険(実機で未確認) */
var CARDICO={card:'💳',cash:'💵',mpesa:'📱'};
/* ---- 1. 日本語の単語カード(選ぶのは1場面に1回)。読み上げない。出た時からタップまでの時間を裏で測る ---- */
function cardsOpts(T){
 G.phase='opts';clearPanel();clearInterval(G.typeTimer);msgText.textContent=npcHide()?'':T.npc;var sid=G.sid;
 var box=el('div','jcards'),t0=performance.now();
 T.opts.forEach(function(o){var b=el('button','jcard');b.type='button';b.setAttribute('data-pay',o.pay||'');
  b.appendChild(el('span','ico',CARDICO[o.pay]||''));b.appendChild(el('span','lb',o.card));
  b.addEventListener('click',function(){cardPick(T,o,performance.now()-t0)});box.appendChild(b)});
 panel.appendChild(box);
 later(LIMIT,function(){if(G.sid===sid&&G.phase==='opts'&&!T.fk){T.fk=1;forkNote(T,'timeout',LIMIT)}})}
function cardPick(T,o,ms){
 if(G.phase!=='opts')return;stopSay();var S=G.scene;
 if(!T.fk){T.fk=1;forkNote(T,ms<=fastMs()?'fast':(ms<=LIMIT?'slow':'timeout'),ms)}
 S.pick=o.pay;T.pk=o.pay;T.cue=o.y;T.cueJp=o.jp;
 if(o.then){   /* 知らない現地のカード: まず店員に聞く → 短い説明 → 支払い */
  T.rep=null;var T2={npc:o.then.n,npcJp:o.then.jp,cue:o.then.y,cueJp:o.then.yjp,rep:o.then.rep,pay:o.pay,ctx:T.ctx,pitch:T.pitch};
  S.turns.splice(G.ti+1,0,T2)}
 else{T.rep=o.rep;T.pay=o.pay}
 sampleThenCue(T)}
/* ---- 2. カードを押したら、見本の英語が音声だけで流れる(文字は出さない)→ そのあとカンペ(文字)が出る ---- */
function sampleThenCue(T){
 G.phase='sample';clearPanel();var sid=G.sid,fired=false;
 var ic=el('div','jsample','🔊');ic.setAttribute('aria-hidden','true');panel.appendChild(ic);
 function go(){if(fired||G.sid!==sid||G.phase!=='sample')return;fired=true;later(350,function(){if(G.phase==='sample')showCue()})}
 say(cueText(T.cue),.9,1,gd(go));
 later(cueText(T.cue).length*85+2600,go)}   /* 声が使えない環境でも止まらない保険 */
/* ---- 3. 間違えたとき(自動おてほん→3回目はルルが代行)は、全場面共通の onFail(土台・タスク074)が受け持つ。この場面だけの失敗の流れは持たない ---- */
/* ---- 4. 支払いの結果を目に見える形で返す: 選んだ方法で払い(カード・現金・スマホ)、コーヒーとケーキが出てくる ---- */
var PAYFX=null;
function payStart(kind,done){
 var S=G.scene;G.phase='pay';clearPanel();PAYFX={S:S,k:kind,t0:t,res:false};
 later(900,function(){try{Snd.fx('ding')}catch(e){}});
 later(1700,function(){if(PAYFX)PAYFX.res=true;try{Snd.fx('sparkle')}catch(e){}});
 later(2900,function(){if(G.phase==='pay')done()})}
function payEase(x){x=Math.max(0,Math.min(1,x));return x*x*(3-2*x)}
function payTick(P,x,y,w){   /* 支払いの終わりのしるし(✓) */
 [[0,3],[1,4],[2,3],[3,2],[4,1],[5,0]].forEach(function(q){R('#34d27b',x+q[0]*w,y+q[1]*w,w,w)})}
function payFg(){
 var P=PAYFX;if(!P||P.S!==G.scene||G.view!=='scene')return;
 var e=t-P.t0,YB=62,rx=142,ry=YB-18,ok=e>=.9&&e<1.8;
 /* カウンターの上を少し片づけて(背景の飾りのカップを隠して)、見やすい大きさで出す */
 R('#e8dcc4',140,30,80,32);
 /* カードリーダー(カウンターの上) */
 R('#2a2f3a',rx,ry,22,18);R('#6b7488',rx,ry,22,3);R('#10131f',rx+3,ry+5,16,6);R(ok||P.res?'#34d27b':'#8a93a8',rx+8,ry+13,6,3);
 if(e<1.8){
  var k=P.k;
  if(k==='card'){   /* カードをリーダーにかざす → ピッ → 戻る */
   var f=e<.7?payEase(e/.7):(e<1.2?1:1-payEase((e-1.2)/.5)),x=108+(rx-1-108)*f,y=104+(ry-14-104)*f;
   R('#f4f1e8',x,y,24,15);R('#2f5fc0',x,y+3,24,5);R('#caa84a',x+3,y+9,6,4);
   if(ok)R('#34d27b',rx+23,ry-4,5,5)}
  else if(k==='cash'){   /* お札を3枚、順にトレーにのせる */
   for(var i=0;i<3;i++){var d0=i*.18,fc=payEase((e-d0)/.6),x2=108+(rx+1-108)*fc,y2=104+(YB-10-i*3-104)*fc;if(e>=1.5)continue;
    R('#3f7f40',x2,y2,20,10);R('#5fa95a',x2+1,y2+1,18,8);R('#e8f2d0',x2+7,y2+3,6,4)}
   if(e>=.9)R('#e8f2d0',rx+23,ry-4,5,5)}
  else{   /* スマホ(M-Pesa): 画面をリーダーにかざす → ✓ → 戻る */
   var fm=e<.7?payEase(e/.7):(e<1.3?1:1-payEase((e-1.3)/.5)),x3=108+(rx+5-108)*fm,y3=108+(ry-22-108)*fm;
   R('#1d2330',x3,y3,13,22);R('#34c46a',x3+1,y3+2,11,16);R('#1d2330',x3+5,y3+19,3,1);
   if(e>=.9)payTick(P,x3+3,y3+6,2)}}
 /* 支払いがすんだら、コーヒー(アイス)とケーキのひと切れが出てくる。場面が終わるまでカウンターに残る */
 if(P.res){
  var r=Math.min(1,(t-P.t0-1.7)/.5),dy=Math.round(12*(1-payEase(r))),cx=168,cy=YB-26+dy,al=Math.min(1,r*2);
  c.globalAlpha=al;
  R('#cfe6ee',cx,cy+2,16,24);R('#6a4023',cx+2,cy+10,12,15);R('#c79a6a',cx+2,cy+10,12,3);
  R('#e04a3c',cx+10,cy-6,3,16);R('#fff',cx+10,cy-2,3,2);
  c.globalAlpha=al*.8;R('#fff',cx+3,cy+13,4,4);R('#fff',cx+9,cy+18,4,4);c.globalAlpha=al;
  if(Math.floor(t*2)%3===0)R('#fff',cx+2,cy+4,2,2);
  var px_=190,py=YB-16+dy;
  R('#f4f1e8',px_,py+13,26,3);R('#d6862a',px_+2,py+2,22,11);R('#fff6d8',px_+2,py+2,22,3);R('#fff6d8',px_+2,py+8,22,2);R('#8a4a1a',px_+7,py+6,2,2);R('#8a4a1a',px_+15,py+11,2,1);
  c.globalAlpha=1}}
