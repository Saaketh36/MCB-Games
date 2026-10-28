import json

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

g = next(x for x in games if x['outcomeId'] == 243)
print("Title:", g['title'])
print("Story:", g['story'])
for i, q in enumerate(g['questions']):
    print(f"Q{i+1}: {q['prompt']}")
    print(f"   Options: {q['options']}")
