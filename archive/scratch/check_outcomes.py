# -*- coding: utf-8 -*-
"""
Generate 440 activities and question sets strictly from the provided PDF:
'skillAreaOutcomes - Sheet1.pdf'
"""
import json
import re

def clean_text(s):
    if not s:
        return ""
    return (s.replace('‘', "'")
             .replace('’', "'")
             .replace('“', '"')
             .replace('”', '"')
             .replace('–', '-')
             .replace('—', '-')
             .strip())

with open('scratch/parsed_sample.json', 'r', encoding='utf-8') as f:
    outcomes = json.load(f)

print(f"Loaded {len(outcomes)} learning outcomes.")

# Check breakdown by class
from collections import Counter
class_counts = Counter(item['class'] for item in outcomes)
print("Class counts:", class_counts)

# Check Class I breakdown
c1 = [o for o in outcomes if o['class'] == 'I']
print(f"Class I Total: {len(c1)}")
c1_by_sa = Counter((o['subject'], o['skillArea']) for o in c1)
for (sub, sa), cnt in c1_by_sa.items():
    print(f"  {sub} -> {sa}: {cnt}")
