from fastapi import APIRouter, HTTPException, Depends
from models.attendance import AttendanceCreate, AttendanceInDB
from utils.auth_utils import get_current_user
from db.connection import get_database
from datetime import datetime

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/update")
async def update_attendance(data: AttendanceCreate, user: dict = Depends(get_current_user)):
    db = get_database()
    student_id = user["user_id"]
    
    filter_q = {"student_id": student_id, "subject_code": data.subject_code}
    update_doc = {
        "$set": {
            "attendance_pct": data.attendance_pct,
            "internal_marks": data.internal_marks,
            "last_updated": datetime.utcnow()
        },
        "$setOnInsert": {
            "student_id": student_id,
            "subject_code": data.subject_code
        }
    }
    await db.attendance.update_one(filter_q, update_doc, upsert=True)
    return {"message": "Attendance updated"}

@router.get("/")
async def get_attendance(user: dict = Depends(get_current_user)):
    db = get_database()
    records = await db.attendance.find({"student_id": user["user_id"]}).to_list(length=100)
    
    formatted = []
    for r in records:
        formatted.append({
            "subject_code": r["subject_code"],
            "attendance_pct": r["attendance_pct"],
            "internal_marks": r.get("internal_marks"),
            "last_updated": r["last_updated"].isoformat()
        })
    return {"attendance": formatted}
