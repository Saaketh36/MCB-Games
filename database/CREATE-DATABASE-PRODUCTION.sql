-- ================================================================================
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
    ('I', 'Class I - Level 1', 1),
    ('II', 'Class II - Level 2', 2),
    ('III', 'Class III - Level 3', 3),
    ('IV', 'Class IV - Level 4', 4),
    ('V', 'Class V - Level 5', 5),
    ('VI', 'Class VI - Level 6', 6),
    ('VII', 'Class VII - Level 7', 7),
    ('VIII', 'Class VIII - Level 8', 8)
ON CONFLICT (name) DO NOTHING;

-- ============================================================
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
    ('English', 'English for Class I', 1, 1),
    ('Mathematics', 'Mathematics for Class I', 1, 2),
    ('English', 'English for Class II', 2, 3),
    ('Mathematics', 'Mathematics for Class II', 2, 4),
    ('EVS', 'EVS for Class III', 3, 5),
    ('English', 'English for Class III', 3, 6),
    ('Mathematics', 'Mathematics for Class III', 3, 7),
    ('EVS', 'EVS for Class IV', 4, 8),
    ('English', 'English for Class IV', 4, 9),
    ('Mathematics', 'Mathematics for Class IV', 4, 10),
    ('EVS', 'EVS for Class V', 5, 11),
    ('English', 'English for Class V', 5, 12),
    ('Mathematics', 'Mathematics for Class V', 5, 13),
    ('English', 'English for Class VI', 6, 14),
    ('Mathematics', 'Mathematics for Class VI', 6, 15),
    ('Science', 'Science for Class VI', 6, 16),
    ('Social Science', 'Social Science for Class VI', 6, 17),
    ('English', 'English for Class VII', 7, 18),
    ('Mathematics', 'Mathematics for Class VII', 7, 19),
    ('Science', 'Science for Class VII', 7, 20),
    ('Social Science', 'Social Science for Class VII', 7, 21),
    ('English', 'English for Class VIII', 8, 22),
    ('Mathematics', 'Mathematics for Class VIII', 8, 23),
    ('Science', 'Science for Class VIII', 8, 24),
    ('Social Science', 'Social Science for Class VIII', 8, 25)
ON CONFLICT (name, class_id) DO NOTHING;

-- ============================================================
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
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Listening', 'Listening skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'I'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Reading', 'Reading skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'I'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Speaking', 'Speaking skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'I'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Vocabulary & Grammar', 'Vocabulary & Grammar skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'I'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Writing', 'Writing skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'I'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Data Handling', 'Data Handling skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'I'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money)', 'Measurement (Length, Weight, Capacity, Time, Money) skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'I'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Numbers & Operations', 'Numbers & Operations skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'I'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Patterns', 'Patterns skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'I'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Shapes & Spatial Understanding', 'Shapes & Spatial Understanding skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'I'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Listening', 'Listening skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'II'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Reading', 'Reading skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'II'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Speaking', 'Speaking skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'II'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Vocabulary & Grammar', 'Vocabulary & Grammar skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'II'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Writing', 'Writing skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'II'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Data Handling', 'Data Handling skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'II'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money)', 'Measurement (Length, Weight, Capacity, Time, Money) skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'II'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Numbers & Operations', 'Numbers & Operations skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'II'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Shapes & Spatial Understanding', 'Shapes & Spatial Understanding skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'II'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Classification & Grouping', 'Classification & Grouping skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Creative Expression', 'Creative Expression skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Estimation, Experimentation & Recording', 'Estimation, Experimentation & Recording skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Explanation & Understanding Relationships', 'Explanation & Understanding Relationships skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Mapping & Spatial Skills', 'Mapping & Spatial Skills skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Observation & Identification', 'Observation & Identification skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Past & Present (Change over Time)', 'Past & Present (Change over Time) skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Values, Sensitivity & Opinion', 'Values, Sensitivity & Opinion skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Listening', 'Listening skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Reading', 'Reading skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Speaking', 'Speaking skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Vocabulary & Grammar', 'Vocabulary & Grammar skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Writing', 'Writing skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Data Handling', 'Data Handling skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money)', 'Measurement (Length, Weight, Capacity, Time, Money) skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Numbers & Operations', 'Numbers & Operations skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Patterns', 'Patterns skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Shapes & Spatial Understanding', 'Shapes & Spatial Understanding skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Classification & Grouping', 'Classification & Grouping skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Creative Expression', 'Creative Expression skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Estimation, Experimentation & Recording', 'Estimation, Experimentation & Recording skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Explanation & Understanding Relationships', 'Explanation & Understanding Relationships skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Mapping & Spatial Skills', 'Mapping & Spatial Skills skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Observation & Identification', 'Observation & Identification skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Past & Present (Change over Time)', 'Past & Present (Change over Time) skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Values, Sensitivity & Opinion', 'Values, Sensitivity & Opinion skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Listening', 'Listening skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Reading', 'Reading skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Speaking', 'Speaking skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Vocabulary & Grammar', 'Vocabulary & Grammar skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Writing', 'Writing skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Data Handling', 'Data Handling skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money)', 'Measurement (Length, Weight, Capacity, Time, Money) skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Numbers & Operations', 'Numbers & Operations skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Patterns', 'Patterns skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Shapes & Spatial Understanding', 'Shapes & Spatial Understanding skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Classification & Grouping', 'Classification & Grouping skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Creative Expression', 'Creative Expression skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Estimation, Experimentation & Recording', 'Estimation, Experimentation & Recording skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Explanation & Understanding Relationships', 'Explanation & Understanding Relationships skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Mapping & Spatial Skills', 'Mapping & Spatial Skills skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Past & Present (Change over Time)', 'Past & Present (Change over Time) skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Values, Sensitivity & Opinion', 'Values, Sensitivity & Opinion skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Listening', 'Listening skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Reading', 'Reading skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Speaking', 'Speaking skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Vocabulary & Grammar', 'Vocabulary & Grammar skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Writing', 'Writing skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Data Handling', 'Data Handling skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money)', 'Measurement (Length, Weight, Capacity, Time, Money) skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Numbers & Operations', 'Numbers & Operations skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Patterns', 'Patterns skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Shapes & Spatial Understanding', 'Shapes & Spatial Understanding skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Listening', 'Listening skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Reading', 'Reading skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Speaking', 'Speaking skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Vocabulary & Grammar', 'Vocabulary & Grammar skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Writing', 'Writing skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Algebra', 'Algebra skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Data Handling', 'Data Handling skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Geometry', 'Geometry skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Mensuration', 'Mensuration skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Number System', 'Number System skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Ratio, Proportion & Commercial Arithmetic', 'Ratio, Proportion & Commercial Arithmetic skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Classification', 'Classification skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Environmental Awareness, Creativity & Values', 'Environmental Awareness, Creativity & Values skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Explaining Processes & Cause-Effect', 'Explaining Processes & Cause-Effect skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Identification & Differentiation', 'Identification & Differentiation skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Measurement, Recording & Representation', 'Measurement, Recording & Representation skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Models & Application in Daily Life', 'Models & Application in Daily Life skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Scientific Inquiry & Investigation', 'Scientific Inquiry & Investigation skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Geography', 'Geography skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'History', 'History skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Social & Political Life (Civics & Economics)', 'Social & Political Life (Civics & Economics) skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Listening', 'Listening skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Reading', 'Reading skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Speaking', 'Speaking skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Vocabulary & Grammar', 'Vocabulary & Grammar skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Writing', 'Writing skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Algebra', 'Algebra skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Data Handling', 'Data Handling skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Geometry', 'Geometry skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Mensuration', 'Mensuration skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Number System', 'Number System skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Ratio, Proportion & Commercial Arithmetic', 'Ratio, Proportion & Commercial Arithmetic skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Classification', 'Classification skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Environmental Awareness, Creativity & Values', 'Environmental Awareness, Creativity & Values skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Explaining Processes & Cause-Effect', 'Explaining Processes & Cause-Effect skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Identification & Differentiation', 'Identification & Differentiation skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Measurement, Recording & Representation', 'Measurement, Recording & Representation skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Models & Application in Daily Life', 'Models & Application in Daily Life skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Scientific Inquiry & Investigation', 'Scientific Inquiry & Investigation skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Geography', 'Geography skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'History', 'History skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Social & Political Life (Civics & Economics)', 'Social & Political Life (Civics & Economics) skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Listening', 'Listening skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Reading', 'Reading skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Speaking', 'Speaking skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Vocabulary & Grammar', 'Vocabulary & Grammar skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Writing', 'Writing skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Algebra', 'Algebra skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Data Handling', 'Data Handling skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Geometry', 'Geometry skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Mensuration', 'Mensuration skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Number System', 'Number System skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Ratio, Proportion & Commercial Arithmetic', 'Ratio, Proportion & Commercial Arithmetic skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Classification', 'Classification skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Environmental Awareness, Creativity & Values', 'Environmental Awareness, Creativity & Values skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Explaining Processes & Cause-Effect', 'Explaining Processes & Cause-Effect skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Identification & Differentiation', 'Identification & Differentiation skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Measurement, Recording & Representation', 'Measurement, Recording & Representation skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Models & Application in Daily Life', 'Models & Application in Daily Life skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Scientific Inquiry & Investigation', 'Scientific Inquiry & Investigation skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Geography', 'Geography skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'History', 'History skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level)
SELECT 'Social & Political Life (Civics & Economics)', 'Social & Political Life (Civics & Economics) skill', s.id, c.id, 'intermediate'
FROM subjects s JOIN classes c ON s.class_id = c.id
WHERE s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name, subject_id) DO NOTHING;

