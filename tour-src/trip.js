/* ===== 世界一周編: 旅の骨組み(タスク030。設計の正本: docs/pm/deliverables/020-journey-structure-design-v1.md) =====
   DAY(朝の1枚を開いた回数)・券の束(搭乗券のつづり)・日ごとの記録(kanpe-trip-v1)・夜の1枚・精算とアルバムへの渡し。
   tour/・tour/doha/・tour/ending/・world/ に、ビルド(tour-src/build.py)が同じものを入れる。
   画面の文字は英語(券の束を見る入口と、世界マップの数え方だけ日本語)。点数・発音の結果は出さない(004-5)。連続記録は使わない。
   記録 kanpe-trip-v1 は端末の中だけ。個人情報・声・画像は入れない(写真は場面の名前を持つだけ)。 */
var TRIP=(function(){
 var KEY='kanpe-trip-v1',TKEY='kanpe-tour-save-v1';
 var has=function(o,k){return Object.prototype.hasOwnProperty.call(o,k)};
 /* ---------- 空港(世界マップの id と 3文字コード) ---------- */
 var AIRP={
  HND:{id:'haneda',n:'羽田',en:'Tokyo',lon:139.78,lat:35.55},DOH:{id:'doha',n:'ドーハ',en:'Doha',lon:51.61,lat:25.27},
  NBO:{id:'nairobi',n:'ナイロビ',en:'Nairobi',lon:36.93,lat:-1.32},HEL:{id:'helsinki',n:'ヘルシンキ',en:'Helsinki',lon:24.96,lat:60.32},
  RVN:{id:'rovaniemi',n:'ロヴァニエミ',en:'Rovaniemi',lon:25.83,lat:66.56},MAD:{id:'madrid',n:'マドリード',en:'Madrid',lon:-3.57,lat:40.49},
  LIM:{id:'lima',n:'リマ',en:'Lima',lon:-77.11,lat:-12.02},CUZ:{id:'cusco',n:'クスコ',en:'Cusco',lon:-71.94,lat:-13.54},
  MIA:{id:'miami',n:'マイアミ',en:'Miami',lon:-80.29,lat:25.79},DFW:{id:'dallas',n:'ダラス',en:'Dallas',lon:-97.04,lat:32.90},
  HNL:{id:'honolulu',n:'ホノルル',en:'Honolulu',lon:-157.92,lat:21.32},IST:{id:'istanbul',n:'イスタンブール',en:'Istanbul',lon:28.82,lat:41.26},
  ADD:{id:'addis',n:'アディスアベバ',en:'Addis Ababa',lon:38.80,lat:8.98},BOG:{id:'bogota',n:'ボゴタ',en:'Bogota',lon:-74.15,lat:4.70},
  IAH:{id:'houston',n:'ヒューストン',en:'Houston',lon:-95.34,lat:29.98},GUM:{id:'guam',n:'グアム',en:'Guam',lon:144.80,lat:13.48},
  NRT:{id:'narita',n:'成田',en:'Tokyo',lon:140.39,lat:35.77},
  ATH:{id:'athens',n:'アテネ',en:'Athens',lon:23.94,lat:37.94},
  FCO:{id:'rome',n:'ローマ',en:'Rome',lon:12.25,lat:41.80},
  ZRH:{id:'zurich',n:'チューリッヒ',en:'Zurich',lon:8.54,lat:47.38},
  FRA:{id:'frankfurt',n:'フランクフルト',en:'Frankfurt',lon:8.66,lat:50.11},
  SYD:{id:'sydney',n:'シドニー',en:'Sydney',lon:151.18,lat:-33.94}};   /* 096: チューリッヒ(中央駅。ローマからミラノ乗り換えの鉄道で着き、フランクフルトへ直通ICE) */   /* 097: フランクフルト(1周目ルートのチューリッヒの次。鉄道の旅。座標は中央駅付近の公開座標) */   /* 090: アテネ(1周目ルートのロヴァニエミの次。窓口の地図 window_data.ROUTE_STOPS と同じ) */
 var IMPL={HND:1,NBO:1,DOH:1,RVN:1,ATH:1,FCO:1,ZRH:1,FRA:1,HNL:1,SYD:1};   /* 065: ロヴァニエミ(到着まわり)。ヘルシンキは乗り継ぎだけ(chain が場面なしの区間をはさむ) */   /* 場面のある空港。ここ以外の行き先は、地図と券には出すが、行けない */
 function codeOf(apId){for(var k in AIRP)if(AIRP[k].id===apId)return k;return null}
 /* ---------- 券ごとの区間(会社は docs/world-tour-design.md の便の表。別切符は会社を書かない)。[出発,到着,会社,表の日,別切符] ---------- */
 var LEGS={
  ow:[['HND','DOH','Qatar Airways',1],['DOH','NBO','Qatar Airways',2],['NBO','DOH','Qatar Airways',6],['DOH','HEL','Qatar Airways',9],
      ['HEL','RVN','Finnair',10],['RVN','MAD','Iberia',13],['MAD','LIM','Iberia',15],['LIM','CUZ','',17,1],['CUZ','LIM','',21,1],
      ['LIM','MIA','American Airlines',21],['MIA','DFW','American Airlines',22],['DFW','HNL','American Airlines',22],['HNL','HND','Japan Airlines',27]],
  star:[['HND','IST','Turkish Airlines',1],['IST','NBO','Turkish Airlines',2],['NBO','ADD','Ethiopian Airlines',6],['ADD','IST','Ethiopian Airlines',7],
      ['IST','RVN','Turkish Airlines',9],['RVN','IST','Turkish Airlines',12],['IST','BOG','Turkish Airlines',13],['BOG','CUZ','Avianca',15],
      ['CUZ','BOG','Avianca',19],['BOG','IAH','United',19],['IAH','HNL','United',20],['HNL','GUM','United',25],['GUM','NRT','United',28]]};
 /* ---------- 30日の表(020 第2章。場所・日の種類・山・ルルの朝のひとこと・その日に載せる既存の場面) ----------
    [表の日, 朝にいる空港, 種類(air/move/city/rest/home), 山(0なし 1☆ 2★), 英語のひとこと, [載せる場面のまとまり]]
    場面のまとまり(GROUPS)が空の日は、まだ作っていない日。休養日(rest)は、場面なしで夜へ進む日。 */
 var ROWS={
  ow:[[1,'HND','air',1,'Tokyo. Today our trip begins.',['hnd','hnd_dep']],
   [2,'NBO','move',1,'Nairobi. We landed in Kenya.',['nbo_arr']],
   [3,'NBO','city',1,"Nairobi. Let's go to the Maasai Market.",['nbo_market']],   /* 058: 3日目=マサイマーケット(旧「キリンセンター(候補)」。キリンは4日目のサファリで会う) */
   [4,'NBO','city',2,"Nairobi. Let's go on a safari.",['nbo_safari']],
   [5,'NBO','rest',0,'Nairobi. A slow morning.',[]],
   [6,'NBO','air',1,'Nairobi. Our flight to Doha is today.',['nbo_air','nbo_dep','doh_arr']],
   [7,'DOH','city',1,"Doha. Let's walk through the old market.",['doh_city','doh_hotel_am']],
   [8,'DOH','rest',0,'Doha. A slow morning.',[]],
   [9,'DOH','air',1,'Doha. Our flight to Helsinki is today.',['doh_dep']],
   [10,'HEL','air',2,'Rovaniemi. The north, at last.',['rvn_arr']],[11,'RVN','city',1,'Lapland. Dogs and reindeer.',['rvn_stay']],
   [12,'RVN','city',2,'Lapland. Tonight we wait for the lights.',['rvn_night']],[13,'RVN','air',0,'Rovaniemi. Madrid is next.',['rvn_dep']],
   [14,'MAD','city',1,'Madrid. Art and a long lunch.',[]],[15,'MAD','move',0,'Madrid. A very long flight today.',[]],
   [16,'LIM','rest',0,'Lima. A slow morning.',[]],[17,'LIM','air',1,'Lima. We go up into the mountains.',[]],
   [18,'CUZ','city',0,"The Sacred Valley. Let's take the train.",[]],[19,'CUZ','city',2,'Machu Picchu. We are really here.',[]],
   [20,'CUZ','rest',0,'Cusco. A slow morning.',[]],[21,'CUZ','move',0,'Cusco. A long way to Miami today.',[]],
   [22,'MIA','move',1,'Miami. Three airports in one day.',[]],[23,'HNL','rest',0,'Honolulu. A slow morning.',[]],
   [24,'HNL','city',2,'Honolulu. Lulu has a plan for us.',[]],[25,'HNL','city',1,"Honolulu. Let's go around the island.",[]],
   [26,'HNL','city',0,'Honolulu. Time to pack.',[]],[27,'HNL','air',2,'Honolulu. We are going home.',[]],
   [28,'HND','air',0,'Tokyo. Welcome back.',['hnd_ret']],[29,'HND','home',0,'Home. The receipts are on the table.',[]],[30,'HND','home',2,'One month later.',[]]],
  star:[[1,'HND','air',1,'Tokyo. Today our trip begins.',['hnd','hnd_dep']],
   [2,'IST','move',1,'Istanbul. A long wait between flights.',[]],
   [3,'NBO','air',1,'Nairobi. We landed in the middle of the night.',['nbo_arr']],
   [4,'NBO','city',2,"Nairobi. Let's go on a safari.",['nbo_market','nbo_safari']],[5,'NBO','rest',0,'Nairobi. A slow morning.',[]],
   [6,'NBO','air',1,'Nairobi. Our flight to Addis Ababa is today.',['nbo_air']],
   [7,'ADD','move',1,'Addis Ababa. Fog this morning.',[]],[8,'IST','city',1,'Istanbul. The old city and the bazaar.',[]],
   [9,'IST','air',2,'Istanbul. We fly north today.',[]],[10,'RVN','city',1,'Lapland. Dogs and reindeer.',['rvn_arr']],
   [11,'RVN','city',2,'Lapland. Tonight we wait for the lights.',['rvn_stay']],[12,'RVN','move',1,'Rovaniemi. Back to Istanbul.',['rvn_dep']],
   [13,'IST','move',0,'Istanbul. A very long flight today.',[]],[14,'BOG','rest',0,'Bogota. A slow morning.',[]],
   [15,'BOG','air',1,'Bogota. We go up into the mountains.',[]],[16,'CUZ','city',0,"The Sacred Valley. Let's take the train.",[]],
   [17,'CUZ','city',2,'Machu Picchu. We are really here.',[]],[18,'CUZ','rest',0,'Cusco. A slow morning.',[]],
   [19,'CUZ','move',0,'Cusco. A long way to Houston today.',[]],[20,'IAH','air',1,'Houston. Hawaii is next.',[]],
   [21,'HNL','rest',0,'Honolulu. A slow morning.',[]],[22,'HNL','city',2,'Honolulu. Lulu has a plan for us.',[]],
   [23,'HNL','city',1,"Honolulu. Let's go around the island.",[]],[24,'HNL','city',0,'Honolulu. Time to pack.',[]],
   [25,'HNL','move',0,'Honolulu. Today the date changes.',[]],[26,'GUM','air',2,'Guam. We have been here before.',[]],
   [27,'GUM','city',0,'Guam. The beach and the hotel.',[]],[28,'GUM','air',0,'Guam. We are going home.',[]],
   [29,'NRT','home',0,'Home. The receipts are on the table.',[]],[30,'NRT','home',2,'One month later.',[]]]};
 /* スパルタ時間の置き場所(タスク032 / 020-8 案1)。休養の翌日の★(ホノルルの着いた翌々日)に、ルルのスパルタ時間(強化合宿)を1回置く。
    ここは枠だけ: 発生の置き方(表のどの日か)・入口(朝の1枚のあと 強化合宿が開く)・終わり(合宿を終えたら その日が終わり、夜の1枚へ)。
    中身は いまある強化合宿(startCamp)をそのまま使う。合宿の作り直しは別タスク(017)。表の日は ROWS の「前の日が rest・この日が山★(2)」の行 */
 var SPARTA={ow:24,star:22};
 function isSparta(td){var t=S().tk;return !!t&&SPARTA[t]===td}
 /* 発生の置き方が表と合っているか(前の日が休養日・この日が★)。テストが使う */
 function spartaRule(){var o={};['ow','star'].forEach(function(k){var d=SPARTA[k],r=ROWS[k][d-1],q=ROWS[k][d-2];o[k]=!!r&&!!q&&r[0]===d&&r[3]===2&&q[2]==='rest'});return o}
 /* 休養日の「知らせ」(タスク032 / 020-7)。休養日に来るのはこれだけ。答えなくてよい。英文1行(日本語なし)。出来事の内容・数字は物語の中の架空(実在の運行情報ではない)。
    キー = 券の種類 + 表の日。休養日(ROWS の種類が rest)の日だけ */
 var NOTICES={ow5:'Airport staff are on strike today. Some flights may be late.',ow8:'Hot and windy this afternoon. Some outdoor tours may change.',
  ow16:'Morning fog at the airport. Some flights may be late.',ow20:"Tomorrow's train leaves one hour earlier.",ow23:'Light rain this morning. It will clear by noon.',
  star5:'Airport staff are on strike today. Some flights may be late.',star14:'Rain in the city this afternoon.',star18:"Tomorrow's train leaves one hour earlier.",star21:'Light rain this morning. It will clear by noon.'};
 /* 場面のまとまり: 各行 = 1つの場所の場面の名前。全部の場所で、どれか1本あそんでいたら、そのまとまりは終わり(いまのクリアと同じ決まり) */
 var GROUPS={
  hnd:[['ticket_ow','ticket_star']],
  hnd_ret:[['hnd_return']],   /* 059: 28日目(oneworld)の羽田。1日目に拾った落とし物を持ち主に返す。保存の keep.hnd1 があるセーブだけ(GCOND) */
  hnd_dep:[['hnd_checkin_ow','hnd_checkin_star'],['hnd_sec'],['hnd_exit'],['hnd_gate_ow','hnd_gate_star'],['hnd_board_ow','hnd_board_star'],['hnd_plane_ow','hnd_plane_star']],   /* 1日目の羽田(タスク043): 券ごとに場面がちがう。どちらか1本あそべば、その場所は終わり */
  nbo_arr:[['nbo_immig1','nbo_immig2'],['nbo_bag1','nbo_bag2'],['nbo_sim1','nbo_sim2'],['nbo_taxi1','nbo_taxi2']],
  nbo_market:[['nbo_market']],nbo_safari:[['nbo_safari']],   /* 058: ナイロビの滞在。市場=3日目(スターは4日目)・サファリ=4日目 */
  nbo_air:[['nbo_java1','nbo_java2'],['nbo_art1','nbo_art2'],['nbo_lounge1','nbo_lounge2'],['nbo_duty1','nbo_duty2']],
  nbo_dep:[['nbo_checkin1','nbo_checkin2'],['nbo_sec1','nbo_sec2'],['nbo_gate1','nbo_gate2'],['nbo_plane1','nbo_plane2']],
  doh_arr:[['doh_immig1','doh_immig2'],['doh_bag1','doh_bag2'],['doh_sim1','doh_sim2'],['doh_taxi','doh_metro']],
  doh_city:[['doh_city_t2','doh_city_t1','doh_city_t3'],['doh_city_h1','doh_city_h2'],['doh_city_s1','doh_city_s2','doh_city_s3'],['doh_city_r1','doh_city_r2','doh_city_r3'],['doh_city_c1','doh_city_c2','doh_city_c3']],
  doh_hotel_am:[['doh_city_h3','doh_city_h4']],
  rvn_arr:[['rvn_immig1','rvn_immig2'],['rvn_bag1','rvn_bag2'],['rvn_lobby1','rvn_lobby2'],['rvn_wifi1','rvn_wifi2'],['rvn_bus1','rvn_bus2']],
  rvn_stay:[['rvn_village1','rvn_village2'],['rvn_post1','rvn_post2'],['rvn_santa1','rvn_santa2'],['rvn_reindeer1','rvn_reindeer2']],   /* 072: ロヴァニエミの滞在(両ルートとも11日目) */
  rvn_night:[['rvn_hotel1','rvn_hotel2']],   /* 072: 夜のオーロラ待ち(oneworld編12日目。スター編は旅程に入らず、チェックモードから入る) */
  rvn_dep:[['rvn_checkin1','rvn_checkin2'],['rvn_sec1','rvn_sec2'],['rvn_shop1','rvn_shop2'],['rvn_ahkio1','rvn_ahkio2'],['rvn_gate1','rvn_gate2']],   /* 072: ロヴァニエミの出発(oneworld編13日目・スター編12日目)。 065: ロヴァニエミの到着(両方の券とも10日目。ドーハの次の到着枠) */
  ath_arr:[['ath_immig1','ath_immig2'],['ath_taxi1'],['ath_transit1']],   /* 090: アテネ到着(入国審査は2場面を順に。どちらか1本で場所は終わり) */
  ath_city:[['ath_cafe1'],['ath_shop1'],['ath_hotel1']],   /* 091: アテネの街(タベルナ・おみやげ屋・ホテル) */
  ath_dep:[['ath_checkin1'],['ath_depimmig1'],['ath_gate1']],   /* 091: アテネの出発(チェックイン→出国審査の列→搭乗口。順に開く) */
  fra_arr:[['fra_arr1'],['fra_bakery1'],['fra_tram1'],['fra_info1']],   /* 097: フランクフルト到着(鉄道着。入国審査なし。最初の駅の場面→ベーカリー・市内切符・案内所) */
  fra_city:[['fra_cafe1'],['fra_shop1'],['fra_hotel1']],   /* 097: フランクフルトの街(カフェ・おみやげ屋・ホテル) */
  fra_dep:[['fra_dep_board1'],['fra_dep_ticket1'],['fra_dep_train1']],   /* 097: フランクフルトの出発(鉄道。発車標→窓口→ホームと車内。順に開く) */
  hnl_arr:[['hnl_form1'],['hnl_bag1'],['hnl_lei1'],['hnl_trolley1']],   /* 101: ホノルル到着(ニューヨークからの国内線。入国審査なし。農産物申告書→荷物→レイ→ワイキキへ) */
  hnl_city:[['hnl_cafe1'],['hnl_shop1'],['hnl_hotel1']],   /* 101: ホノルルの街(シェイブアイス・おみやげ屋・ホテル) */
  hnl_dep:[['hnl_dep_board1'],['hnl_dep_ticket1'],['hnl_dep_gate1']],   /* 101: ホノルルの出発(シドニー行き国際線。出国審査なし。案内→チェックイン→保安検査。順に開く) */
  syd_arr:[['syd_immig1'],['syd_immig2'],['syd_quarantine1'],['syd_train1']],   /* 102: シドニー到着(入国の機械→ゲートと窓口→検疫→空港の駅。順に開く) */
  syd_city:[['syd_cafe1'],['syd_shop1'],['syd_hotel1']],
  syd_dep:[['syd_dep_checkin1'],['syd_dep_exit1'],['syd_dep_gate1']],   /* 102: シドニーの出発(チェックイン→保安と出国→搭乗口) */
  rom_arr:[['rom_bag1'],['rom_info1'],['rom_taxi1'],['rom_train1']],   /* 094: ローマ到着(入国審査なし=シェンゲン圏内。荷物・客引き・タクシー・空港電車) */
  rom_city:[['rom_cafe1'],['rom_shop1'],['rom_hotel1']],   /* 094: ローマの街(ジェラテリア・おみやげ屋・ホテル) */
  rom_dep:[['rom_dep_ticket1'],['rom_dep_platform1'],['rom_dep_train1']],   /* 094: ローマの出発(鉄道。切符の窓口→発車標とホーム→車内。順に開く。ミラノで1回乗り換え) */
  zur_arr:[['zur_arr1'],['zur_locker1'],['zur_tram1'],['zur_info1']],   /* 096: チューリッヒ到着(鉄道・審査なし。ローマ出発 rom_dep_* の次) */
  zur_city:[['zur_cafe1'],['zur_shop1'],['zur_hotel1']],   /* 096: チューリッヒの街(カフェ・おみやげ屋・ホテル) */
  zur_dep:[['zur_dep_board1'],['zur_dep_ticket1'],['zur_dep_train1']],   /* 096: チューリッヒの出発(発車標→窓口→ホームと車内。フランクフルト行き直通。順に開く) */
  doh_dep:[['doh_dep_checkin','doh_dep_passport'],['doh_dep_bear'],['doh_dep_train'],['doh_dep_orchard','doh_dep_lounge'],['doh_dep_gate','doh_dep_plane']]};
 /* 場所の名前(各ページの place id) → まとまり。鍵(ロック)と、タブの開きに使う */
 var PLACEGRP={hreturn:'hnd_ret',hcheckin:'hnd_dep',hsec:'hnd_dep',hexit:'hnd_dep',hgate:'hnd_dep',hboard:'hnd_dep',hplane:'hnd_dep',immig:'nbo_arr',bag:'nbo_arr',sim:'nbo_arr',taxi:'nbo_arr',market:'nbo_market',safari:'nbo_safari',java:'nbo_air',art:'nbo_air',lounge:'nbo_air',duty:'nbo_air',
  qcheckin:'nbo_dep',nsec:'nbo_dep',gate:'nbo_dep',qplane:'nbo_dep',dimmig:'doh_arr',dbag:'doh_arr',dsim:'doh_arr',dride:'doh_arr',
  calley:'doh_city',chotel:'doh_city',csouq:'doh_city',crest:'doh_city',ccorn:'doh_city',cbreak:'doh_hotel_am',
  dcounter:'doh_dep',dsouth:'doh_dep',dtrain:'doh_dep',dnorth:'doh_dep',dgate:'doh_dep',
  rimmig:'rvn_arr',rbag:'rvn_arr',rlobby:'rvn_arr',rwifi:'rvn_arr',rbus:'rvn_arr',
  rvil:'rvn_stay',rpost:'rvn_stay',rsanta:'rvn_stay',rrein:'rvn_stay',rhotel:'rvn_night',rchk:'rvn_dep',rsec:'rvn_dep',rshop:'rvn_dep',rahk:'rvn_dep',rgate:'rvn_dep',
  aimmig:'ath_arr',ataxi:'ath_arr',ametro:'ath_arr',acafe:'ath_city',ashop:'ath_city',ahotel:'ath_city',acheck:'ath_dep',adepimm:'ath_dep',agate:'ath_dep',
  hnform:'hnl_arr',hnbag:'hnl_arr',hnlei:'hnl_arr',hntrolley:'hnl_arr',hncafe:'hnl_city',hnshop:'hnl_city',hnhotel:'hnl_city',hnboard:'hnl_dep',hnticket:'hnl_dep',hngate:'hnl_dep',
  farr:'fra_arr',fbakery:'fra_arr',ftram:'fra_arr',finfo:'fra_arr',fcafe:'fra_city',fshop:'fra_city',fhotel:'fra_city',fboard:'fra_dep',fticket:'fra_dep',ftrain:'fra_dep',
  simmig1:'syd_arr',simmig2:'syd_arr',squar:'syd_arr',strain:'syd_arr',scafe:'syd_city',sshop:'syd_city',shotel:'syd_city',scheck:'syd_dep',sexit:'syd_dep',sgate:'syd_dep',
  mbag:'rom_arr',minfo:'rom_arr',mtaxi:'rom_arr',mtrain:'rom_arr',mcafe:'rom_city',mshop:'rom_city',mhotel:'rom_city',mdtick:'rom_dep',mdplat:'rom_dep',mdtrain:'rom_dep',
  zarr:'zur_arr',zlock:'zur_arr',ztram:'zur_arr',zinfo:'zur_arr',zcafe:'zur_city',zshop:'zur_city',zhotel:'zur_city',zboard:'zur_dep',zticket:'zur_dep',ztrain:'zur_dep'};
 var MODEGRP={hret:{tour:'hnd_ret'},hdep:{tour:'hnd_dep'},arr:{tour:'nbo_arr',doha:'doh_arr',rovaniemi:'rvn_arr',athens:'ath_arr',rome:'rom_arr',zurich:'zur_arr',frankfurt:'fra_arr',honolulu:'hnl_arr',sydney:'syd_arr'},stay:{tour:['nbo_market','nbo_safari'],rovaniemi:['rvn_stay','rvn_night']},air:{tour:'nbo_air'},dep:{tour:'nbo_dep',doha:'doh_dep',rovaniemi:'rvn_dep',athens:'ath_dep',rome:'rom_dep',zurich:'zur_dep',frankfurt:'fra_dep',honolulu:'hnl_dep',sydney:'syd_dep'},city:{doha:'doh_city',athens:'ath_city',rome:'rom_city',zurich:'zur_city',frankfurt:'fra_city',honolulu:'hnl_city',sydney:'syd_city'},sage:{tour:'hnd'}};
 /* お金の1行(場面の台詞に出る値段。円に直すレートは架空で固定)。タクシーとメトロは台詞に値段がないので、架空の値段 */
 var MONEY={nbo_sim1:['sim',1000,'KES'],nbo_taxi1:['taxi',3000,'KES'],nbo_java1:['coffee',800,'KES'],nbo_market:['gift',1500,'KES'],nbo_duty1:['duty',24,'USD'],
  doh_sim1:['sim',30,'QAR'],doh_taxi:['taxi',55,'QAR'],doh_metro:['metro',6,'QAR'],doh_city_t1:['tea',2,'QAR'],doh_city_s1:['gift',10,'QAR'],
  doh_city_s3:['gift',22,'QAR'],doh_city_r3:['dinner',80,'QAR'],doh_city_c2:['boat',50,'QAR']};
 var PICK={doh_taxi:'taxi',doh_metro:'metro'};
 var RATE={JPY:1,KES:1.2,USD:150,QAR:41};
 var LBL={ticket:'Ticket',sim:'SIM card',taxi:'Taxi',metro:'Metro',coffee:'Coffee',duty:'Duty free',tea:'Tea',gift:'Gift',dinner:'Dinner',boat:'Boat ride',fee:'Fee',sep:'Separate ticket'};
 var TICKETPRICE={star:958900,ow5:1074300,ow4:936500};
 /* 29日目の精算の「手数料」「別切符」(タスク032 / 020-10)。値段は物語の中の架空(実在の手数料の数字ではない。020-10)。
    別切符: 券の区間のうち sep の区間(oneworld のリマ⇄クスコ)をちぎったとき、1回ずつ記録帳に載る。手数料: 場面が TRIP.addFee で載せる(いまそれを使う場面はまだない) */
 var SEPTICKET=['sep',95,'USD'];
 /* 場面の絵の名前 → 写真の見た目(場面の絵が使えないページ=世界マップで、控えの写真に使う) */
 var THEME={checkinT:'air',immigH:'air',hgateOW:'air',hgateST:'air',cabinT:'cabin',tdesk:'desk',sage:'desk',javaK:'air',artK:'air',safariK:'street',marketK:'souq',lounge:'lng',duty:'air',gate:'air',sim:'air',taxi:'street',checkinQ:'air',cabinQ:'cabin',
  dimmig:'dair',dbag:'dair',dsim:'dair',dtaxi:'street',dmetro:'dair',dcheck:'dair',dsouth:'dair',dtrain:'dair',dorch:'dair',dlng:'lng',dgate:'dair',dcabin:'cabin',
  calley:'souq',chotel:'hotel',csouq:'souq',crest:'souq',cbreak:'hotel',ccorn:'sea',night:'night',nap:'night',
  rimmig:'dair',rbag:'dair',rlobby:'dair',rwifi:'dair',rbus:'night',
  rvil:'street',rpost:'hotel',rsanta:'hotel',rrein:'street',rhotel:'night',rchk:'dair',rsec:'dair',rshop:'dair',rahk:'dair',rgate:'dair',
  aimmig:'dair',ataxi:'street',ametro:'dair',acafe:'souq',ashop:'souq',ahotel:'hotel',acheck:'dair',adepimm:'dair',agate:'dair',
  hnform:'dair',hnbag:'dair',hnlei:'dair',hntrolley:'street',hncafe:'street',hnshop:'souq',hnhotel:'hotel',hnboard:'dair',hnticket:'dair',hngate:'dair',
  farr:'dair',fbakery:'dair',ftram:'street',finfo:'dair',fcafe:'souq',fshop:'souq',fhotel:'hotel',fboard:'dair',fticket:'dair',ftrain:'dair',
  mbag:'dair',minfo:'dair',mtaxi:'street',mtrain:'dair',mcafe:'souq',mshop:'souq',mhotel:'hotel',mdtick:'dair',mdplat:'dair',mdtrain:'dair',
  zarr:'dair',zlock:'dair',ztram:'street',zinfo:'dair',zcafe:'street',zshop:'souq',zhotel:'hotel',zboard:'dair',zticket:'dair',ztrain:'dair'};

 /* ---------- 場面の現地時刻(タスク032 / 020-3) ----------
    旅の中の場面は、いまの本当の時計でなく「旅の中の現地時刻」で昼夜を決める。
    時刻は場所(各ページの place id)ごと。台本のあいさつ(Good morning / afternoon / evening)と、便の時間(docs/world-tour-design.md)に合わせた。
    便の時刻は作る直前に公式で確認する(docs の決まり)。ここは物語の時刻で、実在の便の時刻ではない。旅の外(ドバイ編・グアム編など)は本当の時計のまま。 */
 var HOUR={
  hreturn:22,hcheckin:21,hsec:22,hexit:22,hgate:23,hboard:23,hplane:0, /* 羽田の出発(深夜便。物語の時刻で、実在の便の時刻ではない) */
  immig:9,bag:9,sim:10,taxi:10,                       /* ナイロビ到着(台本: Good morning) */
  market:11,safari:8,                                  /* ナイロビの滞在(058): 市場=昼前・サファリ=朝(背景は昼の絵。時刻は台本のあいさつに使う) */
  java:12,art:13,lounge:14,duty:15,                    /* ナイロビの空港(昼すぎ) */
  qcheckin:16,nsec:17,gate:18,qplane:19,               /* ナイロビ出発(台本: 午後〜Good evening)。夕方の便 */
  dimmig:22,dbag:22,dsim:22,dride:22,                  /* ドーハ到着(台本: Good evening。ナイロビから約5時間) */
  calley:20,chotel:21,csouq:19,crest:20,               /* ドーハ市内の夜(台本: Good evening) */
  cbreak:7,ccorn:10,                                   /* ドーハの翌朝(朝食 6:30〜・コルニーシュは朝食のあと) */
  dcounter:13,dsouth:14,dtrain:14,dnorth:15,dgate:15,
  rimmig:23,rbag:23,rlobby:23,rwifi:23,rbus:23,
  rvil:13,rpost:14,rsanta:15,rrein:16,rhotel:21,                /* ロヴァニエミの滞在(072): 村=昼すぎ・郵便局・サンタ・トナカイは午後(台本: Good afternoon)・ホテルは夜(台本: Good evening)。物語の時刻 */
  rchk:12,rsec:13,rshop:13,rahk:14,rgate:15,
  aimmig:14,ataxi:15,ametro:15,acafe:13,ashop:16,ahotel:19,acheck:9,adepimm:10,agate:10,
  hnform:14,hnbag:14,hnlei:15,hntrolley:15,hncafe:14,hnshop:16,hnhotel:16,hnboard:9,hnticket:9,hngate:10,   /* ホノルル(101。物語の時刻で、実在の便の時刻ではない) */
  farr:15,fbakery:15,ftram:15,finfo:16,fcafe:14,fshop:16,fhotel:19,fboard:8,fticket:8,ftrain:9,
  mbag:11,minfo:11,mtaxi:12,mtrain:12,mcafe:15,mshop:16,mhotel:19,mdtick:9,mdplat:10,mdtrain:11,
  zarr:14,zlock:14,ztram:15,zinfo:15,zcafe:16,zshop:17,zhotel:19,zboard:9,zticket:9,ztrain:10,
  simmig1:7,simmig2:7,squar:8,strain:8,scafe:10,sshop:14,shotel:16,scheck:10,sexit:10,sgate:11};   /* シドニー(102。物語の時刻で、実在の便の時刻ではない) */   /* チューリッヒ(096。物語の時刻で、実在の便の時刻ではない。ホテルは夕方(台本: Good evening)・出発は翌朝) */   /* ローマ(094。物語の時刻で、実在の便・電車の時刻ではない。ホテルは夕方(台本: Buonasera)・出発は翌朝) */   /* アテネ(090・091。物語の時刻で、実在の便の時刻ではない。ホテルは夕方(台本: Good evening)・出発は翌朝) */
 //                  /* ロヴァニエミの出発(072。台本: Good afternoon) */      /* ロヴァニエミ到着(065。物語の時刻で、実在の便の時刻ではない。夜の便・深夜の到着=021 の R1〜R4) */ /* ドーハ出発(台本: Good afternoon) */
 /* 券ごとの上書き: スターのナイロビ着は 01:25(夜)。台本のあいさつは朝のまま(夜版の台本は未作成) */
 var HOUR_TK={star:{immig:1,bag:2,sim:2,taxi:3}};
 function hourAt(tk,id){if(!id)return null;var o=HOUR_TK[tk];if(o&&has(o,id))return o[id];return has(HOUR,id)?HOUR[id]:null}
 function realHour(tz){try{return +new Intl.DateTimeFormat('en-GB',{timeZone:tz,hour:'2-digit',hourCycle:'h23'}).format(new Date())}catch(e){return -1}}
 /* 場面の絵・音が使う「いまの現地の時(0〜23)」。旅の中で、その日を遊んでいて、場所の時刻が決まっているときだけ旅の時刻。それ以外は tz の本当の時計 */
 function hourNow(tz){
  try{var s=S();if(s.tk&&exists()&&s.ph==='day'){var h=hourAt(s.tk,hooks.at&&hooks.at());if(h!=null)return h}}catch(e){}
  return realHour(tz)}
 /* ---------- 記録の読み書き ---------- */
 var st=null,PAGE='',hooks={};
 function readTour(){try{var t=JSON.parse(localStorage.getItem(TKEY)||'null');return t&&typeof t==='object'?t:{}}catch(e){return {}}}
 function seen(v){var t=readTour();return !!(t.seen&&t.seen[v]>0)}
 function blank(){return {v:1,trip:1,tk:null,day:0,td:1,ph:'morning',legs:[],days:[],cur:{led:[],pick:[]},bun:0}}
 function clean(r){
  var s=blank();if(!r||typeof r!=='object')return s;
  if(r.tk==='ow'||r.tk==='star')s.tk=r.tk;
  ['day','td'].forEach(function(k){if(typeof r[k]==='number'&&r[k]>=0&&r[k]<=40)s[k]=Math.floor(r[k])});
  if(r.ph==='morning'||r.ph==='day'||r.ph==='night'||r.ph==='wait')s.ph=r.ph;
  if(r.bun)s.bun=1;
  if(Array.isArray(r.legs))s.legs=r.legs.filter(function(l){return l&&typeof l.i==='number'}).slice(0,16).map(function(l){return {i:l.i,fr:String(l.fr||''),to:String(l.to||''),d:typeof l.d==='number'?l.d:null,f:l.f?1:0,l:l.l?1:0,dt:/^\d{4}-\d\d-\d\d$/.test(l.dt||'')?l.dt:''}});
  if(Array.isArray(r.days))s.days=r.days.filter(function(d){return d&&typeof d.d==='number'}).slice(0,32).map(function(d){
   var p=d.ph&&typeof d.ph==='object'?d.ph:{};
   return {d:d.d,td:typeof d.td==='number'?d.td:d.d,ph:{s:String(p.s||'night').slice(0,20),k:String(p.k||'night').slice(0,10),f:p.f?1:0},
    led:Array.isArray(d.led)?d.led.filter(function(x){return Array.isArray(x)&&x.length===3&&typeof x[1]==='number'}).slice(0,24):[],
    pick:Array.isArray(d.pick)?d.pick.filter(function(x){return typeof x==='string'}).slice(0,12):[],sp:d.sp?1:0}});
  if(r.cur&&typeof r.cur==='object'){s.cur={led:Array.isArray(r.cur.led)?r.cur.led.filter(function(x){return Array.isArray(x)&&x.length===3}).slice(0,24):[],
   pick:Array.isArray(r.cur.pick)?r.cur.pick.filter(function(x){return typeof x==='string'}).slice(0,12):[]};
   if(r.cur.sp)s.cur.sp=1;
   if(typeof r.cur.bg==='string')s.cur.bg=r.cur.bg.slice(0,20);if(typeof r.cur.ev==='string')s.cur.ev=r.cur.ev.slice(0,20);if(r.cur.n>0)s.cur.n=Math.min(99,r.cur.n|0)}
  return s}
 function load(){try{st=clean(JSON.parse(localStorage.getItem(KEY)||'null'))}catch(e){st=blank()}return st}
 function save(){try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
 function S(){return st||load()}
 function exists(){try{return localStorage.getItem(KEY)!==null}catch(e){return false}}
 function reset(){st=null;try{localStorage.removeItem(KEY)}catch(e){}}
 /* ---------- 表の読み取り ---------- */
 function rows(){var t=S().tk||'ow';return ROWS[t]}
 /* 条件つきのまとまり(059): 保存の keep.hnd1(1日目に拾った落とし物)があるセーブだけ、28日目に hnd_ret が載る。ないセーブでは、その日は今までどおり「まだ作っていない日」 */
 var GCOND={hnd_ret:function(){var t=readTour();return !!(t.keep&&t.keep.hnd1)}};
 function rg(r){var o=[],i;for(i=0;i<r[5].length;i++){var c=GCOND[r[5][i]];if(!c||c())o.push(r[5][i])}return o}
 function rowOf(td){var r=rows();return r[td-1]||null}
 function groupsOf(td){var r=rowOf(td);return r?rg(r):[]}
 function groupTd(g){var r=rows(),i;for(i=0;i<r.length;i++)if(rg(r[i]).indexOf(g)>=0)return r[i][0];return 0}
 function maxTd(){var r=rows(),m=0,i;for(i=0;i<r.length;i++)if(rg(r[i]).length)m=r[i][0];return m}
 function groupDone(g){var G=GROUPS[g],i;if(!G)return false;for(i=0;i<G.length;i++){var ok=false,j;for(j=0;j<G[i].length;j++)if(seen(G[i][j]))ok=true;if(!ok)return false}return true}
 function dayDone(td){if(isSparta(td)){var s0=S();return td===s0.td&&!!(s0.cur&&s0.cur.sp)}var gs=groupsOf(td),i;if(!gs.length)return false;for(i=0;i<gs.length;i++)if(!groupDone(gs[i]))return false;return true}
 function isRest(td){var r=rowOf(td);return !!r&&r[2]==='rest'}
 /* その日は 作ってある日か: 場面があるか、場面のある日のあいだにはさまる休養日 */
 function reachable(td){var r=rowOf(td);if(!r||td>=29)return false;if(rg(r).length||isSparta(td))return true;return r[2]==='rest'&&td<maxTd()}
 function nextTd(td){var n,m=maxTd();for(n=td+1;n<=m;n++)if(reachable(n))return n;return 0}
 /* ---------- 券の束 ---------- */
 function today(){var d=new Date(),z=function(n){return (n<10?'0':'')+n};return d.getFullYear()+'-'+z(d.getMonth()+1)+'-'+z(d.getDate())}
 var MON=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];
 function dtText(iso){var m=/^(\d{4})-(\d\d)-(\d\d)$/.exec(iso||'');return m?(+m[3])+' '+MON[+m[2]-1]+' '+m[1]:''}
 function mkLegs(tk){return LEGS[tk].map(function(l,i){return {i:i,fr:l[0],to:l[1],d:null,f:0,l:0}})}
 function legInfo(i){var s=S(),l=LEGS[s.tk||'ow'][i];return l?{fr:l[0],to:l[1],al:l[2],td:l[3],sep:!!l[4]}:null}
 function here(){var s=S(),i,c='HND';for(i=0;i<s.legs.length;i++)if(s.legs[i].l)c=s.legs[i].to;return c}
 function landed(){var s=S(),n=0,i;for(i=0;i<s.legs.length;i++)if(s.legs[i].l)n++;return n}
 function total(){var s=S();return s.legs.length||13}
 function firstOpen(){var s=S(),i;for(i=0;i<s.legs.length;i++)if(!s.legs[i].l)return i;return -1}
 /* 行き先(3文字コード)へ、いまの場所から飛べる区間のつながり(乗り継ぎだけの区間をはさんでもよい)。飛べないときは null */
 function chain(code){
  var s=S(),i=firstOpen(),out=[],j;if(i<0||!s.tk)return null;
  if(s.legs[i].fr!==here())return null;
  if(i===0&&departPending())return null;   /* 1日目の羽田(タスク043): 出発の場面(チェックイン〜機内)を遊び終えるまでは、世界マップからは飛べない */
  for(j=i;j<s.legs.length;j++){
   out.push(j);if(s.legs[j].to===code)return IMPL[code]?out:null;
   var nx=s.legs[j+1];if(!nx||nx.fr!==s.legs[j].to)return null;
   var a=legInfo(j),b=legInfo(j+1);if(!a||!b||b.td-a.td>1||a.sep||b.sep)return null}
  return null}
 /* 1日目の羽田の出発がまだか(券を買った・まだ羽田・出発の場面が終わっていない)。世界マップの「くうこうに もどる」(羽田)と、飛べるかの判定が使う */
 /* 28日目の羽田の日を遊んでいる最中か(059)。「羽田」タブと、世界マップの「くうこうに もどる」が使う */
 function retToday(){var s=S();return !!s.tk&&exists()&&s.ph==='day'&&groupsOf(s.td).indexOf('hnd_ret')>=0&&here()==='HND'}
 function departPending(){var s=S();return !!s.tk&&here()==='HND'&&!groupDone('hnd_dep')}
 function canFly(apId){var c=codeOf(apId);if(!c)return false;return !!chain(c)}
 function nextLegTo(){var i=firstOpen();return i<0?null:S().legs[i].to}
 function fillD(){var s=S(),i;for(i=0;i<s.legs.length;i++){var l=s.legs[i];if(l.f&&l.d==null){var td=legInfo(i).td,k;for(k=0;k<s.days.length;k++)if(s.days[k].td===td){l.d=s.days[k].d;break}if(l.d==null&&s.day>0)l.d=s.day}}}
 /* 飛ぶ: 区間のつながりを「ちぎれた・着いた」にする。返す値: {tear:[まだちぎれていなかった区間], all:[区間]} */
 function fly(apId){
  var c=codeOf(apId),ch=c&&chain(c);if(!ch)return null;
  var s=S(),tear=[];
  ch.forEach(function(j){var l=s.legs[j];if(!l.f){l.f=1;l.dt=today();tear.push(j);var li=legInfo(j);if(li&&li.sep)ledgerAdd(SEPTICKET)}l.l=1});
  fillD();save();return {tear:tear,all:ch}}
 /* お金の1行を、いまの日(朝〜その日を遊んでいる間)の記録帳に載せる。夜・朝のあいだなら、直前の日の記録に足す。日がまだなければ載せない */
 function ledgerAdd(e){var s=S();if(s.ph==='day'){s.cur.led.push(e.slice(0,3));return true}
  if(s.days.length){var d=s.days[s.days.length-1];if(d.led.length<24){d.led.push(e.slice(0,3));return true}}return false}
 function addFee(amount,cur){if(!(amount>0))return false;var ok=ledgerAdd(['fee',amount,cur||'JPY']);save();return ok}
 function tearNow(i){var s=S(),l=s.legs[i];if(!l||l.f)return false;l.f=1;l.dt=today();var li=legInfo(i);if(li&&li.sep)ledgerAdd(SEPTICKET);fillD();save();return true}
 function setTicket(tk,price){
  var s=S();if(tk!=='ow'&&tk!=='star')return;
  if(s.tk!==tk){s.tk=tk;s.legs=mkLegs(tk)}
  save()}
 /* ---------- お金・写真 ---------- */
 function yen(e){return Math.round(e[1]*(RATE[e[2]]||1))}
 function money(e){return (LBL[e[0]]||e[0])+' · '+e[1].toLocaleString('en-US')+' '+e[2]}
 function big(led){var b=null;(led||[]).forEach(function(e){if(!b||yen(e)>yen(b))b=e});return b}
 function dayRec(d){var s=S(),k;for(k=0;k<s.days.length;k++)if(s.days[k].d===d)return s.days[k];return null}
 function note(S0){   /* 場面が終わるたび: お金の1行・選んだもの・写真の元(その日で最後に遊んだ場面の絵) */
  var s=S();if(!S0||s.ph!=='day')return;
  var vid=S0.vid,d=S0.d||{},first=seen(vid);
  s.cur.n=(s.cur.n||0)+1;
  if(!d.win&&d.bg)s.cur.bg=d.bg;
  if(d.ev&&d.bg)s.cur.ev=d.bg;
  if(vid==='ticket_ow'||vid==='ticket_star'){
   var W=readTour().win||{},p=vid==='ticket_star'?TICKETPRICE.star:(W.cont===4?TICKETPRICE.ow4:TICKETPRICE.ow5);
   s.cur.led.push(['ticket',p,'JPY'])}
  else if(has(MONEY,vid)&&!(s.cur.seenv&&s.cur.seenv[vid])){s.cur.led.push(MONEY[vid].slice())}
  if(has(PICK,vid))s.cur.pick.push(PICK[vid]);
  if(!s.cur.seenv)s.cur.seenv={};s.cur.seenv[vid]=1;
  save()}
 function pickPhoto(td){
  var s=S(),r=rowOf(td),c=s.cur||{};
  if(r&&r[2]==='rest')return rawPhoto();
  if(c.ev)return {s:c.ev,k:'ev',f:0};
  if(c.bg)return {s:c.bg,k:(r&&r[3])?'peak':'day',f:0};
  return rawPhoto()}
 /* 何もなかった日・休養日の写真(020-9): 素の瞬間を、いままでの何もない日の数だけ順に(変顔→寝顔→おやつ→昼寝)。毎回おなじ並びで、読み込み直しても変わらない */
 function rawPhoto(){
  var s=S(),n=0,i;for(i=0;i<s.days.length;i++){var p=s.days[i].ph;if(p&&(p.s==='raw'||p.k==='nap'))n++}
  var k=RAWORDER[n%RAWORDER.length];return k==='nap'?{s:'nap',k:'nap',f:0}:{s:'raw',k:k,f:0}}
 /* ---------- 日の進み ---------- */
 function migrate(){   /* 旅の記録(kanpe-trip-v1)がなく、券だけある古い記録: あそんだぶんの日を作る */
  var t=readTour(),s=blank();if(t.ticket!=='ow'&&t.ticket!=='star')return s;
  s.tk=t.ticket;s.legs=mkLegs(s.tk);st=s;
  var td=1,guard=0;
  while(td&&guard++<40){
   if(!reachable(td)){td=nextTd(td);continue}
   if(!dayDone(td)&&!isRest(td))break;
   if(isRest(td)){var nx=nextTd(td);if(!nx||!dayDone(nx)&&!(isRest(nx)))break}
   s.day++;s.days.push({d:s.day,td:td,ph:{s:isRest(td)?'nap':'night',k:isRest(td)?'nap':'night',f:0},led:[],pick:[]});
   var rr=rowOf(td);
   for(var i=0;i<s.legs.length;i++){var li=legInfo(i);if(li.td<=td&&IMPL[li.to]&&s.legs[i].l===0&&(li.td<td||!rg(rr).length||true)){}}
   td=nextTd(td)}
  s.td=td||s.td;s.ph='morning';
  /* 飛んだ区間: 世界マップの記録で、いる空港と クリアから決める */
  try{var w=JSON.parse(localStorage.getItem('kanpe-world-v1')||'null'),at=w&&w.at,code=at&&codeOf(at);
   if(code&&code!=='HND'){var ch=null,tmp=st;for(var j=0;j<s.legs.length;j++){s.legs[j].f=s.legs[j].l=1;if(s.legs[j].to===code&&IMPL[code]&&legInfo(j).td>=1&&(j===1||j===2))break}}}catch(e){}
  fillD();return s}
 function sync(){
  if(st)return st;
  if(exists()){load();return st}
  var t=readTour();
  if(t.ticket==='ow'||t.ticket==='star'){st=migrate();save();return st}
  st=blank();return st}
 function begin(){sync();return st}
 function openable(td){var r=rowOf(td);return !!r&&reachable(td)&&r[1]===here()}
 /* 朝の1枚の中身(次に開く日)。開く日がなければ null */
 function morningInfo(){
  var s=sync();if(s.ph==='wait'&&reachable(s.td)){s.ph='morning';save()}
  if(s.ph!=='morning')return null;
  var td=s.td;if(!rowOf(td)||!reachable(td)){var n=nextTd(td-1);if(!n)return null;td=n}
  if(!openable(td)&&!(td===1&&s.day===0))return null;
  var r=rowOf(td);return {td:td,day:s.day+1,en:'Day '+(s.day+1)+'. '+r[4],rest:r[2]==='rest',note:r[2]==='rest'&&has(NOTICES,s.tk+td)?NOTICES[s.tk+td]:'',sparta:isSparta(td),fly:legsOnDay(td)}}
 function legsOnDay(td){var s=S(),o=[],i;for(i=0;i<s.legs.length;i++)if(legInfo(i).td===td&&!s.legs[i].l)o.push(i);return o}
 function openMorning(){var m=morningInfo();if(!m)return null;var s=S();s.day=m.day;s.td=m.td;s.ph='day';s.cur={led:[],pick:[]};fillD();save();syncUI();try{var tm=todayMode();if(tm&&hooks.mode)hooks.mode(tm)}catch(e){}return m}
 function nightInfo(){
  var s=S();if(s.ph!=='night'&&!(s.ph==='day'&&(dayDone(s.td)||isRest(s.td))))return null;
  if(s.ph==='day'){s.ph='night';s.nph=pickPhoto(s.td);save();syncUI()}
  var ph=s.nph||pickPhoto(s.td),b=big(s.cur&&s.cur.led);
  return {day:s.day,td:s.td,photo:ph,line:b?money(b):'',rest:isRest(s.td)}}
 function closeNight(){
  var s=S();if(s.ph!=='night')return;
  var ph=s.nph||pickPhoto(s.td);
  s.days.push({d:s.day,td:s.td,ph:ph,led:(s.cur&&s.cur.led)||[],pick:(s.cur&&s.cur.pick)||[],sp:(s.cur&&s.cur.sp)?1:0});
  s.cur={led:[],pick:[]};delete s.nph;
  fillD();
  var n=nextTd(s.td);
  if(n){s.td=n;s.ph='morning'}else{s.td=s.td+1;s.ph='wait'}
  save();syncUI()}
 /* 休養日(朝の1枚を開いてから夜の1枚を閉じるまで)か。この間は 単語バトル・合宿の入口を出さず、場所は全部閉じる。飽きたサインも数えない(020-7) */
 function restToday(){var s=S();return !!s.tk&&exists()&&(s.ph==='day'||s.ph==='night')&&isRest(s.td)}
 /* スパルタ時間(強化合宿)を終えた: その日を終わりにして、夜の1枚へ。スパルタの日でないとき・もう終えたときは何もしない */
 function spartaDone(cb){
  var s=S();if(!s.tk||s.ph!=='day'||!isSparta(s.td)||(s.cur&&s.cur.sp)){if(cb)cb();return false}
  s.cur.sp=1;save();night(cb);return true}
 function lockedGroup(g){
  var s=S();if(!s.tk)return false;
  if(restToday())return true;
  var td=groupTd(g);if(!td)return true;
  return td>s.td||(td===s.td&&s.ph==='morning')}
 function lockedPlace(id){var g=PLACEGRP[id];return g?lockedGroup(g):false}
 /* タブの鍵: タブに場面のまとまりが1つ(文字列)でも、いくつか(配列。058「滞在」タブは市場とサファリ)でも。配列のときは、全部がまだ開かない間だけ閉じる */
 function modeGroups(mode){var m=MODEGRP[mode],g=m&&m[PAGE];return g?(typeof g==='string'?[g]:g):[]}
 function lockedMode(mode){var s=S();if(!s.tk)return false;var gs=modeGroups(mode),i;if(!gs.length)return false;for(i=0;i<gs.length;i++)if(!lockedGroup(gs[i]))return false;return true}
 function modeHidden(mode){var s=S();if(!s.tk)return false;var gs=modeGroups(mode),i;if(!gs.length)return false;for(i=0;i<gs.length;i++)if(groupTd(gs[i]))return false;return true}
 /* 朝の1枚を開いた日に、その日のまとまりがあるタブへ移る(058)。ページが hooks.mode を持つときだけ。見つからなければ何もしない */
 function todayMode(){var s=S(),gs=groupsOf(s.td),k,i;if(!gs.length)return null;for(k in MODEGRP)for(i=0;i<gs.length;i++)if(modeGroups(k).indexOf(gs[i])>=0)return k;return null}

 /* ====================== 画面(ほかの画面の上に重ねる1枚) ====================== */
 var CSS='.trip-ov{position:fixed;inset:0;z-index:2000;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;padding:24px;box-sizing:border-box;background:#0d1226;color:#f4f1e8;font-family:"M PLUS Rounded 1c","Hiragino Maru Gothic ProN",system-ui,sans-serif;text-align:center;cursor:pointer;overflow:auto}'
 +'.trip-ov>*{flex:none}.trip-ov{justify-content:safe center}.trip-ov.mor{background:#1b2a55}.trip-ov.mor .trip-sun{width:46px;height:46px;background:#ffc72c;box-shadow:0 0 0 4px #2a1a10;margin-bottom:6px}'
 +'.trip-day{font-size:clamp(54px,18vw,92px);font-weight:800;letter-spacing:.05em;color:#ffc72c;text-shadow:4px 4px 0 #2a1a10;line-height:1}'
 +'.trip-sub{font-size:clamp(17px,5.2vw,23px);font-weight:800;max-width:20em;line-height:1.4}'
 +'.trip-say{font-size:clamp(14px,4.2vw,18px);color:#cfd6ee;max-width:22em;line-height:1.5}'
 +'.trip-hint{font-size:12px;color:#9aa6c4;animation:tripbl 1.2s steps(2) infinite}@keyframes tripbl{50%{opacity:.25}}'
 +'.trip-photo{display:block;width:min(86vw,360px);aspect-ratio:320/150;image-rendering:pixelated;border:6px solid #fffdf4;box-shadow:0 0 0 3px #2a1a10;background:#222;opacity:0;filter:brightness(.35)}'
 +'.trip-photo.on{opacity:1;filter:none;transition:opacity 3.4s steps(8),filter 3.4s steps(8)}'
 +'.trip-line{font-size:clamp(15px,4.4vw,19px);font-weight:800;color:#ffd36a;min-height:1.4em}'
 +'.tp{position:relative;box-sizing:border-box;width:min(86vw,330px);padding:10px 14px 8px;border:3px solid #2a1a10;border-radius:6px;background:#fff6d8;color:#10131f;text-align:left;box-shadow:0 4px 0 #2a1a10}'
 +'.tp.tp-ow{border-top:14px solid #143fb0}.tp.tp-star{border-top:14px solid #c8182a}.tp.tp-sep{border-top:14px solid #2d8f8a;background:#eaf6f1}'
 +'.tp .al{font-size:11px;font-weight:800;letter-spacing:.08em;color:#27325a;min-height:1.3em}'
 +'.tp .rt{display:flex;align-items:center;gap:10px;font-size:34px;font-weight:800;line-height:1.1;font-family:"Noto Sans","Segoe UI",system-ui,sans-serif}.tp .rt i{font-style:normal;font-size:22px;color:#27325a}'
 +'.tp .cy{font-size:12px;color:#5a5a66;margin-top:2px}.tp .nn{position:absolute;right:12px;top:8px;font-size:12px;font-weight:800;color:#27325a}'
 +'.tp .cut{margin:8px -14px 0;border-top:3px dotted #9a947f}.tp .stub{font-size:11px;color:#5a5a66;padding-top:5px;min-height:1.3em}'
 +'.tp.tp-torn{opacity:.9}.tp.tp-gone{opacity:.45}'
 +'.trip-stack{position:relative;width:min(86vw,330px);height:auto}.trip-stack .tp{margin-top:-6px}'
 +'.trip-list{width:min(92vw,380px);display:flex;flex-direction:column;gap:8px;margin:4px 0}'
 +'.trip-row{display:flex;gap:8px;align-items:center;background:#1c2447;border:2px solid #5b6690;border-radius:6px;padding:6px 8px;text-align:left}'
 +'.trip-row canvas{width:96px;aspect-ratio:320/150;image-rendering:pixelated;border:2px solid #fffdf4;background:#222;flex:none}.trip-row b{font-size:13px;color:#ffc72c}.trip-row span{display:block;font-size:12px;color:#cfd6ee}'
 +'.trip-note{width:min(86vw,330px);box-sizing:border-box;padding:8px 12px;border:3px solid #2a1a10;border-radius:6px;background:#fff6d8;color:#10131f;text-align:left;font-size:14px;line-height:1.45;box-shadow:0 4px 0 #2a1a10}.trip-note b{display:block;font-size:11px;letter-spacing:.12em;color:#8a1538;margin-bottom:2px}'
 +'.trip-btn{font:inherit;font-weight:800;font-size:15px;color:#10131f;background:#ffc72c;border:3px solid #2a1a10;border-radius:10px;padding:10px 22px;cursor:pointer;box-shadow:0 4px 0 #2a1a10}'
 +'.trip-torn{position:relative;width:min(86vw,330px);height:150px}.trip-torn .tp{position:absolute;left:0;right:0;top:0;margin:0}'
 +'.trip-torn .tp.tp-top{clip-path:inset(0 0 52px 0)}.trip-torn .tp.tp-bot{clip-path:inset(98px 0 0 0)}'
 +'.trip-torn .tp.tp-bot.tp-fall{animation:tripfall 1.1s ease-in forwards}@keyframes tripfall{0%{transform:translate(0,0) rotate(0)}30%{transform:translate(4px,8px) rotate(3deg)}100%{transform:translate(30px,170px) rotate(18deg);opacity:0}}'
 +'.trip-torn .tp.tp-top.tp-shake{animation:tripshake .3s 1}@keyframes tripshake{25%{transform:translateX(-4px)}75%{transform:translateX(4px)}}';
 function css(){if(document.getElementById('tripcss'))return;var s=document.createElement('style');s.id='tripcss';s.textContent=CSS;document.head.appendChild(s)}
 function E(tag,cls,text){var e=document.createElement(tag);if(cls)e.className=cls;if(text!=null)e.textContent=text;return e}
 function overlay(cls,onTap){
  css();var o=E('div','trip-ov '+(cls||''));o.setAttribute('role','dialog');o.tabIndex=-1;document.body.appendChild(o);
  var done=false;
  o.close=function(){if(done)return;done=true;try{o.remove()}catch(e){}document.removeEventListener('keydown',kd,true)};
  function go(){if(done)return;if(o.busy)return;if(onTap)onTap(o)}
  function kd(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();go()}}
  o.addEventListener('click',go);document.addEventListener('keydown',kd,true);
  try{o.focus({preventScroll:true})}catch(e){}
  return o}
 function say(text){try{if(hooks.say)hooks.say(text)}catch(e){}}
 function syncUI(){try{if(hooks.ui)hooks.ui()}catch(e){}}   /* 休養日の入口(合宿ボタン)の出し入れを、ページに知らせる */
 function fx(n){try{if(hooks.fx)hooks.fx(n)}catch(e){}}
 /* ---- 搭乗券 ---- */
 function passEl(i,cls){
  var l=legInfo(i),s=S(),a=AIRP[l.fr],b=AIRP[l.to],d=E('div','tp tp-'+(l.sep?'sep':(s.tk||'ow'))+(cls?' tp-'+cls:''));
  d.appendChild(E('div','al',l.sep?'SEPARATE TICKET':l.al.toUpperCase()));
  d.appendChild(E('div','nn','FLIGHT '+(i+1)+' / '+total()));
  var rt=E('div','rt');rt.appendChild(E('b','',l.fr));rt.appendChild(E('i','','→'));rt.appendChild(E('b','',l.to));d.appendChild(rt);
  d.appendChild(E('div','cy',a.en+' → '+b.en));var lg0=s.legs[i];d.appendChild(E('div','cy',dtText((lg0&&lg0.dt)||today())));d.appendChild(E('div','cut'));
  var lg=s.legs[i],stub=E('div','stub');
  if(lg&&lg.f){stub.textContent=lg.d?('DAY '+lg.d):'';}else stub.textContent='';
  d.appendChild(stub);return d}
 /* ---- 写真(1日1枚) ---- */
 var TH=['...hhhhhh...','..hhhhhhhh..','..hssssssh..','..hsessesh..','..hssssssh..','...ssssss...','..bbbbbbbb..','.sbbbaabbbs.','.sbbbaabbbs.','..bbbbbbbb..','..dd....dd..','..dd....dd..'];
 var TB=['.tt....tt.','tttttttttt','ttettttett','tpttttttpt','tttttttttt','aaaaaaaaaa','.tttttttt.','.ff....ff.'];
 var TPH={h:'#2b2b2b',s:'#f2c9a0',e:'#1c2230',b:'#2f5bea',a:'#f2b705',d:'#333a4d'},TPB={t:'#5fd6c3',e:'#10131f',p:'#ff9aa8',a:'#ffc72c',f:'#2f8f82'};
 function spr(g,map,pal,x,y,px){for(var r=0;r<map.length;r++){var row=map[r];for(var k=0;k<row.length;k++){var ch=row.charAt(k);if(ch!=='.'){g.fillStyle=pal[ch]||'#f0f';g.fillRect(Math.round(x+k*px),Math.round(y+r*px),px,px)}}}}
 function rect(g,col,x,y,w,h){g.fillStyle=col;g.fillRect(x,y,w,h)}
 /* ---------- 何もない日の写真(タスク032 / 020-9): 素の瞬間の絵(2人の変顔・寝顔・おやつ) ----------
    場面がなかった日(休養日など)の記録・アルバムに付く。いまのゲームの絵の流儀(キングとルルのドット・グラデーションなし・赤と緑を並べない)で、
    320x150 の小さな絵として描く。あとで差し替えできる: RAW[名前] は g(2Dコンテキスト, 320x150)に描く関数。
    TRIP.setRaw(名前, 関数) で関数を差し替える。TRIP.setRawImage(名前, 画像のURL) なら 320x150 の画像に差し替える(読み込めるまではドット絵)。 */
 var RAWORDER=['face','sleep','snack','nap'];
 var KFACE=['...hhhhhh...','..hhhhhhhh..','..hssssssh..','..hsseessh..','..hsmmmmsh..','...sspps...','..bbbbbbbb..','.sbbbaabbbs.'];
 var LFACE=['.tt....tt.','tttttttttt','tttteetttt','ppttttttpp','ttttmmtttt','aaaaaaaaaa','.tttttttt.','.ff....ff.'];
 var KSLEEP=['...hhhhhh...','..hhhhhhhh..','..hssssssh..','..heesseeh..','..hssssssh..','...ssssss...'];
 var LSLEEP=['.tt....tt.','tttttttttt','teetttteet','tpttttttpt','tttttttttt'];
 var HEROMINI=['...hhhhhh...','..hhhhhhhh..','..hssssssh..','..hsessesh..','..hssssssh..','...ssssss...','..bbbbbbbb..','.sbbbaabbbs.','.sbbbaabbbs.','..bbbbbbbb..'];
 var BUDDYMINI=['.tt....tt.','tttttttttt','ttettttett','tpttttttpt','tttttttttt','aaaaaaaaaa','.tttttttt.','.ff....ff.'];
 var RP={h:'#2b2b2b',s:'#f2c9a0',e:'#1c2230',b:'#2f5bea',a:'#f2b705',d:'#333a4d',m:'#5a2a2a',p:'#ff9aa8',t:'#5fd6c3',f:'#2f8f82'};
 var ZZ=['zzzzz','...z.','..z..','.z...','zzzzz'];
 function plus(g,col,x,y){rect(g,col,x+2,y,2,6);rect(g,col,x,y+2,6,2)}
 function cookie(g,x,y,bite){rect(g,'#c98a3a',x+1,y,4,6);rect(g,'#c98a3a',x,y+1,6,4);rect(g,'#5a3a1a',x+2,y+2,1,1);rect(g,'#5a3a1a',x+4,y+3,1,1);if(bite)rect(g,'#f3e6c8',x+4,y,2,2)}
 var RAW={
  face:function(g){
   rect(g,'#f3e6c8',0,0,320,150);rect(g,'#d9b88a',0,118,320,32);rect(g,'#c9a878',0,118,320,2);
   spr(g,KFACE,RP,64,60,6);spr(g,LFACE,RP,194,60,6);
   plus(g,'#f2b705',40,30);plus(g,'#143fb0',150,24);plus(g,'#f2b705',286,34);plus(g,'#143fb0',172,100)},
  sleep:function(g){
   rect(g,'#1f2750',0,0,320,150);rect(g,'#0e1630',226,10,64,50);rect(g,'#d8dde8',226,10,64,2);rect(g,'#d8dde8',226,58,64,2);rect(g,'#d8dde8',256,10,2,50);
   rect(g,'#ffd36a',236,22,12,12);for(var i=0;i<8;i++)rect(g,'#ffe9a8',(i*41+12)%200,(i*23+10)%52,2,2);
   rect(g,'#6a4428',14,96,292,54);rect(g,'#fffdf4',54,70,92,34);rect(g,'#fffdf4',182,70,92,34);
   spr(g,KSLEEP,RP,70,62,5);spr(g,LSLEEP,RP,198,70,5);
   rect(g,'#5f79c0',22,102,276,48);for(var y=108;y<150;y+=10)rect(g,'#4a62a8',22,y,276,2);
   spr(g,ZZ,{z:'#ffd36a'},150,30,3);spr(g,ZZ,{z:'#ffd36a'},180,14,2)},
  snack:function(g){
   rect(g,'#f3e6c8',0,0,320,150);rect(g,'#d9b88a',0,100,320,2);
   spr(g,HEROMINI,RP,50,46,5);spr(g,BUDDYMINI,RP,216,56,5);
   rect(g,'#8a6238',0,112,320,4);rect(g,'#b98a58',0,116,320,34);
   rect(g,'#fffdf4',112,108,96,6);cookie(g,124,102,0);cookie(g,142,100,0);cookie(g,160,102,1);cookie(g,178,100,1);
   rect(g,'#c98a3a',60,128,2,2);rect(g,'#c98a3a',230,132,2,2);rect(g,'#5a3a1a',104,124,2,2)}};
 function setRaw(k,fn){if(typeof fn==='function')RAW[k]=fn}
 function setRawImage(k,url){var im=new Image();im.onload=function(){RAW[k]=function(g){g.imageSmoothingEnabled=false;g.drawImage(im,0,0,320,150)}};im.src=url}
 function mini(g,ph){
  if(ph&&ph.s==='raw'&&has(RAW,ph.k)){try{RAW[ph.k](g);return}catch(e){}}   /* 何もない日の写真(素の瞬間) */
  /* 場面の絵が使えないとき(世界マップ)の、小さな ドットの写真。グラデーションなし */
  var th=THEME[ph&&ph.s]||'air',k=ph&&ph.k;
  var P={desk:['#e8e4da','#d9d4c6','#143fb0'],air:['#e8e4da','#d8dce6','#143fb0'],dair:['#efe6d2','#e2d6bc','#8a1538'],lng:['#3a2a4a','#5a4a6a','#c9a03a'],
   street:['#7cc4ee','#5a5a66','#143fb0'],cabin:['#e4dfe2','#6a4a5a','#5c0632'],souq:['#d9b888','#c9a878','#7a5a3a'],hotel:['#e8dcc4','#d8c8a8','#8a6a4a'],
   sea:['#bfe4f2','#e2d6bc','#4aa0c8'],night:['#141a3a','#2a3466','#ffd36a']}[th]||['#e8e4da','#d8dce6','#143fb0'];
  rect(g,P[0],0,0,320,98);rect(g,P[1],0,98,320,52);rect(g,P[2],20,10,90,16);
  if(th==='night'){for(var i=0;i<18;i++)rect(g,'#ffe9a8',(i*53)%310,(i*29)%80,2,2);rect(g,'#ffd36a',250,16,22,22)}
  if(th==='sea'){rect(g,'#4aa0c8',0,58,320,36)}
  if(th==='souq'||th==='hotel'){rect(g,P[2],200,50,70,48)}
  if(k==='nap'){rect(g,'#5a3a2a',90,118,150,16);rect(g,'#f4f2ec',96,112,60,10);spr(g,TB,TPB,170,106,4);return}
  spr(g,TB,TPB,96,147-TB.length*4,4);spr(g,TH,TPH,150,147-TH.length*4,4)}
 function drawPhoto(cv,ph){
  var g=cv.getContext('2d');g.imageSmoothingEnabled=false;cv.width=320;cv.height=150;
  try{
   if(typeof BGS!=='undefined'&&typeof R==='function'&&typeof c!=='undefined'&&ph&&BGS[ph.s]&&ph.k!=='nap'){
    var oc=c;c=g;
    try{g.save();g.fillStyle='#222';g.fillRect(0,0,320,150);BGS[ph.s]({bg:ph.s},{});
     if(typeof sp2==='function'&&typeof HEROMAP!=='undefined'){sp2(BUDDYMAP,BPAL,70,147-BUDDYMAP.length*4,4);sp2(HEROMAP,HPAL,126,147-HEROMAP.length*4,4)}
     g.restore()}finally{c=oc}
    return}}catch(e){}
  mini(g,ph)}
 /* ---- 朝の1枚 ---- */
 function morning(cb){
  var m=openMorning();if(!m){if(cb)cb();return false}
  var o=overlay('mor',function(){o.close();if(m.rest){night(cb);return}if(cb)cb();if(m.sparta)try{if(hooks.sparta)hooks.sparta()}catch(e){}});
  o.appendChild(E('div','trip-sun'));
  o.appendChild(E('div','trip-day','DAY '+m.day));
  var row=rowOf(m.td);o.appendChild(E('div','trip-sub',row[4]));
  if(m.fly.length){var pe=passEl(m.fly[0]);o.appendChild(pe)}
  if(m.note){var nb=E('div','trip-note');nb.appendChild(E('b','','NOTICE'));nb.appendChild(E('span','',m.note));o.appendChild(nb)}
  o.appendChild(E('div','trip-hint','▶'));
  say(m.en);fx('page');return true}
 /* ---- 夜の1枚(今日の写真がゆっくり浮かぶ) ---- */
 function night(cb){
  var n=nightInfo();if(!n){if(cb)cb();return false}
  var o=overlay('',function(){o.close();closeNight();dream(function(){after(cb)})});
  o.appendChild(E('div','trip-sub','DAY '+n.day));
  var cv=E('canvas','trip-photo');cv.width=320;cv.height=150;o.appendChild(cv);drawPhoto(cv,n.photo);
  o.appendChild(E('div','trip-line',n.line));
  o.appendChild(E('div','trip-say','Good night, King.'));
  o.appendChild(E('div','trip-hint','▶'));
  o.busy=true;setTimeout(function(){cv.classList.add('on');fx('develop')},120);setTimeout(function(){o.busy=false},1400);
  say('Good night, King.');return true}
 /* 夢(タスク053): 夜の1枚のあと、持ち越しの語があれば、寝る場面で夢の会話に出す。ページが夢のしくみ(hooks.dream)を持たないとき(世界マップ・終わりの場面)・語がないときは何も起きない */
 function dream(k){var h=hooks.dream,done=false;function go(){if(done)return;done=true;k()}if(!h){go();return}try{h(go)}catch(e){go()}}
 function after(cb){   /* 夜のあと: 次の日を、いる場所で開けるなら続けて朝の1枚 */
  if(morningInfo()){morning(cb)}else if(cb)cb()}
 /* ---- ちぎる ---- */
 function tear(i,cb){
  var o=overlay('',null);o.busy=true;
  var box=E('div','trip-torn');var a=passEl(i,'top'),b=passEl(i,'bot');box.appendChild(a);box.appendChild(b);o.appendChild(box);
  o.appendChild(E('div','trip-say','Have a nice flight.'));
  fx('tear');setTimeout(function(){a.classList.add('tp-shake');b.classList.add('tp-fall')},500);
  setTimeout(function(){o.close();if(cb)cb()},1900)}
 function tearAll(list,cb){var k=0;(function nx(){if(k>=list.length){if(cb)cb();return}tear(list[k++],nx)})()}
 /* ---- 券の束(つづり): 1枚目が表向き、ちぎれた控えは、日・写真・お金の1行つき ---- */
 function bundle(opts,cb){
  var s=sync();if(!s.tk){if(cb)cb();return}
  opts=opts||{};var o=overlay('',function(){o.close();if(cb)cb()});
  if(opts.hand){o.appendChild(E('div','trip-sub','Here is your boarding pass.'));say('Here is your boarding pass.');fx('page')}
  else o.appendChild(E('div','trip-sub','Landed '+landed()+' / '+total()));
  var first=firstOpen(),i;
  if(first>=0){var tp=passEl(first);o.appendChild(tp);
   if(first<s.legs.length-1)o.appendChild(E('div','trip-say',(s.legs.length-first-1)+' more'))}
  var list=E('div','trip-list'),any=false;
  for(i=0;i<s.legs.length;i++){var lg=s.legs[i];if(!lg.f)continue;any=true;
   var li=legInfo(i),r=E('div','trip-row'),cv=E('canvas');cv.width=320;cv.height=150;r.appendChild(cv);
   var d=lg.d?dayRec(lg.d):null,t=E('div');t.appendChild(E('b','',li.fr+' → '+li.to+(lg.d?'  ·  DAY '+lg.d:'')));if(lg.dt)t.appendChild(E('span','',dtText(lg.dt)));
   var bg=d?big(d.led):null;t.appendChild(E('span','',bg?money(bg):''));r.appendChild(t);list.appendChild(r);
   drawPhoto(cv,d?d.ph:{s:'night',k:'night'})}
  if(any)o.appendChild(list);
  o.appendChild(E('div','trip-hint','▶'));return true}
 /* ---------- 場面が終わったあと(ページから呼ぶ) ---------- */
 var GATEVID={nbo_gate1:1,nbo_gate2:1,hnd_board_ow:1,hnd_board_star:1};
 function afterScene(S0,cont){
  var steps=[];
  try{
   sync();var s=S();
   if(S0&&(S0.vid==='ticket_ow'||S0.vid==='ticket_star')&&!s.tk){setTicket(S0.vid==='ticket_star'?'star':'ow')}
   note(S0);
   if(S0&&GATEVID[S0.vid]&&s.tk){var nx=firstOpen();if(nx>=0&&IMPL[s.legs[nx].to]&&s.legs[nx].fr===here()&&!s.legs[nx].f){tearNow(nx);steps.push(function(k){tear(nx,k)})}}
   if(S0&&(S0.vid==='ticket_ow'||S0.vid==='ticket_star')&&s.tk&&!s.bun){s.bun=1;save();steps.push(function(k){bundle({hand:1},k)})}
   steps.push(function(k){if(S().ph==='day'&&(dayDone(S().td)||isRest(S().td)))night(k);else k()})
  }catch(e){}
  (function run(i){if(i>=steps.length){cont();return}try{steps[i](function(){run(i+1)})}catch(e){run(i+1)}})(0)}
 /* ページが開いたとき(または遊びはじめるとき) */
 function enter(cb,page){
  PAGE=page||PAGE;
  try{sync()}catch(e){}
  var s=S();syncUI();
  if(s.ph==='night'){night(cb);return}
  if(s.ph==='day'&&isRest(s.td)){night(cb);return}   /* 休養日は 場面がない。朝の1枚のあと閉じて開き直したら そのまま夜へ */
  if(morningInfo()){morning(cb);return}
  if(cb)cb()}
 /* 記録帳: 数える言葉 */
 function stamps(){var w;try{w=JSON.parse(localStorage.getItem('kanpe-world-v1')||'null')}catch(e){}var n=0;if(w&&w.cleared)Object.keys(w.cleared).forEach(function(k){if(k!=='haneda'&&w.cleared[k])n++});return n}
 function inTrip(){var s=S();return !!s.tk&&exists()}
 /* 30日目の朝: DAY は出さない。"One month later" の1枚だけ */
 function oneMonth(cb){var o=overlay('mor',function(){o.close();if(cb)cb()});o.appendChild(E('div','trip-sub','One month later.'));o.appendChild(E('div','trip-hint','▶'));say('One month later.');return true}
 /* ---------- 精算と、アルバムの1日1ページ ---------- */
 function settle(){
  var s=sync(),tot=0,best=null,bestSum=0,picks={},fee=0,sep=0,sv=null;
  s.days.forEach(function(d){var sum=0;d.led.forEach(function(e){var y=yen(e);tot+=y;if(e[0]!=='ticket')sum+=y;if(e[0]==='fee')fee+=y;if(e[0]==='sep')sep+=y});
   if(sum>bestSum){bestSum=sum;best=d}
   d.pick.forEach(function(p){picks[p]=(picks[p]||0)+1})});
  if(picks.metro&&MONEY.doh_taxi&&MONEY.doh_metro){sv={what:'metro',yen:yen(MONEY.doh_taxi)-yen(MONEY.doh_metro)}}
  return {total:tot,best:best,bestSum:bestSum,picks:picks,fee:fee,sep:sep,save:sv,days:s.days.length}}
 /* 精算(29日目)の読み上げ5項目のうち 4(手数料・別切符)と 5(選んだ重さ)。1〜3 は ending.js(合計・いちばん高い日・いちばん得した選択)。
    手数料・別切符が1円もないときは「なかった」と読む(記録がないのは、使ってないから)。選んだ重さ(タクシーとメトロ)は、選んだ記録があるときだけ読む */
 function settleExtra(R0){
  R0=R0||settle();var out=[],fs=R0.fee,sp=R0.sep;
  if(fs>0&&sp>0)out.push('Fees and separate tickets cost us '+yenText(fs+sp)+'.');
  else if(fs>0)out.push('The fees cost us '+yenText(fs)+'.');
  else if(sp>0)out.push('The separate tickets cost us '+yenText(sp)+'.');
  else out.push('No fees this time. No separate tickets, either.');
  var tx=R0.picks.taxi||0,mt=R0.picks.metro||0;
  if(tx+mt>0)out.push('Taxi '+tx+(tx===1?' time':' times')+', metro '+mt+(mt===1?' time':' times')+'.');
  return out}
 function albumPages(){   /* 2日目から。1ページ目は 出発の日(013 E1)。写真と控えと、お金の1行 */
  var s=sync();return s.days.filter(function(d){return d.d>=2}).map(function(d){
   var b=big(d.led),leg=null,i;for(i=0;i<s.legs.length;i++)if(s.legs[i].d===d.d&&s.legs[i].f){leg=legInfo(i)}
   return {d:d.d,ph:d.ph,line:b?money(b):'',stub:leg?(leg.fr+' → '+leg.to):''}})}
 function yenText(n){return n.toLocaleString('en-US')+' yen'}
 return {KEY:KEY,AIRP:AIRP,IMPL:IMPL,LEGS:LEGS,ROWS:ROWS,GROUPS:GROUPS,PLACEGRP:PLACEGRP,MONEY:MONEY,
  hooks:hooks,setPage:function(p){PAGE=p},load:load,sync:sync,begin:begin,reset:reset,exists:exists,save:save,state:S,
  codeOf:codeOf,canFly:canFly,departPending:departPending,fly:fly,chain:chain,here:here,landed:landed,total:total,legInfo:legInfo,nextLegTo:nextLegTo,tearAll:tearAll,tear:tear,
  setTicket:setTicket,rowOf:rowOf,groupTd:groupTd,groupDone:groupDone,dayDone:dayDone,reachable:reachable,nextTd:nextTd,maxTd:maxTd,
  morning:morning,night:night,bundle:bundle,afterScene:afterScene,enter:enter,morningInfo:morningInfo,nightInfo:nightInfo,
  lockedPlace:lockedPlace,retToday:retToday,lockedMode:lockedMode,modeHidden:modeHidden,stamps:stamps,inTrip:inTrip,drawPhoto:drawPhoto,mini:mini,passEl:passEl,
  restToday:restToday,isSparta:isSparta,spartaDone:spartaDone,spartaRule:spartaRule,SPARTA:SPARTA,setRaw:setRaw,setRawImage:setRawImage,RAW:RAW,RAWORDER:RAWORDER,hourNow:hourNow,hourAt:hourAt,HOUR:HOUR,
  tearNow:tearNow,settle:settle,settleExtra:settleExtra,addFee:addFee,albumPages:albumPages,yen:yen,money:money,yenText:yenText,big:big,dayRec:dayRec,overlay:overlay,E:E,css:css,
  migrate:migrate,pickPhoto:pickPhoto,note:note,oneMonth:oneMonth}
})();

try{window.TRIP=TRIP}catch(e){}
