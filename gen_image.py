#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261120.

Front page for Friday 20 November 2026, drawn from scratch with PIL:
masthead + lead story + 5 more panels. Six stories, all reported on
20 November 2026:
  1. Trump, Xi and Putin hold the first-ever three-way summit in Shenzhen
  2. The UN's top court (ICJ) rules Myanmar committed genocide
     against the Rohingya minority
  3. Cyclone Akvan makes landfall on India's Odisha coast
  4. NASA confirms Voyager 1 is one light-day from Earth
  5. GTA VI sales pass $1.8 billion, topping The Odyssey's global run
  6. Russian strikes damage the Austrian and Dutch embassies in Kyiv
Deterministic: no randomness, no network, fixed fonts, fixed layout.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 229)
CARD = (255, 255, 255)
INK = (22, 22, 22)
NAVY = (20, 38, 74)
RED = (176, 42, 42)
GREY = (90, 90, 90)
RULE = (180, 170, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
serif_b = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSerif-Bold.ttf", s)
serif = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSerif.ttf", s)
sans = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", s)
sans_b = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", s)
sans_o = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", s)


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, max_w, fill=INK, leading=None):
    """Draw wrapped paragraph; returns y after the last line."""
    lh = leading or int(font.size * 1.28)
    for line in wrap(d, text, font, max_w):
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_flag_us(d, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        if i % 2 == 0:
            d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                        fill=(178, 34, 52))
    cw, ch = w * 0.4, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(30, 50, 110))
    for r in range(5):
        for c in range(6):
            d.ellipse([x + 4 + c * (cw - 8) / 5, y + 3 + r * (ch - 6) / 4,
                       x + 7 + c * (cw - 8) / 5, y + 6 + r * (ch - 6) / 4],
                      fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def draw_flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.polygon(star_points(x + w * 0.22, y + h * 0.28, h * 0.20, h * 0.08),
              fill=(255, 222, 0))
    for sx, sy in [(0.55, 0.18), (0.72, 0.30), (0.68, 0.55), (0.50, 0.68)]:
        d.polygon(star_points(x + w * sx, y + h * sy, h * 0.07, h * 0.03),
                  fill=(255, 222, 0))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def draw_flag_ru(d, x, y, w, h):
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def draw_flags_scene(d, x, y, w, h):
    """Three flag poles (US, China, Russia) above a summit table."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    fw, fh = 84, 56
    specs = [(draw_flag_us, 0.06), (draw_flag_cn, 0.38), (draw_flag_ru, 0.70)]
    for fn, fx in specs:
        px = x + w * fx
        d.line([px + fw / 2, y + 18, px + fw / 2, y + h - 42],
               fill=(70, 60, 50), width=4)
        d.ellipse([px + fw / 2 - 4, y + 12, px + fw / 2 + 4, y + 20],
                  fill=(200, 170, 60))
        fn(d, px, y + 22, fw, fh)
    # summit table
    d.ellipse([x + 8, y + h - 46, x + w - 8, y + h - 6], fill=(120, 72, 40))
    d.rectangle([x + 30, y + h - 26, x + w - 30, y + h - 14], fill=(96, 56, 30))


def draw_scales(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 232, 238))
    cx, top, bot = x + w / 2, y + 12, y + h - 14
    d.line([cx, top, cx, bot], fill=(60, 60, 70), width=4)
    d.line([cx - 52, top + 16, cx + 52, top + 16], fill=(60, 60, 70), width=4)
    d.ellipse([cx - 5, top - 6, cx + 5, top + 4], fill=(200, 170, 60))
    for sx in (cx - 52, cx + 52):
        d.line([sx, top + 16, sx - 16, top + 52], fill=(60, 60, 70), width=2)
        d.line([sx, top + 16, sx + 16, top + 52], fill=(60, 60, 70), width=2)
        d.pieslice([sx - 18, top + 46, sx + 18, top + 66], 0, 180,
                   fill=(200, 170, 60))
    d.rectangle([cx - 26, bot - 4, cx + 26, bot + 2], fill=(60, 60, 70))


def draw_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 216, 228))
    cx, cy = x + w / 2, y + h / 2
    for r, a0, a1 in [(46, 20, 300), (36, 200, 120), (26, 20, 280),
                      (16, 180, 100)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1,
              fill=(255, 255, 255), width=7)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(20, 38, 74))


def draw_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 16, 40))
    stars = [(0.12, 0.20), (0.30, 0.12), (0.52, 0.28), (0.72, 0.14),
             (0.86, 0.34), (0.20, 0.62), (0.44, 0.72), (0.66, 0.58),
             (0.88, 0.70), (0.08, 0.82)]
    for sx, sy in stars:
        px, py = x + w * sx, y + h * sy
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))
    # Voyager: gold dish + body + boom
    cx, cy = x + w * 0.55, y + h * 0.45
    d.polygon([(cx - 26, cy - 6), (cx + 6, cy - 22), (cx + 22, cy + 2),
               (cx - 6, cy + 12)], fill=(212, 175, 55))
    d.rectangle([cx - 4, cy + 10, cx + 26, cy + 22], fill=(180, 180, 190))
    d.line([cx + 26, cy + 16, cx + 44, cy + 8], fill=(220, 220, 220), width=2)
    d.line([cx - 4, cy + 16, cx - 22, cy + 26], fill=(220, 220, 220), width=2)
    d.ellipse([x + 12, y + h - 26, x + 34, y + h - 4], fill=(70, 130, 200))


def draw_skyline(d, x, y, w, h):
    for i, col in enumerate([(255, 183, 77), (255, 140, 105), (199, 91, 122),
                             (120, 80, 140)]):
        d.rectangle([x, y + i * h / 4, x + w, y + (i + 1) * h / 4], fill=col)
    d.ellipse([x + w - 52, y + 8, x + w - 12, y + 48], fill=(255, 240, 180))
    base = y + h
    heights = [0.42, 0.62, 0.34, 0.72, 0.50, 0.66, 0.38, 0.58]
    bw = w / len(heights)
    for i, fh in enumerate(heights):
        bx = x + i * bw + 2
        d.rectangle([bx, base - h * fh, bx + bw - 4, base], fill=(35, 28, 52))
        for wy in range(3):
            d.rectangle([bx + 5, base - h * fh + 8 + wy * 12,
                         bx + 10, base - h * fh + 13 + wy * 12],
                        fill=(255, 220, 90))


def draw_embassy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 224, 218))
    bx, by, bw, bh = x + 18, y + 22, w - 36, h - 30
    d.rectangle([bx, by, bx + bw, by + bh], fill=(150, 148, 140))
    for r in range(3):
        for c in range(5):
            wx = bx + 10 + c * (bw - 20) / 5
            wy = by + 10 + r * (bh - 20) / 3
            d.rectangle([wx, wy, wx + 12, wy + 14], fill=(60, 60, 66))
    d.line([bx + bw * 0.30, by, bx + bw * 0.42, by + bh * 0.45,
            bx + bw * 0.34, by + bh * 0.70, bx + bw * 0.55, by + bh],
           fill=(40, 40, 44), width=4)
    # two small flags: Austria (red-white-red), Netherlands (red-white-blue)
    for fx, cols in [(0.08, [(213, 0, 50), (255, 255, 255), (213, 0, 50)]),
                     (0.78, [(174, 28, 40), (255, 255, 255), (33, 70, 140)])]:
        px = x + w * fx
        d.line([px, y + 8, px, y + 34], fill=(70, 60, 50), width=2)
        for i, col in enumerate(cols):
            d.rectangle([px, y + 8 + i * 6, px + 16, y + 14 + i * 6], fill=col)


def card(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 8, H - 8], outline=INK, width=3)

    # Masthead
    d.rectangle([16, 16, W - 16, 132], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    f_title = serif_b(60)
    d.text(((W - d.textlength(title, font=f_title)) / 2, 34), title,
           font=f_title, fill=(255, 255, 255))
    d.text(((W - d.textlength("make.fun  •  one day, one picture", font=sans(20))) / 2,
            104), "make.fun  •  one day, one picture", font=sans(20),
           fill=(200, 210, 230))

    # Date line
    date = "FRIDAY, 20 NOVEMBER 2026"
    f_date = serif_b(30)
    dw = d.textlength(date, font=f_date)
    d.line([60, 162, (W - dw) / 2 - 24, 162], fill=RED, width=3)
    d.line([(W + dw) / 2 + 24, 162, W - 60, 162], fill=RED, width=3)
    d.text(((W - dw) / 2, 146), date, font=f_date, fill=RED)
    sub = "Six stories that defined the day"
    d.text(((W - d.textlength(sub, font=sans_o(20))) / 2, 180), sub,
           font=sans_o(20), fill=GREY)

    # ---- Lead story: trilateral summit ----
    lx, ly, lw, lh = 24, 212, 976, 288
    card(d, lx, ly, lw, lh)
    draw_flags_scene(d, lx + 16, ly + 16, 300, 256)
    tx = lx + 336
    d.text((tx, ly + 18), "SHENZHEN, CHINA — THE LEAD STORY",
           font=sans_b(19), fill=RED)
    y = para(d, tx, ly + 48, "THREE LEADERS, ONE TABLE", serif_b(42),
             lw - 356)
    y = para(d, tx, y + 8,
             "Trump, Xi and Putin hold the first-ever three-way summit, "
             "talking nuclear arms control, energy security and Ukraine.",
             sans(22), lw - 356, leading=29)

    # ---- Middle row: two cards ----
    my, mh = 516, 228
    # ICJ / Myanmar
    card(d, 24, my, 481, mh)
    draw_scales(d, 40, my + 12, 449, 82)
    y = para(d, 40, my + 102, "COURT: MYANMAR COMMITTED GENOCIDE",
             sans_b(24), 449)
    para(d, 40, y + 6,
         "The UN's top court rules Myanmar committed genocide against "
         "the Rohingya minority.",
         sans(18), 449, leading=22)
    # Cyclone Akvan
    card(d, 519, my, 481, mh)
    draw_cyclone(d, 535, my + 12, 449, 82)
    y = para(d, 535, my + 102, "CYCLONE AKVAN HITS INDIA'S COAST",
             sans_b(24), 449)
    para(d, 535, y + 6,
         "The storm makes landfall in Odisha; 300,000 evacuated, "
         "423 rescue teams deployed.",
         sans(18), 449, leading=22)

    # ---- Bottom row: three cards ----
    by, bh = 760, 212
    cards = [
        (24, draw_space, "VOYAGER 1, ONE LIGHT-DAY AWAY",
         "NASA confirms the probe is a full light-day from Earth — "
         "the farthest human-made object ever."),
        (352, draw_skyline, "GTA VI PASSES $1.8 BILLION",
         "A day after launch, GTA 6 sales already top The Odyssey's "
         "$1.8bn global box-office run."),
        (680, draw_embassy, "EMBASSIES HIT IN KYIV STRIKES",
         "Russian strikes damage the Austrian and Dutch embassies in "
         "Kyiv, officials say."),
    ]
    for cx, scene, title, body in cards:
        card(d, cx, by, 320, bh)
        scene(d, cx + 14, by + 10, 292, 74)
        y = para(d, cx + 14, by + 92, title, sans_b(20), 292)
        para(d, cx + 14, y + 4, body, sans(16), 292, leading=20)

    # Footer
    foot = "THE WORLD IN ONE DAY  •  20 NOVEMBER 2026  •  make.fun"
    d.text(((W - d.textlength(foot, font=sans(16))) / 2, 986), foot,
           font=sans(16), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
