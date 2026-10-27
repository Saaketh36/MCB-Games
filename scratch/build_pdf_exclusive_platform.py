# -*- coding: utf-8 -*-
"""
Generate 440 activities and question sets strictly from the provided PDF:
'skillAreaOutcomes - Sheet1.pdf'
Replaces all previous video/story data across the platform.
"""
import json
import re

def clean_str(s):
    if not s:
        return ""
    return (s.replace('‘', "'")
             .replace('’', "'")
             .replace('“', '"')
             .replace('”', '"')
             .replace('–', '-')
             .replace('—', '-')
             .replace('\uFFFD', "'")
             .strip())

with open('scratch/parsed_sample.json', 'r', encoding='utf-8') as f:
    records = json.load(f)

with open('skill_areas_data.json', 'r', encoding='utf-8') as f:
    sk_data = json.load(f)

skill_areas = sorted(list(set(item['skillArea'].strip() for item in sk_data if 'skillArea' in item)), key=len, reverse=True)
skill_areas.extend([
    'Measurement (Length, Weight, Capacity, Time, Money)',
    'Measurement, Recording & Representation'
])
skill_areas = sorted(skill_areas, key=len, reverse=True)

sub_skills = sorted(list(set(item['activity'].strip() for item in sk_data if 'activity' in item)), key=len, reverse=True)
sub_skills.extend([
    'Vocabulary',
    'Vocbulary',
    'Labelled Diagrams & Flow Charts',
    'Microscopy & Slide Preparation',
    'Chemical Word Equations',
    'Graphs',
    'Linear Equations',
    'Algebraic Identities'
])
sub_skills = sorted(sub_skills, key=len, reverse=True)

parsed_outcomes = []
for r in records:
    text = r['raw_rest']
    matched_sa = None
    for sa in skill_areas:
        if text.startswith(sa):
            matched_sa = sa
            break
    after_sa = text[len(matched_sa):].strip() if matched_sa else text
    matched_sub = None
    for sub in sub_skills:
        if after_sa.startswith(sub):
            matched_sub = sub
            break
    outcome = clean_str(after_sa[len(matched_sub):].strip() if matched_sub else after_sa)
    normalized_sub = 'Vocabulary' if matched_sub == 'Vocbulary' else (matched_sub or 'General')
    parsed_outcomes.append({
        'id': r['id'],
        'class': r['class'],
        'masterclassId': r['masterclassId'],
        'subject': r['subject'],
        'skillArea': clean_str(matched_sa or 'General'),
        'subSkillArea': clean_str(normalized_sub),
        'learningOutcome': outcome
    })

print(f"Total parsed outcomes: {len(parsed_outcomes)}")

SUBJECT_BADGES = {
    'English': 'badge-eng',
    'Mathematics': 'badge-mat',
    'EVS': 'badge-evs',
    'Science': 'badge-sci',
    'Social Science': 'badge-soc'
}

SUBJECT_THUMBS = {
    'English': 'images/game_english.jpg',
    'Mathematics': 'images/game_math.jpg',
    'EVS': 'images/game_evs.jpg',
    'Science': 'images/game_science.jpg',
    'Social Science': 'images/game_soc.jpg'
}

def derive_title(o):
    """Create a student-friendly, unique title from subskill and outcome text."""
    lo = o['learningOutcome']
    sub = o['subSkillArea']
    oid = o['id']
    
    quotes = re.findall(r"'([^']+)'", lo)
    if quotes and len(quotes) <= 3:
        quoted_part = ", ".join(f"'{q}'" for q in quotes[:2])
        return f"{sub}: {quoted_part} (LO #{oid})"
    
    eg = re.search(r'\((?:e\.g\.,?|viz\.|such as)\s*([^)]+)\)', lo, re.IGNORECASE)
    if eg:
        eg_text = eg.group(1).split(';')[0].split(',')[0].strip()
        if len(eg_text) < 30:
            return f"{sub} - {eg_text} (LO #{oid})"
    
    words = lo.split()
    first_part = " ".join(words[:5])
    return f"{sub}: {first_part} (LO #{oid})"

def determine_gametype(lo, sub):
    lo_lower = lo.lower()
    if 'sequence' in lo_lower or 'steps' in lo_lower or 'order' in lo_lower or 'drafting' in lo_lower:
        return 'Sequence Order'
    if 'match' in lo_lower or 'associates' in lo_lower or 'pairs' in lo_lower or 'differentiates' in lo_lower or 'compares' in lo_lower:
        return 'Match Pairs'
    if 'fill' in lo_lower or 'dictation' in lo_lower or 'writes words' in lo_lower or 'writes simple words' in lo_lower or 'types' in lo_lower:
        return 'Fill in the Blank'
    if 'identifies whether' in lo_lower or 'true' in lo_lower or 'false' in lo_lower or 'classifies' in lo_lower or 'verifies' in lo_lower:
        return 'True or False'
    return 'MCQ Quiz'

