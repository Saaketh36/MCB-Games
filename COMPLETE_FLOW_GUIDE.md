# 🎯 COMPLETE TEACHER-STUDENT GAME FLOW

## Visual Workflow

### HOME PAGE
┌─────────────────────────────────────────┐
│  MyClassboard Kindergarten & Grade      │
│  325 Curriculum Games                   │
│  [PLAY NOW Button]                      │
│                                         │
│  👨‍🎓 Student Portal    👨‍🏫 Teacher Portal  │
└─────────────────────────────────────────┘
         ↓ Both lead to same flow

### STEP 1: CLASS SELECTION
┌─────────────────────────────────────────┐
│ Select Your Class Level                 │
│                                         │
│  🌱 Class I    🌿 Class II   🍀 Class III │
│  📘 Class IV   ⭐ Class V    🚀 Class VI  │
│  🔬 Class VII  🏆 Class VIII            │
└─────────────────────────────────────────┘
         ↓ User clicks Class I

### STEP 2: SUBJECT SELECTION
┌─────────────────────────────────────────┐
│ Class I — Select Subject                │
│                                         │
│  📖 English        📐 Mathematics        │
│  (10 skills)       (7 skills)           │
│                                         │
│  🌿 EVS            🧪 Science           │
│  (11 skills)       (Not in Class I)     │
└─────────────────────────────────────────┘
         ↓ User clicks English

### STEP 3: ACTIVITY CATALOG
┌─────────────────────────────────────────┐
│ Class I English Catalog                 │
│                                         │
│ 🎯 Listen & Do Adventure                │
│    Sub-Skill: Following Instructions    │
│    Type: Sequence Order      [PLAY NOW] │
│                                         │
│ 🎯 Story Time Quiz                      │
│    Sub-Skill: Listening Comprehension   │
│    Type: MCQ Quiz            [PLAY NOW] │
│                                         │
│ 🎯 Picture Story Teller                 │
│    Sub-Skill: Oral Expression           │
│    Type: Story Builder       [PLAY NOW] │
│    ...
└─────────────────────────────────────────┘
         ↓ User clicks "PLAY NOW" on Activity

### GAME LOADING SCREEN
┌─────────────────────────────────────────┐
│ Listen & Do Adventure                   │
│ Class I • English                       │
│                                    Score: 0 │
│                                         │
│ 🔊 AUDIO AGENT BOX:                     │
│  Listen to whole story (11.75 seconds)  │
│  [Audio Player]                         │
│  [Replay Story] [Show Story Text]       │
│  [Start Questions Button]               │
│                                         │
│ Questions locked until story ends       │
└─────────────────────────────────────────┘
         ↓ Audio plays automatically

### GAME QUESTIONS PHASE
┌─────────────────────────────────────────┐
│ Listen & Do Adventure                   │
│ Class I • English          Score: 10    │
│                                         │
│ Question 1 of 4                         │
│ Sub-Skill: Following Instructions       │
│                                         │
│ ❓ What must you do first?               │
│                                         │
│ [▲ Open the book]   [◆ Write your name]│
│ [● Listen more]     [■ None of these]  │
│                                         │
│ [Waiting for answer...]                 │
└─────────────────────────────────────────┘
         ↓ User clicks option

### ANSWER FEEDBACK
┌─────────────────────────────────────────┐
│ Listen & Do Adventure                   │
│ Class I • English          Score: 20    │
│                                         │
│ Question 1 of 4                         │
│                                         │
│ ❓ What must you do first?               │
│                                         │
│ 🎉 CORRECT ANSWER! (+10 pts)           │
│                                         │
│ The passage begins with "First, open   │
│ your book to page five."                │
│                                         │
│ [▲ Open the book ✓]                    │
│ [◆ Write your name] [● Listen more]    │
│ [■ None of these]                      │
│                                         │
│ [Next Question ➔]                      │
│ 🎊 Confetti animation plays!           │
└─────────────────────────────────────────┘
         ↓ User clicks "Next Question"

### MORE QUESTIONS
Question 2, 3, 4 display same way...
         ↓ After all questions answered

### VICTORY SCREEN
┌─────────────────────────────────────────┐
│                                         │
│              🏆                         │
│      Game Completed!                   │
│                                         │
│  Awesome performance in                │
│  "Listen & Do Adventure"!               │
│                                         │
│  Total Score Gained: +40 Points        │
│                                         │
│  [PLAY AGAIN 🔄]  [MORE GAMES 🎮]     │
│                                         │
│  🎊 Confetti animation!                │
└─────────────────────────────────────────┘

---

## CODE FLOW IN index.html

