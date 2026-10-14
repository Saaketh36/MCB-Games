"""
Second pass: find entries where the stated term contradicts the question.

The first detector relied on the explanation naming the answer. Plenty of
entries have a general explanation instead, so a wrong term slips through. This
pass looks for the opposite pattern: a question that asks what is good, best,
should or must be used, answered with something clearly negative.

Run:  python tools\\find_contradictions.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from question_content import FACT_BANK  # noqa: E402

ASKS_GOOD = re.compile(
    r"\b(good|best|should|must|appropriate|suitable|best practice|ideal|"
    r"most useful|most suitable|recommend|advise|useful)\b", re.I)

NEGATIVE = re.compile(
    r"\b(not|never|no|none|nothing|cannot|can't|won't|slouch\w*|shout\w*|"
    r"refus\w*|random|wrong|louder|floor|guess|ignore\w*|interrupt\w*|"
    r"folding your arms|back turned|same volume everywhere|look out|"
    r"pointing|fault|harm\w*|damage\w*|waste\w*|drop\w*|mis\w*|"
    r"break\w*|sell\w*|paint them)\b", re.I)


def main():
    hits = []
    for (subject, skill), facts in FACT_BANK.items():
        for i, f in enumerate(facts):
            q = f["q"]
            term = str(f["t"])
            if not ASKS_GOOD.search(q):
                continue
            m = NEGATIVE.search(term)
            if not m:
                continue
            # Skip when the negative word also appears in the question stem,
            # which usually means the option is quoting the question.
            if NEGATIVE.search(q):
                continue
            hits.append((subject, skill, i, term, q, f["d"], m.group(0)))

    print(f"possible contradictions: {len(hits)}\n")
    for subject, skill, i, term, q, ds, word in hits:
        print(f"[{subject} / {skill}] #{i}   (negative word: {word!r})")
        print(f"  term     : {term}")
        print(f"  question : {q}")
        print(f"  distract : {list(ds)}")
        print()


if __name__ == "__main__":
    main()