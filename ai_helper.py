"""
AI Helper for EduGame Studio & MyClassboard Games.
Generates multi-question game packs with options for ALL game types,
and includes audio scripts for Listening activities (read by the Listening Agent).
"""

import os
import json
import requests

DEFAULT_FREE_API_KEY = os.environ.get("GEMINI_API_KEY", "")

def generate_ai_game_content(class_name, subject, sub_skill, activity_name, game_type, api_key=None):
    """
    Generates dynamic game content with options and audio scripts for Listening activities.
    """
    key_to_use = api_key.strip() if api_key and api_key.strip() else DEFAULT_FREE_API_KEY
    
    if key_to_use:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key_to_use}"
            headers = {"Content-Type": "application/json"}
            
            prompt = f"""You are an expert curriculum game designer. Create a 3-question interactive game pack for:
Class: {class_name}
Subject: {subject}
Sub-Skill Area: {sub_skill}
Activity Name: {activity_name}
Game Type: {game_type}

Ensure ALL questions provide 4 clear options (Option A, Option B, Option C, Option D).
If skill area is Listening or activity involves Listening, include an "audio_script" field containing the audio announcement/story text to be read by the Text-to-Speech Listening Agent.

Return ONLY valid JSON with no markdown formatting matching this structure:
{{
  "title": "{activity_name}",
  "audio_script": "Full audio script/announcement text to be spoken by Listening Agent (if listening activity)",
  "questions": [
    {{
      "question": "Question 1 text for {class_name}",
      "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
      "answer": "Option A text",
      "explanation": "Clear explanation"
    }},
    {{
      "question": "Question 2 text for {class_name}",
      "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
      "answer": "Option B text",
      "explanation": "Clear explanation"
    }}
  ]
}}
"""
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.7, "responseMimeType": "application/json"}
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=8)
            if response.status_code == 200:
                res_data = response.json()
                text_content = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
                if text_content.startswith("```json"):
                    text_content = text_content[7:]
                if text_content.startswith("```"):
                    text_content = text_content[3:]
                if text_content.endswith("```"):
                    text_content = text_content[:-3]
                parsed = json.loads(text_content.strip())
                return parsed, "✨ Live Gemini AI Generated"
        except Exception:
            pass

    # High quality fallback generator with options and audio scripts
    fallback = generate_smart_fallback(class_name, subject, sub_skill, activity_name, game_type)
    return fallback, "⚡ Built-in Curriculum Engine"


def generate_smart_fallback(class_name, subject, sub_skill, activity_name, game_type):
    """Fallback generator with activity-specific questions for ALL 325 games and audio scripts for Listening activities."""
    try:
        from build_question_bank import generate_activity_questions
        item = {
            "class": class_name,
            "subject": subject,
            "sub_skill_area": sub_skill,
            "activity_name": activity_name,
            "game_type": game_type
        }
        return generate_activity_questions(item)
    except Exception:
        pass

    # Basic fallback
    is_listening = "Listening" in sub_skill or "Listen" in activity_name or "Podcast" in activity_name or "Announcement" in activity_name
    audio_script = f"Attention students of {class_name}! Welcome to {activity_name}. Please pay close attention to the instructions." if is_listening else ""
    return {
        "title": activity_name,
        "audio_script": audio_script,
        "questions": [
            {
                "question": f"[{class_name} {subject} - {activity_name}] Select the correct answer for {sub_skill}:",
                "options": ["Option A: Correct Concept", "Option B: Incorrect Option", "Option C: Distractor", "Option D: None"],
                "answer": "Option A: Correct Concept",
                "explanation": f"Focuses on core skills of {sub_skill}."
            }
        ]
    }
