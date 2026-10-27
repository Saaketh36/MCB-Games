import json

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

context_needed = []
for g in catalog:
    qs = g.get('questions', [])
    prompts = " ".join([q.get('prompt', '') for q in qs])
    has_ctx = bool(g.get('audio_script') or g.get('story') or g.get('instructions') or g.get('passage'))
    
    # Check if questions refer to specific context
    indicators = ['according to', 'in the story', 'first step', 'second step', 'third step', 'tube a', 'experiment', 'passage', 'speaker', 'announcement', 'listen', 'audio', 'character', 'twee', 'barnaby', 'which step', 'what step', 'procedure', 'order']
    needs_ctx = any(ind in prompts.lower() for ind in indicators) or g.get('skillArea') in ['Listening', 'Reading'] or g.get('gameType') in ['Sequence Order', 'Reading Comprehension']
    
    context_needed.append({
        'id': g.get('id'),
        'title': g.get('title'),
        'class': g.get('class'),
        'subject': g.get('subject'),
        'skillArea': g.get('skillArea'),
        'gameType': g.get('gameType'),
        'has_ctx': has_ctx,
        'needs_ctx': needs_ctx,
        'has_audio_script': bool(g.get('audio_script')),
        'has_story': bool(g.get('story')),
        'has_instructions': bool(g.get('instructions')),
        'has_passage': bool(g.get('passage'))
    })

print(f"Total games: {len(catalog)}")
print(f"Games with context already in catalog: {sum(1 for c in context_needed if c['has_ctx'])}")
print(f"Games that need context: {sum(1 for c in context_needed if c['needs_ctx'])}")

missing = [c for c in context_needed if c['needs_ctx'] and not c['has_ctx']]
print(f"Missing context count: {len(missing)}")
for m in missing[:30]:
    print(f"  [{m['id']}] {m['class']} {m['subject']} | {m['skillArea']} | {m['gameType']} | {m['title']}")
