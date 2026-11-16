# 021 ロヴァニエミ（オーロラ）の場面設計 v1

作成：2026-11-16（Claude）。設計案のみ。コードとデータは変えていない。決定の正本は `docs/pm/DECISIONS.md`。
読んだもの：docs/rules.md、docs/world-tour-design.md、docs/pm/DECISIONS.md、docs/pm/design-bible.md（§1・§4・§5・§8）、deliverables 003（会話4）・005（割りこみ・持ち越し・顔なじみ、ナイロビ→ドーハの適用例）・007（1-4、P1〜P15）・011（宣言文）、docs/materials/event-materials.md（ヘルシンキの節。ロヴァニエミの節は素材集にまだない）、docs/sources.md。
020（旅全体の構造・日数の配分）に関わる判断はしていない。日程は設計図（world-tour-design.md）の表をそのまま前提にした。

---

## 0. 結論

1. **山場は「3つの夜」で作る。** 1夜目はホテルで待つ、2夜目は車で追いかける、3夜目は丘の焚き火で待つ。どの夜に見えるかは「演出」の線引き（設計図）に入るので、案を3つ出した。推すのは**案3：選び方で変わるが、3夜のうち最低1回は見える**。
2. **場所は19か所（空港10・市内9）。5往復の場面は9本（空港4・市内5）。** 残りは1〜2往復の「ひとこと場面」と割りこみ。
3. **差の付け方は「暗さ・静けさ・無口さ」。** 色は夜の群青と雪の青白だけにし、オーロラの緑は見えた夜まで画面に一度も出さない。音は低い風と雪を踏む音、曲はオーロラが出た瞬間にだけ入る。人は口数が少なく直接的だが、最後の一言が温かい形にする（「進むほど冷たくなる」は望まない、という決まりに合わせる）。
4. **それまでの旅が返ってくる仕掛けは4つ。** 窓口で言った「The aurora」がホテルで返る／冒頭の宣言文がサンタの前で返る／ナイロビ→ドーハの顔なじみ（赤いリボンの人）が2夜目のツアーで再会する／宣言文の「little treasure」が山場の最後の一文になる。
5. **台本の下書きは、3夜目の丘の焚き火で、地元の年配の人と話す1本。** キングの5文は45語で、これまでの資料で数えた苦手な音8種類（R、語頭のL、語尾のL、θ、ð、f、v、ɚ）を全部含む。

---

## 1. 前提（調べて確かめたこと）

