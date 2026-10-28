#!/usr/bin/env python3
"""Run the active, read-only MCB content and behavior verification suites.

Run from any working directory with: ``python tools/verify_all.py``.
The runner deliberately invokes only checks that should not rewrite catalog,
question-bank, thumbnail, or application files.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SUITES = (
    ("Critical content rules", "tools/verify_critical_content_fixes.py"),
    ("Clean question formatting", "tools/verify_clean_formatting.py"),
    ("Assigned-order rendering", "tools/verify_assigned_order_sorting.py"),
    ("Diorama catalog integrity", "tools/verify_diorama_catalog.py"),
)


def main() -> int:
    failures: list[str] = []

    for label, relative_path in SUITES:
        print(f"\n{'=' * 72}\nVERIFY: {label}\n{'=' * 72}")
        result = subprocess.run(
            [sys.executable, relative_path],
            cwd=PROJECT_ROOT,
            check=False,
        )
        if result.returncode:
            failures.append(label)
            print(f"FAILED ({result.returncode}): {label}")
        else:
            print(f"PASSED: {label}")

    if failures:
        print(f"\nVerification failed: {', '.join(failures)}")
        return 1

    print("\nAll active verification suites passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
