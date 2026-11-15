# 冒頭（賢者＋窓口）の体験設計と会話の下書き — 設計案 v1

作成：2026-11-15（Fable）。依頼：Fable依頼文1（docs/pm/tasks/003）。
位置づけ：**設計案であり、決定ではない。** 画面・流れを変える所は、作る前にキングの確認が要る。
読んだもの：CLAUDE.md、docs/rules.md、docs/handover.md、docs/pm/DECISIONS.md、docs/pm/design-bible.md、docs/pm/tasks/002・003・004、docs/materials/event-materials.md（1〜245行：行ける空港の表、賢者のアドバイス集81件、3つの券の比較、判断表、賢者が最初に聞く質問）、docs/world-tour-design.md、tour-src/data.py（sage_1/2/3、ticket_star、ticket_ow）、tour-src/build.py（賢者・窓口の置き方）。確認したコミット：12865e2。

---

## 0. 結論（先に）

冒頭を「質問に答える場面」から、**「白い地図に、自分の線が引かれて、止められて、100万円を自分の声で言う」体験**に変える案です。記憶に残す山は3つ。

1. **白い地図とピン**（賢者）：行きたい場所を、順番より先に全部地図に置く。
2. **止まる線**（窓口）：係員が線を引くと、決まりに合わない所で線が止まる。決まりは説明ではなく「止められた経験」で入る。
3. **値段を自分の声で言う**（購入）：「One million, seventy-four thousand, three hundred yen.」広告のキャッチ「100万円の世界一周航空券、まずゲームで買ってみた。」が、そのままゲームの中の出来事になる。

聞き取りは、判断表の12種類を**10本の会話**にしました（12種類すべてを含む）。各会話に「分かれ目」があり（10本で11か所）、キングが英語の短文を▶で選んで発音します。選んだ答えが券の「印」になります。

1周目の目的地（ナイロビ、ロヴァニエミ、クスコとマチュピチュ、ホノルル）で聞き取ると、**希望が2つの券に割れます**。大陸が5つ→oneworld Explorer（1,074,300円）、南米が主役→スター（958,900円）。差は115,400円。この「割れる」ことを冒頭の一番の見せ場にして、最後はキングが自分で決めます。どちらを先に作るかは未決定なので、この案はどちらでも成り立つ形にしてあります。

---

## 1. 成果物1：冒頭フロー設計

| # | 場面 | 目的 | プレイヤーの気持ちの動き | 記憶に残るもの | いまあるもの／新しく要るもの |
|---|---|---|---|---|---|
| 1 | 入口（羽田の搭乗ゲートで西の？？を選ぶ） | 「行き先の分からない旅」に踏み出す | 何が起きるのか分からない期待 | ？？の行き先 | 決定済みの入口（案1）。追加なし |
| 2 | 賢者の広間：立場を渡す | 自分の立場を知る（1枚の券・同じ向き・戻れない・約1か月） | 「すごい」→「重い。ちゃんと選ばないと」 | 賢者の一言「戻れない。だから先に、夢を全部地図に置きなさい」 | sage_1〜3 はある。足す台詞は第3章 |
| 3 | 賢者の広間：白い地図とピン | 行きたい場所を「必ず」「できれば」に分けて置く（助言29） | 自分の旅になる。指で置いた場所に愛着がわく | 白い地図に刺さった自分のピン | 新しい見た目（▶で複数を選ぶ）。設計図の窓口①を賢者側に寄せる案。**PM確認1** |
| 4 | 賢者の送り出し | 「ここから先は自分の声で」と手を離す。聞き返しの言い方を持たせる（sage_3） | 心細さと、やる気 | 「Could you say that again, please?」が命綱になること | sage_3 はある |
| 5 | 窓口：夢を言う | 係員の「Tell me about your trip.」に、まとまった文で答える | 声に出したら、本当に行く気になる | 自分の声で言った4つの場所 | 新しい会話1本。依頼文2（発音の把握）の埋め込み場所の候補。**PM確認2** |
| 6 | 窓口：聞き取り | 「旅のしかた」で券が決まることを、質問に答えながら知る | 「そんな決まりがあるのか」の小さな驚きが続く | 数えた大陸の数（One, two, three, four, five） | 新しい会話10本（第2章）。1回に出す本数は**PM確認3** |
| 7 | 窓口：線を引く | 係員が地図に線を引く。決まりに合わない所で止まる | ドキッとする → 納得 | 止まった線と、係員の「You cannot go back.」 | 新しい見た目（線を引く地図）。設計図の窓口③ |
| 8 | 窓口：おすすめ | 印の多い券と理由を聞く。割れたらキングが決める | 迷う → 自分で決めた手ごたえ | 「Your dreams point to two tickets.」 | 新しい会話1本。券を選ぶのは今ある▶ |
| 9 | 窓口：値段 | 値段を聞き、自分の声で言い直す。燃油と税は別と知る | 息をのむ → 覚悟 | 100万円を言った自分の声。ルルの記録帳の最初の1行 | 新しい会話1本。記録帳は未作成（設計図「決めること5」） |
| 10 | 窓口：名前の確認と搭乗券 | パスポートと名前が1文字でも違うと乗れない（助言45）。搭乗券を受け取る | 緊張 → ほっとする → うれしい | 搭乗券が出る音 | ticket_star / ticket_ow はある（搭乗券の会話）。名前確認は1往復の追加 |
| 11 | 出発（羽田→機内） | 買った券で本当に飛ぶ。賢者はもう出ない | 「始まった」 | 最初の区間の機内と、行き先がナイロビだと分かる瞬間 | 羽田の出発・飛行の画面は未作成（できていない流れ4・5） |

