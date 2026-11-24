# タスク072 完了報告：ロヴァニエミ第2弾（滞在＋出発）

結論：20場面（滞在8・夜2・出発10）を実装し、`test_rovaniemi072.py` は194項目すべてOK（NG 0）。村の広場・郵便局は実画＋動く別素材で接続済み、ほかの18場面はコード描画。実機（マイク・音・見え方）は未確認。

## 変更したファイル
- 新規：`tour-src/rvn_stay_data.py`（20場面の台詞）、`tour-src/tests/test_rovaniemi072.py`
- 新規素材（`tour/assets/art/`）：`rovaniemi-village-square-v1.png`・`rovaniemi-postoffice-v1.png`・`rovaniemi-village-smoke-strip.png`・`rovaniemi-village-sparkle-strip.png`・`rovaniemi-postoffice-flames-strip.png`（オーロラ strip は065のものを共用）
- 変更：`tour-src/data.py`（取り込み）、`tour-src/build.py`（場所 `RSTAY`/`RDEP`・話し手20人・背景 `BGS` 10個・`stay`/`dep` タブ・art id の振り分け・滞在タブの地図色）、`tour-src/trip.js`（旅程・GROUPS・PLACEGRP・MODEGRP・HOUR・THEME）、`tour-src/art.js`（`ART.rvillage`・`ART.rpostoffice`）
- 既存テストの期待値だけ更新：`test_arrival065.py`（到着の10本だけを対象に・「かいわ n / 30」・背景文字の許可に店名2つ）、`test_departure054.py`（ナイロビ出発の art 一覧から新しい2つを除外）
- 生成物（再生成）：`tour/rovaniemi/index.html`・`tour/index.html`・`tour/doha/index.html`・`tour/ending/index.html`・`world/index.html`

## 新しい art 設定
| art id | 背景 | ルル（後ろ姿） | キング（後ろ姿） | 話し相手（立つ） |
|---|---|---|---|---|
| `rvillage`（rvn_village1/2） | rovaniemi-village-square-v1.png | x=700, 足もと y=884 | x=836, y=884 | 案内の人 x=1010, y=890 / 村で働く人 x=1010, y=890 |
| `rpostoffice`（rvn_post1/2） | rovaniemi-postoffice-v1.png | x=660, y=884 | x=800, y=884 | 係員 x=980, y=890 / 旅行者 x=980, y=890 |

2人の足もとと横位置は同梱プレビューどおり（テストで画素比較）。話し相手は2人の右に立つ（プレビューには相手がいないため、065のロビーと同じ置き方。位置は私が決めた）。

## strip の最終的な切替間隔
- 村：オーロラ (80,16) 1.2秒／煙 (328,136) 0.8秒／雪のきらめき (168,660) 0.6秒（いずれも4コマ）
- 郵便局：暖炉の炎 (132,524) 0.35秒（4コマ）
- 位置は、背景に strip を重ねた画素と実画面の画素が一致することをテストで確認（半透明の縁の丸めはRGB合計12以内）。

## 滞在・出発タブの場所（地図座標 x,y と場所キー）
- 滞在タブ（`stay`）：`rvil` 村の広場 (24,14) → `rpost` 郵便局 (72,32) → `rsanta` サンタに会う (26,50) → `rrein` トナカイ (72,66) → `rhotel` ホテルの夜 (28,84)
- 出発タブ（`dep`）：`rchk` チェックイン (24,14) → `rsec` 保安検査 (72,32) → `rshop` ギフトショップ (26,50) → `rahk` Ahkio (72,66) → `rgate` ゲート (28,84)
- 座標は到着タブ（065）と同じジグザグ配置。タブごとの最小距離はテストで17以上を確認（重なりなし）。
- 鍵：滞在タブは順番なし（ナイロビの滞在と同じ。11日目に4場所とも開く）。ホテルは12日目から。出発タブは到着と同じく上から順に開く。

## 旅程
- oneworld：11日目 `rvn_stay`／12日目 `rvn_night`／13日目 `rvn_dep`
- Star：11日目 `rvn_stay`／12日目 `rvn_dep`。`rvn_night` はStarの旅程に入らず、チェックモードから入る。
- 世界マップのクリアの印は到着の場所だけで決まるまま（`PLACES_AIR=PLACES_RARR`、今回は変えていない）。

## rvn_reindeer の動物と置き方
- 動物：トナカイ（ハスキーは出していない）。
- 置き方：**静止**。別素材は無いため、`BGS.rrein`（コード描画の背景）の中に静止したドット絵のトナカイを描いた。動かない。実画に差し替えるときは、トナカイを別素材（strip／人物の置き方）に分けるのが望ましい（指示書「背景に描き込まない」には沿えていない）。

## rvn_hotel のオーロラ
- オーロラ strip は出していない。ホテルの窓の外は星と雪だけ。台詞でもオーロラは約束せず「Nobody can promise the lights」と言う（hotel1）。

