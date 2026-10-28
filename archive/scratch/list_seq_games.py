import json
with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

print(f"Total games: {len(cat)}")
seq_games = [g for g in cat if g.get('gameType') == 'Sequence Order']
print(f"Sequence Order games ({len(seq_games)}):")
for g in seq_games:
    print(f"  {g['id']} | Class {g['class']} {g['subject']} | {g['title']} | inst={bool(g.get('instructions'))} | audio={bool(g.get('audio_script'))}")
