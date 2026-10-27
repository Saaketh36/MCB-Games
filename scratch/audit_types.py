import json
from collections import defaultdict

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open('question_bank.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = "const QUESTION_BANK = "
raw_json = text[len(prefix):].rstrip(';\n ')
qb = json.loads(raw_json)

# Check all games by gameType
by_type = defaultdict(list)
for g in catalog:
    by_type[g.get('gameType')].append(g)

print("Game types summary:")
for t, games in by_type.items():
    print(f"=== {t} ({len(games)} games) ===")
    sample = games[0]
    print(f"  Example: [{sample['id']}] {sample['title']} (Class {sample['class']} - {sample['subject']} - {sample['skillArea']})")
    print(f"  Q1: {sample['questions'][0]['prompt'] if sample.get('questions') else 'NO QUESTIONS'}")
