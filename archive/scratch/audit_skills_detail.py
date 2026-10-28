import json
from collections import Counter

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open('skill_areas_data.json', 'r', encoding='utf-8') as f:
    skills = json.load(f)

with open('question_bank.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = "const QUESTION_BANK = "
raw_json = text[len(prefix):].rstrip(';\n ')
qb = json.loads(raw_json)

# Check all listening games in catalog and skills
print("=== LISTENING GAMES AUDIT ===")
listening_in_skills = [s for s in skills if s.get('skillArea') == 'Listening']
print(f"Total listening in skills: {len(listening_in_skills)}")
for s in listening_in_skills:
    print(f"Class: {s['class']} | Activity: {s['activity']} | Title: {s['activityName']} | GameType: {s['gameType']}")

# Check reading games in skills
print("\n=== READING GAMES AUDIT ===")
reading_in_skills = [s for s in skills if s.get('skillArea') == 'Reading']
print(f"Total reading in skills: {len(reading_in_skills)}")
for s in reading_in_skills:
    print(f"Class: {s['class']} | Activity: {s['activity']} | Title: {s['activityName']} | GameType: {s['gameType']}")

# Check all non-MCQ gameTypes in catalog
print("\n=== GAME TYPES ACROSS ALL 325 GAMES ===")
cat_types = Counter(g['gameType'] for g in catalog)
for t, c in cat_types.items():
    print(f"  {t}: {c}")
