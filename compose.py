#!/usr/bin/env python3
"""Compose the entry image for 'Sum up 23 November's world news in one
image' (news-image-20261123), second version.

The page is a broadsheet front page rebuilt around pictures: a black
date band makes Monday 23 November 2026 unmissable, the lead story
(COP31 ends without a deal) carries a drawn globe-and-thermometer
illustration, and each of the four grid stories gets a small icon
tile beside its headline, so every story reads from its picture as
well as its words. An ALSO TODAY strip closes the page with the
Banten factory fire and the day's two sports results.

Everything is drawn with PIL at twice size and downscaled, and the
result is written as entry.png beside this script: 1024 by 1024,
well under the gate's 1 MiB cap."""

import math
import os

from PIL import Image, ImageDraw, ImageFont

S = 2                       # supersample factor for clean edges
W = H = 1024
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (246, 241, 229)
INK = (18, 20, 22)
BODY = (52, 58, 64)
RED = (176, 42, 32)
WHITE = (255, 255, 255)

img = Image.new("RGB", (W * S, H * S), PAPER)
d = ImageDraw.Draw(img)


def F(path, size):
    return ImageFont.truetype(path, int(size * S))


def pts(seq):
    return [(x * S, y * S) for x, y in seq]


def text(x, y, s, font, fill, anchor="la"):
    d.text((x * S, y * S), s, font=font, fill=fill, anchor=anchor)


