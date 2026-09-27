import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user, get_db
from app.db.models import Job, Resume, ResumeAnalysis, User
from app.ai.agents.career_advisor import CareerAdvisor
from app.schemas.career import CareerAdviceResponse


router = APIRouter(
    prefix="/career",
    tags=["Career Advisor"],
)


@router.post(
    "/resume/{resume_id}/job/{job_id}",
    response_model=CareerAdviceResponse,
)
def get_career_advice(
    resume_id: int,
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id,
        )
        .first()
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    analysis = (
        db.query(ResumeAnalysis)
        .filter(ResumeAnalysis.resume_id == resume.id)
        .first()
    )

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume has not been analyzed yet",
        )

    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    resume_analysis = {
        "summary": analysis.summary,
        "technical_skills": json.loads(analysis.technical_skills),
        "soft_skills": json.loads(analysis.soft_skills),
        "education": json.loads(analysis.education),
        "experience": json.loads(analysis.experience),
    }

    job_information = {
        "title": job.title,
        "company": job.company,
        "description": job.description,
        "required_skills": json.loads(job.required_skills),
        "preferred_skills": json.loads(job.preferred_skills or "[]"),
        "experience_level": job.experience_level,
        "education": job.education,
    }

    advisor = CareerAdvisor()

    advice, sources = advisor.advise(
    resume_analysis=json.dumps(resume_analysis),
    job_information=json.dumps(job_information),
)

    return CareerAdviceResponse(
        advice=advice,
        sources=sources,
    )