"""Shared palette and window chrome for the profile SVGs.

Colours follow the dark theme of hashim-almasaabi.netlify.app.
"""

BG = "#0d1117"
WINDOW = "#101216"
TITLEBAR = "#15181e"
BORDER = "#262b34"
TEXT = "#e6edf3"
MUTED = "#7d8590"
ACCENT = "#0fbb7e"
ACCENT_LIGHT = "#5ee3ad"
ACCENT_DARK = "#09734d"
ACCENT_DEEP = "#0a4a34"
LINK = "#58a6ff"
GOLD = "#e3b341"
FONT = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

# Empty day, then four intensity steps.
LEVELS = ["#1a1d24", "#0b3d2c", "#0a6547", "#0d9768", "#1fd898"]


def window(width, height, title, body, radius=12):
    """Wrap `body` in a terminal window with traffic lights and a centred title."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="{FONT}">
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="{radius}" fill="{WINDOW}" stroke="{BORDER}"/>
  <path d="M{radius} 0.5 H{width - radius} A{radius - 0.5} {radius - 0.5} 0 0 1 {width - 0.5} {radius} V40 H0.5 V{radius} A{radius - 0.5} {radius - 0.5} 0 0 1 {radius} 0.5 Z" fill="{TITLEBAR}"/>
  <line x1="0.5" y1="40" x2="{width - 0.5}" y2="40" stroke="{BORDER}"/>
  <circle cx="22" cy="20" r="6" fill="#ff5f57"/>
  <circle cx="42" cy="20" r="6" fill="#febc2e"/>
  <circle cx="62" cy="20" r="6" fill="#28c840"/>
  <text x="{width / 2}" y="25" text-anchor="middle" font-size="13" fill="{MUTED}">{title}</text>
{body}
</svg>
"""
