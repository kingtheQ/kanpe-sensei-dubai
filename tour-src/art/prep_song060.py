# -*- coding: utf-8 -*-
"""タスク060: ホテルの歌場面(hsong)の観客5人と歌手(台の上)の絵を作る。NEAREST のみ(ぼかさない)。
使い方: python3 -I tour-src/art/prep_song060.py
  入力  = tour-src/art/song060-src/npc-*.png(素材パックの観客の後ろ姿)・tour-src/art/people-src/npc-woman-hijab-front.png(歌手の原寸)
  出力  = tour/assets/art/npc/a-back-<人>.png(観客。高さは配置の正本プレビューの実測: 230〜236px)・hall-singer-stage.png(歌手。高さ236px)
  背景 nairobi-hotel-lobby-song-v1.png は、そのまま tour/assets/art/ に置く(縮めない)。必要: pillow"""
import os
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'tour-src/art/song060-src'); OUT = os.path.join(ROOT, 'tour/assets/art/npc')
JOBS = [(os.path.join(SRC, 'npc-back-safari.png'), 'a-back-safari', 232), (os.path.join(SRC, 'npc-back-man-thobe.png'), 'a-back-thobe', 236),
        (os.path.join(SRC, 'npc-backpacker-back.png'), 'a-back-backpacker', 230), (os.path.join(SRC, 'npc-back-maasai.png'), 'a-back-maasai', 234),
        (os.path.join(SRC, 'npc-back-man-dashiki.png'), 'a-back-dashiki', 234),
        (os.path.join(ROOT, 'tour-src/art/people-src/npc-woman-hijab-front.png'), 'hall-singer-stage', 236)]
for f, n, H in JOBS:
    im = Image.open(f).convert('RGBA'); W = round(im.width * H / im.height)
    im.resize((W, H), Image.NEAREST).save(os.path.join(OUT, n + '.png'), optimize=True); print(n + '.png', '%dx%d' % (W, H))
