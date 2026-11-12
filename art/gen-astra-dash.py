# Generates art/astra-dash.svg: a bright low-poly sky world of floating islands with the Astra star dashing across.
import math, random
random.seed(11)
K = math.sqrt(3) / 2
S = 30
NAVY = '#1d1f4a'

def island(cx, cy, n, thick=1.1, drop=None, parts_on_top=None):
    """Floating isle. Top-face centre is at (cx, cy); the top surface is z=0, sides go to negative z."""
    drop = drop if drop is not None else n * 0.95
    L = lambda x, y, z=0: (cx + (x - y) * K * S, cy + (x + y - n) * 0.5 * S - z * S)
    fmt = lambda pts: ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)
    out = []
    apex = L(n / 2, n / 2, -thick - drop)
    out.append(f'<polygon points="{fmt([L(0,n,-thick), L(n,n,-thick), apex])}" fill="#6b4a3c"/>')           # rock, left
    out.append(f'<polygon points="{fmt([L(n,0,-thick), L(n,n,-thick), apex])}" fill="#533729"/>')          # rock, right
    mid = L(n * 0.55, n, -thick - drop * 0.42)
    out.append(f'<polygon points="{fmt([L(n*0.2,n,-thick), L(n*0.75,n,-thick), mid])}" fill="#7d5a49" opacity=".7"/>')
    out.append(f'<polygon points="{fmt([L(0,n,0), L(n,n,0), L(n,n,-thick), L(0,n,-thick)])}" fill="#a2622f"/>')   # dirt, left
    out.append(f'<polygon points="{fmt([L(n,0,0), L(n,n,0), L(n,n,-thick), L(n,0,-thick)])}" fill="#7e4a22"/>')   # dirt, right
    out.append(f'<polygon points="{fmt([L(0,n,0), L(n,n,0), L(n,n,-0.28), L(0,n,-0.28)])}" fill="#4fa83f"/>')      # grass lip
    out.append(f'<polygon points="{fmt([L(n,0,0), L(n,n,0), L(n,n,-0.28), L(n,0,-0.28)])}" fill="#3d8a34"/>')
    for i in range(n):                                                                                            # checkered top
        for j in range(n):
            c = '#63c653' if (i + j) % 2 == 0 else '#52b548'
            out.append(f'<polygon points="{fmt([L(i,j), L(i+1,j), L(i+1,j+1), L(i,j+1)])}" fill="{c}"/>')
    return L, ''.join(out)

def pine(x, base, h):
    w = h * .55
    s = [f'<rect x="{x-h*.035:.1f}" y="{base-h*.14:.1f}" width="{h*.07:.1f}" height="{h*.14:.1f}" fill="#6b3f1e"/>']
    for k, c in ((0, '#2f8f46'), (.3, '#37a24f'), (.55, '#43b85a')):
        top = base - h * (.14 + .86 * (1 - k)); bot = top + h * .5; ww = w * (1 - k * .5)
        s.append(f'<polygon points="{x:.1f},{top:.1f} {x-ww/2:.1f},{bot:.1f} {x+ww/2:.1f},{bot:.1f}" fill="{c}"/>')
    return ''.join(s)

def cloud(x, y, s=1.0, o=.95):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#fff" opacity="{o}"><circle cx="0" cy="0" r="30"/><circle cx="34" cy="-12" r="38"/><circle cx="76" cy="0" r="30"/>'
            f'<rect x="-20" y="0" width="120" height="30" rx="15"/></g>')

def coin(x, y, r=13):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffd43b" stroke="#e29a00" stroke-width="3"/>'
            f'<rect x="{x-2.5}" y="{y-r*.5}" width="5" height="{r}" rx="2" fill="#e29a00"/>')

def slime(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="2" rx="30" ry="7" fill="#000" opacity=".18"/>'
            f'<path d="M-28,0 C-28,-34 -12,-44 0,-44 C12,-44 28,-34 28,0 Z" fill="#7be35a" stroke="#4aa832" stroke-width="3"/>'
            f'<ellipse cx="-9" cy="-24" rx="6" ry="8" fill="#fff"/><ellipse cx="9" cy="-24" rx="6" ry="8" fill="#fff"/>'
            f'<circle cx="-8" cy="-22" r="3.4" fill="{NAVY}"/><circle cx="10" cy="-22" r="3.4" fill="{NAVY}"/>'
            f'<path d="M-6,-10 q6,6 12,0" fill="none" stroke="{NAVY}" stroke-width="2.6" stroke-linecap="round"/>'
            f'<ellipse cx="-17" cy="-12" rx="4" ry="2.5" fill="#ff9ab0" opacity=".8"/><ellipse cx="17" cy="-12" rx="4" ry="2.5" fill="#ff9ab0" opacity=".8"/></g>')

def star(cx, cy, R=78, r=36, rot=-14):
    pts = []
    for k in range(10):
        a = math.radians(-90 + k * 36); rad = R if k % 2 == 0 else r
        pts.append((rad * math.cos(a), rad * math.sin(a)))
    p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return (f'<g transform="translate({cx} {cy}) rotate({rot})">'
            f'<polygon points="{p}" fill="#ffd43b" stroke="{NAVY}" stroke-width="9" stroke-linejoin="round"/>'
            f'<polygon points="{p}" fill="none" stroke="#fff3a8" stroke-width="3" stroke-linejoin="round" opacity=".0"/>'
            f'<ellipse cx="-17" cy="-4" rx="7" ry="10" fill="{NAVY}"/><ellipse cx="17" cy="-4" rx="7" ry="10" fill="{NAVY}"/>'
            f'<circle cx="-15" cy="-8" r="3" fill="#fff"/><circle cx="19" cy="-8" r="3" fill="#fff"/>'
            f'<path d="M-12,12 q12,14 24,0" fill="none" stroke="{NAVY}" stroke-width="5" stroke-linecap="round"/>'
            f'<ellipse cx="-31" cy="8" rx="8" ry="5" fill="#ff8fab"/><ellipse cx="31" cy="8" rx="8" ry="5" fill="#ff8fab"/></g>')

