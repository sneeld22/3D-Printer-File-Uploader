import os
import unittest
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import Mock, patch
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

os.environ.setdefault("DATABASE_URL", "postgresql://postgres:test@localhost:5432/app")
os.environ.setdefault("MINIO_ENDPOINT", "localhost:9000")
os.environ.setdefault("MINIO_ACCESS_KEY", "test")
os.environ.setdefault("MINIO_SECRET_KEY", "test")
os.environ.setdefault("MINIO_BUCKET", "test")
os.environ.setdefault("ADMIN_USER", "admin")
os.environ.setdefault("JWT_SECRET", "0123456789abcdef0123456789abcdef")
os.environ.setdefault("LDAP_SERVER", "ldap.example.test")
os.environ.setdefault("LDAP_DOMAIN", "EXAMPLE")

from app.api.routes import files as file_routes  # noqa: E402
from app.db.base import Base  # noqa: E402
from app.db.session import engine as app_engine  # noqa: E402
from app.db.models import (  # noqa: E402
    ModelFile, ModelVerification, PrintJob, PrintStatus, RoleEnum, User, UserRole, VerificationStatus,
)
from app.dependencies import require_role  # noqa: E402
from app.repos.print_job_repo import print_job_repo  # noqa: E402
from app.repos.verification_repo import verification_repo  # noqa: E402
from app.services.file_service import FileService  # noqa: E402
from app.services.print_service import PrintService, print_service  # noqa: E402
from app.services.verification_service import VerificationService  # noqa: E402
from app.schemas.verifications import VerificationCreate  # noqa: E402
from app.utils.upload_validation import normalize_upload_filename  # noqa: E402
from app.utils.bootstrap import bootstrap_roles  # noqa: E402


def user_with_roles(*roles):
    return SimpleNamespace(id=uuid4(), roles=[SimpleNamespace(role_id=role) for role in roles])


class ReleaseGuardTests(unittest.TestCase):
    def test_configured_postgres_driver_is_installed_driver(self):
        self.assertEqual(app_engine.url.drivername, "postgresql+psycopg2")

    def test_verification_permission_rejects_uploaders(self):
        guard = require_role([RoleEnum.verifier, RoleEnum.admin])
        with self.assertRaises(HTTPException) as error:
            guard(user_with_roles(RoleEnum.uploader))
        self.assertEqual(error.exception.status_code, 403)
        self.assertIsNotNone(guard(user_with_roles(RoleEnum.verifier)))

    def test_file_read_requires_owner_or_privileged_role(self):
        service = FileService()
        owner = user_with_roles(RoleEnum.uploader)
        file_record = SimpleNamespace(id=uuid4(), uploader_id=owner.id)
        service.repo = Mock()
        service.repo.get_by_id.return_value = file_record

        self.assertIs(service._get_readable_file(None, file_record.id, owner), file_record)
        with self.assertRaises(HTTPException) as error:
            service._get_readable_file(None, file_record.id, user_with_roles(RoleEnum.uploader))
        self.assertEqual(error.exception.status_code, 403)
        self.assertIs(
            service._get_readable_file(None, file_record.id, user_with_roles(RoleEnum.verifier)),
            file_record,
        )

    def test_upload_rejects_invalid_type_and_oversize(self):
        with self.assertRaises(ValueError):
            normalize_upload_filename("script.exe")
        self.assertEqual(normalize_upload_filename(r"C:\models\part.STL"), "part.STL")

        user = user_with_roles(RoleEnum.uploader)
        invalid = SimpleNamespace(filename="script.exe", file=BytesIO(b"payload"))
        with self.assertRaises(HTTPException) as error:
            file_routes.upload_file(invalid, db=Mock(), user=user)
        self.assertEqual(error.exception.status_code, 400)

        large_file = Mock()
        large_file.tell.return_value = 50 * 1024 * 1024 + 1
        oversized = SimpleNamespace(filename="part.stl", file=large_file)
        with self.assertRaises(HTTPException) as error:
            file_routes.upload_file(oversized, db=Mock(), user=user)
        self.assertEqual(error.exception.status_code, 413)

        stream = BytesIO(b"solid part\nendsolid part\n")
        upload = SimpleNamespace(filename="part.stl", file=stream)
        with patch.object(file_routes.file_service, "upload_file") as save:
            file_routes.upload_file(upload, db=None, user=user)
            save.assert_called_once_with(None, stream, "part.stl", len(stream.getvalue()), user.id)

    def test_print_job_requires_approval_and_no_active_job(self):
        db = Mock()
        db.query.return_value.filter.return_value.with_for_update.return_value.first.return_value = object()
        repo = Mock()
        service = PrintService(repo)
        file_id = uuid4()
        user_id = uuid4()

        with patch("app.services.print_service.verification_repo.get_latest") as latest:
            latest.return_value = None
            with self.assertRaises(HTTPException) as error:
                service.enqueue_print(db, file_id, user_id)
            self.assertEqual(error.exception.status_code, 400)

            latest.return_value = SimpleNamespace(status=VerificationStatus.approved)
            repo.has_active_job.return_value = True
            with self.assertRaises(HTTPException) as error:
                service.enqueue_print(db, file_id, user_id)
            self.assertEqual(error.exception.status_code, 409)

            repo.has_active_job.return_value = False
            service.enqueue_print(db, file_id, user_id)
            repo.create.assert_called_once_with(db, file_id, user_id)

    def test_approval_and_queue_are_atomic(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        with Session(engine) as db:
            verifier = User(username="verifier")
            first_file = ModelFile(filename="first.stl", minio_path="first.stl", size=10, uploader=verifier)
            second_file = ModelFile(filename="second.stl", minio_path="second.stl", size=10, uploader=verifier)
            db.add_all([verifier, first_file, second_file])
            db.commit()

            service = VerificationService(verification_repo, print_service, print_job_repo)
            decision = VerificationCreate(file_id=first_file.id, status=VerificationStatus.approved)
            saved = service.verify_file(db, decision, verifier.id)
            self.assertEqual(saved.status, VerificationStatus.approved)
            jobs = db.query(PrintJob).filter(PrintJob.model_file_id == first_file.id).all()
            self.assertEqual(len(jobs), 1)
            self.assertEqual(jobs[0].status, PrintStatus.queued)

            failing_print_service = Mock()
            failing_print_service.enqueue_print.side_effect = RuntimeError("queue unavailable")
            service = VerificationService(verification_repo, failing_print_service, print_job_repo)
            decision = VerificationCreate(file_id=second_file.id, status=VerificationStatus.approved)
            with self.assertRaises(RuntimeError):
                service.verify_file(db, decision, verifier.id)
            self.assertEqual(
                db.query(ModelVerification).filter(ModelVerification.model_file_id == second_file.id).count(),
                0,
            )
        engine.dispose()

    def test_configured_roles_are_bootstrapped_idempotently(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        with Session(engine) as db:
            with patch("app.utils.bootstrap.settings") as settings:
                settings.ADMIN_USER = "admin"
                settings.VERIFIER_USERS = "teacher1, teacher2"
                bootstrap_roles(db)
                bootstrap_roles(db)

            self.assertEqual(db.query(User).count(), 3)
            self.assertEqual(db.query(UserRole).count(), 3)
            self.assertEqual(
                db.query(UserRole).join(User).filter(User.username == "admin").one().role_id,
                RoleEnum.admin,
            )
        engine.dispose()


if __name__ == "__main__":
    unittest.main()
