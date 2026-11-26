/* =====================================================   場面の絵(タスク028): 枠なし・フルブリードの新しい絵の場面
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
 /* ナイロビの英会話カフェ(タスク068・試作): 人なしの背景(1536×960)。チェックモード(?check=1)からだけ入る。先生(キング制作)は中央の丸テーブルの奥席に座る(素材 teacher-sit-front.png の ×0.791・NEAREST。アフロ幅156px=キングのキャップ幅118pxの1.32倍。
    座席の基準 中心 x=800・底辺 y=706)。下半身はテーブルの天板で隠れる(y=648より下は描かない=同梱プレビューと同じ画素)。キング(左・x=672)とルル(右・x=928.5)は手前の席に後ろ姿(hall-*-back を 148×248・129×200 に拡大。足もと y=932。影なし。= 同梱プレビューの画素。※並びはプレビューどおりで、docs/rules.md の「ルルが左・キングが右」とは逆)。
    strips: 湯気(全面・4コマ・ゆっくり。over=カップはテーブルの手前にあるので人物の手前に重ねる)・ペンダントランプ(全面・4コマ・ゆるやかな明滅)・窓の外を通る人の影((996,172)・4コマ・ゆっくり)。背景に焼き込まない別素材 */
 eikai:{bg:'nairobi-eikaiwa-cafe-v1.png',mode:'wide',
  strips:[{img:'nairobi-eikaiwa-cafe-lamps-strip.png',x:0,y:0,n:4,fw:1536,fh:960,step:.7},{img:'nairobi-eikaiwa-cafe-window-strip.png',x:996,y:172,n:4,fw:200,fh:320,step:1.6},
   {img:'nairobi-eikaiwa-cafe-steam-strip.png',x:0,y:0,n:4,fw:1536,fh:960,step:.9,over:1}],
  dep:{lulu:{n:'hall-lulu-back',x:928,by:932,w:129,h:200},king:{n:'hall-king-back',x:672,by:932,w:148,h:248},
   people:[{n:'@teacher-sit-front',x:800,by:706,z:.791,clipY:648,sit:1,spk:1}],bubble:{x:800,y:400},cup:{x:805,by:736}}},
 /* ナイロビのタクシー乗り場(タスク051): 朝の屋外。人なしの背景(1536×960。黄色の公式タクシーが並ぶ到着カーブ)。歩道(y≥775)に立つ。fx は無し(昼の絵なので、夜の星・ガラスのきらめきは出さない)。
    people=縁石の手前の歩道の右はし(係員・ふたりの動線と重ねない)。*/
 nairobi:{bg:'nairobi-taxi-v1.png',mode:'wide',base:926,lulu:300,king:470,suit:575,npc:{x:1060,px:9,slide:1},fx:'',npcS:{taxi_staff:'w-front-man-dashiki',driver:'w-front-man-suit-1'},
  people:[{n:'t-backpacker-front',x:1250,by:890,sw:79},{n:'t-man-thobe-front',x:1450,by:925,sw:79}]},
 /* ナイロビのSIMの店(タスク051): 人なしの背景(JKIA到着ロビー。中央が Safaricom の緑カウンター、左 Telkom・右 airtel)。ふたりはカウンターの手前の床に立つ(足もと y=900)。
    店員は中央のカウンターの向こう(カウンターの高さ y=500 で切る。入国審査・タクシーと同じ npc/npcS の方式)。
    strips=背景の上・人物より奥に重ねる動き(汎用。{img,x,y,n,fw,fh,step}: 左上(x,y)に n コマの横並びの1コマ(fw×fh)を step 秒ごとに切り替える)。回転台=足もと中心(1264,896)、OPEN看板=(704,524)から128×48。
    people=Telkom と airtel の前(背景の床の楕円の位置)。回転台(x 1204..1324)・店員・ふたりと重ねない */
 simshop:{bg:'nairobi-sim-v1.png',mode:'wide',base:900,lulu:700,king:860,suit:965,npc:{x:768,top:372,clip:500},fx:'',npcS:{sim_staff:'w-front-man-suit-1',sim_staff2:'w-front-man-dashiki'},
  strips:[{img:'nairobi-sim-spinner-strip.png',x:1204,y:596,n:4,fw:120,fh:300,step:.5},{img:'nairobi-sim-blink-strip.png',x:704,y:524,n:2,fw:128,fh:48,step:1}],
  people:[{n:'t-safari-front',x:218,by:702,sw:85},{n:'t-woman-hijab-front',x:1430,by:712,sw:79}]},
 /* ナイロビのホテルの部屋(タスク051): 到着の夜、部屋で休む場面(nbo_room)。人なしの背景をフルブリード。ふたりは後ろ姿(足もと y=884)。075で室内基準に拡大: キング148×248(旧 68×114)・ルル129×200(旧 66×102)=カフェ eikai の主人公と同値。素材を NEAREST で拡大して置く(artSwayZ)。ルル x=690・キング x=846(拡大後に重ならず絨毯 x396-1100 の上)。影(sh)は拡大に合わせた幅(ルル57・キング78=旧 29/36 を表示倍率にそろえた)。人は置かない。
    tv=壁のTV画面の矩形(1536×960座標)。今回は何も映さない。将来の映画場面のために名前つきで記録しておく */
 nroom:{bg:'nairobi-hotel-room-v1.png',mode:'wide',hall:{lulu:{n:'hall-lulu-back',x:690,by:884,w:129,h:200,sh:57},king:{n:'hall-king-back',x:846,by:884,w:148,h:248,sh:78}},tv:{x:1120,y:216,w:344,h:176}},
 hotel:{bg:'hotel-front.png',mode:'room',base:895,lulu:250,king:450,suit:560,npc:{x:1290,px:15,top:262,clip:412},fx:'hotel',npcS:{c_front:'o-front-woman-blonde-suit'}},
 /* ドーハのコルニーシュ(タスク070): 朝・人なしの背景(1536×960)。絵に文字は一切なし。対象は bg ccorn の4場面(doh_city_c1/c2/c3・doh_ev_j_ask。結びは doha 側 artIdFor だけ)。
    ふたりは右の端から歩いて入り、ルル x=1060・キング x=1180(足もと y=884)で止まる(dir:-1)。スーツケースは左どなり。相手は左の広い舗道(ベンチの手前)。
    strips=別素材(背景には舟もきらめきも描いていない): ダウ舟(その場で2コマ揺れる。船体は手すり y=516 より上の水面)・水面のきらめき(4コマ)。
    実画が表示される間は、コード描画(BGS.ccorn)の舟・波は出ない(実画が読めないときだけ、そちらに落ちる) */
 dcorn:{bg:'doha-corniche-v1.png',mode:'wide',base:884,dir:-1,lulu:1060,king:1180,suit:960,npc:{x:800,px:9,slide:1},fx:'',
  strips:[{img:'doha-corniche-sparkle-strip.png',x:0,y:372,n:4,fw:1536,fh:192,step:.5},{img:'doha-corniche-dhow-strip.png',x:700,y:258,n:2,fw:512,fh:256,step:.8}]},
 /* 賢者の広間(タスク040): 人なしの背景をフルブリード。賢者は壇上の中央(大人の高さ136px)、ルル(左)とキング(右)は絨毯の上に後ろ姿で寄って立つ(広い場面の大きさ)。
    globe=背景の球の位置(球の外わく 312..473×356..517)に、球だけ8コマ(96px。2倍=192px)を重ね、period秒で1回転。人は足と影を固定し、上半身だけ小さく揺れる(タスク037) */
 sage:{bg:'sage-hall-bg-clean.png',mode:'wide',hall:{sage:{n:'hall-sage',x:768,by:684},lulu:{n:'hall-lulu-back',x:733,by:905},king:{n:'hall-king-back',x:803,by:905},
  globe:{img:'sage-hall-globe-strip.png',x:296,y:340,n:8,fw:96,z:2,period:1.8}}},
 /* チケット売り場=旅行代理店の一室(タスク041): 人なし・航路なしの背景をフルブリード(028)。係員はカウンターの向こうの中央に大人の大きさ(室内の基準273px)で、カウンターの高さで切って下は隠す。
    ルル(左)とキング(右)は絨毯の上に後ろ姿で寄って立つ(室内の基準の大きさ。素材のまま)。中心の間隔136px・体の横幅は131＋136pxで、すき間は約3px。
    route=壁の地図に航路を引く場面(窓口の「線を引く」会話 bg:'rtmap')だけの設定。bgFix=アニメが描けなかったときの静止画(089: 旧ルートの絵は実際のルートと食い違うので、航路なしの絵に落とす)。
    cities=地図の上の都市の位置(1536×960の座標。地図の枠の内側は x340..1200, y92..478)。segs=区間(出発,到着,横ずれ)。横ずれ -860 は、地図の左はしから出て右はしに入る西まわり */
 ticket:{bg:'ticket-office-bg-clean-noroute.png',mode:'room',tk:{bgFix:'ticket-office-bg-clean-noroute.png',
  clerk:{n:'tk-clerk',x:768,top:420,clip:596},clerkS:{n:'tk-clerk-star'},lulu:{n:'tk-lulu-back',x:699,by:920},king:{n:'tk-king-back',x:835,by:920},
  route:{x0:340,x1:1200,D:.8,sp:15,
   /* 089: 1周目の実際のルート(16区間)。都市の位置は壁の地図(絵)の大陸の上に置いた目安。tag=区間番号の札の位置(絵の座標)。ヨーロッパは都市が近いので、札を輪のように外へ出して線でつなぐ */
   cities:{tok:[1080,193],nbo:[784,237],doh:[905,204],rov:[808,136],ath:[826,164],rom:[806,160],zur:[790,152],fra:[798,142],lon:[766,140],lis:[760,162],nyc:[532,166],hon:[392,206],syd:[1062,333],sin:[1000,256],bkk:[968,222],gum:[1128,268]},
   segs:[['tok','nbo',0],['nbo','doh',0],['doh','rov',0],['rov','ath',0],['ath','rom',0],['rom','zur',0],['zur','fra',0],['fra','lon',0],['lon','lis',0],['lis','nyc',0],['nyc','hon',0],['hon','syd',-860],['syd','sin',0],['sin','bkk',0],['bkk','gum',0],['gum','tok',0]],
   tag:{2:[868,250],3:[886,112],4:[846,112],5:[868,160],6:[804,196],7:[796,106],8:[742,108],9:[722,164],10:[650,140]}}}},
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
   ['front-safari',399,947,'walk'],['front-pilot-fa',1119,946,'walk']]},
 /* ドーハの入国審査・出国審査(タスク064): bg が dimmig で vid が doh_ の場面だけ(ナイロビの immig・羽田の同名 bg は対象外)。人なしの背景(1536×960。窓口3つ・表示灯)。
    係官は3窓口とも同一の絵(o-front-officer-blue)を ×0.93(表示 51×127)にして、top=511・clip=600 で頭と肩だけ見せる(頭56px)。話し相手の窓口(lead)は dimmig=中央・dimmig2(別の窓口)=右。
    表示灯の緑ランプは strips で1秒ごとに点滅(2コマ。背景の上・人物より奥)。キングとルルは右から歩いて入り、行列のロープの右に立つ(ルルが左・キングが右)。ロープの中の並ぶ人は後ろ姿 */
 dimmig:{bg:'doha-immigration-v1.png',mode:'wide',base:818,dir:-1,lulu:1052,king:1151,suit:1253,
  strips:[{img:'doha-immigration-lights-strip.png',x:0,y:300,n:2,fw:1536,fh:64,step:1}],
  booths:[{n:'o-front-officer-blue',x:320,top:511,clip:600,s:.93},{n:'o-front-officer-blue',x:768,top:511,clip:600,s:.93,lead:1},{n:'o-front-officer-blue',x:1216,top:511,clip:600,s:.93}],
  glass:{c:'rgba(190,215,226,.22)',r:[[128,380,385,220],[576,380,385,220],[1024,380,385,220]]},
  crowd:[['back-backpacker',300,845],['back-man-thobe',452,845]]},
 dimmig2:{bg:'doha-immigration-v1.png',mode:'wide',base:818,dir:-1,lulu:1052,king:1151,suit:1253,
  strips:[{img:'doha-immigration-lights-strip.png',x:0,y:300,n:2,fw:1536,fh:64,step:1}],
  booths:[{n:'o-front-officer-blue',x:320,top:511,clip:600,s:.93},{n:'o-front-officer-blue',x:768,top:511,clip:600,s:.93},{n:'o-front-officer-blue',x:1216,top:511,clip:600,s:.93,lead:1}],
  glass:{c:'rgba(190,215,226,.22)',r:[[128,380,385,220],[576,380,385,220],[1024,380,385,220]]},
  crowd:[['back-backpacker',300,845],['back-man-thobe',452,845]]},
 /* 羽田の出発ゲート(タスク043): 人なしの背景をフルブリード。券で絵が出し分けられる(oneworld=DOHA・Qatar Airways / Star=ISTANBUL・Turkish Airlines)。
    ルル(左・102px)とキング(右・114px)は広間と同じ後ろ姿で、足もとは y=884。相手の係員は絵には出さず(声だけ)、話すときカウンターの上に「…」を出す(bubble)。
    秘密イベント(ルルの拾い物)は、この場面を遊び終えたとき 保存の keep に入るだけで、絵にも画面にも何も出さない(予告しない) */
 hgate_ow:{bg:'haneda-departure-gate-v2-ow.png',mode:'wide',hall:{lulu:{n:'hall-lulu-back',x:690,by:884},king:{n:'hall-king-back',x:760,by:884},bubble:{x:250,y:552}}},
 hgate_st:{bg:'haneda-departure-gate-v2-star.png',mode:'wide',hall:{lulu:{n:'hall-lulu-back',x:690,by:884},king:{n:'hall-king-back',x:760,by:884},bubble:{x:250,y:552}}},
 /* 羽田のチェックイン・Turkish(タスク055): 人なしの背景(1536×960)。係員(tk-clerk-star)はカウンター3番の前に全身で立つ(足もと y=700)。ベルトの荷物は別素材で、係員の右どなりのベルト(x1132〜1234・面 y=606)の上を横へ動く(背景に焼き込まない)。
    ルル(左)とキング(右)は室内の大きさの後ろ姿(tk-)。足もと y=884。影は同梱プレビューと同じ(shF:1)。oneworld 側(checkinQ)は対象外 */
 hcheckin_st:{bg:'haneda-turkish-checkin-v1.png',mode:'wide',dep:{shF:1,lulu:{n:'tk-lulu-back',x:716,by:884},king:{n:'tk-king-back',x:800,by:884},
  npcS:{tk_checkin:{n:'tk-clerk-star',x:1024,by:700,sw:150}},bubble:{x:1024,y:400},
  fx:[{k:'shuttle',img:'haneda-checkin-belt-bag.png',x0:1132,x1:1234,w:80,h:96,by:606,v:20,wait:2}]}},
 /* 羽田の出発・残り5場面(タスク067)。結びは本編側の artIdFor だけ(ドーハ側ビルドには入れない)。配置の正本=素材パックの配置プレビュー。背景はどれも人なし(1536×960)。
    hcheckin_ow=Qatar側のチェックイン(bg checkinQ・vid が hnd_ のときだけ。ナイロビの checkinQ は ncheckin のまま)。055 のターキッシュ側と対の形(係員は紺スーツ tk-clerk・足もと y=700。ベルトの荷物は別素材)。 */
 hcheckin_ow:{bg:'haneda-checkin-qatar-v1.png',mode:'wide',dep:{shF:1,lulu:{n:'tk-lulu-back',x:716,by:884},king:{n:'tk-king-back',x:800,by:884},
  npcS:{qr_checkin:{n:'tk-clerk',x:1024,by:700,sw:150}},bubble:{x:1024,y:400},
  fx:[{k:'shuttle',img:'haneda-checkin-qatar-belt-bag.png',x0:1132,x1:1234,w:80,h:96,by:606,v:20,wait:2}]}},
 /* 保安検査(bg security・vid が hnd_ のときだけ。ナイロビの nsec とは別の絵)。係員 sec_n1 は右端のゲート(アーチ)の横(o2-front-officer-blue=×2・足もと y=892)。トレイは別素材(strips)をベルトの上に重ねる(底がベルト面 y=636) */
 hsec:{bg:'haneda-security-v1.png',mode:'wide',strips:[{img:'haneda-security-trays-strip.png',x:0,y:504,n:4,fw:1536,fh:144,step:1}],
  dep:{lulu:{n:'hall-lulu-back',x:690,by:884,w:153,h:236,sh:78},king:{n:'hall-king-back',x:774,by:884,w:158,h:264,sh:82},npcS:{sec_n1:{n:'o2-front-officer-blue',x:1330,by:892,sw:130}},bubble:{x:1330,y:560},
   people:[{n:'a-back-backpacker',x:300,by:706},{n:'a-back-dashiki',x:1130,by:706}]}},
 /* 出国審査(bg immigH・vid が hnd_ のときだけ)。窓口は3つ(中心 x=320/768/1216・ガラス帯 y380〜600・カウンター上端 y=600)。係官は中央の窓口の中に頭と肩だけ(top=482・clip=600。入国審査 immig と同じ booths の作法。絵はプレビューから切り出した hexit-officer=幅97。既存の o2-front-officer-blue は110幅で合わない)。
    青いスーツケースも既存の artSuit(四角い箱)ではなく、プレビューの絵(hexit-suitcase。suitImg)。
    ふたりは中央の窓口の前に正面の立ち姿(歩いて入らない: dist を極小にして止まった状態から)。青いスーツケースはキングの右 x=862。表示灯は別素材(strips・1秒ごと) */
 hexit:{bg:'haneda-exit-immigration-v1.png',mode:'wide',base:812,dist:.001,lulu:662,king:760,lh:236,kh:264,suit:862,suitImg:{n:'hexit-suitcase',x:862},people:[{n:'a-back-backpacker',x:320,by:812}],
  strips:[{img:'haneda-exit-lights-strip.png',x:0,y:300,n:2,fw:1536,fh:64,step:1}],
  booths:[{n:'hexit-officer',x:320,top:482,clip:600},{n:'hexit-officer',x:768,top:482,clip:600,lead:1},{n:'hexit-officer',x:1216,top:482,clip:600}]},
 /* 機内の会話場面(bg cabinQ=えんじ色の座席 / cabinT=赤いヘッドレスト・vid が hnd_plane_ のときだけ。048 の cabinseat・機内食 cabinmeal とは別の絵)。
    客室乗務員は ca-front を高さ274にした絵(npc/ca-front-274。頭105px＝この場面のキングの頭100pxの1.05倍)で通路に立つ(中心 x=1000・足もと y=896)。座席の画面と読書灯の明滅は別素材(全面・2社共通) */
 hcabin_ow:{bg:'haneda-cabin-qatar-pax-v1.png',mode:'wide',strips:[{img:'haneda-cabin-lights-strip.png',x:0,y:0,n:2,fw:1536,fh:960,step:1}],
  dep:{lulu:{n:'tk-lulu-back',x:596,by:896,w:172,h:269,sh:73},king:{n:'tk-king-back',x:712,by:896,w:178,h:300,sh:92},npcS:{qr_crew:{n:'ca-front-274',x:1000,by:896,sw:150}},bubble:{x:1000,y:610}}},
 /* ナイロビのカフェ2軒(タスク085-F): bg javaK=Java House / artK=Artcaffe(vid が nbo_java と nbo_art)。1536×960・人なし。
    店員(t-cafe-java 189×300 / t-cafe-art 192×300)はカウンターの向こう: x=768, top=220 から clip=520(カウンター上面)まで描き、腰から下は描かない(npc 方式=dep の clerk)。
    主人公は hall 方式: ルル x=716・キング x=800、ともに by=884(キング w148 h248 / ルル w140 h234。tk-*-back を拡大)。吹き出しは x=768, y=200。
    pay=支払いの演出(061 の payFg)をカウンター(上面 y≈510)の上に出すための原点と倍率(旧画面の座標×k を足した位置) */
 javaK:{bg:'nairobi-cafe-java-v1.png',mode:'wide',dep:{lulu:{n:'tk-lulu-back',x:716,by:884,w:140,h:234},king:{n:'tk-king-back',x:800,by:884,w:148,h:248},
  clerk:{x:768,top:220,clip:520},npcS:{cafe_staff:'t-cafe-java',cafe_staff2:'t-cafe-java'},bubble:{x:768,y:200},pay:{ox:380,oy:324,k:3}}},
 artK:{bg:'nairobi-cafe-art-v1.png',mode:'wide',dep:{lulu:{n:'tk-lulu-back',x:716,by:884,w:140,h:234},king:{n:'tk-king-back',x:800,by:884,w:148,h:248},
  clerk:{x:768,top:220,clip:520},npcS:{cafe_staff3:'t-cafe-art',cafe_staff4:'t-cafe-art'},bubble:{x:768,y:200},pay:{ox:380,oy:324,k:3}}},
 /* ナイロビ便の機内(タスク085-G): bg cabinQ・vid が nbo_ のとき(nbo_plane1/2)。bg は乗客入り haneda-cabin-qatar-pax-v1.png、配置・strips は hcabin_ow と同じ。 */
 cabinQ:{bg:'haneda-cabin-qatar-pax-v1.png',mode:'wide',strips:[{img:'haneda-cabin-lights-strip.png',x:0,y:0,n:2,fw:1536,fh:960,step:1}],
  dep:{lulu:{n:'tk-lulu-back',x:596,by:896,w:172,h:269,sh:73},king:{n:'tk-king-back',x:712,by:896,w:178,h:300,sh:92},npcS:{qr_crew:{n:'ca-front-274',x:1000,by:896,sw:150},qr_crew2:{n:'ca-front-274',x:1000,by:896,sw:150}},bubble:{x:1000,y:610}}},
 hcabin_st:{bg:'haneda-cabin-turkish-pax-v1.png',mode:'wide',strips:[{img:'haneda-cabin-lights-strip.png',x:0,y:0,n:2,fw:1536,fh:960,step:1}],
  dep:{lulu:{n:'tk-lulu-back',x:596,by:896,w:172,h:269,sh:73},king:{n:'tk-king-back',x:712,by:896,w:178,h:300,sh:92},npcS:{tk_crew:{n:'ca-front-274',x:1000,by:896,sw:150}},bubble:{x:1000,y:610}}},
 /* ナイロビの手荷物受け取り(タスク045): 人なしの背景(主ベルトは荷物も中央の島も描かない版)に、荷物6個が楕円の経路を1周 period 秒でまわる。
    ベルトの形(中心 cx,cy・経路の半径 rx,ry)は素材の絵(768×480)の半分の大きさの座標で書く。荷物は 2倍の NEAREST の粒のまま、2画素単位で動く。
    描く順: 奥の半分(sin<0)の荷物 → 中央の島 → 手前の半分の荷物 → ふたり。荷物は奥ほど小さく暗い(絵の段階 lv=13 を sin で引く)。手前では左→右、奥では右→左。
    ルル(左)とキング(右)は広間と同じ後ろ姿で、足もとは y=884(素材の静止画と同じ)。stopFor=この場面ではベルトを止める(雨もりの出来事「ベルトが止まった」) */
 bagclaim:{bg:'nairobi-baggage-base.png',mode:'wide',hall:{lulu:{n:'hall-lulu-back',x:716,by:884},king:{n:'hall-king-back',x:800,by:884},bubble:{x:1210,y:540}},
  belt:{isl:'nairobi-baggage-island.png',ix:552,iy:602,bags:'nairobi-baggage-bags.png',cw:112,ch:104,ax:56,ay:92,lv:13,n:6,cx:400,cy:330,rx:178,ry:28,period:24,stopFor:['nbo_ev_b_leak'],hero:{i:1,vid:'nbo_bag1',also:['nbo_ev_b_leak'],line:2,th:1.1,tpre:10,creep:.25,ease:1.2,hide:4}},
  /* 同じ便の旅行者(タスク047): nbo_bag1 の5往復のあいだ、ベルトの右端の横に立ち続ける(出入り・移動なし)。n=縮めた素材(126px)、x=足もとの中心、by=足もとの高さ、sw=影の幅(配置の正本プレビューから測定)。絵が読めないときは SP.traveler のドット絵で描く */
  trav:{vid:'nbo_bag1',n:'t-backpacker-front',x:1065,by:708,sw:79}},
 /* ナイロビのホテルのロビー・歌手のイベント(タスク049): 人なしの背景(夜のロビー。右はしの肘かけ椅子のあるラウンジの隅)をフルブリード。
    歌手(正面・大人の高さ136px)はラウンジの隅の手前に立ち、歌っているあいだ 音符(♪)がのぼる(notes)。ルル(左)とキング(右)は広間と同じ後ろ姿で、歌手のほうを向いて少し離れて立つ。 */
 /* ホテルの歌場面(タスク060): 歌場面版の背景(nairobi-hotel-lobby-song-v1.png。受付前の赤カーペットの上に低い木の台とマイクスタンド)。通常のロビー(nlobby)は変えず、歌場面(nbo_song)だけがこちらを使う。
    座標は 1536×960。配置の正本=素材パックの配置プレビュー(tour-src/art/ref-song060/)から実測した値。歌手は台の上(中心 x=790・足もと y=734・高さ236)。
    観客5人は後ろ姿を半円に(people。奥=足もとの小さい順に描く。足と影は動かさず上半身だけ小さく揺れる)。ルル(左)とキング(右)は観客の中央(中心 708 / 844.5・足もと 948)。
    ダシキの男性は、プレビューでも手前のバックパッカーとマサイの陰にほぼ隠れる(見えるのは左はしだけ) */
 nsong:{bg:'nairobi-hotel-lobby-song-v1.png',mode:'wide',
  hall:{sage:{n:'hall-singer-stage',x:790,by:734},lulu:{n:'tk-lulu-back',x:708,by:948,rx:60,bx:46},king:{n:'tk-king-back',x:844,by:948,rx:64},notes:1},
  people:[{n:'a-back-safari',x:494,by:872,sw:150},{n:'a-back-thobe',x:584,by:898,sw:140},{n:'a-back-dashiki',x:1000,by:905,sw:138},{n:'a-back-backpacker',x:990,by:888,sw:118},{n:'a-back-maasai',x:1075,by:862,sw:128}]},
 /* ホテルのロビー・通常版(タスク066): 受付のスタッフがホテルを案内する場面(案内の3択=hub)。060の歌場面版(nsong)は使わなくなったが、設定と絵は残す。
    スタッフ(tk-clerk)は受付カウンターの向こうに立つ: 頭と肩〜カウンターの上(clip)まで描き、腰より上だけ小さく揺れる(037)。ルル(左)・キング(右)は足もとを赤いカーペットの手前に。 */
 nlobby:{bg:'nairobi-hotel-lobby-v1.png',mode:'wide',
  hall:{lulu:{n:'tk-lulu-back',x:700,by:934,rx:60,bx:46},king:{n:'tk-king-back',x:840,by:938,rx:64},clerk:{n:'tk-clerk',x:775,top:352,clip:498}}},
 /* プールサイドのショータイム(タスク066): 人なしの背景(nairobi-pool-v2.png)に、歌手・観客5人・ルル・キングを足もとの浅い順(奥→手前)に重ねる(stage)。
    座標は 1536×960 で、素材パックの配置の正本(プレビュー)どおり。歌手は高さ250(344から NEAREST で縮小)・中心 x=790・足もと y=734(台の上面の前端)。足と影は動かさない(037)。
    歌っているあいだは、テーマ曲の拍(beats)ごとに立つ絵・歌う絵(sing1/sing2)を切りかえる。観客5人は高さ250(後ろ姿)・ルル(712,886)・キング(838,890)は等倍。
    strips: 水面のきらめき(ゆっくり)と、窓・電飾・バーの照明(lights。sync='beat' = 曲が鳴っているあいだは曲の再生位置の拍に合わせて切りかえ、鳴っていないときはゆっくり明滅) */
 npool:{bg:'nairobi-pool-v2.png',mode:'wide',
  strips:[{img:'nairobi-pool-sparkle-strip-v2.png',x:56,y:484,n:4,fw:1148,fh:206,step:.9},{img:'nairobi-pool-lights-strip.png',x:0,y:0,n:4,fw:1536,fh:960,step:1.6,sync:'beat'}],
  stage:{spot:1,singer:{f:'s-stand-front',a:'s-stand-sing1',b:'s-stand-sing2',x:790,by:734,notes:1},
   people:[{n:'b-back-maasai',x:1142,by:856,sw:128},{n:'b-back-safari',x:462,by:864,sw:150},{n:'b-back-backpacker',x:1064,by:868,sw:118},{n:'b-back-thobe',x:585,by:900,sw:140},{n:'b-back-dashiki',x:960,by:906,sw:138}],
   lulu:{n:'tk-lulu-back',x:712,by:886,rx:60,bx:46},king:{n:'tk-king-back',x:838,by:890,rx:64}}},
 /* 静かなプール(タスク077): ロビーの案内「The swimming pool」の行き先 nbo_pool1。背景は同じ(nairobi-pool-v2.png・人なし)・既存の2ストリップも同じ(水面のきらめき/照明)。歌手と観客は置かず、ルルとキングだけ。
    ふたりの足もとは npool の stage 配置と同じ(ルル x=712・by=886／キング x=838・by=890、後ろ姿)。曲は鳴らないので、照明ストリップ(sync='beat')はゆっくり明滅のまま。
    既存の npool(ショータイム・歌場面)の定義は変えない(別定義で分ける)。 */
 npoolq:{bg:'nairobi-pool-v2.png',mode:'wide',
  strips:[{img:'nairobi-pool-sparkle-strip-v2.png',x:56,y:484,n:4,fw:1148,fh:206,step:.9},{img:'nairobi-pool-lights-strip.png',x:0,y:0,n:4,fw:1536,fh:960,step:1.6,sync:'beat'}],
  hall:{lulu:{n:'tk-lulu-back',x:712,by:886,rx:60,bx:46},king:{n:'tk-king-back',x:838,by:890,rx:64}}},
 /* バルコニーバル(タスク077・077b確定): 場面 nbo_bar1。背景 nairobi-balcony-bar-v1.png(1536×960・人なし・文字なし)。動くものは背景に描き込まず別ストリップ:
    lights=フェストゥーン・ペンダントの明かりの明滅+窓と星の瞬き(全画面 4コマ・fw1536 fh960・(0,0))／curtain=バーの右の赤いカーテンの揺れ(4コマ・96×490・(1120,88)。背景側には棒だけ)。
    ルル・キングは室内基準の大きさ指定の後ろ姿(ルル129×200・キング148×248。075 の nroom と同じ「素材を拡大して置く」見え方。影なし=同梱プレビューと同じ画素。足もと ルル y=908・キング y=912)。
    バーテンダー(tk-bartender 135×278。PM素材 npc-front-man-suit-2 を表示サイズにした同梱ファイルがそのまま正本)はカウンターの向こう: top=350 から clip=500(カウンター上面)まで描き、腰から下は描かない。上半身だけ小さく揺れる。
    座標はすべて背景の画素から測定済みの確定値(同梱プレビューが配置の正本)。切り替えは song_data.py の BAR_READY の1か所 */
 nbar:{bg:'nairobi-balcony-bar-v1.png',mode:'wide',
  strips:[{img:'nairobi-balcony-bar-lights-strip.png',x:0,y:0,n:4,fw:1536,fh:960,step:1.1},{img:'nairobi-balcony-bar-curtain-strip.png',x:1120,y:88,n:4,fw:96,fh:490,step:1.4}],
  hall:{lulu:{n:'tk-lulu-back',x:712,by:908,w:129,h:200},king:{n:'tk-king-back',x:838,by:912,w:148,h:248}},
  bartender:{n:'tk-bartender',x:784,top:350,clip:500}},
 /* 機内の対面アップ(タスク048): 1日目の最初の長距離便。CAアナウンス・イベントの2場面。背景は人なし(cabin-close-bg)と、食事のあと(cabin-close-meal。ふたりは絵に描かれている)。
    cabinseat=CAが席に来る場面とマイク画面: キング・ルルは座った上半身。既存の室内の絵(room-king-idle / room-lulu-idle)を、食事の絵(cabin-close-meal)より小さめの 約1.82倍(NEAREST。タスク063: キングの頭がCAの1.2倍以内になるよう2.17から下げた)・頭の中心の横位置はそのまま、テーブルの上端に腰が来る高さ(x,y=左上)で重ね、
      テーブルの上端(clip=585)で切る(テーブルは背景の絵)。CAは正面の絵(npc/ca-front・139×266)を同じ倍率で、右の通路側に立たせる(足もと by)。話しているとき「…」を出す。
    cabinmeal=食事の場面: 背景の絵そのまま。ルルが話しているとき、ルルの頭の上に「…」を出す(bubble) */
 cabinseat:{bg:'cabin-close-bg.png',mode:'room',seat:{king:{x:855,y:227,s:1.82},lulu:{x:468,y:263,s:1.83},clip:585,ca:{n:'ca-front',x:1345,by:700,s:2.17}}},
 cabinmeal:{bg:'cabin-close-meal.png',mode:'room',meal:{bubble:{x:672,y:176}}}};

