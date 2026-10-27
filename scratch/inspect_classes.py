import json

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

print("--- CLASS VIII (350 to 440) ---")
for g in catalog[349:440]:
    print(f"#{g['outcomeId']} [{g['subject']} - {g['subSkillArea']}] {g['learningOutcome']}")
