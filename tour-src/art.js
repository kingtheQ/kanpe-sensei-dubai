/* ============================================================
   場面の絵(タスク028): 枠なし・フルブリードの新しい絵の場面
   - 新しい背景(1536×960)を #sceneA に描く。古い背景(320×150のドット)の場面は今までどおり #scene に描く
   - 人物は キング確定版のスプライト(足もとの芝・縁の黄緑は素材づくりで除去済み)。歩行は「進む方向を向いたコマだけ」
       キング右歩き = walk-12/18 を左右反転 / ルル右歩き = walk-10→17→23→17 / 左歩きはその逆(キングは元の向き、ルルは反転)
   - 場面ごとの置き場は ART に書く。背景を足すときは: 画像を tour/assets/art/ に置く → ART に1項目 → artIdFor で場面と結ぶ
   ============================================================ */
var ARTBASE='/*ARTBASE*/';
var cvA=$('sceneA'),ca=cvA.getContext('2d');ca.imageSmoothingEnabled=false;
var ARTI={},ARTFAIL={},ARTSHOW=0,AW=1536,AH=960;
/* 場面の置き場。mode: wide=ワイド(人物は小さめ、キング124px) / room=室内(背景も人物も2倍、キング248px)
   base=足もとの高さ、lulu/king/suit=立つ位置(ルルが左・キングが右。グアムと同じ)、npc=相手(いつもの顔のドット)の位置と大きさ */
var ART={
 nairobi:{bg:'nairobi-arrivals.png',mode:'wide',base:926,lulu:300,king:470,suit:575,npc:{x:1060,px:9,slide:1},fx:'night',npcS:{taxi_staff:'w-front-man-dashiki',driver:'w-front-man-suit-1'}},
 hotel:{bg:'hotel-front.png',mode:'room',base:895,lulu:250,king:450,suit:560,npc:{x:1290,px:15,top:262,clip:412},fx:'hotel',npcS:{c_front:'o-front-woman-blonde-suit'}},
 /* 入国審査(タスク031): 人なしの背景。キングとルルは右の端から歩いて入り、いちばん右の列(Visitors)のおわりに立つ(dir:-1 = 左へ歩く)。ルルが左・キングが右 */
 immig:{bg:'nairobi-immigration.png',mode:'wide',base:690,dir:-1,lulu:1290,king:1360,suit:1250,
  /* 窓口の係官(頭と肩だけ。大人の高さ136pxに縮めた絵)。lead=話し相手の係官の窓口。sw=話し相手が officer2(女性)のとき入れ替わる絵 */
  booths:[{n:'o-front-officer-green-1',x:215,top:395,clip:488},{n:'o-front-officer-blue',x:585,top:395,clip:488,sw:'o-front-officer-green-1'},
   {n:'o-front-officer-green-2',x:951,top:395,clip:488},{n:'o-front-officer-green-passport',x:1319,top:395,clip:488,lead:1,sw:'o-front-officer-blue'}],
  /* 並ぶ人(後ろ姿)と歩く人(正面)。x=足もとの中心、by=足もとの高さ。高さは大人=キングの約1.1倍(136px。素材を縮めた w- の絵)。奥の人から順に描く */
  crowd:[['back-family',217,686],['back-man-suit-1',215,789],['back-maasai',216,894],
   ['back-backpacker',585,684],['back-woman-hijab',585,788],['back-man-suit-2',584,892],
   ['back-man-thobe',952,684],['back-couple-red',952,786],['back-woman-blonde-suit',952,892],
   ['back-man-dashiki',1320,792],['back-couple-colorful',1321,896],
   ['front-safari',399,947,'walk'],['front-pilot-fa',1119,946,'walk']]}};
/*ARTSEL*/
function artImg(n){var i=ARTI[n];if(!i){i=ARTI[n]=new Image();i.onerror=function(){i.bad=1};i.src=ARTBASE+n}return i}
function artShow(on){if(ARTSHOW===on)return;ARTSHOW=on;cv.hidden=!!on;cvA.hidden=!on}
function artR(col,x,y,w,h){ca.fillStyle=col;ca.fillRect(Math.round(x),Math.round(y),Math.round(w),Math.round(h))}
function artSpr(img,cx,by,flip){var w=img.naturalWidth,h=img.naturalHeight,x=Math.round(cx-w/2),y=Math.round(by-h);
 if(flip){ca.save();ca.translate(x+w,y);ca.scale(-1,1);ca.drawImage(img,0,0);ca.restore()}else ca.drawImage(img,x,y)}
