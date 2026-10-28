import sys
sys.stdout.reconfigure(encoding='utf-8')
import json

with open('question_bank.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = "const QUESTION_BANK = "
raw_json = text[len(prefix):].rstrip(';\n ')
qb = json.loads(raw_json)

has_content = []
for k, v in qb.items():
    if v.get('audio_script') or v.get('story') or v.get('instructions') or v.get('passage'):
        has_content.append((k, v.get('audio_script', ''), v.get('instructions', []), v.get('story', '')))

print(f"Total QB entries with context: {len(has_content)}")
for k, script, instr, story in has_content:
    print(f"Key: {k}")
    if script: print(f"  audio_script ({len(script)} chars): {script[:70]}...")
    if instr: print(f"  instructions: {len(instr)} steps: {instr}")
    if story: print(f"  story ({len(story)} chars): {story[:70]}...")
