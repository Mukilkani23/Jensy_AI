from fastapi import APIRouter, HTTPException, Depends, Request
from bson import ObjectId

from bson.errors import InvalidId
from models.ai_models import ChatRequest, AnalyzeRequest, AnalyzeResponse
from utils.auth_utils import get_current_user
from db.connection import get_database
from services.ai_engine import get_ai_response, analyze_message
from services.behavior import generate_behavior_report
from services.gamification import award_xp
from utils.rate_limit import limiter
from datetime import datetime


router = APIRouter(prefix="/ai", tags=["Assistant"])


@router.post("/chat")
@limiter.limit("20/hour")
async def ai_chat(request_obj: Request, request: ChatRequest, user: dict = Depends(get_current_user)):
    db = get_database()

    student_id = request.student_id

    # Get student context
    try:
        student = await db.students.find_one({"_id": ObjectId(student_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid student ID format")
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Get or create conversation
    conversation = await db.ai_conversations.find_one({"student_id": student_id})
    if not conversation:
        conversation = {
            "student_id": student_id,
            "messages": [],
            "intent_log": [],
            "ner_entities": []
        }
        await db.ai_conversations.insert_one(conversation)
        conversation = await db.ai_conversations.find_one({"student_id": student_id})

    # Add user message
    user_msg = {"role": "user", "content": request.message, "timestamp": datetime.utcnow().isoformat()}

    # Analyze intent/entities
    analysis = await analyze_message(request.message, student)
    
    # Check attendance

    low_attendance = await db.attendance.find({
        "student_id": student_id,
        "attendance_pct": {"$lt": 75.0}
    }).to_list(length=10)
    
    attendance_warning = ""
    if low_attendance:
        subjects = [r["subject_code"] for r in low_attendance]
        attendance_warning = f"The student has low attendance (< 75%) in the following subjects: {', '.join(subjects)}. Warn them about this if they ask about progress or scheduling."

    # Get AI response
    ai_response, tokens_used = await get_ai_response(
        message=request.message,
        student=student,
        conversation_history=conversation.get("messages", [])[-20:],
        analysis=analysis,
        extra_context=attendance_warning
    )



    assistant_msg = {"role": "assistant", "content": ai_response, "timestamp": datetime.utcnow().isoformat()}

    # Update conversation in DB
    await db.ai_conversations.update_one(
        {"student_id": student_id},
        {
            "$push": {
                "messages": {"$each": [user_msg, assistant_msg]},
                "intent_log": analysis.get("intent", "GENERAL"),
                "ner_entities": {"$each": analysis.get("entities", [])}
            }
        }
    )
    
    cues = analysis.get("cues", {})
    profile_updates = {}
    if cues.get("stress"):
        profile_updates["behavior_profile.stress_level"] = "high"
    if cues.get("fast_pace"):
        profile_updates["behavior_profile.learning_pace"] = "fast"
    if cues.get("video_format"):
        profile_updates["behavior_profile.preferred_format"] = "video"
    if cues.get("grades_focus"):
        profile_updates["behavior_profile.goal_orientation"] = "grades"
        
    # Update Token Usage
    token_usage = student.get("token_usage", {"daily_tokens": 0, "total_tokens": 0, "last_reset_date": None})
    now = datetime.utcnow()
    last_reset = token_usage.get("last_reset_date")
    
    if isinstance(last_reset, str):
        try:
            last_reset = datetime.fromisoformat(last_reset)
        except:
            last_reset = None
            
    if last_reset and (now.date() - last_reset.date()).days >= 1:
        token_usage["daily_tokens"] = 0
        
    token_usage["daily_tokens"] += tokens_used
    token_usage["total_tokens"] += tokens_used
    token_usage["last_reset_date"] = now

    if profile_updates:
        profile_updates["token_usage"] = token_usage
        await db.students.update_one(
            {"_id": ObjectId(student_id)},
            {"$set": profile_updates}
        )
    else:
        await db.students.update_one(
            {"_id": ObjectId(student_id)},
            {"$set": {"token_usage": token_usage}}
        )

    # Award 10 XP for using AI chat
    await award_xp(db, student_id, 10, "ai_chat")

    return {
        "response": ai_response,
        "intent": analysis.get("intent", "GENERAL"),
        "entities": analysis.get("entities", []),
        "tokens_used": tokens_used,
        "daily_tokens": token_usage["daily_tokens"]
    }


@router.get("/behavior/{student_id}")
async def get_behavior(student_id: str, user: dict = Depends(get_current_user)):
    db = get_database()
    try:
        student = await db.students.find_one({"_id": ObjectId(student_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid student ID format")
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    report = await generate_behavior_report(student_id, db)
    return report


@router.post("/analyze")
async def analyze_student_message(request: AnalyzeRequest, user: dict = Depends(get_current_user)):
    db = get_database()
    try:
        student = await db.students.find_one({"_id": ObjectId(request.student_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid student ID format")
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    analysis = await analyze_message(request.message, student)
    return AnalyzeResponse(
        intent=analysis.get("intent", "GENERAL"),
        entities=analysis.get("entities", []),
        confidence=analysis.get("confidence", 0.0)
    )


@router.get("/conversations/{student_id}")
async def get_conversations(student_id: str, user: dict = Depends(get_current_user)):
    db = get_database()
    conversation = await db.ai_conversations.find_one({"student_id": student_id})
    if not conversation:
        return {"messages": []}
    
    messages = conversation.get("messages", [])
    return {"messages": messages[-50:]}  # Return last 50 messages
