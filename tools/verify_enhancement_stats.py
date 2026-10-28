import json
import re

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

bracket_opts = []
heavy_imbalance = []
total_q = 0

for g in games:
    for q in g.get('questions', []):
        total_q += 1
        opts = q.get('options', [])
        ans_idx = q.get('answer', 0)
        c = opts[ans_idx]
        distractors = [opts[i] for i in range(len(opts)) if i != ans_idx]
        if not distractors:
            continue
        
        # Check brackets
        for opt in opts:
            if '(' in opt or ')' in opt or '[' in opt or ']' in opt:
                bracket_opts.append((g['id'], opt))
                
        len_c = len(c)
        max_d = max(len(d) for d in distractors)
        avg_d = sum(len(d) for d in distractors) / len(distractors)
        
        # Heavy imbalance threshold: correct answer is > 1.4x max distractor and diff >= 15 chars
        if len_c > 1.4 * max_d and (len_c - max_d) >= 15:
            heavy_imbalance.append({
                'id': g['id'],
                'prompt': q.get('prompt') or q.get('question'),
                'correct': c,
                'distractors': distractors,
                'len_c': len_c,
                'max_d': max_d
            })

print(f"Total questions in catalog: {total_q}")
print(f"Questions with brackets in options: {len(bracket_opts)} (was 426!)")
print(f"Questions with heavy length imbalance: {len(heavy_imbalance)} (was 755!)")

if bracket_opts:
    print("\nRemaining bracket options sample:")
    for b in bracket_opts[:10]:
        print(f"  [{b[0]}] {b[1]}")

if heavy_imbalance:
    print("\nRemaining heavy imbalance sample:")
    for h in heavy_imbalance[:5]:
        print(f"  [{h['id']}] Q: {h['prompt']}")
        print(f"    Correct: {h['correct']} ({h['len_c']})")
        print(f"    Max Distractor: {max(h['distractors'], key=len)} ({h['max_d']})")
