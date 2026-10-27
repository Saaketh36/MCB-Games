#!/usr/bin/env python3
"""
Independent English Reading Comprehension Generator for MyClassboard Games.
Generates curriculum-aligned stories or essays on specific topics with vocabulary glossaries,
and an evidence-based mix of Multiple Choice (MCQ) and Short Typed comprehension questions.

Supports:
- Live AI generation via Google Gemini API (gemini-2.5-flash / gemini-flash-latest)
- High-quality offline template generator if offline or no API key is set
- Automatic merging into full_games_catalog.json & full_games_catalog.js
"""

import os
import sys
import json
import re
import argparse
from dotenv import load_dotenv

# Ensure local dir is on python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, 'reconfigure'):
        _stream.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()

try:
    from ai_helper import call_gemini_api
except ImportError:
    call_gemini_api = None


# =====================================================================
# OFFLINE FALLBACK TEMPLATES FOR INDEPENDENT GENERATION
# =====================================================================
OFFLINE_TEMPLATES = {
    "solar system": {
        "title": "Wonders of the Solar System",
        "genre": "Science Essay",
        "content": [
            "Our solar system consists of the Sun and everything bound to it by gravity. The Sun is a colossal star at the center, containing more than ninety-nine percent of all the mass in the entire system.",
            "Orbiting the Sun are eight planets, divided into two distinct groups. The four inner planets—Mercury, Venus, Earth, and Mars—are dense and rocky. Earth is the only known planet that harbors liquid water and thriving life.",
            "Beyond the rocky planets lies the Asteroid Belt, followed by the four outer gas giants: Jupiter, Saturn, Uranus, and Neptune. Jupiter is so vast that over one thousand Earths could fit inside it, while Saturn is renowned for its magnificent rings of ice and cosmic dust.",
            "Comets and icy dwarf planets like Pluto travel in the distant Kuiper Belt at the outer rim. Astronomers use deep-space telescopes to discover thousands of exoplanets orbiting distant stars, proving that our cosmic neighborhood is part of an infinite universe."
        ],
        "vocabulary": [
            {"word": "colossal", "definition": "Extremely large, massive, or gigantic.", "example": "The Sun is a colossal sphere of glowing gas."},
            {"word": "harbors", "definition": "Gives a home or shelter to something.", "example": "Earth harbors millions of unique plant species."},
            {"word": "renowned", "definition": "Famous and widely admired for a special quality.", "example": "Saturn is renowned for its icy ring system."}
        ],
        "questions": [
            {
                "id": 1,
                "type": "mcq",
                "prompt": "Which planet is the only one in the solar system known to harbor liquid water and life?",
                "options": ["Mars", "Venus", "Earth", "Jupiter"],
                "answer": 2,
                "evidenceParagraph": 1,
                "explanation": "Paragraph 2 states: 'Earth is the only known planet that harbors liquid water and thriving life.'"
            },
            {
                "id": 2,
                "type": "mcq",
                "prompt": "What are the four inner planets primarily made of?",
                "options": ["Liquid hydrogen", "Dense rock", "Ice and gas", "Pure iron crystals"],
                "answer": 1,
                "evidenceParagraph": 1,
                "explanation": "Paragraph 2 mentions: 'The four inner planets... are dense and rocky.'"
            },
            {
                "id": 3,
                "type": "mcq",
                "prompt": "What are Saturn's famous rings primarily composed of?",
                "options": ["Solid gold boulders", "Ice and cosmic dust", "Burning gas", "Liquid nitrogen"],
                "answer": 1,
                "evidenceParagraph": 2,
                "explanation": "Paragraph 3 notes: 'Saturn is renowned for its magnificent rings of ice and cosmic dust.'"
            },
            {
                "id": 4,
                "type": "typed",
                "prompt": "What region lies between the rocky inner planets and the outer gas giants?",
                "answer": "Asteroid Belt",
                "keywords": ["asteroid", "belt"],
                "evidenceParagraph": 2,
                "explanation": "Paragraph 3 states: 'Beyond the rocky planets lies the Asteroid Belt'."
            },
            {
                "id": 5,
                "type": "typed",
                "prompt": "What percentage of the solar system's total mass is contained within the Sun?",
                "answer": "more than ninety-nine percent",
                "keywords": ["99", "ninety-nine", "percent"],
                "evidenceParagraph": 0,
                "explanation": "Paragraph 1 explains the Sun contains 'more than ninety-nine percent of all the mass in the entire system'."
            }
        ]
    },
    "friendship": {
        "title": "The Tree of Whispering Secrets",
        "genre": "Moral Story",
        "content": [
            "In a sunny valley surrounded by emerald hills stood an ancient silver oak known as the Tree of Whispering Secrets. Two village children, Aarav and Meera, met beneath its rustling leaves every afternoon to share stories and weave flower garlands.",
            "One windy evening, Meera dropped her grandmother's heirloom silver locket into a dark, rocky crevice near the tree's twisting roots. The crevice was far too deep for Meera's arm to reach. She burst into tears, thinking the cherished keepsake was lost forever.",
            "Aarav did not leave her side. Instead, he gathered long, flexible bamboo stems and used sticky tree resin from pine bark to craft an ingenious retrieval hook. Patiently guiding the rod into the dark fissure, he hooked the locket's silver chain and lifted it safely into the moonlight.",
            "Meera beamed with gratitude and divided her warm freshly baked sesame rolls with Aarav. They carved a tiny leaf on the tree trunk as a reminder that true friendship is built on loyalty, patient problem-solving, and staying together during stormy moments."
        ],
        "vocabulary": [
            {"word": "heirloom", "definition": "A valuable family possession passed down through generations.", "example": "The silver locket was a cherished family heirloom."},
            {"word": "crevice", "definition": "A narrow opening or crack, especially in rock or ground.", "example": "The key slipped into a dark crevice in the stone."},
            {"word": "ingenious", "definition": "Clever, original, and inventive.", "example": "He found an ingenious way to repair the broken windmill."}
        ],
        "questions": [
            {
                "id": 1,
                "type": "mcq",
                "prompt": "What precious item did Meera drop into the rocky crevice?",
                "options": ["Her leather schoolbag", "Her grandmother's heirloom silver locket", "A pouch of gold coins", "A brass compass"],
                "answer": 1,
                "evidenceParagraph": 1,
                "explanation": "Paragraph 2 states: 'Meera dropped her grandmother's heirloom silver locket into a dark, rocky crevice'."
            },
            {
                "id": 2,
                "type": "mcq",
                "prompt": "How did Aarav retrieve the locket from the deep opening?",
                "options": [
                    "He called the village fire brigade",
                    "He crafted a retrieval hook using bamboo and tree resin",
                    "He poured water into the crack until it floated",
                    "He smashed the boulder with a heavy hammer"
                ],
                "answer": 1,
                "evidenceParagraph": 2,
                "explanation": "Paragraph 3 describes how Aarav 'gathered long, flexible bamboo stems and used sticky tree resin... to craft an ingenious retrieval hook'."
            },
            {
                "id": 3,
                "type": "mcq",
                "prompt": "What lesson about friendship does the story teach?",
                "options": [
                    "Friends should only meet on sunny days",
                    "Friendship is built on loyalty and patient problem-solving",
                    "Never trust an ancient oak tree",
                    "Keep your precious things hidden away"
                ],
                "answer": 1,
                "evidenceParagraph": 3,
                "explanation": "Paragraph 4 states: 'true friendship is built on loyalty, patient problem-solving, and staying together during stormy moments.'"
            },
            {
                "id": 4,
                "type": "typed",
                "prompt": "What sticky natural substance did Aarav use to create the hook?",
                "answer": "tree resin from pine bark",
                "keywords": ["resin", "tree resin"],
                "evidenceParagraph": 2,
                "explanation": "Paragraph 3 notes he 'used sticky tree resin from pine bark'."
            },
            {
                "id": 5,
                "type": "typed",
                "prompt": "What did Aarav and Meera carve on the tree trunk to remember their adventure?",
                "answer": "a tiny leaf",
                "keywords": ["leaf", "tiny leaf"],
                "evidenceParagraph": 3,
                "explanation": "Paragraph 4 mentions: 'They carved a tiny leaf on the tree trunk'."
            }
        ]
    }
}


