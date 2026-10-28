import json
import re

def clean_option_giveaways(opt):
    if not isinstance(opt, str):
        return opt
    s = opt.strip()
    
    # 1. Trailing calculation or colon working out: e.g. "₹1,500: Discount = ..." -> "₹1,500"
    if re.match(r'^(?:[₹$]?\d+(?:,\d+)*(?:\.\d+)?(?:\s*(?:m²|cm²|square meters|meters|cm|km|%|°))?)\s*:\s*.+$', s):
        s = re.sub(r':\s*.+$', '', s).strip()
        
    # 2. Probability working out: "6/36 = 1/6 (favorable...)" -> "1/6"
    m_prob = re.match(r'^\d+\/\d+\s*=\s*(\d+\/\d+)\s*\(.*$', s)
    if m_prob:
        s = m_prob.group(1).strip()
        
    # 3. Repeated subtraction / multiplication steps:
    if 'Subtract 3 repeatedly:' in s:
        s = "Subtract 3 repeatedly until reaching 0"
        
    # 4. Remove all parenthetical explanations, definitions, translations, proofs:
    # e.g.:
    # "0 (Zero)" -> "0"
    # "15 (fifteen)" -> "15"
    # "Bananas (6)" -> "Bananas"
    # "Team Yellow (15 players)" -> "Team Yellow"
    # "By school bus (10 children)" -> "By school bus"
    # "< (8 is less than 14)" -> "<"
    # "> (8 is greater than 14)" -> ">"
    # "= (8 is equal to 14)" -> "="
    # "A round coin (rolls on its edge, slides on its flat face)" -> "A round coin"
    # "A full stop (period)" -> "A full stop"
    # "Sleeping through the night (8 to 9 hours)" -> "Sleeping through the night"
    # "West (where the sun sets in the evening)" -> "West"
    # "Your father's mother and father (Dadi and Dada)" -> "Your father's parents"
    # "Four vertical lines with a diagonal slash across them (卌)" -> "Four vertical lines with a diagonal slash"
    # "8 centimeters (8 cm)" -> "8 centimeters"
    # "Both sides have the exact same weight (equal)" -> "Both sides have the exact same weight"
    # "With a Capital letter (Proper Noun)" -> "With a capital letter"
    
    # Remove parenthetical counts/times/translations/explanations
    s = re.sub(r'\s*\([^)]+\)', '', s).strip()
    
    # Clean up double spaces or trailing punctuation artifacts
    s = re.sub(r'\s{2,}', ' ', s)
    s = s.strip()
    
    return s

def clean_catalog(target_path='full_games_catalog.json'):
    with open(target_path, 'r', encoding='utf-8') as f:
        games = json.load(f)
        
    cleaned_count = 0
    for g in games:
        for q in g.get('questions', []):
            opts = q.get('options', [])
            new_opts = []
            for o in opts:
                co = clean_option_giveaways(o)
                if co != o:
                    cleaned_count += 1
                new_opts.append(co)
            q['options'] = new_opts
            
    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump(games, f, indent=2, ensure_ascii=False)
        
    print(f"Cleaned {cleaned_count} options in {target_path}")

if __name__ == '__main__':
    clean_catalog()

