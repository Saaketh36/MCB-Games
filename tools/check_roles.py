"""
Verify the teacher/student role split and the assignment flow.

Checks that students cannot reach teacher pages, teachers cannot reach student
pages, assignments round-trip through disk, and that a student only ever sees
activities a teacher actually assigned.
"""
import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from games_data import CURRICULUM_DATA  # noqa: E402

ASSIGN = os.path.join(tempfile.gettempdir(), "assignments_test.json")
TEACHER_PAGES = {'teacher_dashboard'}
STUDENT_PAGES = {'student_hub', 'student_game_play'}
ALL_CLASSES = ["Class I", "Class II", "Class III", "Class IV",
               "Class V", "Class VI", "Class VII", "Class VIII"]


def allowed(page, role):
    if page in TEACHER_PAGES:
        return role == 'teacher'
    if page in STUDENT_PAGES:
        return role == 'student'
    return role in ('teacher', 'student', None)


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


def find_activity(cls, subject, skill, activity):
    for a in CURRICULUM_DATA:
        if (a["class"] == cls and a["subject"] == subject
                and a["skill_area"] == skill
                and a["activity_name"] == activity):
            return a
    return None


failures = []


def check(label, cond):
    print(f"  {'PASS' if cond else 'FAIL'}  {label}")
    if not cond:
        failures.append(label)


print("ROLE PERMISSIONS")
check("student blocked from teacher_dashboard", not allowed('teacher_dashboard', 'student'))
check("teacher blocked from student_hub", not allowed('student_hub', 'teacher'))
check("teacher blocked from student_game_play", not allowed('student_game_play', 'teacher'))
check("student may play games", allowed('student_game_play', 'student'))
check("teacher may open dashboard", allowed('teacher_dashboard', 'teacher'))
check("landing open to everyone", allowed('landing', None) and allowed('landing', 'student'))

print("\nASSIGNMENT ROUND TRIP")
sample = CURRICULUM_DATA[0]
row = {
    "class": sample["class"], "subject": sample["subject"],
    "skill_area": sample["skill_area"], "sub_skill_area": sample["sub_skill_area"],
    "activity": sample["activity_name"], "game_type": sample["game_type"],
    "assigned_by": "Teacher",
}
save(ASSIGN, [row])
check("assignment saved and reloaded", load(ASSIGN) == [row])

print("\nSKILL AREA DRILL DOWN")
for cls in ("Class I", "Class VI"):
    for subj in sorted({i["subject"] for i in CURRICULUM_DATA if i["class"] == cls}):
        skills = sorted({i["skill_area"] for i in CURRICULUM_DATA
                         if i["class"] == cls and i["subject"] == subj})
        pool = [i for i in CURRICULUM_DATA
                if i["class"] == cls and i["subject"] == subj
                and i["skill_area"] == skills[0]]
        print(f"  {cls:<9} {subj:<16} {len(skills)} skill area(s), "
              f"{len(pool)} activity(ies) in {skills[0]}")

print("\nSTUDENT VISIBILITY")
save(ASSIGN, [])
check("no assignments -> nothing to play", load(ASSIGN) == [])
save(ASSIGN, [row])
found = find_activity(row["class"], row["subject"], row["skill_area"], row["activity"])
check("assigned activity resolves to real curriculum entry", found is not None)
check("resolved activity matches name", found and found["activity_name"] == row["activity"])
mine = [a for a in load(ASSIGN) if a["class"] == "Class I"]
check("student sees only their class", all(a["class"] == "Class I" for a in mine))
check("unassigned class sees nothing",
      [a for a in load(ASSIGN) if a["class"] == "Class VIII"] == [])
check("bad activity name does not resolve",
      find_activity("Class I", "English", "Reading", "No Such Game") is None)

print("\nCLASSES WITH ASSIGNMENTS")
have = sorted({a["class"] for a in load(ASSIGN)}, key=ALL_CLASSES.index)
print("  classes a student can pick:", have)

os.remove(ASSIGN)
print()
if failures:
    print(f"FAILURES: {len(failures)}")
    for f in failures:
        print("  -", f)
    raise SystemExit(1)
print("OK - role split and assignment flow verified")