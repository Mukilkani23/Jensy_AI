from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class StudyPlanCreate(BaseModel):
    exam_date: datetime
    subjects: List[str]  # Subject codes

class StudyEvent(BaseModel):
    title: str
    start: datetime
    end: datetime
    subject_code: str
    unit: int
    color: str = "blue"

class StudyPlanInDB(BaseModel):
    student_id: str
    exam_date: datetime
    events: List[StudyEvent]
    created_at: datetime = Field(default_factory=datetime.utcnow)
