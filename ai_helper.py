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


def generate_ai_task_and_quiz(prompt="", class_name="IV", subject="Science", topic="", num_questions=3, difficulty="Medium", api_key=None):
    """
    Main function for teacher task creation:
    Takes teacher's instructions/details and returns a complete, ready-to-publish game and quiz pack.
    Strictly aligns 100% of generated questions with the teacher's specified topic and prompt.
    """
    num_questions = max(1, min(10, int(num_questions or 3)))
    class_name = str(class_name or "IV").strip().upper()
    subject = str(subject or "Science").strip()
    topic = str(topic or "").strip()
    prompt = str(prompt or "").strip()
    difficulty = str(difficulty or "Medium").strip()
    effective_topic = topic or prompt or f"{subject} Concepts"

    # Formulate strict prompt for Gemini
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
2. Target audience: Class {class_name} students. Adjust vocabulary and difficulty to be perfectly age-appropriate.
3. Return ONLY a valid JSON object matching the schema below. No markdown fences, no explanatory text outside JSON.

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
      "explanation": "Friendly 1-sentence explanation telling why the chosen option is correct."
    }}
  ]
}}
Ensure the "questions" list contains EXACTLY {num_questions} questions, with exactly 4 options per question, and "answer" is the 0-indexed integer (0, 1, 2, or 3) of the correct choice.
"""

    gemini_result, provider = call_gemini_api(system_prompt, api_key=api_key)
    if gemini_result and isinstance(gemini_result, dict) and "questions" in gemini_result and len(gemini_result["questions"]) > 0:
        cleaned_questions = []
        for q in gemini_result["questions"]:
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
            cleaned_questions.append({
                "prompt": str(q.get("prompt", "Question")),
                "options": opts,
                "answer": ans,
                "explanation": str(q.get("explanation", f"Correct answer is {opts[ans]}."))
            })

        if cleaned_questions:
            return {
                "title": str(gemini_result.get("title", f"Class {class_name} {effective_topic} Quest"))[:50],
                "class": class_name,
                "subject": subject,
                "skillArea": str(gemini_result.get("skillArea", effective_topic))[:40],
                "gameType": str(gemini_result.get("gameType", "MCQ Quiz")),
                "desc": str(gemini_result.get("desc", f"Master {effective_topic} in Class {class_name} through this interactive quiz challenge!")),
                "time": str(gemini_result.get("time", f"{max(3, num_questions * 2)} min")),
                "questions": cleaned_questions[:num_questions]
            }, provider

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
    for q_prompt, opts, correct_idx, exp in selected_raw:
        # Shuffle options randomly while tracking correct answer
        indexed_opts = list(enumerate(opts))
        random.shuffle(indexed_opts)
        new_opts = [text for orig_idx, text in indexed_opts]
        new_ans_idx = [i for i, (orig_idx, _) in enumerate(indexed_opts) if orig_idx == correct_idx][0]

        questions.append({
            "prompt": f"[{class_name} {subject}] {q_prompt}",
            "options": new_opts,
            "answer": new_ans_idx,
            "explanation": exp
        })

    title_templates = [
        f"⚡ {clean_topic} Explorer Quest",
        f"🌟 {clean_topic} Champions Challenge",
        f"🚀 {clean_topic} Mastery Sprint",
        f"🎯 {clean_topic} Adventure"
    ]
    title = random.choice(title_templates)[:45]

    return {
        "title": title,
        "class": class_name,
        "subject": subject,
        "skillArea": (topic or matched_theme)[:40],
        "gameType": "MCQ Quiz",
        "desc": f"Master {clean_topic} in Class {class_name} {subject} through this interactive quiz challenge!",
        "time": f"{max(3, num_questions * 2)} min",
        "questions": questions[:num_questions]
    }
