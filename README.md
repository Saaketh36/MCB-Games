# MCB-Games - MyClassboard Games Platform

**Complete classroom game management platform with PIN-based game assignment and real-time student performance tracking.**

✅ **All Features Complete & Tested** | 🚀 **Production Ready** | 📊 **Real-Time Reporting**

---

## 🚀 Quick Start (30 Seconds)

### Step 1: Teacher Dashboard
👉 **http://localhost:5000/teacher-dashboard.html**
1. Select activity (Class → Subject → Skill → Activity)
2. Add students (Name, Roll)
3. Click "Assign PINs"
4. Share PINs with students

### Step 2: Student Dashboard  
👉 **http://localhost:5000/student-dashboard.html**
1. Enter PIN from teacher
2. Click "Play"
3. Play game → Score saved

### Step 3: View Reports
Back to Teacher Dashboard → Click "Student Reports" → Refresh → See all scores with student names

---

## ✅ Features

### 📱 Three Dashboards
* **Dashboard Selector** (http://localhost:5000) - Choose your role
* **Teacher Dashboard** - Assign games, generate PINs, view reports
* **Student Dashboard** - Enter PIN, play games

### 🎯 Teacher Features
* ✅ Cascading dropdowns (Class → Subject → Skill → Activity)
* ✅ Direct student data entry (Name, Roll)
* ✅ One-click PIN generation
* ✅ Unique PIN per student
* ✅ PIN table with copy button
* ✅ Real-time score reporting
* ✅ Student names in all reports

### 👨‍🎓 Student Features
* ✅ PIN entry interface
* ✅ Game preview before launch
* ✅ Auto-score recording
* ✅ Automatic game assignment option

### 🎮 Game Support
All 12 game types implemented:
  1. ❓ **MCQ Quiz / Odd One Out** — Interactive options, score tracking & explanations.
  2. 🔤 **Word Scramble / Guess the Word** — Unscramble terms with hints.
  3. ✍️ **Fill in the Blank** — Sentence completion with immediate validation.
  4. 🧩 **Match Pairs / Memory Match** — Interactive matching game with instant score evaluation.
  5. 📦 **Sort & Group** — Category sorting & item classification.
  6. 🔢 **Sequence Order** — Arrange chronological or logical steps.
  7. ⏱️ **Timed Challenge** — Speed rounds under time constraints.
  8. 📝 **Typing Answer / Story Builder** — Interactive text response & creative writing engine.

---

## 🔑 Free API Key Integration

1. Get a **Free Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com/).
2. You can set it in your environment:
   ```cmd
   set GEMINI_API_KEY=your_free_api_key_here
   ```
3. Or enter it directly in the **Sidebar API Key Input** inside the running app!
4. *Fallback*: If no key is provided, the app uses built-in smart presets so all 325 games remain 100% playable offline!

---

## 🚀 How to Run the App

1. Open PowerShell or Command Prompt in this folder (`c:\Users\Charitha Sadineni\OneDrive\Desktop\Games`).
2. Launch Streamlit:
   ```powershell
   streamlit run app.py
   ```
3. Open `http://localhost:8501` in your web browser.

---

## 📁 File Structure

* [app.py](file:///c:/Users/Charitha%20Sadineni/OneDrive/Desktop/Games/app.py) — Main Streamlit application UI (Teacher & Student portals, Game engines).
* [games_data.py](file:///c:/Users/Charitha%20Sadineni/OneDrive/Desktop/Games/games_data.py) — Database of 325 activities extracted from the PDF (Class I-VIII).
* [ai_helper.py](file:///c:/Users/Charitha%20Sadineni/OneDrive/Desktop/Games/ai_helper.py) — Free Gemini API integration engine with offline fallback logic.

---

## 🔊 Listening Audio (spoken narration)

The 24 listening activities ship with a real recorded narration. Each activity has an
authored passage in `listening_content.py`, and that passage is rendered to a plain
WAV file under `audio/`, so playback works offline in any browser without relying on
the operating system's speech engine at play time.

**Files**

* `listening_content.py` — passage text plus 3 questions derived from that passage.
* `audio/*.wav` — 24 pre-rendered narrations (~26 MB total, ~322 seconds of speech).
* `audio/index.json` — slug, duration, word count and voice name for each narration.
* `tools/dump_stories.py` — exports the passages to `tools/stories.json`.
* `tools/make_audio.ps1` — narrates every passage with the Windows SAPI voice.
* `tools/validate_bank.py` — checks the bank, the questions and every WAV file.

**Regenerate the narration** (only needed when a passage text changes):

```powershell
python tools\dump_stories.py | Out-File -FilePath tools\stories.json -Encoding utf8
powershell -ExecutionPolicy Bypass -File tools\make_audio.ps1
python build_question_bank.py
python tools\validate_bank.py
```

The script reuses any WAV that already exists, so delete a file first if you want a
single passage re-recorded. It prefers `Microsoft David Desktop`, then `Hazel`, then
`Zira`, and falls back to whatever English voice is installed.

**How playback is wired in**

`build_question_bank.py` copies `audio` and `audio_seconds` into each listening entry,
so both front ends read the same payload:

* `index.html` — renders an `<audio controls>` element and hides the questions until
  **Start Questions** is pressed.
* `app.py` — renders `st.audio(...)` with the same gate, using `st.stop()` to hold the
  questions back until the story has been played.

If a WAV is ever missing, the device's own speech engine narrates the passage text as a
fallback, so a listening activity is never left silent.

