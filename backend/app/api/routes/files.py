from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.minio_service import minio_service

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file directly to MinIO.
    """
    # Read file bytes
    file_bytes = await file.read()

    # Generate unique object name
    object_name = minio_service.generate_object_name(file.filename)

    # Upload to MinIO
    minio_service.upload(
        file_obj=file_bytes,
        object_name=object_name,
        length=len(file_bytes)
    )

    return {
        "filename": file.filename,
        "object_name": object_name,
        "message": "Upload successful"
    }