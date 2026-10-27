# -*- coding: utf-8 -*-
"""
Inspect all 440 outcomes and classify them by subject and domain.
"""
import json

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

for g in games[239:250]:
    print(f"{g['id']}: [{g['subject']} - {g['skillArea']} - {g['subSkillArea']}]")
    print(f"   Outcome: {g['learningOutcome']}\n")
