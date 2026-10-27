import json

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open('question_bank.js', 'r', encoding='utf-8') as f:
    text = f.read()
qb = json.loads(text[len("const QUESTION_BANK = "):].rstrip(';\n '))

with open('tools/stories.json', 'r', encoding='utf-8-sig') as f:
    stories = json.load(f)

print(f"Catalog games: {len(catalog)}")
print(f"QB entries: {len(qb)}")
print(f"Stories entries: {len(stories)}")

# How many catalog games can we enrich with context right now?
can_enrich_listening = 0
for g in catalog:
    title = g['title']
    title_alt = title.replace(' – ', ' - ')
    title_alt2 = title.replace(' - ', ' – ')
    
    # check in stories
    s_match = stories.get(title) or stories.get(title_alt) or stories.get(title_alt2)
    # check in qb
    qb_match = None
    for k, v in qb.items():
        if title in k or title_alt in k or title_alt2 in k:
            qb_match = v
            break
            
    has_script = bool((s_match and s_match.get('story')) or (qb_match and qb_match.get('audio_script')))
    if has_script:
        can_enrich_listening += 1

print(f"Catalog games that have audio/story context available: {can_enrich_listening}")
