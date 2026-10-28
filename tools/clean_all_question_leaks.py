import json
import re
import os
import glob
import sys

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, 'reconfigure'):
        stream.reconfigure(encoding='utf-8', errors='replace')

# -------------------------------------------------------------
# 1. OPTION CLEANER
# -------------------------------------------------------------
# Removes parenthetical math, proofs, steps, and calculations from option texts
# Examples:
#   "₹50 per student (24 x 50 = 1200)" -> "₹50 per student"
#   "2 more children (6 - 4 = 2)" -> "2 more children"
#   "8 cups (4 + 4 = 8)" -> "8 cups"
#   "6 teaspoons (2 x 3 = 6)" -> "6 teaspoons"
#   "13 (5 + 5 + 3)" -> "13"
#   "2 bottles (500 mL + 500 mL = 1000 mL)" -> "2 bottles"
#   "₹90 (60 + 30)" -> "₹90"
#   "Wednesday (2 + 7 = 9)" -> "Wednesday"
#   "October 8th (15 - 7 = 8)" -> "October 8th"
#   "3000 grams (3 x 1000)" -> "3000 grams"
#   "Two 500-gram weights (500 g + 500 g)" -> "Two 500-gram weights"
#   "4 guavas each (3 x 4 = 12)" -> "4 guavas each"
#   "Multiplication (6 x 5)" -> "Multiplication"
#   "Subtraction (6 - 5)" -> "Subtraction"
#   "Addition only (6 + 5)" -> "Addition only"
#   "Division (6 / 5)" -> "Division"
OPT_MATH_PAREN_RE = re.compile(
    r'\s*\([^)]*(?:[₹$]?\d+[^)]*[\+\-\*\/\=x×÷][^)]*(?:\d+|side|length|width)|[\+\-\*\/\=x×÷]\s*\d+)[^)]*\)',
    re.IGNORECASE
)

def clean_option(opt):
    if not isinstance(opt, str):
        return opt
    cleaned = OPT_MATH_PAREN_RE.sub('', opt).strip()
    return cleaned

# -------------------------------------------------------------
# 2. PROMPT / QUESTION STEM CLEANER
# -------------------------------------------------------------
# Removes formula leaks, calculation hints, and answer leaks from question stems
# Examples:
#   "how much does each student pay for travel? (1200 / 24)" -> "how much does each student pay for travel?"
#   "count them together (4 + 2)?" -> "count them together?"
#   "how many are left? (9 - 3)" -> "how many are left?"
#   "fill a 1-litre jug? (Hint: 1 Litre = 1000 mL)" -> "fill a 1-litre jug?"
#   "Convert 4 meters into centimeters. (Remember: 1 m = 100 cm)" -> "Convert 4 meters into centimeters."
#   "... Formula: 2(Length + Width)" -> "..."
#   "... Formula: V = πr²h, use π = 22/7" -> "..."
#   "Calculate: 0.25 x 1.6 = (Hint: 25 x 16 = 400; count 2 + 1 = 3 decimal places)" -> "Calculate: 0.25 x 1.6 ="

