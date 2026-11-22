# -*- coding: utf-8 -*-
"""ナイロビ出発まわり(タスク054)の派生素材。NEAREST のみ(ぼかさない)。使い方: python3 tour-src/art/prep_departure054.py
(1) 立つ旅行者を「室内の大きさ」に: 原寸(高さ約344px。tour-src/art/people-src)を高さ252pxに縮める → tour/assets/art/npc/t2-<人>-front|back.png
    (広間の大きさ=126px の ちょうど2倍。キング(室内)229px×約1.1 に当たる。チェックイン・保安検査・免税店・ゲートの背景は、カウンターが170px前後ある室内の大きさ)
(2) 係官(o-front-officer-*。広間の大きさ136px)を2倍に → npc/o2-front-officer-*.png (保安検査の係員。272px=室内の大人)
(3) ラウンジの手前の覆い: 座る人6人の配置の正本プレビュー(ref-departure/nairobi-lounge-v2-preview2.png)で、丸ブースのマサイ男性の下半身が
    手前のテーブルに隠れているところを、背景(nairobi-lounge-v2.png)の画素のまま取り出す → tour/assets/art/nairobi-lounge-front-054.png(切り出しの左上=(1256,667))"""
import os, glob
import numpy as np
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'tour-src/art/people-src'); ART = os.path.join(ROOT, 'tour/assets/art'); NPC = os.path.join(ART, 'npc')
H_STAND_ROOM = 252
for pose in ('front', 'back'):
    for f in sorted(glob.glob(os.path.join(SRC, 'npc-*-%s.png' % pose))):
        n = os.path.basename(f)[4:]
        im = Image.open(f).convert('RGBA'); W = round(im.width * H_STAND_ROOM / im.height)
        im.resize((W, H_STAND_ROOM), Image.NEAREST).save(os.path.join(NPC, 't2-' + n), optimize=True); print('t2-' + n, W, H_STAND_ROOM)
for n in ('blue', 'green-1', 'green-2'):
    im = Image.open(os.path.join(NPC, 'o-front-officer-%s.png' % n)).convert('RGBA')
    im.resize((im.width * 2, im.height * 2), Image.NEAREST).save(os.path.join(NPC, 'o2-front-officer-%s.png' % n), optimize=True); print('o2-front-officer-' + n, im.width * 2, im.height * 2)
# (3) 手前の覆い
prev = np.array(Image.open(os.path.join(ROOT, 'tour-src/art/ref-departure/nairobi-lounge-v2-preview2.png')).convert('RGB')).astype(int)
base = np.array(Image.open(os.path.join(ART, 'nairobi-lounge-v2.png')).convert('RGB')).astype(int)
X, Y = 1256, 667   # マサイ男性(sit-side-1)の左上(正本プレビューから測った値)
sp = np.array(Image.open(os.path.join(NPC, 't-maasai-sit-side-1.png')).convert('RGBA')); h, w = sp.shape[:2]
op = sp[:, :, 3] > 128; sub = prev[Y:Y + h, X:X + w]; bs = base[Y:Y + h, X:X + w]
dA = np.abs(sub - sp[:, :, :3].astype(int)).sum(axis=2); dB = np.abs(sub - bs).sum(axis=2)
front = op & (dB < 25) & (dA >= 60)       # 正本では背景のほうが見えている = 手前に背景の物(テーブル)がある画素
out = np.zeros((h, w, 4), np.uint8); out[front, :3] = bs[front]; out[front, 3] = 255
Image.fromarray(out, 'RGBA').save(os.path.join(ART, 'nairobi-lounge-front-054.png'), optimize=True)
print('lounge front px', int(front.sum()), 'of', int(op.sum()))
