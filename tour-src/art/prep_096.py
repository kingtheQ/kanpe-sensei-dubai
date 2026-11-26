# -*- coding: utf-8 -*-
"""タスク096: チューリッヒの発車標の別素材(フランクフルト行きの1行)。
背景 zurich-arrival-v1.png の大発車標は、見出しと欄見出しだけで行の中身は暗い質感(動くもの・変わるものは別素材の恒常ルール)。
この1行を、Fernverkehr(赤い見出し)の最初の行の位置(x=232,y=226。432x44)に重ねる静止の重ね絵にする。
 - 行き先 'Frankfurt (Main) Hbf' と、Gleis の欄の番号だけ。発車時刻は出さない(096指示書)。
 - 番号 9 は物語の中の架空(背景の zurich-departure-v1 の9番線=灰色の列車に合わせた。実在の割り当てではない)。
 - 描き方は背景と同じ: 768x480 の粒で描き、NEAREST で2倍(粒2px)。
使い方: python3 tour-src/art/prep_096.py"""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'tour/assets/art/zurich-board-fra-v1.png')
W, H = 216, 22                       # 768x480 での大きさ(出力は 432x44)。スマホで読めるよう、行は大きめに描く
BG = (0, 70, 160)                     # 背景の発車標の青(実測)
WHITE = (240, 244, 250); YEL = (255, 214, 64)
im = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(im); d.fontmode = '1'      # アンチエイリアスなし(粒をそろえる)
fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)
fn = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
d.rectangle((0, 0, W - 1, H - 2), fill=(8, 84, 182))   # 行の帯(この行だけ明るい)
d.text((8, 4), 'Frankfurt (Main) Hbf', font=fb, fill=WHITE)
d.text((151, 1), '9', font=fn, fill=YEL)      # 欄見出し Gleis(全体 x=536 ≒ 重ね絵の x=536-232=304 → 768の粒で152)の下
# 行の下の細い区切り線(背景の行の質感と同じ明るさ)
for x in range(0, W, 1):
    if x % 3: d.point((x, H - 1), fill=(16, 66, 138))
out = im.resize((W * 2, H * 2), Image.NEAREST)
out.save(OUT, optimize=True); print(OUT, out.size)
