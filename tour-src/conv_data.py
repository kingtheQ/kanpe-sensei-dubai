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
}
# 台本のない語(まだ夢の台本を書いていない語)用のひとこと
FALLBACK = ("A word is floating by. Can you catch it?", "ひとつ、ことばがふわふわ浮いているよ。つかまえられる？")