## 既存の情報だけ使った確認（台詞）
使った実在情報は指示書の確認済みだけ：サンタに毎日会える・入場無料・Santa Claus Office／郵便局が公式・北極圏の特別な消印・クリスマスに届くよう預けられる・黄色いポスト／広場の北極圏ライン／Roosevelt Cottage（1950年築）・Mrs. Santa Claus Christmas Cottage（赤）／Napapiirin Lahja（保安検査の前と後）・Ahkio Kitchen and Bar（保安検査の後。クリーミーなサーモンスープ・トナカイバーガー）・新しい広い出発ホール。看板文言・料金・消印の図柄・航空会社・発着案内・行き先の都市名は出していない（出発の台詞は「南へ」「次の街へ」で、oneworld・Starどちらでも成り立つ）。背景の文字は `Napapiirin Lahja` と `Ahkio` だけを追加。

## テスト結果
- `test_rovaniemi072.py`：OK 194／NG 0（素材6・台本20本×6項目・実在情報・strip位置の画素一致・足もと y=884・BGSへのフォールバック・全場面が始まり会話が進む・旅程・鍵・タブ・チェックモード20本・他ページがエラーなく開く・新しい保存キーなし）
- 既存テスト40本（`tour-src/tests/test_*.py`）を全部流した結果：`test_trip030.py` 以外はすべて通過。`test_trip030.py` は、変更前（HEAD）を別フォルダに取り出して流しても同じ行（世界マップの `curName` を読む行）で同じ失敗をするため、072とは無関係の既存の失敗（私は直していない）。
- 期待値を直したのは3本だけ：065（到着の10本だけを対象・「かいわ n / 30」・背景文字の許可に店名2つ）、054（ナイロビ出発のART一覧から新しい2つを除外）、068（既存ARTの比較から新しい2つを除外）。いずれも「新しく足したもの」を数えから外しただけで、既存の中身の判定は変えていない。
- 途中、機械が重いと hnd043 が一度だけ `__T` 未定義で落ちたが、単独で流し直すと通過（タイミングによる）。

## 要確認・判断をPMにお願いしたい点
1. Star 11日目のキャプションが「Tonight we wait for the lights.」のまま、そこに滞在（rvn_stay）を載せた。キャプションが夜の話になっている。指示書どおり実装し、直していない。
2. 出発の台詞を行き先の名前を出さない形にした（oneworld=マドリード・Star=イスタンブール、同じ台詞で使うため）。券ごとに別台詞にするかはPM判断。
3. 店名のルール（実名）：ホテルのフロント・保安検査・ゲートは一般の施設名のみ。確認済みの店名は Napapiirin Lahja と Ahkio だけ使用。
4. 滞在・出発に「お金の1行」（MONEY）は足していない（台詞に値段が無いため）。
5. `rvn_post`・`rvn_santa` の場面のテーマ（切り替え時の絵）は既存の `hotel` を使用（専用が無いため）。
6. 世界マップのクリアの印（出発まで終えたら付ける等）は今回触っていない。

## 実機でしか分からない点
- マイクの聞き取り・発音の判定・実機での声と音（`rvn` の音は065のもの）・実機の画面での文字の見え方・各strip の滑らかさ（ヘッドレスでは画素の一致までしか見ていない）。

## 参考にしたURL
- 新しい外部URLは使っていない（指示書072の「確認済み情報」に従った。出典は指示書の `pm-kit/rovaniemi-prep.md`）。

## 新しく書いた会話文（全文）
各場面：相手の1言目と、ルル/キングの返事（`*` は発音を見る語）。分かれ目は、聞き取れた返事（ok）と聞き違えた返事、それぞれへの相手の返しを併記。画面に日本語訳は出ない（場面の説明文だけ日本語）。

### rvn_village1(村の案内の人)
場面の説明: サンタクロース村の広場。足もとに、細い光の線が通っている。
語: Arctic, line, step, tower, village
1. 相手: Good afternoon. Welcome to Santa Claus Village.
   ルル/キング: Good afternoon. Is this line the Arctic Circle?
2. 相手: Yes. At the airport, the light draws the line. Here it runs across the square, and you can step over it.
   - 返事(聞き取れた): Then we will step over it together. → 相手: Good. One step, and you are in the Arctic. Hold hands, if you like.
   - 返事(聞き違え): Stop? Must we stop at the line? → 相手: No, no. Not stop. Step. Lift your foot, and put it down on the other side.
   - 返事(聞き取れた): May I take a photo on the line? → 相手: Of course. Stand on the line, and ask a friend to take it.
3. 相手: How does it feel? Is it different from the airport?
   ルル/キング: It feels very open. The sky is big.