1. navTo('home') → Shows home page
2. Click "PLAY NOW" or "Teacher Portal"
3. navTo('class_select') → Shows class grid
4. Click Class I → navTo('subject_select')
5. Click English → navTo('activity_catalog')
6. Click "PLAY NOW" → navTo('game_play')

At navTo('game_play'):
- startGameSession() called (line 1181)
- getPresetGamePayload() finds questions (line 1345)
- Audio card shown if questions have audio_script
- Audio plays automatically
- renderGameStage() called twice:
  a) First time: Shows "Questions locked" message
  b) After audio ends: Shows questions
- submitOptionChoice() handles answer (line 1278)
- advanceToNextQuestion() moves to next (line 1323)
- renderVictoryStage() shows final score (line 1328)

---

## KEY FUNCTIONS

### Function: getPresetGamePayload(act)
- Location: Line 1345
- Purpose: Retrieve questions from QUESTION_BANK
- Key Format: "Class I|||English|||Listen & Do Adventure"
- Returns: { title, audio_script, audio, audio_seconds, questions [...] }

### Function: startGameSession()
- Location: Line 1181
- Purpose: Initialize game when activity selected
- Sets up: Score, currentQuestion, activePayload, audio player

### Function: renderGameStage()
- Location: Line 1225
- Purpose: Display current question or victory
- Shows: Locked message → Questions → Victory

### Function: submitOptionChoice(optIdx, choice)
- Location: Line 1278
- Purpose: Process answer selection
- Does: Check if correct, show feedback, play sound, add score

### Function: filterActivities(query)
- Location: Line 1158
- Purpose: Display activities for selected class/subject
- Shows: All matching games with play buttons

---

## QUESTION BANK KEY FORMAT

All questions use this key:
`
"{Class}|||{Subject}|||{ActivityName}"
`

Examples:
- "Class I|||English|||Listen & Do Adventure"
- "Class I|||English|||Story Time Quiz"
- "Class I|||English|||Picture Story Teller"
- "Class I|||Mathematics|||Place Value Tower"
- "Class I|||Mathematics|||Add & Subtract Sprint"

To find questions for an activity:
`javascript
const act = CURRICULUM_DATA.find(...);
const key = \\|||\|||\\;
const questions = QUESTION_BANK[key];
`

---

## TESTING IN BROWSER CONSOLE (F12)

Check if questions loaded:
`javascript
Object.keys(QUESTION_BANK).length  // Should be 300+
`

Get questions for specific game:
`javascript
QUESTION_BANK["Class I|||English|||Listen & Do Adventure"]
// Should return:
// {
//   title: "Listen & Do Adventure",
//   audio_script: "...",
//   audio: "audio/listen-do-adventure.wav",
//   audio_seconds: 11.75,
//   questions: [{ question, options, answer, explanation }, ...]
// }
`

Test answer checking:
`javascript
const q = QUESTION_BANK["Class I|||English|||Story Time Quiz"].questions[0];
console.log(q.question);
console.log(q.options);
console.log("Correct answer:", q.answer);
`

---

## HOW STORY PLAYS

1. startGameSession() loads payload with audio_script
2. Audio card displayed with player and "Replay" button
3. Audio file (if exists) loaded into <audio> element
4. playAudioAgentScript() called after 300ms delay (line 1209, 1213)
5. Audio plays automatically
6. While playing: Questions hidden, "Questions locked" shown
7. User can click "Replay" to hear story again
8. When audio ends, "Start Questions" button appears
9. User clicks button → renderGameStage() shows questions
10. Answer all questions → Victory screen

---

## SCORE SYSTEM

- Each correct answer: +10 points
- Each wrong answer: +0 points
- Shown in real-time on screen
- Persists through game session
- Shown on victory screen as "Score Gained"

Score stored in: state.score (global) and state.sessionScore (per game)

---

## MOBILE RESPONSIVE

- Desktop (1024px+): 2-column option grid
- Tablet (768px): 2-column, smaller fonts
- Mobile (480px): 1-column options, compact layout
- Small Mobile (<480px): Full responsive, touch-friendly

---

## COMPLETE DATA FLOW

USER INTERACTION → INDEX.HTML → GAMES_DATA.JS → QUESTION_BANK.JS → DISPLAY

1. User opens index.html
2. games_data.js and question_bank.js loaded automatically
3. User clicks "PLAY NOW"
4. Gets activity from CURRICULUM_DATA (games_data.js)
5. Gets questions from QUESTION_BANK (question_bank.js)
6. Displays story + questions
7. Validates answers against QUESTION_BANK[key].questions[idx].answer
8. Updates score and displays feedback

---

Status: ✅ IMPLEMENTATION COMPLETE AND VERIFIED
Generated: October 5, 2026
