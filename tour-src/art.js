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
 /* ナイロビのホテルの部屋(タスク051): 到着の夜、部屋で休む場面(nbo_room)。人なしの背景をフルブリード。ふたりは後ろ姿(足もと y=884、ルル x=700・キング x=836)。人は置かない。
    tv=壁のTV画面の矩形(1536×960座標)。今回は何も映さない。将来の映画場面のために名前つきで記録しておく */
 nroom:{bg:'nairobi-hotel-room-v1.png',mode:'wide',hall:{lulu:{n:'hall-lulu-back',x:700,by:884},king:{n:'hall-king-back',x:836,by:884}},tv:{x:1120,y:216,w:344,h:176}},
 hotel:{bg:'hotel-front.png',mode:'room',base:895,lulu:250,king:450,suit:560,npc:{x:1290,px:15,top:262,clip:412},fx:'hotel',npcS:{c_front:'o-front-woman-blonde-suit'}},
 /* 賢者の広間(タスク040): 人なしの背景をフルブリード。賢者は壇上の中央(大人の高さ136px)、ルル(左)とキング(右)は絨毯の上に後ろ姿で寄って立つ(広い場面の大きさ)。
    globe=背景の球の位置(球の外わく 312..473×356..517)に、球だけ8コマ(96px。2倍=192px)を重ね、period秒で1回転。人は足と影を固定し、上半身だけ小さく揺れる(タスク037) */
 sage:{bg:'sage-hall-bg-clean.png',mode:'wide',hall:{sage:{n:'hall-sage',x:768,by:684},lulu:{n:'hall-lulu-back',x:733,by:905},king:{n:'hall-king-back',x:803,by:905},
  globe:{img:'sage-hall-globe-strip.png',x:296,y:340,n:8,fw:96,z:2,period:1.8}}},
 /* チケット売り場=旅行代理店の一室(タスク041): 人なし・航路なしの背景をフルブリード(028)。係員はカウンターの向こうの中央に大人の大きさ(室内の基準273px)で、カウンターの高さで切って下は隠す。
    ルル(左)とキング(右)は絨毯の上に後ろ姿で寄って立つ(室内の基準の大きさ。素材のまま)。中心の間隔136px・体の横幅は131＋136pxで、すき間は約3px。
    route=壁の地図に航路を引く場面(窓口の「線を引く」会話 bg:'rtmap')だけの設定。bgFix=アニメが描けなかったときの、航路入りの静止画。
    cities=地図の上の都市の位置(1536×960の座標。地図の枠の内側は x340..1200, y92..478)。segs=区間(出発,到着,横ずれ)。横ずれ -860 は、地図の左はしから出て右はしに入る西まわり */
 ticket:{bg:'ticket-office-bg-clean-noroute.png',mode:'room',tk:{bgFix:'ticket-office-bg-clean.png',
  clerk:{n:'tk-clerk',x:768,top:420,clip:596},clerkS:{n:'tk-clerk-star'},lulu:{n:'tk-lulu-back',x:699,by:920},king:{n:'tk-king-back',x:835,by:920},
  route:{x0:340,x1:1200,D:1.1,sp:15,cities:{tok:[1080,193],nbo:[784,237],rov:[806,142],cus:[552,300],hon:[476,177]},
   segs:[['tok','nbo',0],['nbo','rov',0],['rov','cus',0],['cus','hon',0],['hon','tok',-860]]}}},
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
 /* 羽田の出発ゲート(タスク043): 人なしの背景をフルブリード。券で絵が出し分けられる(oneworld=DOHA・Qatar Airways / Star=ISTANBUL・Turkish Airlines)。
    ルル(左・102px)とキング(右・114px)は広間と同じ後ろ姿で、足もとは y=884。相手の係員は絵には出さず(声だけ)、話すときカウンターの上に「…」を出す(bubble)。
    秘密イベント(ルルの拾い物)は、この場面を遊び終えたとき 保存の keep に入るだけで、絵にも画面にも何も出さない(予告しない) */
 hgate_ow:{bg:'haneda-departure-gate-v2-ow.png',mode:'wide',hall:{lulu:{n:'hall-lulu-back',x:690,by:884},king:{n:'hall-king-back',x:760,by:884},bubble:{x:250,y:552}}},
 hgate_st:{bg:'haneda-departure-gate-v2-star.png',mode:'wide',hall:{lulu:{n:'hall-lulu-back',x:690,by:884},king:{n:'hall-king-back',x:760,by:884},bubble:{x:250,y:552}}},
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
 nlobby:{bg:'nairobi-hotel-lobby-v1.png',mode:'wide',hall:{sage:{n:'hall-singer',x:1130,by:800},lulu:{n:'hall-lulu-back',x:985,by:915},king:{n:'hall-king-back',x:1060,by:915},notes:1}},
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
var LOUNGEPPL=[{id:'hijab',sit:1,n:'t-woman-hijab-sit-side-2',x:576,by:735},{id:'dashiki',sit:1,n:'t-man-dashiki-sit-side-2',x:632,by:863},
 {id:'maasai',sit:1,n:'t-maasai-sit-side-1',x:1305.5,by:865,after:{img:'nairobi-lounge-front-054.png',x:1256,y:667}},{id:'backpacker',sit:1,n:'t-backpacker-sit-side-1',x:1380.5,by:955},
 {id:'safari',sit:1,n:'t-safari-sit-side-2',x:545,by:960},{id:'thobe',sit:1,n:'t-man-thobe-sit-side-2',x:1051,by:959}];
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
 if(cf.hall){artPeople(cf.people,exi);artHall(cf.hall,exi);return true}
 if(cf.tk){artTicket(cf.tk,exi,S);return true}
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
 (cf.people||[]).forEach(function(q,qi){L.push({by:q.by,f:function(){artPeople([q],exi)}})});
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
function artHall(H,exi){var g=H.globe,gi=g&&artImg(g.img);
 if(g&&artOKimg(gi)){var f=Math.floor(t/(g.period/g.n))%g.n;ca.drawImage(gi,f*g.fw,0,g.fw,g.fw,g.x,g.y,g.fw*g.z,g.fw*g.z)}   /* 球だけ回す(NEAREST。ぼかさない) */
 var sg=H.sage&&exi[H.sage.n],lu=exi[H.lulu.n],kg=exi[H.king.n],sd=Math.floor(t*.8)%2?3:0,ld=Math.floor(t*1.1+.5)%2?3:0,kd=Math.floor(t*1.1)%2?3:0;
 if(sg){artShadow(H.sage.x,H.sage.by,sg.naturalWidth*.6,.45);artSway(sg,H.sage.x,H.sage.by,sd);
  if(spSay&&speaker)artBubble(H.sage.x+Math.round(sg.naturalWidth*.3),H.sage.by-sg.naturalHeight-18);
  /* 歌っているあいだ(テーマ曲が鳴っているあいだ)だけ、音符が歌手の頭の上をのぼって消える(タスク049) */
  if(H.notes&&typeof songPlaying==='function'&&songPlaying()){for(var nq=0;nq<3;nq++){var np2=(t*.45+nq/3)%1;ca.globalAlpha=np2<.65?1:(1-np2)/.35;ca.font='800 44px sans-serif';ca.textAlign='center';ca.textBaseline='middle';ca.lineJoin='round';ca.lineWidth=7;ca.strokeStyle='#05070f';ca.fillStyle='#ffe9a8';
   var nx2=H.sage.x+28+nq*30+Math.round(Math.sin(t*2+nq*2)*8),ny2=H.sage.by-sg.naturalHeight-16-np2*70,nc=nq%2?'♫':'♪';ca.strokeText(nc,nx2,ny2);ca.fillText(nc,nx2,ny2)}ca.globalAlpha=1}}
 else if(H.bubble&&spSay&&speaker)artBubble(H.bubble.x,H.bubble.y);   /* 相手を絵に出さない場面(羽田のゲート): 声のぬしの場所に「…」 */
 if(OUT.lvis){artShadow(H.lulu.x,H.lulu.by,29);artSway(lu,H.lulu.x,H.lulu.by,ld);
  if(luTalk&&spSay)artBubble(H.lulu.x+20,H.lulu.by-lu.naturalHeight-26)}
 if(OUT.hvis){artShadow(H.king.x,H.king.by,36);artSway(kg,H.king.x,H.king.by,kd)}}
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
 if(rw>=6){var f6=Math.max(0,Math.min(1,e/1.2)),H=A.hon,C=A.cus,lim=.28*f6,ex=null;
  for(k=0;k<=24*lim;k++){var u=k/24,xx=H[0]+(C[0]-H[0])*u,yy=H[1]+(C[1]-H[1])*u;if(k%2===0){ca.fillStyle='#5aa0ff';ca.fillRect(Math.round(xx)-2,Math.round(yy)-2,4,4)}ex=[xx,yy]}
  if(f6>=1&&ex&&Math.floor(t*3)%2){ca.fillStyle='#fff';ca.fillRect(Math.round(ex[0])-12,Math.round(ex[1])-12,24,24);ca.fillStyle='#2f6ad8';ca.fillRect(Math.round(ex[0])-10,Math.round(ex[1])-10,20,20);
   ca.fillStyle='#fff';ca.font='800 18px sans-serif';ca.textAlign='center';ca.textBaseline='middle';ca.fillText('✕',Math.round(ex[0]),Math.round(ex[1])+1)}}
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
  L.push({by:q.by,f:function(){if(!q.sit)artShadowP(q.x,q.by,q.sw||Math.round(im.naturalWidth*1.15));artSway(im,q.x,q.by,artSwayD(qi*.37+.2,1));
   if(q.after){var ai=artImg(q.after.img);if(artOKimg(ai))ca.drawImage(ai,q.after.x,q.after.y)}
   if(spSay&&speaker&&(q.spk||(sv&&sv.p&&sv.p===q.id))){artBubble(q.x+Math.round(im.naturalWidth*.3),q.by-im.naturalHeight-18);said=true}}})});
 var lu=D.lulu&&exi[D.lulu.n],kg=D.king&&exi[D.king.n],ld=Math.floor(t*1.1+.5)%2?3:0,kd=Math.floor(t*1.1)%2?3:0;
 if(lu&&OUT.lvis)L.push({by:D.lulu.by,f:function(){artShadow(D.lulu.x,D.lulu.by,56);artSway(lu,D.lulu.x,D.lulu.by,ld);
  if(luTalk&&spSay)artBubble(D.lulu.x+20,D.lulu.by-lu.naturalHeight-26);
  if(luHelp){ca.fillStyle='#e8452c';ca.font='800 26px sans-serif';ca.textAlign='center';ca.textBaseline='middle';ca.fillText('♪',D.lulu.x+Math.round(lu.naturalWidth*.5),D.lulu.by-lu.naturalHeight-12)}}});
 if(kg&&OUT.hvis)L.push({by:D.king.by,f:function(){artShadow(D.king.x,D.king.by,70);artSway(kg,D.king.x,D.king.by,kd)}});
 L.sort(function(a,b){return a.by-b.by});for(i=0;i<L.length;i++)L[i].f();
 if(spSay&&speaker&&!speaker.ghost&&!said&&D.bubble)artBubble(D.bubble.x,D.bubble.y)}   /* 絵に出ない相手(ghost=電話の声・アナウンス)には「…」を出さない。立つ人・係員・座る人が話し相手のとき、その人の上に出す */
