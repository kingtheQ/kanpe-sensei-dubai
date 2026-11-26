/* ===== 世界一周編: 窓口フロー(タスク012→088→089) =====
   (前の旅のメモ・初回のみ) → 宣言(初回のみ) → はじめての人 → 地図とルール(win_route合体版) → (再訪の挨拶) → 値段 → 読み上げ確認 → 名前の確認 → 搭乗券(ticket_star だけ)
   タスク089: 宣言は「係員の短い導入→ルルのお手本→プレイヤーが文ごとに言う(マイク大)」。前の旅のメモは宣言と混ぜず win_memo に分ける。
   win_c2/c5/c7/c8・win_rec・win_rules・win_count のデータは消さず、1周目の流れからは行かない(2周目用)。2回目に窓口へ来たら、宣言・ルール・地図を飛ばして win_back の挨拶から値段へ。
   タスク088: 発券はスターに統一(1周目)。ow4/ow5・ticket_ow のデータは2周目用に残し、この流れからは行かない。
   設計の正本: docs/pm/deliverables/003・004・011。build.py が tour/index.html に差しこむ。 */
var WSTEP=['win_memo','win_decl','win_c1','win_route','win_back','win_price','win_rb','win_name','win_pass'];
var WSTEP_OLD=['win_decl','win_c1','win_c2','win_c5','win_c7','win_c8','win_route','win_rec','win_rules','win_count','win_price','win_rb','win_name','win_pass'];   /* 089より前のセーブの step(番号)を読みかえる用 */
var ORD=['','first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth','eleventh','twelfth','thirteenth','fourteenth','fifteenth','sixteenth','seventeenth','eighteenth','nineteenth','twentieth','twenty first','twenty second','twenty third','twenty fourth','twenty fifth','twenty sixth','twenty seventh','twenty eighth','twenty ninth','thirtieth','thirty first'];
var WSTOP={a:1,an:1,the:1,to:1,of:1,'in':1,on:1,at:1,and:1,or:1,'for':1,'with':1,from:1,as:1,is:1,am:1,are:1,be:1,it:1,that:1,'this':1,my:1,your:1,our:1,so:1};
/* カンペの強調(＊): 冠詞・前置詞などのほかを太字にする(data 側の star() と同じ規則) */
function wst(s){return s.split(' ').map(function(tok){var m=/^([^A-Za-z0-9]*)(.*?[A-Za-z0-9])([^A-Za-z0-9]*)$/.exec(tok);if(!m||WSTOP[m[2].toLowerCase()])return tok;return m[1]+'*'+m[2]+'*'+m[3]}).join(' ')}

/* ---- 次の旅のメモ(はじめからでも消えない別のキー。端末の中だけ) ---- */
var MEMOKEY='kanpe-tour-memo-v1';
function memoLoad(){try{var a=JSON.parse(localStorage.getItem(MEMOKEY)||'[]');return Array.isArray(a)?a.filter(function(x){return typeof x==='string'&&x.length<40}).slice(0,12):[]}catch(e){return[]}}
function winMemo(en){var a=memoLoad();if(a.indexOf(en)<0)a.push(en);try{localStorage.setItem(MEMOKEY,JSON.stringify(a))}catch(e){}}

/* ---- 状態: save.win = {step, m:{場面:{t,why}}, cont, pick, done, ver:2, dd:宣言済み, rr:ルール・地図の説明済み, vis:窓口に来た回数, rrv:説明したときの回数, bk:再訪の挨拶済み} ---- */
function winMigrate(W){
 if(W.ver===2)return;
 var nm=WSTEP_OLD[W.step]||WSTEP_OLD[0],oi=WSTEP_OLD.indexOf(nm),ni=-1,rv=WSTEP_OLD.indexOf('win_route');
 for(var j=oi;j<WSTEP_OLD.length&&ni<0;j++)ni=WSTEP.indexOf(WSTEP_OLD[j]);
 W.step=ni<0?0:ni;W.ver=2;if(oi>0)W.dd=1;if(oi>rv){W.rr=1;W.rrv=1}}
