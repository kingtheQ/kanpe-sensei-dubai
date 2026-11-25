/* ===== 合宿(マッチョルル教室)デモ版(タスク078): ナイロビ(tour/)だけ。チェックモード(?check=1)の一覧からだけ入る独立場面 camp_demo1 =====
   ・本編の進行・セーブ・完了の数えには入れない(save.seen にも書かない)。新しい保存キーは作らない。
   ・発音判定・失敗ルール(074)は既存の「聞く→言う」(showCue / setupAction / onFail / autoRescue)をそのまま使う。新しい採点・中継は作らない。
   ・ルルの絵は GSD.lulu.frames の1か所(データは camp_data.py の LULU_FRAMES)。マッチョルルのダンベル・アニメ(081)。口パーツは083から画面に出さない(素材は残す)。ルルは左下に固定。
   ・画面に数値スコア・失敗回数・点数は出さない。「復習」「テスト」「測定」「練習」の文字も出さない。 */
var GSD=/*CAMPDATA*/null;
var GS=null;
/* 背景(082): ジムの背景画 camp.png(1536×960・人なし)。場面の絵の仕組み(art.js の ART と artIdFor。bg='campK' → 'camp')にそのまま乗せる。
   人物・動くものは描かない(ルルは上に重ねる別の部品。meal は人物を描かない形で、バブルの位置は画面の外) */
ART.camp={bg:'camp.png',mode:'wide',meal:{bubble:{x:-200,y:-200}}};
function gsOff(){
 gsRecDrop();gsOwnStop();
 if(GS&&GS.tm){clearInterval(GS.tm);GS.tm=0}
 var sv=$m('sceneView');if(sv)sv.classList.remove('gs');
 var s=document.getElementById('gsStage');if(s&&s.parentNode)s.parentNode.removeChild(s);
 window.removeEventListener('resize',gsSize);GS=null}
function gsImgEl(src,cls){var i=new Image();i.className=cls||'';i.alt='';i.draggable=false;i.src=src;return i}
/* 大きさ(081): ルルは左下に固定。口パーツの表示・非表示で、ルルの位置も大きさも変えない(口はルルの頭の上に重ねる)。
   ・ルルの大きさ = 従来の表示の高さ(refH) × GSD.lulu.scale。従来=カラムの高さをルルと口で分け合って出していた大きさ(下の計算を、倍率の基準としてだけ残してある)
   ・カードの幅 = ステージの幅(SW) × GSD.cardShare(高さが足りなければ高さに合わせて縮める) */
function gsSize(){
 if(!GS||!GS.box)return;
 var L=GSD.lulu,app=$m('app'),W=Math.min(app.clientWidth||window.innerWidth,480),vh=app.clientHeight||window.innerHeight;
 var sH0=Math.max(340,Math.min(580,Math.round(vh*.52)));                   /* 従来のステージの高さ */
 var cH0=Math.round(sH0*.76),cW0=Math.round((cH0-4)*9/16)+4,colW0=Math.max(96,W-12-8-cW0),mW0=Math.min(150,Math.round(colW0*.78)),mH0=Math.round(mW0*.8);
 var refH=Math.min(sH0-36-6-mH0,Math.round(colW0*L.old[1]/L.old[0]));         /* 従来のルルの表示の高さ(px) */
 var SW=(GS.box.parentNode&&GS.box.parentNode.clientWidth)||W;                 /* ステージの幅(画面いっぱい) */
 var cW=Math.round(SW*GSD.cardShare),cH=Math.round((cW-4)*16/9)+4;
 var sH=Math.min(Math.max(sH0,cH),Math.max(sH0,Math.round(vh*.58)));          /* 背の低い画面は、ステージを少しだけ(画面の高さの58%まで)高くして、カードの幅を確保する */
 if(cH>sH){cH=sH;cW=Math.round((cH-4)*9/16)+4}
 var colW=Math.max(96,SW-12-8-cW),k=refH*L.scale/L.refH;                        /* k=素材の1pxが画面で何pxか(全コマ共通) */
 var fr=L.frames,used=GS.used,i,f,mL=0,mR=0,mU=0,ks={},ki;
 /* 083: コマごとに倍率を変えて、頭のてっぺん(y=12)→足の裏(foot_y)の高さを全コマで同じにする(画面で refH×scale)。足もとの線と中心もそろえる */
 for(i=0;i<used.length;i++){f=fr[used[i]];ki=k*L.refH/(f.foot_y-12);ks[used[i]]=ki;mL=Math.max(mL,f.foot_x*ki);mR=Math.max(mR,(f.w-f.foot_x)*ki);mU=Math.max(mU,f.foot_y*ki)}
 var bw=Math.round(mL+mR),bh=Math.round(mU),fx0=Math.round(mL);
 var cx=6+colW/2,left=Math.round(cx-fx0);left=Math.min(left,SW-cW-6-bw);   /* 箱の右端はカードの左端まで(コマ3の腕で箱が数px広がっても、カードに重ねない。余白は透明) */
 GS.box.style.height=sH+'px';
 GS.cardBox.style.height=cH+'px';GS.cardBox.style.width=cW+'px';
 GS.lulu.style.width=bw+'px';GS.lulu.style.height=bh+'px';GS.lulu.style.left=left+'px';
 for(i=0;i<used.length;i++){f=fr[used[i]];var im=GS.frs[used[i]];
  ki=ks[used[i]];im.style.width=(f.w*ki).toFixed(2)+'px';im.style.height=(f.h*ki).toFixed(2)+'px';
  im.style.left=(mL-f.foot_x*ki).toFixed(2)+'px';im.style.top=(mU-f.foot_y*ki).toFixed(2)+'px'}
 var sw=Math.round(170*k);GS.sh.style.width=sw+'px';GS.sh.style.height=Math.max(4,Math.round(22*k))+'px';GS.sh.style.left=Math.round(fx0-sw/2)+'px';GS.sh.style.bottom=Math.round(-8*k)+'px';
 GS.dim={sH:sH,cH:cH,cW:cW,W:W,SW:SW,refH:refH,k:k,lW:bw,lH:bh,lCharH:Math.round(L.refH*k),colW:colW}}
