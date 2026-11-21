# -*- coding: utf-8 -*-
"""ナイロビのホテルロビーの歌手イベントの素材から、ゲームで使う画像・音を作る(タスク049)。
使い方: python3 -I tour-src/art/prep_singer.py <素材を展開したフォルダ> [tour/assets のフォルダ=tour/assets]
  展開フォルダには nairobi-hotel-lobby-v1.png / npc-woman-hijab-front.png / song-chant.mp3 / song-theme.mp3 がある。必要: pillow numpy
作るもの(縮め方は prep_sage.py と同じ: BOX で縮め、透明度110以上を不透明にそろえる):
  - art/nairobi-hotel-lobby-v1.png  背景(1536×960): そのままコピー(ぼかさない)
  - art/npc/hall-singer.png         歌手(正面): 大人の高さ 136px (031の基準。広間の賢者と同じ)
  - song/song-chant.mp3 / song/song-theme.mp3  そのままコピー"""
import sys, os, shutil
import numpy as np
from PIL import Image
SRC = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tour', 'assets')
for d in ('art/npc', 'song'): os.makedirs(os.path.join(OUT, d), exist_ok=True)
shutil.copy(os.path.join(SRC, 'nairobi-hotel-lobby-v1.png'), os.path.join(OUT, 'art', 'nairobi-hotel-lobby-v1.png'))
for f in ('song-chant.mp3', 'song-theme.mp3'): shutil.copy(os.path.join(SRC, f), os.path.join(OUT, 'song', f))
w, h = Image.open(os.path.join(SRC, 'npc-woman-hijab-front.png')).size
nw = round(w * 136 / h)
r = Image.open(os.path.join(SRC, 'npc-woman-hijab-front.png')).convert('RGBA').resize((nw, 136), Image.BOX)
a = np.array(r); a[..., 3] = np.where(a[..., 3] >= 110, 255, 0)
Image.fromarray(a, 'RGBA').save(os.path.join(OUT, 'art', 'npc', 'hall-singer.png')); print('hall-singer.png', (nw, 136))
