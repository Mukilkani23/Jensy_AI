from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from models.resource import ResourceCreate, ResourceInDB
from utils.auth_utils import get_current_user
from db.connection import get_database
from datetime import datetime
from services.gamification import award_xp
from services.rag import extract_and_store_pdf, ask_rag



router = APIRouter(prefix="/resources", tags=["Resources"])


@router.get("/{subject_code}")
async def get_resources(subject_code: str, user: dict = Depends(get_current_user)):
    db = get_database()
    resources = await db.resources.find({"subject_code": subject_code}).to_list(length=200)
    
    # Sort by score (upvotes - downvotes)
    resources.sort(key=lambda r: r.get("upvotes", 0) - r.get("downvotes", 0), reverse=True)
    
    result = []

    for r in resources:
        result.append({
            "id": str(r["_id"]),
            "subject_code": r["subject_code"],
            "semester": r.get("semester", 0),
            "type": r.get("type", "note"),
            "title": r["title"],
            "url": r["url"],
            "uploaded_by": r.get("uploaded_by"),
            "upvotes": r.get("upvotes", 0),
            "downvotes": r.get("downvotes", 0),
            "created_at": r.get("created_at", datetime.utcnow()).isoformat()
        })

    return {"resources": result}


@router.post("/upload")
async def upload_resource(resource: ResourceCreate, user: dict = Depends(get_current_user)):
    db = get_database()
    resource_doc = ResourceInDB(
        subject_code=resource.subject_code,
        semester=resource.semester,
        type=resource.type,
        title=resource.title,
        url=resource.url,
        uploaded_by=user["user_id"],
        created_at=datetime.utcnow()
    )
    result = await db.resources.insert_one(resource_doc.model_dump())
    
    # Award XP for upload
    await award_xp(db, user["user_id"], 30, "resource_upload")
    
    return {

        "message": "Resource uploaded successfully",
        "resource_id": str(result.inserted_id)
    }

@router.post("/upload_file")
async def upload_resource_file(
    subject_code: str = Form(...),
    semester: int = Form(...),
    title: str = Form(...),
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
    db = get_database()
    
    resource_doc = ResourceInDB(
        subject_code=subject_code,
        semester=semester,
        type="pdf",
        title=title,
        url=f"/local_storage/{file.filename}",  # placeholder url
        uploaded_by=user["user_id"],
        created_at=datetime.utcnow()
    )
    result = await db.resources.insert_one(resource_doc.model_dump())
    
    # Process PDF for RAG
    file_bytes = await file.read()
    metadata = {
        "subject_code": subject_code,
        "title": title,
        "uploader": user["user_id"]
    }
    
    await extract_and_store_pdf(file_bytes, str(result.inserted_id), metadata)
    await award_xp(db, user["user_id"], 30, "resource_upload")
    
    return {
        "message": "PDF uploaded and processed for AI search",
        "resource_id": str(result.inserted_id)
    }

from pydantic import BaseModel
from typing import Optional

class AskRequest(BaseModel):
    question: str
    subject_code: Optional[str] = None

@router.post("/ask")

async def ask_resources(request: AskRequest, user: dict = Depends(get_current_user)):
    answer = await ask_rag(request.question, request.subject_code)
    return {"answer": answer}

class VoteRequest(BaseModel):
    vote: int  # 1 for upvote, -1 for downvote

from bson import ObjectId

@router.post("/{resource_id}/vote")
async def vote_resource(resource_id: str, request: VoteRequest, user: dict = Depends(get_current_user)):
    db = get_database()
    resource = await db.resources.find_one({"_id": ObjectId(resource_id)})
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
        
    if request.vote == 1:
        await db.resources.update_one({"_id": ObjectId(resource_id)}, {"$inc": {"upvotes": 1}})
    elif request.vote == -1:
        await db.resources.update_one({"_id": ObjectId(resource_id)}, {"$inc": {"downvotes": 1}})
        
    return {"message": "Vote recorded"}
