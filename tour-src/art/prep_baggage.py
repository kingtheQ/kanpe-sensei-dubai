# -*- coding: utf-8 -*-
"""ナイロビの手荷物受け取り(バゲージクレーム)の素材から、ゲームで使う画像を作る(タスク045)。
使い方: python3 -I tour-src/art/prep_baggage.py <素材を展開したフォルダ> [出力フォルダ=tour/assets/art]
  展開フォルダには nairobi-baggage-v1.png(1536×960。主ベルトに荷物5個が描き込み済み) と make_nairobi_baggage_bags.py(荷物の描き方) がある。必要: pillow
作るもの(絵は 768×480 の半分の大きさで描き、2倍の NEAREST で拡大する = 素材と同じ粒):
  - nairobi-baggage-base.png    背景。主ベルトを「荷物なし・中央の島なし」に描き直したもの(奥のベルト・壁・床は素材のまま)
  - nairobi-baggage-island.png  中央の島＋緑の広告板(透明つき)。奥側の荷物と手前側の荷物のあいだに重ねる(荷物が島のうしろを通る)
  - nairobi-baggage-bags.png    荷物スプライト(6種×13段階の大きさ。奥ほど小さく暗い)。行=種類、列=奥行き(0=いちばん奥・1=いちばん手前の向きの段階は SIN で引く)
  主ベルトの形と色は、素材のアニメ用スクリプトの carousel_base / island_layer と同じ。描き直しが素材の絵と合っているかは、荷物も島もない場所の画素が
  素材と一致するかで確かめる(ずれたら中止)。
"""
import sys, os, importlib.util
from PIL import Image, ImageDraw
SRC = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tour', 'assets', 'art')
os.makedirs(OUT, exist_ok=True)
spec = importlib.util.spec_from_file_location('bagsmod', os.path.join(SRC, 'make_nairobi_baggage_bags.py'))
bags = importlib.util.module_from_spec(spec); spec.loader.exec_module(bags)
# 素材の背景の色(素材の画素から読んだ値。主ベルトの縁・面・線・島)
STEEL, STEEL_D, STEEL_X, STEEL_L, GREEN = (196, 202, 210), (128, 136, 148), (96, 104, 118), (222, 227, 233), (30, 110, 76)
W, H = 768, 480
CX, CY, RX, RY = 400, 330, 238, 40        # 主ベルト(半分の大きさ)
orig = Image.open(os.path.join(SRC, 'nairobi-baggage-v1.png')).convert('RGB')
assert orig.size == (W * 2, H * 2), orig.size
def carousel_layer():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.ellipse([CX - RX, CY - RY + 10, CX + RX, CY + RY + 34], fill=STEEL_D)
    d.ellipse([CX - RX, CY - RY + 10, CX + RX, CY + RY + 34], outline=STEEL_X, width=2)
    d.ellipse([CX - RX, CY - RY, CX + RX, CY + RY], fill=STEEL)
    for f in (0.82, 0.64, 0.46):
        d.ellipse([CX - RX * f, CY - RY * f, CX + RX * f, CY + RY * f], outline=STEEL_D, width=1)
    d.ellipse([CX - RX, CY - RY, CX + RX, CY + RY], outline=STEEL_X, width=2)
    return img
def island_layer():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    irx, iry = RX * 0.52, RY * 0.52
    d.ellipse([CX - irx, CY - iry - 8, CX + irx, CY + iry - 2], fill=STEEL_L)
    d.ellipse([CX - irx, CY - iry - 8, CX + irx, CY + iry - 2], outline=STEEL_D, width=1)
    pw = int(irx * 1.1)
    d.rounded_rectangle([CX - pw // 2, CY - 6, CX + pw // 2, CY + int(iry * 0.62)], 3, fill=GREEN)
    d.rounded_rectangle([CX - pw // 2, CY - 6, CX + pw // 2, CY + int(iry * 0.62)], 3, outline=STEEL_X, width=1)
    return img
up = lambda im: im.resize((W * 2, H * 2), Image.NEAREST)
car, isl = up(carousel_layer()), up(island_layer())
base = orig.convert('RGBA'); base.alpha_composite(car)
# --- 確かめ: 荷物も島もない場所で、描き直しが素材と一致するか ---
full = orig.convert('RGBA'); full.alpha_composite(car); full.alpha_composite(isl)   # 荷物のないところは素材と同じになるはず
import numpy as np
a, b = np.array(orig).astype(int), np.array(full.convert('RGB')).astype(int)
diff = (np.abs(a - b).sum(axis=2) > 0)
# 素材の主ベルトの荷物5個(半分の大きさの足もと)の外わく(のりしろ込み)
BAGS = [(236, 344), (300, 352), (486, 350), (556, 342), (424, 356)]
m = np.zeros(diff.shape, bool)
for (x, y) in BAGS:
    m[max(0, (y - 52) * 2):(y + 12) * 2, max(0, (x - 24) * 2):(x + 24) * 2] = True
print('描き直しと素材の画素が合わない数(荷物の外):', int((diff & ~m).sum()), '/ 荷物の中:', int((diff & m).sum()))
assert int((diff & ~m).sum()) == 0, '主ベルトの描き直しが素材と合いません'
base.convert('RGB').save(os.path.join(OUT, 'nairobi-baggage-base.png')); print('nairobi-baggage-base.png', base.size)
box = isl.getbbox()   # 島の外わく(全体の大きさでの座標)
isl.crop(box).save(os.path.join(OUT, 'nairobi-baggage-island.png')); print('nairobi-baggage-island.png box', box)
# --- 荷物スプライト: 素材の bag_params と同じ。s=0.86+0.14 sin、暗さ=0.925+0.075 sin(sin=-1 奥 … +1 手前)を13段階で ---
NLV = 13
CW, CH, PAD = 56, 52, 6           # 1コマ(半分の大きさ)。足もと(接地点)は下から PAD の高さ、横は中央
sheet = Image.new('RGBA', (CW * NLV, CH * len(bags.DESIGNS)), (0, 0, 0, 0)); d = ImageDraw.Draw(sheet)
for di in range(len(bags.DESIGNS)):
    kind = bags.DESIGNS[di][0]
    bw, bh = bags.FRONT_DUFFEL if kind == 'duffel' else bags.FRONT
    for li in range(NLV):
        sn = -1 + 2.0 * li / (NLV - 1)
        s, dimf = 0.86 + 0.14 * sn, 0.925 + 0.075 * sn
        w, h = int(round(bw * s)), int(round(bh * s))
        bags.draw_bag(d, li * CW + CW // 2, di * CH + CH - PAD, w, h, di, dimf)
sheet = sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST)
sheet.save(os.path.join(OUT, 'nairobi-baggage-bags.png')); print('nairobi-baggage-bags.png', sheet.size, '1コマ(2倍)', (CW * 2, CH * 2), '段階', NLV, '種類', len(bags.DESIGNS))
