# -*- coding: utf-8 -*-
import json

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

print(f"Total games: {len(games)}")
for g in games[:15]:
    print(f"{g['id']}: [{g['class']} {g['subject']}] {g['skillArea']} -> {g['subSkillArea']}")
    print(f"   Outcome: {g['learningOutcome']}")
