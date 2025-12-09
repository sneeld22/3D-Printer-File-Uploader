from fastapi import APIRouter, UploadFile, File, status, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.services.file_service import file_service
from app.schemas.files import FileUploadResponse, FileMetadataResponse
from app.dependencies import get_db, require_role
from app.db.models import User, RoleEnum
from uuid import UUID

router = APIRouter()

@router.post("/upload", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_role([RoleEnum.uploader, RoleEnum.admin])),
):
    file_bytes = await file.read()
    response = file_service.upload_file(db, file_bytes, file.filename, user.id)

    return response


@router.get("/all", response_model=list[FileMetadataResponse])
def get_all_files(
    db: Session = Depends(get_db),
    _: User = Depends(require_role([RoleEnum.admin, RoleEnum.downloader, RoleEnum.verifier])),
):
    return file_service.list_all_files(db)

@router.get("/unverified", response_model=list[FileMetadataResponse])
def get_pending_files(
    db: Session = Depends(get_db),
    _: User = Depends(require_role([RoleEnum.admin, RoleEnum.downloader, RoleEnum.verifier])),
):
    return file_service.list_unverified_files(db)


@router.get("/me", response_model=list[FileMetadataResponse])
def get_my_files(
    db: Session = Depends(get_db),
    user: User = Depends(require_role([RoleEnum.uploader, RoleEnum.admin]))
):
    return file_service.list_files_by_user(db, user.id)


@router.get("/user/{user_id}", response_model=list[FileMetadataResponse])
def get_files_by_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_role([RoleEnum.admin]))
):
    return file_service.list_files_by_user(db, user_id)


@router.get("/{file_id}", response_model=FileMetadataResponse)
def get_file(
    file_id: UUID,
    db: Session = Depends(get_db)
):
    return file_service.get_file(db, file_id)


@router.get("/{file_id}/download")
def download_file(
    file_id: UUID,
    db: Session = Depends(get_db)
):
    filename, stream_generator = file_service.stream_file(db, file_id)

    return StreamingResponse(
        stream_generator(),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )