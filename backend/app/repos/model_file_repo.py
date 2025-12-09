from sqlalchemy.orm import Session
from app.db.models import ModelFile
from uuid import UUID
from datetime import datetime
from app.db.models import VerificationStatus, ModelVerification

class ModelFileRepository:
    def create(self, db: Session, filename: str, minio_path: str, uploader_id: UUID, size: int) -> ModelFile:
        model_file = ModelFile(
            filename=filename,
            minio_path=minio_path,
            size=size,
            uploader_id=uploader_id,
            created_at=datetime.now()
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

    def list_by_verification_status(self, db: Session, status: VerificationStatus):
        return (
            db.query(ModelFile)
            .filter(ModelFile.latest_verification != None and ModelFile.latest_verification.status == status)
            .all()
        )

    def get_by_id(self, db: Session, file_id: UUID) -> ModelFile:
        return db.query(ModelFile).filter(ModelFile.id == file_id).first()

model_file_repo = ModelFileRepository()
