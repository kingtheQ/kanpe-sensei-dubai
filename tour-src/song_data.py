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