| 項目 | 内容 | 確認 | 出典 |
|---|---|---|---|
| 空港の名前 | サンタクロースの公式の空港（Santa Claus' official airport）と運営会社が名乗っている | A | Finavia（下の出典1・2） |
| 北極圏の線 | ターミナルの天井に、本物の北極圏の線に沿った40mの細い天窓がある。光が床の線を照らす | A | 出典1 |
| 天窓の位置 | 空港を設計した1990年の北極圏の位置に合わせてある（北極圏の線は毎年少しずつ動く） | A | 出典3 |
| 床の作品 | 床にラップランドの花崗岩を彫った作品「Earth's orbit」（Antti Laurila）がある | A | 出典2 |
| 天井の照明 | フィンランドの白樺のランプと、トナカイの角のランプ | A | 出典2 |
| ターミナル | 2019年に広さが倍になり、旅券審査の列が10本増えた。店に Ahkio Kitchen & Bar と Napapiirin Lahja（みやげ店）が入った | A | 出典4 |
| 出発ホール | 2025-10-28 に出発ホールの増築が開いた | A | 出典5 |
| 利用者 | 2024年は過去最高の約94.8万人。滑走路は3,000mで北極圏をまたぐ | A | 出典6 |
| 12月 | 20年以上、12月がいちばん混む月 | A | 出典7 |
| サンタの郵便局の支店 | 保安検査の前のカフェに、サンタの中央郵便局の支店が開いた（2019年の記事） | B | 出典8 |
| 人とトナカイ | ラップランドには約18万2千人と、20万頭を超えるトナカイがいる | A | 出典1 |
| サンタクロース村 | 空港から2〜3km。北極圏の線が舗装に描かれている。サンタに毎日会える（入場無料） | A/B | 出典1、出典9 |
| サンタの中央郵便局 | 黄色のポストは「すぐ届く」、赤いポストは「クリスマスに届く」。郵便は北極圏の特別な消印で押される | A | 出典10 |
| バス | 黄色が市内行き（Airport Express）、赤が サンタクロース村方面（Santa's Express） | C | 出典11 |
| オーロラの確率 | ロヴァニエミ周辺で、晴れた夜に見える確率はおよそ40％（研究者の計算） | A | 出典12 |
| 12月の空 | 12月はくもりの日がとても多い（地元の人の案内では約8割） | C | 出典13 |
| 12月の昼 | 12月30日ごろは日の出11:00、日の入り13:40 | C | 出典13 |
| オーロラの呼び名 | フィンランド語で revontulet＝「キツネの火」。キツネのしっぽが雪をはね上げ、火花が空に散る、という言い伝え | B | 出典14 |
| ホテルの通知 | Arctic TreeHouse Hotel は、オーロラが見えたら知らせる Aurora Alert を出している（空港から約3.4km、サンタクロース村の近く） | A/B | 出典15 |
| 人柄 | 沈黙を気まずく思わない。話し方は直接的。雑談は少ない。「How are you?」は文字どおりの質問と受け取る。人との距離を広くとる | B | 出典16・17 |
| 便（oneworld版） | ヘルシンキ発 21:35 → ロヴァニエミ着 23:00 の便がある（2025-12-30の実績） | B | 出典18 |
| 便（スター版） | イスタンブール 09:50発 → ロヴァニエミ 13:30着（2025/26冬の時刻）。2026/27冬は 2026-12-08〜2027-03-07 の火・木・土・日 | B / A | 出典19、出典20 |

**大事な違い**：oneworld版はヘルシンキで入国が済んでいるので、ロヴァニエミは**国内線の到着**（入国審査なし）。スター版はトルコ（シェンゲン圏の外）から来るので、ロヴァニエミで**入国審査がある**。到着の「4点セット」を崩す理由が、現実の側にもともとある（007 P6・005 案C）。

---

## 2. 場面構成（oneworld版：10〜13日目）

印：◆持ち越し／●顔なじみ／□ひとこと場面（1〜2往復）／★割りこみ／■5往復の場面。英文は例。値段・気温・便名は架空。

### 2-1. 到着（10日目の夜 23:00）

| # | 場所 | 相手 | 目的・起きること | 形 |
|---|---|---|---|---|
| R1 | 機内・着陸前 | 機長のアナウンス | 「The temperature in Rovaniemi is minus twenty-two degrees.」窓の外は真っ暗、滑走路の灯りだけ | □ |
| R2 | 到着の通路 | ルル | 床の線で足が止まる。「Look down, King. We are standing on the Arctic Circle.」夜なので天窓に光はない（◆出発の昼に回収する。D4） | □ |
| R3 | 手荷物 | 同じ便の旅行者（スキー板を持った家族づれ） | 薄いコートのキングを見て「Is that your only coat?」→ 防寒の話。◆種：「warm hat」を買うかどうか | ■ |
| R4 | 到着ロビーの出口 | タクシー乗り場の運転手 | ★最終バスはもう出た（時刻は演出）。乗る前に料金を聞く（「How much is it to the hotel?」）。ホテル名を言う。◆種：Arctic TreeHouse Hotel | ■ |

- 昼に着く版（スター版、13:30着）では、R3の前に**入国審査**（■）が入り、R4は ▶ 黄色のバス／赤いバス／タクシー の選択になる（2-4）。
- バスの色は、赤と黄だけで見分けさせない。車体の文字（Airport Express／Santa's Express）と形もちがえる（色の見え方の決まりに合わせる）。

### 2-2. 市内（10日目の夜〜12日目の夜）

