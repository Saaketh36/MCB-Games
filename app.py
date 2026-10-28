#!/usr/bin/env python3
"""
Root-level compatibility shim.
Allows `python app.py` to continue working from the project root
while the canonical entry point is now `backend/app.py`.
"""
import sys
import os

# Ensure the project root is on the path so `backend.*` imports resolve
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import app  # noqa: F401

if __name__ == '__main__':
    from backend.app import app as _app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    _app.run(debug=debug, port=port)
