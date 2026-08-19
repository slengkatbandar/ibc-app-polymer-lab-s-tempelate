#!/usr/bin/env python3
"""Fetch the Google Fonts faces this design uses and inline them as data URIs.

Keeps the published artifact and the exported video pixel-identical, and removes
the runtime dependency on fonts.googleapis.com.
"""
import base64, pathlib, re, subprocess, sys

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/131.0.0.0 Safari/537.36")
FAMILIES = [
    "Archivo:wdth,wght@62..125,400..700",
    "IBM+Plex+Sans:wght@400;500;600",
    "IBM+Plex+Mono:wght@400;500",
]
KEEP_SUBSETS = ("latin",)   # Indonesian copy needs nothing beyond basic Latin


def fetch(url: str) -> bytes:
    out = subprocess.run(["curl", "-sSL", "-A", UA, url], capture_output=True, check=True)
    return out.stdout


def main() -> None:
    root = pathlib.Path(__file__).parent
    url = "https://fonts.googleapis.com/css2?" + "&".join("family=" + f for f in FAMILIES) + "&display=swap"
    css = fetch(url).decode("utf-8")

    blocks, kept = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{[^}]*\})", css), []
    if not blocks:
        sys.exit("no @font-face blocks returned — check the request URL")
    for subset, block in blocks:
        if subset not in KEEP_SUBSETS:
            continue
        m = re.search(r"url\((https://[^)]+\.woff2)\)", block)
        if not m:
            continue
        data = base64.b64encode(fetch(m.group(1))).decode()
        kept.append(block.replace(m.group(1), "data:font/woff2;base64," + data))

    (root / "fonts.css").write_text("\n".join(kept), encoding="utf-8")
    print(f"fonts.css: {len(kept)} faces, {(root / 'fonts.css').stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
