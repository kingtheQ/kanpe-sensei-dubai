# -*- coding: utf-8 -*-
"""ローマ(テルミニ駅)の発車標の中身(別素材)を作る(タスク094)。
使い方: python3 -I tour-src/art/prep_rome_board.py [出力フォルダ=tour/assets/art]
背景 rome-departure-v2.png の発車標は、枠と見出しだけで「表示面」は暗い線が並ぶだけ。動くもの・読ませる中身は背景に焼かず、
この別素材(2コマ。1コマ 420×240)を、発車標の右半分(Partenze)の上に重ねる。
  - 行き先は、ローマ・テルミニから実際に高速列車が出ている大きな駅の名前だけ(ナポリ・フィレンツェ・ミラノ・ヴェネツィア・トリノ・ボローニャ)。
  - 時刻の列は「--:--」(正確な発車時刻は台詞にも表示にも出さない。094の決まり)。ホームの番号も出さない
    (テルミニでは、ホーム番号は発車の少し前に表示される。番号が出る前は「--」。2コマ目は枠だけにして点滅させる)。
  - ミラノ(チューリッヒ行きの最初の列車)の行だけ、明るい色と細い枠で目立たせる。「Zurigo」の行は無い(ローマ→チューリッヒは直通ではないため)。
絵は半分の大きさ(210×120)で描き、2倍の NEAREST で拡大する(背景と同じ2pxの粒)。必要: pillow・DejaVu Sans Mono Bold。
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tour', 'assets', 'art')
os.makedirs(OUT, exist_ok=True)
BG = (13, 14, 20); LINE = (40, 42, 50); AMB = (214, 166, 58); GREY = (140, 142, 150); HI = (255, 226, 120); HIBOX = (200, 150, 40)
W, H = 210, 120
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 9)
SM = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 8)
ROWS = [('NAPOLI CENTRALE', 'FR'), ('FIRENZE S.M.N.', 'FR'), ('MILANO CENTRALE', 'FR'), ('VENEZIA S.LUCIA', 'FR'), ('TORINO P.NUOVA', 'FR'), ('BOLOGNA CENTRALE', 'FR')]
HILITE = 2   # ミラノ
def txt(d, xy, s, f, fill):
    d.fontmode = '1'; d.text(xy, s, font=f, fill=fill)
def frame(blink):
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    # 列の見出し(小さく・灰色)
    txt(d, (3, 2), 'Ora', SM, GREY); txt(d, (36, 2), 'Destinazione', SM, GREY); txt(d, (134, 2), 'Tr.', SM, GREY); txt(d, (170, 2), 'Bin.', SM, GREY)
    d.line([(0, 12), (W, 12)], fill=LINE)
    for i, (dest, tr) in enumerate(ROWS):
        y = 14 + i * 12
        hi = (i == HILITE)
        col = HI if hi else AMB
        txt(d, (3, y), '--:--', FONT, col); txt(d, (36, y), dest, FONT, col); txt(d, (134, y), tr, FONT, col)
        if hi:
            d.rectangle([167, y - 1, 207, y + 10], outline=HIBOX)
            if not blink: txt(d, (176, y), '--', FONT, HI)
        else:
            txt(d, (176, y), '--', FONT, col)
        d.line([(0, y + 11), (W, y + 11)], fill=LINE)
    # 残りの行は空の線だけ(行き先を作らない)
    for i in range(len(ROWS), 9):
        y = 14 + i * 12
        d.line([(0, y + 11), (W, y + 11)], fill=LINE)
    return im.resize((W * 2, H * 2), Image.NEAREST)
a, b = frame(0), frame(1)
strip = Image.new('RGB', (W * 4, H * 2)); strip.paste(a, (0, 0)); strip.paste(b, (W * 2, 0))
p = os.path.join(OUT, 'rome-departure-board-strip.png'); strip.save(p); print(p, strip.size)
# 確認用: 背景に重ねたプレビュー(1コマ目・2コマ目)
bgp = os.path.join(OUT, 'rome-departure-v2.png')
if os.path.exists(bgp):
    for k, fr in enumerate((a, b)):
        pv = Image.open(bgp).convert('RGB'); pv.paste(fr, (714, 142)); pv.save('/tmp/rome-board-preview-%d.png' % k)