var LB=8;   /* ルルの足もとの下の余白(px) */
function gsBuild(){
 var st=document.querySelector('#sceneView .stage'),old=document.getElementById('gsStage');if(old)old.parentNode.removeChild(old);
 var L=GSD.lulu,box=el('div','');box.id='gsStage';
 var lu=el('div','');lu.id='gsLulu';lu.style.bottom=LB+'px';
 var sh=el('div','sh');lu.appendChild(sh);
 var used=[],frs={};L.seq.forEach(function(i){if(used.indexOf(i)<0)used.push(i)});
 used.forEach(function(i){var im=gsImgEl('assets/art/'+L.dir+L.frames[i].img,'fr');lu.appendChild(im);frs[i]=im});   /* 使うコマは全部先に置いて読み込む(切り替えは visibility だけ) */
 var cb=el('div','');cb.id='gsCardBox';var ci=gsImgEl('','');ci.id='gsCard';var hi=el('div','');hi.id='gsHi';cb.appendChild(ci);cb.appendChild(hi);
 box.appendChild(lu);box.appendChild(cb);
 st.appendChild(box);
 GS.box=box;GS.lulu=lu;GS.sh=sh;GS.frs=frs;GS.used=used;GS.cardBox=cb;GS.cardImg=ci;GS.hi=hi;
 window.addEventListener('resize',gsSize);gsSize();gsLuluGo()}
/* カール運動のコマ送り(1→2→3→2→1…。1コマ GSD.lulu.sec 秒)。時間だけで動く。読み上げ中も続ける(合宿=筋トレの場)。動きを減らす設定のときは1コマ目で止める */
function gsLuluShow(n){var L=GSD.lulu,idx=L.seq[n%L.seq.length];GS.si=n%L.seq.length;GS.lulu.setAttribute('data-f',String(idx+1));
 for(var k in GS.frs)GS.frs[k].classList.toggle('on',+k===idx)}
function gsLuluGo(){
 gsLuluShow(0);
 var red=false;try{red=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}
 if(red||GSD.lulu.seq.length<2)return;
 var me=GS;GS.tm=setInterval(function(){if(GS!==me){clearInterval(me.tm);return}gsLuluShow(GS.si+1)},Math.round(GSD.lulu.sec*1000))}
function gsSetCard(c){GS.cardImg.src=GSD.dir?'assets/art/'+GSD.dir+c.img:c.img;gsHi(null)}
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
/* ---- 自分の声(083): 端末の中だけ。メモリに置いて、1回鳴らしたら捨てる。サーバーへ送らない・どこにも保存しない(ブラウザの保存領域にも、ファイルにも書かない)。
   発音を調べる Azure の中継(voice.js)とは別系統で、このファイルは voice.js の関数・保存キーを呼ばない・書かない。通信の命令(ネットワークへ出す呼び出し)も一切使わない。
   使えない(マイク不許可・MediaRecorderなし・こえを出さないモード)ときは、自分の声の再生だけ静かに飛ばす。音声認識(判定)とは別に同じマイクを開く=実機(特にiOS)での同時利用は未確認 ---- */
