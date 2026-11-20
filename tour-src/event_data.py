# -*- coding: utf-8 -*-
# 世界一周編 ナイロビ→ドーハ「飽き」対策の台本（タスク014）。設計の正本: docs/pm/deliverables/005-boredom-design-v1.md。
# 決定: 005-1（割りこみ＋持ち越し＋顔なじみ。配役入れかえは台本の原則）／005-3（確率でなく「飽きたサイン」で入れる）。
#
# ここに置くもの
#   1. 割りこみ（A）7つ：場面の外から来る出来事。▶で英文を選び、選んだ文を声に出し、世界が反応して終わる（1往復＋反応）
#   2. 顔なじみ（F）2つ：同じ旅行者との再会、木のキリン2回目（1〜2往復のひとこと場面）
#   3. 持ち越し（B）の差しかえ：キングが前に言ったことを、あとで相手の口から返す（言った場合だけ返る）
#   4. 置き場（SLOTS）
# 配役の原則（D）：新しく書く場面は、相手を係員だけに寄せない。7つのうち係員は1つ（g）だけ。
# 値段・便・ゲート番号・時刻は架空。個人名なし。理由は言わせない（機長のおくれ）。
import window_data as W

T, O, OT = W.T, W.O, W.OT


def ev(D, id, who, bg, sp, pairs, fx=None, kind='ev', **kw):
    D.append(dict(id=id, who=who, bg=bg, sp=sp, intro='', pairs=pairs, words=[], ev=1, auto=1, kind=kind, fx=fx, **kw))


