# -*- coding: utf-8 -*-
"""タスク097: フランクフルト中央駅の大発車標の中身(別素材)を作る。
背景 frankfurt-arrival-v1.png の大発車標は、行の中身を描いていない(見出しと淡い帯だけ)。
場面 fra_dep_board1 で重ねる「ブリュッセル行きの行」を、2コマの横並び(strip)として作る。
- 範囲: 背景の x=96..1442 / y=224..342(帯4本。1346×118)。背景の座標にそのまま重ねる(art.js の strips: x:96,y:224)。
- 2コマ: 1コマ目=ふつうの帯 / 2コマ目=ブリュッセルの行(2行目)が黄色く光る(1秒ごと)。
- 表示するのは行き先と「Über」(途中の駅)だけ。時刻とホームは未確認なので「--:--」「-」にする(正確な発車時刻は出さない)。
  行き先は実在のフランクフルト発の行き先(Amsterdam Centraal / München Hbf / Hamburg-Altona)と、
  ICEの直通 Brüssel-Midi(Köln・Aachen を通る。Liège にも停まるが板には2駅だけ書く=DB公式)。
- 粒: 半分の解像度で字を描き、NEAREST で2倍(背景と同じ2px粒)。字のふちをなめらかにしない(fontmode '1')。
使い方: python3 tour-src/art/prep_frankfurt097.py
"""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART = os.path.join(ROOT, 'tour', 'assets', 'art')
BG = Image.open(os.path.join(ART, 'frankfurt-arrival-v1.png')).convert('RGB')
X0, Y0, W, H = 96, 224, 1346, 118
ROWS = [(0, 28, (238, 236, 214)), (30, 58, (150, 196, 202)), (60, 88, (196, 186, 216)), (90, 118, (238, 236, 214))]   # 背景の帯の位置と色(実測)
NAVY = (16, 42, 110); INK = (16, 24, 60); DIM = (110, 116, 128); HI = (255, 211, 106)
DATA = [   # (Über, Ziel)
    ('Köln', 'Amsterdam Centraal'),
    ('Köln · Aachen', 'Brüssel-Midi / Bruxelles-Midi'),
    ('Nürnberg', 'München Hbf'),
    ('Hannover', 'Hamburg-Altona')]
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 11)
COL = {'zeit': 10, 'ueber': 84, 'ziel': 212, 'gleis': 606}   # 背景の見出し(Zeit・Über・Ziel・Gleis)の x(半分の解像度)


def frame(hi):
    base = BG.crop((X0, Y0, X0 + W, Y0 + H)).resize((W // 2, H // 2), Image.NEAREST)   # 区切りの紺の線は背景のまま残す
    d = ImageDraw.Draw(base); d.fontmode = '1'
    for i, (a, b, col) in enumerate(ROWS):
        a2, b2 = a // 2, b // 2
        fill = HI if (hi and i == 1) else col
        d.rectangle([0, a2, W // 2 - 1, b2 - 1], fill=fill)
        y = a2 + 0
        d.text((COL['zeit'], y), '--:--', font=FONT, fill=DIM if not (hi and i == 1) else INK)
        d.text((COL['ueber'], y), DATA[i][0], font=FONT, fill=INK)
        d.text((COL['ziel'], y), DATA[i][1], font=FONT, fill=INK)
        d.text((COL['gleis'], y), '-', font=FONT, fill=DIM if not (hi and i == 1) else INK)
        if i == 1:
            d.polygon([(1, a2 + 2), (1, b2 - 3), (4, (a2 + b2) // 2 - 0)], fill=NAVY if not hi else INK)   # 目じるしの ▶
    return base.resize((W, H), Image.NEAREST)


sheet = Image.new('RGB', (W * 2, H))
sheet.paste(frame(False), (0, 0)); sheet.paste(frame(True), (W, 0))
out = os.path.join(ART, 'frankfurt-board-rows-strip.png')
sheet.save(out)
print('saved', out, sheet.size)
