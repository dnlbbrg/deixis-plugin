# Usage: python3 tools/flow.py   (writes assets/flow-{1,2,3}-{light,dark}.svg)
"""Generates the three step images of the README: point and talk, a round, your Claude Code session.

Each image is 560 x 288 on an 8 px grid with a 32 px outer margin. The README shows them at 560 px, so text is at
least 20 px on a desktop and still about 12 px on a 360 px wide phone.
"""
import sys
from pathlib import Path

from banner import ASSETS, LIGHT, DARK, SANS, DISPLAY, MONO, POINTER, check, spark

W, H = 560, 288


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
    return (f'<circle cx="{cx}" cy="{cy}" r="15" fill="{c["pin"]}"/>'
            f'<text x="{cx}" y="{cy + 7}" text-anchor="middle" font-size="20" font-weight="800" fill="{c["pin_ink"]}">{n}</text>')


def step1(c):
    """A page with a pin on a button and the spoken line."""
    body = f"""
<g filter="url(#sh)"><rect x="32" y="32" width="496" height="136" rx="12" fill="{c['oc_bg']}"/></g>
<rect x="32.5" y="32.5" width="495" height="135" rx="11.5" fill="none" stroke="{c['oc_line']}"/>
<text x="56" y="88" font-family="{DISPLAY}" font-size="32" font-weight="700" letter-spacing="-.5" fill="{c['oc_ink']}">Lisbon</text>
<text x="56" y="128" font-size="20" fill="{c['oc_ink2']}">4 nights · 2 guests</text>
<rect x="404" y="92" width="104" height="48" rx="12" fill="{c['amber_soft']}" stroke="{c['amber_line']}" stroke-width="1.6"/>
<rect x="408" y="96" width="96" height="40" rx="9" fill="{c['oc_brand']}"/>
<text x="456" y="123" text-anchor="middle" font-size="20" font-weight="650" fill="{c['oc_bg']}">Book</text>
<rect x="454.5" y="80" width="3" height="16" rx="1.2" fill="{c['pin']}"/>
<circle cx="456" cy="64" r="16" fill="{c['pin']}" stroke="{c['pin_ring']}" stroke-width="2.4" filter="url(#shs)"/>
<text x="456" y="71" text-anchor="middle" font-size="20" font-weight="800" fill="{c['pin_ink']}">1</text>
<path d="{POINTER}" transform="translate(488 126) scale(1.2) translate(-2 -2)" fill="#111" stroke="#fff" stroke-width="1.5" stroke-linejoin="round" filter="url(#shs)"/>
{glass(32, 192, 496, 64, c)}
{badge(64, 224, 1, c)}
<text x="96" y="232" font-size="22" fill="{c['ink']}"><tspan font-weight="700" fill="{c['amber_ink']}">This</tspan> button is too small.</text>"""
    return frame(c, "Step 1: point and talk",
                 "A pin with the number 1 drops on the Book button of a Trip Planner page while you say: this button is too small.",
                 body)


def step2(c):
    """The round: two numbered points, each with a picture."""
    rows = ""
    for i, (txt, img) in enumerate((("Button too small", c["img"][0]), ("Gap too big", c["img"][1]))):
        y = 112 + i * 72
        rows += f"""
<rect x="56" y="{y}" width="88" height="56" rx="8" fill="url(#img{i})"/>
<rect x="56.5" y="{y + .5}" width="87" height="55" rx="7.5" fill="none" stroke="{c['oc_line']}"/>
{badge(176, y + 28, i + 1, c)}
<text x="208" y="{y + 36}" font-size="22" fill="{c['ink']}">{txt}</text>"""
    grads = "".join(
        f'\n  <linearGradient id="img{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
        for i, (a, b) in enumerate(c["img"][:2]))
    body = f"""
{glass(32, 32, 496, 224, c)}
<text x="56" y="72" font-size="20" fill="{c['ink2']}"><tspan font-weight="700" fill="{c['ink']}">Trip Planner</tspan> · Oct 21</text>
<text x="504" y="72" text-anchor="end" font-size="20" fill="{c['ink3']}">2 points</text>
<rect x="32" y="95.5" width="496" height="1" fill="{c['line']}"/>{rows}"""
    return frame(c, "Step 2: a round",
                 "The Trip Planner round of Oct 21 holds two numbered points, each with a picture: button too small, gap too big.",
                 body, grads)


def step3(c):
    """The Claude Code session working through the round."""
    s = 20 / 11.5
    body = f"""
<g filter="url(#sh)"><rect x="32" y="32" width="496" height="224" rx="12" fill="{c['term']}"/></g>
<rect x="32" y="71.5" width="496" height="1" fill="#ffffff" fill-opacity=".1"/>
<circle cx="56" cy="52" r="6" fill="#ffffff" fill-opacity=".18"/><circle cx="76" cy="52" r="6" fill="#ffffff" fill-opacity=".18"/><circle cx="96" cy="52" r="6" fill="#ffffff" fill-opacity=".18"/>
<g font-family="{MONO}" font-size="20" fill="{c['term_ink']}">
  {spark(120, 59, "#ffb24a", s)}<text x="144" y="59">Claude Code</text>
  <text x="56" y="112" fill="{c['term_dim']}">&gt; /deixis-watch</text>
  <text x="56" y="140"><tspan fill="#ffb24a">●</tspan> watch_rounds()</text>
  <text x="56" y="168" xml:space="preserve" fill="{c['term_dim']}">  Trip Planner · 2 points</text>
  {check(56, 196, "#6fd48b", s)}<text x="80" y="196">Point 1 done</text>
  {check(56, 224, "#6fd48b", s)}<text x="80" y="224">Point 2 done</text>
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
