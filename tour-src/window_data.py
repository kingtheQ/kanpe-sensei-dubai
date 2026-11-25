# -*- coding: utf-8 -*-
# 世界一周編 窓口の台本（タスク012）。設計の正本: docs/pm/deliverables/003（会話）・004（診断）・011（宣言文）。
# 会話1・2・5・7・8 は 003 のとおり。強調の＊印は star() が自動で付ける（冠詞・前置詞などは付けない）。
# 値段は素材集の数字（確認レベルB・公式未確認）。個人名なし。
import re

STOP = set('a an the to of in on at and or for with from as is am are be it that this my your our so'.split())

def star(s):
    out = []
    for tok in s.split(' '):
        m = re.match(r"^([^A-Za-z0-9]*)(.*?[A-Za-z0-9])([^A-Za-z0-9]*)$", tok)
        if not m or m.group(2).lower() in STOP:
            out.append(tok)
        else:
            out.append(m.group(1) + '*' + m.group(2) + '*' + m.group(3))
    return ' '.join(out)

WHO = '世界一周の窓口係'

def scene(D, id, turns, intro='The Round the World desk.', auto=1, bg='tdesk'):
    D.append(dict(id=id, who=WHO, bg=bg, sp='desk_rtw', intro=intro, pairs=turns, words=[], win=1, auto=auto))

def T(n, njp, y, yjp, **kw):
    t = dict(n=n, njp=njp, y=star(y) if not kw.get('diag') else y, yjp=yjp)
    t.update(kw)
    return t

def O(k, y, jp, **kw):
    o = dict(k=k, y=star(y), jp=jp)
    o.update(kw)
    return o

def OT(n, njp, opts, **kw):
    t = dict(n=n, njp=njp, y='', yjp='', opts=opts)
    t.update(kw)
    return t


# ---- スターの決まり(公式・確認日2026-11-25。タスク088) と 1周目のルート ----
# 窓口で係員が一緒に数える。数字は下のルートから計算し、決まりを超えるルートならビルドを止める。
RULE = dict(stops=15, moves=16, same_country=3, days_min=10, days_max=365, trip_days=30)
NUMW = {3: 'three', 5: 'five', 10: 'ten', 13: 'thirteen', 15: 'fifteen', 16: 'sixteen', 30: 'thirty'}
# 寄港(24時間以上の滞在)。出発地(羽田)は数えない。[(都市, 国)]
ROUTE_STOPS = [('Nairobi', 'Kenya'), ('Doha', 'Qatar'), ('Rovaniemi', 'Finland'), ('Athens', 'Greece'), ('Rome', 'Italy'),
               ('Zurich', 'Switzerland'), ('Frankfurt', 'Germany'), ('London', 'United Kingdom'), ('Lisbon', 'Portugal'),
               ('New York', 'United States'), ('Honolulu', 'United States'), ('Sydney', 'Australia'),
               ('Singapore', 'Singapore'), ('Bangkok', 'Thailand'), ('Guam', 'United States')]
JPN = {'Nairobi': 'ナイロビ', 'Doha': 'ドーハ', 'Rovaniemi': 'ロヴァニエミ', 'Athens': 'アテネ', 'Rome': 'ローマ', 'Zurich': 'チューリッヒ',
       'Frankfurt': 'フランクフルト', 'London': 'ロンドン', 'Lisbon': 'リスボン', 'New York': 'ニューヨーク', 'Honolulu': 'ホノルル',
       'Sydney': 'シドニー', 'Singapore': 'シンガポール', 'Bangkok': 'バンコク', 'Guam': 'グアム'}
ROUTE_RAIL = [('Rome', 'Zurich'), ('Zurich', 'Frankfurt'), ('Frankfurt', 'London')]   # 陸路(鉄道)の区間
def route_facts():
    from collections import Counter
    city = ['Haneda'] + [c for c, _ in ROUTE_STOPS] + ['Haneda']
    moves = len(city) - 1
    rail = len(ROUTE_RAIL)
    for a, b in ROUTE_RAIL:
        assert city.index(a) + 1 == city.index(b), 'rail leg not on route: %s-%s' % (a, b)
    cc = Counter(k for _, k in ROUTE_STOPS)
    f = dict(stops=len(ROUTE_STOPS), moves=moves, rail=rail, flights=moves - rail, max_same=max(cc.values()),
             us=[c for c, k in ROUTE_STOPS if k == 'United States'])
    assert 2 <= f['stops'] <= RULE['stops'] and f['moves'] <= RULE['moves'] and f['max_same'] <= RULE['same_country'], f
    assert RULE['days_min'] <= RULE['trip_days'] <= RULE['days_max']
    return f

