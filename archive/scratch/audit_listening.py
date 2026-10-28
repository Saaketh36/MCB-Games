import json

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open('question_bank.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = "const QUESTION_BANK = "
raw_json = text[len(prefix):].rstrip(';\n ')
qb = json.loads(raw_json)

# Check games by skillArea
listening_games = [g for g in catalog if g.get('skillArea') == 'Listening']
print(f"Total Listening games in catalog: {len(listening_games)}")
for g in listening_games:
    print(f"- [{g['id']}] Class {g['class']} | {g['title']} | gameType: {g.get('gameType')}")
    # find in qb
    qb_match = None
    for k, v in qb.items():
        if g['title'] in k or g['title'].replace(' – ', ' - ') in k or g['title'].replace(' - ', ' – ') in k:
            qb_match = v
            break
    if qb_match:
        has_audio_script = bool(qb_match.get('audio_script'))
        has_story = bool(qb_match.get('story'))
        has_instr = bool(qb_match.get('instructions'))
        print(f"    QB match found: audio_script={has_audio_script}, story={has_story}, instructions={has_instr}")
        if has_audio_script:
            print(f"    audio_script: {qb_match['audio_script'][:80]}...")
    else:
        print("    NO QB MATCH FOUND!")

