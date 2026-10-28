# -*- coding: utf-8 -*-
"""
Master script to apply all question enhancements:
1. Clean brackets & explanatory giveaways across all 440 games.
2. Apply crafted balanced options for C1-C2, C3-C4, C5-C6, C7, C8.
3. Sync full_games_catalog.json to:
   - full_games_catalog.js
   - question_bank.js
   - content/class-I.js ... content/class-VIII.js
"""

import os
import sys
import json
import glob
import re

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, PROJECT_ROOT)

from tools.enhancers.clean_brackets import clean_option_giveaways

def master_apply():
    catalog_path = os.path.join(PROJECT_ROOT, 'full_games_catalog.json')
    with open(catalog_path, 'r', encoding='utf-8') as f:
        games = json.load(f)

    print(f"Loaded {len(games)} games from catalog.")

    # 1. Clean brackets and giveaways from all options
    cleaned_giveaways = 0
    for g in games:
        for q in g.get('questions', []):
            opts = q.get('options', [])
            new_opts = []
            for o in opts:
                co = clean_option_giveaways(o)
                if co != o:
                    cleaned_giveaways += 1
                new_opts.append(co)
            q['options'] = new_opts
    print(f"Step 1: Cleaned {cleaned_giveaways} parenthetical giveaways from options.")

    # 2. Apply C1-C2 enhancements
    from tools.enhancers.enhance_c1_c2 import apply_enhancements as apply_c1_c2
    c1_c2_count = apply_c1_c2(games)
    print(f"Step 2: Applied {c1_c2_count} Class I & II enhancements.")

    # 3. Apply C3-C4 enhancements if available
    try:
        from tools.enhancers.enhance_c3_c4 import apply_enhancements as apply_c3_c4
        c3_c4_count = apply_c3_c4(games)
        print(f"Step 3: Applied {c3_c4_count} Class III & IV enhancements.")
    except ImportError:
        print("Step 3: enhance_c3_c4 not ready yet.")

    # 4. Apply C5-C6 enhancements if available
    try:
        from tools.enhancers.enhance_c5_c6 import apply_enhancements as apply_c5_c6
        c5_c6_count = apply_c5_c6(games)
        print(f"Step 4: Applied {c5_c6_count} Class V & VI enhancements.")
    except ImportError:
        print("Step 4: enhance_c5_c6 not ready yet.")

    # 5. Apply C7 enhancements if available
    try:
        from tools.enhancers.enhance_c7 import apply_enhancements as apply_c7
        c7_count = apply_c7(games)
        print(f"Step 5: Applied {c7_count} Class VII enhancements.")
    except ImportError:
        print("Step 5: enhance_c7 not ready yet.")

    # 6. Apply C8 enhancements if available
    try:
        from tools.enhancers.enhance_c8 import apply_enhancements as apply_c8
        c8_count = apply_c8(games)
        print(f"Step 6: Applied {c8_count} Class VIII enhancements.")
    except ImportError:
        print("Step 6: enhance_c8 not ready yet.")

    # 7. Save full_games_catalog.json
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(games, f, indent=2, ensure_ascii=False)
    print(f"Saved {catalog_path}")

    # 8. Sync full_games_catalog.js
    js_catalog_path = os.path.join(PROJECT_ROOT, 'full_games_catalog.js')
    with open(js_catalog_path, 'w', encoding='utf-8') as f:
        f.write("// Authoritative Games Catalog derived STRICTLY from 'skillAreaOutcomes - Sheet1.pdf'\n")
        f.write("// Total Learning Outcomes / Activities: 440 (Classes I to VIII)\n")
        f.write("const FULL_GAMES_CATALOG = ")
        json.dump(games, f, indent=2, ensure_ascii=False)
        f.write(";\n\n")
        f.write("if (typeof window !== 'undefined') {\n")
        f.write("    window.FULL_GAMES_CATALOG = FULL_GAMES_CATALOG;\n")
        f.write("    window.GamesCatalog = FULL_GAMES_CATALOG;\n")
        f.write("}\n")
    print(f"Synced {js_catalog_path}")

    # 9. Sync question_bank.js
    qb_path = os.path.join(PROJECT_ROOT, 'question_bank.js')
    qb = {}
    for g in games:
        key = f"Class {g['class']}|||{g['subject']}|||{g['title']}"
        qb[key] = {
            "title": g['title'],
            "class": g['class'],
            "subject": g['subject'],
            "skillArea": g['skillArea'],
            "subSkillArea": g.get('subSkillArea', g.get('activity', '')),
            "learningOutcome": g.get('learningOutcome', g.get('desc', '')),
            "audio_script": g.get('audio_script', g.get('story', '')),
            "story": g.get('story', ''),
            "instructions": g.get('instructions', ''),
            "questions": g['questions']
        }
    with open(qb_path, 'w', encoding='utf-8') as f:
        f.write("// Authoritative Question Bank derived STRICTLY from 'skillAreaOutcomes - Sheet1.pdf'\n")
        f.write("const QUESTION_BANK = ")
        json.dump(qb, f, indent=2, ensure_ascii=False)
        f.write(";\n\n")
        f.write("if (typeof module !== 'undefined' && module.exports) module.exports = { QUESTION_BANK };\n")
    print(f"Synced {qb_path}")

    # 10. Sync content/class-*.js
    classes = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    for cls in classes:
        cls_games = [g for g in games if g['class'] == cls]
        content_map = {}
        for g in cls_games:
            q_fmt = []
            for q in g['questions']:
                q_fmt.append({
                    "q": q.get('prompt') or q.get('question'),
                    "options": q['options'],
                    "answer": q['answer'],
                    "explain": q.get('explanation', '')
                })
            item_obj = {
                "title": g['title'],
                "desc": g.get('learningOutcome', g.get('desc', '')),
                "subSkill": g.get('subSkillArea', g.get('activity', '')),
                "audio_script": g.get('audio_script', g.get('story', '')),
                "story": g.get('story', ''),
                "instructions": g.get('instructions', ''),
                "questions": q_fmt
            }
            content_map[g['id']] = item_obj
            content_map[str(g.get('outcomeId', ''))] = item_obj

        js_content = f"// Game content for Class {cls} derived STRICTLY from 'skillAreaOutcomes - Sheet1.pdf'\n"
        js_content += "window.GAME_CONTENT = window.GAME_CONTENT || {};\n"
        js_content += f"Object.assign(window.GAME_CONTENT, {json.dumps(content_map, indent=2, ensure_ascii=False)});\n"

        file_path = os.path.join(PROJECT_ROOT, 'content', f"class-{cls}.js")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print(f"Synced {file_path}")

    print("\nMASTER ENHANCEMENT PIPELINE COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    master_apply()

