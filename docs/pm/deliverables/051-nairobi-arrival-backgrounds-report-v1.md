# タスク051 完了報告：ナイロビ到着まわりの新背景（SIM・タクシー・ホテルの部屋）

ベースは main の c56fa45（タスク052を取り込み済み。取り込み後にビルドと新規テストをやり直した）。確認はヘッドレスブラウザ（`tour-src/tests/test_arrival051.py` 101項目すべてOK）。**実機でしか分からない点は末尾に切り分けた。**

## 変更したファイル
- `tour-src/art.js`：art 設定に `simshop`（新規）・`nairobi`（差し替え）・`nroom`（新規）。汎用の strip 描画 `artStrips`（新規）
- `tour-src/build.py`：`artIdFor`（tour側だけ）に bg `sim`→`simshop`、`nroom`→`nroom`。場所 `hroom`。`enterPlace` に `rest`。`lockedPlace`（tourだけ）で「場面の数が空の場所は数えず飛ばす」
- `tour-src/song.js`／`tour-src/song_data.py`：ホテルの部屋の場面（`ROOM_SCENE`＝`nbo_room`、`roomRest`）と、絵が読めないときのドット部屋 `BGS.nroom`
- `tour-src/tests/test_arrival051.py`（新規）、`tour-src/tests/test_song049.py`（到着タブの並びの期待値を hroom 付きに更新）
- 素材5点を `tour/assets/art/` に（`nairobi-sim-v1.png` ほか）。生成物 `tour/index.html`・`tour/doha/index.html`

## art 設定の数値（1536×960座標）
- `simshop`：bg `nairobi-sim-v1.png`／base 900・ルル 700・キング 860・荷物 965／店員 `npc{x:768, top:372, clip:500}`（カウンターの高さ y=500 で切る＝入国審査・タクシーと同じ方式）。`npcS`：`sim_staff`→`w-front-man-suit-1`、`sim_staff2`→`w-front-man-dashiki`
- `nairobi`（タクシー）：bg `nairobi-taxi-v1.png`／base 926・ルル 300・キング 470・荷物 575・係員 x=1060（実測の結果、旧値を維持）／`npcS` 維持
- `nroom`：bg `nairobi-hotel-room-v1.png`／後ろ姿 ルル x=700・キング x=836・足もと y=884／人なし／`tv:{x:1120,y:216,w:344,h:176}`（x1120–1464 / y216–392。何も映さない）

## strip アニメ
- 置き場：`art.js` の `artStrips(list)`。**wide の場面で汎用**（設定の `strips:[{img,x,y,n,fw,fh,step}]`。背景の直後・人物より奥に描く。NEARESTのまま）
- 回転台：左上(1204,596)＝足もと中心(1264,896)・4コマ・**1コマ0.5秒**。OPEN看板：(704,524)から128×48・2コマ・**1秒**。最終値は指示書の目安どおり。画素が strip のコマと一致することをテストで確認
- 動きの絵だけ読めないときは動きだけ消え、背景と人は出る。背景が読めないときは今までのドット描画（BGS）に落ちる（SIM・タクシー・部屋とも確認）

## タクシーの fx
**fx 無し**にした。新背景は昼の屋外（到着は朝）なので、旧設定の夜の星・ガラスのきらめきは合わない。

## 人の配置（足もとの中心 x, y）
- SIM：`t-safari-front`（218, 702）＝Telkom の前、`t-woman-hijab-front`（1430, 712）＝airtel の前。背景の床の楕円の位置。回転台（x1204–1324）・店員・ふたり・荷物と重ならない（矩形でテスト）
- タクシー：`t-backpacker-front`（1250, 890）、`t-man-thobe-front`（1450, 925）。歩道の右はし。係員（x=1060）・ふたり・荷物と重ならない
- 左はしに置かなかった理由：ふたりが左から歩いて入る動線と重なるため
- 動きは 037 の基準（`artPeople`/`artSway` そのまま）

## ホテルの部屋
- 場所 `hroom`「ホテルの部屋」、座標 **(48, 88)**（調整なし。地図のノードどうしが重ならないことを確認）、`v=[]`、`rest='nbo_room'`。到着の完了条件・場面の数（8のまま）・save.seen・「済」の印に入らない
- 開く条件：既存の「上から順に開く」を、tour 側だけ「場面の数が空の場所は数えない」に補正した（補正なしだと hsong が空のため hroom は永久に閉じたままになる）。タクシーを遊ぶと hsong と hroom が同時に開く
- 会話（読み上げ＋表示だけ・マイク/採点なし。入りの日本語は intro の1行のみ）：
  1. ルル：We made it. This is our room at the Villa Rosa Kempinski.
  2. キング：It is so quiet. Look at the moon.
  3. ルル：Nairobi is beautiful at night.
  4. キング：My blue suitcase is here. I am so tired.
  5. ルル：Rest well, King. Tomorrow is a new day.
  6. キング：Lala salama, Lulu.
- intro：「夜のホテルの部屋。長い一日がおわった。ふたりは、ほっと息をついた。」

## テスト結果
- 新規 `test_arrival051.py`：101 OK / 0 NG
- 既存：bag045・bag046・bundle033・chant050・doha023・hnd043・pa034・raw032・readback024・rest032・routes・settle032・song049（hroom 付きの並びに更新）・sparta032・ticket041・time032・train035・trip030_doha・trip030_ending は通過
- 通らないもの（**051と無関係。変更前の main でも同じ**）：`test_trip030.py`（古い画面要素 `curName` を探して落ちる。main でも同じ位置で落ちた）、`test_people047.py`（外部パック `/home/claude/t047` の配置プレビューが無く開始できない）

## ドーハ側
`doha_data.py`・ドーハの組み立て・ドーハの `artIdFor` は変更なし。ただし `art.js` は両ページに同じものが埋め込まれるため、`tour/doha/index.html` の中の art 設定の文字列（ナイロビ用の項目と汎用部品）は増えている。ドーハの場面の動きは変わらない（doha023・trip030_doha が通過）。

## 未確認（実機でしか分からない）
- スマホ実機での見え方（文字・足もと・人の大きさ）、実機の音・読み上げ
- 実機での回転台・OPEN看板の切り替えの滑らかさ
- 最終の見た目の好み（店員の人選は手持ちの素材から `w-front-man-suit-1`／`dashiki`。専用の絵が要るならPMに確認）
