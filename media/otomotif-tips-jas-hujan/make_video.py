#!/usr/bin/env python3
"""Render a short vertical tips video (1080x1920) about rain-coat choice for
motorcycle riders, based on the CNN Indonesia article:

  "Pemotor Tak Direkomendasi Pakai Jas Hujan Ponco, Lalu yang Mana?"
  https://www.cnnindonesia.com/otomotif/20260113075143-595-1316386/
      pemotor-tak-direkomendasi-pakai-jas-hujan-ponco-lalu-yang-mana

Output: tips-jas-hujan-ponco.mp4 (H.264 + AAC, ~19.5s, 30 fps)

Frames are drawn with Pillow and piped as rawvideo into ffmpeg; the rain
ambience is synthesised with numpy, so nothing external is downloaded.

Usage:  python3 make_video.py [output.mp4]
"""

from __future__ import annotations

import math
import os
import random
import struct
import subprocess
import sys
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------------------------------------------------------------- basic setup

W, H = 1080, 1920
FPS = 30
MARGIN = 84

BG_TOP = (7, 17, 28)
BG_BOTTOM = (13, 39, 58)
AMBER = (255, 190, 61)
RED = (255, 92, 92)
GREEN = (56, 224, 138)
WHITE = (255, 255, 255)
MUTED = (166, 190, 209)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
F_BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
F_REG = FONT_DIR / "DejaVuSans.ttf"

_font_cache: dict[tuple[Path, int], ImageFont.FreeTypeFont] = {}


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(str(path), size)
    return _font_cache[key]


def bold(size: int) -> ImageFont.FreeTypeFont:
    return font(F_BOLD, size)


def reg(size: int) -> ImageFont.FreeTypeFont:
    return font(F_REG, size)


# ------------------------------------------------------------------- easing

def clamp01(v: float) -> float:
    return 0.0 if v < 0 else (1.0 if v > 1 else v)


def ease_out(t: float) -> float:
    return 1 - (1 - clamp01(t)) ** 3


def ease_in(t: float) -> float:
    return clamp01(t) ** 3


# ------------------------------------------------------------------ drawing