4. 相手: The sky is big, and the village is quiet. Do you see the tall building with the tower?
   - 返事(聞き取れた): Yes. The tall building with the tower. What is it? → 相手: That is the Santa Claus Office. You can meet Santa Claus there, every day.
   - 返事(聞き違え): A tour? Is it a bus tour? → 相手: Not tour. Tower. A tall, narrow part on top of a building. Look up.
   - 返事(聞き取れた): I see it. May we go and look? → 相手: Of course. It is by the square. You can go after the line.
5. 相手: That is the way. Enjoy the Arctic, and keep your hands warm.
   ルル/キング: Thank you. We will.

### rvn_village2(村で働く人)
場面の説明: 広場のベンチのそば。ここで働く人が、ふたりに声をかける。
語: old, cottage, red, mail, afternoon
1. 相手: Hello. You look a little lost. Can I help you?
   ルル/キング: Hello. Which building is the oldest one here?
2. 相手: That log house, Roosevelt Cottage. It was built in nineteen fifty. It is the oldest in the village.
   - 返事(聞き取れた): Nineteen fifty? That is very old. → 相手: For a village, yes. Those logs have seen many winters.
   - 返事(聞き違え): Cold? The cottage is cold? → 相手: No, no. Old. Not new. Many, many years.
   - 返事(聞き取れた): May I take a picture of it? → 相手: Yes. In the evening light, it looks warm and old.
3. 相手: And the red house over there is the Mrs. Santa Claus Christmas Cottage. Do you like red?
   ルル/キング: Yes, I do. Red looks warm in the snow.
4. 相手: It does. What do you want to do first?
   - 返事(聞き取れた): We want to mail a postcard. → 相手: Good. The post office is a log house, with a yellow post box by the door.
   - 返事(聞き違え): A nail? Do I need a nail? → 相手: No, no. Mail. A letter, or a postcard. You send it by post.
   - 返事(聞き取れた): First, we want to see Santa Claus. → 相手: Then go to the Santa Claus Office. You can meet him every day, and it is free.
5. 相手: Enjoy the village. It is a good place to slow down.
   ルル/キング: Thank you. Goodbye!

### rvn_post1(郵便局の係員)
場面の説明: サンタクロース村の郵便局。丸太の壁と暖炉。窓口の人が、まっすぐこちらを見ている。
語: postcard, postmark, message, Christmas, yellow
1. 相手: Good afternoon. Do you want to send a card?
   ルル/キング: Good afternoon. Yes. We want to send a postcard.
2. 相手: Good. This is Santa Claus' Main Post Office. It is the only official post office of Santa Claus. Who is the card for?
   - 返事(聞き取れた): It is a postcard for my friend at home. → 相手: A friend at home. Good. Write a short message. A short one is nice.
   - 返事(聞き違え): A car? I want to send a car? → 相手: No, no. A card. Postcard. Paper, with a picture on one side. You write on the other.
   - 返事(聞き取れた): It is a card for my family. → 相手: A family card. Good. Please write a short, warm message.
3. 相手: Please write it at the table. A short message is enough.
   ルル/キング: Thank you. I will write it now.
4. 相手: When you are ready, I can put a special postmark on it. It is an Arctic Circle postmark.
   - 返事(聞き取れた): Yes, please. I want the special postmark. → 相手: Good. One press, and it is yours. Very Arctic.
   - 返事(聞き違え): A mask? Do I wear a mask? → 相手: No, no. Postmark. A mark on the card, from the post office. It shows the place.
   - 返事(聞き取れた): Will my card arrive by Christmas? → 相手: You can leave it here, and it will be sent to arrive at Christmas. That is the idea.
5. 相手: Put the card in the box by the door, or leave it with me. Have a warm day.
   ルル/キング: Thank you. Goodbye!

### rvn_post2(手紙を書いている旅行者)
場面の説明: 郵便局のテーブル。手紙を書いている旅行者が、ペンを探している。
語: pen, letter, fire, thank, wish
1. 相手: Excuse me. Do you have a pen? Mine does not work.
   ルル/キング: Yes, I do. Here is a pen.
2. 相手: Thank you. I am writing a letter to Santa Claus. Is that silly?
   - 返事(聞き取れた): No, it is not silly. It is a lovely letter. → 相手: Thank you. I hope it arrives for Christmas.
   - 返事(聞き違え): The latter? What is the latter? → 相手: No, no. Letter. A paper message that you put in an envelope.
   - 返事(聞き取れた): I like writing letters, too. → 相手: Then we are the same. Letters are slow, but they are warm.
3. 相手: The fire is warm, and the room is quiet. It is a good place to write.
   ルル/キング: Yes. It feels like a cabin.
4. 相手: Do you know what to write? I want to say thank you for a good year.
   - 返事(聞き取れた): You can say thank you. That is a good start. → 相手: Yes. Thank you first. Then wishes.
   - 返事(聞き違え): Think? What do I need to think about? → 相手: Ha. Not think. Thank. Say thank you. Two words, and a warm heart.
   - 返事(聞き取れた): I will write a wish for next year. → 相手: A wish. Yes. Keep it small and kind. Those are the best ones.