**流れ全体の考え方**

- 賢者は「何を大事にするか」を渡し、窓口は「どう決まるか」を体で分からせる。賢者が言った助言は、窓口で係員の口から形を変えて戻ってくる（会話6の2往復目など）。同じことを2回説明せず、物語の中で2度出会う。
- 賢者の助言は、旅の途中の出来事としても戻す（例：乗らない便は先に連絡＝助言37、出発前に時刻を確かめる＝助言53）。賢者本人は出さない。「あの時言われたやつだ」とだけ感じる形。
- 冒頭は長くしすぎない。賢者と窓口を全部話すと会話15本を超えるので、1回に通る本数をしぼる案を**PM確認3**に書いた。

---

## 2. 成果物2：窓口の聞き取り会話の下書き（10本）

### 2-1. 共通の前提

- 相手：世界一周の窓口の係員（どちらの連合の券も扱う。今ある窓口の看板は「ROUND THE WORLD」）。口調は落ち着いていて、急がせない。
- キングの地図には、ナイロビ・ロヴァニエミ・クスコとマチュピチュ・ホノルルが置いてある。
- 型：5往復。左が係員、右がキング（カンペ）。日本語は data.py の型に合わせた意味の控えで、画面に出すかどうかは今の設定に従う。強調の＊印は入れていない（組みこむときに付ける）。
- **分かれ目**：各会話に1か所（会話4だけ2か所）、キングが▶で英語の短文を選んで発音する。選択画面は英文だけ。会話の途中に▶を出すのは新しい形なので**PM確認4**。
- 5往復目が分かれ目の会話は、係員の返事を「おすすめ」の場面で受ける。
- 数字と決まりは event-materials.md の記載だけを使った。確認レベルはすべてB（専門の旅行会社の説明、確認日2026-11-12）。画面に出す前に公式で確かめ直す（素材集の注意どおり）。
- 「東京へ行く」という台詞は入れていない。

### 2-2. 12種類と会話の対応

| 判断表の「こうしたい」 | 会話 | 印がつく答え | 合う券 | 理由（素材集の出典） |
|---|---|---|---|---|
| 迷っている。人気の街をひととおり | 会話1 | 2往復目A | スター | 決まりが簡単で、路線がいちばん多い（早見表、助言56） |
| 大陸を4つ以上回りたい | 会話2 | 4往復目A | oneworld Explorer | 距離が関係ないので、遠くまで飛ぶほど得（早見表、助言65・66） |
| アジアで3か所以上に泊まりたい | 会話3 | 5往復目B | スター | oneworld 系はアジアの途中降機が2回まで（早見表、助言39） |
| 欧州の街を細かく回りたい | 会話4 | 2往復目B | スター | 欧州の路線網がいちばん強い（早見表） |
| アフリカをたくさん | 会話4 | 5往復目B | スター | カイロとアディスアベバが拠点（早見表、助言64） |
| 南米が主役 | 会話5 | 2往復目A | スター | アビアンカ航空とコパ航空。oneworld は南米の中が別手配（早見表、助言9・32） |
| オーストラリアを細かく | 会話6 | 3往復目B | oneworld Explorer | カンタス航空の国内線が使える。スターは豪州の国内線が使えない（早見表、助言61） |
| 南太平洋の島 | 会話7 | 5往復目B | Global Explorer かスター | oneworld Explorer は加盟外が飛ばす共同運航便を使えない（早見表、助言72） |
| カナダを回りたい | 会話7 | 5往復目C | Global Explorer かスター | ウエストジェット、またはエア・カナダ（早見表、助言75） |
| 10日より短い弾丸の旅 | 会話8 | 5往復目B | oneworld 系 | スターのビジネスは10泊以上が必要（早見表、助言58） |
| 途中で日本に帰るかもしれない | 会話9 | 5往復目B | スター | 券のまま一時帰国できる（アジア・オセアニアで分ける場合）（早見表、助言33） |
| 地方の空港から出発 | 会話10 | 5往復目B | スター | ANAの国内線を追加料金なしで使える（早見表、助言60） |

### 会話1：はじめての人（迷っている）

知る決まり：値段の決まり方（スターは距離、oneworld Explorer は大陸の数）。

| # | 係員 | キング |
|---|---|---|
| 1 | Welcome to the Round the World desk. Is this your first time? ／世界一周の窓口へようこそ。はじめてですか。 | Yes, it is. I'm excited, but a little nervous. ／はい。わくわくしますが、少し緊張しています。 |
| 2 | That is normal. This is a big ticket. Do you already know where you want to go? ／ふつうのことです。大きな券ですから。行きたい場所はもう決まっていますか。 | ▶A Not really. I just want to see famous cities. ／あまり。有名な街を見たいだけです。　▶B Yes. I have four places on my map. ／はい。地図に4つ置いてあります。 |
| 3 | （A）No problem. Many people start that way. Star Alliance has simple rules and the most routes. ／大丈夫。そう始める人は多いです。スターアライアンスは決まりが簡単で、路線がいちばん多いです。　（B）Good. Then the places will choose the ticket for you. ／よかった。それなら、場所が券を選んでくれます。 | I see. What decides the price? ／なるほど。値段は何で決まるのですか。 |
| 4 | Star Alliance counts your miles. oneworld Explorer counts your continents. ／スターアライアンスは飛ぶ距離を数えます。oneworld Explorer は大陸の数を数えます。 | Miles or continents. That's interesting. ／距離か、大陸か。おもしろいですね。 |
| 5 | So I will ask you a few questions. Take your time. ／ですから、いくつか質問をします。ゆっくりどうぞ。 | Okay. Please ask me anything. ／はい。何でも聞いてください。 |

場面の語：first time／nervous／famous／mile／continent
券へのつながり：A＝スターに印1つ（決まりが簡単で路線がいちばん多い）。B＝印なし、次の質問で決まる。

### 会話2：大陸を数える

知る決まり：日本のあるアジアも1大陸に数える（助言66）。ハワイは北米の扱い（助言67）。

| # | 係員 | キング |
|---|---|---|
| 1 | Let me look at your map. Kenya, Finland, Peru, and Hawaii. ／地図を見せてください。ケニア、フィンランド、ペルー、ハワイ。 | Yes. Those are my four dreams. ／はい。それがわたしの4つの夢です。 |
| 2 | Let's count the continents together. Asia is one, because you start in Japan. ／大陸をいっしょに数えましょう。アジアで1つ。日本から出発するからです。 | Oh, Japan counts too? ／えっ、日本も数えるのですか。 |
| 3 | Yes. Then Africa, Europe, South America, and North America. Hawaii is part of North America. ／はい。それからアフリカ、欧州、南米、北米。ハワイは北米に入ります。 | One, two, three, four, five. Five continents! ／1、2、3、4、5。5大陸！ |
| 4 | Five is a lot. Do you want to keep all five? ／5つは多いですよ。5つとも残しますか。 | ▶A Yes. I want all five. ／はい。5つとも行きたいです。　▶B Maybe I can cut one. ／1つ減らせるかもしれません。 |
| 5 | （A）Then oneworld Explorer is strong. Distance does not matter, so far places cost the same. ／それなら oneworld Explorer が強いです。距離は関係ないので、遠い場所でも値段は同じです。　（B）Then the price goes down one step. We can check both ways. ／それなら値段が1段下がります。両方で見てみましょう。 | Far places cost the same. I like that. ／遠い場所でも同じ値段。いいですね。 |

場面の語：count／continent／distance／far／cost
券へのつながり：A＝oneworld Explorer に印1つ（大陸4つ以上は、距離が関係ない券が得）。B＝印なし。値段の段は素材集のとおり、ビジネスで5大陸1,074,300円、4大陸936,500円（燃油・税は別）。

### 会話3：アジアで泊まる

知る決まり：泊まる（24時間以上）と乗り継ぐの違い。oneworld 系はアジアで泊まれるのは2回まで。

