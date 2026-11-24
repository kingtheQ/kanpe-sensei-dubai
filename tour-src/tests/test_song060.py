# -*- coding: utf-8 -*-
"""タスク060(ロビーの真ん中で歌う形)は、タスク066で廃止された(ロビーは通常版・歌は別場面のプールサイド)。
このテストは、060の素材と art 設定が「消されずに残っている」ことだけを確認する(動作の確認は test_lobby066.py)。
使い方: python3 -I tour-src/tests/test_song060.py"""
import os, sys, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
bad = []
def chk(n, ok):
    print(('OK  ' if ok else 'NG  ') + n)
    if not ok: bad.append(n)
art = open(os.path.join(ROOT, 'tour-src/art.js'), encoding='utf-8').read()
for f in ['nairobi-hotel-lobby-song-v1.png', 'npc/hall-singer-stage.png'] + ['npc/a-back-%s.png' % n for n in ['safari', 'thobe', 'backpacker', 'maasai', 'dashiki']]:
    chk('060の素材は残っている: ' + f, os.path.exists(os.path.join(ROOT, 'tour/assets/art', f)))
chk('060の art 設定 nsong は残っている(使わない)', "nsong:{bg:'nairobi-hotel-lobby-song-v1.png'" in art)
sd = open(os.path.join(ROOT, 'tour-src/song_data.py'), encoding='utf-8').read()
chk('歌場面(nbo_song)の背景は 066 でプールサイド(npool)に変わった', "'bg': 'npool'" in sd and "'bg': 'nsong'" not in sd)
print('FAILED: %s' % bad if bad else 'ALL OK'); sys.exit(1 if bad else 0)
