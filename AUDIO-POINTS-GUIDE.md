# Audio & Points Tracking Guide

## Overview
This guide explains the audio effects and points tracking system used in MyClassboard Games.

---

## 🔊 Audio System

### Files
- **audio-generator.js** - Core audio generation module using Web Audio API

### Audio Effects

#### 1. Correct Answer Sound (Claps)
- **Frequencies**: 800Hz, 900Hz, 1000Hz
- **Duration**: 3 claps, each lasting ~120ms
- **Timing**: Claps play at 250ms intervals
- **Code**: `audioGenerator.playCorrectSound()`

**What you'll hear**: Three distinct ascending "clap" tones that increase in pitch.

#### 2. Wrong Answer Sound (Buzzer)
- **Frequencies**: 400Hz → 250Hz → 400Hz (sweep pattern)
- **Duration**: 350ms total
- **Pattern**: Drops from 400Hz to 250Hz at 150ms, then returns to 400Hz
- **Code**: `audioGenerator.playWrongSound()`

**What you'll hear**: A "wrong answer" buzzer that sweeps down and back up.

#### 3. Celebration Sound (Bonus)
- **Frequencies**: C5(523Hz), E5(659Hz), G5(784Hz), C6(1047Hz), E6(1319Hz)
- **Pattern**: Ascending musical notes
- **Code**: `audioGenerator.playCelebrationSound()`

**What you'll hear**: A cheerful ascending musical scale.

### Implementation Example
```javascript
// In any game file that includes audio-generator.js:
audioGenerator.playCorrectSound();   // Play claps
audioGenerator.playWrongSound();     // Play buzzer
audioGenerator.playCelebrationSound(); // Play celebration
```

---

## 📊 Points Tracking System

### Files
- **points-tracker.js** - Real-time student points and progress display

### Features

#### 1. Real-Time Tracking Widget
The points tracker appears in the top-right corner of the game showing:
- **Total Points**: Cumulative score (10 per correct answer)
- **Correct Answers**: Count of correct responses (green)
- **Wrong Answers**: Count of incorrect responses (red)
- **Progress Bar**: Visual representation of questions answered (5/5)

#### 2. Visual Display
```
┌─────────────────────────────────┐
│  📊 STUDENT PROGRESS            │
├─────────────────────────────────┤
│ Total Points:        50          │
│ Correct Answers:      5    ✓     │
│ Wrong Answers:        0    ✗     │
│ Progress:           5 / 5        │
├─────────────────────────────────┤
│ ████████████████████ 100%        │
└─────────────────────────────────┘
```

#### 3. Score Calculation
- **Correct Answer**: +10 points
- **Wrong Answer**: 0 points
- **Maximum Score**: 50 points (5 questions × 10 points)

### Implementation Example
```javascript
// In game initialization:
pointsTracker.createTracker();     // Create and display widget
pointsTracker.reset();             // Reset to 0 points

// When student answers:
if (answerCorrect) {
    pointsTracker.addCorrectPoints(); // Adds 10 points
    audioGenerator.playCorrectSound();
} else {
    pointsTracker.addWrongAnswer();   // Adds wrong count
    audioGenerator.playWrongSound();
}

// Get final score:
const finalScore = pointsTracker.getFinalScore();
```

---

## 🎮 Games Using Audio & Points

### Simple Addition (simple-addition.html)
- ✅ Audio effects enabled
- ✅ Points tracker enabled
- 5 addition problems, 50 points max

### Fraction Parts (fraction-parts.html)
- ✅ Audio effects enabled
- ✅ Points tracker enabled
- 5 fraction questions, 50 points max

### Other Games
To add audio and points to other games:

1. **Add script includes** to game HTML `<head>`:
```html
<script src="audio-generator.js"></script>
<script src="points-tracker.js"></script>
```

2. **Initialize tracker** in game start function:
```javascript
pointsTracker.createTracker();
pointsTracker.reset();
```

3. **Call audio** on answer check:
```javascript
if (correct) {
    pointsTracker.addCorrectPoints();
    audioGenerator.playCorrectSound();
} else {
    pointsTracker.addWrongAnswer();
    audioGenerator.playWrongSound();
}
```

4. **Get final score** at end:
```javascript
const score = pointsTracker.getFinalScore();
```

---

## 🔧 Browser Compatibility

### Web Audio API Support
- ✅ Chrome/Chromium 14+
- ✅ Firefox 25+
- ✅ Safari 6+
- ✅ Edge 12+
- ✅ Opera 15+

### Audio Context Initialization
The system uses:
```javascript
new (window.AudioContext || window.webkitAudioContext)()
```
This ensures compatibility with both standard and webkit-prefixed browsers.

---

## 🎵 Audio Troubleshooting

### No Sound Playing?
1. **Check browser volume** - System volume must be enabled
2. **Check browser settings** - Allow autoplay of audio
3. **Open browser console** - Look for error messages:
   - Press F12 → Console tab
   - Look for "✅ Correct sound played" or "❌ Wrong sound played" messages

### Console Debugging
When sounds play, you'll see:
- `✅ Correct sound played` - Claps working
- `❌ Wrong sound played` - Buzzer working
- `🎉 Celebration sound played` - Celebration working

---

## 📈 Points Display Lifecycle

### During Game
- Tracker widget always visible in top-right
- Updates in real-time as student answers questions
- Shows current score, correct/wrong counts, progress

### At Game End
- Results screen shows final score: "📊 SCORE: X / 50 points"
- Shows "Correct Answers: X out of 5"
- Emoji feedback based on performance:
  - 🏆 Perfect (50/50 points)
  - 👍 Great (30-40 points)
  - 💪 Keep Practicing (<30 points)

### Data Persistence
- Score saved to localStorage
- Assignment status changed to "completed"
- Teacher can view scores in Student Portal results table

---

## 🎓 Student Data Format

Scores are stored in localStorage as JSON:
```javascript
{
  "student": "John",
  "roll": "001",
  "game": "Simple Addition",
  "skill": "Basic Arithmetic",
  "class": "I",
  "score": 50,
  "status": "completed",
  "date": "2025-10-09"
}
```

---

## 📱 Mobile Support
- Points tracker responsive on all screen sizes
- Audio works on mobile devices (subject to browser permissions)
- Touch-friendly interface for games

---

## Summary

✅ **What's Working**:
- Audio generation via Web Audio API
- Real-time points tracking with visual widget
- Score persistence in localStorage
- Cross-browser audio support
- Mobile-responsive design

✅ **Best Practices**:
- Always initialize tracker before game starts
- Call audio functions immediately on answer check
- Store final score before redirecting to portal
- Use console for debugging audio issues

For questions or issues, check the browser console (F12) for error messages!
