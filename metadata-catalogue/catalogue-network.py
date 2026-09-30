"""Generate the metadata catalogue network view (UKCEH brand) as SVG."""
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


BLACK, WHITE, AIR, WATER, LAND, EARTH, LIME = (
    '#000000', '#FFFFFF', '#D6EAE6', '#477AE2', '#90A968', '#D7B7AA', '#DBFE52')

W, H = 1920, 1080
CHIP_FS, CHIP_H, CHIP_PAD, ARROW = 17, 34, 10, 30

# Chip kinds: stroke colour, dash, text colour.
KINDS = {
    'host':     (WATER, '', WHITE),
    'proxy':    (EARTH, '', WHITE),
    'app':      (WHITE, '', WHITE),
    'external': (AIR, '6 5', AIR),
}

out = []


def chip(x, y, text, kind):
    """Draw a chip with its top-left at (x, y); return its right edge."""
    stroke, dash, fill = KINDS[kind]
    w = width(text, CHIP_FS) + 2 * CHIP_PAD
    d = f' stroke-dasharray="{dash}"' if dash else ''
    out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{CHIP_H}" fill="{BLACK}" '
               f'stroke="{stroke}" stroke-width="2"{d}/>')
    out.append(f'<text class="chip" x="{x + CHIP_PAD:.0f}" y="{y + 23:.0f}" fill="{fill}">{esc(text)}</text>')
    return x + w


def arrow(x1, y1, x2, y2, label=None):
    if y1 == y2:
        out.append(f'<line class="flow" marker-end="url(#arrow)" x1="{x1:.0f}" y1="{y1:.0f}" '
                   f'x2="{x2 - 3:.0f}" y2="{y2:.0f}"/>')
    else:  # elbow: across, then down or up, then across
        mx = x1 + 14
        out.append(f'<path class="flow" marker-end="url(#arrow)" '
                   f'd="M{x1:.0f},{y1:.0f} H{mx:.0f} V{y2:.0f} H{x2 - 3:.0f}"/>')
    if label:
        out.append(f'<text class="path" x="{(x1 + x2) / 2 + 7:.0f}" y="{y2 - 8:.0f}" '
                   f'text-anchor="middle">{esc(label)}</text>')


def chain(x, y, items, limit):
    """Lay chips left to right joined by arrows; return right edges of each chip."""
    edges, cy = [], y + CHIP_H / 2
    for i, (text, kind) in enumerate(items):
        if i:
            arrow(x, cy, x + ARROW, cy)
            x += ARROW
        left = x
        x = chip(x, y, text, kind)
        edges.append((left, x))
    assert x <= limit, f'chain {items[0][0]} overflows by {x - limit:.0f}px'
    return edges


def panel(x, y, w, h, name, caption):
    assert width(name, 26, True) + 14 + width(caption, 17) + 40 <= w, f'{name} header overflows'
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BLACK}" stroke="{AIR}" stroke-width="2"/>')
    out.append(f'<text class="ns" x="{x + 20}" y="{y + 36}">{esc(name)}</text>')
    out.append(f'<text class="cap" x="{x + 20 + width(name, 26, True) + 14:.0f}" y="{y + 35}">{esc(caption)}</text>')


def note(x, y, text):
    out.append(f'<text class="note" x="{x:.0f}" y="{y:.0f}">{esc(text)}</text>')


# ===== the catalogue =====
EX, EY, EW, EH = 96, 222, 810, 676
panel(EX, EY, EW, EH, 'Catalogue', 'records, search and exports')
hx, px, ax = EX + 24, EX + 300, EX + 440
limit = EX + EW - 20

bx = EX + 660  # back-end column: triple store and search index

# SPARQL endpoint -> triple store
fy = EY + 80
h_end = chip(hx, fy, 'SPARQL endpoint', 'host')
arrow(h_end, fy + 17, bx, fy + 17)
f_right = chip(bx, fy, 'triple store', 'app')
f_mid = (bx + f_right) / 2