| # | 係員 | キング |
|---|---|---|
| 1 | Before you leave Asia, do you want to stop anywhere? ／アジアを出る前に、どこかに寄りたいですか。 | Hmm. Asia is close to home. ／うーん。アジアは家から近いですからね。 |
| 2 | True. But some people stay in Bangkok, Singapore, and Hong Kong on the way. ／そうですね。でも、途中でバンコク、シンガポール、香港に泊まる人もいます。 | Three cities? That sounds fun. ／3つの街ですか。楽しそうですね。 |
| 3 | Here is one rule. With oneworld, you can stay in Asia only two times. ／決まりが1つあります。oneworld では、アジアで泊まれるのは2回だけです。 | Only two? What does "stay" mean? ／2回だけ？「泊まる」とはどういう意味ですか。 |
| 4 | A stay is more than twenty-four hours. Less than that is just a transfer. ／泊まるとは、24時間より長くいることです。それより短ければ、ただの乗り継ぎです。 | I see. A stay is longer than one day. ／なるほど。泊まるとは、1日より長いことですね。 |
| 5 | So, how many stays in Asia do you want? ／では、アジアで何回泊まりたいですか。 | ▶A None. I want to go far away first. ／なしで。まず遠くへ行きたいです。　▶B Three or more. I love Asian food. ／3回以上。アジアの料理が大好きなので。 |

場面の語：stop／stay／transfer／rule／twenty-four hours
券へのつながり：B＝スターに印1つ（oneworld 系はアジアの途中降機が2回まで）。A＝印なし。

### 会話4：欧州とアフリカ

知る決まり：海を渡って戻ることはできないが、欧州→アフリカ→欧州の行き来はスターでできる（助言64）。

| # | 係員 | キング |
|---|---|---|
| 1 | You have Finland in Europe, and Kenya in Africa. ／欧州にフィンランド、アフリカにケニアがありますね。 | Yes. The aurora and the safari. ／はい。オーロラとサファリです。 |
| 2 | Do you want more cities in Europe? Rome, Lisbon, Athens? ／欧州の街をもっと入れますか。ローマ、リスボン、アテネなど。 | ▶A One city is enough for me. ／1つで十分です。　▶B Yes! I want to visit many small cities. ／はい！小さな街をたくさん訪ねたいです。 |
| 3 | （A）All right. We keep Europe simple. ／分かりました。欧州は簡単にしておきます。　（B）Then Star Alliance is good. It has the biggest network in Europe. ／それならスターアライアンスが合います。欧州の路線網がいちばん大きいので。 | And how about Africa? ／アフリカはどうですか。 |
| 4 | Africa is big. With Star Alliance, you can fly from Europe to Africa, and back to Europe. ／アフリカは広いです。スターアライアンスなら、欧州からアフリカへ飛んで、また欧州に戻れます。 | Back to Europe? I thought I couldn't go back. ／欧州に戻る？戻れないと思っていました。 |
| 5 | Good question. You cannot go back across the ocean. But this small round trip is okay. How much of Africa do you want? ／よい質問です。海を渡って戻ることはできません。でも、この小さな行き来は大丈夫です。アフリカはどのくらい回りたいですか。 | ▶A Kenya is enough this time. ／今回はケニアで十分です。　▶B A lot. I want to see more of Africa. ／たくさん。アフリカをもっと見たいです。 |

場面の語：network／enough／ocean／round trip／go back
券へのつながり：2往復目B＝スターに印1つ（欧州の路線網がいちばん強い）。5往復目B＝スターに印1つ（カイロとアディスアベバが拠点）。

### 会話5：南米

知る決まり：oneworld には南米を拠点にする航空会社がない。リマからクスコは別の切符。マチュピチュは予約が要る（助言51）。

| # | 係員 | キング |
|---|---|---|
| 1 | Now, South America. You chose Cusco and Machu Picchu. ／次は南米です。クスコとマチュピチュを選びましたね。 | Yes. I have wanted to go there for a long time. ／はい。ずっと前から行きたかった場所です。 |
| 2 | A lovely dream. Is South America the star of your trip? ／すてきな夢ですね。南米は、この旅の主役ですか。 | ▶A Yes. It is the main part. ／はい。いちばんの目的です。　▶B It is one of my four dreams. ／4つの夢のうちの1つです。 |
| 3 | Then please listen carefully. oneworld has no home airline in South America. ／それなら、よく聞いてください。oneworld には、南米を拠点にする航空会社がありません。 | No home airline? Can I still go? ／拠点の航空会社がない？それでも行けますか。 |
| 4 | Yes. You can fly to Lima. But from Lima to Cusco, you buy another ticket. ／はい。リマまでは飛べます。でも、リマからクスコへは、別の切符を買います。 | Another ticket. So I pay more. ／別の切符。つまり、もっと払うのですね。 |
| 5 | With Star Alliance, Avianca can take you to Cusco. And one more thing: Machu Picchu needs a reservation. ／スターアライアンスなら、アビアンカ航空でクスコまで行けます。それからもう1つ。マチュピチュは予約が要ります。 | I'll book it early. I don't want to miss it. ／早めに予約します。見のがしたくないので。 |

