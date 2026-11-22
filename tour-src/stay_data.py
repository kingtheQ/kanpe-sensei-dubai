# -*- coding: utf-8 -*-
# 世界一周編 ナイロビの滞在(観光): サファリ・マサイマーケット(タスク058。クロが執筆)。国ごとのデータは別ファイル(ドーハ・羽田と同じ形)。
# 実在名: Nairobi National Park / Maasai Market。値段は架空。個人名なし。
# 会話の型は 053 の「分かれ目」: 相手の一言に今日の語が入り、プレイヤーは▶で英語の返事を2〜3個から選んで声に出す。
#   ok=1 の返事 = 聞き取れた人が選ぶ返事。ok なし = 聞き違えた人が選ぶ返事(相手が言い直してくれる)。どれを選んでも物語は進む(止めない・合否なし)。
#   画面に出るのは英語だけ。日本語(njp / jp / yjp / rep の2つ目)は保存と台本の確認用で、画面には出さない。選択肢の点数・○×も出さない。
#   fork={'tw':[語]} = その分かれ目で、選ぶまでの時間を裏で測る語(語ごとの記録・持ち越し・夢は 053 のしくみのまま)。
# 場面の置き場所: サファリ nbo_safari(滞在3日の4日目=★の山)、マサイマーケット nbo_market(3日目)。配置は trip.js の ROWS / GROUPS。
import window_data as W
from window_data import star, O, OT


