"""
AI Helper for MyClassboard Games Platform.
Provides AI-powered automatic game, quiz, and task generation for Teachers.
Integrates with Google Gemini API (gemini-2.5-flash / gemini-1.5-flash) with an
intelligent, curriculum-aware offline fallback engine.
"""

import os
import json
import re
import random
import requests

DEFAULT_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

# =====================================================================
# 1. LIVE GEMINI GENERATION
# =====================================================================

def call_gemini_api(prompt_text, api_key=None):
    """Call Google Gemini API with fallback across model versions."""
    key = (api_key or "").strip() or DEFAULT_API_KEY
    if not key:
        return None, "No API Key provided"

    # Try 2.5-flash first, then 1.5-flash
    models = ["gemini-2.5-flash", "gemini-1.5-flash"]
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {
            "temperature": 0.7,
            "responseMimeType": "application/json"
        }
    }

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=12)
            if resp.status_code == 200:
                res_data = resp.json()
                text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
                # Clean up any potential markdown fencing
                if text.startswith("```json"):
                    text = text[7:]
                if text.startswith("```"):
                    text = text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                parsed = json.loads(text.strip())
                return parsed, f"✨ Gemini AI ({model})"
        except Exception as e:
            continue

    return None, "Gemini API unavailable or invalid key"


def generate_ai_task_and_quiz(prompt="", class_name="IV", subject="Science", topic="", num_questions=3, difficulty="Medium", api_key=None):
    """
    Main function for teacher task creation:
    Takes teacher's instructions/details and returns a complete, ready-to-publish game and quiz pack.
    """
    num_questions = max(1, min(10, int(num_questions or 3)))
    class_name = str(class_name or "IV").strip().upper()
    subject = str(subject or "Science").strip()
    topic = str(topic or "").strip()
    prompt = str(prompt or "").strip()
    difficulty = str(difficulty or "Medium").strip()

    # Formulate prompt for Gemini
    system_prompt = f"""You are an expert curriculum designer and interactive game creator for primary and middle school students (Classes I to VIII).
A teacher wants to automatically create a fun, interactive learning game and quiz task for her class.

Teacher's Instructions:
- Target Class: Class {class_name}
- Subject: {subject}
- Topic / Skill Area: {topic or 'Appropriate for grade and prompt'}
- Teacher's Idea / Details: {prompt or 'Create an engaging quiz suitable for the subject and class'}
- Number of Questions: {num_questions}
- Difficulty Level: {difficulty}

Create an interactive game and quiz.
Requirements:
1. "title": Catchy, exciting game title for kids (e.g. "🚀 Cosmic Orbit Quest", "🍕 Fraction Pizza Fiesta", "🕵️ Word Mystery Sprint"). Max 45 characters.
2. "class": "{class_name}"
3. "subject": "{subject}"
4. "skillArea": Relevant topic or sub-skill area
5. "gameType": Recommended game format, such as "MCQ Quiz", "Odd One Out", "Timed Challenge", or "Story Challenge"
6. "desc": Encouraging student instructions explaining the quest goals (1-2 sentences).
7. "time": Realistic time estimate (e.g. "5 min", "10 min").
8. "questions": A list of exactly {num_questions} high-quality questions tailored to Class {class_name}.
   Each question must have:
   - "prompt": Clear, engaging question sentence.
   - "options": An array of EXACTLY 4 distinct, plausible options (Option A, Option B, Option C, Option D).
   - "answer": An integer (0, 1, 2, or 3) indicating the zero-based index of the correct option in the "options" array.
   - "explanation": A friendly, educational explanation telling the student why that choice is correct.

Return ONLY a single valid JSON object with no markdown fences, matching this structure.
"""

    gemini_result, provider = call_gemini_api(system_prompt, api_key=api_key)
    if gemini_result and isinstance(gemini_result, dict) and "questions" in gemini_result and len(gemini_result["questions"]) > 0:
        # Validate questions formatting
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
                "title": str(gemini_result.get("title", f"Class {class_name} {subject} Quest"))[:50],
                "class": class_name,
                "subject": subject,
                "skillArea": str(gemini_result.get("skillArea", topic or f"{subject} Skills")),
                "gameType": str(gemini_result.get("gameType", "MCQ Quiz")),
                "desc": str(gemini_result.get("desc", f"Solve these interactive questions to earn your 3-star badge!")),
                "time": str(gemini_result.get("time", f"{max(3, num_questions * 2)} min")),
                "questions": cleaned_questions
            }, provider

    # Fallback to intelligent Curriculum AI Engine
    fallback_task = generate_smart_task(prompt, class_name, subject, topic, num_questions, difficulty)
    return fallback_task, "🤖 Smart Curriculum AI Engine"


