# Usage: python3 tools/flow.py   (writes assets/flow-{1,2,3}-{light,dark}.svg)
"""Generates the three step images of the README: point and talk, a round, your Claude Code session.

Each image is 880 x 384 on an 8 px grid with a 32 px outer margin. The README shows them across the full 830 px column,
so the smallest text (28 px) reads at about 26 px on a desktop and still about 11 px on a 360 px wide phone.
"""
import sys
from pathlib import Path

from banner import ASSETS, LIGHT, DARK, SANS, DISPLAY, MONO, POINTER, check, spark

W, H = 880, 384


def frame(c, title, desc, body, extra_defs=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc" font-family="{SANS}">
<title id="title">{title}</title>
<desc id="desc">{desc}</desc>
<defs>
  <filter id="sh" x="-20%" y="-20%" width="140%" height="170%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="{c['shadow']}" flood-opacity="{float(c['shadow_op']) * .6:.2f}"/></filter>
  <filter id="shs" x="-60%" y="-60%" width="220%" height="240%"><feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-color="#000" flood-opacity=".3"/></filter>
  <linearGradient id="wall" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{c['wall'][0]}"/><stop offset=".52" stop-color="{c['wall'][1]}"/><stop offset="1" stop-color="{c['wall'][2]}"/>
  </linearGradient>{extra_defs}
</defs>
<rect width="{W}" height="{H}" rx="16" fill="url(#wall)"/>
{body}
</svg>
"""


def glass(x, y, w, h, c, rx=16):
    return (f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c["glass"]}"/></g>'
            f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="{rx - .5}" fill="none" stroke="{c["glass_line"]}"/>')


def badge(cx, cy, n, c):
    return (f'<circle cx="{cx}" cy="{cy}" r="22" fill="{c["pin"]}"/>'
            f'<text x="{cx}" y="{cy + 10}" text-anchor="middle" font-size="28" font-weight="800" fill="{c["pin_ink"]}">{n}</text>')


def step1(c):
    """A page with a pin on a button and the spoken line."""
    body = f"""
<g filter="url(#sh)"><rect x="32" y="32" width="816" height="192" rx="16" fill="{c['oc_bg']}"/></g>
<rect x="32.5" y="32.5" width="815" height="191" rx="15.5" fill="none" stroke="{c['oc_line']}"/>
<text x="64" y="120" font-family="{DISPLAY}" font-size="52" font-weight="700" letter-spacing="-.8" fill="{c['oc_ink']}">Lisbon</text>
<text x="64" y="176" font-size="30" fill="{c['oc_ink2']}">4 nights · 2 guests</text>
<rect x="632" y="112" width="176" height="80" rx="18" fill="{c['amber_soft']}" stroke="{c['amber_line']}" stroke-width="2"/>
<rect x="640" y="120" width="160" height="64" rx="12" fill="{c['oc_brand']}"/>
<text x="720" y="163" text-anchor="middle" font-size="30" font-weight="650" fill="{c['oc_bg']}">Book</text>
<rect x="717.5" y="92" width="5" height="32" rx="2" fill="{c['pin']}"/>
<circle cx="720" cy="72" r="24" fill="{c['pin']}" stroke="{c['pin_ring']}" stroke-width="3" filter="url(#shs)"/>
<text x="720" y="82" text-anchor="middle" font-size="28" font-weight="800" fill="{c['pin_ink']}">1</text>
<path d="{POINTER}" transform="translate(768 160) scale(1.6) translate(-2 -2)" fill="#111" stroke="#fff" stroke-width="1.3" stroke-linejoin="round" filter="url(#shs)"/>
{glass(32, 256, 816, 96, c)}
{badge(80, 304, 1, c)}
<text x="128" y="315" font-size="32" fill="{c['ink']}"><tspan font-weight="700" fill="{c['amber_ink']}">This</tspan> button is too small.</text>"""
    return frame(c, "Step 1: point and talk",
                 "A pin with the number 1 drops on the Book button of a Trip Planner page while you say: this button is too small.",
                 body)


def step2(c):
    """The round: two numbered points, each with a picture."""
    rows = ""
    for i, txt in enumerate(("Button too small", "Gap too big")):
        y = 136 + i * 104
        rows += f"""
<rect x="64" y="{y}" width="136" height="88" rx="10" fill="url(#img{i})"/>
<rect x="64.5" y="{y + .5}" width="135" height="87" rx="9.5" fill="none" stroke="{c['oc_line']}"/>
{badge(248, y + 44, i + 1, c)}
<text x="288" y="{y + 55}" font-size="32" fill="{c['ink']}">{txt}</text>"""
    grads = "".join(
        f'\n  <linearGradient id="img{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
        for i, (a, b) in enumerate(c["img"][:2]))
    body = f"""
{glass(32, 32, 816, 320, c)}
<text x="64" y="84" font-size="28" fill="{c['ink2']}"><tspan font-weight="700" fill="{c['ink']}">Trip Planner</tspan> · Oct 21</text>
<text x="816" y="84" text-anchor="end" font-size="28" fill="{c['ink3']}">2 points</text>
<rect x="32" y="111.5" width="816" height="1" fill="{c['line']}"/>{rows}"""
    return frame(c, "Step 2: a round",
                 "The Trip Planner round of Oct 21 holds two numbered points, each with a picture: button too small, gap too big.",
                 body, grads)


def step3(c):
    """The Claude Code session working through the round."""
    s = 28 / 11.5
    body = f"""
<g filter="url(#sh)"><rect x="32" y="32" width="816" height="320" rx="16" fill="{c['term']}"/></g>
<rect x="32" y="87.5" width="816" height="1" fill="#ffffff" fill-opacity=".1"/>
<circle cx="64" cy="60" r="8" fill="#ffffff" fill-opacity=".18"/><circle cx="88" cy="60" r="8" fill="#ffffff" fill-opacity=".18"/><circle cx="112" cy="60" r="8" fill="#ffffff" fill-opacity=".18"/>
<g font-family="{MONO}" font-size="28" fill="{c['term_ink']}">
  {spark(144, 70, "#ffb24a", s)}<text x="176" y="70">Claude Code</text>
  <text x="64" y="136" fill="{c['term_dim']}">&gt; /deixis-watch</text>
  <text x="64" y="180"><tspan fill="#ffb24a">●</tspan> watch_rounds()</text>
  <text x="64" y="224" xml:space="preserve" fill="{c['term_dim']}">  Trip Planner · 2 points</text>
  {check(64, 268, "#6fd48b", s)}<text x="100" y="268">Point 1 done</text>
  {check(64, 312, "#6fd48b", s)}<text x="100" y="312">Point 2 done</text>
</g>"""
    return frame(c, "Step 3: your Claude Code session",
                 "Claude Code receives the round through watch_rounds and marks point 1 and point 2 done.",
                 body)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ASSETS
    out.mkdir(parents=True, exist_ok=True)
    for n, step in enumerate((step1, step2, step3), 1):
        (out / f"flow-{n}-light.svg").write_text(step(LIGHT))
        (out / f"flow-{n}-dark.svg").write_text(step(DARK))
