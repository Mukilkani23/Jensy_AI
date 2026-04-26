from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    student_id: str
    message: str


class ConversationInDB(BaseModel):
    student_id: str
    messages: list[ChatMessage] = []
    intent_log: list[str] = []
    ner_entities: list[dict] = []


class AnalyzeRequest(BaseModel):
    student_id: str
    message: str


class AnalyzeResponse(BaseModel):
    intent: str
    entities: list[dict]
    confidence: float


class BehaviorReport(BaseModel):
    student_id: str
    strong_subjects: list[str] = []
    weak_subjects: list[str] = []
    recommended_actions: list[str] = []
    study_pattern: str = "unknown"
    generated_at: datetime = Field(default_factory=datetime.utcnow)
