# -*- coding: utf-8 -*-
# 宣言文ソングの組み込み(タスク049)。ナイロビのホテルロビーの「聴く」イベントの会話文(クロが執筆)。
# 発音の課題・言い直し・採点・単語バトルはない(聴くだけ)。英文は短く、歌の余韻をこわさない長さ。
# 実在名: Villa Rosa Kempinski(入国審査の会話 nbo_immig2 と同じホテル)。個人名なし。歌詞(宣言文)は引用しない。
# 画面に出る日本語は、場面の入り(intro)だけ(ほかの場面と同じ)。会話文は英語だけ。
SONG_SCENE = {
    'id': 'nbo_song',
    'who': 'ラウンジの歌手',
    'bg': 'npool',   # タスク066: ショータイムはロビーの真ん中ではなく、別場面のプールサイド(背景 nairobi-pool-v2.png)で歌う。060のロビー版(nsong)は使わない(絵と設定は残す)
    'sp': 'singer',
    'intro': '夜のプールサイド。水辺の小さな台のまわりに、人が集まっている。ふたりも、その輪に加わった。',
    # タスク060: 歌を始める前の、ルルが歌手に気づく一言(英語だけ。日本語訳は出さない。読み上げ+表示。マイクなし)
    'notice': {'who': 'ルル', 'en': 'Look, King! Someone is going to sing.'},
    # 曲が終わったあとの短いやりとり(読み上げ+表示。マイクは使わない)。w = 話す人(singer / lulu / king)
    # タスク066: 曲(song-theme.mp3 / 74.6秒)の拍の時刻(秒)。曲の音から検出した拍(132個・間隔 0.42〜0.85秒)。プールサイドの照明ストリップ・歌手の絵の切りかえを、曲の再生位置に同期させる
    'beats': [0.16,0.74,1.3,1.88,2.43,3.01,3.57,4.03,4.71,5.27,5.73,6.41,6.98,7.54,8.12,8.68,9.12,9.82,10.36,10.94,11.49,12.09,12.63,13.21,13.77,14.33,14.91,15.48,15.9,16.32,16.88,17.44,18.04,18.58,19.14,19.72,20.17,20.85,21.41,21.97,22.53,23.11,23.55,24.23,24.68,25.38,25.92,26.5,27.06,27.62,28.06,28.75,29.21,29.89,30.35,30.99,31.59,32.15,32.71,33.28,33.74,34.42,34.98,35.54,36.1,36.68,37.24,38.09,38.65,39.23,39.65,40.07,40.51,41.19,41.77,42.34,42.9,43.48,44.04,44.58,45.04,45.72,46.16,46.85,47.41,47.99,48.43,49.11,49.67,50.11,50.53,51.1,51.66,52.22,52.78,53.36,53.92,54.48,55.04,55.61,56.15,56.73,57.29,57.85,58.43,58.99,59.55,60.12,60.68,61.24,61.8,62.38,62.92,63.38,64.06,64.63,65.19,65.77,66.31,66.89,67.45,68.01,68.58,69.14,69.7,70.26,70.82,71.38,71.94,72.5,73.07,73.51],
    # タスク076: 歌い始めの呼びかけ(歌手の台詞。英語・短い。読み上げ+表示。読み終わってから曲が始まる)
    'call': {'who': 'ラウンジの歌手', 'en': 'Come on, everybody \u2014 sing with me!'},
    # タスク076: 歌詞(行単位・曲の再生位置 currentTime に連動して画面下のメッセージ欄に1行ずつ表示。英語のみ・単語カラオケなし)。[開始秒, 行]
    # 歌詞の正本は files/song/declaration-song-suno.md パターン1(旅立ちポップ)の21行。時刻は【初版の近似】(曲 74.6秒に、節のまとまりで配分しただけ)。
    # 実曲(song-theme.mp3)がこのテキストどおりに歌っているかは未検証 → キングが実機で聞いて調整する前提。直すのはこの表の秒だけ(拍表 beats と同じ流儀)。
    'lyrics': [
        [4.0, 'Pack my bag, the sky is blue'],            # Verse
        [8.0, 'Every airport waits for you'],
        [12.0, 'Step by step, and mile by mile'],
        [16.0, 'I will say it with a smile'],
        [20.0, 'This is my promise, Lulu'],               # Chorus
        [23.5, 'We will travel around the world together'],
        [28.0, 'And have fun every day'],
        [31.5, 'My body is healthy, my mind is calm'],
        [35.0, 'I eat good food, sleep well'],
        [38.5, 'And never push too hard'],
        [42.0, 'When I feel afraid'],
        [45.0, 'I breathe and think of you'],
        [48.5, 'We both help each other'],
        [52.0, "Let's see every village"],                # Bridge
        [55.0, 'Hear every voice'],
        [58.0, 'Share every little treasure'],
        [61.0, 'Thank you for being here'],
        [64.0, 'This is my promise, Lulu'],               # Final Chorus
        [67.0, 'We will travel around the world together'],
        [70.0, 'And have fun every day'],
        [72.5, "Let's go, let's go!"],
    ],
    'after': [
        {'w': 'singer', 'who': 'ラウンジの歌手', 'en': 'Thank you for listening. Karibu Nairobi. Welcome!'},
        {'w': 'lulu',   'who': 'ルル',           'en': 'That was beautiful. I could listen all night.'},
        {'w': 'king',   'who': 'キング',         'en': 'Asante! It was a wonderful song.'},
        {'w': 'singer', 'who': 'ラウンジの歌手', 'en': 'Asante sana. Sleep well, and enjoy Nairobi.'},
    ],
}

