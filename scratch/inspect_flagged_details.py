import os
import sys
import json

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

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

target_oids = [53, 63, 93, 96, 119, 121, 171, 173, 240, 261, 264, 271, 275, 280, 324, 346, 413, 419, 421, 439]

for oid in target_oids:
    g = all_games[oid]
    print(f"\n==================== OUTCOME #{oid} ====================")
    print(f"Title: {g['title']}")
    print(f"Story: {g['story']}")
    for i, q in enumerate(g['questions']):
        print(f"  Q{i+1}: {q['prompt']}")
        for opt_idx, opt in enumerate(q['options']):
            print(f"     [{opt_idx}]: {opt}")
