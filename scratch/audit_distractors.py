# -*- coding: utf-8 -*-
"""
Audit all 440 games for distractor quality and cognitive trap characteristics:
- Detail Swap
- Common Misconceptions (math/science)
- Plausible Inferences
Flags any options that look overly obvious, silly, or unrealistic.
"""

import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generators'))

from gen_primary_1_2 import PRIMARY_GAMES
from gen_class3 import CLASS3_GAMES
from gen_class4 import CLASS4_GAMES
from gen_class5 import CLASS5_GAMES
from gen_class6 import CLASS6_GAMES
from gen_class7 import CLASS7_GAMES
from gen_class8 import CLASS8_GAMES

all_games = {}
all_games.update(PRIMARY_GAMES)
all_games.update(CLASS3_GAMES)
all_games.update(CLASS4_GAMES)
all_games.update(CLASS5_GAMES)
all_games.update(CLASS6_GAMES)
all_games.update(CLASS7_GAMES)
all_games.update(CLASS8_GAMES)

print(f"Loaded {len(all_games)} games.")

# Heuristics for potentially weak/silly distractors
silly_cues = [
    "alien", "magic wand", "opera", "spaceship", "pirate", "dinosaur", "dragon",
    "paper airplane", "flashlights", "flying carpet", "throw your shoes", "tag",
    "volcano", "secret agent", "run into the hallway", "screaming", "crying",
    "two seconds", "never talk", "eat the paper", "fold the slip into"
]

flagged = []

for oid, g in sorted(all_games.items()):
    story = g.get('story', '')
    for q_idx, q in enumerate(g.get('questions', [])):
        prompt = q['prompt']
        opts = q['options']
        for opt_idx, opt in enumerate(opts[1:], start=1):
            opt_lower = opt.lower()
            for cue in silly_cues:
                # If the cue is already in the story or prompt, it's not silly (e.g. dinosaur stickers in lost pencil box)
                if cue in opt_lower and cue not in story.lower() and cue not in prompt.lower():
                    flagged.append((oid, q_idx + 1, prompt, opt, cue))

print(f"\nTotal flagged distractors: {len(flagged)}")
for f in flagged[:30]:
    print(f"Outcome #{f[0]} Q{f[1]}: '{f[2][:50]}...' -> Distractor: '{f[3]}' (cue: {f[4]})")