# catalogue website routes
cy = EY + 330
c_end = chip(hx, cy, 'catalogue website', 'host')
route_right = 0
for target, path, ty in (('explorer UI', 'map and data explorers', EY + 200),):
    arrow(c_end, cy + 17, ax, ty + 17, path)
    route_right = max(route_right, chip(ax, ty, target, 'app'))
arrow(c_end, cy + 17, px, cy + 17, 'everything else')
p_end = chip(px, cy, 'proxy', 'proxy')

cat_right = None
for target, ty in (('catalogue app', cy), ('file server', cy + 70), ('map server', cy + 140)):
    arrow(p_end, cy + 17, ax, ty + 17)
    r = chip(ax, ty, target, 'app')
    cat_right = cat_right or r

# catalogue app -> triple store and search index: one trunk out of the catalogue, branching up and down
vx = max(cat_right, route_right) + 20
turn = fy + CHIP_H + 26
sy = cy + 70
out.append(f'<line class="flow" x1="{cat_right}" y1="{cy + 17}" x2="{vx}" y2="{cy + 17}"/>')
out.append(f'<path class="flow" marker-end="url(#arrow)" '
           f'd="M{vx},{cy + 17} V{turn} H{f_mid} V{fy + CHIP_H + 3}"/>')
out.append(f'<path class="flow" marker-end="url(#arrow)" d="M{vx},{cy + 17} V{sy + 17} H{bx - 3}"/>')
s_right = chip(bx, sy, 'search index', 'app')
out.append(f'<circle cx="{vx}" cy="{cy + 17}" r="5" fill="{LIME}"/>')
out.append(f'<text class="path" x="{vx + 10}" y="{turn + 24}">loads triples</text>')
out.append(f'<text class="path" x="{vx + 10}" y="{turn + 42}">on a schedule</text>')
out.append(f'<text class="path" x="{vx + 10}" y="{sy + 8}">queries</text>')
assert bx - vx >= 40, f'back-end column too close to the trunk: {bx - vx:.0f}px'
assert max(f_right, s_right) <= limit, 'back-end column overflows'

# ===== the six supporting services =====
COLW, ROWH, GAP = 432, 204, 32
C1 = EX + EW + 28
C2 = C1 + COLW + 24
assert C2 + COLW <= W - 96 + 4, f'right column overflows: {C2 + COLW}'
rows = [EY, EY + ROWH + GAP, EY + 2 * (ROWH + GAP)]
assert rows[-1] + ROWH <= EY + EH + 2, f'rows overflow: {rows[-1] + ROWH}'


def simple(x, y, name, caption, host, items, extra=None):
    panel(x, y, COLW, ROWH, name, caption)
    lim = x + COLW - 16
    hy, ky = y + 62, y + 118
    h_end = chip(x + 20, hy, host, 'host')
    edges = chain(x + 40, ky, items, lim)
    # host drops down into the first chip of the chain
    out.append(f'<path class="flow" marker-end="url(#arrow)" d="M{x + 30},{hy + CHIP_H} V{ky + 17} H{x + 37}"/>')
    if extra:
        note(x + 20, y + ROWH - 18, extra)
    return edges


simple(C1, rows[0], 'Data packaging', 'zips datasets', 'download site',
       [('proxy', 'proxy'), ('packager', 'app')],
       'Adds metadata and licence information to each zip')
simple(C1, rows[1], 'File integrity', 'Hubbub', 'upload site',
       [('proxy', 'proxy'), ('API', 'app')],
       'Scheduled jobs validate files and report problems')
simple(C1, rows[2], 'Acceptance checks', 'staff tool', 'staff site',
       [('checker', 'app')],
       'Checks dataset files are correctly formatted')

simple(C2, rows[0], 'Vocabularies', 'Skosmos', 'vocabulary site',
       [('proxy', 'proxy'), ('Skosmos', 'app'), ('triple store', 'app')],
       'The proxy keeps draft vocabularies private')
simple(C2, rows[1], 'Keyword suggestions', 'Legilo', 'staff site',
       [('proxy', 'proxy'), ('Legilo', 'app'), ('LLM service', 'external')],
       'Finds keywords in supporting documentation')

