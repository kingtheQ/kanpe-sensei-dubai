# -*- coding: utf-8 -*-
# 世界一周編 ドーハ後半（タスク023。設計の正本: docs/pm/deliverables/018-doha-second-half-design-v1.md 案A）
# 市内16＋出発8＝24場面（各5往復・単語5）と、割りこみ・顔なじみ（014 の部品：event_data の ev()/SLOTS/VARIANTS の形）。
# 会話は創作。値段・時刻・ゲート・席・階は架空。個人名なし。ホテル名・予約番号・住所は出さない（018 §5.1・§6）。
#
# 実在の要素（出典）
#   018 §3.2 で確認済み: 空港内の旅客列車（南駅→北駅。Gulf Times 2016-11-01。今も同じ運行かは未確認なので「短い乗車」以上は言わない）
#                         南の広場の大きなクマ（位置のみ。色・絵は使わない。名前だけ出す）／北の広場のオーチャード（屋内の木々）
#                         スーク・ワキーフ（既存データ）
#   タスク023 で追加確認（2026-11-17 検索）:
#     コルニーシュ＝ドーハ湾ぞいの三日月形の遊歩道 https://www.listmag.com/en/see-do/art-culture/ultimate-guide-to-doha-corniche-4258 （公開日は表示なし）
#     コルニーシュから伝統の木の舟（ダウ）で湾をまわる30分の乗船 https://gowithguide.com/qatar/tour/ad-dawhah-doha-private-city-highlights-tour-with-corniche-dhow-boat-cruise-suv-sedan-1-6-pax-25008
#                                                               https://www.nomadotravel.app/en/guides/doha-boat-rides-guide （公開日は表示なし）
#     コルニーシュの南の端がスーク・ワキーフの地区につながる https://www.nomadotravel.app/en/places/doha-corniche
#     スーク・ワキーフで香辛料・布・みやげを売る https://wotif.com/things-to-do/doha-private-city-highlights-guided-tour-and-dhow-cruise.a48016111.activity-details
#   使わないもの（未確認）: 鷹の店（018 の city_s2 → 布の店に変更）、ラウンジ名、航空会社・便名・時刻、ホテル・レストランの実名、
#                           クマの色と絵、出国の指紋、1日券の値段。
import window_data as W

T, O, OT, star = W.T, W.O, W.OT, W.star
NEW = []   # この国で足した場面のID（数える用）


