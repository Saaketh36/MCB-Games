"""
AI Helper for MyClassboard Games Platform.
Provides AI-powered automatic game, quiz, and task generation for Teachers.
Integrates with Google Gemini API (gemini-3.8-flash / gemini-3.7-flash / gemini-3.5-flash) with an
intelligent, curriculum-aware offline fallback engine.
"""

import os
import json
import re
import random
import logging
import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("ai_helper")

# =====================================================================
# 1. LIVE GEMINI GENERATION
# =====================================================================

def call_gemini_api(prompt_text, api_key=None):
    """
    Call Google Gemini API with fallback across current model versions:
    gemini-3.8-flash, gemini-3.7-flash, gemini-3.5-flash, gemini-flash-latest
    """
    key = (api_key or "").strip() or os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return None, "No API Key provided"

    # Fast, ultra-reliable models available on v1beta
    models = [
        "gemini-flash-lite-latest",
        "gemini-3.1-flash-lite",
        "gemini-flash-latest",
        "gemini-3.8-flash",
        "gemini-3.5-flash"
    ]
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "MCB-Games/1.0"
    }
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {
            "temperature": 0.7
        }
    }

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=20)
            if resp.status_code == 200:
                res_data = resp.json()
                text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
                
                # Strip markdown fencing if present
                text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.MULTILINE)
                text = re.sub(r'\s*```$', '', text, flags=re.MULTILINE)
                text = text.strip()
                
                # Find outermost JSON bounds { ... }
                start_idx = text.find('{')
                end_idx = text.rfind('}')
                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    text = text[start_idx:end_idx+1]

                parsed = json.loads(text)
                return parsed, f"✨ Google Gemini AI ({model})"
            else:
                logger.warning(f"Gemini {model} returned HTTP {resp.status_code}: {resp.text[:120]}")
        except Exception as e:
            logger.warning(f"Gemini call to {model} failed: {e}")
            continue

    return None, "Gemini API unavailable or invalid key"


# =====================================================================
# MULTI-MODAL VISUAL ASSETS (SVG DIAGRAMS & VISUAL EMOJI CLUES)
# =====================================================================

TOPIC_SVG_LIBRARY = {
    "electricity": """<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="max-height:120px;width:auto;"><rect width="200" height="120" rx="14" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/><rect x="25" y="45" width="35" height="30" rx="6" fill="#4f46e5"/><rect x="60" y="52" width="6" height="16" rx="2" fill="#818cf8"/><text x="32" y="66" fill="#ffffff" font-size="12" font-weight="bold">+</text><text x="47" y="66" fill="#ffffff" font-size="12" font-weight="bold">-</text><text x="24" y="90" fill="#475569" font-size="9" font-weight="bold">Battery</text><path d="M 66 60 L 100 60 L 115 35" fill="none" stroke="#f59e0b" stroke-width="3" stroke-linecap="round"/><path d="M 125 45 L 140 60 L 150 60" fill="none" stroke="#f59e0b" stroke-width="3" stroke-linecap="round"/><path d="M 150 60 L 150 95 L 42 95 L 42 75" fill="none" stroke="#f59e0b" stroke-width="3" stroke-linecap="round"/><circle cx="115" cy="35" r="4" fill="#475569"/><line x1="115" y1="35" x2="130" y2="28" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/><circle cx="130" cy="45" r="4" fill="#475569"/><text x="106" y="20" fill="#dc2626" font-size="9" font-weight="bold">Switch</text><circle cx="150" cy="60" r="14" fill="#fef08a" stroke="#eab308" stroke-width="2"/><path d="M 144 74 L 156 74" stroke="#64748b" stroke-width="3"/><path d="M 146 78 L 154 78" stroke="#64748b" stroke-width="2"/><text x="136" y="108" fill="#ca8a04" font-size="9" font-weight="bold">Bulb 💡</text></svg>""",

    "magnet": """<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="max-height:120px;width:auto;"><rect width="200" height="120" rx="14" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/><rect x="40" y="44" width="60" height="32" rx="4" fill="#ef4444"/><rect x="100" y="44" width="60" height="32" rx="4" fill="#3b82f6"/><text x="63" y="66" fill="#ffffff" font-size="16" font-weight="bold">N</text><text x="123" y="66" fill="#ffffff" font-size="16" font-weight="bold">S</text><path d="M 40 48 C 10 20, 10 100, 40 74" fill="none" stroke="#a855f7" stroke-width="2" stroke-dasharray="4,4"/><path d="M 160 48 C 190 20, 190 100, 160 74" fill="none" stroke="#a855f7" stroke-width="2" stroke-dasharray="4,4"/><text x="56" y="98" fill="#6d28d9" font-size="9.5" font-weight="bold">Magnetic Poles (N ➔ S)</text></svg>""",

    "plants": """<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="max-height:120px;width:auto;"><rect width="200" height="120" rx="14" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="2"/><circle cx="32" cy="28" r="13" fill="#facc15"/><rect x="20" y="85" width="160" height="25" rx="6" fill="#78350f"/><text x="28" y="100" fill="#fef3c7" font-size="9" font-weight="bold">Soil & Roots</text><path d="M 100 85 Q 90 95 85 105 M 100 85 Q 105 95 110 105" stroke="#d97706" stroke-width="2.5" fill="none"/><path d="M 100 85 L 100 38" stroke="#16a34a" stroke-width="4" stroke-linecap="round"/><path d="M 100 62 Q 75 55 72 65 Q 85 75 100 68" fill="#22c55e"/><path d="M 100 52 Q 125 45 128 55 Q 115 65 100 58" fill="#22c55e"/><circle cx="100" cy="35" r="12" fill="#ec4899"/><circle cx="100" cy="35" r="5" fill="#facc15"/><text x="122" y="38" fill="#15803d" font-size="9" font-weight="bold">Flower 🌸</text></svg>""",

    "solar system": """<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="max-height:120px;width:auto;"><rect width="200" height="120" rx="14" fill="#0f172a" stroke="#334155" stroke-width="2"/><circle cx="30" cy="60" r="22" fill="#f59e0b"/><ellipse cx="30" cy="60" rx="75" ry="34" fill="none" stroke="#475569" stroke-width="1" stroke-dasharray="3,3"/><ellipse cx="30" cy="60" rx="125" ry="46" fill="none" stroke="#475569" stroke-width="1" stroke-dasharray="3,3"/><circle cx="105" cy="60" r="7" fill="#0284c7"/><circle cx="107" cy="59" r="3" fill="#22c55e"/><circle cx="155" cy="60" r="5" fill="#ef4444"/><text x="18" y="100" fill="#fbbf24" font-size="9" font-weight="bold">Sun ☀️</text><text x="94" y="80" fill="#38bdf8" font-size="8.5" font-weight="bold">Earth 🌍</text><text x="146" y="80" fill="#f87171" font-size="8.5" font-weight="bold">Mars 🔴</text></svg>""",

    "water": """<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="max-height:120px;width:auto;"><rect width="200" height="120" rx="14" fill="#f0f9ff" stroke="#bae6fd" stroke-width="2"/><circle cx="30" cy="28" r="13" fill="#f59e0b"/><path d="M 120 30 Q 130 18 145 22 Q 160 18 165 30 Q 175 35 170 45 Q 160 52 130 52 Q 115 48 120 30" fill="#93c5fd" stroke="#60a5fa" stroke-width="1.5"/><line x1="130" y1="58" x2="126" y2="68" stroke="#0284c7" stroke-width="2" stroke-linecap="round"/><line x1="145" y1="58" x2="141" y2="68" stroke="#0284c7" stroke-width="2" stroke-linecap="round"/><line x1="160" y1="58" x2="156" y2="68" stroke="#0284c7" stroke-width="2" stroke-linecap="round"/><path d="M 20 95 Q 55 90 90 95 Q 125 100 160 95 L 180 95 L 180 115 L 20 115 Z" fill="#38bdf8"/><path d="M 60 85 Q 65 65 60 50" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="3,3"/><text x="24" y="70" fill="#b45309" font-size="8.5" font-weight="bold">Evaporation ↑</text><text x="120" y="80" fill="#0369a1" font-size="8.5" font-weight="bold">Precipitation ↓</text></svg>""",

    "fractions": """<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="max-height:120px;width:auto;"><rect width="200" height="120" rx="14" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/><circle cx="65" cy="60" r="36" fill="#e0e7ff" stroke="#6366f1" stroke-width="2"/><path d="M 65 60 L 65 24 A 36 36 0 0 1 101 60 Z" fill="#6366f1"/><line x1="29" y1="60" x2="101" y2="60" stroke="#4f46e5" stroke-width="1.5"/><line x1="65" y1="24" x2="65" y2="96" stroke="#4f46e5" stroke-width="1.5"/><text x="120" y="52" fill="#4338ca" font-size="20" font-weight="bold">1 / 4</text><text x="120" y="72" fill="#64748b" font-size="9.5" font-weight="bold">One Quarter</text><text x="120" y="86" fill="#10b981" font-size="9">Shaded Portion</text></svg>""",

    "shapes": """<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="max-height:120px;width:auto;"><rect width="200" height="120" rx="14" fill="#fdf4ff" stroke="#f0abfc" stroke-width="2"/><polygon points="45,80 70,35 95,80" fill="#ec4899" stroke="#db2777" stroke-width="2"/><rect x="110" y="40" width="40" height="40" rx="4" fill="#8b5cf6" stroke="#7c3aed" stroke-width="2"/><text x="44" y="98" fill="#be185d" font-size="9" font-weight="bold">Triangle (3)</text><text x="112" y="98" fill="#6d28d9" font-size="9" font-weight="bold">Square (4)</text></svg>""",

    "human body": """<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="max-height:120px;width:auto;"><rect width="200" height="120" rx="14" fill="#fff1f2" stroke="#fecdd3" stroke-width="2"/><path d="M 70 45 C 50 20, 20 45, 70 85 C 120 45, 90 20, 70 45 Z" fill="#f43f5e" stroke="#e11d48" stroke-width="2"/><path d="M 115 65 L 130 65 L 136 50 L 144 80 L 152 65 L 175 65" fill="none" stroke="#059669" stroke-width="2.5" stroke-linecap="round"/><text x="44" y="100" fill="#e11d48" font-size="9.5" font-weight="bold">Heart Pump ❤️</text><text x="122" y="100" fill="#047857" font-size="9" font-weight="bold">Pulse Rhythm</text></svg>""",

    "default": """<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" style="max-height:120px;width:auto;"><rect width="200" height="120" rx="14" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/><circle cx="100" cy="52" r="30" fill="#eef2ff" stroke="#6366f1" stroke-width="2"/><text x="86" y="60" font-size="24">✨</text><text x="56" y="98" fill="#4f46e5" font-size="9.5" font-weight="bold">Interactive Learning Quest</text></svg>"""
}

def get_topic_visual_clue_and_svg(topic, subject, class_name, q_index=0):
    """
    Produce educational emoji visual hints and SVG diagrams based on topic and class.
    Especially vital for Classes I to IV visual and conceptual learning.
    """
    t = (topic or "").lower()
    s = (subject or "").lower()

    if any(k in t for k in ["electric", "circuit", "bulb", "current", "switch", "battery"]):
        clues = [
            "💡 Visual Clue: 🔋 A circuit needs an unbroken loop from battery to bulb!",
            "⚡ Visual Clue: 🔌 Copper wires conduct electricity; switches safely open and close circuits!",
            "⚠️ Visual Clue: 💧 Water conducts electricity—always keep hands dry around plugs!"
        ]
        return clues[q_index % len(clues)], TOPIC_SVG_LIBRARY["electricity"]

    elif any(k in t for k in ["magnet", "pole", "compass", "attract", "repel"]):
        clues = [
            "🧲 Visual Clue: Opposite poles attract (N + S), while like poles repel (N + N)!",
            "🧭 Visual Clue: A magnetic compass needle always aligns towards Earth's North!",
            "📎 Visual Clue: Magnets pull iron, steel, and nickel, but leave wood and plastic alone!"
        ]
        return clues[q_index % len(clues)], TOPIC_SVG_LIBRARY["magnet"]

    elif any(k in t for k in ["plant", "leaf", "root", "photosynth", "seed", "flower", "tree"]):
        clues = [
            "🌱 Visual Clue: ☀️ Sunlight + 💧 Soil Water + 🍃 Chlorophyll = Delicious plant food!",
            "🌸 Visual Clue: Roots drink water underground, while green leaves capture the sunshine!",
            "🌿 Visual Clue: Tiny stomata pores on leaves breathe in carbon dioxide and exhale fresh oxygen!"
        ]
        return clues[q_index % len(clues)], TOPIC_SVG_LIBRARY["plants"]

    elif any(k in t for k in ["planet", "solar", "sun", "moon", "space", "orbit", "mars", "earth"]):
        clues = [
            "🪐 Visual Clue: ☀️ The Sun anchors the center; planets orbit in curved paths!",
            "🌍 Visual Clue: Earth takes 365 days to orbit the Sun, and 24 hours to spin on its axis!",
            "🔴 Visual Clue: Mars appears red because its soil is rich in iron rust!"
        ]
        return clues[q_index % len(clues)], TOPIC_SVG_LIBRARY["solar system"]

    elif any(k in t for k in ["water", "rain", "evaporat", "condens", "cloud", "cycle"]):
        clues = [
            "🌧️ Visual Clue: ☀️ Heat evaporates water into clouds, which then cool and rain back down!",
            "💧 Visual Clue: Water freezes into solid ice at 0°C (32°F) and boils into steam at 100°C!",
            "☁️ Visual Clue: Floating clouds are made of billions of tiny condensed water droplets!"
        ]
        return clues[q_index % len(clues)], TOPIC_SVG_LIBRARY["water"]

    elif any(k in t for k in ["fraction", "ratio", "half", "quarter", "percent", "divide"]):
        clues = [
            "🍕 Visual Clue: Sharing a pizza into 4 equal slices makes each slice 1/4 of the whole!",
            "🍰 Visual Clue: The denominator (bottom) is total parts; numerator (top) is the chosen parts!",
            "📊 Visual Clue: 1/2 is equal to 50% and 2/4!"
        ]
        return clues[q_index % len(clues)], TOPIC_SVG_LIBRARY["fractions"]

    elif any(k in t for k in ["shape", "geometry", "triangle", "angle", "polygon", "circle"]):
        clues = [
            "📐 Visual Clue: Count corners and sides: Triangle = 3, Rectangle = 4, Pentagon = 5!",
            "🔷 Visual Clue: A square has 4 equal sides and four right (90°) angles!",
            "⚪ Visual Clue: A circle has zero straight sides and curves continuously 360°!"
        ]
        return clues[q_index % len(clues)], TOPIC_SVG_LIBRARY["shapes"]

    elif any(k in t for k in ["body", "heart", "organ", "bone", "skeleton", "blood", "lung"]):
        clues = [
            "❤️ Visual Clue: Your heart beats ~100,000 times a day to pump life-giving blood!",
            "🫁 Visual Clue: Lungs expand like sponges to exchange oxygen into your bloodstream!",
            "🦴 Visual Clue: 206 bones form your skeletal frame to protect vital organs and let you move!"
        ]
        return clues[q_index % len(clues)], TOPIC_SVG_LIBRARY["human body"]

    else:
        clues = [
            f"✨ Visual Clue: Focus on fundamental {subject} principles for Class {class_name}!",
            "🔍 Visual Clue: Eliminate options that contradict basic classroom rules!",
            "🎯 Visual Clue: Look for key definitions and think step-by-step!"
        ]
        return clues[q_index % len(clues)], TOPIC_SVG_LIBRARY["default"]


