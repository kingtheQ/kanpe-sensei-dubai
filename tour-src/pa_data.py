# -*- coding: utf-8 -*-
# 世界一周編 1日目・最初の長距離便「CAアナウンス・イベント」の台本（タスク048）。指示書: 048-ca-announcement-event.md（PM案）。
# 流れ: 機内の会話(hnd_plane_*)のあと → CAに頼まれる(hnd_ev_ca_*) → マイクを渡される画面(pa.js) → 食事のあと、自分の声が機内放送で流れる(hnd_ev_meal_*)。
# 台詞（CAの頼み方・ルルの反応）は クロード執筆・PM確認待ち。画面に出す言葉は物語の中のものだけ（「録音」「テスト」「測定」などは出さない）。
# 券ごとの出し分け: _ow = oneworld（Qatar Airways・行き先 Doha） / _star = Star Alliance（Turkish Airlines・行き先 Istanbul）。
# 到着時刻: 指示書の「六時・evening」は、機内の既存場面（深夜便・「朝に着きます」）に合わせて「朝」にした（羽田を深夜に出る便。
#   物語の中の時刻で、実在の便の時刻ではない。作る直前に公式で確認する）。ow=ドーハに6時、star=イスタンブールに8時（どちらも現地の朝）。
import window_data as W

T, O, OT = W.T, W.O, W.OT

# アナウンス文（PM案）。マイク画面の「カンペ」は、この「意味のまとまり」ごとに区切って出す（1文=1行、まとまり=1かたまり）。
# 録音された声がそのまま機内放送になる。マイク画面の文と、放送のときに出す文は同じ。
VARIANTS = {
    'ow': dict(who='Qatar Airwaysの客室乗務員', bg='cabinQ', sp='qr_crew', dest='Doha', hour='six'),
    'star': dict(who='Turkish Airlinesの客室乗務員', bg='cabinT', sp='tk_crew', dest='Istanbul', hour='eight'),
}


def chunks(k):
    v = VARIANTS[k]
    return [
        ["Welcome aboard,", "everyone."],
        ["This is King,", "your guest announcer."],
        ["We are flying", "to %s." % v['dest']],
        ["We will arrive", "at %s o'clock" % v['hour'], "in the morning."],
        ["Please enjoy", "the flight."],
        ["Thank you!"],
    ]


def text(k):
    return ' '.join(' '.join(s) for s in chunks(k))


def add(D):
    def ev(id, who, bg, sp, intro, pairs, **kw):
        D.append(dict(id=id, who=who, bg=bg, sp=sp, intro=intro, pairs=pairs, words=[], ev=1, auto=1, kind='ev', **kw))

    for k, v in VARIANTS.items():
        # ---- CAに頼まれる。どれを選んでも、マイクを渡される（その先はマイク画面） ----
        ev('hnd_ev_ca_' + k, v['who'], v['bg'], v['sp'], 'ライトがうすくなった機内で、客室乗務員がもう一度、席に来た。', [
            OT("Excuse me, I am so sorry. My voice is not good tonight. Could you make the announcement for me?",
               "失礼します、すみません。今夜は声の調子がよくなくて。かわりに機内放送をしていただけませんか。", [
                O('yes', "Sure. I will do it.", "いいですよ。やります。",
                  rep=("Thank you so much! Here is the microphone. Please read this card.",
                       "ありがとうございます！マイクをどうぞ。このカードを読んでください。")),
                O('me', "Me? Okay, I will try!", "私が？いいですよ、やってみます！",
                  rep=("Wonderful! It is easy. Here is the microphone. Please read this card.",
                       "すばらしい！かんたんですよ。マイクをどうぞ。このカードを読んでください。")),
                O('again', "Sorry, could you say that again?", "すみません、もう一度言ってもらえますか。",
                  rep=("Of course. Could you make the announcement for me? Here is the microphone, and a card to read.",
                       "もちろん。かわりに放送をお願いできますか。マイクと、読むカードです。"))])],
            fx='ding')

        # ---- 食事のあと。チャイム → 自分の声の放送(pre='own'。pa.js) → ルルの反応 ----
        ev('hnd_ev_meal_' + k, 'Lulu', v['bg'], 'lulu', '', [
            T("King, listen! That is your voice! Everyone on the plane can hear you!",
              "キング、聞いて！いまのキングの声だよ！飛行機のみんなに聞こえてる！",
              "Really? I am so shy!", "ほんとに？はずかしい！"),
            T("You sound like a real captain. I am so proud of you!",
              "本物の機長みたいだったよ。わたし、ほこらしい！",
              "Thank you, Lulu. Now, let's eat!", "ありがとう、ルル。さあ、食べよう！")],
            pre='own')
