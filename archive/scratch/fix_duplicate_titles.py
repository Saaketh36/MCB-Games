import json

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

title_updates = {
    'LO-248': 'Ancient India: Harappan Civilization & First Cities',
    'LO-425': 'Colonial & Modern India: Decline and Rise of Urban Centres',
    'LO-259': 'Equality & Inequality: Understanding Everyday Differences',
    'LO-260': 'Diversity & Combating Discrimination: Identifying Sources',
    'LO-343': 'Democratic Equality: Political, Economic & Social Dimensions',
    'LO-344': 'Right to Equality: Regional Social & Economic Issues',
    'LO-322': 'Disaster Preparedness: Preventive Actions for Floods & Earthquakes',
    'LO-323': 'Environmental Calamities: Factors Leading to Disasters',
    'LO-416': 'Industrial Disasters & Landslides: Risk Reduction Measures',
    'LO-335': 'Medieval India: Administrative Measures of Khaljis & Tughlaqs',
    'LO-336': 'Medieval India: Socio-Political & Economic Transformations',
    'LO-339': 'Medieval India: Comparative Regional Developments',
    'LO-432': 'Historical Periods: Distinguishing Modern, Medieval & Ancient',
    'LO-340': 'Bhakti & Sufi Movements: Emergence of New Religious Ideas',
    'LO-341': 'Bhakti & Sufi Traditions: Inferences from Devotional Poetry',
    'LO-349': 'Role of Media: News Reporting & Creating Advertisements',
    'LO-435': 'How Laws are Made: RTI Act, RTE Act & Domestic Violence Act',
    'LO-412': 'Global Agricultural Production: Wheat, Rice, Cotton & Jute',
    'LO-414': 'Regional Agriculture: Farming Types & Local Crop Practices'
}

count = 0
for g in catalog:
    if g['id'] in title_updates:
        old = g['title']
        g['title'] = title_updates[g['id']]
        print(f"Updated [{g['id']}]: '{old}' -> '{g['title']}'")
        count += 1

print(f"Updated {count} titles.")

# Check for any remaining duplicates
titles = [g['title'] for g in catalog]
unique_titles = set(titles)
print(f"Total games: {len(titles)}, Unique titles: {len(unique_titles)}")
assert len(titles) == len(unique_titles), f"Still duplicates: {len(titles) - len(unique_titles)}"

# Save full_games_catalog.json
with open('full_games_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

# Save full_games_catalog.js
js_content = f"// Full Games Catalog for MyClassboard Games Platform\n// 440 Curriculum Games with Full Multi-Modal Question Bank\n\nconst FULL_GAMES_CATALOG = {json.dumps(catalog, indent=2, ensure_ascii=False)};\n\nif (typeof window !== 'undefined') {{\n    window.FULL_GAMES_CATALOG = FULL_GAMES_CATALOG;\n    window.GamesCatalog = FULL_GAMES_CATALOG;\n}}\n"
with open('full_games_catalog.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

# Update skill_areas_data.json
roman_to_class = {
    'I': 'Class I', 'II': 'Class II', 'III': 'Class III', 'IV': 'Class IV',
    'V': 'Class V', 'VI': 'Class VI', 'VII': 'Class VII', 'VIII': 'Class VIII'
}
clean_skills_data = []
for g in catalog:
    clean_skills_data.append({
        'class': roman_to_class[g['class']],
        'subject': g['subject'],
        'skillArea': g['skillArea'],
        'activity': g['activity'],
        'activityName': g['title'],
        'gameType': g['gameType']
    })

with open('skill_areas_data.json', 'w', encoding='utf-8') as f:
    json.dump(clean_skills_data, f, indent=2, ensure_ascii=False)

# Update question_bank.js
qb = {}
for g in catalog:
    key = f"Class {g['class']}|||{g['subject']}|||{g['title']}"
    qb[key] = {
        "title": g['title'],
        "class": g['class'],
        "subject": g['subject'],
        "skillArea": g['skillArea'],
        "subSkillArea": g.get('subSkillArea', g['activity']),
        "learningOutcome": g['learningOutcome'],
        "questions": g['questions']
    }

with open('question_bank.js', 'w', encoding='utf-8') as f:
    f.write("// Authoritative Question Bank derived STRICTLY from 'skillAreaOutcomes - Sheet1.pdf'\n")
    f.write("const QUESTION_BANK = ")
    json.dump(qb, f, indent=2, ensure_ascii=False)
    f.write(";\n\n")
    f.write("if (typeof module !== 'undefined' && module.exports) module.exports = { QUESTION_BANK };\n")

# Update curriculum-data.js
raw_lines = []
current_class = None
current_subject = None
for g in catalog:
    cls = g['class']
    subj = g['subject']
    if cls != current_class:
        current_class = cls
        current_subject = None
        raw_lines.append(f"@{cls}")
    if subj != current_subject:
        current_subject = subj
        raw_lines.append(f"!{subj}")
    sa = g['skillArea']
    sub = g['activity']
    title = g['title']
    gt = g['gameType']
    raw_lines.append(f"{sa}|{sub}|{title}|{gt}")

with open('curriculum-data.js', 'w', encoding='utf-8') as f:
    f.write("// Authoritative Curriculum Data derived strictly from 'skillAreaOutcomes - Sheet1.pdf'\n")
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

print("SUCCESS: Synchronized all files with 440 100% unique, curriculum-grounded titles!")
