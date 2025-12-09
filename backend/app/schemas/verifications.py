from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.db.models import VerificationStatus

class VerificationCreate(BaseModel):
    file_id: UUID
    status: VerificationStatus
    comments: str | None = None