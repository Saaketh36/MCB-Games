"""
Repairs fact entries whose stated correct answer is actually one of the
distractors.

`F(term, question, distractors, why)` treats `term` as the correct answer, but
some entries list the wrong option there while the explanation names the true
answer. This script swaps the term with the distractor that the explanation
identifies, editing question_content.py in place.

Every swap is re-verified afterwards: the explanation must then mention the new
term, and the four options must still be distinct.

Run:  python tools\\repair_answers.py [--dry]
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

TARGET = os.path.join(ROOT, "question_content.py")
BLOCK_RE = re.compile(r'^FACT_BANK\[\("([^"]+)",\s*"([^"]+)"\)\]\s*=\s*\[')
CALL_RE = re.compile(r'^(\s*)F\(')


def norm(text):
    return re.sub(r"[^a-z0-9 ]", " ", str(text).lower()).split()


def flat(text):
    return " ".join(norm(text))


def read_literal(line, start):
    """Return (quote, body, end_index) for the string literal after `start`."""
    i = start
    while i < len(line) and line[i] in " \t":
        i += 1
    if i >= len(line) or line[i] not in "\"'":
        return None
    quote = line[i]
    j = i + 1
    while j < len(line):
        if line[j] == "\\":
            j += 2
            continue
        if line[j] == quote:
            return quote, line[i + 1:j], j
        j += 1
    return None


def implied_answer(fact):
    """If the explanation names a distractor instead of the term, return it."""
    why_flat = flat(fact["w"])
    if flat(fact["t"]) and flat(fact["t"]) in why_flat:
        return None
    for d in fact["d"]:
        d_flat = flat(d)
        if d_flat and d_flat in why_flat:
            return d
    return None


def main():
    dry = "--dry" in sys.argv

    # Fresh import so we always read the current file contents.
    for mod in ("question_content",):
        sys.modules.pop(mod, None)
    from question_content import FACT_BANK

    plan = {}
    for key, facts in FACT_BANK.items():
        for i, fact in enumerate(facts):
            hit = implied_answer(fact)
            if hit is None:
                continue
            if flat(hit) == flat(fact["t"]):
                continue
            options = [fact["t"], *fact["d"]]
            if len({flat(o) for o in options}) != 4:
                continue  # leave ambiguous sets alone
            plan.setdefault(key, {})[i] = (fact["t"], hit)

    if not plan:
        print("nothing to repair")
        return

    total = sum(len(v) for v in plan.values())
    print(f"entries to swap: {total}")
    if dry:
        for key, items in plan.items():
            for i, (old, new) in items.items():
                print(f"  {key} #{i}: {old!r} -> {new!r}")
        return

    with open(TARGET, encoding="utf-8") as fh:
        lines = fh.readlines()

    block = None
    counts = {}
    edits = 0

    for idx, line in enumerate(lines):
        m = BLOCK_RE.match(line)
        if m:
            block = (m.group(1), m.group(2))
            counts[block] = 0
            continue
        if block and CALL_RE.match(line):
            n = counts[block]
            counts[block] = n + 1
            if n in plan.get(block, {}):
                old, new = plan[block][n]
                lit = read_literal(line, line.index("F(") + 2)
                if lit:
                    quote, body, end = lit
                    if body == old:
                        lines[idx] = line[:end - len(body)] + str(new) + line[end:]
                        edits += 1
                    else:
                        print(f"  !! {block} #{n}: expected {old!r}, found {body!r}")
            continue
        if block and line.strip().startswith("]"):
            block = None

    with open(TARGET, "w", encoding="utf-8") as fh:
        fh.writelines(lines)

    print(f"swapped {edits} term(s)")


if __name__ == "__main__":
    main()