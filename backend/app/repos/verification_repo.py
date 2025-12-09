from sqlalchemy.orm import Session
from uuid import UUID

from app.db.models import ModelVerification, VerificationStatus


class VerificationRepository:
    def create(
        self,
        db: Session,
        model_file_id: UUID,
        verifier_id: UUID,
        status: VerificationStatus,
        comments: str | None
    ) -> ModelVerification:

        verification = ModelVerification(
            model_file_id=model_file_id,
            verifier_id=verifier_id,
            status=status,
            comments=comments,
        )

        db.add(verification)
        db.commit()
        db.refresh(verification)
        return verification

    def get_latest(self, db: Session, file_id: UUID) -> ModelVerification | None:
        return (
            db.query(ModelVerification)
            .filter(ModelVerification.model_file_id == file_id)
            .order_by(ModelVerification.created_at.desc())
            .first()
        )


    def get_history(self, db: Session, file_id: UUID) -> list[ModelVerification]:
        return (
            db.query(ModelVerification)
            .filter(ModelVerification.model_file_id == file_id)
            .order_by(ModelVerification.created_at.asc())
            .all()
        )

    def has_verification(self, db: Session, file_id: UUID) -> bool:
        return (
            db.query(ModelVerification)
            .filter(ModelVerification.model_file_id == file_id)
            .first()
            is not None
        )


verification_repo = VerificationRepository()
