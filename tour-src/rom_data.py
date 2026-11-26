# -*- coding: utf-8 -*-
# 世界一周編 ローマ(タスク094: 到着4場面・街3場面・出発3場面。クロが執筆)。国ごとのデータは別ファイル(アテネ ath_data.py と同じ形)。
#
# 会話の型は 057/061 の新形式(ナイロビ・アテネと同じ flow2=1・cards=1): 相手が英語で話す → 選ぶのは1場面に1回だけ(日本語の短い言葉カード)
#   → お手本は音声だけ → カンペ → 声に出す。失敗時は074の統一ルール(自動おてほん→言い直し→3回目でルルが代わりに言って進む)。
#   どのカードを選んでも物語は進む(止めない・合否なし)。日本語は「カードの言葉」「Meaning!(訳)」にだけ置く。
#
# 雰囲気(PM指示): ローマのスタッフは「陽気で声が大きく、身ぶりが大きい。急いでいても頼めば世話を焼いてくれる」。
#
# 前提(PM指示書 094):
#   - アテネ→ローマはシェンゲン圏内の移動。ローマ到着に入国審査の場面は無い。
#   - ローマの出発は飛行機ではなく鉄道(テルミニ駅)。ローマ→チューリッヒは直通がなく、ミラノ(ミラノ・チェントラーレ)で1回乗り換え(2026-11-26確認済み)。
# 使ってよい実在情報(確認日 2026-11-26。出典は docs/sources.md の「094」):
#   - タクシー: 中心部(城壁の内側)まで 55 ユーロの定額(ADR 公式。PM指示書)。無許可の客引きの「40ユーロ」は断る話(指示書)
#   - 正規のタクシーは白い車で、ドアに「Roma」の文字(PM準備メモ)
#   - レオナルド・エクスプレス: テルミニ駅まで直行・所要は「About thirty minutes」(指示書。運賃・最終便の時刻は資料が割れているので出さない)
#   - 荷物が出てこないときは、受取所を出る前に空港の手荷物の窓口(Baggage Assistance)へ(ITA Airways 公式の案内・PM準備メモ)
#   - テルミニ駅:  発車標でホーム(binario)の番号は発車の少し前に出る(seat61・旅行者の複数の報告。分数は資料が割れているので言わない)。
#     ローマ→ミラノの高速列車は約3時間(PM準備メモ・Interrail 公式)。
#   - 高速列車の席は指定(Trenitalia・Eurail。座席料金の数字は出さない)
# 台詞に出さないもの: 運賃・最終便の時刻・発車時刻・ホーム番号・商品の値段・ホテルや店の値段と名前(指示書に無い。PM確認の点)・個人名。
#   数字は指示書にある 40/55 ユーロ・30分・約3時間と、背景に描かれたベルト番号(twelve)だけ。
import window_data as W
from window_data import star, OT

E = ''


def O(k, y, jp, card, ico, rep):
    return dict(k=k, y=star(y), jp=jp, card=card, ico=ico, rep=rep)


def T(n, njp, y, yjp, **kw):
    d = dict(n=n, njp=njp, y=star(y), yjp=yjp)
    d.update(kw)
    return d


