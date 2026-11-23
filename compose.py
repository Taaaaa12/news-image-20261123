#!/usr/bin/env python3
"""Compose the news-image entry: a 1024x1024 front-page summary of
Monday 23 November 2026 world news. Pure PIL, deterministic output."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
BG = (13, 27, 42)          # deep navy
PANEL = (18, 38, 58)
WHITE = (244, 246, 248)
MUTED = (199, 208, 219)
GOLD = (232, 184, 75)
RULE = (45, 66, 92)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
F_BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")
F_REG = str(FONT_DIR / "DejaVuSans.ttf")

STORIES = [
    ("CLIMATE  ·  ANTALYA", (110, 200, 130),
     "COP31 ends with no deal",
     "Two weeks of talks in Antalya collapse \u2014 the longest climate summit in UN history."),
    ("LIBYA  ·  BENGHAZI", (229, 92, 92),
     "Ukraine sinks Russian warship in Libya",
     "Sea drones hit the corvette Merkury in Benghazi; Libya asks the UN to investigate."),
    ("UKRAINE  ·  KYIV REGION", (229, 120, 90),
     "Strike on Dymer flats kills 11",
     "A Russian attack levels an apartment block near Kyiv; rescuers dig through rubble."),
    ("MARKETS  ·  ASIA", (242, 165, 65),
     "Chip stocks slide on AI-spending fears",
     "Seoul\u2019s Kospi falls as much as 5.8% after a Wall Street rout on AI-spending doubts."),
    ("MIDDLE EAST  ·  THE GULF", (230, 120, 60),
     "Iran strikes Bahrain; tankers hit in Hormuz",
     "An Iranian attack hits a Bahrain industrial site; three tankers attacked in the strait."),
]


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def track(draw, xy, text, font, fill, spacing=2):
    """Draw text with letter spacing."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing
    return x


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    mx = 56  # margin
    cw = W - 2 * mx  # content width

    # --- masthead ------------------------------------------------------
    f_mast = ImageFont.truetype(F_BOLD, 66)
    d.text((mx, 44), "THE WORLD TODAY", font=f_mast, fill=WHITE)

    # small globe motif, top right
    cx, cy, r = 912, 84, 40
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=GOLD, width=3)
    d.ellipse((cx - r // 2, cy - r, cx + r // 2, cy + r), outline=GOLD, width=2)
    d.line((cx - r, cy, cx + r, cy), fill=GOLD, width=2)
    d.arc((cx - r, cy - r // 2, cx + r, cy + r // 2), 200, 340, fill=GOLD, width=2)

    d.line((mx, 140, W - mx, 140), fill=GOLD, width=3)
    f_date = ImageFont.truetype(F_BOLD, 25)
    track(d, (mx, 156), "MONDAY, 23 NOVEMBER 2026", f_date, GOLD, spacing=3)
    f_sub = ImageFont.truetype(F_REG, 21)
    d.text((mx, 190), "Five stories that defined the day", font=f_sub, fill=MUTED)

    # --- stories --------------------------------------------------------
    f_kick = ImageFont.truetype(F_BOLD, 20)
    f_head = ImageFont.truetype(F_BOLD, 33)
    f_deck = ImageFont.truetype(F_REG, 21)
    y = 246
    for i, (kicker, color, head, deck) in enumerate(STORIES):
        track(d, (mx, y), kicker, f_kick, color, spacing=2)
        y += 30
        for line in wrap(d, head, f_head, cw):
            d.text((mx, y), line, font=f_head, fill=WHITE)
            y += 42
        for line in wrap(d, deck, f_deck, cw):
            d.text((mx, y), line, font=f_deck, fill=MUTED)
            y += 30
        y += 14
        if i < len(STORIES) - 1:
            d.line((mx, y, W - mx, y), fill=RULE, width=1)
            y += 22

    # --- footer ---------------------------------------------------------
    f_foot = ImageFont.truetype(F_REG, 17)
    foot = "Compiled from wire and UN reports  \u00b7  23 November 2026"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, H - 44), foot, font=f_foot, fill=(140, 155, 172))

    out = HERE / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, "bytes:", out.stat().st_size, "size:", img.size)


if __name__ == "__main__":
    main()