def add(D):
    # ---- 割りこみ（A）。場面の型は1つ：出来事が来る → ▶で選んで言う → 世界が反応する ----
    # a. 入国審査のあと：落としもの。旅行者が走ってくる（005 #2）
    ev(D, 'nbo_ev_a_dropped', 'Traveler', 'immig', 'ev_runner', [
        OT("Excuse me! Is this yours? You dropped it!", "すみません！これはあなたのですか。落としましたよ！", [
            O('yes', "Yes, it's mine. Thank you!", "はい、私のです。ありがとう！",
              rep=("You are welcome! Safe travels!", "どういたしまして。よい旅を！")),
            O('no', "No, it's not mine.", "いいえ、私のではありません。",
              rep=("Oh, sorry! Then I will take it to the officer.", "あ、失礼しました。では係官に届けます。")),
            O('again', "Sorry, could you say that again?", "すみません、もう一度言ってもらえますか。",
              rep=("Of course. Is this yours? It was on the floor, near the line.", "もちろん。これはあなたのですか。列の近くの床にありました。"))])],
        fx='ding')

    # b. 手荷物の入口：雨もり。ぬれた旅行者がとなりにいる（005 #3。NBO #11 の出来事。配役はDの例どおり旅行者）
    ev(D, 'nbo_ev_b_leak', 'Traveler', 'baggage', 'ev_wet', [
        OT("Oh, watch your step! The floor is wet.", "あっ、足もとに気をつけて！床がぬれています。", [
            O('what', "What happened?", "何があったのですか。",
              rep=("The roof is leaking! And the belt has stopped.", "屋根から雨もりです！ベルトも止まりました。")),
            O('belt', "Is the belt working?", "ベルトは動いていますか。",
              rep=("No, it has stopped. We have to wait.", "いいえ、止まっています。待つしかありません。")),
            O('wait', "Where can I wait?", "どこで待てばいいですか。",
              rep=("Over there, by the dry wall. Everyone is waiting there.", "あそこの、かわいた壁のそばです。みんなそこで待っています。"))])],
        fx='drip')

    # c. 出発の前：電話が鳴る。便は定刻どおり。何も起きない回（005 #8。NBO #3）
    ev(D, 'nbo_ev_c_phone', 'Qatar Airways', 'checkinQ', 'ev_phone', [
        OT("Hello. This is Qatar Airways. Your flight to Doha is on time.", "こんにちは。カタール航空です。ドーハ行きの便は定刻どおりです。", [
            O('thanks', "Thank you. We are on our way.", "ありがとう。いま向かっています。",
              rep=("You are welcome. Have a good flight!", "どういたしまして。よい空の旅を！")),
            O('board', "What time does boarding start?", "搭乗は何時に始まりますか。",
              rep=("Boarding starts forty minutes before the flight.", "搭乗は出発の40分前に始まります。")),
            O('again', "Could you say that again, please?", "もう一度言っていただけますか。",
              rep=("Of course. Your flight is on time. Have a good trip!", "もちろん。便は定刻どおりです。よい旅を！"))])],
        fx='ring')

    # d. 免税店のあと：ルルがいない。ルルの助けなしで言う。終わるとルルが布を持って走ってくる（005 #13）
    ev(D, 'nbo_ev_d_lulu', 'Traveler', 'duty', 'ev_trav3', [
        OT("Excuse me. Are you looking for someone?", "すみません。どなたかをお探しですか。", [
            O('friend', "Yes. I am looking for my friend.", "はい。友だちを探しています。",
              rep=("Your friend? I saw her go back into the shop.", "お友だち？お店にもどっていくのを見ましたよ。")),
            O('seen', "Yes. Have you seen my friend?", "はい。友だちを見ませんでしたか。",
              rep=("She went back to look at the colorful cloth.", "カラフルな布を見にもどりましたよ。")),
            O('wait', "No, I am just waiting.", "いいえ、待っているだけです。",
              rep=("Oh, I see. But look, your friend is coming!", "そうですか。でも見て、お友だちが来ましたよ！"))]),
        T("I'm back! Look, King! I found one more beautiful cloth!", "ただいま！見て、キング！もう1枚、すてきな布を見つけたよ！",
          "It is beautiful! Welcome back, Lulu.", "すてきだね！おかえり、ルル。")],
        lvis=0, nohelp=1,
        inter=[{'after': 0, 'anim': 'fade', 'ms': 1400, 'swapAt': 700, 'set': {'lvis': 1, 'sp': 'lulu', 'who': 'Lulu'}}])

    # e. 搭乗ゲートへ向かう間：ゲート変更のアナウンス（005 #14。この区間の主役）
    ev(D, 'nbo_ev_e_gate', 'Announcement', 'gate', '', [
        OT("Attention, please. Qatar Airways flight to Doha. Your gate has changed. Please go to gate fourteen.",
           "お知らせします。カタール航空ドーハ行き。ゲートが変わりました。14番ゲートへお進みください。", [
            O('go', "Let's go to gate fourteen.", "14番ゲートへ行こう。",
              rep=("Thank you. Boarding will begin soon.", "ありがとうございます。まもなく搭乗が始まります。", 'Announcement')),
            O('forty', "Gate forty?", "40番ゲート？",
              rep=("Gate fourteen, not forty! Run, run!", "14番です、40番じゃありません！急いで！", 'Traveler')),
            O('again', "Could you say that again, please?", "もう一度言っていただけますか。",
              rep=("Attention, please. Your gate has changed. Please go to gate fourteen.", "お知らせします。ゲートが変わりました。14番ゲートへお進みください。", 'Announcement'))])],
        fx='pa')

    # f. 機内：機長のアナウンス。到着が少しおくれる。理由は言わせない（005 #17。確認8は決定ログ005-8「推奨どおり」）
    ev(D, 'nbo_ev_f_captain', 'Captain', 'cabinQ', '', [
        OT("Ladies and gentlemen, this is your captain. We will arrive in Doha about thirty minutes late.",
           "ご搭乗のみなさま、機長です。ドーハへの到着は30分ほどおくれる見込みです。", [
            O('ok', "Is everything okay?", "だいじょうぶですか。",
              rep=("Everything is fine. Please relax and enjoy the flight.", "問題ありません。どうぞくつろいで、空の旅をお楽しみください。", 'Cabin crew')),
            O('time', "What time will we arrive?", "何時に着きますか。",
              rep=("A little later than planned. Please relax.", "予定より少しおそくなります。どうぞおくつろぎください。", 'Cabin crew')),
            O('again', "Could you say that again, please?", "もう一度言っていただけますか。",
              rep=("We will arrive in Doha about thirty minutes late. Thank you.", "ドーハへの到着は30分ほどおくれます。ありがとうございます。", 'Captain'))])],
        fx='pa')

    # g. メトロの改札：ルルだけ先に通ってしまう。どれを選んでも doh_metro へ（005 #24。改札の係員が出るのはこの割り込みだけ。doh_metro 本体の相手は、023で となりの乗客 に入れ替え）
    ev(D, 'doh_ev_g_card', 'Doha Metro', 'dmetro', 'd_metro', [
        OT("Excuse me, sir. Your card, please?", "失礼します。カードを見せていただけますか。", [
            O('nocard', "I don't have a card.", "カードを持っていません。",
              rep=("No problem. You can buy one here.", "だいじょうぶです。ここで買えますよ。")),
            O('where', "Where can I buy one?", "どこで買えますか。",
              rep=("Over there. Just follow the signs.", "あちらです。案内に沿って進んでください。")),
            O('friend', "My friend has my card!", "友だちが私のカードを持っています！",
              rep=("Your friend is already inside. Please come this way.", "お友だちはもう中にいますよ。こちらへどうぞ。"))])],
        fx='ding', lvis=0)

    # ---- 顔なじみ（F）。ひとこと場面（1〜2往復）。赤いリボンの旅行者は、ナイロビの列→機内→ドーハのベルトで会う ----
    # 005 #16：機内。通路の向こうの旅行者。「ドーハに1泊」と「スーク・ワキーフ」を、旅行者の口から先に聞く
    ev(D, 'nbo_ev_f1_ribbon', 'Traveler', 'cabinQ', 'ev_ribbon', [
        T("Hello! Are you flying to Doha too?", "こんにちは！あなたたちもドーハへ行くのですか。",
          "Yes, we are. Only one night.", "はい、そうです。1泊だけです。"),
        T("Only one night? Then go to Souq Waqif tonight. It is lovely at night.", "1泊だけ？それなら今夜はスーク・ワキーフへ。夜はすてきですよ。",
          "Thank you! We will go.", "ありがとう！行ってみます。")],
        kind='short')

    # 005 #22：ドーハの税関。木のキリン2回目。ナイロビの係員は笑い、ここでは表情を変えない（国柄）。木のキリンを出した人（nbo_sec2）だけ
    ev(D, 'doh_ev_f2_customs', 'Customs officer', 'dbag', 'd_officer2', [
        T("Sir. What is this long item?", "お客さま。この長いものは何ですか。",
          "It's a wooden giraffe. It's a souvenir.", "木のキリンです。おみやげです。"),
        T("A giraffe. I see. Welcome to Qatar.", "キリン。なるほど。カタールへようこそ。",
          "Thank you. Have a good night!", "ありがとう。おやすみなさい！")],
        kind='short')


