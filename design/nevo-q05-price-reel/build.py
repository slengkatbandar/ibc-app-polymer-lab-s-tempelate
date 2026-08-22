#!/usr/bin/env python3
"""Inline the cropped photo and the webfonts into src/template.html -> index.html."""
import base64, pathlib

root = pathlib.Path(__file__).parent
img = base64.b64encode((root / "src" / "nevo-q05-solo.webp").read_bytes()).decode()
html = (root / "src" / "template.html").read_text(encoding="utf-8")
html = html.replace("__CAR_IMAGE__", "data:image/webp;base64," + img)
html = html.replace("__FONTS__", (root / "src" / "fonts.css").read_text(encoding="utf-8"))
(root / "index.html").write_text(html, encoding="utf-8")
print("index.html:", len(html), "bytes")