# ---- 宣言文（011 の本文。70語・9文。まとまった1つの文として言う） ----
DECL = ("This is my promise, Lulu. We will travel around the world together, and have fun every day. "
        "My body is healthy, my mind is calm. I eat good food, sleep well, and never push too hard. "
        "When I feel afraid, I breathe and think of you. We both help each other. "
        "Let's see every village, hear every voice, and share every little treasure. "
        "Thank you for being here. Let's go!")
DECL_JP = ("これがわたしの約束だよ、ルル。ふたりで世界じゅうを旅して、毎日、楽しもう。からだは元気。心は穏やか。"
           "おいしいものを食べて、よく眠って、無理はしすぎない。こわくなったら、深呼吸して、あなたのことを思う。"
           "ふたりで、助け合う。すべての村を見て、すべての声を聞いて、小さな宝ものを分かち合おう。"
           "そばにいてくれて、ありがとう。さあ、行こう！")

# 宣言を文ごとに区切る(タスク089)。ルルがお手本→プレイヤーが言う、を1文ずつ。DECL 全体(終わりの宣言・比較の記録)は上の1本のまま。
DECL_SENT = [s.strip() for s in re.split(r'(?<=[.!?]) ', DECL)]
DECL_SENT_JP = ["これがわたしの約束だよ、ルル。", "ふたりで世界じゅうを旅して、毎日、楽しもう。", "からだは元気。心は穏やか。",
                "おいしいものを食べて、よく眠って、無理はしすぎない。", "こわくなったら、深呼吸して、あなたのことを思う。", "ふたりで、助け合う。",
                "すべての村を見て、すべての声を聞いて、小さな宝ものを分かち合おう。", "そばにいてくれて、ありがとう。", "さあ、行こう！"]
assert ' '.join(DECL_SENT) == DECL and ''.join(DECL_SENT_JP) == DECL_JP and len(DECL_SENT) == len(DECL_SENT_JP) == 9, DECL_SENT

# ---- 読み上げ確認（004 の S3。券で値段・大陸の数だけ変わる） ----
def readback(price, cont):
    return ("Let me read it back. Round the world, business class. %s continents in thirty days. "
            "We leave from Haneda on the fifth, and my first destination is Nairobi. "
            "I have one large bag and a small one. The price is %s yen. "
            "Everything is right. I will take it. Please issue the ticket." % (cont, price))
def readback_jp(price_jp, cont_jp):
    return ("読み上げます。世界一周、ビジネスクラス。30日で%s大陸。5日に羽田を出て、最初の目的地はナイロビ。"
            "大きいカバンが1つと小さいのが1つ。値段は%s円。すべて合っています。これにします。発券してください。" % (cont_jp, price_jp))

# 値段（素材集の数字。確認レベルB・確認日2026-11-12・公式未確認）
PRICE = {
    'star': ('nine hundred fifty-eight thousand, nine hundred', '958,900', 'Five'),
    'ow5':  ('one million, seventy-four thousand, three hundred', '1,074,300', 'Five'),
    'ow4':  ('nine hundred thirty-six thousand, five hundred', '936,500', 'Four'),
}
TICKET_NAME = {'star': 'Star Alliance', 'ow5': 'oneworld Explorer', 'ow4': 'oneworld Explorer'}

