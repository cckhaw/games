# Generates art/track-tarmac.svg: a forest trail that turns into an open road, with a runner and cyclists.
import random
random.seed(7)
H = 350  # horizon y
def edge(y, side):  # x of the road edge at screen y
    return 470 - (y - H) * 1.189 if side == 'L' else 490 + (y - H) * 1.189

def pine(x, base, h, dark, light):
    w = h * 0.55
    t = [f'<rect x="{x-h*0.04:.1f}" y="{base-h*0.12:.1f}" width="{h*0.08:.1f}" height="{h*0.14:.1f}" fill="#4a2f1a"/>']
    for i, (k, c) in enumerate(((0.0, dark), (0.28, dark), (0.52, light))):
        top = base - h * (0.12 + 0.88 * (1 - k)) ; bot = base - h * (0.12 + 0.88 * (1 - k) - 0.5)
        ww = w * (1 - k * 0.55)
        t.append(f'<polygon points="{x:.1f},{top:.1f} {x-ww/2:.1f},{bot:.1f} {x+ww/2:.1f},{bot:.1f}" fill="{c}"/>')
    return ''.join(t)

def runner(s=1.0):
    skin, top, shorts, shoe = '#f2c9a0', '#2fbf5a', '#16213e', '#e63946'
    L = lambda x1, y1, x2, y2, w, c: f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
    P = lambda pts, w, c: f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
    g = [P('-8,-42 -26,-20 -50,-30', 13, skin), L(-50, -30, -58, -34, 12, shoe),          # back leg
         P('-8,-42 16,-22 12,-2', 13, skin), L(12, -2, 26, -2, 12, shoe),                    # front leg
         L(-8, -42, 10, -36, 18, shorts),                                                    # shorts
         L(0, -84, -8, -42, 26, top),                                                        # torso
         P('0,-80 -20,-62 -36,-74', 9, skin),                                                # back arm
         '<circle cx="2" cy="-102" r="14" fill="%s"/>' % skin,
         '<path d="M-12,-108 q14,-14 28,0 l-2,5 q-12,-8 -24,0z" fill="#e63946"/>',          # headband
         P('0,-80 20,-62 40,-74', 9, skin)]                                                  # front arm
    return f'<g transform="scale({s})">' + ''.join(g) + '</g>'

def cyclist(jersey='#ffd23f', s=1.0):
    wheel = lambda cx: (f'<circle cx="{cx}" cy="0" r="30" fill="none" stroke="#111" stroke-width="6"/>'
                        f'<circle cx="{cx}" cy="0" r="3" fill="#111"/><line x1="{cx-26}" y1="0" x2="{cx+26}" y2="0" stroke="#555" stroke-width="1.5"/><line x1="{cx}" y1="-26" x2="{cx}" y2="26" stroke="#555" stroke-width="1.5"/>')
    P = lambda pts, w, c: f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
    g = [wheel(-45), wheel(45),
         P('-45,0 -5,0 -12,-42 30,-44 -5,0', 5, '#d62828'), P('30,-44 45,0', 5, '#d62828'), P('30,-44 36,-52 24,-54', 4, '#222'),
         P('-12,-48 6,-26 2,-4', 12, '#f2c9a0'), '<rect x="-4" y="-8" width="14" height="6" rx="3" fill="#111"/>',
         P('-12,-48 22,-84', 22, jersey),                                                                  # torso
         P('22,-84 34,-62 36,-52', 8, '#f2c9a0'),                                                           # arm
         '<circle cx="31" cy="-98" r="12" fill="#f2c9a0"/>',
         f'<path d="M18,-100 q14,-18 28,-2 l-3,5 q-10,-8 -22,-1z" fill="{jersey}" stroke="#a37b00" stroke-width="1.5"/>',
         P('-12,-48 -2,-44', 14, '#16213e')]
    return f'<g transform="scale({s})">' + ''.join(g) + '</g>'