def add(D):
    def d(id, who, bg, sp, intro, pairs, words, **kw):
        D.append(dict(id=id, who=who, bg=bg, sp=sp, intro=intro, pairs=pairs, words=words, **kw))
        NEW.append(id)

    def ev(id, who, bg, sp, pairs, fx=None, kind='ev', **kw):
        D.append(dict(id=id, who=who, bg=bg, sp=sp, intro='', pairs=pairs, words=[], ev=1, auto=1, kind=kind, fx=fx, **kw))
        NEW.append(id)

    # =====================================================================================
    # 状態シート（市内・1日目の夜）
    #   場所: スーク・ワキーフの路地 → ホテル（スークの近く） → スークの店 → スークのレストラン（外の席）
    #   時刻: 到着した日の夜（入国・タクシー／メトロのあと）。あいさつは Good evening
    #   ルル: いる（ただし city_t3 は最初いない → 4往復目のあとで手をふって戻る）
    #   持ち物: 青いスーツケース1つ、スマホ（予約はスマホの中）、木のキリン（ナイロビで買った人だけ）
    #   再登場フレーズ: 1泊だけ（doh_immig1）／ホテル名を忘れた・予約はスマホ（doh_immig2）／木のキリン（nbo_sec2）／
    #                   ニャマチョマ（nbo_java2）／焼き魚（h2 で聞く → r1 で注文 → c3 で好きな食べ物）
    #   禁止: ホテル名・予約番号・住所・個人名／実在の値段／鷹の店／「東京へ行く」／「復習」
    # =====================================================================================
    d('doh_city_t2', '地元の男性', 'calley', 'c_man', '夜のスーク。ベンチにすわった男性が、地図を見ているキングに声をかけた。', [
        ("Good evening, my friend. You look a little lost.", "こんばんは。すこし迷っているようですね。",
         "*Yes*. *I* *am* *looking* *for* *my* *hotel*. *It* *is* *near* *the* *souq*.", "はい。ホテルをさがしています。スークの近くです。"),
        ("Many hotels are near the souq. Do you know the name?", "スークの近くにはホテルが多いです。名前はわかりますか。",
         "*I* *forgot* *it*! *But* *I* *have* *the* *booking* *on* *my* *phone*.", "忘れました！でも予約は携帯にあります。"),
        ("No problem. Please show me.", "だいじょうぶ。見せてください。",
         "*Here* *it* *is*. *Do* *you* *know* *this* *hotel*?", "これです。このホテルを知っていますか。"),
        ("Yes. Go straight, then turn left at the tea shop. Two minutes.", "はい。まっすぐ行って、お茶の店で左へ。2分です。",
         "*Straight*, *and* *left* *at* *the* *tea* *shop*. *Thank* *you*!", "まっすぐ、お茶の店で左。ありがとう！"),
        ("You are welcome. Have some tea first. It is good here. Welcome to Qatar!", "どういたしまして。まずお茶をどうぞ。ここのはおいしいですよ。カタールへようこそ！",
         "*I* *will*. *Thank* *you* *very* *much*.", "そうします。ありがとうございます。")],
        [("lost", "迷った"), ("straight", "まっすぐ"), ("turn left", "左に曲がる"), ("booking", "予約"), ("near", "近く")], kind='trav')

    d('doh_city_t1', 'お茶の屋台の人', 'calley', 'c_tea', '路地の小さなお茶の屋台。湯気と、あまい香り。', [
        ("Good evening! Tea? We have milk tea and mint tea.", "こんばんは！お茶はいかが？ミルクティーとミントティーがあります。",
         "*What* *is* *in* *the* *milk* *tea*?", "ミルクティーには何が入っていますか。"),
        ("Milk, tea, and spices. It is sweet and strong.", "ミルクと紅茶とスパイスです。あまくて濃いですよ。",
         "*Sweet* *and* *strong*. *One* *milk* *tea*, *please*.", "あまくて濃い。ミルクティーを1つください。"),
        ("Small cup or big cup?", "小さいカップと大きいカップ、どちらにしますか。",
         "*A* *small* *cup*, *please*. *How* *much* *is* *it*?", "小さいのをお願いします。いくらですか。"),
        ("Two riyals. Be careful, it is very hot.", "2リヤルです。気をつけて、とても熱いですよ。",
         "*Mmm*. *It's* *really* *good*!", "うーん。本当においしい！"),
        ("Thank you! Come back tomorrow morning, my friend.", "ありがとう！明日の朝もまたどうぞ。",
         "*Maybe*! *We* *fly* *tomorrow* *afternoon*.", "たぶん！明日の午後に飛ぶんです。")],
        [("mint", "ミント"), ("spices", "スパイス"), ("sweet", "あまい"), ("cup", "カップ"), ("careful", "気をつける")])

    d('doh_city_t3', '地元の若者', 'calley', 'c_young', '路地の角。ふり返ると、ルルがいない！', [
        ("Are you okay? You look worried.", "大丈夫ですか。心配そうですね。",
         "*My* *friend* *is* *gone*. *She* *was* *here* *a* *minute* *ago*.", "友だちがいないんです。1分前はここにいました。"),
        ("Don't worry. The souq is like a maze. Many people get lost.", "心配しないで。スークは迷路のようです。迷う人はたくさんいます。",
         "*Really*? *What* *should* *I* *do*?", "本当ですか。どうしたらいいですか。"),
        ("Does your friend like shopping?", "お友だちは買い物が好きですか。",
         "*Yes*! *She* *loves* *shopping*.", "はい！買い物が大好きです。"),
        ("Then try the shops at the end of this street. Let's go together.", "それなら、この通りの先の店へ。いっしょに行きましょう。",
         "*Thank* *you*. *That* *is* *very* *kind*.", "ありがとう。ご親切に。"),
        ("Look! Is that your friend? She is waving at you.", "見て！あれがお友だちですか。手をふっていますよ。",
         "*Yes*! *That's* *her*! *Thank* *you* *so* *much*!", "はい！あの子です！本当にありがとう！")],
        [("worried", "心配そうな"), ("a minute ago", "1分前"), ("maze", "迷路"), ("shopping", "買い物"), ("waving", "手をふっている")],
        kind='trav', lvis=0, nohelp=1,
        inter=[{'after': 3, 'anim': 'fade', 'ms': 1200, 'swapAt': 600, 'set': {'lvis': 1}}])

    d('doh_city_h1', 'ホテルのフロント係', 'chotel', 'c_front', 'ホテルのフロント。夜おそく、しずかなロビー。', [
        ("Good evening, and welcome. Do you have a reservation?", "こんばんは、ようこそ。ご予約はありますか。",
         "*Yes*. *Here* *is* *the* *booking* *on* *my* *phone*.", "はい。スマホに予約があります。"),
        ("Thank you. One night, checking out tomorrow. Is that right?", "ありがとうございます。1泊で、明日チェックアウトですね。",
         "*Yes*. *Only* *one* *night*.", "はい。1泊だけです。"),
        ("May I see your passports, please?", "パスポートを拝見できますか。",
         "*Of* *course*. *Here* *you* *are*.", "もちろん。どうぞ。"),
        ("Your room is on the fourth floor. Breakfast starts at six thirty.", "お部屋は4階です。朝食は6時半からです。",
         "*Six* *thirty*. *Where* *is* *the* *breakfast* *room*?", "6時半ですね。朝食の部屋はどこですか。"),
        ("On the first floor, next to the garden. Here are your keys. Good night!", "1階の、庭のとなりです。お部屋の鍵です。おやすみなさい！",
         "*Thank* *you*. *Good* *night*!", "ありがとう。おやすみなさい！")],
        [("reservation", "予約"), ("check out", "チェックアウトする"), ("floor", "階"), ("breakfast", "朝食"), ("key", "鍵")])

    d('doh_city_h2', '同じホテルのお客さん', 'chotel', 'c_guest', 'ロビーのソファ。となりのお客さんが、地図をのぞきこんでいる。', [
        ("Hi. Are you staying here too?", "こんにちは。ここに泊まっているのですか。",
         "*Yes*. *We* *just* *arrived*.", "はい。着いたばかりです。"),
        ("Are you hungry? I know a good place for dinner.", "おなかはすいていますか。夕食にいい店を知っていますよ。",
         "*Yes*, *very* *hungry*! *Where* *is* *it*?", "はい、とても！どこですか。"),
        ("It is in the souq, near the main street. The grilled fish is great.", "スークの中の、大通りの近くです。焼き魚がおいしいですよ。",
         "*Grilled* *fish*. *Is* *it* *expensive*?", "焼き魚。高いですか。"),
        ("Not too expensive. But it is busy. Go early.", "それほど高くないです。でも混んでいます。早めに行って。",
         "*Okay*. *We* *will* *go* *now*.", "わかりました。今から行きます。"),
        ("Have a nice dinner. Tell them a friend sent you!", "よい夕食を。友だちに聞いたと言ってくださいね！",
         "*Ha*! *We* *will*. *Thank* *you*!", "はは！そうします。ありがとう！")],
        [("staying", "泊まっている"), ("hungry", "おなかがすいた"), ("dinner", "夕食"), ("expensive", "値段が高い"), ("early", "早めに")], kind='trav')

    d('doh_city_s1', '香辛料の店の人', 'csouq', 'c_spice', 'スークの香辛料の店。袋の山から、いろんな香りがする。', [
        ("Welcome! Come in, come in. Smell this.", "いらっしゃい！どうぞ中へ。これをかいでみて。",
         "*Wow*, *it* *smells* *good*. *What* *is* *it*?", "わあ、いい香り。何ですか。"),
        ("Cardamom. We put it in coffee and tea.", "カルダモンです。コーヒーや紅茶に入れます。",
         "*Can* *I* *taste* *a* *little*?", "少し味見できますか。"),
        ("Of course. Try this mix for rice, too.", "もちろん。ごはん用のミックスもどうぞ。",
         "*Mmm*. *It* *is* *a* *little* *spicy*.", "うーん。少しからいです。"),
        ("Only a little! Which one do you want?", "ほんの少しだけです！どれにしますか。",
         "*One* *small* *bag* *of* *cardamom*, *please*.", "カルダモンを小さい袋で1つください。"),
        ("Ten riyals. It is a good gift for your family.", "10リヤルです。ご家族へのいいおみやげですよ。",
         "*Here* *you* *are*. *Thank* *you*!", "どうぞ。ありがとう！")],
        [("smell", "においをかぐ"), ("cardamom", "カルダモン"), ("taste", "味見する"), ("spicy", "からい"), ("gift", "おみやげ・贈り物")])

    d('doh_city_s2', '布の店の人', 'csouq', 'c_cloth', '布の店。色とりどりのスカーフが、天井までかかっている。', [
        ("Good evening. Please, look around.", "こんばんは。どうぞ見ていってください。",
         "*These* *colors* *are* *beautiful*. *May* *I* *take* *a* *photo*?", "色がきれいですね。写真をとってもいいですか。"),
        ("Photos of the shop are fine. But please do not take photos of people.", "お店の写真はかまいません。でも、人の写真はとらないでください。",
         "*Of* *course*. *Just* *the* *scarves*.", "もちろん。スカーフだけです。"),
        ("Thank you. Are you looking for a gift?", "ありがとうございます。おみやげをおさがしですか。",
         "*Maybe*. *Do* *you* *have* *a* *light* *scarf*?", "たぶん。うすいスカーフはありますか。"),
        ("This one is light and soft. It is good for the sun.", "これはうすくてやわらかいです。日よけにいいですよ。",
         "*It* *is* *nice*. *But* *I* *will* *think* *about* *it*.", "すてきです。でも少し考えます。"),
        ("No problem. Take your time. My shop is always here.", "大丈夫です。ごゆっくり。店はいつもここにあります。",
         "*Thank* *you*. *See* *you* *later*!", "ありがとう。またあとで！")],
        [("look around", "見て回る"), ("scarf", "スカーフ"), ("light", "軽い・うすい"), ("think about", "〜について考える"), ("take your time", "ごゆっくり")])

    d('doh_city_s3', 'みやげ物の店の人', 'csouq', 'c_souv', 'みやげ物の店。小さなランプや、木の箱がならんでいる。', [
        ("Hello, hello! Souvenirs for your friends?", "こんにちは！お友だちへのおみやげですか。",
         "*Yes*. *Something* *small* *from* *Qatar*.", "はい。カタールの小さいものを。"),
        ("How about this small wooden box? It is made by hand.", "この小さな木の箱はどうですか。手作りです。",
         "*It* *is* *pretty*. *How* *much* *is* *it*?", "かわいいですね。いくらですか。"),
        ("Thirty riyals. But for you, twenty-five.", "30リヤル。でもあなたには25で。",
         "*Can* *you* *do* *twenty*?", "20にできますか。"),
        ("Twenty? Hmm... Okay, twenty-two. Last price!", "20？うーん…じゃあ22。これ以上は無理！",
         "*Deal*! *Here* *you* *are*.", "決まり！どうぞ。"),
        ("Thank you, my friend. Come again!", "ありがとう、友よ。またどうぞ！",
         "*Thank* *you*. *Goodbye*!", "ありがとう。さようなら！")],
        [("souvenir", "おみやげ"), ("made by hand", "手作りの"), ("pretty", "かわいい"), ("deal", "決まり（取り引き成立）"), ("last price", "最後の値段")])

    d('doh_city_r1', 'レストランの店員', 'crest', 'c_waiter', 'スークの中のレストラン。外の席に、夜風がきもちいい。', [
        ("Good evening. A table for two?", "こんばんは。お二人ですか。",
         "*Yes*, *two*, *please*. *Can* *we* *sit* *outside*?", "はい、二人です。外の席に座れますか。"),
        ("Sure, this way. Here is the menu.", "はい、こちらへ。メニューです。",
         "*What* *is* *popular* *here*?", "ここでは何が人気ですか。"),
        ("The grilled fish, and the lamb with rice.", "焼き魚と、羊肉のごはんです。",
         "*The* *grilled* *fish*, *please*. *A* *friend* *told* *us* *about* *it*.", "焼き魚をお願いします。友だちに聞いたんです。"),
        ("Good choice. Anything to drink?", "いい選択です。お飲み物は？",
         "*Two* *lemon* *mint* *juices*, *please*.", "レモンミントジュースを2つお願いします。"),
        ("Coming soon. Enjoy your evening.", "すぐにお持ちします。よい夜を。",
         "*Thank* *you*. *It* *smells* *great* *here*.", "ありがとう。ここはいいにおい。")],
        [("table for two", "二人用の席"), ("outside", "外で"), ("lamb", "羊の肉"), ("anything to drink", "何か飲み物"), ("coming soon", "すぐ来る")])

    d('doh_city_r2', 'となりの席の家族', 'crest', 'c_family', '長いテーブル。となりの家族が、笑顔で話しかけてきた。', [
        ("Hello! Where are you from?", "こんにちは！どちらから？",
         "*We* *are* *from* *Japan*.", "日本からです。"),
        ("Japan! Welcome. Did you fly here from Japan?", "日本！ようこそ。日本からここへ飛んできたのですか。",
         "*No*. *We* *came* *from* *Nairobi*, *in* *Kenya*.", "いいえ。ケニアのナイロビから来ました。"),
        ("Nairobi! How was the food there?", "ナイロビ！食べ物はどうでしたか。",
         "*It* *was* *good*. *We* *had* *a* *lot* *of* *coffee*.", "おいしかったです。コーヒーをたくさん飲みました。"),
        ("Here, please try our bread too. It is still warm.", "ほら、うちのパンも食べてみて。まだあたたかいですよ。",
         "*Thank* *you*. *It* *is* *so* *soft*!", "ありがとう。とてもやわらかい！"),
        ("Enjoy your time in Doha. Come back again!", "ドーハを楽しんで。また来てくださいね！",
         "*We* *will*. *Thank* *you* *for* *the* *bread*!", "また来ます。パンをありがとう！")],
        [("food", "食べ物"), ("a lot of", "たくさんの"), ("try", "食べてみる・試す"), ("still", "まだ"), ("warm", "あたたかい")], kind='trav')

    d('doh_city_r3', 'レストランの店員', 'crest', 'c_waiter2', '食べ終わった。お会計の紙が、テーブルにとどいた。', [
        ("How was everything?", "いかがでしたか。",
         "*It* *was* *delicious*. *Can* *we* *have* *the* *bill*, *please*?", "とてもおいしかったです。お会計をお願いします。"),
        ("Of course. Here it is. Ninety riyals.", "かしこまりました。こちらです。90リヤルです。",
         "*Ninety*? *Let* *me* *check*.", "90？確認させてください。"),
        ("Take your time.", "ごゆっくりどうぞ。",
         "*Sorry*, *I* *think* *this* *juice* *is* *not* *ours*.", "すみません、このジュースは私たちのではないと思います。"),
        ("Oh, you are right. I am sorry. It is eighty riyals.", "あっ、そのとおりです。失礼しました。80リヤルです。",
         "*No* *problem*. *Can* *I* *pay* *by* *card*?", "大丈夫です。カードで払えますか。"),
        ("Yes. Thank you for telling me. Have a good night!", "はい。教えてくださってありがとうございます。おやすみなさい！",
         "*Thank* *you*. *Good* *night*!", "ありがとう。おやすみなさい！")],
        [("bill", "お会計・伝票"), ("check", "確かめる"), ("ours", "私たちのもの"), ("right", "正しい"), ("pay by card", "カードで払う")])

    # =====================================================================================
    # 状態シート（市内・2日目の朝）
    #   場所: ホテルの朝食の部屋とフロント → コルニーシュ（ドーハ湾ぞいの三日月形の遊歩道）
    #   時刻: 翌朝。午後の便で出発。あいさつは Good morning
    #   ルル: いる
    #   持ち物: スーツケース（フロントにあずける）、おみやげ（木のキリンは持っている人だけ）
    #   再登場フレーズ: 1泊だけ／焼き魚／ナイロビ（最初の寄港地）
    #   禁止: 実在の値段（舟の料金は架空）／くつをぬぐ等の未確認の決まり／個人名
    # =====================================================================================
    d('doh_city_h3', '朝食のとなりのお客さん', 'cbreak', 'c_break', 'ホテルの朝食の部屋。窓から朝の光。となりの人が、コーヒーを手にほほえんだ。', [
        ("Good morning! Did you sleep well?", "おはようございます！よく眠れましたか。",
         "*Yes*, *very* *well*. *The* *bed* *was* *great*.", "はい、とても。ベッドがよかったです。"),
        ("Good. Is this your first time in Doha?", "よかった。ドーハは初めてですか。",
         "*Yes*. *We* *only* *have* *one* *night* *here*.", "はい。ここには1泊だけなんです。"),
        ("One night! Then you must see the sea before you go.", "1泊！それなら出発前に海を見なくちゃ。",
         "*The* *sea*? *Is* *it* *close*?", "海？近いですか。"),
        ("Yes. Walk along the Corniche. It is beautiful in the morning.", "はい。コルニーシュを歩いてみて。朝はきれいですよ。",
         "*The* *Corniche*. *We* *will* *go* *after* *breakfast*.", "コルニーシュですね。朝ごはんのあとに行きます。"),
        ("Try the dates, too. They are very sweet!", "デーツも食べてみて。とてもあまいですよ！",
         "*Mmm*. *They* *are* *delicious*!", "うーん。おいしい！")],
        [("sleep well", "よく眠る"), ("first time", "初めて"), ("sea", "海"), ("walk along", "〜にそって歩く"), ("dates", "デーツ（なつめやしの実）")], kind='trav')

    d('doh_city_h4', 'ホテルのフロント係', 'cbreak', 'c_front2', 'チェックアウトの時間。フロントの人が、にこやかに顔を上げた。', [
        ("Good morning. How can I help you?", "おはようございます。ご用件は？",
         "*We* *are* *checking* *out* *now*. *Can* *you* *keep* *our* *suitcase*?", "今チェックアウトします。スーツケースをあずかってもらえますか。"),
        ("Of course. When will you come back for it?", "もちろんです。いつ取りにもどりますか。",
         "*Around* *eleven*. *We* *want* *to* *walk* *by* *the* *sea*.", "11時ごろです。海ぞいを歩きたいので。"),
        ("No problem. Is there anything fragile inside?", "問題ありません。中にこわれやすいものはありますか。",
         "*Yes*. *There* *is* *a* *small* *souvenir*.", "はい。小さなおみやげがあります。"),
        ("I will put it on the top shelf. Here is your ticket.", "いちばん上の棚に置きますね。こちらが引換券です。",
         "*Thank* *you*. *Should* *I* *keep* *this* *ticket*?", "ありがとう。この券は持っておくのですか。"),
        ("Yes, please. Show it to me when you come back.", "はい、お願いします。もどったときに見せてください。",
         "*Okay*. *See* *you* *at* *eleven*!", "わかりました。11時に！")],
        [("keep", "あずかる・持っておく"), ("come back for", "取りにもどる"), ("fragile", "こわれやすい"), ("shelf", "棚"), ("show", "見せる")])

    d('doh_city_c1', '散歩中の人', 'ccorn', 'c_walker', 'コルニーシュ。三日月の形の湾にそって、遊歩道がつづく。', [
        ("Good morning! Beautiful day, isn't it?", "おはようございます！いい天気ですね。",
         "*Yes*! *Excuse* *me*, *could* *you* *take* *our* *picture*?", "はい！すみません、私たちの写真をとってもらえますか。"),
        ("Of course. With the boats, or with the tall buildings?", "もちろん。舟と？それとも高いビルと？",
         "*With* *the* *buildings*, *please*.", "ビルといっしょにお願いします。"),
        ("Okay. Please move a little to the right.", "はい。少し右へ動いてください。",
         "*Here*? *Is* *this* *okay*?", "ここですか。これでいいですか。"),
        ("Perfect. Smile! One, two, three!", "完ぺき。笑って！1、2、3！",
         "*Can* *you* *take* *one* *more*, *please*?", "もう1枚とってもらえますか。"),
        ("Sure. Done! You both look very happy.", "いいですよ。はい！おふたりとも、とても楽しそう。",
         "*Thank* *you* *so* *much*!", "本当にありがとう！")],
        [("beautiful day", "いい天気の日"), ("picture", "写真"), ("tall buildings", "高いビル"), ("move", "動く"), ("one more", "もう1つ・もう1枚")], kind='trav')

    d('doh_city_c2', '舟の人', 'ccorn', 'c_boat', '湾に木の舟（ダウ）がならんでいる。舟の人が手まねきしている。', [
        ("Hello! Boat ride? Thirty minutes around the bay.", "こんにちは！舟に乗りませんか。湾を30分まわります。",
         "*How* *much* *is* *it* *for* *two*?", "二人でいくらですか。"),
        ("Fifty riyals for two people.", "二人で50リヤルです。",
         "*When* *does* *the* *next* *boat* *leave*?", "次の舟はいつ出ますか。"),
        ("In ten minutes. Please wait here, by the steps.", "10分後です。ここの階段のそばでお待ちください。",
         "*Okay*. *Is* *there* *a* *life* *jacket*?", "わかりました。救命胴衣はありますか。"),
        ("Yes, for everyone. Safety first!", "はい、全員分あります。安全が第一！",
         "*Good*. *Can* *we* *see* *the* *tall* *buildings* *from* *the* *boat*?", "よかった。舟から高いビルが見えますか。"),
        ("Yes, the best view! Here, step in slowly.", "はい、いちばんの景色ですよ！どうぞ、ゆっくり乗って。",
         "*Thank* *you*. *This* *is* *exciting*!", "ありがとう。わくわくする！")],
        [("boat ride", "舟に乗ること"), ("bay", "湾"), ("next", "次の"), ("life jacket", "救命胴衣"), ("step in", "乗りこむ")])

    d('doh_city_c3', '英語を練習している学生', 'ccorn', 'c_student', 'ベンチの学生が、ノートを閉じて話しかけてきた。', [
        ("Hello! May I practice my English with you?", "こんにちは！英語の練習をさせてもらってもいいですか。",
         "*Sure*! *My* *English* *is* *not* *perfect*, *too*.", "もちろん！私の英語も完ぺきじゃないけど。"),
        ("That's okay! Where are you from?", "大丈夫！どちらから？",
         "*I'm* *from* *Japan*. *I'm* *traveling* *around* *the* *world*.", "日本からです。世界一周の旅をしています。"),
        ("Wow! How long is your trip?", "わあ！旅はどのくらいの長さですか。",
         "*About* *one* *month*. *Doha* *is* *our* *second* *stop*.", "1か月くらいです。ドーハは2番目の立ち寄り先です。"),
        ("Your English is good! What was your favorite food here?", "英語上手ですよ！ここで好きだった食べ物は？",
         "*The* *grilled* *fish*, *and* *the* *sweet* *tea*.", "焼き魚と、あまいお茶です。"),
        ("Me too! Thank you for talking with me. Good luck!", "ぼくも！話してくれてありがとう。がんばって！",
         "*Thank* *you*. *Good* *luck* *with* *your* *English*!", "ありがとう。英語、がんばってね！")],
        [("practice", "練習する"), ("second", "2番目の"), ("month", "1か月"), ("favorite", "いちばん好きな"), ("good luck", "がんばって・幸運を")], kind='trav')

    # =====================================================================================
    # 状態シート（出発・2日目の午後）
    #   場所: ハマド国際空港。カウンター → 出国審査 → 南の広場（クマ）→ 空港の列車 → 北の広場（木々）・ラウンジ入口 → ゲート → 機内
    #   時刻: 2日目の午後。あいさつは Good afternoon。行き先はヘルシンキ（航空会社・便名・時刻は出さない）
    #   ルル: いる
    #   持ち物: スーツケース（カウンターで預ける）、おみやげ、あたたかい上着（かばんの中）
    #   再登場: ナイロビのラウンジの客（nbo_lounge2 を遊んだ人だけ再会）／赤いリボンの旅行者（doh_bag2 を遊んだ人だけ、ゲートで）
    #   禁止: 国名・情勢の話（予定の変更だけ）／クマの色・絵／ラウンジ名／指紋の手順／「東京へ行く」
    # =====================================================================================
    d('doh_dep_checkin', 'チェックインの係員', 'dcheck', 'd_ck', 'ハマド国際空港の出発カウンター。天井が高く、しずかで広い。', [
        ("Good afternoon. Where are you flying today?", "こんにちは。今日はどちらへ？",
         "*We* *are* *flying* *to* *Helsinki*.", "ヘルシンキへ行きます。"),
        ("Helsinki. May I see your passports, please?", "ヘルシンキですね。パスポートを拝見できますか。",
         "*Here* *you* *are*. *Two* *passports*.", "どうぞ。2冊です。"),
        ("Thank you. Is this suitcase going to Helsinki too?", "ありがとうございます。このスーツケースもヘルシンキまでですか。",
         "*Yes*. *Just* *one* *suitcase*.", "はい。スーツケース1つだけです。"),
        ("It is a little heavy, but it is fine. Did you pack it yourself?", "少し重いですが、大丈夫です。ご自分で荷造りしましたか。",
         "*Yes*, *I* *did*. *There* *are* *some* *souvenirs* *inside*.", "はい、自分でしました。中におみやげが入っています。"),
        ("Very good. Here are your boarding passes. Passport control is on the left.", "けっこうです。搭乗券です。出国審査は左側です。",
         "*On* *the* *left*. *Thank* *you* *very* *much*.", "左ですね。ありがとうございます。")],
        [("pack", "荷造りする"), ("yourself", "自分で"), ("inside", "中に"), ("passport control", "出入国審査"), ("on the left", "左側に")])

    d('doh_dep_passport', '出国審査の係官', 'dimmig', 'd_exit', '出国審査。係官は、きのうと同じように短くていねいに話す。', [
        ("Good afternoon. Passport and boarding pass.", "こんにちは。パスポートと搭乗券を。",
         "*Here* *they* *are*.", "どうぞ。"),
        ("You arrived yesterday. You are leaving already?", "昨日着いたのですね。もう出発ですか。",
         "*Yes*. *It* *was* *a* *short* *stay*, *but* *we* *loved* *it*.", "はい。短い滞在でしたが、とても気に入りました。"),
        ("What did you see in Doha?", "ドーハでは何を見ましたか。",
         "*We* *saw* *the* *old* *market* *and* *the* *sea*.", "古い市場と海を見ました。"),
        ("Good. Please look at the camera one more time.", "よろしい。もう一度カメラを見てください。",
         "*One* *more* *time*. *Okay*.", "もう一度ですね。はい。"),
        ("Thank you. Have a safe flight. Come back to Qatar.", "ありがとうございます。よい空の旅を。またカタールへ。",
         "*We* *will*. *Goodbye*!", "また来ます。さようなら！")],
        [("already", "もう"), ("short stay", "短い滞在"), ("loved", "とても気に入った"), ("one more time", "もう一度"), ("come back", "戻ってくる")])

    d('doh_dep_bear', '写真をたのむ旅行者', 'dsouth', 'd_photo', '南の広場。大きなクマの前で、旅行者がスマホを手にこまっている。', [
        ("Excuse me. Could you take a photo of us?", "すみません。写真をとってもらえますか。",
         "*Sure*. *With* *the* *big* *bear*?", "いいですよ。大きなクマといっしょに？"),
        ("Yes, please! We want the whole bear in the picture.", "はい、お願いします！クマが全部入るように。",
         "*Okay*. *Stand* *a* *little* *closer*.", "はい。もう少し寄ってください。"),
        ("Like this? Can you see all of us?", "こうですか。全員入っていますか。",
         "*Yes*. *Ready*? *One*, *two*, *three*!", "はい。いいですか。1、2、3！"),
        ("Thank you! Let me see. Oh, it is perfect!", "ありがとう！見せて。わあ、ばっちり！",
         "*I'm* *glad*. *Where* *are* *you* *going*?", "よかった。どちらへ行くんですか。"),
        ("We are going home. And you?", "家に帰るところです。あなたは？",
         "*We* *are* *going* *to* *Helsinki*. *Have* *a* *safe* *trip*!", "ヘルシンキへ行きます。気をつけて！")],
        [("take a photo", "写真をとる"), ("closer", "もっと近くに"), ("all of us", "私たち全員"), ("perfect", "完ぺきな"), ("going home", "家に帰る")], kind='trav')

    d('doh_dep_train', '乗りあわせた人', 'dtrain', 'd_trainp', '空港の中の列車の乗り場。となりの人が、案内の表示を見上げている。', [
        ("Excuse me. Is this the train to the north side?", "すみません。これは北側へ行く列車ですか。",
         "*I* *think* *so*. *We* *are* *going* *to* *our* *gate*, *too*.", "そうだと思います。私たちもゲートへ行くところです。"),
        ("Good. Is your gate far from here?", "よかった。ゲートはここから遠いですか。",
         "*Yes*. *The* *sign* *said*, *take* *the* *train*.", "はい。案内に『列車に乗って』とありました。"),
        ("The ride is very short. Look, here it comes!", "乗っている時間はとても短いですよ。ほら、来ました！",
         "*Wow*. *A* *train* *inside* *the* *airport*!", "わあ。空港の中に列車！"),
        ("Please hold on to the bar.", "手すりにつかまってくださいね。",
         "*Okay*. *Thank* *you* *for* *the* *tip*.", "わかりました。教えてくれてありがとう。"),
        ("Here we are. This is the north side. Have a good flight!", "着きました。ここが北側です。よい空の旅を！",
         "*You* *too*! *Bye*!", "あなたも！さようなら！")],
        [("north", "北"), ("sign", "案内の表示"), ("short", "短い"), ("hold on", "つかまる"), ("bar", "手すり")], kind='trav')

    d('doh_dep_orchard', 'ベンチの旅行者', 'dorch', 'd_bench', '北の広場。空港の中に、本物の木がならんでいる。ベンチで休もう。', [
        ("Is anyone sitting here?", "ここ、だれか座っていますか。",
         "*No*. *Please*, *sit* *down*.", "いいえ。どうぞ座ってください。"),
        ("Thank you. It is nice here. Real trees inside an airport!", "ありがとう。ここはいいですね。空港の中に本物の木が！",
         "*I* *know*! *It* *feels* *like* *a* *park*.", "そうですよね！公園みたいです。"),
        ("How long is your wait?", "待ち時間はどのくらいですか。",
         "*About* *two* *hours*. *And* *you*?", "2時間くらいです。あなたは？"),
        ("Five hours! I will sleep a little.", "5時間！少し寝ます。",
         "*Five* *hours*? *That* *is* *long*.", "5時間？長いですね。"),
        ("It is okay. This is a good place to rest. Enjoy your trip!", "大丈夫。ここは休むのにいい場所です。よい旅を！",
         "*Thank* *you*. *Have* *a* *good* *rest*!", "ありがとう。ゆっくり休んでね！")],
        [("anyone", "だれか"), ("real", "本物の"), ("feels like", "〜のような感じがする"), ("wait", "待ち時間"), ("rest", "休む")], kind='trav')

    d('doh_dep_lounge', 'ラウンジの前の旅行者', 'dlng', 'lounge_guest', 'ラウンジの前。オレンジの上着の人が、こちらを見て手をふった。', [
        ("Hello. You look a little lost. Are you looking for the lounge?", "こんにちは。少し迷っているようですね。ラウンジをさがしていますか。",
         "*Yes*. *I* *cannot* *find* *the* *door*.", "はい。入口が見つかりません。"),
        ("Many people cannot find the door here. This is not the door. Please follow me.", "ここでは入口を見つけられない人が多いんです。ここは入口ではありません。ついてきてください。",
         "*Thank* *you*. *Is* *it* *far*?", "ありがとう。遠いですか。"),
        ("No, it is close. Where are you flying next?", "いいえ、近いです。次はどこへ飛びますか。",
         "*We* *are* *flying* *to* *Helsinki* *today*.", "今日、ヘルシンキへ飛びます。"),
        ("Helsinki! It is cold there in winter. Do you have a warm coat?", "ヘルシンキ！冬は寒いですよ。あたたかい上着はありますか。",
         "*Yes*, *it* *is* *in* *my* *bag*.", "はい、かばんに入っています。"),
        ("Good. Here is the door. Safe travels, my friend!", "よかった。ここが入口です。よい旅を、友よ！",
         "*Thank* *you* *for* *your* *help*!", "助けてくれてありがとう！")],
        [("lost", "迷った"), ("follow", "ついていく"), ("close", "近い"), ("warm coat", "あたたかい上着"), ("safe travels", "よい旅を")], kind='trav')

    d('doh_dep_gate', '搭乗ゲートの係員', 'dgate', 'd_gate', 'ヘルシンキ行きのゲート。大きな窓の外に、飛行機が見える。', [
        ("Good afternoon. This is the gate for Helsinki. May I see your boarding pass?", "こんにちは。こちらはヘルシンキ行きのゲートです。搭乗券を見せていただけますか。",
         "*Here* *it* *is*. *Are* *we* *on* *time*?", "どうぞ。定刻どおりですか。"),
        ("There is a small change. Boarding will start fifteen minutes later.", "少し変更があります。搭乗は15分おそく始まります。",
         "*Fifteen* *minutes* *later*. *No* *problem*.", "15分おそくですね。問題ありません。"),
        ("Thank you for waiting. You can sit over there.", "お待たせしてすみません。あちらにお座りください。",
         "*Is* *there* *a* *restroom* *near* *here*?", "近くにお手洗いはありますか。"),
        ("Yes, just behind the gate, on the right.", "はい、ゲートのすぐ後ろ、右側です。",
         "*Thank* *you*. *I* *will* *go* *now* *and* *come* *back*.", "ありがとう。今行って、もどってきます。"),
        ("Please listen for the announcement. Have a nice flight.", "アナウンスをよく聞いていてくださいね。よい空の旅を。",
         "*I* *will*. *Thank* *you*!", "そうします。ありがとう！")],
        [("change", "変更"), ("later", "あとで・おそく"), ("restroom", "お手洗い"), ("behind", "〜の後ろに"), ("announcement", "アナウンス")])

    d('doh_dep_plane', 'となりの席のお客さん', 'dcabin', 'd_seat', '機内。ヘルシンキへ。自分の席にすわろうとしたら、となりの人が声をかけてきた。', [
        ("Hello. I think you are in my seat.", "こんにちは。そこ、私の席だと思います。",
         "*Oh*, *sorry*! *What* *is* *your* *seat* *number*?", "あっ、すみません！あなたの席番号は？"),
        ("It is the aisle seat. Look, here is my boarding pass.", "通路側の席です。ほら、これが私の搭乗券です。",
         "*You* *are* *right*. *My* *seat* *is* *the* *middle* *one*. *Sorry*!", "そのとおりです。私の席はまん中でした。すみません！"),
        ("No problem. Are you going to Helsinki for a holiday?", "大丈夫ですよ。ヘルシンキへは休暇ですか。",
         "*Yes*. *We* *are* *traveling* *around* *the* *world*.", "はい。世界一周の旅の途中です。"),
        ("Around the world! Where was your last stop?", "世界一周！前はどこにいたのですか。",
         "*Doha*. *We* *stayed* *one* *night* *near* *the* *old* *market*.", "ドーハです。古い市場の近くに1泊しました。"),
        ("Lovely. Helsinki will be cold, but you will like it. Enjoy!", "すてきですね。ヘルシンキは寒いけど、きっと気に入りますよ。楽しんで！",
         "*Thank* *you*. *Goodbye*, *Doha*!", "ありがとう。さよなら、ドーハ！")],
        [("seat number", "座席番号"), ("middle", "まん中の"), ("holiday", "休暇"), ("last stop", "前の立ち寄り先"), ("stayed", "泊まった")], kind='trav')

    # =====================================================================================
    # 割りこみ（018 §4.3）と顔なじみ（018 §4.2）。014 の型：出来事が来る → ▶で選んで言う → 世界が反応する（1往復）
    # =====================================================================================
    # 割りこみ#1 スーク：祈りの呼びかけ。018 は「音だけ」。014 の部品は会話がないと動かないため、ルルとの1往復にした（音源は未作成）
    ev('doh_ev_h_prayer', 'Lulu', 'calley', 'lulu', [
        T("Listen, King. Can you hear that? It is the call to prayer.", "聞いて、キング。聞こえる？お祈りの呼びかけだよ。",
          "Yes, I can. Let's walk quietly for a moment.", "うん、聞こえる。少しのあいだ、しずかに歩こう。")],
        fx='ding')
    # 割りこみ#4 コルニーシュ：道をたずねられる（キングが答える側）。南の端はスーク・ワキーフの地区につながる（出典は上）
    ev('doh_ev_j_ask', 'Traveler', 'ccorn', 'ev_tourist', [
        OT("Excuse me. Do you know the way to Souq Waqif?", "すみません。スーク・ワキーフへの行き方を知っていますか。", [
            O('yes', "Yes! Walk that way, along the sea.", "はい！あっちです。海にそって歩いて。",
              rep=("Along the sea? Thank you so much!", "海にそって？ありがとうございます！")),
            O('tea', "Yes. Try the tea there. It's very good!", "はい。そこでお茶を飲んでみて。とてもおいしいですよ！",
              rep=("Ha! I will. Thank you!", "はは！そうします。ありがとう！")),
            O('again', "Sorry, could you say that again?", "すみません、もう一度言ってもらえますか。",
              rep=("Souq Waqif, the old market. Is it this way?", "スーク・ワキーフ、古い市場です。こっちですか。"))])],
        fx='ding')
    # 割りこみ#2 ゲート：館内放送。理由は「予定の変更」だけ（018 §3.2 #3。国名・情勢にはふれない）
    ev('doh_ev_i_board', 'Announcement', 'dgate', '', [
        OT("Attention, please. Passengers to Helsinki. Because of a schedule change, boarding will start at a new time. Please check the screen.",
           "お知らせします。ヘルシンキへ行くお客さまへ。予定の変更により、搭乗の時刻が変わります。画面をご確認ください。", [
            O('screen', "Let's check the screen.", "画面を見てみよう。",
              rep=("Thank you for waiting. Boarding will start fifteen minutes later.", "お待たせしております。搭乗は15分おそく始まります。", 'Announcement')),
            O('late', "Are we late?", "私たち、おくれてる？",
              rep=("No, you are not late. We just have more time to wait.", "いいえ、おくれていませんよ。待つ時間が少しふえただけです。", 'Traveler')),
            O('again', "Could you say that again, please?", "もう一度言っていただけますか。",
              rep=("Passengers to Helsinki. Please check the screen for the new boarding time.", "ヘルシンキへ行くお客さま。新しい搭乗時刻は画面でご確認ください。", 'Announcement'))])],
        fx='pa')
    # 顔なじみ：赤いリボンの旅行者（doh_bag2・014 の f1）。ドーハに住み、仕事で飛ぶ。doh_bag2 を遊んだ人だけ、ゲートで1回
    ev('doh_ev_k_ribbon', 'Traveler', 'dgate', 'd_traveler', [
        T("Hello again! Remember me? The blue suitcase!", "また会いましたね！覚えてる？青いスーツケースの！",
          "Yes! The red ribbon! Are you flying today, too?", "はい！赤いリボンの！あなたも今日飛ぶのですか。"),
        T("Yes, for work. Look, my ribbon is still on. Safe travels!", "ええ、仕事でね。見て、リボンはまだついてるの。よい旅を！",
          "You too! See you again someday!", "あなたも！またいつか！")],
        kind='short')


