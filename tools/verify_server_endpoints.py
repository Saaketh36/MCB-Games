#!/usr/bin/env python3
"""
Verify Flask server static asset serving and curriculum/game API endpoints.
Ensures zero 404s for index.html, all frontend CSS/JS assets, and API routes.
"""
from __future__ import annotations

import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app import app


def test_routes():
    client = app.test_client()
    failed = []

    # 1. Main entry points
    for route in ['/', '/index.html']:
        res = client.get(route)
        if res.status_code != 200 or len(res.data) < 500:
            failed.append((route, res.status_code, "Entry point failed or empty"))
        else:
            print(f"  OK [200]: {route} ({len(res.data)} bytes)")

    # 2. Assets referenced in index.html
    with open(os.path.join(PROJECT_ROOT, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()

    links = re.findall(r'href=[\'"]([^\'"]+\.css(?:\?[^\'"]*)?)[\'"]', html)
    scripts = re.findall(r'src=[\'"]([^\'"]+\.js(?:\?[^\'"]*)?)[\'"]', html)

    for asset in links + scripts:
        clean_url = '/' + asset.lstrip('/')
        res = client.get(clean_url)
        if res.status_code != 200:
            failed.append((clean_url, res.status_code, "Asset 404/error"))
        else:
            print(f"  OK [200]: {clean_url}")

    # 3. API endpoints
    api_curriculum = client.get('/api/curriculum')
    if api_curriculum.status_code != 200:
        failed.append(('/api/curriculum', api_curriculum.status_code, "API curriculum failed"))
    else:
        data = api_curriculum.get_json()
        total_cls = data.get('total_classes', 0)
        print(f"  OK [200]: /api/curriculum ({total_cls} classes)")
        if total_cls < 8:
            failed.append(('/api/curriculum', 200, f"Expected 8 classes, got {total_cls}"))

    api_games = client.get('/api/available-games')
    if api_games.status_code != 200:
        failed.append(('/api/available-games', api_games.status_code, "API games failed"))
    else:
        data = api_games.get_json()
        total_games = data.get('total_available', 0)
        print(f"  OK [200]: /api/available-games ({total_games} games)")
        if total_games < 440:
            failed.append(('/api/available-games', 200, f"Expected 440 games, got {total_games}"))

    if failed:
        print("\nFAILURES DETECTED:")
        for url, code, reason in failed:
            print(f"  ❌ {url} (HTTP {code}): {reason}")
        return 1

    print("\n✅ All server static routes and API endpoints verified successfully.")
    return 0


if __name__ == '__main__':
    sys.exit(test_routes())
