#!/usr/bin/env python3
"""Animated preview GIF for the Nairobi baggage-claim carousel:
bags ride around the main belt (front edge left -> right, back edge
right -> left), passing behind the centre island, smaller and dimmer
on the far side. Layered build reuses make_nairobi_baggage_v1.build()
with the main carousel's island and painted bags removed, then the
island is composited between the back-half and front-half bags.
King & Lulu (existing repo sprites) stand where the still preview
puts them. 768x480, 60 frames x 120 ms = 7.2 s per revolution
(sped up for the preview; the in-game recommendation is ~24 s)."""
from PIL import Image, ImageDraw
import importlib.util
import math
import os

BASE = os.path.expanduser("~/workspace/goals/kanpe-sensei-airport-english-game/files")
BGD = os.path.join(BASE, "backgrounds")
NPC_REPO = os.path.expanduser("~/workspace/kanpe-repo/tour/assets/art/npc")


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(BGD, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bg = _load("make_nairobi_baggage_v1")
bags = _load("make_nairobi_baggage_bags")

# main carousel geometry (half-scale), from make_nairobi_baggage_v1
CX, CY, RX, RY = 400, 330, 238, 40
PATH_RX, PATH_RY = 178, 28            # ellipse the bags' contact points follow
MAIN_BELT_BAGS = {(236, 344), (300, 352), (486, 350), (556, 342), (424, 356)}

NFRAMES = 60
DURATION = 120                        # ms per frame -> 7.2 s / revolution


def carousel_base(d, cx, cy, rx, ry, dim=0):
    """Main carousel without the centre island (bags pass behind it)."""
    sh = lambda c: tuple(max(0, v - dim) for v in c)
    d.ellipse([cx - rx, cy - ry + 10, cx + rx, cy + ry + 34], fill=sh(bg.STEEL_D))
    d.ellipse([cx - rx, cy - ry + 10, cx + rx, cy + ry + 34], outline=sh(bg.STEEL_X), width=2)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=sh(bg.STEEL))
    for f in (0.82, 0.64, 0.46):
        d.ellipse([cx - rx * f, cy - ry * f, cx + rx * f, cy + ry * f], outline=sh(bg.STEEL_D), width=1)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=sh(bg.STEEL_X), width=2)


def island_layer():
    """Centre island + ad panel on a transparent layer."""
    img = Image.new("RGBA", (bg.W, bg.H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    irx, iry = RX * 0.52, RY * 0.52
    d.ellipse([CX - irx, CY - iry - 8, CX + irx, CY + iry - 2], fill=bg.STEEL_L)
    d.ellipse([CX - irx, CY - iry - 8, CX + irx, CY + iry - 2], outline=bg.STEEL_D, width=1)
    pw = int(irx * 1.1)
    d.rounded_rectangle([CX - pw // 2, CY - 6, CX + pw // 2, CY + int(iry * 0.62)], 3,
                        fill=(30, 110, 76))
    d.rounded_rectangle([CX - pw // 2, CY - 6, CX + pw // 2, CY + int(iry * 0.62)], 3,
                        outline=bg.STEEL_X, width=1)
    return img


def build_base():
    orig_carousel, orig_suitcase = bg.carousel, bg.suitcase

    def carousel_wrap(d, cx, cy, rx, ry, scale=1.0, dim=0):
        if cx == CX and cy == CY:
            carousel_base(d, cx, cy, rx, ry, dim)
        else:
            orig_carousel(d, cx, cy, rx, ry, scale, dim)

    def suitcase_wrap(d, x, y, w, h, body, trim):
        if (x, y) in MAIN_BELT_BAGS:
            return
        orig_suitcase(d, x, y, w, h, body, trim)

    bg.carousel, bg.suitcase = carousel_wrap, suitcase_wrap
    try:
        return bg.build().convert("RGBA")
    finally:
        bg.carousel, bg.suitcase = orig_carousel, orig_suitcase


def characters_layer():
    img = Image.new("RGBA", (bg.W, bg.H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    feet = 442  # 884 at full scale, as in the still preview
    for name, cx in (("hall-lulu-back.png", 358), ("hall-king-back.png", 400)):
        spr = Image.open(os.path.join(NPC_REPO, name)).convert("RGBA")
        spr = spr.resize((spr.width // 2, spr.height // 2), Image.NEAREST)
        d.ellipse([cx - spr.width // 2 - 4, feet - 4, cx + spr.width // 2 + 4, feet + 2],
                  fill=(10, 14, 26, 110))
        img.paste(spr, (cx - spr.width // 2, feet - spr.height), spr)
    return img


def bag_params(theta, design):
    s = 0.86 + 0.14 * math.sin(theta)          # 1.00 front, 0.72 back
    dimf = 0.925 + 0.075 * math.sin(theta)     # 1.00 front, 0.85 back
    kind = bags.DESIGNS[design][0]
    bw, bh = bags.FRONT_DUFFEL if kind == "duffel" else bags.FRONT
    return int(round(bw * s)), int(round(bh * s)), dimf


def make_gif():
    base = build_base()
    island = island_layer()
    chars = characters_layer()
    frames = []
    for f in range(NFRAMES):
        frame = base.copy()
        d = ImageDraw.Draw(frame)
        items = []
        for i in range(len(bags.DESIGNS)):
            theta = i * math.tau / len(bags.DESIGNS) - math.tau * f / NFRAMES
            x = CX + PATH_RX * math.cos(theta)
            y = CY + PATH_RY * math.sin(theta)
            items.append((math.sin(theta), x, y, theta, i))
        for want_back in (True, False):
            group = sorted((it for it in items if (it[0] < 0) == want_back),
                           key=lambda it: it[0])
            for _, x, y, theta, i in group:
                w, h, dimf = bag_params(theta, i)
                bags.draw_bag(d, int(round(x)), int(round(y)), w, h, i, dimf)
            if want_back:
                frame.alpha_composite(island)
                d = ImageDraw.Draw(frame)
        frame.alpha_composite(chars)
        frames.append(frame.convert("RGB"))
    out = os.path.join(BGD, "nairobi-baggage-anim.gif")
    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=DURATION, loop=0)
    print("saved", out, frames[0].size, len(frames), "frames")


if __name__ == "__main__":
    make_gif()
