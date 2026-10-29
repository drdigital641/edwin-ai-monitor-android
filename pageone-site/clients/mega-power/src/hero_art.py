"""Animated SVG scenes for the Mega Power homepage carousel (original artwork, no photos needed).
Each function returns an <svg> string. Motion is CSS (classes styled in mp.css), so it pauses with prefers-reduced-motion."""
import math

# rough continent outlines (lon, lat) - only used to place dots, accuracy is decorative
LAND = [
    [(-10,36),(-9,44),(-5,48),(2,51),(8,55),(5,62),(15,70),(30,71),(40,66),(40,45),(28,41),(20,38),(10,44),(3,43)],  # Europe
    [(-17,21),(-10,35),(10,37),(33,31),(43,12),(51,12),(40,-5),(40,-15),(33,-26),(20,-35),(12,-18),(9,-1),(-8,4),(-17,14)],  # Africa
    [(35,30),(48,30),(57,24),(55,17),(44,12),(38,20)],  # Arabia
    [(40,45),(40,66),(60,70),(100,77),(140,72),(180,68),(160,58),(140,50),(130,42),(122,40),(122,30),(110,20),(108,11),(100,13),(98,8),(92,22),(80,8),(72,20),(62,25),(48,30),(36,36)],  # Asia
    [(98,8),(100,13),(104,10),(103.5,1.5),(101,3)],  # Malay peninsula
    [(95,5),(98,4),(106,-6),(104,-6)],  # Sumatra
    [(109,2),(116,7),(119,5),(117,-3),(111,-3)],  # Borneo
    [(105,-6),(115,-8),(114,-8.8),(106,-7.5)],  # Java
    [(120,18),(122.5,18),(126,7),(122,7)],  # Philippines
    [(131,-1),(141,-3),(150,-10),(141,-9)],  # New Guinea
    [(113,-22),(122,-17),(131,-12),(137,-12),(142,-11),(146,-19),(153,-26),(150,-37),(141,-38),(131,-31),(116,-35),(114,-26)],  # Australia
    [(130,31),(135,34),(141,41),(145,44),(141,36),(135,33)],  # Japan
    [(166,-46),(174,-35),(178,-38),(172,-44)],  # New Zealand
    [(-168,65),(-140,70),(-95,72),(-75,62),(-55,50),(-80,25),(-97,16),(-105,20),(-118,33),(-125,48),(-150,60)],  # N America
    [(-80,10),(-60,11),(-35,-6),(-40,-22),(-58,-38),(-68,-55),(-75,-45),(-71,-18),(-81,-5)],  # S America
]

def _inside(x, y, poly):
    c = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]; xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            c = not c
        j = i
    return c

def world():
    W, H = 1200, 640
    L0, L1, T0, T1 = -6, 214, 72, -48          # Singapore sits at the centre
    def xy(lon, lat):
        return (lon - L0) / (L1 - L0) * W, (T0 - lat) / (T0 - T1) * H
    dots = []
    step = 2.6
    lat = T0
    while lat > T1:
        lon = L0
        while lon < L1:
            ln = lon - 360 if lon > 180 else lon
            if any(_inside(ln, lat, p) for p in LAND):
                x, y = xy(lon, lat)
                dots.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.6"/>')
            lon += step
        lat -= step
    sx, sy = xy(103.8, 1.35)
    targets = [(10, 50), (50, 26), (32, -8), (78, 22), (116, 36), (138, 37), (146, -30), (196, 22)]
    arcs = []
    for k, (lo, la) in enumerate(targets):
        tx, ty = xy(lo, la)
        mx, my = (sx + tx) / 2, (sy + ty) / 2 - max(60, abs(tx - sx) * .28)
        d = f'M{sx:.0f} {sy:.0f} Q{mx:.0f} {my:.0f} {tx:.0f} {ty:.0f}'
        arcs.append(f'<path class="arc" d="{d}" style="animation-delay:{k*.45:.2f}s"/>'
                    f'<path class="arcg" d="{d}"/>'
                    f'<circle class="end" cx="{tx:.0f}" cy="{ty:.0f}" r="4" style="animation-delay:{k*.45+1.2:.2f}s"/>')
    return f'''<svg class="art art-world" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
<g class="land">{"".join(dots)}</g>
<g class="routes">{"".join(arcs)}</g>
<circle class="ring" cx="{sx:.0f}" cy="{sy:.0f}" r="10"/><circle class="ring r2" cx="{sx:.0f}" cy="{sy:.0f}" r="10"/>
<circle class="hub" cx="{sx:.0f}" cy="{sy:.0f}" r="7"/>
<text class="lbl" x="{sx+14:.0f}" y="{sy+5:.0f}">SINGAPORE</text>
</svg>'''

