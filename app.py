#!/usr/bin/env python3
"""
Root-level compatibility shim.
Allows `python app.py` to continue working from the project root
while the canonical entry point is now `backend/app.py`.
"""
import sys
import os

# Ensure the project root is on the path so `backend.*` imports resolve
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app import app, main  # noqa: F401

if __name__ == '__main__':
    main()
