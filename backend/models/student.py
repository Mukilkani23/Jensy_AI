from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = "student"


class StudentLogin(BaseModel):
    email: EmailStr
    password: str


class BehaviorProfile(BaseModel):
    strong_subjects: list[str] = []
    weak_subjects: list[str] = []
    avg_daily_time_mins: float = 0
    preferred_study_time: str = "evening"
    learning_pace: str = "medium"
    preferred_format: str = "mixed"
    stress_level: str = "low"
    goal_orientation: str = "knowledge"
    engagement_frequency: str = "regular"
    last_analyzed: Optional[datetime] = None


class XPSystem(BaseModel):
    total_xp: int = 0
    streak: int = 0
    badges: list[str] = []
    last_streak_date: Optional[datetime] = None

class TokenUsage(BaseModel):
    daily_tokens: int = 0
    total_tokens: int = 0
    last_reset_date: Optional[datetime] = None

class StudentInDB(BaseModel):

    name: str
    email: str
    password_hash: str
    role: str = "student"
    degree: Optional[str] = None
    branch: Optional[str] = None
    college_type: Optional[str] = None  # "autonomous" | "affiliated"
    college_url: Optional[str] = None
    regulation: Optional[str] = None
    preference: Optional[str] = None  # "coding" | "noncoding" | "balanced"
    semester_current: int = 1
    behavior_profile: BehaviorProfile = BehaviorProfile()
    xp_system: XPSystem = XPSystem()
    token_usage: TokenUsage = TokenUsage()
    created_at: datetime = Field(default_factory=datetime.utcnow)




class StudentProfile(BaseModel):
    id: str
    name: str
    email: str
    role: str = "student"
    degree: Optional[str] = None
    branch: Optional[str] = None
    college_type: Optional[str] = None
    college_url: Optional[str] = None
    regulation: Optional[str] = None
    preference: Optional[str] = None
    semester_current: int = 1
    behavior_profile: BehaviorProfile = BehaviorProfile()
    xp_system: XPSystem = XPSystem()
    token_usage: TokenUsage = TokenUsage()




class OnboardingSetup(BaseModel):
    degree: str
    branch: Optional[str] = None
    college_type: str  # "autonomous" | "affiliated"
    college_url: Optional[str] = None
    regulation: Optional[str] = None
    preference: str  # "coding" | "noncoding" | "balanced"
    semester_current: int = 1
