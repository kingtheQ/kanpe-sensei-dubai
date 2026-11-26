# -*- coding: utf-8 -*-
# 世界一周編 ロヴァニエミの第2弾(タスク072。クロが執筆)。滞在(サンタクロース村)・夜(ホテル)・出発(空港の出発側)。
#   滞在 rvn_stay : 村の広場(rvn_village1/2)・郵便局(rvn_post1/2)・サンタ(rvn_santa1/2)・トナカイ(rvn_reindeer1/2)
#   夜   rvn_night: ホテルのオーロラ待ち(rvn_hotel1/2)
#   出発 rvn_dep  : チェックイン(rvn_checkin1/2)・保安検査(rvn_sec1/2)・ギフトショップ(rvn_shop1/2)・Ahkio(rvn_ahkio1/2)・ゲート(rvn_gate1/2)
#
# 使ってよい実在情報(指示書 072 の範囲・確認済みのものだけ):
#   - Santa Claus Office: サンタ本人に毎日会える・入場無料・広場のそばの塔のある建物
#   - Santa Claus' Main Post Office: サンタ唯一の公式郵便局・北極圏の特別な消印が押せる(図柄は語らない)・クリスマスに届くよう手紙を預けられる・入口そばの黄色いポスト
#   - 村の広場の北極圏ライン(またいで渡れる)・Roosevelt Cottage(1950年築・村で一番古い)・Mrs. Santa Claus Christmas Cottage(赤いコテージ)
#   - Santa Claus Reindeer(トナカイそり)と Arctic Circle Husky Park(ハスキー)が実在する(今回の動物の場面はトナカイ)
#   - Napapiirin Lahja(ギフトショップ。保安検査の前と後にある)・Ahkio Kitchen and Bar(保安検査の後。サーモンスープとトナカイバーガー)・出発ホールは新しい広いホール(2025年に拡張)
# それ以外の看板の文言・店の名前・料金・消印の図柄・航空会社の表示・発着案内の文言・行き先の都市名は出さない(値段の話は入れない)。個人名なし。
# 行き先は「南へ」「次の街へ」と言い、都市名を出さない(oneworld編=マドリード行き・スター編=イスタンブール戻りの両方で同じ台詞が成り立つようにする)。
#
# 会話の型(タスク057 第4弾=095 で新しい流れ=061 の flow2 に統一): 選ぶのは1場面に1回だけ。
#   053 では分かれ目(英語の返事を2〜3個から選ぶ)が2か所あったが、「行為の選択」に近い方の1か所だけを日本語の短い単語カード(cards=1・2枚)に作り替え、
#   もう1か所は固定文のターン(本線=ok=1 の返事をカンペで読んで声に出す。相手の反応 rep はそのまま)に戻した。聞き違えの返事(ok なし)は、カードでは選べないので外した。
#   カード → 見本の英語が音声だけ → カンペ(文字) → 声に出す → 間違えたら自動おてほん(074の統一ルール) → 相手の反応(rep)。画面に出るのは英語だけ
#   (日本語 njp / jp / yjp / rep の2つ目は空のまま。選択カードの日本語単語だけは画面に出す)。点数・○×は出さない。現地カード(then)は自然に入る場面がないので作っていない。
#   fork={'tw':[語]} = カードを出してからタップするまでの時間を裏で測る語。もう1か所(固定文に戻した方)の語もカード側に寄せた(語ごとの記録は 061 の forkNote/noteWord)。
# 雰囲気: ロヴァニエミの人は口数が少なく直接的(021)。村と空港で雰囲気を変える: 村=ゆっくり・やさしい / サンタ=あたたかい笑い / 保安検査=短くていねい / ゲート=静かで最後の一言があたたかい。
from window_data import star, O, OT, T

E = ''   # 日本語訳は出さない