場面の語：main／home airline／another ticket／reservation／book
券へのつながり：A＝スターに印1つ（南米が主役ならアビアンカ航空とコパ航空。oneworld は南米の中が別手配）。B＝印なし。ただし「別の切符」の話は、値段の場面でもう一度出てくる。

### 会話6：オーストラリア

知る決まり：買ったあとで行き先を足すのはむずかしい（助言8・36）。スターは豪州の国内線が使えない。

| # | 係員 | キング |
|---|---|---|
| 1 | Some travelers go south. Have you thought about Australia? ／南へ行く人もいます。オーストラリアは考えましたか。 | Australia? I didn't put it on my map. ／オーストラリア？地図には置きませんでした。 |
| 2 | It is not too late today. But after you buy, it is hard to add a place. ／今日ならまだ間に合います。でも買ったあとは、場所を足すのがむずかしいです。 | Right. The wise teacher told me that, too. ／そうですね。賢者さまにも同じことを言われました。 |
| 3 | In Australia, some people only see Sydney. Others fly to Uluru and Cairns. ／オーストラリアでは、シドニーだけ見る人もいます。ウルルやケアンズまで飛ぶ人もいます。 | ▶A Not this time. Maybe on my next trip. ／今回はやめておきます。次の旅で行くかもしれません。　▶B I want to see Uluru, in the middle of the desert. ／砂漠の真ん中にある、ウルルを見たいです。 |
| 4 | （A）Sure. I'll leave it off. But remember this for next time: oneworld has Qantas. ／分かりました。外しておきます。でも次のために覚えておいてください。oneworld にはカンタス航空があります。　（B）Then you need flights inside Australia. oneworld has Qantas. ／それなら、オーストラリアの中を飛ぶ便が要ります。oneworld にはカンタス航空があります。 | Qantas. The airline with the kangaroo? ／カンタス。カンガルーの航空会社ですか。 |
| 5 | That's the one. Star Alliance cannot use flights inside Australia. ／それです。スターアライアンスは、オーストラリアの国内線を使えません。 | So for Australia, oneworld is better. Good to know. ／オーストラリアなら oneworld のほうがいいのですね。知れてよかったです。 |

場面の語：south／add／desert／inside／too late
券へのつながり：B＝oneworld Explorer に印1つ（カンタス航空の国内線が使える）。A＝印なし、「次の旅のメモ」に残す（2-4）。

### 会話7：南の島とカナダ

知る決まり：3つ目の券 Global Explorer がある。oneworld Explorer は、加盟していない会社が飛ばす共同運航便を使えない。

| # | 係員 | キング |
|---|---|---|
| 1 | Do you like islands? Tahiti, for example. ／島は好きですか。たとえばタヒチ。 | I love the sea. Hawaii is on my map. ／海は大好きです。ハワイは地図にあります。 |
| 2 | Hawaii is easy. But Tahiti is different. ／ハワイは簡単です。でもタヒチは別です。 | Different? How? ／別？どうちがうのですか。 |
| 3 | Some flights use a partner's plane. oneworld Explorer cannot use those. ／仲間の会社の飛行機で飛ぶ便があります。oneworld Explorer では、それは使えません。 | So the same flight name, but a different plane? ／便の名前は同じでも、飛行機がちがうのですね。 |
| 4 | Exactly. For those islands, there is a third ticket: Global Explorer. It also works well in Canada. ／そのとおりです。そういう島のために、3つ目の券があります。Global Explorer です。カナダでも使いやすい券です。 | A third ticket! I didn't know that. ／3つ目の券！知りませんでした。 |
| 5 | Do you want the far islands or Canada on this trip? ／この旅に、遠い島やカナダを入れたいですか。 | ▶A No. Hawaii is enough for me. ／いいえ。ハワイで十分です。　▶B Yes. I want to go to Tahiti. ／はい。タヒチに行きたいです。　▶C Yes. I want to travel across Canada. ／はい。カナダを横断したいです。 |

場面の語：island／partner／third／different／across
券へのつながり：B・C＝「Global Explorer かスター」に印1つ。A＝印なし。Global Explorer はまだゲームにない券なので、扱いは**PM確認5**。素材集には、フィジー・エアウェイズなど3社の加盟の扱いに未解決の食い違いがあるので、台詞の島はタヒチだけにした。

