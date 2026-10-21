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

ICON_PIN = "M165.8 854.2 C232.1 661.3 231.7 565.7 267.2 410.3 A286 286 0 1 1 609.7 752.8 C454.3 788.3 358.7 787.9 165.8 854.2 Z"
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

# Canvas: 880 x 712 on an 8 px grid with a 40 px outer margin. Few, large elements in three bands: brand, the page
# across the full width, then the spoken card and the Claude Code session side by side. The smallest text is 24 px, so
# it reads at about 23 px in GitHub's 830 px column and at about 10 px on a 360 px wide phone.
# The base styles are the composed still frame (reduced motion). The animated loop starts from a complete scene:
# window, card and session are always there, the animation only adds pins, words and results and takes them back at the end.
W, H, M = 880, 712, 40

# Cursor positions (tip): rest, target 1 (just inside the top edge of the Book button), target 2 (the wide gap between the cards).
REST, T1, T2 = (560, 256), (748, 236), (436, 324)

# Words of the two spoken lines and the loop percentage at which each appears.
LINE1 = [("This", 19.0, True), ("button", 21.0, False), ("is", 22.6, False), ("too", 24.0, False), ("small.", 25.6, False)]
LINE2 = [("Here", 41.0, True), ("the", 43.0, False), ("gap", 44.4, False), ("is", 46.0, False), ("too", 47.4, False), ("big.", 49.0, False)]

# Everything the loop adds is taken back between OUT and BACK; what it replaced returns between BACK and HOME,
# so nothing ever overlaps and the frame at 100% equals the frame at 0%.
OUT, BACK, HOME = 94.0, 97.0, 99.5


def keyframes(name, frames):
    """frames: list of (percent list, css body, optional easing)."""
    out = [f"@keyframes {name}{{"]
    for pcts, body, *ease in frames:
        sel = ",".join(f"{p:g}%" for p in pcts)
        e = f"animation-timing-function:{ease[0]};" if ease else ""
        out.append(f"{sel}{{{body};{e}}}")
    out.append("}")
    return "".join(out)


def fade(name, on, prop="opacity", dur=1.2):
    """Hidden until `on`, fades in over `dur` percent, fades out between OUT and BACK."""
    return keyframes(name, [([0, on], f"{prop}:0"), ([on + dur, OUT], f"{prop}:1"), ([BACK, 100], f"{prop}:0")])


def unfade(name, off, dur=1.2):
    """The opposite of fade: visible from the start, gone at `off`, back between BACK and HOME."""
    return keyframes(name, [([0, off], "opacity:1"), ([off + dur, BACK], "opacity:0"), ([HOME, 100], "opacity:1")])


