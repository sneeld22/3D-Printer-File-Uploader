from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.services.minio_service import minio_service
from app.repos.model_file_repo import model_file_repo
from app.schemas.files import FileUploadResponse, FileMetadataResponse
from uuid import UUID
from datetime import datetime
from app.db.models import ModelFile, PrintStatus

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
        
        model_file = self.repo.create(db, filename, object_name, uploader_id, size=len(file_bytes))
        
        return FileUploadResponse(
            id=model_file.id,
            filename=model_file.filename,
            message="Upload successful"
        )
    

    def list_all_files(self, db: Session) -> list[FileMetadataResponse]:
        files = self.repo.list_all(db)
        return [self._build_file_metadata(db, file) for file in files]
    
    def list_unverified_files(self, db: Session) -> list[FileMetadataResponse]:
        files = self.repo.list_unverified_files(db)
        return [self._build_file_metadata(db, file) for file in files]

    def list_queued_files(self, db: Session) -> list[FileMetadataResponse]:
        files = self.repo.list_by_print_status(db, PrintStatus.queued)
        return [self._build_file_metadata(db, file) for file in files]
    
    def list_files_by_user(self, db: Session, user_id: UUID) -> list[FileMetadataResponse]:
        files = self.repo.list_by_user(db, user_id)
        return [self._build_file_metadata(db, file) for file in files]
    
    def get_file(self, db: Session, file_id: UUID) -> FileMetadataResponse:
        file = self.repo.get_by_id(db, file_id)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        
        return self._build_file_metadata(db, file)
    

    def delete_file(self, db: Session, file_id: UUID):
        file = self.repo.get_by_id(db, file_id)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        # Delete from MinIO
        try:
            self.minio.client.remove_object(self.minio.bucket_name, file.minio_path)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete file from storage: {str(e)}"
            )

        # Delete from database
        self.repo.delete(db, file)
    
    def stream_file(self, db: Session, file_id: UUID):
        file_record = file_service.repo.get_by_id(db, file_id)
        if not file_record:
            raise HTTPException(status_code=404, detail="File not found")
        
        return file_record.filename, self.minio.stream(file_record.minio_path)
    

    def _build_file_metadata(self, db: Session, file: ModelFile) -> FileMetadataResponse:
        verification = file.latest_verification
        verification_status = verification.status if verification else "pending"

        print_job = file.latest_print_job
        print_status = print_job.status if print_job else "pending"

        return FileMetadataResponse(
            id=file.id,
            filename=file.filename,
            size=file.size,
            user_id=file.uploader_id,
            created_at=file.created_at,
            verification_status=verification_status,
            print_status=print_status
        )



file_service = FileService()