| # | 場所 | 相手 | 目的・起きること | 形 |
|---|---|---|---|---|
| C1 | ホテルのフロント（Arctic TreeHouse Hotel、夜） | フロントの係 | ◆窓口で言った「The aurora」が返る：「So you are the one who came for the aurora.」オーロラの通知を申しこむ（「Please wake us up if the lights come.」） | ■ |
| C2 | 部屋（1夜目） | ルル | オーロラ待ち1夜目。窓の外の空と、鳴るかもしれない通知 | 2-3 |
| C3 | 朝食（11日目、朝9時でも真っ暗） | となりの席の旅行者 | 「Is it morning or night?」「The sun comes up at eleven.」 | □ |
| C4 | サンタクロース村の北極圏の線 | ルル | 舗装に描かれた線をまたぐ。「One step, and we are in the Arctic!」 | □ |
| C5 | サンタの中央郵便局 | 列に並ぶ子どもとその親（旅行者） | 子どもに「Which box? Yellow or red?」と聞かれる。キングははがきを書き、赤いポスト（クリスマスに届く）に入れる。宛先は「未来のキングとルル」 | ■ |
| C6 | サンタクロース・オフィス | サンタ | ◆宣言文が返る：「Do you have a wish for your journey?」に、冒頭の宣言文の1文（例：We both help each other.）で答える | ■ |
| C7 | オーロラを追うツアー（2夜目、車で雲の切れ間へ） | 同じツアーの旅行者 ●赤いリボンの人 | ●ナイロビ→ドーハの便で会った人と再会：「You again! First Doha, now the Arctic!」雲を見ながら待つ | ■ |
| C8 | 犬ぞりかトナカイ（12日目の昼、設計図の「候補」） | ガイド | 実名の施設は作る直前に決める | ■（候補） |
| C9 | オウナスヴァーラの丘の焚き火（3夜目） | 地元の年配の人（係員ではない） | **山場**。台本の下書きは第5章 | ■ |

### 2-3. オーロラ待ちの3夜

| 夜 | 選べる過ごし方（▶） | 見えなかった形 | 見えた形 |
|---|---|---|---|
| 1夜目（C2） | ▶ ホテルで通知を待つ ／ 外に出て空を見る | 通知は鳴らない。窓の外は雪。ルル「The sky is closed tonight.」→ ココアを飲んで寝る（□） | 通知が鳴る（★）。外に出ると、うすい緑が1本だけ |
| 2夜目（C7） | ▶ 追いかけるツアー ／ ホテルで待つ | 車で3か所回るが、どこも雲。帰りの車で、赤いリボンの人が雲の切れ間の話をする | 雲の切れ間で、短く強く出る |
| 3夜目（C9） | ▶ 丘の焚き火 ／ ホテルで待つ ／ 寝る | 雲。地元の人「Not tonight. The lights don't come when we call them.」→ 火の前で話して終わる | 第5章の台本 |

見える夜の決め方は「演出」に入る（設計図の線引き）。案を並べる。

| 案 | 中身 | よい点 | 弱い点 |
|---|---|---|---|
| 案1 固定 | 1夜目は必ず見えない、2夜目はかすか、3夜目にはっきり見える | 山場がいちばん強く作れる。台本が1つで済む | 2周目に同じ筋になる。現実（晴れた夜で約4割）より甘い |
| 案2 確率 | 夜ごとにくもり・晴れを決め、晴れなら約4割で見える | いちばん現実に近い。遊び直しの理由になる | 3夜とも見えない旅がかなりの確率で起きる。最初の山場が消える |
| **案3 選び方で変わる＋下限（推す）** | 夜ごとの過ごし方で出やすさが変わる（追いかけるツアー＞丘＞ホテル）。ただし3夜のうち最低1回は見える | 自分で選んだ結果に見える。最初の山場は消えない。見えなかった夜も物語として残る | 「最低1回」は現実より甘い。その甘さを許すかはキングの判断 |

### 2-4. 出発（13日目の昼）

