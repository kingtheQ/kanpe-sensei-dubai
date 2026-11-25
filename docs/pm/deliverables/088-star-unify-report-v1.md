# タスク088 報告：券をスターに統一＋窓口でルールを教える場面（v1・2026-11-25）

## 結論
- 1周目の発券はスターだけ。窓口の分岐（win_c1〜c8）はそのまま残し、おすすめ（win_rec）はどの分岐でもスター。価格・読み上げ・発券は win_price_star／win_rb_star／ticket_star だけ。
- ow4／ow5・ticket_ow の場面データは残した（窓口の流れ・チケットの場所の場面一覧から到達できないだけ。窓口の古いセーブに pick:'ow' があっても無視してスターにする）。
- ルール説明 `win_rules`（5つの決まり）と、ルートを一緒に数える `win_count` を、おすすめのあと・値段の前に足した。

## 流れ
`win_decl → win_c1 → win_c2 → win_c5 → win_c7 → win_c8 → win_route → win_rec(いつもスター) → win_rules → win_count → win_price_star → win_rb_star → win_name → ticket_star`

## おすすめ（win_rec）の台詞
係員は、印の多さに応じて次のどれかを言い、最後は同じ2往復で締める（選択肢の▶はなくした）。
- 印がない：You are still deciding, so I recommend Star Alliance. The rules are simple, and it has the most routes.
- スター寄り：Let me look at your answers. （スターの理由1〜2文）So I recommend Star Alliance.
- 同数・oneworld寄り：Let me look at your answers. （oneworldの理由1文）oneworld is a good ticket for another trip. But your route goes one way, around the world, and home. Star Alliance fits your route best, and its rules are simple.
- 共通の締め：キング「Thank you. That makes sense.」→ 係員「Shall I prepare the Star Alliance ticket for you?」（スターアライアンスの券を用意しましょうか。）→ キング「Yes, please. I'll take Star Alliance.」（はい、お願いします。スターアライアンスにします。）

## 台詞全文（係員＝NPC／キング＝プレイヤー。英語＋Meaning!。数字は window_data.py の ROUTE_STOPS／ROUTE_RAIL から計算）

### win_rules：スターの決まり

1. 係員：Star Alliance has five simple rules. Rule one: you go the same way, and you come home to the country where you started.
   （Meaning! スターアライアンスの決まりは5つ。1つ目：同じ向きに進んで、出発した国に帰ってきます。）
   キング：The same way, and home to Japan.
   （Meaning! 同じ向きに進んで、日本に帰ります。）

2. 係員：Rule two: you can stop in fifteen places at most. A stop is a stay of twenty-four hours or more.
   （Meaning! 2つ目：寄港は15回まで。寄港とは、24時間以上の滞在です。）
   キング：Fifteen stops at most.
   （Meaning! 寄港は15回までですね。）

3. 係員：Rule three: you can make sixteen moves at most. A flight is one move. A train ride is one move too.
   （Meaning! 3つ目：移動は16回まで。飛行機で1回。鉄道に乗るのも1回です。）
   キング：Sixteen moves. Trains count too.
   （Meaning! 移動は16回まで。鉄道も数えるのですね。）

4. 係員：Rule four: you can visit the same country three times at most.
   （Meaning! 4つ目：同じ国には3回まで寄れます。）
   キング：Three times for one country.
   （Meaning! 1つの国に3回まで。）

5. 係員：Rule five: the trip is ten days at least, and one year at most. Your trip is thirty days.
   （Meaning! 5つ目：旅の長さは10日から1年まで。あなたの旅は30日です。）
   キング：Thirty days. That is fine.
   （Meaning! 30日。大丈夫ですね。）

### win_count：ルートを一緒に数える

1. 係員：Let's check your route together. First, the stops. Nairobi, Doha, Rovaniemi, Athens, Rome.
   （Meaning! あなたのルートをいっしょに確かめましょう。まず寄港地。ナイロビ、ドーハ、ロヴァニエミ、アテネ、ローマ。）
   キング：That is five stops.
   （Meaning! 5か所です。）

