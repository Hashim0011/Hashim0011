"""Career timeline drawn as `git log --graph`, newest first."""

import hashlib
import pathlib
from html import escape

from theme import ACCENT, MUTED, TEXT, window

ROOT = pathlib.Path(__file__).resolve().parent.parent

# (lane, date, refs, message, detail). Lane 1 is the freelance branch that
# runs alongside the main line.
COMMITS = [
    (0, "Apr 2026", "HEAD -> main", "feat: Software Engineer @ Sanal AI", "web & merchant apps, requirements to release"),
    (1, "2026", "freelance", "chore: maintain Jzaa Agency website", "updates, fixes, SEO, hosting"),
    (0, "2026", "tag: v1-hackathon", "feat: 1st Place, Intellectual Empowerment Hackathon", "Fateen, multimodal misinformation detection"),
    (0, "2026", "tag: graduation", "release: B.Sc. Software Engineering, PSAU", "GPA 4.90 / 5.00"),
    (0, "Jan 2026", "", "feat: Software Engineering Trainee @ Silky System", "co-op: QA, requirements analysis"),
    (1, "Nov 2025", "", "feat: Frontend Developer @ Jzaa Agency", "freelance: requirements, build, launch"),
    (0, "2025", "", "feat: ship Faten Platform", "graduation project, CI/CD, v1.0.1"),
    (0, "2021", "", "init: start B.Sc. Software Engineering", "Prince Sattam Bin Abdulaziz University"),
]
FORK_AT = 5   # index where the freelance lane branches off main
LANE_X = [44, 72]
ROW = 50
TOP = 104
HASH_X = 100

LANE_COLOR = [ACCENT, "#e3b341"]
rows = [f'  <text x="30" y="72" font-size="15"><tspan fill="{ACCENT}">$</tspan><tspan fill="{TEXT}"> git log --graph --oneline career</tspan></text>']

ys = [TOP + i * ROW for i in range(len(COMMITS))]
last = len(COMMITS) - 1
# Main line through every row; freelance lane from its fork up to the top.
rows.append(f'  <line x1="{LANE_X[0]}" y1="{ys[0]}" x2="{LANE_X[0]}" y2="{ys[last]}" stroke="{ACCENT}" stroke-width="2.5" stroke-dasharray="{ys[last] - ys[0]}" stroke-dashoffset="{ys[last] - ys[0]}"><animate attributeName="stroke-dashoffset" to="0" dur="1.6s" begin=".2s" fill="freeze"/></line>')
fy = ys[FORK_AT]
rows.append(
    f'  <path d="M{LANE_X[0]} {fy + ROW} C {LANE_X[0]} {fy + ROW / 2}, {LANE_X[1]} {fy + ROW / 2}, {LANE_X[1]} {fy} L {LANE_X[1]} {ys[0] - 14}" '
    f'fill="none" stroke="{LANE_COLOR[1]}" stroke-width="2.5" opacity="0"><animate attributeName="opacity" to="1" begin="1.4s" dur=".6s" fill="freeze"/></path>'
)

for i, (lane, date, refs, msg, detail) in enumerate(COMMITS):
    y = ys[i]
    delay = 0.3 + (last - i) * 0.18
    sha = hashlib.sha1(msg.encode()).hexdigest()[:7]
    ref = f'<tspan fill="{MUTED}">(</tspan><tspan fill="#3fb950">{escape(refs)}</tspan><tspan fill="{MUTED}">) </tspan>' if refs else ""
    rows.append(
        f'  <g opacity="0"><animate attributeName="opacity" to="1" begin="{delay:.2f}s" dur=".4s" fill="freeze"/>'
        f'<circle cx="{LANE_X[lane]}" cy="{y}" r="6.5" fill="#11151c" stroke="{LANE_COLOR[lane]}" stroke-width="2.5"/>'
        f'<circle cx="{LANE_X[lane]}" cy="{y}" r="2.5" fill="{LANE_COLOR[lane]}"/>'
        f'<text x="{HASH_X}" y="{y + 5}" font-size="14"><tspan fill="#e3b341">{sha}</tspan> {ref}<tspan fill="{TEXT}">{escape(msg)}</tspan></text>'
        f'<text x="{HASH_X + 76}" y="{y + 23}" font-size="12" fill="{MUTED}">{escape(detail)}  ·  {date}</text></g>'
    )
    if i == 0:
        rows.append(
            f'  <circle cx="{LANE_X[0]}" cy="{y}" r="6.5" fill="none" stroke="{ACCENT}" stroke-width="2">'
            f'<animate attributeName="r" values="6.5;16" dur="1.8s" begin="2s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values=".8;0" dur="1.8s" begin="2s" repeatCount="indefinite"/></circle>'
        )

W, Hh = 1000, ys[last] + 58
(ROOT / "journey.svg").write_text(window(W, Hh, "~/career", "\n".join(rows)), encoding="utf-8")
print(f"journey.svg {W}x{Hh}")
