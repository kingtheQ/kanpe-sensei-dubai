# -*- coding: utf-8 -*-
"""素材パック(kanpe-assets-v1.zip)から、ゲームで使う画像を作る(タスク028)。
使い方: python3 -I tour-src/art/prep.py <zipを展開したフォルダ> [出力フォルダ=tour/assets/art]
  展開フォルダには characters/ と backgrounds/ がある。必要: pillow numpy scipy
作るもの:
  - 人物: 足もとの芝・縁の黄緑を除き、背景に合う大きさ(wide=ナイロビ到着型 / room=室内型)に縮めた透過PNG
  - 背景: ナイロビ到着(人物なし)、ホテルのフロント(人物・店員・スーツケースを消したもの)
人物の大きさ: キング(立ち姿)の身長が wide=124px / room=248px (1536×960の背景に対して)。歩行コマも同じ倍率にそろえる。"""
import sys, os, shutil
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

SRC = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tour', 'assets', 'art')
os.makedirs(OUT, exist_ok=True)
CH, BG = os.path.join(SRC, 'characters'), os.path.join(SRC, 'backgrounds')

# ---------- 人物 ----------
USE = {'king-idle': 'expr-01', 'lulu-idle': 'expr-02', 'king-walk-a': 'walk-12', 'king-walk-b': 'walk-18',
       'lulu-walk-a': 'walk-10', 'lulu-walk-b': 'walk-17', 'lulu-walk-c': 'walk-23'}

def clean(path):
    a = np.array(Image.open(path).convert('RGBA')).astype(int)
    al = a[..., 3]
    hsv = np.array(Image.fromarray(a.astype('uint8'), 'RGBA').convert('RGB').convert('HSV')).astype(float)
    H, S, V = hsv[..., 0] * 360 / 255, hsv[..., 1] / 255, hsv[..., 2] / 255
    # 芝=足もとの暗い緑のかたまり。色が似ている顔の黄色などを消さないよう、「下のほうにある大きなかたまり」だけを芝とする
    loose = (H >= 62) & (H <= 135) & (S > .3) & (V < .85) & (al > 10)
    lab0, k0 = ndi.label(loose, structure=np.ones((3, 3)))
    grass = np.zeros_like(loose)
    hh = al.shape[0]
    for i in range(1, k0 + 1):
        mm = lab0 == i; ys0 = np.where(mm)[0]
        if mm.sum() > 150 and ys0.mean() > hh * .72: grass |= mm
    grass |= loose & (np.arange(hh)[:, None] > hh * .86)
    al = np.where(grass, 0, al)
    for _ in range(2):   # 縁に残った明るい黄緑だけを、透明に接する画素から2回削る
        near = ndi.binary_dilation(al < 10, structure=np.ones((3, 3)))
        al = np.where(near & (al >= 10) & (H >= 66) & (H <= 120) & (S > .3), 0, al)
    m = al > 10
    lab, k = ndi.label(m, structure=np.ones((3, 3)))
    for i, s in enumerate(ndi.sum(m, lab, range(1, k + 1)), 1):
        if s < 80: al[lab == i] = 0
    a[..., 3] = al
    ys, xs = np.where(al > 10)
    return Image.fromarray(a.astype('uint8'), 'RGBA').crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

cleaned = dict((k, clean(os.path.join(CH, v + '.png'))) for k, v in USE.items())
king_h = cleaned['king-idle'].height
for mode, target in (('wide', 124), ('room', 248)):
    s = target / king_h
    for k, im in cleaned.items():
        w, h = max(1, round(im.width * s)), max(1, round(im.height * s))
        r = im.resize((w, h), Image.BOX)
        a = np.array(r); a[..., 3] = np.where(a[..., 3] >= 110, 255, 0)
        Image.fromarray(a, 'RGBA').save(os.path.join(OUT, '%s-%s.png' % (mode, k)))
        print(mode, k, (w, h))

# ---------- 背景 ----------
shutil.copy(os.path.join(BG, 'nairobi-arrivals-bit-v3-tall-bg.png'), os.path.join(OUT, 'nairobi-arrivals.png'))
im = np.array(Image.open(os.path.join(BG, 'hotel-front-v2-still.png')).convert('RGB'))
out = im.copy()
out[636:960, 80:760] = im[636:960, 80 + 768:760 + 768]          # 床: 同じ模様(横192pxのタイルのくり返し)を右から写す
yy, xx = np.mgrid[:960, :1536]
hidden = ((xx >= 1230) & (xx < 1322) & (yy >= 172) & (yy < 280)) | ((xx >= 1208) & (xx < 1334) & (yy >= 272) & (yy < 412))   # 店員の頭と体
wall = np.roll(im, -150, axis=1)
out[hidden] = wall[hidden]
out[318:412, 1280:1284] = im[318:412, 1024:1028]                 # 壁のつなぎ目を、絵の下からカウンターまでのばす
DARK, CREAM, SKY, MTN, MTN2, SEA = (58, 50, 42), (238, 232, 214), (168, 192, 208), (96, 128, 102), (74, 106, 82), (140, 170, 190)
def paint(mask, c): out[mask & hidden] = c
fr = lambda x0, y0, x1, y1: (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)
paint(fr(1096, 176, 1290, 318), DARK); paint(fr(1108, 188, 1278, 306), CREAM); paint(fr(1120, 200, 1266, 294), SKY)
step = (yy // 4) * 4
paint(fr(1120, 244, 1266, 282) & (xx < 1220 + (step - 244) + 4), MTN)     # 山の右の斜面(店員でかくれていた所)
paint(fr(1120, 282, 1266, 286), SEA); paint(fr(1120, 286, 1266, 288), SKY); paint(fr(1120, 288, 1266, 294), MTN2)
sun = tuple(int(v) for v in im[227, 1228])
paint(((xx - 1238) ** 2 + (yy - 227) ** 2 <= 14 ** 2) & fr(1120, 200, 1266, 282), sun)
Image.fromarray(out).save(os.path.join(OUT, 'hotel-front.png'))
print('backgrounds done')
