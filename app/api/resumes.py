from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user, get_db
from app.db.models import Resume, User
from app.schemas.resume import ResumeResponse

from app.services.resume_parser import extract_resume_text

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)


UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 8 * 1024 * 1024


@router.post(
    
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are allowed",
        )

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 8 MB",
        )

    unique_filename = f"{uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(file_path, "wb") as buffer:
        buffer.write(file_content)
    
    extracted_text = extract_resume_text(
    str(file_path),
    file_extension.replace(".", ""),
    )
    resume = Resume(
    user_id=current_user.id,
    filename=file.filename,
    file_path=str(file_path),
    file_type=file_extension.replace(".", ""),
    extracted_text=extracted_text,
    status="parsed",
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume