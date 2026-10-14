================================================================================
-- MYCLASSBOARD GAMES - PRODUCTION DATABASE SETUP
-- PostgreSQL SQL Script
-- Date: October 9, 2025
-- Status: Production Ready
================================================================================

-- ============================================================
-- DROP EXISTING OBJECTS (Optional - for fresh start)
-- ============================================================
-- Uncomment if you want to drop all existing tables

/*
DROP TABLE IF EXISTS audio_feedback CASCADE;
DROP TABLE IF EXISTS scores CASCADE;
DROP TABLE IF EXISTS assignments CASCADE;
DROP TABLE IF EXISTS analytics CASCADE;
DROP TABLE IF EXISTS games CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS subjects CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS classes CASCADE;
DROP TABLE IF EXISTS teachers CASCADE;
DROP TABLE IF EXISTS api_logs CASCADE;
*/

-- ============================================================
-- 1. CLASSES TABLE
-- ============================================================
-- Stores class levels (I, II, III, ... VIII)

CREATE TABLE IF NOT EXISTS classes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(10) UNIQUE NOT NULL,
    description VARCHAR(255),
    level INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Class Data
INSERT INTO classes (name, description, level) VALUES
    ('I', 'Class I - Age 5-6', 1),
    ('II', 'Class II - Age 6-7', 2),
    ('III', 'Class III - Age 7-8', 3),
    ('IV', 'Class IV - Age 8-9', 4),
    ('V', 'Class V - Age 9-10', 5),
    ('VI', 'Class VI - Age 10-11', 6),
    ('VII', 'Class VII - Age 11-12', 7),
    ('VIII', 'Class VIII - Age 12-13', 8)
ON CONFLICT (name) DO NOTHING;

-- ============================================================
-- 2. SUBJECTS TABLE
-- ============================================================
-- Stores subjects for each class (English, Mathematics, Science)

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

-- Insert Subject Data for All Classes
INSERT INTO subjects (name, description, class_id, order_index) VALUES
    -- Class I
    ('English', 'English Language Learning', 1, 1),
    ('Mathematics', 'Math Fundamentals', 1, 2),
    ('Science', 'Basic Science Concepts', 1, 3),
    -- Class II
    ('English', 'English Language Learning', 2, 1),
    ('Mathematics', 'Math Fundamentals', 2, 2),
    ('Science', 'Basic Science Concepts', 2, 3),
    -- Class III
    ('English', 'English Language Learning', 3, 1),
    ('Mathematics', 'Math Fundamentals', 3, 2),
    ('Science', 'Basic Science Concepts', 3, 3),
    -- Class IV
    ('English', 'English Language Learning', 4, 1),
    ('Mathematics', 'Math Fundamentals', 4, 2),
    ('Science', 'Basic Science Concepts', 4, 3),
    -- Class V
    ('English', 'English Language Learning', 5, 1),
    ('Mathematics', 'Math Fundamentals', 5, 2),
    ('Science', 'Basic Science Concepts', 5, 3),
    -- Class VI
    ('English', 'English Language Learning', 6, 1),
    ('Mathematics', 'Math Fundamentals', 6, 2),
    ('Science', 'Basic Science Concepts', 6, 3),
    -- Class VII
    ('English', 'English Language Learning', 7, 1),
    ('Mathematics', 'Math Fundamentals', 7, 2),
    ('Science', 'Basic Science Concepts', 7, 3),
    -- Class VIII
    ('English', 'English Language Learning', 8, 1),
    ('Mathematics', 'Math Fundamentals', 8, 2),
    ('Science', 'Basic Science Concepts', 8, 3)
ON CONFLICT (name, class_id) DO NOTHING;

-- ============================================================
-- 3. SKILLS TABLE
-- ============================================================
-- Stores skills under each subject

CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    subject_id INT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    class_id INT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    difficulty_level VARCHAR(20) DEFAULT 'beginner', -- beginner, intermediate, advanced
    order_index INT DEFAULT 0,
    icon VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, subject_id)
);

-- Insert Skill Data for Class I English
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level, order_index) VALUES
    ('Listening', 'Learn to listen and understand', 1, 1, 'beginner', 1),
    ('Reading', 'Learn basic reading skills', 1, 1, 'beginner', 2),
    ('Writing', 'Learn to write letters and words', 1, 1, 'beginner', 3),
    ('Speaking', 'Learn pronunciation and speaking', 1, 1, 'beginner', 4)
ON CONFLICT (name, subject_id) DO NOTHING;

-- Insert Skill Data for Class I Mathematics
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level, order_index) VALUES
    ('Numbers', 'Learn numbers 1-10', 5, 1, 'beginner', 1),
    ('Addition', 'Learn basic addition', 5, 1, 'beginner', 2),
    ('Subtraction', 'Learn basic subtraction', 5, 1, 'beginner', 3),
    ('Shapes', 'Learn geometric shapes', 5, 1, 'beginner', 4)
ON CONFLICT (name, subject_id) DO NOTHING;

-- Insert Skill Data for Class I Science
INSERT INTO skills (name, description, subject_id, class_id, difficulty_level, order_index) VALUES
    ('Life Skills', 'Daily life and hygiene', 9, 1, 'beginner', 1),
    ('Nature', 'Nature and environment', 9, 1, 'beginner', 2),
    ('Safety', 'Safety and awareness', 9, 1, 'beginner', 3)
ON CONFLICT (name, subject_id) DO NOTHING;

-- ============================================================
-- 4. GAMES TABLE
-- ============================================================
-- Stores games linked to skills

CREATE TABLE IF NOT EXISTS games (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    skill_id INT NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    class_id INT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    game_type VARCHAR(50), -- multiple-choice, drag-drop, typing, listening, etc
    file_path VARCHAR(255),
    difficulty_level VARCHAR(20) DEFAULT 'beginner',
    max_score INT DEFAULT 50,
    questions_count INT DEFAULT 5,
    duration_minutes INT DEFAULT 5,
    icon VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    order_index INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Games for Class I
INSERT INTO games (name, description, skill_id, class_id, game_type, file_path, max_score, questions_count) VALUES
    ('Listen & Do Adventure', 'Listen to instructions and perform actions', 1, 1, 'listening', 'listen-do-adventure-game.html', 50, 5),
    ('Story Time Quiz', 'Answer questions about a story', 2, 1, 'multiple-choice', 'story-time-quiz.html', 50, 5),
    ('Letter Formation', 'Learn to write letters', 3, 1, 'typing', 'letter-formation.html', 50, 5),
    ('Pronunciation Game', 'Learn correct pronunciation', 4, 1, 'listening', 'pronunciation-game.html', 50, 5),
    ('Simple Addition', 'Solve simple addition problems', 6, 1, 'multiple-choice', 'simple-addition.html', 50, 5),
    ('Fraction Parts', 'Learn about fractions', 7, 1, 'multiple-choice', 'fraction-parts.html', 50, 5),
    ('Count and Match', 'Count objects and match numbers', 5, 1, 'drag-drop', 'count-and-match.html', 50, 5),
    ('Shape Sorter', 'Sort objects by shape', 8, 1, 'categorization', 'shape-sorter.html', 50, 5),
    ('Life Skills Quiz', 'Learn daily life skills', 9, 1, 'multiple-choice', 'life-skills-quiz.html', 50, 5),
    ('Nature Explorer', 'Explore nature and environment', 10, 1, 'multiple-choice', 'nature-explorer.html', 50, 5)
ON CONFLICT (name) DO NOTHING;

-- ============================================================
-- 5. TEACHERS TABLE
-- ============================================================
-- Stores teacher information

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
-- Stores student information

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
-- Stores game assignments to students

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
    status VARCHAR(20) DEFAULT 'pending', -- pending, in_progress, completed
    is_mandatory BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 8. SCORES TABLE
-- ============================================================
-- Stores scores when students complete games

CREATE TABLE IF NOT EXISTS scores (
    id SERIAL PRIMARY KEY,
    assignment_id INT NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    student_id INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    game_id INT NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    class_id INT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    skill_id INT NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    score INT DEFAULT 0,
    max_score INT DEFAULT 50,
    percentage DECIMAL(5,2),
    correct_answers INT DEFAULT 0,
    wrong_answers INT DEFAULT 0,
    total_questions INT DEFAULT 5,
    completion_time INT, -- in seconds
    performance_level VARCHAR(20), -- poor, average, good, excellent
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 9. AUDIO FEEDBACK TABLE
-- ============================================================
-- Stores audio feedback given to students

CREATE TABLE IF NOT EXISTS audio_feedback (
    id SERIAL PRIMARY KEY,
    score_id INT NOT NULL REFERENCES scores(id) ON DELETE CASCADE,
    feedback_type VARCHAR(20), -- correct, wrong, celebration
    frequency INT,
    duration INT,
    is_played BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 10. ANALYTICS TABLE
-- ============================================================
-- Aggregate student performance data

CREATE TABLE IF NOT EXISTS analytics (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(id) ON DELETE CASCADE,
    class_id INT REFERENCES classes(id) ON DELETE CASCADE,
    subject_id INT REFERENCES subjects(id) ON DELETE CASCADE,
    skill_id INT REFERENCES skills(id) ON DELETE CASCADE,
    games_played INT DEFAULT 0,
    games_completed INT DEFAULT 0,
    total_score INT DEFAULT 0,
    average_score DECIMAL(5,2),
    total_time_spent INT, -- in minutes
    last_played TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 11. API LOGS TABLE
-- ============================================================
-- Stores API request logs for monitoring

CREATE TABLE IF NOT EXISTS api_logs (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(255),
    method VARCHAR(10), -- GET, POST, PUT, DELETE
    status_code INT,
    response_time INT, -- in milliseconds
    user_id INT REFERENCES students(id) ON DELETE SET NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 12. SYSTEM SETTINGS TABLE
-- ============================================================
-- Stores system configuration

CREATE TABLE IF NOT EXISTS system_settings (
    id SERIAL PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    setting_type VARCHAR(50), -- string, integer, boolean, json
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Default Settings
INSERT INTO system_settings (setting_key, setting_value, setting_type, description) VALUES
    ('app_name', 'MyClassboard Games', 'string', 'Application name'),
    ('app_version', '1.0.0', 'string', 'Application version'),
    ('max_games_per_assignment', '5', 'integer', 'Maximum games assigned per session'),
    ('points_per_correct', '10', 'integer', 'Points awarded for correct answer'),
    ('enable_audio_feedback', 'true', 'boolean', 'Enable audio feedback for answers'),
    ('enable_animations', 'true', 'boolean', 'Enable visual animations'),
    ('session_timeout_minutes', '30', 'integer', 'Session timeout in minutes'),
    ('max_session_per_student', '3', 'integer', 'Maximum concurrent sessions per student')
ON CONFLICT (setting_key) DO NOTHING;

-- ============================================================
-- CREATE INDEXES FOR PERFORMANCE
-- ============================================================

-- Students Indexes
CREATE INDEX IF NOT EXISTS idx_students_class ON students(class_id);
CREATE INDEX IF NOT EXISTS idx_students_roll ON students(roll_number);
CREATE INDEX IF NOT EXISTS idx_students_active ON students(is_active);

-- Assignments Indexes
CREATE INDEX IF NOT EXISTS idx_assignments_student ON assignments(student_id);
CREATE INDEX IF NOT EXISTS idx_assignments_game ON assignments(game_id);
CREATE INDEX IF NOT EXISTS idx_assignments_status ON assignments(status);
CREATE INDEX IF NOT EXISTS idx_assignments_teacher ON assignments(teacher_id);
CREATE INDEX IF NOT EXISTS idx_assignments_deadline ON assignments(deadline);

-- Scores Indexes
CREATE INDEX IF NOT EXISTS idx_scores_student ON scores(student_id);
CREATE INDEX IF NOT EXISTS idx_scores_game ON scores(game_id);
CREATE INDEX IF NOT EXISTS idx_scores_class ON scores(class_id);
CREATE INDEX IF NOT EXISTS idx_scores_skill ON scores(skill_id);
CREATE INDEX IF NOT EXISTS idx_scores_completed ON scores(completed_at);

-- Games Indexes
CREATE INDEX IF NOT EXISTS idx_games_skill ON games(skill_id);
CREATE INDEX IF NOT EXISTS idx_games_class ON games(class_id);
CREATE INDEX IF NOT EXISTS idx_games_active ON games(is_active);

-- Skills Indexes
CREATE INDEX IF NOT EXISTS idx_skills_subject ON skills(subject_id);
CREATE INDEX IF NOT EXISTS idx_skills_class ON skills(class_id);

-- Subjects Indexes
CREATE INDEX IF NOT EXISTS idx_subjects_class ON subjects(class_id);

-- Analytics Indexes
CREATE INDEX IF NOT EXISTS idx_analytics_student ON analytics(student_id);
CREATE INDEX IF NOT EXISTS idx_analytics_class ON analytics(class_id);
CREATE INDEX IF NOT EXISTS idx_analytics_skill ON analytics(skill_id);

-- API Logs Indexes
CREATE INDEX IF NOT EXISTS idx_api_logs_endpoint ON api_logs(endpoint);
CREATE INDEX IF NOT EXISTS idx_api_logs_user ON api_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_api_logs_created ON api_logs(created_at);

-- ============================================================
-- CREATE VIEWS FOR REPORTING
-- ============================================================

-- Student Performance View
CREATE OR REPLACE VIEW student_performance AS
SELECT
    s.id,
    s.name,
    s.roll_number,
    c.name as class,
    COUNT(DISTINCT sc.id) as games_played,
    ROUND(AVG(sc.score)::numeric, 2) as average_score,
    SUM(CASE WHEN sc.score >= 40 THEN 1 ELSE 0 END) as games_passed,
    MAX(sc.completed_at) as last_played
FROM students s
LEFT JOIN classes c ON s.class_id = c.id
LEFT JOIN scores sc ON s.id = sc.student_id
GROUP BY s.id, s.name, s.roll_number, c.name;

-- Class Performance View
CREATE OR REPLACE VIEW class_performance AS
SELECT
    c.id,
    c.name as class,
    COUNT(DISTINCT s.id) as total_students,
    COUNT(DISTINCT sc.student_id) as students_played,
    ROUND(AVG(sc.score)::numeric, 2) as average_class_score,
    COUNT(DISTINCT sc.id) as total_games_played
FROM classes c
LEFT JOIN students s ON c.id = s.class_id
LEFT JOIN scores sc ON s.id = sc.student_id
GROUP BY c.id, c.name;

-- Skill Performance View
CREATE OR REPLACE VIEW skill_performance AS
SELECT
    sk.id,
    sk.name as skill,
    sub.name as subject,
    c.name as class,
    COUNT(DISTINCT sc.id) as games_played,
    ROUND(AVG(sc.score)::numeric, 2) as average_score,
    COUNT(DISTINCT sc.student_id) as students_attempted
FROM skills sk
LEFT JOIN subjects sub ON sk.subject_id = sub.id
LEFT JOIN classes c ON sk.class_id = c.id
LEFT JOIN games g ON sk.id = g.skill_id
LEFT JOIN scores sc ON g.id = sc.game_id
GROUP BY sk.id, sk.name, sub.name, c.name;

-- ============================================================
-- CREATE FUNCTIONS FOR AUTOMATION
-- ============================================================

-- Function to update assignment status
CREATE OR REPLACE FUNCTION update_assignment_status()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE assignments
    SET status = 'completed', updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.assignment_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update assignment status when score is added
CREATE TRIGGER trigger_update_assignment_status
AFTER INSERT ON scores
FOR EACH ROW
EXECUTE FUNCTION update_assignment_status();

-- Function to update analytics
CREATE OR REPLACE FUNCTION update_analytics()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO analytics (student_id, class_id, skill_id, games_played, total_score, average_score, last_played)
    SELECT
        NEW.student_id,
        NEW.class_id,
        NEW.skill_id,
        1,
        NEW.score,
        NEW.score,
        NEW.completed_at
    ON CONFLICT (student_id, skill_id) DO UPDATE SET
        games_played = analytics.games_played + 1,
        total_score = analytics.total_score + NEW.score,
        average_score = (analytics.total_score + NEW.score)::numeric / (analytics.games_played + 1),
        last_played = NEW.completed_at,
        updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update analytics when score is added
CREATE TRIGGER trigger_update_analytics
AFTER INSERT ON scores
FOR EACH ROW
EXECUTE FUNCTION update_analytics();

-- ============================================================
-- VERIFY SCHEMA
-- ============================================================

SELECT
    'Tables created successfully' as status,
    COUNT(*) as table_count
FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE';

-- ============================================================
-- END OF SCRIPT
-- ============================================================
-- All tables created successfully for production use!
-- Next: Run Flask application to connect to database
-- Then: Update .env file with DATABASE_URL
-- Finally: Test API endpoints with data

COMMIT;