function artShadow(cx,by,rx,al){var ry=rx*.12,ps=4;ca.fillStyle='rgba(0,0,0,'+(al||.62)+')';
 for(var yy=-Math.round(ry);yy<=ry;yy+=ps){var half=rx*Math.sqrt(Math.max(0,1-(yy/ry)*(yy/ry)));ca.fillRect(Math.round(cx-half),Math.round(by-ps/2+yy),Math.round(half*2),ps)}}
function artSuit(cx,by,room){var w=room?58:30,bh=room?96:52,yh=room?18:10,hw=room?6:3,hh=room?24:16,x=Math.round(cx-w/2);
 artR('#8c9098',cx-hw/2,by-bh-yh-hh,hw,hh+2);artR('#facd28',x,by-bh-yh,w,yh);artR('#265496',x,by-bh,w,bh)}
function artSpA(map,pal,x,y,px,clipY){for(var r=0;r<map.length;r++){var yy=y+r*px;if(clipY&&yy>=clipY)break;var row=map[r];
  for(var k=0;k<row.length;k++){var ch=row.charAt(k);if(ch!=='.'){ca.fillStyle=pal[ch]||'#f0f';var hh=clipY?Math.min(px,clipY-yy):px;ca.fillRect(Math.round(x+k*px),Math.round(yy),px,hh)}}}}
function artBubble(cx,cy){artR('#05070f',cx-16,cy-3,36,24);artR('#f4f1e8',cx-14,cy-1,32,20);ca.fillStyle='#05070f';ca.font='800 18px sans-serif';ca.textAlign='center';ca.textBaseline='middle';ca.fillText('…',cx+2,cy+8)}
/* ---- 小さな動き(場面ごと) ---- */
var ARTR=(function(){var s=12345;return function(){s=(s*1103515245+12345)&0x7fffffff;return s/0x7fffffff}})();
var STARS=[],GLINTS=[];
(function(){var i,x,y;for(i=0;i<26;i++){x=20+ARTR()*1490;y=8+ARTR()*140;if(x>1330&&x<1430&&y<96){i--;continue}STARS.push([x,y,ARTR()*6.28,.8+ARTR()*1.2])}
 var NO=[[190,250,382,318],[476,240,1140,340],[1222,250,1420,316],[236,390,350,566],[1116,390,1230,566],[128,220,162,566],[598,220,630,566],[1036,220,1070,566],[1428,220,1462,566]];
 for(i=0;i<16;i++){x=12+ARTR()*1500;y=232+ARTR()*320;var bad=0;for(var k=0;k<NO.length;k++){if(x>NO[k][0]-14&&x<NO[k][2]&&y>NO[k][1]-8&&y<NO[k][3])bad=1}if(bad){i--;continue}GLINTS.push([x,y,ARTR()*6.28,.5+ARTR()*.9,ARTR()<.55?'#a5c8fa':'#fac078'])}})();
function artFxNight(){var i,a;
 for(i=0;i<STARS.length;i++){var s=STARS[i];a=.5+.5*Math.sin(t*s[3]+s[2]);if(a>.35){ca.globalAlpha=a*.9;artR('#eaf0ff',s[0],s[1],4,4)}}
 for(i=0;i<GLINTS.length;i++){var g=GLINTS[i];a=Math.max(0,Math.sin(t*g[3]+g[2]));ca.globalAlpha=a*.75;artR(g[4],g[0],g[1],10,6)}
 ca.globalAlpha=1}
var KEYGOLD=[[0,1],[0,2],[0,4],[1,0],[1,2],[1,3],[2,0],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4]];
function artFxHotel(){
 /* ランプ: 電球の芯がゆっくり明るさを変える(光の輪は出さない) */
 [300,768,1236].forEach(function(x,i){ca.globalAlpha=.18+.14*Math.sin(t*1.1+i*2.1);artR('#fff4c0',x-10,68,20,6)});ca.globalAlpha=1;
 /* ベル: ときどき小さくきらっと光る */
 var bp=(t+1.3)%3.4;if(bp<.45){ca.globalAlpha=bp<.22?1:.5;artR('#fffbe8',918,386,4,12);artR('#fffbe8',912,392,16,4);ca.globalAlpha=1}
 /* 鍵の板: 金色の鍵がひとつずつ、順にちかっと光る */
 var q=Math.floor(t/1.1)%KEYGOLD.length,kp=(t/1.1)%1,kk=KEYGOLD[q];if(kp<.6){ca.globalAlpha=kp<.3?.95:.55;artR('#fffbe8',104+kk[1]*56+8,212+kk[0]*60+8,8,8);ca.globalAlpha=1}}
