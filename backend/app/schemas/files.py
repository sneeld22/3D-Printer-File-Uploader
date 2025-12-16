from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class FileUploadResponse(BaseModel):
    id: UUID
    filename: str
    message: str

class FileMetadataResponse(BaseModel):
    id: UUID
    filename: str
    size: int
    user_id: UUID
    created_at: datetime
    verification_status: str
    print_status: str