var GR=null,GRN=0,GOWN=null;
function gsRecOK(){try{return typeof MediaRecorder!=='undefined'&&!!(navigator.mediaDevices&&navigator.mediaDevices.getUserMedia)&&!PREF.silent}catch(e){return false}}
function gsRecTy(){var L=['audio/mp4','audio/webm;codecs=opus','audio/webm','audio/ogg;codecs=opus'];try{for(var i=0;i<L.length;i++)if(MediaRecorder.isTypeSupported(L[i]))return L[i]}catch(e){}return ''}
function gsRecRel(r){try{if(r&&r.stream)r.stream.getTracks().forEach(function(t){try{t.stop()}catch(e){}})}catch(e){}}
function gsRecDrop(){GRN++;var r=GR;GR=null;if(!r)return;try{r.mr.ondataavailable=null;r.mr.onstop=null;if(r.mr.state!=='inactive')r.mr.stop()}catch(e){}gsRecRel(r);r.parts=null}
function gsRecOn(){   /* 判定の聞き取りが始まるたびに呼ばれる(build.py の差しこみ)。前の録音は捨てて録り直す */
 gsRecDrop();if(!GS||!gsRecOK())return;var n=GRN;
 try{navigator.mediaDevices.getUserMedia({audio:true}).then(function(stream){
  if(n!==GRN||!GS){gsRecRel({stream:stream});return}
  try{var ty=gsRecTy(),mr=ty?new MediaRecorder(stream,{mimeType:ty}):new MediaRecorder(stream),r={stream:stream,mr:mr,parts:[],ty:mr.mimeType||ty||'audio/mp4',t0:Date.now()};
   mr.ondataavailable=function(e){if(e.data&&e.data.size&&r.parts)r.parts.push(e.data)};GR=r;mr.start()}catch(e){gsRecRel({stream:stream});GR=null}
 },function(){})}catch(e){}}
function gsRecTake(cb){   /* 録音を止めて {blob,ms} を返す(なければ null)。マイクはここで閉じる */
 var r=GR;GRN++;GR=null;if(!r){cb(null);return}
 var fin=false;
 function done(){if(fin)return;fin=true;gsRecRel(r);var b=null;try{if(r.parts&&r.parts.length)b=new Blob(r.parts,{type:r.ty})}catch(e){}r.parts=null;cb(b&&b.size?{blob:b,ms:Date.now()-r.t0}:null)}
 r.mr.onstop=done;try{if(r.mr.state!=='inactive')r.mr.stop();else done()}catch(e){done()}
 setTimeout(done,2000)}
function gsOwnStop(){var o=GOWN;GOWN=null;if(!o)return;try{if(o.au)o.au.pause()}catch(e){}try{if(o.url)URL.revokeObjectURL(o.url)}catch(e){}o.blob=null}
function gsPlayOwn(r,cb){   /* 自分の声を1回だけ鳴らして捨てる */
 if(!r||!r.blob){cb();return}
 var sd=G.sid,o={blob:r.blob,url:null,au:null},fin=false;GOWN=o;
 function end(){if(fin)return;fin=true;if(GOWN===o)gsOwnStop();else{try{if(o.au)o.au.pause()}catch(e){}try{if(o.url)URL.revokeObjectURL(o.url)}catch(e){}}if(G.sid===sd)later(350,cb)}
 try{o.url=URL.createObjectURL(r.blob);o.au=new Audio(o.url);o.au.volume=Math.max(0,Math.min(1,(PREF.voice==null?100:PREF.voice)/100));
  o.au.onended=end;o.au.onerror=end;var p=o.au.play();if(p&&p.catch)p.catch(end);setTimeout(end,Math.min(9000,(r.ms||4000)+2500))}catch(e){end()}}
/* ---- ルルの読み上げ ---- */
function gsModelList(items,hiOf,done){
 var seq=[];items.forEach(function(w,i){seq.push({t:w,i:hiOf(i)});seq.push({t:w,i:hiOf(i)})});   /* 1語(1文)ずつ2回ずつ */
 (function step(k){
  if(k>=seq.length){later(250,done);return}
  var q=seq[k];gsHi(q.i);gsBig(q.t);spSay=true;
  say(q.t,.75,1.35,gd(function(){spSay=false;later(k%2?500:380,function(){step(k+1)})}))})(0)}
