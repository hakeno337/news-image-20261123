#!/usr/bin/env python3
"""Compose this entry's image: the front page of THE WORLD TODAY for Monday 23 November 2026.

The day's stories were gathered from the day's reporting (COP31's collapse in Antalya, the AI
sell-off in world markets, the Dymer strike, the US House result, the Hormuz tanker fires, and a
ticker of the Banten factory fire, Marquez's eighth MotoGP title and Alcaraz's ATP Finals win) and
set as a broadsheet front page with PIL, so every headline is crisp and legible at 1024x1024.
Run: python3 compose.py  (writes entry.png beside this file)
"""
from PIL import Image, ImageDraw, ImageFont

W = 1024
PAPER = (246, 241, 231)
INK = (20, 18, 14)
RED = (179, 39, 30)
GREY = (92, 84, 74)
BODY = (46, 42, 36)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

img = Image.new("RGB", (W, W), PAPER)
d = ImageDraw.Draw(img)
M = 56
RIGHT = W - M


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(s, f):
    return d.textbbox((0, 0), s, font=f)[2]


def fit_font(path, s, size, max_w):
    while size > 10 and text_w(s, font(path, size)) > max_w:
        size -= 2
    return font(path, size)


def centered(s, f, y, fill=INK):
    d.text(((W - text_w(s, f)) / 2, y), s, font=f, fill=fill)
    return y + f.size


def wrap(s, f, width):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(t, f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(x, y, lines, f, fill=INK, leading=1.16):
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += int(f.size * leading)
    return y


# ---------- masthead ----------
y = 30
centered("M O N D A Y   ·   2 3   N O V E M B E R   2 0 2 6", font(SANS_B, 24), y, GREY)
y += 40
d.line([(M, y), (RIGHT, y)], fill=INK, width=3)
y += 14
mast = fit_font(SERIF_B, "THE WORLD TODAY", 96, RIGHT - M)
centered("THE WORLD TODAY", mast, y)
y += mast.size + 22
d.line([(M, y), (RIGHT, y)], fill=INK, width=7)
d.line([(M, y + 11), (RIGHT, y + 11)], fill=INK, width=2)
y += 30

# ---------- lead story ----------
d.rectangle([M, y + 3, M + 10, y + 27], fill=RED)
d.text((M + 22, y), "CLIMATE  ·  ANTALYA, TURKEY", font=font(SANS_B, 25), fill=RED)
y += 40
lead_f = font(SERIF_B, 54)
y = block(M, y, wrap("COP31 climate talks end without a deal", lead_f, RIGHT - M), lead_f, leading=1.12)
y += 6
sub_f = font(SANS, 26)
y = block(M, y, wrap(
    "The EU and some 130 nations reject a draft that never mentions fossil fuels; "
    "the summit closes with no agreement.", sub_f, RIGHT - M), sub_f, fill=BODY, leading=1.2)
y += 16
d.line([(M, y), (RIGHT, y)], fill=INK, width=2)
y += 24

# ---------- 2x2 grid ----------
COL_W = (RIGHT - M - 36) // 2
col_x = [M, M + COL_W + 36]
stories = [
    ("MARKETS · TOKYO", "AI sell-off rattles world markets",
     "Japan's Nikkei falls 5.06% and the S&P 500 drops 3.7% as AI-bubble fears bite. Gold jumps 2.7%."),
    ("UKRAINE · DYMER", "Russian strike kills at least 10",
     "A missile hits an apartment block north of Kyiv. Rescuers pull a boy of 7 alive from the rubble."),
    ("WASHINGTON", "Democrats win biggest House majority since 1992",
     "At least 258 seats clinched, after a North Carolina recount flips the final race."),
    ("STRAIT OF HORMUZ", "Tankers ablaze as Iran defies US blockade",
     "Two supertankers catch fire near Hormuz; Tehran vows to use \u201call its tools\u201d in reply."),
]
kick_f = font(SANS_B, 22)
head_f = font(SERIF_B, 31)
body_f = font(SANS, 23)
row_y = y
row_h = 0
for idx, (kick, head, body) in enumerate(stories):
    x = col_x[idx % 2]
    if idx == 2:
        row_y += row_h + 26
        d.line([(M, row_y - 15), (RIGHT, row_y - 15)], fill=(196, 188, 172), width=2)
        row_h = 0
    yy = row_y
    d.rectangle([x, yy + 3, x + 8, yy + 23], fill=RED)
    d.text((x + 18, yy), kick, font=kick_f, fill=RED)
    yy += 33
    yy = block(x, yy, wrap(head, head_f, COL_W), head_f, leading=1.14)
    yy += 4
    yy = block(x, yy, wrap(body, body_f, COL_W), body_f, fill=BODY, leading=1.22)
    row_h = max(row_h, yy - row_y)
y = row_y + row_h + 20

# ---------- bottom ticker ----------
BAND = 104
d.rectangle([0, W - BAND, W, W], fill=INK)
tick_f = font(SANS_B, 23)
ticker = ("ALSO TODAY:  Banten factory fire kills 24 in Indonesia  ·  M\u00e1rquez wins eighth MotoGP title, "
          "equalling Agostini  ·  Alcaraz beats Zverev for his first ATP Finals crown")
ty = W - BAND + 13
for ln in wrap(ticker, tick_f, RIGHT - M):
    d.text((M, ty), ln, font=tick_f, fill=PAPER)
    ty += 30

img.save(__file__.rsplit("/", 1)[0] + "/entry.png", optimize=True)
print("saved; content bottom at y =", y, "; ticker starts at", W - BAND)
