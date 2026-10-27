import json
import sys

for s in (sys.stdout, sys.stderr):
    if hasattr(s, 'reconfigure'):
        s.reconfigure(encoding='utf-8', errors='replace')

with open('data/activity_card_thumbnails.json', 'r', encoding='utf-8') as f:
    thumbnails = json.load(f)

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

print(f"Thumbnails count: {len(thumbnails)}")
print(f"Games catalog count: {len(games)}")

assert len(thumbnails) == 440, f"Expected 440 thumbnails, got {len(thumbnails)}"
assert len(games) == 440, f"Expected 440 games, got {len(games)}"

# Validate every single thumbnail entry
all_have_prompts = all('imagePrompt' in t and len(t['imagePrompt']) > 80 for t in thumbnails)
all_have_scenes = all('dioramaScene' in t and 'summary' in t['dioramaScene'] for t in thumbnails)
all_have_top_right_sky = all('top-right' in t['imagePrompt'] for t in thumbnails)
all_have_island = all('floating green island' in t['imagePrompt'] for t in thumbnails)

print(f"All 440 have robust prompts: {all_have_prompts}")
print(f"All 440 have structured diorama scenes: {all_have_scenes}")
print(f"All 440 preserve UI constraint (clean top-right gradient sky for badge): {all_have_top_right_sky}")
print(f"All 440 feature floating green island diorama aesthetic: {all_have_island}")

# Check breakdown by class
by_class = {}
for t in thumbnails:
    c = t.get('class', 'Unknown')
    by_class[c] = by_class.get(c, 0) + 1

print("\nActivity Breakdown by Class:")
for c in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']:
    print(f"  Class {c}: {by_class.get(c, 0)} activities")

# Check breakdown by subject
by_subj = {}
for t in thumbnails:
    s = t.get('subject', 'Unknown')
    by_subj[s] = by_subj.get(s, 0) + 1

print("\nActivity Breakdown by Subject:")
for s, count in sorted(by_subj.items()):
    print(f"  {s}: {count} activities")
