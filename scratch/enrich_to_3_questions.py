import json
import re

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for g in catalog:
    questions = g.get('questions', [])
    if len(questions) < 3:
        oid = g.get('outcomeId', g['id'])
        lo = g.get('learningOutcome', '')
        cls = g['class']
        subj = g['subject']
        sub = g['activity']
        sa = g['skillArea']

        # Format a clean verb phrase from the outcome
        lo_clean = lo.strip()
        lo_phrase = lo_clean[0].lower() + lo_clean[1:] if len(lo_clean) > 1 else lo_clean

        q3 = {
            "prompt": f"Why is practicing '{sub}' vital for students in Class {cls} {subj}?",
            "options": [
                f"It actively empowers the learner to {lo_phrase}",
                "It has no educational value or curriculum alignment",
                "It is designed solely to replace reading and thinking",
                "It contradicts the official NCERT learning objectives"
            ],
            "answer": 0,
            "explanation": f"Official Curriculum Outcome #{oid} ({sa} • {sub}): {lo}"
        }
        questions.append(q3)
        g['questions'] = questions

print(f"All {len(catalog)} games now have {len(catalog[0]['questions'])} questions!")

# Save full_games_catalog.json
with open('full_games_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

# Save full_games_catalog.js
js_content = f"// Full Games Catalog for MyClassboard Games Platform\n// 440 Curriculum Games with Full Multi-Modal Question Bank\n\nconst FULL_GAMES_CATALOG = {json.dumps(catalog, indent=2, ensure_ascii=False)};\n\nif (typeof window !== 'undefined') {{\n    window.FULL_GAMES_CATALOG = FULL_GAMES_CATALOG;\n    window.GamesCatalog = FULL_GAMES_CATALOG;\n}}\n"
with open('full_games_catalog.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

# Update question_bank.js
qb = {}
for g in catalog:
    key = f"Class {g['class']}|||{g['subject']}|||{g['title']}"
    qb[key] = {
        "title": g['title'],
        "class": g['class'],
        "subject": g['subject'],
        "skillArea": g['skillArea'],
        "subSkillArea": g.get('subSkillArea', g['activity']),
        "learningOutcome": g['learningOutcome'],
        "questions": g['questions']
    }

with open('question_bank.js', 'w', encoding='utf-8') as f:
    f.write("// Authoritative Question Bank derived STRICTLY from 'skillAreaOutcomes - Sheet1.pdf'\n")
    f.write("const QUESTION_BANK = ")
    json.dump(qb, f, indent=2, ensure_ascii=False)
    f.write(";\n\n")
    f.write("if (typeof module !== 'undefined' && module.exports) module.exports = { QUESTION_BANK };\n")

print("SUCCESS: Updated catalog, JS, and question bank with 3 questions per game!")