/* ナイロビ出発まわり(タスク054)。ほかの場面と同じく、絵は 1536×960 の座標。mode:'wide' は歩く人物の絵の読み込み用(この場面では歩かない)。
   背景は人なし。ルル(左)とキング(右)は室内の大きさの後ろ姿(tk-)。立つ旅行者は室内の大きさ(t2-=高さ252px)。係員はカウンターの高さで切って下は描かない。
   場面ごとの配置は、背景の画素から測った値(カウンターの上端・ベルトの面・床の線)に合わせてある */
var TLU='tk-lulu-back',TKG='tk-king-back';
/* チェックイン: 赤いカウンター7〜10番。係員(1)は8番、(2)は「となりのカウンター」の9番。カウンターの上端(濃い灰のふた)は y=528。荷物は8番/9番の右どなりのベルト(x 814〜920 / 1130〜1236, 面は y=604) */
ART.ncheckin1={bg:'nairobi-checkin-v1.png',mode:'wide',dep:{lulu:{n:TLU,x:690,by:925},king:{n:TKG,x:790,by:925},clerk:{x:709,top:388,clip:528},
 npcS:{qr_checkin:'tk-clerk-star',qr_checkin2:'tk-clerk'},bubble:{x:709,y:372},
 fx:[{k:'shuttle',img:'nairobi-checkin-belt-bag.png',x0:814,x1:920,w:80,h:96,by:604,v:20,wait:2}],
 people:[{n:'t2-safari-back',x:200,by:940},{n:'t2-man-thobe-back',x:330,by:945},{n:'t2-woman-hijab-front',x:1390,by:940}]}};
