# -*- coding: utf-8 -*-
# 世界一周編 ナイロビの英会話カフェ(タスク068・試作。クロが執筆)。国ごとのデータは別ファイル(stay_data と同じ形)。
# 先生(キング制作の新キャラ)と、小さなカフェで短い予行練習: ごあいさつ → 飲み物の注文 → ひとこと雑談。型どおりの会話。
# タスク073: 5往復のあとに、先生が英語で5分の自由会話に誘う(freetalk=1。しくみは freetalk.js・relay/worker.js の POST /chat)。台本パートはそのまま。
# 決まり:
#   ・日本語訳は付けない。画面にも台本にも日本語を置かない(njp / yjp は空)。画面に「勉強・テスト・測定・復習」の言葉は出さない。
#   ・実在の店名・メニュー名などの固有名詞は出さない(場所はナイロビのみ)。個人名もなし。値段もなし。
#   ・流れは既存の会話場面と同じ: 先生の英語を聞く → カンペを見て自分の番を発音する(発音採点は既存のしくみ)。5往復=従来の長さ。
#   ・conv=1: Word Battle / Meaning!(日本語で答え合わせ)を出さない。words は空(日本語の意味を持たないので、ほかの場面の答え合わせの選択肢にも混ざらない)。
#   ・本編の進行・セーブには入れない(チェックモードからだけ。build.py の EIKAI / TOUR_IDS に入れない)。
from window_data import star


def add(D):
    D.append(dict(
        id='nbo_eikaiwa1', who='英会話カフェの先生', bg='eikaiK', sp='eikai_teacher',
        intro='ナイロビの小さな英会話カフェ。ピンクのアフロの先生が、奥の席で待っている。',
        pairs=[
            ("Hello! Welcome to our little English café. Please, take a seat.", "",
             star("Hello! Nice to meet you."), ""),
            ("Nice to meet you, too! What would you like to drink?", "",
             star("I would like a cup of tea, please."), ""),
            ("Of course. Would you like some milk in it?", "",
             star("Yes, a little milk, please."), ""),
            ("Here you are, with a little milk. Is this your first time in Nairobi?", "",
             star("Yes. It is our first time."), ""),
            ("Lovely! Enjoy your tea, and enjoy Kenya.", "",
             star("Thank you. See you again!"), ""),
        ],
        words=[],
        conv=1,
        freetalk=1))   # タスク073: 台本パートのあと、先生が5分の自由会話に誘う(音声認識のあるブラウザ・こえをださないモードでないときだけ)