def generate_questions_for_outcome(o):
    """Generate 2 high-quality questions derived strictly from the outcome text and examples."""
    lo = o['learningOutcome']
    sub = o['subSkillArea']
    sa = o['skillArea']
    subj = o['subject']
    cls = o['class']
    oid = o['id']
    
    questions = []
    
    # Extract parenthetical examples if available (e.g., ...)
    eg_match = re.search(r'\((?:e\.g\.,?|viz\.|such as)\s*([^)]+)\)', lo, re.IGNORECASE)
    quotes = re.findall(r"'([^']+)'", lo)
    
    # Question 1: Core comprehension of the learning outcome
    # Check if there are explicit quotes
    if quotes:
        quoted_str = ", ".join(f"'{q}'" for q in quotes[:2])
        q1 = {
            "prompt": f"Which of the following directly reflects the curriculum focus in {sub}?",
            "options": [
                f"Using examples like {quoted_str}",
                "Memorizing random unrelated internet articles",
                "Inventing rules without any practice",
                "Skipping foundational learning completely"
            ],
            "answer": 0,
            "explanation": f"NCERT Learning Outcome #{oid} specifies: {lo}"
        }
    elif eg_match:
        eg_items = [item.strip() for item in eg_match.group(1).split(';') if item.strip()]
        if not eg_items:
            eg_items = [item.strip() for item in eg_match.group(1).split(',') if item.strip()]
        best_eg = eg_items[0] if eg_items else eg_match.group(1)
        q1 = {
            "prompt": f"In {subj} ({sub}), which example is explicitly studied according to the curriculum?",
            "options": [
                best_eg,
                "Unrelated industrial chemical synthesis",
                "Advanced orbital mechanics calculations",
                "Irrelevant non-curriculum concepts"
            ],
            "answer": 0,
            "explanation": f"NCERT Learning Outcome #{oid} states: {lo}"
        }
    else:
        # Grounded in the outcome text itself
        q1 = {
            "prompt": f"What is the key learning objective in Class {cls} {subj} for {sub}?",
            "options": [
                lo,
                "Ignoring all core concepts and instructions",
                "Focusing entirely on unverified external assumptions",
                "Practicing only disconnected trivia"
            ],
            "answer": 0,
            "explanation": f"NCERT Learning Outcome #{oid}: {lo}"
        }
    questions.append(q1)
    
    # Question 2: Action or application question
    q2 = {
        "prompt": f"When practicing '{sub}', what demonstrates achievement of Learning Outcome #{oid}?",
        "options": [
            f"The learner {lo[0].lower() + lo[1:] if len(lo) > 1 else lo}",
            "Guessing answers randomly without reading",
            "Leaving the exercise blank and unanswered",
            "Assuming facts not found in the official curriculum"
        ],
        "answer": 0,
        "explanation": f"Learning Outcome #{oid} ({sa} - {sub}): {lo}"
    }
    questions.append(q2)
    
    return questions

# Build full catalog
full_catalog = []
skill_areas_data = []

for o in parsed_outcomes:
    oid_str = f"LO-{o['id']:03d}"
    title = clean_str(derive_title(o))
    game_type = determine_gametype(o['learningOutcome'], o['subSkillArea'])
    badge_class = SUBJECT_BADGES.get(o['subject'], 'badge-eng')
    thumb = SUBJECT_THUMBS.get(o['subject'], 'images/game_english.jpg')
    questions = generate_questions_for_outcome(o)
    
    game = {
        "id": oid_str,
        "outcomeId": o['id'],
        "title": title,
        "class": o['class'],
        "masterclassId": o['masterclassId'],
        "subject": o['subject'],
        "skillArea": o['skillArea'],
        "activity": o['subSkillArea'],
        "subSkillArea": o['subSkillArea'],
        "learningOutcome": o['learningOutcome'],
        "gameType": game_type,
        "thumb": thumb,
        "badgeClass": badge_class,
        "desc": o['learningOutcome'],
        "time": "3 min",
        "stars": "3 stars",
        "topic": o['subSkillArea'],
        "questions": questions
    }
    full_catalog.append(game)
    
    # skill_areas_data entry
    skill_areas_data.append({
        "class": f"Class {o['class']}",
        "subject": o['subject'],
        "skillArea": o['skillArea'],
        "activity": o['subSkillArea'],
        "activityName": title,
        "gameType": game_type,
        "outcomeId": o['id'],
        "learningOutcome": o['learningOutcome']
    })

print(f"Generated {len(full_catalog)} games in full_catalog.")
print(f"Generated {len(skill_areas_data)} entries in skill_areas_data.")

# Verify Class I specifically
c1_games = [g for g in full_catalog if g['class'] == 'I']
print(f"Class I games count: {len(c1_games)}")
c1_listening = [g for g in c1_games if g['skillArea'] == 'Listening']
c1_reading = [g for g in c1_games if g['skillArea'] == 'Reading']
print(f"  Class I Listening: {len(c1_listening)}")
for g in c1_listening:
    print(f"    - {g['id']}: {g['title']}")
