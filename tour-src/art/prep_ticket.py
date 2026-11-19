# -*- coding: utf-8 -*-
"""チケット売り場(旅行代理店)の素材から、ゲームで使う画像を作る(タスク041)。
使い方: python3 -I tour-src/art/prep_ticket.py <素材を展開したフォルダ> [出力フォルダ=tour/assets/art]
  展開フォルダには ticket-office-bg-clean-noroute.png / ticket-office-bg-clean.png / npc-ticket-clerk-a-front.png / king-back.png / lulu-back.png がある。必要: pillow numpy
作るもの(縮め方は prep.py・prep_sage.py と同じ: BOX で縮め、透明度110以上を不透明にそろえる):
  - 背景 ticket-office-bg-clean-noroute.png(航路なし。ふだん) と ticket-office-bg-clean.png(航路入りの完成形。アニメが描けないときの静止画): そのままコピー(ぼかさない)
  - npc/tk-clerk.png     係員(正面): 室内(room)の大人の高さ 273px(ホテルのフロント係 o-front-woman-blonde-suit と同じ基準)
  - npc/tk-king-back.png / npc/tk-lulu-back.png : 室内の基準の大きさ。素材の後ろ姿は室内型(2倍)と同じ縮尺(キングの横幅136≒室内型137)なので、縮めずそのままコピー"""
import sys, os, shutil
import numpy as np
from PIL import Image
SRC = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tour', 'assets', 'art')
os.makedirs(os.path.join(OUT, 'npc'), exist_ok=True)
for f in ('ticket-office-bg-clean-noroute.png', 'ticket-office-bg-clean.png'):
    shutil.copy(os.path.join(SRC, f), os.path.join(OUT, f)); print(f, Image.open(os.path.join(OUT, f)).size)
cw, ch = Image.open(os.path.join(SRC, 'npc-ticket-clerk-a-front.png')).size
w, h = round(cw * 273 / ch), 273
r = Image.open(os.path.join(SRC, 'npc-ticket-clerk-a-front.png')).convert('RGBA').resize((w, h), Image.BOX)
a = np.array(r); a[..., 3] = np.where(a[..., 3] >= 110, 255, 0)
Image.fromarray(a, 'RGBA').save(os.path.join(OUT, 'npc', 'tk-clerk.png')); print('npc/tk-clerk.png', (w, h))
for n in ('king', 'lulu'):
    shutil.copy(os.path.join(SRC, n + '-back.png'), os.path.join(OUT, 'npc', 'tk-%s-back.png' % n))
    print('npc/tk-%s-back.png' % n, Image.open(os.path.join(OUT, 'npc', 'tk-%s-back.png' % n)).size)
