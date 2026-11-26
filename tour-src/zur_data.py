# -*- coding: utf-8 -*-
# 世界一周編 チューリッヒ(タスク096 到着4場面・街3場面・出発3場面。クロが執筆)。国ごとのデータは別ファイル(ath_data.py と同じ形)。
#
# 会話の型は 057/061 の新形式(flow2=1・cards=1): 相手が英語で話す → 選ぶのは1場面に1回だけ(日本語の短い言葉カード)
#   → お手本は音声だけ → カンペ → 声に出す。失敗時は074の統一ルール(自動おてほん→言い直し→3回目でルルが代わりに言って進む)。
#   どのカードを選んでも物語は進む(止めない・合否なし)。日本語は「カードの言葉」「Meaning!(訳)」にだけ置く。
#
# 雰囲気(096指示書): チューリッヒのスタッフは「正確でてきぱき。少しそっけないが、頼めばきちんと教えてくれる」。
#
# 前提(096指示書・zurich-prep.md): 到着も出発も鉄道(チューリッヒ中央駅 Zürich HB)。到着はローマ発・ミラノ乗り換えのユーロシティ。
#   出発はフランクフルト行きの直通ICE(乗り換えなし・約4時間。時刻表サイト2つの一致で確認済み)。
#   スイスはシェンゲン加盟・この旅はアテネで入国済み → 駅に入国審査の場面は作らない。
#
# 台詞に出さないもの: トラム運賃・コインロッカー料金・商品や飲み物の値段(未確認)・正確な発車時刻・ホームの番号・トラムの系統番号・
#   店名/ホテル名(指示書に無い。PM確認の点)・個人名。数字(0-9)は一切使わない。
#   例外(指示書の前提そのもの): 切符の窓口の「約4時間」は four hours と綴って出す(zur_dep_ticket1 だけ)。
#   使ってよい実在情報: Gleis=ホーム/Fernverkehr=長距離列車/S-Bahn=近郊電車(下絵の写真で読めた実文言)・チューリッヒは物価が高い(口コミ多数・値段は出さない)。
# 発車標の別素材 zurich-board-fra-v1.png(tour-src/art/prep_096.py)は zur_dep_board1 だけに重ねる。番号の9は物語の中の架空(台詞には出さない)。
import window_data as W
from window_data import star, OT

E = ''


def O(k, y, jp, card, ico, rep):
    return dict(k=k, y=star(y), jp=jp, card=card, ico=ico, rep=rep)


def T(n, njp, y, yjp, **kw):
    d = dict(n=n, njp=njp, y=star(y), yjp=yjp)
    d.update(kw)
    return d


