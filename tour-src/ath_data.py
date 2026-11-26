# -*- coding: utf-8 -*-
# 世界一周編 アテネ(タスク090 到着4場面 / タスク091 街3場面＋出発3場面。クロが執筆)。国ごとのデータは別ファイル(ロヴァニエミ rvn_data.py と同じ形)。
#
# 会話の型は 057/061 の新形式(ナイロビと同じ flow2=1・cards=1): 相手が英語で話す → 選ぶのは1場面に1回だけ(日本語の短い言葉カード)
#   → お手本は音声だけ → カンペ → 声に出す。失敗時は074の統一ルール(自動おてほん→言い直し→3回目でルルが代わりに言って進む)。
#   どのカードを選んでも物語は進む(止めない・合否なし)。日本語は「カードの言葉」「Meaning!(訳)」にだけ置く。
#
# 雰囲気(PM指示): アテネのスタッフは「声が大きくて身ぶりが多く、率直だが世話好き」。
#
# 使ってよい実在情報(確認日 2026-11-26。出典は docs/sources.md の「090」「091」):
#   - EES: 顔写真と指紋を記録し、パスポートのスタンプの代わりにデジタル記録を残す(ギリシャは2026-04-10に全面実施。アテネ空港公式・ギリシャ外務省)
#   - 入国審査の前に帽子とサングラスを取り、パスポートは顔写真のページを開く(アテネ空港公式 aia.gr)
#   - タクシー: 中心部まで昼の定額 40 ユーロ(PM指示書で資料が一致)。無許可の客引きは断り、正規の乗り場で乗る
#   - 日本のパスポートは自動ゲートでなく窓口に並ぶ(PM指示書)
# 台詞に出さないもの: 地下鉄の空港用切符の値段(資料が割れている)・おみやげ・料理・ホテルの値段・便の時刻・ゲート番号・チェックイン締切の分数。
#   例外(指示書の前提そのもの): 出国審査の場面の「出発まであと30分」。ホテル名・店名は指示書に無いので出さない(PM確認の点)。個人名なし。
import window_data as W
from window_data import star, OT

E = ''


def O(k, y, jp, card, ico, rep):
    return dict(k=k, y=star(y), jp=jp, card=card, ico=ico, rep=rep)


def T(n, njp, y, yjp, **kw):
    d = dict(n=n, njp=njp, y=star(y), yjp=yjp)
    d.update(kw)
    return d


