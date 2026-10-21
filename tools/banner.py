# Usage: python3 tools/banner.py   (writes assets/banner-light.svg and assets/banner-dark.svg)
"""Generates assets/banner-light.svg and assets/banner-dark.svg for the Deixis plugin README.

One 8 s CSS loop. Base styles are the composed still frame, so prefers-reduced-motion simply drops the animations.
"""
import sys
from pathlib import Path

LIGHT = dict(
    wall=("#dde5ee", "#ece8e2", "#f2e2d6"),
    ink="#1d1d1f", ink2="#55555c", ink3="#8e8e95",
    line="rgba(0,0,0,.09)",
    glass="rgba(250,250,252,.88)", glass_line="rgba(255,255,255,.9)",
    shadow="#1e1e28", shadow_op=".30",
    amber="#ffa31a", amber_ink="#8f4b00", amber_soft="rgba(255,163,26,.16)", amber_line="rgba(240,140,0,.85)",
    pin="#ffaa2b", pin_ink="#3a2200", pin_ring="#ffffff",
    green="#2b9e4c",
    oc_bg="#f6f7f9", oc_card="#ffffff", oc_line="#e6e8ec", oc_ink="#1b1f24", oc_ink2="#68707b",
    oc_brand="#0f6b5c", oc_brand2="#d8ece8", oc_bar="#eef0f3",
    term="#1b1c1f", term_ink="#d9dade", term_dim="#8a8d94",
    kbd="rgba(0,0,0,.06)",
    img=(("#a9d2ec", "#4d8fc2"), ("#f6dfba", "#e2a466"), ("#f7c1a0", "#8d74b4")),
)
DARK = dict(
    wall=("#141a24", "#18171d", "#221817"),
    ink="#f2f2f4", ink2="#a9a9b1", ink3="#7a7a83",
    line="rgba(255,255,255,.12)",
    glass="rgba(40,40,46,.9)", glass_line="rgba(255,255,255,.1)",
    shadow="#000000", shadow_op=".6",
    amber="#ffae33", amber_ink="#ffbe55", amber_soft="rgba(255,170,50,.18)", amber_line="rgba(255,180,70,.85)",
    pin="#ffaa2b", pin_ink="#3a2200", pin_ring="#2a2a30",
    green="#4cc36f",
    oc_bg="#16181c", oc_card="#1e2126", oc_line="#2c3036", oc_ink="#e9ecef", oc_ink2="#959ca6",
    oc_brand="#3fbfa6", oc_brand2="#1d3833", oc_bar="#202328",
    term="#0b0c0e", term_ink="#d9dade", term_dim="#8a8d94",
    kbd="rgba(255,255,255,.1)",
    img=(("#2f5f86", "#173a5a"), ("#6b5638", "#3e3022"), ("#6a4a5e", "#352a4a")),
)

SANS = "-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', system-ui, 'Helvetica Neue', Arial, sans-serif"
DISPLAY = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', system-ui, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"

POINTER = "M2 2v22l6-5.6 3.8 8.6 3.4-1.5-3.7-8.4H20z"
ASSETS = Path(__file__).resolve().parent.parent / "assets"


def check(x, y, color, s=1.0):
    """A drawn check mark one monospace cell wide (at 11.5 px times s), sitting on baseline y. Drawn so no platform swaps in an emoji."""
    return (f'<path d="M{x + .6 * s:g} {y - 4.2 * s:g}l{2.4 * s:g} {2.6 * s:g} {4.6 * s:g} {-6 * s:g}" fill="none" stroke="{color}" '
            f'stroke-width="{1.7 * s:g}" stroke-linecap="round" stroke-linejoin="round"/>')


def spark(x, y, color, s=1.0):
    """A drawn six-spoke asterisk one monospace cell wide (at 11.5 px times s), sitting on baseline y."""
    cx, cy, r = x + 3.5 * s, y - 4 * s, 4.3 * s
    d = f"M{cx:g} {cy - r:g}v{2 * r:g}"
    d += f"M{cx - r * .866:.2f} {cy - r / 2:.2f}l{r * 1.732:.2f} {r:.2f}M{cx - r * .866:.2f} {cy + r / 2:.2f}l{r * 1.732:.2f} {-r:.2f}"
    return f'<path d="{d}" stroke="{color}" stroke-width="{1.7 * s:g}" stroke-linecap="round"/>'