/* 背景に重ねる小さな動き(タスク051)。strips=[{img,x,y,n,fw,fh,step}]。NEARESTの粒のまま(拡大縮小しない)。会話の進み方にはかかわらず、時間だけで切り替わる */
function artStrips(list){for(var i=0;i<(list||[]).length;i++){var q=list[i],im=artImg(q.img);if(im.bad||!artOKimg(im))continue;var f=Math.floor(t/q.step)%q.n;ca.drawImage(im,f*q.fw,0,q.fw,q.fh,q.x,q.y,q.fw,q.fh)}}
function artOKimg(i){return i.complete&&i.naturalWidth>0}
/* この場面が使う人物の絵の名前(npc/ の中)。ひとつでも読めなければ、場面全体が今までの描画に戻る */
function artExtra(cf){var a=[],i;if(cf.seat&&cf.seat.ca)a.push(cf.seat.ca.n);if(cf.hall)['sage','lulu','king'].forEach(function(k){if(cf.hall[k])a.push(cf.hall[k].n)});if(cf.tk)['clerk','clerkS','lulu','king'].forEach(function(k){if(cf.tk[k])a.push(cf.tk[k].n)});(cf.crowd||[]).forEach(function(c){a.push('w-'+c[0])});
 (cf.booths||[]).forEach(function(b){a.push(b.n);if(b.sw)a.push(b.sw)});(cf.people||[]).forEach(function(q){a.push(q.n)});
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
window.__ambDuck=function(f){ambDuck=!!f;ambApply();if(window.__songSync)window.__songSync()};   /* マイクで聞いているあいだは、曲(タスク049)も止める */
window.__ambSync=ambApply;window.__AMB=AMB;
document.addEventListener('visibilitychange',ambApply);
