from fastapi import APIRouter, UploadFile, File, status
from app.services.file_service import file_service
from typing import List
from app.schemas.files import UploadedFileResponse, FileInfo

router = APIRouter()

@router.post("/upload", response_model=UploadedFileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file directly to MinIO.
    """
    file_bytes = await file.read()

    object_name = file_service.upload_file_to_minio(file_bytes, file.filename)

    return UploadedFileResponse(
        filename=file.filename,
        object_name=object_name,
        message="Upload successful"
    )


@router.get("/all", response_model=List[FileInfo])
def get_all_files():
    """
    Return a list of all filenames stored in MinIO.
    """
    files = file_service.list_all_files()
    return files