/* ---- 1フレーム描く。新しい絵の場面なら true ---- */
function ARTframe(S,A0,dt){
 var id=(!A0&&S&&OUT.hero==='blue'&&OUT.lulu==='plain'&&typeof artIdFor==='function')?artIdFor(S):null,cf=id&&ART[id];
 if(!cf||ARTFAIL[id]){artShow(0);return false}
 var room=cf.mode==='room',m=cf.mode,bg=artImg(cf.bg),im={};
 var names=['king-idle','lulu-idle','king-walk-a','king-walk-b','lulu-walk-a','lulu-walk-b','lulu-walk-c'],ok=artOKimg(bg);
 for(var i=0;i<names.length;i++){im[names[i]]=artImg(m+'-'+names[i]+'.png');if(!artOKimg(im[names[i]]))ok=false}
 if(bg.bad){ARTFAIL[id]=1;artShow(0);return false}
 for(var j=0;j<names.length;j++)if(im[names[j]].bad){ARTFAIL[id]=1;artShow(0);return false}
 var ex=artExtra(cf),exi={};for(var e=0;e<ex.length;e++){var xi=artImg('npc/'+ex[e]+'.png');if(xi.bad){ARTFAIL[id]=1;artShow(0);return false}if(!artOKimg(xi))ok=false;exi[ex[e]]=xi}
 artShow(1);
 if(!ok){artR('#10131f',0,0,AW,AH);return true}
 if(S.artT0==null)S.artT0=t;
 var te=t-S.artT0,B=cf.base,BOB=4;
 ca.globalAlpha=1;ca.drawImage(bg,0,0);
 if(cf.fx==='night')artFxNight();else if(cf.fx==='hotel')artFxHotel();
 /* 相手(いつもの顔のドット): 空港では右から入ってくる。カウンターの中は動かず、頭と肩だけ見せる(カウンターの高さで切る) */
 /* 窓口の係官(入国審査): 頭と肩だけ見せる(窓口の台の高さで切る)。話し相手の窓口は、話すとき小さくうなずいて「…」を出す。そのほかの窓口もゆっくり小さく動く */
 if(cf.booths){var lead=S.d&&S.d.sp==='officer2';
  cf.booths.forEach(function(b,bi){var im2=exi[(lead&&b.sw)?b.sw:b.n],bw=im2.naturalWidth,bob2=b.lead&&speaker&&spSay?(Math.floor(t*6)%2?-3:0):(Math.floor(t*.9+bi*.37)%2?-2:0),by0=b.top+bob2,x0=Math.round(b.x-bw/2);
   ca.drawImage(im2,0,0,bw,b.clip-by0,x0,by0,bw,b.clip-by0);
   if(b.lead&&speaker&&spSay)artBubble(b.x+Math.round(bw*.4),b.top-18)})}
 /* 相手が素材の絵(w-:縮めた絵)のとき: 足もとをそろえて立ち、右から入ってくる。いつもの小さな動きは今までと同じ */
 var sk=artSpKey(),spr=(cf.npcS&&sk&&cf.npcS[sk])?exi[cf.npcS[sk]]:null;
 if(spr&&cf.npc.clip){   /* カウンター越しの係員: 頭と肩だけ(カウンターの高さで切る)。動かず、ゆっくり小さく揺れ、話すときうなずいて「…」 */
  var cw=spr.naturalWidth,cy=cf.npc.top+(spSay&&Math.floor(t*6)%2?-3:0),cx3=cf.npc.x+Math.round(Math.sin(t*1.3)*2)+(cf.npc.slide?spX*2:0);
  ca.drawImage(spr,0,0,cw,cf.npc.clip-cy,Math.round(cx3-cw/2),cy,cw,cf.npc.clip-cy);if(spSay)artBubble(cx3+Math.round(cw*.3),cf.npc.top-18)}
 else if(spr){var spw=spr.naturalWidth,spy=B+(Math.floor(t*1.6+.25)%2?-BOB/2:0)+(spSay&&Math.floor(t*6)%2?-3:0),spx=cf.npc.x+Math.round(Math.sin(t*1.3)*2)+(cf.npc.slide?spX*2:0);
  artShadow(spx,B,spw*.6);artSpr(spr,spx,spy,false);if(spSay)artBubble(spx+Math.round(spw*.3),spy-spr.naturalHeight-18)}
 else if(speaker&&!speaker.ghost&&speaker.m&&speaker.m[0]&&cf.npc){var nm=speaker.m[0][0],np=speaker.m[0][1],px=cf.npc.px,nw=nm[0].length*px,nh=nm.length*px;
  var sway=Math.round(Math.sin(t*1.3)*2),nx=cf.npc.x-nw/2+sway+(cf.npc.slide?spX*2:0);
  if(cf.npc.clip){var cyc=t%7.5,wr=cyc>4&&cyc<6,ny=cf.npc.top,hb=wr?10:0,bob=spSay&&Math.floor(t*6)%2?-3:0;
   var head=nm.slice(0,6).map(function(r){return wr?r.replace(/e/g,'s'):r}),body=nm.slice(6);
   artSpA(body,np,nx,ny+6*px,px,cf.npc.clip);artSpA(head,np,nx,ny+hb+bob,px,0);
   if(wr){ca.fillStyle='#4a4a52';ca.fillRect(1140+Math.round((t*38)%36),399,14,3)}
   if(spSay)artBubble(nx+nw*.8,ny-18)}
  else{var nb=Math.floor(t*1.6+.25)%2?-BOB/2:0,ny2=B-nh+nb+(spSay&&Math.floor(t*6)%2?-3:0);artShadow(nx+nw/2,B,nw*.6);artSpA(nm,np,nx,ny2,px,0);
   if(spSay)artBubble(nx+nw*.8,ny2-18)}}
 /* 歩いて入ってくる(ゆっくり一定の速さ)。ルルが左・キングが右でそろって止まる。人物は足もとの高さの順に重ねて描く(奥から手前) */
 var dir=cf.dir||1,sp=room?260:150,dist=cf.dist||(dir>0?cf.king+150:AW+150-cf.king),walked=Math.min(dist,sp*te),walking=walked<dist-.5,sh=dist-walked;
 var kx=cf.king-dir*sh,lx=cf.lulu-dir*sh,shw=room?70:36,L=[];
 /* 並ぶ人・歩く人: 小さく上下にゆれる(ふたりより小さく、ゆっくり。人ごとに周期をずらす)。歩く人は少し速く */
 (cf.crowd||[]).forEach(function(c,ci){L.push({by:c[2],f:function(){var img=exi['w-'+c[0]],bw=img.naturalWidth,
   o=c[3]==='walk'?(Math.floor(t*3.2+ci*.4)%2?-3:0):(Math.floor(t*1.1+ci*.53)%2?-2:0);
   artShadow(c[1],c[2],bw*.42,.3);artSpr(img,c[1],c[2]+o,false)}})});
 L.push({by:B,f:function(){artSuit(cf.suit-dir*sh,B,room)}});
 if(OUT.lvis)L.push({by:B,f:function(){var ly=0,limg;
  if(walking){var lf=Math.floor(te/.2)%4;limg=im[['lulu-walk-a','lulu-walk-b','lulu-walk-c','lulu-walk-b'][lf]];ly=lf%2?-BOB:0}
  else{limg=im['lulu-idle'];ly=Math.floor(t*1.6+.5)%2?-BOB:0}
  if(luHelp&&!walking)ly-=Math.floor(t*7)%2?10:0;
  artShadow(lx,B,shw*.8);artSpr(limg,lx,B+ly,walking&&dir<0);   /* ルルの歩きのコマは右向き。左へ歩くときだけ反転 */
  if(luTalk&&spSay&&!walking)artBubble(lx+20,B-limg.naturalHeight-26);
  if(luHelp&&!walking){ca.fillStyle='#e8452c';ca.font='800 26px sans-serif';ca.textAlign='center';ca.textBaseline='middle';ca.fillText('♪',lx+limg.naturalWidth*.5,B-limg.naturalHeight-12)}}});
 if(OUT.hvis)L.push({by:B,f:function(){var ky=0,kimg;
  if(walking){var kf=Math.floor(te/.32)%2;kimg=im[kf?'king-walk-b':'king-walk-a'];ky=kf?-BOB:0}
  else{kimg=im['king-idle'];ky=Math.floor(t*1.6)%2?-BOB:0}
  artShadow(kx,B,shw);artSpr(kimg,kx,B+ky,walking&&dir>0)}});   /* 右へ歩くときは、元の左向きのコマを左右反転(左へ歩くときは元のまま) */
 L.sort(function(a,b){return a.by-b.by});for(var li=0;li<L.length;li++)L[li].f();
 return true}
