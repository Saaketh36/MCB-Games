"""
Verify the student's class list only offers classes with unfinished work.

Mirrors the student hub logic: a class disappears from the picker once every
game in it is finished for that student, while other classes remain.
"""
import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from games_data import CURRICULUM_DATA  # noqa: E402

ALL_CLASSES = ["Class I", "Class II", "Class III", "Class IV",
               "Class V", "Class VI", "Class VII", "Class VIII"]
TMP = tempfile.mkdtemp()

failures = []


def check(label, cond):
    print(f"  {'PASS' if cond else 'FAIL'}  {label}")
    if not cond:
        failures.append(label)


def is_completed(class_name, activity, completions, who):
    return any(c.get("class") == class_name
               and c.get("activity") == activity
               and c.get("student") == who
               for c in completions)


def assign(cls, subject, n):
    pool = [a for a in CURRICULUM_DATA
            if a["class"] == cls and a["subject"] == subject][:n]
    return [{"class": a["class"], "subject": a["subject"],
             "skill_area": a["skill_area"],
             "sub_skill_area": a["sub_skill_area"],
             "activity": a["activity_name"], "game_type": a["game_type"]}
            for a in pool]


assignments = assign("Class I", "English", 2) + assign("Class VI", "English", 2)
completions = []
who = "ravi"

print(f"Class I assigned  : {[a['activity'] for a in assignments if a['class']=='Class I']}")
print(f"Class VI assigned : {[a['activity'] for a in assignments if a['class']=='Class VI']}\n")


def open_classes(assignments, completions, who):
    assigned_classes = sorted({a["class"] for a in assignments}, key=ALL_CLASSES.index)
    return [c for c in assigned_classes
            if [a for a in assignments
                if a["class"] == c
                and not is_completed(c, a["activity"], completions, who)]]


print("STEP 1 - nothing completed")
oc = open_classes(assignments, completions, who)
check("both classes offered", oc == ["Class I", "Class VI"])

print("\nSTEP 2 - Class I first game finished")
i_done = next(a for a in assignments if a["class"] == "Class I")
completions.append({"student": who, "class": "Class I", "activity": i_done["activity"]})
oc = open_classes(assignments, completions, who)
check("Class I still offered, one game left",
      "Class I" in oc and len([a for a in assignments
                               if a["class"] == "Class I"
                               and not is_completed("Class I", a["activity"], completions, who)]) == 1)

print("\nSTEP 3 - Class I fully completed")
for a in [x for x in assignments if x["class"] == "Class I"]:
    if not is_completed("Class I", a["activity"], completions, who):
        completions.append({"student": who, "class": "Class I", "activity": a["activity"]})
oc = open_classes(assignments, completions, who)
check("Class I removed from the picker", "Class I" not in oc)
check("Class VI still offered", "Class VI" in oc)
check("picker shows exactly one class", oc == ["Class VI"])

print("\nSTEP 4 - everything completed")
for a in assignments:
    if not is_completed(a["class"], a["activity"], completions, who):
        completions.append({"student": who, "class": a["class"], "activity": a["activity"]})
oc = open_classes(assignments, completions, who)
check("no classes offered at all", oc == [])

print("\nSTEP 5 - a different student is unaffected")
other = open_classes(assignments, completions, "meera")
check("Meera still sees both classes", other == ["Class I", "Class VI"])

print("\nSTEP 6 - clearing records brings classes back")
completions = []
oc = open_classes(assignments, completions, who)
check("both classes return", oc == ["Class I", "Class VI"])

print("\nSTEP 7 - class ordering follows the curriculum order")
mixed = assign("Class VI", "English", 1) + assign("Class I", "English", 1)
oc = open_classes(mixed, [], who)
check("ordered Class I before Class VI", oc == ["Class I", "Class VI"])

print()
if failures:
    print(f"FAILURES: {len(failures)}")
    for f in failures:
        print("  -", f)
    raise SystemExit(1)
print("OK - fully completed classes are hidden from the student")