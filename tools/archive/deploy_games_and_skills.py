import json
import os
import sys
import psycopg2
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

print("=" * 70)
print("DEPLOYING GAMES, QUIZZES, AND SKILL AREAS TO PLATFORM & DATABASE")
print("=" * 70)

# Step 1: Load catalog and skills
with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

print(f"Loaded {len(catalog)} games from full_games_catalog.json")

# Standardize skillArea: "Measurement (Length, Weight, Capacity, Time)"
for game in catalog:
    if 'Measurement' in game.get('skillArea', ''):
        game['skillArea'] = 'Measurement (Length, Weight, Capacity, Time)'

# Save updated full_games_catalog.json
with open('full_games_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)
print("✅ Updated full_games_catalog.json with standardized skillArea")

# Save updated full_games_catalog.js
js_content = f"// Full Games Catalog for MyClassboard Games Platform\n// 325 Curriculum Games with Full Multi-Modal Question Bank\n\nconst FULL_GAMES_CATALOG = {json.dumps(catalog, indent=2, ensure_ascii=False)};\n\nif (typeof window !== 'undefined') {{\n    window.FULL_GAMES_CATALOG = FULL_GAMES_CATALOG;\n    window.GamesCatalog = FULL_GAMES_CATALOG;\n}}\n"
with open('full_games_catalog.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
print("✅ Updated full_games_catalog.js")

# Step 2: Build clean skill_areas_data.json
roman_to_class = {
    'I': 'Class I',
    'II': 'Class II',
    'III': 'Class III',
    'IV': 'Class IV',
    'V': 'Class V',
    'VI': 'Class VI',
    'VII': 'Class VII',
    'VIII': 'Class VIII'
}

clean_skills_data = []
for game in catalog:
    cls_str = roman_to_class[game['class']]
    clean_skills_data.append({
        'class': cls_str,
        'subject': game['subject'],
        'skillArea': game['skillArea'],
        'activity': game['activity'],
        'activityName': game['title'],
        'gameType': game['gameType']
    })

with open('skill_areas_data.json', 'w', encoding='utf-8') as f:
    json.dump(clean_skills_data, f, indent=2, ensure_ascii=False)
print(f"✅ Updated skill_areas_data.json with {len(clean_skills_data)} clean entries")

# Step 3: Update curriculum_catalog.json
curr_catalog = []
for game in catalog:
    curr_catalog.append([
        game['class'],
        game['subject'],
        f"{game['skillArea']} – {game['activity']}",
        game['title']
    ])
with open('curriculum_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(curr_catalog, f, ensure_ascii=False)
print("✅ Updated curriculum_catalog.json")

# Step 4: Update curriculum-data.js MEAS token if needed
with open('curriculum-data.js', 'r', encoding='utf-8') as f:
    cdata = f.read()
if 'Measurement (Length, Weight, Capacity, Time, Money)' in cdata:
    cdata = cdata.replace(
        "MEAS: 'Measurement (Length, Weight, Capacity, Time, Money)',",
        "MEAS: 'Measurement (Length, Weight, Capacity, Time)',"
    )
    with open('curriculum-data.js', 'w', encoding='utf-8') as f:
        f.write(cdata)
    print("✅ Updated curriculum-data.js MEAS token")

# Step 5: Deploy to PostgreSQL Database
db_url = os.getenv('DATABASE_URL', '').replace('+psycopg2', '')
print(f"\n🔄 Connecting to PostgreSQL database...")
conn = psycopg2.connect(db_url)
conn.autocommit = False
cur = conn.cursor()

try:
    # 5.1 Ensure classes I through VIII exist
    classes_map = {} # 'I' -> id
    for roman, level in [('I', 1), ('II', 2), ('III', 3), ('IV', 4), ('V', 5), ('VI', 6), ('VII', 7), ('VIII', 8)]:
        cur.execute("SELECT id FROM classes WHERE name = %s;", (roman,))
        row = cur.fetchone()
        if row:
            classes_map[roman] = row[0]
        else:
            cur.execute(
                "INSERT INTO classes (name, description, level) VALUES (%s, %s, %s) RETURNING id;",
                (roman, f"Class {roman} - Level {level}", level)
            )
            classes_map[roman] = cur.fetchone()[0]
    print(f"  ✅ Verified {len(classes_map)} classes in database")

    # 5.2 Build unique subjects per class from clean_skills_data
    # Maps (class_roman, subject_name) -> subject_id
    subjects_needed = set()
    for g in catalog:
        subjects_needed.add((g['class'], g['subject']))

    subjects_map = {}
    order_idx = 1
    for cls_roman, sub_name in sorted(subjects_needed):
        cls_id = classes_map[cls_roman]
        cur.execute("SELECT id FROM subjects WHERE name = %s AND class_id = %s;", (sub_name, cls_id))
        row = cur.fetchone()
        if row:
            subjects_map[(cls_roman, sub_name)] = row[0]
        else:
            cur.execute(
                "INSERT INTO subjects (name, description, class_id, order_index) VALUES (%s, %s, %s, %s) RETURNING id;",
                (sub_name, f"{sub_name} for Class {cls_roman}", cls_id, order_idx)
            )
            subjects_map[(cls_roman, sub_name)] = cur.fetchone()[0]
            order_idx += 1
    print(f"  ✅ Verified {len(subjects_map)} subjects in database")

    # 5.3 Skills: ONLY add skill areas from skill_areas_data.json
    # First, let's identify valid skill areas per (class, subject)
    skills_needed = set() # (class_roman, subject_name, skill_area_name)
    for g in catalog:
        skills_needed.add((g['class'], g['subject'], g['skillArea']))

    # To ensure "only add skill areas from skill areas data", remove any old legacy skills
    # that don't belong to the official skill areas data
    skills_map = {} # (class_roman, subject_name, skill_name) -> skill_id
    skill_order = 1
    for cls_roman, sub_name, skill_name in sorted(skills_needed):
        cls_id = classes_map[cls_roman]
        sub_id = subjects_map[(cls_roman, sub_name)]
        cur.execute(
            "SELECT id FROM skills WHERE name = %s AND subject_id = %s;",
            (skill_name, sub_id)
        )
        row = cur.fetchone()
        if row:
            skills_map[(cls_roman, sub_name, skill_name)] = row[0]
            # Ensure class_id is correct
            cur.execute("UPDATE skills SET class_id = %s WHERE id = %s;", (cls_id, row[0]))
        else:
            cur.execute(
                "INSERT INTO skills (name, description, subject_id, class_id, difficulty_level, order_index) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;",
                (skill_name, f"{skill_name} skill under {sub_name}", sub_id, cls_id, 'intermediate', skill_order)
            )
            skills_map[(cls_roman, sub_name, skill_name)] = cur.fetchone()[0]
            skill_order += 1
    print(f"  ✅ Verified {len(skills_map)} skill areas in database (strictly from skill_areas_data)")

    # 5.4 Deploy Games and Quizzes
    # Delete old obsolete games not in the 325 games catalog
    valid_titles = set(g['title'] for g in catalog)
    cur.execute("SELECT id, name FROM games;")
    existing_games = cur.fetchall()
    obsolete_ids = [row[0] for row in existing_games if row[1] not in valid_titles]
    if obsolete_ids:
        cur.execute("DELETE FROM games WHERE id = ANY(%s);", (obsolete_ids,))
        print(f"  🧹 Removed {len(obsolete_ids)} obsolete dummy games")

    # Upsert all 325 games
    games_deployed = 0
    for idx, g in enumerate(catalog):
        cls_roman = g['class']
        cls_id = classes_map[cls_roman]
        sub_name = g['subject']
        skill_name = g['skillArea']
        skill_id = skills_map[(cls_roman, sub_name, skill_name)]
        title = g['title']
        game_type = g['gameType']
        desc = g.get('desc', f"{g['activity']} ({game_type})")
        questions_count = len(g.get('questions', []))
        level = 'beginner' if cls_roman in ('I', 'II') else ('intermediate' if cls_roman in ('III', 'IV', 'V') else 'advanced')
        file_path = f"index.html#quest={g['id']}"

        cur.execute("SELECT id FROM games WHERE name = %s;", (title,))
        row = cur.fetchone()
        if row:
            cur.execute("""
                UPDATE games SET
                    description = %s,
                    skill_id = %s,
                    class_id = %s,
                    game_type = %s,
                    file_path = %s,
                    difficulty_level = %s,
                    questions_count = %s,
                    max_score = 3,
                    duration_minutes = 5,
                    is_active = TRUE,
                    order_index = %s,
                    updated_at = NOW()
                WHERE id = %s;
            """, (desc, skill_id, cls_id, game_type, file_path, level, questions_count, idx + 1, row[0]))
        else:
            cur.execute("""
                INSERT INTO games (
                    name, description, skill_id, class_id, game_type, file_path,
                    difficulty_level, max_score, questions_count, duration_minutes,
                    is_active, order_index, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    TRUE, %s, NOW(), NOW()
                );
            """, (title, desc, skill_id, cls_id, game_type, file_path, level, 3, questions_count, 5, idx + 1))
        games_deployed += 1

    print(f"  ✅ Deployed all {games_deployed} games and quizzes to database!")

    # 5.5 Deploy / Sync Students from StudentRosters
    student_rosters = {
        "I": [
            (101, "Aarav Sharma"), (102, "Ananya Verma"), (103, "Ishaan Gupta"),
            (104, "Kavya Nair"), (105, "Rohan Mehra")
        ],
        "II": [
            (201, "Aditya Rao"), (202, "Diya Pillai"), (203, "Manish Joshi"),
            (204, "Riya Sen"), (205, "Vivaan Malhotra")
        ],
        "III": [
            (301, "Aryan Saxena"), (302, "Ira Singhania"), (303, "Kabir Das"),
            (304, "Meera Iyer"), (305, "Reyansh Bhatt")
        ],
        "IV": [
            (401, "Aarav Sharma"), (402, "Ananya Reddy"), (403, "Arjun Patel"),
            (404, "Diya Rao"), (405, "Ishaan Kumar"), (406, "Meera Nair"),
            (407, "Rohan Gupta"), (408, "Saanvi Reddy"), (409, "Vihaan Shah"), (410, "Zoya Khan")
        ],
        "V": [
            (501, "Armaan Malik"), (502, "Devika Menon"), (503, "Karan Johar"),
            (504, "Pooja Hegde"), (505, "Siddharth Roy")
        ],
        "VI": [
            (601, "Abhinav Bindra"), (602, "Fatima Sana"), (603, "Gautam Gambhir"),
            (604, "Harmanpreet Kaur"), (605, "Jasprit Bumrah")
        ],
        "VII": [
            (701, "Alia Bhatt"), (702, "Deepika Padukone"), (703, "Ranbir Kapoor"),
            (704, "Ranveer Singh"), (705, "Varun Dhawan")
        ],
        "VIII": [
            (801, "Anushka Sharma"), (802, "KL Rahul"), (803, "Rohit Sharma"),
            (804, "Smriti Mandhana"), (805, "Virat Kohli")
        ]
    }

    students_count = 0
    for cls_roman, students_list in student_rosters.items():
        cls_id = classes_map[cls_roman]
        for roll, sname in students_list:
            cur.execute("SELECT id FROM students WHERE roll_number = %s AND class_id = %s;", (str(roll), cls_id))
            row = cur.fetchone()
            if row:
                cur.execute("UPDATE students SET name = %s, is_active = TRUE WHERE id = %s;", (sname, row[0]))
            else:
                cur.execute("""
                    INSERT INTO students (name, roll_number, class_id, is_active, created_at, updated_at)
                    VALUES (%s, %s, %s, TRUE, NOW(), NOW());
                """, (sname, str(roll), cls_id))
            students_count += 1
    print(f"  ✅ Verified {students_count} students across all classes")

    # Clean any legacy orphan skills with 0 games
    cur.execute("""
        DELETE FROM skills WHERE id NOT IN (SELECT DISTINCT skill_id FROM games);
    """)
    print("  ✅ Pruned any unused skill entries to strictly enforce skill areas from data")

    # Clean any legacy orphan subjects with 0 skills
    cur.execute("""
        DELETE FROM subjects WHERE id NOT IN (SELECT DISTINCT subject_id FROM skills);
    """)
    print("  ✅ Pruned any unused subject entries to strictly enforce curriculum subjects")

    conn.commit()
    print("\n🎉 PostgreSQL database transaction committed successfully!")

except Exception as e:
    conn.rollback()
    print(f"❌ Error during database deployment: {e}")
    raise
finally:
    cur.close()
    conn.close()

print("\n" + "=" * 70)
print("DATABASE & CURRICULUM DEPLOYMENT COMPLETE")
print("=" * 70)