ART.ncheckin2={bg:'nairobi-checkin-v1.png',mode:'wide',dep:{lulu:{n:TLU,x:1006,by:925},king:{n:TKG,x:1106,by:925},clerk:{x:1025,top:388,clip:528},
 npcS:{qr_checkin:'tk-clerk-star',qr_checkin2:'tk-clerk'},bubble:{x:1025,y:372},
 fx:[{k:'shuttle',img:'nairobi-checkin-belt-bag.png',x0:1130,x1:1236,w:80,h:96,by:604,v:20,wait:2}],
 people:[{n:'t2-maasai-back',x:200,by:940},{n:'t2-backpacker-back',x:330,by:945},{n:'t2-man-dashiki-front',x:1390,by:940}]}};

/* 保安検査: 左の手前のベルト(x 0〜528・面 y=648)は X線の機械へ入り、右のベルト(x 862〜1258)は機械から出てくる。トレイは両はしで切る */
var SECQ=function(it,it2){return [{k:'queue',img:'nairobi-security-items.png',x0:0,x1:528,by:648,v:14,gap:150,items:it},{k:'queue',img:'nairobi-security-items.png',x0:862,x1:1258,by:648,v:14,gap:150,items:it2}]};
ART.nsec1={bg:'nairobi-security-v1.png',mode:'wide',dep:{lulu:{n:TLU,x:700,by:930},king:{n:TKG,x:800,by:930},bubble:{x:1215,y:400},
 npcS:{sec_n1:{n:'o2-front-officer-green-1',x:1215,by:730,sw:140},sec_n2:{n:'o2-front-officer-blue',x:1215,by:730,sw:130}},
 fx:SECQ([{c:2,s:0,x:60},{c:3,s:0,x:260}],[{c:1,s:0,x:900},{c:4,s:0,x:1100}]),
 people:[{n:'t2-safari-back',x:200,by:950},{n:'t2-woman-hijab-back',x:330,by:955}]}};
ART.nsec2={bg:'nairobi-security-v1.png',mode:'wide',dep:{lulu:{n:TLU,x:700,by:930},king:{n:TKG,x:800,by:930},bubble:{x:1215,y:400},
 npcS:{sec_n1:{n:'o2-front-officer-green-1',x:1215,by:730,sw:140},sec_n2:{n:'o2-front-officer-blue',x:1215,by:730,sw:130}},
 fx:SECQ([{c:4,s:0,x:80},{c:0,s:0,x:300}],[{c:5,s:0,x:880},{c:2,s:0,x:1120}]),
 people:[{n:'t2-maasai-back',x:200,by:950},{n:'t2-backpacker-back',x:330,by:955}]}};
/* 免税店: 広告画面は左の棚のテレビ(外枠 x 300〜477 / y 280〜393)。レジのカウンターの上端は y=602(右の棚の下) */
var DFAD={k:'strip',img:'nairobi-dutyfree-screen-strip.png',x:301,y:281,fw:176,fh:112,n:3,every:2.5};
ART.nduty1={bg:'nairobi-dutyfree-v1.png',mode:'wide',dep:{lulu:{n:TLU,x:1130,by:935},king:{n:TKG,x:1240,by:935},clerk:{x:1280,top:417,clip:602},
 npcS:{duty_staff:'tk-clerk',duty_staff2:'o-front-woman-blonde-suit',ev_trav3:{n:'t2-woman-hijab-front',x:1010,by:900}},bubble:{x:1280,y:400},fx:[DFAD],
 people:[{n:'t2-man-thobe-back',x:170,by:930},{n:'t2-woman-hijab-back',x:300,by:940}]}};
ART.nduty2={bg:'nairobi-dutyfree-v1.png',mode:'wide',dep:{lulu:{n:TLU,x:1130,by:935},king:{n:TKG,x:1240,by:935},clerk:{x:1280,top:417,clip:602},
 npcS:{duty_staff:'tk-clerk',duty_staff2:'o-front-woman-blonde-suit'},bubble:{x:1280,y:400},fx:[{k:'strip',img:'nairobi-dutyfree-screen-strip.png',x:301,y:281,fw:176,fh:112,n:3,every:2.5,ph:2.5}],
 people:[{n:'t2-safari-back',x:170,by:930},{n:'t2-backpacker-back',x:300,by:940}]}};

/* ラウンジ: 座る人6人の配置・ポーズ・向きは正本プレビュー(nairobi-lounge-v2-preview2.png)から測った値(sit は座面に足が着く全身。影なし)。
   時計の針の中心(850,222)(954,222)(1058,222)・TV画面 x826〜1082 / y348〜476。丸ブースのマサイ男性だけ、正本どおり手前のテーブルが下半身を隠す(after) */
var LOUNGEFX=[{k:'clock',img:'nairobi-lounge-clock-hands.png',fw:64,fh:64,n:12,every:1,c:[[850,222],[954,222],[1058,222]],off:[0,4,8]},
 {k:'strip',img:'nairobi-lounge-tv-strip.png',x:826,y:348,fw:256,fh:128,n:4,every:2.5}];
var LOUNGEPPL=[{id:'hijab',sit:1,n:'t-woman-hijab-sit-front',x:576,by:720},{id:'dashiki',sit:1,n:'t-man-dashiki-sit-front',x:672,by:848},
 {id:'maasai',sit:1,n:'t-maasai-sit-front',x:1305,by:882,after:{img:'nairobi-lounge-front-054.png',x:1256,y:667}},{id:'backpacker',sit:1,n:'t-backpacker-sit-front',x:1380,by:950},
 {id:'safari',sit:1,n:'t-safari-sit-front',x:545,by:952},{id:'thobe',sit:1,n:'t-man-thobe-sit-front',x:1051,by:938,after:{img:'lounge-front-thobe-table.png',x:0,y:0}}];
ART.nlounge1={bg:'nairobi-lounge-v2.png',mode:'wide',dep:{lulu:{n:TLU,x:801,by:905},king:{n:TKG,x:904,by:905},clerk:{x:1030,top:330,clip:516},
 npcS:{lounge_staff:'o-front-woman-blonde-suit'},bubble:{x:1030,y:310},fx:LOUNGEFX,people:LOUNGEPPL}};
ART.nlounge2={bg:'nairobi-lounge-v2.png',mode:'wide',dep:{lulu:{n:TLU,x:801,by:905},king:{n:TKG,x:904,by:905},clerk:{x:1030,top:330,clip:516},
 npcS:{lounge_guest:{p:'dashiki'}},bubble:{x:1030,y:310},fx:LOUNGEFX,people:LOUNGEPPL}};
/* ゲート: 窓の外の飛行機=重ね絵を左へゆっくりタキシング(柱・桟の手前には出ない)。FIDS は (1184,356) に静止。受付の机(14番)の上端は y=660 */
var GATEFX=[{k:'plane',img:'nairobi-gate-plane.png',dx0:70,span:320,v:8,fade:2.5,pause:3,clip:[22,86,1490,506],front:[[760,86,27,506],[1140,86,26,506],[1218,86,39,506],[380,86,26,506],[280,86,42,506],[0,336,1536,16]]},
 {k:'still',img:'nairobi-gate-fids.png',x:1184,y:356}];
ART.ngate1={bg:'nairobi-gate-v1.png',mode:'wide',dep:{lulu:{n:TLU,x:700,by:940},king:{n:TKG,x:800,by:940},clerk:{x:1290,top:480,clip:660},
 npcS:{gate_agent:'o-front-woman-blonde-suit',gate_agent2:'tk-clerk'},bubble:{x:1290,y:470},fx:GATEFX,
 people:[{n:'t2-safari-back',x:140,by:950},{n:'t2-man-thobe-back',x:1440,by:950}]}};
ART.ngate2={bg:'nairobi-gate-v1.png',mode:'wide',dep:{lulu:{n:TLU,x:700,by:940},king:{n:TKG,x:800,by:940},clerk:{x:1290,top:480,clip:660},
 npcS:{gate_agent:'o-front-woman-blonde-suit',gate_agent2:'tk-clerk'},bubble:{x:1290,y:470},fx:GATEFX,
 people:[{n:'t2-maasai-back',x:140,by:950},{n:'t2-man-dashiki-back',x:1440,by:950}]}};
/* ナイロビの滞在(タスク058): サファリ(nbo_safari)とマサイマーケット(nbo_market)。背景は人なし・動物なし・布なし(1536×960 フルブリード)。配置の正本は同梱プレビュー(docs/materials/058/*-preview.png)。
   ルル(左)とキング(右)は広間と同じ後ろ姿(hall-lulu-back x=716・hall-king-back x=800、足もと y=884)。プレビューの画素と一致するまで測った位置(最大一致 100%)。
   fx の fauna=動物の別素材(透過PNG)。x=足もとの中心、by=足もとの高さ。影はプレビューと同じ(背景の色を 0.75 倍にする楕円・12行・幅=sw・中心 sx)。
   時間だけで小さく揺れる(足と影は動かず、上半身だけ)。奥の動物から順に描く。ガイド・店の人は素材の旅行者(t-safari-front / t-maasai-front)で、話すとき「…」を出す。
   cloths=マーケットの中央の屋台に吊るした布。2コマ(112×168)をゆっくり切り替えて、布が風にゆれる。 */
var FAUNA=function(n,x,by,sw,per,amp,sx){return {k:'fauna',img:'nairobi-safari-'+n+'.png',x:x,by:by,sw:sw,sx:sx,per:per,amp:amp}};
ART.nsafari={bg:'nairobi-safari-v1.png',mode:'wide',dep:{shF:1,lulu:{n:'hall-lulu-back',x:716,by:884},king:{n:'hall-king-back',x:800,by:884},
 npcS:{safari_guide:{n:'t-safari-front',x:1000,by:850,sw:79}},
 fx:[FAUNA('giraffe',1090,660,178,.6,3,1060),FAUNA('ostrich',590,690,129,1.3,3),FAUNA('zebra',380,700,233,.9,3),FAUNA('gazelle',830,730,149,1.1,3),FAUNA('rhino',1250,730,237,.45,2),FAUNA('lion',250,760,237,.5,2)]}};
