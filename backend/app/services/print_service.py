from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID

from app.db.models import PrintJob
from app.repos.print_job_repo import print_job_repo


class PrintService:

    def __init__(self, repo):
        self.repo = repo

    def enqueue_print(self, db: Session, model_file_id: UUID, user_id: UUID) -> PrintJob:
        return self.repo.create(db, model_file_id, user_id)

    def get_job(self, db: Session, job_id: UUID) -> PrintJob:
        job = self.repo.get_by_id(db, job_id)
        if not job:
            raise HTTPException(404, "Print job not found")
        return job

    def list_jobs(self, db: Session):
        return self.repo.list_all(db)

    def list_jobs_for_user(self, db: Session, user_id: UUID):
        return self.repo.list_for_user(db, user_id)

    def fetch_next_job_for_worker(self, db: Session) -> PrintJob | None:
        """
        Called by a printer worker.
        """
        job = self.repo.get_next_queued_job(db)
        if not job:
            return None

        self.repo.mark_printing(db, job)
        return job

    def mark_job_completed(self, db: Session, job_id: UUID):
        job = self.get_job(db, job_id)
        self.repo.mark_completed(db, job)

    def mark_job_failed(self, db: Session, job_id: UUID):
        job = self.get_job(db, job_id)
        self.repo.mark_failed(db, job)


print_service = PrintService(print_job_repo)