def build_class2_interactive_config(topic, subject):
    """
    Generate tailored tactile interactive game engine configuration for Class 2 kids.
    Procedurally creates rich random variations on every run.
    Separates Capacity/Volume (liquid-pour) from Weight/Mass (pan-balance).
    """
    t = (topic or "").lower()

    # 1. Capacity & Volume / Pouring Jug (Dedicated Liquid Engine)
    if any(k in t for k in ["jug", "capacity", "volume", "liquid", "pour", "litre", "liter", "millilitre", "ml"]):
        r1_target = random.choice([400, 500, 600])
        r2_target = random.choice([750, 800, 1000])
        return {
            "engine": "liquid-pour",
            "title": f"{topic} Fill the Jug Challenge",
            "icon": "🫗",
            "instruction": "Pour the cups of water into the jug until you reach the exact target line!",
            "speechPrompt": "Tap the cups to pour water into the measuring jug!",
            "rounds": [
                {
                    "targetMl": r1_target,
                    "targetName": f"🥣 {r1_target}ml Bowl",
                    "availableCups": [
                        {"ml": 100, "label": "100ml Glass", "icon": "🥛"},
                        {"ml": 250, "label": "250ml Cup", "icon": "🥤"}
                    ]
                },
                {
                    "targetMl": r2_target,
                    "targetName": f"🫗 {r2_target}ml Jug",
                    "availableCups": [
                        {"ml": 250, "label": "250ml Glass", "icon": "🥤"},
                        {"ml": 500, "label": "500ml Bottle", "icon": "🫖"}
                    ]
                }
            ]
        }

    # 2. Weight & Mass (Dedicated Pan Balance Scale)
    elif any(k in t for k in ["balance", "weight", "heavy", "light", "mass", "scale", "gram", "kg"]):
        items_pool = [
            ("🍉 Watermelon", random.choice([300, 400, 500])),
            ("🎃 Pumpkin", random.choice([450, 500, 600])),
            ("🍍 Pineapple", random.choice([200, 250, 300])),
            ("🥥 Coconut", random.choice([250, 350])),
            ("🧱 Toy Bricks", random.choice([300, 350, 400]))
        ]
        random.shuffle(items_pool)
        i1, i2 = items_pool[0], items_pool[1]
        return {
            "engine": "pan-balance",
            "title": f"{topic} Balance Scale",
            "icon": "⚖️",
            "instruction": "Balance the pans by adding weights until both sides are level!",
            "speechPrompt": "Add matching weights onto the right pan until the balance is level!",
            "rounds": [
                {
                    "leftItem": i1[0],
                    "targetWeight": i1[1],
                    "unit": "g",
                    "availableWeights": [100, 100, 100, 50, 50, 20],
                    "hint": f"Combine weights to reach {i1[1]}g!"
                },
                {
                    "leftItem": i2[0],
                    "targetWeight": i2[1],
                    "unit": "g",
                    "availableWeights": [100, 100, 100, 50, 50, 20],
                    "hint": f"Combine weights to reach {i2[1]}g!"
                }
            ]
        }

    # 3. Time & Clock Challenge (Dedicated Interactive Clock Face)
    elif any(k in t for k in ["time", "clock", "hour", "minute", "half past", "quarter", "o'clock"]):
        h1 = random.choice([2, 4, 7, 9, 11])
        h2 = random.choice([1, 3, 5, 8, 10])
        return {
            "engine": "clock-reader",
            "title": f"{topic} Clock Challenge",
            "icon": "⏰",
            "instruction": "Read the clock prompt and rotate the minute hand to the correct time!",
            "speechPrompt": "Tap the minute hand position to set the correct time on the clock face!",
            "rounds": [
                {
                    "targetHour": h1,
                    "targetMinute": 0,
                    "prompt": f"Set the clock to {h1}:00 ({h1} o'Clock)! ⏰",
                    "speechText": f"Set the clock to {h1} o'clock!"
                },
                {
                    "targetHour": h2,
                    "targetMinute": 30,
                    "prompt": f"Set the clock to {h2}:30 (Half Past {h2})! 🕧",
                    "speechText": f"Set the clock to half past {h2}!"
                }
            ]
        }

    # 4. Number Line Hopper (Frog Jump with Clean Geometric Shapes & Dynamic Targets)
    elif any(k in t for k in ["hop", "number line", "skip", "count", "add", "subtract", "pattern"]):
        shape_prizes = [
            {"icon": "⭐", "shape": "star", "name": "Golden Star", "color": "#f59e0b"},
            {"icon": "💎", "shape": "gem", "name": "Blue Gem", "color": "#06b6d4"},
            {"icon": "🌸", "shape": "flower", "name": "Water Lily", "color": "#ec4899"},
            {"icon": "👑", "shape": "crown", "name": "Royal Crown", "color": "#eab308"},
            {"icon": "🦋", "shape": "butterfly", "name": "Blue Butterfly", "color": "#3b82f6"},
            {"icon": "🐞", "shape": "ladybug", "name": "Lucky Ladybug", "color": "#ef4444"},
            {"icon": "🪰", "shape": "fly", "name": "Dragonfly", "color": "#10b981"}
        ]
        random.shuffle(shape_prizes)
        t1 = random.choice([6, 8, 10, 12, 14])
        t2 = random.choice([15, 18, 20, 24, 25])
        return {
            "engine": "number-line-hopper",
            "title": f"{topic} Froggy Hopper",
            "icon": "🐸",
            "instruction": "Help Freddie Frog hop along the lilypads to catch the prize shape!",
            "speechPrompt": "Choose your hops to land Freddie Frog directly on the prize shape!",
            "rounds": [
                {
                    "start": 0,
                    "target": t1,
                    "step": 2,
                    "allowedHops": [1, 2, 5],
                    "itemAtTarget": shape_prizes[0],
                    "hint": f"Hop by 2s to land on {t1}!"
                },
                {
                    "start": 0,
                    "target": t2,
                    "step": 5,
                    "allowedHops": [2, 5],
                    "itemAtTarget": shape_prizes[1],
                    "hint": f"Take big hops of 5 to reach {t2}!"
                }
            ]
        }

    # 5. Equal Sharing / Division (Fair Share Party)
    elif any(k in t for k in ["share", "divide", "division", "equal", "fraction", "multiply", "table"]):
        friend_sets = [
            [{"id": "bunny", "name": "Bunny", "avatar": "🐰"}, {"id": "bear", "name": "Bear", "avatar": "🐻"}],
            [{"id": "bunny", "name": "Bunny", "avatar": "🐰"}, {"id": "bear", "name": "Bear", "avatar": "🐻"}, {"id": "fox", "name": "Fox", "avatar": "🦊"}]
        ]
        treats = [("🍪", "Cookies"), ("🍓", "Strawberries"), ("🧁", "Cupcakes"), ("🍩", "Donuts")]
        random.shuffle(treats)
        return {
            "engine": "fair-share",
            "title": f"{topic} Fair Share Party",
            "icon": "🍪",
            "instruction": "Share the treats equally among the animal friends!",
            "speechPrompt": "Give each animal the exact same number of treats so it is completely fair!",
            "rounds": [
                {
                    "treatIcon": treats[0][0],
                    "treatName": treats[0][1],
                    "totalTreats": random.choice([4, 6, 8]),
                    "friends": friend_sets[0]
                },
                {
                    "treatIcon": treats[1][0],
                    "treatName": treats[1][1],
                    "totalTreats": random.choice([6, 9, 12]),
                    "friends": friend_sets[1]
                }
            ]
        }

    # 6. Money / Rupees (Toy Shop Cash Register)
    elif any(k in t for k in ["money", "coin", "rupee", "shop", "price", "cash"]):
        toys = [
            ("🧸 Teddy Bear", random.choice([12, 14, 15])),
            ("🚀 Toy Rocket", random.choice([16, 17, 19])),
            ("🏎️ Race Car", random.choice([18, 22, 25])),
            ("🎨 Paint Box", random.choice([11, 13, 21]))
        ]
        random.shuffle(toys)
        return {
            "engine": "coin-shop",
            "title": f"{topic} Toy Shop Counter",
            "icon": "🪙",
            "instruction": "Pay for the toy by dragging the exact rupee coins to the counter!",
            "speechPrompt": "Check the price tag and drag the right rupee coins onto the counter!",
            "rounds": [
                {
                    "item": toys[0][0],
                    "price": toys[0][1],
                    "availableCoins": [20, 10, 10, 5, 5, 2, 2, 1, 1],
                    "hint": f"Count coins to make ₹{toys[0][1]}!"
                },
                {
                    "item": toys[1][0],
                    "price": toys[1][1],
                    "availableCoins": [20, 10, 10, 5, 5, 2, 2, 1, 1],
                    "hint": f"Count coins to make ₹{toys[1][1]}!"
                }
            ]
        }

    # 7. Phonics & Rhymes (Bubble Pop)
    elif any(k in t for k in ["sound", "phonics", "rhyme", "letter", "vowel", "spell"]):
        families = [
            ("CAT", ["BAT 🦇", "HAT 🎩", "MAT 🧘"], ["DOG 🐶", "SUN ☀️", "PEN 🖊️"]),
            ("DOG", ["FOG 🌫️", "LOG 🪵", "FROG 🐸"], ["CAT 🐱", "CUP 🥤", "BAG 🎒"]),
            ("PIN", ["BIN 🗑️", "WIN 🏆", "TIN 🥫"], ["FOX 🦊", "BED 🛏️", "SUN ☀️"])
        ]
        f = random.choice(families)
        bubbles = [{"text": w, "correct": True} for w in f[1]] + [{"text": w, "correct": False} for w in f[2]]
        random.shuffle(bubbles)
        return {
            "engine": "bubble-pop",
            "title": f"{topic} Bubble Pop",
            "icon": "🫧",
            "instruction": f"Pop the bubbles that rhyme with '{f[0]}'!",
            "speechPrompt": f"Find and pop all the bubbles that rhyme with {f[0]}!",
            "rounds": [
                {
                    "prompt": f"Pop all words that rhyme with '{f[0]}'!",
                    "speechText": f"Pop the words that rhyme with {f[0]}!",
                    "bubbles": bubbles
                }
            ]
        }

    # 8. Categorization / Sorter
    else:
        b1_name = f"{topic} Group A 🌟"
        b2_name = f"{topic} Group B 🎯"
        return {
            "engine": "bucket-sorter",
            "title": f"{topic} Tactile Sorter",
            "icon": "🧺",
            "instruction": f"Sort the cards into their matching baskets for {topic}!",
            "speechPrompt": "Sort each card into its correct basket!",
            "buckets": [
                {"id": "b1", "label": b1_name, "color": "#10b981", "border": "#059669"},
                {"id": "b2", "label": b2_name, "color": "#8b5cf6", "border": "#7c3aed"}
            ],
            "items": [
                {"text": "Card 1", "icon": "⭐", "bucket": "b1"},
                {"text": "Card 2", "icon": "🎯", "bucket": "b2"},
                {"text": "Card 3", "icon": "⭐", "bucket": "b1"},
                {"text": "Card 4", "icon": "🎯", "bucket": "b2"}
            ]
        }