5. 相手: Thank you for the pen. Now I can finish. Have a safe trip.
   ルル/キング: You are welcome. Good luck with your letter.

### rvn_santa1(サンタクロース)
場面の説明: サンタクロース・オフィス。あたたかい笑い声がして、サンタが顔を上げる。
語: office, free, Japan, health, safe
1. 相手: Ho ho ho. Come in, come in. Welcome to my office.
   ルル/キング: Hello, Santa. Thank you for meeting us.
2. 相手: I am here every day, and visitors come in for free. Where are you from?
   - 返事(聞き取れた): We come from Japan. It is far from here. → 相手: Japan! That is a long way. You must be tired, and happy to be here.
   - 返事(聞き違え): A pan? Do you cook here? → 相手: Ho ho ho. No pan. Japan. The country far in the east.
   - 返事(聞き取れた): We came from far away. It was a long trip. → 相手: Long trips make the best stories. Tell me one, one day.
3. 相手: And what are you doing on your trip? Are you going around the world?
   ルル/キング: Yes. We are going around the world.
4. 相手: Around the world! Then you need good luck. What do you wish for your trip?
   - 返事(聞き取れた): I wish for good health. → 相手: Good health. That is the best gift of all. I will remember it.
   - 返事(聞き違え): Help? I need help? → 相手: No, no. Health. Being well, and strong, and happy.
   - 返事(聞き取れた): We wish for a safe trip. → 相手: A safe trip. Yes. I will ask the reindeer to watch the sky for you.
5. 相手: Thank you for coming. Take good care, and keep your hearts warm. Ho ho ho.
   ルル/キング: Thank you, Santa. Merry Christmas!

### rvn_santa2(サンタクロース)
場面の説明: サンタクロース・オフィスの奥。いすのそばで、サンタが静かに待っている。
語: reindeer, moment, promise, lights, kind
1. 相手: Ho ho ho. Back again? Please sit down. The chair is warm.
   ルル/キング: Thank you, Santa. We want to ask you something.
2. 相手: Of course. Ask me anything. But it must be a kind question.
   - 返事(聞き取れた): Are your reindeer in the village? → 相手: They are close, and they love the snow. Go and say hello.
   - 返事(聞き違え): Rain? Does it rain here? → 相手: No, no. Reindeer. The animals with big antlers. They pull my sleigh.
   - 返事(聞き取れた): Do you ever get tired? → 相手: Sometimes. Then I sit by the fire, and I am better.
3. 相手: Now, my question. What was your best moment on this trip?
   ルル/キング: The best moment is now. We are talking to you!
4. 相手: Ha ha. Thank you. Tonight the sky may show you something. Nobody can promise it, not even me.
   - 返事(聞き取れた): We hope to see the northern lights tonight. → 相手: Hope, and look up. The sky decides.
   - 返事(聞き違え): Rights? Do I have rights? → 相手: No, no. Lights. The green lights in the sky. The northern lights.
   - 返事(聞き取れた): Can you promise us the lights? → 相手: No promise. The sky decides. But waiting is part of the fun.
5. 相手: Go well, my friends. And remember, kind words are the best gifts.
   ルル/キング: Thank you, Santa. Goodbye!

### rvn_reindeer1(トナカイの世話をする人)
場面の説明: 雪の道のわき。トナカイの世話をする人が、手綱を持って待っている。
語: reindeer, softly, antlers, sleigh, snow
1. 相手: Good afternoon. Would you like to meet the reindeer?
   ルル/キング: Good afternoon. Yes, please. We love animals.
2. 相手: Come this way, slowly. The reindeer are calm, but they do not like loud voices.
   - 返事(聞き取れた): We will walk slowly and talk softly. → 相手: Good. Then they will come close. They are curious.
   - 返事(聞き違え): A sofa? Do the reindeer sit on a sofa? → 相手: Ha. No sofa. Softly. Quietly, and gently, like a whisper.
   - 返事(聞き取れた): I will keep my voice quiet. → 相手: Perfect. Quiet voices, and slow hands.
3. 相手: This one is the oldest. She knows every path in the snow.
   ルル/キング: She has beautiful antlers.
4. 相手: In winter she pulls a sleigh through the snow. Have you ever seen a real sleigh?
   - 返事(聞き取れた): No, never. We only know it from pictures. → 相手: Then today is a good day. A real sleigh is quiet, and slow.
   - 返事(聞き違え): Sly? A sly reindeer? → 相手: Ha. No, no. Sleigh. A seat on runners, for the snow. Santa has one.
   - 返事(聞き取れた): Can we ride in the sleigh? → 相手: Please ask about the sleigh ride. I only look after the reindeer.
5. 相手: Thank you for being so quiet. The reindeer like you. Take a photo, and go slowly.
   ルル/キング: Thank you. Goodbye, reindeer!

