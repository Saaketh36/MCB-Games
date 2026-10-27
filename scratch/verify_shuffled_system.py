# -*- coding: utf-8 -*-
"""
Verification Script: Audits the newly randomized answer positions and upgraded distractors.
"""

import os
import sys
import json
from collections import Counter

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def verify():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    catalog_path = os.path.join(root, 'full_games_catalog.json')

    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    print("--- 1. Catalog & Answer Distribution Audit ---")
    print(f"Total games in catalog: {len(catalog)}")
    assert len(catalog) == 440

    all_answers = []
    triples = 0

    for g in catalog:
        assert len(g['questions']) == 3
        game_ans = [q['answer'] for q in g['questions']]
        if game_ans[0] == game_ans[1] == game_ans[2]:
            triples += 1
        for q in g['questions']:
            ans = q['answer']
            assert ans in (0, 1, 2, 3), f"Invalid answer index {ans}"
            all_answers.append(ans)
            # Verify options
            assert len(q['options']) == 4
            assert len(set(q['options'])) == 4, f"Duplicate options: {q['options']}"
            assert len(q['options'][ans]) > 0, "Empty correct option"

    counts = Counter(all_answers)
    letters = ['A', 'B', 'C', 'D']
    print(f"Total questions audited: {len(all_answers)}")
    print("Answer distribution:")
    for pos in range(4):
        cnt = counts[pos]
        pct = (cnt / len(all_answers)) * 100
        print(f"  Option {letters[pos]} (index {pos}): {cnt} questions ({pct:.2f}%)")
        assert cnt == 330, f"Expected 330 for option {letters[pos]}, got {cnt}"

    print(f"Games with all 3 answers identical: {triples} (0 is ideal)")
    assert triples == 0

    print("\n--- 2. Detailed Inspection of Game #96 (User's Cited Example) ---")
    g96 = next(g for g in catalog if g['outcomeId'] == 96)
    print(f"Title: {g96['title']}")
    print(f"Story: {g96['story']}")
    for q_idx, q in enumerate(g96['questions']):
        ans_idx = q['answer']
        ans_letter = letters[ans_idx]
        print(f"\n  Question {q_idx + 1}: {q['prompt']}")
        for opt_i, opt in enumerate(q['options']):
            tag = f"[CORRECT - Option {letters[opt_i]}]" if opt_i == ans_idx else f"[Option {letters[opt_i]}]"
            print(f"    {tag}: {opt}")
        print(f"    Correct Answer: Option {ans_letter} ({q['options'][ans_idx]})")
        print(f"    Explanation: {q['explanation']}")

    print("\n--- 3. Checking Sample Games Across Grades ---")
    sample_ids = [1, 53, 119, 171, 219, 240, 261, 264, 324, 413, 439]
    for sid in sample_ids:
        gm = next(x for x in catalog if x['outcomeId'] == sid)
        ans_letters = [letters[q['answer']] for q in gm['questions']]
        print(f"Outcome #{sid:3d} (Class {gm['class']:>4s} | {gm['subject']:<14s}): Answers = {ans_letters}")

    print("\nALL AUDITS & CHECKS PASSED FLAWLESSLY!")

if __name__ == '__main__':
    verify()