| # | 場所 | 相手 | 目的・起きること | 形 |
|---|---|---|---|---|
| D1 | チェックイン（冬の混雑） | チェックインの係 | 冬の列。荷物の重さ（買ったみやげ） | ■ |
| D2 | 保安検査の前のカフェ（サンタの郵便局の支店） | ルル | C5 に行かなかった人の受け皿：ここで赤いポストに出せる | □ |
| D3 | 保安検査 | 保安検査の係員 | コート・帽子・ブーツを全部トレーに。「Your boots too, please.」 | ■ |
| D4 | 出発ホール | ルル | 昼の光が天窓から床の線を照らす（R2の回収）。「It was dark when we came.」 | □ |
| D5 | 搭乗ゲート | アナウンス | ★吹雪で遅れる（2025年12月、ラップランドの暴風雪で約20便が欠航・遅延した実例＝素材集 HEL #13、B）。行き先は変えず、着き方だけ変える（007 P10） | ★ |
| D6 | 機内（マドリードへ） | となりの席の客 | 次の国の予告（007 P4）。「Madrid? Wear light clothes. You won't need that hat.」 | □ |

### 2-5. 数（見本と同じ指標：場所の数と5往復の本数で数えた）

| 区分 | 場所 | 5往復の場面 | ひとこと・割りこみ |
|---|---|---|---|
| 空港（R1〜R4、D1〜D6） | 10 | 4（R3・R4・D1・D3） | 6 |
| 市内（C1〜C9） | 9 | 5（C1・C5・C6・C7・C9。C8は候補で数えない） | 4（C2〜C4、オーロラの夜の□は含めず） |
| 合計 | 19 | 9 | 10 |

ロヴァニエミは3泊するので、5往復は市内に寄る（4：5）。旅全体の「空港5割・市内5割」に合わせる調整は 020 の担当なので、ここでは触れない。

---

## 3. ナイロビ・ドーハとの差

### 3-1. 一覧

| 軸 | ナイロビ | ドーハ（005の案） | ロヴァニエミ（この案） |
|---|---|---|---|
| 着く時刻 | 朝 | 夜 | 深夜23:00（スター版は昼13:30。もう夕暮れ） |
| 着いた最初の音 | にぎやか | 曲なしで足音だけ（屋内の静けさ） | 屋内は静か。出口のドアが開いた瞬間に、低い風の音と、雪を踏む「ギュッ」という低い音（屋外の静けさ） |
| 曲 | 現地らしい曲 | 静かな曲 | 基本は曲なし。宿と村ではカンテレ（フィンランドの弦楽器）風のやわらかい音。**オーロラが出た瞬間にだけ曲が入る**（イベントには必ず音楽、の決まり） |
| 色 | 土と緑 | 夜の金色 | 夜の群青・雪の青白・街灯の橙。オーロラの緑は見えた夜まで画面に出さない |
| 手続き | 入国4点セット | 入国の前に列車 | 入国なし（国内線）。床の北極圏の線と、外の寒さが「その空港だけの1か所」 |
| 人 | 明るく話しかける | ていねい・控えめ | 口数が少なく直接的。沈黙を気にしない。ただし最後の一言は温かい |
| 影絵 | — | — | トウヒの森の影絵と、オウナスヴァーラの丘のなだらかな線 |

### 3-2. 絵の差し替え（新しい絵は描かない）

- 既存の背景に**夜のパレット**を当てる：空は群青、地面は雪の青白、窓の灯りは橙。グラデーションの白っぽい表現は使わない決まりなので、雪は2〜3色の平らな塗りで出す。
- 地平線にトウヒの森の影絵を1枚（少ないピクセルで済む）。
- 空港は、床の線を1本足すだけで「ここだ」と分かる（天井の天窓は、出発の昼にだけ光る線として出す）。
- 人物は色ちがいで、厚いコート・帽子・手袋を着せる（服装だけで悪役にしない決まりはそのまま）。

### 3-3. 看板（フィンランド語・スウェーデン語・英語の3段案）

