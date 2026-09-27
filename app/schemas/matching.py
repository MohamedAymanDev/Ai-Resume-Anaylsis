from pydantic import BaseModel


class JobMatchResponse(BaseModel):
    resume_id: int
    job_id: int
    job_title: str
    company: str

    match_score: float
    skill_match_score: float
    semantic_similarity_score: float
    experience_match_score: float
    education_match_score: float

    matched_skills: list[str]
    missing_skills: list[str]


class JobSearchMatchResponse(BaseModel):
    job_id: int
    job_title: str
    company: str
    location: str | None

    match_score: float

    matched_skills: list[str]
    missing_skills: list[str]