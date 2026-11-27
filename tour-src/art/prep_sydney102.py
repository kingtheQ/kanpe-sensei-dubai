# -*- coding: utf-8 -*-
"""タスク102: シドニー空港T1の出発案内板(Departures)の中身(別素材)を作る。
背景 sydney-departure-v1.png の左の「Departures」の板は、行の中身を描いていない(見出しと淡い帯4本だけ)。
場面 syd_dep_gate1 で重ねる「シンガポール行きの行」を、2コマの横並び(strip)として作る。
- 範囲: 背景の x=206..515 / y=396..509(帯4本。310×114)。背景の座標にそのまま重ねる(art.js の strips: x:206,y:396)。
- 2コマ: 1コマ目=ふつうの帯 / 2コマ目=シンガポールの行(2行目)が黄色く光る(1秒ごと)。
- 表示するのは行き先だけ。時刻は「--:--」、搭乗口は「-」にする(未確認の数字は出さない。正確な出発時刻・ゲート番号は台詞にも板にも出さない)。
  行き先(Melbourne / Singapore / Auckland / Los Angeles)は、シドニー発の直行がある都市の一般名(便名・航空会社・時刻は書かない)。
- 粒: 半分の解像度で字を描き、NEAREST で2倍(背景と同じ2px粒)。字のふちをなめらかにしない(fontmode '1')。
使い方: python3 -I tour-src/art/prep_sydney102.py
"""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART = os.path.join(ROOT, 'tour', 'assets', 'art')
BG = Image.open(os.path.join(ART, 'sydney-departure-v1.png')).convert('RGB')
X0, Y0, W, H = 206, 396, 310, 114
# 背景の帯の位置(板の左上 (206,396) からの相対 y)と色(実測): 396-421 / 428-449 / 456-477 / 484-509
ROWS = [(0, 26, (204, 214, 226)), (32, 54, (204, 214, 226)), (60, 82, (214, 222, 232)), (88, 114, (222, 228, 234))]
INK = (16, 24, 60); DIM = (110, 116, 128); HI = (255, 211, 106); NAVY = (28, 60, 120)
DATA = ['Melbourne', 'Singapore', 'Auckland', 'Los Angeles']
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 10)
COL = {'zeit': 5, 'ziel': 44, 'gate': 142}   # 半分の解像度の x


def frame(hi):
    base = BG.crop((X0, Y0, X0 + W, Y0 + H)).resize((W // 2, H // 2), Image.NEAREST)
    d = ImageDraw.Draw(base); d.fontmode = '1'
    for i, (a, b, col) in enumerate(ROWS):
        a2, b2 = a // 2, b // 2
        on = hi and i == 1
        d.rectangle([0, a2, W // 2 - 1, b2 - 1], fill=HI if on else col)
        y = a2 + max(0, (b2 - a2 - 12) // 2)
        d.text((COL['zeit'], y), '--:--', font=FONT, fill=INK if on else DIM)
        d.text((COL['ziel'], y), DATA[i].upper(), font=FONT, fill=INK)
        d.text((COL['gate'], y), '-', font=FONT, fill=INK if on else DIM)
        if i == 1:
            d.polygon([(0, a2 + 2), (0, b2 - 3), (3, (a2 + b2) // 2)], fill=INK if on else NAVY)   # 目じるしの ▶
    return base.resize((W, H), Image.NEAREST)


sheet = Image.new('RGB', (W * 2, H))
sheet.paste(frame(False), (0, 0)); sheet.paste(frame(True), (W, 0))
out = os.path.join(ART, 'sydney-board-sin-strip.png')
sheet.save(out)
print('saved', out, sheet.size)