### rvn_reindeer2(親子連れの旅行者)
場面の説明: 柵のそば。親子連れの旅行者が、トナカイをじっと見ている。
語: kind, nose, cold, tonight, sky
1. 相手: Hello! Look, that reindeer is looking at us. My daughter loves it.
   ルル/キング: Hello! It has big, kind eyes.
2. 相手: Yes! It is getting dark. Are you cold? My daughter says her nose is red.
   - 返事(聞き取れた): Mine is red, too. It is very cold. → 相手: Ha ha. Then we are the same. A warm hat helps.
   - 返事(聞き違え): Knows? What does it know? → 相手: No, no. Nose. The part of your face under your eyes.
   - 返事(聞き取れた): I am a little cold, but happy. → 相手: Me too. Cold, and happy. That is Lapland.
3. 相手: We came to see the northern lights, but the reindeer came first.
   ルル/キング: That is a good start to the trip.
4. 相手: Are you staying in the village tonight? We want to wait for the lights at our hotel.
   - 返事(聞き取れた): Yes. We will go to the hotel tonight. → 相手: Then we may look up at the same sky. That is nice.
   - 返事(聞き違え): Tonic? We drink tonic tonight? → 相手: No, no. Tonight. This evening, after today.
   - 返事(聞き取れた): We will wait for the lights, too. → 相手: Good. Wear everything you have, and wait.
5. 相手: Good luck with the sky. My daughter says goodbye to you, too.
   ルル/キング: Goodbye! Say hello to the reindeer for us.

### rvn_hotel1(ホテルのフロントの人)
場面の説明: ホテルのロビー。窓の外は、星の見える夜。フロントの人が、静かにこちらを見ている。
語: clear, window, sky, luck, night
1. 相手: Good evening. Did you have a good day?
   ルル/キング: Good evening. Yes. We met Santa Claus!
2. 相手: A lucky day. Tonight is for the sky. Do you want to see the northern lights?
   - 返事(聞き取れた): Is the sky clear tonight? → 相手: Very clear now. But clouds can come from nowhere. That is Lapland.
   - 返事(聞き違え): Clean? The sky is clean? → 相手: Ha. No, no. Clear. Not cloudy. You can see far, and see the stars.
   - 返事(聞き取れた): Where is the best place to look? → 相手: Outside, away from the lamps. And wear everything you have.
3. 相手: Nobody can promise the lights. But the night is long. Please stay warm.
   ルル/キング: We have hats and gloves. We are ready.
4. 相手: If you want to wait inside, there are chairs by the window. Waiting is part of the night.
   - 返事(聞き取れた): We will wait by the window. It is warm there. → 相手: A good choice. Warm feet, and a big sky.
   - 返事(聞き違え): A winner? Who is the winner? → 相手: Ha ha. No, no. Window. The glass in the wall, where you can look out.
   - 返事(聞き取れた): Can I wait outside for a little while? → 相手: Yes. But not too long. Come in when your toes hurt.
5. 相手: Good night. And good luck with the sky.
   ルル/キング: Thank you. Good night!

### rvn_hotel2(夜のロビーの旅行者)
場面の説明: ロビーの窓ぎわ。毛布を肩にかけた旅行者が、小さな声で話しかけてくる。
語: stars, patient, blanket, deal, together
1. 相手: Shh. Hello. Sorry. I am only watching the sky.
   ルル/キング: Hello. Is anything out there?
2. 相手: Not yet. I have waited for a long time, but the sky is only stars.
   - 返事(聞き取れた): Stars are beautiful, too. → 相手: Yes. That is true. In my city, I never see so many.
   - 返事(聞き違え): Stairs? Where are the stairs? → 相手: No, no. Stars. The small lights in the sky, far away.
   - 返事(聞き取れた): We can be patient. We have time. → 相手: Patient. Yes. That is the secret. And a warm blanket.
3. 相手: Some people see the lights on the first night. Some never see them. It is luck.
   ルル/キング: We know. We hope for a little luck.
4. 相手: Would you like a blanket? There is a basket by the window.
   - 返事(聞き取れた): Yes, please. A blanket is a good idea. → 相手: Take one. Cold fingers cannot hold a camera.
   - 返事(聞き違え): A blank? Is the paper blank? → 相手: No, no. A blanket. A soft, warm cover for your shoulders.
   - 返事(聞き取れた): I will wait with my hat and gloves. → 相手: Good. Hat, gloves, and patience. That is all you need.
5. 相手: If you see a green light, call me. I will call you, too. Deal?
   ルル/キング: Deal! We will look up together.

### rvn_checkin1(チェックインの係員)
場面の説明: ロヴァニエミ空港の出発ホール。広くて新しいホールの、チェックインカウンター。
語: south, passport, suitcase, glass, flight
1. 相手: Good afternoon. Welcome to the departure hall. It is new, so everything is easy to find.
   ルル/キング: Good afternoon. We would like to check in, please.
