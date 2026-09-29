"""Closing terminal line for the bottom of the profile."""

import pathlib

from theme import ACCENT, MUTED, TEXT, window

ROOT = pathlib.Path(__file__).resolve().parent.parent

LINES = [
    ("$", "echo \"thanks for stopping by\"", TEXT),
    ("", "thanks for stopping by", MUTED),
    ("$", "open https://hashim-almasaabi.netlify.app", TEXT),
    ("", "let's build something people just use.", "#ff8a8e"),
]
W, H = 1000, 196
rows = []
t = 0.3
for i, (prompt, text, color) in enumerate(LINES):
    y = 72 + i * 28
    width = 9.6 * (len(text) + 3)
    typed = bool(prompt)
    dur = 0.03 * len(text) if typed else 0.01
    rows.append(f'  <clipPath id="l{i}"><rect x="28" y="{y - 20}" height="28" width="0"><animate attributeName="width" to="{width:.0f}" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>')
    rows.append(f'  <text x="32" y="{y}" font-size="16" clip-path="url(#l{i})"><tspan fill="{ACCENT}">{prompt}</tspan><tspan fill="{color}" x="{52 if prompt else 32}" textLength="{9.6 * len(text):.1f}" lengthAdjust="spacingAndGlyphs">{text}</tspan></text>')
    t += dur + (0.5 if typed else 0.35)
y = 72 + len(LINES) * 28
rows.append(f'  <text x="32" y="{y}" font-size="16" fill="{ACCENT}" opacity="0">$<animate attributeName="opacity" to="1" begin="{t:.2f}s" dur=".01s" fill="freeze"/></text>')
rows.append(f'  <rect x="52" y="{y - 15}" width="10" height="19" fill="{ACCENT}" opacity="0"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" begin="{t:.2f}s" repeatCount="indefinite"/></rect>')
(ROOT / "footer.svg").write_text(window(W, H, "hashim@github: ~ — exit", "\n".join(rows)), encoding="utf-8")
print("footer.svg")
