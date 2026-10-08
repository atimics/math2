"""math2, Chapter 2: 'The Great Fan-Out' — a whimsical 42-second explainer.

Renders PNG frames and a music-box soundtrack; ffmpeg assembles mp4 + gif:
    python3 render_ch2.py OUTDIR          # writes OUTDIR/f00000.png ... and OUTDIR/music.wav
"""
import math, os, random, sys, wave
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

PAPER = (250, 244, 228); INK = (44, 38, 58); PLUM = (122, 72, 140); TEAL = (38, 140, 132)
CORAL = (232, 106, 84); GOLD = (236, 178, 58); SKY = (196, 226, 236); ZERO = (90, 110, 200)
LEAF = (110, 170, 90); ROSE = (238, 196, 190)

def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)
def lerp(a, b, t): return a + (b - a) * t
def text_c(d, xy, s, f, fill=INK):
    d.text((xy[0] - d.textlength(s, font=f) / 2, xy[1]), s, font=f, fill=fill)

def background(d, t):
    d.rectangle([0, 0, W, H], fill=PAPER)
    off = (t * 12) % 30
    for x in range(-30, W + 30, 30):
        d.line([(x + off, 0), (x + off, H)], fill=(238, 230, 210))
    for y in range(0, H, 30):
        d.line([(0, y), (W, y)], fill=(238, 230, 210))

def eyes(d, cx, ey, sep, r, t, look=0.0, phase=0.0):
    blink = ((t + phase) % 3.1) < 0.12
    for ex in (cx - sep, cx + sep):
        if blink:
            d.line([(ex - r, ey), (ex + r, ey)], fill=INK, width=3)
        else:
            d.ellipse([ex - r, ey - r, ex + r, ey + r], fill="white", outline=INK, width=2)
            px = ex + look * r * 0.45
            d.ellipse([px - r * 0.45, ey - r * 0.45, px + r * 0.45, ey + r * 0.45], fill=INK)

def scroll_char(d, cx, cy, w, h, label, color, t, mood="smile", sub=None, look=0.0, phase=0.0):
    cy = cy + math.sin(t * 4 + cx * 0.01) * 4
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    d.rounded_rectangle([x0 + 5, y0 + 7, x1 + 5, y1 + 7], 18, fill=(220, 210, 190))
    d.rounded_rectangle([x0, y0, x1, y1], 18, fill=(255, 252, 242), outline=color, width=4)
    for yy in (y0, y1):
        d.ellipse([x0 - 10, yy - 10, x0 + 10, yy + 10], fill=color)
        d.ellipse([x1 - 10, yy - 10, x1 + 10, yy + 10], fill=color)
    eyes(d, cx, y0 + h * 0.30, w * 0.17, 11, t, look, phase)
    my = y0 + h * 0.47
    if mood == "smile":
        d.arc([cx - 22, my - 14, cx + 22, my + 14], 15, 165, fill=INK, width=4)
    elif mood == "o":
        d.ellipse([cx - 9, my - 6, cx + 9, my + 14], fill=INK)
    elif mood == "joy":
        d.chord([cx - 22, my - 12, cx + 22, my + 18], 0, 180, fill=INK)
        d.ellipse([cx - w * 0.33, my - 4, cx - w * 0.23, my + 6], fill=ROSE)
        d.ellipse([cx + w * 0.23, my - 4, cx + w * 0.33, my + 6], fill=ROSE)
    text_c(d, (cx, y0 + h * 0.60), label, SERIF_B(int(h * 0.15)), color)
    if sub:
        text_c(d, (cx, y0 + h * 0.80), sub, SANS(int(h * 0.07)), INK)

def agent(d, x, y, t, color, r=18, look=0.0, phase=0.0, glass=False):
    """A little research agent: round body, antenna, optional magnifying glass."""
    y = y + math.sin(t * 6 + phase) * 3
    d.line([(x, y - r), (x + 4, y - r - 12)], fill=INK, width=2)
    d.ellipse([x + 1, y - r - 17, x + 9, y - r - 9], fill=GOLD, outline=INK)
    d.ellipse([x - r, y - r, x + r, y + r], fill=color, outline=INK, width=2)
    eyes(d, x, y - r * 0.15, r * 0.38, r * 0.28, t, look, phase)
    d.arc([x - r * 0.35, y + r * 0.05, x + r * 0.35, y + r * 0.55], 10, 170, fill=INK, width=2)
    if glass:
        gx, gy = x + r + 10, y + 2
        d.line([(gx - 6, gy + 6), (gx - 14, gy + 14)], fill=INK, width=4)
        d.ellipse([gx - 8, gy - 12, gx + 12, gy + 8], outline=INK, width=3, fill=(230, 244, 250))

