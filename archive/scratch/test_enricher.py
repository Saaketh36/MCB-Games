# -*- coding: utf-8 -*-
"""
Test generator for rich, context-aware, kid-friendly activities.
"""
import json
import re

def clean_str(s):
    if not s:
        return ""
    return (s.replace('‘', "'")
             .replace('’', "'")
             .replace('“', '"')
             .replace('”', '"')
             .replace('–', '-')
             .replace('—', '-')
             .replace('\uFFFD', "'")
             .strip())

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

print(f"Total games to enrich: {len(games)}")
