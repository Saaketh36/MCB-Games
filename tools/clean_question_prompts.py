import json
import re
import os

def clean_text(s):
    if not isinstance(s, str):
        return s
    # Regex matches: ^\s*\[Class\s+[^\]]+\]\s*
    # E.g.: "[Class VII Mathematics - Expression Builder] 'Five more than a number is 12' is best represented by"
    # -> "'Five more than a number is 12' is best represented by"
    cleaned = re.sub(r'^\s*\[Class\s+[^\]]+\]\s*', '', s)
    return cleaned

def clean_full_games_catalog_json():
    filepath = 'full_games_catalog.json'
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cleaned_count = 0
    for game in data:
        for q in game.get('questions', []):
            prompt = q.get('prompt', '')
            cleaned_prompt = clean_text(prompt)
            if cleaned_prompt != prompt:
                cleaned_count += 1
                q['prompt'] = cleaned_prompt
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Cleaned {cleaned_count} prompts in {filepath}")

def clean_full_games_catalog_js():
    filepath = 'full_games_catalog.js'
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We can do regex substitution on "prompt": "[Class ...]"
    # or more generally: re.sub(r'(\"prompt\"\s*:\s*\")\[Class\s+[^\]]+\]\s*', r'\1', content)
    cleaned_content, count = re.subn(r'("prompt"\s*:\s*")\[Class\s+[^\]]+\]\s*', r'\1', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print(f"Cleaned {count} prompts in {filepath}")

def clean_question_bank_js():
    filepath = 'question_bank.js'
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # In question_bank.js questions might be "question": "[Class ...]" or "prompt": "[Class ...]"
    cleaned_content, count1 = re.subn(r'("question"\s*:\s*")\[Class\s+[^\]]+\]\s*', r'\1', content)
    cleaned_content, count2 = re.subn(r'("prompt"\s*:\s*")\[Class\s+[^\]]+\]\s*', r'\1', cleaned_content)
    
    # Also check if any standalone "[Class ...]" in strings
    cleaned_content, count3 = re.subn(r'(\"q\"\s*:\s*\")\[Class\s+[^\]]+\]\s*', r'\1', cleaned_content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print(f"Cleaned {count1 + count2 + count3} items (q:{count1}, p:{count2}, other:{count3}) in {filepath}")

def verify_all_clean():
    print("Verifying if any [Class ...] prefixes remain in JSON/JS...")
    pattern = re.compile(r'\[Class\s+[^\]]+\]')
    for target in ['full_games_catalog.json', 'full_games_catalog.js', 'question_bank.js']:
        with open(target, 'r', encoding='utf-8') as f:
            txt = f.read()
        matches = pattern.findall(txt)
        print(f"Remaining in {target}: {len(matches)}")
        if matches:
            for m in matches[:5]:
                print(f"  Sample: {m}")

if __name__ == '__main__':
    clean_full_games_catalog_json()
    clean_full_games_catalog_js()
    clean_question_bank_js()
    verify_all_clean()