def speech(d, x, y, lines, f, tail=None, appear=1.0, bg="white"):
    if appear <= 0: return
    pad = 14; lh = f.size + 8
    w = max(d.textlength(l, font=f) for l in lines) + 2 * pad
    h = lh * len(lines) + 2 * pad - 8
    s = 0.6 + 0.4 * ease(appear)
    cx, cy = x + w / 2, y + h / 2
    x0, y0 = cx - w * s / 2, cy - h * s / 2
    if tail:
        d.polygon([(x0 + 30, y0 + h * s - 2), (x0 + 58, y0 + h * s - 2), tail], fill=bg, outline=INK)
    d.rounded_rectangle([x0, y0, x0 + w * s, y0 + h * s], 16, fill=bg, outline=INK, width=3)
    if appear > 0.6:
        for i, l in enumerate(lines):
            d.text((x0 + pad, y0 + pad + i * lh), l, font=f, fill=INK)

def caption(d, t, lines, start=0.0):
    if t < start: return
    k = ease((t - start) / 0.5)
    for i, (s, f, c) in enumerate(lines):
        text_c(d, (W / 2, 448 + i * 28 + 10 * (1 - k)), s, f, c)

# ---------------------------------------------------------------- scenes
AGENT_COLORS = [TEAL, CORAL, GOLD, PLUM, LEAF, ZERO]
random.seed(11)
DOTS = [(random.uniform(60, W - 60), random.uniform(70, 400)) for _ in range(372)]
MINED_BEFORE = set(random.sample(range(372), 289))

def scene_title(d, t):  # 6 s
    background(d, t)
    for i, (x, y) in enumerate(DOTS):  # the 372 families
        lit = i in MINED_BEFORE or t > 2.0 + (i % 83) * 0.03
        c = TEAL if i in MINED_BEFORE else (CORAL if lit else (215, 205, 185))
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=c)
    for k, col in enumerate(AGENT_COLORS):  # agents fan out from the centre
        a = k * math.tau / 6 + 0.3
        rr = 200 * ease((t - 0.6) / 1.6)
        agent(d, W / 2 + rr * math.cos(a) * 1.5, 230 + rr * math.sin(a) * 0.8, t, col,
              look=math.cos(a), phase=k)
    d.rounded_rectangle([250, 395, 710, 520], 24, fill=(255, 252, 242), outline=INK, width=4)
    text_c(d, (W / 2, 405), "math2 · Chapter 2", SANS_B(22), PLUM)
    text_c(d, (W / 2, 433), "The Great Fan-Out", SERIF_B(40), INK)
    n = 289 + int(83 * ease((t - 2.0) / 2.6))
    text_c(d, (W / 2, 485), f"families mined: {n} / 372", MONO(20), TEAL if n < 372 else CORAL)

def scene_twins(d, t):  # 8 s
    background(d, t + 6)
    k = ease(t / 1.2)
    scroll_char(d, lerp(-150, 270, k), 250, 220, 250, "Elliott", TEAL, t, mood="o" if t > 2.2 else "smile",
                sub="comparator A", look=1)
    scroll_char(d, lerp(W + 150, 690, k), 250, 220, 250, "Elliott", PLUM, t, mood="o" if t > 2.2 else "smile",
                sub="comparator B", look=-1, phase=0.4)
    if t > 1.4:  # mirror sparkle between them
        for i in range(6):
            yy = 160 + i * 34 + 8 * math.sin(t * 5 + i)
            d.text((W / 2 - 8, yy), "=" if i % 2 else "⇔", font=SANS_B(26), fill=GOLD)
    speech(d, 330, 34, ["…wait. We're the SAME theorem!"], SANS_B(22), appear=(t - 2.2) / 0.5, tail=(470, 120))
    caption(d, t, [("OpenAI formalized it twice, with separate proofs.", SANS_B(20), INK),
                   ("Lean: the two statements are equivalent (Ostmann too).", SANS(18), PLUM)], 3.6)

