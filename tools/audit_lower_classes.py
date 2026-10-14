"""Dump Class I and Class II content so it can be checked question by question."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from games_data import CURRICULUM_DATA          # noqa: E402
from listening_content import LISTENING_STORIES  # noqa: E402

text = open(os.path.join(ROOT, "question_bank.js"), encoding="utf-8").read()
bank = json.loads(text[text.index("{"):text.rindex("}") + 1])

only = sys.argv[1] if len(sys.argv) > 1 else "I,II"
classes = {"I": "Class I", "II": "Class II"}

for tag in only.split(","):
    cls = classes[tag.strip().upper()]
    rows = [(k, v) for k, v in bank.items() if k.startswith(cls + "|||")]
    print("=" * 78)
    print(f"{cls}   activities: {len(rows)}")
    print("=" * 78)
    for key, entry in sorted(rows):
        name = key.split("|||")[2]
        story = entry.get("audio_script", "")
        print(f"\n--- {key}")
        if story:
            print(f"    STORY: {story}")
        for i, q in enumerate(entry["questions"]):
            mark = "IMG" if q.get("image") else "   "
            print(f"    [{i}] {mark} {q['question']}")
            print(f"         options: {q['options']}")
            print(f"         answer : {q['answer']}")
    print()