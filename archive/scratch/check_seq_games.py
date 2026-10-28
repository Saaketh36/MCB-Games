import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

seq_games = [g for g in catalog if g.get('gameType') == 'Sequence Order']
print(f"Total Sequence Order games: {len(seq_games)}")
for g in seq_games:
    print(f"[{g['id']}] Class {g['class']} | {g['subject']} | {g['skillArea']} | {g['title']}")
    if g.get('questions'):
        for i, q in enumerate(g['questions']):
            print(f"   Q{i+1}: {q['prompt'][:60]}... -> Ans: {q['options'][q['answer']]}")
