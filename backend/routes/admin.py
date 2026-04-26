from fastapi import APIRouter, HTTPException, Depends
from utils.auth_utils import RoleChecker
from db.connection import get_database

router = APIRouter(prefix="/admin", tags=["Admin"])
require_admin_staff = RoleChecker(["admin", "staff"])

@router.get("/dashboard", dependencies=[Depends(require_admin_staff)])
async def get_admin_dashboard():
    db = get_database()
    
    # Aggregate student progress
    total_students = await db.students.count_documents({})
    
    pipeline = [
        {"$group": {
            "_id": "$semester",
            "avg_completion": {"$avg": "$completion_pct"},
            "total_records": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    progress_stats = await db.student_progress.aggregate(pipeline).to_list(length=100)
    
    formatted_progress = []
    for stat in progress_stats:
        formatted_progress.append({
            "semester": stat["_id"],
            "avg_completion": round(stat.get("avg_completion", 0), 1),
            "total_records": stat["total_records"]
        })
        
    return {
        "total_students": total_students,
        "progress_by_semester": formatted_progress,
        "pending_resources": 0 # placeholder as we don't have approval logic yet
    }
