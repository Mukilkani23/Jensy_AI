from fastapi import APIRouter, Depends
from utils.auth_utils import get_current_user
from db.connection import get_database
from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/")
async def get_analytics(user: dict = Depends(get_current_user)):
    db = get_database()
    student_id = user["user_id"]
    
    # Subjects completed per month
    progress = await db.student_progress.find({"student_id": student_id, "completion_pct": {"$gte": 100}}).to_list(length=100)
    subjects_by_month = {}
    for p in progress:
        # mock date if missing
        date_obj = p.get("last_updated", datetime.utcnow())
        month = date_obj.strftime("%Y-%m")
        subjects_by_month[month] = subjects_by_month.get(month, 0) + 1
        
    subjects_data = [{"month": k, "completed": v} for k, v in sorted(subjects_by_month.items())]
    if not subjects_data:
        subjects_data = [{"month": datetime.utcnow().strftime("%Y-%m"), "completed": 0}]
        
    # Chat frequency
    conversation = await db.conversations.find_one({"student_id": student_id})
    chat_frequency = {}
    if conversation and "messages" in conversation:
        for msg in conversation["messages"]:
            if msg["role"] == "user":
                date_str = msg.get("timestamp", datetime.utcnow().isoformat())[:10]
                chat_frequency[date_str] = chat_frequency.get(date_str, 0) + 1
                
    chat_data = [{"date": k, "messages": v} for k, v in sorted(chat_frequency.items())]
    if not chat_data:
        chat_data = [{"date": datetime.utcnow().strftime("%Y-%m-%d"), "messages": 0}]
        
    # XP over time (Simulated based on streak/current XP for now)
    student = await db.students.find_one({"_id": user["_id"]}) if "_id" in user else None # placeholder
    if not student:
        student = await db.students.find_one({"email": user.get("email")})
        
    xp_data = []
    if student and "xp_system" in student:
        total_xp = student["xp_system"].get("total_xp", 0)
        # simulate past 5 days
        for i in range(4, -1, -1):
            date_str = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
            xp_data.append({"date": date_str, "xp": max(0, total_xp - (i * 50))})
    else:
        xp_data = [{"date": datetime.utcnow().strftime("%Y-%m-%d"), "xp": 0}]

    return {
        "subjects": subjects_data,
        "chats": chat_data,
        "xp": xp_data
    }