def wrap(text: str, fnt: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    """Greedy word wrap. Explicit newlines are honoured."""
    lines: list[str] = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for word in words:
            trial = f"{cur} {word}".strip()
            if fnt.getlength(trial) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


PAD = 26  # slack around a tile so its drop shadow is not clipped


def text_tile(
    text: str,
    fnt: ImageFont.FreeTypeFont,
    color: tuple[int, int, int],
    max_w: int,
    leading: float = 1.22,
    shadow: bool = True,
) -> Image.Image:
    """Render wrapped text into a tight RGBA tile with a soft drop shadow.

    The tile records its shadow padding in `info["pad"]` so layout code can
    measure the *visible* text box rather than the padded bitmap.
    """
    lines = wrap(text, fnt, max_w)
    line_h = int(fnt.size * leading)
    pad = PAD if shadow else 0
    tile_w = max(int(fnt.getlength(ln)) for ln in lines) + pad * 2
    tile_h = line_h * len(lines) + pad * 2
    tile = Image.new("RGBA", (tile_w, tile_h), (0, 0, 0, 0))

    if shadow:
        shade = Image.new("RGBA", tile.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(shade)
        for i, ln in enumerate(lines):
            sd.text((pad, pad + i * line_h + 6), ln, font=fnt, fill=(0, 0, 0, 170))
        tile.alpha_composite(shade.filter(ImageFilter.GaussianBlur(9)))

    d = ImageDraw.Draw(tile)
    for i, ln in enumerate(lines):
        d.text((pad, pad + i * line_h), ln, font=fnt, fill=color + (255,))
    tile.info["pad"] = pad
    # visible height excludes the trailing descender slack of the last line
    tile.info["vis_h"] = line_h * len(lines)
    return tile


def sprite(size: tuple[int, int], paint, ss: int = 3) -> Image.Image:
    """Draw `paint(draw, w, h)` supersampled, then downscale for smooth edges."""
    big = Image.new("RGBA", (size[0] * ss, size[1] * ss), (0, 0, 0, 0))
    paint(ImageDraw.Draw(big), size[0] * ss, size[1] * ss)
    return big.resize(size, Image.LANCZOS)


def pill(label: str, fill: tuple[int, int, int], text_color=(10, 18, 26)) -> Image.Image:
    fnt = bold(34)
    pad_x, pad_y = 34, 18
    w = int(fnt.getlength(label)) + pad_x * 2
    h = fnt.size + pad_y * 2

    def paint(d, bw, bh):
        d.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=bh // 2, fill=fill + (255,))

    tile = sprite((w, h), paint)
    ImageDraw.Draw(tile).text(
        (pad_x, pad_y - 4), label, font=fnt, fill=text_color + (255,)
    )
    return tile


def badge(num: str, color: tuple[int, int, int], size: int = 118) -> Image.Image:
    def paint(d, bw, bh):
        d.ellipse([0, 0, bw - 1, bh - 1], fill=color + (38,), outline=color + (255,), width=int(bh * 0.035))

    tile = sprite((size, size), paint)
    fnt = bold(int(size * 0.52))
    d = ImageDraw.Draw(tile)
    tw = fnt.getlength(num)
    d.text(((size - tw) / 2, size * 0.20), num, font=fnt, fill=color + (255,))
    return tile


def warning_icon(size: int = 150) -> Image.Image:
    def paint(d, bw, bh):
        m = bw * 0.06
        d.polygon(
            [(bw / 2, m), (bw - m, bh - m), (m, bh - m)],
            fill=AMBER + (40,),
            outline=AMBER + (255,),
            width=int(bw * 0.055),
        )
        d.rounded_rectangle(
            [bw / 2 - bw * 0.038, bh * 0.36, bw / 2 + bw * 0.038, bh * 0.66],
            radius=bw * 0.038,
            fill=AMBER + (255,),
        )
        d.ellipse(
            [bw / 2 - bw * 0.045, bh * 0.72, bw / 2 + bw * 0.045, bh * 0.72 + bw * 0.09],
            fill=AMBER + (255,),
        )

    return sprite((size, size), paint)


def check_icon(size: int = 62, color=GREEN) -> Image.Image:
    def paint(d, bw, bh):
        d.ellipse([0, 0, bw - 1, bh - 1], fill=color + (46,), outline=color + (255,), width=int(bw * 0.06))
        d.line(
            [(bw * 0.28, bh * 0.52), (bw * 0.45, bh * 0.68), (bw * 0.74, bh * 0.34)],
            fill=color + (255,),
            width=int(bw * 0.09),
            joint="curve",
        )

    return sprite((size, size), paint)


def cross_icon(size: int = 62, color=RED) -> Image.Image:
    def paint(d, bw, bh):
        d.ellipse([0, 0, bw - 1, bh - 1], fill=color + (46,), outline=color + (255,), width=int(bw * 0.06))
        w = int(bw * 0.09)
        d.line([(bw * 0.33, bh * 0.33), (bw * 0.67, bh * 0.67)], fill=color + (255,), width=w)
        d.line([(bw * 0.67, bh * 0.33), (bw * 0.33, bh * 0.67)], fill=color + (255,), width=w)

    return sprite((size, size), paint)


def build_background() -> Image.Image:
    """Vertical gradient + soft amber glow + vignette, drawn once."""
    bg = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / (H - 1)
        curve = t ** 0.85
        d.line(
            [(0, y), (W, y)],
            fill=tuple(int(BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * curve) for i in range(3)),
        )

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-260, 420, W + 260, 1560], fill=(70, 130, 180, 60))
    bg = Image.alpha_composite(bg.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(180)))

    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    vd.rectangle([0, 0, W, H], fill=(0, 0, 0, 130))
    vd.ellipse([-W * 0.35, H * 0.10, W * 1.35, H * 0.92], fill=(0, 0, 0, 0))
    bg = Image.alpha_composite(bg, vig.filter(ImageFilter.GaussianBlur(220)))
    return bg.convert("RGB")


# --------------------------------------------------------------- rain layer

class Rain:
    def __init__(self, count: int = 190, seed: int = 7):
        rnd = random.Random(seed)
        self.drops = [
            {
                "x": rnd.uniform(-200, W + 200),
                "y": rnd.uniform(-H, H),
                "len": rnd.uniform(34, 120),
                "spd": rnd.uniform(1500, 2600),  # px per second
                "a": rnd.randint(28, 96),
                "w": rnd.choice((1, 1, 2, 2, 3)),
            }
            for _ in range(count)
        ]
        self.slant = 0.28  # horizontal drift per vertical pixel

    def layer(self, t: float) -> Image.Image:
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        for dr in self.drops:
            y = (dr["y"] + dr["spd"] * t) % (H + 400) - 200
            x = (dr["x"] - self.slant * dr["spd"] * t * 0.35) % (W + 400) - 200
            d.line(
                [(x, y), (x + dr["len"] * self.slant, y + dr["len"])],
                fill=(200, 226, 245, dr["a"]),
                width=dr["w"],
            )
        return img


# -------------------------------------------------------------- scene model

