"""Spot-check specific entries that were reported wrong, and the image rule."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

text = open(os.path.join(ROOT, "question_bank.js"), encoding="utf-8").read()
bank = json.loads(text[text.index("{"):text.rindex("}") + 1])

CHECKS = [
    "What is a good posture for presenting?",
    "Which is the correct way to begin addressing an audience?",
    "While giving a speech, where should you look?",
    "How should you adjust your volume in a small room compared with a hall?",
    "How many days are there in 3 weeks?",
    "How many kilograms are there in 1 tonne?",
    "A rectangle is 5 cm by 4 cm. What is its area?",
    "How many degrees are there in a full turn?",
    "A triangle with no equal sides is called",
    "Which organ pumps blood around the body?",
    "Which map colour usually shows a forest?",
    "What comes next: 1, 2, 4, 8, ___?",
]

print("=" * 74)
print("SPOT CHECKS")
print("=" * 74)
for needle in CHECKS:
    found = False
    for entry in bank.values():
        for q in entry.get("questions", []):
            if q["question"].endswith(needle):
                opts = [o.split(": ", 1)[-1] for o in q["options"]]
                ans = q["answer"].split(": ", 1)[-1]
                print(f"\nQ: {needle}")
                print(f"   options : {opts}")
                print(f"   answer  : {ans}")
                found = True
                break
        if found:
            break
    if not found:
        print(f"\nQ: {needle}\n   NOT FOUND")

print()
print("=" * 74)
print("IMAGE RULE  (Class I and II must have no picture questions)")
print("=" * 74)
for cls in ("Class I", "Class II", "Class III"):
    with_img = sum(1 for k, v in bank.items()
                   if k.startswith(cls + "|||")
                   for q in v["questions"] if q.get("image"))
    stories = sum(1 for k, v in bank.items()
                  if k.startswith(cls + "|||") and v.get("audio_script"))
    print(f"{cls:<10} listening activities: {stories:>3}   questions with image: {with_img}")

total_img = sum(1 for v in bank.values() for q in v["questions"] if q.get("image"))
print(f"\ntotal questions with image: {total_img}")