import sys
import os
import re
import json

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.abspath("."))

from ai_helper import (
    clean_prompt_text,
    clean_visual_hint,
    clean_option_text,
    get_curriculum_interactive_sorter_data,
    build_class2_interactive_config,
    build_fallback_small_scale_game,
    generate_smart_task,
    generate_ai_task_and_quiz
)

print("=" * 60)
print("TEST 1: QUESTION STEM METADATA REMOVAL (Directive 1)")
print("=" * 60)

prompt_test_cases = [
    ("[IV Science] Which planet is closest to the Sun in our Solar System?", "Which planet is closest to the Sun in our Solar System?"),
    ("[Class IV] Which plant part absorbs water from soil?", "Which plant part absorbs water from soil?"),
    ("[Science] What force pulls objects downward towards Earth?", "What force pulls objects downward towards Earth?"),
    ("[Grade 5 - Math] How many edges does a cube have?", "How many edges does a cube have?"),
    ("[IV] What do bees collect from flowers?", "What do bees collect from flowers?"),
    ("[Class 3 EVS] Which of these is an omnivorous animal?", "Which of these is an omnivorous animal?"),
    ("If ₹1,200 is shared equally among 24 students, how much does each student pay? (1200 / 24)", "If ₹1,200 is shared equally among 24 students, how much does each student pay?"),
]

for raw, expected in prompt_test_cases:
    cleaned = clean_prompt_text(raw)
    passed = (cleaned == expected)
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] Raw:      {raw}")
    print(f"       Cleaned:  {cleaned}")
    if not passed:
        print(f"       Expected: {expected}")
        sys.exit(1)

print("\n" + "=" * 60)
print("TEST 2: FIELD LABELS & DUPLICATE PREFIXES (Directive 2)")
print("=" * 60)

clue_test_cases = [
    ("Visual Clue: 🪐 Visual Clue: ☀️ The Sun anchors the center; planets orbit in curved paths!", "☀️ The Sun anchors the center; planets orbit in curved paths!"),
    ("💡 Visual Clue: 🔋 A circuit needs an unbroken loop from battery to bulb!", "🔋 A circuit needs an unbroken loop from battery to bulb!"),
    ("Visual Clue: Visual Clue: Water freezes into solid ice at 0°C", "Water freezes into solid ice at 0°C"),
    ("Hint: Clue: Look for the battery and switch!", "Look for the battery and switch!"),
    ("The Sun anchors the center; planets orbit in curved paths! ☀️🪐", "The Sun anchors the center; planets orbit in curved paths! ☀️🪐")
]

for raw, expected in clue_test_cases:
    cleaned = clean_visual_hint(raw)
    passed = (cleaned == expected)
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] Raw:      {raw}")
    print(f"       Cleaned:  {cleaned}")
    if not passed:
        print(f"       Expected: {expected}")
        sys.exit(1)

print("\n" + "=" * 60)
print("TEST 3: REAL INTERACTIVE GAME CONTENT (Directive 3)")
print("=" * 60)

topics_to_test = [
    "Solar System & Space",
    "Electricity & Circuits",
    "Animals & Birds",
    "Plants & Botany",
    "Odd and Even Numbers",
    "English Nouns and Verbs",
    "Arbitrary Custom Topic X"
]

forbidden_regex = re.compile(r'\b(?:Group\s+[AB]|Category\s+[AB]|Primary\s+Fact\s*\d*|Application\s+\d+|Card\s+\d+)\b', re.IGNORECASE)

for topic in topics_to_test:
    buckets, items = get_curriculum_interactive_sorter_data(topic)
    b_text = " ".join([b["label"] + " " + b.get("basket_label", "") + " " + b.get("category_name", "") for b in buckets])
    i_text = " ".join([it["text"] + " " + it.get("card_text", "") + " " + it.get("content", "") for it in items])
    
    match_b = forbidden_regex.findall(b_text)
    match_i = forbidden_regex.findall(i_text)
    
    passed = (len(match_b) == 0 and len(match_i) == 0 and len(buckets) >= 2 and len(items) >= 4)
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] Topic: '{topic}'")
    print(f"       Baskets: {[b['label'] for b in buckets]}")
    print(f"       Cards:   {[it['text'] for it in items[:4]]}...")
    if not passed:
        print(f"       Forbidden matches: Baskets={match_b}, Cards={match_i}")
        sys.exit(1)

print("\n" + "=" * 60)
print("TEST 4: FORMATTING DIRECTIVE FOR GAME SCHEMAS (Directive 4)")
print("=" * 60)

# Test build_fallback_small_scale_game output
game_task = build_fallback_small_scale_game(
    prompt="Solar System",
    class_name="IV",
    subject="Science",
    topic="Solar System & Space",
    engine_key="bucket-sorter",
    display_type="Sort & Group",
    conditions="",
    information=""
)

ic = game_task.get("interactiveConfig", {})
items = ic.get("items", [])
buckets = ic.get("buckets", [])

all_items_compliant = all("card_text" in it and "content" in it and "text" in it for it in items)
all_buckets_compliant = all("basket_label" in b and "category_name" in b and "label" in b for b in buckets)

print(f"Items count: {len(items)}, all have card_text & content: {all_items_compliant}")
print(f"Buckets count: {len(buckets)}, all have basket_label & category_name: {all_buckets_compliant}")

if not all_items_compliant or not all_buckets_compliant:
    print("Schema compliance FAILED!")
    sys.exit(1)
print("[PASS] Game schema contains 100% compliant fields across all cards and baskets!")

print("\n" + "=" * 60)
print("TEST 5: FALLBACK QUESTION GENERATION INTEGRATION")
print("=" * 60)

task = generate_smart_task("Which planet is closest to the Sun?", "IV", "Science", "Solar System", 4)
questions = task.get("questions", [])
for q_idx, q in enumerate(questions):
    prompt = q["prompt"]
    clue = q["visual_hint"]
    opts = q["options"]
    
    has_meta = bool(re.search(r'^\s*\[(?:Class\s*|Grade\s*)?[IVXLCDM\d\s\-_:\/|a-zA-Z]+\]', prompt))
    has_dup_clue = bool(re.search(r'visual\s*clue.*visual\s*clue', clue, re.IGNORECASE))
    
    print(f"Q{q_idx+1}: Prompt:    {prompt}")
    print(f"    Clue:      {clue}")
    print(f"    Meta tag:  {'YES (FAIL)' if has_meta else 'NO (PASS)'}")
    print(f"    Dup clue:  {'YES (FAIL)' if has_dup_clue else 'NO (PASS)'}")
    
    if has_meta or has_dup_clue:
        sys.exit(1)

print("\n" + "=" * 60)
print("ALL 5 VERIFICATION SUITES PASSED FLAWLESSLY!")
print("=" * 60)
