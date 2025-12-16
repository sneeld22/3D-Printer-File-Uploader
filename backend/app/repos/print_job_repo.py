# app/repos/print_job_repo.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from uuid import UUID

from app.db.models import PrintJob, PrintStatus


class PrintJobRepository:

    def create(self, db: Session, model_file_id: UUID, user_id: UUID) -> PrintJob:
        job = PrintJob(
            model_file_id=model_file_id,
            requested_by=user_id,
            status=PrintStatus.queued,
            created_at=datetime.utcnow()
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    def get_by_id(self, db: Session, job_id: UUID) -> PrintJob | None:
        return db.query(PrintJob).filter(PrintJob.id == job_id).first()

    def list_all(self, db: Session) -> list[PrintJob]:
        return db.query(PrintJob).order_by(PrintJob.created_at.desc()).all()


    def get_next_queued_job(self, db: Session) -> PrintJob | None:
        """
        Atomically fetch the next queued job and lock it.
        PostgreSQL ONLY.
        """
        stmt = (
            select(PrintJob)
            .where(PrintJob.status == PrintStatus.queued)
            .order_by(PrintJob.created_at.asc())
            .with_for_update(skip_locked=True)
            .limit(1)
        )

        result = db.execute(stmt).scalars().first()
        return result
    
    def has_active_job(self, db: Session, file_id: UUID) -> bool:
        return (
            db.query(PrintJob)
            .filter(
                PrintJob.model_file_id == file_id,
                PrintJob.status.in_([PrintStatus.queued, PrintStatus.printing])
            )
            .count()
            > 0
        )

    def mark_printing(self, db: Session, job: PrintJob):
        job.status = PrintStatus.printing
        job.started_at = datetime.utcnow()
        db.commit()

    def mark_completed(self, db: Session, job: PrintJob):
        job.status = PrintStatus.completed
        job.completed_at = datetime.utcnow()
        db.commit()

    def mark_failed(self, db: Session, job: PrintJob):
        job.status = PrintStatus.failed
        db.commit()


print_job_repo = PrintJobRepository()
