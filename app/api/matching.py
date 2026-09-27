import json
from app.services.semantic_matcher import calculate_semantic_similarity
from fastapi import (
   APIRouter,
    Depends,
    HTTPException,
    Query,
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
from app.schemas.matching import (
    JobMatchResponse,
    JobSearchMatchResponse,
)
from app.services.job_matcher import (
    get_skill_match_details,
    calculate_experience_match,
    calculate_education_match,
)
from app.services.scoring import calculate_final_match_score
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

    skill_match_score = result["score"]

    semantic_similarity_score = calculate_semantic_similarity(
        resume.extracted_text,
        job.description,
    )
    experience_match_score = calculate_experience_match(
    json.loads(analysis.experience),
    job.experience_level,
    )
    education_match_score = calculate_education_match(
    json.loads(analysis.education),
    job.education,
    )

    final_match_score = calculate_final_match_score(
    skill_match_score=skill_match_score,
    semantic_similarity_score=semantic_similarity_score,
    experience_match_score=experience_match_score,
    education_match_score=education_match_score,
    )

    return JobMatchResponse(
    resume_id=resume.id,
    job_id=job.id,
    job_title=job.title,
    company=job.company,
    match_score=final_match_score,
    skill_match_score=skill_match_score,
    semantic_similarity_score=semantic_similarity_score,
    experience_match_score=experience_match_score,
    education_match_score=education_match_score,
    matched_skills=result["matched_skills"],
    missing_skills=result["missing_skills"],
    )
    
@router.post(
    "/resume/{resume_id}/search",
    response_model=list[JobSearchMatchResponse],
)
def search_and_match_jobs(
    resume_id: int,
    q: str | None = Query(default=None),
    location: str | None = Query(default=None),
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

    # =========================
    # 3. Search Jobs
    # =========================

    query = db.query(Job)

    if q:
        search_term = f"%{q.lower()}%"

        query = query.filter(
            (
                Job.title.ilike(search_term)
                | Job.company.ilike(search_term)
                | Job.description.ilike(search_term)
            )
        )

    if location:
        query = query.filter(
            Job.location.ilike(f"%{location}%")
        )

    jobs = query.all()

    # =========================
    # 4. Resume Skills
    # =========================

    resume_skills = json.loads(
        analysis.technical_skills
    )

    resume_experience = json.loads(
        analysis.experience
    )

    resume_education = json.loads(
        analysis.education
    )

    # =========================
    # 5. Match Every Job
    # =========================

    results = []

    for job in jobs:

        job_required_skills = json.loads(
            job.required_skills
        )

        # Skill matching
        skill_result = get_skill_match_details(
            resume_skills,
            job_required_skills,
        )

        skill_match_score = skill_result["score"]

        # Semantic similarity
        semantic_similarity_score = (
            calculate_semantic_similarity(
                resume.extracted_text,
                job.description,
            )
        )

        # Experience matching
        experience_match_score = (
            calculate_experience_match(
                resume_experience,
                job.experience_level,
            )
        )

        # Education matching
        education_match_score = (
            calculate_education_match(
                resume_education,
                job.education,
            )
        )

        # Final score
        final_match_score = calculate_final_match_score(
            skill_match_score=skill_match_score,
            semantic_similarity_score=semantic_similarity_score,
            experience_match_score=experience_match_score,
            education_match_score=education_match_score,
        )

        results.append(
            JobSearchMatchResponse(
                job_id=job.id,
                job_title=job.title,
                company=job.company,
                location=job.location,
                match_score=final_match_score,
                matched_skills=skill_result[
                    "matched_skills"
                ],
                missing_skills=skill_result[
                    "missing_skills"
                ],
            )
        )

    # =========================
    # 6. Sort by Match Score
    # =========================

    results.sort(
        key=lambda result: result.match_score,
        reverse=True,
    )

    return results

    