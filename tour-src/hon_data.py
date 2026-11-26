# -*- coding: utf-8 -*-
# 世界一周編 ホノルル(タスク101。到着4場面＋街3場面＋出発3場面。クロが執筆)。国ごとのデータは別ファイル(fra_data.py と同じ形)。
#
# 会話の型は fra_data.py と同じ新形式(flow2=1・cards=1): 相手が英語で話す → 選ぶのは1場面に1回だけ(日本語の短い言葉カード)
#   → お手本は音声だけ → カンペ → 声に出す。失敗時は074の統一ルール(自動おてほん→言い直し→3回目でルルが代わりに言って進む)。
#   どのカードを選んでも物語は進む(止めない・合否なし)。日本語は「カードの言葉」「Meaning!(訳)」にだけ置く。
#
# 雰囲気(指示書): ホノルルのスタッフは「明るくのんびり。"Aloha" の挨拶で始まり、急がせない」。
#   → 「No rush.」「Take your time.」「No worries.」で急がせない。ただし毎回同じ文にしないよう、あいさつ・おわりは場面ごとに言い分ける(Aloha / Mahalo / Enjoy など)。
#
# 大前提(指示書): 到着はニューヨークからの国内線なので入国審査はない(入国審査の場面は作らない)。中心は農産物申告書。
#   出発はシドニー行きの国際線。米国の出国審査はない。シドニー行きの航空会社名・便名・ターミナル名は台詞にも表示にも出さない(未決定)。
#
# 使ってよい実在情報(確認日 2026-11-27。出典は docs/sources.md の「タスク101」):
#   - ハワイ州農務局の「植物と動物の申告書」は、本土から着く全員が出す決まり(1973年から)。機内で配られ、着陸前に乗務員が集める(HDOA)。
#     申告する物(果物・植物・動物など)は、荷物受取エリアの出口の近くの農業検査カウンターで検査を受ける(HDOA・HNL空港公式)。
#     → 「どこに出しますか？」への答えは、機内で乗務員が集めるのがふつう。まだ持っていれば検査の係員に見せる。台詞は「この申告書」で通し、正式名称は出さない。
#   - 空港の荷物ベルトの案内: 画面で便とベルトが分かる(一般手順)。荷物が出ないときは航空会社の荷物窓口でタグを見せる(一般手順)。
#   - 空港のレイ売り場は実在(HNL空港公式・Hawaii Magazine)。生花のレイ。蘭やプルメリアが定番。バス停はレイ売り場の東側(空港公式 airports.hawaii.gov/hnl/?p=4024)。
#   - 空港からワイキキへ市バス(W Line)。荷物は「座席の下・足もと・ひざ」に収まるものだけ(TheBus公式・空港公式)。ワイキキ・トロリーは観光用で空港には行かない(waikikitrolley.com)。
#     鉄道(Skyline)は2025年10月に空港駅(Lelepaua)まで開通済みで、ワイキキにはまだ届かない(honolulu.gov・Star-Advertiser)。シャトルバンはワイキキのホテルへ(AAA tripcanvas)。
#   - シェイブアイスは細かく削った柔らかい氷にシロップがしみる。スノーコーンは砕いた氷でシロップが底に沈む(Matador Network・Wikipedia)。レインボーは3色のシロップ。スノーキャップ=練乳(Matador Network)。
#   - ホテルはパスポート確認とクレジットカード(追加料金用)を求めるのが一般的(Hilton公式の注記)。ラナイ=バルコニー。
#   - 米国のTSA: 2025年7月から靴を脱がなくてよい(全国方針)。ただし係員に言われたら従う。ノートPCは通常レーンでは出して別のトレーに(tsa.gov)。新型のCTスキャナーのレーンでは入れたままでよい(2026年は導入の途中。レーンで違う)。
# 台詞に出さないもの(未確認): 運賃・チップの割合・商品や食事の値段・正確な出発時刻・ゲートやベルトの番号・バスの路線番号・所要の分数・航空会社名・便名・ターミナル名・店名・ホテル名。
#   値段は「小さなタグを見て」のように言い、数字は出さない。ゲートは「案内板で見て」と言う。個人名なし。
#   ホノルルの出発の「米国本土行きの農業検査(USDA)」はシドニー行きに適用されるか未確認なので、場面には入れない。
import window_data as W
from window_data import star, OT

