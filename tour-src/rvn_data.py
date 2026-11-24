# -*- coding: utf-8 -*-
# 世界一周編 ロヴァニエミの到着まわり(タスク065。クロが執筆)。国ごとのデータは別ファイル(ドーハ・羽田・ナイロビの滞在と同じ形)。
# 5場所×2場面: 入国審査(rvn_immig1/2)・手荷物受取(rvn_bag1/2)・到着ロビー(rvn_lobby1/2)・無料Wi-Fi(rvn_wifi1/2)・バス乗り場(rvn_bus1/2)。
#
# 使ってよい実在情報(指示書の範囲・確認済みのものだけ。出典は docs/sources.md の「065」):
#   - 無料Wi-Fi名 "Rovaniemi Airport Free Wi-Fi"(Finavia 公式)
#   - サンタクロース村へはバス8番／Airport Express、約2〜3km(Santa Claus Office 公式)
#   - 到着ロビーの北極圏ライン(天窓の光が床に描く線・年のプレート。Finavia ニュースルーム)
#   - "Welcome to Rovaniemi Airport"(Finavia 公式の見出し)
# それ以外の看板の文言・店の名前・料金・時刻・所要時間は未確認なので、台詞にも画面にも出さない(値段の話は入れない)。個人名なし。
#
# 会話の型は 053 の「分かれ目」(058・059 と同じ): 相手の一言に今日の語が入り、プレイヤーは▶で英語の返事を2〜3個から選んで声に出す。
#   ok=1 の返事 = 聞き取れた人が選ぶ返事。ok なし = 聞き違えた人が選ぶ返事(相手が言い直してくれる)。どれを選んでも物語は進む(止めない・合否なし)。
#   画面に出るのは英語だけ。日本語訳は出さない(njp / jp / yjp / rep の2つ目 / 語の2つ目は空)。
#   fork={'tw':[語]} = その分かれ目で、選ぶまでの時間を裏で測る語(053 のしくみのまま)。
#
# 雰囲気(021 の差の付け方): 口数が少なく直接的。沈黙を気にしない。ただし最後の一言は温かい。「How are you?」は文字どおりの質問と受け取る。
# 入国審査について: ヘルシンキ経由(oneworld)は、実際にはシェンゲン圏内の国内線の到着で、ここでの入国審査はない(021 の「大事な違い」)。
#   ゲームでは両方の旅をそろえるため、短い「到着の確認」の形にし、国名の言いかえや便名は出さない。PM確認の点として報告に書く。
import window_data as W
from window_data import star, O, OT

E = ''   # 日本語訳は出さない


def add(D):
    # ---------- 入国審査 ----------
    D.append(dict(
        id='rvn_immig1', who='入国審査の係官', bg='rimmig', sp='r_officer',
        intro='ロヴァニエミ空港。係官は口数が少なく、まっすぐ話す。',
        pairs=[
            ("Good evening. Welcome to Rovaniemi. Passport, please.", E,
             star("Good evening. Here you are."), E),
            OT("Thank you. Why are you visiting Finland?", E, [
                O('sight', "We want to see the northern lights.", E, ok=1,
                  rep=("The northern lights. Many people come for them. I hope you are lucky.", E)),
                O('sigh', "We want a sigh. A very long sigh.", E,
                  rep=("A sigh? No, no. Sightseeing. Do you want to see the sights? The lights?", E)),
                O('trip', "It is a trip around the world.", E, ok=1,
                  rep=("Around the world. And you start the north today. Good.", E))],
               fork={'tw': ['sightseeing']}),
            ("Is this your first time in Lapland?", E,
             star("Yes, it is our first time."), E),
            OT("How long will you stay?", E, [
                O('few', "We will stay a few days.", E, ok=1,
                  rep=("A few days. Good. You will need warm clothes.", E)),
                O('fee', "A fee? Do we pay a fee?", E,
                  rep=("No fee. How long. Two days? Three days? Four days?", E)),
                O('three', "We will stay three nights.", E, ok=1,
                  rep=("Three nights. Then you have three chances to look up at the sky.", E))],
               fork={'tw': ['stay']}),
            ("Thank you. That is all. Welcome to Finland. Stay warm.", E,
             star("Thank you very much. Good night."), E),
        ],
        words=[("passport", E), ("visit", E), ("sightseeing", E), ("stay", E), ("warm", E)],
        conv=1))

    D.append(dict(
        id='rvn_immig2', who='入国審査の係官', bg='rimmig', sp='r_officer2',
        intro='となりの窓口。こんどは、すこし落ち着いた声の係官。',
        pairs=[
            ("Next, please. Good evening. Passport.", E,
             star("Good evening. Here is my passport."), E),
            OT("Do you have a return ticket, or a ticket to your next country?", E, [
                O('next', "Yes. We fly to the next country after Lapland.", E, ok=1,
                  rep=("Good. Please keep it with you. Some people forget it.", E)),
                O('tick', "A ticket? Do you want a ticket to the north?", E,
                  rep=("No, not a new ticket. Your ticket for leaving. Do you have it?", E)),
                O('phone', "Yes. It is on my phone. May I show you?", E, ok=1,
                  rep=("Yes, please show me. A phone is fine.", E))],
               fork={'tw': ['ticket']}),
            ("Where will you sleep tonight?", E,
             star("We have a hotel. Here is the booking."), E),
            OT("I see. Do you have any food or plants with you?", E, [
                O('none', "No. Only clothes and a few snacks.", E, ok=1,
                  rep=("Snacks are fine. Thank you for telling me.", E)),
                O('plant', "A plant? No. I have a plan, not a plant.", E,
                  rep=("Ha. A plan is good. A plant, I mean a flower or a tree. You have none?", E)),
                O('chocolate', "Only a little chocolate for the trip.", E, ok=1,
                  rep=("Chocolate is fine. It is cold outside. You may need it.", E))],
               fork={'tw': ['plant']}),
            ("All good. Welcome to Rovaniemi. Please go on. Your bags are waiting for you.", E,
             star("Thank you. Have a good night."), E),
        ],
        words=[("ticket", E), ("hotel", E), ("booking", E), ("plant", E), ("snacks", E)],
        conv=1))

    # ---------- 手荷物受取 ----------
    D.append(dict(
        id='rvn_bag1', who='手荷物の係員', bg='rbag', sp='r_bag',
        intro='手荷物受け取り。係員が、ベルトの前で静かに待っている。',
        pairs=[
            ("Good evening. Are you looking for your bags?", E,
             star("Yes, we are. The flight from the south."), E),
            OT("The belt is over there. Your bags will come soon. Do you have a big blue suitcase?", E, [
                O('blue', "Yes. It is blue, with a yellow tag.", E, ok=1,
                  rep=("Blue with a yellow tag. Good. It is easy to find.", E)),
                O('blew', "Blew? The wind blew it away?", E,
                  rep=("No, no. Blue. The color. Blue, like the sky before night.", E)),
                O('big', "It is big and blue. It is heavy too.", E, ok=1,
                  rep=("Heavy bags come with a long trip. Take a cart. It will help.", E))],
               fork={'tw': ['suitcase']}),
            ("The carts are by the wall. Please take one.", E,
             star("Thank you. Is the floor slippery outside?"), E),
            OT("Outside, yes. There is snow and ice. Please walk slowly. Do you have boots?", E, [
                O('boots', "Yes. We have warm boots in the bag.", E, ok=1,
                  rep=("Good. Put them on before you go outside.", E)),
                O('boot', "Boots? I only have my sneakers.", E,
                  rep=("Sneakers? Hmm. Boots keep your feet warm and dry. Please find some.", E)),
                O('buy', "Can we buy boots here in Lapland?", E, ok=1,
                  rep=("Maybe in town. Not tonight. Tonight, walk slowly.", E))],
               fork={'tw': ['boots']}),
            ("There is your bag, by the green board. Welcome to the north.", E,
             star("Thank you. Good night."), E),
        ],
        words=[("suitcase", E), ("cart", E), ("slippery", E), ("boots", E), ("snow", E)],
        conv=1))

    D.append(dict(
        id='rvn_bag2', who='同じ便の旅行者', bg='rbag', sp='r_skier',
        intro='ベルトの前。スキー板を持った旅行者が、キングのうすいコートを見ている。',
        pairs=[
            ("Excuse me. Is that your only coat?", E,
             star("Yes, it is. Is it too thin?"), E),
            OT("In Rovaniemi at night, yes. It is very cold. Do you have a warm hat?", E, [
                O('hat', "A hat? I have one in my bag.", E, ok=1,
                  rep=("Good. Put it on before the door. Your head loses heat fast.", E)),
                O('hut', "A hut? We are staying in a hut?", E,
                  rep=("Ha, no. A hat. For your head. H, A, T.", E)),
                O('cold', "No hat. Is it really that cold?", E, ok=1,
                  rep=("Yes. It is really that cold. A hat, gloves, and a scarf. Please.", E))],
               fork={'tw': ['hat']}),
            ("We came for the skis. And you? What brings you here?", E,
             star("We came to see the northern lights."), E),
            OT("Ah, the lights. Nobody can promise them. You look up, and you wait.", E, [
                O('wait', "We can wait. We have time.", E, ok=1,
                  rep=("That is the right way. Wait, and look up.", E)),
                O('weight', "Weight? The lights have weight?", E,
                  rep=("No, no. Wait. W, A, I, T. Stay and look. Wait.", E)),
                O('lucky', "I hope we are lucky.", E, ok=1,
                  rep=("I hope so too. Some nights, the sky is kind.", E))],
               fork={'tw': ['wait']}),
            ("There is my family. Enjoy the north, and keep your head warm.", E,
             star("Thank you. You too. Goodbye!"), E),
        ],
        words=[("coat", E), ("hat", E), ("gloves", E), ("scarf", E), ("wait", E)],
        conv=1))

    # ---------- 到着ロビー(実画) ----------
    D.append(dict(
        id='rvn_lobby1', who='到着ロビーの旅行者', bg='rlobby', sp='r_greeter',
        intro='到着ロビー。天窓の光が、床に細い線を引いている。',
        pairs=[
            ("Welcome to Rovaniemi Airport. Is this your first time here?", E,
             star("Yes. We just landed. What is that line on the floor?"), E),
            OT("That is the Arctic Circle line. The light from the skylight draws it on the floor.", E, [
                O('circle', "The Arctic Circle? We are standing on it?", E, ok=1,
                  rep=("Almost. Walk along the line, and you cross it. It is a good photo place.", E)),
                O('circus', "A circus? Is there a circus here?", E,
                  rep=("No circus. A circle. Round, like a ring. The Arctic Circle.", E)),
                O('light', "The light draws the line. That is beautiful.", E, ok=1,
                  rep=("Yes. In the dark winter, the light on the floor feels special.", E))],
               fork={'tw': ['circle']}),
            ("Look down. There is a small plate with the year on it.", E,
             star("I see it. Why does it have a year?"), E),
            OT("The Arctic Circle moves a little every year. The plate shows the year.", E, [
                O('year', "So every year, the line is in a new place?", E, ok=1,
                  rep=("A very little. Not far. But yes, it moves, a little each year.", E)),
                O('ear', "A new ear? Every year?", E,
                  rep=("Ha. Not an ear. A year. Twelve months. The plate shows the year.", E)),
                O('cross', "Can we cross the line now?", E, ok=1,
                  rep=("Of course. One step, and you are in the Arctic. Go ahead.", E))],
               fork={'tw': ['year']}),
            ("Look at the window. The sky is clear tonight. Maybe it is your lucky night.", E,
             star("Wow. Thank you. We will look up."), E),
        ],
        words=[("welcome", E), ("circle", E), ("skylight", E), ("line", E), ("year", E)],
        conv=1))

    D.append(dict(
        id='rvn_lobby2', who='空港の職員', bg='rlobby', sp='r_local',
        intro='到着ロビーの奥。年配の職員が、ゆっくりと床の線のほうへ歩いてくる。',
        pairs=[
            ("Good evening. You are standing on the line. Do you know where you are?", E,
             star("We are in Lapland, near the Arctic Circle."), E),
            OT("Yes. Lapland. The sun is very low in winter here. Some days, you hardly see it.", E, [
                O('dark', "So the days are dark here in winter?", E, ok=1,
                  rep=("Very dark, and very quiet. But the dark is why the sky is so good.", E)),
                O('duck', "A duck? Why do we see a duck?", E,
                  rep=("No duck. Dark. Not light. The winter days are dark, and short.", E)),
                O('quiet', "It is quiet here. I like it.", E, ok=1,
                  rep=("Good. Many visitors say so. The north is quiet, and kind.", E))],
               fork={'tw': ['dark']}),
            ("Do you have a place to sleep tonight?", E,
             star("Yes. We have a hotel booking. We will take the bus."), E),
            OT("Then please go out and look at the sky first. It is worth it.", E, [
                O('sky', "We will look at the sky first. Thank you.", E, ok=1,
                  rep=("Good. Use your eyes first. Then use the camera.", E)),
                O('sci', "The sci? What is sci?", E,
                  rep=("Not sci. Sky. S, K, Y. Up there, above your head.", E)),
                O('camera', "Can I take a picture with my phone?", E, ok=1,
                  rep=("Yes. But the cold makes phones tired. Keep it in a warm pocket.", E))],
               fork={'tw': ['sky']}),
            ("Enjoy Rovaniemi. And remember, the north is slow. Be slow too.", E,
             star("Thank you. We will. Good night!"), E),
        ],
        words=[("Lapland", E), ("dark", E), ("quiet", E), ("sky", E), ("slow", E)],
        conv=1))

    # ---------- 無料Wi-Fi ----------
    D.append(dict(
        id='rvn_wifi1', who='案内カウンターの係員', bg='rwifi', sp='r_info',
        intro='到着ロビーの案内カウンター。ネットにつなぎたいけれど、どれを選ぶのか分からない。',
        pairs=[
            ("Good evening. How can I help you?", E,
             star("Good evening. Is there free Wi-Fi in the airport?"), E),
            OT("Yes. Open your phone settings and choose Rovaniemi Airport Free Wi-Fi.", E, [
                O('name', "Rovaniemi Airport Free Wi-Fi. Is that the name?", E, ok=1,
                  rep=("Yes, that is the name. Rovaniemi Airport Free Wi-Fi.", E)),
                O('wife', "Wife? My wife is not here.", E,
                  rep=("Not wife. Wi-Fi. W, I, hyphen, F, I. The internet, in the air.", E)),
                O('settings', "I will open my settings. One moment.", E, ok=1,
                  rep=("Take your time. The list may be long. Look for the name with Free.", E))],
               fork={'tw': ['Wi-Fi']}),
            ("Do you see it on your list?", E,
             star("Yes, I see it. I will tap it now."), E),
            OT("Good. When it says connected, you are ready.", E, [
                O('connect', "It says connected. Thank you!", E, ok=1,
                  rep=("Good. Now you can send a message to your family.", E)),
                O('connection', "It says no connection. What should I do?", E,
                  rep=("Try once more. Turn Wi-Fi off, then on. Then choose the name again.", E)),
                O('message', "I want to send a message home.", E, ok=1,
                  rep=("Of course. Tell them you landed safely in the north.", E))],
               fork={'tw': ['connected']}),
            ("Is there anything else? A map, or a bus time?", E,
             star("The bus. Which bus goes to Santa Claus Village?"), E),
        ],
        words=[("free", E), ("Wi-Fi", E), ("settings", E), ("connected", E), ("message", E)],
        conv=1))

    D.append(dict(
        id='rvn_wifi2', who='となりの旅行者', bg='rwifi', sp='r_wifi',
        intro='ロビーのベンチ。となりの旅行者も、スマホの画面と にらめっこしている。',
        pairs=[
            ("Excuse me. Do you know the name of the Wi-Fi here?", E,
             star("Yes. It is Rovaniemi Airport Free Wi-Fi."), E),
            OT("Thank you. I tried, but my phone says it cannot connect. Is yours working?", E, [
                O('work', "Yes, mine is working. Let me look at yours.", E, ok=1,
                  rep=("Thank you. I am bad with phones. Please, take a look.", E)),
                O('walk', "Walking? Do I have to walk to it?", E,
                  rep=("No, not walk. Work. Is your phone working? Does it connect?", E)),
                O('try', "Let us try together. Turn the Wi-Fi off and on.", E, ok=1,
                  rep=("Good idea. Off, and on. I will try it now.", E))],
               fork={'tw': ['working']}),
            ("Oh, it is working now! I can see my messages.", E,
             star("Great. I am happy to help."), E),
            OT("Where are you going now? Is someone waiting for you?", E, [
                O('hotel', "We are going to our hotel by bus.", E, ok=1,
                  rep=("A bus at night is fine. Wear your hat, and hold the rail.", E)),
                O('hotal', "A hot ale? No, no. Our hotel.", E,
                  rep=("Ha. A hotel. A place to sleep. Good. Is it far from here?", E)),
                O('santa', "We want to visit Santa Claus Village.", E, ok=1,
                  rep=("Santa Claus Village. You will like it. It is not far from here.", E))],
               fork={'tw': ['hotel']}),
            ("Have a good stay. And thank you again. I was a little lost.", E,
             star("You are welcome. Good night!"), E),
        ],
        words=[("name", E), ("working", E), ("hotel", E), ("messages", E), ("lost", E)],
        conv=1))

    # ---------- バス乗り場 ----------
    D.append(dict(
        id='rvn_bus1', who='バス乗り場の旅行者', bg='rbus', sp='r_stop',
        intro='空港の外。雪の夜のバス乗り場で、旅行者がバスを待っている。',
        pairs=[
            ("Good evening. Are you waiting for a bus too?", E,
             star("Yes. We want to go to Santa Claus Village. Which bus is it?"), E),
            OT("The Airport Express goes to the village. Bus number eight goes there too, from the city.", E, [
                O('eight', "Bus number eight. Thank you!", E, ok=1,
                  rep=("Yes, eight. Look for the number on the front of the bus.", E)),
                O('eat', "Bus number eat? Do we eat on the bus?", E,
                  rep=("No, eight. E, I, G, H, T. The number after seven. Bus eight.", E)),
                O('express', "Then I will take the Airport Express.", E, ok=1,
                  rep=("Good. Look for the name or the number. Both are easy to see.", E))],
               fork={'tw': ['eight']}),
            ("It is only about two or three kilometers from the airport.", E,
             star("That is close. Can we walk?"), E),
            OT("In the snow, at night? I would not walk. Take the bus, and stay warm.", E, [
                O('bus', "You are right. We will take the bus.", E, ok=1,
                  rep=("Good. It is a short ride. You will be there soon.", E)),
                O('boss', "The boss? Who is the boss?", E,
                  rep=("No boss. Bus. B, U, S. The big car with many seats. It is coming.", E)),
                O('cold', "Yes, it is very cold. The bus is better.", E, ok=1,
                  rep=("Very cold. Yes. Our noses become red. The bus is warm inside.", E))],
               fork={'tw': ['bus']}),
            ("Look, the lights are coming. I think that is your bus.", E,
             star("Thank you. Have a good night!"), E),
        ],
        words=[("bus", E), ("eight", E), ("kilometer", E), ("walk", E), ("village", E)],
        conv=1))

    D.append(dict(
        id='rvn_bus2', who='バスの運転手', bg='rbus', sp='r_driver',
        intro='バスが止まった。運転手が、ドアを開けて待っている。',
        pairs=[
            ("Good evening. Where are you going?", E,
             star("Good evening. Do you go to Santa Claus Village?"), E),
            OT("Yes. This is the Airport Express. Please come in. It is cold outside.", E, [
                O('express', "The Airport Express. Thank you.", E, ok=1,
                  rep=("Yes. Airport Express. Watch your step. The floor may be wet.", E)),
                O('ex', "An X press? What is an X press?", E,
                  rep=("Not X press. Express. It means fast and direct. Airport Express.", E)),
                O('step', "Thank you. I will watch my step.", E, ok=1,
                  rep=("Good. Snow makes shoes wet. Everyone slips a little in winter.", E))],
               fork={'tw': ['express']}),
            ("Please sit anywhere. Put your big bag near the door.", E,
             star("Yes. Is this seat free?"), E),
            OT("Yes, it is free. Some people leave their bags on the seats, but not you. Good.", E, [
                O('seat', "Thank you. We will sit here by the window.", E, ok=1,
                  rep=("Good seat. The window is nice. You can see the snow.", E)),
                O('sit', "Sit? Do I sit here, or stand?", E,
                  rep=("Sit. Please sit down. S, I, T. There are many free seats.", E)),
                O('window', "May I sit by the window and look outside?", E, ok=1,
                  rep=("Of course. The sky is big here. Look up, as well.", E))],
               fork={'tw': ['seat']}),
            ("We will go soon. Sit back. Welcome to the north.", E,
             star("Thank you very much. Good night."), E),
        ],
        words=[("express", E), ("village", E), ("seat", E), ("window", E), ("snow", E)],
        conv=1))