# ---- 持ち越し（014 の VARIANTS と同じ形）。(場面, 何番目の相手のセリフ(0から), 種の場面, 相手, 日本語, キング(なければNone), 日本語) ----
VARIANTS = [
    # #1 「1泊だけ」（doh_immig1 で言った）→ フロントが返す
    ('doh_city_h1', 1, 'doh_immig1',
     "Thank you. Only one night? That is short! Checking out tomorrow, right?", "ありがとうございます。1泊だけ？短いですね！明日チェックアウトですね。",
     "Yes. We fly to Helsinki tomorrow.", "はい。明日ヘルシンキへ飛びます。"),
    # #3 木のキリン（nbo_sec2）→ みやげ物の店の人が気づく／フロントで「こわれやすいもの」
    ('doh_city_s3', 1, 'nbo_sec2',
     "How about this small wooden box? Oh, is that a wooden giraffe in your bag?", "この小さな木の箱はどうですか。あれ、かばんの中のは木のキリンですか。",
     "Yes! It is from Kenya. How much is the box?", "はい！ケニアのです。箱はいくらですか。"),
    ('doh_city_h4', 2, 'nbo_sec2',
     "No problem. Is there anything fragile inside?", "問題ありません。中にこわれやすいものはありますか。",
     "Yes. There is a wooden giraffe. Please be careful.", "はい。木のキリンが入っています。気をつけてください。"),
    # #4 ニャマチョマ（nbo_java2 で教わった）→ 家族に「ナイロビの食べ物は？」ときかれて答える
    ('doh_city_r2', 2, 'nbo_java2',
     "Nairobi! How was the food there?", "ナイロビ！食べ物はどうでしたか。",
     "Great! We tried nyama choma. Grilled meat!", "最高！ニャマチョマを食べました。焼いた肉です！"),
    # #5 「ここが最初の寄港地」（nbo_art2）→ 学生が「最初の旅先ですか」ときく
    ('doh_city_c3', 2, 'nbo_art2',
     "Wow! How long is your trip? Is Doha your first stop?", "わあ！旅はどのくらいですか。ドーハが最初の旅先ですか。",
     "No. Nairobi was the first. Doha is the second.", "いいえ。最初はナイロビ。ドーハは2番目です。"),
    # #6 ナイロビのラウンジの客（nbo_lounge2）→ 再会（顔なじみ）
    ('doh_dep_lounge', 0, 'nbo_lounge2',
     "Hello! I know you. We met at the lounge in Nairobi, right?", "こんにちは！知っていますよ。ナイロビのラウンジで会いましたよね。",
     "Yes! You said safari njema. Hello again!", "はい！「サファリ・ンジェマ」と言ってくれましたね。また会いましたね！"),
    ('doh_dep_lounge', 1, 'nbo_lounge2',
     "Ha, yes! I fly through Doha a lot. Are you looking for the lounge? This is not the door. Please follow me.",
     "ははは、そう！ドーハはよく通るんです。ラウンジをさがしていますか。ここは入口ではありません。ついてきてください。", None, None),
    ('doh_dep_lounge', 4, 'nbo_lounge2',
     "Good. Here is the door. Safe travels, my friend!", "よかった。ここが入口です。よい旅を、友よ！",
     "Thank you. Safari njema to you!", "ありがとう。あなたもサファリ・ンジェマ！"),
]

# ---- 置き場（014 の SLOTS と同じ形）。key は場所のID ----
SLOTS = [
    dict(id='h', vid='doh_ev_h_prayer', at='enter', key='calley', sign=1),
    dict(id='j', vid='doh_ev_j_ask', at='enter', key='ccorn', sign=1),
    dict(id='k', vid='doh_ev_k_ribbon', at='enter', key='dgate', sign=0, need='doh_bag2'),
    dict(id='i', vid='doh_ev_i_board', at='enter', key='dgate', sign=1),
]
