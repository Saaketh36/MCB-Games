import os
import json

if os.path.exists('tools/stories.json'):
    with open('tools/stories.json', 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    print("Stories in tools/stories.json:", len(data))
    for k in list(data.keys())[:5]:
        print(f"  {k}: {list(data[k].keys()) if isinstance(data[k], dict) else type(data[k])}")
        if isinstance(data[k], dict) and 'story' in data[k]:
            print("   story snippet:", data[k]['story'][:80])

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Find match between stories.json and catalog
matched = 0
for g in catalog:
    t = g.get('title')
    if t in data or t.replace(' – ', ' - ') in data or t.replace(' - ', ' – ') in data:
        matched += 1
print(f"Matched stories with catalog: {matched} / {len(data)}")