def generate_ai_task_and_quiz(prompt="", class_name="IV", subject="Science", topic="", num_questions=3, difficulty="Medium", api_key=None):
    """
    Main function for teacher task creation:
    Takes teacher's instructions/details and returns a complete, ready-to-publish game and quiz pack.
    Strictly aligns 100% of generated questions with the teacher's specified topic and prompt.
    Equipped with multi-modal enhancements: visual emoji hints and SVG diagrams for visual learners.
    """
    num_questions = max(1, min(10, int(num_questions or 3)))
    class_name = str(class_name or "IV").strip().upper()
    subject = str(subject or "Science").strip()
    topic = str(topic or "").strip()
    prompt = str(prompt or "").strip()
    difficulty = str(difficulty or "Medium").strip()
    effective_topic = topic or prompt or f"{subject} Concepts"

    # Formulate strict prompt for Gemini with multi-modal requirements
    system_prompt = f"""You are an expert school curriculum designer and interactive game creator for primary and middle school students (Classes I to VIII).
A teacher wants to automatically create an interactive learning game and quiz task for her class.

Teacher's Specifications:
- Target Class: Class {class_name}
- Subject: {subject}
- Primary Topic: {effective_topic}
- Teacher Details / Prompt: {prompt or effective_topic}
- Number of Questions: {num_questions}
- Difficulty Level: {difficulty}

CRITICAL RULES:
1. TOPIC ACCURACY IS MANDATORY: Every single question MUST be strictly, directly, and exclusively about "{effective_topic}".
   - For example, if the topic is "Electricity", ALL questions must be about electricity, electric current, appliances, switches, circuits, batteries, conductors, or electrical safety.
   - Do NOT include questions from other topics like plants or solar system unless specifically requested.
2. MULTI-MODAL VISUAL LEARNING (Especially critical for Classes I-IV):
   - Provide a "visual_hint": An encouraging, age-appropriate emoji-rich clue sentence helping kids visualize the concept (e.g., "💡 Visual Clue: 🔋 A complete circuit needs an unbroken loop to light the bulb!").
   - Optionally provide "svg_diagram": A compact, colorful, valid inline SVG diagram (<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">...</svg>) illustrating the concept (e.g. circuit diagram, fraction circle, plant parts, magnet poles). Must have viewBox, nice colors, and no external resources.
3. Target audience: Class {class_name} students. Adjust vocabulary and difficulty to be perfectly age-appropriate.
4. Return ONLY a valid JSON object matching the schema below. No markdown fences, no explanatory text outside JSON.

JSON Schema:
{{
  "title": "Exciting and catchy game title (e.g. '⚡ Sparky Electricity Quest', '🚀 Fraction Champions') - max 45 chars",
  "class": "{class_name}",
  "subject": "{subject}",
  "skillArea": "{effective_topic[:40]}",
  "gameType": "MCQ Quiz",
  "desc": "Encouraging 1-2 sentence instructions for Class {class_name} students.",
  "time": "{max(3, num_questions * 2)} min",
  "questions": [
    {{
      "prompt": "Engaging question sentence about {effective_topic}?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": 0,
      "explanation": "Friendly 1-sentence explanation telling why the chosen option is correct.",
      "visual_hint": "Fun emoji clue guiding younger learners (e.g. '💡 Clue: Look for the device that opens and closes the circuit!')",
      "svg_diagram": "<svg viewBox='0 0 200 120' xmlns='http://www.w3.org/2000/svg'>...</svg>"
    }}
  ]
}}
Ensure the "questions" list contains EXACTLY {num_questions} questions, with exactly 4 options per question, and "answer" is the 0-indexed integer (0, 1, 2, or 3) of the correct choice.
"""

    gemini_result, provider = call_gemini_api(system_prompt, api_key=api_key)
    if gemini_result and isinstance(gemini_result, dict) and "questions" in gemini_result and len(gemini_result["questions"]) > 0:
        cleaned_questions = []
        for idx, q in enumerate(gemini_result["questions"]):
            if not isinstance(q, dict) or "prompt" not in q:
                continue
            opts = q.get("options", [])
            if not isinstance(opts, list) or len(opts) < 2:
                continue
            while len(opts) < 4:
                opts.append(f"Option {chr(65 + len(opts))}")
            opts = [str(o) for o in opts[:4]]
            ans = q.get("answer", 0)
            if not isinstance(ans, int) or ans < 0 or ans >= len(opts):
                ans = 0

            # Multi-Modal Visual Clue & Diagram Verification
            visual_hint = str(q.get("visual_hint", "")).strip()
            svg_diagram = str(q.get("svg_diagram", "")).strip()

            fallback_clue, fallback_svg = get_topic_visual_clue_and_svg(effective_topic, subject, class_name, idx)
            if not visual_hint or len(visual_hint) < 5:
                visual_hint = fallback_clue

            # Clean and validate SVG diagram
            if not (svg_diagram.startswith("<svg") and "</svg>" in svg_diagram and "viewBox" in svg_diagram):
                svg_diagram = fallback_svg

            cleaned_questions.append({
                "prompt": str(q.get("prompt", "Question")),
                "options": opts,
                "answer": ans,
                "explanation": str(q.get("explanation", f"Correct answer is {opts[ans]}.")),
                "visual_hint": visual_hint,
                "svg_diagram": svg_diagram
            })

        if cleaned_questions:
            task_dict = {
                "title": str(gemini_result.get("title", f"Class {class_name} {effective_topic} Quest"))[:50],
                "class": class_name,
                "subject": subject,
                "skillArea": str(gemini_result.get("skillArea", effective_topic))[:40],
                "gameType": str(gemini_result.get("gameType", "MCQ Quiz")),
                "desc": str(gemini_result.get("desc", f"Master {effective_topic} in Class {class_name} through this interactive quiz challenge!")),
                "time": str(gemini_result.get("time", f"{max(3, num_questions * 2)} min")),
                "questions": cleaned_questions[:num_questions]
            }
            if str(class_name).upper() in ("II", "2"):
                task_dict["interactiveConfig"] = build_class2_interactive_config(effective_topic, subject)
            return task_dict, provider

    # Fallback to intelligent Curriculum AI Engine
    fallback_task = generate_smart_task(prompt, class_name, subject, topic, num_questions, difficulty)
    return fallback_task, "🤖 Smart Curriculum AI Engine"



