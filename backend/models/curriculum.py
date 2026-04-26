from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Subject(BaseModel):
    sub_code : int = 5
    code: str
    name: str
    type: str = "theory"  # "theory" | "lab"
    credits: int = 3


class CurriculumCreate(BaseModel):
    degree: str
    regulation: str
    college_id: Optional[str] = None
    semester: int
    subjects: list[Subject]


class CurriculumInDB(BaseModel):
    degree: str
    regulation: str
    college_id: Optional[str] = None
    semester: int
    subjects: list[Subject]
    auto_updated_at: datetime = Field(default_factory=datetime.utcnow)


class CurriculumResponse(BaseModel):
    id: str
    degree: str
    regulation: str
    semester: int
    subjects: list[Subject]
