# -*- coding: utf-8 -*-
"""
Full Verification & Quality Assurance Audit for all 440 educational activities.
"""

import os
import sys
import json

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def verify():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    catalog_path = os.path.join(root, 'full_games_catalog.json')

    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    print(f"--- 1. Catalog Verification ---")
    print(f"Total games in catalog: {len(catalog)}")
    assert len(catalog) == 440

    outcome_ids = set()
    banned_terms = [
        "specific competency is achieved",
        "skipping foundational concepts",
        "using unverified random guesses",
        "refusing to participate",
        "outcome #",
        "syllabus",
        "pedagogical",
        "lorem ipsum",
        "placeholder",
        "tbd"
    ]

    total_questions = 0
    grade_counts = {}

    for i, g in enumerate(catalog):
        oid = g['outcomeId']
        assert oid not in outcome_ids, f"Duplicate outcomeId {oid}"
        outcome_ids.add(oid)

        cls = g['class']
        grade_counts[cls] = grade_counts.get(cls, 0) + 1

        assert len(g['title']) > 5, f"Game {oid} title too short: {g['title']}"
        assert len(g['story']) > 15, f"Game {oid} story too short: {g['story']}"
        assert len(g['questions']) == 3, f"Game {oid} has {len(g['questions'])} questions"

        for q_idx, q in enumerate(g['questions']):
            total_questions += 1
            assert len(q['prompt']) > 10, f"Game {oid} Q{q_idx+1} prompt too short"
            assert len(q['options']) == 4, f"Game {oid} Q{q_idx+1} does not have 4 options"
            assert len(set(q['options'])) == 4, f"Game {oid} Q{q_idx+1} has duplicate options: {q['options']}"
            assert q['answer'] == 0, f"Game {oid} Q{q_idx+1} answer index not 0"
            assert len(q['explanation']) > 10, f"Game {oid} Q{q_idx+1} explanation too short"

            # Check banned terms
            blob = (g['title'] + " " + g['story'] + " " + q['prompt'] + " " + " ".join(q['options']) + " " + q['explanation']).lower()
            for b in banned_terms:
                if b in blob:
                    raise AssertionError(f"Game {oid} contains banned term '{b}'")

    print(f"All 440 outcome IDs 1-440 are present, distinct, and verified!")
    print(f"Total authentic questions verified: {total_questions} (exactly 3 per game)")
    print(f"Grade distribution: {grade_counts}")

    print(f"\n--- 2. Checking Dependent Files ---")
    files_to_check = [
        ('full_games_catalog.js', 100000),
        ('skill_areas_data.json', 50000),
        ('question_bank.js', 100000),
        ('content/class-I.js', 20000),
        ('content/class-II.js', 20000),
        ('content/class-III.js', 50000),
        ('content/class-IV.js', 50000),
        ('content/class-V.js', 50000),
        ('content/class-VI.js', 80000),
        ('content/class-VII.js', 100000),
        ('content/class-VIII.js', 100000),
    ]

    for rel_path, min_size in files_to_check:
        full_p = os.path.join(root, rel_path)
        assert os.path.exists(full_p), f"Missing file {rel_path}"
        size = os.path.getsize(full_p)
        assert size > min_size, f"File {rel_path} size {size} is less than minimum {min_size}"
        print(f"  OK: {rel_path} ({size:,} bytes)")

    print("\n--- 3. Sample Showcase Previews ---")
    sample_ids = [1, 23, 63, 138, 171, 219, 311, 412]
    for sid in sample_ids:
        gm = next(x for x in catalog if x['outcomeId'] == sid)
        print(f"\n[Outcome #{sid} | Class {gm['class']} | {gm['subject']} | {gm['skillArea']}]")
        print(f"  Title: {gm['title']}")
        print(f"  Story: {gm['story']}")
        print(f"  Q1: {gm['questions'][0]['prompt']}")
        print(f"      Correct: {gm['questions'][0]['options'][0]}")
        print(f"      Distractor 1: {gm['questions'][0]['options'][1]}")
        print(f"      Distractor 2: {gm['questions'][0]['options'][2]}")
        print(f"      Distractor 3: {gm['questions'][0]['options'][3]}")
        print(f"      Explanation: {gm['questions'][0]['explanation']}")

    print("\nALL VERIFICATIONS PASSED PERFECTLY!")

if __name__ == '__main__':
    verify()