# 声(SP)は build.py に置く: z_info(案内係)・z_locker(ロッカーの係員)・z_tram(トラム乗り場の係員)・z_info2(案内所の係員)・z_waiter・z_shop・z_front・
#   z_board(発車標の前の案内係)・z_window(窓口の係員)・z_pass(となりの乗客)・z_conductor(車掌)
def add(D):
    # =================== 到着(鉄道・審査なし) ===================
    D.append(dict(
        id='zur_arr1', who='駅の案内係', bg='zarr', sp='z_info',
        intro='チューリッヒ中央駅の大ホール。ミラノで乗り換えた電車を降りたところ。頭の上に、大きな発車標と駅の時計。',
        pairs=[
            T("Grüezi. Welcome to Zurich. Can I help you?",
              "グリュエツィ(こんにちは)。チューリッヒへようこそ。お手伝いしましょうか。",
              "Hello. Can we go to our hotel by tram?", "こんにちは。ホテルへはトラムで行けますか。"),
            T("Yes, you can. The trams are in front of the station. First, look up at the big board.",
              "はい、行けます。トラムは駅の前です。まず、上の大きな発車標を見てください。",
              "The big board? What do the colors mean?", "大きな発車標ですか。色は何の意味ですか。"),
            T("Red is for the long distance trains. Blue is for the local trains. And the big clock shows the exact time.",
              "赤は長距離列車、青は近郊の電車です。そして大きな時計が、正確な時刻を示します。",
              "I see. Thank you. The clock is important here?", "なるほど。ありがとう。ここでは時計が大事なんですか。"),
            OT("Yes. Trains here are usually on time. Now, what do you need first?",
               "はい。ここの電車はたいてい時間どおりです。さて、まず何が必要ですか。",
               [O('stop', "The tram stop first, please.", "まずトラム乗り場をお願いします。", "乗り場", "🚋",
                  ("Go out through the main exit. The tram stops are right in front of the station.", "正面の出口から出てください。トラムの乗り場は駅のすぐ前です。")),
                O('machine', "The ticket machine first, please.", "まず券売機をお願いします。", "券売機", "🎟️",
                  ("The ticket machines are at the tram stop. You can also use an app.", "券売機はトラムの乗り場にあります。アプリも使えますよ。"))],
               cards=1, fork={'tw': ['tram']}),
            T("You are welcome. Enjoy Zurich.",
              "どういたしまして。チューリッヒを楽しんで。",
              "Thank you very much. Danke!", "本当にありがとう。ダンケ！"),
        ],
        words=[("tram", "トラム(路面電車)"), ("board", "発車標(電光掲示板)"), ("long distance", "長距離の"), ("local", "近くの・地元の"), ("exact", "正確な")],
        conv=1, flow2=1))

    D.append(dict(
        id='zur_locker1', who='駅の係員', bg='zlock', sp='z_locker',
        intro='大ホールのコインロッカーのそば。大きいスーツケースを、ホテルに着く前に預けたい。',
        pairs=[
            T("Hello. Do you need something?",
              "こんにちは。何かご用ですか。",
              "Hello. We want to leave our big suitcases. Where are the lockers?", "こんにちは。大きいスーツケースを預けたいです。ロッカーはどこですか。"),
            T("The lockers are inside the station. Follow the locker signs. It is not far.",
              "ロッカーは駅の中にあります。ロッカーの案内表示について行って。遠くありません。",
              "Thank you. Do you have a big locker?", "ありがとう。大きいロッカーはありますか。"),
            OT("Yes. We have small, medium, and large lockers. Which one do you need?",
               "はい。小・中・大のロッカーがあります。どれが必要ですか。",
               [O('large', "A large locker, please. Our suitcases are big.", "大きいロッカーをお願いします。スーツケースが大きいので。", "大きいの", "🧳",
                  ("A large one. Good. Big bags need a big locker.", "大きいの。いいですね。大きい荷物には大きいロッカーです。")),
                O('medium', "A medium locker, please. We have only one bag.", "中くらいのをお願いします。荷物はひとつだけです。", "中くらい", "👜",
                  ("A medium one. That is fine for one bag.", "中くらいの。荷物がひとつなら大丈夫です。"))],
               cards=1, fork={'tw': ['locker']}),
            T("Put your bag in and close the door. Then follow the machine. It gives you a receipt. Keep it safe.",
              "荷物を入れて、ドアを閉めて。それから機械の案内に従って。レシートが出ます。大切に持っていてください。",
              "Understood. Can we take our bags out later today?", "わかりました。今日あとで荷物を出せますか。"),
            T("Yes. Use the receipt, and the locker opens again. Have a nice day in Zurich.",
              "はい。そのレシートで、ロッカーがまた開きます。チューリッヒで、いい一日を。",
              "Thank you. Goodbye!", "ありがとう。さようなら！"),
        ],
        words=[("locker", "コインロッカー"), ("suitcase", "スーツケース"), ("receipt", "レシート"), ("large", "大きい"), ("keep", "持っておく・保管する")],
        conv=1, flow2=1))

    D.append(dict(
        id='zur_tram1', who='トラム乗り場の係員', bg='ztram', sp='z_tram',
        intro='駅の前のトラム乗り場。青い券売機のそばに、乗り場の係員が立っている。',
        pairs=[
            T("Hello. Are you looking for a tram ticket? The blue machine is right here.",
              "こんにちは。トラムの切符をお探しですか。青い券売機はここです。",
              "Yes, please. How do we buy a ticket?", "はい、お願いします。どうやって切符を買いますか。"),
            T("Choose your ticket on the screen, and pay. Buy the ticket before you get on the tram.",
              "画面で切符を選んで、支払います。切符はトラムに乗る前に買ってください。",
              "Before we get on. I see. Can I use this ticket on the tram?", "乗る前に、ですね。わかりました。この切符でトラムに乗れますか。"),
            OT("Let me see. Yes, this ticket is fine for the tram. Where did you buy it?",
               "見せてください。はい、この切符でトラムに乗れます。どこで買いましたか。",
               [O('here', "I bought it at this machine.", "この券売機で買いました。", "ここで買った", "🎟️",
                  ("Good. Then you can ride the tram right away.", "いいですね。では、すぐトラムに乗れます。")),
                O('app', "I bought it on my phone.", "スマホで買いました。", "スマホで", "📱",
                  ("That is fine. Many people use the app.", "大丈夫です。アプリを使う人は多いですよ。"))],
               cards=1, fork={'tw': ['ticket']}),
            T("Which tram do you need? Tell me the street or the area of your hotel.",
              "どのトラムが必要ですか。ホテルの通りか、地区を教えてください。",
              "Our hotel is near the river. Which tram goes there?", "ホテルは川の近くです。どのトラムが行きますか。"),
            T("Look at the map here. The line number is on the front of every tram. If you are not sure, ask the driver.",
              "ここの地図を見て。系統の番号は、どのトラムの前にも出ています。自信がなければ、運転手に聞いてください。",
              "Thank you. We will ask the driver.", "ありがとう。運転手に聞いてみます。"),
        ],
        words=[("tram", "トラム(路面電車)"), ("ticket", "切符"), ("machine", "券売機"), ("driver", "運転手"), ("map", "地図")],
        conv=1, flow2=1))

    D.append(dict(
        id='zur_info1', who='案内所の係員', bg='zinfo', sp='z_info2',
        intro='大ホールの案内所。明日のフランクフルト行きの乗り方と、駅の出口を聞いておきたい。',
        pairs=[
            T("Grüezi. How can I help you?",
              "グリュエツィ(こんにちは)。ご用件は何でしょう。",
              "Hello. We take a train to Frankfurt tomorrow. How can we find the platform?", "こんにちは。明日フランクフルト行きの電車に乗ります。ホームはどうやって調べますか。"),
            T("Look at the big board, or use the railway app. The platform is called Gleis. Check it again on the day.",
              "大きな発車標を見るか、鉄道のアプリを使ってください。ホームのことはグライスといいます。当日、もう一度確認して。",
              "Gleis means platform, right?", "グライスはホームのことですね。"),
            OT("Right. Is there anything else? The exit, or the taxis?",
               "そのとおりです。ほかにありますか。出口ですか、タクシーですか。",
               [O('exit', "Where is the exit, please?", "出口はどこですか。", "出口", "🚪",
                  ("Follow the signs that say Ausgang. The main exit is at the end of the hall.", "アウスガング(出口)と書かれた案内に従って。正面の出口は、ホールの突き当たりです。")),
                O('taxi', "Where can we find a taxi?", "タクシーはどこで乗れますか。", "タクシー", "🚕",
                  ("The taxis wait outside the main exit. In the city, the tram is easy, too.", "タクシーは正面の出口の外で待っています。街の中なら、トラムも簡単ですよ。"))],
               cards=1, fork={'tw': ['exit']}),
            T("Tomorrow, come to the hall a little early. Look at the board first.",
              "明日は、少し早めにホールへ来てください。まず発車標を見て。",
              "Good idea. Why should we come early?", "いい考えですね。なぜ早く来るのですか。"),
            T("Then you can find the platform calmly. Trains here leave on time, so they do not wait.",
              "そうすれば、落ち着いてホームを探せます。ここの電車は時間どおりに出るので、待ってくれません。",
              "I understand. Thank you for your help.", "わかりました。助けてくれてありがとう。"),
        ],
        words=[("platform", "ホーム"), ("exit", "出口"), ("taxi", "タクシー"), ("early", "早めに"), ("on time", "時間どおりに")],
        conv=1, flow2=1))

    # =================== 街 ===================
    D.append(dict(
        id='zur_cafe1', who='カフェの店員', bg='zcafe', sp='z_waiter',
        intro='バンホフ通りのカフェ。外のテーブルに座る。店員は静かで、てきぱきしている。',
        pairs=[
            T("Grüezi. Please sit anywhere. What would you like?",
              "グリュエツィ(こんにちは)。どこでもお好きな席へ。何にしますか。",
              "An espresso and a water, please.", "エスプレッソと、水をお願いします。"),
            OT("Of course. Still water, or sparkling water?",
               "かしこまりました。炭酸なしの水ですか、炭酸入りですか。",
               [O('still', "Still water, please.", "炭酸なしの水をお願いします。", "炭酸なし", "💧",
                  ("Still water. Good. One moment.", "炭酸なしの水ですね。少々お待ちを。")),
                O('sparkling', "Sparkling water, please.", "炭酸入りの水をお願いします。", "炭酸入り", "🫧",
                  ("Sparkling. Coming right up.", "炭酸入りですね。すぐお持ちします。"))],
               cards=1, fork={'tw': ['water']}),
            T("Here you are. An espresso and a water.",
              "お待たせしました。エスプレッソと、お水です。",
              "Thank you. How much is it, please?", "ありがとう。いくらですか。"),
            T("The bill is on the little tray. Please take a look.",
              "お会計は、小さいトレイの上です。ご覧ください。",
              "Oh... it is expensive, isn't it?", "えっ…高いですね。"),
            T("Yes. Zurich is an expensive city. If you want something cheaper, try a supermarket near the station.",
              "ええ。チューリッヒは物価の高い街です。もっと安くしたいなら、駅の近くのスーパーを試してください。",
              "Good idea. Thank you for telling us.", "いい考えですね。教えてくれてありがとう。"),
        ],
        words=[("espresso", "エスプレッソ"), ("sparkling water", "炭酸水"), ("bill", "お会計"), ("expensive", "高い"), ("cheaper", "もっと安い")],
        conv=1, flow2=1))

    D.append(dict(
        id='zur_shop1', who='おみやげ屋の店員', bg='zshop', sp='z_shop',
        intro='バンホフ通りのおみやげ屋。スイスのチョコレートと、小さい時計。店員はもの静かで、聞けば丁寧に答える。',
        pairs=[
            T("Hello. Take your time. Please tell me if you need help.",
              "こんにちは。ゆっくりどうぞ。お手伝いが必要なら言ってください。",
              "Thank you. We want a Swiss chocolate for a gift.", "ありがとう。おみやげに、スイスのチョコレートがほしいです。"),
            OT("Of course. Milk chocolate, or dark chocolate?",
               "もちろん。ミルクチョコレートですか、ダークチョコレートですか。",
               [O('milk', "Milk chocolate, please.", "ミルクチョコレートをお願いします。", "ミルク", "🍫",
                  ("Milk chocolate. A classic choice.", "ミルクチョコレート。定番の選び方ですね。")),
                O('dark', "Dark chocolate, please.", "ダークチョコレートをお願いします。", "ダーク", "🍫",
                  ("Dark chocolate. A good choice.", "ダークチョコレート。いい選択です。"))],
               cards=1, fork={'tw': ['chocolate']}),
            T("And here are small watches. They are popular souvenirs.",
              "それから、こちらは小さい時計です。人気のおみやげですよ。",
              "Nice. How much is this small watch?", "すてき。この小さい時計はいくらですか。"),
            T("The price is on the tag. It is a Swiss watch, so it is not cheap.",
              "値段はタグに書いてあります。スイスの時計なので、安くはありません。",
              "I see. Do you have a cheaper one?", "そうですか。もう少し安いのはありますか。"),
            T("Yes. These smaller ones are cheaper. A chocolate bar is also a nice, small gift.",
              "はい。こちらの小さいものなら、もっと安いです。板チョコも、ちょっとしたいい贈り物ですよ。",
              "Thank you. We will think about it.", "ありがとう。考えてみます。"),
        ],
        words=[("souvenir", "おみやげ"), ("chocolate", "チョコレート"), ("watch", "腕時計"), ("price", "値段"), ("cheaper", "もっと安い")],
        conv=1, flow2=1))

    D.append(dict(
        id='zur_hotel1', who='ホテルのフロント係', bg='zhotel', sp='z_front',
        intro='ホテルの部屋の前のフロント。夕方。窓の向こうに、川と古い教会の塔が見える。',
        pairs=[
            T("Good evening. Welcome. Do you have a reservation?",
              "こんばんは。ようこそ。ご予約はありますか。",
              "Yes, we do. Here is my passport.", "はい、あります。パスポートです。"),
            T("Thank you. One moment, please. Could you fill in this form?",
              "ありがとうございます。少々お待ちください。この用紙に記入していただけますか。",
              "Of course. Here you are.", "もちろんです。どうぞ。"),
            T("Thank you. All done. Your room has a lovely view of the river and the old church.",
              "ありがとうございます。手続きは終わりです。お部屋からは、川と古い教会がきれいに見えます。",
              "Wonderful. What time is breakfast tomorrow, and where?", "すてき。明日の朝食は何時で、どこですか。"),
            OT("Breakfast is in the restaurant next to the lobby. It starts early in the morning. Do you need a wake-up call for your train?",
               "朝食は、ロビーのとなりのレストランです。朝早くから始まります。電車に乗るので、モーニングコールは必要ですか。",
               [O('call', "Yes, a wake-up call, please.", "はい、モーニングコールをお願いします。", "起こして", "⏰",
                  ("Of course. I will call your room in the morning.", "かしこまりました。朝、お部屋に電話します。")),
                O('alarm', "No, thank you. We have an alarm.", "いいえ、大丈夫です。目覚ましがあります。", "目覚まし", "📱",
                  ("Good. Please set it carefully. Trains here leave on time.", "いいですね。しっかりセットしてください。ここの電車は時間どおりに出ますから。"))],
               cards=1, fork={'tw': ['wake-up']}),
            T("Enjoy your stay. If you need anything, I am here at the front desk.",
              "ごゆっくりお過ごしください。何かあれば、フロントにおります。",
              "Thank you. Good night!", "ありがとう。おやすみなさい！"),
        ],
        words=[("reservation", "予約"), ("form", "用紙"), ("view", "景色"), ("breakfast", "朝食"), ("wake-up call", "モーニングコール")],
        conv=1, flow2=1))

    # =================== 出発(鉄道・フランクフルト行き直通) ===================
    D.append(dict(
        id='zur_dep_board1', who='駅の案内係', bg='zboard', sp='z_board',
        intro='翌朝、大ホール。頭の上の大きな発車標に、フランクフルト行きの行が出ている。',
        pairs=[
            T("Hello. Can I help you?",
              "こんにちは。ご用件は何でしょう。",
              "Hello. Which platform is the train to Frankfurt?", "こんにちは。フランクフルト行きは何番ホームですか。"),
            T("Look at the big board. The long distance trains are on the red side. Find Frankfurt.",
              "大きな発車標を見てください。長距離列車は赤い側です。フランクフルトを探して。",
              "I see Frankfurt. Where do I read the platform?", "フランクフルトがありました。ホームはどこを読みますか。"),
            OT("Read the same line to the right. The column called Gleis shows the platform. Do you see it?",
               "同じ行の右を読んで。グライスという欄に、ホームが出ています。見えますか。",
               [O('see', "Yes, I see it now.", "はい、見えました。", "見えた", "👀",
                  ("Good. Go to that platform.", "いいですね。そのホームへ行ってください。")),
                O('help', "Not yet. Could you show me?", "まだです。教えてもらえますか。", "教えて", "🙏",
                  ("Look at the line with Frankfurt. The number under Gleis is your platform.", "フランクフルトの行を見て。グライスの下の数字が、あなたのホームです。"))],
               cards=1, fork={'tw': ['platform']}),
            T("Trains here leave on time. Please be at the platform a little early.",
              "ここの電車は時間どおりに出ます。少し早めにホームにいてください。",
              "Understood. Is the platform far from here?", "わかりました。ホームはここから遠いですか。"),
            T("No. Follow the signs that say Gleise. They point to the platforms.",
              "いいえ。グライゼ(ホーム)と書かれた案内に従って。ホームのほうを指しています。",
              "Thank you very much.", "どうもありがとうございます。"),
        ],
        words=[("platform", "ホーム"), ("board", "発車標"), ("column", "欄"), ("long distance train", "長距離列車"), ("follow", "従う・ついて行く")],
        conv=1, flow2=1))

    D.append(dict(
        id='zur_dep_ticket1', who='切符の窓口の係員', bg='zticket', sp='z_window',
        intro='ホームのそばの切符の窓口。世界一周航空券の、鉄道の区間を見せる。',
        pairs=[
            T("Hello. Let me see your ticket, please.",
              "こんにちは。切符を見せてください。",
              "Here you are. Can I take the train with this ticket?", "どうぞ。この切符で乗れますか。"),
            T("Let me check. Yes, this ticket works for the train to Frankfurt. Now we check the time and your seat.",
              "確認しますね。はい、この切符でフランクフルト行きに乗れます。では、時刻と席を確認しましょう。",
              "Thank you. Do we need to change trains?", "ありがとう。乗り換えは必要ですか。"),
            OT("No. It is a direct train. It takes about four hours. Would you like a window seat or an aisle seat?",
               "いいえ。直通列車です。約四時間かかります。窓側の席と通路側の席、どちらがいいですか。",
               [O('window', "A window seat, please.", "窓側をお願いします。", "窓側", "🪟",
                  ("A window seat. Good for the view.", "窓側ですね。景色がよく見えますよ。")),
                O('aisle', "An aisle seat, please.", "通路側をお願いします。", "通路側", "🚶",
                  ("An aisle seat. Easy to move around.", "通路側ですね。動きやすいですよ。"))],
               cards=1, fork={'tw': ['seat']}),
            T("Here is your seat reservation. The coach and the seat are written here. Keep it with your ticket.",
              "こちらが座席の予約票です。車両と席が書いてあります。切符と一緒に持っていてください。",
              "Thank you. The time is on the ticket, right?", "ありがとう。時刻は切符に書いてありますね。"),
            T("Yes. The time is on your ticket and on the board. Please check both. Have a good trip.",
              "はい。時刻は切符と発車標に出ています。両方を確認してください。いい旅を。",
              "Thank you very much!", "どうもありがとうございます！"),
        ],
        words=[("direct", "直通の"), ("seat", "席"), ("reservation", "予約"), ("aisle", "通路"), ("coach", "客車")],
        conv=1, flow2=1))

    D.append(dict(
        id='zur_dep_train1', who='となりの乗客', bg='ztrain', sp='z_pass',
        intro='ホームから乗りこんだ列車の中。席を探すと、となりの席の人が声をかけてくれた。',
        pairs=[
            T("Oh, hello. Are you looking for your seats?",
              "あら、こんにちは。席をお探しですか。",
              "Yes. Excuse me, is this our seat?", "はい。すみません、この席ですか。",
              ),
            T("Let me look at your reservation. Yes, these are your seats. Please sit down.",
              "予約票を見せてください。はい、ここがお席です。どうぞ座って。",
              "Thank you. May I put my bag up there?", "ありがとう。荷物を上に置いてもいいですか。"),
            OT("Of course. You can use the rack above the seats, or keep it near your feet.",
               "もちろん。席の上の棚を使えますし、足もとに置いてもいいですよ。",
               [O('rack', "I will put it on the rack.", "棚に置きます。", "棚に", "🧳",
                  ("Good. It is easy to take down later.", "いいですね。あとで下ろしやすいですよ。")),
                O('feet', "I will keep it near my feet.", "足もとに置きます。", "足もと", "🦶",
                  ("Good. Just keep the aisle free.", "いいですね。通路だけはあけておいてくださいね。"))],
               cards=1, fork={'tw': ['rack']}),
            T("Hello. Tickets, please.",
              "こんにちは。切符を拝見します。",
              "Here you are. This is our ticket and our reservation.", "どうぞ。これが切符と予約票です。",
              cx={'sp': 'z_conductor', 'who': '車掌'}),
            T("Thank you. Everything is fine. This train goes straight to Frankfurt. Have a good trip.",
              "ありがとうございます。問題ありません。この列車はフランクフルトまで直通です。いい旅を。",
              "Thank you. We will enjoy the ride.", "ありがとう。乗るのを楽しみます。",
              cx={'sp': 'z_conductor', 'who': '車掌'}),
        ],
        words=[("seat", "席"), ("rack", "(頭上の)荷物棚"), ("conductor", "車掌"), ("ticket", "切符"), ("straight", "まっすぐ・直通で")],
        conv=1, flow2=1))
