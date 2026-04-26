from datetime import datetime
from bson import ObjectId


async def generate_behavior_report(student_id: str, db) -> dict:
    """Generate a behavior/performance report for a student."""
    
    # Get progress data
    progress_records = await db.student_progress.find(
        {"student_id": student_id}
    ).to_list(length=500)

    # Get conversation data
    conversation = await db.ai_conversations.find_one({"student_id": student_id})
    intent_log = conversation.get("intent_log", []) if conversation else []

    # Analyze progress
    subject_scores = {}
    total_time = 0
    for p in progress_records:
        code = p["subject_code"]
        completion = p.get("completion_pct", 0)
        time_spent = p.get("time_spent_mins", 0)
        subject_scores[code] = completion
        total_time += time_spent

    # Determine strong/weak subjects
    sorted_subjects = sorted(subject_scores.items(), key=lambda x: x[1], reverse=True)
    strong = [s[0] for s in sorted_subjects[:3] if s[1] >= 50]
    weak = [s[0] for s in sorted_subjects[-3:] if s[1] < 50]

    # Analyze study patterns from intents
    study_count = intent_log.count("STUDY_HELP")
    schedule_count = intent_log.count("SCHEDULE")
    resource_count = intent_log.count("RESOURCE_REQUEST")

    if study_count > schedule_count and study_count > resource_count:
        study_pattern = "concept-focused"
    elif resource_count > study_count:
        study_pattern = "resource-seeking"
    elif schedule_count > study_count:
        study_pattern = "schedule-oriented"
    else:
        study_pattern = "balanced"

    # Generate recommendations
    recommendations = []
    if weak:
        recommendations.append(f"Focus more on: {', '.join(weak)}")
    if total_time < 60:
        recommendations.append("Try to study at least 1 hour daily")
    if study_pattern == "resource-seeking":
        recommendations.append("You collect many resources — try to spend more time studying them")
    if not progress_records:
        recommendations.append("Start tracking your progress to get personalized insights")

    report = {
        "student_id": student_id,
        "strong_subjects": strong,
        "weak_subjects": weak,
        "total_study_time_mins": total_time,
        "study_pattern": study_pattern,
        "recommended_actions": recommendations,
        "intent_distribution": {
            "study_help": study_count,
            "schedule": schedule_count,
            "resource_request": resource_count,
            "total_conversations": len(intent_log)
        },
        "generated_at": datetime.utcnow().isoformat()
    }

    # Update student behavior profile
    await db.students.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": {
            "behavior_profile": {
                "strong_subjects": strong,
                "weak_subjects": weak,
                "avg_daily_time_mins": round(total_time / max(len(progress_records), 1), 1),
                "last_analyzed": datetime.utcnow()
            }
        }}
    )

    return report
