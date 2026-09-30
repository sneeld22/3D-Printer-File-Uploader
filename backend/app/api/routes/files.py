from fastapi import APIRouter, UploadFile, File, status, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.services.file_service import file_service
from app.schemas.files import FileUploadResponse, FileMetadataResponse
from app.dependencies import get_db, get_current_user, require_role
from app.db.models import User, RoleEnum
from app.utils.upload_validation import MAX_FILE_SIZE, normalize_upload_filename
from os import SEEK_END
from urllib.parse import quote
from uuid import UUID

router = APIRouter()

@router.post("/upload", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_role([RoleEnum.uploader, RoleEnum.admin])),
):
    try:
        filename = normalize_upload_filename(file.filename)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    file.file.seek(0, SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    if size == 0:
        raise HTTPException(status_code=400, detail="The file is empty")
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File exceeds the 50 MiB limit")

    response = file_service.upload_file(db, file.file, filename, size, user.id)

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

@router.get("/queued", response_model=list[FileMetadataResponse])
def get_queued_files(
    db: Session = Depends(get_db),
    _: User = Depends(require_role([RoleEnum.admin, RoleEnum.downloader, RoleEnum.verifier])),
):
    return file_service.list_queued_files(db)

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
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return file_service.get_file(db, file_id, user)

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    file_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_role([RoleEnum.admin]))
):
    file_service.delete_file(db, file_id)
    return

@router.get("/{file_id}/download")
def download_file(
    file_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    filename, stream_generator = file_service.stream_file(db, file_id, user)

    return StreamingResponse(
        stream_generator(),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename, safe='')}"
        }
    )
