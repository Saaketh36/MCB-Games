import json
from collections import Counter

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

print(f"Total catalog items: {len(catalog)}")

game_types = Counter()
skill_areas = Counter()
has_instructions_count = 0
has_story_count = 0
has_audio_script_count = 0
has_passage_count = 0

sample_by_type = {}

for g in catalog:
    gt = g.get('gameType')
    game_types[gt] += 1
    skill_areas[g.get('skillArea')] += 1
    if g.get('instructions'): has_instructions_count += 1
    if g.get('story'): has_story_count += 1
    if g.get('audio_script'): has_audio_script_count += 1
    if g.get('passage'): has_passage_count += 1
    if gt not in sample_by_type:
        sample_by_type[gt] = g

print("\n--- Game Types ---")
for gt, count in game_types.most_common():
    print(f"{gt}: {count}")

print("\n--- Skill Areas ---")
for sa, count in skill_areas.most_common():
    print(f"{sa}: {count}")

print(f"\nHas instructions: {has_instructions_count}")
print(f"Has story: {has_story_count}")
print(f"Has audio_script: {has_audio_script_count}")
print(f"Has passage: {has_passage_count}")

print("\n--- Sample Question for each Game Type ---")
for gt, g in sample_by_type.items():
    qs = g.get('questions', [])
    q0 = qs[0] if qs else None
    print(f"\nGameType: {gt} | ID: {g.get('id')} | Title: {g.get('title')}")
    if q0:
        print(f"  Prompt: {q0.get('prompt')}")
        print(f"  Options: {q0.get('options')}")
        print(f"  Type: {q0.get('type')}")
