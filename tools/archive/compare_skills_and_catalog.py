import json

skills = json.load(open('skill_areas_data.json', encoding='utf-8'))
catalog = json.load(open('full_games_catalog.json', encoding='utf-8'))

print(f"Total skills entries: {len(skills)}")
print(f"Total catalog entries: {len(catalog)}")

cat_map = {(c['class'], c['subject'], c['activity']): c for c in catalog}

# Let's check each skill entry
anomalies = []
for i, s in enumerate(skills):
    cls = s.get('class', '').replace('Class ', '')
    sub = s.get('subject')
    act = s.get('activity')
    act_name = s.get('activityName')
    gt = s.get('gameType')
    c = cat_map.get((cls, sub, act))
    if not c:
        anomalies.append(('Not found in catalog', i, s))
    elif gt == '' or gt in ('Mathematics', 'Science'):
        anomalies.append(('Shifted/Empty gameType', i, s, c['title'], c['gameType']))

print(f"Total anomalies: {len(anomalies)}")
for a in anomalies[:15]:
    print(a)
