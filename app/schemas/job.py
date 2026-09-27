from datetime import datetime

from pydantic import BaseModel


class JobCreate(BaseModel):
    title: str
    company: str
    location: str | None = None
    description: str
    required_skills: list[str]
    preferred_skills: list[str] = []
    experience_level: str | None = None
    education: str | None = None


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str | None
    description: str
    required_skills: list[str]
    preferred_skills: list[str]
    experience_level: str | None
    education: str | None
    created_at: datetime
    
class JobUpdate(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    description: str | None = None
    required_skills: list[str] | None = None
    preferred_skills: list[str] | None = None
    experience_level: str | None = None
    education: str | None = None    