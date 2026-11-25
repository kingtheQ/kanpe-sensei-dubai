# -*- coding: utf-8 -*-
# 世界一周編 ナイロビの滞在(観光): サファリ・マサイマーケット(タスク058。クロが執筆)。国ごとのデータは別ファイル(ドーハ・羽田と同じ形)。
# 実在名: Nairobi National Park / Maasai Market。値段は架空。個人名なし。
# 会話の型(タスク057 第1弾で新しい流れ=061 の flow2 に統一): 選ぶのは1場面に1回だけ。
#   053 では分かれ目(英語の返事を2〜3個から選ぶ)が2か所あったが、「行為の選択」に近い方の1か所だけを日本語の短い単語カード(cards=1)に作り替え、
#   もう1か所は固定文のターン(本線の返事をカンペで読んで声に出す。相手の反応 rep はそのまま)に戻した。
#   カード → 見本の英語が音声だけ → カンペ(文字) → 声に出す → 間違えたら自動おてほん(074の統一ルール) → 相手の反応(rep)。画面に出るのは英語だけ
#   (日本語 njp / jp / yjp / rep の2つ目は保存と台本の確認用。選択カードの日本語単語だけは画面に出す)。点数・○×は出さない。
#   fork={'tw':[語]} = カードを出してからタップするまでの時間を裏で測る語(語ごとの記録・持ち越し・夢は 053 のしくみのまま。061 の forkNote/noteWord)。
# 場面の置き場所: サファリ nbo_safari(滞在3日の4日目=★の山)、マサイマーケット nbo_market(3日目)。配置は trip.js の ROWS / GROUPS。
import window_data as W
from window_data import star, O, OT, T


def add(D):
    D.append(dict(
        id='nbo_safari', who='サファリのガイド', bg='safariK', sp='safari_guide',
        intro='ナイロビ国立公園。ガイドといっしょに、動物を見に行こう。',
        pairs=[
            ("Jambo, my friends! Welcome to Nairobi National Park. Can you see the city behind us?",
             "ジャンボ、みなさん！ナイロビ国立公園へようこそ。うしろに街が見えますか。",
             star("Yes! A city and wild animals. It is amazing."), "はい！街と野生の動物。すごいですね。"),
            T("It is special, yes. Now look at the tall tree. Can you see the giraffe? It is very tall.",
              "そうなんです、特別でしょう。あの高い木を見て。キリンが見えますか。とても背が高いですよ。",
              "Yes! I see the giraffe. It is so tall!", "はい！キリンが見えます。とても高い！",
              rep=("Yes! Its neck is almost two meters long. It eats leaves from the top of the tree.",
                   "そう！首は2メートル近くあります。木のてっぺんの葉を食べるんですよ。")),
            ("Good eyes! Now look at the road. The zebra is walking slowly. Every zebra has different stripes.",
             "いい目ですね！次は道を見て。シマウマがゆっくり歩いています。シマウマはみんな、しまの模様がちがうんです。",
             star("Really? Every zebra is different?"), "本当ですか。どのシマウマもちがうんですか。"),
            OT("Yes, like your fingerprints! And over there, do you see the rhino? It is very rare. Please speak quietly.",
               "そう、指紋みたいに！そして向こう、サイが見えますか。とても珍しいんです。静かに話してくださいね。", [
                O('photo', "Wow, a rhino! Can I take a picture?", "わあ、サイだ！写真を撮ってもいいですか。", card='写真', ico='📷',
                  rep=("Yes, please! But no flash, and stay close to me.",
                       "ええ、どうぞ！ただしフラッシュはなしで、わたしのそばにいてくださいね。")),
                O('quiet', "I see the rhino. I will be very quiet.", "サイが見えます。とても静かにしますね。", card='静かに見る', ico='🤫',
                  rep=("Good. The rhino cannot see well, but it hears very well.",
                       "いいですね。サイは目があまりよくありませんが、耳はとてもいいんです。"))],
               cards=1, fork={'tw': ['rhino']}),
            ("That is our safari! The lion sleeps most of the day, and the ostrich runs very fast. Did you enjoy it?",
             "これでサファリはおしまい！ライオンは1日のほとんどを寝て過ごし、ダチョウはとても速く走ります。楽しめましたか。",
             star("Yes, it was wonderful. Asante sana!"), "はい、すばらしかったです。どうもありがとう！"),
        ],
        words=[("giraffe", "キリン"), ("zebra", "シマウマ"), ("rhino", "サイ"), ("lion", "ライオン"), ("ostrich", "ダチョウ")],
        conv=1, flow2=1))

    D.append(dict(
        id='nbo_market', who='マーケットの店の人', bg='marketK', sp='market_vendor',
        intro='マサイマーケット。布やかごのお店がならんでいる。',
        pairs=[
            ("Jambo, my friends! Welcome to the Maasai Market. Please, look around.",
             "ジャンボ、みなさん！マサイマーケットへようこそ。どうぞ見ていってください。",
             star("Thank you. Everything is so colorful."), "ありがとう。どれもとてもカラフルですね。"),
            T("Look at this cloth. It is from Kenya. Do you like the red one, or the blue one?",
              "この布を見て。ケニアのものです。赤いのが好きですか、それとも青いの？",
              "I like the red cloth.", "赤い布が好きです。",
              rep=("Good choice! Red is very popular here.", "いい選択！赤はここでとても人気があるんですよ。")),
            ("And look at this basket and this mask. Our family made them by hand.",
             "それから、このかごとこのお面も見て。うちの家族が手で作ったんです。",
             star("They are beautiful. How much is the basket?"), "きれいですね。かごはいくらですか。"),
            OT("For you, my friend, a good price. Two thousand shillings.",
               "あなたには、いい値段で。2000シリングです。", [
                O('cheaper', "That is a little expensive. Can you make it cheaper?", "ちょっと高いですね。もう少し安くなりますか。", card='値切る', ico='🪙',
                  rep=("Ah, you are smart! Okay, okay. One thousand five hundred shillings. Only for you.",
                       "おお、お上手ですね！わかりました。1500シリング。あなただけですよ。")),
                O('take', "That is a good price. I will take it.", "いい値段ですね。買います。", card='買う', ico='🧺',
                  rep=("Wonderful! You are kind, so I make it one thousand five hundred shillings.",
                       "すばらしい！やさしい方だから、1500シリングにしますね。"))],
               cards=1, fork={'tw': ['price']}),
            ("Here is your basket, wrapped in paper. Asante sana! Come back soon.",
             "かごです、紙でつつみました。ありがとう！また来てくださいね。",
             star("Thank you! I love the Maasai Market."), "ありがとう！マサイマーケットが大好きです。"),
        ],
        words=[("cloth", "布"), ("mask", "お面"), ("basket", "かご"), ("price", "値段"), ("cheaper", "もっと安い")],
        conv=1, flow2=1))