def wrap(s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw * S:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(s, path, start, minimum, maxw, max_lines):
    """Largest size, down from start, whose wrap fits max_lines."""
    size = start
    while size > minimum:
        f = F(path, size)
        if len(wrap(s, f, maxw)) <= max_lines:
            return f
        size -= 1
    return F(path, minimum)


# ------------------------------------------------------------------ masthead
text(512, 22, "THE WORLD TODAY", F(SERIF_B, 54), INK, anchor="ma")
d.line(pts([(36, 98), (988, 98)]), fill=INK, width=3 * S)
d.line(pts([(36, 105), (988, 105)]), fill=INK, width=S)

# ------------------------------------------------------------------ date band
d.rectangle(pts([(0, 116), (1024, 196)]), fill=INK)
text(512, 131, "MONDAY · 23 NOVEMBER · 2026", F(SANS_B, 52), WHITE,
     anchor="ma")

# ------------------------------------------------------------------ lead art
PX0, PY0, PX1, PY1 = 36, 212, 420, 552
d.rectangle(pts([(PX0, PY0), (PX1, PY1)]), fill=(220, 235, 242))
d.rectangle(pts([(PX0, PY0), (PX1, PY1)]), outline=INK, width=3 * S)

# The globe is drawn on its own layer, then pasted through a round mask.
GS = 256
globe = Image.new("RGBA", (GS * S, GS * S), (0, 0, 0, 0))
gd = ImageDraw.Draw(globe)
gd.ellipse([0, 0, GS * S, GS * S], fill=(47, 111, 143, 255))
LAND_G = (110, 158, 84, 255)
LAND_G2 = (127, 172, 94, 255)


def gpoly(seq, fill):
    gd.polygon([(x * S, y * S) for x, y in seq], fill=fill)


gpoly([(38, 84), (66, 66), (92, 74), (88, 104), (74, 128), (80, 160),
       (64, 186), (46, 160), (34, 120)], LAND_G)                    # N America
gpoly([(70, 168), (92, 178), (88, 208), (72, 224), (62, 200),
       (62, 180)], LAND_G2)                                          # S America
gpoly([(118, 120), (146, 110), (162, 128), (156, 164), (140, 188),
       (124, 166), (114, 140)], LAND_G)                              # Africa
gpoly([(110, 44), (170, 30), (224, 44), (236, 74), (210, 96),
       (168, 92), (140, 74), (116, 64)], LAND_G2)                    # Eurasia
gpoly([(188, 178), (218, 172), (226, 190), (204, 202),
       (188, 194)], LAND_G)                                          # Australia
for rx in (42, 84):
    gd.ellipse([(128 - rx) * S, 4 * S, (128 + rx) * S, (GS - 4) * S],
               outline=(159, 195, 212, 255), width=2 * S)
gd.ellipse([4 * S, 4 * S, (GS - 4) * S, (GS - 4) * S],
           outline=(159, 195, 212, 255), width=2 * S)
for gy in (86, 128, 170):
    gd.line([(6 * S, gy * S), ((GS - 6) * S, gy * S)],
            fill=(159, 195, 212, 255), width=2 * S)
mask = Image.new("L", (GS * S, GS * S), 0)
ImageDraw.Draw(mask).ellipse([0, 0, GS * S, GS * S], fill=255)
img.paste(globe, (100 * S, 257 * S), mask)
d.ellipse(pts([(100, 257), (356, 513)]), outline=INK, width=3 * S)

# A small sun in the panel's empty top-left sky: heat, unambiguously.
SCX, SCY = 72, 238
for i in range(8):
    a = math.pi * i / 4
    d.line(pts([(SCX + 15 * math.cos(a), SCY + 15 * math.sin(a)),
                (SCX + 20 * math.cos(a), SCY + 20 * math.sin(a))]),
           fill=(224, 123, 57), width=3 * S)
d.ellipse(pts([(SCX - 11, SCY - 11), (SCX + 11, SCY + 11)]),
          fill=(245, 176, 65), outline=(224, 123, 57), width=2 * S)

# Thermometer with its mercury high: a warming world, drawn simply.
TX = 374
d.rounded_rectangle(pts([(TX - 8, 262), (TX + 8, 452)]), radius=8 * S,
                    fill=WHITE, outline=INK, width=3 * S)
d.rectangle(pts([(TX - 4, 292), (TX + 4, 452)]), fill=(196, 48, 38))
d.ellipse(pts([(TX - 19, 438), (TX + 19, 476)]), fill=(196, 48, 38),
          outline=INK, width=3 * S)
for ty in (292, 332, 372, 412):
    d.line(pts([(TX + 12, ty), (TX + 24, ty)]), fill=INK, width=2 * S)
text(228, 516, "THE CLIMATE SUMMIT", F(SANS_B, 17), (90, 104, 112),
     anchor="ma")

# ------------------------------------------------------------------ lead text
text(444, 218, "CLIMATE · ANTALYA, TURKEY", F(SANS_B, 25), RED)
hf = F(SERIF_B, 50)
hy = 256
for ln in wrap("COP31 climate talks end without a deal", hf, 544):
    text(444, hy, ln, hf, INK)
    hy += 58
sy = hy + 12
sf = F(SANS, 26)
for ln in wrap("The EU and some 130 nations reject a draft that never "
               "mentions fossil fuels; the summit closes with no "
               "agreement.", sf, 544):
    text(444, sy, ln, sf, BODY)
    sy += 33

d.line(pts([(36, 566), (988, 566)]), fill=INK, width=2 * S)

# ------------------------------------------------------------------ grid icons
def tile(x, y, bg):
    d.rounded_rectangle(pts([(x, y), (x + 96, y + 96)]), radius=10 * S,
                        fill=bg)


def icon_markets(x, y):
    """A red line falling off a cliff edge: the sell-off."""
    tile(x, y, (32, 48, 60))
    line = [(x + 14, y + 26), (x + 32, y + 40), (x + 46, y + 31),
            (x + 64, y + 55), (x + 80, y + 44)]
    d.line(pts(line), fill=(224, 82, 82), width=6 * S)
    d.polygon(pts([(x + 80, y + 44), (x + 66, y + 46), (x + 78, y + 58)]),
              fill=(224, 82, 82))
    d.line(pts([(x + 14, y + 76), (x + 82, y + 76)]),
           fill=(140, 164, 178), width=2 * S)


def icon_ukraine(x, y):
    """A lit apartment block and the burst of the strike that hit it."""
    tile(x, y, (90, 107, 122))
    d.rectangle(pts([(x + 24, y + 28), (x + 58, y + 84)]), fill=(40, 50, 60))
    for r in range(3):
        for c in range(2):
            d.rectangle(pts([(x + 31 + c * 13, y + 36 + r * 15),
                             (x + 39 + c * 13, y + 44 + r * 15)]),
                        fill=(255, 217, 122))
    cx, cy = x + 72, y + 24
    star = []
    for i in range(16):
        r = 13 if i % 2 == 0 else 5
        a = math.pi * i / 8
        star.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts(star), fill=(240, 140, 46))


