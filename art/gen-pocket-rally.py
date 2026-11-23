# Generates art/pocket-rally.svg: a toy RC buggy drifting down a plank floor between giant everyday objects.
import math, random
random.seed(5)
VP = (480, 318)            # vanishing point
FLOOR_Y = VP[1]

def lerp(a, b, t): return a + (b - a) * t

def floor_x(side, y, spread=2.15):   # x of the track edge / plank lines at screen y
    return VP[0] + side * (y - FLOOR_Y) * spread

def coin(x, y, s, glow=False):
    r = 22 * s
    out = [f'<ellipse cx="{x+2*s:.1f}" cy="{y+r*0.55:.1f}" rx="{r*0.9:.1f}" ry="{r*0.22:.1f}" fill="#000" opacity=".25"/>']
    out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r*0.34:.1f}" ry="{r:.1f}" fill="#f0b020" stroke="#a86a00" stroke-width="{max(1.5,3*s):.1f}"/>')
    out.append(f'<ellipse cx="{x-r*0.08:.1f}" cy="{y:.1f}" rx="{r*0.16:.1f}" ry="{r*0.68:.1f}" fill="#ffe27a"/>')
    return ''.join(out)

parts = []
# warm hazy backdrop, cellar wall, ceiling beams
parts.append('<rect width="960" height="720" fill="url(#wall)"/>')
parts.append(f'<ellipse cx="{VP[0]}" cy="{VP[1]-10}" rx="420" ry="190" fill="#ffe3a8" opacity=".7" filter="url(#blur)"/>')
for x, w in ((120, 70), (300, 40), (640, 50), (830, 80)):         # distant timber posts
    parts.append(f'<rect x="{x}" y="60" width="{w}" height="{FLOOR_Y-60}" fill="#6b4425" opacity=".55"/>')
parts.append(f'<rect x="0" y="0" width="960" height="70" fill="#4a2e18" opacity=".75"/>')
parts.append(f'<rect x="0" y="70" width="960" height="14" fill="#2c1a0d" opacity=".35"/>')
# plank floor in perspective
parts.append(f'<polygon points="0,{FLOOR_Y} 960,{FLOOR_Y} 960,720 0,720" fill="url(#floor)"/>')
planks = []
for i in range(-6, 7):
    x_bottom = 480 + i * 230
    planks.append(f'<line x1="{VP[0]}" y1="{FLOOR_Y}" x2="{x_bottom}" y2="720" stroke="#5d3615" stroke-width="3" opacity=".4"/>')
y = FLOOR_Y + 8; step = 5
while y < 720:                                                    # board joints, spaced wider as they get closer
    t = (y - FLOOR_Y) / (720 - FLOOR_Y)
    planks.append(f'<line x1="0" y1="{y:.0f}" x2="960" y2="{y:.0f}" stroke="#4a2a10" stroke-width="{1+3*t:.1f}" opacity=".35"/>')
    step *= 1.32; y += step
parts.append(''.join(planks))
# alternating plank shading
shade = []
for i in range(-6, 6):
    c = '#ffffff' if i % 2 else '#000000'
    shade.append(f'<polygon points="{VP[0]},{FLOOR_Y} {480+i*230},720 {480+(i+1)*230},720" fill="{c}" opacity=".06"/>')
parts.append(''.join(shade))

