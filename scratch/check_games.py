import json
import re

with open('ai_helper.py', 'r', encoding='utf-8') as f:
    text = f.read()

engines = set(re.findall(r'engine["\']?:\s*["\']([^"\']+)["\']', text))
print("Engines in ai_helper.py:", engines)

with open('js/class2_games.js', 'r', encoding='utf-8') as f:
    text2 = f.read()

# Let's see how class2_games renders engines
engines_render = set(re.findall(r'case\s+["\']([^"\']+)["\']:', text2))
print("Engines in class2_games.js switch:", engines_render)
