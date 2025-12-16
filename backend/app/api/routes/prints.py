# app/api/routes/prints.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.prints import PrintJobCreate, PrintJobOut
from app.services.print_service import print_service
from app.dependencies import get_db, require_role
from app.db.models import User, RoleEnum

router = APIRouter()

@router.post("/", response_model=PrintJobOut)
def enqueue_print(
    payload: PrintJobCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role([RoleEnum.uploader, RoleEnum.admin])),
):
    return print_service.enqueue_print(db, payload.model_file_id, user.id)


@router.get("/", response_model=list[PrintJobOut])
def all_print_jobs(
    db: Session = Depends(get_db),
    _: User = Depends(require_role([RoleEnum.admin])),
):
    return print_service.list_jobs(db)


@router.get("/{job_id}", response_model=PrintJobOut)
def get_print_job(
    job_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_role([RoleEnum.admin])),
):
    return print_service.get_job(db, job_id)