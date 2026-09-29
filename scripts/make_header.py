"""Animated banner: the name in block letters plus a typed, rotating role line."""

import pathlib

from theme import ACCENT, ACCENT_DARK, ACCENT_DEEP, ACCENT_LIGHT, BORDER, FONT, MUTED, TEXT, TITLEBAR, WINDOW

ROOT = pathlib.Path(__file__).resolve().parent.parent

# ANSI Shadow glyphs. "█" becomes a solid pixel, the box-drawing strokes
# become the thin drop shadow.
GLYPHS = {
    "H": ["██╗  ██╗", "██║  ██║", "███████║", "██╔══██║", "██║  ██║", "╚═╝  ╚═╝"],
    "A": [" █████╗ ", "██╔══██╗", "███████║", "██╔══██║", "██║  ██║", "╚═╝  ╚═╝"],
    "S": ["███████╗", "██╔════╝", "███████╗", "╚════██║", "███████║", "╚══════╝"],
    "I": ["██╗", "██║", "██║", "██║", "██║", "╚═╝"],
    "M": ["███╗   ███╗", "████╗ ████║", "██╔████╔██║", "██║╚██╔╝██║", "██║ ╚═╝ ██║", "╚═╝     ╚═╝"],
}
WORD = "HASHIM"
ROLES = ["Software Engineer", "Business Analyst", "Frontend Developer", "Automation Builder"]

CW, CH = 13, 17  # one character cell of the block font
W, H = 1000, 330

rows = ["" for _ in range(6)]
for letter in WORD:
    for i, line in enumerate(GLYPHS[letter]):
        rows[i] += line
cols = len(rows[0])
ox = (W - cols * CW) / 2
oy = 78

# Shadow strokes, drawn per cell as short line segments.
seg = {
    "═": [(0, .5, 1, .5)], "║": [(.5, 0, .5, 1)],
    "╗": [(0, .5, .5, .5), (.5, .5, .5, 1)], "╔": [(.5, .5, 1, .5), (.5, .5, .5, 1)],
    "╝": [(0, .5, .5, .5), (.5, 0, .5, .5)], "╚": [(.5, 0, .5, .5), (.5, .5, 1, .5)],
}
blocks, shadow = [], []
for r, line in enumerate(rows):
    for c, ch in enumerate(line):
        x, y = ox + c * CW, oy + r * CH
        if ch == "█":
            delay = 0.25 + c * 0.018 + r * 0.03
            blocks.append(
                f'<rect x="{x:.1f}" y="{y}" width="{CW - 1}" height="{CH - 1}" rx="1.5" fill="url(#g)" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur=".25s" fill="freeze"/></rect>'
            )
        for x1, y1, x2, y2 in seg.get(ch, []):
            shadow.append(f'<line x1="{x + x1 * CW:.1f}" y1="{y + y1 * CH:.1f}" x2="{x + x2 * CW:.1f}" y2="{y + y2 * CH:.1f}"/>')

# Rotating roles: each is typed, held, then erased, in turn.
slot, n = 3.2, len(ROLES)
period = slot * n
char_w = 12.6
ry = oy + 6 * CH + 58
role_x = W / 2 - 150
roles = []
for i, role in enumerate(ROLES):
    full = char_w * len(role) + 4
    a, b, c, d = (i * slot) / period, (i * slot + 1.0) / period, (i * slot + 2.5) / period, (i * slot + 3.0) / period
    kt = sorted({0, a, b, c, d, 1})
    val = {0: 0, a: 0, b: full, c: full, d: 0, 1: 0}
    roles.append(f"""  <clipPath id="r{i}"><rect x="{role_x}" y="{ry - 22}" height="30" width="0">
    <animate attributeName="width" dur="{period}s" begin="1.3s" repeatCount="indefinite" keyTimes="{';'.join(f'{k:.4f}' for k in kt)}" values="{';'.join(f'{val[k]:.0f}' for k in kt)}"/>
  </rect></clipPath>
  <text x="{role_x}" y="{ry}" font-size="21" fill="{TEXT}" clip-path="url(#r{i})" textLength="{char_w * len(role):.1f}" lengthAdjust="spacingAndGlyphs">{role}</text>""")

# One cursor that tracks the end of whichever role is being typed.
points = [(0.0, 0.0)]
for i, role in enumerate(ROLES):
    full = char_w * len(role) + 4
    for off, w in ((0, 0), (1.0, full), (2.5, full), (3.0, 0)):
        points.append(((i * slot + off) / period, w))
points.append((1.0, 0.0))
points = sorted(dict(points).items())
cursor_kt = ";".join(f"{k:.4f}" for k, _ in points)
cursor_x = ";".join(f"{role_x + w + 3:.0f}" for _, w in points)
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
  <defs>
    <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="{ACCENT_LIGHT}"/>
      <stop offset=".55" stop-color="{ACCENT}"/>
      <stop offset="1" stop-color="{ACCENT_DARK}"/>
    </linearGradient>
    <radialGradient id="glow" cx=".5" cy=".42" r=".6">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity=".16"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#ffffff" opacity=".025"/>
    </pattern>
    <clipPath id="win"><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12"/></clipPath>
  </defs>
  <g clip-path="url(#win)">
    <rect width="{W}" height="{H}" fill="{WINDOW}"/>
    <rect width="{W}" height="{H}" fill="url(#glow)"/>
    <rect width="{W}" height="40" fill="{TITLEBAR}"/>
    <line x1="0" y1="40" x2="{W}" y2="40" stroke="{BORDER}"/>
    <circle cx="22" cy="20" r="6" fill="#ff5f57"/><circle cx="42" cy="20" r="6" fill="#febc2e"/><circle cx="62" cy="20" r="6" fill="#28c840"/>
    <text x="{W / 2}" y="25" text-anchor="middle" font-size="13" fill="{MUTED}">hashim@riyadh: ~/welcome</text>
    <g stroke="{ACCENT_DEEP}" stroke-width="1.6" stroke-linecap="round" opacity=".9">{''.join(shadow)}</g>
    {''.join(blocks)}
    <text x="{W / 2}" y="{oy + 6 * CH + 22}" text-anchor="middle" font-size="14" letter-spacing="9" fill="{MUTED}" opacity="0">AL MASAABI<animate attributeName="opacity" from="0" to="1" begin="1.1s" dur=".6s" fill="freeze"/></text>
    <text x="{role_x - 26}" y="{ry}" font-size="21" fill="{ACCENT}">&gt;</text>
{chr(10).join(roles)}
    <rect x="{role_x + 3}" y="{ry - 18}" width="11" height="22" fill="{ACCENT}" opacity="0">
      <animate attributeName="x" dur="{period}s" begin="1.3s" repeatCount="indefinite" keyTimes="{cursor_kt}" values="{cursor_x}"/>
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" begin="1.3s" repeatCount="indefinite"/>
    </rect>
    <text x="{W / 2}" y="{H - 26}" text-anchor="middle" font-size="13" fill="{MUTED}">Riyadh, Saudi Arabia  ·  Software Engineering, PSAU  ·  open to new projects</text>
    <rect width="{W}" height="{H}" fill="url(#scan)"/>
    <rect y="-60" width="{W}" height="60" fill="url(#g)" opacity=".05">
      <animate attributeName="y" from="-60" to="{H}" dur="4s" repeatCount="indefinite"/>
    </rect>
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{BORDER}"/>
</svg>
"""
(ROOT / "header.svg").write_text(svg, encoding="utf-8")
print(f"header.svg {W}x{H}")