### 会話8：旅の長さ

知る決まり：スターのビジネスは全体で10泊以上。oneworld 系は短くてもよい（3泊5日も可）。

| # | 係員 | キング |
|---|---|---|
| 1 | How long is your trip? ／旅はどのくらいの長さですか。 | About one month. Thirty days. ／約1か月。30日です。 |
| 2 | A month is good. With a very short trip, you are tired all the way. ／1か月はいいですね。とても短い旅だと、最後までずっと疲れたままです。 | I want to enjoy every city. So, one month. ／どの街も楽しみたいのです。だから1か月。 |
| 3 | Some people go around the world in five days. ／5日で世界を一周する人もいます。 | Five days? Is that possible? ／5日？そんなことができるのですか。 |
| 4 | With oneworld, yes. With Star Alliance business class, you need ten nights or more. ／oneworld ならできます。スターアライアンスのビジネスクラスは、10泊以上が必要です。 | Ten nights or more. That's an important rule. ／10泊以上。大事な決まりですね。 |
| 5 | Is there any chance your trip gets shorter than ten days? ／旅が10日より短くなることは、ありそうですか。 | ▶A No. I have one full month. ／いいえ。まる1か月あります。　▶B Maybe. My work is busy. ／あるかもしれません。仕事が忙しいので。 |

場面の語：how long／tired／possible／night／shorter
券へのつながり：B＝oneworld 系に印1つ（スターのビジネスは10泊以上が必要）。A＝印なし。

### 会話9：途中で家に帰る

知る決まり：途中で帰るとき、oneworld は別の往復切符。スターは、アジア・オセアニアで分ける場合、最初と違う日本の都市なら券のまま帰れる（助言33）。

| # | 係員 | キング |
|---|---|---|
| 1 | A month is a long time. Is anyone waiting for you at home? ／1か月は長いです。家で待っている人はいますか。 | Yes. My family. ／はい。家族が。 |
| 2 | Sometimes people need to go home in the middle of the trip. ／旅の途中で、家に帰らなければならなくなる人もいます。 | In the middle? What happens to the ticket? ／途中で？券はどうなるのですか。 |
| 3 | With oneworld, you buy a round-trip ticket by yourself. With Star Alliance, in Asia or Oceania, you can go home on the same ticket. ／oneworld では、往復の切符を自分で買います。スターアライアンスでは、アジアかオセアニアにいるときなら、同じ券のまま帰れます。 | On the same ticket? That helps a lot. ／同じ券のまま？それは助かります。 |
| 4 | But you must land in a different city in Japan from your start. ／ただし、出発した街とはちがう日本の街に降りなければなりません。 | A different city. Not the same airport. ／ちがう街。同じ空港ではないのですね。 |
| 5 | Do you think you may need a break at home? ／途中で家にもどって休むことは、ありそうですか。 | ▶A No. I'll go all the way around. ／いいえ。最後まで回ります。　▶B Maybe. I want to keep that door open. ／あるかもしれません。その道は残しておきたいです。 |

場面の語：wait／in the middle／round-trip／land／break
券へのつながり：B＝スターに印1つ（券のまま一時帰国できる。アジア・オセアニアで分ける場合）。A＝印なし。「家に帰る」という話題そのものが、決まり「会話で東京へ行くと言わせない」に触れないかは**PM確認6**（台詞に東京は出していない）。

### 会話10：出発する空港

知る決まり：旅は出発した国で終わる。スターは地方空港からANAの国内線を追加料金なしで使える（助言60）。

| # | 係員 | キング |
|---|---|---|
| 1 | Last question. Where does your trip start? ／最後の質問です。旅はどこから始まりますか。 | From Haneda Airport. ／羽田空港からです。 |
| 2 | Good. Some people start from a small airport far from here. ／分かりました。ここから遠い、小さな空港から出発する人もいます。 | Do they pay more to come here? ／ここまで来るのに、もっと払うのですか。 |
| 3 | With Star Alliance, no. They can use ANA flights inside Japan at no extra cost. ／スターアライアンスなら、いいえ。日本の中はANAの便を、追加の料金なしで使えます。 | No extra cost. That's nice for them. ／追加の料金なし。それはうれしいですね。 |
| 4 | And one more rule. Your trip must end in the country where it started. ／決まりがもう1つ。旅は、始まった国で終わらなければなりません。 | So I start in Japan, and I finish in Japan. ／つまり、日本で始まって、日本で終わるのですね。 |
| 5 | Right. Will you start from Haneda, or from a local airport? ／そうです。羽田から出発しますか。それとも地方の空港からですか。 | ▶A From Haneda. It's close to me. ／羽田から。近いので。　▶B From a local airport. I want to start near my home. ／地方の空港から。家の近くから出発したいです。 |

