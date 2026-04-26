from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CollegeCreate(BaseModel):
    name: str
    url: Optional[str] = None
    is_autonomous: bool = False
    regulation: Optional[str] = None


class CollegeInDB(BaseModel):
    name: str
    url: Optional[str] = None
    is_autonomous: bool = False
    regulation: Optional[str] = None
    scraped_curriculum: dict = {}
    last_scraped: Optional[datetime] = None


class CollegeResponse(BaseModel):
    id: str
    name: str
    url: Optional[str] = None
    is_autonomous: bool
    regulation: Optional[str] = None
    last_scraped: Optional[datetime] = None
