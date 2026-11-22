/* ===== チェックモード(タスク056)の入口: ページの最初に走る。URL に ?check=1 がなければ何もしない(通常の見た目・動作のまま) =====
   ?check=1 のときだけ、localStorage の読み書きを専用の名前(chk1:)へ向ける。通常のセーブ(kanpe-…)は読まず・書かず・消さない。
   設定(音のON/OFFなど)だけは、専用の記録が空のあいだ通常の値を読む(書くのは専用側)。 */
(function(){
 var CHK=/[?&]check=1(?:&|#|$)/.test(location.search);
 window.__CHK=CHK;if(!CHK)return;
 var P='chk1:',SHARE={'kd_snd':1,'kanpe-set-v1':1},S=Storage.prototype,g=S.getItem,s=S.setItem,r=S.removeItem;
 function mine(o){try{return o===window.localStorage}catch(e){return false}}
 S.getItem=function(k){if(!mine(this))return g.call(this,k);k=String(k);var v=g.call(this,P+k);if(v===null&&SHARE[k])return g.call(this,k);return v};
 S.setItem=function(k,v){if(!mine(this))return s.call(this,k,v);return s.call(this,P+String(k),v)};
 S.removeItem=function(k){if(!mine(this))return r.call(this,k);return r.call(this,P+String(k))};
 /* IndexedDB(CAアナウンスの録音 kanpe-pa-rec-v1)も、専用の名前(chk1:…)へ向ける。通常の録音は読まず・書かず・消さない */
 var IDBX=null;try{var F=IDBFactory.prototype,io=F.open,idd=F.deleteDatabase;IDBX={del:function(n){try{idd.call(window.indexedDB,P+n)}catch(e){}}};
  F.open=function(n){return io.apply(this,[P+String(n)].concat([].slice.call(arguments,1)))};F.deleteDatabase=function(n){return idd.call(this,P+String(n))}}catch(e){}
 /* 専用の記録だけを消す(通常のセーブは消さない) */
 window.__chkReset=function(){var ks=[],i,L=window.localStorage;for(i=0;i<L.length;i++){var k=L.key(i);if(k&&k.indexOf(P)===0)ks.push(k)}ks.forEach(function(k){r.call(L,k)});if(IDBX)IDBX.del('kanpe-pa-rec-v1')};
})();
