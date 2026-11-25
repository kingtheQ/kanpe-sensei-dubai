/* ===== チェックモード(タスク056): ?check=1 を付けた時だけ動く。付けなければ、ここは何もしない =====
   (1) 場所は全部ロックなしで開く(build.py 側で lockedPlace・タブの鍵・券のタブの出し入れを window.__CHK で外す)
   (2) 「CHECK」ボタンから場面一覧を開き、どの場面でも直接始められる。券は Star / oneworld をここで切りかえる
   (3) 前提は満たしたものとして扱う: 券は選んだ扱い・前の場面の言い分け(持ち越し)は返る・割りこみ(出来事)は自動では入らない
   (4) 進行は専用の記録(chk1:)へ。通常のセーブは変わらない(check_shim.js)。旅の骨組み(TRIP: DAY・お金・場所の鍵)は動かさない */
(function(){
if(!window.__CHK)return;
var OTHER_HREF='__OTHER_HREF__',OTHER_LABEL='__OTHER_LABEL__';
if(save.ticket!=='star'&&save.ticket!=='ow')save.ticket='ow';
try{document.title='[CHECK] '+document.title}catch(e){}
var css=document.createElement('style');
css.textContent='#chkBtn{position:fixed;left:0;top:46%;z-index:99990;min-width:48px;min-height:40px;padding:4px 8px;border-left:0!important;border-radius:0 8px 8px 0!important;font:700 13px monospace;color:#10131f;background:#ffc72c;border:2px solid #10131f;opacity:.9}'
+'#chkPan{position:fixed;inset:0;z-index:99991;overflow:auto;-webkit-overflow-scrolling:touch;background:#10131f;color:#fff;font:14px/1.45 monospace;padding:12px 12px 80px;box-sizing:border-box}'
+'#chkPan[hidden]{display:none}#chkPan h2{margin:0 0 4px;font-size:16px;color:#ffc72c}#chkPan h3{margin:14px 0 4px;font-size:14px;color:#9ad0e4;border-bottom:1px solid #3a4260}'
+'#chkPan .row{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:4px 0}#chkPan .pn{flex:0 0 100%;font-size:12px;color:#c9cfe4}'
+'#chkPan button,#chkPan a.b{min-height:40px;padding:6px 10px;font:13px monospace;color:#fff;background:#2a3050;border:2px solid #6a74a8;border-radius:6px;text-decoration:none;display:inline-flex;align-items:center}'
+'#chkPan button.on{background:#ffc72c;color:#10131f;border-color:#fff}#chkPan .x{position:sticky;top:0;float:right;background:#8a1538;border-color:#fff}#chkPan p{margin:4px 0;font-size:12px;color:#c9cfe4}';
document.head.appendChild(css);
var btn=el('button','','CHECK');btn.id='chkBtn';btn.type='button';document.body.appendChild(btn);
var pan=el('div','');pan.id='chkPan';pan.hidden=true;document.body.appendChild(pan);
function close(){pan.hidden=true}
function modeOf(id){var ks=Object.keys(MODES),i,j;for(i=0;i<ks.length;i++){var ps=MODES[ks[i]].p;for(j=0;j<ps.length;j++)if(ps[j].id===id)return ks[i]}return null}
/* 場面を直接始める。前の場面・券・お金は満たしたものとして、場所の鍵は見ない */
function start(pl,vid,from){
 if(!DLG[vid])return;close();
 var mk=modeOf(pl.id);if(mk&&MODE!==mk)setMode(mk);G.at=pl.id;showMap();
 G.evCont=null;startVid(pl,vid,from||null)}
function startPA(from){
 var pl=PBY.hplane;if(!pl||!window.PA)return;close();
 var mk=modeOf(pl.id);if(mk&&MODE!==mk)setMode(mk);G.at=pl.id;showMap();G.evCont=null;
 PA.chk(pl,save.ticket==='star'?'star':'ow',from)}
function startWin(key){
 var i=WSTEP.indexOf(key);if(i<0)return;close();
 if(MODE!=='sage'&&MODES.sage){setMode('sage')}G.at='ticket';showMap();
 save.win={step:i,m:{},cont:5,pick:'star'};storeSave();winRun()}
function openPlace(pl){close();var mk=modeOf(pl.id);if(mk&&MODE!==mk)setMode(mk);G.at=pl.id;showMap();enterPlace(pl.id)}
function vids(p){var a=[],add=function(v){if(v&&a.indexOf(v)<0&&DLG[v])a.push(v)};(p.v||[]).forEach(add);if(p.tkv)Object.keys(p.tkv).forEach(function(k){p.tkv[k].forEach(add)});if(p.menu)p.menu.forEach(function(m){add(m[1])});return a}
function sbtn(t,fn,on){var b=el('button',on?'on':'',t);b.type='button';b.addEventListener('click',fn);return b}
function build(){
 pan.textContent='';
 var x=sbtn('閉じる',close);x.className='x';pan.appendChild(x);
 pan.appendChild(el('h2','','点検モード(?check=1)'));
 pan.appendChild(el('p','','記録は専用の置き場。通常のセーブは読みも書きも消しもしません。'));
 pan.appendChild(el('h3','','券(場面が券ごとに分かれる場所に効く)'));
 var r1=el('div','row');
 r1.appendChild(sbtn('Star Alliance',function(){save.ticket='star';storeSave();build()},save.ticket==='star'));
 r1.appendChild(sbtn('oneworld',function(){save.ticket='ow';storeSave();build()},save.ticket==='ow'));
 pan.appendChild(r1);
 pan.appendChild(el('h3','','ページ'));
 var r2=el('div','row'),a=el('a','b',OTHER_LABEL+'へ(点検モードのまま)');a.href=OTHER_HREF;r2.appendChild(a);
 var a2=el('a','b','通常モードで開く');a2.href=location.pathname;r2.appendChild(a2);
 r2.appendChild(sbtn('専用の記録を消す',function(){if(window.__chkReset)window.__chkReset();location.reload()}));
 pan.appendChild(r2);
 Object.keys(MODES).forEach(function(k){
  pan.appendChild(el('h3','','場面一覧: '+MODES[k].b));
  MODES[k].p.forEach(function(p){
   var row=el('div','row');row.appendChild(el('div','pn',(p.name||p.id)+'  ['+p.id+']'));
   var vs=vids(p);
   vs.forEach(function(v){row.appendChild(sbtn(v,function(){start(p,v,p.hub?'hub':null)}))});
   if(!vs.length||p.listen||p.rest)row.appendChild(sbtn('開く',function(){openPlace(p)}));
   pan.appendChild(row)})});
 var evs=[];(typeof EVSLOTS!=='undefined'?EVSLOTS:[]).forEach(function(s){if(DLG[s.vid]&&evs.indexOf(s.vid)<0)evs.push(s.vid)});
 if(evs.length){pan.appendChild(el('h3','','割りこみ・顔なじみ(出来事の場面)'));var re=el('div','row');
  evs.forEach(function(v){var sl=null;EVSLOTS.forEach(function(s){if(s.vid===v&&!sl)sl=s});var pl=(sl&&PBY[sl.key])||PBY[Object.keys(PBY)[0]];re.appendChild(sbtn(v,function(){start(pl,v,'ev')}))});pan.appendChild(re)}
 if(window.PA&&PA.chk&&PBY.hplane){var pk=save.ticket==='star'?'star':'ow',pr=el('div','row');
  pr.appendChild(el('div','pn','CAアナウンス(048): いまの券 '+(pk==='star'?'Star Alliance → Istanbul':'oneworld → Doha')+'(券は上で切りかえ)'));
  pr.appendChild(sbtn('CAアナウンス 通し',function(){startPA('ca')}));
  pr.appendChild(sbtn('機内食の場面だけ',function(){startPA('meal')}));
  pan.appendChild(pr);pan.appendChild(el('p','','通し: CA場面 → マイク → 機内食で自分の声。声は専用の置き場だけ。終わると地図へ戻る。'))}
 if(typeof WSTEP!=='undefined'&&MODES.sage){pan.appendChild(el('h3','','窓口の流れ(選んだ段から先へ進む)'));var rw=el('div','row');
  WSTEP.forEach(function(k){rw.appendChild(sbtn(k,function(){startWin(k)}))});pan.appendChild(rw)}
}
btn.addEventListener('click',function(){build();pan.hidden=false;pan.scrollTop=0});
})();
