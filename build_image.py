#!/usr/bin/env python3
"""Build the 1024x1024 'world news of 25 Nov 2026 in one image' artwork.

Deterministic: pure PIL drawing, fixed geometry, no randomness, no clock.
Output: world-news-2026-11-25.png next to this script.

Stories are the real world news of Wednesday 25 November 2026, researched
on the day from Reuters, Xinhua, AP/AFP, PM.gov.au and market wires; see
NEWS_SOURCES.md for the source headline behind every panel.

Design: newspaper front page. The lead story has a drawn launch scene;
every grid panel carries a small pictogram on a coloured band, so the
page reads visually as well as in text.
"""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "world-news-2026-11-25.png")

W = H = 1024
PAPER = (247, 243, 234)
INK = (20, 24, 38)
MUTED = (92, 96, 110)
CARD = (255, 255, 255)
ACCENT = (178, 34, 52)      # headline red
SPACE = (16, 24, 54)
EARTH = (46, 110, 168)
FLAME = (232, 116, 32)
WHITE = (235, 238, 250)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def centered(text, font, y, fill=INK):
    d.text(((W - d.textlength(text, font=font)) / 2, y), text, font=font, fill=fill)


# ---------- masthead ----------
centered("THE WORLD IN ONE IMAGE", F(SERIF_B, 58), 26)
centered("Wednesday, 25 November 2026  ·  The day's biggest stories, in a single picture",
         F(SANS, 24), 102, MUTED)
d.line([(36, 148), (W - 36, 148)], fill=INK, width=4)
d.line([(36, 156), (W - 36, 156)], fill=INK, width=1)

# ---------- lead story ----------
lead = (36, 168, W - 36, 424)
d.rounded_rectangle(lead, radius=14, fill=CARD, outline=INK, width=3)
# launch scene (left): night sky, stars, Earth arc, rocket climbing.
sx0, sy0, sx1, sy1 = 56, 188, 356, 404
scene = Image.new("RGB", (sx1 - sx0, sy1 - sy0), SPACE)
s = ImageDraw.Draw(scene)
SW, SH = sx1 - sx0, sy1 - sy0
# stars (fixed positions, no randomness)
stars = [(18, 16), (58, 40), (96, 12), (140, 34), (188, 14), (232, 44),
         (268, 18), (24, 84), (70, 66), (250, 78), (282, 58), (150, 62),
         (200, 90), (40, 120)]
for px, py in stars:
    s.ellipse((px, py, px + 5, py + 5), fill=WHITE)
# Earth arc at the bottom
s.ellipse((-60, SH - 92, SW + 60, SH + 130), fill=EARTH)
s.ellipse((30, SH - 78, 120, SH - 40), fill=(74, 148, 96))
s.ellipse((170, SH - 70, 268, SH - 34), fill=(74, 148, 96))
# rocket body, nose cone, fins, flame
rx, ry = 128, 42          # top-left of the rocket body
s.polygon([(rx + 4, ry), (rx + 36, ry), (rx + 20, ry - 26)], fill=(206, 212, 222), outline=INK)
s.rectangle((rx + 4, ry, rx + 36, ry + 96), fill=(236, 238, 244), outline=INK, width=2)
s.rectangle((rx + 4, ry + 34, rx + 36, ry + 58), fill=ACCENT)
s.polygon([(rx + 4, ry + 96), (rx - 14, ry + 122), (rx + 4, ry + 112)], fill=(150, 158, 172), outline=INK)
s.polygon([(rx + 36, ry + 96), (rx + 54, ry + 122), (rx + 36, ry + 112)], fill=(150, 158, 172), outline=INK)
s.polygon([(rx + 10, ry + 96), (rx + 30, ry + 96), (rx + 20, ry + 150)], fill=FLAME)
s.polygon([(rx + 14, ry + 96), (rx + 26, ry + 96), (rx + 20, ry + 128)], fill=(244, 196, 66))
# Tiangong station top right: core module with two solar wings
s.rectangle((210, 52, 270, 68), fill=(206, 212, 222), outline=INK, width=2)
s.rectangle((190, 56, 210, 64), fill=(46, 110, 168), outline=INK, width=1)
s.rectangle((270, 56, 290, 64), fill=(46, 110, 168), outline=INK, width=1)
img.paste(scene, (sx0, sy0))
d.rectangle((sx0, sy0, sx1, sy1), outline=INK, width=2)
# lead text
tx = 380
d.text((tx, 186), "SPACE · CHINA–PAKISTAN", font=F(SANS_B, 22), fill=ACCENT)
lh = F(SERIF_B, 37)
y = 216
for line in wrap("Pakistan's first astronaut reaches orbit", lh, W - 36 - tx - 18):
    d.text((tx, y), line, font=lh, fill=INK)
    y += 43