print(f"  Class I Reading: {len(c1_reading)}")
for g in c1_reading:
    print(f"    - {g['id']}: {g['title']}")

# Write to full_games_catalog.json
with open('full_games_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(full_catalog, f, indent=2, ensure_ascii=False)

# Write to full_games_catalog.js
with open('full_games_catalog.js', 'w', encoding='utf-8') as f:
    f.write("// Authoritative Games Catalog derived STRICTLY from 'skillAreaOutcomes - Sheet1.pdf'\n")
    f.write("// Total Learning Outcomes / Activities: 440 (Classes I to VIII)\n")
    f.write("const FULL_GAMES_CATALOG = ")
    json.dump(full_catalog, f, indent=2, ensure_ascii=False)
    f.write(";\n\n")
    f.write("if (typeof window !== 'undefined') {\n")
    f.write("    window.FULL_GAMES_CATALOG = FULL_GAMES_CATALOG;\n")
    f.write("    window.GamesCatalog = FULL_GAMES_CATALOG;\n")
    f.write("}\n")

# Write to skill_areas_data.json
with open('skill_areas_data.json', 'w', encoding='utf-8') as f:
    json.dump(skill_areas_data, f, indent=2, ensure_ascii=False)

# Write to curriculum-data.js
raw_lines = []
current_class = None
current_subject = None

for g in full_catalog:
    if g['class'] != current_class:
        current_class = g['class']
        current_subject = None
        raw_lines.append(f"@{current_class}")
    if g['subject'] != current_subject:
        current_subject = g['subject']
        raw_lines.append(f"!{current_subject}")
    raw_lines.append(f"{g['skillArea']}|{g['subSkillArea']}|{g['title']}|{g['gameType']}")

with open('curriculum-data.js', 'w', encoding='utf-8') as f:
    f.write("// Authoritative Curriculum Data derived STRICTLY from 'skillAreaOutcomes - Sheet1.pdf'\n")
    f.write("// Total Learning Outcomes: 440 across Classes I to VIII\n")
    f.write("(function (root) {\n")
    f.write("  const SUBJECT_CODE = { 'English': 'ENG', 'Mathematics': 'MAT', 'EVS': 'EVS', 'Science': 'SCI', 'Social Science': 'SOC' };\n")
    f.write("  const RAW = `\n" + "\n".join(raw_lines) + "\n`;\n\n")
    f.write("""  const ACTIVITIES = [];
  const CURRICULUM_DATA = {};
  let cls = '', subject = '';
  const counters = {};

  RAW.split('\\n').forEach(function (line) {
    line = line.trim();
    if (!line) return;
    if (line[0] === '@') { cls = line.slice(1); CURRICULUM_DATA[cls] = {}; return; }
    if (line[0] === '!') { subject = line.slice(1); CURRICULUM_DATA[cls][subject] = {}; return; }
    const p = line.split('|');
    const skill = p[0];
    const sub = p[1], name = p[2], type = p[3];
    const ck = cls + '-' + (SUBJECT_CODE[subject] || 'GEN');
    counters[ck] = (counters[ck] || 0) + 1;
    const id = ck + '-' + String(counters[ck]).padStart(2, '0');
    const act = { id: id, class: cls, subject: subject, skill: skill, subSkill: sub, name: name, type: type, file: 'play.html' };
    ACTIVITIES.push(act);
    const key = skill + ' – ' + sub;
    (CURRICULUM_DATA[cls][subject][key] = CURRICULUM_DATA[cls][subject][key] || []).push(act);
  });

  function getActivity(id) { return ACTIVITIES.find(function (a) { return a.id === id; }); }

  root.ACTIVITIES = ACTIVITIES;
  root.CURRICULUM_DATA = CURRICULUM_DATA;
  root.getActivity = getActivity;
  if (typeof module !== 'undefined' && module.exports) module.exports = { ACTIVITIES, CURRICULUM_DATA, getActivity };
})(typeof window !== 'undefined' ? window : globalThis);
""")

# Write to question_bank.js
qb = {}
for g in full_catalog:
    key = f"Class {g['class']}|||{g['subject']}|||{g['title']}"
    qb[key] = {
        "title": g['title'],
        "class": g['class'],
        "subject": g['subject'],
        "skillArea": g['skillArea'],
        "subSkillArea": g['subSkillArea'],
        "learningOutcome": g['learningOutcome'],
        "questions": g['questions']
    }

with open('question_bank.js', 'w', encoding='utf-8') as f:
    f.write("// Authoritative Question Bank derived STRICTLY from 'skillAreaOutcomes - Sheet1.pdf'\n")
    f.write("const QUESTION_BANK = ")
    json.dump(qb, f, indent=2, ensure_ascii=False)
    f.write(";\n\n")
    f.write("if (typeof module !== 'undefined' && module.exports) module.exports = { QUESTION_BANK };\n")

print("SUCCESS: Updated full_games_catalog.json, full_games_catalog.js, skill_areas_data.json, curriculum-data.js, and question_bank.js!")