def css(c):
    k = []
    t = lambda p: f"transform:translate({p[0]}px,{p[1]}px)"
    k.append(keyframes("cur", [
        ([0, 6], t(REST), EASE), ([18, 30], t(T1), EASE), ([40, 56], t(T2), EASE), ([68, 100], t(REST)),
    ]))
    k.append(keyframes("listen", [([0, 5], "opacity:0"), ([9, 54], "opacity:1"), ([60, 100], "opacity:0")]))
    k.append(unfade("c0", 21.6, dur=1.0))
    k.append(keyframes("c1", [([0, 21.6], "opacity:0"), ([22.6, 43.6], "opacity:1"), ([44.6, 100], "opacity:0")]))
    k.append(keyframes("c2", [([0, 43.6], "opacity:0"), ([44.6, OUT], "opacity:1"), ([BACK, 100], "opacity:0")]))
    for i, (_, p, _) in enumerate(LINE1 + LINE2):
        k.append(fade(f"w{i}", p, prop="fill-opacity", dur=1.0))
    for i, p in ((1, 19.0), (2, 41.0)):
        k.append(fade(f"b{i}", p, dur=0.8))
        k.append(unfade(f"ph{i}", p - 0.6, dur=0.6))
    for i, p in ((1, 22.0), (2, 44.0)):
        # The pin stays fully opaque while it is on screen: it drops in and leaves by shrinking into its tip.
        hidden = "opacity:0;transform:translateY(-14px) scale(.4)"
        k.append(keyframes(f"pin{i}", [
            ([0, p], hidden, "cubic-bezier(.3,1.5,.5,1)"),
            ([p + 2.4, OUT], "opacity:1;transform:none", "cubic-bezier(.5,0,.75,0)"),
            ([BACK - .1], "opacity:1;transform:scale(0)"),
            ([BACK, 100], hidden),
        ]))
        k.append(keyframes(f"rip{i}", [
            ([0, p + 0.6], "opacity:0;transform:scale(.3)"), ([p + 1.2], "opacity:.9;transform:scale(.5)"),
            ([p + 5.5, 100], "opacity:0;transform:scale(1.6)"),
        ]))
        k.append(fade(f"hl{i}", p + 0.4))
    for name, p in (("ok1", 72), ("ok2", 82)):
        k.append(keyframes(name, [([0, p], "opacity:0"), ([p + 1.5, BACK - .1], "opacity:1"), ([BACK, 100], "opacity:0")]))
    k.append(unfade("wait", 70))
    k.append(fade("t2", 72))
    k.append(fade("t3", 82))
    k.append(keyframes("wave", [([0], "transform:scaleY(.35)"), ([100], "transform:scaleY(1)")]))

    rules = f"""
.a{{animation-duration:8s;animation-iteration-count:infinite;animation-timing-function:linear;animation-fill-mode:both}}
#cur{{transform:translate({T2[0]}px,{T2[1]}px);animation-name:cur}}
.listen{{opacity:0;animation-name:listen}}
#c0,#c1,#ph1,#ph2,#wait{{opacity:0}} #c0{{animation-name:c0}} #c1{{animation-name:c1}} #c2{{animation-name:c2}}
#ph1{{animation-name:ph1}} #ph2{{animation-name:ph2}} #b1{{animation-name:b1}} #b2{{animation-name:b2}}
#pin1{{animation-name:pin1}} #pin2{{animation-name:pin2}}
#rip1,#rip2{{opacity:0;transform-box:fill-box;transform-origin:50% 50%}} #rip1{{animation-name:rip1}} #rip2{{animation-name:rip2}}
#hl1{{animation-name:hl1}} #hl2{{animation-name:hl2}}
#ok2,#t3{{opacity:0}} #ok1{{animation-name:ok1}} #ok2{{animation-name:ok2}}
#wait{{animation-name:wait}} #t2{{animation-name:t2}} #t3{{animation-name:t3}}
.wv{{transform-box:fill-box;transform-origin:50% 50%;animation:wave .9s ease-in-out infinite alternate}}
.wv:nth-child(2){{animation-delay:-.3s}} .wv:nth-child(3){{animation-delay:-.55s}} .wv:nth-child(4){{animation-delay:-.15s}}
""" + "".join(f"#w{i}{{animation-name:w{i}}}" for i in range(len(LINE1 + LINE2))) + """
@media (prefers-reduced-motion: reduce){.a,.wv{animation:none!important}}
"""
    return "\n".join(k) + rules


TX = 112  # left edge of the spoken words in the card


def words(line, start, y, c):
    parts = []
    for j, (w, _, deictic) in enumerate(line):
        i = start + j
        style = f' fill="{c["amber_ink"]}" font-weight="700"' if deictic else ""
        sep = " " if j else ""
        parts.append(f'<tspan id="w{i}" class="a"{style}>{sep}{w}</tspan>')
    return f'<text x="{TX}" y="{y}" font-size="24" fill="{c["ink"]}" xml:space="preserve">{"".join(parts)}</text>'


def pin(n, x, y, c):
    return f"""
  <g transform="translate({x} {y})">
    <circle id="rip{n}" class="a" cx="0" cy="-4" r="24" fill="none" stroke="{c['amber']}" stroke-width="2"/>
    <g id="pin{n}" class="a">
      <rect x="-2.5" y="-18" width="5" height="18" rx="2" fill="{c['pin']}"/>
      <circle cx="0" cy="-36" r="20" fill="{c['pin']}" stroke="{c['pin_ring']}" stroke-width="2.4" filter="url(#shs)"/>
      <text x="0" y="-27.6" text-anchor="middle" font-size="24" font-weight="800" fill="{c['pin_ink']}">{n}</text>
      <g id="ok{n}" class="a">
        <circle cx="0" cy="-36" r="20" fill="{c['green']}" stroke="{c['pin_ring']}" stroke-width="2.4"/>
        <path d="M-8.4 -36l5.6 5.6 10.8-11.6" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
    </g>
  </g>"""


def row(n, cy, words_svg, bar, c):
    """One spoken point in the card: a placeholder (outlined number, grey bar) until the words arrive."""
    return f"""
    <g id="ph{n}" class="a">
      <circle cx="80" cy="{cy}" r="17" fill="none" stroke="{c['ink3']}" stroke-opacity=".6" stroke-width="2"/>
      <text x="80" y="{cy + 8.4}" text-anchor="middle" font-size="24" font-weight="700" fill="{c['ink3']}">{n}</text>
      <rect x="{TX}" y="{cy - 6}" width="{bar}" height="12" rx="6" fill="{c['ink3']}" fill-opacity=".28"/>
    </g>
    <g id="b{n}" class="a"><circle cx="80" cy="{cy}" r="18" fill="{c['pin']}"/><text x="80" y="{cy + 8.4}" text-anchor="middle" font-size="24" font-weight="800" fill="{c['pin_ink']}">{n}</text></g>
    {words_svg}"""


