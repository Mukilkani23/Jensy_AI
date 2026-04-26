from datetime import datetime, timedelta
from bson import ObjectId

async def award_xp(db, student_id: str, amount: int, action: str):
    """Award XP to student and update streak."""
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        return
        
    xp_system = student.get("xp_system", {"total_xp": 0, "streak": 0, "badges": [], "last_streak_date": None})
    
    # Check streak
    now = datetime.utcnow()
    last_date = xp_system.get("last_streak_date")
    
    # If last_date is string, parse it (mongodb might store as datetime though)
    if isinstance(last_date, str):
        try:
            last_date = datetime.fromisoformat(last_date)
        except:
            last_date = None
            
    if last_date:
        delta = now.date() - last_date.date()
        if delta.days == 1:
            xp_system["streak"] += 1
            amount += 20  # Daily streak bonus
        elif delta.days > 1:
            xp_system["streak"] = 1
    else:
        xp_system["streak"] = 1
        
    xp_system["last_streak_date"] = now
    xp_system["total_xp"] += amount
    
    # Check for new badges based on XP or action
    badges = set(xp_system.get("badges", []))
    if xp_system["total_xp"] >= 100:
        badges.add("Bronze Scholar")
    if xp_system["total_xp"] >= 500:
        badges.add("Silver Sage")
    if xp_system["streak"] >= 7:
        badges.add("7-Day Streak")
    if action == "subject_complete":
        badges.add("Subject Master")
        
    xp_system["badges"] = list(badges)
    
    await db.students.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": {"xp_system": xp_system}}
    )
    return xp_system
