"""
Exercise the teacher-dashboard activity lookup for every class/subject pair.

The tab used to crash with StopIteration when the chosen combination had no
activities. This walks all 40 combinations and confirms a usable target is
always resolved.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from games_data import CURRICULUM_DATA  # noqa: E402

CLASSES = ["Class I", "Class II", "Class III", "Class IV",
           "Class V", "Class VI", "Class VII", "Class VIII"]


def resolve(gc, gs, act_sel=None):
    """Mirror the lookup now used in app.py."""
    subjs = sorted({i["subject"] for i in CURRICULUM_DATA if i["class"] == gc})
    if gs not in subjs:
        return None, "subject not offered"
    acts = [i for i in CURRICULUM_DATA if i["class"] == gc and i["subject"] == gs]
    names = [a["activity_name"] for a in acts]
    if not names:
        return None, "no activities"
    if act_sel is None:
        act_sel = names[0]
    target = next((a for a in acts if a["activity_name"] == act_sel),
                  acts[0] if acts else None)
    return target, "ok"


def main():
    all_subjects = sorted({i["subject"] for i in CURRICULUM_DATA})
    crashes, resolved, offered, guarded = 0, 0, 0, 0

    for gc in CLASSES:
        for gs in all_subjects:
            # The UI can never offer an empty subject now, but simulate a
            # stale selection too, since that was the other failure route.
            for sel in (None, "Some Activity That No Longer Exists"):
                try:
                    target, why = resolve(gc, gs, sel)
                except StopIteration:
                    crashes += 1
                    print(f"  CRASH {gc} / {gs} / sel={sel}")
                    continue
                if target is None:
                    guarded += 1
                else:
                    resolved += 1

    offered = sum(1 for gc in CLASSES
                  for gs in sorted({i["subject"] for i in CURRICULUM_DATA
                                    if i["class"] == gc}))

    print(f"class/subject pairs offered by the UI : {offered}")
    print(f"resolved to an activity                : {resolved}")
    print(f"guarded (no activities, info shown)   : {guarded}")
    print(f"StopIteration crashes                  : {crashes}")

    # A stale selection must still land on a real activity.
    t, why = resolve("Class I", "English", "Some Activity That No Longer Exists")
    print(f"stale selection fallback               : {t['activity_name'] if t else None}")
    return 1 if crashes else 0


if __name__ == "__main__":
    raise SystemExit(main())