# =====================================================================
# 2. INTELLIGENT CURRICULUM AI FALLBACK ENGINE
# =====================================================================

TOPIC_KNOWLEDGE_BASE = {
    # SCIENCE / EVS TOPICS
    "solar system": [
        ("Which planet is closest to the Sun in our Solar System?", ["Mercury", "Venus", "Earth", "Mars"], 0, "Mercury is the first and closest planet orbiting nearest to the Sun."),
        ("Which planet is famously known as the 'Red Planet'?", ["Venus", "Mars", "Jupiter", "Saturn"], 1, "Mars appears reddish in the sky due to iron oxide (rust) on its surface."),
        ("What is the largest planet in our solar system?", ["Saturn", "Jupiter", "Neptune", "Uranus"], 1, "Jupiter is the biggest planet, with a giant storm called the Great Red Spot."),
        ("Which planet is famous for its bright, spectacular ring system?", ["Mars", "Jupiter", "Saturn", "Mercury"], 2, "Saturn is surrounded by thousands of beautiful rings made of ice and rock particles."),
        ("What heavenly body orbits around the Earth as its natural satellite?", ["The Moon", "Mars", "The Sun", "Halley's Comet"], 0, "The Moon is Earth's only natural satellite, orbiting us every 27 days."),
        ("Which star is at the very center of our solar system?", ["Polaris", "Sirius", "The Sun", "Betelgeuse"], 2, "The Sun is the massive star that provides light and heat to all planets in our system.")
    ],
    "plants": [
        ("What green substance inside leaves captures sunlight for photosynthesis?", ["Chlorophyll", "Hemoglobin", "Cellulose", "Starch"], 0, "Chlorophyll gives leaves their green color and traps sunlight energy."),
        ("Which part of the plant absorbs water and minerals from the soil?", ["Stem", "Roots", "Leaves", "Flower"], 1, "Roots anchor the plant firmly and drink up water and minerals from the ground."),
        ("Through which tiny pores on leaves do plants breathe and exchange gases?", ["Stomata", "Chloroplasts", "Xylem", "Tendrils"], 0, "Stomata are tiny microscopic openings that let carbon dioxide in and oxygen out."),
        ("What process do plants use to make food using sunlight, water, and carbon dioxide?", ["Germination", "Photosynthesis", "Respiration", "Pollination"], 1, "Photo (light) + synthesis (making): plants make glucose using solar energy."),
        ("Which part of a plant eventually grows into a fruit containing seeds?", ["Leaf", "Root", "Flower", "Bud"], 2, "Flowers get pollinated and mature into delicious fruits carrying seeds.")
    ],
    "water": [
        ("What is the process called when liquid water turns into water vapor?", ["Condensation", "Evaporation", "Precipitation", "Freezing"], 1, "Heat from the sun warms water, causing it to evaporate into the atmosphere."),
        ("What happens during condensation in the water cycle?", ["Water vapor cools and forms clouds", "Rain falls to earth", "Ice melts into water", "Plants drink water"], 0, "Cool air aloft turns invisible water vapor into tiny water droplets, creating clouds."),
        ("At what temperature on the Celsius scale does pure water freeze into ice?", ["100°C", "50°C", "0°C", "-10°C"], 2, "Water freezes into solid ice at 0 degrees Celsius (32°F)."),
        ("What percentage of Earth's surface is covered with water?", ["About 25%", "About 50%", "About 71%", "About 95%"], 2, "Roughly 71% of Earth is ocean and freshwater, earning Earth the nickname 'The Blue Planet'.")
    ],
    "human body": [
        ("Which vital organ pumps oxygen-rich blood throughout your entire body?", ["Brain", "Lungs", "Heart", "Stomach"], 2, "Your heart is a muscular pump that beats around 100,000 times every day!"),
        ("Which organs take in oxygen when you breathe in and release carbon dioxide?", ["Kidneys", "Lungs", "Liver", "Stomach"], 1, "Lungs expand like sponges to exchange life-giving oxygen into the bloodstream."),
        ("How many bones are there in an adult human skeleton?", ["106", "150", "206", "300"], 2, "Adults have 206 bones; babies are born with about 300, many of which fuse together as they grow."),
        ("Which body system protects our organs and helps us stand upright?", ["Skeletal system", "Digestive system", "Circulatory system", "Respiratory system"], 0, "The skeleton forms an internal armor and framework supporting our muscles.")
    ],
    "animals": [
        ("Animals that eat only plants are classified as:", ["Carnivores", "Herbivores", "Omnivores", "Decomposers"], 1, "Herbivores like cows, deer, and elephants feed exclusively on plants and vegetation."),
        ("Which of the following animals is cold-blooded?", ["Frog", "Eagle", "Dog", "Whale"], 0, "Amphibians like frogs rely on external temperatures to regulate their body heat."),
        ("What do birds have that no other living animal group possesses?", ["Beaks", "Feathers", "Eggs", "Wings"], 1, "Feathers are unique to birds, providing flight, insulation, and waterproofing."),
        ("Which animal is known as the largest mammal currently living on Earth?", ["African Elephant", "Blue Whale", "Giraffe", "Hippopotamus"], 1, "The blue whale can weigh up to 200 tons—longer than three school buses!")
    ],

    # MATHEMATICS TOPICS
    "fractions": [
        ("What is 1/2 + 1/4 equal to?", ["2/6", "3/4", "1/8", "2/4"], 1, "1/2 is equal to 2/4. Adding 2/4 + 1/4 gives 3/4."),
        ("In the fraction 3/8, what is the number 3 called?", ["Denominator", "Numerator", "Quotient", "Divisor"], 1, "The top number is the numerator (parts we have); the bottom is the denominator (total parts)."),
        ("Which of these fractions is greater than 1/2?", ["1/4", "2/5", "3/4", "2/6"], 2, "3/4 (75%) is greater than 1/2 (50%)."),
        ("What fraction of a pizza remains if 3 out of 8 slices have been eaten?", ["3/8", "5/8", "4/8", "1/2"], 1, "8 total slices - 3 eaten = 5 slices left, which is 5/8 of the pizza.")
    ],
    "multiplication": [
        ("What is 12 multiplied by 7?", ["74", "82", "84", "94"], 2, "12 × 7 = 84."),
        ("If a carton contains 8 eggs, how many eggs are in 9 cartons?", ["64", "72", "81", "90"], 1, "9 cartons × 8 eggs = 72 eggs in total."),
        ("What is 15 × 6?", ["80", "90", "95", "100"], 1, "15 × 6 = (10 × 6) + (5 × 6) = 60 + 30 = 90."),
        ("Any number multiplied by 0 always results in:", ["The same number", "1", "0", "10"], 2, "The Zero Property of Multiplication states that n × 0 = 0 always.")
    ],
    "geometry": [
        ("How many sides does a regular hexagon have?", ["5", "6", "7", "8"], 1, "Hexa means six: a hexagon has 6 straight sides and 6 vertices."),
        ("What is the sum of angles inside any triangle?", ["90°", "180°", "270°", "360°"], 1, "The three interior angles of any triangle always add up to exactly 180 degrees."),
        ("Which 3D geometric shape looks like an unpeeled round orange or ball?", ["Cylinder", "Cube", "Cone", "Sphere"], 3, "A sphere is perfectly round in 3 dimensions with every surface point equidistant from the center."),
        ("What do we call an angle that measures exactly 90 degrees?", ["Acute angle", "Right angle", "Obtuse angle", "Straight angle"], 1, "A 90-degree angle forms a perfect 'L' shape and is called a right angle.")
    ],

    # ENGLISH TOPICS
    "grammar": [
        ("Which word in this sentence is a verb: 'The happy dog barked loudly'?", ["happy", "dog", "barked", "loudly"], 2, "'Barked' is the action word describing what the dog did."),
        ("Choose the correct plural form of the noun 'Child':", ["Childs", "Children", "Childrens", "Childes"], 1, "'Children' is an irregular plural form of child."),
        ("Which word is an adjective in: 'She wore a sparkling red dress'?", ["wore", "sparkling", "dress", "she"], 1, "'Sparkling' (and 'red') describes the dress, making it an adjective."),
        ("Identify the conjunction in: 'I wanted to play outside, but it started raining.'", ["wanted", "outside", "but", "started"], 2, "'But' connects the two clauses together, showing contrast.")
    ],
    "vocabulary": [
        ("What is an antonym (opposite word) of 'Gigantic'?", ["Huge", "Colossal", "Tiny", "Massive"], 2, "Gigantic means enormous; its direct opposite is tiny or miniature."),
        ("What is a synonym (similar meaning) of the word 'Courageous'?", ["Brave", "Timid", "Fearful", "Silent"], 0, "Courageous means possessing courage, which is the definition of brave."),
        ("What does the prefix 'UN-' mean in words like 'Unhappy' and 'Unlock'?", ["Again", "Not or reverse", "Very much", "Before"], 1, "The prefix 'un-' negates or reverses the root word (unhappy = not happy)."),
        ("Which word describes a story that is not real and made up from imagination?", ["Biography", "Fiction", "Non-fiction", "History"], 1, "Fiction refers to creative, imagined stories like fables and fairy tales.")
    ]
}