function winStart(){
 var W=save.win,old=W;if(!W||typeof W!=='object'||W.done){W=save.win={step:0,m:{},cont:5,pick:null,ver:2,vis:0,dd:(old&&old.dd)?1:0,rr:(old&&old.rr)?1:0,rrv:(old&&old.rrv)||0}}
 if(!W.m||typeof W.m!=='object')W.m={};if(typeof W.step!=='number'||W.step<0||W.step>=WSTEP.length)W.step=0;
 winMigrate(W);W.vis=(W.vis||0)+1;
 if(W.rr&&W.vis>(W.rrv||0)&&!W.bk&&W.step>WSTEP.indexOf('win_back'))W.gh=1;   /* 説明のあと、値段などへ進んだ状態で出た人も、戻ったら挨拶から */
 storeSave();winRun()}
function winVid(k){
 /* 088: どの分岐でも券はスター。save.win.pick が ow でも(古いセーブ・点検モード)、ここで無視する */
 if(k==='win_price')return 'win_price_star';if(k==='win_rb')return 'win_rb_star';if(k==='win_pass')return 'ticket_star';return k}
/* 089: 済んだ部分は飛ばす。前の旅のメモは中身があるときだけ。再訪の挨拶は「説明したのとは別の回に来たとき」だけ */
function winSkip(W,k){
 if(k==='win_memo')return !!W.dd||!winMemoBuild();
 if(k==='win_decl')return !!W.dd;
 if(k==='win_c1'||k==='win_route')return !!W.rr;
 if(k==='win_back')return !(W.rr&&(W.vis||0)>(W.rrv||0)&&!W.bk);
 return false}
function winRun(){
 var W=save.win;
 if(W.gh===1&&!W.bk){W.bk=1;W.gh=2;storeSave();startVid(PBY.ticket,'win_back','win');return}   /* 挨拶だけ。終わったら同じ段にもどる */
 while(WSTEP[W.step]&&winSkip(W,WSTEP[W.step]))W.step++;
 var k=WSTEP[W.step];if(!k){showMap();return}
 if(k==='win_decl'&&voiceNeedConsent()){winConsent();return}   /* 宣言の直前に、声を送ってよいかを一度だけ聞く(013 3-3) */
 if(k==='win_rec')winRecBuild();
 if(k==='win_back'){W.bk=1;storeSave()}
 var vid=winVid(k),pl=PBY.ticket;
 if(k==='win_pass'){save.ticket='star';W.pick='star';W.done=1;storeSave();startVid(pl,vid,'hub');return}
 startVid(pl,vid,'win')}
function winAfter(S){var W=save.win,k=WSTEP[W.step];
 if(W.gh===2){W.gh=0;storeSave();winRun();return}

 if(k==='win_decl')W.dd=1;
 if(k==='win_route'){W.rr=1;W.rrv=W.vis||1}
 W.step++;storeSave();winRun()}

/* 同意の1枚: 賢者の見送りのあと、宣言の直前。ルルが紙をわたす。選んだら宣言へ進む */
function winConsent(){
 DLG.win_consent=DLG.win_consent||{who:'Lulu',story:0,bg:'tdesk',sp:'',hero:'blue',lulu:'plain',nogold:1,inter:[],intro:'',lines:[],words:[],win:1,auto:1,hook:'consent'};
 startVid(PBY.ticket,'win_consent','win')}
function consentScene(S){
 applyCtx({bg:'tdesk',who:'Lulu',sp:'lulu',hero:'blue',lulu:'plain',gold:0});
 var en='King, one question before we start.';setMsgInstant(en,'Lulu');spSay=false;say(en,.95,1.35);
 consentCard(function(){winRun()})}

