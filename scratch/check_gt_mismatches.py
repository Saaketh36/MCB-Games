import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open('skill_areas_data.json', 'r', encoding='utf-8') as f:
    skills = json.load(f)

# Map title to skill entry
skill_map = {}
for s in skills:
    skill_map[s['activityName']] = s

gt_mismatches = []
for g in catalog:
    s = skill_map.get(g['title'])
    if s:
        if g['gameType'] != s['gameType']:
            gt_mismatches.append({
                'id': g['id'],
                'title': g['title'],
                'catalog_gameType': g['gameType'],
                'skill_gameType': s['gameType']
            })

print(f"Mismatches between catalog and skill_areas: {len(gt_mismatches)}")
for m in gt_mismatches:
    print(m)
