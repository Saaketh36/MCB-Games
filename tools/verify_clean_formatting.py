#!/usr/bin/env python3
"""
Verification Script for Strict Clean-Formatting Rules (No Answer Leaks):
1. No math operators or formulas leaked in question stems.
2. All options clean, matching in format, without parenthetical calculations or proofs.
3. Proofs and working out separated entirely into the explanation field.
"""

import json
import re
import glob
import sys
import os

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, 'reconfigure'):
        stream.reconfigure(encoding='utf-8', errors='replace')

# Formula leak pattern in options
OPT_LEAK_RE = re.compile(
    r'\s*\([^)]*(?:[₹$]?\d+[^)]*[\+\-\*\/\=x×÷][^)]*(?:\d+|side|length|width)|[\+\-\*\/\=x×÷]\s*\d+)[^)]*\)',
    re.IGNORECASE
)

# Formula leak pattern in question stems (e.g. calculation hint at end or before question mark)
PROMPT_LEAK_RE = re.compile(
    r'\s*\([^)]*\d+\s*[\+\-\*\/\=x×÷]\s*[\d\w]+[^)]*\)\s*(\?|$)',
    re.IGNORECASE
)

def verify_catalog(fpath='full_games_catalog.json'):
    print(f"\n[1] Verifying {fpath}...")
    with open(fpath, 'r', encoding='utf-8') as f:
        games = json.load(f)

    prompt_leaks = 0
    option_leaks = 0
    total_questions = 0

    for g in games:
        for q in g.get('questions', []):
            total_questions += 1
            prompt = q.get('prompt', '') or q.get('question', '')
            if PROMPT_LEAK_RE.search(prompt):
                print(f"  ❌ PROMPT LEAK in {g.get('id')}: {prompt}")
                prompt_leaks += 1
            for opt in q.get('options', []):
                if OPT_LEAK_RE.search(opt):
                    print(f"  ❌ OPTION LEAK in {g.get('id')}: {opt}")
                    option_leaks += 1

    print(f"  Checked {len(games)} activities, {total_questions} questions.")
    if prompt_leaks == 0 and option_leaks == 0:
        print(f"  ✅ {fpath} is 100% CLEAN! 0 leaks found.")
        return True
    else:
        print(f"  ❌ {fpath} has {prompt_leaks} prompt leaks and {option_leaks} option leaks.")
        return False

def verify_content_classes():
    print("\n[2] Verifying content/class-*.js files...")
    all_ok = True
    for cfile in sorted(glob.glob('content/class-*.js')):
        with open(cfile, 'r', encoding='utf-8') as f:
            text = f.read()

        brace_start = text.find('{', text.find('Object.assign'))
        brace_end = text.rfind('}')
        if brace_start == -1 or brace_end == -1:
            continue

        try:
            data = json.loads(text[brace_start:brace_end + 1])
        except Exception as e:
            print(f"  ❌ JSON parse error in {cfile}: {e}")
            all_ok = False
            continue

        prompt_leaks = 0
        option_leaks = 0
        total_q = 0

        for act_id, act in data.items():
            for q in act.get('questions', []):
                total_q += 1
                prompt = q.get('q', '')
                if PROMPT_LEAK_RE.search(prompt):
                    print(f"  ❌ PROMPT LEAK in {cfile} [{act_id}]: {prompt}")
                    prompt_leaks += 1
                for opt in q.get('options', []):
                    if OPT_LEAK_RE.search(opt):
                        print(f"  ❌ OPTION LEAK in {cfile} [{act_id}]: {opt}")
                        option_leaks += 1

        if prompt_leaks == 0 and option_leaks == 0:
            print(f"  ✅ {cfile} ({total_q} questions): 0 leaks.")
        else:
            print(f"  ❌ {cfile}: {prompt_leaks} prompt leaks, {option_leaks} option leaks.")
            all_ok = False

    return all_ok

def verify_question_bank():
    print("\n[3] Verifying question_bank.js...")
    with open('question_bank.js', 'r', encoding='utf-8') as f:
        text = f.read()

    mod_idx = text.find('if (typeof module')
    end_idx = text[:mod_idx].rfind('}') if mod_idx != -1 else text.rfind('}')
    start_idx = text.index('{')

    data = json.loads(text[start_idx:end_idx + 1])
    prompt_leaks = 0
    option_leaks = 0
    total_q = 0

    for act_key, act in data.items():
        for q in act.get('questions', []):
            total_q += 1
            p = q.get('prompt', '') or q.get('question', '')
            if PROMPT_LEAK_RE.search(p):
                print(f"  ❌ PROMPT LEAK in question_bank [{act_key}]: {p}")
                prompt_leaks += 1
            for opt in q.get('options', []):
                if OPT_LEAK_RE.search(opt):
                    print(f"  ❌ OPTION LEAK in question_bank [{act_key}]: {opt}")
                    option_leaks += 1

    if prompt_leaks == 0 and option_leaks == 0:
        print(f"  ✅ question_bank.js ({total_q} questions): 0 leaks.")
        return True
    else:
        print(f"  ❌ question_bank.js: {prompt_leaks} prompt leaks, {option_leaks} option leaks.")
        return False

def main():
    print("=" * 60)
    print("STRICT CLEAN-FORMATTING VERIFICATION SUITE")
    print("=" * 60)
    r1 = verify_catalog('full_games_catalog.json')
    r2 = verify_content_classes()
    r3 = verify_question_bank()

    print("\n" + "=" * 60)
    if r1 and r2 and r3:
        print("🎉 ALL CHECKS PASSED! NO ANSWER OR FORMULA LEAKS DETECTED.")
        print("=" * 60)
        return 0
    else:
        print("⚠️ SOME CHECKS FAILED.")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
