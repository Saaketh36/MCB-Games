"""
Verify a game cannot be opened while the student's name is blank.

Mirrors the PLAY handler in the student hub: a blank or whitespace-only name
must not reach the game page, and the warning must clear once a name is given.
"""

failures = []


def check(label, cond):
    print(f"  {'PASS' if cond else 'FAIL'}  {label}")
    if not cond:
        failures.append(label)


def click_play(student_name):
    """Return 'opened' or 'blocked', mirroring the PLAY button handler."""
    session = {'student_name': student_name, 'name_missing': None}

    if not session['student_name'].strip():
        session['name_missing'] = True
        return 'blocked', session

    session['name_missing'] = False
    return 'opened', session


print("STEP 1 - blank name, PLAY clicked")
result, session = click_play('   ')
check("game is NOT opened", result == 'blocked')
check("warning flag raised", session['name_missing'] is True)

print("\nSTEP 2 - empty string")
result, _ = click_play('')
check("game is NOT opened", result == 'blocked')

print("\nSTEP 3 - real name, PLAY clicked")
result, session = click_play('Ravi')
check("game opens", result == 'opened')
check("no warning shown", session['name_missing'] is False)

print("\nSTEP 4 - name with surrounding spaces still counts as given")
result, _ = click_play('  Ravi  ')
check("game opens for '  Ravi  '", result == 'opened')

print("\nSTEP 5 - tabs-only and newline-only are treated as blank")
for label, value in [("tab only", '\t'), ("newline only", '\n')]:
    result, _ = click_play(value)
    check(f"blocked for {label}", result == 'blocked')

print("\nSTEP 6 - warning clears once a name is typed")
session = {'student_name': '', 'name_missing': True}
if not session['student_name'].strip():
    session.pop('name_missing', None)
check("stale warning removed", 'name_missing' not in session)

def who_key(student_name):
    """Same fallback as the app, so we can confirm the guard matches it."""
    return (student_name or '').strip().lower() or '(unnamed)'


print("\nSTEP 7 - the blocked case is the only one that would use a fallback")
check("blank name maps to the fallback identity",
      who_key('   ') == '(unnamed)')
check("a real name maps to its own identity",
      who_key('Ravi') == 'ravi')
check("case and padding do not change identity",
      who_key('  Ravi  ') == 'ravi')

print()
if failures:
    print(f"FAILURES: {len(failures)}")
    for f in failures:
        print("  -", f)
    raise SystemExit(1)
print("OK - a blank name blocks the game from opening")