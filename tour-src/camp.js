/* ===== 合宿(マッチョルル教室)デモ版(タスク078): ナイロビ(tour/)だけ。チェックモード(?check=1)の一覧からだけ入る独立場面 camp_demo1 =====
   ・本編の進行・セーブ・完了の数えには入れない(save.seen にも書かない)。新しい保存キーは作らない。
   ・発音判定・失敗ルール(074)は既存の「聞く→言う」(showCue / setupAction / onFail / autoRescue)をそのまま使う。新しい採点・中継は作らない。
   ・ルルの絵は GSD.lulu.img の1か所(データは camp_data.py の LULU_IMG)。マッチョルルの絵が無いので通常のルルを大きく出している。
   ・画面に数値スコア・失敗回数・点数は出さない。「復習」「テスト」「測定」「練習」の文字も出さない。 */
var GSD=/*CAMPDATA*/null;
var GS=null;
function gsOff(){
 var sv=$m('sceneView');if(sv)sv.classList.remove('gs');
 var s=document.getElementById('gsStage');if(s&&s.parentNode)s.parentNode.removeChild(s);
 window.removeEventListener('resize',gsSize);GS=null}
function gsImgEl(src,cls){var i=new Image();i.className=cls||'';i.alt='';i.draggable=false;i.src=src;return i}
function gsSize(){
 if(!GS||!GS.box)return;
 var app=$m('app'),W=Math.min(app.clientWidth||window.innerWidth,480),vh=app.clientHeight||window.innerHeight;
 var sH=Math.max(340,Math.min(580,Math.round(vh*.52))),cH=Math.round(sH*.76),cW=Math.round((cH-4)*9/16)+4;   /* 枠(2px×2)の内側が 9:16 になるように */
 var colW=Math.max(96,W-12-8-cW),mW=Math.min(150,Math.round(colW*.78)),mH=Math.round(mW*.8);
 var lH=Math.min(sH-36-6-mH,Math.round(colW*GSD.lulu.h/GSD.lulu.w)),lW=Math.round(lH*GSD.lulu.w/GSD.lulu.h);
 GS.box.style.height=sH+'px';
 GS.cardBox.style.height=cH+'px';GS.cardBox.style.width=cW+'px';
 GS.lulu.style.width=lW+'px';GS.lulu.style.height=lH+'px';
 GS.mouth.style.width=mW+'px';
 GS.lulu.style.setProperty('--gsk',(1+3/(lH*GSD.lulu.hip/GSD.lulu.h)).toFixed(4));
 GS.dim={sH:sH,cH:cH,cW:cW,lW:lW,lH:lH,mW:mW,mH:mH}}
function gsBuild(){
 var st=document.querySelector('#sceneView .stage'),old=document.getElementById('gsStage');if(old)old.parentNode.removeChild(old);
 var box=el('div','');box.id='gsStage';
 var col=el('div','');col.id='gsLuluCol';
 var lu=el('div','');lu.id='gsLulu';
 var src='assets/art/'+GSD.lulu.img,hp=(GSD.lulu.hip/GSD.lulu.h*100).toFixed(2);
 var low=gsImgEl(src,'lay low'),up=gsImgEl(src,'lay up');
 low.style.clipPath='inset('+hp+'% 0 0 0)';up.style.clipPath='inset(0 0 '+(100-hp).toFixed(2)+'% 0)';up.style.transformOrigin='50% '+hp+'%';
 lu.appendChild(el('div','sh'));lu.appendChild(low);lu.appendChild(up);
 var mo=el('div','');mo.id='gsMouth';var mi=gsImgEl('','');mo.appendChild(mi);
 col.appendChild(lu);col.appendChild(mo);
 var cb=el('div','');cb.id='gsCardBox';var ci=gsImgEl('','');ci.id='gsCard';var hi=el('div','');hi.id='gsHi';cb.appendChild(ci);cb.appendChild(hi);
 box.appendChild(col);box.appendChild(cb);
 st.appendChild(box);
 GS.box=box;GS.lulu=lu;GS.mouth=mo;GS.mouthImg=mi;GS.cardBox=cb;GS.cardImg=ci;GS.hi=hi;
 window.addEventListener('resize',gsSize);gsSize()}