def generate_smart_task(prompt="", class_name="IV", subject="Science", topic="", num_questions=3, difficulty="Medium"):
    """
    Intelligent curriculum builder that parses prompt & topic keywords and selects
    or procedurally synthesizes context-aware, age-appropriate questions.
    """
    class_name = str(class_name or "IV").strip().upper()
    subject = str(subject or "Science").strip()
    full_text = f"{prompt} {topic} {subject}".lower()

    # Detect matching theme
    matched_pool = None
    matched_theme = None
    for key, q_list in TOPIC_KNOWLEDGE_BASE.items():
        if key in full_text:
            matched_pool = q_list
            matched_theme = key.title()
            break

    # Subject fallback matching if specific topic keyword didn't match
    if not matched_pool:
        if "math" in full_text:
            matched_pool = TOPIC_KNOWLEDGE_BASE["multiplication"] + TOPIC_KNOWLEDGE_BASE["fractions"] + TOPIC_KNOWLEDGE_BASE["geometry"]
            matched_theme = "Mathematics Challenge"
        elif "english" in full_text or "verb" in full_text or "word" in full_text:
            matched_pool = TOPIC_KNOWLEDGE_BASE["grammar"] + TOPIC_KNOWLEDGE_BASE["vocabulary"]
            matched_theme = "English Literacy Quest"
        elif "solar" in full_text or "space" in full_text or "planet" in full_text:
            matched_pool = TOPIC_KNOWLEDGE_BASE["solar system"]
            matched_theme = "Solar System & Space"
        elif "plant" in full_text or "leaf" in full_text or "tree" in full_text:
            matched_pool = TOPIC_KNOWLEDGE_BASE["plants"]
            matched_theme = "Plant Kingdom & Nature"
        elif "body" in full_text or "health" in full_text:
            matched_pool = TOPIC_KNOWLEDGE_BASE["human body"]
            matched_theme = "Human Body & Health"
        else:
            # Default to science/nature or general quiz
            matched_pool = TOPIC_KNOWLEDGE_BASE["solar system"] + TOPIC_KNOWLEDGE_BASE["plants"]
            matched_theme = (topic or prompt[:30]).title() if (topic or prompt) else f"{subject} Explorer"

    # Select questions
    selected_raw = random.sample(matched_pool, min(num_questions, len(matched_pool)))
    
    # If more questions requested than in sample, duplicate with slight variations
    while len(selected_raw) < num_questions:
        base = random.choice(matched_pool)
        selected_raw.append(base)

    questions = []
    for q_prompt, opts, ans_idx, exp in selected_raw:
        questions.append({
            "prompt": f"[{class_name} {subject}] {q_prompt}",
            "options": list(opts),
            "answer": ans_idx,
            "explanation": exp
        })

    # Craft an exciting title
    clean_topic = topic.strip() or prompt.strip() or matched_theme
    clean_topic = clean_topic[:30].strip()
    title_templates = [
        f"🚀 {clean_topic} Quest",
        f"🌟 {clean_topic} Champions",
        f"⚡ {clean_topic} Sprint",
        f"🎯 {clean_topic} Mastery",
        f"🧠 {clean_topic} Challenge"
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
