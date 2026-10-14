# Game Scoring & Performance Tracking API

Complete API documentation for student scoring, feedback, and performance analytics.

---

## 🎯 Overview

The scoring system provides:
- ✅ Real-time score calculation
- ✅ Visual feedback (✅ correct, ❌ wrong)
- ✅ Performance tracking (Excellent, Good, Average, Poor)
- ✅ Student analytics and mastery levels
- ✅ Class leaderboards
- ✅ Skill-based performance reports

---

## 📊 Scoring Calculation

### Score Formula
```
Score = Correct Answers × 10 points
Max Score = Total Questions × 10 points
Percentage = (Correct Answers / Total Questions) × 100
```

### Performance Levels
- **Excellent** (80-100%) - ⭐⭐⭐⭐⭐ 🎉
- **Good** (60-79%) - ⭐⭐⭐⭐ 👏
- **Average** (40-59%) - ⭐⭐⭐ 👍
- **Poor** (0-39%) - ⭐⭐ 💪

---

## 🎮 API Endpoints

### 1. Submit Game Score

**Endpoint:** `POST /api/scoring/submit`

**Description:** Submit game responses and calculate score

**Request Body:**
```json
{
  "assignment_id": 1,
  "student_id": 1,
  "game_id": 1,
  "class_id": 1,
  "skill_id": 1,
  "responses": [
    {
      "question_id": 1,
      "user_answer": "A",
      "correct_answer": "A"
    },
    {
      "question_id": 2,
      "user_answer": "B",
      "correct_answer": "C"
    }
  ]
}
```

**Response (Success):**
```json
{
  "status": "success",
  "message": "Score submitted successfully",
  "score_id": 1,
  "score_data": {
    "score": 50,
    "max_score": 100,
    "percentage": 50,
    "correct_answers": 5,
    "wrong_answers": 5,
    "total_questions": 10,
    "performance_level": "average"
  },
  "visual_feedback": {
    "emoji": "👍",
    "message": "Good effort! Keep practicing!",
    "color": "yellow",
    "stars": "⭐⭐⭐",
    "percentage": 50,
    "performance_level": "average",
    "correct": 5,
    "wrong": 5,
    "total": 10
  },
  "responses_feedback": [
    {
      "question_id": 1,
      "feedback": {
        "status": "✅ CORRECT",
        "emoji": "✅",
        "message": "Great!",
        "color": "green",
        "sound": "correct"
      }
    },
    {
      "question_id": 2,
      "feedback": {
        "status": "❌ WRONG",
        "emoji": "❌",
        "message": "Correct answer: C",
        "color": "red",
        "sound": "wrong"
      }
    }
  ]
}
```

---

### 2. Get Student Performance

**Endpoint:** `GET /api/scoring/student/<student_id>/performance`

**Description:** Get student's overall performance across all games

**Response:**
```json
{
  "status": "success",
  "data": {
    "student_id": 1,
    "total_games_played": 10,
    "total_score": 450,
    "average_percentage": 75.5,
    "performance_breakdown": {
      "excellent": 5,
      "good": 3,
      "average": 1,
      "poor": 1
    },
    "scores": [
      {
        "id": 1,
        "game_id": 1,
        "score": 80,
        "percentage": 80,
        "performance_level": "excellent",
        "completed_at": "2025-10-09T10:30:00"
      }
    ]
  }
}
```

---

### 3. Get Skill Mastery Level

**Endpoint:** `GET /api/scoring/student/<student_id>/skill/<skill_id>/mastery`

**Description:** Get student's mastery level for a specific skill

**Response:**
```json
{
  "status": "success",
  "data": {
    "student_id": 1,
    "skill_id": 1,
    "attempts": 5,
    "average_percentage": 82.0,
    "mastery_level": "Mastered",
    "scores": [
      {
        "id": 1,
        "score": 90,
        "percentage": 90,
        "performance_level": "excellent",
        "completed_at": "2025-10-09T10:30:00"
      }
    ]
  }
}
```

**Mastery Levels:**
- **Mastered** - 80% and above
- **Proficient** - 60-79%
- **Developing** - 40-59%
- **Beginning** - Below 40%

---

### 4. Get Class Performance

**Endpoint:** `GET /api/scoring/class/<class_id>/performance`

**Description:** Get performance summary for entire class

**Response:**
```json
{
  "status": "success",
  "data": {
    "class_id": 1,
    "total_students": 30,
    "students_data": [
      {
        "student_id": 1,
        "total_games_played": 10,
        "total_score": 450,
        "average_percentage": 75.5,
        "performance_breakdown": {
          "excellent": 5,
          "good": 3,
          "average": 1,
          "poor": 1
        }
      }
    ]
  }
}
```

---

### 5. Get Student Scores

**Endpoint:** `GET /api/scoring/student/<student_id>/scores`

**Description:** Get all scores for a specific student

**Response:**
```json
{
  "status": "success",
  "student_id": 1,
  "total_scores": 10,
  "scores": [
    {
      "id": 1,
      "game_id": 1,
      "score": 80,
      "max_score": 100,
      "percentage": 80.0,
      "correct_answers": 8,
      "wrong_answers": 2,
      "total_questions": 10,
      "performance_level": "excellent",
      "completed_at": "2025-10-09T10:30:00"
    }
  ]
}
```

---

### 6. Get Game Scores

**Endpoint:** `GET /api/scoring/game/<game_id>/scores`

**Description:** Get all scores for a specific game (across all students)

**Response:**
```json
{
  "status": "success",
  "game_id": 1,
  "total_attempts": 45,
  "average_percentage": 72.5,
  "scores": [
    {
      "id": 1,
      "student_id": 1,
      "score": 80,
      "percentage": 80.0,
      "performance_level": "excellent"
    }
  ]
}
```

