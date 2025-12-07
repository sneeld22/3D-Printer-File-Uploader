from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.services.minio_service import minio_service
from app.repos.model_file_repo import model_file_repo
from app.schemas.files import FileUploadResponse, FileMetadataResponse
from uuid import UUID
from datetime import datetime

class FileService:
    def __init__(self):
        self.minio = minio_service
        self.repo = model_file_repo

    def upload_file(self, db: Session, file_bytes: bytes, filename: str, uploader_id: UUID) -> str:
        object_name = self.minio.generate_object_name(filename)
        try:
            self.minio.upload(
                file_obj=file_bytes,
                object_name=object_name,
                length=len(file_bytes),
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"File upload failed: {str(e)}"
            )
        
        model_file = self.repo.create(db, filename, object_name, uploader_id)
        
        return FileUploadResponse(
            id=model_file.id,
            filename=model_file.filename,
            message="Upload successful"
        )
    

    def list_all_files(self, db: Session) -> list[FileMetadataResponse]:
        files = self.repo.list_all(db)
         # Convert DB models to Pydantic responses with size & last_modified from MinIO
        result = []
        for file in files:
            # Get MinIO metadata for size/last_modified
            try:
                minio_info = self.minio.get_file(file.minio_path)
                size = minio_info["size"]
                last_modified = datetime.fromisoformat(minio_info["last_modified"]) if minio_info["last_modified"] else None
            except HTTPException:
                size = 0
                last_modified = None

            result.append(FileMetadataResponse(
                id=file.id,
                filename=file.filename,
                size=size,
                last_modified=last_modified
            ))
        return result
    
    def list_files_by_user(self, db: Session, user_id: UUID) -> list[FileMetadataResponse]:
        files = self.repo.list_by_user(db, user_id)

        result = []
        for file in files:
            try:
                minio_info = self.minio.get_file(file.minio_path)
                size = minio_info["size"]
                last_modified = datetime.fromisoformat(minio_info["last_modified"]) if minio_info["last_modified"] else None
            except:
                size = 0
                last_modified = None

            result.append(FileMetadataResponse(
                id=file.id,
                filename=file.filename,
                size=size,
                last_modified=last_modified
            ))

        return result
    
    def get_file_metadata(self, db: Session, file_id: UUID) -> FileMetadataResponse:
        file = self.repo.get_by_id(db, file_id)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        minio_info = self.minio.get_file(file.minio_path)
        last_modified = datetime.fromisoformat(minio_info["last_modified"]) if minio_info["last_modified"] else None

        return FileMetadataResponse(
            id=file.id,
            filename=file.filename,
            size=minio_info["size"],
            last_modified=last_modified
        )
    
    def stream_file(self, db: Session, file_id: UUID):
        file_record = file_service.repo.get_by_id(db, file_id)
        if not file_record:
            raise HTTPException(status_code=404, detail="File not found")
        
        return file_record.filename, self.minio.stream(file_record.minio_path)



file_service = FileService()
