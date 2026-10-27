import json
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('.')
import listening_content

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

with open('question_bank.js', 'r', encoding='utf-8') as f:
    text = f.read()
qb = json.loads(text[len("const QUESTION_BANK = "):].rstrip(';\n '))

with open('tools/stories.json', 'r', encoding='utf-8-sig') as f:
    stories = json.load(f)

# Step procedure definitions for Following Instructions / Sequence Order games
EXPLICIT_INSTRUCTIONS = {
    "Follow the Steps Race – Class VIII": [
        "First, label three clean test tubes A, B and C.",
        "Next, pour five millilitres of distilled water into each tube.",
        "Then add universal indicator: 1 drop to tube A, 2 drops to tube B, and 3 drops to tube C.",
        "After that, swirl each tube gently and compare the colours with the chart.",
        "Finally, record the matching colour and pH value for each tube in your notebook."
    ],
    "Follow the Steps Race - Class VIII": [
        "First, label three clean test tubes A, B and C.",
        "Next, pour five millilitres of distilled water into each tube.",
        "Then add universal indicator: 1 drop to tube A, 2 drops to tube B, and 3 drops to tube C.",
        "After that, swirl each tube gently and compare the colours with the chart.",
        "Finally, record the matching colour and pH value for each tube in your notebook."
    ],
    "Follow the Steps Race": [
        "First, take a rectangular sheet of paper and fold it in half the long way.",
        "Next, fold the top corners down to make a triangle.",
        "Then press the sides together to form a hull.",
        "After that, fold the bottom points upwards on both sides.",
        "Last, pull the two sides apart gently and your paper boat will float."
    ],
    "Listen & Do Adventure": [
        "First, open your book to page five.",
        "Next, draw a small blue star next to the heading.",
        "Then read the three sentences aloud.",
        "After that, circle the picture of a red bus.",
        "Last, close your book and wait for the bell."
    ],
    "Mission Control Orders": [
        "First, collect three empty bottles and two lids from the store room.",
        "Next, carry them to the laboratory on the first floor.",
        "Then wash each bottle and let them dry in the sun.",
        "After that, label each bottle with your team number.",
        "Finally, report to the science teacher when you are ready."
    ],
    "Simon Says Challenge – Class VI": [
        "Simon says: touch your nose.",
        "Simon says: clap three times.",
        "Simon says: stand on your left foot.",
        "Jump three times! (Nobody said Simon says!)",
        "Simon says: count backwards from ten to five."
    ],
    "Announcement Detective": [
        "Announcement starts: Welcome children to the morning announcement.",
        "The science exhibition will be held on Friday in the main hall.",
        "Classes 4 to 8 must set up models by 9:00 AM.",
        "The judges will arrive at 10:00 AM.",
        "Visitors may enter the main hall from 11:00 AM."
    ],
    "Announcement Detective – Class VII": [
        "Attention passengers: Platform 4 will be in use for Rajdhani Express.",
        "The train will depart from platform 4 at 7:25 in the evening.",
        "Coaches S7 and S8 will be attached at the rear.",
        "Passengers holding confirmed tickets should board now.",
        "The last door closes five minutes before departure."
    ],
    "Listen & Repeat Lab": [
        "Step 1: Say each tongue twister slowly.",
        "Step 2: Say it again faster.",
        "Step 3: Record yourself the first time.",
        "Step 4: Record yourself the fifth time.",
        "Step 5: Compare the two recordings."
    ],
    "Slide Prep Step Order": [
        "Step 1: Place a clean glass slide on a flat work surface.",
        "Step 2: Add a single drop of water or stain to the center of the slide.",
        "Step 3: Carefully place the specimen into the drop with forceps.",
        "Step 4: Lower the cover slip at a 45-degree angle to avoid air bubbles.",
        "Step 5: Blot any excess liquid gently with filter paper."
    ]
}

