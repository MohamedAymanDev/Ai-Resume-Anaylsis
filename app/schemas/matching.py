from pydantic import BaseModel


class JobMatchResponse(BaseModel):
    resume_id: int
    job_id: int
    job_title: str
    company: str
    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]