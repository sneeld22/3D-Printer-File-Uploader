import uuid
import enum
from datetime import datetime
from sqlalchemy import (
    Column, String, Enum, ForeignKey, TIMESTAMP, Text, Integer
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ------------------------------
# ENUMS
# ------------------------------
class RoleEnum(enum.Enum):
    uploader = "uploader"
    verifier = "verifier"
    downloader = "downloader"
    admin = "admin"

class VerificationStatus(enum.Enum):
    approved = "approved"
    rejected = "rejected"

class PrintStatus(enum.Enum):
    queued = "queued"
    printing = "printing"
    completed = "completed"
    failed = "failed"


# ------------------------------
# USERS & ROLES
# ------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    roles = relationship("UserRole", back_populates="user")
    uploaded_files = relationship("ModelFile", back_populates="uploader")
    verifications = relationship("ModelVerification", back_populates="verifier")
    print_jobs = relationship("PrintJob", back_populates="requester")

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password_hash)

    @staticmethod
    def hash_password(password: str):
        return pwd_context.hash(password)


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    role_id = Column(Enum(RoleEnum), primary_key=True)

    user = relationship("User", back_populates="roles")


# ------------------------------
# MODEL FILES
# ------------------------------
class ModelFile(Base):
    __tablename__ = "model_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    minio_path = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    uploader_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    uploader = relationship("User", back_populates="uploaded_files")
    verifications = relationship("ModelVerification", back_populates="model_file")
    print_jobs = relationship("PrintJob", back_populates="model_file")


# ------------------------------
# MODEL VERIFICATIONS
# ------------------------------
class ModelVerification(Base):
    __tablename__ = "model_verifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_file_id = Column(UUID(as_uuid=True), ForeignKey("model_files.id"), nullable=False)
    verifier_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(Enum(VerificationStatus), nullable=False)
    comments = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    model_file = relationship("ModelFile", back_populates="verifications")
    verifier = relationship("User", back_populates="verifications")


# ------------------------------
# PRINT JOBS
# ------------------------------
class PrintJob(Base):
    __tablename__ = "print_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_file_id = Column(UUID(as_uuid=True), ForeignKey("model_files.id"), nullable=False)
    requested_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(Enum(PrintStatus), nullable=False)
    started_at = Column(TIMESTAMP, nullable=True)
    completed_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    model_file = relationship("ModelFile", back_populates="print_jobs")
    requester = relationship("User", back_populates="print_jobs")
