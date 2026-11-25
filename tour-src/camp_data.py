# -*- coding: utf-8 -*-
# 世界一周編 合宿(マッチョルル教室)デモ版(タスク078。クロが執筆)。国ごとのデータは別ファイル(eikaiwa_data と同じ形)。
# 位置づけ: チェックモード(?check=1)の一覧からだけ入る独立場面。入口の仕組み(失敗ポイントが尽きると強制的に発音教室へ=案B第4項)は未決定なので作らない。
#   本編の進行・セーブ・完了の数え(TOUR_IDS・trip.js・save.seen)に入れない。新しい保存キーは作らない。
# 決まり:
#   ・日本語訳は付けない。画面にも台本にも日本語を置かない。「復習」「テスト」「測定」「練習」など勉強感の強い言葉は出さない。数値スコア・失敗回数も出さない。
#   ・流れ(キング指定 2026-11-24。カードごとに繰り返す): ルルの導入 → ルルが全単語を1語ずつ2回ずつ読む → "Repeat after me!" → プレイヤーが1語ずつ →
#     短文も同じ流れ(2回読む → "Repeat after me!" → 丸ごと) → 次のカード。終わったら締めの台詞。
#   ・発音判定・失敗ルール(074: 自動おてほん→3回目でルルが代わりに言う)は既存の「聞く→言う」フローを流用(新しい仕組みなし)。
#   ・マッチョルルの画像素材は存在しない。通常のルルを大きく表示して代用する。差し替えは下の LULU_IMG(と LULU_W/LULU_H/LULU_HIP)の1か所だけ。

# ---- ルルの表示素材(1か所で指定)。マッチョルルの絵ができたら、ここを差し替える ----
LULU_IMG = 'room-lulu-idle.png'   # tour/assets/art/ 直下。通常のルル(正面)。マッチョルルの素材は無いので代用
LULU_W, LULU_H = 138, 184         # 素材の大きさ(px)
LULU_HIP = 146                    # 腰の高さ(上端から。これより上だけが伸び縮みし、足もと・影は動かさない=037の標準)

CARD_DIR = 'camp/'                # tour/assets/art/camp/
CARDS = [
    dict(id='ill', img='card-ill-v3.png', mouth='v3-i-160x128.png', snd='-ill /ɪl/',
         words=['skill', 'drill', 'grill', 'chill', 'mill', 'pill'],          # カードの並び(左上→右上→次の段…)
         sentence='Drills build grill skills.',
         intro="Welcome to camp! I'm Macho Lulu. Let's make our mouths strong!"),
    dict(id='thr', img='card-thr-v3.png', mouth='v3-th-160x128.png', snd='thr /θr/',
         words=['three', 'thrill', 'thriller', 'throw', 'through', 'three-point'],
         sentence='The throw went through for three points!',
         intro="Next card! Stick your tongue out a little."),
]
OUTRO = "Great work! Your mouth is getting strong. See you at camp!"
REPEAT = "Repeat after me!"
READY = "Ready?"

# カード画像v3(1080×1920)の上の、単語のマスと短文の位置(タスク080: 生成スクリプトから実測。ハイライトの枠に使う)。左上x,y,幅,高さ
CELL_X = (64, 556); CELL_Y = (380, 708, 1036); CELL_W, CELL_H = 460, 300
SENT_BOX = (40, 1400, 1000, 468)


def payload():
    return dict(lulu=dict(img=LULU_IMG, w=LULU_W, h=LULU_H, hip=LULU_HIP), dir=CARD_DIR, repeat=REPEAT, ready=READY, outro=OUTRO,
                cell=dict(x=list(CELL_X), y=list(CELL_Y), w=CELL_W, h=CELL_H), sent=list(SENT_BOX), cardW=1080, cardH=1920,
                cards=[dict(id=c['id'], img=c['img'], mouth=c['mouth'], words=c['words'], sentence=c['sentence'], intro=c['intro']) for c in CARDS])


def add(D):
    D.append(dict(id='camp_demo1', who='Lulu', bg='campK', sp='camp', intro='', pairs=[], words=[], conv=1, nohelp=1, camp78=payload()))