# ---- 持ち越し（B）：(場面, 何番目の相手のセリフか(0から), 種の場面, 相手のセリフ, 日本語, キングのセリフ(なければNone), 日本語) ----
# 種の場面を遊んでいたときだけ返る（遊んでいなければ元のセリフ）。相手が「キングが言ったこと」を質問にして返す形。
VARIANTS = [
    # 005 1-4 の種5つ
    ('nbo_plane2', 1, 'sage_3',
     "Of course. What polite English! Chicken with rice, or vegetable pasta?", "もちろん。なんて丁寧な英語でしょう。チキンとライス、または野菜のパスタです。", None, None),
    ('nbo_taxi1', 1, 'nbo_immig2',
     "Sure. Villa Rosa Kempinski? Nice choice. Please wait in this line. The next car is yours.", "かしこまりました。ヴィラ・ローザ・ケンピンスキー？いいですね。この列でお待ちください。次の車があなたたちのです。", None, None),
    ('nbo_sec2', 3, 'nbo_lounge2',
     "Ah, a giraffe! Did you meet the real ones here? Very nice. No problem.", "ああ、キリンですね。こちらで本物には会えましたか。すてきです。問題ありません。",
     "Yes, we did! Can I close my bag?", "はい、会えました！かばんを閉めてもいいですか。"),
    ('doh_immig1', 1, 'nbo_checkin1',
     "How long will you stay in Qatar? One night, yes?", "カタールにはどのくらい滞在しますか。1泊ですよね。",
     "Yes. Only one night. We fly to Helsinki tomorrow.", "はい。1泊だけです。明日ヘルシンキへ飛びます。"),
    ('doh_taxi', 1, 'doh_immig2',
     "Souq Waqif, the old market? It takes about twenty minutes.", "スーク・ワキーフ、古い市場ですね。20分ほどです。", None, None),
    # 005 #7：入国で言った「3日」が、運転手の口から返る（1行差しかえ）
    ('nbo_taxi2', 4, 'nbo_immig2',
     "Three days in Nairobi? Then you must see the giraffes. Sit back and enjoy the ride!", "ナイロビに3日？それならキリンを見なくちゃ。ゆったり座って、ドライブを楽しんで！", None, None),
    # 005 #14 に理由がつく／#3 雨もりが出来事の理由になる／#21 再会
    ('nbo_gate1', 2, 'nbo_ev_e_gate',
     "Yes, this is the new gate. Gate fourteen. Please wait over there.", "はい、新しいゲートです。14番ゲートです。あちらでお待ちください。", None, None),
    ('nbo_bag1', 0, 'nbo_ev_b_leak',
     "Excuse me. The belt stopped for a while because of the rain. Is this the belt for the flight from Tokyo?", "すみません。雨でベルトがしばらく止まっていました。ここは東京からの便のベルトですか。", None, None),
    ('doh_bag2', 0, 'nbo_ev_f1_ribbon',
     "Oh! You again! From the plane! I think this blue suitcase is mine.", "あっ！また会いましたね。飛行機の！この青いスーツケース、私のだと思います。", None, None),
]

# ---- 置き場。at: enter=その場所に入るとき／after=その場所の場面が終わったとき／vid=その場面が始まるとき。
# sign=1 は「飽きたサイン」があるときだけ（005-3）。sign=0 は物語の決まった出会い（顔なじみ）。need=その場面を遊んでいたときだけ ----
SLOTS = [
    dict(id='a', vid='nbo_ev_a_dropped', at='after', key='immig', sign=1),
    dict(id='b', vid='nbo_ev_b_leak', at='enter', key='bag', sign=1),
    dict(id='c', vid='nbo_ev_c_phone', at='enter', key='qcheckin', sign=1),
    dict(id='d', vid='nbo_ev_d_lulu', at='after', key='duty', sign=1),
    dict(id='e', vid='nbo_ev_e_gate', at='enter', key='gate', sign=1),
    dict(id='f', vid='nbo_ev_f_captain', at='after', key='qplane', sign=1),
    dict(id='g', vid='doh_ev_g_card', at='vid', key='doh_metro', sign=1),
    dict(id='f1', vid='nbo_ev_f1_ribbon', at='enter', key='qplane', sign=0),
    dict(id='f2', vid='doh_ev_f2_customs', at='after', key='dbag', sign=0, need='nbo_sec2'),
]
