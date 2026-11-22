# -*- coding: utf-8 -*-
# 宣言文ソングの組み込み(タスク049)。ナイロビのホテルロビーの「聴く」イベントの会話文(クロが執筆)。
# 発音の課題・言い直し・採点・単語バトルはない(聴くだけ)。英文は短く、歌の余韻をこわさない長さ。
# 実在名: Villa Rosa Kempinski(入国審査の会話 nbo_immig2 と同じホテル)。個人名なし。歌詞(宣言文)は引用しない。
# 画面に出る日本語は、場面の入り(intro)だけ(ほかの場面と同じ)。会話文は英語だけ。
SONG_SCENE = {
    'id': 'nbo_song',
    'who': 'ラウンジの歌手',
    'bg': 'nlobby',
    'sp': 'singer',
    'intro': '夜のホテルのロビー。奥のラウンジの隅から、やさしい歌声が聞こえてくる。ふたりは足をとめて、耳をかたむけた。',
    # 曲が終わったあとの短いやりとり(読み上げ+表示。マイクは使わない)。w = 話す人(singer / lulu / king)
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