def clean_prompt(prompt):
    if not isinstance(prompt, str):
        return prompt
    p = prompt.strip()

    # 1. Trailing formula / calculation after question mark
    if '?' in p:
        p = re.sub(
            r'\?\s*(?:\([^)]*[\+\-\*\/\=x×÷][^)]*\)|[0-9x\s\*\/\+\-]+\([A-Z\s\+\-]+\)|Formula:.*|Hint:.*|Remember:.*|\(Find the Lowest Common Multiple.*|\(By negative exponent rule.*|\(Slope\s*=.*|\(Speed\s*x\s*Time.*|\(Step\s*\d+.*).*$',
            '?',
            p,
            flags=re.IGNORECASE
        ).strip()

    # 2. Parenthetical hint right before question mark:
    # e.g. "count together (4 + 2)?", "multiply it by 100 (e.g., 36 x 100)?", "5th SQUARE NUMBER (formed by a 5 x 5 square array of dots)?"
    p = re.sub(
        r'\s*\((?:(?:e\.g\.|Hint|Remember|Formula|Formulae|Clue|Step \d+|formed by)?:?\s*)?(?:[₹$]?\d+[^)]*[\+\-\*\/\=x×÷][^)]+|(?:Hint|Remember|Formula|Step \d+|formed by)[^)]+)\)\s*\?',
        '?',
        p,
        flags=re.IGNORECASE
    )

    # Clean specific remaining calculation hints before question marks:
    p = re.sub(r'\s*\(e\.g\.,?\s*[^)]*[\d\s]+[\+\-\*\/\=x×÷]+[^)]*\)\s*\?', '?', p, flags=re.IGNORECASE)
    p = re.sub(r'\s*\(formed by\s*[^)]*\)\s*\?', '?', p, flags=re.IGNORECASE)
    p = p.replace('Product of Extremes (a x d) and Product of Means (b x c)?', 'Product of Extremes and Product of Means?')

    # 3. Parenthetical hint at end of sentence
    p = re.sub(
        r'\s*\((?:(?:e\.g\.|Hint|Remember|Formula|Formulae|Clue|Step \d+)?:?\s*)?(?:[₹$]?\d+[^)]*[\+\-\*\/\=x×÷][^)]+|(?:Hint|Remember|Formula|Step \d+)[^)]+)\)\s*$',
        '',
        p,
        flags=re.IGNORECASE
    )

    # 4. Trailing working out that leaked answers in stems
    p = re.sub(r'\s+by treating 99 as.*$', ':', p)
    p = re.sub(r':\s*\(50 \+ 3\)\(50 - 3\).*$', ':', p)
    p = re.sub(r'=\s*2x\(3x \+ 4\).*$', '=', p)
    p = re.sub(r'=\s*10,000 x \(1\.10\)²\s*=', '=', p)
    p = re.sub(r'=\s*1\/2 x \(1\/4 \+ 2\/4\)\s*=', '=', p)
    p = re.sub(r'\s*\(40 \+ 50 \+ 50 \+ 60 \+ 100\) \/ 5\s*=', '', p)

    return p.strip()

# -------------------------------------------------------------
# 3. EXPLANATION ENHANCER
# -------------------------------------------------------------
def ensure_explanation(explanation, prompt, options, answer_idx):
    if not isinstance(explanation, str) or not explanation.strip():
        ans_text = options[answer_idx] if 0 <= answer_idx < len(options) else "the correct choice"
        return f"The correct answer is {ans_text}."
    return explanation.strip()

# -------------------------------------------------------------
# 4. EXECUTION ON TARGET FILES
# -------------------------------------------------------------

