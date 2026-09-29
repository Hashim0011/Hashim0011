"""Turn assets/portrait.webp into a coloured ASCII-art SVG.

The photo is a cut-out with a transparent background; transparent cells are
left blank so only the person is drawn.
"""

import pathlib

from PIL import Image, ImageEnhance

from theme import window

ROOT = pathlib.Path(__file__).resolve().parent.parent
COLS = 150
FONT_SIZE = 4.9
CHAR_W = FONT_SIZE * 0.6
LINE_H = FONT_SIZE * 0.98
RAMP = "=+*o#%@"

src = Image.open(ROOT / "assets" / "portrait.webp").convert("RGBA")
left, top, right, bottom = src.getchannel("A").point(lambda a: 255 if a > 128 else 0).getbbox()
# Frame head and shoulders: trim the sides and the lower part of the torso.
w, h = right - left, bottom - top
src = src.crop((left + int(w * 0.1), top, right - int(w * 0.1), top + int(h * 0.82)))
alpha = src.getchannel("A")
img = src.convert("RGB")
img = ImageEnhance.Brightness(img).enhance(1.12)
img = ImageEnhance.Contrast(img).enhance(1.1)
img = ImageEnhance.Color(img).enhance(1.25)

rows = round(COLS * img.height / img.width * CHAR_W / LINE_H)
px = img.resize((COLS, rows), Image.LANCZOS).load()
mask = alpha.resize((COLS, rows), Image.LANCZOS).load()
blank = [[mask[x, y] < 110 for x in range(COLS)] for y in range(rows)]


def cell(x, y):
    r, g, b = px[x, y]
    # Lift near-black (the agal, the beard) so it still reads on a dark card.
    if r + g + b < 150:
        r, g, b = ((c + 70) // 2 + 20 for c in (r, g, b))
    lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    char = RAMP[min(len(RAMP) - 1, int(lum * len(RAMP)))]
    # Quantise so neighbouring cells share a colour and collapse into one tspan.
    q = lambda c: min(255, (c // 12) * 12 + 6)
    return char, f"#{q(r):02x}{q(g):02x}{q(b):02x}"


PAD_X, PAD_Y = 22, 58
lines = []
for y in range(rows):
    runs, cur_color, buf = [], None, ""
    for x in range(COLS):
        char, color = (" ", None) if blank[y][x] else cell(x, y)
        if color != cur_color and buf:
            runs.append((cur_color, buf))
            buf = ""
        cur_color = color
        buf += char
    runs.append((cur_color, buf))
    spans = "".join(
        f'<tspan fill="{c}">{t}</tspan>' if c else f"<tspan>{t}</tspan>" for c, t in runs
    )
    lines.append(f'  <text x="{PAD_X}" y="{PAD_Y + y * LINE_H:.1f}" textLength="{COLS * CHAR_W:.1f}" lengthAdjust="spacing" xml:space="preserve">{spans}</text>')

width = round(PAD_X * 2 + COLS * CHAR_W)
height = round(PAD_Y + rows * LINE_H + 16)
body = f'  <g font-size="{FONT_SIZE}" letter-spacing="0">\n' + "\n".join(lines) + "\n  </g>"
(ROOT / "ascii-portrait.svg").write_text(window(width, height, "portrait.txt", body), encoding="utf-8")
print(f"ascii-portrait.svg {width}x{height}, {rows} rows")
