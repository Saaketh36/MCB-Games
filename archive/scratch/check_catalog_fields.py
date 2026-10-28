import json

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

print("Total games in catalog:", len(catalog))
has_config = [g['id'] for g in catalog if g.get('interactiveConfig')]
print("Games with interactiveConfig:", len(has_config))

# Check gameTypes of games
from collections import Counter
print("GameTypes in catalog:", Counter(g.get('gameType') for g in catalog))

# Check games that have 'passage'
has_passage = [g['id'] for g in catalog if g.get('passage')]
print("Games with passage:", len(has_passage), has_passage)

# Check games with 'story'
has_story = [g['id'] for g in catalog if g.get('story')]
print("Games with story:", len(has_story), has_story)

# Check games with 'instructions'
has_instr = [g['id'] for g in catalog if g.get('instructions')]
print("Games with instructions:", len(has_instr), has_instr)
