"""Whimsical explainer for math2: 'The Theorem That Was Already There'.

Renders PNG frames with Pillow; ffmpeg assembles mp4 + gif.
Usage: python3 render.py OUTDIR
"""
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 960, 540, 30
F = "/usr/share/fonts/truetype/dejavu/"
def font(name, size): return ImageFont.truetype(F + name, size)
SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
MONO = lambda s: font("DejaVuSansMono.ttf", s)

PAPER = (250, 244, 228)
INK = (44, 38, 58)
PLUM = (122, 72, 140)
TEAL = (38, 140, 132)
CORAL = (232, 106, 84)
GOLD = (236, 178, 58)
SKY = (196, 226, 236)
ZERO = (90, 110, 200)

def ease(t):  # smoothstep, clamped
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def lerp(a, b, t): return a + (b - a) * t

def text_c(d, xy, s, f, fill=INK):
    w = d.textlength(s, font=f)
    d.text((xy[0] - w / 2, xy[1]), s, font=f, fill=fill)

def background(d, t):
    d.rectangle([0, 0, W, H], fill=PAPER)
    # faint grid, gently drifting like graph paper on a breeze
    off = (t * 12) % 30
    for x in range(-30, W + 30, 30):
        d.line([(x + off, 0), (x + off, H)], fill=(238, 230, 210))
    for y in range(0, H, 30):
        d.line([(0, y), (W, y)], fill=(238, 230, 210))

def scroll_char(d, cx, cy, w, h, label, color, t, mood="smile", sub=None, look=0.0):
    """A paper-scroll creature with eyes. bob with t."""
    bob = math.sin(t * 4 + cx * 0.01) * 4
    cy = cy + bob
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    d.rounded_rectangle([x0 + 5, y0 + 7, x1 + 5, y1 + 7], 18, fill=(220, 210, 190))
    d.rounded_rectangle([x0, y0, x1, y1], 18, fill=(255, 252, 242), outline=color, width=4)
    # scroll curls
    for yy in (y0, y1):
        d.ellipse([x0 - 10, yy - 10, x0 + 10, yy + 10], fill=color)
        d.ellipse([x1 - 10, yy - 10, x1 + 10, yy + 10], fill=color)
    # eyes (blink every ~3s)
    blink = (t % 3.1) < 0.12
    ey = y0 + h * 0.30
    for ex in (cx - w * 0.17, cx + w * 0.17):
        if blink:
            d.line([(ex - 9, ey), (ex + 9, ey)], fill=INK, width=4)
        else:
            d.ellipse([ex - 11, ey - 11, ex + 11, ey + 11], fill="white", outline=INK, width=3)
            px = ex + look * 5
            d.ellipse([px - 5, ey - 5, px + 5, ey + 5], fill=INK)
    my = y0 + h * 0.47
    if mood == "smile":
        d.arc([cx - 22, my - 14, cx + 22, my + 14], 15, 165, fill=INK, width=4)
    elif mood == "proud":
        d.arc([cx - 26, my - 20, cx + 26, my + 12], 20, 160, fill=INK, width=4)
        d.ellipse([cx - w * 0.33, my - 4, cx - w * 0.23, my + 6], fill=(250, 190, 190))
        d.ellipse([cx + w * 0.23, my - 4, cx + w * 0.33, my + 6], fill=(250, 190, 190))
    elif mood == "o":
        d.ellipse([cx - 9, my - 6, cx + 9, my + 14], fill=INK)
    elif mood == "meh":
        d.line([(cx - 16, my + 4), (cx + 16, my + 4)], fill=INK, width=4)
    text_c(d, (cx, y0 + h * 0.62), label, SERIF_B(int(h * 0.17)), color)
    if sub:
        text_c(d, (cx, y0 + h * 0.80), sub, SANS(int(h * 0.075)), INK)

