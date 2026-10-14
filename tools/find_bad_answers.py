"""
Find question-bank entries whose stated correct answer looks wrong.

Two signals are used:

1. explanation names a distractor   - the `why` text repeats one of the
   distractors but never mentions the term, so the term is probably not the
   intended answer.
2. near-duplicate option           - the term and a distractor say almost the
   same thing, which makes the question ambiguous.

Run:  python tools\\find_bad_answers.py [ClassPrefix]
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


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    flagged = []

    for (subject, skill), facts in FACT_BANK.items():
        for i, f in enumerate(facts):
            term = f["t"]
            why = f["w"]
            distractors = list(f["d"])
            tags = []

            why_low = why.lower()
            term_low = term.lower().strip("'\"")
            if term_low and term_low not in why_low:
                for d in distractors:
                    dl = str(d).lower().strip("'\"")
                    core = " ".join(norm(d))
                    if dl and dl in why_low:
                        tags.append(f"explanation names distractor {d!r}")
                        break
                    if len(core) > 12 and core in re.sub(r"[^a-z0-9 ]", " ", why_low):
                        tags.append(f"explanation echoes distractor {d!r}")
                        break

            for d in distractors:
                if similarity(term, d) >= 0.72:
                    tags.append(f"near-duplicate option {d!r} (sim {similarity(term, d):.2f})")
                    break

            if tags:
                flagged.append((subject, skill, i, term, f["q"], tags))

    if only:
        flagged = [f for f in flagged if f[1].lower().startswith(only.lower())
                   or f[2] == only]

    print(f"flagged entries: {len(flagged)}")
    print()
    for subject, skill, i, term, question, tags in flagged:
        print(f"[{subject} / {skill}] #{i}")
        print(f"  term     : {term}")
        print(f"  question : {question}")
        for t in tags:
            print(f"  FLAG     : {t}")
        print()


if __name__ == "__main__":
    main()