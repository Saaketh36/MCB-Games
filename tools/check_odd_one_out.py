"""
Verify the Odd One Out activities: real classification content, four pictures
per question, pictures aligned with their options, and a genuine odd item.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from odd_pictograms import PICTOGRAMS            # noqa: E402
from odd_one_out_content import ODD_ONE_OUT      # noqa: E402
from odd_one_out_build import build_questions   # noqa: E402
from games_data import CURRICULUM_DATA           # noqa: E402

failures = []


def check(label, cond):
    print(f"  {'PASS' if cond else 'FAIL'}  {label}")
    if not cond:
        failures.append(label)


def load_bank():
    text = open(os.path.join(ROOT, "question_bank.js"), encoding="utf-8").read()
    return json.loads(text[text.index("{"):text.rindex("}") + 1])


odd_acts = [a for a in CURRICULUM_DATA if a["game_type"] == "Odd One Out"]
bank = load_bank()

print(f"Odd One Out activities in curriculum: {len(odd_acts)}")
check("every Odd One Out activity has authored sets",
      all(ODD_ONE_OUT.get(a["activity_name"]) for a in odd_acts))

print("\nSTEP 1 - each set names four items and one odd item")
for activity, sets in ODD_ONE_OUT.items():
    for e in sets:
        ok = len(e["items"]) == 4 and 0 <= e["odd"] < 4
        check(f"{e['set_id']}: four items, valid odd index", ok)

print("\nSTEP 2 - the odd item is not repeated inside its own set")
for activity, sets in ODD_ONE_OUT.items():
    for e in sets:
        check(f"{e['set_id']}: four distinct items",
              len(set(e["items"])) == 4)

print("\nSTEP 3 - every item has a drawable pictogram")
for activity, sets in ODD_ONE_OUT.items():
    for e in sets:
        missing = [s for s in e["items"] if s not in PICTOGRAMS]
        check(f"{e['set_id']}: all pictograms exist", not missing)

print("\nSTEP 4 - the odd item is explained in the reason")
for activity, sets in ODD_ONE_OUT.items():
    for e in sets:
        odd = e["items"][e["odd"]]
        others = [i for i in e["items"] if i != odd]
        check(f"{e['set_id']}: reason names the odd item", odd in e["reason"].lower())
        check(f"{e['set_id']}: reason explains the group",
              any(o.split()[-1].lower() in e["reason"].lower() for o in others))

print("\nSTEP 5 - generated SVGs exist and are not blank")
for activity, sets in ODD_ONE_OUT.items():
    for e in sets:
        for i in range(4):
            path = os.path.join(ROOT, "images", "odd", f"{e['set_id']}-{i}.svg")
            if not os.path.exists(path):
                check(f"{e['set_id']}-{i}: file exists", False)
                continue
            body = open(path, encoding="utf-8").read()
            draws = sum(body.count(f"<{t}") for t in
                        ("rect", "circle", "path", "ellipse", "polygon", "text"))
            check(f"{e['set_id']}-{i}: real drawing ({draws} shapes)",
                  body.rstrip().endswith("</svg>") and draws >= 2)

print("\nSTEP 6 - bank questions carry one image per option")
for a in odd_acts:
    key = f"{a['class']}|||{a['subject']}|||{a['activity_name']}"
    qs = bank[key]["questions"]
    check(f"{a['activity_name']}: has 3 questions", len(qs) == 3)
    for n, q in enumerate(qs):
        check(f"{a['activity_name']} q{n}: four options", len(q["options"]) == 4)
        check(f"{a['activity_name']} q{n}: four pictures",
              len(q.get("option_images") or []) == 4)
        check(f"{a['activity_name']} q{n}: marked as odd one out",
              q.get("odd_one_out") is True)
        check(f"{a['activity_name']} q{n}: answer is one of the options",
              q["answer"] in q["options"])
        check(f"{a['activity_name']} q{n}: options are unique",
              len(set(q["options"])) == 4)
        on_disk = [os.path.exists(os.path.join(ROOT, *p.split("/")))
                   for p in q["option_images"]]
        check(f"{a['activity_name']} q{n}: all pictures on disk", all(on_disk))

print("\nSTEP 7 - the prompt actually asks for the odd one")
for a in odd_acts:
    key = f"{a['class']}|||{a['subject']}|||{a['activity_name']}"
    for n, q in enumerate(bank[key]["questions"]):
        check(f"{a['activity_name']} q{n}: prompt mentions odd one out",
              "odd one out" in q["question"].lower())

print("\nSTEP 8 - no leftover shape-arithmetic questions")
for a in odd_acts:
    key = f"{a['class']}|||{a['subject']}|||{a['activity_name']}"
    blob = json.dumps(bank[key]).lower()
    check(f"{a['activity_name']}: no cone/cylinder/quarter-turn leftovers",
          not any(w in blob for w in ("cone", "cylinder", "quarter turn",
                                      "flat faces")))

print("\nSTEP 9 - the odd item moves around, so 'always A' is not learnable")
positions = set()
for a in odd_acts:
    key = f"{a['class']}|||{a['subject']}|||{a['activity_name']}"
    for q in bank[key]["questions"]:
        positions.add(q["options"].index(q["answer"]))
check("more than one slot is used for the odd item", len(positions) > 1)
print(f"      slots used: {sorted(positions)}")

print("\nSTEP 10 - other game types are untouched")
non_odd = [a for a in CURRICULUM_DATA if a["game_type"] != "Odd One Out"]
touched = [a["activity_name"] for a in non_odd
           if any(q.get("odd_one_out")
                  for q in bank.get(f"{a['class']}|||{a['subject']}|||"
                                    f"{a['activity_name']}", {}).get("questions", []))]
check("no non-odd activity gained odd-one-out questions", not touched)

print("\nSTEP 11 - the rest of the bank still builds")
check("all 325 activities present", len(bank) == 325)
total = sum(len(p.get("questions", [])) for p in bank.values())
check("975 questions written", total == 975)

print()
if failures:
    print(f"FAILURES: {len(failures)}")
    for f in failures[:25]:
        print("  -", f)
    raise SystemExit(1)
print("OK - Odd One Out shows four pictures and a genuine odd item")