def zero_creature(d, x, y, t, scared=False, r=17):
    d.ellipse([x - r, y - r, x + r, y + r], fill=ZERO, outline=INK, width=2)
    for ex in (x - 6, x + 6):
        d.ellipse([ex - 4, y - 7, ex + 4, y + 1], fill="white")
        d.ellipse([ex - 1.5, y - 4, ex + 1.5, y - 1], fill=INK)
    if scared:
        d.ellipse([x - 4, y + 3, x + 4, y + 11], fill=INK)
    else:
        d.arc([x - 6, y, x + 6, y + 9], 0, 180, fill="white", width=2)
    d.text((x + r - 4, y - r - 10), "ρ", font=SERIF_B(14), fill=ZERO)

def speech(d, x, y, lines, f, fill=INK, bg="white", tail=None, appear=1.0):
    if appear <= 0: return
    pad = 14
    lw = max(d.textlength(l, font=f) for l in lines)
    lh = f.size + 8
    w, h = lw + 2 * pad, lh * len(lines) + 2 * pad - 8
    s = 0.6 + 0.4 * ease(appear)
    cx, cy = x + w / 2, y + h / 2
    x0, y0 = cx - w * s / 2, cy - h * s / 2
    if tail:
        d.polygon([(x0 + 30, y0 + h * s - 2), (x0 + 58, y0 + h * s - 2), tail], fill=bg, outline=INK)
    d.rounded_rectangle([x0, y0, x0 + w * s, y0 + h * s], 16, fill=bg, outline=INK, width=3)
    if appear > 0.6:
        for i, l in enumerate(lines):
            d.text((x0 + pad, y0 + pad + i * lh), l, font=f, fill=fill)

random.seed(7)
RAIN = [(random.uniform(40, W - 40), random.uniform(-900, -40), random.uniform(-25, 25),
         random.uniform(130, 260), random.choice([PLUM, TEAL, CORAL, GOLD])) for _ in range(46)]

def scene_title(d, t):  # 0..5s
    background(d, t)
    for x, y0, rot, v, c in RAIN:  # papers falling
        y = y0 + v * t
        if -40 < y < H + 40:
            a = math.radians(rot + 40 * math.sin(t * 2 + x))
            pts = []
            for dx, dy in ((-14, -18), (14, -18), (14, 18), (-14, 18)):
                pts.append((x + dx * math.cos(a) - dy * math.sin(a), y + dx * math.sin(a) + dy * math.cos(a)))
            d.polygon(pts, fill=(255, 252, 242), outline=c)
    k = ease(t / 1.2)
    d.rounded_rectangle([170, 150, 790, 370], 30, fill=(255, 252, 242), outline=INK, width=4)
    text_c(d, (W / 2, 175 - 30 * (1 - k)), "722 papers fell from the sky…", SANS_B(30), PLUM)
    if t > 1.4:
        text_c(d, (W / 2, 235), "math2", SERIF_B(int(lerp(20, 76, ease((t - 1.4) / 0.7)))), INK)
    if t > 2.6:
        text_c(d, (W / 2, 325), "or: The Theorem That Was Already There", SANS(24), TEAL)

def strip(d, x0, x1, y0, y1, wall_t):
    # the critical strip 0 < Re s < 1, with a wall at 7/8
    d.rectangle([x0, y0, x1, y1], fill=SKY, outline=INK, width=3)
    for i, lab in ((0, "0"), (0.5, "½"), (7 / 8, "7/8"), (1, "1")):
        x = lerp(x0, x1, i)
        text_c(d, (x, y1 + 8), lab, SANS_B(20))
    d.text((x0 - 4, y0 - 34), "the critical strip  (Re s)", font=SANS(18), fill=INK)
    xw = lerp(x0, x1, 7 / 8)
    hh = (y1 - y0) * ease(wall_t)
    d.rectangle([xw, y1 - hh, x1, y1], fill=(255, 236, 196))
    d.line([(xw, y1 - hh), (xw, y1)], fill=CORAL, width=7)
    if wall_t > 0.9:
        d.text((xw + 8, y0 + 8), "NO\nZEROS", font=SANS_B(18), fill=CORAL)
    return xw

