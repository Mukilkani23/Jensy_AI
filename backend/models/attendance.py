from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AttendanceCreate(BaseModel):
    subject_code: str
    attendance_pct: float
    internal_marks: Optional[float] = None

class AttendanceInDB(BaseModel):
    student_id: str
    subject_code: str
    attendance_pct: float
    internal_marks: Optional[float] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)
