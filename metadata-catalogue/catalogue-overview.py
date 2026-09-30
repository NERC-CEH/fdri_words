"""Generate the EIDC catalogue overview diagram (UKCEH brand) as SVG."""
from PIL import ImageFont

FONT_DIR = '/usr/share/fonts/truetype/liberation/'
_fonts = {}


def width(text, size, bold=False):
    key = (size, bold)
    if key not in _fonts:
        name = 'LiberationSans-Bold.ttf' if bold else 'LiberationSans-Regular.ttf'
        _fonts[key] = ImageFont.truetype(FONT_DIR + name, size)
    return _fonts[key].getlength(text)


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def wrap(text, size, max_w):
    lines, line = [], ''
    for word in text.split():
        trial = (line + ' ' + word).strip()
        if width(trial, size) > max_w and line:
            lines.append(line)
            line = word
        else:
            line = trial
    lines.append(line)
    return lines


BLACK, WHITE, AIR, WATER, LAND, EARTH, LIME = (
    '#000000', '#FFFFFF', '#D6EAE6', '#477AE2', '#90A968', '#D7B7AA', '#DBFE52')

W, H = 1920, 1080
TOP, BOTTOM = 292, 968
LEFT_X, LEFT_W = 96, 684          # left panel rows
CAT_X, CAT_W = 832, 256           # catalogue box
RIGHT_X = CAT_X + CAT_W + 52      # right panel rows
RIGHT_W = W - 96 - RIGHT_X
LABEL_COL = 190                   # group-name column inside a row
CHIP_FS, CHIP_H, CHIP_PAD, CHIP_GAP = 18, 36, 10, 8
NOTE_FS = 15

# (group, relationship, chips, note). A chip is a name or (name, 'planned').
LEFT = [
    ('Access', 'authenticates users', ['Proxy', 'Crowd'], None),
    ('Storage', 'holds records and files', ['SAN (Git datastore)', 'Data Store Nginx'], None),
    ('Search & maps', 'indexes and renders', ['Solr', 'MapServer'], None),
    ('Upload', 'receives data files', ['Hubbub', 'Postgres', 'Jira'],
     'Hubbub uploads straight to the SAN; Jira tracks ingestion'),
    ('Vocabularies', 'loads at startup', ['Skosmos', 'GEMET', 'eLTER', 'NVS', 'AGROVOC'], None),
    ('Assistance', 'helps the editor', ['Legilo', 'LLM', 'Amazon Bedrock'],
     'Legilo suggests keywords; Bedrock powers semantic search'),
    ('Harvested', 'imports metadata', ['GitHub', ('FDRI Metadata Service', 'planned')], None),
    ('Publishing', 'exports and hosts', ['Fuseki', 'DataCite', 'DRI-UI'], None),
]

RIGHT = [
    ('Data access', 'downloads and orders',
     ['Data Packager', 'Datastore downloads', 'CEDA archive', 'Order Manager'],
     'Data Packager serves zipped files from the SAN; Order Manager (Licensing Team) uses MongoDB and FME'),
    ('Documents', 'supporting files', ['Data Packager'], None),
    ('Map layers', 'view data on a map', ['WMS via MapServer'], None),
    ('Identifiers', 'IDs and registries',
     ['DOIs (DataCite)', 'ORCID', 'ROR', 'Gateway to Research', 'Wikidata', 'GeoNames', 'DEIMS'], None),
    ('Entry point', 'links into the catalogue', ['EIDC website'], None),
]


def layout_chips(chips, x0, max_w):
    """Return [(x, line, name, planned)] and the number of lines."""
    placed, x, line = [], x0, 0
    for chip in chips:
        name, planned = (chip, False) if isinstance(chip, str) else (chip[0], True)
        w = width(name, CHIP_FS) + 2 * CHIP_PAD
        if planned:
            w += width('PLANNED', 13, True) + 14
        if x + w > x0 + max_w and x > x0:
            x, line = x0, line + 1
        placed.append((x, line, name, planned, w))
        x += w + CHIP_GAP
    return placed, line + 1


def row_height(chips, note, chip_w):
    _, n = layout_chips(chips, 0, chip_w)
    h = 16 + n * CHIP_H + (n - 1) * 8 + 16
    if note:
        h += len(wrap(note, NOTE_FS, chip_w)) * 20 + 2
    return max(h, 70)


