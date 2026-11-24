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

# ホテルのロビー・通常版(タスク066): 受付のスタッフがホテルを案内する場面(hub)。案内の3択 = ショータイム / プール / Balcony Bar。
# 選択肢と案内の一言は英文だけ(日本語は足さない)。ショータイム → プールサイドの歌場面(nbo_song)。プール・Balcony Bar は、スタッフの一言を読み上げて、選択にもどる(場面は増やさない)。
# 実在: Villa Rosa Kempinski(入国審査の会話 nbo_immig2 と同じホテル)。個人名・値段・営業時間など確かめていない事実は入れない。
LOBBY_HUB = {
    'en': 'Welcome to the Villa Rosa Kempinski. What would you like to see?',
    'msg': 'ホテルのロビー。受付のスタッフが、ホテルを案内してくれる。',
    'menu': [['See the evening show', 'nbo_show'], ['The swimming pool', 'nbo_pool'], ['The Balcony Bar', 'nbo_bbar']],
    'lines': {
        'nbo_pool': 'The pool is just outside. It is so beautiful at night.',
        'nbo_bbar': 'The Balcony Bar has a lovely view. Please enjoy your evening.',
    },
}