ART.nmarket={bg:'nairobi-market-v1.png',mode:'wide',dep:{shF:'rgba(3,10,21,.4)',lulu:{n:'hall-lulu-back',x:716,by:884},king:{n:'hall-king-back',x:800,by:884},
 npcS:{market_vendor:{n:'t-maasai-front',x:900,by:596,sw:79}},
 fx:[{k:'strip',img:'nairobi-market-cloths-strip.png',x:704,y:326,fw:112,fh:168,n:2,every:1.4}]}};
/* アテネ(タスク090 到着 / タスク091 街・出発): 人なしの背景(1536×960)。ふたりは後ろ姿(足もと y=884。ルルが左 x=700・キングが右 x=836。ロヴァニエミと同じ大きさ)。
   相手の人物は既存の素材の流用(アテネ専用の人物素材はまだ無い)。画像が読めないときは build.py の BGA(コード描画)にもどる。
   到着(athens-arrival-v2・093で v1→v2): 窓口は5つ(6〜10番。ガラス y432〜585・カウンター上面 y=585・中央=8番 x=769)。入国審査の係官は窓口の中(頭〜カウンターの高さ y=585 で切る)。客引きと運転手・地下鉄の係員は、ふたりの右の床に立つ(客引き=話し相手が替わるので同じ画面に2人)。
   街(athens-street-v2): 左がタベルナ(戸口 x30〜240・y660〜880・メニュー板 y775〜)・右がおみやげの壁(x1212〜)。店員は戸口の前(x150・足もと y775)、おみやげ屋の人は右の壁ぎわの石畳(x1140・足もと y915)。ホテル(athens-hotel-v2)は手前が一面のベッド(y745〜)なので、3人はベッドの奥の縁(足もと y=752)に立つ。
   出発(athens-departure-v2): 受付は1本(カウンター上面 y=595・看板の隙間 x=775)。チェックインの係員は看板「123」と「eTicket」の間でカウンターの向こう(y=595 で切る)。出国審査の列と搭乗口の係員は、ふたりの右に立つ。 */
