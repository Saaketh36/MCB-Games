"""
Verify the Student Portal button refuses to open when the student has already
finished every assigned game.

Mirrors the landing-page gate: type name -> check that student's own records ->
open only if work remains.
"""

failures = []


def check(label, cond):
    print(f"  {'PASS' if cond else 'FAIL'}  {label}")
    if not cond:
        failures.append(label)


def pending_for_student(assignments, completions, name):
    who = (name or '').strip().lower() or '(unnamed)'
    return [a for a in assignments
            if not any(c.get('student') == who
                       and c.get('class') == a['class']
                       and c.get('activity') == a['activity']
                       for c in completions)]


assignments = [
    {'class': 'Class I', 'activity': 'Listen & Do Adventure'},
    {'class': 'Class IV', 'activity': 'Follow the Steps Race'},
    {'class': 'Class VI', 'activity': 'Eco Hero Choices'},
]

completions = [
    {'student': 'charitha', 'class': 'Class I', 'activity': 'Listen & Do Adventure'},
    {'student': 'charitha', 'class': 'Class IV', 'activity': 'Follow the Steps Race'},
    {'student': 'charitha', 'class': 'Class VI', 'activity': 'Eco Hero Choices'},
    {'student': 'meera', 'class': 'Class I', 'activity': 'Listen & Do Adventure'},
]


def click_student_portal(typed_name, assignments=assignments, completions=completions):
    """Return 'opened', 'blocked' or 'needs_name', mirroring the button."""
    typed = typed_name.strip()
    if not typed:
        return 'needs_name'
    # With nothing assigned the hub explains it, so the gate lets the student in.
    if not assignments:
        return 'opened'
    left = pending_for_student(assignments, completions, typed)
    return 'opened' if left else 'blocked'


print("STEP 1 - finished student is blocked")
check("portal does NOT open", click_student_portal('charitha') == 'blocked')

print("\nSTEP 2 - partly finished student gets in")
part = [c for c in completions if c['student'] == 'charitha'][:2]
check("portal opens with work left",
      click_student_portal('charitha', assignments, part) == 'opened')

print("\nSTEP 3 - student who has done nothing gets in")
check("portal opens for a new name",
      click_student_portal('newkid') == 'opened')

print("\nSTEP 4 - another student is unaffected by the first one finishing")
check("Meera still gets in", click_student_portal('meera') == 'opened')

print("\nSTEP 5 - blank name is refused, never guessed")
for label, value in [('empty', ''), ('spaces', '   '),
                     ('tab', '\t'), ('newline', '\n')]:
    check(f"asks for a name on {label}",
          click_student_portal(value) == 'needs_name')

print("\nSTEP 6 - name matching ignores case and padding")
for variant in ['CHARITHA', '  charitha  ', 'ChaRitHa']:
    check(f"'{variant}' treated as charitha",
          click_student_portal(variant) == 'blocked')

print("\nSTEP 7 - the same activity in two classes counts separately")
dual = [
    {'class': 'Class I', 'activity': 'Sound Detective'},
    {'class': 'Class VI', 'activity': 'Sound Detective'},
]
one_done = [{'student': 'kid', 'class': 'Class I',
             'activity': 'Sound Detective'}]
check("still has the Class VI copy left",
      len(pending_for_student(dual, one_done, 'kid')) == 1)
check("blocked only once both classes are done",
      click_student_portal('kid', dual,
                           one_done + [{'student': 'kid', 'class': 'Class VI',
                                        'activity': 'Sound Detective'}]) == 'blocked')

print("\nSTEP 8 - teacher assigning new work reopens the portal")
extra = assignments + [{'class': 'Class II', 'activity': 'Verb Action Sort'}]
check("new assignment means work remains",
      click_student_portal('charitha', extra, completions) == 'opened')

print("\nSTEP 9 - clearing records reopens the portal")
check("portal opens after records are cleared",
      click_student_portal('charitha', assignments, []) == 'opened')

print("\nSTEP 10 - no assignments at all does not read as finished")
check("empty assignment list leaves nothing pending",
      click_student_portal('charitha', [], completions) == 'opened')

print("\nSTEP 11 - the hub guards itself, so a browser refresh cannot bypass it")


def render_hub(student_name, assignments=assignments, completions=completions):
    """Mirror the student_hub page guard."""
    if not assignments:
        return 'no_assignments'
    who = (student_name or '').strip().lower()

    def pending_for(class_name):
        return [a for a in assignments
                if a['class'] == class_name
                and not any(c.get('student') == who
                        and c.get('class') == class_name
                        and c.get('activity') == a['activity']
                        for c in completions)]

    open_classes = [c for c in sorted({a['class'] for a in assignments})
                    if pending_for(c)]
    if not open_classes and student_name.strip():
        return 'redirect_to_landing'
    return 'shows_games'


check("finished student is bounced off the hub",
      render_hub('charitha') == 'redirect_to_landing')
check("student with work left still gets the game list",
      render_hub('newkid') == 'shows_games')
check("partly finished student still gets the game list",
      render_hub('charitha', assignments, part) == 'shows_games')
check("blank name is not bounced, so the field can be filled",
      render_hub('   ') != 'redirect_to_landing')
check("no assignments shows the teacher notice, not a bounce",
      render_hub('charitha', [], completions) == 'no_assignments')
check("case and padding still bounce",
      render_hub('  CHARITHA  ') == 'redirect_to_landing')
check("another student is not bounced",
      render_hub('meera') == 'shows_games')

print()
if failures:
    print(f"FAILURES: {len(failures)}")
    for f in failures:
        print("  -", f)
    raise SystemExit(1)
print("OK - the Student Portal stays closed once a student finishes everything")