parts = []
# sky, sun, distant hills
parts.append('<rect width="960" height="720" fill="url(#sky)"/>')
parts.append(f'<circle cx="480" cy="{H-10}" r="120" fill="#fff1c7" opacity=".85" filter="url(#blur)"/><circle cx="480" cy="{H-6}" r="62" fill="#ffe6a0"/>')
parts.append(f'<path d="M0,{H} L0,{H-70} Q90,{H-130} 190,{H-80} T380,{H-60} T580,{H-90} T780,{H-70} T960,{H-100} L960,{H}z" fill="#6c8a8c" opacity=".7"/>')
parts.append(f'<path d="M0,{H} L0,{H-40} Q120,{H-85} 250,{H-45} T520,{H-50} T760,{H-55} T960,{H-45} L960,{H}z" fill="#3f6b57"/>')
# grass either side of the road
parts.append(f'<polygon points="0,{H} 960,{H} 960,720 0,720" fill="url(#grass)"/>')
# tarmac road + edges
parts.append(f'<polygon points="470,{H} 490,{H} {edge(720,"R"):.0f},720 {edge(720,"L"):.0f},720" fill="url(#tarmac)"/>')
# dirt trail in the foreground with a wavy top edge
yt = 545
xl, xr = edge(yt, 'L'), edge(yt, 'R')
wav = f'M{xl:.0f},{yt} q60,-22 120,-4 t120,2 t120,-6 t{xr-xl-360:.0f},4 L{edge(720,"R"):.0f},720 L{edge(720,"L"):.0f},720z'
parts.append(f'<path d="{wav}" fill="url(#dirt)"/>')
# road edge lines + lane dashes (tarmac section only)
parts.append(f'<g stroke="#fff" stroke-linecap="round" opacity=".9"><line x1="{edge(362,"L")+14:.0f}" y1="362" x2="{edge(535,"L")+20:.0f}" y2="535" stroke-width="5"/><line x1="{edge(362,"R")-14:.0f}" y1="362" x2="{edge(535,"R")-20:.0f}" y2="535" stroke-width="5"/></g>')
for frac in (1/3, 2/3):
    dashes = []
    y = 358
    d = 6
    while y < 520:
        y2 = min(y + d * 1.3, 540)
        xa = edge(y, 'L') + (edge(y, 'R') - edge(y, 'L')) * frac; xb = edge(y2, 'L') + (edge(y2, 'R') - edge(y2, 'L')) * frac
        dashes.append(f'<line x1="{xa:.1f}" y1="{y:.1f}" x2="{xb:.1f}" y2="{y2:.1f}" stroke-width="{1.5 + (y-H)/45:.1f}"/>')
        y = y2 + d * 1.1; d *= 1.28
    parts.append('<g stroke="#ffd23f" stroke-linecap="round" opacity=".95">' + ''.join(dashes) + '</g>')
# pine forest on both sides, small to large (far to near)
trees = []
for i in range(20):
    for side in ('L', 'R'):
        for col, (base_off, step) in enumerate(((22, 40), (120, 72))):
            yb = H + 6 + i * 19 + random.uniform(-6, 6) + col * 9; sc = 0.3 + i * 0.13
            off = base_off + i * step * 0.9 + random.uniform(-16, 16)
            x = edge(yb, side) + (-off if side == 'L' else off)
            if -90 < x < 1050: trees.append((yb, pine(x, yb, 90 * sc, '#1c5236' if col else '#1f5a3a', '#2a7347' if col else '#2f7a4a')))
parts += [t for _, t in sorted(trees)]
# finish arch far down the road
parts.append(f'<g transform="translate(480 {H+10})"><rect x="-26" y="-34" width="3" height="34" fill="#eee"/><rect x="23" y="-34" width="3" height="34" fill="#eee"/>'
             + ''.join(f'<rect x="{-26+i*5.2:.1f}" y="{-36+j*4}" width="5.2" height="4" fill="{"#111" if (i+j)%2 else "#fff"}"/>' for i in range(10) for j in range(2)) + '</g>')
# cyclists on tarmac (rival far, hero closer), runner in the foreground
parts.append(f'<g transform="translate(535 420)">{cyclist("#4cc9f0", 0.55)}</g>')
parts.append(f'<g transform="translate(600 505)">{cyclist("#ffd23f", 0.95)}</g>')
parts.append('<g stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".6"><line x1="455" y1="468" x2="505" y2="468"/><line x1="440" y1="490" x2="496" y2="490"/><line x1="462" y1="512" x2="508" y2="512"/></g>')
parts.append('<ellipse cx="300" cy="702" rx="80" ry="11" fill="#000" opacity=".28"/>')
parts.append('<g fill="#b78b5f" opacity=".7"><circle cx="205" cy="690" r="14"/><circle cx="178" cy="682" r="10"/><circle cx="228" cy="702" r="9"/><circle cx="158" cy="694" r="7"/></g>')
parts.append(f'<g transform="translate(300 700) rotate(7)">{runner(1.75)}</g>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="720" viewBox="0 0 960 720">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f8fc0"/><stop offset=".55" stop-color="#a9cfdc"/><stop offset="1" stop-color="#ffd9a0"/></linearGradient>
<linearGradient id="grass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3c7a45"/><stop offset="1" stop-color="#24562e"/></linearGradient>
<linearGradient id="tarmac" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b7077"/><stop offset="1" stop-color="#34383e"/></linearGradient>
<linearGradient id="dirt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a9764a"/><stop offset="1" stop-color="#6e4627"/></linearGradient>
<filter id="blur"><feGaussianBlur stdDeviation="16"/></filter>
</defs>
{chr(10).join(parts)}
</svg>'''
open('art/track-tarmac.svg', 'w').write(svg)
