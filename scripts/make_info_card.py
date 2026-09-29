"""Render the `whoami` card shown next to the portrait."""

import pathlib
from html import escape

from theme import ACCENT, LEVELS, MUTED, TEXT, window

ROOT = pathlib.Path(__file__).resolve().parent.parent

HANDLE = "hashim@github"
GROUPS = [
    [
        ("name", "Hashim Al Masaabi"),
        ("role", "Software Engineer @ Sanal AI"),
        ("freelance", "Frontend Developer @ Jzaa Agency"),
        ("degree", "B.Sc. Software Engineering, PSAU 2026"),
        ("gpa", "4.90 / 5.00"),
    ],
    [
        ("lifecycle", "requirements > analysis > build > test > ship"),
        ("analysis", "user stories, acceptance criteria, specs"),
        ("quality", "manual & automated testing, Vitest, Playwright"),
        ("automation", "n8n workflows, Google Sheets sync"),
    ],
    [
        ("web", "React, Next.js, TypeScript, Tailwind CSS"),
        ("backend", "Node.js, Supabase, PostgreSQL, REST APIs"),
        ("design", "Figma, Framer, UI/UX prototyping"),
        ("tools", "Git, GitHub Actions, Jira, VS Code"),
    ],
    [
        ("awards", "1st Place, Intellectual Empowerment Hackathon"),
    ],
    [
        ("site", "hashim0011.github.io"),
        ("linkedin", "in/hashim-almasaabi-b51ba4353"),
    ],
]

KEY_X, VAL_X = 30, 136
LINE, GAP = 21, 12
y = 76
rows = [f'  <text x="{KEY_X}" y="{y}" font-size="14" font-weight="700" fill="{ACCENT}">{HANDLE}</text>']
y += 12
rows.append(f'  <line x1="{KEY_X}" y1="{y}" x2="{KEY_X + 9 * len(HANDLE)}" y2="{y}" stroke="{ACCENT}" stroke-opacity=".5"/>')
y += 14

i = 0
for group in GROUPS:
    for key, value in group:
        y += LINE
        delay = 0.3 + i * 0.07
        rows.append(
            f'  <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<text x="{KEY_X}" y="{y}" font-size="13" fill="{ACCENT}">{key}</text>'
            f'<text x="{VAL_X}" y="{y}" font-size="13" fill="{TEXT}">{escape(value)}</text></g>'
        )
        i += 1
    y += GAP

y += 14
palette = LEVELS[1:] + ["#5ee3ad", "#58a6ff", "#e3b341", "#e6edf3"]
for n, color in enumerate(palette):
    rows.append(f'  <rect x="{KEY_X + n * 30}" y="{y}" width="26" height="12" rx="2" fill="{color}"/>')

height = y + 36
width = 540
(ROOT / "info-card.svg").write_text(window(width, height, "whoami", "\n".join(rows)), encoding="utf-8")
print(f"info-card.svg {width}x{height}")
