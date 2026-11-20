# -*- coding: utf-8 -*-
"""荷物スプライト(nairobi-baggage-bags.png)の2行目(種類1)を、青+黄タグの専用スーツケースに差し替える(タスク046)。
使い方: python3 -I tour-src/art/prep_hero_bag.py <nairobi-baggage-hero-bag.png> [bags画像=tour/assets/art/nairobi-baggage-bags.png]
素材は 96×196 の2段(上=手前用 66×88、下=奥用 46×66。絵の粒は2×2)。13段階の大きさ(奥ほど小さく暗い)は、045 と同じ式
(暗さ 0.925+0.075·sin、sin=-1 奥 … +1 手前)で作る。手前=素材の上段そのまま、奥=素材の下段(暗さをかける)、間は上段を半分の粒で拡縮(NEAREST)。
1コマは 112×104(2倍)、足もとは下から9画素(半分の座標で4)、横は中央。"""
import sys, os
from PIL import Image
import numpy as np
SRC = sys.argv[1]
SHEET = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tour', 'assets', 'art', 'nairobi-baggage-bags.png')
CW, CH, NLV, ROW = 112, 104, 13, 1
hero = Image.open(SRC).convert('RGBA'); assert hero.size == (96, 196), hero.size
def crop2x(y0, y1):          # 外わくで切り出し、2×2の粒を1画素にもどす(半分の座標)
    box = hero.crop((0, y0, 96, y1 + 1)); bb = box.getbbox(); box = box.crop(bb)
    a = np.array(box); assert (a[0::2, 0::2] == a[1::2, 1::2]).all() and box.width % 2 == 0 and box.height % 2 == 0
    return box.resize((box.width // 2, box.height // 2), Image.NEAREST)
front, back = crop2x(24, 111), crop2x(130, 195)          # 33×44 と 23×33
assert front.size == (33, 44) and back.size == (23, 33), (front.size, back.size)
sheet = Image.open(SHEET).convert('RGBA'); assert sheet.size == (CW * NLV, CH * 6), sheet.size
cell = Image.new('RGBA', (CW * NLV, CH), (0, 0, 0, 0))
for li in range(NLV):
    sn = -1 + 2.0 * li / (NLV - 1); dimf = 0.925 + 0.075 * sn
    if li == NLV - 1: im = front
    elif li == 0: im = back
    else:
        w = int(round(back.width + (front.width - back.width) * li / (NLV - 1))); h = int(round(back.height + (front.height - back.height) * li / (NLV - 1)))
        im = front.resize((w, h), Image.NEAREST)
    a = np.array(im).astype(float); a[:, :, :3] *= dimf; im = Image.fromarray(np.clip(a + .5, 0, 255).astype('uint8'), 'RGBA')
    x0 = 28 - im.width // 2; y0 = 48 - im.height            # 半分の座標(足もと y=48)
    big = im.resize((im.width * 2, im.height * 2), Image.NEAREST)
    cell.alpha_composite(big, (li * CW + x0 * 2, y0 * 2))
blank = Image.new('RGBA', (CW * NLV, CH), (0, 0, 0, 0)); sheet.paste(blank, (0, ROW * CH)); sheet.alpha_composite(cell, (0, ROW * CH))
sheet.save(SHEET); print('差し替え完了 行', ROW, sheet.size)