---

### 7. Get Score Details

**Endpoint:** `GET /api/scoring/score/<score_id>`

**Description:** Get detailed information about a specific score

**Response:**
```json
{
  "status": "success",
  "score": {
    "id": 1,
    "student_id": 1,
    "game_id": 1,
    "score": 80,
    "percentage": 80.0,
    "performance_level": "excellent"
  },
  "visual_feedback": {
    "emoji": "🎉",
    "message": "Excellent! Outstanding performance!",
    "color": "green",
    "stars": "⭐⭐⭐⭐⭐",
    "percentage": 80.0,
    "correct": 8,
    "wrong": 2,
    "total": 10
  }
}
```

---

### 8. Get Class Leaderboard

**Endpoint:** `GET /api/scoring/class/<class_id>/leaderboard`

**Description:** Get top performers in a class

**Response:**
```json
{
  "status": "success",
  "class_id": 1,
  "leaderboard": [
    {
      "rank": 1,
      "student_id": 1,
      "student_name": "John Doe",
      "roll_number": "001",
      "average_percentage": 85.5,
      "total_games": 10,
      "total_score": 855
    },
    {
      "rank": 2,
      "student_id": 2,
      "student_name": "Jane Smith",
      "roll_number": "002",
      "average_percentage": 78.3,
      "total_games": 10,
      "total_score": 783
    }
  ]
}
```

---

### 9. Get Skill Leaderboard

**Endpoint:** `GET /api/scoring/skill/<skill_id>/leaderboard`

**Description:** Get top performers for a specific skill

**Response:**
```json
{
  "status": "success",
  "skill_id": 1,
  "leaderboard": [
    {
      "rank": 1,
      "student_id": 1,
      "student_name": "John Doe",
      "average_percentage": 90.0,
      "attempts": 5
    },
    {
      "rank": 2,
      "student_id": 2,
      "student_name": "Jane Smith",
      "average_percentage": 85.0,
      "attempts": 4
    }
  ]
}
```

---

## 🧪 Example Usage

### Submit Game with 5 Questions

```bash
curl -X POST http://localhost:5000/api/scoring/submit \
  -H "Content-Type: application/json" \
  -d '{
    "assignment_id": 1,
    "student_id": 1,
    "game_id": 1,
    "class_id": 1,
    "skill_id": 1,
    "responses": [
      {"question_id": 1, "user_answer": "A", "correct_answer": "A"},
      {"question_id": 2, "user_answer": "B", "correct_answer": "B"},
      {"question_id": 3, "user_answer": "C", "correct_answer": "D"},
      {"question_id": 4, "user_answer": "A", "correct_answer": "A"},
      {"question_id": 5, "user_answer": "B", "correct_answer": "B"}
    ]
  }'
```

**Result:** 4/5 correct = 80% = Excellent ✅ 👏

---

### Get Student Performance

```bash
curl http://localhost:5000/api/scoring/student/1/performance
```

---

### Get Class Leaderboard

```bash
curl http://localhost:5000/api/scoring/class/1/leaderboard
```

---

## 📈 Visual Feedback System

### Correct Answer
```
✅ CORRECT - Great!
Sound: "correct" (ding/bell)
```

### Wrong Answer
```
❌ WRONG - Correct answer: [answer]
Sound: "wrong" (buzzer/error)
```

### Game Completion
```
🎉 Excellent! Outstanding performance! ⭐⭐⭐⭐⭐
👏 Great job! Good performance! ⭐⭐⭐⭐
👍 Good effort! Keep practicing! ⭐⭐⭐
💪 Keep trying! You can do better! ⭐⭐
```

---

## 💾 Database Schema

### Score Table
```sql
CREATE TABLE scores (
  id SERIAL PRIMARY KEY,
  assignment_id INT NOT NULL,
  student_id INT NOT NULL,
  game_id INT NOT NULL,
  class_id INT NOT NULL,
  skill_id INT NOT NULL,
  score INT DEFAULT 0,
  max_score INT DEFAULT 50,
  percentage DECIMAL(5,2),
  correct_answers INT DEFAULT 0,
  wrong_answers INT DEFAULT 0,
  total_questions INT DEFAULT 5,
  performance_level VARCHAR(20),
  completion_time INT,
  completed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔐 Error Handling

### Missing Fields
```json
{
  "status": "error",
  "message": "Missing required fields"
}
```

### Score Not Found
```json
{
  "status": "error",
  "message": "Score not found"
}
```

### Server Error
```json
{
  "status": "error",
  "message": "Error message here"
}
```

---

## 📱 Frontend Integration Example

```javascript
// Submit game score
fetch('http://localhost:5000/api/scoring/submit', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    assignment_id: 1,
    student_id: 1,
    game_id: 1,
    class_id: 1,
    skill_id: 1,
    responses: [
      {question_id: 1, user_answer: 'A', correct_answer: 'A'},
      {question_id: 2, user_answer: 'B', correct_answer: 'C'}
    ]
  })
})
.then(res => res.json())
.then(data => {
  console.log(data.visual_feedback);
  // Show emoji, stars, and message to student
  showFeedback(data.visual_feedback);
});
```

---

## ✨ Features

✅ Real-time scoring  
✅ Instant visual feedback  
✅ Performance tracking  
✅ Skill mastery levels  
✅ Student analytics  
✅ Class leaderboards  
✅ Detailed reports  
✅ Sound feedback  

---

## 📝 Notes

- All timestamps are in UTC
- Percentages are rounded to 2 decimal places
- Performance levels are automatically calculated
- Scores are immutable once saved
- Assignments auto-update to "completed" when score is submitted

---

**Last Updated:** October 9, 2025  
**Version:** 1.0
