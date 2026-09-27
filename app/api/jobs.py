import json

from fastapi import APIRouter, Depends, status,HTTPException
from sqlalchemy.orm import Session

from app.api.auth import get_current_user, get_db
from app.db.models import Job, User
from app.schemas.job import JobCreate, JobResponse,JobUpdate


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "/",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = Job(
        title=job_data.title,
        company=job_data.company,
        location=job_data.location,
        description=job_data.description,
        required_skills=json.dumps(
            job_data.required_skills
        ),
        preferred_skills=json.dumps(
            job_data.preferred_skills
        ),
        experience_level=job_data.experience_level,
        education=job_data.education,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return JobResponse(
        id=job.id,
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description,
        required_skills=json.loads(
            job.required_skills
        ),
        preferred_skills=json.loads(
            job.preferred_skills
        ),
        experience_level=job.experience_level,
        education=job.education,
        created_at=job.created_at,
    )

@router.get(
    "/",
    response_model=list[JobResponse],
)
def get_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    jobs = db.query(Job).all()

    return [
        JobResponse(
            id=job.id,
            title=job.title,
            company=job.company,
            location=job.location,
            description=job.description,
            required_skills=json.loads(
                job.required_skills
            ),
            preferred_skills=json.loads(
                job.preferred_skills or "[]"
            ),
            experience_level=job.experience_level,
            education=job.education,
            created_at=job.created_at,
        )
        for job in jobs
    ]

@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
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

    return JobResponse(
        id=job.id,
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description,
        required_skills=json.loads(
            job.required_skills
        ),
        preferred_skills=json.loads(
            job.preferred_skills or "[]"
        ),
        experience_level=job.experience_level,
        education=job.education,
        created_at=job.created_at,
    )

@router.put(
    "/{job_id}",
    response_model=JobResponse,
)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
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

    if job_data.title is not None:
        job.title = job_data.title

    if job_data.company is not None:
        job.company = job_data.company

    if job_data.location is not None:
        job.location = job_data.location

    if job_data.description is not None:
        job.description = job_data.description

    if job_data.required_skills is not None:
        job.required_skills = json.dumps(
            job_data.required_skills
        )

    if job_data.preferred_skills is not None:
        job.preferred_skills = json.dumps(
            job_data.preferred_skills
        )

    if job_data.experience_level is not None:
        job.experience_level = job_data.experience_level

    if job_data.education is not None:
        job.education = job_data.education

    db.commit()
    db.refresh(job)

    return JobResponse(
        id=job.id,
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description,
        required_skills=json.loads(
            job.required_skills
        ),
        preferred_skills=json.loads(
            job.preferred_skills or "[]"
        ),
        experience_level=job.experience_level,
        education=job.education,
        created_at=job.created_at,
    )            

@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
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

    db.delete(job)
    db.commit()    