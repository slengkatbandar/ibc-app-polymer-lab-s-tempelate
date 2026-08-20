#!/usr/bin/env python3
"""Cuts the two Nevo Q05 units out of the location photo.

Segmentation is rembg's isnet-general-use model (github.com/danielgatis/rembg).
Each car is segmented from its own half of the frame so the model sees it at a
higher effective resolution - segmenting the full 4096px frame in one pass
clipped the tyres. Afterwards only the two largest connected regions are kept,
which drops stray keeps such as the painted parking line between the cars.
"""
import pathlib
import sys

import numpy as np
from PIL import Image
from rembg import new_session, remove
from scipy import ndimage

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "nevo-q05-pair-source.png"
OUT = ROOT / "nevo-q05-pair.webp"
SPLIT = 0.505      # the gap between the two cars, as a fraction of the width
OVERLAP = 120      # px of overlap so neither car is cut by the split itself
KEEP = 2           # number of subjects to keep
PAD = 4
MAX_W = 2200       # plenty for a 1080-wide stage at 2x


def segment(img: Image.Image, session) -> np.ndarray:
    """Alpha channel for one crop, as uint8."""
    return np.array(remove(img, session=session, post_process_mask=True).split()[-1])


def main() -> None:
    img = Image.open(SRC).convert("RGB")
    w, h = img.size
    cut = int(w * SPLIT)
    session = new_session("isnet-general-use")

    alpha = np.zeros((h, w), dtype=np.uint8)
    left = (0, 0, min(w, cut + OVERLAP), h)
    right = (max(0, cut - OVERLAP), 0, w, h)
    for box in (left, right):
        part = segment(img.crop(box), session)
        region = alpha[box[1]:box[3], box[0]:box[2]]
        np.maximum(region, part, out=region)

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