# =====================================================================
# 2. INTELLIGENT CURRICULUM AI FALLBACK ENGINE
# =====================================================================

TOPIC_KNOWLEDGE_BASE = {
    # ELECTRICITY & ENERGY
    "electricity": [
        ("Which of these household items needs electricity to work?", ["Television", "Wooden chair", "Pencil", "Cotton blanket"], 0, "A television contains electronic components that require electric power to display picture and sound."),
        ("What safe device do we press to turn electric lights ON and OFF?", ["Electric Switch", "Door Handle", "Water Tap", "Window Latch"], 0, "A switch safely completes or breaks an electric circuit to control the flow of electricity."),
        ("What small portable object stores electrical energy to power a handheld torch or toy car?", ["Battery / Dry Cell", "Bar Magnet", "Rubber band", "Glass marble"], 0, "Batteries store chemical energy that transforms into electrical energy whenever needed."),
        ("Why must we NEVER touch electric switches or plug sockets with wet hands?", ["Water conducts electricity and can give a severe shock", "Switches get slippery", "It wastes battery power", "Water cools the light bulb"], 0, "Water is a natural conductor of electricity; wet hands drastically increase shock hazards."),
        ("Which material easily allows electric current to pass through it?", ["Copper metal wire", "Plastic ruler", "Dry wooden stick", "Rubber eraser"], 0, "Metals like copper and aluminum are good conductors of electricity."),
        ("What do we call the continuous unbroken loop through which electricity travels?", ["An Electric Circuit", "A Solar Orbit", "A Water Pipeline", "A Mountain Tunnel"], 0, "A closed electric circuit forms a complete loop from the power source through the bulb and back.")
    ],

    # MAGNETS & MAGNETISM
    "magnet": [
        ("What are the two opposite ends or poles of every magnet called?", ["North and South poles", "East and West poles", "Top and Bottom poles", "Plus and Minus poles"], 0, "Every magnet has two poles: a North-seeking pole and a South-seeking pole."),
        ("What happens when you bring two identical North poles of magnets close together?", ["They repel (push each other away)", "They attract and stick together", "They turn into liquid", "They lose all magnetic power"], 0, "Like poles repel each other, while unlike poles attract."),
        ("Which of the following objects will be pulled and attracted by a magnet?", ["An iron nail", "A plastic spoon", "A wooden pencil", "A cotton ball"], 0, "Magnets attract ferromagnetic metals like iron, steel, nickel, and cobalt."),
        ("What small navigation tool uses a magnetized needle to always point North?", ["A Magnetic Compass", "A Thermometer", "A Telescope", "A Magnifying glass"], 0, "A magnetic compass needle aligns with Earth's magnetic field to indicate North.")
    ],

    # LIGHT & SHADOWS
    "light": [
        ("What is our planet's main natural source of light and warmth?", ["The Sun", "The Moon", "Candles", "Street lamps"], 0, "The Sun is the massive star that provides natural daylight and warmth to Earth."),
        ("What dark shape is formed behind an opaque object when light is blocked?", ["A Shadow", "A Rainbow", "A Mirror", "A Cloud"], 0, "Because light travels in straight lines, blocking it casts a dark shadow behind the object."),
        ("Which object reflects light clearly to let you see your own reflection?", ["A Plane Mirror", "A Brick Wall", "A Cardboard box", "A Woolen sweater"], 0, "Smooth, shiny glass mirrors reflect light rays evenly so you see an image of yourself.")
    ],

    # SOUND
    "sound": [
        ("How is sound produced by all instruments, voices, and objects?", ["By vibrating back and forth rapidly", "By standing completely still", "By freezing in ice", "By shining bright light"], 0, "Sounds are born whenever an object vibrates, creating pressure waves in the surrounding air."),
        ("Which sensory organ in our body detects sound waves and sends signals to our brain?", ["Ears", "Eyes", "Nose", "Tongue"], 0, "Our ears capture sound vibrations and translate them into hearing signals.")
    ],

    # FORCE & MOTION
    "force": [
        ("A push or a pull applied on an object is defined as a:", ["Force", "Temperature", "Volume", "Weightlessness"], 0, "In physics, any action that pushes or pulls an object is called a force."),
        ("What invisible force pulls all objects down toward the center of the Earth?", ["Gravity", "Friction", "Magnetism", "Wind"], 0, "Earth's gravitational pull keeps our feet on the ground and brings falling objects down.")
    ],

    # AIR & ATMOSPHERE
    "air": [
        ("What gas in the air is essential for humans and animals to breathe and live?", ["Oxygen", "Carbon Dioxide", "Helium", "Neon"], 0, "Oxygen is the vital atmospheric gas our lungs absorb for respiration."),
        ("What do we call air when it is moving across the earth?", ["Wind", "Fog", "Ice", "Steam"], 0, "Moving air currents are referred to as wind or breezes.")
    ],

    # SOLAR SYSTEM & SPACE
    "solar system": [
        ("Which planet is closest to the Sun in our Solar System?", ["Mercury", "Venus", "Earth", "Mars"], 0, "Mercury is the first and closest planet orbiting nearest to the Sun."),
        ("Which planet is famously known as the 'Red Planet'?", ["Mars", "Venus", "Jupiter", "Saturn"], 0, "Mars appears reddish in the sky due to iron oxide (rust) on its surface."),
        ("What is the largest planet in our solar system?", ["Jupiter", "Saturn", "Neptune", "Uranus"], 0, "Jupiter is the biggest planet, with a giant storm called the Great Red Spot."),
        ("Which planet is famous for its bright, spectacular ring system?", ["Saturn", "Mars", "Jupiter", "Mercury"], 0, "Saturn is surrounded by thousands of beautiful rings made of ice and rock particles."),
        ("What heavenly body orbits around the Earth as its natural satellite?", ["The Moon", "Mars", "The Sun", "Halley's Comet"], 0, "The Moon is Earth's only natural satellite, orbiting us every 27 days.")
    ],

    # PLANTS & NATURE
    "plants": [
        ("What green substance inside leaves captures sunlight for photosynthesis?", ["Chlorophyll", "Hemoglobin", "Cellulose", "Starch"], 0, "Chlorophyll gives leaves their green color and traps sunlight energy."),
        ("Which part of the plant absorbs water and minerals from the soil?", ["Roots", "Stem", "Leaves", "Flower"], 0, "Roots anchor the plant firmly and drink up water and minerals from the ground."),
        ("Through which tiny pores on leaves do plants breathe and exchange gases?", ["Stomata", "Chloroplasts", "Xylem", "Tendrils"], 0, "Stomata are tiny microscopic openings that let carbon dioxide in and oxygen out."),
        ("What process do plants use to make food using sunlight, water, and carbon dioxide?", ["Photosynthesis", "Germination", "Respiration", "Pollination"], 0, "Photo (light) + synthesis (making): plants make glucose using solar energy.")
    ],

    # WATER CYCLE
    "water": [
        ("What is the process called when liquid water turns into invisible water vapor?", ["Evaporation", "Condensation", "Precipitation", "Freezing"], 0, "Heat from the sun warms water, causing it to evaporate into the atmosphere."),
        ("What happens during condensation in the water cycle?", ["Water vapor cools and forms clouds", "Rain falls to earth", "Ice melts into water", "Plants drink water"], 0, "Cool air aloft turns invisible water vapor into tiny water droplets, creating clouds."),
        ("At what temperature on the Celsius scale does pure water freeze into solid ice?", ["0°C", "100°C", "50°C", "-50°C"], 0, "Water freezes into solid ice at 0 degrees Celsius (32°F).")
    ],

    # HUMAN BODY
    "human body": [
        ("Which vital organ pumps oxygen-rich blood throughout your entire body?", ["Heart", "Brain", "Lungs", "Stomach"], 0, "Your heart is a muscular pump that beats around 100,000 times every day!"),
        ("Which organs take in oxygen when you breathe in and release carbon dioxide?", ["Lungs", "Kidneys", "Liver", "Stomach"], 0, "Lungs expand like sponges to exchange life-giving oxygen into the bloodstream."),
        ("How many bones are there in an adult human skeleton?", ["206", "106", "150", "300"], 0, "Adults have 206 bones; babies are born with about 300, many of which fuse together as they grow.")
    ],

    # ANIMALS
    "animals": [
        ("Animals that eat only plants are classified as:", ["Herbivores", "Carnivores", "Omnivores", "Decomposers"], 0, "Herbivores like cows, deer, and elephants feed exclusively on plants and vegetation."),
        ("Which animal is known as the largest mammal currently living on Earth?", ["Blue Whale", "African Elephant", "Giraffe", "Hippopotamus"], 0, "The blue whale can weigh up to 200 tons—longer than three school buses!")
    ],

    # MATHEMATICS: FRACTIONS
    "fractions": [
        ("What is 1/2 + 1/4 equal to?", ["3/4", "2/6", "1/8", "2/4"], 0, "1/2 is equal to 2/4. Adding 2/4 + 1/4 gives 3/4."),
        ("In the fraction 3/8, what is the number 3 called?", ["Numerator", "Denominator", "Quotient", "Divisor"], 0, "The top number is the numerator (parts we have); the bottom is the denominator (total parts)."),
        ("Which of these fractions is greater than 1/2?", ["3/4", "1/4", "2/5", "2/6"], 0, "3/4 (75%) is greater than 1/2 (50%).")
    ],

    # MATHEMATICS: MULTIPLICATION
    "multiplication": [
        ("What is 12 multiplied by 7?", ["84", "74", "82", "94"], 0, "12 × 7 = 84."),
        ("If a carton contains 8 eggs, how many eggs are in 9 cartons?", ["72", "64", "81", "90"], 0, "9 cartons × 8 eggs = 72 eggs in total."),
        ("Any number multiplied by 0 always results in:", ["0", "The same number", "1", "10"], 0, "The Zero Property of Multiplication states that n × 0 = 0 always.")
    ],

    # MATHEMATICS: GEOMETRY
    "geometry": [
        ("How many sides does a regular hexagon have?", ["6", "5", "7", "8"], 0, "Hexa means six: a hexagon has 6 straight sides and 6 vertices."),
        ("What is the sum of angles inside any triangle?", ["180°", "90°", "270°", "360°"], 0, "The three interior angles of any triangle always add up to exactly 180 degrees.")
    ],

    # ENGLISH: GRAMMAR
    "grammar": [
        ("Which word in this sentence is a verb: 'The happy dog barked loudly'?", ["barked", "happy", "dog", "loudly"], 0, "'Barked' is the action word describing what the dog did."),
        ("Choose the correct plural form of the noun 'Child':", ["Children", "Childs", "Childrens", "Childes"], 0, "'Children' is an irregular plural form of child.")
    ],

    # ENGLISH: VOCABULARY
    "vocabulary": [
        ("What is an antonym (opposite word) of 'Gigantic'?", ["Tiny", "Huge", "Colossal", "Massive"], 0, "Gigantic means enormous; its direct opposite is tiny or miniature."),
        ("What is a synonym (similar meaning) of the word 'Courageous'?", ["Brave", "Timid", "Fearful", "Silent"], 0, "Courageous means possessing courage, which is the definition of brave.")
    ]
}