# giant barrel (left) and giant pencil (right) as oversized everyday props
def barrel(cx, base, w, h):
    s = []
    s.append(f'<ellipse cx="{cx+10}" cy="{base+8}" rx="{w*0.62}" ry="{w*0.13}" fill="#000" opacity=".3"/>')
    s.append(f'<path d="M{cx-w/2},{base-h} Q{cx-w*0.62},{base-h/2} {cx-w/2},{base} L{cx+w/2},{base} Q{cx+w*0.62},{base-h/2} {cx+w/2},{base-h}Z" fill="url(#oak)"/>')
    for k in (0.12, 0.38, 0.62, 0.88):
        yy = base - h * k; bulge = w * 0.5 + w * 0.12 * math.sin(k * math.pi)
        s.append(f'<path d="M{cx-bulge},{yy} q{bulge},{w*0.1} {bulge*2},0" fill="none" stroke="#2b1b10" stroke-width="{w*0.05}" opacity=".85"/>')
    s.append(f'<ellipse cx="{cx}" cy="{base-h}" rx="{w/2}" ry="{w*0.13}" fill="#c58a4e"/><ellipse cx="{cx}" cy="{base-h}" rx="{w/2-8}" ry="{w*0.1}" fill="#a96f38"/>')
    return ''.join(s)
parts.append(barrel(130, 470, 210, 250))
parts.append(barrel(46, 360, 90, 100))

def pencil(x0, y0, x1, y1, thick, body, tip='#f1d4a6', lead='#333', ferrule='#c9ced6', eraser='#f08ba0'):
    ang = math.atan2(y1 - y0, x1 - x0); L = math.hypot(x1 - x0, y1 - y0)
    return (f'<g transform="translate({x0} {y0}) rotate({math.degrees(ang):.1f})">'
            f'<ellipse cx="{L/2}" cy="{thick*0.8}" rx="{L*0.52}" ry="{thick*0.28}" fill="#000" opacity=".22"/>'
            f'<rect x="0" y="{-thick/2}" width="{L*0.84}" height="{thick}" rx="4" fill="{body}"/>'
            f'<rect x="0" y="{-thick/2}" width="{L*0.84}" height="{thick*0.28}" rx="3" fill="#fff" opacity=".28"/>'
            f'<polygon points="{L*0.84},{-thick/2} {L},0 {L*0.84},{thick/2}" fill="{tip}"/><polygon points="{L*0.94},{-thick*0.14} {L},0 {L*0.94},{thick*0.14}" fill="{lead}"/>'
            f'<rect x="-{thick*0.5}" y="{-thick/2}" width="{thick*0.5}" height="{thick}" rx="5" fill="{eraser}"/><rect x="-6" y="{-thick/2}" width="8" height="{thick}" fill="{ferrule}"/></g>')
parts.append(pencil(840, 440, 1060, 372, 40, '#f4c430'))
parts.append(pencil(700, 372, 880, 346, 22, '#4fa3e0'))

# coin trail leading to the horizon
for t in (0.05, 0.17, 0.3, 0.44, 0.6, 0.78):
    yy = lerp(FLOOR_Y + 12, 590, t ** 1.1); s = 0.28 + t * 1.15
    xx = 480 + math.sin(t * 5.2) * (40 + 110 * t)
    parts.append(coin(xx, yy, s))

# dust puffs + speed lines behind the car
car_x, car_y = 470, 668
for (dx, dy, r, o) in ((-170, -6, 40, .55), (-215, -26, 30, .45), (-120, -4, 28, .6), (150, -12, 34, .5), (205, -30, 26, .4)):
    parts.append(f'<circle cx="{car_x+dx}" cy="{car_y+dy}" r="{r}" fill="#f1dcb2" opacity="{o}" filter="url(#puff)"/>')