2. 相手: Of course. Passports, please. Are you flying south today?
   - 返事(聞き取れた): Yes. We are flying south today. → 相手: South. Good. It will be warmer there.
   - 返事(聞き違え): Mouth? We fly to a mouth? → 相手: No, no. South. The opposite of north. Warm places are in the south.
   - 返事(聞き取れた): Here are our passports. Thank you. → 相手: Thank you. Please wait one moment while I look.
3. 相手: Do you have a bag to check in? Please put it on the belt.
   ルル/キング: Yes. One big blue suitcase.
4. 相手: Thank you. Is there anything fragile in the bag? Anything made of glass?
   - 返事(聞き取れた): No glass. Only clothes and a hat. → 相手: Good. Clothes are the best travelers.
   - 返事(聞き違え): Grass? We have no grass. → 相手: Ha. No, no. Glass. A hard, clear material. A cup is made of glass.
   - 返事(聞き取れた): Only a small gift from the village. → 相手: A gift. Lovely. Keep it in your hand bag, to be safe.
5. 相手: Here are your boarding passes. Please go to security. Have a good flight.
   ルル/キング: Thank you. Goodbye!

### rvn_checkin2(となりのカウンターの係員)
場面の説明: となりのカウンター。落ち着いた声の係員が、ゆっくり話す。
語: aisle, window, backpack, boarding, travel
1. 相手: Hello. Next, please. Where are you traveling today?
   ルル/キング: Hello. We are traveling south, to our next city.
2. 相手: I see. Do you want a window seat, or an aisle seat?
   - 返事(聞き取れた): An aisle seat, please. I like to walk. → 相手: An aisle seat. Good. It is easy to stand up.
   - 返事(聞き違え): Ill? Is the seat ill? → 相手: Ha. No, no. Aisle. The walkway between the seats.
   - 返事(聞き取れた): A window seat, please. I like to look outside. → 相手: A window seat. Good. You can look at the snow from above.
3. 相手: Is this your only bag? Do you have any hand luggage?
   ルル/キング: Yes. Only a small backpack.
4. 相手: Please keep your passport and your boarding pass together. You need them at security.
   - 返事(聞き取れた): Yes. I will keep them together. → 相手: Good. A boarding pass is easy to lose, and hard to replace.
   - 返事(聞き違え): Boring? Is the pass boring? → 相手: Ha. No, no. Boarding. The paper, or phone, that lets you get on the plane.
   - 返事(聞き取れた): Can I keep my boarding pass on my phone? → 相手: Yes, if you like. Keep the screen bright.
5. 相手: That is all. Safe travels, and come back to Lapland again.
   ルル/キング: Thank you. We will!

### rvn_sec1(保安検査の係員)
場面の説明: 保安検査場。係員が、トレイを指さしている。
語: tray, jacket, laptop, bottle, gate
1. 相手: Good afternoon. Please put your jacket and your bag in a tray.
   ルル/キング: Good afternoon. Should I take my jacket off?
2. 相手: Yes, your jacket, and anything in your pockets. Do you have a laptop or a tablet?
   - 返事(聞き取れた): Yes. I have a laptop in my bag. → 相手: Please take it out, and put it in a tray by itself.
   - 返事(聞き違え): A lap? Do I put it on my lap? → 相手: Ha. No, no. Laptop. The small computer that you open and close.
   - 返事(聞き取れた): No. Only my phone. → 相手: Good. The phone goes in the tray, too.
3. 相手: Please walk through the gate, one at a time.
   ルル/キング: Thank you. I am going through now.
4. 相手: Wait, please. Do you have any liquids in your bag, like water?
   - 返事(聞き取れた): Yes. I have a small bottle of water. → 相手: Please put it in the tray, too. We need to look at it.
   - 返事(聞き違え): A battle? There is no battle. → 相手: Ha. No, no. Bottle. A container for water. Is there a bottle in your bag?
   - 返事(聞き取れた): No liquids. I drank my water. → 相手: Good. That makes it easy.
5. 相手: All clear. Please take your things from the tray. Have a good flight.
   ルル/キング: Thank you. Goodbye!

### rvn_sec2(保安検査の係員)
場面の説明: 荷物がベルトを通っていく。係員が、画面をじっと見ている。
語: globe, tray, metal, belt, safe
1. 相手: Excuse me. Is this your bag? The screen shows something round.
   ルル/キング: Yes, it is my bag. What is it?
2. 相手: I think it is a snow globe. Is it a gift?
   - 返事(聞き取れた): Yes. It is a gift from the village. → 相手: Pretty. Please hold it in your hand when you go through.
   - 返事(聞き違え): A glove? No, it is not a glove. → 相手: Ha. No, no. Globe. A round ball, made of glass, with snow inside.
   - 返事(聞き取れた): Yes. It is for my family at home. → 相手: A good gift. Wrap it well, so that it does not break.