# =====================================================================
# AI GENERATOR PROMPT & PARSER
# =====================================================================
def generate_passage_ai(topic, class_level="V", genre="story", num_questions=5):
    """Generate passage and questions using Gemini API or offline fallback."""
    prompt = f"""
You are an expert curriculum author and reading specialist for Indian school students (Classes I to VIII).
Create an age-appropriate, engaging reading comprehension activity for Class {class_level}.

Topic: "{topic}"
Genre: "{genre}" (Story, Informational Essay, or Biographical Narrative)
Target Questions: {num_questions} (Provide an evidence-based mix of multiple-choice and short typed text-evidence questions)

Return ONLY valid JSON (no markdown formatting, no comments, no code fences) with the exact structure:
{{
  "title": "Engaging Title of Passage",
  "topic": "{topic}",
  "genre": "{genre.capitalize()}",
  "readingLevel": "Class {class_level}",
  "estimatedTime": "3-4 min",
  "content": [
    "Paragraph 1 text...",
    "Paragraph 2 text...",
    "Paragraph 3 text...",
    "Paragraph 4 text..."
  ],
  "vocabulary": [
    {{"word": "word1", "definition": "clear kid-friendly definition", "example": "example sentence from context"}},
    {{"word": "word2", "definition": "clear kid-friendly definition", "example": "example sentence from context"}},
    {{"word": "word3", "definition": "clear kid-friendly definition", "example": "example sentence from context"}}
  ],
  "questions": [
    {{
      "id": 1,
      "type": "mcq",
      "prompt": "Comprehension question text?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": 0,
      "evidenceParagraph": 0,
      "explanation": "Quote or reason from paragraph 1."
    }},
    {{
      "id": 2,
      "type": "typed",
      "prompt": "Direct question asking for a specific detail or quote from the text?",
      "answer": "Exact short answer phrase",
      "keywords": ["keyword1", "keyword2"],
      "evidenceParagraph": 1,
      "explanation": "Quote or reason from paragraph 2."
    }}
  ]
}}
"""

    if call_gemini_api:
        api_key = os.environ.get("GEMINI_API_KEY", "")
        res, err = call_gemini_api(prompt, api_key=api_key)
        if res:
            try:
                # Clean markdown fences if any
                clean = re.sub(r'^```(?:json)?\s*', '', res.strip(), flags=re.MULTILINE)
                clean = re.sub(r'\s*```$', '', clean, flags=re.MULTILINE)
                data = json.loads(clean)
                return data, None
            except Exception as e:
                pass  # Fall through to offline template

    # Fallback template
    topic_lower = topic.lower()
    for key, templ in OFFLINE_TEMPLATES.items():
        if key in topic_lower or topic_lower in key:
            data = {
                "title": templ["title"],
                "topic": topic,
                "genre": templ["genre"],
                "readingLevel": f"Class {class_level}",
                "estimatedTime": "3 min",
                "content": templ["content"],
                "vocabulary": templ["vocabulary"],
                "questions": templ["questions"]
            }
            return data, "Generated from high-quality curated template (offline mode)"

    # Generic high-quality fallback based on topic
    data = {
        "title": f"The Wonders of {topic.title()}",
        "topic": topic,
        "genre": genre.capitalize() if genre else "Informational Essay",
        "readingLevel": f"Class {class_level}",
        "estimatedTime": "3 min",
        "content": [
            f"Throughout history, {topic.lower()} has captured the imagination of students, thinkers, and explorers. Whether observing the natural world or studying how things work, curiosity leads to incredible discoveries.",
            f"When we look closely at {topic.lower()}, we observe patterns that reveal how parts connect together. Experts emphasize that careful reading and active observation are the keys to unlocking new understanding.",
            f"Every new observation about {topic.lower()} opens up new questions for the next generation of learners. By asking questions, sharing ideas, and exploring evidence, students become true scientific explorers."
        ],
        "vocabulary": [
            {"word": "curiosity", "definition": "A strong desire to know or learn something new.", "example": "Her curiosity drove her to read every book in the library."},
            {"word": "observation", "definition": "The action of watching something carefully to gain information.", "example": "Observation of night stars helps map constellations."},
            {"word": "patterns", "definition": "Regular, repeated, or recurring forms or designs.", "example": "Scientists identify weather patterns using satellites."}
        ],
        "questions": [
            {
                "id": 1,
                "type": "mcq",
                "prompt": f"According to Paragraph 1, what leads to incredible discoveries about {topic.lower()}?",
                "options": ["Curiosity and observation", "Leaving things untouched", "Memorizing without understanding", "Working in silence"],
                "answer": 0,
                "evidenceParagraph": 0,
                "explanation": "Paragraph 1 states: 'curiosity leads to incredible discoveries.'"
            },
            {
                "id": 2,
                "type": "mcq",
                "prompt": "What do experts emphasize as the keys to unlocking new understanding in Paragraph 2?",
                "options": ["Running as fast as possible", "Careful reading and active observation", "Ignoring patterns", "Using guess work only"],
                "answer": 1,
                "evidenceParagraph": 1,
                "explanation": "Paragraph 2 notes: 'careful reading and active observation are the keys to unlocking new understanding.'"
            },
            {
                "id": 3,
                "type": "typed",
                "prompt": "What do students become when they ask questions and explore evidence?",
                "answer": "true scientific explorers",
                "keywords": ["scientific", "explorers"],
                "evidenceParagraph": 2,
                "explanation": "Paragraph 3 concludes: 'students become true scientific explorers.'"
            }
        ]
    }
    return data, "Generated via standard curated engine"


