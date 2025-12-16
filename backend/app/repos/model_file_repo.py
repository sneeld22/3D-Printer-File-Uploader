from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_, desc
from app.db.models import ModelFile
from uuid import UUID
from datetime import datetime
from app.db.models import VerificationStatus, ModelVerification, PrintStatus, PrintJob

class ModelFileRepository:
    def create(self, db: Session, filename: str, minio_path: str, uploader_id: UUID, size: int) -> ModelFile:
        model_file = ModelFile(
            filename=filename,
            minio_path=minio_path,
            size=size,
            uploader_id=uploader_id,
            created_at=datetime.utcnow()
        )
        db.add(model_file)
        db.commit()
        db.refresh(model_file)
        return model_file

    def list_all(self, db: Session) -> list[ModelFile]:
        return db.query(ModelFile).all()
    
    def list_by_user(self, db: Session, user_id: UUID) -> list[ModelFile]:
        return (
            db.query(ModelFile)
            .filter(ModelFile.uploader_id == user_id)
            .all()
        )
    
    def list_unverified_files(self, db: Session) -> list[ModelFile]:
        return (
            db.query(ModelFile)
            .filter(ModelFile.latest_verification == None)
            .all()
        )
    
    def list_by_print_status(self, db: Session, status: PrintStatus) -> list[ModelFile]:
        # Subquery to get latest print job per ModelFile by created_at
        latest_print_job_subq = (
            db.query(
                PrintJob.model_file_id,
                func.max(PrintJob.created_at).label("max_created_at")
            )
            .group_by(PrintJob.model_file_id)
            .subquery()
        )

        # Join ModelFile -> PrintJob (latest only), filter by status
        query = (
            db.query(ModelFile)
            .join(
                latest_print_job_subq,
                ModelFile.id == latest_print_job_subq.c.model_file_id
            )
            .join(
                PrintJob,
                and_(
                    PrintJob.model_file_id == latest_print_job_subq.c.model_file_id,
                    PrintJob.created_at == latest_print_job_subq.c.max_created_at
                )
            )
            .filter(PrintJob.status == status)
        )

        return query.all()

    def list_by_verification_status(self, db: Session, status: VerificationStatus):
        # Subquery to get latest verification per ModelFile by created_at
        latest_verification_subq = (
            db.query(
                ModelVerification.model_file_id,
                func.max(ModelVerification.created_at).label("max_created_at")
            )
            .group_by(ModelVerification.model_file_id)
            .subquery()
        )

        # Join ModelFile -> ModelVerification (latest only), filter by status
        query = (
            db.query(ModelFile)
            .join(
                latest_verification_subq,
                ModelFile.id == latest_verification_subq.c.model_file_id
            )
            .join(
                ModelVerification,
                and_(
                    ModelVerification.model_file_id == latest_verification_subq.c.model_file_id,
                    ModelVerification.created_at == latest_verification_subq.c.max_created_at
                )
            )
            .filter(ModelVerification.status == status)
        )

    def get_by_id(self, db: Session, file_id: UUID) -> ModelFile:
        return db.query(ModelFile).filter(ModelFile.id == file_id).first()
    
    def delete(self, db: Session, model_file: ModelFile):
        db.delete(model_file)
        db.commit()

model_file_repo = ModelFileRepository()
