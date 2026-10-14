"""
Draws one SVG picture per option of every Odd One Out question.

Every picture is drawn from scratch as plain SVG shapes, so there are no
external image files, no downloads and no licensing questions. Output:

    images/odd/<set-id>-<n>.svg
    images/odd_index.json   -> "<activity>|||<set-id>": [4 paths]

Run:  python tools\\make_odd_images.py
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from odd_one_out_content import ODD_ONE_OUT      # noqa: E402
import odd_pictograms                            # noqa: E402


def main():
    out_dir = os.path.join(ROOT, "images", "odd")
    os.makedirs(out_dir, exist_ok=True)
    index, missing = {}, []

    for activity, sets in ODD_ONE_OUT.items():
        for entry in sets:
            paths = []
            for i, slug in enumerate(entry["items"]):
                try:
                    body = odd_pictograms.render(slug)
                except KeyError as exc:
                    missing.append((activity, entry["set_id"], str(exc)))
                    paths = []
                    break
                name = f"{entry['set_id']}-{i}.svg"
                with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
                    fh.write(body)
                paths.append(f"images/odd/{name}")
            if paths:
                index[f"{activity}|||{entry['set_id']}"] = paths

    with open(os.path.join(ROOT, "images", "odd_index.json"), "w",
              encoding="utf-8") as fh:
        json.dump({"items": index}, fh, ensure_ascii=False, indent=1)

    total = sum(len(v) for v in index.values())
    print(f"sets written : {len(index)}")
    print(f"images written: {total}")
    print(f"unmapped      : {len(missing)}")
    for m in missing:
        print("   -", m)

    if missing:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())