E = ''


def O(k, y, jp, card, ico, rep):
    return dict(k=k, y=star(y), jp=jp, card=card, ico=ico, rep=rep)


def T(n, njp, y, yjp, **kw):
    d = dict(n=n, njp=njp, y=star(y), yjp=yjp)
    d.update(kw)
    return d


# 声(SP)は build.py に置く: h_agri・h_bagst・h_lei・h_bus・h_ice・h_shop・h_front・h_board・h_ticket・h_tsa
def add(D):
    # =================== 到着(タスク101。ニューヨークからの国内線。入国審査なし) ===================
    D.append(dict(
        id='hnl_form1', who='農業検査の係員', bg='hnarr', sp='h_agri',
        intro='ホノルル空港。機内で書いた申告書を持って、農業検査の係員に聞く。ハワイは農業と自然を守る決まりが厳しい。係員は明るくのんびり話す。',
        pairs=[
            T("Aloha! Welcome to Hawaii. Can I help you?",
              "アロハ！ハワイへようこそ。何かお手伝いしましょうか。",
              "Aloha. Where do we give this form, please?", "アロハ。この申告書はどこに出しますか。"),
            T("No rush. On the plane, the crew usually collects it before landing. If you still have it, show it to me.",
              "急がなくて大丈夫。ふつうは着陸の前に、機内で乗務員が集めます。まだ持っているなら、私に見せてください。",
              "Here it is. We wrote it on the plane.", "これです。機内で書きました。"),
            OT("Thank you. Now, do you have any fruit, plants, or seeds in your bags?",
               "ありがとうございます。では、かばんに果物や植物、種はありますか。",
               [O('no', "No, we have no fruit or plants.", "いいえ、果物も植物もありません。", "ない", "✅",
                  ("Good. Then you are all set. Thank you for helping to protect Hawaii.", "けっこうです。では手続きは終わりです。ハワイを守る協力に感謝します。")),
                O('yes', "Yes, we have some fruit in our bag.", "はい、かばんに果物があります。", "ある", "🍎",
                  ("Thank you for telling me. Please bring it to the agriculture counter. An inspector will look at it.", "教えてくれてありがとう。農業検査のカウンターに持って行ってください。検査員が見ます。"))],
               cards=1, fork={'tw': ['fruit']}),
            T("Hawaii has many special plants and animals. One small insect or seed can hurt them. So we check.",
              "ハワイには特別な植物や動物がたくさんいます。小さな虫や種ひとつで、傷つくことがあります。だから調べるのです。",
              "I see. That is why this form is important.", "なるほど。だからこの申告書が大切なのですね。"),
            T("Exactly. The agriculture counter is near the exits, in the baggage claim area. Enjoy your stay. Aloha!",
              "そのとおり。農業検査のカウンターは、荷物受取エリアの出口の近くです。ごゆっくり。アロハ！",
              "Thank you very much. Aloha!", "どうもありがとうございます。アロハ！"),
        ],
        words=[("form", "申告書"), ("fruit", "果物"), ("plant", "植物"), ("inspector", "検査員"), ("protect", "守る")],
        conv=1, flow2=1))

    D.append(dict(
        id='hnl_bag1', who='荷物の案内係', bg='hnarr', sp='h_bagst',
        intro='荷物受取エリア。ベルトの番号を確かめて待つ。荷物がなかなか出てこないので、係に聞く。係員はのんびりしているが、探すときはていねい。',
        pairs=[
            T("Aloha! Are you looking for your belt?",
              "アロハ！ベルトをお探しですか。",
              "Aloha. Yes. How can we check our belt?", "アロハ。はい。ベルトはどう調べればいいですか。"),
            T("Look at the screen. It shows your flight and the belt. Then wait there. Your bags come soon.",
              "画面を見てください。便とベルトが出ています。そこで待ってください。荷物はもうすぐ出てきます。",
              "Thank you. We will wait here.", "ありがとう。ここで待ちます。"),
            OT("Oh, you are still here. The belt is empty now. Is everything okay?",
               "おや、まだいらっしゃいますね。ベルトはもう空です。大丈夫ですか。",
               [O('none', "Our bags are not coming out.", "荷物が出てきません。", "出てこない", "🧳",
                  ("I see. Please do not worry. We will look for them together.", "わかりました。心配しないで。いっしょに探しましょう。")),
                O('one', "One of our bags is not here.", "荷物がひとつ見つかりません。", "ひとつ無い", "☝️",
                  ("One bag is missing. I understand. Let us check it now.", "荷物がひとつ無いのですね。わかりました。いま確認しましょう。"))],
               cards=1, fork={'tw': ['empty']}),
            T("Please go to the baggage service office of your airline. It is near the belts. Show your bag tag there.",
              "航空会社の荷物サービスの窓口へ行ってください。ベルトの近くです。そこで荷物のタグを見せてください。",
              "I have my bag tag here. Is it okay?", "荷物のタグはここにあります。これでいいですか。"),
            T("Yes, that is perfect. With the tag, they can search for your bags. Do not worry. Take your time.",
              "はい、完ぺきです。タグがあれば、荷物を探せます。心配しないで。ゆっくりで大丈夫です。",
              "Thank you so much for your help.", "助けてくれて本当にありがとう。"),
        ],
        words=[("belt", "ベルト"), ("screen", "画面"), ("empty", "空の"), ("tag", "タグ"), ("worry", "心配する")],
        conv=1, flow2=1))

    D.append(dict(
        id='hnl_lei1', who='レイスタンドの店員', bg='hnarr', sp='h_lei',
        intro='到着ロビーのレイスタンド。赤白のひさしの下に、花のレイが並んでいる。生花のよい香りがする。',
        pairs=[
            T("Aloha! Welcome to Hawaii. Fresh flower leis, right here.",
              "アロハ！ハワイへようこそ。生花のレイは、こちらです。",
              "Aloha. Which lei is the most popular, please?", "アロハ。いちばん人気のレイはどれですか。"),
            T("Many visitors take the orchid lei. The plumeria lei smells very sweet. Both are fresh flowers.",
              "たくさんの旅行者が、蘭のレイを選びます。プルメリアのレイは、とても甘い香りです。どちらも生花です。",
              "They are beautiful. How do we wear a lei?", "きれいですね。レイはどうやってかけますか。"),
            OT("Around your neck, so it hangs in front and in back. So, which one do you like?",
               "首にかけて、前と後ろに垂らします。それで、どちらがお好きですか。",
               [O('orchid', "One orchid lei, please.", "蘭のレイを1つください。", "蘭", "🌸",
                  ("An orchid lei. A very good choice. It looks lovely with a smile.", "蘭のレイですね。とてもいい選択です。笑顔によく似合います。")),
                O('plumeria', "One plumeria lei, please.", "プルメリアのレイを1つください。", "プルメリア", "🌺",
                  ("A plumeria lei. Lovely. You will smell it all day.", "プルメリアのレイですね。すてき。一日じゅう香りが楽しめます。"))],
               cards=1, fork={'tw': ['orchid']}),
            T("In Hawaii, a lei says welcome. Would you like to wear it now? I can put it on for you.",
              "ハワイでは、レイは「ようこそ」の気持ちです。いま着けますか。私がかけますよ。",
              "Yes, please. Thank you.", "はい、お願いします。ありがとう。"),
            T("There you are. It looks great on you. Enjoy the islands!",
              "はい、どうぞ。よくお似合いです。島を楽しんでくださいね！",
              "Mahalo! It smells wonderful.", "マハロ！すばらしい香りです。"),
        ],
        words=[("lei", "レイ(花の首飾り)"), ("fresh", "新鮮な"), ("orchid", "蘭"), ("neck", "首"), ("welcome", "ようこそ")],
        conv=1, flow2=1))

    D.append(dict(
        id='hnl_trolley1', who='乗り場の係員', bg='hnarr', sp='h_bus',
        intro='空港の外の乗り場。バス停はレイスタンドの近く。ワイキキへの行き方を聞く。係員は荷物を見て、親切に選び方を教えてくれる。',
        pairs=[
            T("Aloha! Where are you going today?",
              "アロハ！今日はどちらへ？",
              "Aloha. Can we go to Waikiki by bus?", "アロハ。ワイキキへはバスで行けますか。"),
            T("Yes. There is a city bus to Waikiki. The bus stop is outside, near the lei stands. But look at your bags.",
              "はい。ワイキキへの市バスがあります。バス停は外の、レイスタンドの近くです。でも、荷物を見てください。",
              "We have one big suitcase. Is that a problem?", "大きいスーツケースが1つあります。問題ですか。"),
            OT("On the bus, bags must fit under your seat or between your feet. A big suitcase is hard. What do you prefer?",
               "バスでは、荷物は座席の下か足もとに収まる大きさでなければなりません。大きいスーツケースは大変です。どちらがいいですか。",
               [O('bus', "We will take the bus with small bags.", "小さい荷物でバスに乗ります。", "バス", "🚌",
                  ("Okay. Keep your bags with you, and sit down. The bus goes to Waikiki.", "わかりました。荷物は手元に置いて、座ってください。バスはワイキキへ行きます。")),
                O('shuttle', "A shuttle van is better for us.", "シャトルバンのほうがいいです。", "シャトル", "🚐",
                  ("Good choice. The shuttle vans are outside. Ask there for your hotel.", "いい選択です。シャトルバンは外にいます。そこでホテルを伝えてください。"))],
               cards=1, fork={'tw': ['bus']}),
            T("The Waikiki Trolley is different. It is for sightseeing in Waikiki. It does not go to the airport.",
              "ワイキキ・トロリーは別のものです。ワイキキの観光用です。空港には行きません。",
              "I see. Is there a train, too?", "なるほど。電車もありますか。"),
            T("Yes! The train is called Skyline. It stops at the airport, but it does not reach Waikiki yet. Have a good ride!",
              "はい！電車はスカイラインといいます。空港には停まりますが、ワイキキにはまだ届きません。いい旅を！",
              "Thank you. That is very useful.", "ありがとう。とても役に立ちました。"),
        ],
        words=[("bus", "バス"), ("suitcase", "スーツケース"), ("shuttle", "シャトル"), ("trolley", "トロリー"), ("train", "電車")],
        conv=1, flow2=1))

    # =================== 街(タスク101) ===================
    D.append(dict(
        id='hnl_cafe1', who='シェイブアイスの店員', bg='hnstreet', sp='h_ice',
        intro='ワイキキ、カラカウア通りのシェイブアイスの店。ダイヤモンドヘッドと海が見える。店員は、のんびり笑顔で話す。',
        pairs=[
            T("Aloha! Welcome. Shave ice today?",
              "アロハ！いらっしゃい。今日はシェイブアイスですか。",
              "Aloha. Yes, please. Which flavor is the most popular?", "アロハ。はい。いちばん人気の味はどれですか。"),
            T("Rainbow! It has three colors of syrup in one cup. Kids and grown-ups love it.",
              "レインボーです！1つのカップに3色のシロップが入ります。子どもにも大人にも人気です。",
              "Is shave ice the same as a snow cone?", "シェイブアイスは、かき氷(スノーコーン)と同じですか。"),
            T("Not quite. Our ice is shaved fine, soft like snow, so the syrup soaks in. In a snow cone, the ice is crushed.",
              "ちょっとちがいます。うちの氷は細かく削って雪のように柔らかいので、シロップがしみこみます。スノーコーンは氷をくだいたものです。",
              "I understand. I will have the rainbow, please.", "わかりました。レインボーでお願いします。"),
            OT("Rainbow, coming up! Would you like a snow cap on top? It is sweet milk.",
               "レインボーですね！上にスノーキャップをのせますか。甘いミルクです。",
               [O('cap', "Yes, a snow cap, please.", "はい、スノーキャップをお願いします。", "のせる", "🥛",
                  ("A snow cap. Sweet and creamy. Very good.", "スノーキャップですね。甘くてなめらかです。とてもおいしいですよ。")),
                O('plain', "No, just the rainbow, please.", "いいえ、レインボーだけでお願いします。", "のせない", "🌈",
                  ("Simple and good. Just the rainbow.", "シンプルでいいですね。レインボーだけです。"))],
               cards=1, fork={'tw': ['snow cap']}),
            T("Here you go. Be careful, it melts fast in the sun. Enjoy!",
              "はい、どうぞ。日なたではすぐ溶けるので気をつけて。楽しんでね！",
              "Thank you. This looks great!", "ありがとう。おいしそうです！"),
        ],
        words=[("shave ice", "シェイブアイス"), ("rainbow", "レインボー"), ("syrup", "シロップ"), ("snow cone", "スノーコーン"), ("flavor", "味")],
        conv=1, flow2=1))

    D.append(dict(
        id='hnl_shop1', who='おみやげ屋の店員', bg='hnstreet', sp='h_shop',
        intro='ワイキキのおみやげ屋。棚には、マカダミアナッツと小さいウクレレが並んでいる。店員はゆっくり、いろいろ見せてくれる。',
        pairs=[
            T("Aloha! Welcome to our shop. Take your time and look around.",
              "アロハ！いらっしゃいませ。ゆっくり見て行ってください。",
              "Aloha. What do people buy here as a gift?", "アロハ。ここでは、おみやげに何を買う人が多いですか。"),
            T("Macadamia nuts are very popular. They are grown here in Hawaii. And many visitors take home a small ukulele.",
              "マカダミアナッツがとても人気です。ハワイで育てています。それから、小さいウクレレを持ち帰る人も多いですよ。",
              "A small ukulele! How much is it?", "小さいウクレレ！いくらですか。"),
            OT("The price is on the small tag. This one is a normal size. Would you like to see a smaller one?",
               "値段は小さなタグに書いてあります。これは普通の大きさです。もう少し小さいものも見ますか。",
               [O('smaller', "Do you have a smaller one, please?", "もう少し小さいのはありますか。", "小さいの", "🔍",
                  ("Yes. This one is smaller. It fits in your bag.", "はい。こちらがもっと小さいものです。かばんに入ります。")),
                O('normal', "I will look at the normal size first.", "まず普通の大きさのを見ます。", "普通の", "🎸",
                  ("Of course. Please hold it gently. Take your time.", "もちろん。そっと持ってくださいね。ゆっくりどうぞ。"))],
               cards=1, fork={'tw': ['smaller']}),
            T("And the macadamia nuts? We have plain ones and chocolate ones.",
              "マカダミアナッツはいかがですか。プレーンとチョコがあります。",
              "The plain ones, please. They are a gift.", "プレーンをお願いします。おみやげなんです。"),
            T("Good choice. I put them in a nice bag. Mahalo!",
              "いい選択です。すてきな袋に入れますね。マハロ！",
              "Mahalo to you, too!", "こちらこそ、マハロ！"),
        ],
        words=[("gift", "おみやげ・贈りもの"), ("macadamia", "マカダミア"), ("ukulele", "ウクレレ"), ("smaller", "もっと小さい"), ("tag", "タグ")],
        conv=1, flow2=1))

    D.append(dict(
        id='hnl_hotel1', who='ホテルのフロント', bg='hnhotel', sp='h_front',
        intro='ワイキキのホテル。部屋のラナイ(バルコニー)から、海とダイヤモンドヘッドが見える。フロントの人はゆったり、順番に案内してくれる。',
        pairs=[
            T("Aloha! Welcome. Do you have a reservation?",
              "アロハ！ようこそ。ご予約はありますか。",
              "Aloha. Yes. We would like to check in, please.", "アロハ。はい。チェックインをお願いします。"),
            T("Wonderful. May I see your passport? I also need a card for extras. No rush.",
              "すばらしい。パスポートを見せてもらえますか。追加の料金用に、カードもお預かりします。急ぎません。",
              "Here are my passport and my card.", "パスポートとカードです。"),
            T("Thank you. Here are your keys. Your room has a lanai with a view of the ocean and Diamond Head.",
              "ありがとうございます。鍵です。お部屋にはラナイがあって、海とダイヤモンドヘッドが見えます。",
              "Beautiful! What time is breakfast tomorrow?", "すてき！明日の朝食は何時ですか。"),
            OT("Breakfast starts early in the morning. The hours are on the card in your room. Where would you like to eat?",
               "朝食は朝早くからです。時間はお部屋のカードに書いてあります。どこで召し上がりますか。",
               [O('rest', "We will eat in the restaurant.", "レストランで食べます。", "レストラン", "🍳",
                  ("Good. The restaurant is next to the garden, past the lobby.", "わかりました。レストランは、ロビーを抜けた庭のとなりです。")),
                O('lanai', "Can we eat on our lanai?", "ラナイで食べられますか。", "ラナイで", "🌴",
                  ("Yes, we can bring breakfast to your room. Please tell me tonight.", "はい、お部屋にお持ちできます。今夜のうちにお知らせください。"))],
               cards=1, fork={'tw': ['breakfast']}),
            T("That is all. If you need anything, call the front desk. Have a lovely evening.",
              "以上です。ご用があれば、フロントにお電話ください。すてきな夜を。",
              "Thank you. Good night.", "ありがとう。おやすみなさい。"),
        ],
        words=[("reservation", "予約"), ("passport", "パスポート"), ("lanai", "ラナイ(バルコニー)"), ("breakfast", "朝食"), ("view", "景色")],
        conv=1, flow2=1))

    # =================== 出発(タスク101。シドニー行きの国際線。米国の出国審査なし。航空会社名・便名は出さない) ===================
    D.append(dict(
        id='hnl_dep_board1', who='案内係', bg='hnboard', sp='h_board',
        intro='ホノルル空港の出発ロビー。大きな青い案内板の前で、シドニー行きのゲートを探す。案内係は、聞かれたことをゆっくり教えてくれる。',
        pairs=[
            T("Aloha! Are you looking for your flight?",
              "アロハ！便をお探しですか。",
              "Aloha. Which gate is the flight to Sydney, please?", "アロハ。シドニー行きは何番ゲートですか。"),
            T("Good question. Look at the big board. Find Sydney in the list. The gate is on the same line.",
              "いい質問です。大きな案内板を見てください。リストの中からシドニーを探します。ゲートは同じ行にあります。",
              "I found Sydney. What else is on the board?", "シドニーを見つけました。ほかには何が出ていますか。"),
            OT("The time, the gate, and the status. If the gate changes, the board changes, too. Do you see it?",
               "時刻とゲートと、状況です。ゲートが変わると、案内板も変わります。見えますか。",
               [O('yes', "Yes, I can see Sydney. Thank you.", "はい、シドニーが見えます。ありがとう。", "見えた", "👀",
                  ("Good. Please look at the board again before you walk to the gate. It can change.", "よかった。ゲートへ歩く前に、もう一度案内板を見てください。変わることがあります。")),
                O('where', "Where is the gate, please? I cannot see it.", "ゲートはどこですか。見つかりません。", "どこ？", "🔎",
                  ("It is on the same line as Sydney, in the gate column. Take your time.", "シドニーと同じ行の、ゲートの欄にあります。ゆっくりどうぞ。"))],
               cards=1, fork={'tw': ['board']}),
            T("Do you have another question?",
              "ほかに質問はありますか。",
              "How do we get to the gates after security?", "保安検査のあと、ゲートへはどう行きますか。"),
            T("After security, follow the signs for your gate. Check the board again there. Have a nice flight!",
              "保安検査のあとは、ゲートの案内板について行ってください。そこでもう一度案内板を見てください。いい旅を！",
              "Mahalo for your help.", "助けてくれてマハロ。"),
        ],
        words=[("gate", "ゲート"), ("board", "案内板"), ("list", "リスト"), ("same", "同じ"), ("change", "変わる")],
        conv=1, flow2=1))

    D.append(dict(
        id='hnl_dep_ticket1', who='チェックインの係員', bg='hnticket', sp='h_ticket',
        intro='出発ロビーのチェックイン・カウンター。「Australia」の札のカウンターで、世界一周航空券を見せてチェックインする。',
        pairs=[
            T("Aloha! Passport and ticket, please. Where are you flying today?",
              "アロハ！パスポートと切符をお願いします。今日はどちらへ？",
              "Aloha. We are flying to Sydney. Here is our round the world ticket.", "アロハ。シドニーへ行きます。世界一周航空券です。"),
            T("Thank you. This is the Australia counter, so you are in the right place. Let me check your trip.",
              "ありがとうございます。ここはオーストラリア行きのカウンターなので、正しい場所です。旅程を確認しますね。",
              "Can we fly with this ticket?", "この切符で乗れますか。"),
            OT("Yes, your ticket is fine. Would you like a window seat or an aisle seat?",
               "はい、切符は大丈夫です。窓側の席と通路側の席、どちらがいいですか。",
               [O('window', "A window seat, please.", "窓側をお願いします。", "窓側", "🪟",
                  ("A window seat. You can see the ocean from the sky.", "窓側ですね。空から海が見えますよ。")),
                O('aisle', "An aisle seat, please.", "通路側をお願いします。", "通路側", "🚶",
                  ("An aisle seat. Easy to stand up and walk.", "通路側ですね。立ち上がるのが楽です。"))],
               cards=1, fork={'tw': ['window']}),
            T("Do you have bags to check?",
              "預ける荷物はありますか。",
              "Yes, we do. Will they go all the way to Sydney?", "はい、あります。荷物はシドニーまで行きますか。"),
            T("Yes. I tag them for Sydney. Keep the claim stickers. Here are your boarding passes. Have a good trip!",
              "はい。シドニー行きのタグをつけます。引き換えのシールは持っていてください。搭乗券です。いい旅を！",
              "Thank you very much. Aloha!", "どうもありがとうございます。アロハ！"),
        ],
        words=[("ticket", "切符"), ("counter", "カウンター"), ("window seat", "窓側の席"), ("aisle", "通路"), ("boarding pass", "搭乗券")],
        conv=1, flow2=1))

    D.append(dict(
        id='hnl_dep_gate1', who='保安検査の係員(TSA)', bg='hngate', sp='h_tsa',
        intro='保安検査場の入口。黄色い「SECURITY」の札のそば。係員は落ち着いて、一つずつ手順を教えてくれる。',
        pairs=[
            T("Aloha. Boarding pass and passport, please.",
              "アロハ。搭乗券とパスポートをお願いします。",
              "Here you are. Do I need to take off my shoes?", "どうぞ。靴は脱がないとだめですか。"),
            T("Most lanes let you keep your shoes on now. If I ask, please take them off. Please follow the officer's instructions.",
              "いまはほとんどのレーンで、靴を履いたままで大丈夫です。私が頼んだら、脱いでください。係員の指示に従ってください。",
              "Okay. Do I take my laptop out of my bag?", "わかりました。パソコンはかばんから出しますか。"),
            T("It depends on the lane. In this lane, yes. Take it out and put it in a bin by itself. Some new lanes let you keep it in your bag.",
              "レーンによります。このレーンでは、はい。出して、トレーに1つだけ入れてください。新しいレーンでは、かばんに入れたままでよいところもあります。",
              "I understand. Here is my laptop.", "わかりました。これがパソコンです。"),
            OT("Thank you. Now, what is in your pockets?",
               "ありがとうございます。では、ポケットには何が入っていますか。",
               [O('yes', "I have my phone and my keys.", "スマホと鍵が入っています。", "入っている", "🔑",
                  ("Please put them in the bin, too. Thank you.", "それもトレーに入れてください。ありがとう。")),
                O('no', "Nothing. My pockets are empty.", "何もありません。ポケットは空です。", "空っぽ", "🙌",
                  ("Good. That makes it easy.", "いいですね。これなら簡単です。"))],
               cards=1, fork={'tw': ['pockets']}),
            T("Walk through slowly, and wait for your things at the end. No worries. Have a nice flight!",
              "ゆっくり通って、最後で荷物を待ってください。大丈夫ですよ。いい旅を！",
              "Thank you. See you!", "ありがとう。それでは！"),
        ],
        words=[("shoes", "靴"), ("laptop", "ノートパソコン"), ("bin", "トレー"), ("pocket", "ポケット"), ("lane", "レーン")],
        conv=1, flow2=1))