function artOKimg(i){return i.complete&&i.naturalWidth>0}
/* この場面が使う人物の絵の名前(npc/ の中)。ひとつでも読めなければ、場面全体が今までの描画に戻る */
function artExtra(cf){var a=[],i;(cf.crowd||[]).forEach(function(c){a.push('w-'+c[0])});
 (cf.booths||[]).forEach(function(b){a.push(b.n);if(b.sw)a.push(b.sw)});
 if(cf.npcS)for(var k in cf.npcS)a.push(cf.npcS[k]);return a}
function artSpKey(){if(!speaker)return null;for(var k in SP)if(SP[k]===speaker)return k;return null}
/* ============================================================
   場面の環境音(タスク028): 場面→音の対応表 + 再生の口 + ミュート。音源ファイルは素材パック第2弾で納品する
   - src が空のカテゴリは何も鳴らさない(いまは全部空)。入れるときは tour/assets/amb/ に置いて src にファイル名を書く
   - 音量は会話の音声より十分小さく(vol 0.1前後)。ミュートは今ある音の設定(🔊/🔇、kd_snd)と同じ。マイクで聞いている間は止める
   ============================================================ */
var AMBBASE=ARTBASE.replace(/art\/$/,'amb/');
var AMB={
 airport:{src:'',vol:.10,note:'空港(入国・手荷物・チェックイン・ゲート): ざわめきと遠いアナウンス'},
 outdoor:{src:'',vol:.10,note:'空港の外(タクシー乗り場など): 夜風と遠い車の音'},
 cafe:{src:'',vol:.10,note:'カフェ・店: 食器の小さな音と話し声'},
 lounge:{src:'',vol:.08,note:'ラウンジ: ごく静かな空調'},
 hotel:{src:'',vol:.08,note:'ホテル・室内: 静かな室内'},
 cabin:{src:'',vol:.12,note:'機内: 低いエンジン音'},
 street:{src:'',vol:.10,note:'街・スーク: 遠い人ごみ'},
 sea:{src:'',vol:.10,note:'海ぞい: 波'}};