2. 係員：Zurich, Frankfurt, London, Lisbon, New York.
   （Meaning! チューリッヒ、フランクフルト、ロンドン、リスボン、ニューヨーク。）
   キング：Five more. Ten stops.
   （Meaning! あと5か所。10か所です。）

3. 係員：Honolulu, Sydney, Singapore, Bangkok, Guam.
   （Meaning! ホノルル、シドニー、シンガポール、バンコク、グアム。）
   キング：Five more. Fifteen stops!
   （Meaning! あと5か所。15か所！）

4. 係員：Fifteen. That is the limit, and you are right on it. Now the moves. You have thirteen flights, and three train rides: Rome to Zurich, Zurich to Frankfurt, and Frankfurt to London.
   （Meaning! 15回。ちょうど上限ですね。次は移動。飛行機が13回、鉄道が3回：ローマからチューリッヒ、チューリッヒからフランクフルト、フランクフルトからロンドン。）
   キング：Thirteen flights and three trains. Sixteen moves.
   （Meaning! 飛行機13回と鉄道3回。移動は16回です。）

5. 係員：Sixteen. Right on the limit again. Now the countries. You visit the United States three times: New York, Honolulu, and Guam.
   （Meaning! 16回。これもちょうど上限。次は国。アメリカには3回寄ります。ニューヨーク、ホノルル、グアム。）
   キング：Three times. That is the limit, too.
   （Meaning! 3回。それも上限ですね。）

6. 係員：Last, your trip goes west, one way, and home to Japan. It is thirty days. Everything fits the rules. It is a good route!
   （Meaning! 最後に。旅は西へ、一方向に進んで、日本に帰ります。期間は30日。すべて決まりに合っています。いいルートです。）
   キング：Everything fits. Thank you!
   （Meaning! すべて合っています。ありがとう。）

## 数えた数字（決まりとの照合）
| 項目 | ルート | 決まり |
|---|---|---|
| 寄港（24時間以上） | 15 | 2〜15 |
| 移動 | 16（飛行機13＋鉄道3） | 16まで（陸路は5区間まで → 3） |
| 同じ国 | 最大3（アメリカ：ニューヨーク・ホノルル・グアム） | 3回まで |
| 旅の長さ | 30日 | 10日〜1年 |

## 要確認（PMへ）
- 台詞で数えたルート（PM指示書の1周目ルート）は、リポジトリの既存データと食い違っている：`trip.js` の `LEGS.star`／`ROWS.star`（羽田→イスタンブール→ナイロビ→アディスアベバ→…→クスコ→ヒューストン→ホノルル→グアム→成田）と、窓口の「線を引く地図」`win_route`（ケニア・フィンランド・ペルー・ハワイの4つの夢）。指示書どおり「ルートの変更」はしていない。窓口では、決まりの数えは指示書のルートで行い、「線を引く」の直後ではなく、おすすめのあとに置いた。ルートのデータ（trip.js・地図）をどちらに合わせるかはPM決定が必要。
- スターの陸路は公式で5区間までだが、台詞では「移動16回に数える」だけにした（指示書どおり）。
- 数え方の「出発国に戻る」に、グアム（米国領）→羽田の帰りを含めている。

## 確認
- `python3 tour-src/tests/test_star088.py`（新規）：窓口を先頭／最後／古いセーブが ow／大陸4つ、の4とおりで最後まで遊び、すべて ticket=star・価格/読み上げ/発券はスター版だけ・ルール→数える→値段の順。
- `test_ticket041.py` に win_rules／win_count を足した。`test_gasshuku078.py` の「変更前と同じ」の除外リストに新場面2つを足した。
- 未確認：実機のマイク・声・見え方（ヘッドレスのみ）。