def generate_smart_task(prompt="", class_name="IV", subject="Science", topic="", num_questions=3, difficulty="Medium"):
    """
    Intelligent curriculum builder that parses prompt & topic keywords and selects
    topic-accurate questions. For any novel or unlisted topic, it dynamically synthesizes
    authentic topic-centered questions rather than defaulting to unrelated topics.
    """
    class_name = str(class_name or "IV").strip().upper()
    subject = str(subject or "Science").strip()
    topic = str(topic or "").strip()
    prompt = str(prompt or "").strip()
    full_text = f"{prompt} {topic} {subject}".lower()
    clean_topic = topic or prompt or f"{subject} Concepts"
    clean_topic = clean_topic[:35].strip()

    # 1. Check exact topic keyword matches
    matched_pool = None
    matched_theme = None
    for key, q_list in TOPIC_KNOWLEDGE_BASE.items():
        if key in full_text:
            matched_pool = list(q_list)
            matched_theme = key.title()
            break

    # 2. Check subject-level aliases if no specific topic matched
    if not matched_pool:
        if any(w in full_text for w in ["electric", "circuit", "bulb", "switch", "battery", "power"]):
            matched_pool = list(TOPIC_KNOWLEDGE_BASE["electricity"])
            matched_theme = "Electricity & Circuits"
        elif any(w in full_text for w in ["magnet", "pole", "attract"]):
            matched_pool = list(TOPIC_KNOWLEDGE_BASE["magnet"])
            matched_theme = "Magnets & Magnetism"
        elif any(w in full_text for w in ["light", "shadow", "reflection", "mirror"]):
            matched_pool = list(TOPIC_KNOWLEDGE_BASE["light"])
            matched_theme = "Light & Shadows"
        elif any(w in full_text for w in ["sound", "vibration", "hear", "music"]):
            matched_pool = list(TOPIC_KNOWLEDGE_BASE["sound"])
            matched_theme = "Sound & Vibrations"
        elif any(w in full_text for w in ["force", "push", "pull", "gravity"]):
            matched_pool = list(TOPIC_KNOWLEDGE_BASE["force"])
            matched_theme = "Force & Motion"
        elif any(w in full_text for w in ["fraction", "half", "quarter"]):
            matched_pool = list(TOPIC_KNOWLEDGE_BASE["fractions"])
            matched_theme = "Fractions & Decimals"
        elif any(w in full_text for w in ["multiply", "product", "times table"]):
            matched_pool = list(TOPIC_KNOWLEDGE_BASE["multiplication"])
            matched_theme = "Multiplication & Arithmetic"
        elif any(w in full_text for w in ["shape", "angle", "geometry", "triangle"]):
            matched_pool = list(TOPIC_KNOWLEDGE_BASE["geometry"])
            matched_theme = "Geometry & Shapes"
        elif any(w in full_text for w in ["noun", "verb", "tense", "grammar", "sentence"]):
            matched_pool = list(TOPIC_KNOWLEDGE_BASE["grammar"])
            matched_theme = "Grammar & Sentence Skills"
        elif any(w in full_text for w in ["synonym", "antonym", "vocab", "word"]):
            matched_pool = list(TOPIC_KNOWLEDGE_BASE["vocabulary"])
            matched_theme = "Vocabulary & Word Power"

    # 3. DYNAMIC SYNTHESIZER FOR NOVEL / UNLISTED TOPICS
    # If a teacher assigns ANY novel topic (e.g., "Dinosaurs", "Weather", "Ancient India", "Robotics"),
    # we procedurally create authentic questions strictly around clean_topic!
    if not matched_pool:
        matched_theme = clean_topic.title()
        matched_pool = [
            (
                f"What is the primary focus when learning about {clean_topic} in Class {class_name} {subject}?",
                [f"Understanding key concepts and real-world examples of {clean_topic}", "Memorizing unrelated history dates", "Writing random numbers", "Drawing completely unrelated patterns"],
                0,
                f"In Class {class_name} {subject}, we explore {clean_topic} through fundamental concepts and observable examples."
            ),
            (
                f"Which of the following is most closely related to the study of {clean_topic}?",
                [f"Core principles and applications of {clean_topic}", "Deep sea submarine navigation", "Cooking recipes from 500 years ago", "Rocket fuel chemical formulas"],
                0,
                f"The study of {clean_topic} centers on its foundational principles and practical observations."
            ),
            (
                f"Why is understanding {clean_topic} valuable for young learners in Class {class_name}?",
                [f"It helps us observe, explain, and interact with {clean_topic} in our daily lives", "It is only useful for astronauts in space", "It replaces the need to read books", "It has no practical connection to the world"],
                0,
                f"Learning {clean_topic} connects classroom concepts to everyday observations and problem-solving."
            ),
            (
                f"When investigating {clean_topic}, which scientific method step is most beneficial?",
                [f"Observing carefully, asking questions, and recording findings about {clean_topic}", "Guessing without ever observing", "Ignoring facts that disagree with guesses", "Skipping all questions"],
                0,
                f"Careful observation and inquiry are the core building blocks of understanding {clean_topic}."
            ),
            (
                f"Which statement regarding {clean_topic} is most accurate for Class {class_name} students?",
                [f"{clean_topic} is an essential curriculum topic in {subject} that builds strong fundamentals", f"{clean_topic} is never studied in schools", f"{clean_topic} is completely unrelated to {subject}", f"{clean_topic} applies only on other planets"],
                0,
                f"{clean_topic} provides essential foundation knowledge for Class {class_name} {subject}."
            )
        ]

    # Select questions and shuffle options so answer 0 isn't always the top choice
    selected_raw = random.sample(matched_pool, min(num_questions, len(matched_pool)))
    while len(selected_raw) < num_questions:
        selected_raw.append(random.choice(matched_pool))

    questions = []
    for idx, (q_prompt, opts, correct_idx, exp) in enumerate(selected_raw):
        # Shuffle options randomly while tracking correct answer
        indexed_opts = list(enumerate(opts))
        random.shuffle(indexed_opts)
        new_opts = [text for orig_idx, text in indexed_opts]
        new_ans_idx = [i for i, (orig_idx, _) in enumerate(indexed_opts) if orig_idx == correct_idx][0]

        clue, svg = get_topic_visual_clue_and_svg(clean_topic, subject, class_name, idx)
        questions.append({
            "prompt": f"[{class_name} {subject}] {q_prompt}",
            "options": new_opts,
            "answer": new_ans_idx,
            "explanation": exp,
            "visual_hint": clue,
            "svg_diagram": svg
        })

    title_templates = [
        f"⚡ {clean_topic} Explorer Quest",
        f"🌟 {clean_topic} Champions Challenge",
        f"🚀 {clean_topic} Mastery Sprint",
        f"🎯 {clean_topic} Adventure"
    ]
    title = random.choice(title_templates)[:45]

    res_task = {
        "title": title,
        "class": class_name,
        "subject": subject,
        "skillArea": (topic or matched_theme)[:40],
        "gameType": "MCQ Quiz",
        "desc": f"Master {clean_topic} in Class {class_name} {subject} through this interactive quiz challenge!",
        "time": f"{max(3, num_questions * 2)} min",
        "questions": questions[:num_questions]
    }
    if str(class_name).upper() in ("II", "2"):
        res_task["interactiveConfig"] = build_class2_interactive_config(clean_topic, subject)
    return res_task