def panel(rows, x, w, stroke):
    chip_w = w - LABEL_COL - 36
    heights = [row_height(c, n, chip_w) for _, _, c, n in rows]
    gap = (BOTTOM - TOP - sum(heights)) / (len(rows) - 1)
    assert gap >= 8, f'rows overflow: gap {gap:.1f}'
    out, centres, y = [], [], TOP
    for (name, rel, chips, note), h in zip(rows, heights):
        out.append(f'<rect x="{x}" y="{y:.0f}" width="{w}" height="{h}" fill="{BLACK}" '
                   f'stroke="{stroke}" stroke-width="2"/>')
        out.append(f'<text class="grp" x="{x + 20}" y="{y + 34:.0f}">{esc(name)}</text>')
        out.append(f'<text class="rel" x="{x + 20}" y="{y + 58:.0f}">{esc(rel)}</text>')
        cx0 = x + LABEL_COL + 16
        placed, n = layout_chips(chips, cx0, chip_w)
        for cx, line, cname, planned, cw in placed:
            cy = y + 16 + line * (CHIP_H + 8)
            dash = ' stroke-dasharray="6 5"' if planned else ''
            out.append(f'<rect x="{cx:.0f}" y="{cy:.0f}" width="{cw:.0f}" height="{CHIP_H}" '
                       f'fill="{BLACK}" stroke="{WHITE}" stroke-width="1.5"{dash}/>')
            out.append(f'<text class="chip" x="{cx + CHIP_PAD:.0f}" y="{cy + 24:.0f}">{esc(cname)}</text>')
            if planned:
                tx = cx + CHIP_PAD + width(cname, CHIP_FS) + 10
                out.append(f'<text class="tag" x="{tx:.0f}" y="{cy + 23:.0f}">PLANNED</text>')
        if note:
            ny = y + 16 + n * CHIP_H + (n - 1) * 8 + 22
            for i, ln in enumerate(wrap(note, NOTE_FS, chip_w)):
                out.append(f'<text class="note" x="{cx0}" y="{ny + i * 20:.0f}">{esc(ln)}</text>')
        centres.append(y + h / 2)
        y += h + gap
    return out, centres


left_svg, left_c = panel(LEFT, LEFT_X, LEFT_W, AIR)
right_svg, right_c = panel(RIGHT, RIGHT_X, RIGHT_W, EARTH)

links = []
mid = (TOP + BOTTOM) / 2
# Left: every row stubs into one vertical bus, which joins the catalogue.
bx = (LEFT_X + LEFT_W + CAT_X) / 2
for yc in left_c:
    links.append(f'<line class="need" x1="{LEFT_X + LEFT_W}" y1="{yc:.0f}" x2="{bx}" y2="{yc:.0f}"/>')
links.append(f'<line class="need" x1="{bx}" y1="{left_c[0]:.0f}" x2="{bx}" y2="{left_c[-1]:.0f}"/>')
links.append(f'<line class="need" x1="{bx}" y1="{mid:.0f}" x2="{CAT_X - 8}" y2="{mid:.0f}"/>')
# Right: the catalogue feeds a dashed bus that points at every row.
rb = (CAT_X + CAT_W + RIGHT_X) / 2
links.append(f'<line class="link" x1="{CAT_X + CAT_W + 8}" y1="{mid:.0f}" x2="{rb}" y2="{mid:.0f}"/>')
links.append(f'<line class="link" x1="{rb}" y1="{right_c[0]:.0f}" x2="{rb}" y2="{right_c[-1]:.0f}"/>')
for yc in right_c:
    links.append(f'<line class="link" marker-end="url(#arrow)" x1="{rb}" y1="{yc:.0f}" x2="{RIGHT_X - 3}" y2="{yc:.0f}"/>')
for x in (bx, rb):
    links.append(f'<circle cx="{x}" cy="{mid:.0f}" r="6" fill="{LIME}"/>')

# Centre: catalogue box with the knowledge-graph motif and its parts.
ccx = CAT_X + CAT_W / 2
nodes = [(0, 0, 18, WHITE), (-62, -58, 11, AIR), (0, -86, 8, LAND), (60, -60, 11, EARTH),
         (84, 6, 9, LAND), (56, 66, 11, AIR), (0, 88, 8, EARTH), (-58, 64, 9, LAND), (-84, 4, 8, EARTH)]
gy = 470
edges = [(0, i) for i in range(1, 9)] + [(i, i % 8 + 1) for i in range(1, 9)]
centre = []
for a, b in edges:
    xa, ya, *_ = nodes[a]
    xb, yb, *_ = nodes[b]
    centre.append(f'<line class="edge" x1="{ccx + xa:.0f}" y1="{gy + ya}" x2="{ccx + xb:.0f}" y2="{gy + yb}"/>')
for x, y, r, c in nodes:
    centre.append(f'<circle cx="{ccx + x:.0f}" cy="{gy + y}" r="{r}" fill="{c}"/>')
