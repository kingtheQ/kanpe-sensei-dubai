# -*- coding: utf-8 -*-
"""旅行者NPC(タスク047)のスプライトを、場面の大きさに縮める(NEAREST のみ。ぼかさない)。
使い方: python3 tour-src/art/prep_people.py
  原寸(高さ約344px)= tour-src/art/people-src/npc-<人>-<ポーズ>.png
  出力 = tour/assets/art/npc/t-<人>-<ポーズ>.png
  立ち(front/back)= 大人126px(広間基準 キング114px×約1.1)
  座り(sit-side-1/2)= 198px(ラウンジの座り配置プレビューから測った値。ラウンジ背景を入れる回に、実物と合わせて確かめる)"""
import os, glob
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'tour-src/art/people-src'); OUT = os.path.join(ROOT, 'tour/assets/art/npc')
H_STAND, H_SIT = 126, 198
for f in sorted(glob.glob(os.path.join(SRC, 'npc-*.png'))):
    n = os.path.basename(f)[4:]            # <人>-<ポーズ>.png
    im = Image.open(f).convert('RGBA'); H = H_SIT if '-sit-' in n else H_STAND
    W = round(im.width * H / im.height)
    im.resize((W, H), Image.NEAREST).save(os.path.join(OUT, 't-' + n), optimize=True)
    print('t-' + n, '%dx%d' % (W, H))