def add(D):
    D.append(dict(
        id='nbo_safari', who='サファリのガイド', bg='safariK', sp='safari_guide',
        intro='ナイロビ国立公園。ガイドといっしょに、動物を見に行こう。',
        pairs=[
            ("Jambo, my friends! Welcome to Nairobi National Park. Can you see the city behind us?",
             "ジャンボ、みなさん！ナイロビ国立公園へようこそ。うしろに街が見えますか。",
             star("Yes! A city and wild animals. It is amazing."), "はい！街と野生の動物。すごいですね。"),
            OT("It is special, yes. Now look at the tall tree. Can you see the giraffe? It is very tall.",
               "そうなんです、特別でしょう。あの高い木を見て。キリンが見えますか。とても背が高いですよ。", [
                O('see', "Yes! I see the giraffe. It is so tall!", "はい！キリンが見えます。とても高い！", ok=1,
                  rep=("Yes! Its neck is almost two meters long. It eats leaves from the top of the tree.",
                       "そう！首は2メートル近くあります。木のてっぺんの葉を食べるんですよ。")),
                O('graph', "A graph? I do not see a graph.", "グラフ？グラフは見えません。",
                  rep=("A graph? Ha ha! No, no. A giraffe! The tall animal with the long neck.",
                       "グラフ？あはは！いえいえ、キリンです！首の長い、背の高い動物。")),
                O('closer', "Yes, I see it. Can we go closer?", "はい、見えます。もっと近くへ行けますか。", ok=1,
                  rep=("Not too close, my friend. Giraffes are shy. But your camera can go closer.",
                       "近づきすぎはだめですよ。キリンは恥ずかしがりやです。でもカメラなら近くまで寄れます。"))],
               fork={'tw': ['giraffe']}),
            ("Good eyes! Now look at the road. The zebra is walking slowly. Every zebra has different stripes.",
             "いい目ですね！次は道を見て。シマウマがゆっくり歩いています。シマウマはみんな、しまの模様がちがうんです。",
             star("Really? Every zebra is different?"), "本当ですか。どのシマウマもちがうんですか。"),
            OT("Yes, like your fingerprints! And over there, do you see the rhino? It is very rare. Please speak quietly.",
               "そう、指紋みたいに！そして向こう、サイが見えますか。とても珍しいんです。静かに話してくださいね。", [
                O('lion', "A lion? Is it dangerous?", "ライオン？危ないですか。",
                  rep=("No, no! A rhino, not a lion. R, H, I, N, O. The gray one with the horn.",
                       "いえいえ！ライオンではなくサイです。R・H・I・N・O。つのがある、灰色の動物。")),
                O('see', "I see the rhino. I will be very quiet.", "サイが見えます。とても静かにしますね。", ok=1,
                  rep=("Good. The rhino cannot see well, but it hears very well.",
                       "いいですね。サイは目があまりよくありませんが、耳はとてもいいんです。")),
                O('photo', "Wow, a rhino! Can I take a picture?", "わあ、サイだ！写真を撮ってもいいですか。", ok=1,
                  rep=("Yes, please! But no flash, and stay close to me.",
                       "ええ、どうぞ！ただしフラッシュはなしで、わたしのそばにいてくださいね。"))],
               fork={'tw': ['rhino']}),
            ("That is our safari! The lion sleeps most of the day, and the ostrich runs very fast. Did you enjoy it?",
             "これでサファリはおしまい！ライオンは1日のほとんどを寝て過ごし、ダチョウはとても速く走ります。楽しめましたか。",
             star("Yes, it was wonderful. Asante sana!"), "はい、すばらしかったです。どうもありがとう！"),
        ],
        words=[("giraffe", "キリン"), ("zebra", "シマウマ"), ("rhino", "サイ"), ("lion", "ライオン"), ("ostrich", "ダチョウ")],
        conv=1))

    D.append(dict(
        id='nbo_market', who='マーケットの店の人', bg='marketK', sp='market_vendor',
        intro='マサイマーケット。布やかごのお店がならんでいる。',
        pairs=[
            ("Jambo, my friends! Welcome to the Maasai Market. Please, look around.",
             "ジャンボ、みなさん！マサイマーケットへようこそ。どうぞ見ていってください。",
             star("Thank you. Everything is so colorful."), "ありがとう。どれもとてもカラフルですね。"),
            OT("Look at this cloth. It is from Kenya. Do you like the red one, or the blue one?",
               "この布を見て。ケニアのものです。赤いのが好きですか、それとも青いの？", [
                O('red', "I like the red cloth.", "赤い布が好きです。", ok=1,
                  rep=("Good choice! Red is very popular here.", "いい選択！赤はここでとても人気があるんですよ。")),
                O('clock', "A clock? I like the clock.", "時計？時計が好きです。",
                  rep=("A clock? Ha ha! No, a cloth. You can use it as a scarf.",
                       "時計？あはは！いえ、布です。スカーフとして使えますよ。")),
                O('blue', "The blue one, please. May I touch it?", "青いのをください。さわってもいいですか。", ok=1,
                  rep=("Of course! Feel it. It is very soft.", "もちろん！さわってみて。とてもやわらかいですよ。"))],
               fork={'tw': ['cloth']}),
            ("And look at this basket and this mask. Our family made them by hand.",
             "それから、このかごとこのお面も見て。うちの家族が手で作ったんです。",
             star("They are beautiful. How much is the basket?"), "きれいですね。かごはいくらですか。"),
            OT("For you, my friend, a good price. Two thousand shillings.",
               "あなたには、いい値段で。2000シリングです。", [
                O('cheaper', "That is a little expensive. Can you make it cheaper?", "ちょっと高いですね。もう少し安くなりますか。", ok=1,
                  rep=("Ah, you are smart! Okay, okay. One thousand five hundred shillings. Only for you.",
                       "おお、お上手ですね！わかりました。1500シリング。あなただけですよ。")),
                O('prize', "A prize? Did I win a prize?", "賞品？賞品が当たったんですか。",
                  rep=("A prize? Ha ha! No, a price. Two thousand shillings. But for you, one thousand five hundred.",
                       "賞品？あはは！いえ、値段です。2000シリング。でもあなたには1500シリングにしますよ。")),
                O('take', "That is a good price. I will take it.", "いい値段ですね。買います。", ok=1,
                  rep=("Wonderful! You are kind, so I make it one thousand five hundred shillings.",
                       "すばらしい！やさしい方だから、1500シリングにしますね。"))],
               fork={'tw': ['price']}),
            ("Here is your basket, wrapped in paper. Asante sana! Come back soon.",
             "かごです、紙でつつみました。ありがとう！また来てくださいね。",
             star("Thank you! I love the Maasai Market."), "ありがとう！マサイマーケットが大好きです。"),
        ],
        words=[("cloth", "布"), ("mask", "お面"), ("basket", "かご"), ("price", "値段"), ("cheaper", "もっと安い")],
        conv=1))