フィンランドの空港の看板は、フィンランド語・スウェーデン語・英語の3つで書かれ、ヘルシンキ空港では2017年から英語をいちばん大きくしている（出典21、A）。ロヴァニエミでも同じ並びかは、写真が見つからず確かめられなかった（第6章）。下の案は「英語を大きく、その上に現地語」の形。

| 英語（大） | フィンランド語 | スウェーデン語 | 使う場所 | 確認 |
|---|---|---|---|---|
| Arrivals | Saapuvat | Ankommande | R2 | フィンランド語の意味は辞書（出典22、B）。看板の実物は未確認 |
| Baggage | Matkatavarat | Bagage | R3 | 同上 |
| Exit | Uloskäynti | Utgång | R4 | 同上 |
| Check-in | Lähtöselvitys | Incheckning | D1 | 同上 |
| Security | Turvatarkastus | Säkerhetskontroll | D3 | 同上 |
| Departures | Lähtevät | Avgående | D4 | 同上 |
| Arctic Circle | Napapiiri | Polcirkeln | R2・C4 | Napapiiri はサンタの郵便局の住所に使われている（出典23、B）。スウェーデン語は未確認 |
| Rovaniemi Airport | Rovaniemen lentoasema | — | R2 | 正式名（出典24、B） |
| Santa Claus' Main Post Office | Joulupukin Pääposti | — | C5 | 出典24、B |

- スウェーデン語の語は、ヘルシンキの3段表示の形を借りた案。ロヴァニエミの看板に実際に出ているかは未確認なので、作る前に空港の写真で確かめる。
- 頼まれていない日本語は入れない。フィンランド語は看板のフォント表示と、地元の人の「revontulet」の1語だけ。
- サーミの文化の要素（ヨイクの歌い方、民族衣装の柄）は、扱いに配慮が要るので使わない案。

### 3-4. 人柄の出し方（台本の原則）

- 係員：文が短い。前置きがない。「Your boots too, please.」で終わる。冷たいのではなく、要点だけ。
- 地元の人：間を空ける。「How are you?」を文字どおりの質問として受け、本当の答えを返す。
- 旅行者（英国のチャーター客、家族づれ）：よく話す。無口な地元の人との差がはっきりする。
- 「沈黙は失敗ではない」を体で知る場面を1つ作る（第5章の3往復目）。

---

## 4. 山場としての仕掛け

### 4-1. それまでの旅が返る（持ち越し・顔なじみ）

| 返るもの | 最初に出た場所 | ロヴァニエミで返る形 | 仕組み |
|---|---|---|---|
| 窓口の「The aurora and the safari.」 | 003 会話4・1往復目 | C1 フロント「So you are the one who came for the aurora.」 | 005 の B1（文を固定）でできる。言った場合だけ返る |
| 宣言文（011） | 冒頭 | C6 サンタ「Do you have a wish for your journey?」→ 宣言文の1文で答える。山場の最後（C9）の「This is our little treasure.」は宣言文の「share every little treasure」から | B1。宣言文は全員が言うので、言わなかった場合の分岐は要らない |
| 赤いリボンの人 | 005 ナイロビ→ドーハ | C7 ツアーで再会 | 007 P11（旅を通して出る相手）の候補。採るかは確認2 |
| 賢者の聞き返し（sage_3） | 冒頭 | C9 の暗闇。顔も口も見えないので、聞き返しの言い方がそのまま役に立つ | 台本だけ |
| 夜の数 | — | C9 の1往復目「This is our first / second / third night.」 | 005 の B2（選んだことで文が変わる）。軽い |

### 4-2. 弱い音の生かし方

- 第5章の台本で、キングの5文に**これまでの資料で数えた苦手な音8種類を全部入れた**（数は 5-3）。山場で「言えた」体験が、そのまま苦手な音の筋トレになる。
- 007 の写真のルールに合わせ、写真は**発音の出来では撮れない**。言えなかった語は、いつもどおり記録に溜めるだけ。
- 案（確認3）：暗闇の場面だけ、ルルの声を小さくする（「Shh... whisper.」）。カンペはそのまま出すので画面の作りは変えないが、演出が変わるので確認がいる。