y += 4
ls = F(SANS, 21)
for line in wrap("Shenzhou-24 lifts off at 00:18 UTC and docks with Tiangong, "
                 "carrying Muhammad Zeeshan Ali — the first Pakistani in "
                 "orbit and the first foreign astronaut aboard China's "
                 "space station.", ls, W - 36 - tx - 18):
    d.text((tx, y), line, font=ls, fill=MUTED)
    y += 27


# ---------- pictograms for the grid panels ----------
def pictogram(kind, x0, y0, w, h):
    """Draw a simple white pictogram centred in the box (x0, y0, w, h)."""
    cx, cy = x0 + w // 2, y0 + h // 2
    if kind == "ship":  # oil tanker on waves
        d.rectangle((cx - 22, cy - 22, cx - 8, cy - 8), fill=WHITE)
        d.rectangle((cx - 6, cy - 22, cx + 8, cy - 8), fill=WHITE)
        d.rectangle((cx + 10, cy - 22, cx + 24, cy - 8), fill=WHITE)
        d.polygon([(cx - 28, cy - 6), (cx + 28, cy - 6), (cx + 20, cy + 12),
                   (cx - 20, cy + 12)], fill=WHITE)
        d.arc((cx - 28, cy + 16, cx - 2, cy + 30), 0, 180, fill=WHITE, width=3)
        d.arc((cx + 2, cy + 16, cx + 28, cy + 30), 0, 180, fill=WHITE, width=3)
    elif kind == "island":  # Pacific island with palm and sun
        d.ellipse((cx + 8, cy - 30, cx + 26, cy - 12), fill=WHITE)
        d.ellipse((cx - 28, cy + 6, cx + 28, cy + 30), fill=WHITE)
        d.line((cx - 4, cy + 6, cx - 2, cy - 14), fill=WHITE, width=4)
        d.line((cx - 2, cy - 14, cx - 18, cy - 24), fill=WHITE, width=3)
        d.line((cx - 2, cy - 14, cx + 12, cy - 26), fill=WHITE, width=3)
        d.line((cx - 2, cy - 14, cx - 2, cy - 28), fill=WHITE, width=3)
    elif kind == "shop":  # supermarket storefront
        d.rectangle((cx - 26, cy - 26, cx + 26, cy - 12), fill=WHITE)
        d.rectangle((cx - 26, cy - 12, cx + 26, cy + 28), outline=WHITE, width=3)
        d.rectangle((cx - 8, cy + 2, cx + 8, cy + 28), fill=WHITE)
        d.line((cx - 26, cy - 12, cx + 26, cy - 12), fill=WHITE, width=3)
    elif kind == "shirt":  # garment t-shirt
        d.polygon([(cx - 12, cy - 24), (cx + 12, cy - 24), (cx + 28, cy - 14),
                   (cx + 20, cy + 2), (cx + 12, cy - 4), (cx + 12, cy + 26),
                   (cx - 12, cy + 26), (cx - 12, cy - 4), (cx - 20, cy + 2),
                   (cx - 28, cy - 14)], fill=WHITE)
    elif kind == "mine":  # mine tunnel with lamp
        d.arc((cx - 24, cy - 24, cx + 24, cy + 24), 180, 360, fill=WHITE, width=4)
        d.line((cx - 24, cy, cx - 24, cy + 28), fill=WHITE, width=4)
        d.line((cx + 24, cy, cx + 24, cy + 28), fill=WHITE, width=4)
        d.ellipse((cx - 7, cy - 2, cx + 7, cy + 12), fill=WHITE)
        d.line((cx, cy + 12, cx, cy + 20), fill=WHITE, width=3)
    elif kind == "chart":  # falling stock chart
        d.line((cx - 26, cy + 26, cx + 26, cy + 26), fill=WHITE, width=3)
        d.line((cx - 26, cy + 26, cx - 26, cy - 26), fill=WHITE, width=3)
        d.line((cx - 24, cy - 18, cx - 8, cy - 2, cx + 6, cy - 10, cx + 24, cy + 14),
               fill=WHITE, width=4)
        d.polygon([(cx + 24, cy + 14), (cx + 12, cy + 12), (cx + 22, cy + 24)], fill=WHITE)


