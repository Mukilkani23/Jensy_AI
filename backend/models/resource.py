from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ResourceCreate(BaseModel):
    subject_code: str
    semester: int
    type: str = "note"  # "note" | "video" | "pyq"
    title: str
    url: str
    uploaded_by: Optional[str] = None


class ResourceInDB(BaseModel):
    subject_code: str
    semester: int
    type: str
    title: str
    url: str
    uploaded_by: Optional[str] = None
    upvotes: int = 0
    downvotes: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)



class ResourceResponse(BaseModel):
    id: str
    subject_code: str
    semester: int
    type: str
    title: str
    url: str
    uploaded_by: Optional[str] = None
    upvotes: int = 0
    downvotes: int = 0
    created_at: datetime