class El:
    """One animated element: a tile placed at (x, y) with a staggered entry."""

    def __init__(self, tile: Image.Image, x, y, delay: float = 0.0, dy: int = 46,
                 dur: float = 0.5, center: bool = False):
        self.tile = tile
        self.x = int(x - tile.width / 2) if center else int(x)
        self.y = int(y)
        self.delay = delay
        self.dy = dy
        self.dur = dur


class Scene:
    def __init__(self, duration: float, els: list[El]):
        self.duration = duration
        self.els = els


def alpha_scaled(tile: Image.Image, factor: float) -> Image.Image:
    if factor >= 0.999:
        return tile
    out = tile.copy()
    out.putalpha(out.getchannel("A").point(lambda v, f=factor: int(v * f)))
    return out


# ------------------------------------------------------------ scene builder

CONTENT_W = W - MARGIN * 2
SOURCE_NOTE = "Sumber: CNN Indonesia"
HEADER_Y = 300          # fixed header pill baseline, shared by every scene
CONTENT_CENTER = 1010   # blocks are centred on this line


def vis_h(tile: Image.Image) -> int:
    """Visible height of a tile, ignoring drop-shadow padding."""
    pad = tile.info.get("pad", 0)
    return tile.info.get("vis_h", tile.height - 2 * pad)


class Block:
    """Vertical stack that measures itself, so nothing ever overlaps.

    Rows are added top to bottom with an explicit gap; `emit()` then centres
    the whole stack on `center_y` and returns positioned, animated elements.
    """

    def __init__(self, align: str = "center", x: int = MARGIN):
        self.align = align
        self.x = x
        self.rows: list[dict] = []

    def add(self, tile: Image.Image, gap: int = 0, delay: float = 0.0,
            dy: int = 46, indent: int = 0) -> "Block":
        self.rows.append({"tile": tile, "gap": gap, "delay": delay, "dy": dy,
                          "indent": indent, "inline": False})
        return self

    def add_inline(self, tile: Image.Image, dx: int, dy_off: int, delay: float = 0.0,
                   dy: int = 24) -> "Block":
        """Attach a tile beside the row added last (e.g. a bullet icon)."""
        self.rows.append({"tile": tile, "gap": 0, "delay": delay, "dy": dy,
                          "indent": dx, "inline": True, "dy_off": dy_off})
        return self

    def height(self) -> int:
        total = 0
        for r in self.rows:
            if r["inline"]:
                continue
            total += r["gap"] + vis_h(r["tile"])
        return total

    def emit(self, center_y: int = CONTENT_CENTER) -> list[El]:
        els: list[El] = []
        y = center_y - self.height() / 2
        last_top = y
        for r in self.rows:
            tile, pad = r["tile"], r["tile"].info.get("pad", 0)
            if r["inline"]:
                if self.align == "center":
                    x = W / 2 + r["indent"]
                else:
                    x = self.x + r["indent"]
                els.append(El(tile, x - pad, last_top + r["dy_off"] - pad,
                              delay=r["delay"], dy=r["dy"]))
                continue
            y += r["gap"]
            last_top = y
            if self.align == "center":
                x = (W - tile.width) / 2
            else:
                x = self.x - pad + r["indent"]
            els.append(El(tile, x, y - pad, delay=r["delay"], dy=r["dy"]))
            y += vis_h(tile)
        return els


def header(label: str, color: tuple[int, int, int], text_color=(10, 18, 26),
           delay: float = 0.05) -> El:
    return El(pill(label, color, text_color=text_color), W / 2, HEADER_Y,
              delay=delay, dy=30, center=True)


def hook_scene() -> Scene:
    b = Block("center")
    b.add(warning_icon(196), delay=0.16, dy=30)
    b.add(text_tile("JANGAN PAKAI\nJAS HUJAN PONCO", bold(92), WHITE, CONTENT_W, leading=1.18),
          gap=54, delay=0.32)
    b.add(text_tile("Bukan didesain untuk berkendara,\nmalah bisa memicu kecelakaan.",
                    reg(46), MUTED, CONTENT_W, leading=1.34),
          gap=54, delay=0.56)
    b.add(text_tile("4 alasannya ↓", bold(50), RED, CONTENT_W, leading=1.2),
          gap=76, delay=0.86)
    els = [header("TIPS OTOMOTIF · MUSIM HUJAN", AMBER)] + b.emit(1000)
    return Scene(3.4, els)


