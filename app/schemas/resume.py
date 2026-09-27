from datetime import datetime

from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    status: str
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }


class ResumeAnalysis(BaseModel):
    summary: str
    technical_skills: list[str]
    soft_skills: list[str]
    education: list[str]
    experience: list[str]


class ResumeAnalysisResponse(BaseModel):
    resume_id: int
    summary: str
    technical_skills: list[str]
    soft_skills: list[str]
    education: list[str]
    experience: list[str]
    created_at: datetime