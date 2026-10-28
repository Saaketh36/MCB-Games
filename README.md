# 🎮 MyClassboard Games Platform — Kids Learning Arena

[![Platform](https://img.shields.io/badge/Platform-MyClassboard%20Games-6366f1.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.7+-3776AB.svg?logo=python&logoColor=white)](#)
[![Flask](https://img.shields.io/badge/Backend-Flask%20%2B%20SQLAlchemy-000000.svg?logo=flask)](#)
[![Database](https://img.shields.io/badge/Database-PostgreSQL-336791.svg?logo=postgresql&logoColor=white)](#)
[![Frontend](https://img.shields.io/badge/Frontend-Vanilla%20JS%20%2B%20Modern%20CSS-F7DF1E.svg)](#)

A comprehensive interactive educational games platform covering **Class I through Class VIII** across **English**, **Mathematics**, and **Science**. Features a clean white-themed modern UI, an interactive **Student Learning Arena**, a **Teacher Hub** for task assignments, PIN-based exam access, real-time score tracking, audio feedback, and video lessons.

---

## 🌟 Key Features

* **🎨 Kids Learning Arena (`index.html`)**: Clean, responsive, glassmorphic UI with grade selector (Class I–VIII), subject filtering, and skill-area table grouping.
* **👩‍🏫 Teacher Hub**:
  * Create assignments for students with customized deadlines.
  * Unique PIN generation for student exams and tasks.
  * Real-time student performance tracking and score table.
  * Assignment management (filter by class/subject, delete completed tasks).
* **🎮 12 Interactive Game Types**:
  * ❓ MCQ Quiz / Odd One Out
  * 🔤 Word Scramble / Guess the Word
  * ✍️ Fill in the Blank
  * 🧩 Match Pairs / Memory Match
  * 📦 Sort & Group
  * 🔢 Sequence Order
  * ⏱️ Timed Challenge
  * 📝 Story Builder / Typing Answer
* **🔊 Audio & Sound Feedback**: Spoken listening narrations (`audio/*.wav`) and Web Audio synth for instant correctness sounds.
* **📊 Analytics & Visualizations**: Interactive performance reports and data visualization charts (`data-graphs.html`).
* **🗄️ Robust PostgreSQL Backend**: SQLAlchemy ORM models for Classes, Subjects, Skills, Games, Teachers, Students, Assignments, Scores, and PINs.

---

## 🚀 Quick Start

### 1. Requirements
* **Python**: 3.7 or higher
* **PostgreSQL**: Local or remote instance
* **Node.js** *(optional)*: For `npm run dev` server runner

### 2. Install Dependencies
```bash
pip install -r requirements.txt
npm install
```

### 3. Initialize PostgreSQL Database
Ensure PostgreSQL is running, then run the automated setup script:
```bash
python setup_database.py
```
*(On Windows, you can also double-click `RUN_SETUP.bat`)*

### 4. Run the Application
```bash
npm run dev
# or: python backend/app.py
```
Open your browser and navigate to:
👉 **[http://localhost:5000](http://localhost:5000)** *(or open `index.html` directly)*

### 5. Run Verification Suites
```bash
npm test
# or: python tools/verify_all.py
```

---

## 📂 Project Organization

```
├── index.html                   # Main application: Kids Learning Arena & Teacher Hub SPA
├── package.json                 # Node scripts (npm run dev, npm test)
├── requirements.txt             # Python dependencies
├── REORGANIZATION_PLAN.md       # Comprehensive modular architectural plan
├── RUN_SETUP.bat                # 1-click Windows database setup launcher
├── full_games_catalog.js        # Authoritative catalog of all 440 curriculum games & questions
├── full_games_catalog.json      # JSON mirror of the 440-activity dataset
├── .env.example                 # Sanitized environment configuration template
│
├── js/                          # Modular Frontend JavaScript Architecture
│   ├── core/                    # Reactive state, rosters, storage ('mcb_assignments_v8')
│   ├── portals/                 # Kid Zone, Teacher Hub (table with assigned-order sort), Split View
│   ├── quest/                   # Fullscreen Quest Arena, question evaluators, review screen
│   ├── authoring/               # Custom task builder, hierarchical skill picker, offline AI generator
│   ├── class2_games.js          # Interactive mini-game engine
│   └── app.js                   # Application bootstrap & lifecycle orchestrator
│
├── css/                         # Modular CSS Component Layers
│   ├── base/                    # Resets, typography, tokens, responsive breakpoints
│   ├── components/              # Navigation, badges, cards, assignment modals
│   ├── portals/                 # Kid Zone hero/grid, Teacher Hub, Split View
│   ├── quest/                   # Quest runner, question screen, context studio
│   ├── authoring/               # Create task dialog, skill area tree picker
│   └── styles.css               # Main entry point importing component layers
│
├── backend/                     # Structured Python / Flask API Backend
│   ├── app.py                   # Canonical Flask REST server & routes
│   ├── models.py                # SQLAlchemy ORM models (PostgreSQL)
│   ├── ai_helper.py             # Gemini AI question generator
│   ├── ai_cache.py              # Local task & question cache
│   ├── routes/                  # Modular Blueprints (assignment_routes.py, scoring_routes.py)
│   └── services/                # Business logic (scoring_system.py, setup_database.py)
│
├── database/                    # SQL Database Schemas & Setup Scripts
│   ├── CREATE-DATABASE-PRODUCTION.sql # Production PostgreSQL DDL & seeds
│   └── create_tables.sql        # Table definitions
│
├── tools/                       # Active Verification Suites & Content Pipeline
│   ├── verify_all.py            # Master CLI runner executing all active quality suites
│   ├── verify_critical_content_fixes.py # Content directives & prompt cleaner
│   ├── verify_clean_formatting.py # Formula and answer leak validator
│   ├── verify_assigned_order_sorting.py # Teacher table assigned-order sort validator
│   ├── verify_diorama_catalog.py # 3D diorama thumbnail integrity suite
│   ├── pipeline/                # Offline media, audio, and reading passage generators
│   └── archive/                 # Archived historical one-off patch scripts
│
├── audio/                       # Spoken voice narrations (WAV) & sound effects
├── images/                      # Bespoke 3D diorama thumbnails & UI assets
├── docs/                        # Complete project documentation library
└── archive/                     # Historical prototypes, legacy pages, and scratch scripts
```

---

## 🔌 API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/curriculum` | Returns all classes, subjects, and skill areas |
| `GET` | `/api/subjects/<class_id>` | Returns subjects for a specific class |
| `GET` | `/api/skills/<class_id>/<subject>` | Returns skills for a specific class and subject |
| `GET` | `/api/games/<skill>` | Returns games associated with a skill |
| `GET` | `/api/available-games` | Returns list of available games and paths |
| `GET` | `/api/portal/assignments` | Fetches all student assignments |
| `POST` | `/api/portal/assignments` | Creates an assignment for a student |
| `DELETE` | `/api/portal/assignments/<id>` | Deletes an assignment |
| `POST` | `/api/portal/generate-pin` | Generates a 6-digit PIN for an activity |
| `POST` | `/api/portal/verify-pin` | Verifies a student PIN and retrieves game info |
| `POST` | `/api/portal/store-student-score` | Records game completion score and locks PIN |
| `POST` | `/api/scoring/submit` | Submits score to the scoring engine |

---

## 📚 Documentation Library

For in-depth guides, architecture specifications, and setup instructions, consult the [docs/](docs/README.md) directory:

* [Database Setup Guide](docs/setup/DATABASE-SETUP-GUIDE.md)
* [Environment Configuration Guide](docs/setup/ENV-SETUP-GUIDE.md)
* [Scoring API Documentation](docs/guides/SCORING_API_DOCUMENTATION.md)
* [Curriculum Question Audit](docs/guides/QUESTION_AUDIT.md)
* [Teacher Workflow & Implementation](docs/guides/TEACHER_WORKFLOW.md)
* [Glassmorphism Design Guide](docs/guides/GLASS_MORPHISM_GUIDE.md)

---

## 📄 License
This project is licensed under the MIT License.
