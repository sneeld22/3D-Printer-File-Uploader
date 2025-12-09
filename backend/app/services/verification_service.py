from sqlalchemy.orm import Session
from app.schemas.verifications import VerificationCreate
from app.repos.verification_repo import verification_repo
from uuid import UUID

class VerificationService:
    def verify_file(self, db: Session, verification: VerificationCreate, verifier_id: UUID):
        verification_repo.create(db, verification.file_id, verifier_id, verification.status, verification.comments)

verification_service = VerificationService()