/* 場面の音の名前(場所の snd) → カテゴリ */
var AMBSND={info:'airport',hall:'airport',tdesk:'airport',map:'airport',nbo:'airport',doh:'airport',cafe:'cafe',costa:'cafe',mall:'cafe',s34:'cafe',
 ahlan:'lounge',hotel:'hotel',room:'hotel',home:'hotel',sage:'hotel',vault:'hotel',mosque:'hotel',atop:'cabin',souk:'street',city:'street',dohc:'street',
 beach:'sea',marina:'sea',fountain:'outdoor',safari:'outdoor'};
/* 背景の名前 → カテゴリ(場所の音と食いちがうとき、こちらが先) */
var AMBBG={taxi:'outdoor',dtaxi:'outdoor',cabinQ:'cabin',cabin:'cabin',chotel:'hotel',cbreak:'hotel'};
var ambEl=null,ambCat=null,ambDuck=false;
function ambOn(){try{return localStorage.getItem('kd_snd')!=='off'}catch(e){return true}}
function ambApply(){var c=ambCat&&AMB[ambCat];
 if(!c||!c.src||!ambOn()||ambDuck||document.hidden){if(ambEl){try{ambEl.pause()}catch(e){}}return}
 var u=/^(data:|https?:)/.test(c.src)?c.src:AMBBASE+c.src;
 if(!ambEl||ambEl._u!==u){if(ambEl){try{ambEl.pause()}catch(e){}}ambEl=new Audio(u);ambEl.loop=true;ambEl._u=u}
 ambEl.volume=c.vol;var p=ambEl.play();if(p&&p.catch)p.catch(function(){})}
window.__ambGo=function(kind){ambCat=AMBSND[kind]||null;ambApply()};
window.__ambScene=function(kind,bg){ambCat=AMBBG[bg]||AMBSND[kind]||null;ambApply()};
window.__ambDuck=function(f){ambDuck=!!f;ambApply()};
window.__ambSync=ambApply;window.__AMB=AMB;
document.addEventListener('visibilitychange',ambApply);
