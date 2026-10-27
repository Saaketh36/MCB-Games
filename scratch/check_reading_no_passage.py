import json

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

reading_no_passage = [g for g in catalog if g.get('skillArea') == 'Reading' and not g.get('passage')]
print(f"Reading games without passage: {len(reading_no_passage)}")
for g in reading_no_passage:
    print(f"[{g['id']}] Class {g['class']} | {g['title']} | activity={g.get('activity')} | gameType={g.get('gameType')}")
    if g.get('questions'):
        print(f"   Q1: {g['questions'][0]['prompt']}")