-- ============================================================
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
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Classroom Instructions: ''Shut the Door'' & ''Bring the Book''', 'Carries out simple instructions such as ''Shut the door'', ''Bring me the book'', and such others', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-001', 'beginner', 3, 3, 5, TRUE, 1
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Listen to Instructions & Draw a Picture', 'Listens to instructions and draws a picture', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-002', 'beginner', 3, 3, 5, TRUE, 2
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Greetings & Polite Responses (English and Signing)', 'Listens to English words, greetings, polite forms of expression, simple sentences, and responds in English or the home language or ''signing'' (using sign language)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-003', 'beginner', 3, 3, 5, TRUE, 3
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Small & Capital Letters (Print and Braille)', 'Differentiates between small and capital letters in print or Braille', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-004', 'beginner', 3, 3, 5, TRUE, 4
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Phonics Blends: ''br'' and ''fr'' (''brother'', ''frog'')', 'Produces words with common blends like ''br'', ''fr'' like ''brother'', ''frog'' etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-005', 'beginner', 3, 3, 5, TRUE, 5
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Alphabet Sounds & Letter Recognition A-Z', 'Recognises letters and their sounds A-Z', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-006', 'beginner', 3, 3, 5, TRUE, 6
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Word Recognition & Picture Association', 'Associates words with pictures', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-007', 'beginner', 3, 3, 5, TRUE, 7
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Oral Expression & Narration (LO #8)', 'Responds orally (in any language including sign language) to comprehension questions related to stories/poems', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-008', 'beginner', 3, 3, 5, TRUE, 8
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Oral Expression & Narration (LO #9)', 'Talks about self/situations/pictures in English', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-009', 'beginner', 3, 3, 5, TRUE, 9
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Questioning (LO #10)', 'Identifies characters and sequence of a story and asks questions about the story', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-010', 'beginner', 3, 3, 5, TRUE, 10
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Recitation & Performance (LO #11)', 'Recites poems/rhymes with actions', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-011', 'beginner', 3, 3, 5, TRUE, 11
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Parts of Speech: Nouns (''boy'', ''sun'') & Prepositions (''in'', ''on'', ''under'')', 'Uses nouns such as ''boy'', ''sun'', and prepositions like ''in'', ''on'', ''under'', etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-012', 'beginner', 3, 3, 5, TRUE, 12
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Vocabulary (LO #13)', 'Names familiar objects seen in the pictures', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-013', 'beginner', 3, 3, 5, TRUE, 13
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Pre-Writing: Drawing & Scribbling to Stories', 'Draws, scribbles in response to poems and stories', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-014', 'beginner', 3, 3, 5, TRUE, 14
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Simple Word Writing (''fan'', ''hen'', ''rat'')', 'Writes simple words like fan, hen, rat etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-015', 'beginner', 3, 3, 5, TRUE, 15
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Data Handling: Data Collection & Interpretation (LO #16)', 'Collects, records (using pictures/numerals) and interprets simple information by looking at visuals', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-016', 'beginner', 3, 3, 5, TRUE, 16
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Data Handling' AND s.name = 'Mathematics' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Non-Uniform Units: Hand Span, Forearm & Footsteps', 'Estimates and measures short lengths using non-uniform units like a finger, hand span, length of a forearm, footsteps, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-017', 'beginner', 3, 3, 5, TRUE, 17
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Addition & Subtraction within 20 and up to 9', 'Applies addition and subtraction of numbers 1 to 20 in daily life - constructs addition facts up to 9 using concrete objects; subtracts numbers using 1 to 9; solves day-to-day problems related to addition and subtraction of numbers up to 9', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-018', 'beginner', 3, 3, 5, TRUE, 18
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Understanding the Concept of Zero', 'Develops the concept of zero', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-019', 'beginner', 3, 3, 5, TRUE, 19
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Number Sense & Place Value (LO #20)', 'Recites number names and counts objects up to 20, concretely, pictorially and symbolically', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-020', 'beginner', 3, 3, 5, TRUE, 20
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Number Sense & Place Value (LO #21)', 'Recognises numbers up to 99 and writes numerals', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-021', 'beginner', 3, 3, 5, TRUE, 21
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Number Sense & Place Value (LO #22)', 'Works with numbers 1 to 20 - counts objects using numbers 1 to 9; compares numbers up to 20 (e.g., tells whether the number of girls or boys is more in the class)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-022', 'beginner', 3, 3, 5, TRUE, 22
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Patterns: Number Patterns (LO #23)', 'Observes, extends and creates patterns of shapes and numbers (e.g., 1,2,3,4,5…; 1,3,5…; 2,4,6…)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-023', 'beginner', 3, 3, 5, TRUE, 23
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Patterns' AND s.name = 'Mathematics' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Physical Features of Shapes: A Ball Rolls, a Box Slides', 'Describes the physical features of various solids/shapes in her own language (e.g., a ball rolls, a box slides)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-024', 'beginner', 3, 3, 5, TRUE, 24
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Shapes & Spatial Understanding' AND s.name = 'Mathematics' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Shapes & Spatial Understanding: Classification of Objects (LO #25)', 'Classifies objects into groups based on a few physical attributes such as shape, size and other observable properties including rolling and sliding', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-025', 'beginner', 3, 3, 5, TRUE, 25
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Shapes & Spatial Understanding' AND s.name = 'Mathematics' AND c.name = 'I'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Follow Audio Instructions to Draw', 'Listens to instructions and draws a picture', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-026', 'beginner', 3, 3, 5, TRUE, 26
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Polite Conversations: ''How are you?''', 'Listens to English words, greetings, polite forms of expression, and responds in English/home language like ''How are you?'', ''I''m fine, thank you.'' etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-027', 'beginner', 3, 3, 5, TRUE, 27
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Children''s Newspaper Section Read-Aloud', 'Listens to short texts from children''s section of newspapers, read out by the teacher', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-028', 'beginner', 3, 3, 5, TRUE, 28
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Reading Comprehension (LO #29)', 'Identifies characters and sequence of events in a story', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-029', 'beginner', 3, 3, 5, TRUE, 29
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Reading Comprehension (LO #30)', 'Responds to comprehension questions related to stories and poems, in home language or English or sign language, orally and in writing (phrases/short sentences)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-030', 'beginner', 3, 3, 5, TRUE, 30
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Questioning (LO #31)', 'Expresses verbally her or his opinion and asks questions about the characters, storyline, etc., in English or home language', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-031', 'beginner', 3, 3, 5, TRUE, 31
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Recitation & Performance (LO #32)', 'Sings songs or rhymes with action', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-032', 'beginner', 3, 3, 5, TRUE, 32
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Prepositions of Place & Order: ''before'', ''between''', 'Uses prepositions like ''before'', ''between'' etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-033', 'beginner', 3, 3, 5, TRUE, 33
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Pronouns: Gender (''he/she'', ''his/her'') & Demonstratives (''this/that'')', 'Uses pronouns related to gender like ''his/her'', ''he/she'', ''it'' and other pronouns like ''this/that'', ''here/there'', ''these/those'' etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-034', 'beginner', 3, 3, 5, TRUE, 34
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Adjectives: Size, Shape, Colour & Texture (''big'', ''pink'', ''soft'')', 'Uses simple adjectives related to size, shape, colour, weight, texture such as ''big'', ''small'', ''round'', ''pink'', ''red'', ''heavy'', ''light'', ''soft'' etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-035', 'beginner', 3, 3, 5, TRUE, 35
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Pre-writing (LO #36)', 'Draws or writes a few words or short sentences in response to poems and stories', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-036', 'beginner', 3, 3, 5, TRUE, 36
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Word, Sentence & Paragraph Writing (LO #37)', 'Composes and writes simple, short sentences with space between words', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-037', 'beginner', 3, 3, 5, TRUE, 37
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Data Handling: Data Collection & Interpretation (LO #38)', 'Draws inference based on the data collected (e.g., the number of vehicles used in Samir''s house is more than that in Angelina''s)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-038', 'beginner', 3, 3, 5, TRUE, 38
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Data Handling' AND s.name = 'Mathematics' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Capacity & Volume (LO #39)', 'Estimates and measures length/distances and capacities of containers using uniform non-standard units like a rod/pencil, cup/spoon/bucket etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-039', 'beginner', 3, 3, 5, TRUE, 39
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Money (LO #40)', 'Represents an amount up to Rs. 100 using 3-4 notes and coins (of same/different denominations) of play money', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-040', 'beginner', 3, 3, 5, TRUE, 40
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Time & Calendar (LO #41)', 'Identifies the days of the week and months of the year', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-041', 'beginner', 3, 3, 5, TRUE, 41
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Time & Calendar (LO #42)', 'Sequences events according to their duration in terms of hours/days (e.g., does a child remain in school for a longer period than at home?)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-042', 'beginner', 3, 3, 5, TRUE, 42
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Weight (LO #43)', 'Compares objects as heavier/lighter than, using a simple balance', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-043', 'beginner', 3, 3, 5, TRUE, 43
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Addition & Subtraction (LO #44)', 'Solves simple daily life problems/situations based on addition and subtraction of two digit numbers', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-044', 'beginner', 3, 3, 5, TRUE, 44
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Number Sense & Place Value (LO #45)', 'Works with two digit numbers - reads and writes numerals up to 99; uses place value in writing and comparing two digit numbers; forms the greatest and smallest two digit numbers (with and without repetition of digits)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-045', 'beginner', 3, 3, 5, TRUE, 45
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Shapes & Spatial Understanding: 2D Shapes & Lines (LO #46)', 'Distinguishes between straight and curved lines; draws/represents straight lines in various orientations (vertical, horizontal, slant)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-046', 'beginner', 3, 3, 5, TRUE, 46
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Shapes & Spatial Understanding' AND s.name = 'Mathematics' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Shapes & Spatial Understanding: 3D Shapes & Nets (LO #47)', 'Describes basic 3D and 2D shapes with their observable characteristics - identifies cuboid, cylinder, cone and sphere by their names', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-047', 'beginner', 3, 3, 5, TRUE, 47
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Shapes & Spatial Understanding' AND s.name = 'Mathematics' AND c.name = 'II'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Oral Messages & Telephonic Communication', 'Responds appropriately to oral messages/telephonic communication', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-048', 'intermediate', 3, 3, 5, TRUE, 48
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Environmental Print & Information (LO #49)', 'Reads printed scripts on the classroom walls: poems, posters, charts etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-049', 'intermediate', 3, 3, 5, TRUE, 49
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Reading Aloud & Fluency (LO #50)', 'Reads aloud with appropriate pronunciation and pause', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-050', 'intermediate', 3, 3, 5, TRUE, 50
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Reading Comprehension (LO #51)', 'Reads small texts in English with comprehension i.e., identifies main idea, details and sequence and draws conclusions in English', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-051', 'intermediate', 3, 3, 5, TRUE, 51
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Oral Expression & Narration (LO #52)', 'Expresses orally her/his opinion/understanding about the story and characters in the story, in English/home language', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-052', 'intermediate', 3, 3, 5, TRUE, 52
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Recitation & Performance (LO #53)', 'Performs in events such as role play/skit in English with appropriate expressions', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-053', 'intermediate', 3, 3, 5, TRUE, 53
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Recitation & Performance (LO #54)', 'Recites poems individually/in groups with correct pronunciation and intonation', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-054', 'intermediate', 3, 3, 5, TRUE, 54
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Parts of Speech (LO #55)', 'Uses a variety of nouns, pronouns, adjectives and prepositions in context as compared to previous class', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-055', 'intermediate', 3, 3, 5, TRUE, 55
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Tenses (LO #56)', 'Distinguishes between simple past and simple present tenses', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-056', 'intermediate', 3, 3, 5, TRUE, 56
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Opposites (Antonyms): ''day/night'', ''close/open''', 'Identifies opposites like ''day/night'', ''close/open'', and such others', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-057', 'intermediate', 3, 3, 5, TRUE, 57
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Vocabulary (LO #58)', 'Uses vocabulary related to subjects like Maths, EVS, relevant to Class III', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-058', 'intermediate', 3, 3, 5, TRUE, 58
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Dictation (LO #59)', 'Writes/types dictation of words/phrases/sentences', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-059', 'intermediate', 3, 3, 5, TRUE, 59
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Punctuation & Mechanics (Class III)', 'Uses punctuation such as question mark, full stop and capital letters appropriately', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-060', 'intermediate', 3, 3, 5, TRUE, 60
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Word, Sentence & Paragraph Writing (LO #61)', 'Uses meaningful short sentences in English, orally and in writing', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-061', 'intermediate', 3, 3, 5, TRUE, 61
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Word, Sentence & Paragraph Writing (LO #62)', 'Writes 5-6 sentences in English on personal experiences/events using verbal or visual clues', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-062', 'intermediate', 3, 3, 5, TRUE, 62
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Grouping by Features & Properties (LO #63)', 'Groups objects, birds, animals, features and activities according to differences/similarities using different senses (appearance, place of living, food, movement, likes/dislikes)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-063', 'intermediate', 3, 3, 5, TRUE, 63
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Classification & Grouping' AND s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Drawings, Models & Maps (LO #64)', 'Creates drawings, designs, motifs, models, top/front/side views of objects, simple maps (of classroom, sections of home/school) and slogans, poems, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-064', 'intermediate', 3, 3, 5, TRUE, 64
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Creative Expression' AND s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Estimation & Verification (LO #65)', 'Guesses properties, estimates quantities of materials/activities in daily life and verifies using symbols/non-standard units (hand spans, spoons/mugs, etc.)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-065', 'intermediate', 3, 3, 5, TRUE, 65
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Estimation, Experimentation & Recording' AND s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Recording & Predicting Patterns (LO #66)', 'Records observations, experiences, information on objects/activities/places visited in different ways and predicts patterns (e.g., shapes of moon, seasons)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-066', 'intermediate', 3, 3, 5, TRUE, 66
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Estimation, Experimentation & Recording' AND s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Family & Community (LO #67)', 'Describes roles of family members, family influences (traits/features/habits/practices), and need for living together, through oral/written/other ways', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-067', 'intermediate', 3, 3, 5, TRUE, 67
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explanation & Understanding Relationships' AND s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Food & Water (LO #68)', 'Describes need of food for people of different age groups, animals and birds; availability of food and water and use of water at home and surroundings', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-068', 'intermediate', 3, 3, 5, TRUE, 68
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explanation & Understanding Relationships' AND s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Map Reading & Directions (LO #69)', 'Identifies directions, location of objects/places in simple maps (of home/classroom/school) using signs/symbols/verbally', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-069', 'intermediate', 3, 3, 5, TRUE, 69
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Mapping & Spatial Skills' AND s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Animals & Birds (LO #70)', 'Identifies simple features (movement, places found/kept, eating habits, sounds) of animals and birds in the immediate surroundings', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-070', 'intermediate', 3, 3, 5, TRUE, 70
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Observation & Identification' AND s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Family & Relationships (LO #71)', 'Identifies relationships with and among family members', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-071', 'intermediate', 3, 3, 5, TRUE, 71
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Observation & Identification' AND s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Plants (LO #72)', 'Identifies simple observable features (shape, colour, texture, aroma) of leaves, trunk and bark of plants in immediate surroundings', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-072', 'intermediate', 3, 3, 5, TRUE, 72
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Observation & Identification' AND s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Surroundings (Objects, Places & Activities) (LO #73)', 'Identifies objects, signs (vessels, stoves, transport, means of communication, signboards), places (types of houses/shelters, bus stand, petrol pump) and activities (work people do, cooking processes) at home/school/neighbourhood', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-073', 'intermediate', 3, 3, 5, TRUE, 73
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Observation & Identification' AND s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Continuity & Change (LO #74)', 'Differentiates between objects and activities of present and past (at the time of the elders) - clothes, vessels, games played, work done by people', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-074', 'intermediate', 3, 3, 5, TRUE, 74
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Past & Present (Change over Time)' AND s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Opinion on Social Issues (LO #75)', 'Voices opinion on good/bad touch, gender stereotypes for tasks/play/food in family, misuse/wastage of food and water in family and school', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-075', 'intermediate', 3, 3, 5, TRUE, 75
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Values, Sensitivity & Opinion' AND s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Rules & Cooperation (LO #76)', 'Observes rules in games (local, indoor, outdoor) and other collective tasks', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-076', 'intermediate', 3, 3, 5, TRUE, 76
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Values, Sensitivity & Opinion' AND s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Sensitivity, Hygiene & Conservation (LO #77)', 'Shows sensitivity for plants, animals, the elderly, differently abled and diverse family set-ups in surroundings', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-077', 'intermediate', 3, 3, 5, TRUE, 77
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Values, Sensitivity & Opinion' AND s.name = 'EVS' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Data Handling: Data Representation (Tables & Graphs) (LO #78)', 'Records data using tally marks, represents pictorially and draws conclusions', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-078', 'intermediate', 3, 3, 5, TRUE, 78
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Data Handling' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Capacity & Volume (LO #79)', 'Compares the capacity of different containers in terms of non-standard units', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-079', 'intermediate', 3, 3, 5, TRUE, 79
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Length & Distance (LO #80)', 'Estimates and measures length and distance using standard units like centimetres or metres and identifies relationships', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-080', 'intermediate', 3, 3, 5, TRUE, 80
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Money (LO #81)', 'Adds and subtracts small amounts of money with or without regrouping', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-081', 'intermediate', 3, 3, 5, TRUE, 81
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Money (LO #82)', 'Makes rate charts and simple bills', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-082', 'intermediate', 3, 3, 5, TRUE, 82
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Time & Calendar (LO #83)', 'Identifies a particular day and date on a calendar', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-083', 'intermediate', 3, 3, 5, TRUE, 83
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Time & Calendar (LO #84)', 'Reads the time correctly to the hour using a clock/watch', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-084', 'intermediate', 3, 3, 5, TRUE, 84
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Weight (LO #85)', 'Adds and subtracts measures involving grams and kilograms in life situations', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-085', 'intermediate', 3, 3, 5, TRUE, 85
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Weight (LO #86)', 'Weighs objects using standard units - grams and kilograms - using a simple balance', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-086', 'intermediate', 3, 3, 5, TRUE, 86
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Addition & Subtraction (LO #87)', 'Solves simple daily life problems using addition and subtraction of three digit numbers with and without regrouping, sums not exceeding 999', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-087', 'intermediate', 3, 3, 5, TRUE, 87
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Estimation & Problem Solving (LO #88)', 'Analyses and applies an appropriate number operation in the situation/context', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-088', 'intermediate', 3, 3, 5, TRUE, 88
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Multiplication & Division (LO #89)', 'Constructs and uses the multiplication facts (tables) of 2, 3, 4, 5 and 10 in daily life situations', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-089', 'intermediate', 3, 3, 5, TRUE, 89
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Division by Equal Sharing & Repeated Subtraction (''12 ÷ 3'')', 'Explains the meaning of division facts by equal grouping/sharing and finds it by repeated subtraction (e.g., 12 ÷ 3)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-090', 'intermediate', 3, 3, 5, TRUE, 90
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Number Sense & Place Value (LO #91)', 'Works with three digit numbers - reads and writes numbers up to 999 using place value; compares numbers up to 999 based on place value', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-091', 'intermediate', 3, 3, 5, TRUE, 91
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Patterns: Number Patterns (LO #92)', 'Extends patterns in simple shapes and numbers', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-092', 'intermediate', 3, 3, 5, TRUE, 92
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Patterns' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Shapes & Spatial Understanding: 2D Shapes & Lines (LO #93)', 'Describes 2D shapes by the number of sides, corners and diagonals', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-093', 'intermediate', 3, 3, 5, TRUE, 93
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Shapes & Spatial Understanding' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Shapes & Spatial Understanding: 2D Shapes & Lines (LO #94)', 'Fills a given region leaving no gaps using a tile of a given shape', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-094', 'intermediate', 3, 3, 5, TRUE, 94
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Shapes & Spatial Understanding' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Shapes & Spatial Understanding: 2D Shapes & Lines (LO #95)', 'Identifies and makes 2D shapes by paper folding, paper cutting on the dot grid, using straight lines etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-095', 'intermediate', 3, 3, 5, TRUE, 95
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Shapes & Spatial Understanding' AND s.name = 'Mathematics' AND c.name = 'III'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'School Announcements & Instructions', 'Responds to simple instructions, announcements in English made in class/school', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-096', 'intermediate', 3, 3, 5, TRUE, 96
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Listening Comprehension & Public Broadcast (LO #97)', 'Responds verbally/in writing in English to questions based on day-to-day life experiences, an article, story or poem heard or read', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-097', 'intermediate', 3, 3, 5, TRUE, 97
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Environmental Print & Information (LO #98)', 'Reads printed script on the classroom walls, notice board, in posters and in advertisements', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-098', 'intermediate', 3, 3, 5, TRUE, 98
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Environmental Print & Information (LO #99)', 'Reads subtitles on TV, titles of books, news headlines, pamphlets and advertisements', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-099', 'intermediate', 3, 3, 5, TRUE, 99
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Reading Aloud & Fluency (LO #100)', 'Uses punctuation marks appropriately in reading aloud with intonation and pauses such as question mark, comma and full stop', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-100', 'intermediate', 3, 3, 5, TRUE, 100
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reference Skills: Dictionary, Thesaurus & Encyclopedia (Class IV)', 'Uses dictionary to find out spelling and meaning', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-101', 'intermediate', 3, 3, 5, TRUE, 101
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Vocabulary in Context (LO #102)', 'Infers the meaning of unfamiliar words by reading them in context', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-102', 'intermediate', 3, 3, 5, TRUE, 102
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Oral Expression & Narration (LO #103)', 'Describes briefly, orally/in writing, events, places and/or personal experiences in English', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-103', 'intermediate', 3, 3, 5, TRUE, 103
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Oral Expression & Narration (LO #104)', 'Presents orally and in writing the highlights of a given written text/short speech/narration/video, film, pictures, photograph etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-104', 'intermediate', 3, 3, 5, TRUE, 104
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Oral Expression & Narration (LO #105)', 'Shares riddles and tongue-twisters in English', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-105', 'intermediate', 3, 3, 5, TRUE, 105
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Oral Expression & Narration (LO #106)', 'Speaks briefly on a familiar issue like conservation of water and experiences of day-to-day life like a visit to a zoo or going to a mela', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-106', 'intermediate', 3, 3, 5, TRUE, 106
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Recitation & Performance (LO #107)', 'Enacts different roles in short skits', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-107', 'intermediate', 3, 3, 5, TRUE, 107
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Recitation & Performance (LO #108)', 'Recites poems with appropriate expressions and intonation', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-108', 'intermediate', 3, 3, 5, TRUE, 108
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Discourse Linkers & Connectors: ''First'', ''Next''', 'Uses linkers to indicate connections between words and sentences such as ''First'', ''Next'', etc.', sk.id, c.id, 'Sequence Order', 'index.html#quest=LO-109', 'intermediate', 3, 3, 5, TRUE, 109
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Parts of Speech (LO #110)', 'Uses nouns, verbs, adjectives and prepositions in speech and writing', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-110', 'intermediate', 3, 3, 5, TRUE, 110
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Vocabulary (LO #111)', 'Solves simple crossword puzzles, builds word chains, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-111', 'intermediate', 3, 3, 5, TRUE, 111
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Dictation (LO #112)', 'Writes/types dictation of short paragraphs (7-8 sentences)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-112', 'intermediate', 3, 3, 5, TRUE, 112
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Functional Writing (LO #113)', 'Writes informal letters or messages with a sense of audience', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-113', 'intermediate', 3, 3, 5, TRUE, 113
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Punctuation & Mechanics (Class IV)', 'Uses punctuation marks appropriately in writing such as question mark, comma, full stop and capital letters', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-114', 'intermediate', 3, 3, 5, TRUE, 114
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Grouping by Features & Properties (LO #115)', 'Groups animals, birds, plants, objects, waste material by observable features, instincts, uses and traits', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-115', 'intermediate', 3, 3, 5, TRUE, 115
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Classification & Grouping' AND s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Drawings, Models & Maps (LO #116)', 'Creates collage, designs, models, rangolis, posters, albums, and simple maps (of school/neighbourhood, flow diagrams, etc.) using local/waste material', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-116', 'intermediate', 3, 3, 5, TRUE, 116
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Creative Expression' AND s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Estimation & Verification (LO #117)', 'Guesses properties/conditions of phenomena, estimates spatial quantities (distance, weight, time, duration) in standard/local units and verifies using simple tools/set-ups to establish cause and effect (evaporation, condensation, dissolution, absorption)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-117', 'intermediate', 3, 3, 5, TRUE, 117
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Estimation, Experimentation & Recording' AND s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Recording & Predicting Patterns (LO #118)', 'Records observations/experiences/information for objects, activities, phenomena, places visited (mela, festival, historical place) in different ways and predicts patterns', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-118', 'intermediate', 3, 3, 5, TRUE, 118
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Estimation, Experimentation & Recording' AND s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Animal Herd Behavior: Ants, Bees & Elephants', 'Explains herd/group behaviour in animals (ants, bees, elephants), birds (building nests), and changes in family (due to birth, marriage, transfer, etc.)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-119', 'intermediate', 3, 3, 5, TRUE, 119
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explanation & Understanding Relationships' AND s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Food Supply Journey: Field to Mandi to Home', 'Explains the process of producing and procuring daily needs (food, water, clothes) from source to home (e.g., crops from field to mandi to home, water purification)', sk.id, c.id, 'Sequence Order', 'index.html#quest=LO-120', 'intermediate', 3, 3, 5, TRUE, 120
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explanation & Understanding Relationships' AND s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Work & Livelihood (LO #121)', 'Describes different skilled work (farming, construction, art/craft, etc.), their inheritance (from elders) and training (role of institutions) in daily life', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-121', 'intermediate', 3, 3, 5, TRUE, 121
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explanation & Understanding Relationships' AND s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Map Reading & Directions (LO #122)', 'Identifies signs, location of objects/places and guides for directions with respect to a landmark in school/neighbourhood using maps etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-122', 'intermediate', 3, 3, 5, TRUE, 122
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Mapping & Spatial Skills' AND s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Using Signs & Information (LO #123)', 'Uses the information on signboards, posters, currency (notes/coins), railway ticket/time table', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-123', 'intermediate', 3, 3, 5, TRUE, 123
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Mapping & Spatial Skills' AND s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Animals & Birds (LO #124)', 'Identifies different features (beaks/teeth, claws, ears, hair, nests/shelters, etc.) of birds and animals', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-124', 'intermediate', 3, 3, 5, TRUE, 124
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Observation & Identification' AND s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Family & Relationships (LO #125)', 'Identifies relationship with and among family members in extended family', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-125', 'intermediate', 3, 3, 5, TRUE, 125
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Observation & Identification' AND s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Plants (LO #126)', 'Identifies simple features (shape, colour, aroma, where they grow) of flowers, roots and fruits in immediate surroundings', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-126', 'intermediate', 3, 3, 5, TRUE, 126
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Observation & Identification' AND s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Continuity & Change (LO #127)', 'Differentiates between objects and activities of past and present (transport, currency, houses, materials, tools, skills - farming, construction, etc.)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-127', 'intermediate', 3, 3, 5, TRUE, 127
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Past & Present (Change over Time)' AND s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Opinion on Social Issues (LO #128)', 'Voices opinion on issues observed/experienced in family/school/neighbourhood - stereotypes, discriminatory practices, child rights (schooling, child abuse, punishment, labour)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-128', 'intermediate', 3, 3, 5, TRUE, 128
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Values, Sensitivity & Opinion' AND s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Sensitivity, Hygiene & Conservation (LO #129)', 'Suggests ways for hygiene, reduce, reuse, recycle and takes care of living beings (plants, animals, the elderly, differently abled) and resources (food, water, public property)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-129', 'intermediate', 3, 3, 5, TRUE, 129
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Values, Sensitivity & Opinion' AND s.name = 'EVS' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Data Handling: Data Representation (Tables & Graphs) (LO #130)', 'Represents the collected information in tables and bar graphs and draws inferences from these', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-130', 'intermediate', 3, 3, 5, TRUE, 130
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Data Handling' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Area & Perimeter (LO #131)', 'Explores the area and perimeter of simple geometrical shapes (triangle, rectangle, square) in terms of a given shape as a unit', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-131', 'intermediate', 3, 3, 5, TRUE, 131
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Estimation & Verification of Measures (LO #132)', 'Estimates the length of an object/distance between two locations, weight of objects, volume of liquid, etc., and verifies them by actual measurement', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-132', 'intermediate', 3, 3, 5, TRUE, 132
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Problem Solving with Measures (LO #133)', 'Solves problems involving daily life situations related to length, distance, weight, volume and time involving four basic arithmetic operations', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-133', 'intermediate', 3, 3, 5, TRUE, 133
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Time & Calendar (LO #134)', 'Calculates time intervals/duration of familiar daily life events using forward or backward counting/addition and subtraction', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-134', 'intermediate', 3, 3, 5, TRUE, 134
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Time & Calendar (LO #135)', 'Reads clock time in hours and minutes and expresses the time in a.m. and p.m.; relates 24 hr clock with 12 hr clock', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-135', 'intermediate', 3, 3, 5, TRUE, 135
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Unit Conversion (LO #136)', 'Converts metre into centimetre and vice versa', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-136', 'intermediate', 3, 3, 5, TRUE, 136
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Estimation & Problem Solving (LO #137)', 'Creates and solves simple real life situations/problems including money, length, mass and capacity by using the four operations', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-137', 'intermediate', 3, 3, 5, TRUE, 137
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Fractions & Decimals (LO #138)', 'Identifies half, one-fourth, three-fourths of a whole in a given picture, by paper folding and in a collection of objects', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-138', 'intermediate', 3, 3, 5, TRUE, 138
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Fractions & Decimals (LO #139)', 'Represents fractions as half, one-fourth and three-fourths using numbers/numerals; shows the equivalence of a fraction with other fractions', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-139', 'intermediate', 3, 3, 5, TRUE, 139
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Multiplication & Division (LO #140)', 'Divides a number by another using different methods - pictorially (by drawing dots), equal grouping or repeated subtraction, and using the inter-relationship between division and multiplication', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-140', 'intermediate', 3, 3, 5, TRUE, 140
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Multiplication & Division (LO #141)', 'Multiplies 2 and 3 digit numbers', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-141', 'intermediate', 3, 3, 5, TRUE, 141
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Patterns: Number Patterns (LO #142)', 'Identifies the pattern in multiplication and division (up to multiples of 9)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-142', 'intermediate', 3, 3, 5, TRUE, 142
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Patterns' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Patterns: Shape & Geometric Patterns (LO #143)', 'Observes, identifies and extends geometrical patterns based on symmetry', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-143', 'intermediate', 3, 3, 5, TRUE, 143
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Patterns' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Shapes & Spatial Understanding: 2D Shapes & Lines (LO #144)', 'Identifies the centre, radius and diameter of a circle', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-144', 'intermediate', 3, 3, 5, TRUE, 144
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Shapes & Spatial Understanding' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Shapes & Spatial Understanding: 3D Shapes & Nets (LO #145)', 'Finds out shapes that can be used for tiling; makes cubes/cuboids using given nets', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-145', 'intermediate', 3, 3, 5, TRUE, 145
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Shapes & Spatial Understanding' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Shapes & Spatial Understanding: Spatial Views (LO #146)', 'Draws top view, front view and side view of simple objects', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-146', 'intermediate', 3, 3, 5, TRUE, 146
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Shapes & Spatial Understanding' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Shapes & Spatial Understanding: Symmetry (LO #147)', 'Shows the concept of symmetry by reflection through paper folding/paper cutting, ink blots, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-147', 'intermediate', 3, 3, 5, TRUE, 147
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Shapes & Spatial Understanding' AND s.name = 'Mathematics' AND c.name = 'IV'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Sports Field Instructions: ''Hit the ball!'' & ''Run!''', 'Acts according to instructions given in English, in games/sports, such as ''Hit the ball!'', ''Throw the ring.'', ''Run to the finish line!'' etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-148', 'intermediate', 3, 3, 5, TRUE, 148
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Listening Comprehension & Public Broadcast (LO #149)', 'Answers coherently in written or oral form to questions in English based on day-to-day life experiences, unfamiliar story, poem heard or read', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-149', 'intermediate', 3, 3, 5, TRUE, 149
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Critical Reading (LO #150)', 'Connects ideas that he/she has inferred, through reading and interaction, with his/her personal experiences', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-150', 'intermediate', 3, 3, 5, TRUE, 150
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Environmental Print & Information (LO #151)', 'Reads print in the surroundings (advertisements, directions, names of places etc.), understands and answers queries', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-151', 'intermediate', 3, 3, 5, TRUE, 151
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Extensive Reading (LO #152)', 'Reads independently English storybooks, news items/headlines, advertisements etc., talks about them, and composes short paragraphs', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-152', 'intermediate', 3, 3, 5, TRUE, 152
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Reading Comprehension (LO #153)', 'Reads text with comprehension, locates details and sequence of events', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-153', 'intermediate', 3, 3, 5, TRUE, 153
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reference Skills: Dictionary, Thesaurus & Encyclopedia (Class V)', 'Uses the dictionary for reference', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-154', 'intermediate', 3, 3, 5, TRUE, 154
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Conversation & Polite Expressions (LO #155)', 'Conducts short interviews of people around him/her e.g. grandparents, teachers, school librarian, gardener etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-155', 'intermediate', 3, 3, 5, TRUE, 155
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Oral Expression & Narration (LO #156)', 'Appreciates, verbally/in writing, the variety in food, dress, customs and festivals as read/heard in day-to-day life, in storybooks, narratives, videos, films etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-156', 'intermediate', 3, 3, 5, TRUE, 156
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Oral Expression & Narration (LO #157)', 'Writes and speaks on peace, equality etc. suggesting personal views', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-157', 'intermediate', 3, 3, 5, TRUE, 157
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Recitation & Performance (LO #158)', 'Recites and shares English songs, poems, games, riddles, stories, tongue twisters etc. with peers and family members', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-158', 'intermediate', 3, 3, 5, TRUE, 158
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Grammar in Use (LO #159)', 'Uses meaningful grammatically correct sentences to describe and narrate incidents and for framing questions', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-159', 'intermediate', 3, 3, 5, TRUE, 159
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Tenses (LO #160)', 'Identifies kinds of nouns, adverbs; differentiates between simple past and simple present verbs', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-160', 'intermediate', 3, 3, 5, TRUE, 160
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Synonyms & Antonyms in Context (''big/large'', ''inside/outside'')', 'Uses synonyms such as ''big/large'', ''shut/close'', and antonyms like ''inside/outside'', ''light/dark'' from clues in context', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-161', 'intermediate', 3, 3, 5, TRUE, 161
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Creative Writing (LO #162)', 'Attempts to write creatively (stories, poems, posters, etc.)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-162', 'intermediate', 3, 3, 5, TRUE, 162
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Creative Writing: Mini Biography & Autobiography', 'Writes a ''mini biography'' and ''mini autobiography''', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-163', 'intermediate', 3, 3, 5, TRUE, 163
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Dictation (LO #164)', 'Takes dictation for different purposes, such as lists, paragraphs, dialogues etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-164', 'intermediate', 3, 3, 5, TRUE, 164
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Functional Writing (LO #165)', 'Writes informal letters, messages and e-mails', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-165', 'intermediate', 3, 3, 5, TRUE, 165
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Word, Sentence & Paragraph Writing (LO #166)', 'Writes paragraphs in English from verbal, visual clues, with appropriate punctuation marks and linkers', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-166', 'intermediate', 3, 3, 5, TRUE, 166
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Grouping by Features & Properties (LO #167)', 'Groups objects, materials, activities by features and properties such as shape, taste, colour, texture, sound, traits etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-167', 'intermediate', 3, 3, 5, TRUE, 167
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Classification & Grouping' AND s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Drawings, Models & Maps (LO #168)', 'Creates posters, designs, models, set-ups, local dishes, sketches, maps (of neighbourhood/places visited) using local/waste material and writes poems/slogans/travelogue etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-168', 'intermediate', 3, 3, 5, TRUE, 168
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Creative Expression' AND s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Estimation & Verification (LO #169)', 'Guesses properties/conditions of phenomena, estimates spatial quantities (distance, area, volume, weight) and time in simple standard units and verifies using simple tools/set-ups (floating, sinking, mixing, evaporation, germination, spoilage)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-169', 'intermediate', 3, 3, 5, TRUE, 169
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Estimation, Experimentation & Recording' AND s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Recording & Predicting Patterns (LO #170)', 'Records observations, experiences and information in an organised manner (tables, sketches, bar graphs, pie charts) and predicts patterns to establish cause and effect', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-170', 'intermediate', 3, 3, 5, TRUE, 170
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Estimation, Experimentation & Recording' AND s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Animals & Birds (LO #171)', 'Explains the super senses and unusual features (sight, smell, hearing, sleep, sound, etc.) of animals and their responses to light, sound, food etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-171', 'intermediate', 3, 3, 5, TRUE, 171
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explanation & Understanding Relationships' AND s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Food & Water (LO #172)', 'Explains the use of technology and the process of accessing basic needs (food, water etc.) in daily life (farm produce to kitchen, preservation techniques, storage and tracking of water source)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-172', 'intermediate', 3, 3, 5, TRUE, 172
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explanation & Understanding Relationships' AND s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Institutions (LO #173)', 'Explains the role and functions of different institutions in daily life (Bank, Panchayat, cooperatives, police station, etc.)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-173', 'intermediate', 3, 3, 5, TRUE, 173
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explanation & Understanding Relationships' AND s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Interdependence in Nature (LO #174)', 'Describes the interdependence among animals, plants and humans (livelihoods from animals, dispersal of seeds etc.)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-174', 'intermediate', 3, 3, 5, TRUE, 174
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explanation & Understanding Relationships' AND s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Terrain, Climate & Culture (LO #175)', 'Establishes linkages among terrain, climate, resources (food, water, shelter, livelihood) and cultural life (e.g., life in hot/cold deserts)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-175', 'intermediate', 3, 3, 5, TRUE, 175
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explanation & Understanding Relationships' AND s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Map Reading & Directions (LO #176)', 'Identifies signs, directions, location of objects/landmarks of a locality/place visited in maps and predicts directions in context of positions at different places', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-176', 'intermediate', 3, 3, 5, TRUE, 176
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Mapping & Spatial Skills' AND s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Continuity & Change (LO #177)', 'Traces changes in practices, customs, techniques of past and present through coins, paintings, monuments, museums and interacting with elders', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-177', 'intermediate', 3, 3, 5, TRUE, 177
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Past & Present (Change over Time)' AND s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Opinion on Social Issues (LO #178)', 'Voices opinions on issues observed/experienced and relates them to larger issues of society (discrimination, migration/displacement, exclusion, child rights)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-178', 'intermediate', 3, 3, 5, TRUE, 178
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Values, Sensitivity & Opinion' AND s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'EVS Studio: Sensitivity, Hygiene & Conservation (LO #179)', 'Suggests ways for hygiene, health, managing waste, disaster/emergency situations and protecting/saving resources (land, fuels, forests), and shows sensitivity for the disadvantaged/deprived', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-179', 'intermediate', 3, 3, 5, TRUE, 179
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Values, Sensitivity & Opinion' AND s.name = 'EVS' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Data Handling: Data Representation (Tables & Graphs) (LO #180)', 'Collects data related to various daily life situations, represents it in tabular form and as bar graphs and interprets it', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-180', 'intermediate', 3, 3, 5, TRUE, 180
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Data Handling' AND s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Estimation & Verification of Measures (LO #181)', 'Estimates the volume of a solid body in known units (e.g., volume of a bucket is about 20 times that of a mug)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-181', 'intermediate', 3, 3, 5, TRUE, 181
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Problem Solving with Measures (LO #182)', 'Applies the four fundamental arithmetic operations in solving problems involving money, length, mass, capacity and time intervals', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-182', 'intermediate', 3, 3, 5, TRUE, 182
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Measurement (Length, Weight, Capacity, Time, Money): Unit Conversion (LO #183)', 'Relates commonly used larger and smaller units of length, weight and volume and converts larger units to smaller units and vice versa', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-183', 'intermediate', 3, 3, 5, TRUE, 183
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement (Length, Weight, Capacity, Time, Money)' AND s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Estimation & Problem Solving (LO #184)', 'Estimates sum, difference, product and quotient of numbers and verifies them using different strategies', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-184', 'intermediate', 3, 3, 5, TRUE, 184
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Fractions & Decimals (LO #185)', 'Expresses fractions like 1/2, 1/4, 1/5 in decimal notation and vice versa (e.g., in units of length and money); converts fractions into decimals and vice versa', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-185', 'intermediate', 3, 3, 5, TRUE, 185
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Fractions & Decimals (LO #186)', 'Finds the number corresponding to part of a collection; identifies and forms equivalent fractions of a given fraction', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-186', 'intermediate', 3, 3, 5, TRUE, 186
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Multiplication & Division (LO #187)', 'Performs four basic arithmetic operations on numbers beyond 1000 by understanding place value; divides a number by another using standard algorithms', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-187', 'intermediate', 3, 3, 5, TRUE, 187
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Numbers & Operations: Number Sense & Place Value (LO #188)', 'Reads and writes numbers bigger than 1000 being used in her/his surroundings', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-188', 'intermediate', 3, 3, 5, TRUE, 188
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Numbers & Operations' AND s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Patterns: Number Patterns (LO #189)', 'Identifies the pattern in triangular numbers and square numbers', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-189', 'intermediate', 3, 3, 5, TRUE, 189
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Patterns' AND s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Shapes & Spatial Understanding: 3D Shapes & Nets (LO #190)', 'Makes cube, cylinder and cone using nets designed for this purpose', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-190', 'intermediate', 3, 3, 5, TRUE, 190
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Shapes & Spatial Understanding' AND s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Shapes & Spatial Understanding: Angles (LO #191)', 'Classifies angles into right angle, acute angle, obtuse angle and represents them by drawing and tracing', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-191', 'intermediate', 3, 3, 5, TRUE, 191
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Shapes & Spatial Understanding' AND s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Shapes & Spatial Understanding: Symmetry (LO #192)', 'Identifies 2D shapes from the immediate environment that have rotation and reflection symmetry like alphabets and shapes', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-192', 'intermediate', 3, 3, 5, TRUE, 192
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Shapes & Spatial Understanding' AND s.name = 'Mathematics' AND c.name = 'V'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Public Announcements: Railway Station & Assembly', 'Responds to announcements and instructions made in class, school assembly, railway station and in other public places', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-193', 'advanced', 3, 3, 5, TRUE, 193
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Language Laboratory Session (Class VI)', 'Visits a language laboratory', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-194', 'advanced', 3, 3, 5, TRUE, 194
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Listening Comprehension & Public Broadcast (LO #195)', 'Responds to oral messages, telephonic communication in English and communicates them in English or home language', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-195', 'advanced', 3, 3, 5, TRUE, 195
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Environmental Print & Information (LO #196)', 'Reads to seek information from notice board, newspaper, Internet, tables, charts, diagrams and maps etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-196', 'advanced', 3, 3, 5, TRUE, 196
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Reading Comprehension (LO #197)', 'Reads a variety of texts in English/Braille and identifies main ideas, characters, sequence of ideas and events and relates with his/her personal experiences', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-197', 'advanced', 3, 3, 5, TRUE, 197
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Reading Comprehension (LO #198)', 'Responds to a variety of questions on familiar and unfamiliar texts verbally and in writing', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-198', 'advanced', 3, 3, 5, TRUE, 198
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reference Skills: Dictionary, Thesaurus & Encyclopedia (Class VI)', 'Refers to dictionary to check meaning and spelling, and to suggested websites for information', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-199', 'advanced', 3, 3, 5, TRUE, 199
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Oral Expression & Narration (LO #200)', 'Uses meaningful sentences to describe/narrate factual/imaginary situations in speech and writing', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-200', 'advanced', 3, 3, 5, TRUE, 200
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Recitation & Performance (LO #201)', 'Participates in activities in English like role play, group discussion, debate, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-201', 'advanced', 3, 3, 5, TRUE, 201
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Recitation & Performance (LO #202)', 'Recites and shares poems, songs, jokes, riddles, tongue twisters, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-202', 'advanced', 3, 3, 5, TRUE, 202
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Grammar in Use (LO #203)', 'Writes grammatically correct sentences for a variety of situations, using noun, pronoun, verb, adverb, determiners, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-203', 'advanced', 3, 3, 5, TRUE, 203
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Vocabulary (LO #204)', 'Uses synonyms, antonyms appropriately; deduces word meanings from clues in context while reading a variety of texts', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-204', 'advanced', 3, 3, 5, TRUE, 204
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Creative Writing: Book Review (Class VI)', 'Writes a book review', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-205', 'advanced', 3, 3, 5, TRUE, 205
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Dictation (LO #206)', 'Writes words/phrases/simple sentences and short paragraphs as dictated by the teacher', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-206', 'advanced', 3, 3, 5, TRUE, 206
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Functional Writing (LO #207)', 'Writes messages, invitations, short paragraphs and letters (formal and informal) with a sense of audience', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-207', 'advanced', 3, 3, 5, TRUE, 207
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Word, Sentence & Paragraph Writing (LO #208)', 'Drafts, revises and writes short paragraphs based on verbal, print and visual clues', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-208', 'advanced', 3, 3, 5, TRUE, 208
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Word, Sentence & Paragraph Writing (LO #209)', 'Writes coherently with focus on appropriate beginning, middle and end in English/Braille', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-209', 'advanced', 3, 3, 5, TRUE, 209
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Algebra: Variables & Generalised Perimeter (''2(x+3)'')', 'Uses variables with different operations to generalise a given situation (e.g., perimeter of a rectangle with sides x units and 3 units is 2(x+3) units)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-210', 'advanced', 3, 3, 5, TRUE, 210
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Algebra' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Data Handling: Data Representation & Interpretation (LO #211)', 'Arranges given/collected information (e.g., family expenditure over six months) in the form of table, pictograph and bar graph and interprets them', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-211', 'advanced', 3, 3, 5, TRUE, 211
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Data Handling' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geometry: 3D Shapes & Visualisation (LO #212)', 'Identifies 3D objects like sphere, cube, cuboid, cylinder, cone from the surroundings; describes and gives examples of edges, vertices and faces', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-212', 'advanced', 3, 3, 5, TRUE, 212
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geometry: Basic Geometrical Ideas (LO #213)', 'Describes geometrical ideas like line, line segment, open and closed figures, angle, triangle, quadrilateral, circle, etc., with examples in surroundings', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-213', 'advanced', 3, 3, 5, TRUE, 213
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geometry: Lines & Angles (LO #214)', 'Demonstrates an understanding of angles - identifies examples in surroundings, classifies angles by measure, estimates measures using 45°, 90° and 180° as reference', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-214', 'advanced', 3, 3, 5, TRUE, 214
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geometry: Quadrilaterals (LO #215)', 'Classifies quadrilaterals into different groups/types on the basis of their sides/angles', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-215', 'advanced', 3, 3, 5, TRUE, 215
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geometry: Symmetry (LO #216)', 'Demonstrates an understanding of line symmetry - identifies and creates symmetrical 2D shapes', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-216', 'advanced', 3, 3, 5, TRUE, 216
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geometry: Triangles & Congruence (LO #217)', 'Classifies triangles on the basis of their angles and sides (scalene, isosceles, equilateral)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-217', 'advanced', 3, 3, 5, TRUE, 217
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Mensuration: Perimeter & Area (LO #218)', 'Finds out the perimeter and area of rectangular objects in the surroundings like floor of the classroom, surfaces of a chalk box etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-218', 'advanced', 3, 3, 5, TRUE, 218
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Mensuration' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Factors, Multiples & Divisibility (LO #219)', 'Applies HCF or LCM in a particular situation', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-219', 'advanced', 3, 3, 5, TRUE, 219
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Factors, Multiples & Divisibility (LO #220)', 'Recognises and appreciates (through patterns) the broad classification of numbers as even, odd, prime, co-prime, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-220', 'advanced', 3, 3, 5, TRUE, 220
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Fractions, Decimals & Rational Numbers (LO #221)', 'Solves problems on daily life situations involving addition and subtraction of fractions/decimals', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-221', 'advanced', 3, 3, 5, TRUE, 221
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Fractions, Decimals & Rational Numbers (LO #222)', 'Uses fractions and decimals in different situations which involve money, length, temperature etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-222', 'advanced', 3, 3, 5, TRUE, 222
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Integers (LO #223)', 'Solves problems involving addition and subtraction of integers', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-223', 'advanced', 3, 3, 5, TRUE, 223
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Whole Numbers & Operations (LO #224)', 'Solves problems involving large numbers by applying appropriate operations (addition, subtraction, multiplication and division)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-224', 'advanced', 3, 3, 5, TRUE, 224
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Ratio, Proportion & Commercial Arithmetic: Ratio & Proportion (LO #225)', 'Compares quantities using ratios in different situations (e.g., ratio of girls to boys in a class is 3:2)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-225', 'advanced', 3, 3, 5, TRUE, 225
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Ratio, Proportion & Commercial Arithmetic' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Ratio, Proportion & Commercial Arithmetic: Unitary Method (LO #226)', 'Uses unitary method in solving various word problems', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-226', 'advanced', 3, 3, 5, TRUE, 226
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Ratio, Proportion & Commercial Arithmetic' AND s.name = 'Mathematics' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Classification of Matter & Motion (Biotic/Abiotic, Rectilinear/Circular)', 'Classifies materials, organisms and processes based on observable properties (soluble/insoluble; transparent/translucent/opaque; reversible/irreversible changes; herbs, shrubs, trees, creepers, climbers; biotic/abiotic; rectilinear, circular, periodic motion)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-227', 'advanced', 3, 3, 5, TRUE, 227
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Classification' AND s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Creativity (LO #228)', 'Exhibits creativity in designing, planning, making use of available resources, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-228', 'advanced', 3, 3, 5, TRUE, 228
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Environmental Awareness, Creativity & Values' AND s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Environmental Protection (LO #229)', 'Makes efforts to protect environment (minimising wastage of food, water, electricity; rainwater harvesting; care for plants)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-229', 'advanced', 3, 3, 5, TRUE, 229
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Environmental Awareness, Creativity & Values' AND s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Scientific Values (LO #230)', 'Exhibits values of honesty, objectivity, cooperation, freedom from fear and prejudices', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-230', 'advanced', 3, 3, 5, TRUE, 230
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Environmental Awareness, Creativity & Values' AND s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: General (LO #231)', 'Cause-Effect Relationships Relates processes and phenomena with causes (deficiency diseases with diet; adaptations with habitats; air quality with pollutants)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-231', 'advanced', 3, 3, 5, TRUE, 231
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explaining Processes & Cause-Effect' AND s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Explaining Processes & Phenomena (LO #232)', 'Explains processes and phenomena (processing of plant fibres, movements in plants and animals, formation of shadows, reflection from plane mirror, composition of air, preparation of vermicompost)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-232', 'advanced', 3, 3, 5, TRUE, 232
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explaining Processes & Cause-Effect' AND s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Differentiation (LO #233)', 'Differentiates materials and organisms (fibre and yarn; tap and fibrous roots; electrical conductors and insulators) on the basis of properties, structure and functions', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-233', 'advanced', 3, 3, 5, TRUE, 233
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Identification & Differentiation' AND s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Identification (LO #234)', 'Identifies materials and organisms, such as plant fibres and flowers, on the basis of observable features (appearance, texture, function, aroma)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-234', 'advanced', 3, 3, 5, TRUE, 234
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Identification & Differentiation' AND s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Labelled Diagrams & Flow Charts (LO #235)', 'Draws labelled diagrams/flow charts of organisms and processes (parts of flowers, joints, filtration, water cycle)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-235', 'advanced', 3, 3, 5, TRUE, 235
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement, Recording & Representation' AND s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Measurement & Calculation (LO #236)', 'Measures physical quantities and expresses them in SI units (e.g., length)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-236', 'advanced', 3, 3, 5, TRUE, 236
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement, Recording & Representation' AND s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Application of Concepts in Daily Life (LO #237)', 'Applies learning of scientific concepts in day-to-day life (balanced diet, separating materials, season-appropriate fabrics, compass for directions, coping with heavy rain/drought)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-237', 'advanced', 3, 3, 5, TRUE, 237
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Models & Application in Daily Life' AND s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Model Construction (LO #238)', 'Constructs models using materials from surroundings and explains their working (pinhole camera, periscope, electric torch)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-238', 'advanced', 3, 3, 5, TRUE, 238
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Models & Application in Daily Life' AND s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Conducting Investigations (LO #239)', 'Conducts simple investigations to seek answers to queries (e.g., nutrients in animal fodder; can all physical changes be reversed; does a freely suspended magnet align in a particular direction)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-239', 'advanced', 3, 3, 5, TRUE, 239
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Scientific Inquiry & Investigation' AND s.name = 'Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Earth''s Rotation & Revolution: Day, Night and Seasons', 'Demonstrates day and night and seasons', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-240', 'advanced', 3, 3, 5, TRUE, 240
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Celestial Bodies: Sun, Earth and Moon', 'Distinguishes between stars, planets and satellites (Sun, Earth and Moon)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-241', 'advanced', 3, 3, 5, TRUE, 241
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Understanding Eclipses & Scientific Evidence', 'Examines critically the superstitions related to eclipses', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-242', 'advanced', 3, 3, 5, TRUE, 242
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Earth: A Unique Planet & The Biosphere', 'Recognises that the earth is a unique celestial body due to existence of life, zones of the earth with special reference to biosphere', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-243', 'advanced', 3, 3, 5, TRUE, 243
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Maps, Globe & Diagrams (LO #244)', 'Draws a neighbourhood map showing scale, direction and features using conventional symbols', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-244', 'advanced', 3, 3, 5, TRUE, 244
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grid Lines: Latitudes, Longitudes, Poles & Tropics', 'Identifies latitudes and longitudes (poles, equator, tropics), States/UTs of India and neighbouring countries on globe and world map', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-245', 'advanced', 3, 3, 5, TRUE, 245
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Continents and Oceans on the World Map', 'Locates directions on a flat surface and continents and oceans on the world map', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-246', 'advanced', 3, 3, 5, TRUE, 246
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Major Physical Features of India', 'Locates physical features of India (mountains, plateaus, plains, rivers, desert) on the map of India', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-247', 'advanced', 3, 3, 5, TRUE, 247
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Ancient India: Harappan Civilization & First Cities', 'Explains broad developments during the ancient period (hunting-gathering, beginning of agriculture, first cities on the Indus) and relates developments in one place with another', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-248', 'advanced', 3, 3, 5, TRUE, 248
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Ancient Dynasties: Mauryas, Guptas and Pallavas', 'Lists significant contributions of important kingdoms and dynasties (Ashokan inscriptions, Gupta coins, Ratha temples by Pallavas)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-249', 'advanced', 3, 3, 5, TRUE, 249
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Ancient India (LO #250)', 'Locates important historical sites and places on an outline map of India', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-250', 'advanced', 3, 3, 5, TRUE, 250
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Ancient India (LO #251)', 'Recognises distinctive features of early human cultures and explains their growth', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-251', 'advanced', 3, 3, 5, TRUE, 251
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Ancient India (LO #252)', 'Synthesises information related to various historical developments', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-252', 'advanced', 3, 3, 5, TRUE, 252
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Art, Architecture & Culture (LO #253)', 'Describes issues, events, personalities mentioned in literary works of the time', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-253', 'advanced', 3, 3, 5, TRUE, 253
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Art, Architecture & Culture (LO #254)', 'Describes the implications of India''s contacts with regions outside India in religion, art, architecture, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-254', 'advanced', 3, 3, 5, TRUE, 254
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Art, Architecture & Culture (LO #255)', 'Outlines India''s significant contributions in culture and science (astronomy, medicine, mathematics, knowledge of metals)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-255', 'advanced', 3, 3, 5, TRUE, 255
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Religious Ideas & Movements (LO #256)', 'Analyses basic ideas and values of various religions and systems of thought during the ancient period', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-256', 'advanced', 3, 3, 5, TRUE, 256
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Sources of History (LO #257)', 'Identifies different types of sources (archaeological, literary etc.) and describes their use in reconstructing history of this period', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-257', 'advanced', 3, 3, 5, TRUE, 257
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Civics: Diversity & Discrimination (LO #258)', 'Describes various forms of human diversity around her/him and develops a healthy attitude towards diversity', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-258', 'advanced', 3, 3, 5, TRUE, 258
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Equality & Inequality: Understanding Everyday Differences', 'Differentiates between equality and inequality in various forms to treat them in a healthy way', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-259', 'advanced', 3, 3, 5, TRUE, 259
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Diversity & Combating Discrimination: Identifying Sources', 'Recognises various forms of discrimination and understands the nature and sources of discrimination', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-260', 'advanced', 3, 3, 5, TRUE, 260
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Civics: Government (LO #261)', 'Describes the functioning of rural and urban local government bodies in sectors like health and education', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-261', 'advanced', 3, 3, 5, TRUE, 261
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Three Levels of Government: Local, State & Union', 'Describes the role of government, especially at the local level; identifies levels of government - local, state and union', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-262', 'advanced', 3, 3, 5, TRUE, 262
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Civics: Markets, Economy & Public Facilities (LO #263)', 'Describes factors responsible for availability of different occupations in rural and urban areas', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-263', 'advanced', 3, 3, 5, TRUE, 263
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VI'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Listening Comprehension & Public Broadcast (LO #264)', 'Responds to different kinds of instructions, requests, directions in varied contexts viz. school, bank, railway station', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-264', 'advanced', 3, 3, 5, TRUE, 264
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Language Laboratory Session (Class VII)', 'Visits a language laboratory', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-265', 'advanced', 3, 3, 5, TRUE, 265
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Listening Comprehension & Public Broadcast (LO #266)', 'Speaks about excerpts, dialogues, skits, short films, news and debate on TV and radio, audio-video programmes on suggested websites', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-266', 'advanced', 3, 3, 5, TRUE, 266
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Critical Reading (LO #267)', 'Thinks critically, compares and contrasts characters, events, ideas, themes and relates them to life', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-267', 'advanced', 3, 3, 5, TRUE, 267
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Environmental Print & Information (LO #268)', 'Reads to seek information in print/online, notice board, signboards in public places, newspaper, hoardings etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-268', 'advanced', 3, 3, 5, TRUE, 268
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Extensive Reading (LO #269)', 'Reads a variety of texts for pleasure e.g. adventure stories, science fiction, fairy tales, biography, autobiography, travelogue etc. (extensive reading)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-269', 'advanced', 3, 3, 5, TRUE, 269
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Reading Comprehension (LO #270)', 'Answers questions orally and in writing on a variety of texts', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-270', 'advanced', 3, 3, 5, TRUE, 270
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Reading Comprehension (LO #271)', 'Identifies details, characters, main idea and sequence of ideas and events in textual/non-textual material', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-271', 'advanced', 3, 3, 5, TRUE, 271
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Reading Comprehension (LO #272)', 'Reads textual/non-textual materials in English/Braille with comprehension', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-272', 'advanced', 3, 3, 5, TRUE, 272
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Questioning (LO #273)', 'Asks and responds to questions based on texts (from books or other resources) and out of curiosity', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-273', 'advanced', 3, 3, 5, TRUE, 273
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Recitation & Performance (LO #274)', 'Engages in conversations in English with family, friends, and people from different professions such as shopkeeper, salesperson etc. using appropriate vocabulary', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-274', 'advanced', 3, 3, 5, TRUE, 274
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Recitation & Performance (LO #275)', 'Participates in different activities in English such as role play, poetry recitation, skit, drama, debate, speech, elocution, declamation, quiz, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-275', 'advanced', 3, 3, 5, TRUE, 275
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Recitation & Performance (LO #276)', 'Reads aloud stories and recites poems with appropriate pause, intonation and pronunciation', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-276', 'advanced', 3, 3, 5, TRUE, 276
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Grammar in Use (LO #277)', 'Uses appropriate grammatical forms in communication (e.g. noun, pronoun, verb, determiners, time and tense, passivisation, adjective, adverb, etc.)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-277', 'advanced', 3, 3, 5, TRUE, 277
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Vocabulary (LO #278)', 'Infers the meaning of unfamiliar words by reading them in context', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-278', 'advanced', 3, 3, 5, TRUE, 278
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Vocabulary (LO #279)', 'Refers dictionary, thesaurus and encyclopedia to find meanings/spelling of words while reading and writing', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-279', 'advanced', 3, 3, 5, TRUE, 279
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Creative Writing: Book Review (Class VII)', 'Writes a book review', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-280', 'advanced', 3, 3, 5, TRUE, 280
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Creative Writing (LO #281)', 'Writes descriptions/narratives showing sensitivity to gender, environment and appreciation of cultural diversity', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-281', 'advanced', 3, 3, 5, TRUE, 281
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Creative Writing (LO #282)', 'Writes dialogues from a story and story from dialogues', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-282', 'advanced', 3, 3, 5, TRUE, 282
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Functional Writing (LO #283)', 'Writes formal letters, personal diary, list, email, SMS, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-283', 'advanced', 3, 3, 5, TRUE, 283
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Note Taking (LO #284)', 'Takes notes while teacher teaches/from books/from online materials', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-284', 'advanced', 3, 3, 5, TRUE, 284
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Word, Sentence & Paragraph Writing (LO #285)', 'Organises sentences coherently in English/Braille with the help of verbal and visual clues and with a sense of audience', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-285', 'advanced', 3, 3, 5, TRUE, 285
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Algebra: Linear Equations (LO #286)', 'Represents daily life situations in the form of a simple equation and solves it', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-286', 'advanced', 3, 3, 5, TRUE, 286
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Algebra' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Algebra: Variables & Algebraic Expressions (LO #287)', 'Adds/subtracts algebraic expressions', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-287', 'advanced', 3, 3, 5, TRUE, 287
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Algebra' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Data Handling: Data Representation & Interpretation (LO #288)', 'Interprets data using bar graphs (e.g., electricity consumption in winter vs summer, runs scored in first 10 overs)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-288', 'advanced', 3, 3, 5, TRUE, 288
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Data Handling' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Data Handling: Measures of Central Tendency (LO #289)', 'Finds representative values for simple data from daily life contexts like mean, median and mode', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-289', 'advanced', 3, 3, 5, TRUE, 289
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Data Handling' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Data Handling: Probability & Chance (LO #290)', 'Recognises variability in real life situations (e.g., heights of students) and uncertainty in happening of events like throwing a coin', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-290', 'advanced', 3, 3, 5, TRUE, 290
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Data Handling' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geometry: Constructions (LO #291)', 'Using ruler and compasses, constructs a line parallel to a given line from a point outside it, and triangles', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-291', 'advanced', 3, 3, 5, TRUE, 291
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geometry: Lines & Angles (LO #292)', 'Classifies pairs of angles as linear, supplementary, complementary, adjacent and vertically opposite, and finds the value of one when the other is given', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-292', 'advanced', 3, 3, 5, TRUE, 292
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geometry: Lines & Angles (LO #293)', 'Verifies the properties of pairs of angles formed when a transversal cuts two lines', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-293', 'advanced', 3, 3, 5, TRUE, 293
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geometry: Triangles & Congruence (LO #294)', 'Explains congruency of triangles on the basis of information given (SSS, SAS, ASA, RHS)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-294', 'advanced', 3, 3, 5, TRUE, 294
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geometry: Triangles & Congruence (LO #295)', 'Finds unknown angle of a triangle when its two angles are known', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-295', 'advanced', 3, 3, 5, TRUE, 295
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Mensuration: Perimeter & Area (LO #296)', 'Calculates areas of the regions enclosed in a rectangle and a square', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-296', 'advanced', 3, 3, 5, TRUE, 296
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Mensuration' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Mensuration: Perimeter & Area (LO #297)', 'Finds approximate area of closed shapes using unit square grid/graph sheet', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-297', 'advanced', 3, 3, 5, TRUE, 297
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Mensuration' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Exponents, Squares & Roots (LO #298)', 'Uses exponential form of numbers to simplify problems involving multiplication and division of large numbers', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-298', 'advanced', 3, 3, 5, TRUE, 298
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Fractions, Decimals & Rational Numbers (LO #299)', 'Interprets the division and multiplication of fractions', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-299', 'advanced', 3, 3, 5, TRUE, 299
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Fractions, Decimals & Rational Numbers (LO #300)', 'Solves problems related to daily life situations involving rational numbers', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-300', 'advanced', 3, 3, 5, TRUE, 300
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Fractions, Decimals & Rational Numbers (LO #301)', 'Uses algorithms to multiply and divide fractions/decimals', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-301', 'advanced', 3, 3, 5, TRUE, 301
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Integers (LO #302)', 'Multiplies/divides two integers', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-302', 'advanced', 3, 3, 5, TRUE, 302
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Ratio, Proportion & Commercial Arithmetic: Percentage, Profit & Loss, Interest (LO #303)', 'Calculates profit/loss percent and rate percent in simple interest', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-303', 'advanced', 3, 3, 5, TRUE, 303
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Ratio, Proportion & Commercial Arithmetic' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Ratio, Proportion & Commercial Arithmetic: Percentage, Profit & Loss, Interest (LO #304)', 'Solves problems related to conversion of percentage to fraction and decimal and vice versa', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-304', 'advanced', 3, 3, 5, TRUE, 304
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Ratio, Proportion & Commercial Arithmetic' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Ratio & Proportion: Proportional Quantities (15, 45, 40, 120)', 'Distinguishes quantities that are in proportion (e.g., 15, 45, 40, 120)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-305', 'advanced', 3, 3, 5, TRUE, 305
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Ratio, Proportion & Commercial Arithmetic' AND s.name = 'Mathematics' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Classification of Materials, Organisms & Processes (LO #306)', 'Classifies materials and organisms based on properties/characteristics (plant and animal fibres; physical and chemical changes)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-306', 'advanced', 3, 3, 5, TRUE, 306
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Classification' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Creativity (LO #307)', 'Exhibits creativity in designing, planning, making use of available resources, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-307', 'advanced', 3, 3, 5, TRUE, 307
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Environmental Awareness, Creativity & Values' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Environmental Protection (LO #308)', 'Makes efforts to protect environment (sanitation in public places, minimising pollutants, planting trees, sensitising others on overconsumption)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-308', 'advanced', 3, 3, 5, TRUE, 308
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Environmental Awareness, Creativity & Values' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Scientific Values (LO #309)', 'Exhibits values of honesty, objectivity, cooperation, freedom from fear and prejudices', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-309', 'advanced', 3, 3, 5, TRUE, 309
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Environmental Awareness, Creativity & Values' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: General (LO #310)', 'Cause-Effect Relationships Relates processes and phenomena with causes (wind speed with air pressure; crops with soil types; depletion of water table with human activities)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-310', 'advanced', 3, 3, 5, TRUE, 310
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explaining Processes & Cause-Effect' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Chemical Word Equations (LO #311)', 'Writes word equations for chemical reactions (acid-base reactions, corrosion, photosynthesis, respiration)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-311', 'advanced', 3, 3, 5, TRUE, 311
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explaining Processes & Cause-Effect' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Explaining Processes & Phenomena (LO #312)', 'Explains processes and phenomena (processing of animal fibres, modes of heat transfer, organs and systems in humans and plants, heating and magnetic effects of electric current)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-312', 'advanced', 3, 3, 5, TRUE, 312
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explaining Processes & Cause-Effect' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Differentiation (LO #313)', 'Differentiates materials and organisms (digestion in different organisms; unisexual and bisexual flowers; conductors and insulators of heat; acidic, basic and neutral substances; images by mirrors and lenses) on the basis of properties, structure and function', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-313', 'advanced', 3, 3, 5, TRUE, 313
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Identification & Differentiation' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Identification (LO #314)', 'Identifies materials and organisms (animal fibres, types of teeth, mirrors and lenses) on the basis of observable features', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-314', 'advanced', 3, 3, 5, TRUE, 314
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Identification & Differentiation' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Graphs (LO #315)', 'Plots and interprets graphs (e.g., distance-time graph)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-315', 'advanced', 3, 3, 5, TRUE, 315
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement, Recording & Representation' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Labelled Diagrams & Flow Charts (LO #316)', 'Draws labelled diagrams/flow charts (organ systems, electric circuits, experimental set-ups, life cycle of silk moth)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-316', 'advanced', 3, 3, 5, TRUE, 316
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement, Recording & Representation' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Measurement & Calculation (LO #317)', 'Measures and calculates temperature, pulse rate, speed of moving objects, time period of a simple pendulum, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-317', 'advanced', 3, 3, 5, TRUE, 317
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement, Recording & Representation' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Application of Concepts in Daily Life (LO #318)', 'Applies learning of scientific concepts in day-to-day life (dealing with acidity, testing and treating soil, preventing corrosion, vegetative propagation, connecting cells, disaster measures, treating polluted water)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-318', 'advanced', 3, 3, 5, TRUE, 318
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Models & Application in Daily Life' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: History of Scientific Discoveries (LO #319)', 'Discusses and appreciates stories of scientific discoveries', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-319', 'advanced', 3, 3, 5, TRUE, 319
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Models & Application in Daily Life' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Surrounding Models: Stethoscope, Anemometer & Newton''s Disc', 'Constructs models using materials from surroundings and explains their working (stethoscope, anemometer, electromagnet, Newton''s colour disc)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-320', 'advanced', 3, 3, 5, TRUE, 320
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Models & Application in Daily Life' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Scientific Investigation: Flower Extract as Acid-Base Indicator', 'Conducts simple investigations to seek answers to queries (flower extract as acid-base indicator; photosynthesis in non-green leaves; is white light composed of many colours)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-321', 'advanced', 3, 3, 5, TRUE, 321
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Scientific Inquiry & Investigation' AND s.name = 'Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Disaster Preparedness: Preventive Actions for Floods & Earthquakes', 'Explains preventive actions to be undertaken in the event of disasters (earthquake, floods, droughts)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-322', 'advanced', 3, 3, 5, TRUE, 322
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Environmental Calamities: Factors Leading to Disasters', 'Reflects on the factors leading to disasters and calamities', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-323', 'advanced', 3, 3, 5, TRUE, 323
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Earth''s Interior, Landforms & Atmosphere (LO #324)', 'Describes formation of landforms due to various factors', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-324', 'advanced', 3, 3, 5, TRUE, 324
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Composition and Structure of the Atmosphere', 'Explains composition and structure of the atmosphere', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-325', 'advanced', 3, 3, 5, TRUE, 325
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Layers of Earth''s Interior & Rock Types', 'Identifies major layers of the earth''s interior, rock types and layers of the atmosphere in a diagram', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-326', 'advanced', 3, 3, 5, TRUE, 326
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Environment & Natural Resources (LO #327)', 'Analyses factors contributing to pollution in surroundings and lists measures to prevent it', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-327', 'advanced', 3, 3, 5, TRUE, 327
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Environment & Natural Resources (LO #328)', 'Describes different components of the environment and the interrelationship between them', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-328', 'advanced', 3, 3, 5, TRUE, 328
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Environment & Natural Resources (LO #329)', 'Reasons out factors leading to diversity in flora and fauna (climate, landforms)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-329', 'advanced', 3, 3, 5, TRUE, 329
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Environment & Natural Resources (LO #330)', 'Shows sensitivity to the need for conservation of natural resources - air, water, energy, flora and fauna', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-330', 'advanced', 3, 3, 5, TRUE, 330
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Human Geography & Development (LO #331)', 'Analyses factors that impact development of specific regions', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-331', 'advanced', 3, 3, 5, TRUE, 331
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Human Geography & Development (LO #332)', 'Draws interrelationship between climatic regions and life of people in different climatic regions of the world, including India', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-332', 'advanced', 3, 3, 5, TRUE, 332
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Maps, Globe & Diagrams (LO #333)', 'Locates distribution and extent of different climatic regions on the world map or globe', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-333', 'advanced', 3, 3, 5, TRUE, 333
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Art, Architecture & Culture (LO #334)', 'Describes distinctive developments in style and technology used for construction of temples, tombs and mosques', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-334', 'advanced', 3, 3, 5, TRUE, 334
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Medieval India: Administrative Measures of Khaljis & Tughlaqs', 'Analyses administrative measures and strategies for military control adopted by different kingdoms (Khaljis, Tughluqs, Mughals)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-335', 'advanced', 3, 3, 5, TRUE, 335
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Medieval India: Socio-Political & Economic Transformations', 'Analyses socio-political and economic changes during the medieval period', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-336', 'advanced', 3, 3, 5, TRUE, 336
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Medieval India (LO #337)', 'Draws comparisons between policies of different rulers', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-337', 'advanced', 3, 3, 5, TRUE, 337
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Medieval India (LO #338)', 'Explains the relationship between livelihood patterns and geographical conditions (tribes, nomadic pastoralists, banjaras)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-338', 'advanced', 3, 3, 5, TRUE, 338
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Medieval India: Comparative Regional Developments', 'Relates key historical developments during the medieval period in one place with another', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-339', 'advanced', 3, 3, 5, TRUE, 339
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Bhakti & Sufi Movements: Emergence of New Religious Ideas', 'Analyses factors which led to the emergence of new religious ideas and movements (bhakti and sufi)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-340', 'advanced', 3, 3, 5, TRUE, 340
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Bhakti & Sufi Traditions: Inferences from Devotional Poetry', 'Draws inferences from poetry of bhakti and sufi saints about the existing social order', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-341', 'advanced', 3, 3, 5, TRUE, 341
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Sources of History (LO #342)', 'Provides examples of sources used to study various periods in history', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-342', 'advanced', 3, 3, 5, TRUE, 342
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Democratic Equality: Political, Economic & Social Dimensions', 'Explains the significance of equality in democracy; distinguishes between political, economic and social equality', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-343', 'advanced', 3, 3, 5, TRUE, 343
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Right to Equality: Regional Social & Economic Issues', 'Interprets social, political and economic issues in one''s own region with reference to the right to equality', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-344', 'advanced', 3, 3, 5, TRUE, 344
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Civics: Elections & Constituencies (LO #345)', 'Differentiates between local government and State government; describes the process of election to the legislative assembly', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-345', 'advanced', 3, 3, 5, TRUE, 345
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Civics: Elections & Constituencies (LO #346)', 'Locates one''s own constituency on the assembly constituency map of State/UT and names local MLA', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-346', 'advanced', 3, 3, 5, TRUE, 346
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Civics: Gender (LO #347)', 'Analyses causes and consequences of disadvantages faced by women; identifies women achievers and illustrates their contributions', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-347', 'advanced', 3, 3, 5, TRUE, 347
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Civics: Markets, Economy & Public Facilities (LO #348)', 'Differentiates between different kinds of markets; traces how goods travel through various market places', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-348', 'advanced', 3, 3, 5, TRUE, 348
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Role of Media: News Reporting & Creating Advertisements', 'Explains the functioning of media with examples from newspapers; creates an advertisement', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-349', 'advanced', 3, 3, 5, TRUE, 349
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Listening Comprehension & Public Broadcast (LO #350)', 'Responds to instructions and announcements in school and public places viz. railway station, market, airport, cinema hall, and acts accordingly', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-350', 'advanced', 3, 3, 5, TRUE, 350
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Language Laboratory Session (Class VIII)', 'Visits a language laboratory', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-351', 'advanced', 3, 3, 5, TRUE, 351
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Listening Comprehension & Public Broadcast (LO #352)', 'Reads excerpts, dialogues, poems, commentaries of sports and games, speeches, news, debates on TV, radio and expresses opinions about them', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-352', 'advanced', 3, 3, 5, TRUE, 352
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Listening' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Critical Reading (LO #353)', 'Interprets quotations, sayings and proverbs', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-353', 'advanced', 3, 3, 5, TRUE, 353
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Critical Reading (LO #354)', 'Reads, compares, contrasts, thinks critically and relates ideas to life', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-354', 'advanced', 3, 3, 5, TRUE, 354
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Extensive Reading (LO #355)', 'Reads a variety of texts for pleasure e.g. adventure stories, science fiction, fairy tales, non-fiction articles, narratives, travelogues, biographies, etc. (extensive reading)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-355', 'advanced', 3, 3, 5, TRUE, 355
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Reading Comprehension (LO #356)', 'Identifies details, characters, main idea and sequence of ideas and events while reading', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-356', 'advanced', 3, 3, 5, TRUE, 356
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Reading Studio: Reading Comprehension (LO #357)', 'Reads textual/non-textual materials in English/Braille with comprehension', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-357', 'advanced', 3, 3, 5, TRUE, 357
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Reading' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Conversation & Polite Expressions (LO #358)', 'Introduces guests in English, interviews people by asking questions based on the work they do', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-358', 'advanced', 3, 3, 5, TRUE, 358
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Conversation & Polite Expressions (LO #359)', 'Uses formulaic/polite expressions to communicate such as ''May I borrow your book?'', ''I would like to differ'' etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-359', 'advanced', 3, 3, 5, TRUE, 359
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Oral Expression & Narration (LO #360)', 'Narrates stories (real or imaginary) and real life experiences in English', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-360', 'advanced', 3, 3, 5, TRUE, 360
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Oral Expression & Narration (LO #361)', 'Speaks about objects/events in the class/school environment and outside surroundings', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-361', 'advanced', 3, 3, 5, TRUE, 361
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Oral Expression & Narration (LO #362)', 'Speaks short prepared speech in morning assembly', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-362', 'advanced', 3, 3, 5, TRUE, 362
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Questioning (LO #363)', 'Asks questions in different contexts and situations (based on the text/beyond the text/out of curiosity/while engaging in conversation) using appropriate vocabulary and accurate sentences', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-363', 'advanced', 3, 3, 5, TRUE, 363
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Recitation & Performance (LO #364)', 'Engages in conversations in English with people from different professions such as bank staff, railway staff, etc. using appropriate vocabulary', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-364', 'advanced', 3, 3, 5, TRUE, 364
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Speaking Studio: Recitation & Performance (LO #365)', 'Participates in different events such as role play, poetry recitation, skit, drama, debate, speech, elocution, declamation, quiz, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-365', 'advanced', 3, 3, 5, TRUE, 365
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Speaking' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Grammar in Use (LO #366)', 'Communicates accurately using appropriate grammatical forms (e.g., clauses, comparison of adjectives, time and tense, active/passive voice, reported speech etc.)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-366', 'advanced', 3, 3, 5, TRUE, 366
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Grammar in Use (LO #367)', 'Participates in grammar games and kinaesthetic activities for language learning', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-367', 'advanced', 3, 3, 5, TRUE, 367
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Vocabulary (LO #368)', 'Infers the meaning of unfamiliar words by reading them in context', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-368', 'advanced', 3, 3, 5, TRUE, 368
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Grammar & Vocabulary Studio: Vocabulary (LO #369)', 'Refers dictionary, thesaurus and encyclopedia as reference books for meaning and spelling while reading and writing', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-369', 'advanced', 3, 3, 5, TRUE, 369
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Vocabulary & Grammar' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Answer Writing (LO #370)', 'Writes answers to textual/non-textual questions after comprehension/inference; draws character sketch, attempts extrapolative writing', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-370', 'advanced', 3, 3, 5, TRUE, 370
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Creative Writing (LO #371)', 'Develops a skit (dialogues from a story) and story from dialogues', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-371', 'advanced', 3, 3, 5, TRUE, 371
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Creative Writing: Book Review (Class VIII)', 'Writes a book review', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-372', 'advanced', 3, 3, 5, TRUE, 372
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Functional Writing (LO #373)', 'Prepares a write-up after seeking information in print/online, notice board, newspaper, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-373', 'advanced', 3, 3, 5, TRUE, 373
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Functional Writing (LO #374)', 'Writes email, messages, notice, formal letters, descriptions/narratives, personal diary, report, short personal/biographical experiences etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-374', 'advanced', 3, 3, 5, TRUE, 374
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'The Writing Process: Drafting, Revising, Editing & Finalising', 'Writes a coherent and meaningful paragraph through the process of drafting, revising, editing and finalising', sk.id, c.id, 'Sequence Order', 'index.html#quest=LO-375', 'advanced', 3, 3, 5, TRUE, 375
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Writing Studio: Word, Sentence & Paragraph Writing (LO #376)', 'Writes short paragraphs coherently in English/Braille with a proper beginning, middle and end with appropriate punctuation marks', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-376', 'advanced', 3, 3, 5, TRUE, 376
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Writing' AND s.name = 'English' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Algebra: Algebraic Identities (LO #377)', 'Uses various algebraic identities in solving problems of daily life', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-377', 'advanced', 3, 3, 5, TRUE, 377
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Algebra' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Algebra: Variables & Algebraic Expressions (LO #378)', 'Multiplies algebraic expressions (e.g., expands (2x-5)(3x²+7))', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-378', 'advanced', 3, 3, 5, TRUE, 378
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Algebra' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Algebra: Variables & Algebraic Expressions (LO #379)', 'Solves puzzles and daily life problems using variables', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-379', 'advanced', 3, 3, 5, TRUE, 379
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Algebra' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Data Handling: Data Representation & Interpretation (LO #380)', 'Draws and interprets bar charts and pie charts', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-380', 'advanced', 3, 3, 5, TRUE, 380
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Data Handling' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Data Handling: Probability & Chance (LO #381)', 'Makes hypotheses on chances of future events on the basis of earlier occurrences or available data (e.g., repeated throws of dice and coins)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-381', 'advanced', 3, 3, 5, TRUE, 381
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Data Handling' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geometry: 3D Shapes & Visualisation (LO #382)', 'Represents 3D shapes on a plane surface such as sheet of paper, blackboard etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-382', 'advanced', 3, 3, 5, TRUE, 382
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Euler''s Relation for Polyhedra (F + V - E = 2)', 'Verifies Euler''s relation through pattern', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-383', 'advanced', 3, 3, 5, TRUE, 383
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geometry: Constructions (LO #384)', 'Constructs different quadrilaterals using compasses and straight edge', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-384', 'advanced', 3, 3, 5, TRUE, 384
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geometry: Quadrilaterals (LO #385)', 'Solves problems related to angles of a quadrilateral using angle sum property', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-385', 'advanced', 3, 3, 5, TRUE, 385
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geometry: Quadrilaterals (LO #386)', 'Verifies properties of parallelograms and establishes the relationship between them through reasoning', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-386', 'advanced', 3, 3, 5, TRUE, 386
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geometry' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Mensuration: Perimeter & Area (LO #387)', 'Estimates the area of shapes like trapezium and other polygons using square grid/graph sheet and verifies using formulas', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-387', 'advanced', 3, 3, 5, TRUE, 387
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Mensuration' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Mensuration: Perimeter & Area (LO #388)', 'Finds the area of a polygon', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-388', 'advanced', 3, 3, 5, TRUE, 388
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Mensuration' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Mensuration: Surface Area & Volume (LO #389)', 'Finds surface area and volume of cuboidal and cylindrical objects', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-389', 'advanced', 3, 3, 5, TRUE, 389
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Mensuration' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Exponents, Squares & Roots (LO #390)', 'Finds squares, cubes, square roots and cube roots of numbers using different methods', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-390', 'advanced', 3, 3, 5, TRUE, 390
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Exponents, Squares & Roots (LO #391)', 'Solves problems with integral exponents', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-391', 'advanced', 3, 3, 5, TRUE, 391
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Factors, Multiples & Divisibility (LO #392)', 'Proves divisibility rules of 2, 3, 4, 5, 6, 9 and 11', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-392', 'advanced', 3, 3, 5, TRUE, 392
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Fractions, Decimals & Rational Numbers (LO #393)', 'Finds out as many rational numbers as possible between two given rational numbers', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-393', 'advanced', 3, 3, 5, TRUE, 393
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Number System: Fractions, Decimals & Rational Numbers (LO #394)', 'Generalises properties of addition, subtraction, multiplication and division of rational numbers through patterns', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-394', 'advanced', 3, 3, 5, TRUE, 394
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Number System' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Ratio, Proportion & Commercial Arithmetic: Percentage, Profit & Loss, Interest (LO #395)', 'Applies the concept of per cent in profit and loss situations to find discount, VAT and compound interest', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-395', 'advanced', 3, 3, 5, TRUE, 395
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Ratio, Proportion & Commercial Arithmetic' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Ratio, Proportion & Commercial Arithmetic: Ratio & Proportion (LO #396)', 'Solves problems based on direct and inverse proportions', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-396', 'advanced', 3, 3, 5, TRUE, 396
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Ratio, Proportion & Commercial Arithmetic' AND s.name = 'Mathematics' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Classification of Materials, Organisms & Processes (LO #397)', 'Classifies materials and organisms based on properties/characteristics (metals and non-metals; kharif and rabi crops; useful and harmful microorganisms; sexual and asexual reproduction; celestial objects; exhaustible and inexhaustible resources)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-397', 'advanced', 3, 3, 5, TRUE, 397
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Classification' AND s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Creativity (LO #398)', 'Exhibits creativity in designing, planning, making use of available resources, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-398', 'advanced', 3, 3, 5, TRUE, 398
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Environmental Awareness, Creativity & Values' AND s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Environmental Protection (LO #399)', 'Makes efforts to protect environment (judicious use of resources, controlled use of fertilisers and pesticides, coping with environmental hazards)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-399', 'advanced', 3, 3, 5, TRUE, 399
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Environmental Awareness, Creativity & Values' AND s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Scientific Values (LO #400)', 'Exhibits values of honesty, objectivity, cooperation, freedom from fear and prejudices', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-400', 'advanced', 3, 3, 5, TRUE, 400
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Environmental Awareness, Creativity & Values' AND s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: General (LO #401)', 'Cause-Effect Relationships Relates processes and phenomena with causes (smog with air pollutants; deterioration of monuments with acid rain)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-401', 'advanced', 3, 3, 5, TRUE, 401
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explaining Processes & Cause-Effect' AND s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Chemical Word Equations (LO #402)', 'Writes word equations for chemical reactions (reactions of metals and non-metals with air, water and acids)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-402', 'advanced', 3, 3, 5, TRUE, 402
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explaining Processes & Cause-Effect' AND s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Explaining Processes & Phenomena (LO #403)', 'Explains processes and phenomena (reproduction in humans and animals, production and propagation of sound, chemical effects of electric current, multiple images, structure of flame)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-403', 'advanced', 3, 3, 5, TRUE, 403
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Explaining Processes & Cause-Effect' AND s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Differentiation (LO #404)', 'Differentiates materials and organisms (natural and human-made fibres; contact and non-contact forces; liquids as conductors and insulators; plant and animal cells; viviparous and oviparous animals) on the basis of properties, structure and functions', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-404', 'advanced', 3, 3, 5, TRUE, 404
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Identification & Differentiation' AND s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Labelled Diagrams & Flow Charts (LO #405)', 'Draws labelled diagrams/flow charts (structure of cell, eye, human reproductive organs, experimental set-ups)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-405', 'advanced', 3, 3, 5, TRUE, 405
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement, Recording & Representation' AND s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Measurement & Calculation (LO #406)', 'Measures angles of incidence and reflection, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-406', 'advanced', 3, 3, 5, TRUE, 406
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement, Recording & Representation' AND s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Microscopy & Slide Preparation (LO #407)', 'Prepares slides of microorganisms, onion peel, human cheek cells, etc., and describes their microscopic features', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-407', 'advanced', 3, 3, 5, TRUE, 407
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Measurement, Recording & Representation' AND s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Application of Concepts in Daily Life (LO #408)', 'Applies learning of scientific concepts in day-to-day life (purifying water, segregating wastes, increasing crop production, using metals/non-metals, friction, challenging myths and taboos about adolescence)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-408', 'advanced', 3, 3, 5, TRUE, 408
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Models & Application in Daily Life' AND s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: History of Scientific Discoveries (LO #409)', 'Discusses and appreciates stories of scientific discoveries', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-409', 'advanced', 3, 3, 5, TRUE, 409
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Models & Application in Daily Life' AND s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Model Construction (LO #410)', 'Constructs models using materials from surroundings and explains their working (ektara, electroscope, fire extinguisher)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-410', 'advanced', 3, 3, 5, TRUE, 410
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Models & Application in Daily Life' AND s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Science Studio: Conducting Investigations (LO #411)', 'Conducts simple investigations to seek answers to queries (conditions for combustion; salt and sugar in pickles; do liquids exert equal pressure at the same depth)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-411', 'advanced', 3, 3, 5, TRUE, 411
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Scientific Inquiry & Investigation' AND s.name = 'Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Global Agricultural Production: Wheat, Rice, Cotton & Jute', 'Analyses factors due to which some countries are known for production of major crops (wheat, rice, cotton, jute) and locates them on the world map', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-412', 'advanced', 3, 3, 5, TRUE, 412
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Agriculture & Industries (LO #413)', 'Classifies different types of industries based on raw materials, size and ownership', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-413', 'advanced', 3, 3, 5, TRUE, 413
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Regional Agriculture: Farming Types & Local Crop Practices', 'Describes major crops, types of farming and agricultural practices in her/his own area/state', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-414', 'advanced', 3, 3, 5, TRUE, 414
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Agriculture & Industries (LO #415)', 'Draws interrelationship between types of farming and development in different regions of the world', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-415', 'advanced', 3, 3, 5, TRUE, 415
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Industrial Disasters & Landslides: Risk Reduction Measures', 'Describes causes of forest fire, landslide, industrial disasters and their risk reduction measures', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-416', 'advanced', 3, 3, 5, TRUE, 416
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Environment & Natural Resources (LO #417)', 'Analyses uneven distribution of natural and human-made resources on the earth', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-417', 'advanced', 3, 3, 5, TRUE, 417
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Environment & Natural Resources (LO #418)', 'Justifies judicious use of natural resources such as water, soil, forest, etc.', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-418', 'advanced', 3, 3, 5, TRUE, 418
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Maps, Globe & Diagrams (LO #419)', 'Draws bar diagrams to show population of different countries/India/states', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-419', 'advanced', 3, 3, 5, TRUE, 419
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Maps, Globe & Diagrams (LO #420)', 'Interprets the world map for uneven distribution of population', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-420', 'advanced', 3, 3, 5, TRUE, 420
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Geography: Maps, Globe & Diagrams (LO #421)', 'Locates distribution of important minerals (coal, mineral oil) on the world map', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-421', 'advanced', 3, 3, 5, TRUE, 421
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Geography' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Art, Architecture & Culture (LO #422)', 'Outlines major developments during the modern period in the field of arts', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-422', 'advanced', 3, 3, 5, TRUE, 422
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Colonial & Modern India (LO #423)', 'Analyses issues related to caste, women, widow remarriage, child marriage, social reforms and colonial laws/policies on these issues', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-423', 'advanced', 3, 3, 5, TRUE, 423
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Colonial & Modern India (LO #424)', 'Analyses significant developments in the process of nation building', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-424', 'advanced', 3, 3, 5, TRUE, 424
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Colonial & Modern India: Decline and Rise of Urban Centres', 'Analyses the decline of pre-existing urban centres and handicraft industries and development of new urban centres and industries during the colonial period', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-425', 'advanced', 3, 3, 5, TRUE, 425
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Colonial & Modern India (LO #426)', 'Describes the forms of tribal societies in the 19th century and their relationship with the environment; explains colonial policies towards tribal communities', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-426', 'advanced', 3, 3, 5, TRUE, 426
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Colonial & Modern India (LO #427)', 'Explains differences in the impact of colonial agrarian policies in different regions (e.g., indigo rebellion)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-427', 'advanced', 3, 3, 5, TRUE, 427
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Colonial & Modern India (LO #428)', 'Explains how the English East India Company became the most dominant power', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-428', 'advanced', 3, 3, 5, TRUE, 428
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'History: Colonial & Modern India (LO #429)', 'Explains the institutionalisation of the new education system in India', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-429', 'advanced', 3, 3, 5, TRUE, 429
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'The Revolt of 1857: Origins, Spread & Impact', 'Explains the origin, nature and spread of the revolt of 1857 and the lessons learned from it', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-430', 'advanced', 3, 3, 5, TRUE, 430
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Indian National Movement: 1870s to 1947', 'Outlines the course of the Indian national movement from the 1870s till Independence', sk.id, c.id, 'Sequence Order', 'index.html#quest=LO-431', 'advanced', 3, 3, 5, TRUE, 431
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Historical Periods: Distinguishing Modern, Medieval & Ancient', 'Distinguishes the ''modern period'' from the ''medieval'' and ''ancient'' periods through sources, nomenclature and broad developments', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-432', 'advanced', 3, 3, 5, TRUE, 432
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'History' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Civics: Constitution, Rights & Laws (LO #433)', 'Analyses causes and consequences of marginalisation faced by disadvantaged sections of one''s own region', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-433', 'advanced', 3, 3, 5, TRUE, 433
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'The Judicial System & How to File an FIR', 'Describes the functioning of the judicial system in India citing landmark cases; demonstrates how to file an FIR', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-434', 'advanced', 3, 3, 5, TRUE, 434
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'How Laws are Made: RTI Act, RTE Act & Domestic Violence Act', 'Describes the process of making a law (e.g., Domestic Violence Act, RTI Act, RTE Act)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-435', 'advanced', 3, 3, 5, TRUE, 435
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Civics: Constitution, Rights & Laws (LO #436)', 'Illustrates the Fundamental Rights and Fundamental Duties with examples; applies them to find out about their violation, protection and promotion (e.g., Child Rights)', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-436', 'advanced', 3, 3, 5, TRUE, 436
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Civics: Constitution, Rights & Laws (LO #437)', 'Interprets social and political issues in one''s own region with reference to the Constitution of India', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-437', 'advanced', 3, 3, 5, TRUE, 437
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Civics: Elections & Constituencies (LO #438)', 'Differentiates between State government and Union government; describes the process of election to the Lok Sabha', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-438', 'advanced', 3, 3, 5, TRUE, 438
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Civics: Elections & Constituencies (LO #439)', 'Locates one''s own constituency on the parliamentary constituency map of State/UT and names local MP', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-439', 'advanced', 3, 3, 5, TRUE, 439
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, difficulty_level, max_score, questions_count, duration_minutes, is_active, order_index)
SELECT 'Civics: Markets, Economy & Public Facilities (LO #440)', 'Identifies the role of Government in providing public facilities (water, sanitation, road, electricity) and in regulating economic activities', sk.id, c.id, 'MCQ Quiz', 'index.html#quest=LO-440', 'advanced', 3, 3, 5, TRUE, 440
FROM skills sk
JOIN subjects s ON sk.subject_id = s.id
JOIN classes c ON sk.class_id = c.id
WHERE sk.name = 'Social & Political Life (Civics & Economics)' AND s.name = 'Social Science' AND c.name = 'VIII'
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    skill_id = EXCLUDED.skill_id,
    class_id = EXCLUDED.class_id,
    game_type = EXCLUDED.game_type,
    file_path = EXCLUDED.file_path,
    questions_count = EXCLUDED.questions_count,
    updated_at = CURRENT_TIMESTAMP;

-- ============================================================
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
