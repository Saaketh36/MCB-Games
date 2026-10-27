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
python app.py
```
*(Or run `npm run dev` to start the server and automatically launch your default browser).*

Open your browser and navigate to:
👉 **[http://localhost:5000](http://localhost:5000)**

---

## 📂 Project Organization

```
├── index.html                   # Main application: Kids Learning Arena & Teacher Hub SPA
├── play.html                    # Interactive activity player
├── exam.html                    # PIN-based student exam taker
├── data-graphs.html             # Student performance data visualization & Chart.js graphs
├── app.py                       # Main Flask web application and API server
├── models.py                    # SQLAlchemy database models
├── assignment_routes.py         # Blueprint for /api/portal (assignments, PINs, student scores)
├── scoring_routes.py            # Blueprint for /api/scoring (score calculations & feedback)
├── scoring_system.py            # Scoring rules and audio feedback helper
├── setup_database.py            # Automated PostgreSQL database initializer
├── RUN_SETUP.bat                # 1-click Windows database setup launcher
├── full_games_catalog.js        # Catalog of 325 curriculum games with rich question data
├── curriculum-data.js           # Curriculum hierarchy (Classes, Subjects, Skills, Activities)
├── curriculum_catalog.json      # Valid curriculum combinations for validation
├── requirements.txt             # Python dependencies
├── package.json                 # Node scripts & dependencies
├── .env                         # Local environment settings & database URL (git-ignored)
├── .env.example                 # Sanitized environment configuration template
│
├── audio/                       # Spoken voice narrations (WAV) & sound effects
├── content/                     # Class-specific modular game content (class-I.js ... class-VIII.js)
├── curriculum/                  # Official curriculum specifications and PDF references
├── database/                    # SQL database schemas & setup scripts
│   ├── CREATE-DATABASE-PRODUCTION.sql # Production PostgreSQL database DDL
│   ├── create_tables.sql              # Table creation scripts
│   └── scripts/                       # Migration & auxiliary database tools
├── docs/                        # Complete project documentation library
│   ├── README.md                # Documentation index & map
│   ├── guides/                  # Architecture, feature, and scoring guides
│   ├── setup/                   # Setup guides for PostgreSQL, Python, and Node
│   ├── reports/                 # Verification certificates and audit logs
│   └── design/                  # UI design tokens, templates, and wireframes
├── images/                      # Game thumbnails, subject banners, and UI icons
├── scripts/                     # Developer automation & launcher scripts (open-browser.js)
├── legacy/                      # Archived early iterations, standalone games & flat JSON stores
│   ├── standalone_games/        # 46 early standalone HTML games & score_client.js
│   ├── data/                    # Legacy flat JSON stores (assignments, completions, games-data)
│   └── generators/              # Early standalone game generators (create_all_games.py)
├── tools/                       # Maintenance scripts, bank auditors, and audio generators
└── videos/                      # Lesson video metadata and content
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
