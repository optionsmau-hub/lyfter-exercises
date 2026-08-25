"""
Builds the SQLite database from schema.sql + seed_data.sql, runs each
labeled query from queries.sql, prints a box-style result table for each
one (like the sqlite3 CLI ".mode box" output) and also renders a
terminal-style PNG "screenshot" of each result using Pillow.
"""
import re
import sqlite3
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "library.db")
SHOT_DIR = os.path.join(BASE, "screenshots")
os.makedirs(SHOT_DIR, exist_ok=True)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

# ---------------------------------------------------------------
# 1. Build the database from scratch
# ---------------------------------------------------------------
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

with open(os.path.join(BASE, "schema.sql")) as f:
    cur.executescript(f.read())
with open(os.path.join(BASE, "seed_data.sql")) as f:
    cur.executescript(f.read())
conn.commit()

# ---------------------------------------------------------------
# 2. Parse queries.sql into labeled (title, sql) pairs
# ---------------------------------------------------------------
with open(os.path.join(BASE, "queries.sql")) as f:
    content = f.read()

blocks = re.split(r"-- =+\n-- (Query \d+: .*?)\n-- =+\n", content)
# blocks[0] is empty/leading whitespace, then alternates: title, sql, title, sql...
pairs = []
for i in range(1, len(blocks), 2):
    title = blocks[i].strip()
    sql = blocks[i + 1].strip()
    pairs.append((title, sql))

# ---------------------------------------------------------------
# 3. Helpers: run a query and format as a box table (text)
# ---------------------------------------------------------------
def run_query(sql):
    cur.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    return cols, rows


def fmt_cell(v):
    return "NULL" if v is None else str(v)


def box_table(cols, rows):
    data = [[fmt_cell(v) for v in row] for row in rows]
    widths = [len(c) for c in cols]
    for row in data:
        for i, v in enumerate(row):
            widths[i] = max(widths[i], len(v))

    def hline(l, m, r):
        return l + m.join("-" * (w + 2) for w in widths) + r

    def row_line(values):
        return "|" + "|".join(f" {v.ljust(w)} " for v, w in zip(values, widths)) + "|"

    lines = [hline("+", "+", "+"), row_line(cols), hline("+", "+", "+")]
    if not data:
        lines.append("|" + " (no rows) ".center(sum(widths) + 3 * len(widths) - 1) + "|")
    else:
        for row in data:
            lines.append(row_line(row))
    lines.append(hline("+", "+", "+"))
    return "\n".join(lines)


# ---------------------------------------------------------------
# 4. Render a terminal-style PNG screenshot for a query result
# ---------------------------------------------------------------
def render_screenshot(path, title, sql, cols, rows):
    font = ImageFont.truetype(FONT_PATH, 18)
    font_bold = ImageFont.truetype(FONT_BOLD_PATH, 18)

    sql_lines = sql.strip().split("\n")
    table_text = box_table(cols, rows)
    table_lines = table_text.split("\n")

    pad = 24
    line_h = 24
    header_h = 42
    bar_label = "sqlite3 -- library.db"

    body_lines = (
        [f"-- {title}", ""]
        + ["sqlite> " + sql_lines[0]]
        + ["   " + l for l in sql_lines[1:]]
        + [""]
        + table_lines
    )

    # Measure using the actual font metrics instead of a rough char estimate
    tmp_img = Image.new("RGB", (10, 10))
    tmp_draw = ImageDraw.Draw(tmp_img)
    max_body_w = max(tmp_draw.textlength(l, font=font) for l in body_lines)
    bar_w = tmp_draw.textlength(bar_label, font=font_bold)

    width = int(max(max_body_w + pad * 2, bar_w + 120, 620))
    height = int(header_h + pad * 2 + line_h * len(body_lines) + 30)

    img = Image.new("RGB", (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    # fake title bar (fixed label, independent of query title length)
    draw.rectangle([0, 0, width, header_h], fill=(45, 45, 48))
    for i, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse([16 + i * 22, header_h / 2 - 7, 30 + i * 22, header_h / 2 + 7], fill=color)
    draw.text((width / 2, header_h / 2), bar_label, font=font_bold, fill=(210, 210, 210), anchor="mm")

    y = header_h + pad
    for line in body_lines:
        if line.startswith("--"):
            color = (150, 150, 150)
        elif line.startswith("sqlite>"):
            color = (120, 200, 255)
        else:
            color = (220, 220, 220)
        draw.text((pad, y), line, font=font, fill=color)
        y += line_h

    img.save(path)


# ---------------------------------------------------------------
# 5. Run everything, print to console, save screenshots
# ---------------------------------------------------------------
summary_lines = []
for idx, (title, sql) in enumerate(pairs, start=1):
    cols, rows = run_query(sql)
    table_text = box_table(cols, rows)
    print(f"\n### {title}\n")
    print(sql)
    print()
    print(table_text)

    slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
    shot_path = os.path.join(SHOT_DIR, f"{idx:02d}_{slug}.png")
    render_screenshot(shot_path, title, sql, cols, rows)
    summary_lines.append((title, sql, cols, rows, os.path.relpath(shot_path, BASE)))

conn.close()

# ---------------------------------------------------------------
# 6. Save a machine-readable summary for building results.md
# ---------------------------------------------------------------
import json
with open(os.path.join(BASE, "_query_results.json"), "w") as f:
    json.dump(
        [
            {"title": t, "sql": s, "cols": c, "rows": r, "screenshot": sp}
            for (t, s, c, r, sp) in summary_lines
        ],
        f,
        indent=2,
    )

print("\n\nDone. Screenshots saved to:", SHOT_DIR)
