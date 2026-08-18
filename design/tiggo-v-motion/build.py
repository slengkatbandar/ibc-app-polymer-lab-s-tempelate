#!/usr/bin/env python3
"""Inline the cropped TIGGO V photo into src/template.html -> index.html (self-contained)."""
import base64, pathlib

root = pathlib.Path(__file__).parent
img = base64.b64encode((root / "src" / "tiggo-v-card.jpg").read_bytes()).decode()
html = (root / "src" / "template.html").read_text(encoding="utf-8")
html = html.replace("__CAR_IMAGE__", "data:image/jpeg;base64," + img)
(root / "index.html").write_text(html, encoding="utf-8")
print("index.html:", len(html), "bytes")
