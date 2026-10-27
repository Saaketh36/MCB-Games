# -*- coding: utf-8 -*-
"""
Master Build Script: Updates the full educational platform with child-appropriate,
curriculum-aligned activities for all 440 learning outcomes (Classes I through VIII).
Includes:
1. Balanced randomization of correct answer positions across A, B, C, and D (indices 0, 1, 2, 3)
   with exactly 25% distribution each, preventing guessing by position.
2. High-quality cognitive trap distractors (Detail Swaps, Common Misconceptions, Plausible Inferences).
3. Zero curriculum meta-talk, 3 authentic questions per game.
"""

import os
import sys
import json
import random
from collections import Counter

# Ensure generators package is discoverable
sys.path.insert(0, os.path.dirname(__file__))

from gen_primary_1_2 import PRIMARY_GAMES
from gen_class3 import CLASS3_GAMES
from gen_class4 import CLASS4_GAMES
from gen_class5 import CLASS5_GAMES
from gen_class6 import CLASS6_GAMES
from gen_class7 import CLASS7_GAMES
from gen_class8 import CLASS8_GAMES

def build_all():
    print("Combining educational activities from all 7 modules...")
    all_outcomes = {}
    all_outcomes.update(PRIMARY_GAMES)
    all_outcomes.update(CLASS3_GAMES)
    all_outcomes.update(CLASS4_GAMES)
    all_outcomes.update(CLASS5_GAMES)
    all_outcomes.update(CLASS6_GAMES)
    all_outcomes.update(CLASS7_GAMES)
    all_outcomes.update(CLASS8_GAMES)

    print(f"Total outcomes authored: {len(all_outcomes)}")
    assert len(all_outcomes) == 440, f"Expected 440 outcomes, but found {len(all_outcomes)}"

    # Check that all outcome IDs 1 to 440 are present
    missing = [i for i in range(1, 441) if i not in all_outcomes]
    if missing:
        raise ValueError(f"Missing outcome IDs: {missing}")

    # Load base catalog
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    catalog_path = os.path.join(root_dir, 'full_games_catalog.json')

    with open(catalog_path, 'r', encoding='utf-8') as f:
        games = json.load(f)

    print(f"Loaded {len(games)} games from {catalog_path}")
    assert len(games) == 440, f"Expected 440 games in catalog, found {len(games)}"

    # -------------------------------------------------------------
    # 1. Generate Balanced Answer Position Plan across all 440 games
    # -------------------------------------------------------------
    # Total 1,320 questions across 440 games (3 questions each)
    # Exactly 330 questions each for indices 0 (A), 1 (B), 2 (C), 3 (D) -> 25.0% each!
    rng = random.Random(20261027)
    positions_pool = [0, 1, 2, 3] * 330
    rng.shuffle(positions_pool)

    # Distribute into 440 games of 3 questions, avoiding all-identical positions within a single game
    games_positions = []
    pool_idx = 0
    for g_num in range(440):
        trio = positions_pool[pool_idx:pool_idx+3]
        pool_idx += 3
        # If all 3 are identical, swap the 3rd with a later different element in the pool
        while trio[0] == trio[1] == trio[2] and pool_idx < len(positions_pool):
            for swap_idx in range(pool_idx, len(positions_pool)):
                if positions_pool[swap_idx] != trio[0]:
                    positions_pool[pool_idx-1], positions_pool[swap_idx] = positions_pool[swap_idx], positions_pool[pool_idx-1]
                    trio = [trio[0], trio[1], positions_pool[pool_idx-1]]
                    break
        games_positions.append(trio)

    # Verify distribution
    all_assigned = [p for trio in games_positions for p in trio]
    counts = Counter(all_assigned)
    print("\nAnswer Position Distribution across 1,320 questions:")
    for pos in range(4):
        letter = chr(65 + pos)
        cnt = counts[pos]
        pct = (cnt / len(all_assigned)) * 100
        print(f"  Option {letter} (index {pos}): {cnt} questions ({pct:.2f}%)")

    # -------------------------------------------------------------
    # 2. Enrich and Shuffle Games
    # -------------------------------------------------------------
    enriched_games = []
    banned_meta_phrases = [
        "specific competency is achieved",
        "Skipping foundational concepts",
        "Using unverified random guesses",
        "Refusing to participate",
        "Outcome #",
        "Outcome 1:",
        "Outcome 2:",
        "Outcome 3:",
    ]

    for g_idx, g in enumerate(games):
        oid = g['outcomeId']
        auth = all_outcomes[oid]
        assigned_positions = games_positions[g_idx]

        # Validation and Shuffling
        questions = auth['questions']
        assert len(questions) == 3, f"Outcome {oid} has {len(questions)} questions instead of 3!"
        
        shuffled_questions = []
        for q_idx, q in enumerate(questions):
            assert 'prompt' in q and len(q['prompt']) > 10, f"Outcome {oid} Q{q_idx+1} missing prompt!"
            assert 'options' in q and len(q['options']) == 4, f"Outcome {oid} Q{q_idx+1} must have 4 options!"
            assert len(set(q['options'])) == 4, f"Outcome {oid} Q{q_idx+1} has duplicates: {q['options']}"
            assert 'explanation' in q and len(q['explanation']) > 10, f"Outcome {oid} Q{q_idx+1} missing explanation!"

            # Check banned phrases
            full_text = q['prompt'] + " " + " ".join(q['options']) + " " + q['explanation']
            for phrase in banned_meta_phrases:
                assert phrase.lower() not in full_text.lower(), f"Banned phrase '{phrase}' in Outcome {oid} Q{q_idx+1}!"

            # Target position for correct answer (0, 1, 2, or 3)
            target_pos = assigned_positions[q_idx]

            # In source authored games, index 0 is currently the correct answer
            # If q has already an answer index, use it, otherwise assume 0
            curr_answer_idx = q.get('answer', 0)
            correct_opt = q['options'][curr_answer_idx]
            distractors = [opt for i, opt in enumerate(q['options']) if i != curr_answer_idx]
            rng.shuffle(distractors)

            # Build shuffled options list with correct answer at target_pos
            new_options = [None] * 4
            new_options[target_pos] = correct_opt
            dist_ptr = 0
            for slot in range(4):
                if slot != target_pos:
                    new_options[slot] = distractors[dist_ptr]
                    dist_ptr += 1

            shuffled_questions.append({
                "prompt": q['prompt'],
                "options": new_options,
                "answer": target_pos,
                "explanation": q['explanation']
            })

        # Overwrite content fields
        g['title'] = auth['title']
        g['story'] = auth['story']
        g['audio_script'] = auth.get('audio_script', auth['story'])
        g['questions'] = shuffled_questions
        enriched_games.append(g)

    # 1. Save full_games_catalog.json
    with open(os.path.join(root_dir, 'full_games_catalog.json'), 'w', encoding='utf-8') as f:
        json.dump(enriched_games, f, indent=2, ensure_ascii=False)
    print("Saved full_games_catalog.json")

    # 2. Save full_games_catalog.js
    with open(os.path.join(root_dir, 'full_games_catalog.js'), 'w', encoding='utf-8') as f:
        f.write("// Authoritative Games Catalog derived STRICTLY from 'skillAreaOutcomes - Sheet1.pdf'\n")
        f.write("// Total Learning Outcomes / Activities: 440 (Classes I to VIII)\n")
        f.write("const FULL_GAMES_CATALOG = ")
        json.dump(enriched_games, f, indent=2, ensure_ascii=False)
        f.write(";\n\n")
        f.write("if (typeof window !== 'undefined') {\n")
        f.write("    window.FULL_GAMES_CATALOG = FULL_GAMES_CATALOG;\n")
        f.write("    window.GamesCatalog = FULL_GAMES_CATALOG;\n")
        f.write("}\n")
    print("Saved full_games_catalog.js")

    # 3. Save skill_areas_data.json
    skill_areas_data = []
    for g in enriched_games:
        skill_areas_data.append({
            "class": f"Class {g['class']}",
            "subject": g['subject'],
            "skillArea": g['skillArea'],
            "activity": g['subSkillArea'],
            "activityName": g['title'],
            "gameType": g['gameType'],
            "outcomeId": g['outcomeId'],
            "learningOutcome": g['learningOutcome']
        })

    with open(os.path.join(root_dir, 'skill_areas_data.json'), 'w', encoding='utf-8') as f:
        json.dump(skill_areas_data, f, indent=2, ensure_ascii=False)
    print("Saved skill_areas_data.json")

    # 4. Save question_bank.js
    qb = {}
    for g in enriched_games:
        key = f"Class {g['class']}|||{g['subject']}|||{g['title']}"
        qb[key] = {
            "title": g['title'],
            "class": g['class'],
            "subject": g['subject'],
            "skillArea": g['skillArea'],
            "subSkillArea": g['subSkillArea'],
            "learningOutcome": g['learningOutcome'],
            "audio_script": g['audio_script'],
            "story": g['story'],
            "instructions": g.get('instructions', ''),
            "questions": g['questions']
        }

    with open(os.path.join(root_dir, 'question_bank.js'), 'w', encoding='utf-8') as f:
        f.write("// Authoritative Question Bank derived STRICTLY from 'skillAreaOutcomes - Sheet1.pdf'\n")
        f.write("const QUESTION_BANK = ")
        json.dump(qb, f, indent=2, ensure_ascii=False)
        f.write(";\n\n")
        f.write("if (typeof module !== 'undefined' && module.exports) module.exports = { QUESTION_BANK };\n")
    print("Saved question_bank.js")

    # 5. Save content/class-*.js
    classes = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    for cls in classes:
        cls_games = [g for g in enriched_games if g['class'] == cls]
        content_map = {}
        for g in cls_games:
            q_fmt = []
            for q in g['questions']:
                q_fmt.append({
                    "q": q['prompt'],
                    "options": q['options'],
                    "answer": q['answer'],
                    "explain": q['explanation']
                })
            item_obj = {
                "title": g['title'],
                "desc": g['learningOutcome'],
                "subSkill": g['subSkillArea'],
                "audio_script": g['audio_script'],
                "story": g['story'],
                "instructions": g.get('instructions', ''),
                "questions": q_fmt
            }
            content_map[g['id']] = item_obj
            content_map[str(g['outcomeId'])] = item_obj

        js_content = f"// Game content for Class {cls} derived STRICTLY from 'skillAreaOutcomes - Sheet1.pdf'\n"
        js_content += "window.GAME_CONTENT = window.GAME_CONTENT || {};\n"
        js_content += f"Object.assign(window.GAME_CONTENT, {json.dumps(content_map, indent=2, ensure_ascii=False)});\n"

        file_path = os.path.join(root_dir, 'content', f"class-{cls}.js")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print(f"Saved {file_path} ({len(cls_games)} games)")

    print("\nSUCCESS: All 440 games successfully built with balanced randomized answer positions across platform!")

if __name__ == '__main__':
    build_all()
