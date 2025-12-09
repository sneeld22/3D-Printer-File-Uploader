from fastapi import APIRouter, UploadFile, File, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models import User, RoleEnum
from app.dependencies import require_role, get_db
router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_role([RoleEnum.uploader, RoleEnum.admin])),
):
    pass