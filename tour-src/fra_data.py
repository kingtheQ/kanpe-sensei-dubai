# -*- coding: utf-8 -*-
# 世界一周編 フランクフルト(タスク097。到着4場面＋街3場面＋出発3場面。クロが執筆)。国ごとのデータは別ファイル(ath_data.py と同じ形)。
#
# 会話の型は ath_data.py と同じ新形式(flow2=1・cards=1): 相手が英語で話す → 選ぶのは1場面に1回だけ(日本語の短い言葉カード)
#   → お手本は音声だけ → カンペ → 声に出す。失敗時は074の統一ルール(自動おてほん→言い直し→3回目でルルが代わりに言って進む)。
#   どのカードを選んでも物語は進む(止めない・合否なし)。日本語は「カードの言葉」「Meaning!(訳)」にだけ置く。
#
# 雰囲気(PM指示): フランクフルトのスタッフは「きっちり正確で愛想は少なめ。聞けば要点を順番に教えてくれる」。
#   → 台詞は短く、First / Second / Then の順番で要点を言う。笑いや身ぶりの声かけは少ない。
#
# 大前提(指示書): 到着も出発も鉄道(フランクフルト中央駅 Frankfurt Hbf)。到着はチューリッヒからの直通ICE。
#   ドイツはシェンゲン圏内でこの旅はアテネで入国済みなので、入国審査の場面はない。
#   ロンドン行きは直通でなく、ICEでブリュッセル(Brussels-Midi)まで行き、ユーロスターに乗り換える。
#
# 使ってよい実在情報(確認日 2026-11-26。出典は docs/sources.md の「097」):
#   - ICEはフランクフルトからケルン・アーヘンを通ってブリュッセル(Brussels-Midi)へ直通。所要は約3時間(DB公式プレスリリース)。台詞には時間を出さない。
#   - ブリュッセル・ミディで乗り換え(同じ駅の中。案内板で次の列車のホームを確かめる=ユーロスター公式)。
#   - フランクフルト中央駅に DB Reisezentrum(切符・予約・時刻の相談窓口)がある(bahnhof.de 公式)。
#   - ベンペル(Bembel)はりんご酒(Apfelwein)を注ぐ陶器の水差し。小さな置物・キーホルダーのおみやげがある(visitfrankfurt.travel・Glorious Food Glossary)。
# 台詞に出さないもの(未確認): 運賃・商品や食事の値段・正確な発車時刻・ホーム番号・トラムの路線番号・所要の分数・乗り換え時間の分数・ホテル名や店名。
#   値段は「小さなタグを見て」のように言い、数字は出さない。ホーム番号は「案内板で見て」と言う。個人名なし。
#   りんご酒はお酒なので、聞くだけ(店員が説明する)。ふたりが頼むのは、りんごジュース。
import window_data as W
from window_data import star, OT

E = ''


def O(k, y, jp, card, ico, rep):
    return dict(k=k, y=star(y), jp=jp, card=card, ico=ico, rep=rep)


def T(n, njp, y, yjp, **kw):
    d = dict(n=n, njp=njp, y=star(y), yjp=yjp)
    d.update(kw)
    return d


