from fastapi import APIRouter, HTTPException, Depends
from utils.auth_utils import get_current_user
from db.connection import get_database
from bson import ObjectId
from openai import AsyncOpenAI
import os

router = APIRouter(prefix="/career", tags=["Career"])
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

@router.get("/generate")
async def generate_career_materials(user: dict = Depends(get_current_user)):
    db = get_database()
    student_id = user["user_id"]
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    # Get completed subjects
    progress_records = await db.student_progress.find(
        {"student_id": student_id, "completion_pct": {"$gte": 100}}
    ).to_list(length=100)
    
    completed_subjects = [p["subject_code"] for p in progress_records]
    
    prompt = f"""Generate a markdown resume and 10 mock interview Q&As for an engineering student.
    
Student Details:
- Name: {student.get('name', 'Student')}
- Degree: {student.get('degree', '')}
- Branch: {student.get('branch', '')}
- Track Preference: {student.get('preference', 'balanced')}
- Completed Subjects: {', '.join(completed_subjects) if completed_subjects else 'General Engineering'}

Format the output EXACTLY like this:
# RESUME
[Markdown Resume content here]

---
# MOCK_INTERVIEW
[10 Q&A pairs here]
"""

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000
    )
    
    content = response.choices[0].message.content
    parts = content.split("---")
    resume = parts[0].replace("# RESUME\n", "").strip() if len(parts) > 0 else "Could not generate resume."
    interview = parts[1].replace("# MOCK_INTERVIEW\n", "").strip() if len(parts) > 1 else "Could not generate interview."
    
    return {
        "resume": resume,
        "interview": interview
    }