場面の語：start／local／extra cost／end／finish
券へのつながり：B＝スターに印1つ（ANAの国内線を追加料金なしで使える）。A＝印なし。いまのゲームは入口が羽田なので、Bを選べるようにするかは**PM確認7**。

### 2-3. 印からおすすめへ

- 印がいちばん多い券を係員がすすめ、印になった答えを理由として読み上げる。例：「You said five continents. So I recommend oneworld Explorer.」
- 印が同じ数なら「Your dreams point to two tickets.」と言って、キングが▶で決める。
- 印が1つもなければ、会話1のとおり「決まりが簡単で路線がいちばん多い」スターを基本にする（素材集の助言56「迷ったらスター、が専門店の基本」）。これをゲームの決まりにするかは**PM確認8**。
- **1周目の基本の結果**：会話2でA（5大陸）＝oneworld Explorer、会話5でA（南米が主役）＝スター。同点になり、キングが選ぶ。
  - oneworld Explorer（5大陸）：券面1,074,300円。リマ⇄クスコは別の切符。
  - スター（39,000マイル以内）：券面958,900円。アビアンカ航空でクスコまで。
  - 差：1,074,300 − 958,900 = 115,400円。どちらも燃油・税は別。
- 値段の場面の山場の台詞（案）：係員「That will be one million, seventy-four thousand, three hundred yen. Fuel and taxes are extra.」／キング「One million, seventy-four thousand, three hundred yen. ... Okay. I'll take it.」スターを選んだときは「Nine hundred fifty-eight thousand, nine hundred yen.」

### 2-4. 「次の旅のメモ」（くり返し遊ぶための案）

地図にない場所を答えたとき（ウルル、タヒチ、カナダ、アジアの3都市など）は、係員が「I'll write it down for your next trip.」とメモに残す。2周目の窓口で、係員が「Last time, you said you wanted to see Uluru.」と切り出す。前の自分の答えが、次の旅の始まりとして戻ってくる。何度でも遊べる決まり（別の券＝別のルート）と、51空港を全部作る絵につながる。新しい仕組みなので**PM確認9**。

---

## 3. 成果物3：賢者の役割の再定義

### 役割

賢者は「決まりを説明する人」をやめて、**「先に失敗した人」**にする。世界一周を何度もして、そのたびに何かを後悔した人。だから言葉が短く、重い。決まりの説明は窓口にゆずる。

賢者が渡すものは3つだけ。

1. **立場**：これは1枚の大きな券で、同じ向きにしか進めず、戻れない旅だということ。
2. **後悔しない勧め**：「先に全部置く。あとで足さない。変えるのは日付だけ」。
3. **送り出し**：ここから先は自分の声で話すこと。困ったら聞き返せばよいこと（sage_3 をそのまま生かす）。

### 台詞の設計方針

- 1つの台詞に、助言は1つ。数字は1つまで。
- 決まりを言うときは「〜できない」で終わらせず、「だから先に〜しなさい」まで言う。
- 賢者自身の失敗を1つ入れる。プレイヤーが覚えるのは決まりより、人の失敗。
- 短く、ゆっくり読める文にする（今の sage_1〜3 の文の長さに合わせる）。
- 窓口で係員が同じ助言に形を変えて触れる（会話6の2往復目）。賢者の言葉が「当たった」と感じる瞬間を作る。
- 券を買ったあとは出さない（決定どおり）。助言は旅の出来事として戻す。

### 台詞の例（3つ）

1. 立場：「This ticket goes one way around the earth. You cannot turn back. So first, put every dream on the map.」／この券は、地球を1つの向きに回ります。引き返せません。だからまず、夢を全部、地図に置きなさい。（助言1）
2. 後悔しない勧め：「Once, I said, 'I will add one more city later.' It cost me one hundred and twenty-five dollars. Change your dates, not your places.」／昔わたしは「あとで1つ街を足そう」と言いました。125ドルかかりました。変えるのは日付だけ。場所は変えないこと。（助言8・36。行き先の変更は1回125米ドル、日付だけの変更は無料）
3. 送り出し：「At the desk, no one will speak for you. Say what you want, in your own voice. After you buy the ticket, you will not see me again.」／窓口では、だれもあなたの代わりに話してくれません。自分の声で、望みを言いなさい。券を買ったら、もうわたしに会うことはありません。（助言46）

### いまの sage_1〜3 との関係

