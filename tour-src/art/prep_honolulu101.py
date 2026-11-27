# -*- coding: utf-8 -*-
"""タスク101: ホノルル空港の出発案内板の中身(別素材)を作る。
背景 honolulu-departure-v1.png の青い板は「WAIT TIMES / CHECKPOINT」(保安検査の待ち時間板)で、行き先の欄がない。
場面 hnl_dep_board1(シドニー行きのゲートを探す)のため、この板の中を「DEPARTURES」の表に描き直した2コマ(strip)を、背景の座標にそのまま重ねる。
- 範囲: 背景の x=76..534 / y=116..370(板の枠は背景のまま残す。458×254)。art.js の strips: x:76,y:116。
- 2コマ: 1コマ目=ふつうの表 / 2コマ目=シドニーの行が黄色く光る(1秒ごと)。
- 表示するのは行き先だけ。時刻は「--:--」・ゲートは「-」(未確認の数字は出さない)。航空会社名・便名も出さない。
  行き先(Los Angeles・Tokyo・Sydney・Auckland)はホノルルから行ける代表的な都市の例で、どの便が実在するかは示さない(板の見た目の素材)。
- 粒: 半分の解像度で字を描き、NEAREST で2倍(背景と同じ2px粒)。字のふちをなめらかにしない(fontmode '1')。
使い方: python3 tour-src/art/prep_honolulu101.py
"""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART = os.path.join(ROOT, 'tour', 'assets', 'art')
BG = Image.open(os.path.join(ART, 'honolulu-departure-v1.png')).convert('RGB')
X0, Y0, W, H = 76, 116, 458, 254
BLUE = BG.getpixel((90, 230)); HEAD = BG.getpixel((90, 130))
WHITE = (252, 250, 240); LIGHT = (218, 224, 236); LIGHT2 = (200, 212, 228); GOLD = (250, 200, 40); INK = (16, 42, 110); DIM = (96, 108, 130)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
FS = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 10)
FM = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 11)
DEST = ['Los Angeles', 'Tokyo', 'Sydney', 'Auckland']; HI = 2


def frame(hi):
    w, h = W // 2, H // 2
    im = Image.new('RGB', (w, h), BLUE)
    d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([0, 0, w - 1, 28], fill=HEAD)
    tw = d.textlength('DEPARTURES', font=FB); d.text(((w - tw) // 2, 5), 'DEPARTURES', font=FB, fill=WHITE)
    d.text((14, 34), 'TIME', font=FS, fill=GOLD); d.text((62, 34), 'DESTINATION', font=FS, fill=GOLD); d.text((w - 44, 34), 'GATE', font=FS, fill=GOLD)
    y = 48
    for i, name in enumerate(DEST):
        on = hi and i == HI
        d.rectangle([8, y, w - 9, y + 17], fill=GOLD if on else (LIGHT if i % 2 == 0 else LIGHT2))
        d.text((14, y + 3), '--:--', font=FM, fill=INK if on else DIM)
        d.text((62, y + 3), name, font=FM, fill=INK)
        d.text((w - 36, y + 3), '-', font=FM, fill=INK if on else DIM)
        if i == HI:
            d.polygon([(2, y + 3), (2, y + 14), (6, y + 8)], fill=GOLD if not hi else INK)   # 目じるしの ▶
        y += 21
    return im.resize((W, H), Image.NEAREST)


sheet = Image.new('RGB', (W * 2, H))
sheet.paste(frame(False), (0, 0)); sheet.paste(frame(True), (W, 0))
out = os.path.join(ART, 'honolulu-board-rows-strip.png')
sheet.save(out)
print('saved', out, sheet.size)
