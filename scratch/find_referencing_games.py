import json
with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

print("Games with questions referencing steps/procedures/stories but missing context:")
for g in cat:
    if not (g.get('instructions') or g.get('audio_script') or g.get('story') or g.get('passage')):
        qs = g.get('questions', [])
        prompts = ' '.join([q.get('prompt', '') for q in qs])
        if any(w in prompts.lower() for w in ['first step', 'second step', 'according to', 'in the story', 'procedure', 'following steps', 'which step', 'tube', 'experiment']):
            print(f"  [{g['id']}] {g['class']} {g['subject']} | {g['title']} | {g['gameType']}")
            for q in qs[:2]:
                print(f"    -> {q.get('prompt')}")