def scene_pi(d, t):  # 8 s
    background(d, t + 14)
    x0, x1, y = 120, 840, 270
    def X(p): return lerp(x0, x1, p / 4)
    d.rectangle([X(0), y - 50, X(2), y], fill=(214, 236, 206))
    d.rectangle([X(2), y - 50, X(4), y], fill=(248, 214, 204))
    d.line([(x0, y), (x1, y)], fill=INK, width=3)
    for p in range(5):
        d.line([(X(p), y - 6), (X(p), y + 6)], fill=INK, width=3)
        text_c(d, (X(p), y + 12), str(p), SANS_B(20))
    text_c(d, (W / 2, y + 42), "Liouville exponent p", SANS(18))
    text_c(d, (X(1), y - 42), "LiouvilleWith p ✓", SANS_B(17), LEAF)
    text_c(d, (X(1), y - 22), "(Dirichlet, new in Lean)", SANS(14), INK)
    text_c(d, (X(3), y - 42), "LiouvilleWith p ✗", SANS_B(17), CORAL)
    text_c(d, (X(3), y - 22), "(OpenAI's μ(π) claim)", SANS(14), INK)
    hh = 130 * ease((t - 0.6) / 0.8)  # the fence at exactly 2
    d.rectangle([X(2) - 5, y - hh, X(2) + 5, y], fill=GOLD, outline=INK)
    # π walks right and bonks the fence
    walk = 1.6 * ease((t - 1.2) / 2.0)
    px = X(0.4 + walk)
    bonk = 2.0 < t - 1.2 < 2.6
    d.ellipse([px - 26, y - 130, px + 26, y - 78], fill=(255, 252, 242), outline=PLUM, width=3)
    text_c(d, (px, y - 122), "π", SERIF_B(30), PLUM)
    if bonk:
        d.text((X(2) + 12, y - 150), "bonk!", font=SANS_B(18), fill=CORAL)
    caption(d, t, [("Irrationality exponent of rπ + s is exactly 2,", SANS_B(20), INK),
                   ("and so is every rational Möbius image of π (if OpenAI's claim holds).", SANS(17), PLUM)], 3.8)

def scene_gottschalk(d, t):  # 8 s
    background(d, t + 22)
    text_c(d, (W / 2, 30), "a cellular automaton  T_b  (cartoon: the real sets are infinite)", SANS(17), INK)
    left = [(260, 110 + i * 62) for i in range(5)]
    right = [(700, 90 + i * 58) for i in range(6)]
    hit = [0, 1, 2, 4, 5]
    for (x, y) in left:
        d.rounded_rectangle([x - 34, y - 20, x + 34, y + 20], 8, fill=SKY, outline=INK, width=2)
    for i, (x, y) in enumerate(right):
        lonely = i == 3
        d.rounded_rectangle([x - 34, y - 20, x + 34, y + 20], 8,
                            fill=(248, 214, 204) if lonely else SKY, outline=INK, width=2)
    for i, (lx, ly) in enumerate(left):
        k = ease((t - 0.5 - i * 0.35) / 0.6)
        rx, ry = right[hit[i]]
        if k > 0:
            ex, ey = lerp(lx + 36, rx - 36, k), lerp(ly, ry, k)
            d.line([(lx + 36, ly), (ex, ey)], fill=TEAL, width=3)
            if k > 0.95:
                d.polygon([(rx - 36, ry), (rx - 48, ry - 6), (rx - 48, ry + 6)], fill=TEAL)
    if t > 2.8:  # the lonely configuration nobody reaches
        x, y = right[3]
        d.text((x + 44, y - 16), "?  never reached", font=SANS_B(18), fill=CORAL)
        eyes(d, x, y - 2, 10, 6, t)
    caption(d, t, [("Injective but not surjective: Gottschalk's surjunctivity fails", SANS_B(19), INK),
                   ("for OpenAI's Kaplansky groups, checked against their own `cellular` map.", SANS(16), PLUM)], 3.6)