def aircon():
    # a stylised A/C loop: compressor -> condenser -> drier -> expansion valve -> evaporator -> back
    fins = "".join(f'<line x1="{760+i*14}" y1="150" x2="{760+i*14}" y2="300"/>' for i in range(22))
    evap = "".join(f'<line x1="{200+i*14}" y1="400" x2="{200+i*14}" y2="520"/>' for i in range(16))
    flakes = "".join(f'<g class="flake" style="left:0;animation-delay:{i*.9:.1f}s" transform="translate({230+i*45} 540)"><path d="M0-7V7M-6-3.5 6 3.5M-6 3.5 6-3.5"/></g>' for i in range(5))
    return f'''<svg class="art art-ac" viewBox="0 0 1200 640" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
<defs><pattern id="gridp" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="rgba(255,255,255,.05)"/></pattern></defs>
<rect width="1200" height="640" fill="url(#gridp)"/>
<g class="pipe hot"><path d="M560 300 H700 V225 H750"/><path d="M1080 225 H1110 V470 H980"/></g>
<g class="pipe cold"><path d="M940 470 H880"/><path d="M840 470 H440"/><path d="M200 460 H140 V330 H400"/></g>
<g class="flow hot"><path d="M560 300 H700 V225 H750"/><path d="M1080 225 H1110 V470 H980"/></g>
<g class="flow cold"><path d="M940 470 H880"/><path d="M840 470 H440"/><path d="M200 460 H140 V330 H400"/></g>
<g class="unit comp"><rect x="400" y="250" width="160" height="110" rx="22"/><rect x="420" y="270" width="120" height="70" rx="12" class="inner"/>
<g class="pulley" transform="translate(400 305)"><circle r="46"/><circle r="12"/><path d="M0-46V-12M0 12V46M-46 0H-12M12 0H46"/></g>
<text x="480" y="390" class="cap">COMPRESSOR</text></g>
<g class="unit"><rect x="750" y="140" width="330" height="170" rx="10"/><g class="fins">{fins}</g><text x="915" y="340" class="cap">CONDENSER</text></g>
<g class="unit"><rect x="940" y="440" width="40" height="70" rx="12"/><text x="960" y="540" class="cap">DRIER</text></g>
<g class="unit"><path d="M840 455 L880 485 M840 485 L880 455"/><rect x="840" y="452" width="40" height="36" rx="6"/><text x="860" y="520" class="cap">VALVE</text></g>
<g class="unit cool"><rect x="190" y="390" width="230" height="140" rx="10"/><g class="fins">{evap}</g><text x="305" y="570" class="cap">COOLING COIL</text></g>
<g class="fan" transform="translate(915 225)"><g class="blades"><path d="M0 0C10-30 30-34 34-20S12 0 0 0ZM0 0C30 10 34 30 20 34S0 12 0 0ZM0 0C-10 30-30 34-34 20S-12 0 0 0ZM0 0C-30-10-34-30-20-34S0-12 0 0Z"/></g></g>
<g class="flakes">{flakes}</g>
</svg>'''

def singapore(branches):
    # Singapore main island, simplified (lon, lat)
    isl = [(103.64,1.315),(103.655,1.36),(103.69,1.40),(103.72,1.43),(103.76,1.45),(103.80,1.465),(103.84,1.455),(103.87,1.44),(103.91,1.425),(103.95,1.405),(103.99,1.395),(104.03,1.39),(104.07,1.375),(104.09,1.355),(104.04,1.325),(103.99,1.31),(103.95,1.30),(103.91,1.295),(103.87,1.275),(103.84,1.262),(103.80,1.262),(103.76,1.28),(103.72,1.295),(103.68,1.30)]
    W, H = 1200, 640
    L0, L1, T0, T1 = 103.40, 104.16, 1.57, 1.17
    def xy(lon, lat):
        return (lon - L0) / (L1 - L0) * W, (T0 - lat) / (T0 - T1) * H
    dots = []
    lat = T0
    while lat > T1:
        lon = L0
        while lon < L1:
            if _inside(lon, lat, isl):
                x, y = xy(lon, lat)
                dots.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.4"/>')
            lon += .0085
        lat -= .0085
    pins = []
    for k, (name, lo, la) in enumerate(branches):
        x, y = xy(lo, la)
        pins.append(f'''<g class="pin" style="animation-delay:{.3+k*.35:.2f}s" transform="translate({x:.0f} {y:.0f})">
<circle class="ring" r="12" style="animation-delay:{k*.6:.1f}s"/><circle class="dot" r="9"/>
<g class="tag" transform="translate(0 {48 if k == 3 else -24})"><rect x="-{len(name)*5.6+16:.0f}" y="-20" width="{len(name)*11.2+32:.0f}" height="30" rx="15"/><text y="1">{name}</text></g></g>''')
    links = []
    pts = [xy(lo, la) for _, lo, la in branches]
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            links.append(f'<line x1="{pts[i][0]:.0f}" y1="{pts[i][1]:.0f}" x2="{pts[j][0]:.0f}" y2="{pts[j][1]:.0f}"/>')
    return f'''<svg class="art art-sg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
<g class="land">{"".join(dots)}</g><g class="links">{"".join(links)}</g>{"".join(pins)}
</svg>'''