/* 前の旅のメモ・苦手な音があれば、宣言とは別の短いやり取りにする(089。係員の1つの吹き出しは1文まで)。なければ false を返し、この段は飛ばす */
function winMemoBuild(){
 var mm=memoLoad(),nx=vLoad().next,k=nx&&nx.k?String(nx.k).slice(0,12):'',L=[];
 if(!mm.length&&!k)return false;
 L.push({n:"Welcome back.",jp:'おかえりなさい。'},{y:wst("Thank you."),jp:'ありがとう。'});
 if(mm.length){
  L.push({n:"Last time, you wanted to see "+mm.join(' and ')+".",jp:'前回、'+mm.join('と')+'に行きたいと言っていましたね。'},{y:wst("Yes, I did."),jp:'はい、そうです。'});
  L.push({n:"I wrote it down for your next trip.",jp:'次の旅のために、メモしておきました。'},{y:wst("Thank you."),jp:'ありがとう。'})}
 if(k){
  L.push({n:"Last time, the \""+k+"\" sound was a little hard.",jp:'前回は、「'+k+'」の音が少しむずかしかったですね。'},{y:wst("Yes, it was."),jp:'はい、そうでした。'});
  L.push({n:"Let's meet it again on the road.",jp:'旅の途中で、また会いましょう。'},{y:wst("Okay!"),jp:'はい！'})}
 DLG.win_memo={who:'世界一周の窓口係',story:1,bg:'tdesk',sp:'desk_rtw',hero:'blue',lulu:'plain',nogold:1,inter:[],intro:'The Round the World desk.',win:1,auto:1,words:[],lines:L};
 return true}

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

/* ---- 宣言のマイク(タスク089): プレイヤーが話す番になったら、ステージの右下に大きいマイクのドット絵を出す。
   「ルルが言う → 大きなマイクが出る → プレイヤーが言う」を目で見て分かるように。きいている間は、はねる。次の画面(clearPanel)で消える。
   素材: PM が新しいドット絵を用意する。MICBIG_IMG にファイル名を入れると、それに差しかわる(空のあいだは、下の仮のドット絵) ---- */
var MICBIG_IMG='assets/art/mic-large-v1.png';   /* タスク090: PM作成の大きなマイク(240×240・透明PNG)。仮のドット絵(MICPIX)は、画像が読めないときの保険として残す */
var MICPIX=["...XXXXXX...","..XhggggggX.",".XhgXgXgXggX",".XgXgXgXgXgX",".XgggggggggX",".XgXgXgXgXgX",".XgggggggggX",".XmmmmmmmmmX","..XmmmmmmmX.","...XrrrrrX..","....XmmmX...","....XmmmX...","....XmmmX...","....XmmmX...","..XXXmmmXXX.",".XmmmmmmmmmX",".XXXXXXXXXXX"];
function declMicPix(box){var cv=document.createElement('canvas');cv.width=12;cv.height=17;var cx=cv.getContext('2d'),COL={X:'#3a2a1a',g:'#d8dce6',h:'#ffffff',m:'#8a8f9a',r:'#e8452c'};
 MICPIX.forEach(function(row,y){for(var x=0;x<row.length;x++){var c=COL[row.charAt(x)];if(c){cx.fillStyle=c;cx.fillRect(x,y,1,1)}}});box.appendChild(cv)}
function declMic(act){
 var st=document.querySelector('#sceneView .stage');if(!st)return;declMicOff();
 var box=el('div','declmic');box.setAttribute('aria-hidden','true');
 if(MICBIG_IMG){var im=new Image();im.alt='';im.onerror=function(){if(im.parentNode){box.removeChild(im);declMicPix(box)}};im.src=MICBIG_IMG;box.appendChild(im)}
 else declMicPix(box);
 st.appendChild(box);G.dmic=box;
 function sync(){box.classList.toggle('on',act.classList.contains('down'))}
 try{var mo=new MutationObserver(sync);mo.observe(act,{attributes:true,attributeFilter:['class']});box._mo=mo}catch(e){}
 sync()}
function declMicOff(){var b=G.dmic;if(b){if(b._mo){try{b._mo.disconnect()}catch(e){}}if(b.parentNode)b.parentNode.removeChild(b)}G.dmic=null}

