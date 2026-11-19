# -*- coding: utf-8 -*-
"""賢者の広間の素材から、ゲームで使う画像を作る(タスク040)。
使い方: python3 -I tour-src/art/prep_sage.py <素材を展開したフォルダ> [出力フォルダ=tour/assets/art]
  展開フォルダには sage-hall-bg-clean.png / sage-hall-globe-strip.png / npc-sage-front.png / king-back.png / lulu-back.png がある。必要: pillow numpy
作るもの(縮め方は prep.py と同じ: BOX で縮め、透明度110以上を不透明にそろえる):
  - 背景 sage-hall-bg-clean.png と 地球儀の8コマ sage-hall-globe-strip.png: そのままコピー(ぼかさない)
  - npc/hall-sage.png      賢者(正面): 大人の高さ 136px (031の基準)
  - npc/hall-king-back.png キングの後ろ姿 / npc/hall-lulu-back.png ルルの後ろ姿: 広い場面(wide)の大きさ。
      素材の後ろ姿は room(室内型=2倍)と同じ縮尺(横幅 キング136≒room 137)なので、wide = 0.5倍に縮める"""
import sys, os, shutil
import numpy as np
from PIL import Image
SRC = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tour', 'assets', 'art')
os.makedirs(os.path.join(OUT, 'npc'), exist_ok=True)
def shrink(src, dst, w, h):
    r = Image.open(os.path.join(SRC, src)).convert('RGBA').resize((w, h), Image.BOX)
    a = np.array(r); a[..., 3] = np.where(a[..., 3] >= 110, 255, 0)
    Image.fromarray(a, 'RGBA').save(os.path.join(OUT, dst)); print(dst, (w, h))
for f in ('sage-hall-bg-clean.png', 'sage-hall-globe-strip.png'):
    shutil.copy(os.path.join(SRC, f), os.path.join(OUT, f))
sw, sh = Image.open(os.path.join(SRC, 'npc-sage-front.png')).size
shrink('npc-sage-front.png', 'npc/hall-sage.png', round(sw * 136 / sh), 136)
for n in ('king', 'lulu'):
    w, h = Image.open(os.path.join(SRC, n + '-back.png')).size
    shrink(n + '-back.png', 'npc/hall-%s-back.png' % n, round(w / 2), round(h / 2))
