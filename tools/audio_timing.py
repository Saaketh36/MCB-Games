"""Report narration duration vs the 11-15s target window."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from listening_content import LISTENING_STORIES  # noqa: E402

LO, HI = 11.0, 15.0
WPM = 155.0

rows = []
for slug, meta in json.load(open(os.path.join(ROOT, "audio", "index.json"), encoding="utf-8"))["stories"].items():
    entry = next((v for v in LISTENING_STORIES.values() if v.get("audio") == f"audio/{slug}.wav"), None)
    words = len(entry["story"].split()) if entry else meta["words"]
    rows.append((slug, meta["seconds"], words))

rows.sort(key=lambda r: r[1])
print(f'{"story":40}{"sec":>7}{"words":>7}{"need":>7}  flag')
for slug, sec, words in rows:
    est = words / WPM * 60.0
    flag = 'OK' if LO <= sec <= HI else ('SHORT' if sec < LO else 'LONG')
    print(f'{slug:40}{sec:7.2f}{words:7}{est:7.1f}  {flag}')

secs = [r[1] for r in rows]
bad = [r for r in rows if not (LO <= r[1] <= HI)]
print()
print(f'min {min(secs):.2f}  max {max(secs):.2f}  avg {sum(secs)/len(secs):.2f}')
print(f'outside {LO}-{HI}s: {len(bad)}')
for slug, sec, words in bad:
    target_words = round((LO + HI) / 2 * WPM / 60.0)
    print(f'  {slug:40} {sec:6.2f}s  {words:3}w  -> aim ~{target_words}w')