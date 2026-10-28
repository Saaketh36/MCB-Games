import json

# Load catalog
cat = json.load(open('full_games_catalog.json', encoding='utf-8'))
skills_raw = json.load(open('skill_areas_data.json', encoding='utf-8'))

# The skillArea name in skill_areas_data.json is "Measurement (Length, Weight, Capacity, Time)"
# Let's verify mapping for each of the 325 games
clean_data = []

roman_to_class = {
    'I': 'Class I',
    'II': 'Class II',
    'III': 'Class III',
    'IV': 'Class IV',
    'V': 'Class V',
    'VI': 'Class VI',
    'VII': 'Class VII',
    'VIII': 'Class VIII'
}

for c in cat:
    cls_roman = c['class']
    cls_name = roman_to_class[cls_roman]
    sub = c['subject']
    sa = c['skillArea']
    if 'Measurement' in sa:
        sa = 'Measurement (Length, Weight, Capacity, Time)'
    act = c['activity']
    act_name = c['title']
    gt = c['gameType']
    
    clean_data.append({
        'class': cls_name,
        'subject': sub,
        'skillArea': sa,
        'activity': act,
        'activityName': act_name,
        'gameType': gt
    })

print(f"Generated {len(clean_data)} clean entries.")
# Check unique skill areas
unique_sa = sorted(list(set(d['skillArea'] for d in clean_data)))
print(f"Total unique skill areas: {len(unique_sa)}")
raw_unique_sa = sorted(list(set(s['skillArea'] for s in skills_raw if s.get('skillArea'))))
print("Any new skill areas not in skill_areas_data?", set(unique_sa) - set(raw_unique_sa))

# Check game types
unique_gt = sorted(list(set(d['gameType'] for d in clean_data)))
print("Unique game types:", unique_gt)

# Save to cleaned file test
with open('tools/test_clean_skills.json', 'w', encoding='utf-8') as f:
    json.dump(clean_data, f, indent=2, ensure_ascii=False)
print("Saved tools/test_clean_skills.json successfully.")
