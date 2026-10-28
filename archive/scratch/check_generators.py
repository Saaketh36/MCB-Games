import re

with open('js/class2_games.js', 'r', encoding='utf-8') as f:
    text = f.read()

keys = re.findall(r'"([A-Za-z0-9_\-]+)":\s*function', text)
print(f"Total interactive keys: {len(keys)}")
print(keys)