# 声(SP)は build.py に置く: m_bag(手荷物の窓口)・m_tout(客引き)・m_info(案内係)・m_rank(乗り場の係)・m_driver(正規の運転手)・m_rail(空港駅の窓口)・
#   m_gelato・m_shop・m_front・m_tk(テルミニの窓口)・m_board(案内係)・m_pax(となりの乗客)・m_cond(車掌)
def add(D):
    # =================== 到着(入国審査なし) ===================
    D.append(dict(
        id='rom_bag1', who='手荷物の窓口の係員', bg='mbag', sp='m_bag',
        intro='ローマ空港の荷物受取ホール。ベルトの番号は「12」。荷物が1個、いつまでも出てこない。係員は声が大きく、身ぶりが大きい。',
        pairs=[
            T("Ciao, ciao! Waiting for your bags? Look at the sign, my friends. Belt twelve is yours!",
              "チャオ、チャオ！荷物を待っているの？看板を見て。12番のベルトがあなたたちのですよ！",
              "Thank you. Belt twelve. We will wait here.", "ありがとう。12番ですね。ここで待ちます。"),
            T("Good, good! Watch the belt. When your bag comes, take it quickly!",
              "いいですね！ベルトを見ていて。荷物が来たら、すぐ取って！",
              "Our suitcase is blue, with a yellow tag.", "うちのスーツケースは青で、黄色い札がついています。"),
            OT("Hmm... The belt is almost empty now. Is your bag here, my friends?",
               "うーん…ベルトはもうほとんど空っぽです。荷物はありましたか？",
               [O('one', "Excuse me, my bag has not come out.", "すみません、荷物が出てきません。", "出てこない", "🧳",
                  ("Oh, not come out? Don't worry, don't worry! You are at the right place.", "おや、出てこない？心配いりません、心配いりません！ちょうどいい所に来ましたよ。")),
                O('blue', "Excuse me, our blue suitcase is not here.", "すみません、うちの青いスーツケースがありません。", "青いやつ", "🔵",
                  ("Blue, with a yellow tag? I remember! Don't worry, I help you.", "青に、黄色い札ですね？覚えてますよ！心配いりません、手伝います。"))],
               cards=1, fork={'tw': ['bag']}),
            T("This is the baggage desk. Before you leave the hall, you tell us. Your baggage tag, please!",
              "ここは手荷物の窓口です。ホールを出る前に、私たちに言ってください。荷物の札をどうぞ！",
              "Here is the tag. Please find our bag.", "これが札です。荷物を探してください。"),
            T("Perfect! I write everything. We find it, I promise! Where do you stay in Rome?",
              "完璧！全部書きます。きっと見つけます、約束します！ローマではどこに泊まるの？",
              "We stay in a hotel in the city center. Thank you!", "市の中心部のホテルです。ありがとう！"),
        ],
        words=[("belt", "ベルト"), ("baggage tag", "荷物の札"), ("suitcase", "スーツケース"), ("desk", "窓口"), ("wait", "待つ")],
        conv=1, flow2=1))

    D.append(dict(
        id='rom_info1', who='客引きの男', bg='minfo', sp='m_tout',
        intro='到着ロビーを出ると、首から札をさげた男が声をかけてくる。正規のタクシー乗り場は、案内係が知っている。',
        pairs=[
            OT("Taxi, taxi, my friends! Special price! Forty euros, fixed! Come, come with me!",
               "タクシー、タクシー！特別な値段！40ユーロの定額！さあ、さあ、こっちへ！",
               [O('rank', "No, thank you. We will go to the official taxi rank.", "いいえ、けっこうです。正規のタクシー乗り場に行きます。", "正規の乗り場へ", "🚖",
                  ("Okay, okay, no problem! The information desk is over there!", "わかった、わかった！案内所はあっちだよ！")),
                O('where', "No, thank you. Where is the taxi rank, please?", "いいえ、けっこうです。タクシー乗り場はどこですか。", "場所を聞く", "🗺️",
                  ("Okay, okay! Ask the lady at the information desk. Ciao!", "わかった、わかった！案内所のお姉さんに聞いてね。チャオ！"))],
               cards=1, fork={'tw': ['official']}),
            T("Ciao! Buongiorno! The man with the card on his neck? Many people say no to him. How can I help?",
              "チャオ！ブォンジョルノ！首から札をさげた男の人？みんな断りますよ。どうしましたか。",
              "We want a taxi to the city center. Where is the official taxi rank?", "市の中心部までタクシーに乗りたいです。正規の乗り場はどこですか。",
              cx={'sp': 'm_info', 'who': '案内係'}),
            T("Good question! Go out of this hall, and follow the taxi signs. The official taxis are white, with the word Roma on the door.",
              "いい質問です！このホールを出て、タクシーの案内表示について行って。正規のタクシーは白い車で、ドアに「Roma」と書いてあります。",
              "White taxis, with Roma on the door. Thank you.", "白い車で、ドアにRoma。ありがとう。",
              cx={'sp': 'm_info', 'who': '案内係'}),
            T("Exactly! And ask the price before you get in. Always, always!",
              "そのとおり！それから、乗る前に値段を聞いてね。いつでも、いつでも！",
              "We will ask first. Is it far from here?", "先に聞きます。ここから遠いですか。",
              cx={'sp': 'm_info', 'who': '案内係'}),
            T("No, no, not far! Walk, walk, and you see them. Easy! Enjoy Rome, my friends!",
              "いえいえ、遠くないですよ！歩いて、歩いて、見えてきます。簡単！ローマを楽しんで！",
              "Thank you very much. Grazie!", "本当にありがとう。グラーツィエ！",
              cx={'sp': 'm_info', 'who': '案内係'}),
        ],
        words=[("fixed price", "定額"), ("official", "正規の"), ("taxi rank", "タクシー乗り場"), ("information desk", "案内所"), ("door", "ドア")],
        conv=1, flow2=1))

    D.append(dict(
        id='rom_taxi1', who='乗り場の係', bg='mtaxi', sp='m_rank',
        intro='正規のタクシー乗り場。白い車がずらりと並ぶ。乗る前に、定額かどうかを確かめる。',
        pairs=[
            T("Ciao! Welcome to the taxi rank, the real one! Where to, my friends?",
              "チャオ！タクシー乗り場へようこそ、ほんものです！どちらまで？",
              "To the city center, please.", "市の中心部までお願いします。"),
            T("Bene, bene! Come, come. This white car is yours. Let me take your suitcase!",
              "いいね、いいね！さあ、さあ。この白い車です。スーツケースをお預かりします！",
              "Thank you. Careful, please. It is heavy.", "ありがとう。気をつけてください。重いんです。",
              cx={'sp': 'm_driver', 'who': 'タクシーの運転手'}),
            OT("No problem! I am very careful. All good? Any question before we go?",
               "お安いご用です！とても慎重にやりますよ。大丈夫？出発の前に何か質問は？",
               [O('price', "It is a fixed price of fifty-five euros to the center, right?", "中心部まで55ユーロの定額ですよね？", "55ユーロ？", "💶",
                  ("Yes, yes, correct! Fifty-five euros, fixed price, inside the old city walls.", "そう、そのとおり！55ユーロの定額、古い城壁の内側までです。")),
                O('fixed', "Is the fixed price fifty-five euros? We do not want surprises.", "定額は55ユーロですか。びっくりしたくないので。", "びっくり回避", "😅",
                  ("No surprises, my friend! Fifty-five euros, fixed price, to the center.", "びっくりはなし！中心部まで55ユーロの定額です。"))],
               cards=1, fork={'tw': ['fixed']},
               cx={'sp': 'm_driver', 'who': 'タクシーの運転手'}),
            T("Bene! Now sit back and relax. Rome is beautiful today. Is this your first time here?",
              "よし！さあ、ゆったり座って。今日のローマはきれいですよ。ローマは初めて？",
              "Yes, our first time. We are very excited!", "はい、初めてです。とてもわくわくしています！",
              cx={'sp': 'm_driver', 'who': 'タクシーの運転手'}),
            T("Ah, then you will love it! Ask me anything. Let's go, let's go!",
              "おお、じゃあきっと気に入りますよ！何でも聞いてください。さあ、出発、出発！",
              "Thank you. Let's go!", "ありがとう。出発しましょう！",
              cx={'sp': 'm_driver', 'who': 'タクシーの運転手'}),
        ],
        words=[("taxi", "タクシー"), ("fixed price", "定額"), ("city center", "市の中心部"), ("euro", "ユーロ"), ("surprise", "びっくり")],
        conv=1, flow2=1))

    D.append(dict(
        id='rom_train1', who='空港駅の窓口の係員', bg='mtrain', sp='m_rail',
        intro='空港駅の切符売り場。レオナルド・エクスプレスで、テルミニ駅へ。係員はよくしゃべる。',
        pairs=[
            T("Buongiorno, my friends! Tickets for the train? Tell me, tell me. Where do you go?",
              "ブォンジョルノ！電車の切符ですか？教えて、教えて。どちらまで？",
              "To Termini station, please. We would like two tickets.", "テルミニ駅までお願いします。切符を2枚ください。"),
            OT("Ah, Termini! The Leonardo Express goes there. Do you have a question?",
               "ああ、テルミニ駅！レオナルド・エクスプレスが行きますよ。何か質問はありますか。",
               [O('direct', "Does it go straight to Termini?", "テルミニ駅まで直行ですか。", "直行？", "🚆",
                  ("Yes, yes! Straight to Termini, no stops. About thirty minutes!", "はい、はい！テルミニ駅まで直行、止まりません。約30分です！")),
                O('time', "How long does it take?", "何分かかりますか。", "何分？", "⏱️",
                  ("About thirty minutes, and straight to Termini! Very quick, my friend!", "約30分、しかもテルミニ駅まで直行！とても速いですよ！"))],
               cards=1, fork={'tw': ['straight']}),
            T("Perfect! Two tickets, then. How do you pay, by card or in cash?",
              "完璧！では切符を2枚。お支払いは、カードですか、現金ですか。",
              "By card, please.", "カードでお願いします。"),
            T("Bene! Here are your tickets. The train is just there. Look for the sign: Leonardo Express!",
              "よし！切符です。電車はすぐそこ。案内表示を探して：レオナルド・エクスプレス！",
              "Thank you. Which way is the train?", "ありがとう。電車はどちらですか。"),
            T("Follow the signs, and you see it! Have a wonderful time in Rome!",
              "案内表示について行けば、見えますよ！ローマで素敵な時間を！",
              "Thank you very much. Grazie!", "本当にありがとう。グラーツィエ！"),
        ],
        words=[("ticket", "切符"), ("straight", "まっすぐ"), ("minutes", "分"), ("card", "カード"), ("sign", "案内表示")],
        conv=1, flow2=1))

    # =================== 街 ===================
    D.append(dict(
        id='rom_cafe1', who='ジェラテリアの店員', bg='mcafe', sp='m_gelato',
        intro='コロッセオが見える通りのジェラテリア。店員は身ぶりたっぷりで、客を呼びこむ。',
        pairs=[
            T("Ciao, ciao! Welcome! Gelato is happiness, my friends!",
              "チャオ、チャオ！ようこそ！ジェラートは幸せそのものですよ！",
              "It looks great. We would like some gelato.", "おいしそうですね。ジェラートをいただきたいです。"),
            OT("Of course! First, cone or cup?",
               "もちろん！まず、コーンですか、カップですか。",
               [O('cone', "A cone, please.", "コーンでお願いします。", "コーン", "🍦",
                  ("Cone! Crunchy and happy! Perfect for walking.", "コーン！サクサクで幸せ！歩きながら食べるのにぴったり。")),
                O('cup', "A cup, please.", "カップでお願いします。", "カップ", "🥣",
                  ("Cup! Clean and easy. Very smart!", "カップ！汚れなくて食べやすい。かしこい選択！"))],
               cards=1, fork={'tw': ['cone']}),
            T("Now the flavors: chocolate, pistachio, lemon, strawberry... so many!",
              "さあ、味です：チョコ、ピスタチオ、レモン、いちご…たくさんあるでしょう！",
              "Could I have two flavors, half and half?", "2つの味を半分ずつにできますか。"),
            T("Half and half? Of course, no problem! Which two?",
              "半分ずつ？もちろん、お安いご用！どの2つにしますか。",
              "Pistachio and lemon, please.", "ピスタチオとレモンをお願いします。"),
            T("Bellissimo! Here you go. Buon appetito!",
              "ベリッシモ！はい、どうぞ。ボナペティート！",
              "Grazie! It looks delicious.", "グラーツィエ！おいしそう。"),
        ],
        words=[("gelato", "ジェラート"), ("cone", "コーン"), ("cup", "カップ"), ("flavor", "味"), ("half", "半分")],
        conv=1, flow2=1))

    D.append(dict(
        id='rom_shop1', who='おみやげ屋の店主', bg='mshop', sp='m_shop',
        intro='コロッセオの近くのおみやげ屋。店主はよく話し、商品をどんどん見せてくれる。',
        pairs=[
            T("Ciao, ciao! Come in, come in! Look, touch, choose! Rome is in every little thing!",
              "チャオ、チャオ！入って、入って！見て、さわって、選んで！小さな物ひとつひとつにローマが詰まってます！",
              "Thank you. We would like a small souvenir of Rome.", "ありがとう。ローマの小さなおみやげがほしいです。"),
            OT("Wonderful! A magnet, a mug, the Colosseum in miniature... What do you like?",
               "すばらしい！マグネット、マグカップ、コロッセオのミニチュア…どれがお好き？",
               [O('colo', "I like the little Colosseum. How much is it?", "小さなコロッセオがいいです。いくらですか。", "コロッセオ", "🏛️",
                  ("Good eye, my friend! The price is on the little tag. Look, look!", "お目が高い！値段は小さな札に書いてあります。ほら、ほら！")),
                O('mug', "I like the mug. How much is it?", "マグカップがいいです。いくらですか。", "マグカップ", "☕",
                  ("Ah, nice mug! The price is on the bottom. Turn it, turn it!", "おお、いいマグカップ！値段は底に書いてあります。ひっくり返して、ひっくり返して！"))],
               cards=1, fork={'tw': ['price']}),
            T("Look at this one: big, beautiful, no? Everybody loves the big one!",
              "これを見て：大きくて、きれいでしょう？みんな大きいのが大好きなんです！",
              "It is beautiful. Do you have a smaller one, please?", "きれいですね。もう少し小さいのはありますか。"),
            T("Smaller? Sure, sure! Look: a medium one, and a tiny one. Which one?",
              "小さいの？もちろん！ほら：中くらいのと、ちっちゃいの。どっちにします？",
              "The tiny one, please. It fits in our bag.", "ちっちゃいのをお願いします。かばんに入ります。"),
            T("Perfect! I wrap it with love. Is it a gift for a friend?",
              "完璧！愛をこめて包みます。お友だちへの贈り物ですか。",
              "Yes, a gift for a friend at home. Thank you!", "はい、家にいる友だちへの贈り物です。ありがとう！"),
        ],
        words=[("souvenir", "おみやげ"), ("small", "小さい"), ("tag", "値札"), ("wrap", "包む"), ("gift", "贈り物")],
        conv=1, flow2=1))

    D.append(dict(
        id='rom_hotel1', who='ホテルのフロント', bg='mhotel', sp='m_front',
        intro='ローマのホテル。夕方の窓の向こうに、屋根の波とドームが見える。フロントの人は元気いっぱい。',
        pairs=[
            T("Buonasera, and welcome to Rome! Do you have a reservation?",
              "ブォナセーラ、ローマへようこそ！ご予約はありますか。",
              "Yes, we do. Here are our passports.", "はい、あります。パスポートです。"),
            T("Passports, please! I check you in, one moment. Please sign here.",
              "パスポートをどうぞ！チェックインしますね、少々お待ちを。ここにサインを。",
              "Here you are. Thank you.", "どうぞ。ありがとう。"),
            T("Done! Your room is on the top floor. Look out of the window: the roofs of Rome, and a beautiful dome!",
              "できました！お部屋は最上階です。窓の外をどうぞ：ローマの屋根と、きれいなドームが見えますよ！",
              "Wonderful! What time is breakfast tomorrow?", "すてき！明日の朝食は何時ですか。"),
            OT("Breakfast starts early in the morning, on the ground floor. Do you want it in the dining room, or in your room?",
               "朝食は朝早くから、1階です。食堂と、お部屋と、どちらがいいですか。",
               [O('dining', "We will have breakfast in the dining room.", "朝食は食堂でいただきます。", "食堂で", "🍳",
                  ("Wonderful! Fresh bread, fruit, and a real Italian cappuccino!", "すばらしい！焼きたてのパンと果物、本物のイタリアのカプチーノがありますよ！")),
                O('room', "Could we have breakfast in our room?", "朝食を部屋でとれますか。", "部屋で", "🛏️",
                  ("Of course! Tell me tonight, and a cornetto and cappuccino come to your door!", "もちろん！今夜のうちに言ってくれれば、コルネットとカプチーノをお部屋までお届けします！"))],
               cards=1, fork={'tw': ['breakfast']}),
            T("Enjoy your stay, my friends! If you need anything, call me. Now, go and rest!",
              "ごゆっくり！何かあれば呼んでくださいね。さあ、休んで！",
              "Thank you. Buonanotte!", "ありがとう。ブォナノッテ！"),
        ],
        words=[("reservation", "予約"), ("passport", "パスポート"), ("sign", "サインする"), ("breakfast", "朝食"), ("dome", "ドーム")],
        conv=1, flow2=1))

    # =================== 出発(鉄道。テルミニ駅→チューリッヒは、ミラノで1回乗り換え) ===================
    D.append(dict(
        id='rom_dep_ticket1', who='窓口の駅員', bg='mdtick', sp='m_tk',
        intro='テルミニ駅の切符の窓口。世界一周の切符の、鉄道の区間を見せる。駅員は陽気で、話が早い。',
        pairs=[
            T("Buongiorno! Welcome to Termini station. Tickets, information? Tell me, tell me!",
              "ブォンジョルノ！テルミニ駅へようこそ。切符ですか、案内ですか。教えて、教えて！",
              "Hello. We have a world ticket with a train part. Here it is.", "こんにちは。世界一周の切符で、鉄道の区間があります。これです。"),
            T("Oh, a world ticket! Wonderful. Where are you going?",
              "おお、世界一周の切符！すばらしい。どちらまで？",
              "To Zurich, in Switzerland. By train.", "スイスのチューリッヒまで。電車で行きます。"),
            OT("Zurich! Let me look at your ticket... Hmm, interesting. What do you want to know?",
               "チューリッヒ！切符を見せてください…うーん、おもしろい。何が知りたいですか。",
               [O('use', "Can we use this ticket for the train?", "この切符で乗れますか。", "乗れる？", "🎫",
                  ("Yes, yes! This ticket works for the train part. But there is no direct train to Zurich, my friend!", "はい、はい！この切符は鉄道の区間に使えます。でも、チューリッヒへの直通列車はないんです！")),
                O('seat', "What time is the train, and where is our seat?", "電車は何時ですか。座席はどこですか。", "時刻と座席", "💺",
                  ("I check, I check! The seat is on your ticket. But there is no direct train to Zurich, my friend!", "調べますね！座席は切符に書いてあります。でも、チューリッヒへの直通列車はないんです！"))],
               cards=1, fork={'tw': ['ticket']}),
            T("You change in Milan! The first train goes from Rome to Milan, about three hours. Then you take another train to Zurich.",
              "ミラノで乗り換えです！最初の電車はローマからミラノまで、約3時間。それから別の電車でチューリッヒへ行きます。",
              "Change in Milan. Got it. Is our seat on the ticket?", "ミラノで乗り換え。わかりました。座席は切符に書いてありますか。"),
            T("Yes, yes! Look: the carriage and the seat are here. Keep it with you. Safe trip, my friends!",
              "はい、はい！ほら：車両と座席がここに。持っていてくださいね。いい旅を！",
              "Thank you very much. Grazie!", "本当にありがとう。グラーツィエ！"),
        ],
        words=[("ticket", "切符"), ("window", "窓口"), ("change", "乗り換える"), ("seat", "座席"), ("direct", "直通の")],
        conv=1, flow2=1))

    D.append(dict(
        id='rom_dep_platform1', who='案内係', bg='mdplat', sp='m_board',
        intro='テルミニ駅の大きな発車標の前。右の半分が「Partenze(出発)」。ミラノ行きの行だけ光っているが、ホームの番号はまだ出ていない。',
        pairs=[
            T("Ciao! You look at the big board? Very good. It is the departure board: Partenze!",
              "チャオ！大きな発車標を見ていますね？いいですよ。出発の案内板：パルテンツェ！",
              "Yes. Can you tell us how to read it?", "はい。見方を教えてもらえますか。"),
            T("Easy, easy! Left side, arrivals. Right side, departures. Find your city, then look at the last box: Binario, the platform!",
              "簡単、簡単！左が到着、右が出発。行き先の町を見つけて、いちばん右の枠を見て：ビナーリオ、ホームです！",
              "Binario means platform. Okay.", "ビナーリオはホームのことですね。わかりました。"),
            OT("And you? Where do you go, my friends?",
               "それで、あなたたちは？どちらへ行くの？",
               [O('zurich', "Which platform is the train to Zurich?", "チューリッヒ行きは何番ホームですか。", "チューリッヒ行き", "🇨🇭",
                  ("Zurich? No, no, no direct train! First you take the train to Milan. Look, Milano Centrale is here!", "チューリッヒ？いえいえ、直通はありません！まずミラノ行きに乗るんです。ほら、ミラノ・チェントラーレはここ！")),
                O('milan', "Which platform is the train to Milan?", "ミラノ行きは何番ホームですか。", "ミラノ行き", "🚄",
                  ("Milano! Yes! The line is here, look. This is your first train to Zurich!", "ミラノ！そう！行はここ、ほら。これがチューリッヒへの最初の電車です！"))],
               cards=1, fork={'tw': ['platform']}),
            T("Wait, wait. The platform number is not on the board yet. It shows a little before the train leaves. Look: two dashes!",
              "待って、待って。ホームの番号はまだ板に出ていません。電車が出る少し前に出ます。ほら：横線が2本！",
              "I see. So we wait here and watch the board.", "なるほど。ここで待って、板を見ていればいいんですね。"),
            T("Exactly! When the number comes, go to the platform. Be quick, but not crazy! Safe trip, my friends!",
              "そのとおり！番号が出たら、ホームへ。急いで、でも慌てすぎないで！いい旅を！",
              "Thank you. Grazie mille!", "ありがとう。グラーツィエ・ミッレ！"),
        ],
        words=[("board", "発車標"), ("departures", "出発"), ("platform", "ホーム"), ("number", "番号"), ("wait", "待つ")],
        conv=1, flow2=1))

    D.append(dict(
        id='rom_dep_train1', who='となりの乗客', bg='mdtrain', sp='m_pax',
        intro='ミラノ行きの電車の中。席を探す。となりの乗客はおしゃべりで、車掌は陽気。',
        pairs=[
            T("Ciao! You look for your seats? Check your ticket: carriage and seat.",
              "チャオ！席を探してる？切符を見て：車両と座席ですよ。",
              "Yes. Excuse me, is this my seat?", "はい。すみません、この席ですか。"),
            T("Let me see your ticket... Yes, yes, it is! And the seat next to it is for your friend.",
              "切符を見せて…そう、そうです！そのとなりがお友だちの席。",
              "Great. It is a long trip, so I am happy.", "よかった。長い旅なので、ほっとしました。"),
            OT("Welcome, welcome! Is your suitcase heavy? There is a rack above the seats, my friend.",
               "ようこそ、ようこそ！スーツケースは重い？席の上に荷物棚がありますよ。",
               [O('up', "May I put my luggage up there?", "荷物を上に置いてもいいですか。", "上に置く", "🧳",
                  ("Of course, of course! Careful, careful. You are strong!", "もちろん、もちろん！気をつけて。力持ちですね！")),
                O('help', "Could you help me put it up there?", "上に置くのを手伝ってもらえますか。", "手伝って", "💪",
                  ("Sure, sure! One, two, three, up! Bellissimo!", "まかせて！せーの、よいしょ！ベリッシモ！"))],
               cards=1, fork={'tw': ['luggage']}),
            T("Buongiorno! Tickets, please. Show me, show me!",
              "ブォンジョルノ！切符を拝見します。見せて、見せて！",
              "Here is our ticket. Thank you.", "切符です。ありがとう。",
              cx={'sp': 'm_cond', 'who': '車掌'}),
            T("Perfect! Remember: you change in Milan. Check the board there. Safe trip, my friends!",
              "完璧！覚えておいて：ミラノで乗り換えです。あちらでも発車標を見てね。いい旅を！",
              "Thank you. We will. Grazie!", "ありがとう。そうします。グラーツィエ！",
              cx={'sp': 'm_cond', 'who': '車掌'}),
        ],
        words=[("seat", "席"), ("luggage", "荷物"), ("rack", "荷物棚"), ("carriage", "車両"), ("conductor", "車掌")],
        conv=1, flow2=1))