def add(D):
    # ---------- 宣言(089) ----------
    # 係員の短い一言 → ルルがお手本(1文) → プレイヤーが言う(マイクの大きい絵)、を9文ぶん。前の旅のメモは win_memo(window.js が組む)に分けた。
    LULU = {'who': 'Lulu', 'sp': 'lulu'}
    decl = [T("This is a promise for your trip.", "これは、あなたの旅の約束です。",
              "Okay. I'm ready.", "はい。いいですよ。")]
    for i, (en, jp) in enumerate(zip(DECL_SENT, DECL_SENT_JP)):
        kw = dict(diag='decl', dp=1, cx=LULU)
        if i == 0: kw['df'] = 1
        if i == len(DECL_SENT) - 1:
            kw['dl'] = 1
            kw['rep'] = ("That was beautiful, King.", "すてきだったよ、キング。")
        decl.append(T(en, jp, en, jp, **kw))
    scene(D, 'win_decl', decl, intro='The Round the World desk. Lulu is beside you.', auto=0)

    # ---------- 会話1：はじめての人(089: 1つの吹き出しは1文まで) ----------
    scene(D, 'win_c1', [
        T("Is this your first time?", "はじめてですか。",
          "Yes. I'm excited, but a little nervous.", "はい。わくわくしますが、少し緊張しています。"),
        OT("Do you already know where you want to go?",
           "行きたい場所はもう決まっていますか。", [
            O('A', "Not really. I just want to see famous cities.", "あまり。有名な街を見たいだけです。",
              mt='star', why="You want to see famous cities."),
            O('B', "Yes. I have a few places on my map.", "はい。地図にいくつか置いてあります。")]),
        T("Many people start that way.", "そう始める人は多いです。",
          "I see. Thank you.", "なるほど。ありがとう。",
          by={'A': ("Many people start that way.", "そう始める人は多いです。"),
              'B': ("Good. Your places will help us choose the ticket.", "よかった。その場所が、券選びの助けになります。")}),
        T("Star Alliance has simple rules.", "スターアライアンスは、決まりが簡単です。",
          "Simple rules. That sounds good.", "簡単な決まり。いいですね。"),
        T("Let me show you the rules on the map.", "地図で、決まりをお見せします。",
          "Yes, please show me.", "はい、お願いします。"),
    ])

    # ---------- 会話2：大陸を数える ----------
    scene(D, 'win_c2', [
        T("Let me look at your map. Kenya, Finland, Peru, and Hawaii.", "地図を見せてください。ケニア、フィンランド、ペルー、ハワイ。",
          "Yes. Those are my four dreams.", "はい。それがわたしの4つの夢です。"),
        T("Let's count the continents together. Asia is one, because you start in Japan.",
          "大陸をいっしょに数えましょう。アジアで1つ。日本から出発するからです。",
          "Oh, Japan counts too?", "えっ、日本も数えるのですか。"),
        T("Yes. Then Africa, Europe, South America, and North America. Hawaii is part of North America.",
          "はい。それからアフリカ、欧州、南米、北米。ハワイは北米に入ります。",
          "One, two, three, four, five. Five continents!", "1、2、3、4、5。5大陸！"),
        OT("Five is a lot. Do you want to keep all five?", "5つは多いですよ。5つとも残しますか。", [
            O('A', "Yes. I want all five.", "はい。5つとも行きたいです。", mt='ow', why="You said five continents.", cont=5),
            O('B', "Maybe I can cut one.", "1つ減らせるかもしれません。", cont=4)]),
        T("Then oneworld Explorer is strong.", "それなら oneworld Explorer が強いです。",
          "Far places cost the same. I like that.", "遠い場所でも同じ値段。いいですね。",
          by={'A': ("Then oneworld Explorer is strong. Distance does not matter, so far places cost the same.",
                    "それなら oneworld Explorer が強いです。距離は関係ないので、遠い場所でも値段は同じです。"),
              'B': ("Then the price goes down one step. We can check both ways.", "それなら値段が1段下がります。両方で見てみましょう。")},
          cueBy={'B': (star("Okay. Let's check both ways."), "はい。両方で見てみましょう。")}),
    ])

    # ---------- 会話5：南米 ----------
    scene(D, 'win_c5', [
        T("Now, South America. You chose Cusco and Machu Picchu.", "次は南米です。クスコとマチュピチュを選びましたね。",
          "Yes. I have wanted to go there for a long time.", "はい。ずっと前から行きたかった場所です。"),
        OT("A lovely dream. Is South America the star of your trip?", "すてきな夢ですね。南米は、この旅の主役ですか。", [
            O('A', "Yes. It is the main part.", "はい。いちばんの目的です。", mt='star', why="You said South America is the star of your trip."),
            O('B', "It is one of my four dreams.", "4つの夢のうちの1つです。")]),
        T("Then please listen carefully. oneworld has no home airline in South America.",
          "それなら、よく聞いてください。oneworld には、南米を拠点にする航空会社がありません。",
          "No home airline? Can I still go?", "拠点の航空会社がない？それでも行けますか。"),
        T("Yes. You can fly to Lima. But from Lima to Cusco, you buy another ticket.",
          "はい。リマまでは飛べます。でも、リマからクスコへは、別の切符を買います。",
          "Another ticket. So I pay more.", "別の切符。つまり、もっと払うのですね。"),
        T("With Star Alliance, Avianca can take you to Cusco. And one more thing: Machu Picchu needs a reservation.",
          "スターアライアンスなら、アビアンカ航空でクスコまで行けます。それからもう1つ。マチュピチュは予約が要ります。",
          "I'll book it early. I don't want to miss it.", "早めに予約します。見のがしたくないので。"),
    ])

    # ---------- 会話7：南の島とカナダ（Global Explorer は名前だけ） ----------
    scene(D, 'win_c7', [
        T("Do you like islands? Tahiti, for example.", "島は好きですか。たとえばタヒチ。",
          "I love the sea. Hawaii is on my map.", "海は大好きです。ハワイは地図にあります。"),
        T("Hawaii is easy. But Tahiti is different.", "ハワイは簡単です。でもタヒチは別です。",
          "Different? How?", "別？どうちがうのですか。"),
        T("Some flights use a partner's plane. oneworld Explorer cannot use those.",
          "仲間の会社の飛行機で飛ぶ便があります。oneworld Explorer では、それは使えません。",
          "So the same flight name, but a different plane?", "便の名前は同じでも、飛行機がちがうのですね。"),
        T("Exactly. For those islands, there is a third ticket: Global Explorer. It also works well in Canada.",
          "そのとおりです。そういう島のために、3つ目の券があります。Global Explorer です。カナダでも使いやすい券です。",
          "A third ticket! I didn't know that.", "3つ目の券！知りませんでした。"),
        OT("Do you want the far islands or Canada on this trip?", "この旅に、遠い島やカナダを入れたいですか。", [
            O('A', "No. Hawaii is enough for me.", "いいえ。ハワイで十分です。",
              rep=("Good. Hawaii is easy.", "よかった。ハワイは簡単です。")),
            O('B', "Yes. I want to go to Tahiti.", "はい。タヒチに行きたいです。", mt='star', why="You want to see Tahiti.", memo='Tahiti',
              rep=("Tahiti. I'll write it down for your next trip.", "タヒチ。次の旅のためにメモしておきます。")),
            O('C', "Yes. I want to travel across Canada.", "はい。カナダを横断したいです。", mt='star', why="You want to travel across Canada.", memo='Canada',
              rep=("Canada. I'll write it down for your next trip.", "カナダ。次の旅のためにメモしておきます。"))]),
    ])

    # ---------- 会話8：旅の長さ ----------
    scene(D, 'win_c8', [
        T("How long is your trip?", "旅はどのくらいの長さですか。",
          "About one month. Thirty days.", "約1か月。30日です。"),
        T("A month is good. With a very short trip, you are tired all the way.",
          "1か月はいいですね。とても短い旅だと、最後までずっと疲れたままです。",
          "I want to enjoy every city. So, one month.", "どの街も楽しみたいのです。だから1か月。"),
        T("Some people go around the world in five days.", "5日で世界を一周する人もいます。",
          "Five days? Is that possible?", "5日？そんなことができるのですか。"),
        T("With oneworld, yes. With Star Alliance business class, you need ten nights or more.",
          "oneworld ならできます。スターアライアンスのビジネスクラスは、10泊以上が必要です。",
          "Ten nights or more. That's an important rule.", "10泊以上。大事な決まりですね。"),
        OT("Is there any chance your trip gets shorter than ten days?", "旅が10日より短くなることは、ありそうですか。", [
            O('A', "No. I have one full month.", "いいえ。まる1か月あります。"),
            O('B', "Maybe. My work is busy.", "あるかもしれません。仕事が忙しいので。", mt='ow', why="You said your trip may be short.")]),
    ])

    # ---------- 地図とルール(089: win_route にルール説明を合体)。route=何本目の区間まで引くか(1〜16)、stp=寄港を何か所まで数えたか ----------
    # 区間: 1羽田→ナイロビ 2→ドーハ 3→ロヴァニエミ 4→アテネ 5→ローマ 6→チューリッヒ(鉄道) 7→フランクフルト(鉄道) 8→ロンドン(鉄道) 9→リスボン 10→ニューヨーク 11→ホノルル 12→シドニー 13→シンガポール 14→バンコク 15→グアム 16→羽田
    F = route_facts(); N = NUMW
    assert F['moves'] == 16 and F['rail'] == 3 and F['flights'] == 13 and F['stops'] == 15 and len(ROUTE_STOPS) == 15
    assert [c for c, _ in ROUTE_STOPS][:2] == ['Nairobi', 'Doha'] and ROUTE_RAIL[0] == ('Rome', 'Zurich')
    stops = [c for c, _ in ROUTE_STOPS]
    scene(D, 'win_route', [
        T("Round-the-world ticket rules!", "世界一周券のルールです！",
          "Rules! I'm ready.", "ルール！ いいですよ。"),
        T("Rule one: you go the same way, and you come home to Japan.", "ルール1：同じ向きに進んで、日本に帰ってきます。",
          "The same way, and home to Japan.", "同じ向きに進んで、日本に帰ります。"),
        T("Rule two: a flight is one move, and a train ride is one move.", "ルール2：飛行機は1回、鉄道も1回と数えます。",
          "A flight is one move. A train is one move, too.", "飛行機で1回。鉄道も1回。"),
        T("Let's draw your trip: west from Japan to Kenya.", "旅を地図に描きましょう。日本から西へ、ケニアへ。",
          "Move one.", "1回目。", route=1),
        T("Then Qatar, and Finland.", "次はカタールと、フィンランド。",
          "Move two. Move three.", "2回目。3回目。", route=3),
        T("Then Greece, and Italy.", "次はギリシャと、イタリア。",
          "Move four. Move five.", "4回目。5回目。", route=5),
        T("From Rome, we take three train rides: Zurich, Frankfurt, and London.", "ローマからは鉄道に3回乗ります。チューリッヒ、フランクフルト、ロンドン。",
          "Moves six, seven, and eight.", "6回目、7回目、8回目。", route=8),
        T("Then Portugal, and New York.", "次はポルトガルと、ニューヨーク。",
          "Move nine. Move ten.", "9回目。10回目。", route=10),
        T("Then Hawaii, and Australia.", "次はハワイと、オーストラリア。",
          "Move eleven. Move twelve.", "11回目。12回目。", route=12),
        T("Then Singapore, and Thailand.", "次はシンガポールと、タイ。",
          "Move thirteen. Move fourteen.", "13回目。14回目。", route=14),
        T("Then Guam, and home to Japan.", "次はグアム、そして日本へ。",
          "Move fifteen. Move sixteen.", "15回目。16回目。", route=16),
        T("That is %s flights and %s train rides: %s moves." % (N[F['flights']], N[F['rail']], N[F['moves']]), "飛行機が%d回、鉄道が%d回です。" % (F['flights'], F['rail']),
          "%s moves. That is the limit." % N[F['moves']].capitalize(), "移動は%d回。上限ぴったりです。" % F['moves']),
        T("Rule three: you can stop %s times at most." % N[RULE['stops']], "ルール3：寄港は%d回までです。" % RULE['stops'],
          "%s stops at most." % N[RULE['stops']].capitalize(), "寄港は%d回まで。" % RULE['stops']),
        T("A stop is a stay of twenty-four hours or more.", "寄港とは、24時間以上の滞在のことです。",
          "One day or more.", "1日以上ですね。"),
        T("Let's count your stops: %s." % ', '.join(stops[0:5]), "寄港を数えましょう。" + '、'.join(JPN[c] for c in stops[0:5]) + "。",
          "Five stops.", "5か所。", stp=5),
        T("%s." % ', '.join(stops[5:10]), '、'.join(JPN[c] for c in stops[5:10]) + "。",
          "Ten stops.", "10か所。", stp=10),
        T("%s." % ', '.join(stops[10:15]), '、'.join(JPN[c] for c in stops[10:15]) + "。",
          "%s stops!" % N[F['stops']].capitalize(), "%dか所！" % F['stops'], stp=15),
        T("%s stops is the limit, too." % N[F['stops']].capitalize(), "%d回。これも上限です。" % F['stops'],
          "Right on the limit!", "ぴったり！"),
        T("Rule four: you can visit the same country %s times at most." % N[RULE['same_country']],
          "ルール4：同じ国には%d回まで寄れます。" % RULE['same_country'],
          "%s times at most." % N[RULE['same_country']].capitalize(), "%d回まで。" % RULE['same_country']),
        T("You visit America %s times: %s, %s, and %s." % (N[F['max_same']], F['us'][0], F['us'][1], F['us'][2]),
          "アメリカには%d回。%s、%s、%s。" % (F['max_same'], JPN[F['us'][0]], JPN[F['us'][1]], JPN[F['us'][2]]),
          "%s times. That is the limit." % N[F['max_same']].capitalize(), "%d回。上限ぴったりです。" % F['max_same']),
        T("Rule five: the trip is ten days at least, and one year at most.", "ルール5：旅は10日以上、1年までです。",
          "Ten days to one year.", "10日から1年まで。"),
        T("Your thirty-day trip fits every rule!", "あなたの旅は30日。すべてルールに合っています！",
          "Everything fits. Thank you!", "すべて合っています。ありがとう！"),
    ], bg='rtmap', intro='Round-the-world ticket rules!')

    # ---------- 再訪の挨拶(089): 2回目に窓口へ来たとき。宣言・ルール・地図の説明は飛ばして、値段へ ----------
    scene(D, 'win_back', [
        T("Welcome back!", "おかえりなさい！", "Hello again.", "また来ました。"),
        T("Shall we finish your ticket?", "券の手続きを進めましょうか。", "Yes, please.", "はい、お願いします。"),
    ], intro='The Round the World desk.')

    # ---------- スターの決まり(088)。券のおすすめのあと・値段の前 ----------
    F = route_facts(); N = NUMW
    scene(D, 'win_rules', [
        T("Star Alliance has five simple rules. Rule one: you go the same way, and you come home to the country where you started.",
          "スターアライアンスの決まりは5つ。1つ目：同じ向きに進んで、出発した国に帰ってきます。",
          "The same way, and home to Japan.", "同じ向きに進んで、日本に帰ります。"),
        T("Rule two: you can stop in %s places at most. A stop is a stay of twenty-four hours or more." % N[RULE['stops']],
          "2つ目：寄港は%d回まで。寄港とは、24時間以上の滞在です。" % RULE['stops'],
          "%s stops at most." % N[RULE['stops']].capitalize(), "寄港は%d回までですね。" % RULE['stops']),
        T("Rule three: you can make %s moves at most. A flight is one move. A train ride is one move too." % N[RULE['moves']],
          "3つ目：移動は%d回まで。飛行機で1回。鉄道に乗るのも1回です。" % RULE['moves'],
          "%s moves. Trains count too." % N[RULE['moves']].capitalize(), "移動は%d回まで。鉄道も数えるのですね。" % RULE['moves']),
        T("Rule four: you can visit the same country %s times at most." % N[RULE['same_country']],
          "4つ目：同じ国には%d回まで寄れます。" % RULE['same_country'],
          "%s times for one country." % N[RULE['same_country']].capitalize(), "1つの国に%d回まで。" % RULE['same_country']),
        T("Rule five: the trip is ten days at least, and one year at most. Your trip is thirty days.",
          "5つ目：旅の長さは10日から1年まで。あなたの旅は30日です。",
          "Thirty days. That is fine.", "30日。大丈夫ですね。"),
    ], intro='The Round the World desk. Star Alliance rules.')

    # ---------- ルートを一緒に数える(088)。数字は route_facts() から ----------
    stops = [c for c, _ in ROUTE_STOPS]
    scene(D, 'win_count', [
        T("Let's check your route together. First, the stops. %s." % ', '.join(stops[0:5]),
          "あなたのルートをいっしょに確かめましょう。まず寄港地。" + '、'.join(JPN[c] for c in stops[0:5]) + "。",
          "That is five stops.", "5か所です。"),
        T("%s." % ', '.join(stops[5:10]), '、'.join(JPN[c] for c in stops[5:10]) + "。",
          "Five more. Ten stops.", "あと5か所。10か所です。"),
        T("%s." % ', '.join(stops[10:15]), '、'.join(JPN[c] for c in stops[10:15]) + "。",
          "Five more. %s stops!" % N[F['stops']].capitalize(), "あと5か所。%dか所！" % F['stops']),
        T("%s. That is the limit, and you are right on it. Now the moves. You have %s flights, and %s train rides: Rome to Zurich, Zurich to Frankfurt, and Frankfurt to London."
          % (N[F['stops']].capitalize(), N[F['flights']], N[F['rail']]),
          "%d回。ちょうど上限ですね。次は移動。飛行機が%d回、鉄道が%d回：ローマからチューリッヒ、チューリッヒからフランクフルト、フランクフルトからロンドン。" % (F['stops'], F['flights'], F['rail']),
          "%s flights and %s trains. %s moves." % (N[F['flights']].capitalize(), N[F['rail']], N[F['moves']].capitalize()),
          "飛行機%d回と鉄道%d回。移動は%d回です。" % (F['flights'], F['rail'], F['moves'])),
        T("%s. Right on the limit again. Now the countries. You visit the United States %s times: %s, %s, and %s."
          % (N[F['moves']].capitalize(), N[F['max_same']], F['us'][0], F['us'][1], F['us'][2]),
          "%d回。これもちょうど上限。次は国。アメリカには%d回寄ります。%s、%s、%s。" % (F['moves'], F['max_same'], JPN[F['us'][0]], JPN[F['us'][1]], JPN[F['us'][2]]),
          "%s times. That is the limit, too." % N[F['max_same']].capitalize(), "%d回。それも上限ですね。" % F['max_same']),
        T("Last, your trip goes west, one way, and home to Japan. It is thirty days. Everything fits the rules. It is a good route!",
          "最後に。旅は西へ、一方向に進んで、日本に帰ります。期間は30日。すべて決まりに合っています。いいルートです。",
          "Everything fits. Thank you!", "すべて合っています。ありがとう。"),
    ], intro='The Round the World desk. Your route.')

    # ---------- 値段（3通り。発券で使うのは star だけ。ow は2周目用に残す） ----------
    for key in ('star', 'ow5', 'ow4'):
        words, num, _ = PRICE[key]
        scene(D, 'win_price_' + key, [
            T("The ticket is %s yen." % words, "券は%s円です。" % num,
              (words[0].upper() + words[1:]) + " yen.", "%s円。" % num),
            T("Fuel and taxes are extra. Do you want to buy it?", "燃油と税は別です。買いますか。",
              "Okay. I'll take it.", "はい。これにします。"),
        ])

    # ---------- 読み上げ確認（004 の S3。3通り） ----------
    for key in ('star', 'ow5', 'ow4'):
        words, num, cont = PRICE[key]
        cont_jp = {'Five': '5', 'Four': '4'}[cont]
        scene(D, 'win_rb_' + key, [
            T("Please read the ticket back to me. We must be sure everything is right.",
              "券の控えを読み上げてください。すべて合っているか、確かめましょう。",
              readback(words, cont), readback_jp(num, cont_jp), diag='readback',
              rep=("Perfect. Everything is right.", "完璧です。すべて合っています。")),
        ], intro='The Round the World desk. Your ticket is ready.')

    # ---------- 名前の確認（003 フロー10の1往復） ----------
    scene(D, 'win_name', [
        T("Last check. Your name must match your passport, letter by letter. One wrong letter, and you cannot fly.",
          "最後の確認です。名前はパスポートと1文字ずつ同じでなければなりません。1文字でもちがうと、乗れません。",
          "Yes. Every letter is the same.", "はい。1文字ずつ同じです。",
          rep=("Good. Please go to the airline desk for your boarding pass.", "よろしい。搭乗券は、航空会社の窓口で受け取ってください。")),
    ])
