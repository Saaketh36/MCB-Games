import json

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

dups = {}
for g in catalog:
    dups.setdefault(g['title'], []).append(g)

for title, items in dups.items():
    if len(items) > 1:
        print(f"\n=== Title: {title} ({len(items)} items) ===")
        for g in items:
            print(f"  [{g['id']}] Class {g['class']} | {g['subject']} | {g['skillArea']} | Sub: {g['activity']}")
            print(f"    LO: {g['learningOutcome'][:110]}...")
