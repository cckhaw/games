# Generates art/mastermind.svg: a decoding board with glossy pegs on a dark chocolate background.
COL = {'R': '#e53935', 'Y': '#fdd835', 'G': '#2e9e57', 'B': '#4fc3f7', 'O': '#fb8c00', 'P': '#8e55d8'}
def peg(x, y, c, r=30, glow=False):
    base = COL[c]
    s = [f'<ellipse cx="{x+3}" cy="{y+r*0.9+3}" rx="{r*0.95}" ry="{r*0.3}" fill="#000" opacity=".3"/>']
    if glow: s.append(f'<circle cx="{x}" cy="{y}" r="{r+9}" fill="{base}" opacity=".35" filter="url(#blur)"/>')
    s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{base}"/><circle cx="{x}" cy="{y}" r="{r}" fill="url(#gloss)"/>'
             f'<ellipse cx="{x-r*0.32}" cy="{y-r*0.42}" rx="{r*0.34}" ry="{r*0.2}" fill="#fff" opacity=".75" transform="rotate(-25 {x-r*0.32} {y-r*0.42})"/>')
    return ''.join(s)
hole = lambda x, y, r=30: f'<circle cx="{x}" cy="{y}" r="{r}" fill="#1f130c"/><circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#000" stroke-opacity=".5" stroke-width="3"/><circle cx="{x}" cy="{y+2}" r="{r-4}" fill="#170e08"/>'
def key(x, y, k):                       # tiny feedback peg: 'b' black = right place, 'w' white = right colour, '.' empty
    if k == '.': return f'<circle cx="{x}" cy="{y}" r="9" fill="#170e08"/>'
    c = '#111' if k == 'b' else '#f4efe6'
    return f'<circle cx="{x}" cy="{y}" r="9" fill="{c}" stroke="#000" stroke-opacity=".35" stroke-width="1.5"/><circle cx="{x-3}" cy="{y-3}" r="3" fill="#fff" opacity=".7"/>'

parts = []
parts.append('<rect width="960" height="720" fill="url(#bg)"/>')
parts.append('<circle cx="170" cy="130" r="260" fill="#c8794a" opacity=".16" filter="url(#blur)"/><circle cx="820" cy="600" r="280" fill="#d9a066" opacity=".13" filter="url(#blur)"/>')
# board
BX0, BY0, BW, BH = 180, 36, 600, 648
parts.append(f'<rect x="{BX0+8}" y="{BY0+16}" width="{BW}" height="{BH}" rx="34" fill="#000" opacity=".45" filter="url(#blur)"/>')
parts.append(f'<rect x="{BX0}" y="{BY0}" width="{BW}" height="{BH}" rx="34" fill="url(#panel)" stroke="#7a5238" stroke-width="3"/>')
parts.append(f'<rect x="{BX0+14}" y="{BY0+14}" width="{BW-28}" height="{BH-28}" rx="24" fill="none" stroke="#fff" stroke-opacity=".08" stroke-width="2"/>')
# secret code, covered
parts.append(f'<rect x="{BX0+44}" y="{BY0+30}" width="{BW-88}" height="92" rx="20" fill="#2a1a11" stroke="#8a6140" stroke-width="3"/>')
parts.append(f'<rect x="{BX0+52}" y="{BY0+38}" width="{BW-104}" height="76" rx="14" fill="url(#cover)"/>')
parts.append(f'<g font-family="Inter, Helvetica, Arial, sans-serif" font-weight="800" font-size="44" fill="#e9d2b0" text-anchor="middle">'
             + ''.join(f'<text x="{BX0+130+i*103}" y="{BY0+90}" opacity=".9">?</text>' for i in range(4)) + '</g>')
rows = [('RYGB', 'bw..'), ('OORB', 'bbw.'), ('GBYP', 'bww.'), ('PRYG', 'bbb.'), ('RGYR', None)]
y0 = BY0 + 178
for i, (code, fb) in enumerate(rows):
    y = y0 + i * 98
    xs = [BX0 + 112 + k * 88 for k in range(4)]
    if fb is not None:
        for x, c in zip(xs, code): parts.append(hole(x, y)); parts.append(peg(x, y, c))
        for k, f in enumerate(fb):
            parts.append(key(BX0 + 488 + (k % 2) * 28, y - 14 + (k // 2) * 28, f))
    else:                                    # the row being played: three placed, one empty with a peg about to drop in
        for k, (x, c) in enumerate(zip(xs, code)):
            parts.append(hole(x, y))
            if k < 3: parts.append(peg(x, y, c))
        for k in range(4): parts.append(key(BX0 + 488 + (k % 2) * 28, y - 14 + (k // 2) * 28, '.'))
        parts.append(f'<rect x="{BX0+60}" y="{y-44}" width="{BW-120}" height="88" rx="22" fill="none" stroke="#fdd835" stroke-width="3" opacity=".55"/>')
parts.append(peg(xs[3], y0 + 4 * 98 - 34, 'B', 30, glow=True))      # hovering peg
# stray pegs around the board
for (x, y, c, r) in ((92, 560, 'R', 38), (856, 190, 'G', 34), (110, 250, 'Y', 28), (872, 470, 'P', 40), (60, 420, 'O', 24), (900, 640, 'B', 26)):
    parts.append(peg(x, y, c, r))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="720" viewBox="0 0 960 720">
<defs>
<radialGradient id="bg" cx=".5" cy=".4" r=".9"><stop offset="0" stop-color="#4a3022"/><stop offset="1" stop-color="#1b110b"/></radialGradient>
<linearGradient id="panel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a5a40"/><stop offset="1" stop-color="#5a3826"/></linearGradient>
<linearGradient id="cover" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b4a36"/><stop offset="1" stop-color="#4a3022"/></linearGradient>
<radialGradient id="gloss" cx=".35" cy=".3" r=".85"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></radialGradient>
<filter id="blur"><feGaussianBlur stdDeviation="16"/></filter>
</defs>
{chr(10).join(parts)}
</svg>'''
open('art/mastermind.svg', 'w').write(svg)