def icon_washington(x, y):
    """The Capitol dome: the House whose majority was settled today."""
    tile(x, y, (39, 65, 86))
    d.rectangle(pts([(x + 18, y + 74), (x + 78, y + 81)]), fill=WHITE)
    for cx in (28, 40, 52, 64):
        d.line(pts([(x + cx, y + 60), (x + cx, y + 74)]), fill=WHITE,
               width=3 * S)
    d.rectangle(pts([(x + 16, y + 55), (x + 80, y + 60)]), fill=WHITE)
    d.pieslice(pts([(x + 28, y + 28), (x + 68, y + 62)]), start=180, end=0,
               fill=WHITE)
    d.rectangle(pts([(x + 46, y + 20), (x + 50, y + 30)]), fill=WHITE)
    d.ellipse(pts([(x + 45, y + 15), (x + 51, y + 21)]), fill=WHITE)


def icon_hormuz(x, y):
    """A tanker silhouette with a flame above it, on wavy water."""
    tile(x, y, (31, 95, 110))
    flame = [(x + 40, y + 12), (x + 48, y + 26), (x + 50, y + 36),
             (x + 44, y + 44), (x + 36, y + 40), (x + 34, y + 28)]
    d.polygon(pts(flame), fill=(240, 140, 46))
    d.ellipse(pts([(x + 39, y + 30), (x + 46, y + 40)]),
              fill=(255, 205, 84))
    d.polygon(pts([(x + 14, y + 62), (x + 82, y + 62), (x + 72, y + 76),
                   (x + 24, y + 76)]), fill=(24, 34, 42))
    d.rectangle(pts([(x + 30, y + 52), (x + 64, y + 62)]),
                fill=(24, 34, 42))
    d.rectangle(pts([(x + 54, y + 42), (x + 64, y + 52)]),
                fill=(24, 34, 42))
    for wy in (y + 82, y + 89):
        d.arc(pts([(x + 12, wy - 5), (x + 44, wy + 5)]), 0, 180,
              fill=(159, 212, 222), width=2 * S)
        d.arc(pts([(x + 48, wy - 5), (x + 84, wy + 5)]), 0, 180,
              fill=(159, 212, 222), width=2 * S)


def cell(x, y, icon, kicker, headline, summary):
    icon(x, y + 30)
    tx = x + 112
    tw = 468 - 112
    text(tx, y + 6, kicker, F(SANS_B, 20), RED)
    hf = fit(headline, SERIF_B, 29, 23, tw, 2)
    hy = y + 36
    for ln in wrap(headline, hf, tw):
        text(tx, hy, ln, hf, INK)
        hy += 33
    sf = fit(summary, SANS, 21, 19, tw, 2)
    sy = hy + 5
    for ln in wrap(summary, sf, tw):
        text(tx, sy, ln, sf, BODY)
        sy += 26


cell(36, 580, icon_markets, "MARKETS · TOKYO",
     "AI sell-off rattles world markets",
     "Nikkei \u22125.06%, S&P 500 \u22123.7% on AI-bubble fears; gold +2.7%.")
cell(520, 580, icon_ukraine, "UKRAINE · DYMER",
     "Russian strike kills at least 10",
     "Missile hits apartment block north of Kyiv; boy, 7, alive.")
cell(36, 748, icon_washington, "WASHINGTON",
     "Democrats win biggest House majority since 1992",
     "At least 258 seats; North Carolina recount flips final race.")
cell(520, 748, icon_hormuz, "STRAIT OF HORMUZ",
     "Tankers ablaze as Iran defies US blockade",
     "Two supertankers ablaze; Tehran vows to use \u201call its tools\u201d.")

d.line(pts([(36, 740), (988, 740)]), fill=(196, 188, 168), width=S)
d.line(pts([(512, 592), (512, 904)]), fill=(196, 188, 168), width=S)

# ------------------------------------------------------------------ also strip
d.rectangle(pts([(0, 928), (1024, 1024)]), fill=INK)
strip = ("Banten factory fire kills 24 in Indonesia · Márquez wins eighth "
         "MotoGP title, equalling Agostini · Alcaraz beats Zverev for his "
         "first ATP Finals crown")
sf2 = F(SANS, 21)
lines = wrap(strip, sf2, 830)
lx = 36 + d.textlength("ALSO TODAY   ", font=F(SANS_B, 21)) / S
text(36, 946, "ALSO TODAY", F(SANS_B, 21), (232, 163, 61))
ly = 946
for ln in lines:
    text(lx, ly, ln, sf2, WHITE)
    ly += 26

# ------------------------------------------------------------------ save
img = img.resize((W, H), Image.LANCZOS)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
