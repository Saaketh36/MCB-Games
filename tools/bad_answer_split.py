"""
Split the bad-answer flags into strong and weak signals.

Strong: the explanation repeats a distractor but never mentions the stated
term, which means the term is not the intended answer.
Weak: the term and a distractor are merely similar, which may just be two
valid ways of saying the same thing.

Run:  python tools\\bad_answer_split.py
"""
import difflib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from question_content import FACT_BANK  # noqa: E402


def norm(text):
    return re.sub(r"[^a-z0-9 ]", " ", str(text).lower()).split()


def similarity(a, b):
    return difflib.SequenceMatcher(None, " ".join(norm(a)), " ".join(norm(b))).ratio()


def why_says(why, term, distractors):
    why_flat = re.sub(r"[^a-z0-9 ]", " ", why.lower())
    why_flat = " ".join(why_flat.split())
    term_flat = " ".join(norm(term))
    if term_flat and term_flat in why_flat:
        return None
    for d in distractors:
        d_flat = " ".join(norm(d))
        if d_flat and d_flat in why_flat:
            return str(d)
    return None


def main():
    strong, weak = [], []
    for (subject, skill), facts in FACT_BANK.items():
        for i, f in enumerate(facts):
            term, why, ds = f["t"], f["w"], list(f["d"])
            hit = why_says(why, term, ds)
            if hit:
                strong.append((subject, skill, i, term, hit, f["q"], why))
                continue
            for d in ds:
                if similarity(term, d) >= 0.72:
                    weak.append((subject, skill, i, term, str(d),
                                 similarity(term, d), f["q"]))
                    break

    print(f"STRONG (explanation names a distractor): {len(strong)}")
    for subject, skill, i, term, hit, q, why in strong:
        print(f"\n[{subject} / {skill}] #{i}")
        print(f"  stated term : {term}")
        print(f"  why implies : {hit}")
        print(f"  question    : {q}")
        print(f"  why         : {why}")
    print()
    print(f"WEAK (near-duplicate options): {len(weak)}")
    for subject, skill, i, term, d, sim, q in weak:
        print(f"  [{subject} / {skill}] #{i} sim={sim:.2f}  {term!r} vs {d!r}")


if __name__ == "__main__":
    main()