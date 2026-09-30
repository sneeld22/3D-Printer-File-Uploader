from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.services.minio_service import minio_service
from app.repos.model_file_repo import model_file_repo
from app.schemas.files import FileUploadResponse, FileMetadataResponse
from uuid import UUID
from datetime import datetime
from app.db.models import ModelFile, PrintStatus
from app.db.models import RoleEnum, User
from typing import BinaryIO


import logging

logger = logging.getLogger(__name__)
class FileService:
    def __init__(self):
        self.minio = minio_service
        self.repo = model_file_repo

    def upload_file(self, db: Session, file_obj: BinaryIO, filename: str, size: int, uploader_id: UUID) -> FileUploadResponse:
        logger.info(
            "Uploading file",
            extra={
                "file_name": filename,
                "uploader_id": str(uploader_id),
                "size": size,
            },
        )
        
        object_name = self.minio.generate_object_name(filename)
        try:
            self.minio.upload(
                file_obj=file_obj,
                object_name=object_name,
                length=size,
            )
        except HTTPException:
            raise
        except Exception:
            logger.exception(
                "MinIO upload failed",
                extra={"file_name": filename, "object_name": object_name},
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="File upload failed",
            )
        
        try:
            model_file = self.repo.create(db, filename, object_name, uploader_id, size=size)
        except Exception:
            logger.exception("Database record creation failed after upload", extra={"object_name": object_name})
            try:
                self.minio.client.remove_object(self.minio.bucket_name, object_name)
            except Exception:
                logger.exception("Failed to remove orphaned uploaded object", extra={"object_name": object_name})
            raise
        
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
    
    def get_file(self, db: Session, file_id: UUID, user: User) -> FileMetadataResponse:
        file = self._get_readable_file(db, file_id, user)
        return self._build_file_metadata(db, file)
    

    def delete_file(self, db: Session, file_id: UUID):
        file = self.repo.get_by_id(db, file_id)
        if not file:
            logger.warning("Delete failed: file not found", extra={"file_id": str(file_id)})
            raise HTTPException(status_code=404, detail="File not found")
            

        # Delete from MinIO
        try:
            self.minio.client.remove_object(self.minio.bucket_name, file.minio_path)
        except Exception:
            logger.exception(
            "Failed to delete file from MinIO",
            extra={"file_id": str(file_id), "path": file.minio_path},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete file from storage"
            )

        # Delete from database
        self.repo.delete(db, file)
        logger.info("File deleted", extra={"file_id": str(file_id)})
    
    def stream_file(self, db: Session, file_id: UUID, user: User):
        file_record = self._get_readable_file(db, file_id, user)
        return file_record.filename, self.minio.stream(file_record.minio_path)

    def _get_readable_file(self, db: Session, file_id: UUID, user: User) -> ModelFile:
        file_record = self.repo.get_by_id(db, file_id)
        if not file_record:
            raise HTTPException(status_code=404, detail="File not found")

        privileged_roles = {RoleEnum.admin, RoleEnum.verifier, RoleEnum.downloader}
        user_roles = {role.role_id for role in user.roles}
        if file_record.uploader_id != user.id and not user_roles.intersection(privileged_roles):
            raise HTTPException(status_code=403, detail="Not allowed to access this file")
        return file_record
    

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