# 声(SP)はあとで build.py に置く: a_officer(入国審査1)・a_officer2(入国審査2)・a_tout(客引き)・a_driver(正規の運転手)・a_metro(地下鉄の係員)・
#   a_waiter・a_shop・a_front・a_ck・a_dep・a_gate
def add(D):
    # =================== 到着(タスク090) ===================
    D.append(dict(
        id='ath_immig1', who='入国審査の係官', bg='aimmig', sp='a_officer',
        intro='アテネ空港の入国審査。日本のパスポートは自動ゲートでなく、窓口の列。係官は声が大きく、身ぶりが大きい。',
        pairs=[
            T("Hello, hello! A Japanese passport? No automatic gate for you today. Come to the window, please!",
              "こんにちは！日本のパスポート？今日は自動ゲートは使えません。窓口へどうぞ！",
              "Hello. Thank you. Here I come.", "こんにちは。ありがとう。いま行きます。"),
            T("Hat off, sunglasses off, please! I need to see your face. And the passport, open at the photo page!",
              "帽子とサングラスを取って！顔を見せて。パスポートは写真のページを開いて！",
              "Sorry. Here is my passport.", "すみません。パスポートです。"),
            OT("Good, good. Why are you visiting Greece?",
               "よし、よし。ギリシャには何をしに？",
               [O('sight', "We are here for sightseeing.", "観光で来ました。", "観光", "📷",
                  ("Sightseeing! The best reason. We have a lot of old stones here, my friend!", "観光！いちばんいい理由です。ここには古い石がたくさんありますよ！")),
                O('world', "We are traveling around the world.", "世界一周をしています。", "世界一周", "🌏",
                  ("Around the world! Wonderful. Greece is a very good stop!", "世界一周！すばらしい。ギリシャは最高の寄港地ですよ！"))],
               cards=1, fork={'tw': ['sightseeing']}),
            T("And how long will you stay in Athens?",
              "アテネにはどのくらい滞在しますか。",
              "We will stay for a few days.", "数日、滞在します。"),
            T("Perfect! Enjoy the sun and the old stones. Welcome to Greece, my friends!",
              "完璧！太陽と古い石を楽しんで。ギリシャへようこそ！",
              "Thank you very much!", "ありがとうございます！"),
        ],
        words=[("sunglasses", "サングラス"), ("passport", "パスポート"), ("sightseeing", "観光"), ("stay", "滞在する"), ("window", "窓口")],
        conv=1, flow2=1))

    D.append(dict(
        id='ath_immig2', who='入国審査の係官', bg='aimmig', sp='a_officer2',
        intro='同じ窓口の続き。新しい出入国システム(EES)で、顔写真と指紋を記録する。',
        pairs=[
            T("Next, please! This is the new system. First, look at the camera. Straight, my friend, straight!",
              "次の方！これは新しいシステムです。まずカメラを見て。まっすぐ！",
              "Like this? Okay.", "こうですか。はい。"),
            T("Good photo! Now your fingers. Put them on the glass, please. Flat, flat!",
              "いい写真！次は指です。ガラスに置いて。しっかり平らに！",
              "Is this right?", "これでいいですか。"),
            OT("Perfect. The machine is happy! Do you know the new system? It is called EES.",
               "完璧。機械も喜んでいます！この新しいシステムを知っていますか。EESといいます。",
               [O('no', "No, I didn't know. What is it?", "いいえ、知りませんでした。何ですか。", "知らない", "🤔",
                  ("It keeps a digital record of your face and fingers when you come in. Easy!", "入るとき、顔と指のデジタル記録を残すんです。簡単でしょう！")),
                O('yes', "Yes, I read about it.", "はい、読んだことがあります。", "知ってる", "📖",
                  ("Smart traveler! Then you know the rule.", "かしこい旅行者ですね！じゃあ決まりは知っていますね。"))],
               cards=1, fork={'tw': ['system']}),
            T("So, no stamp in your passport now. The computer keeps the record, not the paper.",
              "というわけで、もうパスポートにスタンプは押しません。記録は紙でなく、コンピューターが持っています。",
              "No stamp? That is a little sad.", "スタンプなし？ちょっと寂しいですね。"),
            T("Ha! I know, I know. Many travelers say so. Maybe next time it will be faster. Welcome to Athens!",
              "ははは！そうなんです。みんなそう言います。次はもっと早いかもしれません。アテネへようこそ！",
              "Thank you. See you!", "ありがとう。またね！"),
        ],
        words=[("camera", "カメラ"), ("fingerprints", "指紋"), ("system", "システム"), ("stamp", "スタンプ"), ("digital", "デジタルの")],
        conv=1, flow2=1))

    D.append(dict(
        id='ath_taxi1', who='客引きの男', bg='ataxi', sp='a_tout',
        intro='到着ロビーを出ると、声をかけてくる人がいる。正規のタクシー乗り場は、そのさき。',
        pairs=[
            OT("Taxi, taxi, my friend! Good price, good price! Come, come with me!",
               "タクシー、タクシー！安いよ、安いよ！さあ、こっちへ！",
               [O('rank', "No, thank you. We will go to the taxi rank.", "いいえ、けっこうです。タクシー乗り場に行きます。", "乗り場へ", "🚖",
                  ("Okay, okay, no problem! Have a nice day!", "わかった、わかった！いい一日を！")),
                O('official', "No, thank you. We only take the official taxi.", "いいえ。正規のタクシーにしか乗りません。", "正規だけ", "✅",
                  ("Okay, okay. You are smart! Have a nice day!", "わかった。かしこいね！いい一日を！"))],
               cards=1, fork={'tw': ['official']}),
            T("Welcome! This is the taxi rank, the real one. Where to, my friends?",
              "ようこそ！ここがタクシー乗り場、ほんものです。どちらまで？",
              "To the city center, please.", "市の中心部までお願いします。",
              cx={'sp': 'a_driver', 'who': 'タクシーの運転手'}),
            T("No problem! Please get in. The luggage goes in the back.",
              "お安いご用です！どうぞ乗って。荷物はうしろへ。",
              "Thank you. It is a fixed price of forty euros to the center, right?", "ありがとう。中心部まで40ユーロの定額ですよね？",
              cx={'sp': 'a_driver', 'who': 'タクシーの運転手'}),
            T("Yes, yes, correct! Forty euros to the center, a fixed price. No surprise, my friend!",
              "そう、そのとおり！中心部まで40ユーロの定額。びっくりすることはないよ！",
              "Good. Thank you for telling us.", "よかった。教えてくれてありがとう。",
              cx={'sp': 'a_driver', 'who': 'タクシーの運転手'}),
            T("Sit back and relax. Welcome to Athens!",
              "ゆっくりくつろいで。アテネへようこそ！",
              "Thank you. Efharisto!", "ありがとう。エフハリスト！",
              cx={'sp': 'a_driver', 'who': 'タクシーの運転手'}),
        ],
        words=[("taxi", "タクシー"), ("official", "正規の"), ("fixed price", "定額"), ("luggage", "荷物"), ("center", "中心")],
        conv=1, flow2=1))

    D.append(dict(
        id='ath_transit1', who='地下鉄の係員', bg='ametro', sp='a_metro',
        intro='地下鉄の券売機の前。係員が、困った顔のふたりに声をかけてくれた。',
        pairs=[
            T("Hello, hello! You look lost, my friends. Can I help you?",
              "こんにちは！迷っているようですね。お手伝いしましょうか。",
              "Yes, please. We want to go to the city by metro.", "はい、お願いします。地下鉄で街へ行きたいです。"),
            OT("Great choice! Look at the machine. There are many tickets. Which one do you want?",
               "いい選択です！券売機を見て。切符がたくさんあります。どれにしますか。",
               [O('air', "Which one is the airport ticket?", "空港用の切符はどれですか。", "空港用", "✈️",
                  ("This one! Many people choose the wrong one, so you are smart to ask!", "これです！間違える人が多いので、聞いて正解ですよ！")),
                O('cheap', "I want the cheapest ticket.", "いちばん安い切符がほしいです。", "いちばん安い", "💶",
                  ("No, no, no! The cheap city ticket does not go to the airport. You need the airport ticket!", "だめ、だめ！市内の安い切符では空港まで行けません。空港用の切符が必要です！"))],
               cards=1, fork={'tw': ['airport']}),
            T("Press the button for the airport ticket here. Then pay, and take your ticket.",
              "ここの空港用切符のボタンを押して。それから払って、切符を取って。",
              "This button? Okay. Can I pay by card?", "このボタンですか。わかりました。カードで払えますか。"),
            T("Yes, a card is fine. The machine will tell you what to do. Easy, easy!",
              "はい、カードで大丈夫。機械が次にすることを教えてくれます。簡単、簡単！",
              "Thank you. Which way is the train to the city?", "ありがとう。街へ行く電車はどちらですか。"),
            T("Follow the signs for the metro! The train comes soon. Have a good trip, my friends!",
              "地下鉄の案内表示について行って！電車はすぐ来ます。いい旅を！",
              "Thank you very much. Bye!", "本当にありがとう。さようなら！"),
        ],
        words=[("ticket machine", "券売機"), ("airport", "空港"), ("cheap", "安い"), ("card", "カード"), ("sign", "案内表示")],
        conv=1, flow2=1))

    # =================== 街(タスク091) ===================
    D.append(dict(
        id='ath_cafe1', who='タベルナの店員', bg='acafe', sp='a_waiter',
        intro='プラカ風の街のタベルナ。店員が身ぶりたっぷりで呼びこんでくる。',
        pairs=[
            T("Yia sas, my friends! Come, come! You look hungry!",
              "ヤー・サス！さあ、さあ！おなかがすいているみたいですね！",
              "Yes, we are. What do you recommend?", "はい、すいています。おすすめは何ですか。"),
            OT("Gyros! Everybody loves it. Meat, tomato, onion, and pita, all together. Here, or to go?",
               "ギロ！みんな大好きです。肉、トマト、玉ねぎ、ピタが全部入り。ここで食べますか、持ち帰りですか。",
               [O('here', "We'll eat here, please.", "ここで食べます。", "ここで", "🍽️",
                  ("Wonderful! Fresh and hot, coming right up!", "すばらしい！できたて、あつあつですぐ出します！")),
                O('go', "To take away, please. Could you wrap it?", "持ち帰りでお願いします。包んでもらえますか。", "持ち帰り", "🥡",
                  ("Of course! I wrap it nicely, no problem!", "もちろん！きれいに包みます、お安いご用！"))],
               cards=1, fork={'tw': ['gyros']}),
            T("Anything else? Try the loukoumades! Little fried sweets with honey. Very good!",
              "ほかには？ルクマデスをどうぞ！はちみつをかけた小さな揚げ菓子です。おいしいですよ！",
              "Sounds nice. We will try the loukoumades too.", "いいですね。ルクマデスもいただきます。"),
            T("Excellent choice! Everything is almost ready. Please wait just a little.",
              "いい選択！もうすぐ全部できます。ほんの少しだけ待ってください。",
              "Thank you. It smells so good.", "ありがとう。いいにおいですね。"),
            T("Enjoy, enjoy! Come back again, my friends!",
              "どうぞ、どうぞ！また来てくださいね！",
              "We will. Thank you!", "また来ます。ありがとう！"),
        ],
        words=[("gyros", "ギロ(肉を焼いてピタで包む料理)"), ("take away", "持ち帰り"), ("wrap", "包む"), ("sweets", "甘いお菓子"), ("recommend", "おすすめする")],
        conv=1, flow2=1))

    D.append(dict(
        id='ath_shop1', who='おみやげ屋の店主', bg='ashop', sp='a_shop',
        intro='街のおみやげ屋。店主はよく話し、商品をどんどん見せてくれる。',
        pairs=[
            T("Welcome, welcome! Look, touch, smell! Everything is made with love!",
              "いらっしゃい！見て、さわって、においをかいで！ぜんぶ愛情をこめて作っています！",
              "Thank you. We like your sandals. Can we try a pair?", "ありがとう。このサンダルがいいですね。試してもいいですか。"),
            OT("Of course! Leather sandals, very comfortable. Try this pair. How do they feel?",
               "もちろん！革のサンダルです、とても楽ですよ。この1足をどうぞ。どうですか。",
               [O('fit', "They fit well. This size is good.", "ぴったりです。このサイズでいいです。", "ちょうどいい", "👍",
                  ("Perfect! Greek feet, I think!", "完璧！ギリシャの足みたいですね！")),
                O('tight', "They are a little tight. Do you have a bigger size?", "少しきついです。大きいサイズはありますか。", "きつい", "😣",
                  ("Of course! Wait, wait, I bring the bigger ones!", "もちろん！待って、待って、大きいのを持ってきます！"))],
               cards=1, fork={'tw': ['size']}),
            T("Good, good. Now look here. Mastic soap, and natural cosmetics. Very Greek!",
              "よし、よし。さあ、こちらも。マスティハの石けんと、自然派の化粧品。とてもギリシャらしいですよ！",
              "They smell nice. What is mastic?", "いいにおい。マスティハって何ですか。"),
            T("Mastic comes from a tree on a Greek island. We use it in sweets, and in cosmetics. Very special!",
              "マスティハは、ギリシャの島の木からとれます。お菓子にも、化粧品にも使います。とても特別なんですよ！",
              "Interesting. How much are the sandals?", "おもしろい。サンダルはいくらですか。"),
            T("The price is on the little tag, my friend. And for two pairs, I make you a better price. Okay?",
              "値段は小さなタグに書いてあります。2足なら、もっといい値段にしますよ。どうですか。",
              "Okay. We will think about it. Thank you!", "わかりました。考えてみます。ありがとう！"),
        ],
        words=[("sandals", "サンダル"), ("leather", "革"), ("size", "サイズ"), ("price", "値段"), ("cosmetics", "化粧品")],
        conv=1, flow2=1))

    D.append(dict(
        id='ath_hotel1', who='ホテルのフロント', bg='ahotel', sp='a_front',
        intro='アテネのホテル。夕方の窓の向こうに、丘の上の神殿が見える。フロントの人は元気いっぱい。',
        pairs=[
            T("Good evening, and welcome to Athens! Do you have a reservation?",
              "こんばんは、アテネへようこそ！ご予約はありますか。",
              "Yes, we do. Here is my passport.", "はい、あります。パスポートです。"),
            T("Perfect! I make your check-in, one moment! Please sign here.",
              "完璧！チェックインしますね、少々お待ちを！ここにサインを。",
              "Here you are. Thank you.", "どうぞ。ありがとう。"),
            T("Done! Your room has a beautiful view of the Acropolis. You will love it, I promise!",
              "できました！お部屋からアクロポリスがきれいに見えますよ。きっと気に入ります、約束します！",
              "Wonderful! What time is breakfast tomorrow?", "すてき！明日の朝食は何時ですか。"),
            OT("Breakfast is in the restaurant, early in the morning. Do you prefer the restaurant, or your room?",
               "朝食はレストランで、朝早くからです。レストランと、お部屋と、どちらがいいですか。",
               [O('rest', "We'll have breakfast in the restaurant.", "朝食はレストランでいただきます。", "レストラン", "🍳",
                  ("Good choice! Fresh bread, fresh fruit, and good coffee!", "いい選択！焼きたてのパン、新鮮な果物、おいしいコーヒーがありますよ！")),
                O('room', "Could we have breakfast in our room?", "朝食を部屋でとれますか。", "部屋で", "🛏️",
                  ("Of course! Just tell me tonight, and I arrange everything.", "もちろん！今夜のうちに言ってくれれば、全部手配します。"))],
               cards=1, fork={'tw': ['breakfast']}),
            T("Enjoy your stay, my friends! If you need anything, call me!",
              "ごゆっくり！何かあったら、呼んでくださいね！",
              "Thank you. Good night!", "ありがとう。おやすみなさい！"),
        ],
        words=[("reservation", "予約"), ("check in", "チェックインする"), ("view", "景色"), ("breakfast", "朝食"), ("restaurant", "レストラン")],
        conv=1, flow2=1))

    # =================== 出発(タスク091) ===================
    D.append(dict(
        id='ath_checkin1', who='チェックインの係員', bg='acheck', sp='a_ck',
        intro='アテネ空港の出発ホール。チェックインのカウンター。係員は早口で、はきはきしている。',
        pairs=[
            T("Hello! Passport and ticket, please. Let's go, let's go!",
              "こんにちは！パスポートと航空券をどうぞ。さあ、さあ！",
              "Here you are.", "どうぞ。"),
            T("Thank you. You want to check this bag, yes? Put it on the belt, please.",
              "ありがとう。この荷物を預けますね。ベルトの上に置いてください。",
              "Yes. Just this one suitcase.", "はい。このスーツケースだけです。"),
            OT("Good! Now, window seat, or aisle seat?",
               "いいですね！さて、窓側と通路側、どちらにしますか。",
               [O('win', "A window seat, please.", "窓側をお願いします。", "窓側", "🪟",
                  ("Window! You will see the clouds!", "窓側！雲が見えますよ！")),
                O('aisle', "An aisle seat, please.", "通路側をお願いします。", "通路側", "🚶",
                  ("Aisle! Easy to stand up and walk!", "通路側！立ち上がって歩きやすいですよ！"))],
               cards=1, fork={'tw': ['aisle seat']}),
            T("Here is your boarding pass. Now listen to me, my friends: passport control takes time today. Please go early!",
              "搭乗券です。さあ、よく聞いてください。今日は出国審査に時間がかかります。早めに行って！",
              "Is the line long today?", "今日は列が長いんですか。"),
            T("It can be very long! Don't take your time. Go now, go, go!",
              "とても長くなることがあります！のんびりしないで。いますぐ行って、さあ、さあ！",
              "I see. We will go right now. Thank you!", "わかりました。すぐ行きます。ありがとう！"),
        ],
        words=[("suitcase", "スーツケース"), ("aisle seat", "通路側の席"), ("window seat", "窓側の席"), ("boarding pass", "搭乗券"), ("early", "早めに")],
        conv=1, flow2=1))

    D.append(dict(
        id='ath_depimmig1', who='出国審査の係員', bg='adep', sp='a_dep',
        intro='出国審査の列。出発まであと30分。時間がない。',
        pairs=[
            T("Next, next! Passport and boarding pass, please!",
              "次の方、次の方！パスポートと搭乗券をどうぞ！",
              "Here you are. Our flight leaves in thirty minutes.", "どうぞ。出発まであと30分です。"),
            OT("Thirty minutes? Oh my! The line is long today. What do you need?",
               "30分！？おやおや！今日は列が長いんです。何が必要ですか。",
               [O('prio', "Is there a priority lane, please?", "優先の列はありますか。", "優先の列", "⏩",
                  ("A priority lane? Not always, my friend. But your flight is soon, so I help you. Come, come!", "優先の列？いつもあるわけじゃないんです。でも出発が近いので、手伝いますよ。さあ、こっちへ！")),
                O('hurry', "We are in a hurry. Can we go first, please?", "急いでいます。先に行かせてもらえますか。", "急いでる", "🏃",
                  ("I understand, I understand. Okay, okay, come with me, quickly!", "わかりました、わかりました。さあ、ついて来て、急いで！"))],
               cards=1, fork={'tw': ['priority']}),
            T("This way! Please stand here. Passport open at the photo page.",
              "こちらへ！ここに立って。パスポートは写真のページを開いて。",
              "Thank you so much.", "本当にありがとうございます。"),
            T("Camera, please. Then your fingers. Fast, fast! Good!",
              "カメラを見て。次に指。急いで、急いで！いいですね！",
              "Okay. Is that all?", "はい。これで全部ですか。"),
            T("All done! Now walk fast, but don't fall! Go, go, go!",
              "終わりです！さあ急いで歩いて、でも転ばないでね！行って、行って！",
              "Thank you! Goodbye!", "ありがとう！さようなら！"),
        ],
        words=[("priority", "優先の"), ("lane", "列(レーン)"), ("hurry", "急ぐ"), ("boarding pass", "搭乗券"), ("line", "列")],
        conv=1, flow2=1))

    D.append(dict(
        id='ath_gate1', who='搭乗口の係員', bg='agate', sp='a_gate',
        intro='搭乗口。出発の直前に、便の時刻が変わった。',
        pairs=[
            T("Attention, my friends! Your flight has a change. The time is different now!",
              "みなさん、お知らせです！この便に変更があります。出発の時刻が変わりました！",
              "Oh no. What is the new time?", "えっ。新しい時刻は何時ですか。"),
            T("The flight leaves later than before. Please look at the screen. The new time is there. Very clear!",
              "出発は、前よりあとになります。画面を見てください。新しい時刻が出ています。とてもわかりやすいですよ！",
              "Thank you. And the gate? Is it the same?", "ありがとう。搭乗口は？同じですか。"),
            OT("The gate changed too! Please check the board. Do you want me to show you?",
               "搭乗口も変わりました！案内板を確認してください。ご案内しましょうか。",
               [O('show', "Yes, please show us the way.", "はい、案内してください。", "案内して", "🙏",
                  ("Of course! Come, I show you. Follow me!", "もちろん！おいで、案内しますよ。ついて来て！")),
                O('self', "No, thank you. We will check the screen.", "いいえ、大丈夫です。画面を見て確認します。", "自分で見る", "👀",
                  ("Good, good! The board is right there. You are very quick!", "いいですね！案内板はすぐそこです。しっかりしてますね！"))],
               cards=1, fork={'tw': ['gate']}),
            T("Don't worry. You have time. Sit, drink some water, relax!",
              "心配いりません。時間はあります。座って、お水を飲んで、くつろいで！",
              "Thank you. We will wait here.", "ありがとう。ここで待ちます。"),
            T("I call everyone when we board. Please listen for the announcement!",
              "搭乗が始まったら、みなさんをお呼びします。アナウンスを聞いていてくださいね！",
              "Okay. Thank you very much!", "わかりました。本当にありがとう！"),
        ],
        words=[("change", "変更"), ("gate", "搭乗口"), ("screen", "画面"), ("announcement", "アナウンス"), ("later", "もっとあとに")],
        conv=1, flow2=1))
