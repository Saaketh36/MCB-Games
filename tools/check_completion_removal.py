"""
Verify a finished game disappears from the student's list.

Checks the completion filter against the real assignments: completing a game
hides it, it stays hidden after a reload, another student still sees it, and
clearing the records brings it back.
"""
import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from games_data import CURRICULUM_DATA  # noqa: E402

TMP = tempfile.mkdtemp()
ASSIGN = os.path.join(TMP, "assignments.json")
DONE = os.path.join(TMP, "completions.json")

failures = []


def check(label, cond):
    print(f"  {'PASS' if cond else 'FAIL'}  {label}")
    if not cond:
        failures.append(label)


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return []
    return data if isinstance(data, list) else []


def save(path, items):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(items, fh, ensure_ascii=False, indent=1)


def hidden(class_name, activity, completions, who):
    return any(c.get("class") == class_name
               and c.get("activity") == activity
               and c.get("student") == who
               for c in completions)


# Two Class I English games, as a teacher would assign them.
pool = [a for a in CURRICULUM_DATA
        if a["class"] == "Class I" and a["subject"] == "English"][:2]
assignments = [{"class": a["class"], "subject": a["subject"],
                "skill_area": a["skill_area"],
                "sub_skill_area": a["sub_skill_area"],
                "activity": a["activity_name"], "game_type": a["game_type"],
                "assigned_by": "Teacher"} for a in pool]
save(ASSIGN, assignments)

a0, a1 = assignments[0]["activity"], assignments[1]["activity"]
print(f"assigned: {a0} | {a1}\n")

print("BEFORE ANY COMPLETION")
save(DONE, [])
done = load(DONE)
check("both games visible to the student",
      not hidden("Class I", a0, done, "ravi") and not hidden("Class I", a1, done, "ravi"))

print("\nAFTER RAVI FINISHES THE FIRST GAME")
save(DONE, [{"student": "ravi", "display_name": "Ravi", "class": "Class I",
             "subject": "English", "activity": a0, "points": 20, "total_q": 3, "right": 2}])
done = load(DONE)
check("finished game hidden", hidden("Class I", a0, done, "ravi"))
check("unfinished game still visible", not hidden("Class I", a1, done, "ravi"))

print("\nAFTER A RELOAD (simulated by re-reading the file)")
done = load(DONE)
check("still hidden after reload", hidden("Class I", a0, done, "ravi"))

print("\nANOTHER STUDENT IN THE SAME CLASS")
check("other student still sees the game", not hidden("Class I", a0, done, "meera"))
check("other student sees unfinished too", not hidden("Class I", a1, done, "meera"))

print("\nSAME ACTIVITY IN A DIFFERENT CLASS IS UNAFFECTED")
check("class I completion does not hide another class's copy",
      not hidden("Class VI", a0, done, "ravi"))

print("\nTEACHER CLEARS THE RECORDS")
save(DONE, [])
done = load(DONE)
check("game returns after clearing", not hidden("Class I", a0, done, "ravi"))

print("\nNO COMPLETIONS FILE AT ALL")
if os.path.exists(DONE):
    os.remove(DONE)
check("missing file is treated as empty", load(DONE) == [])
check("everything still visible", not hidden("Class I", a0, load(DONE), "ravi"))

print("\nCORRUPTED FILE IS SURVIVED")
with open(DONE, "w", encoding="utf-8") as fh:
    fh.write("{not valid json")
check("corrupt file falls back to empty list", load(DONE) == [])

print()
if failures:
    print(f"FAILURES: {len(failures)}")
    for f in failures:
        print("  -", f)
    raise SystemExit(1)
print("OK - completed games are removed and stay removed")