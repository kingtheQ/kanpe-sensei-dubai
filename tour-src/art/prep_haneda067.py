# -*- coding: utf-8 -*-
"""羽田出発の残り場面(タスク067)の派生素材。NEAREST のみ(ぼかさない)。使い方: python3 tour-src/art/prep_haneda067.py
機内の会話場面の客室乗務員: 既存の正面の絵 npc/ca-front.png(139×266)を高さ274に → npc/ca-front-274.png
  (頭105px＝この場面のキングの頭100pxの1.05倍。配置の正本プレビューと画素を突き合わせて同じ絵と確認済み)"""
import os
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NPC = os.path.join(ROOT, 'tour/assets/art/npc')
im = Image.open(os.path.join(NPC, 'ca-front.png')).convert('RGBA')
H = 274; W = round(im.width * H / im.height)
im.resize((W, H), Image.NEAREST).save(os.path.join(NPC, 'ca-front-274.png'), optimize=True)
print('ca-front-274.png', W, H)

# (2) 出国審査(hnd_exit)の係官と青いスーツケース: 配置の正本プレビュー(ref-haneda067/)から、背景(haneda-exit-immigration-v1.png)と違う画素だけを切り出す。
#   係官: プレビューの係官は既存の o2-front-officer-blue(110×272)より小さく(幅97)、作りも細かい別の絵。既存を流用すると大きさが合わないので、見えている頭と肩(窓口のカウンター y=600 まで)をそのまま使う。
#   スーツケース: 既存の artSuit(四角い箱)とは別の絵(青い本体・黄色の荷札・持ち手・車輪)。
#   どちらも 中心 x が 768 / 862 になるよう左右に透明の列を足し、係官は下に8行足す(うなずきの上下で窓の下に隙間が出ないため。最下行のくり返し)。
import numpy as np, scipy.ndimage as nd
REF = os.path.join(ROOT, 'tour-src/art/ref-haneda067/haneda-exit-immigration-preview.png')
pv = np.array(Image.open(REF).convert('RGB')); bg = np.array(Image.open(os.path.join(ROOT, 'tour/assets/art/haneda-exit-immigration-v1.png')).convert('RGB'))
dd = np.abs(pv.astype(int) - bg.astype(int)).sum(2)
def cut(x0, y0, x1, y1, th, cx, pad_bottom=0):
    m = np.zeros(dd.shape, bool); m[y0:y1, x0:x1] = dd[y0:y1, x0:x1] > th
    lab, n = nd.label(m); k = 1 + int(np.argmax(nd.sum(m, lab, range(1, n + 1)))); m = nd.binary_fill_holes(lab == k)
    ys, xs = np.where(m); l, r, t, b = xs.min(), xs.max(), ys.min(), ys.max()
    half = max(cx - l, r - cx + 1); W = 2 * half; out = np.zeros((b - t + 1 + pad_bottom, W, 4), np.uint8)
    for y in range(t, b + 1):
        for x in range(l, r + 1):
            if m[y, x]: out[y - t, x - (cx - half)] = (*pv[y, x], 255)
    for i in range(pad_bottom): out[b - t + 1 + i] = out[b - t]
    return out, (cx - half, t, b)
off, (ol, ot, ob) = cut(690, 440, 850, 606, 60, 768, 8)
Image.fromarray(off, 'RGBA').save(os.path.join(NPC, 'hexit-officer.png'), optimize=True); print('hexit-officer.png', off.shape[1], off.shape[0], 'left', ol, 'top', ot, 'bottom', ob)
su, (sl, st, sb) = cut(815, 700, 915, 830, 60, 862)
Image.fromarray(su, 'RGBA').save(os.path.join(NPC, 'hexit-suitcase.png'), optimize=True); print('hexit-suitcase.png', su.shape[1], su.shape[0], 'left', sl, 'top', st, 'bottom(足もと)', sb)