# 声(SP)は build.py に置く: f_guide(到着の案内係)・f_baker・f_tram・f_info・f_waiter・f_shop・f_front・f_board・f_ticket・f_conductor・f_pax
def add(D):
    # =================== 到着(タスク097) ===================
    D.append(dict(
        id='fra_arr1', who='駅の案内係', bg='farr', sp='f_guide',
        intro='フランクフルト中央駅の大ホール。チューリッヒからの直通ICEを降りたところ。青い大きな発車標と、駅の時計が見える。',
        pairs=[
            T("Good afternoon. You have just arrived from Zurich, yes? Welcome to Frankfurt Central Station.",
              "こんにちは。チューリッヒから着いたところですね。フランクフルト中央駅へようこそ。",
              "Yes, we have. Thank you.", "はい、そうです。ありがとう。"),
            T("The big blue board shows the departures. First, the time. Second, the destination. Third, the platform.",
              "大きな青い板が発車標です。まず時刻。次に行き先。そのつぎにホーム。",
              "I see. Can we read the clock there, too?", "なるほど。時計もそこで見られますか。"),
            OT("Yes. The station clock is in the top corner. Do you need the exit, or the travel center?",
               "はい。駅の時計は右上のすみです。出口が必要ですか。それとも案内の窓口ですか。",
               [O('exit', "We need the exit to the city, please.", "街への出口が必要です。", "出口", "🚪",
                  ("The sign says Ausgang City. Follow the arrow, and you will be outside.", "案内板に「Ausgang City」とあります。矢印について行けば外に出られます。")),
                O('center', "We need the travel center, please.", "案内の窓口が必要です。", "窓口", "ℹ️",
                  ("The sign says Reise Zentrum. It is on the left side of the hall.", "案内板に「ReiseZentrum」とあります。ホールの左側です。"))],
               cards=1, fork={'tw': ['exit']}),
            T("Do you have luggage? Keep it with you at all times in the station.",
              "荷物はありますか。駅の中では、いつも手元に置いてください。",
              "Yes, one suitcase. Can we go to the hotel by tram?", "はい、スーツケースが1つ。ホテルへはトラムで行けますか。"),
            T("Yes. The tram stop is outside the station. Buy a ticket first. Then ask at the tram counter for the right line.",
              "はい。トラムの乗り場は駅の外にあります。まず切符を買って。それからトラムの窓口で、正しい路線を聞いてください。",
              "Thank you. We will do that.", "ありがとう。そうします。"),
        ],
        words=[("arrive", "着く"), ("departure", "出発"), ("platform", "ホーム"), ("exit", "出口"), ("clock", "時計")],
        conv=1, flow2=1))

    D.append(dict(
        id='fra_bakery1', who='パン屋の店員', bg='fbakery', sp='f_baker',
        intro='駅のホールのベーカリー。ガラスのケースにパンが並んでいる。店員は手早く、必要なことだけ言う。',
        pairs=[
            T("Hello. What would you like?",
              "こんにちは。何にしますか。",
              "Hello. What is the most popular bread here?", "こんにちは。いちばん人気のパンはどれですか。"),
            T("The pretzel. Many travelers take it. Next is the cheese roll. Third is the apple pastry.",
              "プレッツェルです。旅行の人がよく買います。次がチーズのロール。3番目がりんごのパイ。",
              "Then we will take two pretzels, please.", "では、プレッツェルを2つお願いします。"),
            OT("Two pretzels. And a drink? We have coffee and tea.",
               "プレッツェルを2つ。飲み物は？コーヒーと紅茶があります。",
               [O('coffee', "Two coffees, please.", "コーヒーを2つお願いします。", "コーヒー", "☕",
                  ("Two coffees. Small or large?", "コーヒーを2つ。小さいのと大きいの、どちらですか。")),
                O('tea', "Two teas, please.", "紅茶を2つお願いします。", "紅茶", "🍵",
                  ("Two teas. Small or large?", "紅茶を2つ。小さいのと大きいの、どちらですか。"))],
               cards=1, fork={'tw': ['coffees']}),
            T("Small or large?",
              "小さいのと、大きいの、どちらですか。",
              "Small, please. And to take away, please.", "小さいのをお願いします。持ち帰りでお願いします。"),
            T("To take away. I put everything in a bag. The price is on the screen. Thank you.",
              "持ち帰りですね。全部、袋に入れます。値段は画面に出ています。ありがとうございます。",
              "Thank you. Have a nice day.", "ありがとう。いい一日を。"),
        ],
        words=[("popular", "人気の"), ("bread", "パン"), ("pretzel", "プレッツェル"), ("coffee", "コーヒー"), ("take away", "持ち帰り")],
        conv=1, flow2=1))

    D.append(dict(
        id='fra_tram1', who='乗り場の係員', bg='ftram', sp='f_tram',
        intro='駅の外のトラム乗り場。券売機のそばに、係員が立っている。きっちりした話し方で、順番に教えてくれる。',
        pairs=[
            T("Good afternoon. Can I help you?",
              "こんにちは。何かお困りですか。",
              "Yes, please. How do we buy a city ticket?", "はい、お願いします。市内の切符はどう買いますか。"),
            T("First, touch the screen. Second, choose a single ticket for the city. Third, pay. Then take your ticket.",
              "まず画面にふれます。次に、市内の1回券を選びます。3つめに、支払い。そして切符を取ります。",
              "Can I pay by card?", "カードで払えますか。"),
            OT("Yes, you can pay by card. Where is your hotel? I show you the right tram.",
               "はい、カードで払えます。ホテルはどこですか。正しいトラムをお見せします。",
               [O('map', "Could you show us on the map, please?", "地図で教えてもらえますか。", "地図で", "🗺️",
                  ("Of course. Here is the map. You take the tram from this stop. Then you get off at the stop near your hotel.", "もちろん。この地図です。この乗り場からトラムに乗って、ホテルの近くの停留所で降ります。")),
                O('name', "The hotel is near the Roemer square.", "ホテルはレーマー広場の近くです。", "広場の近く", "🏛️",
                  ("The Roemer square. Good. You take the tram from this stop, and get off near the old town.", "レーマー広場ですね。この乗り場からトラムに乗って、旧市街の近くで降ります。"))],
               cards=1, fork={'tw': ['hotel']}),
            T("Here is your ticket. Do you have another question?",
              "切符です。ほかに質問はありますか。",
              "Is this ticket valid for the tram?", "この切符でトラムに乗れますか。"),
            T("Yes. Before you get on, check your ticket. If you are not sure, ask the driver. Have a good trip.",
              "はい。乗る前に切符を確認してください。わからなければ、運転手に聞いてください。よい旅を。",
              "Thank you very much.", "どうもありがとうございます。"),
        ],
        words=[("ticket", "切符"), ("single ticket", "1回券"), ("pay", "払う"), ("tram", "トラム"), ("map", "地図")],
        conv=1, flow2=1))

    D.append(dict(
        id='fra_info1', who='案内所の係員', bg='finfo', sp='f_info',
        intro='中央駅の案内所(ReiseZentrum)。明日のロンドン行きのことを聞きに来た。係員は愛想は少なめだが、とても正確。',
        pairs=[
            T("Good afternoon. How can I help you?",
              "こんにちは。ご用件は何でしょう。",
              "Hello. We want to go to London tomorrow. How do we check the trip?", "こんにちは。明日ロンドンへ行きたいです。どうやって調べますか。"),
            T("There is no direct train to London. First, you take the ICE to Brussels. Second, you change to the Eurostar.",
              "ロンドンへの直通列車はありません。まず、ICEでブリュッセルまで行きます。次に、ユーロスターに乗りかえます。",
              "I see. So we change trains in Brussels?", "なるほど。ブリュッセルで乗りかえるのですね。"),
            OT("Correct. Please come back tomorrow morning, and look at the board again. Do you want the printed times, or the app?",
               "そのとおりです。明日の朝、もう一度、発車標を見てください。時刻の紙がいいですか、アプリがいいですか。",
               [O('paper', "A printed paper, please.", "紙でお願いします。", "紙", "📄",
                  ("Here is a paper with the connection. Keep it in your bag.", "乗りかえが書いてある紙です。かばんに入れておいてください。")),
                O('app', "The app is fine for us.", "アプリで大丈夫です。", "アプリ", "📱",
                  ("Good. Please check the app again tomorrow morning. Times can change.", "わかりました。明日の朝にもう一度アプリを見てください。時刻は変わることがあります。"))],
               cards=1, fork={'tw': ['printed']}),
            T("Is there anything else?",
              "ほかにございますか。",
              "Where is the exit to the taxi stand, please?", "タクシー乗り場への出口はどこですか。"),
            T("Go straight, then turn right at the big board. The sign says Ausgang. The taxi stand is outside.",
              "まっすぐ行って、大きな発車標のところで右に曲がります。案内板に「Ausgang」とあります。タクシー乗り場は外です。",
              "Thank you. That is very clear.", "ありがとう。とてもわかりやすいです。"),
        ],
        words=[("direct", "直通の"), ("change", "乗りかえる"), ("morning", "朝"), ("printed", "印刷した"), ("exit", "出口")],
        conv=1, flow2=1))

    # =================== 街(タスク097) ===================
    D.append(dict(
        id='fra_cafe1', who='カフェの店員', bg='fcafe', sp='f_waiter',
        intro='レーマー広場のカフェ。黄色いパラソルの下。名物のりんご酒は、お酒なので聞くだけ。ふたりが頼むのは、りんごジュース。',
        pairs=[
            T("Good afternoon. Please sit anywhere. Do you know what you want?",
              "こんにちは。お好きな席にどうぞ。もうお決まりですか。",
              "Hello. We want to try something from Frankfurt.", "こんにちは。フランクフルトのものを食べてみたいです。"),
            T("Then take the Frankfurter. It is a sausage, with mustard and a bread roll. It is the classic here.",
              "それならフランクフルターです。ソーセージで、マスタードとパンがつきます。ここの定番です。",
              "Two Frankfurters, please. What is the famous drink here?", "フランクフルターを2つお願いします。ここの有名な飲み物は何ですか。"),
            OT("Apple wine. It comes in a stone jug called a Bembel. But it is alcohol. For you, I recommend apple juice.",
               "りんご酒です。ベンペルという陶器の水差しで出ます。でもお酒です。おふたりには、りんごジュースをおすすめします。",
               [O('juice', "Apple juice for us, please.", "りんごジュースをお願いします。", "りんごジュース", "🍎",
                  ("Two apple juices. Very good with the sausage.", "りんごジュースを2つ。ソーセージとよく合います。")),
                O('ask', "Do you have apple juice, please?", "りんごジュースはありますか。", "ジュースある？", "❓",
                  ("Yes, we do. Cold, and in a big glass.", "はい、ございます。冷たくて、大きなグラスで出します。"))],
               cards=1, fork={'tw': ['apple juice']}),
            T("Anything else? Many guests take a pretzel with it.",
              "ほかにはございますか。ソーセージにプレッツェルを添えるお客様が多いです。",
              "No, thank you. That is enough for us.", "いいえ、けっこうです。これで十分です。"),
            T("Understood. Your order will be ready soon. Please wait here.",
              "かしこまりました。もうすぐできます。こちらでお待ちください。",
              "Thank you. This square is very beautiful.", "ありがとう。この広場はとてもきれいですね。"),
        ],
        words=[("sausage", "ソーセージ"), ("mustard", "からし(マスタード)"), ("apple juice", "りんごジュース"), ("famous", "有名な"), ("jug", "水差し")],
        conv=1, flow2=1))

    D.append(dict(
        id='fra_shop1', who='おみやげ屋の店員', bg='fshop', sp='f_shop',
        intro='広場のおみやげ屋(Souvenirs)。りんご酒用の陶器の水差し「ベンペル」が棚に並んでいる。',
        pairs=[
            T("Hello. Please look around. Ask me if you have a question.",
              "こんにちは。ゆっくりご覧ください。ご質問があれば、声をかけてください。",
              "Thank you. What is this blue and gray jug?", "ありがとう。この青と灰色の水差しは何ですか。"),
            T("That is a Bembel. It is a stone jug for apple wine. It is a symbol of Frankfurt.",
              "それはベンペルです。りんご酒を入れる陶器の水差しで、フランクフルトの象徴です。",
              "It is beautiful. How much is it?", "きれいですね。いくらですか。"),
            OT("The price is on the small tag. This one is big. We also have a smaller one. Which do you prefer?",
               "値段は小さなタグに書いてあります。これは大きいです。もっと小さいものもあります。どちらがいいですか。",
               [O('small', "Do you have a smaller one, please?", "もう少し小さいのはありますか。", "小さいの", "🔍",
                  ("Yes. Here is a small one. It is easy to carry in your bag.", "はい。こちらが小さいものです。かばんに入れて持ち運べます。")),
                O('big', "I would like to see the big one.", "大きいのを見せてください。", "大きいの", "🏺",
                  ("Of course. Please hold it with both hands. It is heavy.", "もちろん。両手で持ってください。重いです。"))],
               cards=1, fork={'tw': ['smaller']}),
            T("Good. Is that everything?",
              "けっこうです。ほかにはございますか。",
              "That is all. Can you wrap it, please? It is a gift.", "それだけです。包んでもらえますか。贈りものなんです。"),
            T("Yes. I wrap it in paper, and I put it in a box. Please wait a moment.",
              "はい。紙で包んで、箱に入れます。少しお待ちください。",
              "Thank you very much.", "ありがとうございます。"),
        ],
        words=[("souvenir", "おみやげ"), ("jug", "水差し"), ("smaller", "もっと小さい"), ("gift", "贈りもの"), ("wrap", "包む")],
        conv=1, flow2=1))

    D.append(dict(
        id='fra_hotel1', who='ホテルのフロント', bg='fhotel', sp='f_front',
        intro='フランクフルトのホテル。夕方の窓の向こうに、マイン川と大聖堂、高いビルが見える。フロントの人は、手順を順番に説明してくれる。',
        pairs=[
            T("Good evening. Welcome. Do you have a reservation?",
              "こんばんは。ようこそ。ご予約はありますか。",
              "Yes, we do. Here is my passport.", "はい、あります。パスポートです。"),
            T("Thank you. First, please check your name. Second, please sign here. Then I give you the key.",
              "ありがとうございます。まずお名前を確認してください。次に、こちらにサインを。それから鍵をお渡しします。",
              "Here you are. Thank you.", "どうぞ。ありがとう。"),
            T("Your room has a view of the river and the cathedral. The lift is on your left.",
              "お部屋からは、川と大聖堂が見えます。エレベーターは左側です。",
              "Wonderful. What time is breakfast tomorrow?", "すてき。明日の朝食は何時ですか。"),
            OT("Breakfast is in the restaurant on the ground floor, from early in the morning. The hours are on the card in your room.",
               "朝食は、1階のレストランで、朝早くからです。時間は、お部屋のカードに書いてあります。",
               [O('rest', "We will go to the restaurant.", "レストランに行きます。", "レストラン", "🍳",
                  ("Good. The restaurant is next to the lobby. You can walk there from the lift.", "わかりました。レストランはロビーのとなりです。エレベーターから歩いて行けます。")),
                O('room', "Can we have breakfast in our room?", "朝食を部屋でとれますか。", "部屋で", "🛏️",
                  ("Yes. Please tell me tonight. I arrange it.", "はい。今夜のうちにお知らせください。手配します。"))],
               cards=1, fork={'tw': ['breakfast']}),
            T("That is all. If you need anything, call the front desk. Good night.",
              "以上です。ご用があれば、フロントにお電話ください。おやすみなさい。",
              "Thank you. Good night.", "ありがとう。おやすみなさい。"),
        ],
        words=[("reservation", "予約"), ("sign", "サインする"), ("key", "鍵"), ("breakfast", "朝食"), ("view", "景色")],
        conv=1, flow2=1))

    # =================== 出発(タスク097。鉄道: フランクフルト中央駅→ブリュッセル乗りかえ→ロンドン) ===================
    D.append(dict(
        id='fra_dep_board1', who='案内係', bg='fboard', sp='f_board',
        intro='朝の中央駅の大ホール。青い大きな発車標の前で、ブリュッセル行きのICEを探す。係員は、聞かれたことを順番に答える。',
        pairs=[
            T("Good morning. Are you looking for your train?",
              "おはようございます。列車をお探しですか。",
              "Good morning. Which platform is the train to London?", "おはようございます。ロンドン行きは何番ホームですか。"),
            T("There is no train to London from here. First, take the ICE to Brussels. You change there.",
              "ここからロンドンへ行く列車はありません。まず、ブリュッセル行きのICEに乗ります。そこで乗りかえます。",
              "I see. Where is the Brussels train on the board?", "なるほど。ブリュッセル行きは、発車標のどこですか。"),
            OT("Look at the board. Brussels is on the second line. It stops in Cologne and Aachen. Do you see it?",
               "発車標を見てください。ブリュッセルは2行目です。ケルンとアーヘンに停まります。見えますか。",
               [O('yes', "Yes, I can see it. Thank you.", "はい、見えます。ありがとう。", "見えた", "👀",
                  ("Good. The platform is on the same line. Check it again before you go. It can change.", "よかった。ホームも同じ行にあります。出発の前にもう一度確認してください。変わることがあります。")),
                O('where', "Which line, please? I cannot see it.", "何行目ですか。見つかりません。", "どこ？", "🔎",
                  ("The second line from the top. It says Brussels-Midi. The platform is on the same line.", "上から2行目です。「Brussels-Midi」と書いてあります。ホームも同じ行です。"))],
               cards=1, fork={'tw': ['line']}),
            T("Do you have another question?",
              "ほかに質問はありますか。",
              "Is this the right train for the Eurostar in Brussels?", "この列車で、ブリュッセルのユーロスターにつながりますか。"),
            T("Yes. In Brussels, you follow the signs and look at the board again. Have a good trip.",
              "はい。ブリュッセルでは、案内板について行って、もう一度発車標を見てください。よい旅を。",
              "Thank you for your help.", "助けてくれてありがとう。"),
        ],
        words=[("platform", "ホーム"), ("line", "行"), ("board", "発車標"), ("change", "乗りかえる"), ("right", "正しい")],
        conv=1, flow2=1))

    D.append(dict(
        id='fra_dep_ticket1', who='窓口の係員', bg='fticket', sp='f_ticket',
        intro='中央駅の窓口(ReiseZentrum)。世界一周航空券の鉄道の区間を見せて、時刻と座席を確かめる。',
        pairs=[
            T("Good morning. Your ticket and your passport, please.",
              "おはようございます。切符とパスポートをお願いします。",
              "Here you are. This is the rail part of our round the world ticket.", "どうぞ。世界一周航空券の鉄道の区間です。"),
            T("Thank you. Let me check. First, the train. Second, the date. Third, the seat.",
              "ありがとうございます。確認します。まず列車。次に日付。3つめに座席。",
              "Can we ride with this ticket?", "この切符で乗れますか。"),
            OT("Yes. The ticket is valid for the ICE to Brussels. Do you want a seat reservation?",
               "はい。この切符は、ブリュッセル行きのICEで使えます。座席の予約はしますか。",
               [O('yes', "Yes, please. Two seats together.", "はい、お願いします。2席、並びで。", "予約する", "💺",
                  ("Two seats together. I reserve them now. Please check the car and the seat number on the paper.", "2席、並びで。いま予約します。紙に書いた号車と席の番号を確認してください。")),
                O('no', "No, thank you. We will sit anywhere.", "いいえ、けっこうです。空いている席に座ります。", "予約しない", "🙅",
                  ("Understood. Then look for a free seat on the train. Please keep your luggage with you.", "わかりました。では、列車で空いている席を探してください。荷物は手元に置いてください。"))],
               cards=1, fork={'tw': ['reservation']}),
            T("Do you have another question?",
              "ほかに質問はありますか。",
              "Is the time to change trains in Brussels enough?", "ブリュッセルでの乗りかえの時間は足りますか。"),
            T("Yes, it is enough if the train is on time. Go to the Eurostar area early, and follow the signs there.",
              "はい、列車が時間どおりなら足ります。ユーロスターの乗り場へは早めに行って、そこの案内に従ってください。",
              "Thank you. We will do that.", "ありがとう。そうします。"),
        ],
        words=[("passport", "パスポート"), ("seat", "座席"), ("reservation", "予約"), ("enough", "足りる"), ("early", "早めに")],
        conv=1, flow2=1))

    D.append(dict(
        id='fra_dep_train1', who='となりの乗客', bg='ftrain', sp='f_pax',
        intro='ホームに止まった白いICE。席を探して、荷物を置く。車掌が切符を見に来る。',
        pairs=[
            T("Good morning. Are you looking for your seats?",
              "おはようございます。お席をお探しですか。",
              "Excuse me. Is this our seat?", "すみません、この席ですか。"),
            T("Yes, it is. The seat number is on the screen above the seat. It is yours.",
              "はい、そうです。席の番号は、席の上の画面に出ています。あなたの席です。",
              "Thank you. Can I put my luggage up there?", "ありがとう。荷物を上に置いてもいいですか。"),
            OT("Of course. Put the big bag on the rack up there. Keep your small bag with you.",
               "もちろん。大きいかばんは、上の棚に置いてください。小さいかばんは手元に。",
               [O('up', "I will put it up there. Thank you.", "上に置きます。ありがとう。", "上に置く", "⬆️",
                  ("Good. The rack is strong. It is safe there.", "いいですね。棚はじょうぶです。そこなら安全です。")),
                O('keep', "I will keep it at my feet.", "足もとに置いておきます。", "足もと", "🧳",
                  ("That is fine, too. Please do not block the aisle.", "それでもかまいません。通路をふさがないようにしてください。"))],
               cards=1, fork={'tw': ['luggage']}),
            T("Good morning. Tickets, please.",
              "おはようございます。切符を拝見します。",
              "Here are our tickets. We change to the Eurostar in Brussels, right?", "切符です。ブリュッセルでユーロスターに乗りかえるのですよね。",
              cx={'sp': 'f_conductor', 'who': '車掌'}),
            T("Correct. This train goes to Brussels. There you change to the Eurostar for London. Enjoy the trip.",
              "そのとおりです。この列車はブリュッセルへ行きます。そこでロンドン行きのユーロスターに乗りかえます。よい旅を。",
              "Thank you very much.", "どうもありがとうございます。",
              cx={'sp': 'f_conductor', 'who': '車掌'}),
        ],
        words=[("seat", "席"), ("luggage", "荷物"), ("rack", "棚"), ("ticket", "切符"), ("conductor", "車掌")],
        conv=1, flow2=1))