/* ---- 線を引く地図(窓口の壁。絵が使えないときの描き直し用): 1周目の実際のルート16区間(089) 羽田→ナイロビ→ドーハ→…→グアム→羽田。番号の札と数えるカウンターは、絵の側(art.js)と同じ ---- */
var WM=/*WMAP*/[];
var WP={tok:[139.8,35.5,'HANEDA',0,8],nbo:[36.8,-1.3,'',0,0],doh:[51.5,25.3,'',0,0],rov:[25.7,66.5,'',0,0],ath:[23.7,38,'',0,0],rom:[12.5,41.9,'',0,0],zur:[8.5,47.4,'',0,0],fra:[8.7,50.1,'',0,0],lon:[-0.1,51.5,'',0,0],lis:[-9.1,38.7,'',0,0],nyc:[-74,40.7,'',0,0],hon:[-157.9,21.3,'',0,0],syd:[151.2,-33.9,'',0,0],sin:[103.8,1.4,'',0,0],bkk:[100.5,13.7,'',0,0],gum:[144.8,13.5,'',0,0]};
var WSG=[['tok','nbo',0],['nbo','doh',0],['doh','rov',0],['rov','ath',0],['ath','rom',0],['rom','zur',0],['zur','fra',0],['fra','lon',0],['lon','lis',0],['lis','nyc',0],['nyc','hon',0],['hon','syd',-360],['syd','sin',0],['sin','bkk',0],['bkk','gum',0],['gum','tok',0]];
function wmx(lon){return 22+(lon+180)/360*276}function wmy(lat){return 40+(75-lat)/130*48}
function wmPt(a,b,sh,f){var A=WP[a],B=WP[b],lon=A[0]+(B[0]+sh-A[0])*f,lat=A[1]+(B[1]-A[1])*f,x=wmx(lon),y=wmy(lat);while(x<22)x+=276;while(x>=298)x-=276;return [x,y]}
function wmN(a,b,sh){var A=WP[a],B=WP[b];return Math.max(2,Math.round(Math.sqrt(Math.pow((B[0]+sh-A[0])*.77,2)+Math.pow((B[1]-A[1])*.37,2))/2.2))}
function wmSeg(i,f,col){var sg=WSG[i],n=wmN(sg[0],sg[1],sg[2]);for(var k=0;k<=n*f;k++){var q=wmPt(sg[0],sg[1],sg[2],k/n);R(col,q[0]-1,q[1]-1,2,2)}}
BGS.rtmap=function(ctx,S){
 airWall('#e9edf3');floorAir('#d8dce6','#c4c8d4');
 R('#0b1d33',17,36,286,56);R('#f4f1e8',17,36,286,1);R('#f4f1e8',17,91,286,1);R('#1c4a78',22,40,276,48);
 for(var r=0;r<WM.length;r++){var row=WM[r];for(var c0=0;c0<row.length;c0++)if(row.charAt(c0)==='#')R(((r+c0)%5===0)?'#4f9a5c':'#3f8450',22+c0*3,40+r*3,3,3)}
 var rf=(S&&S.rf)||0,rn=(S&&S.rn)||0,e=(S&&S.rt!=null)?t-S.rt:0,D=.8,mv=0;
 for(var i=0;i<WSG.length;i++){if(i<rf){wmSeg(i,1,'#ffd36a');mv=i+1}else if(i<rn){var f=Math.max(0,Math.min(1,(e-(i-rf)*D)/D));if(f>0){wmSeg(i,f,'#ffd36a');mv=i+1}}}
 Object.keys(WP).forEach(function(k){var p=WP[k],x=wmx(p[0]),y=wmy(p[1]);R('#0b1d33',x-2,y-2,4,4);R('#ffd36a',x-1,y-1,2,2);if(p[2])T(p[2],x+p[3],y+p[4],5,'#fff')});
 if(mv>0)T('MOVES '+mv+'/16',60,98,6,'#ffd36a');
 if(S&&S.stp>0)T('STOPS '+S.stp+'/15',250,98,6,'#ffd36a')};