parts = ['Metadata editor', 'Knowledge graph', 'Templates', 'MCP server']
py = 668
for i, p in enumerate(parts):
    y = py + i * 56
    centre.append(f'<rect x="{CAT_X + 24}" y="{y}" width="{CAT_W - 48}" height="42" fill="{BLACK}" '
                  f'stroke="{LAND}" stroke-width="2"/>')
    centre.append(f'<text class="chip" x="{ccx:.0f}" y="{y + 28}" text-anchor="middle">{p}</text>')
b = 28
x0, y0, x1, y1 = CAT_X, TOP, CAT_X + CAT_W, BOTTOM
brackets = [f'M{x0},{y0 + b} V{y0} H{x0 + b}', f'M{x1},{y0 + b} V{y0} H{x1 - b}',
            f'M{x0},{y1 - b} V{y1} H{x0 + b}', f'M{x1},{y1 - b} V{y1} H{x1 - b}']

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <title>EIDC catalogue overview</title>
  <desc>The services the EIDC metadata catalogue needs to run, grouped on the left, and the services its record content links to, grouped on the right.</desc>
  <defs>
    <style>
      text {{ font-family: 'Suisse International', Arial, 'Liberation Sans', sans-serif; }}
      .title {{ font-size: 48px; font-weight: 500; fill: {WHITE}; }}
      .sub   {{ font-size: 24px; fill: {AIR}; }}
      .label {{ font-size: 24px; font-weight: 600; fill: {WATER}; letter-spacing: 1px; }}
      .grp   {{ font-size: 21px; font-weight: 600; fill: {WHITE}; }}
      .rel   {{ font-size: 16px; fill: {AIR}; }}
      .chip  {{ font-size: {CHIP_FS}px; fill: {WHITE}; }}
      .tag   {{ font-size: 13px; font-weight: 700; fill: {LAND}; letter-spacing: 1px; }}
      .note  {{ font-size: {NOTE_FS}px; fill: {AIR}; }}
      .cat   {{ font-size: 30px; font-weight: 500; fill: {WHITE}; }}
      .cap   {{ font-size: 17px; fill: {AIR}; }}
      .foot  {{ font-size: 18px; fill: {AIR}; }}
      .need  {{ fill: none; stroke: {LIME}; stroke-width: 3; }}
      .link  {{ fill: none; stroke: {LIME}; stroke-width: 3; stroke-dasharray: 10 8; }}
      .edge  {{ stroke: {AIR}; stroke-width: 2; opacity: 0.7; }}
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="{LIME}"/>
    </marker>
  </defs>
  <rect width="{W}" height="{H}" fill="{BLACK}"/>
  <text class="title" x="96" y="112">What the EIDC catalogue runs on, and what it links to</text>
  <text class="sub" x="96" y="156">Infrastructure the catalogue needs to run, and the services its records point people to</text>
  <text class="label" x="{LEFT_X}" y="262">[  NEEDS TO RUN  ]</text>
  <text class="label" x="{ccx:.0f}" y="262" text-anchor="middle">[  CATALOGUE  ]</text>
  <text class="label" x="{RIGHT_X}" y="262">[  CONTENT LINKS TO  ]</text>
  {chr(10).join('  ' + s for s in left_svg)}
  {chr(10).join('  ' + s for s in right_svg)}
  {chr(10).join('  ' + s for s in links)}
  <g fill="none" stroke="{WHITE}" stroke-width="3">{''.join(f'<path d="{d}"/>' for d in brackets)}</g>
  {chr(10).join('  ' + s for s in centre)}
  <text class="cat" x="{ccx:.0f}" y="606" text-anchor="middle">EIDC catalogue</text>
  <text class="cap" x="{ccx:.0f}" y="634" text-anchor="middle">Java application</text>
  <line class="need" x1="{RIGHT_X}" y1="1016" x2="{RIGHT_X + 60}" y2="1016"/>
  <text class="foot" x="{RIGHT_X + 74}" y="1022">Catalogue depends on it</text>
  <line class="link" x1="{RIGHT_X + 330}" y1="1016" x2="{RIGHT_X + 390}" y2="1016" marker-end="url(#arrow)"/>
  <text class="foot" x="{RIGHT_X + 404}" y="1022">Records link to it</text>
  <text class="foot" x="96" y="1022">UKCEH Environmental Information Data Centre · metadata catalogue overview</text>
</svg>
'''

with open(__file__.replace('.py', '.svg'), 'w') as f:
    f.write(svg)
print('left rows', [round(c) for c in left_c])
print('right rows', [round(c) for c in right_c])