ART.athimm1={bg:'athens-arrival-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},clerk:{x:769,top:459,clip:585},npcS:{a_officer:'hexit-officer'},bubble:{x:769,y:417}}};
ART.athimm2={bg:'athens-arrival-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},clerk:{x:769,top:449,clip:585},npcS:{a_officer2:'o-front-officer-blue'},bubble:{x:769,y:417}}};
ART.athtaxi={bg:'athens-arrival-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},people:[{id:'tout',n:'w-front-safari',x:1040,by:890,sw:90},{id:'drv',n:'w-front-man-suit-1',x:1250,by:850,sw:70}],npcS:{a_tout:{p:'tout'},a_driver:{p:'drv'}}}};
ART.athmetro={bg:'athens-arrival-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},npcS:{a_metro:{n:'o-front-officer-blue',x:1040,by:890,sw:70}}}};
ART.athcafe={bg:'athens-street-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},npcS:{a_waiter:{n:'w-front-man-dashiki',x:150,by:775,sw:90}}}};
ART.athshop={bg:'athens-street-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},npcS:{a_shop:{n:'t-woman-hijab-front',x:1140,by:915,sw:79}}}};
ART.athhotel={bg:'athens-hotel-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:640,by:752},king:{n:'hall-king-back',x:776,by:752},npcS:{a_front:{n:'w-front-man-suit-1',x:1010,by:752,sw:70}}}};
ART.athck={bg:'athens-departure-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},clerk:{x:775,top:473,clip:595},npcS:{a_ck:'hexit-officer'},bubble:{x:775,y:433}}};
ART.athdep={bg:'athens-departure-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},npcS:{a_dep:{n:'o-front-officer-blue',x:1160,by:890,sw:70},a_gate:{n:'w-front-pilot-fa',x:1160,by:890,sw:80}}}};
/* ローマ(タスク094 到着4・街3・出発3): 人なしの背景(1536×960・v2)。ふたりは後ろ姿(足もと y=884。ルルが左 x=700・キングが右 x=836。アテネと同じ大きさ)。相手の人物は既存の素材の流用。画像が読めないときは build.py の BGM(コード描画)にもどる。
   到着(rome-arrival-v2): 左に手荷物の窓口(カウンター x40〜418・上面 y=524。係員はカウンターの向こう x=229・y=524 で切る)、中央〜右に「Nastro · Belt 12」のベルト(y568〜)。客引き・案内係・乗り場の係・運転手・窓口の人は、ふたりの右の床(y>713)に立つ。
   街(rome-street-v2): 左がジェラテリア(戸口 x265〜378・y785〜858。店員は戸口の前 x=300・足もと y=860)・右がトラットリアの前の石畳(おみやげ屋の人 x=1180・足もと y=940)。ホテル(rome-hotel-v2)の3人は木の床(y≥876)に立つ(足もと y=900)。
   出発(rome-departure-v2): 切符の窓口「Biglietti · TICKETS」(x678〜1025・窓の中の暗い面 y622〜745)に駅員が立つ(y=745 で切る・x=765)。発車標(x96〜1154・y52〜420)の右半分「Partenze」の中身は背景に描いていないので、別素材 rome-departure-board-strip.png(420×240・2コマ・1秒ごと)を (714,142) に重ねる(fx strip。行き先だけ・時刻は「--:--」・ホーム番号は出ない=テルミニでは発車の少し前に出る)。
   車内の場面(rom_dep_train1)は、右のホーム(x≥1180・y≥690)に停まった電車のそばで、ふたりが乗客・車掌と話す。 */
ART.rombag={bg:'rome-arrival-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},clerk:{x:229,top:402,clip:530},npcS:{m_bag:'hexit-officer'},bubble:{x:229,y:370}}};
ART.rominfo={bg:'rome-arrival-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},people:[{id:'tout',n:'w-front-safari',x:1040,by:890,sw:90},{id:'info',n:'o-front-officer-blue',x:1250,by:880,sw:70}],npcS:{m_tout:{p:'tout'},m_info:{p:'info'}}}};
ART.romtaxi={bg:'rome-arrival-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},people:[{id:'rank',n:'o-front-officer-blue',x:1040,by:890,sw:70},{id:'drv',n:'w-front-man-suit-1',x:1250,by:880,sw:70}],npcS:{m_rank:{p:'rank'},m_driver:{p:'drv'}}}};
ART.romtrain={bg:'rome-arrival-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},npcS:{m_rail:{n:'o-front-officer-green-1',x:1100,by:890,sw:70}}}};
ART.romcafe={bg:'rome-street-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},npcS:{m_gelato:{n:'w-front-man-dashiki',x:300,by:860,sw:90}}}};
ART.romshop={bg:'rome-street-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},npcS:{m_shop:{n:'t-woman-hijab-front',x:1180,by:940,sw:79}}}};
ART.romhotel={bg:'rome-hotel-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:640,by:900},king:{n:'hall-king-back',x:776,by:900},npcS:{m_front:{n:'w-front-man-suit-1',x:1010,by:900,sw:70}}}};
ART.romdtick={bg:'rome-departure-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},clerk:{x:765,top:620,clip:745},npcS:{m_tk:'hexit-officer'},bubble:{x:765,y:588}}};
ART.romdplat={bg:'rome-departure-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},fx:[{k:'strip',img:'rome-departure-board-strip.png',x:714,y:142,fw:420,fh:240,n:2,every:1}],npcS:{m_board:{n:'o-front-officer-blue',x:1010,by:900,sw:70}}}};
ART.romdtrain={bg:'rome-departure-v2.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:1020,by:900},king:{n:'hall-king-back',x:1150,by:900},people:[{id:'pax',n:'t-backpacker-front',x:1290,by:905,sw:79},{id:'cond',n:'w-front-pilot-fa',x:1410,by:905,sw:80}],npcS:{m_pax:{p:'pax'},m_cond:{p:'cond'}}}};
/* チューリッヒ(タスク096 到着4・街3・出発3): 人なしの背景(1536×960)。到着も出発も鉄道(Zürich HB)。ふたりは後ろ姿(足もと y=884。ルルが左 x=700・キングが右 x=836。アテネと同じ大きさ)。
   相手の人物は既存の素材の流用(チューリッヒ専用の人物素材はまだ無い)。画像が読めないときは build.py の BGZ(コード描画)にもどる。
   到着(zurich-arrival-v1): 床は y=712〜。相手はふたりの右の床に立つ。発車標(zur_dep_board1)は fx の still(zurich-board-fra-v1.png=フランクフルト行きの1行。Fernverkehr の最初の行 x=232,y=226 に重ねる。時刻は出さない)。
   街(zurich-street-v1): トラム乗り場(zur_tram1)・カフェ(右の手前のテーブル)・おみやげ屋(左のキオスクの前)。ホテル(zurich-hotel-v1)は部屋の床(ラグの上 y≈925)。
   出発(zurich-departure-v1): ホームホール。床は y=660〜。窓口の係員と、列車の中の乗客・車掌(zur_dep_train1)はふたりの右に立つ。 */
ART.zurarr1={bg:'zurich-arrival-v1.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},npcS:{z_info:{n:'o-front-officer-blue',x:1040,by:890,sw:70}}}};
ART.zurlock={bg:'zurich-arrival-v1.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},npcS:{z_locker:{n:'o-front-officer-green-1',x:1040,by:890,sw:70}}}};
ART.zurtram={bg:'zurich-street-v1.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},npcS:{z_tram:{n:'o-front-officer-blue',x:1040,by:890,sw:70}}}};
ART.zurinfo={bg:'zurich-arrival-v1.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},npcS:{z_info2:{n:'o-front-woman-blonde-suit',x:1040,by:890,sw:70}}}};
ART.zurcafe={bg:'zurich-street-v1.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},npcS:{z_waiter:{n:'w-front-man-suit-1',x:1130,by:880,sw:70}}}};
ART.zurshop={bg:'zurich-street-v1.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},npcS:{z_shop:{n:'o-front-woman-blonde-suit',x:300,by:800,sw:70}}}};
ART.zurhotel={bg:'zurich-hotel-v1.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:470,by:925},king:{n:'hall-king-back',x:606,by:925},npcS:{z_front:{n:'w-front-man-suit-1',x:1010,by:925,sw:70}}}};
ART.zurboard={bg:'zurich-arrival-v1.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},fx:[{k:'still',img:'zurich-board-fra-v1.png',x:232,y:226}],npcS:{z_board:{n:'o2-front-officer-blue',x:1040,by:890,sw:70}}}};
ART.zurticket={bg:'zurich-departure-v1.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},npcS:{z_window:{n:'o-front-woman-blonde-suit',x:1040,by:890,sw:70}}}};
ART.zurtrain={bg:'zurich-departure-v1.png',mode:'wide',dep:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},npcS:{z_pass:{n:'w-front-safari',x:1040,by:890,sw:80},z_conductor:{n:'o-front-officer-green-1',x:1160,by:890,sw:70}}}};
/* ロヴァニエミの到着ロビー(タスク065): 人なしの背景(1536×960。天窓の光が床に描く北極圏ラインが主役)に、オーロラの別素材(4コマ。1コマ1376×172)を左上(80,128)=窓帯の空の部分に重ねる。
   ふたりは後ろ姿で足もと y=884(ルルが左 x=700・キングが右 x=836。ラインの手前。配置の正本は同梱の rovaniemi-arrivals-preview.png)。
   話し相手(rvn_lobby1/2)は、ふたりの右(トロリーとウェルカム看板のあいだの床)に立つ。キャンバスの上から2番目の重ね(背景→オーロラ→人)。 */
ART.rvnlobby={bg:'rovaniemi-arrivals-v1.png',mode:'wide',strips:[{img:'rovaniemi-aurora-strip.png',x:80,y:128,n:4,fw:1376,fh:172,step:1.2}],
 dep:{shF:'rgba(3,10,21,.4)',lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},
  npcS:{r_greeter:{n:'t-backpacker-front',x:1010,by:890,sw:79},r_local:{n:'w-front-man-suit-1',x:1010,by:890,sw:70}}}};
/* ロヴァニエミの村の広場・郵便局の実画(タスク072): 人なしの背景(1536×960)。ふたりは後ろ姿で足もと y=884(配置の正本は同梱プレビュー rovaniemi-village-preview.png / rovaniemi-postoffice-preview.png)。
   広場: オーロラ(80,16)・煙(328,136)・雪のきらめき(168,660)。郵便局: 暖炉の炎(132,524)。strip は汎用の仕組み(065 の rvnlobby と同じ)。話し相手は、ふたりの右の床に立つ。画像が読めないときは build.py の BGS.rvil / rpost(コード描画)にもどる。 */
ART.rvillage={bg:'rovaniemi-village-square-v1.png',mode:'wide',strips:[{img:'rovaniemi-aurora-strip.png',x:80,y:16,n:4,fw:1376,fh:172,step:1.2},{img:'rovaniemi-village-smoke-strip.png',x:328,y:136,n:4,fw:160,fh:120,step:.8},{img:'rovaniemi-village-sparkle-strip.png',x:168,y:660,n:4,fw:1200,fh:240,step:.6}],
 dep:{shF:'rgba(3,10,21,.4)',lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884},
  npcS:{r_vguide:{n:'o-front-woman-blonde-suit',x:1010,by:890,sw:70},r_vwoman:{n:'t-backpacker-front',x:1010,by:890,sw:79}}}};
ART.rpostoffice={bg:'rovaniemi-postoffice-v1.png',mode:'wide',strips:[{img:'rovaniemi-postoffice-flames-strip.png',x:132,y:524,n:4,fw:120,fh:148,step:.35}],
 dep:{shF:'rgba(20,8,2,.35)',lulu:{n:'hall-lulu-back',x:660,by:884},king:{n:'hall-king-back',x:800,by:884},
  npcS:{r_postclerk:{n:'o-front-woman-blonde-suit',x:980,by:890,sw:70},r_poststand:{n:'w-front-man-suit-1',x:980,by:890,sw:70}}}};
/* ドーハ・スークの実画(タスク071): 人なしの背景(1536×960。文字は一切なし)。人物は mode:'wide' の前向きのキング・ルル(足もとの位置は同梱プレビューが正本)。相手(c_tea・c_man など)は今までのドット絵のまま、場面の既存の仕組みで出す。
   ルルがいない場面(doh_city_t3)は、人物の出し分け(OUT.lvis)が今までどおり働く。絵の側でルルを常時描くことはしない。スーツケースは、プレビューに無いので出さない(nosuit)。
   dalley=スークの路地(夜): doh_city_t1/t2/t3 と割りこみ doh_ev_h_prayer。ランタンの明滅(1秒)と吊り布の揺れ(0.8秒)は全面ストリップ(1536×960・(0,0))。ルル x=700・キング x=806・足もと y=856
   dsouq=スークの広場(昼): doh_city_s1/s2/s3 は店の会話だが「店先の広場」として広場の絵で統一(PM判断)。屋台の日よけ布(0.8秒・(0,452)・1536×176)と空の小鳥(0.4秒・(0,36)・1536×120。その場の羽ばたきだけ)。ルル x=660・キング x=770・足もと y=836 */
ART.dalley={bg:'doha-souq-alley-v1.png',mode:'wide',base:856,lulu:700,king:806,suit:0,nosuit:1,npc:{x:228,px:9},fx:'',
 strips:[{img:'doha-souq-alley-lanterns-strip.png',x:0,y:0,n:2,fw:1536,fh:960,step:1},{img:'doha-souq-alley-cloth-strip.png',x:0,y:0,n:2,fw:1536,fh:960,step:.8}]};
ART.dsouq={bg:'doha-souq-square-v1.png',mode:'wide',base:836,lulu:660,king:770,suit:0,nosuit:1,npc:{x:980,px:9},fx:'',
 strips:[{img:'doha-souq-square-cloth-strip.png',x:0,y:452,n:2,fw:1536,fh:176,step:.8},{img:'doha-souq-square-birds-strip.png',x:0,y:36,n:2,fw:1536,fh:120,step:.4}]};
/*ARTSEL*/
function artImg(n){var i=ARTI[n];if(!i){i=ARTI[n]=new Image();i.onerror=function(){i.bad=1};i.src=ARTBASE+n}return i}
function artShow(on){if(ARTSHOW===on)return;ARTSHOW=on;cv.hidden=!!on;cvA.hidden=!on}
function artR(col,x,y,w,h){ca.fillStyle=col;ca.fillRect(Math.round(x),Math.round(y),Math.round(w),Math.round(h))}
function artSprH(img,cx,by,h,flip){var w=Math.round(img.naturalWidth*h/img.naturalHeight),x=Math.round(cx-w/2),y=Math.round(by-h);   /* 表示の高さ h にそろえる(縦横比は素材のまま・NEAREST) */
 if(flip){ca.save();ca.translate(x+w,y);ca.scale(-1,1);ca.drawImage(img,0,0,w,h);ca.restore()}else ca.drawImage(img,x,y,w,h)}
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
 var ex=artExtra(cf),exi={};for(var e=0;e<ex.length;e++){var xi=artImg(artNpcSrc(ex[e]));if(xi.bad){ARTFAIL[id]=1;artShow(0);return false}if(!artOKimg(xi))ok=false;exi[ex[e]]=xi}
 if(cf.dep){var dfi=artDepImgs(cf.dep);for(var dk=0;dk<dfi.length;dk++){var dim=artImg(dfi[dk]);if(!dim.bad&&!artOKimg(dim))ok=false}}   /* 出発まわり(054): 動く別素材が読めないときは、その動きだけ描かない(場面は出す)。読み込み中は暗い板 */
 if(cf.belt){var bt=[artImg(cf.belt.isl),artImg(cf.belt.bags)];for(var bi=0;bi<2;bi++){if(bt[bi].bad){ARTFAIL[id]=1;artShow(0);return false}if(!artOKimg(bt[bi]))ok=false}
  if(cf.trav){var ti=artImg('npc/'+cf.trav.n+'.png');if(!ti.bad&&!artOKimg(ti))ok=false}}   /* 旅行者の絵だけは、読めなくても場面は出す(フォールバックで描く) */
 (cf.strips||[]).forEach(function(q){var si=artImg(q.img);if(!si.bad&&!artOKimg(si))ok=false});   /* 動きの絵が読めないときは、動きだけ出さない(背景と人は出す) */
 artShow(1);
 if(!ok){artR('#10131f',0,0,AW,AH);return true}
 if(S.artT0==null)S.artT0=t;
 var te=t-S.artT0,B=cf.base,BOB=4;
 ca.globalAlpha=1;ca.drawImage(bg,0,0);artStrips(cf.strips);
 if(cf.belt){artBelt(cf,exi,te,S);return true}
 if(cf.seat){artSeat(cf.seat,im,exi,S);return true}
 if(cf.meal){artMeal(cf.meal);return true}
 if(cf.dep){artDep(cf,exi,S,te);return true}
 if(cf.stage){artStage(cf.stage,exi);return true}
 if(cf.hall){artPeople(cf.people,exi);if(cf.bartender&&cf.bartender.n&&exi[cf.bartender.n])artClerk(cf.bartender,exi);artHall(cf.hall,exi);return true}   /* バーテンダー(077b)はカウンターの向こう。ルル・キングより先(奥)に描く */
 if(cf.tk){artTicket(cf.tk,exi,S);return true}
 if(cf.fx==='night')artFxNight();else if(cf.fx==='hotel')artFxHotel();
 /* 相手(いつもの顔のドット): 空港では右から入ってくる。カウンターの中は動かず、頭と肩だけ見せる(カウンターの高さで切る) */
 /* 窓口の係官(入国審査): 頭と肩だけ見せる(窓口の台の高さで切る)。話し相手の窓口は、話すとき小さくうなずいて「…」を出す。そのほかの窓口もゆっくり小さく動く */
 if(cf.booths){var lead=S.d&&S.d.sp==='officer2',pb=null;
  cf.booths.forEach(function(b,bi){var im2=exi[(lead&&b.sw)?b.sw:b.n],bw=im2.naturalWidth,bob2=b.lead&&speaker&&spSay?(Math.floor(t*6)%2?-3:0):(Math.floor(t*.9+bi*.37)%2?-2:0),by0=b.top+bob2,x0=Math.round(b.x-bw/2);
   if(b.s){var dw=Math.round(bw*b.s),dh=Math.round(im2.naturalHeight*b.s),vis=Math.min(b.clip-by0,dh);   /* 倍率つきの窓口(タスク064): 最近傍で縮め、頭と肩だけ(clip の高さで切る) */
    ca.drawImage(im2,0,0,bw,vis/b.s,Math.round(b.x-dw/2),by0,dw,vis);
    if(b.lead&&speaker&&spSay)pb=[b.x+Math.round(dw*.4),b.top-18];return}
   ca.drawImage(im2,0,0,bw,b.clip-by0,x0,by0,bw,b.clip-by0);
   if(b.lead&&speaker&&spSay)artBubble(b.x+Math.round(bw*.4),b.top-18)});
  if(cf.glass){ca.fillStyle=cf.glass.c;cf.glass.r.forEach(function(q){ca.fillRect(q[0],q[1],q[2],q[3])})}   /* ガラス越し(タスク064): 係官の上にガラスの薄い色を重ねる(正本プレビューと同じ)。「…」はガラスの手前 */
  if(pb)artBubble(pb[0],pb[1])}
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
 (cf.people||[]).forEach(function(q,qi){L.push({by:q.by,f:function(){artPeople([q],exi)}})});
 (cf.crowd||[]).forEach(function(c,ci){L.push({by:c[2],f:function(){var img=exi['w-'+c[0]],bw=img.naturalWidth,
   o=c[3]==='walk'?(Math.floor(t*3.2+ci*.4)%2?-3:0):(Math.floor(t*1.1+ci*.53)%2?-2:0);
   artShadow(c[1],c[2],bw*.42,.3);artSpr(img,c[1],c[2]+o,false)}})});
 if(!cf.nosuit)L.push({by:B,f:function(){if(cf.suitImg){var si=exi[cf.suitImg.n];ca.drawImage(si,Math.round(cf.suitImg.x-si.naturalWidth/2),B-si.naturalHeight)}else artSuit(cf.suit-dir*sh,B,room)}});
 if(OUT.lvis)L.push({by:B,f:function(){var ly=0,limg;
  if(walking){var lf=Math.floor(te/.2)%4;limg=im[['lulu-walk-a','lulu-walk-b','lulu-walk-c','lulu-walk-b'][lf]];ly=lf%2?-BOB:0}
  else{limg=im['lulu-idle'];ly=Math.floor(t*1.6+.5)%2?-BOB:0}
  if(luHelp&&!walking)ly-=Math.floor(t*7)%2?10:0;
  var lk=cf.lh?cf.lh/limg.naturalHeight:1;artShadow(lx,B,shw*.8*lk);if(cf.lh)artSprH(limg,lx,B+ly,cf.lh,walking&&dir<0);else artSpr(limg,lx,B+ly,walking&&dir<0);   /* ルルの歩きのコマは右向き。左へ歩くときだけ反転。lh=表示の高さ(085-I) */
  if(luTalk&&spSay&&!walking)artBubble(lx+20,B-(cf.lh||limg.naturalHeight)-26);
  if(luHelp&&!walking){ca.fillStyle='#e8452c';ca.font='800 26px sans-serif';ca.textAlign='center';ca.textBaseline='middle';ca.fillText('♪',lx+(cf.lh?cf.lh/limg.naturalHeight:1)*limg.naturalWidth*.5,B-(cf.lh||limg.naturalHeight)-12)}}});
 if(OUT.hvis)L.push({by:B,f:function(){var ky=0,kimg;
  if(walking){var kf=Math.floor(te/.32)%2;kimg=im[kf?'king-walk-b':'king-walk-a'];ky=kf?-BOB:0}
  else{kimg=im['king-idle'];ky=Math.floor(t*1.6)%2?-BOB:0}
  artShadow(kx,B,shw*(cf.kh?cf.kh/kimg.naturalHeight:1));if(cf.kh)artSprH(kimg,kx,B+ky,cf.kh,walking&&dir>0);else artSpr(kimg,kx,B+ky,walking&&dir>0)}});   /* 右へ歩くときは、元の左向きのコマを左右反転(左へ歩くときは元のまま) */
 L.sort(function(a,b){return a.by-b.by});for(var li=0;li<L.length;li++)L[li].f();
 return true}
/* 荷物受け取りを描く(タスク045)。荷物6個が楕円の経路を1周 period 秒でまわる(時間だけで動く。会話の進み方にはかかわらない)。
   θ=i/n の等間隔 − 2π×経過/period(θは減る向き=手前の縁で左→右、奥の縁で右→左)。接地点 x=cx+rx cosθ, y=cy+ry sinθ(半分の大きさの座標。四捨五入して2画素単位)。
   描く順は 奥の半分→島→手前の半分→ふたり。同じ半分の中では sin の小さい(奥の)順。 */
/* 専用スーツケースの角度(タスク046)。台詞(3番目 line=2)の「緑の板のとなりの青いの」に合わせて、その台詞が始まったとき緑の板のとなり(右どなり)に来る。
   それまでは、ほかの荷物と同じ向き・同じ速さでベルトをまわる(始まりから tpre 秒後に板のとなりに着く並び)。台詞が始まったら ease 秒でなめらかに板のとなりへ寄せ、
   台詞のあいだは ほかの荷物の creep 倍の速さでゆっくり進む(読めるあいだ、板のとなりにとどまる)。会話の進み方(G.ti)にだけ合わせ、時計にはよらない */
function artWrapPi(a){var W=6.283185307179586;a=a%W;if(a>Math.PI)a-=W;if(a<-Math.PI)a+=W;return a}
function artHeroTh(S,te,L,H,om){
 if(L<H.line)return H.th+om*(H.tpre-te);
 if(S.hz0==null){S.hz0=te;S.hzD=artWrapPi(om*(H.tpre-te))}
 var u=Math.max(0,Math.min(1,(te-S.hz0)/H.ease)),e=u*u*(3-2*u);
 return H.th-om*H.creep*(te-S.hz0)+S.hzD*(1-e)}
function artBelt(cf,exi,te,S){var B=cf.belt,bi=artImg(B.bags),isl=artImg(B.isl),ths=[],i,stop=false;
 for(var q=0;q<B.stopFor.length;q++)if(S&&S.vid===B.stopFor[q])stop=true;
 var ph=stop?0:te/B.period;
 for(i=0;i<B.n;i++){var th=i*6.283185307179586/B.n-6.283185307179586*ph,sn;
  if(B.hero&&i===B.hero.i){var H=B.hero,hv=S&&S.vid,hL=(typeof G!=='undefined'&&G.ti)|0;   /* 専用スーツケース(046): 受け取り前の場面だけ見える。会話で取った(hide番目の台詞)あとと、荷物を受け取ったあとの場面(nbo_bag2)では、ベルトから消える */
   if(hv!==H.vid&&H.also.indexOf(hv)<0)continue;
   if(hv===H.vid){if(hL>=H.hide)continue;th=artHeroTh(S,te,hL,H,6.283185307179586/B.period)}}
  sn=Math.sin(th);
  ths.push({i:i,sn:sn,x:2*Math.round(B.cx+B.rx*Math.cos(th)),y:2*Math.round(B.cy+B.ry*sn)})}
 var drawG=function(back){var g=ths.filter(function(o){return (o.sn<0)===back}).sort(function(a,b){return a.sn-b.sn});
  for(var k=0;k<g.length;k++){var o=g[k],lv=Math.max(0,Math.min(B.lv-1,Math.round((o.sn+1)/2*(B.lv-1))));
   ca.drawImage(bi,lv*B.cw,o.i*B.ch,B.cw,B.ch,o.x-B.ax,o.y-B.ay,B.cw,B.ch)}};
 drawG(true);ca.drawImage(isl,B.ix,B.iy);drawG(false);
 if(cf.trav&&S&&S.vid===cf.trav.vid)artTrav(cf.trav);
 artHall(cf.hall,exi)}
/* 場面の人(タスク047)。人は「いる」だけ(会話・採点の対象にしない)。足と影は動かさず、腰から上だけ小さく揺れる(037)。縮小は素材づくりの段階(NEAREST)で済んでいて、ここでは拡大縮小しない。
   影: 正本プレビューの楕円(幅 sw の9行。縦の半径は約4画素)。色 rgba(68,70,82,.62)(床で(196,202,210)→(117,121,131)、ベルトの縁で(128,136,148)→(90,95,107)。正本と同じ) */
var ARTSHK=[.835,.899,.949,.975,1,.975,.949,.899,.835];
/* 058: 素材パックのプレビューと同じ影(12行の楕円。shF が色の文字列ならその色、1なら黒の29%)。dep に shF:1 を付けた場面のルル・キングだけ */
function artShadowF(cx,top,sw,col){ca.fillStyle=typeof col==='string'?col:'rgba(0,0,0,.29)';for(var fr=0;fr<12;fr++){var fv=sw*Math.sqrt(1-((fr-5.5)/6)*((fr-5.5)/6));ca.fillRect(Math.round(cx-fv/2),top+fr,Math.round(fv),1)}}
function artShadowP(cx,by,sw){ca.fillStyle='rgba(68,70,82,.62)';for(var r=0;r<9;r++){var w=Math.round(sw*ARTSHK[r]);ca.fillRect(Math.round(cx-w/2),by-1+r-4,w,1)}}
function artSwayD(ph,per){return Math.floor(t*(per||1.1)+(ph||0))%2?3:0}
/* 荷物受け取りの旅行者。ベルトの右端の横。絵が読めないときは SP.traveler(コードで描いたドット絵)で同じ高さに描く */
function artTrav(T){var im=artImg('npc/'+T.n+'.png');
 if(!im.bad&&artOKimg(im)){artShadowP(T.x,T.by,T.sw);artSway(im,T.x,T.by,artSwayD(.7,.9));return}
 var m=SP.traveler&&SP.traveler.m&&SP.traveler.m[0];if(!m)return;var nm=m[0],px=Math.max(1,Math.round(126/nm.length));
 artShadowP(T.x,T.by,T.sw);artSpA(nm,m[1],Math.round(T.x-nm[0].length*px/2),T.by-nm.length*px,px,0)}
/* 人なし背景の場面に置く旅行者。list=[{n:'t-safari-front',x:足もとの中心,by:足もとの高さ,sw:影の幅,sit:座り(影なし。座面に足が着く)}]。端の位置に置くのは場面を入れる側 */
function artPeople(list,exi){for(var i=0;i<(list||[]).length;i++){var P=list[i],im=exi[P.n];if(!im||im.bad||!artOKimg(im))continue;
 if(!P.sit)artShadowP(P.x,P.by,P.sw||Math.round(im.naturalWidth*1.2));artSway(im,P.x,P.by,artSwayD(i*.37+.2,1))}}
/* 機内の対面アップ(タスク048)。ふたりは座った上半身(テーブルの上端で切る)。小さく上下にゆれる。CAは右の通路側に立ち、話しているとき小さく跳ねて「…」を出す */
function artSeat(H,im,exi,S){
 var ki=im['king-idle'],li=im['lulu-idle'],kd=Math.floor(t*1.1)%2?3:0,ld=Math.floor(t*1.1+.5)%2?3:0;
 ca.save();ca.beginPath();ca.rect(0,0,AW,H.clip);ca.clip();
 ca.drawImage(li,Math.round(H.lulu.x),Math.round(H.lulu.y-ld),Math.round(li.naturalWidth*H.lulu.s),Math.round(li.naturalHeight*H.lulu.s));
 ca.drawImage(ki,Math.round(H.king.x),Math.round(H.king.y-kd),Math.round(ki.naturalWidth*H.king.s),Math.round(ki.naturalHeight*H.king.s));
 ca.restore();
 var ci=exi[H.ca.n];if(!ci)return;var cw=Math.round(ci.naturalWidth*H.ca.s),chh=Math.round(ci.naturalHeight*H.ca.s),hop=spSay&&Math.floor(t*6)%2?-4:0,cx=Math.round(H.ca.x-cw/2),cy=H.ca.by-chh+hop+(Math.floor(t*1.3)%2?-2:0);
 ca.drawImage(ci,cx,cy,cw,chh);
 if(spSay)artBubble(cx+Math.round(cw*.2),cy-20)}
/* 機内食の場面(タスク048): 背景の絵そのまま。ルルが話しているとき、ルルの頭の上に「…」 */
function artMeal(M){if(luTalk&&spSay)artBubble(M.bubble.x,M.bubble.y)}
/* 賢者の広間を描く(タスク040)。歩かない。足と影は動かさず、上半身だけ小さく揺れる(タスク037)。話しているとき「…」を出す */
function artSway(img,cx,by,d){var w=img.naturalWidth,h=img.naturalHeight,x=Math.round(cx-w/2),y=by-h,cut=Math.round(h*.58);
 ca.drawImage(img,0,0,w,cut,x,y-d,w,cut+d);   /* 上半身: 上へd画素のばす(足側は動かない) */
 ca.drawImage(img,0,cut,w,h-cut,x,y+cut,w,h-cut)}   /* 腰から下: 固定 */
/* ホテルのロビー・通常版(タスク066): 受付カウンターの向こうのスタッフ。頭と肩〜カウンターの上(clip)まで描き、腰より上だけ小さく揺れる。話しているとき「…」を出す */
function artClerk(C,exi){var im=exi[C.n];if(!im||im.bad||!artOKimg(im))return;
 artCounterNpc(im,C.x,C.top-(spSay&&Math.floor(t*6)%2?3:0),C.clip,Math.floor(t*.8)%2?3:0);
 if(spSay&&speaker)artBubble(C.x+Math.round(im.naturalWidth*.3),C.top-18)}
/* プールサイドのステージ(タスク066)。歌手・観客・ルル・キングを足もとの浅い順(奥→手前)に重ねて描く。足と影は動かさず、上半身だけ小さく揺れる(037)。
   歌手: 歌っていない間は正面(f)、テーマ曲が鳴っているあいだは拍ごとに歌う絵(a/b)を切りかえる。♪は歌っているあいだだけ頭の上をのぼる */
function artStage(H,exi){var L=[],sg=H.singer,fi=exi[sg.f],ai=exi[sg.a],bi=exi[sg.b],i;
 var pl=(typeof songPlaying==='function')&&songPlaying(),bn=pl&&typeof songBeatN==='function'?songBeatN():-1,sim=fi;
 if(pl)sim=[ai,fi,bi,fi][(bn>=0?bn:Math.floor(t*2))%4];   /* タスク076: 歌っているあいだは拍ごとに [歌う絵1(左向き) → 正面 → 歌う絵2(右向き) → 正面]。足もと・影は固定(037) */
 (H.people||[]).forEach(function(q,qi){var im=exi[q.n];if(!im||im.bad||!artOKimg(im))return;
  L.push({by:q.by,f:function(){artShadowP(q.x,q.by,q.sw||Math.round(im.naturalWidth*1.2));artSway(im,q.x,q.by,artSwayD(qi*.37+.2,1))}})});
 if(sim&&!sim.bad&&artOKimg(sim))L.push({by:sg.by,f:function(){artShadow(sg.x,sg.by,sg.sw||sim.naturalWidth*.6,.45);artSway(sim,sg.x,sg.by,pl?0:(Math.floor(t*.8)%2?3:0));
  if(spSay&&speaker)artBubble(sg.x+Math.round(sim.naturalWidth*.3),sg.by-sim.naturalHeight-18);
  if(sg.notes&&pl){for(var nq=0;nq<3;nq++){var np2=(t*.45+nq/3)%1;ca.globalAlpha=np2<.65?1:(1-np2)/.35;ca.font='800 44px sans-serif';ca.textAlign='center';ca.textBaseline='middle';ca.lineJoin='round';ca.lineWidth=7;ca.strokeStyle='#05070f';ca.fillStyle='#ffe9a8';
   var nx2=sg.x+28+nq*30+Math.round(Math.sin(t*2+nq*2)*8),ny2=sg.by-sim.naturalHeight-16-np2*70,nc=nq%2?'♫':'♪';ca.strokeText(nc,nx2,ny2);ca.fillText(nc,nx2,ny2)}ca.globalAlpha=1}}});
 var lu=exi[H.lulu.n],kg=exi[H.king.n],ld=Math.floor(t*1.1+.5)%2?3:0,kd=Math.floor(t*1.1)%2?3:0;
 if(OUT.lvis&&lu&&!lu.bad)L.push({by:H.lulu.by,f:function(){artShadow(H.lulu.x,H.lulu.by,H.lulu.rx||29);artSway(lu,H.lulu.x,H.lulu.by,ld);if(luTalk&&spSay)artBubble(H.lulu.x+(H.lulu.bx||20),H.lulu.by-lu.naturalHeight-26)}});
 if(OUT.hvis&&kg&&!kg.bad)L.push({by:H.king.by,f:function(){artShadow(H.king.x,H.king.by,H.king.rx||36);artSway(kg,H.king.x,H.king.by,kd)}});
 if(H.spot)artSpot(sg,1);   /* 光の円錐と足もとの光だまり: 人物より先(下)に描く → 観客・ルル・キング・歌手を隠さない */
 L.sort(function(a,b){return a.by-b.by});for(i=0;i<L.length;i++)L[i].f();
 if(H.spot)artSpot(sg,2)}   /* キラキラ: 人物の上の空の側にだけ小さく */
/* ステージ照明(タスク076)。コード描画・単純な半透明図形だけ(shadowBlur・グラデーションは使わない。ドットの粒を潰さない)。曲が鳴っている間だけ強く、鳴っていないときは消える。拍で脈打つ。
   artSpotK = 光の強さ(0〜1。曲が鳴ると上がり、止まるとなめらかに消える)。part 1 = 光の円錐+足もとの光だまり、part 2 = キラキラ */
var artSpotK=0,artSpotT0=0;
function artSpot(sg,part){
 if(part===1){var dt=Math.min(.1,Math.max(0,t-artSpotT0));artSpotT0=t;var on=(typeof songPlaying==='function')&&songPlaying();artSpotK+=((on?1:0)-artSpotK)*Math.min(1,dt*3);if(artSpotK<.01)artSpotK=0}
 if(artSpotK<=0)return;
 var k=artSpotK,pu=(typeof songBeatPulse==='function')?songBeatPulse():0,x=sg.x,by=sg.by;
 ca.save();
 if(part===1){
  /* 円錐: 歌手の上方(y=40・幅±22)から足もと(幅±190)へ。ふたつ重ねて中心を少し濃く。透明度は控えめ(拍で少しだけ強まる) */
  ca.fillStyle='#ffe3a0';
  ca.globalAlpha=(.07+.03*pu)*k;ca.beginPath();ca.moveTo(x-22,40);ca.lineTo(x+22,40);ca.lineTo(x+190,by);ca.lineTo(x-190,by);ca.closePath();ca.fill();
  ca.globalAlpha=(.07+.04*pu)*k;ca.beginPath();ca.moveTo(x-12,40);ca.lineTo(x+12,40);ca.lineTo(x+95,by);ca.lineTo(x-95,by);ca.closePath();ca.fill();
  /* 足もとの光だまり(楕円・外と内) */
  ca.globalAlpha=.14*k;ca.beginPath();ca.ellipse(x,by,170,30,0,0,6.2832);ca.fill();
  ca.globalAlpha=(.12+.06*pu)*k;ca.beginPath();ca.ellipse(x,by,96,17,0,0,6.2832);ca.fill()}
 else{
  /* キラキラ: 位置は固定(決め打ちの配列)・星(十字のドット)。瞬き=ゆっくりの位相、脈打ち=拍。観客の頭(y>600)より上の空の側に置く */
  var S0=[[-300,-210,0],[-210,-90,1.3],[-120,-330,2.1],[-150,-170,.7],[0,-290,3.2],[-250,-60,1.9],[130,-210,4.1],[200,-120,2.6],[290,-260,.4],[340,-80,3.7],[-340,-70,5.0],[250,-70,1.1],[-170,-50,4.4],[40,-340,5.6]];   /* 歌手の体(x±110・y 484〜734)と観客の頭(y>600)には重ならない位置 */
  ca.fillStyle='#fff3c4';
  for(var i=0;i<S0.length;i++){var q=S0[i],tw=.5+.5*Math.sin(t*2.4+q[2]*2),a=(.18+.5*tw)*(.4+.6*pu)*k;if(a<.03)continue;
   var sx=Math.round(x+q[0]),sy=Math.round(by+q[1]-60),r=(i%3===0)?10:6;ca.globalAlpha=Math.min(.7,a);
   ca.fillRect(sx-1,sy-1,3,3);if(tw>.45||pu>.5){ca.fillRect(sx-r,sy,r*2+1,2);ca.fillRect(sx,sy-r,2,r*2+1)}}}
 ca.restore()}
/* 大きさを指定して描く artSway(タスク068。同梱プレビューの大きさに合わせる。NEAREST)。dw×dh=描く大きさ(素材を一様に拡大)、clipY=これより下(画面の y)は描かない(テーブルの天板で下半身が隠れる)。
   揺れていないコマ(d=0)は1回で描く(同梱プレビューと同じ画素になる)。上半身は d 画素ふくらむ(artSway と同じ)。 */
function artSwayZ(img,cx,by,d,dw,dh,clipY){var w=img.naturalWidth,h=img.naturalHeight,x=Math.round(cx-dw/2),y=by-dh;
 ca.save();if(clipY){ca.beginPath();ca.rect(0,0,AW,clipY);ca.clip()}
 if(!d)ca.drawImage(img,x,y,dw,dh);
 else{var sc=Math.round(h*.58),dc=Math.round(dh*sc/h);ca.drawImage(img,0,0,w,sc,x,y-d,dw,dc+d);ca.drawImage(img,0,sc,w,h-sc,x,y+dc,dw,dh-dc)}
 ca.restore()}
function artHall(H,exi){var g=H.globe,gi=g&&artImg(g.img);
 if(g&&artOKimg(gi)){var f=Math.floor(t/(g.period/g.n))%g.n;ca.drawImage(gi,f*g.fw,0,g.fw,g.fw,g.x,g.y,g.fw*g.z,g.fw*g.z)}   /* 球だけ回す(NEAREST。ぼかさない) */
 var sg=H.sage&&exi[H.sage.n],lu=exi[H.lulu.n],kg=exi[H.king.n],sd=Math.floor(t*.8)%2?3:0,ld=Math.floor(t*1.1+.5)%2?3:0,kd=Math.floor(t*1.1)%2?3:0;
 if(sg){artShadow(H.sage.x,H.sage.by,sg.naturalWidth*.6,.45);artSway(sg,H.sage.x,H.sage.by,sd);
  if(spSay&&speaker)artBubble(H.sage.x+Math.round(sg.naturalWidth*.3),H.sage.by-sg.naturalHeight-18);
  /* 歌っているあいだ(テーマ曲が鳴っているあいだ)だけ、音符が歌手の頭の上をのぼって消える(タスク049) */
  if(H.notes&&typeof songPlaying==='function'&&songPlaying()){for(var nq=0;nq<3;nq++){var np2=(t*.45+nq/3)%1;ca.globalAlpha=np2<.65?1:(1-np2)/.35;ca.font='800 44px sans-serif';ca.textAlign='center';ca.textBaseline='middle';ca.lineJoin='round';ca.lineWidth=7;ca.strokeStyle='#05070f';ca.fillStyle='#ffe9a8';
   var nx2=H.sage.x+28+nq*30+Math.round(Math.sin(t*2+nq*2)*8),ny2=H.sage.by-sg.naturalHeight-16-np2*70,nc=nq%2?'♫':'♪';ca.strokeText(nc,nx2,ny2);ca.fillText(nc,nx2,ny2)}ca.globalAlpha=1}}
 else if(H.clerk)artClerk(H.clerk,exi);
 else if(H.bubble&&spSay&&speaker)artBubble(H.bubble.x,H.bubble.y);   /* 相手を絵に出さない場面(羽田のゲート): 声のぬしの場所に「…」 */
 if(OUT.lvis){if(H.lulu.h){if(H.lulu.sh)artShadow(H.lulu.x,H.lulu.by,H.lulu.sh);artSwayZ(lu,H.lulu.x,H.lulu.by,ld,H.lulu.w,H.lulu.h);   /* 大きさ指定の後ろ姿(077b): 影なし・素材を拡大して置く(dep の w/h と同じ作法) */
   if(luTalk&&spSay)artBubble(H.lulu.x+(H.lulu.bx||20),H.lulu.by-H.lulu.h-26)}
  else{artShadow(H.lulu.x,H.lulu.by,H.lulu.rx||29);artSway(lu,H.lulu.x,H.lulu.by,ld);
  if(luTalk&&spSay)artBubble(H.lulu.x+(H.lulu.bx||20),H.lulu.by-lu.naturalHeight-26)}}
 if(OUT.hvis){if(H.king.h){if(H.king.sh)artShadow(H.king.x,H.king.by,H.king.sh);artSwayZ(kg,H.king.x,H.king.by,kd,H.king.w,H.king.h)}
  else{artShadow(H.king.x,H.king.by,H.king.rx||36);artSway(kg,H.king.x,H.king.by,kd)}}}
/* チケット売り場を描く(タスク041)。歩かない。足と影は動かさず、上半身だけ小さく揺れる(037)。係員は話しているとき「…」を出す。
   航路の地図(route)は、窓口の「線を引く」会話(bg:'rtmap')のあいだだけ。描けなければ、航路入りの静止画に切りかえる。会話の進み方には一切かかわらない(時間だけで動く) */
function artTicket(H,exi,S){
 var rt=!!(S.d&&S.d.bg==='rtmap');
 if(rt&&!S.rtFail){try{ca.save();artRoute(H.route,S);ca.restore()}catch(e){S.rtFail=1;try{ca.restore()}catch(e2){}ca.globalAlpha=1}}
 if(rt&&S.rtFail){var fb=artImg(H.bgFix);if(artOKimg(fb))ca.drawImage(fb,0,0)}
 var star=!!(S.d&&(artSpKey()==='desk_star'||/_star$/.test(String(S.vid||''))));   /* スター側の場面は女性の係員(タスク044) */
 var cl=exi[star&&H.clerkS?H.clerkS.n:H.clerk.n],lu=exi[H.lulu.n],kg=exi[H.king.n],sd=Math.floor(t*.8)%2?3:0,ld=Math.floor(t*1.1+.5)%2?3:0,kd=Math.floor(t*1.1)%2?3:0;
 /* 係員: 足もとはカウンターの向こうに隠れる。頭と肩〜カウンターの高さまでを描き、腰より上だけ上へ伸び縮み */
 var cw=cl.naturalWidth,chh=cl.naturalHeight,cx=Math.round(H.clerk.x-cw/2),cut=Math.round(chh*.58),vis=H.clerk.clip-H.clerk.top;   /* vis=見える高さ(カウンターの高さまで) */
 ca.drawImage(cl,0,0,cw,Math.min(cut,vis),cx,H.clerk.top-sd,cw,Math.min(cut,vis)+sd);
 if(vis>cut)ca.drawImage(cl,0,cut,cw,vis-cut,cx,H.clerk.top+cut,cw,vis-cut);
 if(spSay&&speaker)artBubble(H.clerk.x+Math.round(cw*.3),H.clerk.top-18);
 if(OUT.lvis){artShadow(H.lulu.x,H.lulu.by,56);artSway(lu,H.lulu.x,H.lulu.by,ld);
  if(luTalk&&spSay)artBubble(H.lulu.x+20,H.lulu.by-lu.naturalHeight-26);
  if(luHelp){ca.fillStyle='#e8452c';ca.font='800 26px sans-serif';ca.textAlign='center';ca.textBaseline='middle';ca.fillText('♪',H.lulu.x+Math.round(lu.naturalWidth*.5),H.lulu.by-lu.naturalHeight-12)}}
 if(OUT.hvis){artShadow(H.king.x,H.king.by,70);artSway(kg,H.king.x,H.king.by,kd)}}
/* ---- 壁の地図に航路を引く(タスク041): 場面の進み(S.rf=ここまで引いた本数 / S.rn=この会話で引く本数 / S.rt=その始まりの時刻)に合わせて、1区間ずつ ----
   小さい飛行機が今の区間を飛び、点線を引く。着いた都市の印が光る。もどる線(rn>=6)は、青い点線が少し進んで止まり、✕が点滅(赤は使わない) */
var RTP=null;
function rtPath(R,i){var sg=R.segs[i],A=R.cities[sg[0]],B=R.cities[sg[1]],ax=A[0],ay=A[1],bx=B[0]+sg[2],by=B[1],dx=bx-ax,dy=by-ay,L=Math.sqrt(dx*dx+dy*dy)||1,nx=-dy/L,ny=dx/L;
 if(ny>0){nx=-nx;ny=-ny}var h=L*.16,qx=(ax+bx)/2+nx*h,qy=(ay+by)/2+ny*h,pts=[],cum=[0],k,N=80,px=ax,py=ay;
 for(k=0;k<=N;k++){var u=k/N,w=1-u,x=w*w*ax+2*w*u*qx+u*u*bx,y=w*w*ay+2*w*u*qy+u*u*by;pts.push([x,y]);if(k){cum.push(cum[k-1]+Math.sqrt((x-px)*(x-px)+(y-py)*(y-py)))}px=x;py=y}
 return {pts:pts,cum:cum,len:cum[N]}}
function rtAt(P,s){var c=P.cum,n=c.length-1,k=0;while(k<n-1&&c[k+1]<s)k++;var u=c[k+1]>c[k]?(s-c[k])/(c[k+1]-c[k]):0;u=Math.max(0,Math.min(1,u));
 var a=P.pts[k],b=P.pts[k+1];return [a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u]}
function rtWrap(R,x){var W=R.x1-R.x0;while(x<R.x0)x+=W;while(x>=R.x1)x-=W;return x}
var PLANE=[[10,0,3,1],[8,1,6,1],[3,2,16,2],[0,2,3,1],[2,4,16,1],[7,5,6,1],[9,6,3,1],[1,1,2,1],[0,0,2,1]],PLCOL=['#f4f1e8','#f4f1e8','#f4f1e8','#c8522f','#8fb4c0','#f4f1e8','#f4f1e8','#c8522f','#c8522f'];
function rtPlane(x,y,face){var p=3,W=19;for(var i=0;i<PLANE.length;i++){var r=PLANE[i],rx=face>0?r[0]:W-r[0]-r[2];ca.fillStyle=PLCOL[i];ca.fillRect(Math.round(x-W*p/2+rx*p),Math.round(y-4*p+r[1]*p),r[2]*p,r[3]*p)}}
var RING=['..XXXXX..','.XX...XX.','XX.....XX','X...o...X','X..ooo..X','X...o...X','XX.....XX','.XX...XX.','..XXXXX..'];
function rtCity(x,y,lit,since){var p=3,s=9*p,r,c;
 if(lit&&since>=0&&since<1.4){var g=Math.floor(since*6)%2,k=since<.7?1:0,o=(2+Math.floor(since*8))*p+(g?p:0);ca.globalAlpha=Math.max(.2,1-since/1.4);
  for(r=0;r<9;r++)for(c=0;c<9;c++){if(RING[r].charAt(c)!=='X')continue;var dx=(c-4)*(p+o/4),dy=(r-4)*(p+o/4);ca.fillStyle='#ffb02e';ca.fillRect(Math.round(x+dx-p/2),Math.round(y+dy-p/2),p,p)}ca.globalAlpha=1}
 for(r=0;r<9;r++)for(c=0;c<9;c++){var ch=RING[r].charAt(c);if(ch==='.')continue;ca.fillStyle=lit?(ch==='X'?'#c9730e':'#ffd36a'):'#c98a22';ca.fillRect(Math.round(x-s/2+c*p),Math.round(y-s/2+r*p),p,p)}}
function artRoute(R,S){
 if(window.__artRouteBreak)throw new Error('route break');
 if(!RTP){RTP=R.segs.map(function(s,i){return rtPath(R,i)})}
 var rf=S.rf||0,rw=S.rn||0,rn=Math.min(rw,R.segs.length),e=(S.rt!=null)?t-S.rt:0,D=R.D,SP=R.sp,i,k,head=null,face=-1,ci={};
 ca.globalAlpha=1;
 for(i=0;i<R.segs.length;i++){var f=0;if(i<rf)f=1;else if(i<rn)f=Math.max(0,Math.min(1,(e-(i-rf)*D)/D));if(f<=0)break;
  var P=RTP[i],sg=R.segs[i],S0=f*P.len;
  for(var s=SP*.5;s<=S0;s+=SP){var q=rtAt(P,s);ca.fillStyle='#d98a1c';ca.fillRect(Math.round(rtWrap(R,q[0]))-4,Math.round(q[1])-1,8,3);ca.fillRect(Math.round(rtWrap(R,q[0]))-1,Math.round(q[1])-4,3,8)}
  var hp=rtAt(P,S0),h2=rtAt(P,Math.max(0,S0-6));head=[rtWrap(R,hp[0]),hp[1]];if(Math.abs(hp[0]-h2[0])>.5)face=hp[0]>h2[0]?1:-1;
  if(f>=1){ci[sg[1]]=(i<rf)?99:(e-(i-rf+1)*D)}}
 /* 都市の印: 出発地は最初から光り、着いた都市は光る(着いてすぐは光の輪がまたたく) */
 var A=R.cities;rtCity(A.tok[0],A.tok[1],true,99);
 for(var kc in ci){rtCity(A[kc][0],A[kc][1],true,ci[kc])}
 /* 区間の番号の札(089): 線を半分引いたところで、その区間の番号(1〜16)が出る。引いた番号は残る。札は区間の中ほどか、R.tag の位置(札が重なるところ)。札の位置が線から離れるときは、細い線でつなぐ */
 var mv=0;
 for(i=0;i<R.segs.length;i++){var f2=0;if(i<rf)f2=1;else if(i<rn)f2=Math.max(0,Math.min(1,(e-(i-rf)*D)/D));if(f2>0)mv=i+1;if(f2<.5)continue;
  var mp=rtAt(RTP[i],RTP[i].len*.5),mx=rtWrap(R,mp[0]),my=mp[1],tg=R.tag&&R.tag[i+1],tx=tg?tg[0]:mx,ty=tg?tg[1]:my-26;
  if(tg||Math.abs(tx-mx)+Math.abs(ty-my)>30){ca.strokeStyle='#6e4c2c';ca.lineWidth=3;ca.beginPath();ca.moveTo(mx,my);ca.lineTo(tx,ty);ca.stroke()}
  var pop=(i>=rf&&f2<1)?1.2:1,rr=19*pop;
  ca.fillStyle='#6e4c2c';ca.beginPath();ca.arc(tx,ty,rr+3,0,6.2832);ca.fill();ca.fillStyle='#fff7dc';ca.beginPath();ca.arc(tx,ty,rr,0,6.2832);ca.fill();
  ca.fillStyle='#6e4c2c';ca.font='900 '+Math.round(24*pop)+'px sans-serif';ca.textAlign='center';ca.textBaseline='middle';ca.fillText(String(i+1),tx,ty+1)}
 /* 数えるカウンター(089): 左下に「移動 n/16」、寄港を数えている会話では右に「寄港 m/15」。大きい数字で、いくつまで数えたかが見える */
 function plaque(x,label,n,mx2){ca.fillStyle='#6e4c2c';ca.fillRect(x-4,358,208,122);ca.fillStyle='#f4ecd0';ca.fillRect(x,362,200,114);
  ca.fillStyle='#8a7b55';ca.font='800 28px sans-serif';ca.textAlign='left';ca.textBaseline='alphabetic';ca.fillText(label,x+12,396);
  ca.fillStyle='#c9730e';ca.font='900 62px sans-serif';ca.fillText(n+'/'+mx2,x+12,460)}
 if(mv>0)plaque(350,'MOVES',mv,16);
 if(S.stp>0)plaque(850,'STOPS',S.stp,15);
 /* 小さい飛行機: いま飛んでいる区間の先頭。どこも引いていないときは羽田で待つ */
 if(!head)head=[A.tok[0],A.tok[1]];
 rtPlane(head[0],head[1]-14+(Math.floor(t*3)%2?-1:0),face)}

/* ============================================================
   ナイロビ出発まわり(タスク054): チェックイン・保安検査・免税店・ラウンジ・ゲートの新しい背景(1536×960・人なし)
   描く順: 背景 → 動く別素材(fx) → 相手(カウンター越し) → 人(座る人・立つ旅行者・ルル・キングを足もとの高さの順) → 手前の覆い(after)
   - fx: still=止まった重ね絵 / strip=コマ切り替え(NEAREST) / clock=時計の針(3つ) / shuttle=ベルトを1個だけ横へ(両はしのカウンターに隠れる)
         / queue=トレイが列でベルトを流れる(両はしで切る) / plane=窓の外の飛行機(ゆっくり横へ。柱の手前には出ない)
   - 人は 047 の artSway(足と影は固定・上半身だけ小さく揺れる)。座る人(sit)は影なし。
   - npcS: 話し相手(SP のキー)→ 絵。文字列=カウンター越しの係員(頭と肩だけ。clerk の top〜clip で切って下は描かない)。{p:'id'}=座る人のひとりが話し相手。{n,x,by,sw}=立つ人
   - 相手を絵に出さない声だけの場面(電話・アナウンス)は bubble の位置に「…」 */
function artDepImgs(D){var a=[];(D.fx||[]).forEach(function(f){if(f.img)a.push(f.img)});(D.people||[]).forEach(function(q){if(q.after)a.push(q.after.img)});return a}
function artDepNames(D){var a=[];['lulu','king'].forEach(function(k){if(D[k])a.push(D[k].n)});(D.people||[]).forEach(function(q){a.push(q.n)});
 if(D.npcS)for(var k in D.npcS){var v=D.npcS[k];if(typeof v==='string')a.push(v);else if(v&&v.n)a.push(v.n)}return a}
function artFx(f,te,bg){var im=f.img?artImg(f.img):null,i,k;
 if(im&&(im.bad||!artOKimg(im)))return;
 if(f.k==='still'){ca.drawImage(im,f.x,f.y)}
 else if(f.k==='strip'){var fr=Math.floor((t+(f.ph||0))/f.every)%f.n;ca.drawImage(im,fr*f.fw,0,f.fw,f.fh,f.x,f.y,f.fw,f.fh)}
 else if(f.k==='fauna'){   /* 動物(タスク058): 影(背景を0.75倍に。12行の楕円)→ 上半身だけ小さく揺れる動物。per=周期の秒数・amp=揺れの画素 */
  var fw=im.naturalWidth,fA=(f.sw||fw)/2,fcx=f.sx!=null?f.sx:f.x,fr,fv;ca.fillStyle='rgba(0,0,0,.25)';
  for(fr=0;fr<12;fr++){fv=2*fA*Math.sqrt(1-((fr-5.5)/6)*((fr-5.5)/6));ca.fillRect(Math.round(fcx-fv/2),f.by-8+fr,Math.round(fv),1)}
  artSway(im,f.x,f.by,Math.floor(t*f.per+(f.x%7)*.31)%2?f.amp:0)}
 else if(f.k==='clock'){var cn=Math.floor(t/f.every);for(i=0;i<f.c.length;i++){var fc=(cn+(f.off[i]||0))%f.n;ca.drawImage(im,fc*f.fw,0,f.fw,f.fh,f.c[i][0]-f.fw/2,f.c[i][1]-f.fh/2,f.fw,f.fh)}}
 else if(f.k==='shuttle'){   /* ベルトの上の荷物1個。左のカウンターの奥から出て右のカウンターの奥へ消え、wait 秒あいてまた出てくる */
  var W=f.x1-f.x0+f.w,mv=W/f.v,u=(te%(mv+f.wait))*f.v;if(u>W)return;
  ca.save();ca.beginPath();ca.rect(f.x0,f.by-f.h-4,f.x1-f.x0,f.h+8);ca.clip();ca.drawImage(im,2*Math.round((f.x0-f.w+u)/2),f.by-f.h);ca.restore()}
 else if(f.k==='queue'){   /* トレイ(と中身)が列でベルトを流れる。x0〜x1の外は描かない(機械に入る・出てくる)。large=112×96のコマ(トレイの底は y=86)、small=88×60のコマ(底は y=58) */
  var L=f.x1-f.x0+f.gap,p;ca.save();ca.beginPath();ca.rect(f.x0,f.by-100,f.x1-f.x0,104);ca.clip();
  for(i=0;i<f.items.length;i++){var it=f.items[i],sm=it.s?1:0,cw=sm?88:112,ch=sm?60:96,bt=sm?58:86;
   p=((it.x-f.x0+f.v*te)%L+L)%L+f.x0-cw;ca.drawImage(im,it.c*cw,sm?96:0,cw,ch,2*Math.round(p/2),f.by-bt,cw,ch)}ca.restore()}
 else if(f.k==='plane'){   /* 窓の外の飛行機(1536×960の重ね絵)。左へゆっくりタキシング(機首が左)。両はしでフェード。柱・窓の桟の手前には出ない(front=背景から柱を描き直す) */
  var T=f.span/f.v,P=T+f.pause,u2=te%P;if(u2>T)return;var a=Math.max(0,Math.min(1,u2/f.fade,(T-u2)/f.fade));
  ca.save();ca.beginPath();ca.rect(f.clip[0],f.clip[1],f.clip[2],f.clip[3]);ca.clip();ca.globalAlpha=a;ca.drawImage(im,2*Math.round((f.dx0-f.v*u2)/2),0);ca.globalAlpha=1;
  for(k=0;k<f.front.length;k++){var r=f.front[k];ca.drawImage(bg,r[0],r[1],r[2],r[3],r[0],r[1],r[2],r[3])}ca.restore()}}
/* カウンター越しの相手: 頭と肩〜カウンターの高さ(clip)まで。腰より上だけ小さく伸び縮み(037)。下は描かない */
function artCounterNpc(img,x,top,clip,d){var w=img.naturalWidth,h=img.naturalHeight,cx=Math.round(x-w/2),cut=Math.round(h*.58),vis=clip-top;
 ca.drawImage(img,0,0,w,Math.min(cut,vis),cx,top-d,w,Math.min(cut,vis)+d);if(vis>cut)ca.drawImage(img,0,cut,w,vis-cut,cx,top+cut,w,vis-cut)}
function artDep(cf,exi,S,te){
 var D=cf.dep,bg=artImg(cf.bg),i,fx=D.fx||[],sk=artSpKey(),sv=(D.npcS&&sk)?D.npcS[sk]:null,said=false,L=[];
 for(i=0;i<fx.length;i++)artFx(fx[i],te,bg);
 /* 話し相手が カウンター越しの係員 */
 if(typeof sv==='string'&&D.clerk&&exi[sv]){var cl=exi[sv],cs=Math.floor(t*.8)%2?3:0,cy=D.clerk.top+(spSay&&Math.floor(t*6)%2?-3:0);
  artCounterNpc(cl,D.clerk.x,cy,D.clerk.clip,cs);if(spSay&&speaker)artBubble(D.clerk.x+Math.round(cl.naturalWidth*.3),D.clerk.top-18);said=true}
 /* 人: 座る人・立つ旅行者(話し相手が立つ人{n,x,by,sw}なら、それもここに入る) */
 var ppl=(D.people||[]).slice();if(sv&&typeof sv==='object'&&sv.n)ppl.push({n:sv.n,x:sv.x,by:sv.by,sw:sv.sw,spk:1});
 ppl.forEach(function(q,qi){var im=exi[q.n];if(!im||im.bad||!artOKimg(im))return;
  L.push({by:q.by,f:function(){if(!q.sit)artShadowP(q.x,q.by,q.sw||Math.round(im.naturalWidth*1.15));
   if(q.z)artSwayZ(im,q.x,q.by,artSwayD(qi*.37+.2,1),Math.round(im.naturalWidth*q.z),Math.round(im.naturalHeight*q.z),q.clipY);else artSway(im,q.x,q.by,artSwayD(qi*.37+.2,1));
   if(q.after){var ai=artImg(q.after.img);if(artOKimg(ai))ca.drawImage(ai,q.after.x,q.after.y)}
   if(spSay&&speaker&&(q.spk||(sv&&sv.p&&sv.p===q.id))){artBubble(q.x+Math.round(im.naturalWidth*(q.z||1)*.3),q.by-Math.round(im.naturalHeight*(q.z||1))-18);said=true}}})});
 var lu=D.lulu&&exi[D.lulu.n],kg=D.king&&exi[D.king.n],ld=Math.floor(t*1.1+.5)%2?3:0,kd=Math.floor(t*1.1)%2?3:0;
 if(lu&&OUT.lvis)L.push({by:D.lulu.by,f:function(){if(D.lulu.h){if(D.lulu.sh)artShadow(D.lulu.x,D.lulu.by,D.lulu.sh);artSwayZ(lu,D.lulu.x,D.lulu.by,ld,D.lulu.w,D.lulu.h);   /* 大きさ指定の後ろ姿(068): 影は描かない(同梱プレビューと同じ) */
   if(luTalk&&spSay)artBubble(D.lulu.x+20,D.lulu.by-D.lulu.h-26);return}
  if(D.shF)artShadowF(D.lulu.x,D.lulu.by-7,84,D.shF);else artShadow(D.lulu.x,D.lulu.by,56);artSway(lu,D.lulu.x,D.lulu.by,ld);
  if(luTalk&&spSay)artBubble(D.lulu.x+20,D.lulu.by-lu.naturalHeight-26);
  if(luHelp){ca.fillStyle='#e8452c';ca.font='800 26px sans-serif';ca.textAlign='center';ca.textBaseline='middle';ca.fillText('♪',D.lulu.x+Math.round(lu.naturalWidth*.5),D.lulu.by-lu.naturalHeight-12)}}});
 if(kg&&OUT.hvis)L.push({by:D.king.by,f:function(){if(D.king.h){if(D.king.sh)artShadow(D.king.x,D.king.by,D.king.sh);artSwayZ(kg,D.king.x,D.king.by,kd,D.king.w,D.king.h);return}
  if(D.shF)artShadowF(D.king.x,D.king.by-7,84,D.shF);else artShadow(D.king.x,D.king.by,70);artSway(kg,D.king.x,D.king.by,kd)}});
 L.sort(function(a,b){return a.by-b.by});for(i=0;i<L.length;i++)L[i].f();
 if(D.cup)artCup(D.cup);
 if(D.pay&&typeof payFg==='function'&&typeof PAYFX!=='undefined'&&PAYFX){var c0=c;c=ca;ca.save();ca.translate(D.pay.ox,D.pay.oy);ca.scale(D.pay.k,D.pay.k);try{payFg(1)}catch(e){}ca.restore();c=c0}   /* 支払いの演出(061): 旧画面の座標を ox,oy + k倍で重ねる(背景を塗りつぶす片づけは art では出さない) */
 artStrips(cf.strips,1);
 if(spSay&&speaker&&!speaker.ghost&&!said&&D.bubble)artBubble(D.bubble.x,D.bubble.y)}   /* 絵に出ない相手(ghost=電話の声・アナウンス)には「…」を出さない。立つ人・係員・座る人が話し相手のとき、その人の上に出す */
/* 自由会話のコーヒーカップ(タスク073): 残り時間の見せ方。数字・文字は出さない。FT.cup()=残り(1→0)。自由会話の最中だけ、テーブルの手前(先生とキング・ルルのあいだ)に大きめのカップを置き、コーヒーが少しずつ(4px刻みで12段)減っていく。cx=中心 by=受け皿の底 */
function artCup(C){
 var f=(typeof FT!=='undefined'&&FT.cup)?FT.cup():null;if(f==null)return;
 var O='#5a3a24',CUP='#f6f1e6',SH='#e0d6c0',bx=C.x-48,top=C.by-80,sx=C.x-60,i;
 artR('#5a4a3a',sx-4,C.by-12,128,4);artR('#c9bfa8',sx,C.by-8,120,8);artR('#f4eee0',sx,C.by-8,120,4);   /* 受け皿 */
 var hb=[[bx+92,top+16,20,8],[bx+104,top+16,8,32],[bx+92,top+40,20,8]];   /* 取っ手(Cの字) */
 for(i=0;i<3;i++)artR(O,hb[i][0]-4,hb[i][1]-4,hb[i][2]+8,hb[i][3]+8);
 for(i=0;i<3;i++)artR(CUP,hb[i][0],hb[i][1],hb[i][2],hb[i][3]);
 artR(O,bx-4,top-4,104,64);artR(O,bx+4,top+56,88,24);   /* 本体のふち(上は広く、下はすぼむ) */
 artR(CUP,bx,top,96,56);artR(CUP,bx+8,top+56,80,16);artR(SH,bx+80,top+4,16,52);artR(SH,bx+72,top+56,16,16);
 artR('#fffaf0',bx,top,96,4);
 artR('#d8cdb4',bx+8,top+8,80,44);   /* カップのなか(空) */
 var h=Math.round(f*40/4)*4;
 if(h>0){artR('#6b3f23',bx+8,top+52-h,80,h);artR('#8f5a34',bx+8,top+52-h,80,4)}   /* コーヒー。h=0〜40 */
 if(f>.05){var ph;for(i=0;i<2;i++){ph=(Math.floor(t*1.5)+i*2)%4;ca.globalAlpha=.5;artR('#fff',bx+28+i*28+(ph%2)*4,top-14-ph*6,8,8)}ca.globalAlpha=1}}
/* 背景に重ねる小さな動き(タスク051)。strips=[{img,x,y,n,fw,fh,step}]。NEARESTの粒のまま(拡大縮小しない)。会話の進み方にはかかわらず、時間だけで切り替わる */
function artStrips(list,over){for(var i=0;i<(list||[]).length;i++){var q=list[i],im=artImg(q.img);if(!!q.over!==!!over||im.bad||!artOKimg(im))continue;var f=Math.floor(t/q.step)%q.n;
  if(q.sync==='beat'&&typeof songBeatN==='function'){var bn=songBeatN();if(bn>=0)f=bn%q.n}   /* タスク066: テーマ曲が鳴っているあいだは、曲の再生位置の拍に合わせて切りかえる(鳴っていないときは、ゆっくりの時間切りかえ) */
  ca.drawImage(im,f*q.fw,0,q.fw,q.fh,q.x,q.y,q.fw,q.fh)}}
/* 人物の絵の置き場: ふつうは npc/ の中。'@' で始まる名前は art/ の直下(先生の素材。タスク068) */
function artNpcSrc(n){return n.charAt(0)==='@'?n.slice(1)+'.png':'npc/'+n+'.png'}
function artOKimg(i){return i.complete&&i.naturalWidth>0}
/* この場面が使う人物の絵の名前(npc/ の中)。ひとつでも読めなければ、場面全体が今までの描画に戻る */
function artExtra(cf){var a=[],i;if(cf.seat&&cf.seat.ca)a.push(cf.seat.ca.n);if(cf.hall)['sage','lulu','king'].forEach(function(k){if(cf.hall[k])a.push(cf.hall[k].n)});if(cf.hall&&cf.hall.clerk)a.push(cf.hall.clerk.n);if(cf.bartender&&cf.bartender.n)a.push(cf.bartender.n);if(cf.stage){var sg=cf.stage.singer;[sg.f,sg.a,sg.b,cf.stage.lulu.n,cf.stage.king.n].forEach(function(n){a.push(n)});(cf.stage.people||[]).forEach(function(q){a.push(q.n)})}if(cf.tk)['clerk','clerkS','lulu','king'].forEach(function(k){if(cf.tk[k])a.push(cf.tk[k].n)});(cf.crowd||[]).forEach(function(c){a.push('w-'+c[0])});
 (cf.booths||[]).forEach(function(b){a.push(b.n);if(b.sw)a.push(b.sw)});if(cf.suitImg)a.push(cf.suitImg.n);(cf.people||[]).forEach(function(q){a.push(q.n)});
 if(cf.npcS)for(var k in cf.npcS)a.push(cf.npcS[k]);if(cf.dep)a=a.concat(artDepNames(cf.dep));return a}
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
 rvn:'airport',ath:'airport',zur:'airport',ahlan:'lounge',hotel:'hotel',room:'hotel',home:'hotel',sage:'hotel',vault:'hotel',mosque:'hotel',atop:'cabin',souk:'street',city:'street',dohc:'street',
 beach:'sea',marina:'sea',fountain:'outdoor',safari:'outdoor'};
/* 背景の名前 → カテゴリ(場所の音と食いちがうとき、こちらが先) */
var AMBBG={taxi:'outdoor',dtaxi:'outdoor',rbus:'outdoor',ataxi:'outdoor',acafe:'street',ashop:'street',ahotel:'hotel',ztram:'outdoor',zcafe:'street',zshop:'street',zhotel:'hotel',cabinQ:'cabin',cabin:'cabin',chotel:'hotel',cbreak:'hotel'};
var ambEl=null,ambCat=null,ambDuck=false;
function ambOn(){try{return localStorage.getItem('kd_snd')!=='off'}catch(e){return true}}
function ambApply(){var c=ambCat&&AMB[ambCat];
 if(!c||!c.src||!ambOn()||ambDuck||document.hidden){if(ambEl){try{ambEl.pause()}catch(e){}}return}
 var u=/^(data:|https?:)/.test(c.src)?c.src:AMBBASE+c.src;
 if(!ambEl||ambEl._u!==u){if(ambEl){try{ambEl.pause()}catch(e){}}ambEl=new Audio(u);ambEl.loop=true;ambEl._u=u}
 ambEl.volume=c.vol;var p=ambEl.play();if(p&&p.catch)p.catch(function(){})}
window.__ambGo=function(kind){ambCat=AMBSND[kind]||null;ambApply()};
window.__ambScene=function(kind,bg){ambCat=AMBBG[bg]||AMBSND[kind]||null;ambApply()};
window.__ambDuck=function(f){ambDuck=!!f;ambApply();if(window.__songSync)window.__songSync()};   /* マイクで聞いているあいだは、曲(タスク049)も止める */
window.__ambSync=ambApply;window.__AMB=AMB;
document.addEventListener('visibilitychange',ambApply);