### 4-3. 写真（007 P8：1日1枚、失敗も写真になる）

| 日 | 写真になる「初めて」 | 見えなかった場合 |
|---|---|---|
| 10日目 | 初めて北極圏の線の上に立った（R2） | — |
| 11日目 | 見えた夜：オーロラと、キングとルルの影 | 赤いポストに、はがきを入れた手（C5）。またはサンタとの1枚（C6） |
| 12日目 | 見えた夜：焚き火の向こうの緑の帯と、ふたりの影 | 雲の下の焚き火とココア。地元の人の「Not tonight.」の場面をそのまま切りとる |

- 同じ日に2つ「初めて」があるときは、**オーロラを優先**する案。
- 見えなかった写真も、アルバムでは「見えなかった夜」として並ぶ（失敗も写真になる）。

### 4-4. 終わりへの糸（赤いポストのはがき）

- C5 で赤いポストに入れたはがきは、クリスマスに届く（実物の決まり）。帰国後1か月のアルバムの場面（007-7）で、アルバムにはがきがはさまっている形にできる。
- 出発の月（未決定）で意味が変わる：12月出発なら「旅の間に家に届いていた」、2月出発なら「次のクリスマスに届く」（2周目への引きになる）。

---

## 5. 台本の下書き：C9 オウナスヴァーラの丘の焚き火（3夜目・見えた版）

- 相手：地元の年配の人。係員でもツアーの人でもない。丘の焚き火に薪を足している。無口。
- 状態：3夜目。それまでの2夜は見えていない（案3で、この夜が「最低1回」になる場合）。ルルはキングの左。
- 音：最初は焚き火のパチパチ（低い音）と風だけ。3往復目でオーロラが出た瞬間に曲が入る。

| # | 地元の人 | キング |
|---|---|---|
| 1 | Waiting for the lights? ／ 光を待っているのかい。 | Yes. This is our third night here. ／ はい。ここで3日目の夜です。 |
| 2 | Clear sky tonight. Look north. Over the trees. ／ 今夜は晴れだ。北を見な。木の上だ。 | Over the trees? I can't see anything yet. ／ 木の上？ まだ何も見えません。 |
| 3 | Wait. ……（5秒の沈黙）…… There. Low and green. You see it? ／ 待ちな。……ほら。低くて、緑の。見えるか。 | I see it! The green line is moving! ／ 見えます！ 緑の線が動いてる！ |
| 4 | We call them revontulet. Fox fires. A fox runs on the snow, and its tail throws sparks into the sky. ／ わたしらは revontulet と呼ぶ。キツネの火だ。キツネが雪の上を走って、しっぽが空に火花を飛ばすんだ。 | A fire fox? What a beautiful story. ／ 火のキツネ？ なんてきれいなお話。 |
| 5 | Where are you from? ／ どこから来た。 | From Japan. We came all this way for the lights. This is our little treasure. ／ 日本からです。光を見に、はるばる来ました。これがぼくたちの小さな宝ものです。 |
| 締め | Good. Take one picture. Then put the camera down, and just look. ／ いいね。写真は1枚。それからカメラを置いて、ただ見な。 | （写真の画面へ。1日1枚の写真になる） |

日本語は確認用。画面には出さない（決まりのとおり）。

### 5-1. 作るときに考えたこと

- 1往復目の「third」は、その夜の数で first／second／third に変わる（4-1）。
- 3往復目の5秒の沈黙は「無口な国」の体験。マイクは相手が言い終えたら自動で聞き始める決まりなので、**沈黙は相手の音声の途中に入れる**（2つの音声に分けて間を空ける）。読み上げの間の作り方は実装のときに確かめる。
- 4往復目の言い伝えは、出典14の内容に沿う。説明ではなく、相手の昔話として出す。
- 5往復目の「little treasure」は宣言文からの持ち越し（4-1）。
- 締めの「写真は1枚」は、写真のルール（1日1枚）を世界の言葉で言っている。
- 見えなかった版：3往復目から変える。「Clouds. Not tonight.」→「Maybe tomorrow?」→「Maybe. The lights don't come when we call them.」→ 火の前で revontulet の話（4往復目はそのまま）→ 5往復目の最後を「This fire is our little treasure tonight.」にする。

