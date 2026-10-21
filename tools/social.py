# Usage: python3 tools/social.py   (writes assets/social-preview.svg; tools/social.sh renders the PNG from it)
"""Generates assets/social-preview.svg, the 1280 x 640 GitHub social preview.

Same visual language as the banner: the still frame of the banner scene on the right, brand and tagline on the left.
Everything stays inside a 40 px safe margin.
"""
import re
import sys
from pathlib import Path

from banner import ASSETS, DISPLAY, LIGHT, MONO, POINTER, SANS, build

W, H, MARGIN = 1280, 640, 40
# Part of the banner that holds the scene: Trip Planner window, pins, spoken-line card and Claude Code session.
CROP = (584, 30, 648, 370)
SCALE = 1.0


def still_scene(c):
    """The banner markup without its background, brand block and title, frozen on the composed still frame."""
    svg = build(c, "light")
    svg = svg.replace('<rect width="1280" height="400" fill="url(#wall)"/>', "", 1)
    svg = svg.replace('<g clip-path="url(#frame)">', "<g>", 1)
    svg = re.sub(r"<!-- Brand -->.*?(?=<!-- Trip Planner window -->)", "", svg, count=1, flags=re.S)
    svg = re.sub(r"<title[^>]*>.*?</title>\s*<desc[^>]*>.*?</desc>\s*", "", svg, count=1, flags=re.S)
    svg = svg.replace("</style>", ".a,.wv{animation:none!important}</style>", 1)
    x, y, w, h = CROP
    sw, sh = w * SCALE, h * SCALE
    sx, sy = W - MARGIN - sw, (H - sh) / 2 + 10
    head = (f'<svg x="{sx:g}" y="{sy:g}" width="{sw:g}" height="{sh:g}" viewBox="{x} {y} {w} {h}" '
            f'overflow="visible" aria-hidden="true" font-family="{SANS}"')
    return re.sub(r"^<svg [^>]*", head, svg, count=1)


def social(c):
    tx = MARGIN + 44
    ring = "#ffffff"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="s-title" font-family="{SANS}">
<title id="s-title">Deixis, Claude Code plugin. Show it, don't describe it.</title>
<defs>
  <linearGradient id="s-wall" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{c['wall'][0]}"/><stop offset=".52" stop-color="{c['wall'][1]}"/><stop offset="1" stop-color="{c['wall'][2]}"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#s-wall)"/>
<text x="{tx}" y="196" font-family="{MONO}" font-size="20" font-weight="600" letter-spacing="3.4" fill="{c['amber_ink']}">CLAUDE CODE PLUGIN</text>
<g>
  <circle cx="{tx + 26}" cy="250" r="26" fill="{c['amber']}"/>
  <path d="{POINTER}" transform="translate({tx + 43} 267) scale(1.6) translate(-2 -2)" fill="{c['ink']}" stroke="{ring}" stroke-width="1.8" stroke-linejoin="round"/>
</g>
<text x="{tx + 82}" y="280" font-family="{DISPLAY}" font-size="84" font-weight="700" letter-spacing="-1.8" fill="{c['ink']}">Deixis</text>
<g font-family="{DISPLAY}" font-size="44" font-weight="650" letter-spacing="-.6" fill="{c['ink']}">
  <text x="{tx}" y="372">Show it,</text>
  <text x="{tx}" y="424">don’t describe it.</text>
</g>
<text x="{tx}" y="476" font-size="22" fill="{c['ink2']}">Screenshot feedback for the Mac</text>
{still_scene(c)}
</svg>
"""


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ASSETS
    out.mkdir(parents=True, exist_ok=True)
    (out / "social-preview.svg").write_text(social(LIGHT))