def build(c, mode):
    img = c["img"]
    # Trip Planner window: x 40..840, y 128..424. Two cards 312 wide; the 128 px gap between them is the one that is too big.
    cards = []
    for i, (title, x) in enumerate((("Alfama", 64), ("Belém", 504))):
        cards.append(f"""
    <g>
      <rect x="{x}" y="312" width="312" height="88" rx="12" fill="{c['oc_card']}" stroke="{c['oc_line']}"/>
      <rect x="{x + 8}" y="320" width="96" height="72" rx="8" fill="url(#img{i})"/>
      <text x="{x + 128}" y="352" font-size="24" font-weight="650" fill="{c['oc_ink']}">{title}</text>
      <rect x="{x + 128}" y="368" width="{112 - i * 24}" height="8" rx="4" fill="{c['oc_line']}"/>
    </g>""")
    grads = "".join(
        f'<linearGradient id="img{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
        for i, (a, b) in enumerate(img[:2]))

    rows = row(1, 560, words(LINE1, 0, 568, c), 264, c) + row(2, 616, words(LINE2, len(LINE1), 624, c), 240, c)
    edge = '0' if mode == 'light' else '.14'
    s = 24 / 11.5

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc" font-family="{SANS}">
<title id="title">Deixis plugin for Claude Code</title>
<desc id="desc">Show it, don't describe it. A pointer moves over a Trip Planner page, two numbered pins drop while the spoken line appears in a glass card, and the round arrives in a Claude Code session where both points are marked done.</desc>
<defs>
  <linearGradient id="wall" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{c['wall'][0]}"/><stop offset=".52" stop-color="{c['wall'][1]}"/><stop offset="1" stop-color="{c['wall'][2]}"/>
  </linearGradient>
  {grads}
  <filter id="sh" x="-20%" y="-20%" width="140%" height="170%"><feDropShadow dx="0" dy="12" stdDeviation="14" flood-color="{c['shadow']}" flood-opacity="{c['shadow_op']}"/></filter>
  <filter id="shs" x="-60%" y="-60%" width="220%" height="240%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#000" flood-opacity=".3"/></filter>
  <filter id="glow" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="10"/></filter>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  <clipPath id="win"><rect x="40" y="128" width="800" height="296" rx="12"/></clipPath>
  <pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="4" height="8" fill="{c['amber_soft']}"/></pattern>
  <linearGradient id="iconbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22335a"/><stop offset="1" stop-color="#0a1120"/></linearGradient>
  <linearGradient id="iconpin" x1="0.25" y1="0" x2="0.55" y2="1"><stop offset="0" stop-color="#ffb850"/><stop offset="0.55" stop-color="#f49e34"/><stop offset="1" stop-color="#e5831c"/></linearGradient>
  <style>{css(c)}</style>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#wall)"/>

  <!-- Brand and tagline: y 40..104 -->
  <g>
    <!-- The Deixis app icon at 56 px: ink-blue squircle, the pointed orange pin. -->
    <g transform="translate(36 44) scale(0.0546875)">
      <rect width="1024" height="1024" rx="230" fill="url(#iconbg)"/>
      <path d="{ICON_PIN}" fill="url(#iconpin)"/>
      <rect x="9" y="9" width="1006" height="1006" rx="222" fill="none" stroke="#ffffff" stroke-opacity="{edge}" stroke-width="18"/>
    </g>
  </g>
  <text x="104" y="90" font-family="{DISPLAY}" font-size="48" font-weight="700" letter-spacing="-1" fill="{c['ink']}">Deixis</text>
  <text x="840" y="88" text-anchor="end" font-family="{DISPLAY}" font-size="32" font-weight="650" letter-spacing="-.4" fill="{c['ink']}">Show it, don’t describe it.</text>

  <!-- Trip Planner window: x 40..840, y 128..424 -->
  <g filter="url(#sh)"><rect x="40" y="128" width="800" height="296" rx="12" fill="{c['oc_bg']}"/></g>
  <g clip-path="url(#win)">
    <rect x="40" y="128" width="800" height="48" fill="{c['oc_bar']}"/>
    <rect x="40" y="175.5" width="800" height="1" fill="{c['oc_line']}"/>
    <circle cx="64" cy="152" r="7" fill="#ff5f57"/><circle cx="88" cy="152" r="7" fill="#febc2e"/><circle cx="112" cy="152" r="7" fill="#28c840"/>
    <rect x="272" y="136" width="336" height="32" rx="8" fill="{c['oc_bg']}"/>
    <text x="440" y="160" text-anchor="middle" font-size="24" fill="{c['oc_ink2']}"><tspan fill="{c['oc_ink']}" font-weight="600">localhost:5173</tspan>/trips</text>
    <text x="64" y="240" font-family="{DISPLAY}" font-size="40" font-weight="700" letter-spacing="-.6" fill="{c['oc_ink']}">Lisbon</text>
    <text x="64" y="280" font-size="24" fill="{c['oc_ink2']}">4 nights · 2 guests</text>
    <rect x="680" y="232" width="136" height="56" rx="12" fill="{c['oc_brand']}"/>
    <text x="748" y="268" text-anchor="middle" font-size="24" font-weight="650" fill="{c['oc_bg']}">Book</text>
    {''.join(cards)}
  </g>

  <!-- Highlights where the pins drop; the size tag sits inside the gap, clear of both cards -->
  <g id="hl1" class="a">
    <rect x="672" y="224" width="152" height="72" rx="18" fill="{c['amber_soft']}" stroke="{c['amber_line']}" stroke-width="2"/>
  </g>
  <g id="hl2" class="a">
    <rect x="376" y="312" width="128" height="88" rx="8" fill="url(#hatch)" stroke="{c['amber_line']}" stroke-width="1.6" stroke-dasharray="5 4"/>
    <rect x="384" y="360" width="112" height="32" rx="8" fill="{c['amber']}"/>
    <text x="440" y="384" text-anchor="middle" font-family="{MONO}" font-size="24" font-weight="700" fill="{c['pin_ink']}">128 px</text>
  </g>

  <!-- Spoken card: x 40..480, y 448..672, always on screen -->
  <g filter="url(#sh)"><rect x="40" y="448" width="440" height="224" rx="16" fill="{c['glass']}"/></g>
  <rect x="40.5" y="448.5" width="439" height="223" rx="15.5" fill="none" stroke="{c['glass_line']}"/>
  <g fill="{c['amber']}">
    <rect class="wv" x="64" y="467" width="5" height="18" rx="2.5"/>
    <rect class="wv" x="72" y="461" width="5" height="30" rx="2.5"/>
    <rect class="wv" x="80" y="466" width="5" height="20" rx="2.5"/>
    <rect class="wv" x="88" y="460" width="5" height="32" rx="2.5"/>
  </g>
  <text x="{TX}" y="484" font-size="24" font-weight="700" fill="{c['ink']}">Trip Planner</text>
  <g font-size="24" fill="{c['ink2']}" text-anchor="end">
    <text id="c0" class="a" x="456" y="484">0 points</text>
    <text id="c1" class="a" x="456" y="484">1 point</text>
    <text id="c2" class="a" x="456" y="484">2 points</text>
  </g>
  <rect x="40" y="503.5" width="440" height="1" fill="{c['line']}"/>
  {rows}

  <!-- Claude Code session: x 504..840, y 448..672 -->
  <g filter="url(#sh)"><rect x="504" y="448" width="336" height="224" rx="12" fill="{c['term']}"/></g>
  <g font-family="{MONO}" font-size="24" fill="{c['term_ink']}">
    <rect x="504" y="487.5" width="336" height="1" fill="#ffffff" fill-opacity=".1"/>
    <circle cx="528" cy="468" r="6" fill="#ffffff" fill-opacity=".18"/><circle cx="548" cy="468" r="6" fill="#ffffff" fill-opacity=".18"/><circle cx="568" cy="468" r="6" fill="#ffffff" fill-opacity=".18"/>
    {spark(592, 477, "#ffb24a", s)}<text x="616" y="477">Claude Code</text>
    <text x="528" y="528" fill="{c['term_dim']}">&gt; /deixis-watch</text>
    <text x="528" y="568"><tspan fill="#ffb24a">●</tspan> watch_rounds()</text>
    <text id="wait" class="a" x="528" y="608" xml:space="preserve" fill="{c['term_dim']}">  waiting…</text>
    <g id="t2" class="a">{check(528, 608, "#6fd48b", s)}<text x="560" y="608">Point 1 done</text></g>
    <g id="t3" class="a">{check(528, 648, "#6fd48b", s)}<text x="560" y="648">Point 2 done</text></g>
  </g>

  {pin(1, *T1, c)}
  {pin(2, *T2, c)}

  <!-- Pointer -->
  <g id="cur" class="a">
    <path d="{POINTER}" transform="scale(1.25) translate(-2 -2)" fill="#111" stroke="#fff" stroke-width="1.5" stroke-linejoin="round" filter="url(#shs)"/>
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
