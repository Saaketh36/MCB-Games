import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open('skill_areas_data.json', 'r', encoding='utf-8') as f:
    skills = json.load(f)

with open('question_bank.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = "const QUESTION_BANK = "
raw_json = text[len(prefix):].rstrip(';\n ')
qb = json.loads(raw_json)

print(f"Total catalog games: {len(catalog)}")
print(f"Total skill_areas entries: {len(skills)}")

# 1. Check Listening activities and audio_script
missing_audio = []
for g in catalog:
    # find in qb
    qb_entry = None
    for k, v in qb.items():
        title_norm = g['title'].replace(' – ', ' - ').strip()
        k_norm = k.replace(' – ', ' - ').strip()
        if title_norm in k_norm:
            qb_entry = v
            break
    if qb_entry and qb_entry.get('audio_script'):
        if not g.get('audio_script') and not g.get('story') and not g.get('passage'):
            missing_audio.append((g['id'], g['title'], g['class'], g['skillArea'], qb_entry['audio_script'][:60]))

print(f"\n1. Games with audio_script/story in QB but missing in catalog: {len(missing_audio)}")
for item in missing_audio:
    print(f"  [{item[0]}] Class {item[2]} | {item[1]} ({item[3]}): {item[4]}...")

# 2. Check games where skillArea == 'Listening'
listening_missing = []
for g in catalog:
    if g.get('skillArea') == 'Listening':
        has_context = bool(g.get('audio_script') or g.get('story') or g.get('passage'))
        if not has_context:
            listening_missing.append((g['id'], g['title'], g['class']))
print(f"\n2. Listening games with NO audio_script/story in catalog: {len(listening_missing)} / {len([g for g in catalog if g.get('skillArea') == 'Listening'])}")

# 3. Check Reading games with NO passage in catalog
reading_games = [g for g in catalog if g.get('skillArea') == 'Reading']
reading_missing = [g for g in reading_games if not g.get('passage')]
print(f"\n3. Reading games: total {len(reading_games)}, missing passage in catalog: {len(reading_missing)}")
for g in reading_missing:
    print(f"  [{g['id']}] Class {g['class']} | {g['title']}")

# 4. Check gameTypes across catalog
from collections import Counter
print(f"\n4. Catalog gameTypes: {Counter(g.get('gameType') for g in catalog)}")

# 5. Check questions type vs gameType
# E.g. gameType is 'Sequence Order', but questions are standard MCQ
seq_games = [g for g in catalog if g.get('gameType') == 'Sequence Order']
print(f"\n5. Sequence Order games count: {len(seq_games)}")
for g in seq_games[:5]:
    print(f"  [{g['id']}] {g['title']}: Q1={g['questions'][0]['prompt'] if g.get('questions') else 'None'}")