parts = []
parts.append('<rect width="960" height="720" fill="url(#sky)"/>')
parts.append('<circle cx="820" cy="110" r="150" fill="#fff8c9" opacity=".6" filter="url(#blur)"/><circle cx="820" cy="110" r="52" fill="#fff2a8"/>')
# rainbow
for i, c in enumerate(('#ff6b6b', '#ffa94d', '#ffe066', '#8ce99a', '#74c0fc', '#b197fc')):
    parts.append(f'<circle cx="480" cy="600" r="{430 - i*22}" fill="none" stroke="{c}" stroke-width="22" opacity=".8"/>')
parts += [cloud(60, 150, 1.1), cloud(640, 70, .9, .9), cloud(790, 300, 1.0, .9), cloud(300, 40, .7, .85), cloud(-10, 470, 1.2, .9)]
# sea
parts.append('<rect y="590" width="960" height="130" fill="url(#sea)"/>')
for i, (y, op) in enumerate(((606, .35), (630, .3), (660, .25), (692, .2))):
    parts.append(f'<path d="M0,{y} q60,-10 120,0 t120,0 t120,0 t120,0 t120,0 t120,0 t120,0 t120,0" fill="none" stroke="#fff" stroke-width="4" opacity="{op}"/>')
for (x, y, rx) in ((330, 668, 130), (720, 625, 100), (150, 610, 60)):
    parts.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx*.13:.0f}" fill="#0b3d73" opacity=".25"/>')

# small far isle (coins), medium isle (flag + pines), big isle (slime + pines)
L, svg = island(150, 250, 3, 0.8)
parts.append(svg); parts.append(pine(*L(1.0, 1.2), 62)[0:0] or pine(L(1.0, 1.2)[0], L(1.0, 1.2)[1], 62))
L, svg = island(735, 395, 5, 1.0)
parts.append(svg)
fx, fy = L(3.4, 2.4)
parts.append(f'<circle cx="{fx:.0f}" cy="{fy-86:.0f}" r="60" fill="#fff59d" opacity=".5" filter="url(#blur)"/>')
for (x, y, h) in ((0.8, 1.0, 92), (1.6, 0.7, 70)):
    px, py = L(x, y); parts.append(pine(px, py, h))
parts.append(f'<rect x="{fx-3:.0f}" y="{fy-120:.0f}" width="6" height="120" rx="3" fill="#f4f4f8" stroke="{NAVY}" stroke-width="2"/>'
             f'<polygon points="{fx+3:.0f},{fy-118:.0f} {fx+56:.0f},{fy-98:.0f} {fx+3:.0f},{fy-76:.0f}" fill="#f0457a" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>'
             f'<circle cx="{fx:.0f}" cy="{fy-122:.0f}" r="6" fill="#ffd43b" stroke="{NAVY}" stroke-width="2"/>')
L, svg = island(330, 498, 7, 1.3, drop=3.6)
parts.append(svg)
for (x, y, h) in ((1.0, 1.3, 118), (2.3, 0.9, 90), (0.9, 3.0, 100), (5.9, 1.0, 84)):
    px, py = L(x, y); parts.append(pine(px, py, h))
sx, sy = L(4.6, 4.2); parts.append(slime(sx, sy, 1.15))
sx2, sy2 = L(2.8, 5.4); parts.append(slime(sx2, sy2, .8))
# coin arc between the small isle and the flag isle
for k in range(6):
    t = k / 5; x = 215 + t * 360; y = 195 - math.sin(t * math.pi) * 25 + t * 30
    parts.append(coin(round(x), round(y)))
# star mascot with a teal speed trail
parts.append('<g stroke-linecap="round" fill="none" opacity=".95"><path d="M380,300 Q440,260 500,238" stroke="#2dd4bf" stroke-width="16"/><path d="M360,330 Q430,290 490,272" stroke="#5eead4" stroke-width="11"/><path d="M400,268 Q450,238 505,214" stroke="#99f6e4" stroke-width="8"/></g>')
parts.append(star(560, 240))
# sparkles
parts.append('<g fill="#fff"><path d="M650 170 l5 13 13 5 -13 5 -5 13 -5 -13 -13 -5 13 -5z"/><path d="M420 150 l4 10 10 4 -10 4 -4 10 -4 -10 -10 -4 10 -4z" opacity=".85"/><path d="M880 330 l4 10 10 4 -10 4 -4 10 -4 -10 -10 -4 10 -4z" opacity=".85"/></g>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="720" viewBox="0 0 960 720">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b82d6"/><stop offset=".6" stop-color="#7cc4f0"/><stop offset="1" stop-color="#bfe6fa"/></linearGradient>
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a97d6"/><stop offset="1" stop-color="#1767a8"/></linearGradient>
<filter id="blur"><feGaussianBlur stdDeviation="18"/></filter>
</defs>
{chr(10).join(parts)}
</svg>'''
open('art/astra-dash.svg', 'w').write(svg)