def scene_wall(d, t):  # 5..12s
    background(d, t + 5)
    x0, x1, y0, y1 = 360, 900, 110, 420
    xw = strip(d, x0, x1, y0, y1, ease((t - 0.8) / 1.2))
    scroll_char(d, 180, 300, 210, 250, "7/8", TEAL, t, mood="smile", sub="Sept 30 paper", look=1)
    speech(d, 40, 50, ["No zeros past 7/8!", "Not for ANY Dirichlet L!"], SANS_B(19),
           appear=(t - 0.3) / 0.5, tail=(150, 175))
    random.seed(3)
    for i in range(9):
        y = lerp(y0 + 30, y1 - 30, i / 8)
        target = lerp(x0 + 30, x1 - 20, random.random())
        start = x0 + 40 + 40 * math.sin(i)
        p = ease((t - 2.0 - i * 0.25) / 1.2)
        x = lerp(start, target, p)
        scared = False
        if x > xw - 18 and p > 0:  # bonk! bounce back
            over = x - (xw - 18)
            x = xw - 18 - over * 0.8
            scared = True
            if 0 < over < 40:
                d.text((xw - 6, y - 32), "boing!", font=SANS_B(14), fill=CORAL)
        zero_creature(d, x, y, t, scared)

def scene_siegel(d, t):  # 12..19s
    background(d, t + 12)
    scroll_char(d, 220, 320, 210, 250, "7/8", TEAL, t, mood="smile", sub="Sept 30 paper", look=1)
    enter = ease(t / 1.4)
    sx = lerp(W + 150, 700, enter)
    scroll_char(d, sx, 320, 250, 270, "Siegel", PLUM, t, mood="proud", sub="Oct 1 paper · own proof", look=-1)
    speech(d, 470, 40, ["Behold! A brand-new paper!", "Real zeros keep (1−β)·log q ≥ c", "for some c > 0. Somewhere."],
           SANS_B(19), appear=(t - 1.5) / 0.5, tail=(640, 180))
    if t > 4.3:
        speech(d, 40, 40, ["…um. I already", "did that."], SANS_B(22), appear=(t - 4.3) / 0.4, tail=(190, 185))

def scene_proof(d, t):  # 19..27s
    background(d, t + 19)
    scroll_char(d, 140, 330, 170, 210, "7/8", TEAL, t, mood="smile", look=1)
    scroll_char(d, 830, 330, 190, 220, "Siegel", PLUM, t, mood="o" if t > 5.2 else "meh", look=-1)
    d.rounded_rectangle([250, 90, 710, 470], 24, fill=(36, 54, 52), outline=INK, width=5)  # chalkboard
    steps = ["IF no zero lies past 7/8, then",
             "so  β ≤ 7/8,  so  1 − β ≥ 1/8;",
             "and  q ≥ 3,  so  log q ≥ log 3:",
             "",
             "(1 − β) · log q  ≥  log 3 / 8"]
    chalk = (236, 240, 228)
    shown = t * 26  # characters of chalk per second
    used = 0
    for i, s in enumerate(steps):
        n = int(max(0, min(len(s), shown - used)))
        used += len(s) + 6
        f = SERIF_B(23) if i == 4 else SANS(20)
        col = GOLD if i == 4 else chalk
        text_c(d, (480, 130 + i * 52), s[:n], f, col)
    if t > 5.2:
        k = ease((t - 5.2) / 0.6)
        text_c(d, (480, 405), "c = 0.137…   explicit!", SANS_B(int(20 + 6 * k)), CORAL)

