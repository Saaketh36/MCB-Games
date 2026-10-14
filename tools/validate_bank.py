"""
Validate the generated question bank and the listening assets.

Run:  python tools\\validate_bank.py
"""

import json
import os
import sys
import wave
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from games_data import CURRICULUM_DATA            # noqa: E402
from listening_content import LISTENING_STORIES    # noqa: E402


def load_bank():
    path = os.path.join(ROOT, "question_bank.js")
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    return json.loads(text[text.index("{"):text.rindex("}") + 1])


def main():
    problems = []
    bank = load_bank()

    expected = {f"{a['class']}|||{a['subject']}|||{a['activity_name']}"
                for a in CURRICULUM_DATA}
    if set(bank) != expected:
        problems.append(f"bank/curriculum mismatch: "
                        f"{len(expected - set(bank))} missing, {len(set(bank) - expected)} extra")

    stems = Counter()
    answers = Counter()
    letters = Counter()
    total_q = 0

    for key, entry in bank.items():
        questions = entry.get("questions") or []
        if not questions:
            problems.append(f"{key}: no questions")
        for q in questions:
            total_q += 1
            stem = q.get("question", "")
            stems[stem] += 1
            opts = q.get("options") or []
            ans = q.get("answer")
            if len(opts) != 4:
                problems.append(f"{key}: {len(opts)} options for {stem[:40]}")
            if ans not in opts:
                problems.append(f"{key}: answer not in options for {stem[:40]}")
            if len(set(opts)) != len(opts):
                problems.append(f"{key}: duplicate options for {stem[:40]}")
            if opts:
                letters["ABCD"[opts.index(ans)]] += 1
                answers[ans] += 1
        if not str(key).startswith(tuple(f"{c}|||" for c in (
                "Class I", "Class II", "Class III", "Class IV", "Class V",
                "Class VI", "Class VII", "Class VIII"))):
            problems.append(f"bad class key: {key}")

    dupes = [s for s, n in stems.items() if n > 1]

    # listening assets
    audio_ok = audio_missing = 0
    img_ok = img_missing = 0
    for name, entry in LISTENING_STORIES.items():
        for q in entry["questions"]:
            src = q.get("image")
            if not src:
                img_missing += 1
                problems.append(f"{name}: question without an image")
                continue
            path = os.path.join(ROOT, *src.split("/"))
            if not os.path.exists(path):
                img_missing += 1
                problems.append(f"{name}: missing image {src}")
                continue
            with open(path, encoding="utf-8") as fh:
                body = fh.read()
            draws = sum(body.count(f"<{tag}") for tag in
                        ("rect", "circle", "path", "ellipse", "polygon", "text"))
            if not body.rstrip().endswith("</svg>") or draws < 3:
                img_missing += 1
                problems.append(f"{name}: image looks empty ({src}, {draws} shapes)")
            else:
                img_ok += 1

    for name, entry in LISTENING_STORIES.items():
        src = entry.get("audio")
        if not src:
            audio_missing += 1
            problems.append(f"{name}: no audio file linked")
            continue
        path = os.path.join(ROOT, *src.split("/"))
        if not os.path.exists(path):
            audio_missing += 1
            problems.append(f"{name}: missing file {src}")
            continue
        try:
            with wave.open(path) as w:
                if w.getnframes() <= 0:
                    raise ValueError("empty")
            audio_ok += 1
        except Exception as exc:
            audio_missing += 1
            problems.append(f"{name}: unreadable wav ({exc})")
        if len(entry["questions"]) < 3:
            problems.append(f"{name}: only {len(entry['questions'])} questions")
        if len(entry["story"].split()) < 45:
            problems.append(f"{name}: story only {len(entry['story'].split())} words")

    print(f"activities          : {len(bank)}")
    print(f"questions           : {total_q}")
    print(f"unique stems        : {len(stems)}  (duplicates: {len(dupes)})")
    print(f"unique answer terms : {len(answers)}")
    print(f"answer key spread   : " +
          "  ".join(f"{k} {v / total_q:.1%}" for k, v in sorted(letters.items())))
    print(f"listening passages  : {len(LISTENING_STORIES)}  with audio: {audio_ok}")
    print(f"question images     : {img_ok}  (missing: {img_missing})")
    print()
    if dupes:
        print("duplicate stems:")
        for s in dupes[:10]:
            print("  ", s[:90])
        print()
    if problems:
        print(f"PROBLEMS: {len(problems)}")
        for p in problems[:25]:
            print("  -", p)
        return 1
    print("OK - no problems found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())