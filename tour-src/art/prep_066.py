# -*- coding: utf-8 -*-
"""タスク066: プールサイドのショータイムの絵を作る。NEAREST のみ(ぼかさない)。
使い方: python3 -I tour-src/art/prep_066.py <素材パック(kanpe-assets-lobby-showtime-066)を展開したフォルダ>
  出力: tour/assets/art/nairobi-pool-v2.png・nairobi-pool-sparkle-strip-v2.png・nairobi-pool-lights-strip.png(そのままコピー)
        tour/assets/art/npc/s-stand-front.png / s-stand-sing1.png / s-stand-sing2.png(歌手。高さ250・NEAREST・縮小率250/344)
        tour/assets/art/npc/b-back-<人>.png(観客5人。高さ250。060の a-back-* の原寸素材 song060-src から。060の絵は消さない)
  必要: pillow"""
import os, shutil, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = sys.argv[1]; ART = os.path.join(ROOT, 'tour/assets/art'); NPC = os.path.join(ART, 'npc'); S60 = os.path.join(ROOT, 'tour-src/art/song060-src')
for f in ('nairobi-pool-v2.png', 'nairobi-pool-sparkle-strip-v2.png', 'nairobi-pool-lights-strip.png'): shutil.copy(os.path.join(SRC, f), os.path.join(ART, f))
shutil.copy(os.path.join(SRC, 'nairobi-pool-v2-preview.png'), os.path.join(ROOT, 'tour-src/art/ref-066/nairobi-pool-v2-preview.png'))
JOBS = [(os.path.join(SRC, 'singer-stand-front.png'), 's-stand-front'), (os.path.join(SRC, 'singer-stand-sing-left-1.png'), 's-stand-sing1'),
        (os.path.join(SRC, 'singer-stand-sing-left-2.png'), 's-stand-sing2'),
        (os.path.join(S60, 'npc-back-safari.png'), 'b-back-safari'), (os.path.join(S60, 'npc-back-man-thobe.png'), 'b-back-thobe'),
        (os.path.join(S60, 'npc-backpacker-back.png'), 'b-back-backpacker'), (os.path.join(S60, 'npc-back-maasai.png'), 'b-back-maasai'),
        (os.path.join(S60, 'npc-back-man-dashiki.png'), 'b-back-dashiki')]
for f, n in JOBS:
    im = Image.open(f).convert('RGBA'); W = round(im.width * 250 / im.height)
    im.resize((W, 250), Image.NEAREST).save(os.path.join(NPC, n + '.png'), optimize=True); print(n + '.png', '%dx%d' % (W, 250))
