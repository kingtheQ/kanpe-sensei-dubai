#!/usr/bin/env python3
"""Baggage sprites for the Nairobi baggage-claim carousel animation.
Drawn at 768x480 half-scale and upscaled x2 NEAREST, exactly like the
background (make_nairobi_baggage_v1.py), so the grain (2px) and palette
match. Six designs, each in two native sizes:
  front size - for the near edge of the belt
  back size  - for the far edge (drawn natively smaller, not rescaled,
               so the pixel grain stays honest)
Anchor of every sprite = bottom centre of its cell (the contact point
with the belt surface).

Designs: 0 white hard-shell, 1 navy soft, 2 red hard-shell,
         3 mustard soft, 4 teal hard-shell, 5 brown duffel.
Colours reuse the suitcases already painted in nairobi-baggage-v1.png.
"""
from PIL import Image, ImageDraw
import os

BASE = os.path.expanduser("~/workspace/goals/kanpe-sensei-airport-english-game/files")
BGD = os.path.join(BASE, "backgrounds")

# (kind, body, trim) - same colours as the still background's suitcases
DESIGNS = [
    ("hard",   (233, 233, 230), (150, 152, 156)),   # 0 white hard-shell
    ("soft",   (40, 48, 70),    (18, 22, 34)),      # 1 navy soft
    ("hard",   (168, 44, 44),   (104, 26, 26)),     # 2 red hard-shell
    ("soft",   (196, 150, 52),  (128, 94, 30)),     # 3 mustard soft
    ("hard",   (38, 92, 88),    (20, 54, 52)),      # 4 teal hard-shell
    ("duffel", (96, 64, 44),    (64, 42, 28)),      # 5 brown duffel
]

FRONT = (32, 38)        # suitcase w,h at half-scale (front edge)
BACK = (23, 27)         # suitcase w,h at half-scale (back edge)
FRONT_DUFFEL = (42, 24)
BACK_DUFFEL = (30, 17)

CELL_A = (48, 56)       # front-row cell (half-scale)
CELL_B = (36, 42)       # back-row cell (half-scale)


def _dim(c, f):
    return tuple(max(0, min(255, int(round(v * f)))) for v in c)


def draw_bag(d, cx, base, w, h, design, dimf=1.0):
    """Draw one bag. (cx, base) = bottom centre (contact point)."""
    kind, body, trim = DESIGNS[design]
    body, trim = _dim(body, dimf), _dim(trim, dimf)
    x0, x1 = cx - w // 2, cx + w // 2
    y0 = base - h
    if kind == "duffel":
        d.rounded_rectangle([x0, y0, x1, base], max(3, h // 4), fill=body)
        d.rounded_rectangle([x0, y0, x1, base], max(3, h // 4), outline=trim, width=1)
        # two straps + top seam
        for fx in (0.3, 0.7):
            sx = int(x0 + w * fx)
            d.line([sx, y0 + 2, sx, base - 2], fill=trim, width=1)
        d.line([x0 + 3, y0 + h // 3, x1 - 3, y0 + h // 3], fill=trim, width=1)
        # carry handle
        hw = max(4, w // 5)
        d.line([cx - hw, y0, cx - hw, y0 - 3], fill=trim, width=1)
        d.line([cx + hw, y0, cx + hw, y0 - 3], fill=trim, width=1)
        d.line([cx - hw, y0 - 3, cx + hw, y0 - 3], fill=trim, width=1)
        return
    # suitcase (hard / soft), same construction as the background's suitcase()
    d.rounded_rectangle([x0, y0, x1, base], 3, fill=body)
    d.rounded_rectangle([x0, y0, x1, base], 3, outline=trim, width=1)
    d.line([x0 + 3, y0 + 4, x1 - 3, y0 + 4], fill=trim, width=1)      # lid seam
    if kind == "hard":
        for fx in (0.28, 0.5, 0.72):                                  # shell ridges
            sx = int(x0 + w * fx)
            d.line([sx, y0 + 6, sx, base - 4], fill=trim, width=1)
    else:  # soft: front pocket
        d.rectangle([x0 + 4, y0 + h // 2, x1 - 4, base - 5], outline=trim, width=1)
        d.line([x0 + 4, y0 + h // 2 + 3, x1 - 4, y0 + h // 2 + 3], fill=trim, width=1)
    d.rectangle([cx - 4, y0 - 4, cx + 4, y0 - 1], outline=trim, width=1)  # handle
    d.ellipse([x0 + 2, base - 3, x0 + 6, base + 1], fill=trim)        # wheels
    d.ellipse([x1 - 6, base - 3, x1 - 2, base + 1], fill=trim)


def bag_image(design, w, h):
    """One bag on a transparent half-scale canvas, anchor bottom-centre."""
    pad = 6
    img = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    draw_bag(d, (w + pad * 2) // 2, h + pad, w, h, design)
    return img


def build_sheet():
    cols = len(DESIGNS)
    sw = cols * CELL_A[0]
    sh = CELL_A[1] + CELL_B[1]
    sheet = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    d = ImageDraw.Draw(sheet)
    for i in range(cols):
        kind = DESIGNS[i][0]
        w, h = FRONT_DUFFEL if kind == "duffel" else FRONT
        draw_bag(d, i * CELL_A[0] + CELL_A[0] // 2, CELL_A[1] - 2, w, h, i)
        w2, h2 = BACK_DUFFEL if kind == "duffel" else BACK
        draw_bag(d, i * CELL_B[0] + CELL_B[0] // 2, sh - 2, w2, h2, i)
    out = sheet.resize((sw * 2, sh * 2), Image.NEAREST)
    path = os.path.join(BGD, "nairobi-baggage-bags.png")
    out.save(path)
    print("saved", path, out.size)


if __name__ == "__main__":
    build_sheet()