### 5-2. 場面の語

north／clear／spark／tail／fox／treasure／all this way

### 5-3. 数（011・004 と同じ指標：苦手な音ごとに語を数えた。CMU 発音辞書で判定）

| 音 | キングの5文（45語） | 地元の人（56語。revontulet は辞書になく数えない） |
|---|---|---|
| R | 7（for from green here story treasure trees） | 12 |
| 語頭のL | 3（lights line little） | 4 |
| 語尾のL | 3（all beautiful little） | 2 |
| θ | 2（anything third） | 2 |
| ð | 2（the this） | 4 |
| f | 5（beautiful fire for fox from） | 4 |
| v | 2（moving over） | 1 |
| ɚ | 5（fire our over third treasure） | 4 |
| 合計 | 8種類すべてを含む | 8種類すべてを含む |

---

## 6. 未確認のこと（調べたが確かめられなかったもの）

1. ロヴァニエミ空港の看板の実際の文言と、スウェーデン語が出ているか（Finavia の資料ではヘルシンキの3段表示だけ確認できた）。
2. 天窓と床の線が、到着側と出発側のどちらから見えるか（Finavia の資料に場所の説明がない）。R2 と D4 の置き方はこれで変わる。
3. 保安検査の前のサンタの郵便局の支店が、2025年の増築のあとも同じ場所にあるか（記事は2019年）。
4. 夜23時着の便のときに Airport Express が走っているか（資料により「全便に合わせる」と「9時〜21時30分」が割れている。出典11）。
5. 2026/27冬のフィンエアーのヘルシンキ→ロヴァニエミ夜便の時刻（使ったのは2025年12月の実績）と、ターキッシュの到着時刻（使ったのは2025/26冬の時刻）。
6. オウナスヴァーラの丘の焚き火の場所が、冬の夜に誰でも使えるか。作る前に Visit Rovaniemi などで確かめる。

---

## 7. キングに決めてほしいこと

1. **オーロラが見える夜の決め方**：案1 固定／案2 確率／案3 選び方で変わる＋最低1回（推す）。
2. **赤いリボンの人を2夜目のツアーで再会させるか**（007 P11 の「旅を通して出る相手」に使うか）。
3. **暗闇の場面の演出**：ルルの声を小さくする（4-2）。画面は変えないが演出が変わる。
4. **山場（C9）のあとに単語バトルを付けるか**。案：付けない（余韻を壊さないため）。流れの変更なので確認がいる。
5. **泊まるホテル**：Arctic TreeHouse Hotel（オーロラの通知あり、空港・サンタクロース村に近い）を推す。ほかの候補は Apukka Resort（ガラス屋根の部屋、アプリで通知）、Arctic SnowHotel & Glass Igloos（イグルーに通知）。
6. **スター版の入国審査をロヴァニエミで作るか**（スター版ではフィンランドの1枚画面もここで出ることになる。oneworld版はヘルシンキで出る）。
7. **ふざけた一言の案**：「More reindeer than people.」（ラップランドの人口約18万2千人、トナカイ20万頭超。出典1）を、フィンランドの1枚画面かルルのひとことに使うか。

---

## 8. 最後の点検

- お金：値段はすべて架空。タクシーは「乗る前に料金を聞く」を会話にしただけで、金額は出していない。
- 健康：寒さの話はあるが、健康の助言・診断に見える表現はない。
- 個人情報：個人名なし。地元の人・旅行者・サンタは役名だけ。
- 権利：お店・ホテル・施設は実名（決まりのとおり）。ロゴ・商標の絵は使わない。「The Official Hometown of Santa Claus」は登録商標の表記がある（出典25）ので、看板の文言としては使わず、地名と施設名だけを使う。サンタの見た目は一般的なサンタにし、特定の施設のサンタの衣装・顔を写さない。
- 文化：サーミの文化の要素は使わない（3-3）。revontulet の言い伝えは、フィンランドの昔話として広く紹介されている範囲にとどめた。

