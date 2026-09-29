"""Render data/contributions.json as a terminal-style contribution graph."""

import datetime as dt
import json
import pathlib

from theme import ACCENT, LEVELS, MUTED, TEXT, window

ROOT = pathlib.Path(__file__).resolve().parent.parent
calendar = json.loads((ROOT / "data" / "contributions.json").read_text())

days = [d for w in calendar["weeks"] for d in w["contributionDays"]]
counts = [d["contributionCount"] for d in days]
nonzero = sorted(c for c in counts if c)


def level(count):
    """Map a count to 0-4 using quartiles of the non-zero days, like GitHub does."""
    if not count:
        return 0
    if not nonzero:
        return 1
    q = [nonzero[int(len(nonzero) * p)] for p in (0.25, 0.5, 0.75)]
    return 1 + sum(count > t for t in q)


streak = best = 0
for c in counts:
    streak = streak + 1 if c else 0
    best = max(best, streak)

stats = [
    (calendar["totalContributions"], "contributions"),
    (sum(1 for c in counts if c), "active days"),
    (best, "day best streak"),
    (max(counts, default=0), "on busiest day"),
]

CELL, GAP = 13, 3
STEP = CELL + GAP
LEFT, TOP = 72, 112
weeks = calendar["weeks"]
WIDTH = LEFT + len(weeks) * STEP + 36
HEIGHT = TOP + 7 * STEP + 72

parts = []

# Prompt, revealed like it is being typed, then a blinking cursor.
cmd = "./contributions.sh --last-year"
cmd_w = 9.6 * (len(cmd) + 2)
parts.append(f"""  <clipPath id="typing"><rect x="30" y="56" height="26" width="0">
    <animate attributeName="width" from="0" to="{cmd_w}" dur="1.4s" fill="freeze" calcMode="discrete" values="{';'.join(str(round(cmd_w * i / len(cmd))) for i in range(len(cmd) + 1))}"/>
  </rect></clipPath>
  <g clip-path="url(#typing)" font-size="16">
    <text x="32" y="75" fill="{ACCENT}">$</text>
    <text x="52" y="75" fill="{TEXT}">{cmd}</text>
  </g>
  <rect x="{52 + 9.6 * len(cmd) + 4}" y="61" width="9" height="18" fill="{ACCENT}">
    <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.5;0.5;0.99;1" dur="1s" begin="1.4s" repeatCount="indefinite"/>
  </rect>""")

grid = []
last_month = None
for x, week in enumerate(weeks):
    first = dt.date.fromisoformat(week["contributionDays"][0]["date"])
    if first.month != last_month and x < len(weeks) - 1:
        if last_month is not None or first.day <= 7:
            grid.append(f'<text x="{LEFT + x * STEP}" y="{TOP - 12}" font-size="12" fill="{MUTED}">{first.strftime("%b")}</text>')
        last_month = first.month
    for d in week["contributionDays"]:
        y = TOP + d["weekday"] * STEP
        tip = f'{d["contributionCount"]} on {d["date"]}'
        grid.append(f'<rect x="{LEFT + x * STEP}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{LEVELS[level(d["contributionCount"])]}"><title>{tip}</title></rect>')

for i, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    grid.append(f'<text x="{LEFT - 14}" y="{TOP + i * STEP + 11}" font-size="12" text-anchor="end" fill="{MUTED}">{name}</text>')

base = TOP + 7 * STEP + 40
x = 32
for value, label in stats:
    grid.append(f'<text x="{x}" y="{base}" font-size="14"><tspan fill="{TEXT}" font-weight="700">{value}</tspan><tspan fill="{MUTED}"> {label}</tspan></text>')
    x += 9 * (len(str(value)) + len(label) + 1) + 30

lx = WIDTH - 36 - 5 * 16 - 44
grid.append(f'<text x="{lx - 10}" y="{base}" font-size="12" text-anchor="end" fill="{MUTED}">less</text>')
for i, color in enumerate(LEVELS):
    grid.append(f'<rect x="{lx + i * 16}" y="{base - 11}" width="12" height="12" rx="3" fill="{color}"/>')
grid.append(f'<text x="{lx + 5 * 16 + 6}" y="{base}" font-size="12" fill="{MUTED}">more</text>')

parts.append(f"""  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="1.2s" dur="0.8s" fill="freeze"/>
    {chr(10).join('    ' + g for g in grid)}
  </g>""")

svg = window(WIDTH, HEIGHT, "hashim@github: ~", "\n".join(parts))
(ROOT / "contrib-heatmap.svg").write_text(svg, encoding="utf-8")
print(f"contrib-heatmap.svg {WIDTH}x{HEIGHT}")
