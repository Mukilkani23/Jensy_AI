from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from models.student import StudentProfile, OnboardingSetup
from utils.auth_utils import get_current_user
from db.connection import get_database

router = APIRouter(prefix="/student", tags=["Student"])


@router.get("/{student_id}", response_model=StudentProfile)
async def get_student(student_id: str, user: dict = Depends(get_current_user)):
    db = get_database()
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return StudentProfile(
        id=str(student["_id"]),
        name=student["name"],
        email=student["email"],
        degree=student.get("degree"),
        branch=student.get("branch"),
        college_type=student.get("college_type"),
        college_url=student.get("college_url"),
        regulation=student.get("regulation"),
        preference=student.get("preference"),
        semester_current=student.get("semester_current", 1),
        behavior_profile=student.get("behavior_profile", {})
    )


@router.patch("/update")
async def update_student(student_id: str, updates: dict, user: dict = Depends(get_current_user)):
    db = get_database()
    result = await db.students.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": updates}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found or no changes")
    return {"message": "Student updated successfully"}

from datetime import datetime

@router.get("/me/notifications")
async def get_notifications(user: dict = Depends(get_current_user)):
    db = get_database()
    notifs = await db.notifications.find({"student_id": user["user_id"]}).sort("created_at", -1).to_list(length=20)
    
    formatted = []
    for n in notifs:
        formatted.append({
            "id": str(n["_id"]),
            "message": n["message"],
            "read": n.get("read", False),
            "created_at": n.get("created_at", datetime.utcnow()).isoformat()
        })
    return {"notifications": formatted}

