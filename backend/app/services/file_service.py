from fastapi import HTTPException, status
from app.services.minio_service import minio_service
from app.schemas.files import FileInfo
from typing import List

class FileService:
    def __init__(self):
        self.minio = minio_service

    def upload_file_to_minio(self, file_bytes: bytes, filename: str) -> str:
        """
        Upload file bytes to MinIO and return the generated object name.
        Raises HTTPException on failure.
        """
        object_name = self.minio.generate_object_name(filename)
        try:
            self.minio.upload(
                file_obj=file_bytes,
                object_name=object_name,
                length=len(file_bytes),
            )
        except HTTPException:
            # Re-raise so the FastAPI exception handler can catch it
            raise
        except Exception as e:
            # Wrap any other exception into HTTPException
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"File upload failed: {str(e)}"
            )
        return object_name
    

    def list_all_files(self) -> List[FileInfo]:
        """
        List all object names in the MinIO bucket.
        Returns a list of filenames (object names).
        """
        raw_files = minio_service.list_objects()
        files = [FileInfo(**file) for file in raw_files]
        return files
    
    def get_file(self, object_name: str) -> FileInfo:
        file = minio_service.get_file(object_name)
        return FileInfo(**file)


file_service = FileService()
