import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.api.auth import get_current_user, get_db
from app.db.models import (
    Job,
    Resume,
    ResumeAnalysis,
    User,
)
from app.schemas.matching import JobMatchResponse
from app.services.job_matcher import (
    get_skill_match_details,
)


router = APIRouter(
    prefix="/matching",
    tags=["Job Matching"],
)


@router.post(
    "/resume/{resume_id}/job/{job_id}",
    response_model=JobMatchResponse,
)
def match_resume_with_job(
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
        .filter(
            ResumeAnalysis.resume_id == resume.id
        )
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

    resume_skills = json.loads(
        analysis.technical_skills
    )

    job_required_skills = json.loads(
        job.required_skills
    )

    result = get_skill_match_details(
        resume_skills,
        job_required_skills,
    )

    return JobMatchResponse(
        resume_id=resume.id,
        job_id=job.id,
        job_title=job.title,
        company=job.company,
        match_score=result["score"],
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
    )