function gsSetCard(c){GS.cardImg.src=GSD.dir?'assets/art/'+GSD.dir+c.img:c.img;GS.mouthImg.src='assets/art/'+GSD.dir+c.mouth;gsHi(null);gsMouth(false)}
function gsMouth(on){if(GS&&GS.mouth)GS.mouth.classList.toggle('on',!!on)}
/* 今の単語(i=0..5)か短文(i=-1)のところに、青い枠を出す(カードのどこを言うか分かるように)。赤は使わない */
function gsHi(i){
 var h=GS&&GS.hi;if(!h)return;if(i==null){h.style.display='none';return}
 var r;if(i<0)r=GSD.sent;else{r=[GSD.cell.x[i%2],GSD.cell.y[Math.floor(i/2)],GSD.cell.w,GSD.cell.h]}
 h.style.left=(r[0]/GSD.cardW*100)+'%';h.style.top=(r[1]/GSD.cardH*100)+'%';h.style.width=(r[2]/GSD.cardW*100)+'%';h.style.height=(r[3]/GSD.cardH*100)+'%';h.style.display='block'}
function gsBig(txt){
 clearPanel();var card=el('div','cue gsm'),s=el('span','w s',txt);card.appendChild(s);panel.appendChild(card);
 try{fitCue(card);requestAnimationFrame(function(){fitCue(card)})}catch(e){}}
/* ルルが言う(画面の台詞＋ say())。口の絵は、モデルの読み上げのときだけ別に出す */
function gsLine(text,cb,rate){
 who.textContent='Lulu';setMsgInstant(text,'Lulu');spSay=true;
 say(text,rate||.85,1.35,gd(function(){spSay=false;later(350,cb)}))}
function gsModelList(items,hiOf,done){
 var seq=[];items.forEach(function(w,i){seq.push({t:w,i:hiOf(i)});seq.push({t:w,i:hiOf(i)})});   /* 1語ずつ2回ずつ */
 gsMouth(true);
 (function step(k){
  if(k>=seq.length){gsMouth(false);later(250,done);return}
  var q=seq[k];gsHi(q.i);gsBig(q.t);spSay=true;
  say(q.t,.75,1.35,gd(function(){spSay=false;later(k%2?500:380,function(){step(k+1)})}))})(0)}
function gsPlayList(list,done){
 (function step(i){
  if(i>=list.length){done();return}
  var it=list[i];
  GS.after=function(){later(250,function(){step(i+1)})};
  var S=G.scene;S.turns=[{npc:GSD.repeat,npcJp:'',cue:it.cue,cueJp:'',pitch:1.35}];G.ti=0;G.tries=0;
  gsHi(it.i);gsMouth(false);who.textContent='Lulu';showCue()})(0)}
/* advance() から呼ばれる(合格・ルルの救済のあと) */
function gsAfter(){var f=GS&&GS.after;GS&&(GS.after=null);if(f)f()}
function gsStar(s){return s.split(' ').map(function(w){return '*'+w+'*'}).join(' ')}
function gsCard(){
 var c=GSD.cards[GS.ci];gsSetCard(c);
 gsLine(c.intro,function(){
  gsModelList(c.words,function(i){return i},function(){
   gsLine(GSD.repeat,function(){
    gsPlayList(c.words.map(function(w,i){return {cue:gsStar(w),i:i}}),function(){
     gsModelList([c.sentence],function(){return -1},function(){   /* 短文: gsModelList は1項目を2回読む */
      gsLine(GSD.repeat,function(){
       gsPlayList([{cue:gsStar(c.sentence),i:-1}],function(){
        GS.ci++;if(GS.ci<GSD.cards.length)gsCard();else gsEnd()})})})})})})})}
function gsEnd(){
 gsHi(null);gsMouth(false);
 gsLine(GSD.outro,function(){
  G.phase='clear';Snd.jingle('clear');later(1600,function(){showMap()})})}
/* startScene() の入口(build.py が差しこむ): GO を押すと始まる */
function gsReady(){
 var S=G.scene;S.pitch=1.35;S.turns=[];G.ti=0;G.tries=0;
 $m('sceneView').classList.add('gs');
 GS={ci:0,after:null};gsBuild();gsSetCard(GSD.cards[0]);
 clearPanel();setMsgInstant(GSD.ready,'Lulu');$m('tapHint').textContent='';
 var b=el('button','btn go','GO！');b.type='button';panel.appendChild(b);
 b.addEventListener('click',function(){b.disabled=true;clearPanel();gsCard()})}
