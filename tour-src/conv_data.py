# -*- coding: utf-8 -*-
# 世界一周編 夢の台本(タスク053 手順1)。設計の正本: docs/pm/deliverables/015(案2＋夢)・053指示書。
# 夢は「寝る場面(夜の1枚のあと)」に出る。持ち越し(save.missed)の語(上位5語まで)が、夢の中の会話に自然に出てくる。
#   - 夢の中も3択にしない。相手の一言に語が入り、プレイヤーは声で返す(カンペの発音チェック)。
#   - 自然に通じたら(7割以上で、その語が言えていたら)持ち越しから外れる。通じなかった語は残る(会話は止めない)。
#   - 夢の語り手は 達人賢者(夢の中の「雲のカフェ」の主人)。画面に点数・○×・「復習」「テスト」の言葉は出さない。
# 語(キー)は小文字。変換した場面の語を増やすたびに、ここへその語の夢の一言を足す(足りない語は夢の外の一般の一言で出す)。
# 台本は (相手の一言, 日本語(保存だけ・画面に出さない), プレイヤーの返事(声に出す), 日本語(保存だけ))
DREAM = {
    # Java House (nbo_java1)
    'latte': ("Welcome to the Cloud Café. What can I make for you?", "雲のカフェへようこそ。何をお作りしましょう。",
              "A latte, please.", "ラテをお願いします。"),
    'iced': ("It is a warm night on the moon. Would you like it iced?", "月の夜はあたたかいね。氷入りにしますか。",
             "Yes, iced, please.", "はい、アイスでお願いします。"),
    'slice': ("The star oven just finished. Would you like a slice?", "星のオーブンが焼きあがったよ。ひと切れどう？",
              "Yes, a slice, please.", "はい、ひと切れお願いします。"),
    'carrot cake': ("Tonight we have moon cheese and carrot cake. Which one?", "今夜は、月のチーズとキャロットケーキがあるよ。どっち？",
                    "Carrot cake, please.", "キャロットケーキをお願いします。"),
    'shillings': ("That is eight hundred shillings. Or one good dream.", "800シリング。それか、いい夢をひとつ。",
                  "Here are eight hundred shillings.", "800シリングです、どうぞ。"),
    # サファリ (nbo_safari) とマサイマーケット (nbo_market)(タスク058)
    'giraffe': ("A very tall guest is drinking tea on the cloud. Can you see the giraffe?", "とても背の高いお客さんが、雲の上でお茶を飲んでいるよ。キリンが見えるかな。",
                "Yes, I see the giraffe.", "はい、キリンが見えます。"),
    'zebra': ("The zebra is crossing the cloud road. Every stripe is different.", "シマウマが雲の道をわたっているよ。しまは、ぜんぶちがうんだ。",
              "I see the zebra.", "シマウマが見えます。"),
    'rhino': ("Shh. A rhino is sleeping on the moon. Please speak quietly.", "しーっ。サイが月の上で眠っているよ。静かに話してね。",
              "I see the rhino. I will be quiet.", "サイが見えます。静かにしますね。"),
    'lion': ("A lion is sleeping under the star tree. He sleeps all day.", "ライオンが星の木の下で眠っているよ。1日じゅう寝ているんだ。",
             "I see the lion.", "ライオンが見えます。"),
    'ostrich': ("Look! The ostrich is running across the sky. It is very fast.", "見て！ダチョウが空を走っているよ。とても速いね。",
                "The ostrich is so fast!", "ダチョウはとても速い！"),
    'cloth': ("Welcome to the Cloud Market. Do you like this cloth?", "雲のマーケットへようこそ。この布は気に入った？",
              "Yes, I like the cloth.", "はい、この布が好きです。"),
    'mask': ("This mask is smiling at you. Can you see it?", "このお面、きみに笑いかけているよ。見えるかな。",
             "Yes, I see the mask.", "はい、お面が見えます。"),
    'basket': ("A basket full of stars. Would you like one?", "星がいっぱいのかごだよ。ひとつどう？",
               "Yes, a basket, please.", "はい、かごをください。"),
    'price': ("The price tonight is one good dream.", "今夜の値段は、いい夢をひとつ。",
              "That is a good price.", "いい値段ですね。"),
    'cheaper': ("Cheaper? Tonight the stars are free.", "もっと安く？今夜は星はただだよ。",
                "Can you make it cheaper?", "もう少し安くなりますか。"),
}
# 台本のない語(まだ夢の台本を書いていない語)用のひとこと
FALLBACK = ("A word is floating by. Can you catch it?", "ひとつ、ことばがふわふわ浮いているよ。つかまえられる？")