def scene_referees(d, t):  # 7 s
    background(d, t + 30)
    for i in range(50):  # every catalogue entry
        x, y = 128 + (i % 17) * 42, 110 + (i // 17) * 70
        d.rounded_rectangle([x - 16, y - 24, x + 16, y + 24], 5, fill=(255, 252, 242), outline=INK, width=2)
        if t > 0.8 + i * 0.04:
            d.text((x - 7, y - 14), "✓", font=SANS_B(20), fill=TEAL)
    sweep = lerp(120, 840, ease((t - 0.6) / 2.6))
    agent(d, sweep, 330, t, ZERO, r=22, look=1, glass=True)
    agent(d, sweep - 70, 360, t, LEAF, r=20, look=1, phase=1.3, glass=True)
    stamps = [("0 wrong", TEAL), ("4 citations fixed", PLUM), ("~25 upgraded to D", CORAL)]
    for i, (s, c) in enumerate(stamps):
        k = ease((t - 3.2 - i * 0.6) / 0.4)
        if k > 0:
            x = 200 + i * 280
            w = d.textlength(s, font=SANS_B(22)) + 30
            d.rounded_rectangle([x - w / 2, 405, x + w / 2, 450], 10, outline=c, width=4)
            text_c(d, (x, 414), s, SANS_B(22), c)
    text_c(d, (W / 2, 470), "independent referees re-checked every entry", SANS(17), INK)

def scene_end(d, t):  # 6 s
    background(d, t + 37)
    d.rounded_rectangle([120, 70, 840, 470], 30, fill=(255, 252, 242), outline=INK, width=4)
    text_c(d, (W / 2, 96), "after the fan-out", SANS(22), PLUM)
    items = [("14", "Lean-checked", "implications", TEAL), ("31", "complete written", "derivations", CORAL),
             ("5", "research", "leads", GOLD)]
    for i, (n, a, b, c) in enumerate(items):
        k = ease((t - 0.4 - i * 0.3) / 0.5)
        x = 255 + i * 225
        if k > 0:
            text_c(d, (x, 140 - 18 * (1 - k)), n, SERIF_B(60), c)
            text_c(d, (x, 216), a, SANS(16)); text_c(d, (x, 238), b, SANS(16))
    if t > 1.6:
        text_c(d, (W / 2, 290), "all 372 families mined · 5 pull requests merged", SANS_B(19), INK)
        text_c(d, (W / 2, 322), "OpenAI's claims assumed; only the implications are checked", SANS(17), PLUM)
    if t > 2.4:
        text_c(d, (W / 2, 392), "github.com/atimics/math2", MONO(24), INK)
    for k, col in enumerate(AGENT_COLORS):
        agent(d, 70 + k * 30, 505, t, col, r=11, phase=k)
    d.text((262, 494), "see you in chapter 3!", font=SANS_B(16), fill=ZERO)

SCENES = [(scene_title, 6.0), (scene_twins, 8.0), (scene_pi, 8.0),
          (scene_gottschalk, 8.0), (scene_referees, 7.0), (scene_end, 6.0)]
FADE = 0.35
idx = 0
for si, (fn, dur) in enumerate(SCENES):
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = Image.new("RGB", (W, H))
        fn(ImageDraw.Draw(img), t)
        a = min(1.0, t / FADE, (dur - t) / FADE)
        if si == 0: a = min(1.0, (dur - t) / FADE)
        if si == len(SCENES) - 1: a = min(1.0, t / FADE)
        if a < 1:
            img = Image.blend(Image.new("RGB", (W, H), PAPER), img, max(0, a))
        img.save(os.path.join(OUT, f"f{idx:05d}.png"))
        idx += 1
total = idx / FPS

# ---------------------------------------------------------------- music box
import numpy as np
sr = 44100
tt = np.arange(int(sr * total)) / sr
out = np.zeros_like(tt)
def note(f, start, length=0.9, amp=0.17):
    i0 = int(start * sr); n = min(int(length * sr), len(out) - i0)
    if n <= 0: return
    x = np.arange(n) / sr
    env = np.exp(-x * 4.5) * (1 - np.exp(-x * 200))
    out[i0:i0 + n] += (np.sin(2 * np.pi * f * x) + 0.35 * np.sin(4 * np.pi * f * x)
                       + 0.12 * np.sin(2 * np.pi * 3.01 * f * x)) * env * amp
scale = [440.0, 493.88, 554.37, 659.25, 739.99, 880.0]  # A major pentatonic
prog = [[0, 2, 4, 2], [1, 3, 5, 3], [2, 4, 5, 4], [3, 2, 1, 0]]
s, k = 0.3, 0
while s < total - 1.2:
    bar = prog[(k // 4) % 4]; f = scale[bar[k % 4]]
    note(f, s)
    if k % 4 == 0: note(f / 2, s, 1.6, 0.11)
    k += 1; s += 0.25
for j, f in enumerate([880.0, 1108.7, 1318.5]):        # twins sparkle
    note(f, 7.6 + j * 0.12, 1.0, 0.10)
i0 = int(19.4 * sr); n = int(0.4 * sr); x = np.arange(n) / sr   # π bonk
out[i0:i0 + n] += 0.4 * np.sin(2 * np.pi * 80 * x) * np.exp(-x * 10)
for b in np.arange(33.2, 35.0, 0.6):                     # referee stamps
    i0 = int(b * sr); n = int(0.3 * sr); x = np.arange(n) / sr
    out[i0:i0 + n] += 0.35 * np.sin(2 * np.pi * 95 * x) * np.exp(-x * 12)
out *= np.minimum(1, (total - tt) / 1.5)
out /= max(1e-9, np.abs(out).max()) / 0.85
with wave.open(os.path.join(OUT, "music.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("frames", idx, "seconds", total)
