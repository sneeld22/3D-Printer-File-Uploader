from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID

from app.db.models import ModelFile, PrintJob, VerificationStatus
from app.repos.print_job_repo import print_job_repo
from app.repos.verification_repo import verification_repo

import logging

logger = logging.getLogger(__name__)

class PrintService:

    def __init__(self, repo):
        self.repo = repo

    def enqueue_print(self, db: Session, model_file_id: UUID, user_id: UUID) -> PrintJob:
        # Lock the file so concurrent requests cannot create duplicate active jobs.
        model_file = (
            db.query(ModelFile)
            .filter(ModelFile.id == model_file_id)
            .with_for_update()
            .first()
        )
        if not model_file:
            raise HTTPException(404, "File not found")

        latest_verification = verification_repo.get_latest(db, model_file_id)
        if not latest_verification or latest_verification.status != VerificationStatus.approved:
            raise HTTPException(400, "File must be approved before it can be queued")
        if self.repo.has_active_job(db, model_file_id):
            raise HTTPException(409, "File already has an active print job")

        logger.info(
            "Enqueuing print job",
            extra={
                "model_file_id": str(model_file_id),
                "user_id": str(user_id),
            },
        )
        try:
            job = self.repo.create(db, model_file_id, user_id)
            db.commit()
            db.refresh(job)
        except Exception:
            db.rollback()
            raise

        logger.info(
            "Print job enqueued",
            extra={
                "job_id": str(job.id),
                "model_file_id": str(model_file_id),
            },
        )

        return job
        

    def get_job(self, db: Session, job_id: UUID) -> PrintJob:
        job = self.repo.get_by_id(db, job_id)
        if not job:
            logger.warning(
                "Print job not found",
                extra={"job_id": str(job_id)},
            )
            raise HTTPException(404, "Print job not found")
        return job

    def list_jobs(self, db: Session):
        logger.debug("Listing all print jobs")
        return self.repo.list_all(db)

    def list_jobs_for_user(self, db: Session, user_id: UUID):
        logger.debug(
            "Listing print jobs for user",
            extra={"user_id": str(user_id)},
        )
        return self.repo.list_for_user(db, user_id)

    def fetch_next_job_for_worker(self, db: Session) -> PrintJob | None:
        """
        Called by a printer worker.
        """
        job = self.repo.get_next_queued_job(db)
        if not job:
           return None
        
        logger.info(
            "Assigning print job to worker",
            extra={"job_id": str(job.id)},
        )


        self.repo.mark_printing(db, job)
        return job

    def mark_job_completed(self, db: Session, job_id: UUID):
        logger.info(
            "Marking print job as completed",
            extra={"job_id": str(job_id)},
        )
        job = self.get_job(db, job_id)
        self.repo.mark_completed(db, job)

    def mark_job_failed(self, db: Session, job_id: UUID):
        logger.error(
            "Marking print job as failed",
            extra={"job_id": str(job_id)},
        )
        job = self.get_job(db, job_id)
        self.repo.mark_failed(db, job)


print_service = PrintService(print_job_repo)
