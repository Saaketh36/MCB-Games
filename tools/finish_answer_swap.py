"""
Completes the term/distractor swap started by repair_answers.py.

repair_answers.py replaced the stated term with the option the explanation
identifies as correct, but left that option in the distractor list as well, so
those calls now list the correct answer twice and F() asserts. The original
(wrong) term for each affected entry is read back from bad_answers.txt, which
recorded "stated term" before the swap.

Result for each repaired entry:
    F(<correct answer>, q, (<original wrong answer>, ...), why)

Run:  python tools\\finish_answer_swap.py [--dry]
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TARGET = os.path.join(ROOT, "question_content.py")
REPORT = os.path.join(ROOT, "tools", "bad_answers.txt")

BLOCK_RE = re.compile(r'^FACT_BANK\[\("([^"]+)",\s*"([^"]+)"\)\]\s*=\s*\[')
HEAD_RE = re.compile(r"^\[([^\]]+?)\]\s*#(\d+)\s*$")
TERM_RE = re.compile(r"^\s*stated term\s*:\s*(.*)$")


def read_original_terms():
    """Map (subject, skill, index) -> the term that was stated before the swap."""
    original = {}
    subject = skill = None
    if not os.path.exists(REPORT):
        return original

    # PowerShell redirection writes UTF-16, Python writes UTF-8.
    raw = open(REPORT, "rb").read()
    enc = "utf-16" if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else "utf-8"
    for line in raw.decode(enc, errors="replace").splitlines():
        head = HEAD_RE.match(line.rstrip())
        if head:
            left = head.group(1)
            if "/" in left:
                subject, skill = [p.strip() for p in left.split("/", 1)]
            original[(subject, skill, int(head.group(2)))] = None
            continue
        term = TERM_RE.match(line.rstrip())
        if term and subject is not None:
            value = term.group(1).strip()
            for key in original:
                if original[key] is None and key[0] == subject and key[1] == skill:
                    original[key] = value
                    break
    return {k: v for k, v in original.items() if v}


def literals(text):
    return [x or y for x, y in re.findall(r'"([^"]*)"|\'([^\']*)\'', text)]


def main():
    dry = "--dry" in sys.argv
    originals = read_original_terms()
    if not originals:
        raise SystemExit(f"no original terms found in {REPORT}")

    lines = open(TARGET, encoding="utf-8").readlines()
    block, counts, fixed, missed = None, {}, 0, []

    for idx, line in enumerate(lines):
        m = BLOCK_RE.match(line)
        if m:
            block = (m.group(1), m.group(2))
            counts[block] = 0
            continue
        if block is None:
            continue
        if line.strip().startswith("]"):
            block = None
            continue
        if not re.match(r"^\s*F\(", line):
            continue

        n = counts[block]
        counts[block] = n + 1
        old = originals.get((block[0], block[1], n))
        if old is None:
            continue

        # The correct answer is now the stated term; find it among the
        # distractors and put the original wrong term back in its place.
        d_start = line.find("(")
        if d_start == -1:
            continue
        head, _, rest = line.partition("(")
        d_items = literals(rest)
        if not d_items:
            continue

        lit = re.match(r"^\s*F\(\s*(\"[^\"]*\"|'[^']*')", line)
        if not lit:
            continue
        term = (lit.group(1)[1:-1])

        if term not in d_items:
            continue
        new_items = [old if it == term else it for it in d_items]
        tail = rest
        for it, rep in zip(d_items, new_items):
            tail = tail.replace(f'"{it}"', f'@@{rep}@@', 1) if it == term else tail
        tail = re.sub(r'"@@(.*?)@@"', lambda mm: '"' + mm.group(1) + '"', tail)

        new_line = head + "(" + tail
        if not dry:
            lines[idx] = new_line
        fixed += 1
        if not dry and n < 3 and block[1] in ("Speaking",):
            print(f"  {block} #{n}: term {term!r} <- {old!r}")

    print(f"entries completed: {fixed}")
    if fixed != len(originals):
        missed = len(originals) - fixed
        print(f"note: {missed} report entries had no duplicate to repair")

    if not dry:
        open(TARGET, "w", encoding="utf-8").writelines(lines)


if __name__ == "__main__":
    main()