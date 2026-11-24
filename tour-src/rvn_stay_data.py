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
# 会話の型は 053 の「分かれ目」(065 と同じ): 相手の一言に今日の語が入り、プレイヤーは▶で英語の返事を2〜3個から選んで声に出す。
#   ok=1 の返事 = 聞き取れた人が選ぶ返事。ok なし = 聞き違えた人が選ぶ返事(相手が言い直してくれる)。どれを選んでも物語は進む(止めない・合否なし)。
#   画面に出るのは英語だけ。日本語訳は出さない。fork={'tw':[語]} = その分かれ目で、選ぶまでの時間を裏で測る語。
# 雰囲気: ロヴァニエミの人は口数が少なく直接的(021)。村と空港で雰囲気を変える: 村=ゆっくり・やさしい / サンタ=あたたかい笑い / 保安検査=短くていねい / ゲート=静かで最後の一言があたたかい。
from window_data import star, O, OT

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
                O('step', "Then we will step over it together.", E, ok=1,
                  rep=("Good. One step, and you are in the Arctic. Hold hands, if you like.", E)),
                O('stop', "Stop? Must we stop at the line?", E,
                  rep=("No, no. Not stop. Step. Lift your foot, and put it down on the other side.", E)),
                O('photo', "May I take a photo on the line?", E, ok=1,
                  rep=("Of course. Stand on the line, and ask a friend to take it.", E))],
               fork={'tw': ['step']}),
            ("How does it feel? Is it different from the airport?", E,
             star("It feels very open. The sky is big."), E),
            OT("The sky is big, and the village is quiet. Do you see the tall building with the tower?", E, [
                O('tower', "Yes. The tall building with the tower. What is it?", E, ok=1,
                  rep=("That is the Santa Claus Office. You can meet Santa Claus there, every day.", E)),
                O('tour', "A tour? Is it a bus tour?", E,
                  rep=("Not tour. Tower. A tall, narrow part on top of a building. Look up.", E)),
                O('look', "I see it. May we go and look?", E, ok=1,
                  rep=("Of course. It is by the square. You can go after the line.", E))],
               fork={'tw': ['tower']}),
            ("That is the way. Enjoy the Arctic, and keep your hands warm.", E,
             star("Thank you. We will."), E),
        ],
        words=[("Arctic", E), ("line", E), ("step", E), ("tower", E), ("village", E)],
        conv=1))

    D.append(dict(
        id='rvn_village2', who='村で働く人', bg='rvil', sp='r_vwoman',
        intro='広場のベンチのそば。ここで働く人が、ふたりに声をかける。',
        pairs=[
            ("Hello. You look a little lost. Can I help you?", E,
             star("Hello. Which building is the oldest one here?"), E),
            OT("That log house, Roosevelt Cottage. It was built in nineteen fifty. It is the oldest in the village.", E, [
                O('old', "Nineteen fifty? That is very old.", E, ok=1,
                  rep=("For a village, yes. Those logs have seen many winters.", E)),
                O('cold', "Cold? The cottage is cold?", E,
                  rep=("No, no. Old. Not new. Many, many years.", E)),
                O('picture', "May I take a picture of it?", E, ok=1,
                  rep=("Yes. In the evening light, it looks warm and old.", E))],
               fork={'tw': ['old']}),
            ("And the red house over there is the Mrs. Santa Claus Christmas Cottage. Do you like red?", E,
             star("Yes, I do. Red looks warm in the snow."), E),
            OT("It does. What do you want to do first?", E, [
                O('mail', "We want to mail a postcard.", E, ok=1,
                  rep=("Good. The post office is a log house, with a yellow post box by the door.", E)),
                O('nail', "A nail? Do I need a nail?", E,
                  rep=("No, no. Mail. A letter, or a postcard. You send it by post.", E)),
                O('santa', "First, we want to see Santa Claus.", E, ok=1,
                  rep=("Then go to the Santa Claus Office. You can meet him every day, and it is free.", E))],
               fork={'tw': ['mail']}),
            ("Enjoy the village. It is a good place to slow down.", E,
             star("Thank you. Goodbye!"), E),
        ],
        words=[("old", E), ("cottage", E), ("red", E), ("mail", E), ("afternoon", E)],
        conv=1))

    # ======================= 滞在: 郵便局(実画) =======================
    D.append(dict(
        id='rvn_post1', who='郵便局の係員', bg='rpost', sp='r_postclerk',
        intro='サンタクロース村の郵便局。丸太の壁と暖炉。窓口の人が、まっすぐこちらを見ている。',
        pairs=[
            ("Good afternoon. Do you want to send a card?", E,
             star("Good afternoon. Yes. We want to send a postcard."), E),
            OT("Good. This is Santa Claus' Main Post Office. It is the only official post office of Santa Claus. Who is the card for?", E, [
                O('postcard', "It is a postcard for my friend at home.", E, ok=1,
                  rep=("A friend at home. Good. Write a short message. A short one is nice.", E)),
                O('car', "A car? I want to send a car?", E,
                  rep=("No, no. A card. Postcard. Paper, with a picture on one side. You write on the other.", E)),
                O('family', "It is a card for my family.", E, ok=1,
                  rep=("A family card. Good. Please write a short, warm message.", E))],
               fork={'tw': ['postcard']}),
            ("Please write it at the table. A short message is enough.", E,
             star("Thank you. I will write it now."), E),
            OT("When you are ready, I can put a special postmark on it. It is an Arctic Circle postmark.", E, [
                O('postmark', "Yes, please. I want the special postmark.", E, ok=1,
                  rep=("Good. One press, and it is yours. Very Arctic.", E)),
                O('mask', "A mask? Do I wear a mask?", E,
                  rep=("No, no. Postmark. A mark on the card, from the post office. It shows the place.", E)),
                O('christmas', "Will my card arrive by Christmas?", E, ok=1,
                  rep=("You can leave it here, and it will be sent to arrive at Christmas. That is the idea.", E))],
               fork={'tw': ['postmark']}),
            ("Put the card in the box by the door, or leave it with me. Have a warm day.", E,
             star("Thank you. Goodbye!"), E),
        ],
        words=[("postcard", E), ("postmark", E), ("message", E), ("Christmas", E), ("yellow", E)],
        conv=1))

    D.append(dict(
        id='rvn_post2', who='手紙を書いている旅行者', bg='rpost', sp='r_poststand',
        intro='郵便局のテーブル。手紙を書いている旅行者が、ペンを探している。',
        pairs=[
            ("Excuse me. Do you have a pen? Mine does not work.", E,
             star("Yes, I do. Here is a pen."), E),
            OT("Thank you. I am writing a letter to Santa Claus. Is that silly?", E, [
                O('letter', "No, it is not silly. It is a lovely letter.", E, ok=1,
                  rep=("Thank you. I hope it arrives for Christmas.", E)),
                O('latter', "The latter? What is the latter?", E,
                  rep=("No, no. Letter. A paper message that you put in an envelope.", E)),
                O('like', "I like writing letters, too.", E, ok=1,
                  rep=("Then we are the same. Letters are slow, but they are warm.", E))],
               fork={'tw': ['letter']}),
            ("The fire is warm, and the room is quiet. It is a good place to write.", E,
             star("Yes. It feels like a cabin."), E),
            OT("Do you know what to write? I want to say thank you for a good year.", E, [
                O('thank', "You can say thank you. That is a good start.", E, ok=1,
                  rep=("Yes. Thank you first. Then wishes.", E)),
                O('think', "Think? What do I need to think about?", E,
                  rep=("Ha. Not think. Thank. Say thank you. Two words, and a warm heart.", E)),
                O('wish', "I will write a wish for next year.", E, ok=1,
                  rep=("A wish. Yes. Keep it small and kind. Those are the best ones.", E))],
               fork={'tw': ['thank']}),
            ("Thank you for the pen. Now I can finish. Have a safe trip.", E,
             star("You are welcome. Good luck with your letter."), E),
        ],
        words=[("pen", E), ("letter", E), ("fire", E), ("thank", E), ("wish", E)],
        conv=1))

    # ======================= 滞在: サンタ =======================
    D.append(dict(
        id='rvn_santa1', who='サンタクロース', bg='rsanta', sp='r_santa',
        intro='サンタクロース・オフィス。あたたかい笑い声がして、サンタが顔を上げる。',
        pairs=[
            ("Ho ho ho. Come in, come in. Welcome to my office.", E,
             star("Hello, Santa. Thank you for meeting us."), E),
            OT("I am here every day, and visitors come in for free. Where are you from?", E, [
                O('Japan', "We come from Japan. It is far from here.", E, ok=1,
                  rep=("Japan! That is a long way. You must be tired, and happy to be here.", E)),
                O('pan', "A pan? Do you cook here?", E,
                  rep=("Ho ho ho. No pan. Japan. The country far in the east.", E)),
                O('far', "We came from far away. It was a long trip.", E, ok=1,
                  rep=("Long trips make the best stories. Tell me one, one day.", E))],
               fork={'tw': ['Japan']}),
            ("And what are you doing on your trip? Are you going around the world?", E,
             star("Yes. We are going around the world."), E),
            OT("Around the world! Then you need good luck. What do you wish for your trip?", E, [
                O('health', "I wish for good health.", E, ok=1,
                  rep=("Good health. That is the best gift of all. I will remember it.", E)),
                O('help', "Help? I need help?", E,
                  rep=("No, no. Health. Being well, and strong, and happy.", E)),
                O('safe', "We wish for a safe trip.", E, ok=1,
                  rep=("A safe trip. Yes. I will ask the reindeer to watch the sky for you.", E))],
               fork={'tw': ['health']}),
            ("Thank you for coming. Take good care, and keep your hearts warm. Ho ho ho.", E,
             star("Thank you, Santa. Merry Christmas!"), E),
        ],
        words=[("office", E), ("free", E), ("Japan", E), ("health", E), ("safe", E)],
        conv=1))

    D.append(dict(
        id='rvn_santa2', who='サンタクロース', bg='rsanta', sp='r_santa',
        intro='サンタクロース・オフィスの奥。いすのそばで、サンタが静かに待っている。',
        pairs=[
            ("Ho ho ho. Back again? Please sit down. The chair is warm.", E,
             star("Thank you, Santa. We want to ask you something."), E),
            OT("Of course. Ask me anything. But it must be a kind question.", E, [
                O('reindeer', "Are your reindeer in the village?", E, ok=1,
                  rep=("They are close, and they love the snow. Go and say hello.", E)),
                O('rain', "Rain? Does it rain here?", E,
                  rep=("No, no. Reindeer. The animals with big antlers. They pull my sleigh.", E)),
                O('tired', "Do you ever get tired?", E, ok=1,
                  rep=("Sometimes. Then I sit by the fire, and I am better.", E))],
               fork={'tw': ['reindeer']}),
            ("Now, my question. What was your best moment on this trip?", E,
             star("The best moment is now. We are talking to you!"), E),
            OT("Ha ha. Thank you. Tonight the sky may show you something. Nobody can promise it, not even me.", E, [
                O('lights', "We hope to see the northern lights tonight.", E, ok=1,
                  rep=("Hope, and look up. The sky decides.", E)),
                O('rights', "Rights? Do I have rights?", E,
                  rep=("No, no. Lights. The green lights in the sky. The northern lights.", E)),
                O('promise', "Can you promise us the lights?", E, ok=1,
                  rep=("No promise. The sky decides. But waiting is part of the fun.", E))],
               fork={'tw': ['lights']}),
            ("Go well, my friends. And remember, kind words are the best gifts.", E,
             star("Thank you, Santa. Goodbye!"), E),
        ],
        words=[("reindeer", E), ("moment", E), ("promise", E), ("lights", E), ("kind", E)],
        conv=1))

    # ======================= 滞在: トナカイ(動物は静止。素材がないため) =======================
    D.append(dict(
        id='rvn_reindeer1', who='トナカイの世話をする人', bg='rrein', sp='r_herder',
        intro='雪の道のわき。トナカイの世話をする人が、手綱を持って待っている。',
        pairs=[
            ("Good afternoon. Would you like to meet the reindeer?", E,
             star("Good afternoon. Yes, please. We love animals."), E),
            OT("Come this way, slowly. The reindeer are calm, but they do not like loud voices.", E, [
                O('softly', "We will walk slowly and talk softly.", E, ok=1,
                  rep=("Good. Then they will come close. They are curious.", E)),
                O('sofa', "A sofa? Do the reindeer sit on a sofa?", E,
                  rep=("Ha. No sofa. Softly. Quietly, and gently, like a whisper.", E)),
                O('quiet', "I will keep my voice quiet.", E, ok=1,
                  rep=("Perfect. Quiet voices, and slow hands.", E))],
               fork={'tw': ['softly']}),
            ("This one is the oldest. She knows every path in the snow.", E,
             star("She has beautiful antlers."), E),
            OT("In winter she pulls a sleigh through the snow. Have you ever seen a real sleigh?", E, [
                O('sleigh', "No, never. We only know it from pictures.", E, ok=1,
                  rep=("Then today is a good day. A real sleigh is quiet, and slow.", E)),
                O('sly', "Sly? A sly reindeer?", E,
                  rep=("Ha. No, no. Sleigh. A seat on runners, for the snow. Santa has one.", E)),
                O('ride', "Can we ride in the sleigh?", E, ok=1,
                  rep=("Please ask about the sleigh ride. I only look after the reindeer.", E))],
               fork={'tw': ['sleigh']}),
            ("Thank you for being so quiet. The reindeer like you. Take a photo, and go slowly.", E,
             star("Thank you. Goodbye, reindeer!"), E),
        ],
        words=[("reindeer", E), ("softly", E), ("antlers", E), ("sleigh", E), ("snow", E)],
        conv=1))

    D.append(dict(
        id='rvn_reindeer2', who='親子連れの旅行者', bg='rrein', sp='r_family',
        intro='柵のそば。親子連れの旅行者が、トナカイをじっと見ている。',
        pairs=[
            ("Hello! Look, that reindeer is looking at us. My daughter loves it.", E,
             star("Hello! It has big, kind eyes."), E),
            OT("Yes! It is getting dark. Are you cold? My daughter says her nose is red.", E, [
                O('nose', "Mine is red, too. It is very cold.", E, ok=1,
                  rep=("Ha ha. Then we are the same. A warm hat helps.", E)),
                O('knows', "Knows? What does it know?", E,
                  rep=("No, no. Nose. The part of your face under your eyes.", E)),
                O('happy', "I am a little cold, but happy.", E, ok=1,
                  rep=("Me too. Cold, and happy. That is Lapland.", E))],
               fork={'tw': ['nose']}),
            ("We came to see the northern lights, but the reindeer came first.", E,
             star("That is a good start to the trip."), E),
            OT("Are you staying in the village tonight? We want to wait for the lights at our hotel.", E, [
                O('tonight', "Yes. We will go to the hotel tonight.", E, ok=1,
                  rep=("Then we may look up at the same sky. That is nice.", E)),
                O('tonic', "Tonic? We drink tonic tonight?", E,
                  rep=("No, no. Tonight. This evening, after today.", E)),
                O('wait', "We will wait for the lights, too.", E, ok=1,
                  rep=("Good. Wear everything you have, and wait.", E))],
               fork={'tw': ['tonight']}),
            ("Good luck with the sky. My daughter says goodbye to you, too.", E,
             star("Goodbye! Say hello to the reindeer for us."), E),
        ],
        words=[("kind", E), ("nose", E), ("cold", E), ("tonight", E), ("sky", E)],
        conv=1))

    # ======================= 夜: ホテルのオーロラ待ち(オーロラは出る約束にしない。strip は出さない) =======================
    D.append(dict(
        id='rvn_hotel1', who='ホテルのフロントの人', bg='rhotel', sp='r_hfront',
        intro='ホテルのロビー。窓の外は、星の見える夜。フロントの人が、静かにこちらを見ている。',
        pairs=[
            ("Good evening. Did you have a good day?", E,
             star("Good evening. Yes. We met Santa Claus!"), E),
            OT("A lucky day. Tonight is for the sky. Do you want to see the northern lights?", E, [
                O('clear', "Is the sky clear tonight?", E, ok=1,
                  rep=("Very clear now. But clouds can come from nowhere. That is Lapland.", E)),
                O('clean', "Clean? The sky is clean?", E,
                  rep=("Ha. No, no. Clear. Not cloudy. You can see far, and see the stars.", E)),
                O('place', "Where is the best place to look?", E, ok=1,
                  rep=("Outside, away from the lamps. And wear everything you have.", E))],
               fork={'tw': ['clear']}),
            ("Nobody can promise the lights. But the night is long. Please stay warm.", E,
             star("We have hats and gloves. We are ready."), E),
            OT("If you want to wait inside, there are chairs by the window. Waiting is part of the night.", E, [
                O('window', "We will wait by the window. It is warm there.", E, ok=1,
                  rep=("A good choice. Warm feet, and a big sky.", E)),
                O('winner', "A winner? Who is the winner?", E,
                  rep=("Ha ha. No, no. Window. The glass in the wall, where you can look out.", E)),
                O('outside', "Can I wait outside for a little while?", E, ok=1,
                  rep=("Yes. But not too long. Come in when your toes hurt.", E))],
               fork={'tw': ['window']}),
            ("Good night. And good luck with the sky.", E,
             star("Thank you. Good night!"), E),
        ],
        words=[("clear", E), ("window", E), ("sky", E), ("luck", E), ("night", E)],
        conv=1))

    D.append(dict(
        id='rvn_hotel2', who='夜のロビーの旅行者', bg='rhotel', sp='r_nguest',
        intro='ロビーの窓ぎわ。毛布を肩にかけた旅行者が、小さな声で話しかけてくる。',
        pairs=[
            ("Shh. Hello. Sorry. I am only watching the sky.", E,
             star("Hello. Is anything out there?"), E),
            OT("Not yet. I have waited for a long time, but the sky is only stars.", E, [
                O('stars', "Stars are beautiful, too.", E, ok=1,
                  rep=("Yes. That is true. In my city, I never see so many.", E)),
                O('stairs', "Stairs? Where are the stairs?", E,
                  rep=("No, no. Stars. The small lights in the sky, far away.", E)),
                O('patient', "We can be patient. We have time.", E, ok=1,
                  rep=("Patient. Yes. That is the secret. And a warm blanket.", E))],
               fork={'tw': ['stars']}),
            ("Some people see the lights on the first night. Some never see them. It is luck.", E,
             star("We know. We hope for a little luck."), E),
            OT("Would you like a blanket? There is a basket by the window.", E, [
                O('blanket', "Yes, please. A blanket is a good idea.", E, ok=1,
                  rep=("Take one. Cold fingers cannot hold a camera.", E)),
                O('blank', "A blank? Is the paper blank?", E,
                  rep=("No, no. A blanket. A soft, warm cover for your shoulders.", E)),
                O('gloves', "I will wait with my hat and gloves.", E, ok=1,
                  rep=("Good. Hat, gloves, and patience. That is all you need.", E))],
               fork={'tw': ['blanket']}),
            ("If you see a green light, call me. I will call you, too. Deal?", E,
             star("Deal! We will look up together."), E),
        ],
        words=[("stars", E), ("patient", E), ("blanket", E), ("deal", E), ("together", E)],
        conv=1))

    # ======================= 出発: チェックイン =======================
    D.append(dict(
        id='rvn_checkin1', who='チェックインの係員', bg='rchk', sp='r_ck1',
        intro='ロヴァニエミ空港の出発ホール。広くて新しいホールの、チェックインカウンター。',
        pairs=[
            ("Good afternoon. Welcome to the departure hall. It is new, so everything is easy to find.", E,
             star("Good afternoon. We would like to check in, please."), E),
            OT("Of course. Passports, please. Are you flying south today?", E, [
                O('south', "Yes. We are flying south today.", E, ok=1,
                  rep=("South. Good. It will be warmer there.", E)),
                O('mouth', "Mouth? We fly to a mouth?", E,
                  rep=("No, no. South. The opposite of north. Warm places are in the south.", E)),
                O('pass', "Here are our passports. Thank you.", E, ok=1,
                  rep=("Thank you. Please wait one moment while I look.", E))],
               fork={'tw': ['south']}),
            ("Do you have a bag to check in? Please put it on the belt.", E,
             star("Yes. One big blue suitcase."), E),
            OT("Thank you. Is there anything fragile in the bag? Anything made of glass?", E, [
                O('glass', "No glass. Only clothes and a hat.", E, ok=1,
                  rep=("Good. Clothes are the best travelers.", E)),
                O('grass', "Grass? We have no grass.", E,
                  rep=("Ha. No, no. Glass. A hard, clear material. A cup is made of glass.", E)),
                O('gift', "Only a small gift from the village.", E, ok=1,
                  rep=("A gift. Lovely. Keep it in your hand bag, to be safe.", E))],
               fork={'tw': ['glass']}),
            ("Here are your boarding passes. Please go to security. Have a good flight.", E,
             star("Thank you. Goodbye!"), E),
        ],
        words=[("south", E), ("passport", E), ("suitcase", E), ("glass", E), ("flight", E)],
        conv=1))

    D.append(dict(
        id='rvn_checkin2', who='となりのカウンターの係員', bg='rchk', sp='r_ck2',
        intro='となりのカウンター。落ち着いた声の係員が、ゆっくり話す。',
        pairs=[
            ("Hello. Next, please. Where are you traveling today?", E,
             star("Hello. We are traveling south, to our next city."), E),
            OT("I see. Do you want a window seat, or an aisle seat?", E, [
                O('aisle', "An aisle seat, please. I like to walk.", E, ok=1,
                  rep=("An aisle seat. Good. It is easy to stand up.", E)),
                O('ill', "Ill? Is the seat ill?", E,
                  rep=("Ha. No, no. Aisle. The walkway between the seats.", E)),
                O('window', "A window seat, please. I like to look outside.", E, ok=1,
                  rep=("A window seat. Good. You can look at the snow from above.", E))],
               fork={'tw': ['aisle']}),
            ("Is this your only bag? Do you have any hand luggage?", E,
             star("Yes. Only a small backpack."), E),
            OT("Please keep your passport and your boarding pass together. You need them at security.", E, [
                O('boarding', "Yes. I will keep them together.", E, ok=1,
                  rep=("Good. A boarding pass is easy to lose, and hard to replace.", E)),
                O('boring', "Boring? Is the pass boring?", E,
                  rep=("Ha. No, no. Boarding. The paper, or phone, that lets you get on the plane.", E)),
                O('phone', "Can I keep my boarding pass on my phone?", E, ok=1,
                  rep=("Yes, if you like. Keep the screen bright.", E))],
               fork={'tw': ['boarding']}),
            ("That is all. Safe travels, and come back to Lapland again.", E,
             star("Thank you. We will!"), E),
        ],
        words=[("aisle", E), ("window", E), ("backpack", E), ("boarding", E), ("travel", E)],
        conv=1))

    # ======================= 出発: 保安検査 =======================
    D.append(dict(
        id='rvn_sec1', who='保安検査の係員', bg='rsec', sp='r_sec1',
        intro='保安検査場。係員が、トレイを指さしている。',
        pairs=[
            ("Good afternoon. Please put your jacket and your bag in a tray.", E,
             star("Good afternoon. Should I take my jacket off?"), E),
            OT("Yes, your jacket, and anything in your pockets. Do you have a laptop or a tablet?", E, [
                O('laptop', "Yes. I have a laptop in my bag.", E, ok=1,
                  rep=("Please take it out, and put it in a tray by itself.", E)),
                O('lap', "A lap? Do I put it on my lap?", E,
                  rep=("Ha. No, no. Laptop. The small computer that you open and close.", E)),
                O('phone', "No. Only my phone.", E, ok=1,
                  rep=("Good. The phone goes in the tray, too.", E))],
               fork={'tw': ['laptop']}),
            ("Please walk through the gate, one at a time.", E,
             star("Thank you. I am going through now."), E),
            OT("Wait, please. Do you have any liquids in your bag, like water?", E, [
                O('bottle', "Yes. I have a small bottle of water.", E, ok=1,
                  rep=("Please put it in the tray, too. We need to look at it.", E)),
                O('battle', "A battle? There is no battle.", E,
                  rep=("Ha. No, no. Bottle. A container for water. Is there a bottle in your bag?", E)),
                O('none', "No liquids. I drank my water.", E, ok=1,
                  rep=("Good. That makes it easy.", E))],
               fork={'tw': ['bottle']}),
            ("All clear. Please take your things from the tray. Have a good flight.", E,
             star("Thank you. Goodbye!"), E),
        ],
        words=[("tray", E), ("jacket", E), ("laptop", E), ("bottle", E), ("gate", E)],
        conv=1))

    D.append(dict(
        id='rvn_sec2', who='保安検査の係員', bg='rsec', sp='r_sec2',
        intro='荷物がベルトを通っていく。係員が、画面をじっと見ている。',
        pairs=[
            ("Excuse me. Is this your bag? The screen shows something round.", E,
             star("Yes, it is my bag. What is it?"), E),
            OT("I think it is a snow globe. Is it a gift?", E, [
                O('globe', "Yes. It is a gift from the village.", E, ok=1,
                  rep=("Pretty. Please hold it in your hand when you go through.", E)),
                O('glove', "A glove? No, it is not a glove.", E,
                  rep=("Ha. No, no. Globe. A round ball, made of glass, with snow inside.", E)),
                O('family', "Yes. It is for my family at home.", E, ok=1,
                  rep=("A good gift. Wrap it well, so that it does not break.", E))],
               fork={'tw': ['globe']}),
            ("Thank you. Please put it in a tray, and put the tray on the belt.", E,
             star("Like this? Is this right?"), E),
            OT("Yes, that is right. Now, your belt. Is there metal in it?", E, [
                O('metal', "Yes. My belt has metal. I will take it off.", E, ok=1,
                  rep=("Thank you. Put it in the tray, with the jacket.", E)),
                O('medal', "A medal? I did not win a medal.", E,
                  rep=("Ha. No, no. Metal. Hard and shiny, like iron or steel.", E)),
                O('soft', "No metal. It is a soft belt.", E, ok=1,
                  rep=("Good. Then walk through, slowly.", E))],
               fork={'tw': ['metal']}),
            ("All good. Your snow globe is safe. Have a lovely trip.", E,
             star("Thank you. You are kind."), E),
        ],
        words=[("globe", E), ("tray", E), ("metal", E), ("belt", E), ("safe", E)],
        conv=1))

    # ======================= 出発: ギフトショップ Napapiirin Lahja =======================
    D.append(dict(
        id='rvn_shop1', who='ギフトショップの店員', bg='rshop', sp='r_shop1',
        intro='ギフトショップ Napapiirin Lahja。ラップランドの小さな贈りものが、棚にならんでいる。',
        pairs=[
            ("Welcome to Napapiirin Lahja. Are you looking for a gift?", E,
             star("Hello. Yes. We want a small gift for home."), E),
            OT("Then you are in the right place. We have a shop before security, and one here, after security.", E, [
                O('small', "Yes. Something small and light, please.", E, ok=1,
                  rep=("Light is good. A small gift is easy to carry.", E)),
                O('smell', "Smell? Is the gift something to smell?", E,
                  rep=("No, no. Small. Not big. Easy to hold in one hand.", E)),
                O('reindeer', "Something with a reindeer on it.", E, ok=1,
                  rep=("A reindeer. Good choice. Look on the shelf by the window.", E))],
               fork={'tw': ['small']}),
            ("Take your time. Look around.", E,
             star("Thank you. This one is nice. What is it?"), E),
            OT("It is a little wooden reindeer. Do you want to hold it?", E, [
                O('wooden', "Yes, it is cute. Is it made of wood?", E, ok=1,
                  rep=("Yes, it is wooden. Light, and warm in the hand.", E)),
                O('would', "Would not? It would not stand?", E,
                  rep=("No, no. Wooden. Made of wood, from a tree.", E)),
                O('hold', "May I hold it? It looks very small.", E, ok=1,
                  rep=("Please. It is light. Be careful, it is a little shy.", E))],
               fork={'tw': ['wooden']}),
            ("A good choice. Please bring it to the counter. I will put it in a bag.", E,
             star("Thank you. We will take it."), E),
        ],
        words=[("gift", E), ("small", E), ("wooden", E), ("counter", E), ("shop", E)],
        conv=1))

    D.append(dict(
        id='rvn_shop2', who='ギフトショップの店員', bg='rshop', sp='r_shop2',
        intro='ギフトショップのレジのそば。落ち着いた声の店員が、棚をなおしている。',
        pairs=[
            ("Hello. Do you need help, or are you only looking?", E,
             star("We are only looking. It is a lovely shop."), E),
            OT("Thank you. Look at the pretty cards on the stand. They show the northern lights.", E, [
                O('cards', "I like the cards. Which one is your favorite?", E, ok=1,
                  rep=("This one, with the green sky and the black trees. It feels like home.", E)),
                O('cars', "Cars? Are there cars on the cards?", E,
                  rep=("Ha. No, no. Cards. Small, flat paper, with a picture on one side.", E)),
                O('friend', "I will send a card to a friend.", E, ok=1,
                  rep=("A friend will be glad. A real card is rare today.", E))],
               fork={'tw': ['cards']}),
            ("Do you want a bag for your things?", E,
             star("Yes, please. A small bag is fine."), E),
            OT("Here you are. You are lucky. It is the last one of this kind.", E, [
                O('last', "Really? The last one? Thank you!", E, ok=1,
                  rep=("Really. It was waiting for you.", E)),
                O('lost', "Lost? Did you lose the others?", E,
                  rep=("Ha. No, no. Last. Not first. There are no more behind it.", E)),
                O('safe', "I will keep it safe on the plane.", E, ok=1,
                  rep=("Good. Keep it flat, and it will stay pretty.", E))],
               fork={'tw': ['last']}),
            ("Safe travels. Come back to Lapland in the summer, too.", E,
             star("Thank you. We would love to."), E),
        ],
        words=[("cards", E), ("lovely", E), ("last", E), ("bag", E), ("summer", E)],
        conv=1))

    # ======================= 出発: Ahkio Kitchen and Bar(保安検査の後。サーモンスープとトナカイバーガー) =======================
    D.append(dict(
        id='rvn_ahkio1', who='レストランの店員', bg='rahk', sp='r_waiter1',
        intro='保安検査の先のレストラン、Ahkio Kitchen and Bar。クリーミーなサーモンスープの、いい香りがする。',
        pairs=[
            ("Welcome to Ahkio Kitchen and Bar. A table for two?", E,
             star("Yes, please. A table for two."), E),
            OT("Please sit anywhere. Our famous dish is the creamy salmon soup. Would you like to try it?", E, [
                O('soup', "Yes, please. We will have the salmon soup.", E, ok=1,
                  rep=("Good choice. It is creamy and warm, perfect for a cold day.", E)),
                O('soap', "Soap? We do not eat soap!", E,
                  rep=("Ha ha. No, no. Soup. Hot, in a bowl, with a spoon.", E)),
                O('what', "What is in the soup?", E, ok=1,
                  rep=("Salmon, and a creamy soup. Simple, and very good.", E))],
               fork={'tw': ['soup']}),
            ("And to drink? Water, or something warm?", E,
             star("Water, please. Thank you."), E),
            OT("The soup will come soon. Would you like bread with it?", E, [
                O('bread', "Yes. Bread with the soup, please.", E, ok=1,
                  rep=("Good. It is the best way. Bread, and soup.", E)),
                O('bed', "Bed? Do we sleep here?", E,
                  rep=("Ha. No, no. Bread. Soft food, made from flour. You eat it with soup.", E)),
                O('only', "No, thank you. Only the soup.", E, ok=1,
                  rep=("Understood. Only the soup. A good, simple lunch.", E))],
               fork={'tw': ['bread']}),
            ("Enjoy your meal. Take your time, but watch the clock.", E,
             star("Thank you. It smells wonderful."), E),
        ],
        words=[("table", E), ("soup", E), ("salmon", E), ("bread", E), ("creamy", E)],
        conv=1))

    D.append(dict(
        id='rvn_ahkio2', who='となりの席の旅行者', bg='rahk', sp='r_diner',
        intro='となりの席の旅行者が、ハンバーガーを食べながら、こちらを見ている。',
        pairs=[
            ("Excuse me. Are you going to order? Try the reindeer burger. It is the local favorite.", E,
             star("A reindeer burger? That is a surprise!"), E),
            OT("I was surprised, too, but it is really good. Do you eat meat?", E, [
                O('meat', "Yes, I eat meat. I will try it.", E, ok=1,
                  rep=("Good. Hold it with both hands. It is big.", E)),
                O('meet', "Meet? I meet the burger?", E,
                  rep=("Ha ha. No, no. Meat. The food from an animal. Meat, not meet.", E)),
                O('strong', "I am not sure. Is it strong?", E, ok=1,
                  rep=("It has a strong taste, but a kind one. Try a small bite.", E))],
               fork={'tw': ['meat']}),
            ("Please call the waiter. He is very kind.", E,
             star("Thank you for the tip."), E),
            OT("Are you flying today? I am staying one more night. I still want to see the northern lights.", E, [
                O('fly', "We are flying today. Lapland was wonderful.", E, ok=1,
                  rep=("Then you saw a lot. I hope the lights come to you, wherever you go.", E)),
                O('fry', "Fry? We fry something today?", E,
                  rep=("Ha. No, no. Fly. Go by plane, through the sky.", E)),
                O('santa', "We saw so much. We saw Santa Claus!", E, ok=1,
                  rep=("You did! Then your trip is already a success.", E))],
               fork={'tw': ['fly']}),
            ("Enjoy the burger. And have a safe flight.", E,
             star("Thank you. Enjoy your stay in Lapland!"), E),
        ],
        words=[("reindeer", E), ("burger", E), ("meat", E), ("fly", E), ("waiter", E)],
        conv=1))

    # ======================= 出発: ゲート =======================
    D.append(dict(
        id='rvn_gate1', who='ゲートの係員', bg='rgate', sp='r_gate1',
        intro='出発ゲート。大きな窓の向こうは、雪と夜のはじまりの空。係員がゆっくり話しかけてくる。',
        pairs=[
            ("Good afternoon. This is your gate. Boarding will start soon.", E,
             star("Good afternoon. Thank you. Is the flight on time?"), E),
            OT("Yes, so far. Please sit near the gate. We will call you when it is time.", E, [
                O('board', "Thank you. We will be ready to board.", E, ok=1,
                  rep=("Good. Have your boarding pass ready.", E)),
                O('bored', "Bored? I am not bored.", E,
                  rep=("Ha. No, no. Board. To get on the plane.", E)),
                O('sit', "We will sit by the window and wait.", E, ok=1,
                  rep=("Good. You can see the snow outside.", E))],
               fork={'tw': ['board']}),
            ("Is this your first time in Finland?", E,
             star("Yes. It is our first time, and we loved it."), E),
            OT("I am glad. What was your best memory of Lapland?", E, [
                O('village', "I loved the village, and the quiet.", E, ok=1,
                  rep=("Quiet is something we have a lot of. Take it with you.", E)),
                O('vintage', "Vintage? A vintage car?", E,
                  rep=("No, no. Village. A small town, with houses and a square.", E)),
                O('wait', "I loved waiting for the sky.", E, ok=1,
                  rep=("That is Lapland. Waiting, and hoping.", E))],
               fork={'tw': ['village']}),
            ("Please come back soon. Good luck with your trip.", E,
             star("Thank you. We will."), E),
        ],
        words=[("gate", E), ("board", E), ("village", E), ("quiet", E), ("memory", E)],
        conv=1))

    D.append(dict(
        id='rvn_gate2', who='ゲートの係員', bg='rgate', sp='r_gate2',
        intro='アナウンスが鳴った。ゲートの係員が、搭乗券を受け取っている。',
        pairs=[
            ("Good afternoon. Boarding is open. Boarding pass, please.", E,
             star("Good afternoon. Here is my boarding pass."), E),
            OT("Thank you. And your passport, please. Just a quick look.", E, [
                O('passport', "Of course. Here is my passport.", E, ok=1,
                  rep=("Good. Quick and easy.", E)),
                O('port', "A pass port? Is it a port?", E,
                  rep=("Ha. No, no. Passport. The little book with your photo.", E)),
                O('seat', "Is my seat by the window?", E, ok=1,
                  rep=("Yes. Look outside when we take off. The north is white, and beautiful.", E))],
               fork={'tw': ['passport']}),
            ("You are all set. Please walk through the door, and follow the people to the plane.", E,
             star("Thank you. We will."), E),
            OT("One more thing. Did you see the northern lights?", E, [
                O('green', "We saw something green. We are so lucky!", E, ok=1,
                  rep=("Then you are very lucky. Not everyone sees them.", E)),
                O('grin', "A grin? Is it a smile?", E,
                  rep=("Ha. No, no. Green. The color of leaves, and of the lights.", E)),
                O('happy', "No. But we are happy anyway.", E, ok=1,
                  rep=("That is a good answer. Come back, and look again.", E))],
               fork={'tw': ['green']}),
            ("Safe flight! And remember, the north will wait for you.", E,
             star("Thank you. Goodbye, Lapland!"), E),
        ],
        words=[("passport", E), ("boarding", E), ("green", E), ("lucky", E), ("north", E)],
        conv=1))
