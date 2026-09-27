import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user, get_db
from app.db.models import Job, Resume, ResumeAnalysis, User
from app.schemas.career import CareerAdviceResponse
from app.ai.agents.career_advisor import CareerAdvisor


router = APIRouter(
    prefix="/career",
    tags=["Career"],
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
    # =========================
    # 1. Get Resume
    # =========================

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

    # =========================
    # 2. Get Resume Analysis
    # =========================

    resume_analysis = (
        db.query(ResumeAnalysis)
        .filter(
            ResumeAnalysis.resume_id == resume.id
        )
        .first()
    )

    if resume_analysis is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume has not been analyzed yet",
        )

    # =========================
    # 3. Get Job
    # =========================

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

    # =========================
    # 4. Prepare Resume Analysis
    # =========================

    resume_analysis_data = {
        "summary": resume_analysis.summary,
        "technical_skills": json.loads(
            resume_analysis.technical_skills
        ),
        "soft_skills": json.loads(
            resume_analysis.soft_skills
        ),
        "education": json.loads(
            resume_analysis.education
        ),
        "experience": json.loads(
            resume_analysis.experience
        ),
    }

    # =========================
    # 5. Prepare Job Information
    # =========================

    job_information = {
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "description": job.description,
        "required_skills": json.loads(
            job.required_skills
        ),
        "preferred_skills": json.loads(
            job.preferred_skills or "[]"
        ),
        "experience_level": job.experience_level,
        "education": job.education,
    }

    # =========================
    # 6. Run Career Advisor
    # =========================

    advisor = CareerAdvisor()

    advice, sources = advisor.advise(
        resume_analysis=json.dumps(
            resume_analysis_data,
            ensure_ascii=False,
        ),
        job_information=json.dumps(
            job_information,
            ensure_ascii=False,
        ),
    )

    # =========================
    # 7. Return Response
    # =========================

    return CareerAdviceResponse(
        advice=advice,
        sources=sources,
    )