- sage_1（旅のしくみ）と sage_3（旅の英語のコツ）は、この役割に合っている。そのまま使える。
- sage_2 の最後の2往復（「どちらがよいということはない。楽しそうな方を選びなさい」「どちらでも行きたい空港すべてに行ける」）は、窓口の「旅のしかたで券が決まる」と食い違う。直し方は2つ。
  - 案A：sage_2 の最後の2往復だけを「窓口でよく話しなさい。旅のしかたが券を決める」という内容に入れ替える。
  - 案B：sage_2 は変えず、上の3つの台詞を入れた会話を1本足し、賢者の最後に置く。
  - 「すでに作った冒頭3場面は作り直さない」という決定があるので、どちらにするかは**PM確認10**。

---

## 4. PM確認事項（未決定なので、この案では決めていない）

1. 行きたい場所を選ぶ場面（▶で複数を選ぶ）を、賢者の広間に置くか、窓口に置くか（設計図は窓口①）。1周目の目的地は券共通の4つなので、選ぶのは「必ず／できれば」の分け方だけにする案と、候補を全部並べて未作成を「？」にする案がある。
2. フロー5「夢を言う」を、依頼文2（まとまった文で発音の弱点を把握する）の埋め込み場所にするか。
3. 1回の旅で出す聞き取りの本数。案A：1周目は4本（会話1・2・5・8）で、残りは周回ごとに入れ替える。案B：10本を全部並べて、1本クリアで先へ進める（今の決まり「1か所に会話が3つあっても1つクリアできれば次へ」と同じ）。
4. 会話の途中に▶の分かれ目を入れる形（新しいUI）。
5. Global Explorer（3つ目の券）の扱い。案A：名前だけ出して、券は2つのまま。案B：3つ目の券として作る。
6. 会話9の「途中で家に帰る」という話題を冒頭に入れてよいか。
7. 会話10で「地方の空港から」を選べるようにするか（選んでも入口は羽田のまま）。
8. 印が1つもないときの基本をスターにするか。
9. 「次の旅のメモ」を入れるか。
10. sage_2 の直し方（案A／案B）。
11. 最初に作る券（設計図の「決めること1」。未決定のまま）。この案は割れた結果をキングが選ぶ形なので、どちらが先でも使える。
12. 聞き取りの会話のあとに単語バトルを入れるか。決定ログでは「英単語→日本語3択」は廃止の方向なので、この案では入れていない。

## 5. 最後の点検

- お金：券の値段は素材集の数字（確認レベルB、確認日2026-11-12）。燃油・税の金額は素材集の数字が2024年11月時点で古いので、台詞には金額を入れず「別」とだけ言わせた。画面に出す前に公式で確かめ直す。
- 健康：会話8の「短い旅は疲れる」は旅の計画の目安で、体の助言ではない。
- 診断と誤解される表現：なし。
- 個人情報：個人名なし。
- 権利：連合・航空会社・券の名前は実名（決まりどおり）。ロゴや図柄は使っていない。
- 守ること：「東京へ行く」の台詞なし／券を買ったあとの賢者なし／資料にない数字なし／並べ替え・英単語→日本語3択なし／文字を打つ入力なし。

## 6. 数字（見本＝今の data.py の会話と同じ指標）

| 指標 | 見本（sage・ticket の5本） | この下書き |
|---|---|---|
| 会話の本数 | 5 | 10 |
| 1本の往復数 | 5 | 5（10本すべて） |
| 場面の語 | 1本に5つ | 1本に5つ（合計50） |
| 判断表12種類のうち含めた数 | 0 | 12 |
| 分かれ目（▶） | 0 | 11か所（会話4だけ2か所） |
| 英語の語数（係員＋キング、選択肢を含む） | — | のべ1,130語、327種類 |

## 7. 参考URL（素材集に載っている出典。今回あらたに開いたページはない）

- 世界一周堂：スター https://www.sekai1.co.jp/rtwticket/type/staralliance/ ／ oneworld Explorer https://www.sekai1.co.jp/rtwticket/type/oneworld/ ／ Global Explorer https://www.sekai1.co.jp/rtwticket/type/globalex/ ／ 3つの特徴 https://www.sekai1.co.jp/rtwticket/rtwbasics/features/ ／ 変更・キャンセル https://www.sekai1.co.jp/rtwticket/rtwbasics/cancel-change/ ／ よくある質問 https://www.sekai1.co.jp/faq/
- HIS 初心者ガイド https://rtw.his-j.com/before/
- oneworld 公式 https://www.oneworld.com/round-the-world
- ゲーム本体 https://github.com/kingtheQ/kanpe-sensei-dubai