def add(D):
    # ======================= 滞在: 村の広場(実画) =======================
    D.append(dict(
        id='rvn_village1', who='村の案内の人', bg='rvil', sp='r_vguide',
        intro='サンタクロース村の広場。足もとに、細い光の線が通っている。',
        pairs=[
            ("Good afternoon. Welcome to Santa Claus Village.", E,
             star("Good afternoon. Is this line the Arctic Circle?"), E),
            OT("Yes. At the airport, the light draws the line. Here it runs across the square, and you can step over it.", E, [
                O("step", "Then we will step over it together.", E, card="線をまたぐ", ico="👣",
                  rep=("Good. One step, and you are in the Arctic. Hold hands, if you like.", E)),
                O("photo", "May I take a photo on the line?", E, card="写真を撮る", ico="📷",
                  rep=("Of course. Stand on the line, and ask a friend to take it.", E))],
               cards=1, fork={'tw': ['step', 'tower']}),
            ("How does it feel? Is it different from the airport?", E,
             star("It feels very open. The sky is big."), E),
            T("The sky is big, and the village is quiet. Do you see the tall building with the tower?", E,
              "Yes. The tall building with the tower. What is it?", E,
              rep=("That is the Santa Claus Office. You can meet Santa Claus there, every day.", E)),
            ("That is the way. Enjoy the Arctic, and keep your hands warm.", E,
             star("Thank you. We will."), E),
        ],
        words=[("Arctic", E), ("line", E), ("step", E), ("tower", E), ("village", E)],
        conv=1, flow2=1))

    D.append(dict(
        id='rvn_village2', who='村で働く人', bg='rvil', sp='r_vwoman',
        intro='広場のベンチのそば。ここで働く人が、ふたりに声をかける。',
        pairs=[
            ("Hello. You look a little lost. Can I help you?", E,
             star("Hello. Which building is the oldest one here?"), E),
            T("That log house, Roosevelt Cottage. It was built in nineteen fifty. It is the oldest in the village.", E,
              "Nineteen fifty? That is very old.", E,
              rep=("For a village, yes. Those logs have seen many winters.", E)),
            ("And the red house over there is the Mrs. Santa Claus Christmas Cottage. Do you like red?", E,
             star("Yes, I do. Red looks warm in the snow."), E),
            OT("It does. What do you want to do first?", E, [
                O("mail", "We want to mail a postcard.", E, card="はがきを出す", ico="✉️",
                  rep=("Good. The post office is a log house, with a yellow post box by the door.", E)),
                O("santa", "First, we want to see Santa Claus.", E, card="サンタに会う", ico="🎅",
                  rep=("Then go to the Santa Claus Office. You can meet him every day, and it is free.", E))],
               cards=1, fork={'tw': ['mail', 'old']}),
            ("Enjoy the village. It is a good place to slow down.", E,
             star("Thank you. Goodbye!"), E),
        ],
        words=[("old", E), ("cottage", E), ("red", E), ("mail", E), ("afternoon", E)],
        conv=1, flow2=1))

    # ======================= 滞在: 郵便局(実画) =======================
    D.append(dict(
        id='rvn_post1', who='郵便局の係員', bg='rpost', sp='r_postclerk',
        intro='サンタクロース村の郵便局。丸太の壁と暖炉。窓口の人が、まっすぐこちらを見ている。',
        pairs=[
            ("Good afternoon. Do you want to send a card?", E,
             star("Good afternoon. Yes. We want to send a postcard."), E),
            T("Good. This is Santa Claus' Main Post Office. It is the only official post office of Santa Claus. Who is the card for?", E,
              "It is a postcard for my friend at home.", E,
              rep=("A friend at home. Good. Write a short message. A short one is nice.", E)),
            ("Please write it at the table. A short message is enough.", E,
             star("Thank you. I will write it now."), E),
            OT("When you are ready, I can put a special postmark on it. It is an Arctic Circle postmark.", E, [
                O("postmark", "Yes, please. I want the special postmark.", E, card="スタンプ", ico="🔖",
                  rep=("Good. One press, and it is yours. Very Arctic.", E)),
                O("christmas", "Will my card arrive by Christmas?", E, card="クリスマス", ico="🎄",
                  rep=("You can leave it here, and it will be sent to arrive at Christmas. That is the idea.", E))],
               cards=1, fork={'tw': ['postmark', 'postcard']}),
            ("Put the card in the box by the door, or leave it with me. Have a warm day.", E,
             star("Thank you. Goodbye!"), E),
        ],
        words=[("postcard", E), ("postmark", E), ("message", E), ("Christmas", E), ("yellow", E)],
        conv=1, flow2=1))

    D.append(dict(
        id='rvn_post2', who='手紙を書いている旅行者', bg='rpost', sp='r_poststand',
        intro='郵便局のテーブル。手紙を書いている旅行者が、ペンを探している。',
        pairs=[
            ("Excuse me. Do you have a pen? Mine does not work.", E,
             star("Yes, I do. Here is a pen."), E),
            T("Thank you. I am writing a letter to Santa Claus. Is that silly?", E,
              "No, it is not silly. It is a lovely letter.", E,
              rep=("Thank you. I hope it arrives for Christmas.", E)),
            ("The fire is warm, and the room is quiet. It is a good place to write.", E,
             star("Yes. It feels like a cabin."), E),
            OT("Do you know what to write? I want to say thank you for a good year.", E, [
                O("thank", "You can say thank you. That is a good start.", E, card="ありがとう", ico="🙏",
                  rep=("Yes. Thank you first. Then wishes.", E)),
                O("wish", "I will write a wish for next year.", E, card="ねがいごと", ico="🌠",
                  rep=("A wish. Yes. Keep it small and kind. Those are the best ones.", E))],
               cards=1, fork={'tw': ['thank', 'letter']}),
            ("Thank you for the pen. Now I can finish. Have a safe trip.", E,
             star("You are welcome. Good luck with your letter."), E),
        ],
        words=[("pen", E), ("letter", E), ("fire", E), ("thank", E), ("wish", E)],
        conv=1, flow2=1))

    # ======================= 滞在: サンタ =======================
    D.append(dict(
        id='rvn_santa1', who='サンタクロース', bg='rsanta', sp='r_santa',
        intro='サンタクロース・オフィス。あたたかい笑い声がして、サンタが顔を上げる。',
        pairs=[
            ("Ho ho ho. Come in, come in. Welcome to my office.", E,
             star("Hello, Santa. Thank you for meeting us."), E),
            T("I am here every day, and visitors come in for free. Where are you from?", E,
              "We come from Japan. It is far from here.", E,
              rep=("Japan! That is a long way. You must be tired, and happy to be here.", E)),
            ("And what are you doing on your trip? Are you going around the world?", E,
             star("Yes. We are going around the world."), E),
            OT("Around the world! Then you need good luck. What do you wish for your trip?", E, [
                O("health", "I wish for good health.", E, card="健康", ico="💪",
                  rep=("Good health. That is the best gift of all. I will remember it.", E)),
                O("safe", "We wish for a safe trip.", E, card="安全な旅", ico="🧳",
                  rep=("A safe trip. Yes. I will ask the reindeer to watch the sky for you.", E))],
               cards=1, fork={'tw': ['health', 'Japan']}),
            ("Thank you for coming. Take good care, and keep your hearts warm. Ho ho ho.", E,
             star("Thank you, Santa. Merry Christmas!"), E),
        ],
        words=[("office", E), ("free", E), ("Japan", E), ("health", E), ("safe", E)],
        conv=1, flow2=1))

    D.append(dict(
        id='rvn_santa2', who='サンタクロース', bg='rsanta', sp='r_santa',
        intro='サンタクロース・オフィスの奥。いすのそばで、サンタが静かに待っている。',
        pairs=[
            ("Ho ho ho. Back again? Please sit down. The chair is warm.", E,
             star("Thank you, Santa. We want to ask you something."), E),
            T("Of course. Ask me anything. But it must be a kind question.", E,
              "Are your reindeer in the village?", E,
              rep=("They are close, and they love the snow. Go and say hello.", E)),
            ("Now, my question. What was your best moment on this trip?", E,
             star("The best moment is now. We are talking to you!"), E),
            OT("Ha ha. Thank you. Tonight the sky may show you something. Nobody can promise it, not even me.", E, [
                O("lights", "We hope to see the northern lights tonight.", E, card="オーロラ", ico="🌌",
                  rep=("Hope, and look up. The sky decides.", E)),
                O("promise", "Can you promise us the lights?", E, card="約束して", ico="🤝",
                  rep=("No promise. The sky decides. But waiting is part of the fun.", E))],
               cards=1, fork={'tw': ['lights', 'reindeer']}),
            ("Go well, my friends. And remember, kind words are the best gifts.", E,
             star("Thank you, Santa. Goodbye!"), E),
        ],
        words=[("reindeer", E), ("moment", E), ("promise", E), ("lights", E), ("kind", E)],
        conv=1, flow2=1))

    # ======================= 滞在: トナカイ(動物は静止。素材がないため) =======================
    D.append(dict(
        id='rvn_reindeer1', who='トナカイの世話をする人', bg='rrein', sp='r_herder',
        intro='雪の道のわき。トナカイの世話をする人が、手綱を持って待っている。',
        pairs=[
            ("Good afternoon. Would you like to meet the reindeer?", E,
             star("Good afternoon. Yes, please. We love animals."), E),
            T("Come this way, slowly. The reindeer are calm, but they do not like loud voices.", E,
              "We will walk slowly and talk softly.", E,
              rep=("Good. Then they will come close. They are curious.", E)),
            ("This one is the oldest. She knows every path in the snow.", E,
             star("She has beautiful antlers."), E),
            OT("In winter she pulls a sleigh through the snow. Have you ever seen a real sleigh?", E, [
                O("sleigh", "No, never. We only know it from pictures.", E, card="見たことない", ico="👀",
                  rep=("Then today is a good day. A real sleigh is quiet, and slow.", E)),
                O("ride", "Can we ride in the sleigh?", E, card="そりに乗る", ico="🛷",
                  rep=("Please ask about the sleigh ride. I only look after the reindeer.", E))],
               cards=1, fork={'tw': ['sleigh', 'softly']}),
            ("Thank you for being so quiet. The reindeer like you. Take a photo, and go slowly.", E,
             star("Thank you. Goodbye, reindeer!"), E),
        ],
        words=[("reindeer", E), ("softly", E), ("antlers", E), ("sleigh", E), ("snow", E)],
        conv=1, flow2=1))

    D.append(dict(
        id='rvn_reindeer2', who='親子連れの旅行者', bg='rrein', sp='r_family',
        intro='柵のそば。親子連れの旅行者が、トナカイをじっと見ている。',
        pairs=[
            ("Hello! Look, that reindeer is looking at us. My daughter loves it.", E,
             star("Hello! It has big, kind eyes."), E),
            T("Yes! It is getting dark. Are you cold? My daughter says her nose is red.", E,
              "Mine is red, too. It is very cold.", E,
              rep=("Ha ha. Then we are the same. A warm hat helps.", E)),
            ("We came to see the northern lights, but the reindeer came first.", E,
             star("That is a good start to the trip."), E),
            OT("Are you staying in the village tonight? We want to wait for the lights at our hotel.", E, [
                O("tonight", "Yes. We will go to the hotel tonight.", E, card="ホテルへ", ico="🏨",
                  rep=("Then we may look up at the same sky. That is nice.", E)),
                O("wait", "We will wait for the lights, too.", E, card="オーロラを待つ", ico="⏳",
                  rep=("Good. Wear everything you have, and wait.", E))],
               cards=1, fork={'tw': ['tonight', 'nose']}),
            ("Good luck with the sky. My daughter says goodbye to you, too.", E,
             star("Goodbye! Say hello to the reindeer for us."), E),
        ],
        words=[("kind", E), ("nose", E), ("cold", E), ("tonight", E), ("sky", E)],
        conv=1, flow2=1))

    # ======================= 夜: ホテルのオーロラ待ち(オーロラは出る約束にしない。strip は出さない) =======================
    D.append(dict(
        id='rvn_hotel1', who='ホテルのフロントの人', bg='rhotel', sp='r_hfront',
        intro='ホテルのロビー。窓の外は、星の見える夜。フロントの人が、静かにこちらを見ている。',
        pairs=[
            ("Good evening. Did you have a good day?", E,
             star("Good evening. Yes. We met Santa Claus!"), E),
            T("A lucky day. Tonight is for the sky. Do you want to see the northern lights?", E,
              "Is the sky clear tonight?", E,
              rep=("Very clear now. But clouds can come from nowhere. That is Lapland.", E)),
            ("Nobody can promise the lights. But the night is long. Please stay warm.", E,
             star("We have hats and gloves. We are ready."), E),
            OT("If you want to wait inside, there are chairs by the window. Waiting is part of the night.", E, [
                O("window", "We will wait by the window. It is warm there.", E, card="まどぎわで待つ", ico="🪟",
                  rep=("A good choice. Warm feet, and a big sky.", E)),
                O("outside", "Can I wait outside for a little while?", E, card="外で待つ", ico="🧤",
                  rep=("Yes. But not too long. Come in when your toes hurt.", E))],
               cards=1, fork={'tw': ['window', 'clear']}),
            ("Good night. And good luck with the sky.", E,
             star("Thank you. Good night!"), E),
        ],
        words=[("clear", E), ("window", E), ("sky", E), ("luck", E), ("night", E)],
        conv=1, flow2=1))

    D.append(dict(
        id='rvn_hotel2', who='夜のロビーの旅行者', bg='rhotel', sp='r_nguest',
        intro='ロビーの窓ぎわ。毛布を肩にかけた旅行者が、小さな声で話しかけてくる。',
        pairs=[
            ("Shh. Hello. Sorry. I am only watching the sky.", E,
             star("Hello. Is anything out there?"), E),
            T("Not yet. I have waited for a long time, but the sky is only stars.", E,
              "Stars are beautiful, too.", E,
              rep=("Yes. That is true. In my city, I never see so many.", E)),
            ("Some people see the lights on the first night. Some never see them. It is luck.", E,
             star("We know. We hope for a little luck."), E),
            OT("Would you like a blanket? There is a basket by the window.", E, [
                O("blanket", "Yes, please. A blanket is a good idea.", E, card="ブランケット", ico="🧣",
                  rep=("Take one. Cold fingers cannot hold a camera.", E)),
                O("gloves", "I will wait with my hat and gloves.", E, card="手ぶくろ", ico="🧤",
                  rep=("Good. Hat, gloves, and patience. That is all you need.", E))],
               cards=1, fork={'tw': ['blanket', 'stars']}),
            ("If you see a green light, call me. I will call you, too. Deal?", E,
             star("Deal! We will look up together."), E),
        ],
        words=[("stars", E), ("patient", E), ("blanket", E), ("deal", E), ("together", E)],
        conv=1, flow2=1))

    # ======================= 出発: チェックイン =======================
    D.append(dict(
        id='rvn_checkin1', who='チェックインの係員', bg='rchk', sp='r_ck1',
        intro='ロヴァニエミ空港の出発ホール。広くて新しいホールの、チェックインカウンター。',
        pairs=[
            ("Good afternoon. Welcome to the departure hall. It is new, so everything is easy to find.", E,
             star("Good afternoon. We would like to check in, please."), E),
            T("Of course. Passports, please. Are you flying south today?", E,
              "Yes. We are flying south today.", E,
              rep=("South. Good. It will be warmer there.", E)),
            ("Do you have a bag to check in? Please put it on the belt.", E,
             star("Yes. One big blue suitcase."), E),
            OT("Thank you. Is there anything fragile in the bag? Anything made of glass?", E, [
                O("glass", "No glass. Only clothes and a hat.", E, card="ガラスなし", ico="🚫",
                  rep=("Good. Clothes are the best travelers.", E)),
                O("gift", "Only a small gift from the village.", E, card="おみやげ", ico="🎁",
                  rep=("A gift. Lovely. Keep it in your hand bag, to be safe.", E))],
               cards=1, fork={'tw': ['glass', 'south']}),
            ("Here are your boarding passes. Please go to security. Have a good flight.", E,
             star("Thank you. Goodbye!"), E),
        ],
        words=[("south", E), ("passport", E), ("suitcase", E), ("glass", E), ("flight", E)],
        conv=1, flow2=1))

    D.append(dict(
        id='rvn_checkin2', who='となりのカウンターの係員', bg='rchk', sp='r_ck2',
        intro='となりのカウンター。落ち着いた声の係員が、ゆっくり話す。',
        pairs=[
            ("Hello. Next, please. Where are you traveling today?", E,
             star("Hello. We are traveling south, to our next city."), E),
            OT("I see. Do you want a window seat, or an aisle seat?", E, [
                O("aisle", "An aisle seat, please. I like to walk.", E, card="通路側", ico="🚶",
                  rep=("An aisle seat. Good. It is easy to stand up.", E)),
                O("window", "A window seat, please. I like to look outside.", E, card="まど側", ico="🪟",
                  rep=("A window seat. Good. You can look at the snow from above.", E))],
               cards=1, fork={'tw': ['aisle', 'boarding']}),
            ("Is this your only bag? Do you have any hand luggage?", E,
             star("Yes. Only a small backpack."), E),
            T("Please keep your passport and your boarding pass together. You need them at security.", E,
              "Yes. I will keep them together.", E,
              rep=("Good. A boarding pass is easy to lose, and hard to replace.", E)),
            ("That is all. Safe travels, and come back to Lapland again.", E,
             star("Thank you. We will!"), E),
        ],
        words=[("aisle", E), ("window", E), ("backpack", E), ("boarding", E), ("travel", E)],
        conv=1, flow2=1))

    # ======================= 出発: 保安検査 =======================
    D.append(dict(
        id='rvn_sec1', who='保安検査の係員', bg='rsec', sp='r_sec1',
        intro='保安検査場。係員が、トレイを指さしている。',
        pairs=[
            ("Good afternoon. Please put your jacket and your bag in a tray.", E,
             star("Good afternoon. Should I take my jacket off?"), E),
            T("Yes, your jacket, and anything in your pockets. Do you have a laptop or a tablet?", E,
              "Yes. I have a laptop in my bag.", E,
              rep=("Please take it out, and put it in a tray by itself.", E)),
            ("Please walk through the gate, one at a time.", E,
             star("Thank you. I am going through now."), E),
            OT("Wait, please. Do you have any liquids in your bag, like water?", E, [
                O("bottle", "Yes. I have a small bottle of water.", E, card="水のボトル", ico="💧",
                  rep=("Please put it in the tray, too. We need to look at it.", E)),
                O("none", "No liquids. I drank my water.", E, card="液体なし", ico="🚫",
                  rep=("Good. That makes it easy.", E))],
               cards=1, fork={'tw': ['bottle', 'laptop']}),
            ("All clear. Please take your things from the tray. Have a good flight.", E,
             star("Thank you. Goodbye!"), E),
        ],
        words=[("tray", E), ("jacket", E), ("laptop", E), ("bottle", E), ("gate", E)],
        conv=1, flow2=1))

    D.append(dict(
        id='rvn_sec2', who='保安検査の係員', bg='rsec', sp='r_sec2',
        intro='荷物がベルトを通っていく。係員が、画面をじっと見ている。',
        pairs=[
            ("Excuse me. Is this your bag? The screen shows something round.", E,
             star("Yes, it is my bag. What is it?"), E),
            T("I think it is a snow globe. Is it a gift?", E,
              "Yes. It is a gift from the village.", E,
              rep=("Pretty. Please hold it in your hand when you go through.", E)),
            ("Thank you. Please put it in a tray, and put the tray on the belt.", E,
             star("Like this? Is this right?"), E),
            OT("Yes, that is right. Now, your belt. Is there metal in it?", E, [
                O("metal", "Yes. My belt has metal. I will take it off.", E, card="ベルトを外す", ico="👖",
                  rep=("Thank you. Put it in the tray, with the jacket.", E)),
                O("soft", "No metal. It is a soft belt.", E, card="金属なし", ico="✅",
                  rep=("Good. Then walk through, slowly.", E))],
               cards=1, fork={'tw': ['metal', 'globe']}),
            ("All good. Your snow globe is safe. Have a lovely trip.", E,
             star("Thank you. You are kind."), E),
        ],
        words=[("globe", E), ("tray", E), ("metal", E), ("belt", E), ("safe", E)],
        conv=1, flow2=1))

    # ======================= 出発: ギフトショップ Napapiirin Lahja =======================
    D.append(dict(
        id='rvn_shop1', who='ギフトショップの店員', bg='rshop', sp='r_shop1',
        intro='ギフトショップ Napapiirin Lahja。ラップランドの小さな贈りものが、棚にならんでいる。',
        pairs=[
            ("Welcome to Napapiirin Lahja. Are you looking for a gift?", E,
             star("Hello. Yes. We want a small gift for home."), E),
            OT("Then you are in the right place. We have a shop before security, and one here, after security.", E, [
                O("small", "Yes. Something small and light, please.", E, card="小さいもの", ico="🎁",
                  rep=("Light is good. A small gift is easy to carry.", E)),
                O("reindeer", "Something with a reindeer on it.", E, card="トナカイ", ico="🦌",
                  rep=("A reindeer. Good choice. Look on the shelf by the window.", E))],
               cards=1, fork={'tw': ['small', 'wooden']}),
            ("Take your time. Look around.", E,
             star("Thank you. This one is nice. What is it?"), E),
            T("It is a little wooden reindeer. Do you want to hold it?", E,
              "Yes, it is cute. Is it made of wood?", E,
              rep=("Yes, it is wooden. Light, and warm in the hand.", E)),
            ("A good choice. Please bring it to the counter. I will put it in a bag.", E,
             star("Thank you. We will take it."), E),
        ],
        words=[("gift", E), ("small", E), ("wooden", E), ("counter", E), ("shop", E)],
        conv=1, flow2=1))

    D.append(dict(
        id='rvn_shop2', who='ギフトショップの店員', bg='rshop', sp='r_shop2',
        intro='ギフトショップのレジのそば。落ち着いた声の店員が、棚をなおしている。',
        pairs=[
            ("Hello. Do you need help, or are you only looking?", E,
             star("We are only looking. It is a lovely shop."), E),
            OT("Thank you. Look at the pretty cards on the stand. They show the northern lights.", E, [
                O("cards", "I like the cards. Which one is your favorite?", E, card="カードを見る", ico="🖼️",
                  rep=("This one, with the green sky and the black trees. It feels like home.", E)),
                O("friend", "I will send a card to a friend.", E, card="友だちに送る", ico="💌",
                  rep=("A friend will be glad. A real card is rare today.", E))],
               cards=1, fork={'tw': ['cards', 'last']}),
            ("Do you want a bag for your things?", E,
             star("Yes, please. A small bag is fine."), E),
            T("Here you are. You are lucky. It is the last one of this kind.", E,
              "Really? The last one? Thank you!", E,
              rep=("Really. It was waiting for you.", E)),
            ("Safe travels. Come back to Lapland in the summer, too.", E,
             star("Thank you. We would love to."), E),
        ],
        words=[("cards", E), ("lovely", E), ("last", E), ("bag", E), ("summer", E)],
        conv=1, flow2=1))

    # ======================= 出発: Ahkio Kitchen and Bar(保安検査の後。サーモンスープとトナカイバーガー) =======================
    D.append(dict(
        id='rvn_ahkio1', who='レストランの店員', bg='rahk', sp='r_waiter1',
        intro='保安検査の先のレストラン、Ahkio Kitchen and Bar。クリーミーなサーモンスープの、いい香りがする。',
        pairs=[
            ("Welcome to Ahkio Kitchen and Bar. A table for two?", E,
             star("Yes, please. A table for two."), E),
            OT("Please sit anywhere. Our famous dish is the creamy salmon soup. Would you like to try it?", E, [
                O("soup", "Yes, please. We will have the salmon soup.", E, card="サーモンスープ", ico="🍲",
                  rep=("Good choice. It is creamy and warm, perfect for a cold day.", E)),
                O("what", "What is in the soup?", E, card="スープの中身", ico="❓",
                  rep=("Salmon, and a creamy soup. Simple, and very good.", E))],
               cards=1, fork={'tw': ['soup', 'bread']}),
            ("And to drink? Water, or something warm?", E,
             star("Water, please. Thank you."), E),
            T("The soup will come soon. Would you like bread with it?", E,
              "Yes. Bread with the soup, please.", E,
              rep=("Good. It is the best way. Bread, and soup.", E)),
            ("Enjoy your meal. Take your time, but watch the clock.", E,
             star("Thank you. It smells wonderful."), E),
        ],
        words=[("table", E), ("soup", E), ("salmon", E), ("bread", E), ("creamy", E)],
        conv=1, flow2=1))

    D.append(dict(
        id='rvn_ahkio2', who='となりの席の旅行者', bg='rahk', sp='r_diner',
        intro='となりの席の旅行者が、ハンバーガーを食べながら、こちらを見ている。',
        pairs=[
            ("Excuse me. Are you going to order? Try the reindeer burger. It is the local favorite.", E,
             star("A reindeer burger? That is a surprise!"), E),
            OT("I was surprised, too, but it is really good. Do you eat meat?", E, [
                O("meat", "Yes, I eat meat. I will try it.", E, card="ためしてみる", ico="🍔",
                  rep=("Good. Hold it with both hands. It is big.", E)),
                O("strong", "I am not sure. Is it strong?", E, card="味は強い？", ico="🤔",
                  rep=("It has a strong taste, but a kind one. Try a small bite.", E))],
               cards=1, fork={'tw': ['meat', 'fly']}),
            ("Please call the waiter. He is very kind.", E,
             star("Thank you for the tip."), E),
            T("Are you flying today? I am staying one more night. I still want to see the northern lights.", E,
              "We are flying today. Lapland was wonderful.", E,
              rep=("Then you saw a lot. I hope the lights come to you, wherever you go.", E)),
            ("Enjoy the burger. And have a safe flight.", E,
             star("Thank you. Enjoy your stay in Lapland!"), E),
        ],
        words=[("reindeer", E), ("burger", E), ("meat", E), ("fly", E), ("waiter", E)],
        conv=1, flow2=1))

    # ======================= 出発: ゲート =======================
    D.append(dict(
        id='rvn_gate1', who='ゲートの係員', bg='rgate', sp='r_gate1',
        intro='出発ゲート。大きな窓の向こうは、雪と夜のはじまりの空。係員がゆっくり話しかけてくる。',
        pairs=[
            ("Good afternoon. This is your gate. Boarding will start soon.", E,
             star("Good afternoon. Thank you. Is the flight on time?"), E),
            OT("Yes, so far. Please sit near the gate. We will call you when it is time.", E, [
                O("board", "Thank you. We will be ready to board.", E, card="搭乗にそなえる", ico="✈️",
                  rep=("Good. Have your boarding pass ready.", E)),
                O("sit", "We will sit by the window and wait.", E, card="まどで待つ", ico="🪟",
                  rep=("Good. You can see the snow outside.", E))],
               cards=1, fork={'tw': ['board', 'village']}),
            ("Is this your first time in Finland?", E,
             star("Yes. It is our first time, and we loved it."), E),
            T("I am glad. What was your best memory of Lapland?", E,
              "I loved the village, and the quiet.", E,
              rep=("Quiet is something we have a lot of. Take it with you.", E)),
            ("Please come back soon. Good luck with your trip.", E,
             star("Thank you. We will."), E),
        ],
        words=[("gate", E), ("board", E), ("village", E), ("quiet", E), ("memory", E)],
        conv=1, flow2=1))

    D.append(dict(
        id='rvn_gate2', who='ゲートの係員', bg='rgate', sp='r_gate2',
        intro='アナウンスが鳴った。ゲートの係員が、搭乗券を受け取っている。',
        pairs=[
            ("Good afternoon. Boarding is open. Boarding pass, please.", E,
             star("Good afternoon. Here is my boarding pass."), E),
            OT("Thank you. And your passport, please. Just a quick look.", E, [
                O("passport", "Of course. Here is my passport.", E, card="パスポート", ico="🛂",
                  rep=("Good. Quick and easy.", E)),
                O("seat", "Is my seat by the window?", E, card="席はまど側？", ico="💺",
                  rep=("Yes. Look outside when we take off. The north is white, and beautiful.", E))],
               cards=1, fork={'tw': ['passport', 'green']}),
            ("You are all set. Please walk through the door, and follow the people to the plane.", E,
             star("Thank you. We will."), E),
            T("One more thing. Did you see the northern lights?", E,
              "We saw something green. We are so lucky!", E,
              rep=("Then you are very lucky. Not everyone sees them.", E)),
            ("Safe flight! And remember, the north will wait for you.", E,
             star("Thank you. Goodbye, Lapland!"), E),
        ],
        words=[("passport", E), ("boarding", E), ("green", E), ("lucky", E), ("north", E)],
        conv=1, flow2=1))
