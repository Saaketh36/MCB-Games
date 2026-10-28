"""
Fixes a hand-checked list of entries whose stated answer is wrong.

Each fix names a snippet of the question and the option that should be the
answer. The stated term and that option swap places, so the wrong answer stays
available as a distractor. An optional third field replaces a distractor that
was too similar to the correct answer.

Run:  python tools\\fix_known.py [--dry]
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "question_content.py")

LIT_RE = re.compile(r"\"([^\"]*)\"|'([^']*)'")

# (question snippet, correct answer, distractor to replace or None)
FIXES = [
    ("Which opening is most suitable when complaining",
     "I am writing to bring to your attention a fault in the item I purchased on Monday.",
     None),
    ("While giving a speech, where should you look?",
     "Look at the audience",
     None),
    ("What is a good posture for presenting?",
     "Stand straight",
     None),
    ("How should you adjust your volume in a small room",
     "Volume that matches the room",
     None),
    ("If a name is spelled out on the phone and sounds unclear",
     "Ask the speaker to spell it",
     "Ask for spelling"),
]


def literals(line):
    return [a or b for a, b in LIT_RE.findall(line)]


def replace_first(line, old, new):
    for m in LIT_RE.finditer(line):
        value = m.group(1) if m.group(1) is not None else m.group(2)
        if value == old:
            quote = m.group(0)[0]
            return line[:m.start()] + quote + new + quote + line[m.end():]
    return None


def main():
    dry = "--dry" in sys.argv
    lines = open(TARGET, encoding="utf-8").readlines()
    applied = 0

    for needle, correct, replace_d in FIXES:
        hit = None
        for i, line in enumerate(lines):
            if needle in line and literals(line):
                hit = i
                break
        if hit is None:
            print(f"  MISS: {needle[:50]}")
            continue

        term_line, d_line = hit - 1, hit + 1
        old_term = literals(lines[term_line])
        if not old_term:
            print(f"  MISS term line: {needle[:50]}")
            continue
        old_term = old_term[0]

        if correct not in literals(lines[d_line]):
            print(f"  MISS correct option not in distractors: {needle[:50]}")
            continue

        new_term_line = replace_first(lines[term_line], old_term, correct)
        new_d_line = replace_first(lines[d_line], correct, old_term)
        if replace_d:
            swapped = replace_first(new_d_line, replace_d, old_term)
            if swapped:
                new_d_line = swapped
        if new_term_line is None or new_d_line is None:
            print(f"  MISS rewrite: {needle[:50]}")
            continue

        print(f"  {needle[:46]:<46} {old_term!r} -> {correct!r}")
        if not dry:
            lines[term_line], lines[d_line] = new_term_line, new_d_line
        applied += 1

    print(f"\napplied: {applied}/{len(FIXES)}")
    if not dry and applied:
        open(TARGET, "w", encoding="utf-8").writelines(lines)


if __name__ == "__main__":
    main()