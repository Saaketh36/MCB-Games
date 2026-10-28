import json
from collections import Counter

cat = json.load(open('full_games_catalog.json', encoding='utf-8'))
print(f"Total catalog games: {len(cat)}")

titles = [c['title'] for c in cat]
too_long = [t for t in titles if len(t) > 100]
print(f"Titles > 100 chars: {len(too_long)}")

counts = Counter(titles)
duplicates = [t for t, count in counts.items() if count > 1]
print(f"Duplicate titles: {len(duplicates)}")
for d in duplicates:
    matching = [(c['id'], c['class'], c['subject'], c['title']) for c in cat if c['title'] == d]
    print(" -", d, matching)
