from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from models.progress import ProgressUpdate, ProgressInDB
from utils.auth_utils import get_current_user
from db.connection import get_database
from datetime import datetime
from services.gamification import award_xp


router = APIRouter(tags=["Progress & Dashboard"])


@router.get("/dashboard/{student_id}")
async def get_dashboard(student_id: str, user: dict = Depends(get_current_user)):
    db = get_database()
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    degree = student.get("degree", "")
    regulation = student.get("regulation", "")
    preference = student.get("preference", "balanced")

    # Get curriculum
    curricula = await db.curriculum.find(
        {"degree": degree, "regulation": regulation}
    ).sort("semester", 1).to_list(length=100)

    # Get progress
    progress_records = await db.student_progress.find(
        {"student_id": student_id}
    ).to_list(length=500)

    progress_map = {}
    for p in progress_records:
        key = f"{p['semester']}_{p['subject_code']}"
        progress_map[key] = {
            "completion_pct": p.get("completion_pct", 0),
            "time_spent_mins": p.get("time_spent_mins", 0),
            "last_accessed": p.get("last_accessed", "").isoformat() if p.get("last_accessed") else None
        }

    # Build semester blocks
    semesters = []
    for c in curricula:
        sem = c["semester"]
        subjects_with_progress = []
        for subj in c.get("subjects", []):
            key = f"{sem}_{subj['code']}"
            prog = progress_map.get(key, {"completion_pct": 0, "time_spent_mins": 0, "last_accessed": None})
            subjects_with_progress.append({
                **subj,
                "progress": prog
            })
        semesters.append({
            "semester": sem,
            "subjects": subjects_with_progress,
        })

    # Stats
    total_subjects = sum(len(s["subjects"]) for s in semesters)
    completed = sum(
        1 for s in semesters
        for subj in s["subjects"]
        if subj["progress"]["completion_pct"] >= 100
    )

    return {
        "student_name": student["name"],
        "degree": degree,
        "regulation": regulation,
        "preference": preference,
        "semester_current": student.get("semester_current", 1),
        "semesters": semesters,
        "stats": {
            "total_subjects": total_subjects,
            "completed_subjects": completed,
            "overall_completion": round((completed / total_subjects * 100) if total_subjects > 0 else 0, 1)
        },
        "xp_system": student.get("xp_system", {"total_xp": 0, "streak": 0, "badges": []})
    }



@router.patch("/progress/update")
async def update_progress(data: ProgressUpdate, user: dict = Depends(get_current_user)):
    db = get_database()
    filter_q = {
        "student_id": data.student_id,
        "semester": data.semester,
        "subject_code": data.subject_code
    }
    update_doc = {
        "$set": {
            "completion_pct": data.completion_pct,
            "time_spent_mins": data.time_spent_mins,
            "last_accessed": datetime.utcnow()
        },
        "$setOnInsert": {
            "student_id": data.student_id,
            "semester": data.semester,
            "subject_code": data.subject_code
        }
    }
    existing_progress = await db.student_progress.find_one(filter_q)
    is_newly_completed = False
    
    if data.completion_pct >= 100 and (not existing_progress or existing_progress.get("completion_pct", 0) < 100):
        is_newly_completed = True

    await db.student_progress.update_one(filter_q, update_doc, upsert=True)
    
    if is_newly_completed:
        await award_xp(db, data.student_id, 50, "subject_complete")
        
    return {"message": "Progress updated"}