# ---------- grid panels ----------
panels = [
    ("HORMUZ", ACCENT, "Iran says two tankers hit mines",
     "Tehran says two tankers hit mines and caught fire; the claim is unverified.",
     "ship"),
    ("PACIFIC", (16, 80, 160), "Solomons picks Australia, bars foreign bases",
     "Canberra signs a treaty making it Honiara's top partner; no foreign base.",
     "island"),
    ("COLOMBIA", (120, 60, 140), "Cartagena hostages freed",
     "Troops storm a supermarket at dawn, freeing all hostages; one captor killed.",
     "shop"),
    ("BANGLADESH", (16, 110, 60), "Garment wage up 36% after protests",
     "Dhaka raises the minimum wage to 17,000 taka after weeks of protests.",
     "shirt"),
    ("INDONESIA", ACCENT, "Three bodies found in flooded mine",
     "Three bodies found in a flooded illegal gold mine in Bogor; 23 still trapped.",
     "mine"),
    ("MARKETS", (196, 124, 22), "Asian stocks slide in AI sell-off",
     "Nikkei falls 2.8% and Kospi 6.2% as AI-spending doubts hit chip shares.",
     "chart"),
]
gx0, gy0 = 36, 434
gw, gh, gap = 468, 176, 12
BAND = 74
for i, (kicker, kc, head, sub, icon) in enumerate(panels):
    cx = gx0 + (i % 2) * (gw + gap)
    cy = gy0 + (i // 2) * (gh + gap)
    d.rounded_rectangle((cx, cy, cx + gw, cy + gh), radius=12, fill=CARD, outline=INK, width=2)
    # coloured pictogram band on the left
    d.rectangle((cx + 2, cy + 2, cx + BAND, cy + gh - 2), fill=kc)
    pictogram(icon, cx + 2, cy + 2, BAND - 2, gh - 4)
    tx = cx + BAND + 16
    tw = gw - BAND - 16 - 16
    d.text((tx, cy + 12), kicker, font=F(SANS_B, 18), fill=kc)
    hy = cy + 38
    hf = F(SANS_B, 24)
    head_lines = wrap(head, hf, tw)
    for line in head_lines:
        d.text((tx, hy), line, font=hf, fill=INK)
        hy += 28
    max_sub = 3 if len(head_lines) <= 2 else 2
    sf = F(SANS, 18)
    for line in wrap(sub, sf, tw)[:max_sub]:
        d.text((tx, hy + 2), line, font=sf, fill=MUTED)
        hy += 23

# ---------- footer ----------
fy = gy0 + 3 * gh + 2 * gap + 14
d.line([(36, fy), (W - 36, fy)], fill=INK, width=1)
centered("Compiled from the day's wire reports — Reuters, Xinhua, AP, AFP and PM.gov.au, 25 November 2026.",
         F(SANS, 16), fy + 8, MUTED)

img.save(OUT, format="PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
