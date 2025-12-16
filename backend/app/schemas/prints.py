from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from app.db.models import PrintStatus


class PrintJobCreate(BaseModel):
    model_file_id: UUID


class PrintJobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    model_file_id: UUID
    requested_by: UUID
    status: PrintStatus
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
