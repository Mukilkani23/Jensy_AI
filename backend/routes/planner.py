from fastapi import APIRouter, HTTPException, Depends
from models.planner import StudyPlanCreate, StudyPlanInDB, StudyEvent
from utils.auth_utils import get_current_user
from db.connection import get_database
from datetime import datetime, timedelta
from bson import ObjectId

router = APIRouter(prefix="/planner", tags=["Planner"])

@router.post("/generate")
async def generate_plan(request: StudyPlanCreate, user: dict = Depends(get_current_user)):
    db = get_database()
    student_id = user["user_id"]
    
    now = datetime.utcnow()
    exam_date = request.exam_date.replace(tzinfo=None)
    
    if exam_date <= now:
        raise HTTPException(status_code=400, detail="Exam date must be in the future")
        
    days_until_exam = (exam_date - now).days
    if days_until_exam < len(request.subjects):
        raise HTTPException(status_code=400, detail="Not enough time to study all subjects")
        
    events = []
    current_date = now + timedelta(days=1)
    
    colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]
    
    # Simple distribution: 5 units per subject
    total_tasks = len(request.subjects) * 5
    days_per_task = max(1, days_until_exam // total_tasks)
    
    for i, subject in enumerate(request.subjects):
        color = colors[i % len(colors)]
        for unit in range(1, 6):
            # Schedule 2 hours for each unit
            start_time = current_date.replace(hour=18, minute=0, second=0, microsecond=0)
            end_time = start_time + timedelta(hours=2)
            
            events.append(StudyEvent(
                title=f"{subject} - Unit {unit}",
                start=start_time,
                end=end_time,
                subject_code=subject,
                unit=unit,
                color=color
            ))
            current_date += timedelta(days=days_per_task)
            
    plan_doc = StudyPlanInDB(
        student_id=student_id,
        exam_date=exam_date,
        events=events
    )
    
    await db.study_plans.delete_many({"student_id": student_id})  # Replace old plan
    result = await db.study_plans.insert_one(plan_doc.model_dump())
    
    return {"message": "Plan generated", "id": str(result.inserted_id), "events": events}

@router.get("/")
async def get_plan(user: dict = Depends(get_current_user)):
    db = get_database()
    plan = await db.study_plans.find_one({"student_id": user["user_id"]})
    if not plan:
        return {"events": []}
    return {"events": plan.get("events", []), "exam_date": plan.get("exam_date")}
