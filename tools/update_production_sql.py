import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Roman to Level
roman_levels = [('I', 1), ('II', 2), ('III', 3), ('IV', 4), ('V', 5), ('VI', 6), ('VII', 7), ('VIII', 8)]

# Extract unique subjects
subjects_set = set() # (class_roman, subject_name)
for g in catalog:
    subjects_set.add((g['class'], g['subject']))
subjects_list = sorted(list(subjects_set))

# Extract unique skills strictly from skill_areas_data
skills_set = set() # (class_roman, subject_name, skill_name)
for g in catalog:
    skills_set.add((g['class'], g['subject'], g['skillArea']))
skills_list = sorted(list(skills_set))

sql = """-- ================================================================================
-- MYCLASSBOARD GAMES - PRODUCTION DATABASE SETUP
-- PostgreSQL SQL Script
-- Status: Production Ready (All 440 Games & Quizzes with Curriculum Skills)
-- ================================================================================

-- ============================================================
-- 1. CLASSES TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS classes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(10) UNIQUE NOT NULL,
    description VARCHAR(255),
    level INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO classes (name, description, level) VALUES
"""

class_rows = [f"    ('{roman}', 'Class {roman} - Level {level}', {level})" for roman, level in roman_levels]
sql += ",\n".join(class_rows) + "\nON CONFLICT (name) DO NOTHING;\n\n"

sql += """-- ============================================================
-- 2. SUBJECTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    class_id INT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    order_index INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, class_id)
);

INSERT INTO subjects (name, description, class_id, order_index) VALUES
"""

sub_rows = []
for idx, (cls_roman, sub_name) in enumerate(subjects_list):
    cls_id = [r[0] for r in roman_levels].index(cls_roman) + 1
    sub_rows.append(f"    ('{sub_name}', '{sub_name} for Class {cls_roman}', {cls_id}, {idx + 1})")
sql += ",\n".join(sub_rows) + "\nON CONFLICT (name, class_id) DO NOTHING;\n\n"

sql += """-- ============================================================
-- 3. SKILLS TABLE (Strictly from skill_areas_data)
-- ============================================================
CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    subject_id INT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    class_id INT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    difficulty_level VARCHAR(20) DEFAULT 'intermediate',
    order_index INT DEFAULT 0,
    icon VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, subject_id)
);

-- Insert Skills dynamically mapped to subjects
"""

for cls_roman, sub_name, skill_name in skills_list:
    safe_skill = skill_name.replace("'", "''")
    sql += f"""INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT '{safe_skill}', '{safe_skill} skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = '{sub_name}' AND c.name = '{cls_roman}'
ON CONFLICT (name, subject_id) DO NOTHING;
"""

sql += """\n-- ============================================================
-- 4. GAMES TABLE (All 440 Curriculum Games & Quizzes)
-- ============================================================
CREATE TABLE IF NOT EXISTS games (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    skill_id INT NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    class_id INT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    game_type VARCHAR(50),
    file_path VARCHAR(255),
    difficulty_level VARCHAR(20) DEFAULT 'intermediate',
    max_score INT DEFAULT 3,
    questions_count INT DEFAULT 5,
    duration_minutes INT DEFAULT 5,
    icon VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    order_index INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Games dynamically mapped to skills and classes
"""

for idx, g in enumerate(catalog):
    cls_roman = g['class']
    sub_name = g['subject']
    skill_name = g['skillArea'].replace("'", "''")
    safe_title = g['title'].replace("'", "''")
    safe_desc = g.get('desc', g['activity']).replace("'", "''")
    game_type = g['gameType']
    questions_count = len(g.get('questions', []))
    diff_lvl = 'beginner' if cls_roman in ('I', 'II') else ('intermediate' if cls_roman in ('III', 'IV', 'V') else 'advanced')
    file_path = f"index.html#quest={g['id']}"

    sql += f"""INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT '{safe_title}', '{safe_desc}', sk.id, c.id, '{game_type}', '{file_path}', '{diff_lvl}', 3, {questions_count}, 5, TRUE, {idx + 1}
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = '{skill_name}' AND s.name = '{sub_name}' AND c.name = '{cls_roman}'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
"""

# Append students, teachers, assignments, scores, analytics tables
sql += """\n-- ============================================================
-- 5. TEACHERS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    class_id INT REFERENCES classes(id) ON DELETE SET NULL,
    department VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 6. STUDENTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(20) NOT NULL,
    class_id INT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    email VARCHAR(100),
    phone VARCHAR(20),
    parent_name VARCHAR(100),
    parent_phone VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(roll_number, class_id)
);

-- ============================================================
-- 7. ASSIGNMENTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS assignments (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    game_id INT NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    class_id INT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    subject_id INT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    skill_id INT NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    teacher_id INT REFERENCES teachers(id) ON DELETE SET NULL,
    assigned_by VARCHAR(100),
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deadline TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    is_mandatory BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 8. SCORES TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS scores (
    id SERIAL PRIMARY KEY,
    assignment_id INT REFERENCES assignments(id) ON DELETE SET NULL,
    student_id INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    game_id INT NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    class_id INT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    skill_id INT NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    score INT NOT NULL,
    max_score INT NOT NULL DEFAULT 50,
    percentage NUMERIC(5,2),
    correct_answers INT DEFAULT 0,
    wrong_answers INT DEFAULT 0,
    total_questions INT DEFAULT 5,
    completion_time INT,
    performance_level VARCHAR(20),
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 9. GAME PINS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS game_pins (
    id SERIAL PRIMARY KEY,
    pin VARCHAR(10) UNIQUE NOT NULL,
    game_id INT NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    teacher_id INT REFERENCES teachers(id) ON DELETE SET NULL,
    created_by VARCHAR(100),
    expires_at TIMESTAMP,
    max_attempts INT DEFAULT 1,
    current_attempts INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 10. SYSTEM SETTINGS & LOGS
-- ============================================================
CREATE TABLE IF NOT EXISTS system_settings (
    id SERIAL PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    description VARCHAR(255),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS api_logs (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INT,
    response_time_ms INT,
    ip_address VARCHAR(45),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

with open('database/CREATE-DATABASE-PRODUCTION.sql', 'w', encoding='utf-8') as f:
    f.write(sql)

print(f"✅ Generated and saved production SQL to database/CREATE-DATABASE-PRODUCTION.sql ({len(sql)} bytes)")
