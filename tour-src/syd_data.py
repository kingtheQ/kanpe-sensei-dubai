# -*- coding: utf-8 -*-
# 世界一周編 シドニー(タスク102。到着4場面＋街3場面＋出発3場面。クロが執筆)。国ごとのデータは別ファイル(fra_data.py と同じ形)。
#
# 会話の型は fra_data.py と同じ新形式(flow2=1・cards=1): 相手が英語で話す → 選ぶのは1場面に1回だけ(日本語の短い言葉カード)
#   → お手本は音声だけ → カンペ → 声に出す。失敗時は074の統一ルール(自動おてほん→言い直し→3回目でルルが代わりに言って進む)。
#   どのカードを選んでも物語は進む(止めない・合否なし)。日本語は「カードの言葉」「Meaning!(訳)」にだけ置く。
#
# 雰囲気(PM指示): シドニーのスタッフは「明るく気さく。No worries と言ってくれる」。検疫の係員だけは、やさしいが決まりには厳しい。
#
# 使ってよい実在情報(確認日 2026-11-27。出典は docs/sources.md の「102」):
#   - SmartGate: キオスクでパスポートを読み取り、質問に答えて、チケットを受け取る → ゲートへ(2段階)。通れなければ係員(ABF)が窓口で対応。
#     チケット・パスポート・入国カード(紙のIncoming Passenger Card。デジタル申告は順次導入中)は手元に持っておく。
#   - 検疫(DAFF): すべて申告する。全部申告すれば、持ち込めない物でも罰はない。チョコレート・ビスケット・焼いたお菓子は持ち込める。
#     生の果物・干した果物(かんきつ・柿など)は持ち込めない。探知犬は荷物のそばに座って知らせる(受け身の探知)。
#   - 空港の駅: OpalカードもタッチのカードもAirport駅の「駅アクセス料」は同じ。空港の駅では最低チャージ額がある(台詞に金額は出さない)。
#   - 出発(T1国際線): 保安検査のあとに出国(パスポート)の確認。CTレーンはノートパソコンと液体を袋に入れたままにできる場合があるが、液体の量の上限はあり、レーンによって違う。
#     → 「指示書は、出国の機械のあとに保安」だが、実際の順番(保安が先)に合わせた。理由は docs/handover.md に書く。
# 台詞に出さないもの(指示書): 航空会社名・便名・未確認の数字(運賃・罰金額・商品の値段・時刻・ゲート番号)。数字(0〜9)は1つも入れない。
#   値段は「小さなタグ」「画面」と言う。ホテル名・店名は出さない。個人名なし。
#   探知犬は別素材で後から足す。台詞は係員との会話だけで成り立つ(犬のことは「犬が荷物のそばを通ることがある」と言葉でだけ触れる)。
import window_data as W
from window_data import star, OT

E = ''


def O(k, y, jp, card, ico, rep):
    return dict(k=k, y=star(y), jp=jp, card=card, ico=ico, rep=rep)


def T(n, njp, y, yjp, **kw):
    d = dict(n=n, njp=njp, y=star(y), yjp=yjp)
    d.update(kw)
    return d