def reason_scene(num: str, head: str, body: str, duration: float) -> Scene:
    b = Block("left")
    b.add(badge(num, RED, 138), delay=0.14, dy=30)
    b.add(text_tile(head, bold(76), WHITE, CONTENT_W, leading=1.18), gap=42, delay=0.28)
    b.add(text_tile(body, reg(46), MUTED, CONTENT_W, leading=1.42), gap=34, delay=0.46)
    els = [header("KENAPA PONCO BERISIKO", RED, text_color=WHITE)] + b.emit(980)
    return Scene(duration, els)


def solution_scene() -> Scene:
    bullets = [
        "Potongannya pas di badan",
        "Tak berisiko tersangkut roda",
        "Lampu rem dan sein tetap terlihat",
    ]
    b = Block("center")
    b.add(check_icon(126, GREEN), delay=0.16, dy=28)
    b.add(text_tile("JAS HUJAN\n2 POTONG", bold(92), WHITE, CONTENT_W, leading=1.18),
          gap=48, delay=0.30)
    b.add(text_tile("jaket + celana", bold(56), GREEN, CONTENT_W, leading=1.2),
          gap=26, delay=0.48)

    left = Block("left")
    for i, text in enumerate(bullets):
        row = text_tile(text, reg(44), WHITE, CONTENT_W - 96, leading=1.3)
        left.add(row, gap=(0 if i == 0 else 40), delay=0.66 + i * 0.16, indent=88)
        left.add_inline(check_icon(56, GREEN), dx=0, dy_off=-4, delay=0.66 + i * 0.16)

    top = b.emit(830)
    els = [header("YANG DIREKOMENDASIKAN", GREEN)] + top + left.emit(1350)
    return Scene(3.6, els)


def checklist_scene() -> Scene:
    items = [
        ("Warna terang", "mudah terlihat saat hujan lebat"),
        ("Material reflektif", "scotchlite memantulkan cahaya malam"),
        ("Bahan PVC", "lebih awet dan tahan air"),
    ]
    b = Block("left")
    for i, (title, sub) in enumerate(items):
        b.add(text_tile(title, bold(54), AMBER, CONTENT_W - 104, leading=1.2),
              gap=(0 if i == 0 else 52), delay=0.34 + i * 0.20, indent=96)
        b.add_inline(check_icon(62, AMBER), dx=0, dy_off=-2, delay=0.34 + i * 0.20)
        b.add(text_tile(sub, reg(40), MUTED, CONTENT_W - 104, leading=1.3),
              gap=8, delay=0.44 + i * 0.20, indent=96)

    head = Block("center")
    head.add(text_tile("Selain modelnya,\nperhatikan ini", bold(70), WHITE, CONTENT_W,
                       leading=1.2), delay=0.16)

    outro = Block("center")
    outro.add(text_tile("Ganti ponco sekarang,\nselamat sampai tujuan.", bold(50), WHITE,
                        CONTENT_W, leading=1.26), delay=1.05, dy=32)

    els = ([header("CHECKLIST PILIH JAS HUJAN", AMBER)]
           + head.emit(560) + b.emit(1030) + outro.emit(1500))
    return Scene(3.8, els)


def build_scenes() -> list[Scene]:
    return [
        hook_scene(),
        reason_scene(
            "1", "Riskan tersangkut",
            "Jubah yang menjuntai bisa masuk ke rantai, gir, atau jari-jari roda. "
            "Pengendara bisa terjatuh atau roda mendadak terkunci.",
            3.0,
        ),
        reason_scene(
            "2", "Keseimbangan terganggu",
            "Ponco punya banyak celah. Terpaan angin dari depan mudah masuk "
            "dan membuat pemotor kehilangan keseimbangan.",
            2.8,
        ),
        reason_scene(
            "3", "Lampu ikut tertutup",
            "Jubah panjang berpotensi menutupi lampu rem dan sein, "
            "sehingga pengendara di belakang tak mendapat peringatan.",
            2.8,
        ),
        reason_scene(
            "4", "Melindungi tak tuntas",
            "Ponco umumnya tidak menutup sampai kaki, jadi celana "
            "dan sepatu tetap basah kuyup.",
            2.7,
        ),
        solution_scene(),
        checklist_scene(),
    ]


# ------------------------------------------------------------------- audio