EASE = "cubic-bezier(.45,0,.2,1)"

# Cursor positions (tip): rest, target 1 (top edge of the Book button), target 2 (the wide gap between trip cards).
# Canvas: 880 x 520, laid out on an 8 px grid with a 40 px outer margin, so it reads at GitHub's 830 px column.
W, H, M = 880, 520, 40
REST, T1, T2 = (304, 312), (464, 266), (208, 432)

# Words of the two spoken lines and the loop percentage at which each appears.
LINE1 = [("This", 19.0, True), ("button", 21.0, False), ("is", 22.6, False), ("too", 24.0, False), ("small.", 25.6, False)]
LINE2 = [("Here", 41.0, True), ("the", 43.0, False), ("gap", 44.4, False), ("is", 46.0, False), ("too", 47.4, False), ("big.", 49.0, False)]


def keyframes(name, frames):
    """frames: list of (percent list, css body, optional easing)."""
    out = [f"@keyframes {name}{{"]
    for pcts, body, *ease in frames:
        sel = ",".join(f"{p:g}%" for p in pcts)
        e = f"animation-timing-function:{ease[0]};" if ease else ""
        out.append(f"{sel}{{{body};{e}}}")
    out.append("}")
    return "".join(out)


def fade(name, on, off=None, prop="opacity", dur=1.2):
    """Visible from `on` (fading in over `dur` percent) until `off` (fading out), else hidden."""
    if off is None:
        return keyframes(name, [([0, on], f"{prop}:0"), ([on + dur, 100], f"{prop}:1")])
    return keyframes(name, [([0, on], f"{prop}:0"), ([on + dur, off], f"{prop}:1"), ([off + 3, 100], f"{prop}:0")])