3. 相手: Thank you. Please put it in a tray, and put the tray on the belt.
   ルル/キング: Like this? Is this right?
4. 相手: Yes, that is right. Now, your belt. Is there metal in it?
   - 返事(聞き取れた): Yes. My belt has metal. I will take it off. → 相手: Thank you. Put it in the tray, with the jacket.
   - 返事(聞き違え): A medal? I did not win a medal. → 相手: Ha. No, no. Metal. Hard and shiny, like iron or steel.
   - 返事(聞き取れた): No metal. It is a soft belt. → 相手: Good. Then walk through, slowly.
5. 相手: All good. Your snow globe is safe. Have a lovely trip.
   ルル/キング: Thank you. You are kind.

### rvn_shop1(ギフトショップの店員)
場面の説明: ギフトショップ Napapiirin Lahja。ラップランドの小さな贈りものが、棚にならんでいる。
語: gift, small, wooden, counter, shop
1. 相手: Welcome to Napapiirin Lahja. Are you looking for a gift?
   ルル/キング: Hello. Yes. We want a small gift for home.
2. 相手: Then you are in the right place. We have a shop before security, and one here, after security.
   - 返事(聞き取れた): Yes. Something small and light, please. → 相手: Light is good. A small gift is easy to carry.
   - 返事(聞き違え): Smell? Is the gift something to smell? → 相手: No, no. Small. Not big. Easy to hold in one hand.
   - 返事(聞き取れた): Something with a reindeer on it. → 相手: A reindeer. Good choice. Look on the shelf by the window.
3. 相手: Take your time. Look around.
   ルル/キング: Thank you. This one is nice. What is it?
4. 相手: It is a little wooden reindeer. Do you want to hold it?
   - 返事(聞き取れた): Yes, it is cute. Is it made of wood? → 相手: Yes, it is wooden. Light, and warm in the hand.
   - 返事(聞き違え): Would not? It would not stand? → 相手: No, no. Wooden. Made of wood, from a tree.
   - 返事(聞き取れた): May I hold it? It looks very small. → 相手: Please. It is light. Be careful, it is a little shy.
5. 相手: A good choice. Please bring it to the counter. I will put it in a bag.
   ルル/キング: Thank you. We will take it.

### rvn_shop2(ギフトショップの店員)
場面の説明: ギフトショップのレジのそば。落ち着いた声の店員が、棚をなおしている。
語: cards, lovely, last, bag, summer
1. 相手: Hello. Do you need help, or are you only looking?
   ルル/キング: We are only looking. It is a lovely shop.
2. 相手: Thank you. Look at the pretty cards on the stand. They show the northern lights.
   - 返事(聞き取れた): I like the cards. Which one is your favorite? → 相手: This one, with the green sky and the black trees. It feels like home.
   - 返事(聞き違え): Cars? Are there cars on the cards? → 相手: Ha. No, no. Cards. Small, flat paper, with a picture on one side.
   - 返事(聞き取れた): I will send a card to a friend. → 相手: A friend will be glad. A real card is rare today.
3. 相手: Do you want a bag for your things?
   ルル/キング: Yes, please. A small bag is fine.
4. 相手: Here you are. You are lucky. It is the last one of this kind.
   - 返事(聞き取れた): Really? The last one? Thank you! → 相手: Really. It was waiting for you.
   - 返事(聞き違え): Lost? Did you lose the others? → 相手: Ha. No, no. Last. Not first. There are no more behind it.
   - 返事(聞き取れた): I will keep it safe on the plane. → 相手: Good. Keep it flat, and it will stay pretty.
5. 相手: Safe travels. Come back to Lapland in the summer, too.
   ルル/キング: Thank you. We would love to.

### rvn_ahkio1(レストランの店員)
場面の説明: 保安検査の先のレストラン、Ahkio Kitchen and Bar。クリーミーなサーモンスープの、いい香りがする。
語: table, soup, salmon, bread, creamy
1. 相手: Welcome to Ahkio Kitchen and Bar. A table for two?
   ルル/キング: Yes, please. A table for two.
2. 相手: Please sit anywhere. Our famous dish is the creamy salmon soup. Would you like to try it?
   - 返事(聞き取れた): Yes, please. We will have the salmon soup. → 相手: Good choice. It is creamy and warm, perfect for a cold day.
   - 返事(聞き違え): Soap? We do not eat soap! → 相手: Ha ha. No, no. Soup. Hot, in a bowl, with a spoon.
   - 返事(聞き取れた): What is in the soup? → 相手: Salmon, and a creamy soup. Simple, and very good.
3. 相手: And to drink? Water, or something warm?
   ルル/キング: Water, please. Thank you.
