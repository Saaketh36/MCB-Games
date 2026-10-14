"""Check the instruction lists reach the payload for instruction-style games."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from games_data import CURRICULUM_DATA          # noqa: E402
from listening_content import LISTENING_STORIES  # noqa: E402

text = open(os.path.join(ROOT, "question_bank.js"), encoding="utf-8").read()
bank = json.loads(text[text.index("{"):text.rindex("}") + 1])

by_name = {v["title"]: v for v in bank.values() if v.get("title")}

print("INSTRUCTION LISTS IN THE PAYLOAD")
found = 0
for title, entry in sorted(by_name.items()):
    steps = entry.get("instructions") or []
    if not steps:
        continue
    found += 1
    act = next((a for a in CURRICULUM_DATA if a["activity_name"] == title), {})
    print(f"\n{title}   ({act.get('class','?')} {act.get('subject','?')})")
    print(f"  audio: {entry.get('audio')}  ({entry.get('audio_seconds')}s)")
    for i, s in enumerate(steps, 1):
        print(f"    {i}. {s}")
    # every step should be traceable to the passage
    story = entry.get("audio_script", "").lower()
    missing = [s for s in steps
               if s.split()[0].lower() not in story
               and s.split()[0].lower() not in ("take", "record")]
    if missing:
        print(f"  note: first word not found in passage for {missing}")

print(f"\nactivities carrying an instruction list: {found}")
plain = sum(1 for v in bank.values() if v.get("audio_script") and not v.get("instructions"))
print(f"listening activities without one (normal): {plain}")

# The specific activity the teacher asked about
key = "Listen & Do Adventure"
e = by_name.get(key)
print(f"\n{key}:")
print(f"  steps   : {len(e.get('instructions') or [])}")
print(f"  audio   : {e.get('audio')}")
print(f"  seconds : {e.get('audio_seconds')}")
print(f"  questions: {len(e['questions'])}")