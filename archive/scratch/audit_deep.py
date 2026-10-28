import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open('skill_areas_data.json', 'r', encoding='utf-8') as f:
    skills = json.load(f)

with open('question_bank.js', 'r', encoding='utf-8') as f:
    text = f.read()
qb = json.loads(text[len("const QUESTION_BANK = "):].rstrip(';\n '))

print("==================================================")
print("AUDITING ALL 325 GAMES FOR CONTEXT & GAMETYPE MATCH")
print("==================================================")

# A. Mismatches between skill_areas_data.json and full_games_catalog.json
skill_by_title = {s['activityName']: s for s in skills}
mismatches_gt = []
for g in catalog:
    s = skill_by_title.get(g['title'])
    if s and s['gameType'] != g['gameType']:
        mismatches_gt.append((g['id'], g['title'], g['gameType'], s['gameType']))

print(f"\nA. Mismatches between catalog gameType & skill_areas gameType: {len(mismatches_gt)}")
for m in mismatches_gt:
    print(f"  [{m[0]}] '{m[1]}': catalog={m[2]} vs skills={m[3]}")

# B. Activities that need context (Listening, Reading, Story, Procedure)
needs_context = []
for g in catalog:
    # Check if this is listening or reading or has story in QB
    is_listening = g.get('skillArea') == 'Listening'
    is_reading = g.get('skillArea') == 'Reading'
    
    # find in qb
    qb_item = None
    for k, v in qb.items():
        if g['title'].replace(' – ', ' - ') in k.replace(' – ', ' - '):
            qb_item = v
            break
            
    has_qb_script = bool(qb_item and qb_item.get('audio_script'))
    has_qb_story = bool(qb_item and qb_item.get('story'))
    has_qb_instr = bool(qb_item and qb_item.get('instructions'))
    
    catalog_has_context = bool(g.get('passage') or g.get('audio_script') or g.get('story') or g.get('instructions'))
    
    if (is_listening or has_qb_script or has_qb_story or has_qb_instr) and not catalog_has_context:
        needs_context.append({
            'id': g['id'],
            'title': g['title'],
            'class': g['class'],
            'skillArea': g['skillArea'],
            'activity': g['activity'],
            'gameType': g['gameType'],
            'has_qb_script': has_qb_script,
            'has_qb_instr': has_qb_instr
        })

print(f"\nB. Activities with missing context in catalog: {len(needs_context)}")
for item in needs_context:
    print(f"  [{item['id']}] Class {item['class']} | {item['title']} ({item['skillArea']} - {item['activity']}) [gameType: {item['gameType']}]")

# C. Activities by gameType and how they are handled
print("\nC. All GameTypes in Catalog:")
from collections import Counter
for gt, count in Counter(g['gameType'] for g in catalog).items():
    print(f"  {gt}: {count}")

