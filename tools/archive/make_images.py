"""
Builds one SVG picture per listening question so a student can match the
picture to the answer instead of guessing from text alone.

Every picture is drawn here from scratch as plain SVG shapes, so there are no
external image files, no downloads and no licensing questions. Output:

    images/listening/<story-slug>-q<n>.svg
    images/index.json          -> "<activity>|||<n>": "images/listening/..."

Run:  python tools\\make_images.py
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from listening_content import LISTENING_STORIES  # noqa: E402

W, H = 240, 160
BG = "#F7FAFF"
INK = "#2D3748"

CLOTH = {"blue": "#2B6CB0", "red": "#C53030", "green": "#2F855A",
         "yellow": "#D69E2E", "purple": "#6B46C1", "grey": "#718096"}


def svg(body, caption=""):
    cap = ""
    if caption:
        cap = (f'<text x="{W/2}" y="{H-8}" text-anchor="middle" font-size="15" '
               f'font-weight="700" fill="{INK}" font-family="Segoe UI, Arial">{caption}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}">'
            f'<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>'
            f'{body}{cap}</svg>')


# --- people -------------------------------------------------------------
def person(hair="#4A5568", dress="#6B46C1", grey=False, glasses=False):
    hair_col = "#A0AEC0" if grey else hair
    g = (f'<circle cx="88" cy="66" r="6" fill="none" stroke="{INK}" stroke-width="2"/>'
         f'<circle cx="112" cy="66" r="6" fill="none" stroke="{INK}" stroke-width="2"/>'
         f'<path d="M94 66 h12" stroke="{INK}" stroke-width="2"/>') if glasses else ""
    bun = f'<circle cx="100" cy="26" r="9" fill="{hair_col}"/>' if grey else ""
    return (f'<circle cx="100" cy="52" r="22" fill="#FED7AA"/>'
            f'<path d="M78 48 a22 22 0 0 1 44 0 v-6 a22 22 0 0 0 -44 0z" fill="{hair_col}"/>{bun}'
            f'<rect x="74" y="78" width="52" height="46" rx="12" fill="{dress}"/>'
            f'<rect x="62" y="80" width="12" height="34" rx="6" fill="#FED7AA"/>'
            f'<rect x="126" y="80" width="12" height="34" rx="6" fill="#FED7AA"/>{g}')


P = {
    # --- objects ---------------------------------------------------------
    "lion": '<circle cx="120" cy="78" r="42" fill="#C05621"/>'
            '<circle cx="120" cy="82" r="30" fill="#F6AD55"/>'
            '<circle cx="110" cy="76" r="4.5" fill="#2D3748"/><circle cx="130" cy="76" r="4.5" fill="#2D3748"/>'
            '<path d="M112 92 h16 l-8 8z" fill="#2D3748"/>'
            '<path d="M104 100 q16 12 32 0" stroke="#2D3748" stroke-width="3" fill="none"/>',
    "apple": '<path d="M120 56 q-34 6 -34 40 t34 40 t34 -40 t-34 -40z" fill="#E53E3E"/>'
             '<path d="M120 56 q-2 -18 14 -22 q2 16 -14 22z" fill="#38A169"/>'
             '<rect x="118" y="34" width="5" height="26" rx="2" fill="#7B341E"/>'
             '<ellipse cx="102" cy="86" rx="7" ry="11" fill="#FFF5F5" opacity="0.55"/>',
    "bird": '<ellipse cx="116" cy="86" rx="34" ry="26" fill="#4299E1"/>'
            '<circle cx="146" cy="64" r="17" fill="#4299E1"/>'
            '<circle cx="152" cy="60" r="4" fill="#2D3748"/>'
            '<path d="M162 64 l16 6 l-16 6z" fill="#F6AD55"/>'
            '<path d="M104 84 q22 -14 40 4 q-22 12 -40 -4z" fill="#63B3ED"/>'
            '<path d="M96 108 l-10 14 M106 110 l-6 16" stroke="#F6AD55" stroke-width="4" stroke-linecap="round"/>',
    "hen_house": '<path d="M56 78 h128 v46 h-128z" fill="#B7791F"/>'
                 '<path d="M48 78 l72 -34 l72 34z" fill="#975A16"/>'
                 '<rect x="84" y="96" width="30" height="28" rx="4" fill="#5F370E"/>'
                 '<rect x="52" y="126" width="136" height="8" rx="4" fill="#8B5A2B"/>'
                 '<circle cx="158" cy="60" r="13" fill="#FFF5F5"/><circle cx="162" cy="57" r="3" fill="#2D3748"/>'
                 '<path d="M170 60 l10 4 l-10 4z" fill="#F6AD55"/>'
                 '<rect x="150" y="72" width="4" height="12" fill="#F6AD55"/>',
    "book": '<path d="M40 52 q40 -12 80 6 v66 q-40 -18 -80 -6z" fill="#4299E1"/>'
            '<path d="M200 52 q-40 -12 -80 6 v66 q40 -18 80 -6z" fill="#2B6CB0"/>'
            '<rect x="116" y="56" width="8" height="70" fill="#1A365D"/>'
            '<rect x="58" y="72" width="44" height="5" rx="2" fill="#EBF8FF"/>'
            '<rect x="58" y="86" width="34" height="5" rx="2" fill="#EBF8FF"/>',
    "bus": '<rect x="34" y="52" width="172" height="60" rx="12" fill="#C53030"/>'
           '<rect x="46" y="62" width="34" height="24" rx="5" fill="#EBF8FF"/>'
           '<rect x="90" y="62" width="34" height="24" rx="5" fill="#EBF8FF"/>'
           '<rect x="134" y="62" width="34" height="24" rx="5" fill="#EBF8FF"/>'
           '<rect x="178" y="62" width="18" height="24" rx="5" fill="#EBF8FF"/>'
           '<circle cx="76" cy="116" r="16" fill="#2D3748"/><circle cx="76" cy="116" r="6" fill="#A0AEC0"/>'
           '<circle cx="166" cy="116" r="16" fill="#2D3748"/><circle cx="166" cy="116" r="6" fill="#A0AEC0"/>',
    "basket": '<path d="M56 74 h128 l-14 52 h-100z" fill="#C05621"/>'
              '<path d="M70 74 q50 -46 100 0" stroke="#8B4513" stroke-width="6" fill="none"/>'
              '<path d="M66 92 h108 M74 108 h92" stroke="#8B4513" stroke-width="4" opacity="0.6"/>',
    "flower": '<g fill="#ED8936">'
              '<circle cx="120" cy="52" r="18"/><circle cx="120" cy="112" r="18"/>'
              '<circle cx="92" cy="82" r="18"/><circle cx="148" cy="82" r="18"/>'
              '<circle cx="101" cy="63" r="18"/><circle cx="139" cy="63" r="18"/>'
              '<circle cx="101" cy="101" r="18"/><circle cx="139" cy="101" r="18"/></g>'
              '<circle cx="120" cy="82" r="18" fill="#F6AD55"/>'
              '<rect x="116" y="98" width="8" height="42" fill="#2F855A"/>',
    "storm": '<path d="M70 88 a26 26 0 0 1 26 -26 a30 30 0 0 1 56 -6 a22 22 0 0 1 6 42 h-88z" fill="#A0AEC0"/>'
             '<path d="M84 100 l-6 18 M110 100 l-6 18 M136 100 l-6 18 M162 100 l-6 18" '
             'stroke="#4299E1" stroke-width="5" stroke-linecap="round"/>'
             '<path d="M60 132 q40 -16 84 -6" stroke="#7B341E" stroke-width="7" fill="none" stroke-linecap="round"/>'
             '<path d="M96 128 l-10 -22 M120 126 l-8 -24 M146 124 l-6 -20" stroke="#2F855A" stroke-width="5" stroke-linecap="round"/>',
    "tag": '<path d="M60 52 h74 l48 40 l-48 40 h-74z" fill="#DD6B20"/>'
           '<circle cx="86" cy="92" r="10" fill="#FFF5F5"/>'
           '<path d="M108 84 h56 M108 100 h40" stroke="#FFF5F5" stroke-width="6" stroke-linecap="round"/>',
    "bell": '<path d="M88 108 q0 -46 32 -46 t32 46z" fill="#D69E2E"/>'
            '<rect x="78" y="108" width="84" height="12" rx="6" fill="#B7791F"/>'
            '<circle cx="120" cy="128" r="9" fill="#B7791F"/>'
            '<path d="M62 74 a34 34 0 0 0 0 40 M178 74 a34 34 0 0 1 0 40" stroke="#D69E2E" '
            'stroke-width="5" fill="none" stroke-linecap="round"/>',
    "blanket": '<rect x="52" y="86" width="136" height="20" rx="7" fill="#4299E1"/>'
               '<rect x="60" y="66" width="120" height="20" rx="7" fill="#63B3ED"/>'
               '<rect x="68" y="46" width="104" height="20" rx="7" fill="#90CDF4"/>'
               '<path d="M52 106 h136" stroke="#2B6CB0" stroke-width="4"/>',
    "backpack": '<rect x="62" y="48" width="116" height="88" rx="20" fill="#2F855A"/>'
                '<rect x="84" y="84" width="72" height="52" rx="10" fill="#38A169"/>'
                '<path d="M100 48 q20 -22 40 0" stroke="#276749" stroke-width="7" fill="none"/>'
                '<rect x="104" y="96" width="32" height="10" rx="5" fill="#9AE6B4"/>',
    "geometry_box": '<rect x="44" y="66" width="152" height="72" rx="12" fill="#805AD5"/>'
                    '<rect x="44" y="58" width="152" height="20" rx="9" fill="#6B46C1"/>'
                    '<circle cx="84" cy="100" r="16" fill="#FAF5FF"/>'
                    '<rect x="108" y="86" width="30" height="28" fill="#FAF5FF"/>'
                    '<path d="M156 114 l16 -30 l16 30z" fill="#FAF5FF"/>',
    "runner": '<circle cx="150" cy="40" r="15" fill="#FED7AA"/>'
              '<path d="M146 60 l-28 22 l20 10 l-16 32" stroke="#2B6CB0" stroke-width="11" '
              'stroke-linecap="round" fill="none"/>'
              '<path d="M148 62 l26 14" stroke="#2B6CB0" stroke-width="11" stroke-linecap="round"/>'
              '<path d="M132 78 l-30 2" stroke="#2B6CB0" stroke-width="10" stroke-linecap="round"/>'
              '<path d="M40 96 h44 M28 116 h40 M44 76 h32" stroke="#A0AEC0" stroke-width="6" stroke-linecap="round"/>',
    "paper_fold": '<path d="M64 40 h84 l30 34 v52 h-114z" fill="#EDF2F7" stroke="#A0AEC0" stroke-width="3"/>'
                  '<path d="M148 40 v34 h30" fill="#CBD5E0"/>'
                  '<path d="M84 40 v34 h-20z" fill="#E2E8F0"/>'
                  '<path d="M78 122 q34 -22 62 0" stroke="#2B6CB0" stroke-width="5" fill="none" stroke-dasharray="8 7"/>'
                  '<path d="M140 114 l12 10 l-14 6z" fill="#2B6CB0"/>',
    "triangle": '<path d="M120 44 l72 84 h-144z" fill="#DD6B20"/>'
                '<path d="M120 44 l72 84 h-144z" fill="none" stroke="#9C4221" stroke-width="6"/>',
    "calendar": '<rect x="46" y="46" width="148" height="94" rx="12" fill="#FFFFFF" stroke="#A0AEC0" stroke-width="3"/>'
                '<rect x="46" y="46" width="148" height="28" rx="12" fill="#C53030"/>'
                '<rect x="70" y="34" width="10" height="24" rx="5" fill="#7B341E"/>'
                '<rect x="160" y="34" width="10" height="24" rx="5" fill="#7B341E"/>'
                '<circle cx="120" cy="102" r="18" fill="#C53030"/>',
    "lab": '<path d="M104 40 v40 l-38 56 a10 10 0 0 0 8 16 h92 a10 10 0 0 0 8 -16 l-38 -56 v-40z" '
           'fill="#E2E8F0" stroke="#718096" stroke-width="4"/>'
           '<rect x="96" y="32" width="48" height="12" rx="6" fill="#4A5568"/>'
           '<path d="M84 116 h72 l24 36 h-120z" fill="#63B3ED" opacity="0.85"/>'
           '<circle cx="104" cy="126" r="6" fill="#EBF8FF"/><circle cx="136" cy="134" r="5" fill="#EBF8FF"/>',
    "compost": '<path d="M62 62 h116 l-12 76 h-92z" fill="#7B341E"/>'
               '<rect x="56" y="50" width="128" height="16" rx="8" fill="#975A16"/>'
               '<path d="M92 62 q6 -30 28 -34 q2 26 -28 34z" fill="#38A169"/>'
               '<path d="M124 62 q4 -24 24 -28 q2 22 -24 28z" fill="#48BB78"/>'
               '<circle cx="120" cy="104" r="14" fill="#9AE6B4"/>',
    "watering_can": '<rect x="62" y="66" width="76" height="62" rx="12" fill="#2B6CB0"/>'
                    '<path d="M138 82 h34 l16 -22" stroke="#2B6CB0" stroke-width="12" fill="none" stroke-linecap="round"/>'
                    '<circle cx="190" cy="56" r="14" fill="#4299E1"/>'
                    '<path d="M84 66 q-14 -26 12 -26 t12 26" stroke="#2B6CB0" stroke-width="8" fill="none"/>'
                    '<path d="M182 74 q6 12 0 20 M196 70 q8 14 0 24" stroke="#4299E1" stroke-width="5" fill="none" stroke-linecap="round"/>',
    "wire": '<path d="M40 96 q50 -34 100 0 t60 -6" stroke="#718096" stroke-width="7" fill="none"/>'
            '<circle cx="128" cy="80" r="16" fill="#FED7AA"/>'
            '<path d="M120 62 l-8 -16 M136 62 l8 -16" stroke="#FED7AA" stroke-width="8" stroke-linecap="round"/>'
            '<path d="M56 52 l14 10 l-16 8z" fill="#C53030"/>',
    "cup": '<path d="M76 56 h74 l-10 74 h-54z" fill="#FFFFFF" stroke="#2B6CB0" stroke-width="5"/>'
           '<path d="M84 100 h58 l-4 28 h-50z" fill="#90CDF4"/>'
           '<path d="M152 74 q26 0 26 20 t-26 20" stroke="#2B6CB0" stroke-width="5" fill="none"/>',
    "speech": '<path d="M40 60 h160 v64 h-84 l-30 26 v-26 h-46z" fill="#4299E1"/>'
              '<circle cx="84" cy="92" r="7" fill="#EBF8FF"/><circle cx="120" cy="92" r="7" fill="#EBF8FF"/>'
              '<circle cx="156" cy="92" r="7" fill="#EBF8FF"/>'
              '<path d="M84 132 q36 20 72 0" stroke="#4299E1" stroke-width="6" fill="none"/>',
    "platform": '<rect x="34" y="44" width="172" height="92" rx="12" fill="#2D3748"/>'
                '<circle cx="120" cy="90" r="34" fill="#FFFFFF"/>'
                '<rect x="150" y="118" width="56" height="18" rx="6" fill="#F6AD55"/>',
    "money": '<rect x="40" y="60" width="160" height="60" rx="8" fill="#38A169"/>'
             '<circle cx="120" cy="90" r="22" fill="#9AE6B4"/>'
             '<path d="M110 90 h20 M120 80 v20" stroke="#276749" stroke-width="5" stroke-linecap="round"/>',
    "measuring": '<path d="M88 40 h48 v92 a10 10 0 0 1 -10 10 h-28 a10 10 0 0 1 -10 -10z" fill="#EBF8FF" stroke="#2B6CB0" stroke-width="5"/>'
                 '<path d="M92 112 h40 v18 a10 10 0 0 1 -10 10 h-20 a10 10 0 0 1 -10 -10z" fill="#63B3ED"/>'
                 '<path d="M100 60 h18 M100 78 h26 M100 96 h18" stroke="#2B6CB0" stroke-width="4"/>',
    "dropper": '<rect x="112" y="34" width="20" height="46" rx="8" fill="#A0AEC0"/>'
               '<rect x="106" y="76" width="32" height="40" rx="6" fill="#E2E8F0" stroke="#718096" stroke-width="3"/>'
               '<path d="M122 116 v14" stroke="#4299E1" stroke-width="4"/>'
               '<path d="M122 138 q10 12 0 18 q-10 -6 0 -18z" fill="#4299E1"/>',
    "chart": '<rect x="44" y="42" width="152" height="92" rx="10" fill="#FFFFFF" stroke="#A0AEC0" stroke-width="3"/>'
             '<circle cx="80" cy="76" r="16" fill="#E53E3E"/><circle cx="120" cy="76" r="16" fill="#4299E1"/>'
             '<circle cx="160" cy="76" r="16" fill="#38A169"/><circle cx="80" cy="114" r="16" fill="#F6AD55"/>'
             '<circle cx="120" cy="114" r="16" fill="#805AD5"/>',
    "shells": '<path d="M52 122 q4 -46 34 -46 t34 46z" fill="#F6AD55"/>'
              '<path d="M52 122 q16 -18 34 0" stroke="#C05621" stroke-width="4" fill="none"/>'
              '<path d="M120 122 q4 -40 30 -40 t30 40z" fill="#F687B3"/>'
              '<path d="M120 122 q14 -16 30 0" stroke="#B83280" stroke-width="4" fill="none"/>'
              '<path d="M92 126 h56" stroke="#A0AEC0" stroke-width="5" stroke-linecap="round"/>',
    "mouth": '<path d="M56 78 q64 -46 128 0 q-64 46 -128 0z" fill="#C53030"/>'
             '<path d="M64 78 h112" stroke="#7B341E" stroke-width="4"/>'
             '<path d="M100 78 q20 -20 40 0 q-20 20 -40 0z" fill="#FED7AA"/>'
             '<path d="M40 60 l-14 -10 M40 96 l-14 10 M200 60 l14 -10 M200 96 l14 10" stroke="#A0AEC0" stroke-width="5" stroke-linecap="round"/>',
    "coconut": '<circle cx="120" cy="94" r="42" fill="#8B5A2B"/>'
                '<circle cx="106" cy="82" r="5" fill="#4A5568"/><circle cx="134" cy="82" r="5" fill="#4A5568"/>'
                '<circle cx="106" cy="106" r="5" fill="#4A5568"/><circle cx="134" cy="106" r="5" fill="#4A5568"/>'
                '<path d="M104 58 l18 -30" stroke="#E53E3E" stroke-width="8" stroke-linecap="round"/>',
    "bottle": '<path d="M104 34 h32 v22 l16 20 v56 a10 10 0 0 1 -10 10 h-44 a10 10 0 0 1 -10 -10 v-56 l16 -20z" '
              'fill="#EBF8FF" stroke="#2B6CB0" stroke-width="5"/>'
              '<rect x="100" y="28" width="40" height="12" rx="5" fill="#2B6CB0"/>',
    "jars": '<rect x="40" y="70" width="42" height="60" rx="8" fill="#EDF2F7" stroke="#718096" stroke-width="4"/>'
            '<rect x="40" y="62" width="42" height="12" rx="5" fill="#A0AEC0"/>'
            '<rect x="99" y="70" width="42" height="60" rx="8" fill="#EDF2F7" stroke="#718096" stroke-width="4"/>'
            '<rect x="99" y="62" width="42" height="12" rx="5" fill="#A0AEC0"/>'
            '<rect x="158" y="70" width="42" height="60" rx="8" fill="#EDF2F7" stroke="#718096" stroke-width="4"/>'
            '<rect x="158" y="62" width="42" height="12" rx="5" fill="#A0AEC0"/>',
    "gate": '<rect x="36" y="70" width="168" height="62" rx="10" fill="#4A5568"/>'
            '<rect x="52" y="34" width="26" height="110" rx="8" fill="#2D3748"/>'
            '<rect x="162" y="34" width="26" height="110" rx="8" fill="#2D3748"/>'
            '<rect x="78" y="88" width="84" height="12" rx="6" fill="#A0AEC0"/>'
            '<rect x="78" y="108" width="84" height="12" rx="6" fill="#A0AEC0"/>',
    "bell_count": None,   # built below
}


def clock(hour):
    import math
    a = math.radians((hour % 12) / 12 * 360 - 90)
    x, y = 120 + 46 * math.cos(a), 88 + 46 * math.sin(a)
    return (f'<circle cx="120" cy="88" r="56" fill="#FFFFFF" stroke="#2D3748" stroke-width="6"/>'
            f'<circle cx="120" cy="88" r="6" fill="#2D3748"/>'
            f'<path d="M120 88 L120 54" stroke="#2D3748" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M120 88 L{x:.1f} {y:.1f}" stroke="#C53030" stroke-width="5" stroke-linecap="round"/>'
            + "".join(f'<circle cx="{120+50*math.sin(i*math.pi/6):.1f}" cy="{88-50*math.cos(i*math.pi/6):.1f}" r="3" fill="#A0AEC0"/>' for i in range(12)))


def numerals(items, color="#4299E1", per_row=5):
    out, n = [], len(items)
    for i in range(n):
        r, c = divmod(i, per_row)
        x = 40 + c * (160 / max(per_row, n)) + (160 / max(per_row, n)) / 2
        y = 60 + r * 56
        out.append(f'<circle cx="{x:.0f}" cy="{y}" r="19" fill="{color}"/>')
    return "".join(out)


# Answer text -> (pictogram, caption).  Every one of the 72 answers is listed.
SCENES = {
    "A lion": ("lion", None), "Apple": ("apple", None),
    "At the bird house": ("hen_house", None),
    "Open the book to page five": ("book", "page 5"),
    "Blue": ("swatch", None), "A red bus": ("bus", None),
    "The first basket": ("basket", "1st"), "Three": ("numerals", None),
    "A flower": ("flower", None), "A bird": ("bird", None),
    "A storm broke the branch": ("storm", None), "Nana": ("nana", None),
    "In the back hall": ("hall", "BACK"), "Eight o'clock": ("clock8", None),
    "Label them with name and class": ("tag", "name + class"),
    "A bus hissing": ("bus", "hiss"), "Twice": ("numerals2", None),
    "His mother": ("mother", None), "Folds": ("blanket", "fold"),
    "Pack her bag": ("backpack", None), "She packs her bag": ("backpack", None),
    "Nine o'clock": ("clock9", None), "The dancing contest": ("dancing", None),
    "A geometry box": ("geometry_box", None), "An adverb": ("runner", "how?"),
    "Imran": ("boy", None), "Fold the paper in half the long way": ("paper_fold", None),
    "Last of all": ("last", None), "A triangle": ("triangle", None),
    "At ten o'clock": ("clock10", None), "On Monday": ("calendar", "MON"),
    "On the second floor": ("floors", "2nd floor"),
    "To the laboratory on the first floor": ("lab2", None),
    "Forty": ("num40", None), "About 900 jars": ("jars", None),
    "In straw": ("straw", None), "Saved": ("money", "saved"),
    "Two": ("numerals2", None), "It describes the girl": ("girl", None),
    "At six o'clock": ("clock6", None), "Three bottles and two lids": ("bottles", None),
    "Four": ("num4", None), "Compost": ("compost", None),
    "The watering": ("watering_can", None), "The first": ("first", None),
    "Jump three times": ("jump3", None), "From ten": ("fromten", None),
    "He plucked the wire": ("wire", None),
    "The cup jumped much higher": ("cup_high", None),
    "The cup hardly moved": ("cup_low", None),
    "SHED yool": ("letters", "shed / yool"),
    "They say it aloud both ways": ("speech", None),
    "Platform four": ("platform4", None), "7:25 in the evening": ("clock725", None),
    "S seven and S eight": ("letters2", "S7 S8"),
    "Four crore rupees": ("money4", None), "Twenty-two": ("num22", None),
    "Five millilitres": ("measuring5", None), "Two drops": ("drops2", None),
    "Colours are compared with the chart": ("chart", None),
    "She sells seashells by the seashore": ("shells", None),
    "They use different mouth movements": ("mouth", None),
    "Coconut water": ("coconut", None), "A free glass bottle": ("bottle", None),
    "The first one hundred": ("hundred", None),
}


def build(kind, caption):
    if kind == "swatch":
        return svg(f'<rect x="56" y="42" width="128" height="88" rx="14" fill="{CLOTH["blue"]}"/>'
                   f'<path d="M76 62 l-24 26 M76 100 l-44 0" stroke="#FFF" stroke-width="6" opacity="0.5"/>',
                   "BLUE")
    if kind.startswith("clock"):
        h = {"clock8": 8, "clock9": 9, "clock10": 10, "clock6": 6, "clock725": 7}[kind]
        extra = ('<text x="120" y="26" text-anchor="middle" font-size="17" font-weight="800" fill="#2D3748" font-family="Segoe UI, Arial">7:25 PM</text>'
                 if kind == "clock725" else "")
        return svg(clock(h) + extra)
    if kind == "numerals":
        return svg(numerals(list(range(3)), "#4299E1"), "3")
    if kind == "numerals2":
        return svg(numerals(list(range(2)), "#38A169"), "2")
    if kind == "num4":
        return svg(numerals(list(range(4)), "#805AD5", per_row=4), "4")
    if kind == "num40":
        return svg('<rect x="46" y="46" width="148" height="76" rx="12" fill="#DD6B20"/>'
                   '<text x="120" y="102" text-anchor="middle" font-size="52" font-weight="800" fill="#FFF" font-family="Segoe UI, Arial">40</text>',
                   "forty")
    if kind == "num22":
        return svg('<rect x="46" y="46" width="148" height="76" rx="12" fill="#2F855A"/>'
                   '<text x="120" y="102" text-anchor="middle" font-size="52" font-weight="800" fill="#FFF" font-family="Segoe UI, Arial">22</text>',
                   "twenty-two")
    if kind == "hundred":
        return svg('<rect x="42" y="46" width="156" height="76" rx="12" fill="#2B6CB0"/>'
                   '<text x="120" y="102" text-anchor="middle" font-size="48" font-weight="800" fill="#FFF" font-family="Segoe UI, Arial">100</text>',
                   "the first 100")
    if kind == "money4":
        return svg(P["money"] + '<text x="120" y="34" text-anchor="middle" font-size="17" font-weight="800" fill="#2D3748" font-family="Segoe UI, Arial">4 crore</text>')
    if kind == "boy":
        return svg(person(hair="#4A5568", dress="#3182CE"))
    if kind == "girl":
        return svg(person(hair="#975A16", dress="#D53F8C"))
    if kind == "mother":
        return svg(person(hair="#2D3748", dress="#DD6B20"))
    if kind == "nana":
        return svg(person(grey=True, dress="#805AD5", glasses=True), "Nana")
    if kind == "hall":
        return svg('<rect x="40" y="46" width="160" height="88" rx="10" fill="#CBD5E0"/>'
                   '<rect x="40" y="46" width="160" height="26" rx="10" fill="#718096"/>'
                   '<rect x="56" y="92" width="30" height="42" rx="5" fill="#2D3748"/>'
                   '<rect x="154" y="92" width="30" height="42" rx="5" fill="#2D3748"/>'
                   '<rect x="100" y="60" width="40" height="22" rx="6" fill="#F6AD55"/>'
                   '<text x="120" y="77" text-anchor="middle" font-size="14" font-weight="800" fill="#2D3748" font-family="Segoe UI, Arial">BACK</text>')
    if kind == "floors":
        return svg('<rect x="58" y="30" width="124" height="106" rx="8" fill="#EDF2F7" stroke="#4A5568" stroke-width="4"/>'
                   + "".join(f'<rect x="70" y="{40+i*30}" width="100" height="22" rx="4" fill="{"#F6AD55" if i==1 else "#CBD5E0"}"/>' for i in range(3))
                   + '<text x="120" y="57" text-anchor="middle" font-size="13" font-weight="800" fill="#2D3748" font-family="Segoe UI, Arial">2nd</text>')
    if kind == "lab2":
        return svg(P["lab"] + '<rect x="140" y="34" width="60" height="26" rx="6" fill="#2B6CB0"/>'
                   '<text x="170" y="52" text-anchor="middle" font-size="13" font-weight="800" fill="#FFF" font-family="Segoe UI, Arial">1st floor</text>')
    if kind == "first":
        return svg('<circle cx="60" cy="82" r="22" fill="#38A169"/>'
                   '<text x="60" y="91" text-anchor="middle" font-size="24" font-weight="800" fill="#FFF" font-family="Segoe UI, Arial">1</text>'
                   + "".join(f'<circle cx="{118+i*34}" cy="82" r="22" fill="#CBD5E0"/>' for i in range(3))
                   + '<path d="M38 118 h164" stroke="#A0AEC0" stroke-width="5" stroke-linecap="round"/>', "FIRST")
    if kind == "dancing":
        return svg('<circle cx="84" cy="52" r="17" fill="#FED7AA"/>'
                   '<path d="M84 74 l-16 30 l22 12" stroke="#C53030" stroke-width="11" stroke-linecap="round" fill="none"/>'
                   '<path d="M86 74 l22 26" stroke="#C53030" stroke-width="11" stroke-linecap="round"/>'
                   '<circle cx="156" cy="52" r="17" fill="#FED7AA"/>'
                   '<path d="M156 74 l18 28 l-22 14" stroke="#6B46C1" stroke-width="11" stroke-linecap="round" fill="none"/>'
                   '<path d="M154 74 l-22 26" stroke="#6B46C1" stroke-width="11" stroke-linecap="round"/>'
                   '<circle cx="206" cy="44" r="6" fill="#2B6CB0"/><circle cx="216" cy="62" r="6" fill="#2B6CB0"/>')
    if kind == "jump3":
        return svg('<circle cx="86" cy="46" r="15" fill="#FED7AA"/>'
                   '<path d="M86 66 v34 M86 74 l-24 -12 M86 74 l24 -14 M86 100 l-20 26 M86 100 l20 26" '
                   'stroke="#2F855A" stroke-width="10" stroke-linecap="round" fill="none"/>'
                   '<path d="M40 130 h160" stroke="#A0AEC0" stroke-width="5"/>'
                   '<text x="170" y="60" text-anchor="middle" font-size="34" font-weight="800" fill="#2F855A" font-family="Segoe UI, Arial">x3</text>')
    if kind == "fromten":
        return svg('<rect x="46" y="52" width="60" height="60" rx="10" fill="#2B6CB0"/>'
                   '<text x="76" y="93" text-anchor="middle" font-size="34" font-weight="800" fill="#FFF" font-family="Segoe UI, Arial">10</text>'
                   '<path d="M114 82 h34" stroke="#C53030" stroke-width="6" marker-end="url(#a)"/>'
                   '<path d="M156 82 h40" stroke="#C53030" stroke-width="6" stroke-dasharray="8 8"/>'
                   '<text x="120" y="136" text-anchor="middle" font-size="18" font-weight="700" fill="#2D3748" font-family="Segoe UI, Arial">to the next ten</text>')
    if kind == "cup_high" or kind == "cup_low":
        up = kind == "cup_high"
        arr = "M74 44 v-24 m0 0 l-8 10 m8 -10 l8 10" if up else "M74 44 v24 m0 0 l-8 -10 m8 10 l8 -10"
        return svg(P["cup"] + f'<path d="{arr}" stroke="#38A169" stroke-width="6" fill="none" stroke-linecap="round"/>',
                   "jumped higher" if up else "hardly moved")
    if kind == "letters":
        return svg("".join(f'<rect x="{44+i*44}" y="52" width="38" height="52" rx="8" fill="#4299E1"/>'
                           f'<text x="{63+i*44}" y="88" text-anchor="middle" font-size="28" font-weight="800" fill="#FFF" font-family="Segoe UI, Arial">{c}</text>'
                           for i, c in enumerate("SHED")))
    if kind == "letters2":
        return svg('<rect x="40" y="48" width="66" height="60" rx="10" fill="#2F855A"/>'
                   '<text x="73" y="90" text-anchor="middle" font-size="38" font-weight="800" fill="#FFF" font-family="Segoe UI, Arial">S7</text>'
                   '<rect x="134" y="48" width="66" height="60" rx="10" fill="#2B6CB0"/>'
                   '<text x="167" y="90" text-anchor="middle" font-size="38" font-weight="800" fill="#FFF" font-family="Segoe UI, Arial">S8</text>',
                   "/s/")
    if kind == "platform4":
        return svg(P["platform"] + '<text x="120" y="104" text-anchor="middle" font-size="44" font-weight="800" fill="#2D3748" font-family="Segoe UI, Arial">4</text>'
                   '<text x="178" y="132" text-anchor="middle" font-size="15" font-weight="700" fill="#7B341E" font-family="Segoe UI, Arial">PLATFORM</text>')
    if kind == "measuring5":
        return svg(P["measuring"] + '<text x="164" y="60" text-anchor="middle" font-size="20" font-weight="800" fill="#2D3748" font-family="Segoe UI, Arial">5 mL</text>')
    if kind == "drops2":
        return svg(P["dropper"] + "".join(f'<path d="M122 {142+i*10} q10 12 0 18 q-10 -6 0 -18z" fill="#4299E1"/>' for i in range(2)), "2 drops")
    if kind == "bottles":
        return svg("".join(f'<rect x="{44+i*38}" y="72" width="30" height="52" rx="7" fill="#EBF8FF" stroke="#2B6CB0" stroke-width="4"/>'
                           f'<rect x="{48+i*38}" y="62" width="22" height="12" rx="4" fill="#2B6CB0"/>' for i in range(3))
                   + "".join(f'<rect x="{150+i*30}" y="44" width="24" height="10" rx="4" fill="#A0AEC0"/>' for i in range(2)),
                   "3 bottles  2 lids")
    if kind == "straw":
        return svg('<path d="M92 34 l34 78" stroke="#E53E3E" stroke-width="9" stroke-linecap="round"/>'
                   '<path d="M74 84 h92 l-10 52 h-72z" fill="#EBF8FF" stroke="#2B6CB0" stroke-width="4"/>'
                   '<path d="M82 106 h72 l-6 30 h-60z" fill="#90CDF4"/>')
    if kind == "coconut":
        return svg(P["coconut"])
    if kind == "bottle":
        return svg(P["bottle"] + '<text x="120" y="34" text-anchor="middle" font-size="17" font-weight="800" fill="#2F855A" font-family="Segoe UI, Arial">FREE</text>')
    if kind == "last":
        return svg("".join(f'<circle cx="{46+i*40}" cy="80" r="17" fill="{"#38A169" if i<3 else "#CBD5E0"}"/>' for i in range(4))
                   + '<path d="M186 80 h26" stroke="#C53030" stroke-width="6"/>'
                     '<path d="M212 80 l-12 -10 v20z" fill="#C53030"/>', "LAST")
    return svg(P[kind], caption)


def slugify(name):
    out = "".join(c if c.isalnum() else "-" for c in name.lower())
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def main():
    out_dir = os.path.join(ROOT, "images", "listening")
    os.makedirs(out_dir, exist_ok=True)
    index, missing = {}, []

    for name, entry in LISTENING_STORIES.items():
        slug = slugify(name)
        for i, q in enumerate(entry["questions"]):
            key = q["answer"]
            if key not in SCENES:
                missing.append((name, i, key))
                continue
            kind, caption = SCENES[key]
            path = os.path.join(out_dir, f"{slug}-q{i}.svg")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(build(kind, caption))
            index[f"{name}|||{i}"] = f"images/listening/{slug}-q{i}.svg"

    meta = {"canvas": [W, H], "count": len(index), "items": index}
    with open(os.path.join(ROOT, "images", "index.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)

    print(f"images written : {len(index)}")
    print(f"unmapped       : {len(missing)}")
    for m in missing:
        print("   -", m)


if __name__ == "__main__":
    main()