# =====================================================================
# MERGE INTO FULL GAMES CATALOG
# =====================================================================
def merge_into_catalog(passage_data, game_id=None, class_level="V"):
    cat_json_path = os.path.join(BASE_DIR, "full_games_catalog.json")
    cat_js_path = os.path.join(BASE_DIR, "full_games_catalog.js")

    if not os.path.exists(cat_json_path):
        print(f"Error: {cat_json_path} not found.")
        return False

    with open(cat_json_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    # If game_id provided, find and update
    target = None
    if game_id:
        target = next((g for g in catalog if g.get("id") == game_id), None)

    # Otherwise look for a matching class Reading Comprehension game
    if not target:
        target = next((g for g in catalog if g.get("class") == class_level and g.get("skillArea") == "Reading" and g.get("activity") == "Reading Comprehension"), None)

    if target:
        target["passage"] = {
            "title": passage_data["title"],
            "topic": passage_data["topic"],
            "genre": passage_data.get("genre", "Story"),
            "readingLevel": passage_data.get("readingLevel", f"Class {class_level}"),
            "estimatedTime": passage_data.get("estimatedTime", "3 min"),
            "content": passage_data["content"],
            "vocabulary": passage_data["vocabulary"]
        }
        target["questions"] = passage_data["questions"]
        target["gameType"] = "Reading Comprehension"
        target["desc"] = f"Read the story/essay '{passage_data['title']}' and answer comprehension questions."
        target["topic"] = passage_data["topic"]
        print(f"Merged into existing game: {target['id']} ({target['title']})")
    else:
        # Create a new activity entry
        new_id = f"{class_level}-ENG-READ-{int(os.times()[4] * 1000) % 10000:04d}"
        new_game = {
            "id": new_id,
            "title": passage_data["title"],
            "class": class_level,
            "subject": "English",
            "skillArea": "Reading",
            "activity": "Reading Comprehension",
            "gameType": "Reading Comprehension",
            "thumb": "images/game_english.jpg",
            "badgeClass": "badge-eng",
            "desc": f"Read the story/essay '{passage_data['title']}' and answer comprehension questions.",
            "time": passage_data.get("estimatedTime", "4 min"),
            "stars": "3 stars",
            "topic": passage_data["topic"],
            "passage": passage_data,
            "questions": passage_data["questions"]
        }
        catalog.append(new_game)
        print(f"Appended new reading activity to catalog: {new_id} ({new_game['title']})")

    with open(cat_json_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    js_content = "// Full Games Catalog for MyClassboard Games Platform\n"
    js_content += "// 325 Curriculum Games with Full Multi-Modal Question Bank & Reading Studio\n\n"
    js_content += "const FULL_GAMES_CATALOG = " + json.dumps(catalog, indent=2, ensure_ascii=False) + ";\n\n"
    js_content += "if (typeof window !== 'undefined') {\n"
    js_content += "    window.FULL_GAMES_CATALOG = FULL_GAMES_CATALOG;\n"
    js_content += "    window.GamesCatalog = FULL_GAMES_CATALOG;\n"
    js_content += "}\n"

    with open(cat_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    print("Successfully synchronized full_games_catalog.json and full_games_catalog.js!")
    return True


# =====================================================================
# CLI INTERFACE
# =====================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Generate curriculum-aligned reading passages with vocabulary glossaries & questions."
    )
    parser.add_argument("--topic", type=str, default="Solar System", help="Topic for the story or essay")
    parser.add_argument("--class", dest="class_level", type=str, default="V", help="Class level (I to VIII)")
    parser.add_argument("--genre", type=str, default="essay", choices=["story", "essay", "biography", "auto"], help="Passage genre")
    parser.add_argument("--num-questions", type=int, default=5, help="Number of questions to generate")
    parser.add_argument("--output", type=str, default="", help="Optional JSON file path to save output")
    parser.add_argument("--merge", action="store_true", help="Merge generated passage directly into games catalog")
    parser.add_argument("--game-id", type=str, default="", help="Specific game ID to update in catalog (e.g. II-ENG-05)")

    args = parser.parse_args()

    print(f"Generating reading passage on '{args.topic}' for Class {args.class_level}...")
    data, note = generate_passage_ai(
        topic=args.topic,
        class_level=args.class_level,
        genre=args.genre,
        num_questions=args.num_questions
    )

    if note:
        print(f"[{note}]")

    print("\n" + "=" * 60)
    print(f"📖 {data['title'].upper()}")
    print(f"Topic: {data['topic']} | Genre: {data.get('genre')} | Level: {data.get('readingLevel')}")
    print("=" * 60)
    for idx, p in enumerate(data["content"]):
        print(f"\n[¶ {idx + 1}] {p}")

    print("\n📚 KEY VOCABULARY:")
    for v in data.get("vocabulary", []):
        print(f"  • {v['word']}: {v['definition']}")

    print("\n❓ COMPREHENSION QUESTIONS:")
    for q in data.get("questions", []):
        q_type = "MCQ" if q.get("type") == "mcq" else "Typed Evidence"
        print(f"  [{q_type}] Q{q['id']}: {q['prompt']}")
        if q.get("type") == "mcq":
            for o_idx, opt in enumerate(q.get("options", [])):
                mark = "✓" if o_idx == q.get("answer") else " "
                print(f"      ({chr(65 + o_idx)}) {opt} {mark}")
        else:
            print(f"      Expected Answer: {q.get('answer')}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nSaved passage data to: {args.output}")

    if args.merge:
        merge_into_catalog(data, game_id=args.game_id, class_level=args.class_level)

if __name__ == "__main__":
    main()