---

## 出典（確認日はすべて 2026-11-16）

1. Finavia「Rovaniemi Airport（サンタと北極圏）」https://www.finavia.fi/sv/node/4402
2. Finavia「Travel to Lapland via Santa's official home airport」（2017-03-08）https://www.finavia.fi/sv/node/4918
3. Finavia「Art, Rovaniemi」https://finavia.fi/sv/node/3012
4. Finavia 2019-11-08 プレスリリース（増築完了）https://www.finavia.fi/sv/node/6422
5. Finavia 2025年「Expansion of the departures hall at Rovaniemi Airport has been completed」https://www.finavia.fi/en/newsroom/2025/expansion-departures-hall-rovaniemi-airport-has-been-completed
6. Finavia 2025-04-22「Extending Rovaniemi Airport's terminal」https://www.finavia.fi/en/newsroom/2025/finavia-invests-development-tourism-lapland-extending-rovaniemi-airports-terminal
7. Finavia 2023「Learn more about Rovaniemi Airport」https://finavia.fi/en/newsroom/2023/lapland-attracts-tourists-all-over-world-learn-more-about-rovaniemi-airport
8. Lapland's attractiveness increases（Finavia 発表の転載）https://www.infolotnicze.pl/?p=61172
9. This is Finland「Sending Santa letters in Finnish Lapland」https://finland.fi/?p=3952
10. Santa Claus Village 公式「Shopping in Santa Claus Main Post Office」https://santaclausvillage.info/?p=1507
11. App Savvy Traveller「Rovaniemi airport transfers」https://appsavvytraveller.com/rovaniemi-airport-transfers/ ／ vincent.voyage https://souvenirs.vincent.voyage/?p=32547
12. Visit Rovaniemi「What's the best time of year to spot the aurora borealis」https://www.visitrovaniemi.fi/whats-best-time-year-spot-aurora-borealis
13. Megan Starr「A Local's Guide to Rovaniemi in December」https://www.meganstarr.com/?p=94954
14. Discovering the Arctic「The Northern Lights」https://discoveringthearctic.org.uk/science-and-research/research/the-northern-lights/ ／ Wikipedia「Firefox (mythology)」https://en.wikipedia.org/wiki/Firefox_(mythology)
15. Arctic TreeHouse Hotel 公式 https://arctictreehousehotel.com/seasons-in-lapland/magnificent-northern-lights/ ／ 距離 https://grandhotelvillaigiea.icastelli.net/en/arctic-treehouse-hotel
16. Aalto University「Finland Studies MOOC」https://openlearning.aalto.fi/mod/page/view.php?id=16060
17. Tampere University「Finnishness - Finnish small talk」https://blogs.tuni.fi/finnishness/uncategorized/finnishness-finnish-small-talk/
18. AY525 の実績 https://whatflytime.com/flight-status/ay525
19. TK1749 の時刻（2025/26冬）https://20230216t125414-dot-fltmapper.appspot.com/route/YY_IST_RVN
20. Visit Rovaniemi「Flights to Rovaniemi」https://www.visitrovaniemi.fi/plan/getting-here/flights-to-rovaniemi/
21. Finavia「Have you noticed the new signs at Helsinki Airport?」（2017-03-08）https://www.finavia.fi/fi/node/5303
22. Preply「Finnish airport vocabulary」https://preply.com/en/blog/finnish-airport-vocabulary
23. Edelweiss「Rovaniemi tips」https://www.flyedelweiss.com/ch/en/destinations/rovaniemi/tips-santa.html
24. Wikipedia「Rovaniemi Airport」https://en.wikipedia-on-ipfs.org/wiki/Rovaniemi_Airport ／「Santa Claus' Main Post Office」https://en.wikipedia.org/wiki/Santa_Claus%27_Main_Post_Office
25. Visit Rovaniemi「The Official Hometown of Santa Claus®」https://www.visitrovaniemi.fi/love/santa-claus-magic-of-christmas/
