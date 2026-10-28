"""
Odd One Out questions for the bank builder.

An odd-one-out question shows four pictures and asks the student to tap the one
that does not belong, so the options must stay in step with the pictures. The
pictures are shuffled together with the option text, then the answer label is
rebuilt from wherever the odd item landed.
"""

import hashlib
import json
import os

from odd_one_out_content import sets_for

# This module sits in the project root, not in tools/, so one dirname is enough.
ROOT = os.path.dirname(os.path.abspath(__file__))


def _load_index():
    try:
        with open(os.path.join(ROOT, "images", "odd_index.json"), encoding="utf-8") as fh:
            return json.load(fh).get("items", {})
    except (OSError, ValueError):
        return {}


ODD_INDEX = _load_index()

LABELS = ["A", "B", "C", "D"]


def _seed(*parts):
    return int(hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()[:12], 16)


def _title(slug):
    return slug.replace("_", " ").title()


def build_questions(activity):
    """Odd-one-out questions for one activity, or [] if none are authored."""
    name = activity["activity_name"]
    cls = activity["class"]
    subject = activity["subject"]
    tag = f"[{cls} {subject} - {name}]"

    built = []
    for entry in sets_for(name):
        paths = ODD_INDEX.get(f"{name}|||{entry['set_id']}")
        if not paths or len(paths) != len(entry["items"]):
            continue

        # Rotate the pictures so the odd one is not always in the same slot.
        shift = _seed(cls, subject, name, entry["set_id"]) % len(paths)
        rotated = entry["items"][shift:] + entry["items"][:shift]
        rot_paths = paths[shift:] + paths[:shift]
        odd_pos = rotated.index(entry["items"][entry["odd"]])

        options = [f"Option {LABELS[i]}: {_title(s)}" for i, s in enumerate(rotated)]
        built.append({
            "question": f"{tag} {entry['prompt']}",
            "options": options,
            "answer": f"Option {LABELS[odd_pos]}: {_title(rotated[odd_pos])}",
            "explanation": entry["reason"],
            # One picture per option, in the same order as options.
            "option_images": rot_paths,
            "odd_one_out": True,
        })
    return built