# the buggy, seen from behind, drifting a few degrees
def car():
    g = []
    g.append('<ellipse cx="0" cy="8" rx="150" ry="20" fill="#000" opacity=".35"/>')
    for sx in (-1, 1):                                            # rear wheels
        x0 = 70 if sx > 0 else -122
        g.append(f'<rect x="{x0}" y="-86" width="52" height="86" rx="16" fill="#1c1c1f"/>')
        g.append(f'<rect x="{x0+6}" y="-80" width="14" height="74" rx="7" fill="#3a3a40"/>')
        for k in range(5): g.append(f'<line x1="{x0+4}" y1="{-74+k*16}" x2="{x0+48}" y2="{-70+k*16}" stroke="#0a0a0c" stroke-width="4"/>')
    g.append('<rect x="-84" y="-62" width="168" height="24" rx="8" fill="#2e3340"/>')                         # axle block
    g.append('<polygon points="-86,-40 86,-40 70,-110 -70,-110" fill="#3f64b4"/>')                            # body, rear face
    g.append('<polygon points="-70,-110 70,-110 54,-136 -54,-136" fill="#7ea3ea"/>')                          # top face
    g.append('<polygon points="-86,-40 -70,-110 -54,-136 -70,-70" fill="#2f4d92" opacity=".55"/>')
    for sx in (-1, 1):
        x = 14 * sx - 9
        g.append(f'<rect x="{x}" y="-136" width="18" height="96" fill="#f4f6fa" opacity=".95"/>')              # racing stripes
    for sx in (-1, 1):
        x = 52 * sx - 15
        g.append(f'<rect x="{x}" y="-92" width="30" height="16" rx="5" fill="#ff3b30"/><rect x="{x+4}" y="-90" width="12" height="5" rx="2" fill="#ff9b94"/>')  # tail lights
    g.append('<rect x="-52" y="-150" width="8" height="30" fill="#c53026"/><rect x="44" y="-150" width="8" height="30" fill="#c53026"/>')            # spoiler struts
    g.append('<rect x="-84" y="-168" width="168" height="22" rx="7" fill="#ee4a3c"/><rect x="-84" y="-168" width="168" height="7" rx="4" fill="#ff9a8e"/>')  # spoiler wing
    g.append('<line x1="62" y1="-132" x2="74" y2="-262" stroke="#17171a" stroke-width="5" stroke-linecap="round"/><circle cx="75" cy="-268" r="11" fill="#ee3a2d"/><circle cx="72" cy="-272" r="4" fill="#ffd0cb"/>')  # antenna
    g.append('<circle cx="0" cy="-170" r="34" fill="#7bd651"/>')                                               # driver, from behind
    g.append('<path d="M-36,-170 A36,36 0 0 1 36,-170 L36,-160 Q0,-148 -36,-160 Z" fill="#e53935"/><path d="M-30,-182 A30,30 0 0 1 8,-200" fill="none" stroke="#ff9a94" stroke-width="5" stroke-linecap="round"/>')
    g.append('<polygon points="-26,-198 -16,-224 -6,-198" fill="#58bd34"/><polygon points="6,-198 16,-224 26,-198" fill="#58bd34"/>')   # little horns
    return ''.join(g)
parts.append(f'<g transform="translate({car_x} {car_y}) rotate(-7) scale(1.12)">{car()}</g>')
parts.append('<g stroke="#fff" stroke-linecap="round" opacity=".5" stroke-width="5"><line x1="70" y1="560" x2="200" y2="548"/><line x1="40" y1="610" x2="170" y2="602"/><line x1="790" y1="560" x2="900" y2="572"/><line x1="820" y1="612" x2="935" y2="622"/></g>')
parts.append('<rect width="960" height="720" fill="url(#vig)"/>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="720" viewBox="0 0 960 720">
<defs>
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a5230"/><stop offset=".6" stop-color="#d9b27a"/><stop offset="1" stop-color="#f0d49b"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d7a566"/><stop offset=".45" stop-color="#b9763b"/><stop offset="1" stop-color="#7d4a22"/></linearGradient>
<linearGradient id="oak" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7a4a24"/><stop offset=".45" stop-color="#b57a42"/><stop offset="1" stop-color="#6a3f1e"/></linearGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#1a0d04" stop-opacity=".5"/></radialGradient>
<filter id="blur"><feGaussianBlur stdDeviation="22"/></filter><filter id="puff"><feGaussianBlur stdDeviation="6"/></filter>
</defs>
{chr(10).join(parts)}
</svg>'''
open('art/pocket-rally.svg', 'w').write(svg)