# ホテルの部屋(タスク051): 到着の夜、部屋で休む場面 nbo_room(クロが執筆)。049のホテルロビー(Villa Rosa Kempinski)と同じホテル。
# 読み上げ+表示だけ(発音の課題・言い直し・採点・マイク・単語バトルはない)。英文は短く、夜の静けさに合う長さ。個人名なし。
# 画面に出る日本語は、場面の入り(intro)だけ(ほかの場面と同じ)。w = 話す人(lulu / king)
ROOM_SCENE = {
    'id': 'nbo_room',
    'who': 'ホテルの部屋',
    'bg': 'nroom',
    'sp': 'lulu',
    'intro': '夜のホテルの部屋。長い一日がおわった。ふたりは、ほっと息をついた。',
    'lines': [
        {'w': 'lulu', 'who': 'ルル',   'en': 'We made it. This is our room at the Villa Rosa Kempinski.'},
        {'w': 'king', 'who': 'キング', 'en': 'It is so quiet. Look at the moon.'},
        {'w': 'lulu', 'who': 'ルル',   'en': 'Nairobi is beautiful at night.'},
        {'w': 'king', 'who': 'キング', 'en': 'My blue suitcase is here. I am so tired.'},
        {'w': 'lulu', 'who': 'ルル',   'en': 'Rest well, King. Tomorrow is a new day.'},
        {'w': 'king', 'who': 'キング', 'en': 'Lala salama, Lulu.'},
    ],
}

# ホテルのロビー・通常版(タスク066/077): 受付のスタッフがホテルを案内する場面(hub)。案内の3択 = ショータイム / プール / Balcony Bar。
# 選択肢と案内の一言は英文だけ(日本語は足さない)。ショータイム → プールサイドの歌場面(nbo_song)。
# タスク077: プール → 実在の場面 nbo_pool1(下の POOL_SCENE。聞くだけ型)。Balcony Bar → 場面 nbo_bar1(下の BAR_SCENE)。タスク077b で素材を結び、実在の行き先として有効(BAR_READY=True)。
#   BAR_READY が False のときだけ、バーを選ぶとスタッフの一言(下の lines['nbo_bbar'] = 仮置き)を言ってメニューに戻る(壊れた場面には遷移しない)。いまは True なので場面 nbo_bar1 へ行く。
# 実在: Villa Rosa Kempinski(入国審査の会話 nbo_immig2 と同じホテル)。個人名・値段・営業時間など確かめていない事実は入れない。
#
# ★★ バーを有効にする切り替えは、この1か所だけ ★★
#    背景 nairobi-balcony-bar-v1.png・別ストリップ2点・バーテンダー(tk-bartender)を結び、art.js の ART.nbar を確定した(タスク077b)ので True。
BAR_READY = True

LOBBY_HUB = {
    'en': 'Welcome to the Villa Rosa Kempinski. What would you like to see?',
    'msg': 'ホテルのロビー。受付のスタッフが、ホテルを案内してくれる。',
    'menu': [['See the evening show', 'nbo_show'], ['The swimming pool', 'nbo_pool'], ['The Balcony Bar', 'nbo_bbar']],
    'lines': {
        # プールは場面ができたので、一言は不要(場面の入りから始まる)。
        # バー: 【素材待ちの仮置き】BAR_READY が True になるまでの間だけ使う一言(True になると場面 nbo_bar1 へ行き、この一言は使わない)
        'nbo_bbar': 'The Balcony Bar has a lovely view. Please enjoy your evening.',
    },
}

# プールの場面(タスク077): 静かな夜のプールサイド nbo_pool1(聞くだけ型。nbo_room と同じ流儀。マイク・発音採点・単語バトルなし・新しい保存キーなし)。
# 絵は art.js の npoolq(背景 nairobi-pool-v2.png+既存の2ストリップ。歌手と観客は置かず、ルルとキングだけ)。画面に出る日本語は入りの1行(intro)だけ。w = 話す人(lulu / king)
POOL_SCENE = {
    'id': 'nbo_pool1',
    'who': 'ホテルのプール',
    'bg': 'npoolq',
    'sp': None,
    'intro': '夜のプールサイド。ショーのない時間は静かで、水が光っている。',
    'lines': [
        {'w': 'lulu', 'who': 'ルル',   'en': 'Look at the water. It is so quiet now.'},
        {'w': 'king', 'who': 'キング', 'en': 'The pool looks beautiful at night.'},
        {'w': 'lulu', 'who': 'ルル',   'en': "Let's sit here for a while."},
        {'w': 'king', 'who': 'キング', 'en': 'Good idea. What a long day.'},
    ],
}

# バルコニーバルの場面(タスク077で枠組み・077bで素材を結んで有効化): nbo_bar1。背景 nairobi-balcony-bar-v1.png(1536×960・人なし)。
# 台本は077で確定したまま(077bでは変更しない)。値段は入れない・ジュース類・営業時間など未確認の事実は書かない。
BAR_SCENE = {
    'id': 'nbo_bar1',
    'who': 'バルコニーバル',
    'bg': 'nbar',
    'sp': None,
    'intro': 'ホテルのバルコニーバル。街の明かりが見える。',
    'lines': [
        {'w': 'bartender', 'who': 'バーテンダー', 'en': 'Good evening. What can I get you?'},
        {'w': 'king',       'who': 'キング',       'en': 'A mango juice, please.'},
        {'w': 'bartender',  'who': 'バーテンダー', 'en': 'Here you are. Enjoy the view.'},
        {'w': 'lulu',       'who': 'ルル',         'en': 'Look at the city lights, King.'},
        {'w': 'king',       'who': 'キング',       'en': 'Thank you. What a beautiful night.'},
    ],
}
