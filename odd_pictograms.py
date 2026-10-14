"""
SVG pictograms for the Odd One Out activities.

Each item is drawn from scratch with plain SVG shapes, so there are no external
image files, no downloads and no licensing questions. Every entry is keyed by a
short slug that `odd_one_out_content.py` refers to.

Rendered by tools/make_odd_images.py into images/odd/<set>-<n>.svg.
"""

W, H = 200, 150
BG = "#F7FAFF"
INK = "#2D3748"


def svg(body, caption=""):
    cap = ""
    if caption:
        cap = (f'<text x="{W / 2}" y="{H - 8}" text-anchor="middle" font-size="15" '
               f'font-weight="700" fill="{INK}" font-family="Segoe UI, Arial">{caption}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}">'
            f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>'
            f'{body}{cap}</svg>')


def _star(cx, cy, outer, inner, points=5):
    import math
    d = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        a = math.radians(i * 180 / points - 90)
        d.append(f'{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}')
    return f'<polygon points="{" ".join(d)}"/>'


def _cat_face(fur, muzzle, ear_in, stripe=None):
    stripes = ''
    if stripe:
        stripes = ''.join(
            f'<path d="M{72 + i * 16} 50 q6 8 2 16" stroke="{stripe}" '
            f'stroke-width="5" fill="none" stroke-linecap="round"/>'
            for i in range(4))
    return (f'<path d="M62 58 l-6 -30 l30 18z" fill="{ear_in}"/>'
            f'<path d="M138 58 l6 -30 l-30 18z" fill="{ear_in}"/>'
            f'<ellipse cx="100" cy="82" rx="42" ry="38" fill="{fur}"/>'
            f'{stripes}'
            f'<circle cx="86" cy="74" r="5.5" fill="{INK}"/>'
            f'<circle cx="114" cy="74" r="5.5" fill="{INK}"/>'
            f'<ellipse cx="100" cy="94" rx="18" ry="13" fill="{muzzle}"/>'
            f'<path d="M94 88 h12 l-6 8z" fill="{INK}"/>'
            f'<path d="M100 96 q-9 8 -17 3 M100 96 q9 8 17 3" stroke="{INK}" '
            f'stroke-width="3" fill="none" stroke-linecap="round"/>')