4. 相手: The soup will come soon. Would you like bread with it?
   - 返事(聞き取れた): Yes. Bread with the soup, please. → 相手: Good. It is the best way. Bread, and soup.
   - 返事(聞き違え): Bed? Do we sleep here? → 相手: Ha. No, no. Bread. Soft food, made from flour. You eat it with soup.
   - 返事(聞き取れた): No, thank you. Only the soup. → 相手: Understood. Only the soup. A good, simple lunch.
5. 相手: Enjoy your meal. Take your time, but watch the clock.
   ルル/キング: Thank you. It smells wonderful.

### rvn_ahkio2(となりの席の旅行者)
場面の説明: となりの席の旅行者が、ハンバーガーを食べながら、こちらを見ている。
語: reindeer, burger, meat, fly, waiter
1. 相手: Excuse me. Are you going to order? Try the reindeer burger. It is the local favorite.
   ルル/キング: A reindeer burger? That is a surprise!
2. 相手: I was surprised, too, but it is really good. Do you eat meat?
   - 返事(聞き取れた): Yes, I eat meat. I will try it. → 相手: Good. Hold it with both hands. It is big.
   - 返事(聞き違え): Meet? I meet the burger? → 相手: Ha ha. No, no. Meat. The food from an animal. Meat, not meet.
   - 返事(聞き取れた): I am not sure. Is it strong? → 相手: It has a strong taste, but a kind one. Try a small bite.
3. 相手: Please call the waiter. He is very kind.
   ルル/キング: Thank you for the tip.
4. 相手: Are you flying today? I am staying one more night. I still want to see the northern lights.
   - 返事(聞き取れた): We are flying today. Lapland was wonderful. → 相手: Then you saw a lot. I hope the lights come to you, wherever you go.
   - 返事(聞き違え): Fry? We fry something today? → 相手: Ha. No, no. Fly. Go by plane, through the sky.
   - 返事(聞き取れた): We saw so much. We saw Santa Claus! → 相手: You did! Then your trip is already a success.
5. 相手: Enjoy the burger. And have a safe flight.
   ルル/キング: Thank you. Enjoy your stay in Lapland!

### rvn_gate1(ゲートの係員)
場面の説明: 出発ゲート。大きな窓の向こうは、雪と夜のはじまりの空。係員がゆっくり話しかけてくる。
語: gate, board, village, quiet, memory
1. 相手: Good afternoon. This is your gate. Boarding will start soon.
   ルル/キング: Good afternoon. Thank you. Is the flight on time?
2. 相手: Yes, so far. Please sit near the gate. We will call you when it is time.
   - 返事(聞き取れた): Thank you. We will be ready to board. → 相手: Good. Have your boarding pass ready.
   - 返事(聞き違え): Bored? I am not bored. → 相手: Ha. No, no. Board. To get on the plane.
   - 返事(聞き取れた): We will sit by the window and wait. → 相手: Good. You can see the snow outside.
3. 相手: Is this your first time in Finland?
   ルル/キング: Yes. It is our first time, and we loved it.
4. 相手: I am glad. What was your best memory of Lapland?
   - 返事(聞き取れた): I loved the village, and the quiet. → 相手: Quiet is something we have a lot of. Take it with you.
   - 返事(聞き違え): Vintage? A vintage car? → 相手: No, no. Village. A small town, with houses and a square.
   - 返事(聞き取れた): I loved waiting for the sky. → 相手: That is Lapland. Waiting, and hoping.
5. 相手: Please come back soon. Good luck with your trip.
   ルル/キング: Thank you. We will.

### rvn_gate2(ゲートの係員)
場面の説明: アナウンスが鳴った。ゲートの係員が、搭乗券を受け取っている。
語: passport, boarding, green, lucky, north
1. 相手: Good afternoon. Boarding is open. Boarding pass, please.
   ルル/キング: Good afternoon. Here is my boarding pass.
2. 相手: Thank you. And your passport, please. Just a quick look.
   - 返事(聞き取れた): Of course. Here is my passport. → 相手: Good. Quick and easy.
   - 返事(聞き違え): A pass port? Is it a port? → 相手: Ha. No, no. Passport. The little book with your photo.
   - 返事(聞き取れた): Is my seat by the window? → 相手: Yes. Look outside when we take off. The north is white, and beautiful.
3. 相手: You are all set. Please walk through the door, and follow the people to the plane.
   ルル/キング: Thank you. We will.
4. 相手: One more thing. Did you see the northern lights?
   - 返事(聞き取れた): We saw something green. We are so lucky! → 相手: Then you are very lucky. Not everyone sees them.
   - 返事(聞き違え): A grin? Is it a smile? → 相手: Ha. No, no. Green. The color of leaves, and of the lights.
   - 返事(聞き取れた): No. But we are happy anyway. → 相手: That is a good answer. Come back, and look again.
5. 相手: Safe flight! And remember, the north will wait for you.
   ルル/キング: Thank you. Goodbye, Lapland!

