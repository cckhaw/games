# Generates art/xiangqi.svg: a wooden Xiangqi board in the starting position.
import math
W, H = 960, 720
CELL = 66
BX, BY = 480 - 4 * CELL, 360 - 4.5 * CELL           # top-left grid intersection
P = lambda c, r: (BX + c * CELL, BY + r * CELL)
FONT = "'Noto Serif CJK SC','Noto Sans CJK SC','Songti SC','SimSun','Source Han Serif SC',serif"
RED, BLK = '#c62828', '#1c1c1c'

parts = []
# walnut surround, warm light, board frame
parts.append('<rect width="960" height="720" fill="url(#walnut)"/>')
for i in range(0, 960, 22):
    parts.append(f'<line x1="{i}" y1="0" x2="{i+30}" y2="720" stroke="#000" stroke-opacity=".07" stroke-width="3"/>')
parts.append('<rect width="960" height="720" fill="url(#vignette)"/>')
fx0, fy0, fx1, fy1 = BX - 52, BY - 50, BX + 8 * CELL + 52, BY + 9 * CELL + 50
parts.append(f'<rect x="{fx0+6}" y="{fy0+14}" width="{fx1-fx0}" height="{fy1-fy0}" rx="22" fill="#000" opacity=".35" filter="url(#blur)"/>')
parts.append(f'<rect x="{fx0}" y="{fy0}" width="{fx1-fx0}" height="{fy1-fy0}" rx="22" fill="url(#frame)"/>')
parts.append(f'<rect x="{fx0+14}" y="{fy0+14}" width="{fx1-fx0-28}" height="{fy1-fy0-28}" rx="12" fill="url(#board)" stroke="#6b4423" stroke-width="3"/>')
# grid
g = ['<g stroke="#5a3b1c" stroke-width="2.6" stroke-linecap="round">']
for r in range(10):
    (x0, y), (x1, _) = P(0, r), P(8, r); g.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}"/>')
for c in range(9):
    x, y0 = P(c, 0); _, y1 = P(c, 9)
    if c in (0, 8): g.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}"/>')
    else:
        _, ya = P(c, 4); _, yb = P(c, 5)
        g.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{ya}"/><line x1="{x}" y1="{yb}" x2="{x}" y2="{y1}"/>')
for (r0, r1) in ((0, 2), (7, 9)):                               # palace diagonals
    for (ca, cb) in ((3, 5), (5, 3)):
        (xa, ya), (xb, yb) = P(ca, r0), P(cb, r1); g.append(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}"/>')
g.append('</g>'); parts.append(''.join(g))
# river
rx, ry = P(0, 4.5)
parts.append(f'<g font-family="{FONT}" font-size="34" fill="#6b4423" opacity=".75" text-anchor="middle" font-weight="700">'
             f'<text x="{BX+1.1*CELL:.0f}" y="{ry+12:.0f}" letter-spacing="14">楚 河</text><text x="{BX+6.9*CELL:.0f}" y="{ry+12:.0f}" letter-spacing="14">漢 界</text></g>')

def piece(c, r, ch, colour, hi=False):
    x, y = P(c, r); R = 29
    s = [f'<ellipse cx="{x+3}" cy="{y+R*0.78+3}" rx="{R*0.95}" ry="{R*0.34}" fill="#000" opacity=".30"/>']
    if hi: s.append(f'<circle cx="{x}" cy="{y}" r="{R+9}" fill="none" stroke="#ffc83d" stroke-width="5"/>')
    s.append(f'<circle cx="{x}" cy="{y}" r="{R}" fill="url(#disc)" stroke="#8a5a2b" stroke-width="3"/>'
             f'<circle cx="{x}" cy="{y}" r="{R-6}" fill="none" stroke="{colour}" stroke-width="2.2"/>'
             f'<text x="{x}" y="{y+11}" font-family="{FONT}" font-size="31" font-weight="900" fill="{colour}" text-anchor="middle">{ch}</text>')
    return ''.join(s)

black_back = ['車', '馬', '象', '士', '將', '士', '象', '馬', '車']
red_back = ['俥', '傌', '相', '仕', '帥', '仕', '相', '傌', '俥']
items = []
for c in range(9):
    items.append((0, c, black_back[c], BLK)); items.append((9, c, red_back[c], RED))
for c in (1, 7): items.append((2, c, '砲', BLK)); items.append((7, c, '炮', RED))
for c in (0, 2, 4, 6, 8): items.append((3, c, '卒', BLK)); items.append((6, c, '兵', RED))
for r, c, ch, col in sorted(items): parts.append(piece(c, r, ch, col, hi=(r, c) == (7, 1)))
# gold move hints for the highlighted cannon
for (c, r) in ((1, 6), (1, 5)):
    x, y = P(c, r); parts.append(f'<circle cx="{x}" cy="{y}" r="9" fill="#ffc83d" opacity=".9"/>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="walnut" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5a3a22"/><stop offset="1" stop-color="#2e1c10"/></linearGradient>
<radialGradient id="vignette" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>
<linearGradient id="frame" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a6633"/><stop offset="1" stop-color="#6e4421"/></linearGradient>
<linearGradient id="board" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f1d49b"/><stop offset="1" stop-color="#dcb575"/></linearGradient>
<radialGradient id="disc" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="#fff8e4"/><stop offset=".7" stop-color="#f0dcae"/><stop offset="1" stop-color="#d9b97a"/></radialGradient>
<filter id="blur"><feGaussianBlur stdDeviation="14"/></filter>
</defs>
{chr(10).join(parts)}
</svg>'''
open('art/xiangqi.svg', 'w').write(svg)