# Enrich catalog
updated_count = 0
for g in catalog:
    title = g['title']
    title_alt1 = title.replace(' – ', ' - ')
    title_alt2 = title.replace(' - ', ' – ')
    
    ls = (listening_content.LISTENING_STORIES.get(title) or 
          listening_content.LISTENING_STORIES.get(title_alt1) or 
          listening_content.LISTENING_STORIES.get(title_alt2))
    
    st = (stories.get(title) or 
          stories.get(title_alt1) or 
          stories.get(title_alt2))
          
    qb_item = None
    for k, v in qb.items():
        k_clean = k.replace(' – ', ' - ')
        if title_alt1 in k_clean:
            qb_item = v
            break
            
    audio_script = ""
    story = ""
    instructions = []
    audio_file = ""
    
    if ls:
        if ls.get('story'): story = ls['story']
        if ls.get('instructions'): instructions = list(ls['instructions'])
    if st:
        if st.get('story') and not story: story = st['story']
        if st.get('audio'): audio_file = st['audio']
    if qb_item:
        if qb_item.get('audio_script'): audio_script = qb_item['audio_script']
        if qb_item.get('instructions') and not instructions: instructions = list(qb_item['instructions'])
        if qb_item.get('audio') and not audio_file: audio_file = qb_item['audio']
        
    # Check explicit instructions
    for key, inst_list in EXPLICIT_INSTRUCTIONS.items():
        if key.replace(' – ', ' - ') == title_alt1:
            instructions = inst_list
            break
            
    if not audio_script and story: audio_script = story
    if not story and audio_script: story = audio_script
    
    if audio_script:
        g['audio_script'] = audio_script
        g['story'] = story
        if instructions:
            g['instructions'] = instructions
        if audio_file:
            g['audio'] = audio_file
        updated_count += 1

print(f"Enriched {updated_count} games with context in catalog.")

# Also verify Reading Comprehension gameType in catalog & skills
with open('skill_areas_data.json', 'r', encoding='utf-8') as f:
    skills_data = json.load(f)

# Sync gameType from catalog to skills_data
cat_gt_map = {g['title']: g['gameType'] for g in catalog}
cat_gt_map.update({g['title'].replace(' – ', ' - '): g['gameType'] for g in catalog})

synced_skills = 0
for s in skills_data:
    t = s['activityName']
    t_clean = t.replace(' – ', ' - ')
    if t in cat_gt_map and s['gameType'] != cat_gt_map[t]:
        print(f"Syncing skill {t}: {s['gameType']} -> {cat_gt_map[t]}")
        s['gameType'] = cat_gt_map[t]
        synced_skills += 1
    elif t_clean in cat_gt_map and s['gameType'] != cat_gt_map[t_clean]:
        print(f"Syncing skill {t}: {s['gameType']} -> {cat_gt_map[t_clean]}")
        s['gameType'] = cat_gt_map[t_clean]
        synced_skills += 1

print(f"Synced {synced_skills} skill entries.")

# Write back full_games_catalog.json
with open('full_games_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

# Write back full_games_catalog.js
js_content = f"// Full Games Catalog for MyClassboard Games Platform\n// 325 Curriculum Games with Full Multi-Modal Question Bank & Context\n\nconst FULL_GAMES_CATALOG = {json.dumps(catalog, indent=2, ensure_ascii=False)};\n\nif (typeof window !== 'undefined') {{\n    window.FULL_GAMES_CATALOG = FULL_GAMES_CATALOG;\n    window.GamesCatalog = FULL_GAMES_CATALOG;\n}}\n"
with open('full_games_catalog.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

# Write back skill_areas_data.json
with open('skill_areas_data.json', 'w', encoding='utf-8') as f:
    json.dump(skills_data, f, indent=2, ensure_ascii=False)

print("SUCCESS: Saved full_games_catalog.json, full_games_catalog.js, and skill_areas_data.json!")