def process_full_games_catalog_json():
    target = 'full_games_catalog.json'
    print(f"Processing {target}...")
    with open(target, 'r', encoding='utf-8') as f:
        data = json.load(f)

    q_count = 0
    opt_count = 0
    for game in data:
        for q in game.get('questions', []):
            prompt = q.get('prompt', '') or q.get('question', '')
            cp = clean_prompt(prompt)
            if cp != prompt:
                q['prompt'] = cp
                q_count += 1

            opts = q.get('options', [])
            new_opts = []
            for opt in opts:
                co = clean_option(opt)
                if co != opt:
                    opt_count += 1
                new_opts.append(co)
            q['options'] = new_opts

            ans = q.get('answer', 0)
            exp = q.get('explanation', '')
            q['explanation'] = ensure_explanation(exp, cp, new_opts, ans)

    with open(target, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  -> Cleaned {q_count} prompts and {opt_count} options in {target}")

def process_full_games_catalog_js():
    target = 'full_games_catalog.js'
    print(f"Syncing {target} from full_games_catalog.json...")
    with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    js_content = "// Authoritative Games Catalog derived STRICTLY from 'skillAreaOutcomes - Sheet1.pdf'\n"
    js_content += "// Total Learning Outcomes / Activities: 440 (Classes I to VIII)\n"
    js_content += "const FULL_GAMES_CATALOG = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n\n"
    js_content += "if (typeof window !== 'undefined') {\n"
    js_content += "    window.FULL_GAMES_CATALOG = FULL_GAMES_CATALOG;\n"
    js_content += "    window.GamesCatalog = FULL_GAMES_CATALOG;\n"
    js_content += "}\n"

    with open(target, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"  -> Updated {target}")

def process_question_bank_js():
    target = 'question_bank.js'
    print(f"Processing {target}...")
    with open(target, 'r', encoding='utf-8') as f:
        text = f.read()

    # question_bank.js has: const QUESTION_BANK = { ... };
    mod_idx = text.find('if (typeof module')
    if mod_idx != -1:
        brace_end = text[:mod_idx].rfind('}')
        suffix = text[brace_end + 1:]
    else:
        brace_end = text.rfind('}')
        suffix = text[brace_end + 1:]

    brace_start = text.index('{')
    prefix = text[:brace_start]
    json_text = text[brace_start:brace_end + 1].strip()

    data = json.loads(json_text)
    q_count = 0
    opt_count = 0
    for act_key, act_val in data.items():
        for q in act_val.get('questions', []):
            prompt = q.get('prompt', '') or q.get('question', '')
            cp = clean_prompt(prompt)
            if cp != prompt:
                if 'prompt' in q:
                    q['prompt'] = cp
                if 'question' in q:
                    q['question'] = cp
                q_count += 1

            opts = q.get('options', [])
            new_opts = []
            for opt in opts:
                co = clean_option(opt)
                if co != opt:
                    opt_count += 1
                new_opts.append(co)
            q['options'] = new_opts

            ans = q.get('answer', 0)
            exp = q.get('explanation', '')
            q['explanation'] = ensure_explanation(exp, cp, new_opts, ans)

    new_text = prefix + json.dumps(data, indent=2, ensure_ascii=False) + suffix
    with open(target, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print(f"  -> Cleaned {q_count} prompts and {opt_count} options in {target}")

def process_content_classes():
    for fpath in sorted(glob.glob('content/class-*.js')):
        print(f"Processing {fpath}...")
        with open(fpath, 'r', encoding='utf-8') as f:
            text = f.read()

        brace_start = text.find('{', text.find('Object.assign'))
        brace_end = text.rfind('}')
        if brace_start == -1 or brace_end == -1:
            print(f"  Skipping {fpath}: could not find Object.assign dict")
            continue

        prefix = text[:brace_start]
        json_text = text[brace_start:brace_end + 1]
        suffix = text[brace_end + 1:]

        try:
            data = json.loads(json_text)
        except Exception as e:
            print(f"  JSON decode failed on {fpath}: {e}")
            continue

        q_count = 0
        opt_count = 0
        for act_id, act_val in data.items():
            for q in act_val.get('questions', []):
                prompt = q.get('q', '')
                cp = clean_prompt(prompt)
                if cp != prompt:
                    q['q'] = cp
                    q_count += 1

                opts = q.get('options', [])
                new_opts = []
                for opt in opts:
                    co = clean_option(opt)
                    if co != opt:
                        opt_count += 1
                    new_opts.append(co)
                q['options'] = new_opts

                ans = q.get('answer', 0)
                exp = q.get('explain', '')
                q['explain'] = ensure_explanation(exp, cp, new_opts, ans)

        new_text = prefix + json.dumps(data, indent=2, ensure_ascii=False) + suffix
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f"  -> Cleaned {q_count} prompts and {opt_count} options in {fpath}")

def process_scratch_generators():
    for fpath in sorted(glob.glob('archive/scratch/generators/gen_class*.py')):
        print(f"Processing generator {fpath}...")
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        def replace_prompt_line(m):
            lead = m.group(1)
            text = m.group(2)
            trail = m.group(3)
            return lead + clean_prompt(text) + trail

        new_content = re.sub(r'("prompt"\s*:\s*")([^"]+)(")', replace_prompt_line, content)
        new_content = re.sub(r'("q"\s*:\s*")([^"]+)(")', replace_prompt_line, new_content)
        new_content = OPT_MATH_PAREN_RE.sub('', new_content)

        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  -> Cleaned {fpath}")
        else:
            print(f"  -> No changes needed in {fpath}")

def process_sql_files():
    for fpath in sorted(glob.glob('database/*.sql')):
        print(f"Processing SQL {fpath}...")
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        cleaned_sql = OPT_MATH_PAREN_RE.sub('', content)
        if cleaned_sql != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(cleaned_sql)
            print(f"  -> Cleaned {fpath}")

if __name__ == '__main__':
    process_full_games_catalog_json()
    process_full_games_catalog_js()
    process_question_bank_js()
    process_content_classes()
    process_scratch_generators()
    process_sql_files()
    print("\nALL FILES PROCESSED SUCCESSFULLY!")
