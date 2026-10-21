# Usage: python3 tools/social.py   (writes assets/social-preview.svg; tools/social.sh renders the PNG from it)
"""Generates assets/social-preview.svg, the 1280 x 640 GitHub social preview.

The still frame of the banner (brand, tagline and scene) scaled up to the full height, on the same wallpaper.
The banner keeps its own 40 px margin, so everything stays at least 49 px from the edges.
"""
import re
import sys
from pathlib import Path

from banner import ASSETS, LIGHT, SANS, W as BW, H as BH, build

W, H = 1280, 640
SCALE = H / BH


def still_banner(c):
    """The banner markup without its background, frozen on the composed still frame."""
    svg = build(c, "light")
    svg = svg.replace(f'<rect width="{BW}" height="{BH}" fill="url(#wall)"/>', "", 1)
    svg = svg.replace('<g clip-path="url(#frame)">', "<g>", 1)
    svg = re.sub(r"<title[^>]*>.*?</title>\s*<desc[^>]*>.*?</desc>\s*", "", svg, count=1, flags=re.S)
    svg = svg.replace("</style>", ".a,.wv{animation:none!important}</style>", 1)
    sw, sh = BW * SCALE, BH * SCALE
    head = (f'<svg x="{(W - sw) / 2:g}" y="0" width="{sw:g}" height="{sh:g}" viewBox="0 0 {BW} {BH}" '
            f'aria-hidden="true" font-family="{SANS}"')
    return re.sub(r"^<svg [^>]*", head, svg, count=1)


def social(c):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="s-title" font-family="{SANS}">
<title id="s-title">Deixis, Claude Code plugin. Show it, don't describe it.</title>
<defs>
  <linearGradient id="s-wall" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{c['wall'][0]}"/><stop offset=".52" stop-color="{c['wall'][1]}"/><stop offset="1" stop-color="{c['wall'][2]}"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#s-wall)"/>
{still_banner(c)}
</svg>
"""


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ASSETS
    out.mkdir(parents=True, exist_ok=True)
    (out / "social-preview.svg").write_text(social(LIGHT))
