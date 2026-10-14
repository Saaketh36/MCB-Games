# Game Scoring System - Quick Reference

## 🎯 Quick Start

### Submit Game Score
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
      {"question_id": 3, "user_answer": "C", "correct_answer": "D"}
    ]
  }'
```

**Result:** 2/3 = 66.67% = Good 👏

---

## 📊 All Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/scoring/submit` | POST | Submit game score |
| `/api/scoring/student/<id>/performance` | GET | Student performance |
| `/api/scoring/student/<id>/skill/<id>/mastery` | GET | Skill mastery |
| `/api/scoring/class/<id>/performance` | GET | Class performance |
| `/api/scoring/student/<id>/scores` | GET | All student scores |
| `/api/scoring/game/<id>/scores` | GET | All game scores |
| `/api/scoring/score/<id>` | GET | Score details |
| `/api/scoring/class/<id>/leaderboard` | GET | Class leaderboard |
| `/api/scoring/skill/<id>/leaderboard` | GET | Skill leaderboard |

---

## 🎮 Scoring Formula

```
Score = Correct Answers × 10
Percentage = (Correct Answers / Total Questions) × 100
```

---

## ⭐ Performance Levels

| Level | Range | Icon | Color |
|-------|-------|------|-------|
| Excellent | 80-100% | 🎉 ⭐⭐⭐⭐⭐ | Green |
| Good | 60-79% | 👏 ⭐⭐⭐⭐ | Light Green |
| Average | 40-59% | 👍 ⭐⭐⭐ | Yellow |
| Poor | 0-39% | 💪 ⭐⭐ | Orange |

---

## ✅ Answer Feedback

| Status | Icon | Color |
|--------|------|-------|
| Correct | ✅ | Green |
| Wrong | ❌ | Red |

---

## 📈 Get Student Performance

```bash
curl http://localhost:5000/api/scoring/student/1/performance
```

Response includes:
- Total games played
- Average percentage
- Performance breakdown (Excellent/Good/Average/Poor)
- All individual scores

---

## 🏆 Get Class Leaderboard

```bash
curl http://localhost:5000/api/scoring/class/1/leaderboard
```

Response shows:
- Student ranks by average percentage
- Total games played
- Total score
- Student names and roll numbers

---

## 🎯 Get Skill Mastery

```bash
curl http://localhost:5000/api/scoring/student/1/skill/1/mastery
```

Response shows:
- Mastery level (Mastered/Proficient/Developing/Beginning)
- Attempts count
- Average percentage
- All attempts

**Mastery Levels:**
- Mastered: 80%+
- Proficient: 60-79%
- Developing: 40-59%
- Beginning: <40%

---

## 📝 Request Format

All score submissions require:
```json
{
  "assignment_id": NUMBER,
  "student_id": NUMBER,
  "game_id": NUMBER,
  "class_id": NUMBER,
  "skill_id": NUMBER,
  "responses": [
    {
      "question_id": NUMBER,
      "user_answer": "STRING",
      "correct_answer": "STRING"
    }
  ]
}
```

---

## 📊 Response Format

Success response includes:
```json
{
  "status": "success",
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
    "stars": "⭐⭐⭐",
    "message": "Good effort! Keep practicing!"
  }
}
```

---

## 🔍 Common Queries

### Get Student's Best Score
```bash
curl http://localhost:5000/api/scoring/student/1/scores | jq '.scores | max_by(.percentage)'
```

### Get Game Average Score
```bash
curl http://localhost:5000/api/scoring/game/1/scores
# Look for "average_percentage" in response
```

### Get Top Student in Class
```bash
curl http://localhost:5000/api/scoring/class/1/leaderboard | jq '.leaderboard[0]'
```

---

## 💡 Tips

1. **Always include all 5 fields** in submit request
2. **Use question_id** to track which question has errors
3. **Case-insensitive** matching for answers
4. **Scores are immutable** once saved
5. **Performance level auto-calculated** based on percentage
6. **Assignment auto-updated** to "completed" when scored

---

## 🧪 Example: 5-Question Game

**Input:**
- Questions: 5
- Correct: 4
- Wrong: 1

**Calculation:**
- Score: 4 × 10 = 40 points
- Percentage: 4/5 × 100 = 80%
- Level: Excellent 🎉
- Stars: ⭐⭐⭐⭐⭐
- Message: "Excellent! Outstanding performance!"

---

## 🧪 Example: 10-Question Game

**Input:**
- Questions: 10
- Correct: 7
- Wrong: 3

**Calculation:**
- Score: 7 × 10 = 70 points
- Percentage: 7/10 × 100 = 70%
- Level: Good 👏
- Stars: ⭐⭐⭐⭐
- Message: "Great job! Good performance!"

---

## 🔐 Status Codes

| Code | Meaning |
|------|---------|
| 201 | Score submitted successfully |
| 200 | Data retrieved successfully |
| 400 | Missing or invalid fields |
| 404 | Data not found |
| 500 | Server error |

---

## 📱 JavaScript Example

```javascript
async function submitGameScore(gameData) {
  const response = await fetch('http://localhost:5000/api/scoring/submit', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(gameData)
  });
  
  const result = await response.json();
  
  if (result.status === 'success') {
    // Show visual feedback
    console.log(result.visual_feedback.emoji);
    console.log(result.visual_feedback.stars);
    console.log(result.visual_feedback.message);
  }
}
```

---

## 📚 For More Information

See **SCORING_API_DOCUMENTATION.md** for:
- Complete endpoint documentation
- Detailed request/response examples
- Error handling
- Database schema
- Integration samples

---

## ✨ What You Get

✅ Real-time scoring  
✅ Instant visual feedback  
✅ Performance tracking  
✅ Leaderboards  
✅ Skill mastery tracking  
✅ Complete analytics  

---

**Last Updated:** October 9, 2025
