import json

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

seq_games = [g for g in catalog if g.get('gameType') == 'Sequence Order']
print(f"Total Sequence Order games: {len(seq_games)}")

for g in seq_games:
    has_inst = bool(g.get('instructions'))
    has_audio = bool(g.get('audio_script'))
    has_story = bool(g.get('story'))
    print(f"[{g.get('id')}] {g.get('class')} | {g.get('subject')} | {g.get('skillArea')} | {g.get('title')}")
    print(f"   has_instructions: {has_inst}, has_audio: {has_audio}, has_story: {has_story}")
    qs = g.get('questions', [])
    for q in qs[:2]:
        print(f"   Q: {q.get('prompt')[:60]}... -> Opts: {q.get('options')}")
