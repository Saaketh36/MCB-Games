import json
import re

with open('skill_areas_data.json', 'r', encoding='utf-8', errors='replace') as f:
    skills = json.load(f)

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

def clean_str(s):
    if not s: return ''
    s = s.replace('â€“', '–').replace('\u00e2\u20ac\u201c', '–')
    return re.sub(r'[\s\-_–—]+', ' ', s).strip().lower()

def clean_class(c):
    if not c: return ''
    return c.replace('Class', '').strip()

cat_by_name = {clean_str(c.get('title')): c for c in catalog}

mismatches = []
missing_in_catalog = []

for i, s in enumerate(skills):
    s_name = clean_str(s.get('activityName'))
    s_type = s.get('gameType')
    matched = cat_by_name.get(s_name)
    if not matched:
        s_cls = clean_class(s.get('class'))
        s_subj = s.get('subject')
        s_act = clean_str(s.get('activity'))
        for c in catalog:
            if clean_class(c.get('class')) == s_cls and c.get('subject') == s_subj and clean_str(c.get('activity')) == s_act:
                matched = c
                break
    if not matched:
        missing_in_catalog.append((i, s))
    else:
        c_type = matched.get('gameType')
        if s_type != c_type:
            mismatches.append({
                'class': s.get('class'),
                'subject': s.get('subject'),
                'skillArea': s.get('skillArea'),
                'activityName': s.get('activityName'),
                'catalogTitle': matched.get('title'),
                'skillType': s_type,
                'catalogType': c_type,
                'id': matched.get('id')
            })

print(f"Total skills: {len(skills)}")
print(f"Missing in catalog: {len(missing_in_catalog)}")
if missing_in_catalog:
    for item in missing_in_catalog[:5]:
        print("Missing:", item)
print(f"Mismatches between skill_areas_data and catalog: {len(mismatches)}")
for m in mismatches:
    print(m)