/* お手本をふつうの速さで1回、自動で流す(言えなかったあと。ボタンは押さない) */
function gsModelOnce(text,cb){spSay=true;say(text,1,1,gd(function(){spSay=false;later(300,cb)}))}
/* 1項目を言わせる。it={cue,i,text,kind:'word'|'chunk'|'whole',pre:言う前にお手本を流す}。言えたら advance()→gsAfter()で次へ */
function gsPlayList(list,done){
 (function step(i){
  if(i>=list.length){done();return}
  var it=list[i];it.fails=0;
  GS.after=function(){later(250,function(){step(i+1)})};
  GS.cur=it;gsHi(it.i);who.textContent='Lulu';
  if(it.pre)gsModelOnce(it.text,function(){gsAsk(it)});else gsAsk(it)})(0)}
function gsAsk(it){
 var S=G.scene;S.turns=[{npc:GSD.repeat,npcJp:'',cue:it.cue,cueJp:'',pitch:1.35}];G.ti=0;G.tries=0;
 gsHi(it.i);who.textContent='Lulu';showCue()}
/* 言えなかったとき(onFail から。083): 自分の声→お手本(自動・ふつうの速さ)→言い直し。短まとまりは2回続けて外れたら、お手本をもう一度流して次へ。
   単語・全文は3回続けて外れたらルルが代わりに言って次へ(074と同じ)。数字・失敗回数は画面に出さない */
function gsFail(){
 var it=GS&&GS.cur;if(!it)return;var sd=G.sid;it.fails++;G.phase='gsfail';G.tries=0;
 Snd.jingle('buzz');A_shake();if(G.mute)G.mute();
 var chunk=it.kind==='chunk';
 gsRecTake(function(r){
  if(G.sid!==sd)return;
  if(chunk&&it.fails>=2){gsOwnStop();gsModelOnce(it.text,function(){gsAfter()});return}
  if(!chunk&&it.fails>=3){gsOwnStop();setMsgInstant(it.text,'Lulu');spSay=true;say(it.text,.85,1.75,gd(function(){spSay=false;later(900,function(){gsAfter()})}));return}
  gsPlayOwn(r,function(){gsModelOnce(it.text,function(){gsAsk(it)})})})}
/* advance() から呼ばれる(合格・ルルの救済のあと) */
function gsAfter(){var f=GS&&GS.after;GS&&(GS.after=null);if(f)f()}
function gsStar(s){return s.split(' ').map(function(w){return '*'+w+'*'}).join(' ')}
/* 1回の合宿=カード1枚(083: 先頭の1枚。選ぶ画面なし。ほかのカードのデータは camp_data.py に残してある) */
function gsCard(){
 var c=GSD.cards[0];gsSetCard(c);
 gsLine(c.intro,function(){
  gsModelList(c.words,function(i){return i},function(){
   gsLine(GSD.repeat,function(){
    gsPlayList(c.words.map(function(w,i){return {cue:gsStar(w),i:i,text:w,kind:'word'}}),function(){
     gsModelList([c.sentence],function(){return -1},function(){   /* 短文: gsModelList は1項目を2回読む */
      gsLine(GSD.repeat,function(){
       gsPlayList(c.chunks.map(function(t){return {cue:gsStar(t),i:-1,text:t,kind:'chunk',pre:true}}),function(){
        gsLine(GSD.all,function(){
         gsPlayList([{cue:gsStar(c.sentence),i:-1,text:c.sentence,kind:'whole'}],function(){gsEnd()})})})})})})})})})}
function gsEnd(){
 gsHi(null);
 gsLine(GSD.outro,function(){
  G.phase='clear';Snd.jingle('clear');later(1600,function(){showMap()})})}
/* startScene() の入口(build.py が差しこむ): GO を押すと始まる */
function gsReady(){
 var S=G.scene;S.pitch=1.35;S.turns=[];G.ti=0;G.tries=0;
 $m('sceneView').classList.add('gs');
 GS={ci:0,after:null,cur:null};gsBuild();gsSetCard(GSD.cards[0]);
 clearPanel();setMsgInstant(GSD.ready,'Lulu');$m('tapHint').textContent='';
 var b=el('button','btn go','GO！');b.type='button';panel.appendChild(b);
 b.addEventListener('click',function(){b.disabled=true;clearPanel();gsCard()})}
