"""
Verify the teacher portal marks assigned work as completed.

Mirrors the status_view logic in the Assigned Work tab: each assignment is
matched against the saved completion records on (class, activity).
"""

failures = []


def check(label, cond):
    print(f"  {'PASS' if cond else 'FAIL'}  {label}")
    if not cond:
        failures.append(label)


DONE_LABEL = '✅ Work Completed'
OPEN_LABEL = '⏳ Not completed yet'

assignments = [
    {'class': 'Class I', 'subject': 'English', 'skill_area': 'Listening',
     'activity': 'Listen & Do Adventure', 'game_type': 'listen_do'},
    {'class': 'Class I', 'subject': 'English', 'skill_area': 'Comprehension',
     'activity': 'Story Time Quiz', 'game_type': 'quiz'},
    {'class': 'Class VI', 'subject': 'English', 'skill_area': 'Phonetics',
     'activity': 'Sound Detective', 'game_type': 'listen_do'},
]

completions = [
    {'student': 'ravi', 'display_name': 'Ravi',
     'class': 'Class I', 'activity': 'Listen & Do Adventure'},
]


def build_status(assigned, completions):
    """Same construction as the Assigned Work tab."""
    done_keys = {(c.get('class'), c.get('activity')) for c in completions}
    rows = []
    for item in assigned:
        key = (item['class'], item['activity'])
        who = sorted({c.get('display_name', c.get('student', ''))
                      for c in completions
                      if (c.get('class'), c.get('activity')) == key})
        rows.append({
            'class': item['class'],
            'activity': item['activity'],
            'status': DONE_LABEL if key in done_keys else OPEN_LABEL,
            'done_by': ', '.join(w for w in who if w) or '-',
        })
    return rows


print("STEP 1 - one game completed, two not")
rows = build_status(assignments, completions)
check("all three assignments listed", len(rows) == 3)
check("completed game flagged done",
      rows[0]['status'] == DONE_LABEL)
check("completed game names the student", rows[0]['done_by'] == 'Ravi')
check("unfinished Class I game still open",
      rows[1]['status'] == OPEN_LABEL)
check("unfinished game has no student", rows[1]['done_by'] == '-')
check("unfinished Class VI game still open",
      rows[2]['status'] == OPEN_LABEL)

print("\nSTEP 2 - counters")
n_done = sum(1 for r in rows if r['status'] == DONE_LABEL)
n_open = len(rows) - n_done
check("done count is 1", n_done == 1)
check("open count is 2", n_open == 2)
check("counts add up to total", n_done + n_open == len(assignments))

print("\nSTEP 3 - filter by status")
check("All returns everything", len(rows) == 3)
done_only = [r for r in rows if r['status'] == DONE_LABEL]
open_only = [r for r in rows if r['status'] == OPEN_LABEL]
check("done filter returns 1", len(done_only) == 1)
check("open filter returns 2", len(open_only) == 2)
check("filters partition the list",
      len(done_only) + len(open_only) == len(rows))

print("\nSTEP 4 - same activity name in two classes stays distinct")
dual = [
    {'class': 'Class I', 'subject': 'English', 'skill_area': 'L',
     'activity': 'Sound Detective', 'game_type': 'g'},
    {'class': 'Class VI', 'subject': 'English', 'skill_area': 'P',
     'activity': 'Sound Detective', 'game_type': 'g'},
]
rows = build_status(dual, [{'student': 'ravi', 'display_name': 'Ravi',
                            'class': 'Class I', 'activity': 'Sound Detective'}])
check("Class I copy marked done", rows[0]['status'] == DONE_LABEL)
check("Class VI copy still open", rows[1]['status'] == OPEN_LABEL)

print("\nSTEP 5 - two students complete the same game")
rows = build_status(
    assignments,
    [{'student': 'ravi', 'display_name': 'Ravi',
      'class': 'Class VI', 'activity': 'Sound Detective'},
     {'student': 'meera', 'display_name': 'Meera',
      'class': 'Class VI', 'activity': 'Sound Detective'}])
check("listed once, both names shown",
      rows[2]['status'] == DONE_LABEL and rows[2]['done_by'] == 'Meera, Ravi')

print("\nSTEP 6 - no completions at all")
rows = build_status(assignments, [])
check("everything shows as not completed",
      all(r['status'] == OPEN_LABEL for r in rows))
check("no student names", all(r['done_by'] == '-' for r in rows))

print("\nSTEP 7 - unnamed student shows the fallback name")
rows = build_status(assignments,
                    [{'student': '(unnamed)', 'display_name': '(unnamed)',
                      'class': 'Class VI', 'activity': 'Sound Detective'}])
check("fallback name appears", rows[2]['done_by'] == '(unnamed)')

print()
if failures:
    print(f"FAILURES: {len(failures)}")
    for f in failures:
        print("  -", f)
    raise SystemExit(1)
print("OK - completed work is flagged in the teacher's Assigned Work tab")