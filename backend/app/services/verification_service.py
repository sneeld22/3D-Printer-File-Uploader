from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas.verifications import VerificationCreate

from app.repos.verification_repo import verification_repo
from app.services.print_service import print_service
from app.repos.print_job_repo import print_job_repo

from app.db.models import VerificationStatus
from uuid import UUID

import logging

logger = logging.getLogger(__name__)

class VerificationService:
    def __init__(self, verification_repo, print_service, print_job_repo):
        self.verification_repo = verification_repo
        self.print_service = print_service
        self.print_repo = print_job_repo

    def verify_file(self, db: Session, verification: VerificationCreate, verifier_id: UUID):


        logger.info(
            "Verification attempt",
            extra={
                "file_id": str(verification.file_id),
                "verifier_id": str(verifier_id),
                "status": verification.status.value,
            },
        )
        # Guard: prevent duplicate prints
        if verification.status == VerificationStatus.approved:
            if self.print_repo.has_active_job(db, verification.file_id):

                logger.warning(
                    "Verification blocked: active print job exists",
                    extra={
                        "file_id": str(verification.file_id),
                        "verifier_id": str(verifier_id),
                    },
                )
                raise HTTPException(
                    400,
                    "File already has an active print job"
                )
        
        verification_repo.create(db, verification.file_id, verifier_id, verification.status, verification.comments)


        logger.info(
            "Verification recorded",
            extra={
                "file_id": str(verification.file_id),
                "verifier_id": str(verifier_id),
                "status": verification.status.value,
            },
        )

        # EVENT: enqueue print job AFTER approval
        if verification.status == VerificationStatus.approved:

            logger.info(
                "Verification approved — enqueuing print job",
                extra={
                    "file_id": str(verification.file_id),
                    "verifier_id": str(verifier_id),
                },
            )

            self.print_service.enqueue_print(
                db,
                model_file_id=verification.file_id,
                user_id=verifier_id,
            )
        
        return verification
        

verification_service = VerificationService(verification_repo, print_service, print_job_repo)