def render_audio(path: Path, duration: float, cuts: list[float], sr: int = 44100) -> None:
    """Synthesised rain ambience plus a soft whoosh on every scene change."""
    import numpy as np

    rng = np.random.default_rng(11)
    n = int(duration * sr)
    noise = rng.normal(0, 1, n)

    # crude one-pole low-pass + high-pass shaping to get "rain" out of noise
    lp = np.copy(noise)
    a = 0.22
    for _ in range(2):
        lp = np.concatenate(([lp[0]], lp[1:] * a + lp[:-1] * (1 - a)))
    rain = noise * 0.35 + lp * 0.9

    # slow amplitude drift so the loop does not sound static
    t = np.arange(n) / sr
    drift = 1 + 0.16 * np.sin(2 * math.pi * 0.13 * t) + 0.08 * np.sin(2 * math.pi * 0.37 * t + 1.1)
    sig = rain * drift * 0.11

    # transition whooshes
    for c in cuts:
        start = int(max(0.0, c - 0.18) * sr)
        seg_n = int(0.55 * sr)
        if start + seg_n > n:
            seg_n = n - start
        if seg_n <= 0:
            continue
        env = np.linspace(0, 1, seg_n) ** 0.5
        env = env * (1 - np.linspace(0, 1, seg_n)) ** 1.6
        sweep = rng.normal(0, 1, seg_n)
        k = np.copy(sweep)
        for _ in range(3):
            k = np.concatenate(([k[0]], k[1:] * 0.35 + k[:-1] * 0.65))
        sig[start:start + seg_n] += k * env * 0.55

    # global fade in/out
    fade = int(0.5 * sr)
    sig[:fade] *= np.linspace(0, 1, fade)
    sig[-fade:] *= np.linspace(1, 0, fade)

    peak = float(np.max(np.abs(sig))) or 1.0
    sig = np.tanh(sig / peak * 1.6) * 0.72
    pcm = (sig * 32767).astype("<i2")
    stereo = np.repeat(pcm[:, None], 2, axis=1).tobytes()

    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(stereo)


# -------------------------------------------------------------------- render

def ffmpeg_bin() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def main() -> int:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "tips-jas-hujan-ponco.mp4").resolve()
    scenes = build_scenes()
    total = sum(s.duration for s in scenes)
    n_frames = int(round(total * FPS))
    cuts, acc = [], 0.0
    for s in scenes[:-1]:
        acc += s.duration
        cuts.append(acc)

    print(f"durasi {total:.2f}s · {n_frames} frame · {W}x{H}@{FPS}")

    bg = build_background()
    rain = Rain()
    footer = text_tile(SOURCE_NOTE, reg(32), (135, 158, 176), CONTENT_W, shadow=False)

    tmp_wav = out.with_suffix(".tmp.wav")
    render_audio(tmp_wav, total, cuts)

    cmd = [
        ffmpeg_bin(), "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", str(tmp_wav),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest", "-movflags", "+faststart",
        str(out),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None

    FADE = 0.30
    for i in range(n_frames):
        t_global = i / FPS

        # locate the active scene
        scene, t_scene = scenes[-1], 0.0
        acc = 0.0
        for s in scenes:
            if t_global < acc + s.duration or s is scenes[-1]:
                scene, t_scene = s, t_global - acc
                break
            acc += s.duration

        frame = bg.copy()
        frame = Image.alpha_composite(frame.convert("RGBA"), rain.layer(t_global))

        # scene-level fade in / out
        s_alpha = ease_out(t_scene / FADE) if t_scene < FADE else 1.0
        exit_t = (t_scene - (scene.duration - FADE)) / FADE
        exit_p = ease_in(exit_t) if exit_t > 0 else 0.0
        s_alpha *= 1 - exit_p

        for el in scene.els:
            p = ease_out((t_scene - el.delay) / el.dur)
            if p <= 0.001:
                continue
            a = p * s_alpha
            if a <= 0.004:
                continue
            y = el.y + int((1 - p) * el.dy) - int(exit_p * 34)
            frame.alpha_composite(alpha_scaled(el.tile, a), (el.x, y))

        d = ImageDraw.Draw(frame)
        # progress bar
        bar_y, bar_w = H - 96, W - MARGIN * 2
        d.rounded_rectangle([MARGIN, bar_y, MARGIN + bar_w, bar_y + 8], radius=4,
                            fill=(255, 255, 255, 46))
        filled = int(bar_w * (i + 1) / n_frames)
        if filled > 8:
            d.rounded_rectangle([MARGIN, bar_y, MARGIN + filled, bar_y + 8], radius=4,
                                fill=AMBER + (235,))
        frame.alpha_composite(footer, (MARGIN, H - 178))

        proc.stdin.write(frame.convert("RGB").tobytes())
        if i % 60 == 0:
            print(f"  frame {i}/{n_frames}", flush=True)

    proc.stdin.close()
    rc = proc.wait()
    if tmp_wav.exists():
        os.unlink(tmp_wav)
    if rc != 0:
        print("ffmpeg gagal", file=sys.stderr)
        return rc
    print(f"selesai -> {out} ({out.stat().st_size / 1_048_576:.2f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
