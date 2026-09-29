"""One SVG card per featured project, with an embedded screenshot."""

import base64
import io
import pathlib
from html import escape

from PIL import Image

from theme import ACCENT, BORDER, FONT, MUTED, TEXT, TITLEBAR, WINDOW

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "cards"

PROJECTS = [
    ("faten-platform", "Faten Platform", "Intellectual security platform with role-based dashboards, discussions and an AI assistant.",
     ["React", "TypeScript", "Supabase", "CI/CD"], "TypeScript", "#3178c6", "graduation project"),
    ("dashy-ai", "DashyAI", "AI analytics dashboard: Sheets sync via n8n, live KPIs and what-if forecasting.",
     ["React", "Recharts", "n8n", "AI"], "TypeScript", "#3178c6", "product"),
    ("personal-website", "Personal Website", "Bilingual EN/AR portfolio with true RTL, light/dark themes and accessible motion.",
     ["React", "Vite", "Tailwind", "Framer Motion"], "TypeScript", "#3178c6", "live"),
    ("foodie-flow", "FoodieFlow", "Recipe manager with favourites, your own recipes and AI-generated details.",
     ["React", "React Router", "Gemini"], "TypeScript", "#3178c6", "app"),
]

W, H = 480, 350
IMG_H = 190


def embed(slug):
    """Crop the screenshot to the card's banner ratio and inline it as WebP."""
    img = Image.open(ROOT / "assets" / "projects" / f"{slug}.webp").convert("RGB")
    ratio = W / IMG_H
    w, h = img.size
    if w / h > ratio:
        nw = int(h * ratio)
        img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        img = img.crop((0, 0, w, int(w / ratio)))
    img = img.resize((W * 2, IMG_H * 2), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "WEBP", quality=72)
    return base64.b64encode(buf.getvalue()).decode()


def wrap(text, width=54):
    lines, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > width:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + [line]


OUT.mkdir(exist_ok=True)
for slug, name, desc, stack, lang, lang_color, badge in PROJECTS:
    y0 = IMG_H + 40
    desc_lines = "".join(
        f'<text x="22" y="{y0 + 44 + i * 19}" font-size="13" fill="{MUTED}">{escape(l)}</text>' for i, l in enumerate(wrap(desc))
    )
    chips, cx = [], 22
    for s in stack:
        cw = 8 * len(s) + 20
        chips.append(f'<rect x="{cx}" y="{H - 44}" width="{cw}" height="24" rx="12" fill="{ACCENT}" fill-opacity=".12" stroke="{ACCENT}" stroke-opacity=".45"/>'
                     f'<text x="{cx + cw / 2}" y="{H - 27.5}" font-size="12" text-anchor="middle" fill="#ff8a8e">{escape(s)}</text>')
        cx += cw + 8
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
  <defs>
    <clipPath id="c"><rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12"/></clipPath>
    <linearGradient id="fade" x1="0" x2="0" y1="0" y2="1">
      <stop offset=".55" stop-color="{WINDOW}" stop-opacity="0"/><stop offset="1" stop-color="{WINDOW}"/>
    </linearGradient>
    <linearGradient id="shine" x1="0" x2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".10"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <g clip-path="url(#c)">
    <rect width="{W}" height="{H}" fill="{WINDOW}"/>
    <rect width="{W}" height="32" fill="{TITLEBAR}"/>
    <circle cx="18" cy="16" r="5" fill="#ff5f57"/><circle cx="34" cy="16" r="5" fill="#febc2e"/><circle cx="50" cy="16" r="5" fill="#28c840"/>
    <text x="{W / 2}" y="20.5" text-anchor="middle" font-size="12" fill="{MUTED}">~/projects/{slug}</text>
    <image x="0" y="32" width="{W}" height="{IMG_H}" preserveAspectRatio="xMidYMid slice" href="data:image/webp;base64,{embed(slug)}"/>
    <rect x="0" y="32" width="{W}" height="{IMG_H}" fill="url(#fade)"/>
    <rect x="-200" y="32" width="160" height="{IMG_H}" fill="url(#shine)" transform="skewX(-20)">
      <animate attributeName="x" values="-200;{W + 200}" dur="3.5s" begin="1s" repeatCount="indefinite"/>
    </rect>
    <text x="22" y="{y0 + 16}" font-size="19" font-weight="700" fill="{TEXT}">{escape(name)}</text>
    <rect x="{W - 22 - 9 * len(badge) - 18}" y="{y0}" width="{9 * len(badge) + 18}" height="22" rx="11" fill="none" stroke="{BORDER}"/>
    <text x="{W - 22 - (9 * len(badge) + 18) / 2}" y="{y0 + 15}" text-anchor="middle" font-size="11" fill="{MUTED}">{badge}</text>
    {desc_lines}
    {''.join(chips)}
    <circle cx="{W - 30 - 8 * len(lang)}" cy="{H - 32}" r="5" fill="{lang_color}"/>
    <text x="{W - 22}" y="{H - 27.5}" text-anchor="end" font-size="12" fill="{MUTED}">{lang}</text>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{BORDER}"/>
</svg>
"""
    (OUT / f"{slug}.svg").write_text(svg, encoding="utf-8")
    print(f"cards/{slug}.svg {len(svg) // 1024} KB")
