from fastapi import APIRouter, UploadFile, File, status, Depends
from sqlalchemy.orm import Session
from app.services.file_service import file_service
from typing import List
from app.schemas.files import FileUploadResponse, FileMetadataResponse
from app.dependencies import get_db
from uuid import UUID

router = APIRouter()

@router.post("/upload", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_bytes = await file.read()
    response = file_service.upload_file(db, file_bytes, file.filename, UUID("12345678-1234-5678-1234-567812345678"))

    return response


@router.get("/all", response_model=List[FileMetadataResponse])
def get_all_files(
    db: Session = Depends(get_db)
):
    return file_service.list_all_files(db)


@router.get("/{file_id}", response_model=FileMetadataResponse)
def get_file(
    file_id: UUID,
    db: Session = Depends(get_db)
):
    return file_service.get_file(db, file_id)