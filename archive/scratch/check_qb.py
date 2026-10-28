import json

with open('question_bank.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = "const QUESTION_BANK = "
raw_json = text[len(prefix):].rstrip(';\n ')
qb = json.loads(raw_json)

for k, v in qb.items():
    if 'Class VIII' in k:
        print(f"{k}: fields={list(v.keys())}")
        if 'audio_script' in v:
            print("  audio_script:", v['audio_script'][:100])
