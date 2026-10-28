import json
import re

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open('question_bank.js', 'r', encoding='utf-8') as f:
    text = f.read()
qb = json.loads(text[len("const QUESTION_BANK = "):].rstrip(';\n '))

with open('tools/stories.json', 'r', encoding='utf-8-sig') as f:
    stories = json.load(f)

import sys
sys.path.append('.')
import listening_content

print("Auditing context sources...")

enriched_count = 0
for g in catalog:
    title = g['title']
    title_alt1 = title.replace(' – ', ' - ')
    title_alt2 = title.replace(' - ', ' – ')
    
    # 1. Check listening_content.LISTENING_STORIES
    ls = (listening_content.LISTENING_STORIES.get(title) or 
          listening_content.LISTENING_STORIES.get(title_alt1) or 
          listening_content.LISTENING_STORIES.get(title_alt2))
    
    # 2. Check tools/stories.json
    st = (stories.get(title) or 
          stories.get(title_alt1) or 
          stories.get(title_alt2))
          
    # 3. Check question_bank.js
    qb_item = None
    for k, v in qb.items():
        k_clean = k.replace(' – ', ' - ')
        if title_alt1 in k_clean:
            qb_item = v
            break
            
    # Gather fields
    audio_script = ""
    story = ""
    instructions = []
    audio_file = ""
    
    if ls:
        if ls.get('story'): story = ls['story']
        if ls.get('instructions'): instructions = ls['instructions']
    if st:
        if st.get('story') and not story: story = st['story']
        if st.get('audio'): audio_file = st['audio']
    if qb_item:
        if qb_item.get('audio_script'): audio_script = qb_item['audio_script']
        if qb_item.get('instructions') and not instructions: instructions = qb_item['instructions']
        if qb_item.get('audio') and not audio_file: audio_file = qb_item['audio']
        
    # If audio_script is empty but story is present, audio_script = story
    if not audio_script and story:
        audio_script = story
    if not story and audio_script:
        story = audio_script
        
    if audio_script or story or instructions:
        enriched_count += 1
        print(f"[{g['id']}] Class {g['class']} | {g['title']} | script_len={len(audio_script)}, instr_len={len(instructions)}, audio={audio_file}")

print(f"\nTotal enriched activities: {enriched_count}")