# order-manager: proxy fans out to client and api; api calls FME.
ox, oy = C2, rows[2]
panel(ox, oy, COLW, ROWH, 'Orders', 'spatial subsetting')
hy, ky = oy + 62, oy + 112
h_end = chip(ox + 20, hy, 'order site', 'host')
out.append(f'<path class="flow" marker-end="url(#arrow)" d="M{ox + 30},{hy + CHIP_H} V{ky + 17} H{ox + 37}"/>')
p_end = chip(ox + 40, ky, 'proxy', 'proxy')
cl = p_end + ARROW
arrow(p_end, ky + 17, cl, ky + 17)
chip(cl, ky, 'web app', 'app')
ay = ky + 46
arrow(p_end, ky + 17, cl, ay + 17)
a_end = chip(cl, ay, 'API', 'app')
arrow(a_end, ay + 17, a_end + ARROW, ay + 17)
fme_end = chip(a_end + ARROW, ay, 'FME spatial processing', 'external')
assert fme_end <= ox + COLW - 16, 'order-manager overflows'

# ===== storage band =====
SY = EY + EH + 26
out.append(f'<rect x="{EX}" y="{SY}" width="{W - 192}" height="54" fill="{BLACK}" stroke="{LAND}" stroke-width="2"/>')
out.append(f'<text class="ns" x="{EX + 20}" y="{SY + 36}">Storage</text>')
out.append(f'<text class="cap" x="{EX + 34 + width('Storage', 26, True):.0f}" y="{SY + 35}">Shared network storage, mounted into every part of the system: '
           f'datasets, uploads, supporting documents, map files and vocabulary databases</text>')

# ===== legend =====
LY = 1030
lx = EX
for text, kind, desc in (('host', 'host', 'entry point'), ('proxy', 'proxy', 'authentication'),
                         ('app', 'app', 'service and its deployment'), ('external', 'external', 'outside the cluster')):
    stroke, dash, _ = KINDS[kind]
    d = f' stroke-dasharray="{dash}"' if dash else ''
    out.append(f'<rect x="{lx}" y="{LY - 16}" width="34" height="22" fill="{BLACK}" stroke="{stroke}" stroke-width="2"{d}/>')
    out.append(f'<text class="foot" x="{lx + 44}" y="{LY + 1}">{esc(desc)}</text>')
    lx += 44 + width(desc, 18) + 40
out.append(f'<line class="flow" marker-end="url(#arrow)" x1="{lx}" y1="{LY - 5}" x2="{lx + 50}" y2="{LY - 5}"/>')
out.append(f'<text class="foot" x="{lx + 62}" y="{LY + 1}">request or call</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <title>Metadata catalogue network view</title>
  <desc>The parts of the EIDC metadata catalogue system, the entry points that route into each one, the services behind them, and the shared storage they all mount.</desc>
  <defs>
    <style>
      text {{ font-family: 'Suisse International', Arial, 'Liberation Sans', sans-serif; }}
      .title {{ font-size: 48px; font-weight: 500; fill: {WHITE}; }}
      .sub   {{ font-size: 24px; fill: {AIR}; }}
      .ns    {{ font-size: 26px; font-weight: 700; fill: {WHITE}; }}
      .cap   {{ font-size: 17px; fill: {AIR}; }}
      .chip  {{ font-size: {CHIP_FS}px; }}
      .path  {{ font-size: 14px; fill: {AIR}; }}
      .note  {{ font-size: 15px; fill: {AIR}; }}
      .foot  {{ font-size: 18px; fill: {AIR}; }}
      .flow  {{ fill: none; stroke: {LIME}; stroke-width: 2.5; }}
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="{LIME}"/>
    </marker>
  </defs>
  <rect width="{W}" height="{H}" fill="{BLACK}"/>
  <text class="title" x="96" y="112">Metadata catalogue network view</text>
  <text class="sub" x="96" y="156">How requests reach the catalogue and its supporting services, and the storage they share</text>
{chr(10).join('  ' + s for s in out)}
</svg>
'''

import os
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'catalogue-network.svg'), 'w') as f:
    f.write(svg)
