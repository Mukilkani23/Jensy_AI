from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProgressUpdate(BaseModel):
    student_id: str
    semester: int
    subject_code: str
    completion_pct: float = 0
    time_spent_mins: float = 0


class ProgressInDB(BaseModel):
    student_id: str
    semester: int
    subject_code: str
    completion_pct: float = 0
    time_spent_mins: float = 0
    last_accessed: datetime = Field(default_factory=datetime.utcnow)


class ProgressResponse(BaseModel):
    id: str
    student_id: str
    semester: int
    subject_code: str
    completion_pct: float
    time_spent_mins: float
    last_accessed: datetime
