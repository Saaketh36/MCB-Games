# -*- coding: utf-8 -*-
"""
Test the randomized answer assignment algorithm for all 440 games.
"""
import random
from collections import Counter

rng = random.Random(20261027)

# Pre-generate a balanced pool of positions
# For 1,320 questions, exactly 330 of each: 0, 1, 2, 3
positions_pool = [0, 1, 2, 3] * 330
rng.shuffle(positions_pool)

# Distribute into 440 games of 3 questions each, ensuring no game has identical positions for all 3 questions
games_positions = []
idx = 0
for g in range(440):
    trio = positions_pool[idx:idx+3]
    idx += 3
    # If all 3 are identical, swap one with later element
    while trio[0] == trio[1] == trio[2] and idx < len(positions_pool):
        # find first different element in remaining pool
        for swap_idx in range(idx, len(positions_pool)):
            if positions_pool[swap_idx] != trio[0]:
                positions_pool[idx-1], positions_pool[swap_idx] = positions_pool[swap_idx], positions_pool[idx-1]
                trio = [trio[0], trio[1], positions_pool[idx-1]]
                break
    games_positions.append(trio)

all_pos = [p for trio in games_positions for p in trio]
counts = Counter(all_pos)
print("Position counts (0=A, 1=B, 2=C, 3=D):")
for pos, cnt in sorted(counts.items()):
    letter = chr(65 + pos)
    pct = (cnt / len(all_pos)) * 100
    print(f"  Option {letter} (index {pos}): {cnt} questions ({pct:.2f}%)")

# Check triple duplicates in any game
triples = sum(1 for trio in games_positions if trio[0] == trio[1] == trio[2])
print(f"Games with all 3 identical positions: {triples}")

# Sample first 5 games
letters = ['A', 'B', 'C', 'D']
for g_num in range(5):
    trio_letters = [letters[p] for p in games_positions[g_num]]
    print(f"Game {g_num+1} answer positions: {trio_letters} (indices: {games_positions[g_num]})")