# 声(SP)は build.py に置く: s_smart・s_abf・s_quar・s_train・s_barista・s_shop・s_front・s_check・s_sec・s_pcheck・s_board
def add(D):
    # =================== 到着 ===================
    D.append(dict(
        id='syd_immig1', who='SmartGateの係員', bg='simmig1', sp='s_smart',
        intro='シドニー空港の入国ホール。SmartGateのキオスクが並んでいる。係員が明るく声をかけてくれる。',
        pairs=[
            T("G'day! Welcome to Sydney. Are you using SmartGate today?",
              "こんにちは！シドニーへようこそ。今日はSmartGateを使いますか。",
              "Yes, we are. Is this the right line?", "はい。この列でいいですか。"),
            T("No worries. First, go to the kiosk. Scan your passport and answer the questions. Then take your ticket.",
              "大丈夫ですよ。まずキオスクへ。パスポートを読み取って、質問に答えます。そしてチケットを受け取ります。",
              "Then we go to the gate, right?", "そのあとゲートへ行くのですよね。"),
            OT("That's right. Keep the ticket with your passport. Do you need any help?",
               "そのとおり。チケットはパスポートと一緒に持っていてください。お手伝いは必要ですか。",
               [O('ok', "No, thank you. We have our passport and the card.", "いいえ、大丈夫です。パスポートとカードがあります。", "だいじょうぶ", "🛂",
                  ("Great. Off you go, then.", "いいですね。では、どうぞ。")),
                O('help', "Yes, please. Where does the passport go?", "はい、お願いします。パスポートはどこに置きますか。", "手伝って", "🙋",
                  ("Sure thing. Put the passport in the reader, photo page down. Then follow the screen.", "もちろん。パスポートは、写真のページを下にして読み取り機へ。あとは画面のとおりに。"))],
               cards=1, fork={'tw': ['passport']}),
            T("Good. Take your ticket. Then go to the gate. Look at the camera, and wait for the gate to open.",
              "いいですね。チケットを取って、ゲートへ。カメラを見て、ゲートが開くのを待ちます。",
              "Okay. Thank you.", "わかりました。ありがとう。"),
            T("If the gate says no, don't worry. An officer will help you. Enjoy Sydney!",
              "もしゲートが通れなくても、心配いりません。係員が手伝います。シドニーを楽しんで！",
              "Thank you. See you.", "ありがとう。ではまた。"),
        ],
        words=[("passport", "パスポート"), ("kiosk", "キオスク"), ("ticket", "チケット"), ("gate", "ゲート"), ("officer", "係員")],
        conv=1, flow2=1))

    D.append(dict(
        id='syd_immig2', who='入国の係員', bg='simmig2', sp='s_abf',
        intro='ゲートが開かなかったので、窓口へ。係員は気さくに話してくれる。',
        pairs=[
            T("Hi there. The gate did not open. No worries. Come to the desk.",
              "こんにちは。ゲートが開きませんでしたね。大丈夫です。窓口へどうぞ。",
              "Okay. Sorry about that.", "わかりました。すみません。"),
            T("No need to be sorry. It happens. Can I have your passport and your ticket?",
              "あやまらなくていいですよ。よくあることです。パスポートとチケットをお願いします。",
              "Here you are.", "どうぞ。"),
            OT("Thanks. Please look at the camera. And why are you visiting Australia?",
               "ありがとう。カメラを見てください。オーストラリアへは、何をしに来ましたか。",
               [O('holiday', "We are here on holiday. We want to visit Sydney.", "休暇で来ました。シドニーを訪ねたいです。", "休暇で", "🏖️",
                  ("Lovely. You picked a good place.", "いいですね。いい場所を選びましたね。")),
                O('friend', "We are here to visit a friend.", "友だちを訪ねに来ました。", "友だちに会う", "🤝",
                  ("Nice. Have a great time together.", "いいですね。楽しい時間を。"))],
               cards=1, fork={'tw': ['visit']}),
            T("And how long will you stay? Just tell me the days.",
              "どのくらい滞在しますか。日にちを教えてください。",
              "Only a few days. Then we fly to Singapore.", "ほんの数日です。そのあとシンガポールへ飛びます。"),
            T("All good. Keep your passport with you. The exit is this way. Welcome to Australia!",
              "問題ありません。パスポートは手元に。出口はこちらです。オーストラリアへようこそ！",
              "Thank you very much.", "どうもありがとうございます。"),
        ],
        words=[("gate", "ゲート"), ("desk", "窓口"), ("camera", "カメラ"), ("holiday", "休暇"), ("stay", "滞在する")],
        conv=1, flow2=1))

    D.append(dict(
        id='syd_quarantine1', who='検疫の係員', bg='squar', sp='s_quar',
        intro='荷物を受け取ったあとの検疫の列。係員はやさしいが、決まりにはきびしい。全部、正直に伝えれば大丈夫。',
        pairs=[
            T("Hello there. Welcome to Australia. Do you have anything to declare today?",
              "こんにちは。オーストラリアへようこそ。今日、申告するものはありますか。",
              "Yes. We have some food.", "はい。食べ物があります。"),
            T("Thank you for telling me. Do you have fruit, meat, or milk things? Or seeds, or wooden things?",
              "教えてくれてありがとう。果物、肉、乳製品はありますか。種や、木でできた物は。",
              "We have sweets from Japan. Chocolate and biscuits.", "日本のお菓子があります。チョコレートとビスケットです。"),
            OT("Chocolate and biscuits are fine. Anything else? Fresh fruit, or dried fruit?",
               "チョコレートとビスケットは大丈夫です。ほかには。生の果物や、干した果物は。",
               [O('persimmon', "Yes. We want to declare dried persimmons.", "はい。干し柿を申告したいです。", "干し柿", "🍊",
                  ("Thank you for telling me. We have to keep that one today. But you told me, so no problem at all.", "教えてくれてありがとう。それは今日、預かります。でも、申告してくれたので、まったく問題ありません。")),
                O('none', "No fruit. We want to declare only the chocolate.", "果物はありません。チョコレートだけ申告したいです。", "チョコだけ", "🍫",
                  ("Great. Thanks for telling me. That is all good.", "いいですね。教えてくれてありがとう。それで大丈夫です。"))],
               cards=1, fork={'tw': ['declare']}),
            T("Good job telling me everything. Please put your bag on the table. I will take a quick look.",
              "全部話してくれて、えらいです。かばんをテーブルにのせてください。さっと見ます。",
              "Sure. Here you are.", "はい。どうぞ。"),
            T("All done. Thank you. Sometimes a dog walks by the bags. That is normal. Enjoy your stay!",
              "終わりです。ありがとう。ときどき、犬が荷物のそばを通ります。ふつうのことです。ご滞在を楽しんで！",
              "Thank you. Goodbye.", "ありがとう。さようなら。"),
        ],
        words=[("declare", "申告する"), ("food", "食べ物"), ("chocolate", "チョコレート"), ("fruit", "果物"), ("bag", "かばん")],
        conv=1, flow2=1))

    D.append(dict(
        id='syd_train1', who='駅の係員', bg='strain', sp='s_train',
        intro='空港の地下の駅。券売機と改札が並んでいる。係員が、街への行き方を教えてくれる。',
        pairs=[
            T("G'day! Where are you headed today?",
              "こんにちは！今日はどちらへ。",
              "We are going to the city. Which way do we go?", "街へ行きます。どちらへ行けばいいですか。"),
            T("Easy. Go down to the trains. Follow the signs for City. The trains come often.",
              "かんたんです。電車のところへ降りて。「City」の案内に従って。電車はよく来ます。",
              "Do we need a ticket?", "切符は必要ですか。"),
            OT("You can use a card or a phone. Tap on at the gate, and tap off at the end. Or you can buy an Opal card.",
               "カードやスマホが使えます。入るときにタッチして、最後にもタッチ。オパールカードを買ってもいいですよ。",
               [O('card', "We will tap on with my card.", "私のカードでタッチして入ります。", "カードで", "💳",
                  ("Great. Tap on here, and tap off at the other end. The airport station has a small extra fee. The gate adds it for you.", "いいですね。ここでタッチして、着いた先でもタッチ。空港の駅には小さな追加料金があります。改札が足してくれます。")),
                O('opal', "We will buy an Opal card and tap on.", "オパールカードを買って、タッチして入ります。", "オパール", "🎫",
                  ("Okay. The machine is over there. At the airport you add a little more money first.", "わかりました。機械はあちらです。空港では、最初に少し多めにチャージします。"))],
               cards=1, fork={'tw': ['tap']}),
            T("Which stop do you need? Check the screen on the train.",
              "どの駅で降りますか。電車の中の画面で確かめてください。",
              "We need the stop for the city.", "街の駅で降ります。"),
            T("Good. Stay back from the edge when the train comes. Have a good one!",
              "いいですね。電車が来るときは、ホームのはしから下がって。いい一日を！",
              "Thank you. You too.", "ありがとう。あなたも。"),
        ],
        words=[("station", "駅"), ("train", "電車"), ("tap on", "タッチして入る"), ("card", "カード"), ("stop", "停車駅")],
        conv=1, flow2=1))

    # =================== 街 ===================
    D.append(dict(
        id='syd_cafe1', who='バリスタ', bg='scafe', sp='s_barista',
        intro='シドニーの街角のカフェ。カウンターの向こうで、バリスタが明るく手を振っている。',
        pairs=[
            T("Hi there! What can I get for you?",
              "いらっしゃい！何にしますか。",
              "Hello. What do you recommend?", "こんにちは。おすすめは何ですか。"),
            T("The flat white is very popular here. It is a small, smooth coffee with milk.",
              "ここではフラット・ホワイトがとても人気です。小さくて口当たりのよい、ミルク入りのコーヒーです。",
              "That sounds good. Is it strong?", "おいしそうです。濃いですか。"),
            OT("Not too strong. Would you like a flat white, or a hot chocolate?",
               "そんなに濃くないですよ。フラット・ホワイトにしますか、ホットチョコレートにしますか。",
               [O('flat', "Two flat whites, please.", "フラット・ホワイトを二つ、お願いします。", "フラット・ホワイト", "☕",
                  ("Two flat whites. Coming up!", "フラット・ホワイトが二つ。すぐできます！")),
                O('choc', "Two hot chocolates, please.", "ホットチョコレートを二つ、お願いします。", "ホットチョコ", "🍫",
                  ("Two hot chocolates. Good choice!", "ホットチョコレートが二つ。いい選択です！"))],
               cards=1, fork={'tw': ['please']}),
            T("Here or takeaway?",
              "ここで飲みますか、持ち帰りですか。",
              "Takeaway, please.", "持ち帰りでお願いします。"),
            T("No worries. It will be ready soon. The total is on the screen. Have a good one!",
              "大丈夫です。すぐできます。合計は画面に出ています。いい一日を！",
              "Thanks. You too.", "ありがとう。あなたも。"),
        ],
        words=[("recommend", "すすめる"), ("flat white", "フラット・ホワイト"), ("hot chocolate", "ホットチョコレート"), ("takeaway", "持ち帰り"), ("milk", "ミルク")],
        conv=1, flow2=1))

    D.append(dict(
        id='syd_shop1', who='おみやげ屋の店員', bg='sshop', sp='s_shop',
        intro='港の近くのおみやげ屋。コアラやカンガルーのぬいぐるみが並んでいる。店員は気さくに話しかけてくれる。',
        pairs=[
            T("G'day! Are you looking for a souvenir?",
              "こんにちは！おみやげをお探しですか。",
              "Yes. What do people usually buy?", "はい。みなさん、ふつう何を買いますか。"),
            T("Many people buy a toy, or a postcard. Small things for friends at home.",
              "ぬいぐるみや絵はがきを買う人が多いです。家にいる友だちへの小さな物を。",
              "A toy sounds nice. What do you have?", "ぬいぐるみがいいですね。何がありますか。"),
            OT("We have a koala and a kangaroo. The koala is soft. The kangaroo has a baby in the pocket.",
               "コアラとカンガルーがあります。コアラはふわふわ。カンガルーはポケットに赤ちゃんがいます。",
               [O('koala', "We would like the koala toy, please.", "コアラのぬいぐるみをお願いします。", "コアラ", "🐨",
                  ("Good pick! It is very soft.", "いい選択！とてもふわふわですよ。")),
                O('kangaroo', "We would like the kangaroo toy, please.", "カンガルーのぬいぐるみをお願いします。", "カンガルー", "🦘",
                  ("Good pick! The baby comes out of the pocket.", "いい選択！赤ちゃんはポケットから出てきますよ。"))],
               cards=1, fork={'tw': ['toy']}),
            T("Would you like a gift bag? The price is on the little tag.",
              "ギフト用の袋はいりますか。値段は小さなタグにあります。",
              "Yes, please. Can we pay by card?", "はい、お願いします。カードで払えますか。"),
            T("No worries. Tap here. Thanks, mate! Enjoy Sydney.",
              "大丈夫です。ここにタッチしてください。ありがとう！シドニーを楽しんで。",
              "Thank you. Goodbye.", "ありがとう。さようなら。"),
        ],
        words=[("souvenir", "おみやげ"), ("toy", "ぬいぐるみ"), ("postcard", "絵はがき"), ("koala", "コアラ"), ("kangaroo", "カンガルー")],
        conv=1, flow2=1))

    D.append(dict(
        id='syd_hotel1', who='フロントの係', bg='shotel', sp='s_front',
        intro='街のホテルのロビー。フロントの係が、にこにこして迎えてくれる。',
        pairs=[
            T("G'day! Welcome. Do you have a booking?",
              "こんにちは！ようこそ。ご予約はありますか。",
              "Yes, we do.", "はい、あります。"),
            T("Great. May I see your passport, please?",
              "ありがとうございます。パスポートを見せていただけますか。",
              "Here you are.", "どうぞ。"),
            OT("Thanks. Would you like a room with a view, or a quiet room?",
               "ありがとう。景色のよい部屋にしますか、それとも静かな部屋にしますか。",
               [O('view', "A room with a view, please.", "景色のよい部屋をお願いします。", "景色", "🌆",
                  ("Lovely. You can see the city from the window.", "いいですね。窓から街が見えますよ。")),
                O('quiet', "A quiet room, please.", "静かな部屋をお願いします。", "静かな部屋", "🤫",
                  ("No worries. It is at the back, away from the street.", "大丈夫です。通りから離れた、奥の部屋です。"))],
               cards=1, fork={'tw': ['room']}),
            T("Here is your key card. Breakfast is in the restaurant.",
              "こちらがカードキーです。朝食はレストランです。",
              "Thank you. Is there Wi-Fi in the room?", "ありがとう。部屋にWi-Fiはありますか。"),
            T("Yes, there is. The details are on the card. Enjoy your stay!",
              "はい、あります。くわしくはカードに書いてあります。ご滞在を楽しんで！",
              "Thank you very much.", "どうもありがとうございます。"),
        ],
        words=[("booking", "予約"), ("passport", "パスポート"), ("view", "景色"), ("key card", "カードキー"), ("breakfast", "朝食")],
        conv=1, flow2=1))

    # =================== 出発 ===================
    D.append(dict(
        id='syd_dep_checkin1', who='チェックインの係', bg='sdepcheck', sp='s_check',
        intro='出発ホールのチェックインカウンター。次の行き先はシンガポール。係が明るく迎えてくれる。',
        pairs=[
            T("G'day! Where are you flying today?",
              "こんにちは！今日はどちらへ飛びますか。",
              "We are flying to Singapore.", "シンガポールへ飛びます。"),
            T("Lovely. Passports, please. Are you checking a bag?",
              "いいですね。パスポートをお願いします。荷物は預けますか。",
              "Yes, one suitcase.", "はい、スーツケースが一つ。"),
            OT("Okay. Put it on the belt. Would you like a window seat, or an aisle seat?",
               "わかりました。ベルトにのせてください。窓側の席にしますか、通路側にしますか。",
               [O('window', "A window seat, please.", "窓側の席をお願いします。", "窓側", "🪟",
                  ("A window seat. No worries.", "窓側ですね。大丈夫です。")),
                O('aisle', "An aisle seat, please.", "通路側の席をお願いします。", "通路側", "🚶",
                  ("An aisle seat. No worries.", "通路側ですね。大丈夫です。"))],
               cards=1, fork={'tw': ['seat']}),
            T("Here are your boarding passes. The gate will be on the screens. Check the board again before you go.",
              "搭乗券です。ゲートは画面に出ます。行く前に、もう一度案内板を見てください。",
              "Thank you. Where do we go now?", "ありがとう。このあとはどこへ行きますか。"),
            T("Go to security, then passport control. Just follow the signs. Have a great flight!",
              "保安検査へ、そのあと出国の確認へ。案内に沿って行くだけです。いい旅を！",
              "Thank you. Goodbye.", "ありがとう。さようなら。"),
        ],
        words=[("check in", "チェックインする"), ("suitcase", "スーツケース"), ("boarding pass", "搭乗券"), ("window seat", "窓側の席"), ("aisle seat", "通路側の席")],
        conv=1, flow2=1))

    D.append(dict(
        id='syd_dep_exit1', who='保安検査の係', bg='sdepexit', sp='s_sec',
        intro='保安検査と出国の確認。まず保安検査、そのあとに出国のパスポート確認。係はどちらも明るく声をかけてくれる。',
        pairs=[
            T("Hi there. Boarding pass, please. Welcome to security.",
              "こんにちは。搭乗券をお願いします。保安検査へようこそ。",
              "Here you are.", "どうぞ。"),
            T("Thanks. Put your bag in the tray. Look at the sign above the lane. Some lanes need the laptop out.",
              "ありがとう。かばんをトレイに入れてください。レーンの上の表示を見て。ノートパソコンを出すレーンもあります。",
              "Okay. We have some small bottles.", "わかりました。小さなボトルがあります。"),
            OT("No worries. Put them in the tray. Do you have any other liquids?",
               "大丈夫です。トレイに入れてください。ほかに液体はありますか。",
               [O('yes', "Yes, we have some liquids.", "はい、液体があります。", "ある", "🧴",
                  ("Okay. Put them in the tray, too. They must be small.", "わかりました。それもトレイへ。小さいものだけです。")),
                O('no', "No, we have no liquids.", "いいえ、液体はありません。", "ない", "🙅",
                  ("Great. Just the bag in the tray, then.", "いいですね。では、かばんだけトレイへ。"))],
               cards=1, fork={'tw': ['liquids']}),
            T("Next, passport control. Passport and boarding pass, please. Where are you going next?",
              "次は出国の確認です。パスポートと搭乗券をお願いします。次はどちらへ。",
              "We are going to Singapore.", "シンガポールへ行きます。",
              cx={'sp': 's_pcheck', 'who': '出国の係'}),
            T("All done. Have a safe trip!",
              "終わりです。気をつけて、いい旅を！",
              "Thank you. Goodbye.", "ありがとう。さようなら。",
              cx={'sp': 's_pcheck', 'who': '出国の係'}),
        ],
        words=[("security", "保安検査"), ("tray", "トレイ"), ("liquids", "液体"), ("laptop", "ノートパソコン"), ("passport control", "出国の確認")],
        conv=1, flow2=1))

    D.append(dict(
        id='syd_dep_gate1', who='案内の係', bg='sdepgate', sp='s_board',
        intro='搭乗ゲートの手前。大きな出発案内板に、シンガポール行きの行が光っている。係が声をかけてくれる。',
        pairs=[
            T("Hello! Can I help you find your gate?",
              "こんにちは！ゲートを探すお手伝いをしましょうか。",
              "Yes, please. We are going to Singapore.", "はい、お願いします。シンガポールへ行きます。"),
            T("Look at the board. Find Singapore. The gate is on the right side of the row.",
              "案内板を見て。シンガポールを探して。ゲートは、その行の右側にあります。",
              "I see it. Is the gate far?", "見つけました。ゲートは遠いですか。"),
            OT("Not far. Just follow the signs. Do you want to eat first, or go to the gate?",
               "遠くないですよ。案内に沿って行くだけです。先に何か食べますか、それともゲートへ行きますか。",
               [O('eat', "Let's eat first. We have time.", "先に食べましょう。時間はあります。", "先に食べる", "🍴",
                  ("Good idea. There are shops near the gate. Just check the board again.", "いいですね。ゲートの近くにお店があります。案内板だけ、もう一度見てください。")),
                O('gate', "Let's go to the gate first.", "先にゲートへ行きましょう。", "ゲートへ", "🚪",
                  ("Good idea. Then you can relax at the gate.", "いいですね。そうすれば、ゲートでゆっくりできます。"))],
               cards=1, fork={'tw': ['first']}),
            T("Remember to check the board again. The gate can change.",
              "もう一度、案内板を見るのを忘れずに。ゲートは変わることがあります。",
              "Thank you. We will check.", "ありがとう。確かめます。"),
            T("Have a great flight. Safe travels!",
              "いい旅を。気をつけて！",
              "Goodbye!", "さようなら！"),
        ],
        words=[("board", "案内板"), ("gate", "ゲート"), ("boarding", "搭乗"), ("flight", "飛行"), ("far", "遠い")],
        conv=1, flow2=1))
