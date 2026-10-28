# -*- coding: utf-8 -*-
"""
Regenerate content/class-I.js through content/class-VIII.js strictly from the 440 learning outcomes in 'skillAreaOutcomes - Sheet1.pdf'.
"""
import json
import os

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

classes = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']

os.makedirs('content', exist_ok=True)

for cls in classes:
    cls_games = [g for g in catalog if g['class'] == cls]
    content_map = {}
    
    for g in cls_games:
        lo = g['learningOutcome']
        gt = g['gameType']
        title = g['title']
        sub = g['subSkillArea']
        
        # Convert questions to play.html format
        questions_fmt = []
        for q in g['questions']:
            questions_fmt.append({
                "q": q['prompt'],
                "options": q['options'],
                "answer": q['answer'],
                "explain": q['explanation']
            })
            
        game_obj = {
            "title": title,
            "desc": lo,
            "subSkill": sub,
            "questions": questions_fmt
        }
        
        # Key by LO ID and title
        content_map[g['id']] = game_obj
        # Also key by outcomeId
        content_map[str(g['outcomeId'])] = game_obj
    
    js_content = f"// Game content for Class {cls} derived STRICTLY from 'skillAreaOutcomes - Sheet1.pdf'\n"
    js_content += "window.GAME_CONTENT = window.GAME_CONTENT || {};\n"
    js_content += f"Object.assign(window.GAME_CONTENT, {json.dumps(content_map, indent=2, ensure_ascii=False)});\n"
    
    file_path = f"content/class-{cls}.js"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"Updated {file_path} with {len(cls_games)} activities.")

print("All class content files updated successfully!")
