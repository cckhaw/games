# Generates art/tower-stack.svg: an isometric tower of studded bricks on a baseplate.
import math
S = 44                      # px per unit
OX, OY = 480, 270           # screen position of plate corner (x=0,y=0,z=0)
K = math.sqrt(3) / 2
def P(x, y, z=0):           # +x goes right-down, +y goes left-down, +z goes up
    return (OX + (x - y) * K * S, OY + (x + y) * 0.5 * S - z * S)
def poly(pts, fill, extra=''):
    return f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{fill}" {extra}/>'
def shade(hexc, f):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    m = lambda c: max(0, min(255, int(c * f)))
    return f'#{m(r):02x}{m(g):02x}{m(b):02x}'
def stud(cx, cy_top, base, hs=0.18):
    rx, ry = 1.2247 * 0.34 * S, 0.7071 * 0.34 * S
    h = hs * S
    return (f'<path d="M{cx-rx:.1f},{cy_top:.1f} v{h:.1f} a{rx:.1f},{ry:.1f} 0 0 0 {2*rx:.1f},0 v{-h:.1f}z" fill="{shade(base,.78)}"/>'
            f'<ellipse cx="{cx:.1f}" cy="{cy_top:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{shade(base,1.12)}"/>')
def brick(x0, y0, w, d, z0, h, color, studs=True, stroke='rgba(0,0,0,.18)'):
    z1 = z0 + h
    out = [poly([P(x0, y0 + d, z0), P(x0 + w, y0 + d, z0), P(x0 + w, y0 + d, z1), P(x0, y0 + d, z1)], shade(color, .86)),   # left face
           poly([P(x0 + w, y0, z0), P(x0 + w, y0 + d, z0), P(x0 + w, y0 + d, z1), P(x0 + w, y0, z1)], shade(color, .66)),   # right face
           poly([P(x0, y0, z1), P(x0 + w, y0, z1), P(x0 + w, y0 + d, z1), P(x0, y0 + d, z1)], shade(color, 1.0))]            # top face
    if studs:
        cells = [(i, j) for i in range(int(w)) for j in range(int(d))]
        cx0, cy0 = (w - int(w)) / 2, (d - int(d)) / 2
        for i, j in sorted(cells, key=lambda c: c[0] + c[1]):
            sx, sy = P(x0 + cx0 + i + .5, y0 + cy0 + j + .5, z1)
            out.append(stud(sx, sy, color))
    return '\n'.join(out)

parts = []
# soft shadow under the plate
parts.append(f'<ellipse cx="480" cy="{OY+9*0.5*S*1.0+40:.0f}" rx="380" ry="46" fill="#7a3b4a" opacity=".16" filter="url(#blur)"/>')
# baseplate (9x9, 0.6 high) with a stud grid
parts.append(brick(0, 0, 9, 9, 0, 0.6, '#8d9bb0'))
# tower: [x offset, y offset, size, color] bottom -> top, slightly imperfect like a real game
levels = [(2.5, 2.5, 4.0, '#e8343c'), (2.6, 2.4, 3.8, '#ffc928'), (2.4, 2.7, 3.7, '#7ed321'),
          (2.7, 2.5, 3.5, '#19c3e6'), (2.55, 2.55, 3.2, '#9b45e8'), (2.7, 2.6, 3.0, '#ff5fa2')]
z = 0.6
for (x, y, sz, c) in levels:
    parts.append(brick(x, y, sz, sz, z, 1.0, c)); z += 1.0
# the sliver that just got sliced off, falling away
sx0, sy0, sw, sd, sz0 = 8.4, 0.4, 1.2, 2.4, 2.6
parts.append(brick(sx0, sy0, sw, sd, sz0, 0.9, '#ff5fa2', studs=False))
tx, ty = P(sx0 + sw / 2, sy0 + sd / 2, sz0 + 0.9)       # top-centre of the falling slice, for its motion lines
trail = ''.join(f'<line x1="{tx+dx:.0f}" y1="{ty-off-70+dy:.0f}" x2="{tx+dx:.0f}" y2="{ty-off:.0f}"/>' for dx, off, dy in ((-28, 34, 14), (0, 44, 0), (28, 30, 18)))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="720" viewBox="0 0 960 720">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff0e6"/><stop offset=".55" stop-color="#ffd9dc"/><stop offset="1" stop-color="#ffc3c9"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".4" r=".6"><stop offset="0" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<filter id="blur"><feGaussianBlur stdDeviation="14"/></filter>
</defs>
<rect width="960" height="720" fill="url(#bg)"/><rect width="960" height="720" fill="url(#glow)"/>
<g fill="#fff" opacity=".45"><circle cx="110" cy="130" r="46"/><circle cx="860" cy="190" r="70"/><circle cx="170" cy="610" r="34"/><circle cx="830" cy="640" r="52"/></g>
{chr(10).join(parts)}
<!-- motion lines for the falling slice -->
<g stroke="#ff5fa2" stroke-width="7" stroke-linecap="round" opacity=".55">{trail}</g>
<!-- perfect sparkles -->
<g fill="#ffb800"><path d="M300 150 l9 24 24 9 -24 9 -9 24 -9 -24 -24 -9 24 -9z"/><path d="M230 250 l6 15 15 6 -15 6 -6 15 -6 -15 -15 -6 15 -6z" opacity=".8"/><path d="M345 80 l5 12 12 5 -12 5 -5 12 -5 -12 -12 -5 12 -5z" opacity=".7"/></g>
</svg>'''
open('art/tower-stack.svg', 'w').write(svg)
