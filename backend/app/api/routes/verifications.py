from fastapi import APIRouter, UploadFile, File, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models import User, RoleEnum
from app.dependencies import require_role, get_db
from app.schemas.verifications import VerificationCreate
from uuid import UUID

router = APIRouter()

@router.post("")
async def verify_file(
    verification: VerificationCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role([RoleEnum.uploader, RoleEnum.admin])),
):
    pass