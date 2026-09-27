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