# -*- coding: utf-8 -*-
# 世界一周編 1日目「羽田から出発」(タスク043)。チェックイン → 保安検査 → 出国 → 出発ゲート → 搭乗 → 機内(深夜便)。
# ※会話文はすべて仮(台本は後から差し込む)。差し込むときは、場面の id・bg・sp・words の形は変えず、pairs と intro だけを入れ替える。
#   券ごとの出し分け: _ow = oneworld(Qatar Airways・ドーハ乗り継ぎ) / _star = Star Alliance(Turkish Airlines・イスタンブール乗り継ぎ)。
#   便の時刻・便名は物語の中の架空(実在の便の時刻ではない。作る直前に公式で確認する)。会話に「復習」「テスト」の言葉は使わない。
# 秘密イベントの下地: hnd_gate_ow / hnd_gate_star は keep='hnd1' を持つ。この場面を最後まで遊ぶと、ルルが小さな忘れ物を拾ってカバンに入る
#   (保存は既存の kanpe-tour-save-v1 の keep。画面では予告せず、設定のルルのカバンの記録帳に静かに載るだけ)。回収の場面(帰国の羽田)はまだない。
from window_data import star, O, OT


def add(D):
    def d(id, who, bg, sp, intro, pairs, words, **kw):
        D.append(dict(id=id, who=who, bg=bg, sp=sp, intro=intro, pairs=pairs, words=words, **kw))

    # ---- チェックイン(券ごとに航空会社がちがう) ----
    d('hnd_checkin_ow', 'Qatar Airwaysのチェックイン係', 'checkinQ', 'qr_checkin', '羽田空港の夜。Qatar Airwaysのカウンターで、係の人が笑顔で待っている。', [
        ("Good evening. Welcome to Qatar Airways. Where are you flying tonight?", "こんばんは。カタール航空へようこそ。今夜はどちらへ？", "*We* *are* *flying* *to* *Doha*, *then* *Nairobi*.", "ドーハを通って、ナイロビへ行きます。"),
        ("Passports, please. Do you have any bags to check in?", "パスポートをお願いします。預ける荷物はありますか。", "*Yes*. *One* *suitcase*, *please*.", "はい。スーツケースを1つお願いします。"),
        ("Please put it on the scale. Thank you. It is fine.", "はかりにのせてください。ありがとうございます。大丈夫です。", "*Can* *I* *have* *a* *window* *seat*?", "窓側の席をお願いできますか。"),
        ("Yes, a window seat. Your flight leaves late tonight.", "はい、窓側です。便は今夜おそくに出発します。", "*What* *time* *does* *boarding* *start*?", "搭乗は何時からですか。"),
        ("About forty minutes before. Here are your boarding passes. Have a good trip!", "出発の約40分前です。こちらが搭乗券です。よい旅を！", "*Thank* *you*. *See* *you* *later*!", "ありがとう。またあとで！")],
        [("check in", "チェックインする"), ("suitcase", "スーツケース"), ("window seat", "窓側の席"), ("boarding pass", "搭乗券"), ("tonight", "今夜")])
    d('hnd_checkin_star', 'Turkish Airlinesのチェックイン係', 'checkinT', 'tk_checkin', '羽田空港の夜。Turkish Airlinesのカウンターで、係の人が手をあげている。', [
        ("Good evening. Welcome to Turkish Airlines. Where are you flying tonight?", "こんばんは。ターキッシュ エアラインズへようこそ。今夜はどちらへ？", "*We* *are* *flying* *to* *Istanbul*, *then* *Nairobi*.", "イスタンブールを通って、ナイロビへ行きます。"),
        ("Passports, please. Do you have any bags to check in?", "パスポートをお願いします。預ける荷物はありますか。", "*Yes*. *One* *suitcase*, *please*.", "はい。スーツケースを1つお願いします。"),
        ("Please put it on the scale. Thank you. It is fine.", "はかりにのせてください。ありがとうございます。大丈夫です。", "*Can* *I* *have* *a* *window* *seat*?", "窓側の席をお願いできますか。"),
        ("Yes, a window seat. Your flight leaves late tonight.", "はい、窓側です。便は今夜おそくに出発します。", "*What* *time* *does* *boarding* *start*?", "搭乗は何時からですか。"),
        ("About forty minutes before. Here are your boarding passes. Have a good trip!", "出発の約40分前です。こちらが搭乗券です。よい旅を！", "*Thank* *you*. *See* *you* *later*!", "ありがとう。またあとで！")],
        [("check in", "チェックインする"), ("suitcase", "スーツケース"), ("window seat", "窓側の席"), ("boarding pass", "搭乗券"), ("tonight", "今夜")])

    # ---- 保安検査(券によらず1本) ----
    d('hnd_sec', '保安検査の係員', 'security', 'sec_n1', '保安検査の列。係員がていねいに、ゆっくり案内している。', [
        ("Next, please. Please put your bag on the belt.", "次の方どうぞ。かばんをベルトにのせてください。", "*Okay*. *Do* *I* *take* *out* *my* *laptop*?", "はい。ノートパソコンは出しますか。"),
        ("Yes, please. Put it in a separate tray.", "はい、お願いします。べつのトレーに入れてください。", "*Here* *you* *are*. *What* *about* *my* *jacket*?", "どうぞ。上着はどうしますか。"),
        ("Jackets off, please. Do you have any liquids?", "上着はぬいでください。液体はお持ちですか。", "*Only* *a* *small* *bottle*. *It* *is* *empty*.", "小さいボトルだけです。空です。"),
        ("That is fine. Please walk through the gate.", "大丈夫です。ゲートを通ってください。", "*Like* *this*? *Is* *it* *okay*?", "こうですか。大丈夫ですか。"),
        ("Yes, all clear. Thank you. Have a safe flight.", "はい、問題ありません。ありがとうございます。よい空の旅を。", "*Thank* *you*. *Good* *night*!", "ありがとう。おやすみなさい！")],
        [("laptop", "ノートパソコン"), ("tray", "トレー"), ("jacket", "上着"), ("liquids", "液体"), ("empty", "空の")])

    # ---- 出国審査(券によらず1本) ----
    d('hnd_exit', '出国審査の係官', 'immigH', 'officer', '出国審査の窓口。係官が、パスポートを受け取った。', [
        ("Passport and boarding pass, please.", "パスポートと搭乗券をお願いします。", "*Here* *you* *are*.", "どうぞ。"),
        ("Thank you. Where are you going tonight?", "ありがとうございます。今夜はどちらへ？", "*We* *are* *going* *to* *Nairobi*, *in* *Kenya*.", "ケニアのナイロビへ行きます。"),
        ("Nairobi, nice. Is this a business trip?", "ナイロビですか、いいですね。お仕事ですか。", "*No*. *We* *are* *traveling* *around* *the* *world*.", "いいえ。世界を旅しています。"),
        ("Wonderful. Please look at the camera.", "すばらしい。カメラを見てください。", "*Like* *this*?", "こうですか。"),
        ("Perfect. All done. Enjoy your trip!", "完ぺきです。終わりました。旅を楽しんで！", "*Thank* *you*. *Goodbye*!", "ありがとう。さようなら！")],
        [("passport", "パスポート"), ("business trip", "出張"), ("around the world", "世界じゅうを"), ("camera", "カメラ"), ("enjoy", "楽しむ")])

    # ---- 出発ゲート(背景は券で出し分け。ルルの拾い物=秘密イベントの下地: keep='hnd1') ----
    d('hnd_gate_ow', '出発ゲートの係員', 'hgateOW', 'gate_agent', '深夜の出発ゲート。大きな窓のむこうに、Qatar Airwaysの飛行機がとまっている。', [
        ("Good evening. Is this your first time on Qatar Airways?", "こんばんは。カタール航空は、はじめてですか。", "*Yes*, *it* *is*. *Is* *this* *the* *gate* *for* *Doha*?", "はい、はじめてです。ここはドーハ行きのゲートですか。"),
        ("Yes, this is Gate 141. Boarding will start soon.", "はい、141番ゲートです。まもなく搭乗が始まります。", "*Can* *we* *sit* *here* *and* *wait*?", "ここで座って待ってもいいですか。"),
        ("Of course. Please sit on any bench.", "もちろん。どのベンチでもどうぞ。", "*It* *is* *very* *quiet* *tonight*.", "今夜はとても静かですね。"),
        ("Yes, it is a late flight. Most people are already asleep.", "はい、おそい便です。ほとんどの人はもう眠っています。", "*That* *is* *fine*. *We* *can* *sleep* *on* *the* *plane*.", "大丈夫です。機内で眠ります。"),
        ("Good idea. I will call you when it is time.", "いい考えです。時間になったらお呼びします。", "*Thank* *you*. *We* *will* *wait* *here*.", "ありがとう。ここで待っています。")],
        [("gate", "ゲート"), ("bench", "ベンチ"), ("quiet", "静かな"), ("late", "おそい"), ("asleep", "眠っている")], keep='hnd1')
    d('hnd_gate_star', '出発ゲートの係員', 'hgateST', 'gate_agent2', '深夜の出発ゲート。大きな窓のむこうに、Turkish Airlinesの飛行機がとまっている。', [
        ("Good evening. Is this your first time on Turkish Airlines?", "こんばんは。ターキッシュ エアラインズは、はじめてですか。", "*Yes*, *it* *is*. *Is* *this* *the* *gate* *for* *Istanbul*?", "はい、はじめてです。ここはイスタンブール行きのゲートですか。"),
        ("Yes, this is Gate 141. Boarding will start soon.", "はい、141番ゲートです。まもなく搭乗が始まります。", "*Can* *we* *sit* *here* *and* *wait*?", "ここで座って待ってもいいですか。"),
        ("Of course. Please sit on any bench.", "もちろん。どのベンチでもどうぞ。", "*It* *is* *very* *quiet* *tonight*.", "今夜はとても静かですね。"),
        ("Yes, it is a late flight. Most people are already asleep.", "はい、おそい便です。ほとんどの人はもう眠っています。", "*That* *is* *fine*. *We* *can* *sleep* *on* *the* *plane*.", "大丈夫です。機内で眠ります。"),
        ("Good idea. I will call you when it is time.", "いい考えです。時間になったらお呼びします。", "*Thank* *you*. *We* *will* *wait* *here*.", "ありがとう。ここで待っています。")],
        [("gate", "ゲート"), ("bench", "ベンチ"), ("quiet", "静かな"), ("late", "おそい"), ("asleep", "眠っている")], keep='hnd1')

    # ---- 搭乗(同じゲート。ここで1区間めの券をちぎる) ----
    d('hnd_board_ow', '出発ゲートの係員', 'hgateOW', 'gate_agent2', 'アナウンスが流れた。搭乗がはじまる。', [
        ("Attention, please. Flight to Doha is now boarding.", "お知らせします。ドーハ行きの搭乗がはじまりました。", "*Excuse* *me*. *Can* *we* *board* *now*?", "すみません。いま乗れますか。"),
        ("May I see your boarding passes and passports?", "搭乗券とパスポートを見せていただけますか。", "*Here* *they* *are*.", "どうぞ。"),
        ("Thank you. Please go down the bridge to the plane.", "ありがとうございます。ブリッジを通って飛行機へどうぞ。", "*Is* *it* *a* *long* *flight*?", "長いフライトですか。"),
        ("It is a long flight. Please get some rest.", "長いフライトです。ゆっくり休んでください。", "*We* *will*. *Thank* *you* *for* *your* *help*.", "そうします。ありがとうございました。"),
        ("My pleasure. Have a safe flight!", "どういたしまして。よい空の旅を！", "*Goodbye*, *Tokyo*!", "さよなら、東京！")],
        [("board", "搭乗する"), ("bridge", "ブリッジ"), ("flight", "フライト"), ("rest", "休む"), ("safe", "安全な")])
    d('hnd_board_star', '出発ゲートの係員', 'hgateST', 'gate_agent2', 'アナウンスが流れた。搭乗がはじまる。', [
        ("Attention, please. Flight to Istanbul is now boarding.", "お知らせします。イスタンブール行きの搭乗がはじまりました。", "*Excuse* *me*. *Can* *we* *board* *now*?", "すみません。いま乗れますか。"),
        ("May I see your boarding passes and passports?", "搭乗券とパスポートを見せていただけますか。", "*Here* *they* *are*.", "どうぞ。"),
        ("Thank you. Please go down the bridge to the plane.", "ありがとうございます。ブリッジを通って飛行機へどうぞ。", "*Is* *it* *a* *long* *flight*?", "長いフライトですか。"),
        ("It is a long flight. Please get some rest.", "長いフライトです。ゆっくり休んでください。", "*We* *will*. *Thank* *you* *for* *your* *help*.", "そうします。ありがとうございました。"),
        ("My pleasure. Have a safe flight!", "どういたしまして。よい空の旅を！", "*Goodbye*, *Tokyo*!", "さよなら、東京！")],
        [("board", "搭乗する"), ("bridge", "ブリッジ"), ("flight", "フライト"), ("rest", "休む"), ("safe", "安全な")])

    # ---- 機内(深夜便。終わると世界マップの飛ぶ画面 → ナイロビ到着) ----
    d('hnd_plane_ow', 'Qatar Airwaysの客室乗務員', 'cabinQ', 'qr_crew', '機内。ライトがうすくなって、客室乗務員が小さな声で声をかけてくれた。', [
        ("Good evening. Welcome aboard. May I see your boarding pass?", "こんばんは。ご搭乗ありがとうございます。搭乗券を見せていただけますか。", "*Good* *evening*. *Here* *it* *is*.", "こんばんは。これです。"),
        ("Thank you. Your seat is on the left, by the window.", "ありがとうございます。お席は左の窓側です。", "*Thank* *you*. *Where* *can* *I* *put* *my* *bag*?", "ありがとう。かばんはどこに置けますか。"),
        ("In the overhead bin. Let me help you.", "頭上の荷物入れに。お手伝いします。", "*That* *is* *very* *kind*. *May* *I* *have* *a* *blanket*?", "ご親切にどうも。毛布をいただけますか。"),
        ("Of course. It is a night flight, so we will turn the lights down.", "もちろんです。夜の便ですので、ライトを少し暗くしますね。", "*That* *sounds* *nice*. *Good* *night*.", "いいですね。おやすみなさい。"),
        ("Good night. Sleep well. We will land in Doha in the morning.", "おやすみなさい。ぐっすりどうぞ。ドーハには朝に着きます。", "*Thank* *you*. *See* *you* *in* *Doha*!", "ありがとう。ドーハで会いましょう！")],
        [("aboard", "搭乗して"), ("overhead bin", "頭上の荷物入れ"), ("blanket", "毛布"), ("night flight", "夜の便"), ("land", "着陸する")])
    d('hnd_plane_star', 'Turkish Airlinesの客室乗務員', 'cabinT', 'tk_crew', '機内。ライトがうすくなって、客室乗務員が小さな声で声をかけてくれた。', [
        ("Good evening. Welcome aboard. May I see your boarding pass?", "こんばんは。ご搭乗ありがとうございます。搭乗券を見せていただけますか。", "*Good* *evening*. *Here* *it* *is*.", "こんばんは。これです。"),
        ("Thank you. Your seat is on the left, by the window.", "ありがとうございます。お席は左の窓側です。", "*Thank* *you*. *Where* *can* *I* *put* *my* *bag*?", "ありがとう。かばんはどこに置けますか。"),
        ("In the overhead bin. Let me help you.", "頭上の荷物入れに。お手伝いします。", "*That* *is* *very* *kind*. *May* *I* *have* *a* *blanket*?", "ご親切にどうも。毛布をいただけますか。"),
        ("Of course. It is a night flight, so we will turn the lights down.", "もちろんです。夜の便ですので、ライトを少し暗くしますね。", "*That* *sounds* *nice*. *Good* *night*.", "いいですね。おやすみなさい。"),
        ("Good night. Sleep well. We will land in Istanbul in the morning.", "おやすみなさい。ぐっすりどうぞ。イスタンブールには朝に着きます。", "*Thank* *you*. *See* *you* *in* *Istanbul*!", "ありがとう。イスタンブールで会いましょう！")],
        [("aboard", "搭乗して"), ("overhead bin", "頭上の荷物入れ"), ("blanket", "毛布"), ("night flight", "夜の便"), ("land", "着陸する")])

    # ---- 28日目 羽田に戻った場面: 初日に拾った落とし物(木のおもちゃの飛行機)を持ち主に返す(タスク059・oneworld の28日目だけ) ----
    # 出る条件: 保存の keep.hnd1(1日目の出発ゲートで拾った)があるセーブだけ。ない人には、この場面もタブも出ない。
    # 新しい保存キーは作らない。場面を遊ぶと save.seen['hnd_return'] が立つだけ(既存の記録)。keep.hnd1 はそのまま残し、カバンの記録帳の1行がここで「かえした」に変わる。
    # 背景は既存の出発ゲート(hgateOW)。人の絵は出さない(声だけ。出発ゲートの場面と同じ)。会話の型は 053 の「分かれ目」(conv=1): 画面は英語だけ・日本語訳は出さない。
    # ok なしの返事 = 聞き違えた人の返事(相手が言い直してくれる。物語は止まらない)。個人名なし・実在の店名なし。
    d('hnd_return', '落とし物の持ち主', 'hgateOW', 'gate_agent2', 'ひさしぶりの羽田。出発ゲートの前で、ひとりの男の人が、足もとを見ながらゆっくり歩いている。', [
        ("Excuse me, I am sorry to bother you. A month ago, I lost a small toy at this gate.",
         "すみません、お邪魔してごめんなさい。1か月前、このゲートで小さなおもちゃをなくしたんです。",
         star("A toy? What kind of toy is it?"), "おもちゃ？どんなおもちゃですか。"),
        OT("It is a wooden airplane with a blue tail. My son loves it. He asks about it every day.",
           "青い尾翼の、木の飛行機です。息子が大好きで、毎日それのことを聞くんです。", [
            O('plane', "A wooden airplane? I think we found it!", "木の飛行機？それ、見つけたと思います！", ok=1,
              rep=("You found it? Oh, that is wonderful news!", "見つけた？ああ、すばらしい知らせです！")),
            O('plain', "A wooden plain? What is a plain?", "木の平原？平原って何ですか。",
              rep=("Not a plain. An airplane! It has two wings and it flies in the sky.",
                   "平原ではなく、飛行機です！翼が2つあって、空を飛びます。")),
            O('blue', "A blue tail? Wait, I think my friend has it.", "青い尾翼？待って、友だちが持っていると思います。", ok=1,
              rep=("Your friend has it? Please, where is it?", "友だちが持っている？お願いです、どこですか。"))],
           fork={'tw': ['airplane']}),
        ("Please, may I see it? I only want to know if it is the same one.",
         "見せてもらえませんか。同じものか、確かめたいだけなんです。",
         star("Yes. Lulu found it at this gate. She kept it safe in her bag."), "はい。ルルがこのゲートで拾いました。ずっとカバンの中で大切に持っていました。"),
        OT("It is the same one! It traveled around the world with you. How can I thank you?",
           "同じものです！あなたたちと世界をひとまわりしたんですね。どうお礼をしたらいいでしょう。", [
            O('home', "No thanks. I am just happy it is home.", "お礼はいりません。帰ってこられて、うれしいだけです。", ok=1,
              rep=("You are very kind. My son will be so happy.", "とても親切な方ですね。息子がどんなに喜ぶでしょう。")),
            O('tank', "A tank? I do not need a tank.", "戦車？戦車はいりません。",
              rep=("Ha ha, not a tank! Thank you. T, H, A, N, K. It means I am very grateful.",
                   "あはは、戦車ではなく！サンキューです。T・H・A・N・K。とても感謝している、という意味です。")),
            O('son', "Please give it to your son. Thank you for waiting.", "息子さんにわたしてあげてください。待っていてくれて、ありがとう。", ok=1,
              rep=("I will. He will take it to bed tonight, I am sure.", "そうします。今夜はきっと、ベッドに持っていきますよ。"))],
           fork={'tw': ['thank']}),
        ("Welcome home, travelers. Please take care on your way. I hope you had a wonderful trip.",
         "おかえりなさい、旅人さん。気をつけて帰ってくださいね。すばらしい旅だったのならいいのですが。",
         star("Thank you. It was the best trip. Goodbye!"), "ありがとう。最高の旅でした。さようなら！"),
    ],
        [("airplane", "飛行機"), ("wooden", "木の"), ("toy", "おもちゃ"), ("lost", "なくした"), ("thank", "感謝する")], conv=1)
