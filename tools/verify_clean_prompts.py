import json
import re

print("=== CLEAN PROMPTS AUDIT REPORT ===")

# Check 1: Catalog files
for path in ['full_games_catalog.json', 'full_games_catalog.js', 'question_bank.js']:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'\[Class\s+[^\]]+\]', content)
    print(f"File {path}: {len(matches)} class prefix occurrences found.")

# Check 2: Expression Builder specific check
with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for g in catalog:
    if g.get('title') == 'Expression Builder':
        print(f"\nGame: {g.get('title')} (Class {g.get('class')}, {g.get('subject')}, {g.get('skillArea')})")
        for idx, q in enumerate(g.get('questions', [])):
            print(f"  Q{idx+1} Prompt: {q.get('prompt')}")

# Check 3: Check other sample classes
samples = ['Story Time Quiz', 'Water Source Sorter', 'Model Engineer Challenge']
for g in catalog:
    if g.get('title') in samples:
        print(f"\nGame: {g.get('title')} (Class {g.get('class')}, {g.get('subject')})")
        for idx, q in enumerate(g.get('questions', [])[:2]):
            print(f"  Q{idx+1} Prompt: {q.get('prompt')}")

# Check 4: App.js checks
with open('js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()
print("\napp.js checks:")
print("  cleanQuestionPrompt defined:", 'function cleanQuestionPrompt(' in app_js)
print("  questPromptTitle sanitized:", ('rawPrompt = cleanQuestionPrompt(q.prompt)' in app_js or 'textContent = cleanQuestionPrompt(q.prompt)' in app_js))
print("  utterance sanitized:", ('textToSpeak = cleanQuestionPrompt(q.prompt)' in app_js or 'new SpeechSynthesisUtterance(cleanQuestionPrompt(q.prompt))' in app_js))
print("  review-q-prompt-text sanitized:", '${cleanQuestionPrompt(q.prompt)}' in app_js)
print("  reading-question-title sanitized:", '${cleanQuestionPrompt(q.prompt)}' in app_js)

# Check 5: play.html checks
with open('play.html', 'r', encoding='utf-8') as f:
    play_html = f.read()
print("\nplay.html checks:")
print("  cleanQ defined:", 'function cleanQ(' in play_html)
print("  cleanQ usages count:", play_html.count('cleanQ('))

# Check 6: index.html script tags
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()
print("\nindex.html checks:")
print("  full_games_catalog.js?v=2.0 present:", 'full_games_catalog.js?v=2.0' in index_html)
print("  js/app.js?v=3.4 present:", 'js/app.js?v=3.4' in index_html)

print("\nAudit Complete!")
