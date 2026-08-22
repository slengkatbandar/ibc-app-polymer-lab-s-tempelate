#!/usr/bin/env python3
"""Cuts the Nevo Q05 out of its studio frame.

Segmentation is rembg's isnet-general-use model (github.com/danielgatis/rembg).
Only the largest connected region is kept, so the studio floor's reflection does
not come along, and the result is trimmed to the subject's alpha bounds.
"""
import pathlib
import sys

import numpy as np
from PIL import Image
from rembg import new_session, remove
from scipy import ndimage

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "nevo-q05-solo-source.jpg"
OUT = ROOT / "nevo-q05-solo.webp"
KEEP = 1           # a single car in this frame
PAD = 4
MAX_W = 2200       # plenty for a 1080-wide stage at 2x


def segment(img: Image.Image, session) -> np.ndarray:
    """Alpha channel for one crop, as uint8."""
    return np.array(remove(img, session=session, post_process_mask=True).split()[-1])


def main() -> None:
    img = Image.open(SRC).convert("RGB")
    w, h = img.size
    session = new_session("isnet-general-use")

    alpha = segment(img, session)

    labels, count = ndimage.label(alpha > 24)
    if count == 0:
        sys.exit("segmentation returned an empty mask")
    sizes = ndimage.sum(np.ones_like(labels), labels, range(1, count + 1))
    keep = np.argsort(sizes)[-KEEP:] + 1
    alpha[~np.isin(labels, keep)] = 0

    out = img.convert("RGBA")
    out.putalpha(Image.fromarray(alpha))
    box = out.getbbox()
    l, t, r, b = box
    out = out.crop((max(0, l - PAD), max(0, t - PAD), min(w, r + PAD), min(h, b + PAD)))
    if out.width > MAX_W:
        out = out.resize((MAX_W, round(out.height * MAX_W / out.width)), Image.LANCZOS)
    out.save(OUT, quality=92, method=6)   # WebP keeps the alpha at a fraction of PNG's size
    print(f"{OUT.name}: {out.width}x{out.height}, ratio {out.width / out.height:.3f}, "
          f"{OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
