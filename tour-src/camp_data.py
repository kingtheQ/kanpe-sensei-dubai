# -*- coding: utf-8 -*-
# 世界一周編 合宿(マッチョルル教室)デモ版(タスク078。クロが執筆)。国ごとのデータは別ファイル(eikaiwa_data と同じ形)。
# 位置づけ: チェックモード(?check=1)の一覧からだけ入る独立場面。入口の仕組み(失敗ポイントが尽きると強制的に発音教室へ=案B第4項)は未決定なので作らない。
#   本編の進行・セーブ・完了の数え(TOUR_IDS・trip.js・save.seen)に入れない。新しい保存キーは作らない。
# 決まり:
#   ・日本語訳は付けない。画面にも台本にも日本語を置かない。「復習」「テスト」「測定」「練習」など勉強感の強い言葉は出さない。数値スコア・失敗回数も出さない。
#   ・流れ(キング指定 2026-11-24。カードごとに繰り返す): ルルの導入 → ルルが全単語を1語ずつ2回ずつ読む → "Repeat after me!" → プレイヤーが1語ずつ →
#     短文も同じ流れ(2回読む → "Repeat after me!" → 丸ごと) → 次のカード。終わったら締めの台詞。
#   ・発音判定・失敗ルール(074: 自動おてほん→3回目でルルが代わりに言う)は既存の「聞く→言う」フローを流用(新しい仕組みなし)。
#   ・ルルはマッチョルルのダンベル・アニメーション(タスク081)。素材の指定は下の LULU_FRAMES(と LULU_SEQ・LULU_FRAME_SEC・LULU_SCALE)の1か所だけ。
#   ・口パーツはルルの頭の上に出す(ルルは左下に固定。口の表示・非表示でルルの位置も大きさも変えない=081)。背景は背景画(camp.png)。

# ---- ルルの表示素材(1か所で指定)。ポーズ(コマ)を足す・順番を変えるときは、ここだけ変える ----
LULU_DIR = 'camp/'                # tour/assets/art/camp/
# 各コマ: img=ファイル名 / w,h=画像の大きさ(px) / foot_y=足もと(下端)の y(画像の上から。透明でない最下行の次) / foot_x=足もとの中心の x。
# foot_y・foot_x は素材から測った値(測り方は tests/test_gasshuku078.py が同じ式で照合する)。素材ごとに高さが少し違うので、足もとをこの2つでそろえる。
LULU_FRAMES = [
    dict(img='macho-dumbbell-1.png', w=334, h=360, foot_y=352, foot_x=167.0),   # ダンベルを下ろす
    dict(img='macho-dumbbell-2.png', w=380, h=360, foot_y=352, foot_x=185.0),   # 上げる
    dict(img='macho-dumbbell-3.png', w=392, h=357, foot_y=346, foot_x=195.0),   # 頭上
    dict(img='macho-dumbbell-4.png', w=368, h=358, foot_y=346, foot_x=184.5),   # 下ろす(今回の往復では使わない)
]
LULU_SEQ = [0, 1, 2, 1]           # コマの順(0始まり)。1→2→3→2→1→2→3→2… のカール往復ループ
LULU_FRAME_SEC = 0.45             # 1コマの長さ(秒)
LULU_SCALE = 0.66                 # ルルの表示倍率(従来の表示の高さに対する倍率。ここ1か所で変える)
LULU_REF_H = 340                  # 素材の中のルルの背の高さ(px。頭のてっぺん y=12 から足もと y=352 まで。コマ1で測った値)
LULU_OLD = (138, 184)             # 従来の通常ルル素材の大きさ(倍率の基準=従来の表示の高さを出すためだけに使う)
CARD_SHARE = 0.55                 # カードの表示の幅(ステージの幅に対する割合。従来は約0.46)

CARD_DIR = 'camp/'                # tour/assets/art/camp/
CARDS = [
    dict(id='ill', img='card-ill-v2.png', mouth='v3-i-160x128.png', snd='-ill /ɪl/',
         words=['pill', 'drill', 'hill', 'spill', 'gill', 'grill'],          # カードの並び(左上→右上→次の段…)
         sentence='Dan spilled ketchup on the grill.',
         intro="Welcome to camp! I'm Macho Lulu. Let's make our mouths strong!"),
    dict(id='thr', img='card-thr-v2.png', mouth='v3-th-160x128.png', snd='thr /θr/',
         words=['three', 'throne', 'throb', 'thread', 'throat', 'throw'],
         sentence='Pat threw three balls to his dog.',
         intro="Next card! Stick your tongue out a little."),
]
OUTRO = "Great work! Your mouth is getting strong. See you at camp!"
REPEAT = "Repeat after me!"
READY = "Ready?"

# カード画像(1080×1920)の上の、単語のマスと短文の位置(カードの絵から実測。ハイライトの枠に使う)。左上x,y,幅,高さ
CELL_X = (50, 553); CELL_Y = (464, 814, 1164); CELL_W, CELL_H = 478, 308
SENT_BOX = (40, 1530, 1000, 330)


def payload():
    return dict(lulu=dict(dir=LULU_DIR, frames=LULU_FRAMES, seq=LULU_SEQ, sec=LULU_FRAME_SEC, scale=LULU_SCALE, refH=LULU_REF_H, old=list(LULU_OLD)),
                cardShare=CARD_SHARE, dir=CARD_DIR, repeat=REPEAT, ready=READY, outro=OUTRO,
                cell=dict(x=list(CELL_X), y=list(CELL_Y), w=CELL_W, h=CELL_H), sent=list(SENT_BOX), cardW=1080, cardH=1920,
                cards=[dict(id=c['id'], img=c['img'], mouth=c['mouth'], words=c['words'], sentence=c['sentence'], intro=c['intro']) for c in CARDS])


def add(D):
    D.append(dict(id='camp_demo1', who='Lulu', bg='campK', sp='camp', intro='', pairs=[], words=[], conv=1, nohelp=1, camp78=payload()))
