import json

with open('skill_areas_data.json', 'r', encoding='utf-8') as f:
    skills = json.load(f)

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Build map from catalog title to catalog game
cat_map = {g['title']: g for g in catalog}

mismatches = []
for s in skills:
    t = s.get('activityName')
    g = cat_map.get(t)
    if not g:
        # try fuzzy
        for gt, gentry in cat_map.items():
            if t.replace(' – ', ' - ') == gt.replace(' – ', ' - '):
                g = gentry
                break
    if g:
        if s.get('gameType') != g.get('gameType'):
            mismatches.append((t, s.get('gameType'), g.get('gameType')))

print(f"Mismatches between skill_areas_data.json and full_games_catalog.json: {len(mismatches)}")
for m in mismatches[:10]:
    print(m)