def scene_lean(d, t):  # 27..33s
    background(d, t + 27)
    scroll_char(d, 270, 300, 180, 200, "7/8", TEAL, t, mood="proud", look=0.5)
    scroll_char(d, 690, 300, 180, 200, "Siegel", PLUM, t, mood="smile", look=-0.5)
    # the Lean stamp comes crashing down
    p = ease(t / 0.7)
    sy = lerp(-200, 175, p)
    wob = math.sin(t * 18) * max(0, 1 - (t - 0.7) * 2) * 6 if t > 0.7 else 0
    d.ellipse([W / 2 - 110 + wob, sy - 110, W / 2 + 110 + wob, sy + 110], outline=TEAL, width=10)
    d.ellipse([W / 2 - 92 + wob, sy - 92, W / 2 + 92 + wob, sy + 92], outline=TEAL, width=3)
    text_c(d, (W / 2 + wob, sy - 62), "✓", SANS_B(64), TEAL)
    text_c(d, (W / 2 + wob, sy + 14), "checked", SANS_B(26), TEAL)
    text_c(d, (W / 2 + wob, sy + 46), "by Lean", SANS_B(22), TEAL)
    if t > 0.3:
        text_c(d, (W / 2, 22), "a CONDITIONAL implication:", SANS_B(20), PLUM)
        text_c(d, (W / 2, 48), "IF OpenAI's 7/8 claim holds, THEN Siegel follows", SANS(19), PLUM)
    if t > 1.2:
        text_c(d, (W / 2, 446), "Lean checks the step, not OpenAI's 7/8 proof (assumed)", MONO(16), INK)
        text_c(d, (W / 2, 472), "axioms: propext · Quot.sound · Classical.choice", MONO(16), INK)
        text_c(d, (W / 2, 498), "hypothesis = OpenAI's statement, byte for byte", MONO(16), INK)
    if 0.65 < t < 1.3:
        for i in range(10):  # sparkles
            a = i * 0.63
            r = 140 + (t - 0.65) * 160
            x, y = W / 2 + r * math.cos(a), 150 + r * math.sin(a) * 0.7
            d.text((x, y), "✦", font=SANS_B(20), fill=GOLD)

def scene_end(d, t):  # 33..38s
    background(d, t + 33)
    d.rounded_rectangle([140, 110, 820, 430], 30, fill=(255, 252, 242), outline=INK, width=4)
    text_c(d, (W / 2, 140), "the moral:", SANS(24), PLUM)
    text_c(d, (W / 2, 180), "check how your theorems talk to each other", SERIF_B(27), INK)
    if t > 1.6:
        text_c(d, (W / 2, 352), "upstream claims assumed · all 372 families mined", SANS(16), PLUM)
    items = [("12", "Lean-checked implications"), ("31", "written derivations"), ("5", "research leads")]
    for i, (n, lab) in enumerate(items):
        k = ease((t - 0.6 - i * 0.35) / 0.5)
        x = 260 + i * 220
        text_c(d, (x, 255 - 20 * (1 - k)), n if k > 0 else "", SERIF_B(54), [TEAL, CORAL, GOLD][i])
        if k > 0:
            text_c(d, (x, 325), lab, SANS(15))
    if t > 2.0:
        text_c(d, (W / 2, 386), "github.com/atimics/math2", MONO(22), INK)
    zero_creature(d, 90 + 30 * math.sin(t * 2), 470, t)
    d.text((115 + 30 * math.sin(t * 2), 452), "bye!", font=SANS_B(16), fill=ZERO)

SCENES = [(scene_title, 5.0), (scene_wall, 7.0), (scene_siegel, 7.0),
          (scene_proof, 8.0), (scene_lean, 6.0), (scene_end, 5.0)]
FADE = 0.35
idx = 0
for si, (fn, dur) in enumerate(SCENES):
    n = int(dur * FPS)
    for i in range(n):
        t = i / FPS
        img = Image.new("RGB", (W, H))
        fn(ImageDraw.Draw(img), t)
        # cross-fade to/from paper at scene edges
        a = min(1.0, t / FADE, (dur - t) / FADE)
        if si == 0: a = min(1.0, (dur - t) / FADE)
        if si == len(SCENES) - 1: a = min(1.0, t / FADE)
        if a < 1:
            img = Image.blend(Image.new("RGB", (W, H), PAPER), img, max(0, a))
        img.save(os.path.join(OUT, f"f{idx:05d}.png"))
        idx += 1
print("frames", idx, "seconds", idx / FPS)