def css(c):
    k = []
    t = lambda p: f"transform:translate({p[0]}px,{p[1]}px)"
    k.append(keyframes("cur", [
        ([0, 6], t(REST), EASE), ([18, 30], t(T1), EASE), ([40, 56], t(T2), EASE), ([68, 100], t(REST)),
    ]))
    k.append(keyframes("listen", [([0, 5], "opacity:0"), ([9, 54], "opacity:1"), ([60, 100], "opacity:0")]))
    k.append(keyframes("card", [
        ([0, 7], "opacity:0;transform:translateY(8px) scale(.97)", "cubic-bezier(.16,1,.3,1)"),
        ([11, 56], "opacity:1;transform:none"), ([61, 100], "opacity:0;transform:translateY(-6px)"),
    ]))
    k.append(keyframes("c0", [([0, 21.6], "opacity:1"), ([22.6, 100], "opacity:0")]))
    k.append(keyframes("c1", [([0, 21.6], "opacity:0"), ([22.6, 43.6], "opacity:1"), ([44.6, 100], "opacity:0")]))
    k.append(keyframes("c2", [([0, 43.6], "opacity:0"), ([44.6, 100], "opacity:1")]))
    for i, (_, p, _) in enumerate(LINE1 + LINE2):
        k.append(fade(f"w{i}", p, prop="fill-opacity", dur=1.0))
    for i, p in ((1, 19.0), (2, 41.0)):
        k.append(fade(f"b{i}", p, dur=0.8))
        k.append(keyframes(f"th{i}", [
            ([0, p], "stroke-dashoffset:1;opacity:1"), ([p + 2.75], "stroke-dashoffset:0;opacity:1"),
            ([56], "stroke-dashoffset:0;opacity:1"), ([60, 100], "stroke-dashoffset:0;opacity:0"),
        ]))
    for i, p in ((1, 22.0), (2, 44.0)):
        k.append(keyframes(f"pin{i}", [
            ([0, p], "opacity:0;transform:translateY(-14px) scale(.4)", "cubic-bezier(.3,1.5,.5,1)"),
            ([p + 2.4, 91], "opacity:1;transform:none"),
            ([96, 100], "opacity:0;transform:scale(.6)"),
        ]))
        k.append(keyframes(f"rip{i}", [
            ([0, p + 0.6], "opacity:0;transform:scale(.3)"), ([p + 1.2], "opacity:.9;transform:scale(.5)"),
            ([p + 5.5, 100], "opacity:0;transform:scale(1.6)"),
        ]))
        k.append(fade(f"hl{i}", p + 0.4, 90))
    k.append(fade("ok1", 72, 91, dur=1.5))
    k.append(fade("ok2", 82, 91, dur=1.5))
    k.append(fade("t1", 62, 94))
    k.append(fade("t2", 72, 94))
    k.append(fade("t3", 82, 94))
    k.append(keyframes("gring", [
        ([0, 61], "stroke-dashoffset:1;opacity:1"), ([86, 91], "stroke-dashoffset:0;opacity:1"),
        ([96, 100], "stroke-dashoffset:0;opacity:0"),
    ]))
    k.append(keyframes("wave", [([0], "transform:scaleY(.35)"), ([100], "transform:scaleY(1)")]))

    rules = f"""
.a{{animation-duration:8s;animation-iteration-count:infinite;animation-timing-function:linear;animation-fill-mode:both}}
#cur{{transform:translate({T2[0]}px,{T2[1]}px);animation-name:cur}}
.listen{{opacity:0;animation-name:listen}}
#card{{animation-name:card;transform-box:fill-box;transform-origin:50% 0}}
#c0,#c1{{opacity:0}} #c0{{animation-name:c0}} #c1{{animation-name:c1}} #c2{{animation-name:c2}}
#b1{{animation-name:b1}} #b2{{animation-name:b2}}
#th1{{animation-name:th1}} #th2{{animation-name:th2}}
#pin1{{animation-name:pin1}} #pin2{{animation-name:pin2}}
#rip1,#rip2{{opacity:0;transform-box:fill-box;transform-origin:50% 50%}} #rip1{{animation-name:rip1}} #rip2{{animation-name:rip2}}
#hl1{{animation-name:hl1}} #hl2{{animation-name:hl2}}
#ok2,#t3{{opacity:0}} #ok1{{animation-name:ok1}} #ok2{{animation-name:ok2}}
#t1{{animation-name:t1}} #t2{{animation-name:t2}} #t3{{animation-name:t3}}
#gring{{stroke-dashoffset:.35;animation-name:gring}}
.wv{{transform-box:fill-box;transform-origin:50% 50%;animation:wave .9s ease-in-out infinite alternate}}
.wv:nth-child(2){{animation-delay:-.3s}} .wv:nth-child(3){{animation-delay:-.55s}} .wv:nth-child(4){{animation-delay:-.15s}}
""" + "".join(f"#w{i}{{animation-name:w{i}}}" for i in range(len(LINE1 + LINE2))) + """
@media (prefers-reduced-motion: reduce){.a,.wv{animation:none!important}}
"""
    return "\n".join(k) + rules


def words(line, start, y, c):
    parts = []
    for j, (w, _, deictic) in enumerate(line):
        i = start + j
        style = f' fill="{c["amber_ink"]}" font-weight="700"' if deictic else ""
        sep = " " if j else ""
        parts.append(f'<tspan id="w{i}" class="a"{style}>{sep}{w}</tspan>')
    return f'<text x="592" y="{y}" font-size="16" fill="{c["ink"]}" xml:space="preserve">{"".join(parts)}</text>'


def pin(n, x, y, c):
    return f"""
  <g transform="translate({x} {y})">
    <circle id="rip{n}" class="a" cx="0" cy="-4" r="20" fill="none" stroke="{c['amber']}" stroke-width="2"/>
    <g id="pin{n}" class="a">
      <rect x="-1.5" y="-14" width="3" height="14" rx="1.2" fill="{c['pin']}"/>
      <circle cx="0" cy="-28" r="14" fill="{c['pin']}" stroke="{c['pin_ring']}" stroke-width="2.4" filter="url(#shs)"/>
      <text x="0" y="-22.6" text-anchor="middle" font-size="15" font-weight="800" fill="{c['pin_ink']}">{n}</text>
      <g id="ok{n}" class="a">
        <circle cx="0" cy="-28" r="14" fill="{c['green']}" stroke="{c['pin_ring']}" stroke-width="2.4"/>
        <path d="M-6 -28l4 4 7.6-8.4" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
    </g>
  </g>"""


