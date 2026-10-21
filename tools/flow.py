# Usage: python3 tools/flow.py   (writes assets/flow-light.svg and assets/flow-dark.svg)
"""Generates assets/flow-light.svg and assets/flow-dark.svg: point and talk, a round, your Claude Code session."""
import sys
from pathlib import Path

from banner import ASSETS, LIGHT, DARK, SANS, MONO, POINTER, check


def panel(x, c):
    return f'<g filter="url(#sh)"><rect x="{x}" y="28" width="340" height="196" rx="18" fill="{c["glass"]}"/></g>' \
           f'<rect x="{x + .5}" y="28.5" width="339" height="195" rx="17.5" fill="none" stroke="{c["glass_line"]}"/>'


def pin(x, y, n, c, done=False):
    head = c["green"] if done else c["pin"]
    label = (f'<path d="M{x - 4.2} {y - 18}l2.8 2.8 5.4-6" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
             if done else f'<text x="{x}" y="{y - 14.4}" text-anchor="middle" font-size="11" font-weight="800" fill="{c["pin_ink"]}">{n}</text>')
    return (f'<rect x="{x - 1}" y="{y - 9}" width="2" height="9" rx="1" fill="{head}"/>'
            f'<circle cx="{x}" cy="{y - 18}" r="10" fill="{head}" stroke="{c["pin_ring"]}" stroke-width="2"/>{label}')


def arrow(x1, x2, y, label, c):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2 - 6}" y2="{y}" stroke="{c["amber_line"]}" stroke-width="1.6" stroke-linecap="round"/>'
            f'<path d="M{x2 - 9} {y - 5}l7 5-7 5" fill="none" stroke="{c["amber_line"]}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<text x="{(x1 + x2) / 2}" y="{y - 12}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{c["ink3"]}">{label}</text>')


def caption(x, title, line, c):
    return (f'<text x="{x}" y="264" font-size="16" font-weight="700" fill="{c["ink"]}">{title}</text>'
            f'<text x="{x}" y="288" font-size="14" fill="{c["ink2"]}">{line}</text>')


def build(c):
    W, H = 1280, 320
    a, b, d = 70, 470, 870
    # Panel 1: a page with a pin and the spoken line.
    p1 = f"""
  <rect x="{a + 22}" y="50" width="296" height="110" rx="10" fill="{c['oc_bg']}" stroke="{c['oc_line']}"/>
  <text x="{a + 40}" y="82" font-size="15" font-weight="700" fill="{c['oc_ink']}">Lisbon</text>
  <rect x="{a + 40}" y="92" width="96" height="6" rx="3" fill="{c['oc_line']}"/>
  <rect x="{a + 40}" y="120" width="140" height="24" rx="7" fill="{c['oc_line']}" fill-opacity=".7"/>
  <rect x="{a + 214}" y="116" width="52" height="20" rx="6" fill="{c['oc_brand']}"/>
  <text x="{a + 240}" y="130" text-anchor="middle" font-size="10.5" font-weight="650" fill="{c['oc_bg']}">Book</text>
  {pin(a + 250, 118, 1, c)}
  <path d="{POINTER}" transform="translate({a + 258} 128) scale(.9) translate(-2 -2)" fill="#111" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/>
  <circle cx="{a + 34}" cy="190" r="8" fill="{c['pin']}"/>
  <text x="{a + 34}" y="194" text-anchor="middle" font-size="10" font-weight="800" fill="{c['pin_ink']}">1</text>
  <text x="{a + 50}" y="195" font-size="14" fill="{c['ink']}"><tspan font-weight="700" fill="{c['amber_ink']}">This</tspan> button is too small.</text>"""
    # Panel 2: the round.
    rows = ""
    for i, (txt, img) in enumerate((("Button too small", c["img"][0]), ("Gap too big", c["img"][1]))):
        y = 92 + i * 58
        rows += f"""
  <rect x="{b + 22}" y="{y}" width="64" height="44" rx="8" fill="{img[0]}"/>
  <rect x="{b + 22}" y="{y + 22}" width="64" height="22" rx="0" fill="{img[1]}" fill-opacity=".55"/>
  <rect x="{b + 22}" y="{y}" width="64" height="44" rx="8" fill="none" stroke="{c['oc_line']}"/>
  <circle cx="{b + 108}" cy="{y + 22}" r="10" fill="{c['pin']}"/>
  <text x="{b + 108}" y="{y + 26}" text-anchor="middle" font-size="11" font-weight="800" fill="{c['pin_ink']}">{i + 1}</text>
  <text x="{b + 128}" y="{y + 27}" font-size="14" fill="{c['ink']}">{txt}</text>"""
    p2 = f"""
  <text x="{b + 22}" y="66" font-size="13" fill="{c['ink2']}"><tspan font-weight="700" fill="{c['ink']}">Trip Planner</tspan> · Oct 21</text>
  <text x="{b + 318}" y="66" text-anchor="end" font-size="12.5" fill="{c['ink3']}">2 points</text>
  <rect x="{b}" y="78" width="340" height=".8" fill="{c['line']}"/>{rows}"""
    # Panel 3: the session.
    p3 = f"""
  <rect x="{d + 14}" y="42" width="312" height="168" rx="10" fill="{c['term']}"/>
  <g font-family="{MONO}" font-size="12" fill="{c['term_ink']}" xml:space="preserve">
    <text x="{d + 30}" y="70" fill="{c['term_dim']}">&gt; /deixis-watch</text>
    <text x="{d + 30}" y="94"><tspan fill="#ffb24a">●</tspan> watch_rounds()</text>
    <text x="{d + 30}" y="114" fill="{c['term_dim']}" xml:space="preserve">  Trip Planner · 2 points</text>
    <text x="{d + 30}" y="138"><tspan fill="#ffb24a">●</tspan> set_status(in_progress)</text>
    {check(d + 30, 162, "#6fd48b")}<text x="{d + 44.4}" y="162">Point 1 done</text>
    {check(d + 30, 186, "#6fd48b")}<text x="{d + 44.4}" y="186">Point 2 done</text>
  </g>"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc" font-family="{SANS}">
<title id="title">How a round reaches a Claude Code session</title>
<desc id="desc">Three steps. Point and talk: a pin drops on a button while you say this button is too small. A round: the Trip Planner round of Oct 21 holds two numbered points, each with a picture. Your session: Claude Code receives the round through watch_rounds and marks each point done.</desc>
<defs>
  <filter id="sh" x="-20%" y="-20%" width="140%" height="170%"><feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="{c['shadow']}" flood-opacity="{float(c['shadow_op']) * .7:.2f}"/></filter>
  <linearGradient id="wall" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{c['wall'][0]}"/><stop offset=".52" stop-color="{c['wall'][1]}"/><stop offset="1" stop-color="{c['wall'][2]}"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="22" fill="url(#wall)"/>
{panel(a, c)}{p1}
{panel(b, c)}{p2}
{panel(d, c)}{p3}
{arrow(a + 348, b - 8, 126, "send", c)}
{arrow(b + 348, d - 8, 126, "deliver", c)}
{caption(a + 4, "1  Point and talk", "Hold right ⌥, point at it and say what should change.", c)}
{caption(b + 4, "2  A round", "Numbered points, each with a picture.", c)}
{caption(d + 4, "3  Your session", "Claude Code works through it point by point.", c)}
</svg>
"""


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ASSETS
    (out / "flow-light.svg").write_text(build(LIGHT))
    (out / "flow-dark.svg").write_text(build(DARK))
