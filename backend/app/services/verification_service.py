import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import ModelFile, VerificationStatus
from app.repos.print_job_repo import print_job_repo
from app.repos.verification_repo import verification_repo
from app.schemas.verifications import VerificationCreate
from app.services.print_service import print_service

logger = logging.getLogger(__name__)


class VerificationService:
    def __init__(self, verification_repo, print_service, print_job_repo):
        self.verification_repo = verification_repo
        self.print_service = print_service
        self.print_repo = print_job_repo

    def verify_file(self, db: Session, verification: VerificationCreate, verifier_id: UUID):
        # Serialize decisions for one file with direct queue requests.
        model_file = (
            db.query(ModelFile)
            .filter(ModelFile.id == verification.file_id)
            .with_for_update()
            .first()
        )
        if not model_file:
            raise HTTPException(404, "File not found")
        if self.print_repo.has_active_job(db, verification.file_id):
            raise HTTPException(409, "File already has an active print job")

        try:
            saved = self.verification_repo.create(
                db, verification.file_id, verifier_id, verification.status, verification.comments
            )
            if verification.status == VerificationStatus.approved:
                # PrintService commits the verification and queued job together.
                self.print_service.enqueue_print(db, verification.file_id, verifier_id)
            else:
                db.commit()
            db.refresh(saved)
        except Exception:
            db.rollback()
            raise

        logger.info(
            "Verification recorded",
            extra={
                "file_id": str(verification.file_id),
                "verifier_id": str(verifier_id),
                "status": verification.status.value,
            },
        )
        return saved


verification_service = VerificationService(verification_repo, print_service, print_job_repo)
