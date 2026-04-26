import os
import json
import re
from openai import AsyncOpenAI
from dotenv import load_dotenv

import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

INTENT_KEYWORDS = {
    "STUDY_HELP": ["help", "explain", "understand", "what is", "how to", "teach"],
    "SCHEDULE": ["schedule", "plan", "time", "when", "calendar", "deadline"],
    "RESOURCE_REQUEST": ["resource", "notes", "book", "pdf", "video", "material", "pyq"],
    "PROGRESS_CHECK": ["progress", "completed", "score", "marks", "grade", "done", "status"]
}

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))


from typing import Tuple

async def get_ai_response(message: str, student: dict, conversation_history: list, analysis: dict, extra_context: str = "") -> Tuple[str, int]:


    preference = student.get("preference", "balanced")
    degree = student.get("degree", "Unknown")
    branch = student.get("branch", "")
    semester = student.get("semester_current", 1)
    behavior = student.get("behavior_profile", {})

    tone_instruction = ""
    if preference == "coding":
        tone_instruction = "You are talking to a coding-focused student. Give technical, code-oriented answers with examples. Include code snippets when relevant."
    elif preference == "noncoding":
        tone_instruction = "You are talking to a non-coding student. Give conceptual, theory-focused explanations. Avoid code unless asked."
    else:
        tone_instruction = "Give a balanced mix of conceptual explanations and practical examples."

    system_prompt = f"""You are GENZ AI — a smart, friendly academic assistant for bachelor's degree students.

Student Profile:
- Degree: {degree} {branch}
- Current Semester: {semester}
- Preference: {preference}
- Strong subjects: {behavior.get('strong_subjects', [])}
- Weak subjects: {behavior.get('weak_subjects', [])}
- Learning Pace: {behavior.get('learning_pace', 'medium')}
- Preferred Format: {behavior.get('preferred_format', 'mixed')}
- Stress Level: {behavior.get('stress_level', 'low')}
- Goal Orientation: {behavior.get('goal_orientation', 'knowledge')}

{tone_instruction}

Detected intent: {analysis.get('intent', 'GENERAL')}
Detected entities: {json.dumps(analysis.get('entities', []))}

{extra_context}

Guidelines:

- Adapt your explanation speed to their Learning Pace ({behavior.get('learning_pace', 'medium')}).
- Provide {behavior.get('preferred_format', 'mixed')} resources when possible.
- If Stress Level is high, be extra encouraging, calm, and break things into small steps.
- Align advice with their Goal Orientation ({behavior.get('goal_orientation', 'knowledge')}).
- Be concise but helpful
- If the student asks about a specific subject, provide semester-relevant guidance
- For STUDY_HELP: give clear explanations and study tips
- For SCHEDULE: help plan study schedules
- For RESOURCE_REQUEST: suggest relevant resources
- For PROGRESS_CHECK: analyze and motivate
- Always be encouraging and supportive"""


    messages = [{"role": "system", "content": system_prompt}]

    for msg in conversation_history[-10:]:
        messages.append({
            "role": msg.get("role", "user"),
            "content": msg.get("content", "")
        })

    messages.append({"role": "user", "content": message})

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content, response.usage.total_tokens
    except Exception as e:
        return f"I'm having trouble connecting to my AI brain right now. Error: {str(e)}", 0



async def analyze_message(message: str, student: dict) -> dict:
    """Use spaCy to extract intent and entities from student message."""
    try:
        doc = nlp(message)
        
        entities = []
        for ent in doc.ents:
            ent_type = "unknown"
            if ent.label_ in ["EVENT", "DATE", "TIME"]:
                ent_type = "deadline" if "due" in message.lower() or "deadline" in message.lower() else "exam"
            elif ent.label_ in ["ORG", "PRODUCT", "WORK_OF_ART", "PERSON"]:
                ent_type = "subject"
            
            if ent_type != "unknown":
                entities.append({"type": ent_type, "value": ent.text})
                
        # Additional custom regex for semesters
        sem_match = re.search(r'(sem|semester)\s*(\d)', message.lower())
        if sem_match:
            entities.append({"type": "semester", "value": sem_match.group(2)})
            
        # Rule-based Intent classification
        msg_lower = message.lower()
        detected_intent = "GENERAL"
        max_matches = 0
        
        for intent, keywords in INTENT_KEYWORDS.items():
            matches = sum(1 for kw in keywords if kw in msg_lower)
            if matches > max_matches:
                max_matches = matches
                detected_intent = intent
                
        # Extract behavioral cues
        stress_cues = ["stressed", "anxious", "worried", "panic", "hard", "difficult", "overwhelmed", "failing", "scared"]
        fast_cues = ["quick", "fast", "summary", "tldr", "short", "brief"]
        video_cues = ["video", "watch", "youtube", "visual"]
        grade_cues = ["marks", "grade", "gpa", "cgpa", "score", "pass"]
        
        cues = {
            "stress": any(w in msg_lower for w in stress_cues),
            "fast_pace": any(w in msg_lower for w in fast_cues),
            "video_format": any(w in msg_lower for w in video_cues),
            "grades_focus": any(w in msg_lower for w in grade_cues),
        }
                
        return {
            "intent": detected_intent,
            "entities": entities,
            "confidence": 0.8 if max_matches > 0 else 0.5,
            "cues": cues
        }

    except Exception as e:
        print(f"Error in analyze_message: {e}")
        return {"intent": "GENERAL", "entities": [], "confidence": 0.5}