PICTOGRAMS = {
    # --- zoo animals ------------------------------------------------------
    "lion": lambda: _cat_face("#C05621", "#F6AD55", "#C05621"),
    "tiger": lambda: _cat_face("#DD6B20", "#FED7AA", "#DD6B20", stripe="#7B341E"),
    "cow": lambda: (
        '<path d="M64 62 q-16 -14 -28 -6 q10 14 24 12z" fill="#A0AEC0"/>'
        '<path d="M136 62 q16 -14 28 -6 q-10 14 -24 12z" fill="#A0AEC0"/>'
        '<ellipse cx="100" cy="84" rx="44" ry="36" fill="#FFFFFF"/>'
        '<ellipse cx="80" cy="70" rx="11" ry="9" fill="#2D3748"/>'
        '<ellipse cx="120" cy="96" rx="9" ry="8" fill="#2D3748"/>'
        '<circle cx="86" cy="80" r="5" fill="{0}"/><circle cx="114" cy="80" r="5" fill="{0}"/>'
        '<ellipse cx="100" cy="100" rx="20" ry="13" fill="#F7FAFF" stroke="#A0AEC0" stroke-width="3"/>'
        '<circle cx="94" cy="98" r="3.5" fill="#2D3748"/><circle cx="106" cy="98" r="3.5" fill="#2D3748"/>'
        '<path d="M100 104 v6 M92 110 q8 6 16 0" stroke="#2D3748" stroke-width="3" '
        'fill="none" stroke-linecap="round"/>'.format(INK)),
    "eagle": lambda: (
        '<ellipse cx="92" cy="94" rx="34" ry="28" fill="#4A5568"/>'
        '<path d="M74 76 q-28 -22 -44 -6 q18 20 44 14z" fill="#718096"/>'
        '<path d="M96 78 q30 -18 50 2 q-24 16 -50 6z" fill="#718096"/>'
        '<circle cx="136" cy="70" r="19" fill="#FFFFFF"/>'
        '<path d="M124 62 a17 17 0 0 1 26 4 a13 13 0 0 0 -22 8z" fill="#E2E8F0"/>'
        '<circle cx="141" cy="67" r="4.5" fill="{0}"/>'
        '<path d="M152 70 l20 7 l-20 8z" fill="#F6AD55"/>'
        '<path d="M92 116 l-4 18 M106 118 l-2 16" stroke="#F6AD55" stroke-width="4" '
        'stroke-linecap="round"/>'.format(INK)),

    # --- food -------------------------------------------------------------
    "apple": lambda: (
        '<path d="M100 52 q-32 8 -32 40 t32 38 t32 -38 t-32 -40z" fill="#E53E3E"/>'
        '<path d="M100 52 q-2 -18 14 -22 q2 16 -14 22z" fill="#38A169"/>'
        '<rect x="98" y="30" width="5" height="26" rx="2" fill="#7B341E"/>'
        '<ellipse cx="84" cy="82" rx="7" ry="11" fill="#FFF5F5" opacity="0.55"/>'),
    "banana": lambda: (
        '<path d="M58 56 q4 62 62 66 q26 2 34 -12 q-14 4 -28 -2 q-42 -18 -44 -52z" fill="#F6C343"/>'
        '<path d="M64 66 q8 46 54 50" stroke="#D69E2E" stroke-width="5" fill="none" '
        'stroke-linecap="round"/>'
        '<path d="M58 56 l-6 -14 l14 6z" fill="#7B341E"/>'),
    "carrot": lambda: (
        '<path d="M100 62 l24 30 l-24 44 l-24 -44z" fill="#DD6B20"/>'
        '<path d="M88 92 h24 M92 106 h16" stroke="#C05621" stroke-width="4" stroke-linecap="round"/>'
        '<path d="M100 62 q-22 -6 -26 -26 q20 2 26 20z" fill="#2F855A"/>'
        '<path d="M100 62 q22 -6 26 -26 q-20 2 -26 20z" fill="#38A169"/>'),

    # --- objects ----------------------------------------------------------
    "ball": lambda: (
        '<circle cx="100" cy="84" r="42" fill="#E53E3E"/>'
        '<path d="M58 84 a42 42 0 0 0 84 0" fill="#C53030"/>'
        '<path d="M74 54 q26 30 26 60 M126 54 q-26 30 -26 60" stroke="#FFF5F5" '
        'stroke-width="4" fill="none"/>'),
    "bus": lambda: (
        '<rect x="34" y="56" width="132" height="52" rx="11" fill="#C53030"/>'
        '<rect x="44" y="65" width="28" height="20" rx="4" fill="#EBF8FF"/>'
        '<rect x="80" y="65" width="28" height="20" rx="4" fill="#EBF8FF"/>'
        '<rect x="116" y="65" width="28" height="20" rx="4" fill="#EBF8FF"/>'
        '<circle cx="70" cy="112" r="14" fill="#2D3748"/><circle cx="70" cy="112" r="5" fill="#A0AEC0"/>'
        '<circle cx="132" cy="112" r="14" fill="#2D3748"/><circle cx="132" cy="112" r="5" fill="#A0AEC0"/>'),
    "train": lambda: (
        '<rect x="38" y="56" width="86" height="52" rx="10" fill="#2B6CB0"/>'
        '<rect x="46" y="64" width="30" height="22" rx="4" fill="#EBF8FF"/>'
        '<rect x="84" y="64" width="30" height="22" rx="4" fill="#EBF8FF"/>'
        '<rect x="126" y="46" width="38" height="62" rx="9" fill="#1A365D"/>'
        '<circle cx="145" cy="66" r="7" fill="#F6AD55"/>'
        '<circle cx="68" cy="112" r="13" fill="#2D3748"/><circle cx="68" cy="112" r="5" fill="#A0AEC0"/>'
        '<circle cx="106" cy="112" r="13" fill="#2D3748"/><circle cx="106" cy="112" r="5" fill="#A0AEC0"/>'
        '<circle cx="145" cy="112" r="13" fill="#2D3748"/><circle cx="145" cy="112" r="5" fill="#A0AEC0"/>'),
    "bicycle": lambda: (
        '<circle cx="60" cy="100" r="26" fill="none" stroke="#2D3748" stroke-width="6"/>'
        '<circle cx="146" cy="100" r="26" fill="none" stroke="#2D3748" stroke-width="6"/>'
        '<path d="M60 100 l30 -42 l32 42 l-30 0z" fill="none" stroke="#E53E3E" stroke-width="6" '
        'stroke-linejoin="round"/>'
        '<path d="M90 58 h22 M102 58 l12 -12" stroke="#4A5568" stroke-width="6" '
        'stroke-linecap="round"/>'),

    # --- shapes -----------------------------------------------------------
    "circle": lambda: '<circle cx="100" cy="80" r="44" fill="#4299E1"/>',
    "square": lambda: '<rect x="56" y="36" width="88" height="88" rx="6" fill="#4299E1"/>',
    "triangle": lambda: '<path d="M100 34 l54 92 l-108 0z" fill="#4299E1"/>',
    "rectangle": lambda: '<rect x="34" y="52" width="132" height="56" rx="6" fill="#4299E1"/>',
    "star": lambda: f'<g fill="#DD6B20">{_star(100, 80, 50, 22)}</g>',

    # --- nature -----------------------------------------------------------
    "tree": lambda: (
        '<rect x="92" y="86" width="16" height="44" rx="4" fill="#7B341E"/>'
        '<circle cx="76" cy="72" r="28" fill="#2F855A"/>'
        '<circle cx="124" cy="72" r="28" fill="#38A169"/>'
        '<circle cx="100" cy="52" r="30" fill="#48BB78"/>'),
    "flower": lambda: (
        '<g fill="#ED8936">'
        '<circle cx="100" cy="46" r="18"/><circle cx="100" cy="110" r="18"/>'
        '<circle cx="72" cy="78" r="18"/><circle cx="128" cy="78" r="18"/>'
        '<circle cx="81" cy="59" r="18"/><circle cx="119" cy="59" r="18"/>'
        '<circle cx="81" cy="97" r="18"/><circle cx="119" cy="97" r="18"/></g>'
        '<circle cx="100" cy="78" r="17" fill="#F6AD55"/>'
        '<rect x="96" y="94" width="8" height="38" fill="#2F855A"/>'),
    "grass": lambda: (
        '<path d="M74 130 q4 -46 12 -66 q10 22 12 66z" fill="#38A169"/>'
        '<path d="M92 130 q-2 -58 8 -80 q12 26 8 80z" fill="#2F855A"/>'
        '<path d="M110 130 q2 -50 14 -68 q6 24 4 68z" fill="#48BB78"/>'
        '<rect x="52" y="128" width="96" height="10" rx="5" fill="#7B341E"/>'),

    # --- places -----------------------------------------------------------
    "shop": lambda: (
        '<rect x="46" y="72" width="108" height="58" rx="6" fill="#EDF2F7" stroke="#A0AEC0" stroke-width="3"/>'
        '<path d="M42 72 h116 l-8 -20 h-100z" fill="#DD6B20"/>'
        '<path d="M42 72 h116 l-2 10 h-112z" fill="#FFF5F5"/>'
        '<rect x="82" y="94" width="36" height="36" rx="4" fill="#2B6CB0"/>'),
    "school": lambda: (
        '<rect x="44" y="66" width="112" height="64" rx="6" fill="#EDF2F7" stroke="#A0AEC0" stroke-width="3"/>'
        '<path d="M100 34 v34" stroke="#4A5568" stroke-width="5" stroke-linecap="round"/>'
        '<path d="M100 34 l24 8 l-24 8z" fill="#C53030"/>'
        '<rect x="56" y="80" width="26" height="24" rx="3" fill="#90CDF4"/>'
        '<rect x="118" y="80" width="26" height="24" rx="3" fill="#90CDF4"/>'
        '<rect x="86" y="100" width="28" height="30" rx="3" fill="#7B341E"/>'),
    "hospital": lambda: (
        '<rect x="48" y="58" width="104" height="72" rx="8" fill="#FFFFFF" stroke="#A0AEC0" stroke-width="3"/>'
        '<rect x="92" y="72" width="16" height="40" fill="#C53030"/>'
        '<rect x="80" y="84" width="40" height="16" fill="#C53030"/>'
        '<rect x="60" y="116" width="80" height="14" rx="4" fill="#EDF2F7"/>'),
    "park": lambda: (
        '<rect x="90" y="72" width="14" height="58" rx="4" fill="#7B341E"/>'
        '<circle cx="76" cy="62" r="26" fill="#2F855A"/>'
        '<circle cx="118" cy="62" r="24" fill="#38A169"/>'
        '<rect x="36" y="112" width="46" height="10" rx="4" fill="#DD6B20"/>'
        '<rect x="36" y="122" width="46" height="8" rx="3" fill="#C05621"/>'
        '<rect x="40" y="96" width="7" height="18" fill="#4A5568"/>'
        '<rect x="72" y="96" width="7" height="18" fill="#4A5568"/>'),
}


def render(slug):
    """Return the full SVG document for one pictogram."""
    if slug not in PICTOGRAMS:
        raise KeyError(f"no pictogram for {slug!r}")
    body = PICTOGRAMS[slug]()
    return svg(body, slug.replace("_", " ").title())