def build(c, mode):
    img = c["img"]
    # Trip Planner window: x 40..520, y 160..480. Cards 112 wide, the first gap (64) is the one that is too big.
    cards = []
    for i, (title, x) in enumerate((("Alfama", 64), ("Belém", 240), ("Sintra", 384))):
        g = img[i]
        cards.append(f"""
    <g>
      <rect x="{x}" y="336" width="112" height="120" rx="10" fill="{c['oc_card']}" stroke="{c['oc_line']}"/>
      <path d="M{x} 346a10 10 0 0 1 10-10h92a10 10 0 0 1 10 10v54h-112z" fill="url(#img{i})"/>
      <text x="{x + 12}" y="424" font-size="15" font-weight="650" fill="{c['oc_ink']}">{title}</text>
      <rect x="{x + 12}" y="436" width="{64 - i * 8}" height="6" rx="3" fill="{c['oc_line']}"/>
    </g>""")
    grads = "".join(
        f'<linearGradient id="img{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
        for i, (a, b) in enumerate(img))

    l1 = words(LINE1, 0, 242, c)
    l2 = words(LINE2, len(LINE1), 274, c)
    ring = c['pin_ring'] if mode == 'light' else '#111216'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc" font-family="{SANS}">
<title id="title">Deixis plugin for Claude Code</title>
<desc id="desc">Show it, don't describe it. A pointer moves over a Trip Planner page, two numbered pins drop while a spoken line appears in a small glass card, and the round arrives in a Claude Code session where both points are marked done.</desc>
<defs>
  <linearGradient id="wall" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{c['wall'][0]}"/><stop offset=".52" stop-color="{c['wall'][1]}"/><stop offset="1" stop-color="{c['wall'][2]}"/>
  </linearGradient>
  {grads}
  <filter id="sh" x="-20%" y="-20%" width="140%" height="170%"><feDropShadow dx="0" dy="12" stdDeviation="14" flood-color="{c['shadow']}" flood-opacity="{c['shadow_op']}"/></filter>
  <filter id="shs" x="-60%" y="-60%" width="220%" height="240%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#000" flood-opacity=".3"/></filter>
  <filter id="glow" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="10"/></filter>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  <clipPath id="win"><rect x="40" y="160" width="480" height="320" rx="12"/></clipPath>
  <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="3" height="6" fill="{c['amber_soft']}"/></pattern>
  <style>{css(c)}</style>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#wall)"/>

  <!-- Brand: y 40..128 -->
  <text x="40" y="56" font-family="{MONO}" font-size="14" font-weight="600" letter-spacing="2.4" fill="{c['amber_ink']}">CLAUDE CODE PLUGIN</text>
  <g>
    <circle class="a listen" cx="64" cy="104" r="23" fill="none" stroke="{c['amber']}" stroke-opacity=".45" stroke-width="2"/>
    <circle id="gring" class="a" cx="64" cy="104" r="23" fill="none" stroke="{c['green']}" stroke-width="2.4" pathLength="1" stroke-dasharray="1" transform="rotate(-90 64 104)"/>
    <circle cx="64" cy="104" r="15" fill="{c['amber']}"/>
    <path d="{POINTER}" transform="translate(73 113) scale(1) translate(-2 -2)" fill="{c['ink']}" stroke="{ring}" stroke-width="1.8" stroke-linejoin="round"/>
  </g>
  <text x="104" y="120" font-family="{DISPLAY}" font-size="44" font-weight="700" letter-spacing="-.9" fill="{c['ink']}">Deixis</text>
  <text x="840" y="120" text-anchor="end" font-family="{DISPLAY}" font-size="26" font-weight="650" letter-spacing="-.3" fill="{c['ink']}">Show it, don’t describe it.</text>

  <!-- Option key held: top right, x 760..840, y 40..72 -->
  <g class="a listen">
    <rect x="760.5" y="40.5" width="79" height="31" rx="8" fill="{c['glass']}" stroke="{c['glass_line']}"/>
    <rect x="768" y="46" width="24" height="20" rx="5" fill="{c['kbd']}"/>
    <text x="780" y="61" text-anchor="middle" font-size="15" font-weight="600" fill="{c['ink']}">⌥</text>
    <text x="800" y="61" font-size="15" fill="{c['ink2']}">held</text>
  </g>

  <!-- Trip Planner window: x 40..520, y 160..480 -->
  <g filter="url(#sh)"><rect x="40" y="160" width="480" height="320" rx="12" fill="{c['oc_bg']}"/></g>
  <g clip-path="url(#win)">
    <rect x="40" y="160" width="480" height="40" fill="{c['oc_bar']}"/>
    <rect x="40" y="199.5" width="480" height="1" fill="{c['oc_line']}"/>
    <circle cx="64" cy="180" r="6" fill="#ff5f57"/><circle cx="84" cy="180" r="6" fill="#febc2e"/><circle cx="104" cy="180" r="6" fill="#28c840"/>
    <rect x="176" y="168" width="208" height="24" rx="7" fill="{c['oc_bg']}"/>
    <text x="280" y="185" text-anchor="middle" font-size="14" fill="{c['oc_ink2']}"><tspan fill="{c['oc_ink']}" font-weight="600">localhost:5173</tspan>/trips</text>
    <circle cx="72" cy="220" r="8" fill="{c['oc_brand']}"/>
    <path d="M68.5 222.5l3.5-6 3.5 6z" fill="{c['oc_bg']}"/>
    <text x="88" y="225.5" font-size="15" font-weight="700" fill="{c['oc_ink']}">Trip Planner</text>
    <rect x="384" y="216" width="40" height="8" rx="4" fill="{c['oc_line']}"/>
    <rect x="432" y="216" width="32" height="8" rx="4" fill="{c['oc_line']}"/>
    <circle cx="488" cy="220" r="8" fill="{c['oc_brand2']}"/>
    <rect x="40" y="239.5" width="480" height="1" fill="{c['oc_line']}"/>
    <text x="64" y="282" font-family="{DISPLAY}" font-size="30" font-weight="700" letter-spacing="-.5" fill="{c['oc_ink']}">Lisbon</text>
    <text x="64" y="308" font-size="15" fill="{c['oc_ink2']}">4 nights · 2 guests</text>
    <rect x="432" y="264" width="64" height="32" rx="8" fill="{c['oc_brand']}"/>
    <text x="464" y="285" text-anchor="middle" font-size="15" font-weight="650" fill="{c['oc_bg']}">Book</text>
    {''.join(cards)}
  </g>

  <!-- Highlights where the pins drop -->
  <g id="hl1" class="a">
    <rect x="428" y="260" width="72" height="40" rx="10" fill="{c['amber_soft']}" stroke="{c['amber_line']}" stroke-width="1.6"/>
    <rect x="344" y="268" width="72" height="24" rx="6" fill="{c['amber']}"/>
    <text x="380" y="285" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="600" fill="{c['pin_ink']}">64 × 32</text>
  </g>
  <g id="hl2" class="a">
    <rect x="180" y="336" width="56" height="120" rx="4" fill="url(#hatch)" stroke="{c['amber_line']}" stroke-width="1.4" stroke-dasharray="4 3"/>
    <rect x="180" y="344" width="56" height="24" rx="6" fill="{c['amber']}"/>
    <text x="208" y="361" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="600" fill="{c['pin_ink']}">64 px</text>
  </g>

  <!-- Begleiter HUD card: x 544..840, y 160..296 -->
  <g id="card" class="a">
    <g filter="url(#sh)"><rect x="544" y="160" width="296" height="136" rx="16" fill="{c['glass']}"/></g>
    <rect x="544.5" y="160.5" width="295" height="135" rx="15.5" fill="none" stroke="{c['glass_line']}"/>
    <g fill="{c['amber']}">
      <rect class="wv" x="562" y="178" width="3" height="12" rx="1.5"/>
      <rect class="wv" x="567.5" y="174" width="3" height="20" rx="1.5"/>
      <rect class="wv" x="573" y="177" width="3" height="14" rx="1.5"/>
      <rect class="wv" x="578.5" y="173" width="3" height="22" rx="1.5"/>
    </g>
    <text x="592" y="189" font-size="14" fill="{c['ink2']}"><tspan font-weight="700" fill="{c['ink']}">Trip Planner</tspan> · Oct 21</text>
    <g font-size="14" fill="{c['ink3']}" text-anchor="end">
      <text id="c0" class="a" x="824" y="189">0 points</text>
      <text id="c1" class="a" x="824" y="189">1 point</text>
      <text id="c2" class="a" x="824" y="189">2 points</text>
    </g>
    <rect x="544" y="207.6" width="296" height=".8" fill="{c['line']}"/>
    <g id="b1" class="a"><circle cx="572" cy="236" r="11" fill="{c['pin']}"/><text x="572" y="241" text-anchor="middle" font-size="14" font-weight="800" fill="{c['pin_ink']}">1</text></g>
    <g id="b2" class="a"><circle cx="572" cy="268" r="11" fill="{c['pin']}"/><text x="572" y="273" text-anchor="middle" font-size="14" font-weight="800" fill="{c['pin_ink']}">2</text></g>
    {l1}
    {l2}
  </g>

  <!-- Claude Code session: x 544..840, y 320..480 -->
  <g filter="url(#sh)"><rect x="544" y="320" width="296" height="160" rx="12" fill="{c['term']}"/></g>
  <g font-family="{MONO}" font-size="14" fill="{c['term_ink']}">
    <rect x="544" y="351.6" width="296" height=".8" fill="#ffffff" fill-opacity=".1"/>
    <circle cx="564" cy="336" r="4.5" fill="#ffffff" fill-opacity=".18"/><circle cx="578" cy="336" r="4.5" fill="#ffffff" fill-opacity=".18"/><circle cx="592" cy="336" r="4.5" fill="#ffffff" fill-opacity=".18"/>
    {spark(612, 341, "#ffb24a", 14 / 11.5)}<text x="629" y="341">Claude Code</text>
    <text x="560" y="380" fill="{c['term_dim']}">&gt; /deixis-watch</text>
    <text x="560" y="400"><tspan fill="#ffb24a">●</tspan> watch_rounds()</text>
    <text id="t1" class="a" x="560" y="420" xml:space="preserve" fill="{c['term_dim']}">  Trip Planner · 2 points</text>
    <g id="t2" class="a">{check(560, 440, "#6fd48b", 14 / 11.5)}<text x="577" y="440">Point 1 done</text></g>
    <g id="t3" class="a">{check(560, 460, "#6fd48b", 14 / 11.5)}<text x="577" y="460">Point 2 done</text></g>
  </g>

  <!-- Threads from the spoken word to the pointer -->
  <line id="th1" class="a" x1="561" y1="236" x2="{T1[0]}" y2="{T1[1] - 28}" pathLength="1" stroke-dasharray="1" stroke="{c['amber_line']}" stroke-width="1.6" stroke-linecap="round"/>
  <line id="th2" class="a" x1="561" y1="268" x2="{T2[0]}" y2="{T2[1] - 28}" pathLength="1" stroke-dasharray="1" stroke="{c['amber_line']}" stroke-width="1.6" stroke-linecap="round"/>

  {pin(1, *T1, c)}
  {pin(2, *T2, c)}

  <!-- Pointer -->
  <g id="cur" class="a">
    <path d="{POINTER}" transform="scale(1.2) translate(-2 -2)" fill="#111" stroke="#fff" stroke-width="1.5" stroke-linejoin="round" filter="url(#shs)"/>
  </g>

  <!-- Screen edge light while listening -->
  <g class="a listen" fill="none">
    <rect x="0" y="0" width="{W}" height="{H}" rx="16" stroke="rgb(255,150,40)" stroke-opacity=".45" stroke-width="22" filter="url(#glow)"/>
    <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="15" stroke="rgb(255,168,38)" stroke-opacity=".95" stroke-width="2"/>
  </g>
</g>
</svg>
"""


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ASSETS
    out.mkdir(parents=True, exist_ok=True)
    (out / "banner-light.svg").write_text(build(LIGHT, "light"))
    (out / "banner-dark.svg").write_text(build(DARK, "dark"))
