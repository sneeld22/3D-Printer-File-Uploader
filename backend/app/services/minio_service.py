from minio import Minio
from minio.error import S3Error
from fastapi import HTTPException
from app.core.config import settings
import uuid
from io import BytesIO

class MinioService:
    def __init__(self):
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket_name = settings.MINIO_BUCKET

        # Ensure bucket exists
        if not self.client.bucket_exists(bucket_name=self.bucket_name):
            self.client.make_bucket(bucket_name=self.bucket_name)

    def generate_object_name(self, filename: str) -> str:
        ext = filename.split(".")[-1]
        return f"{uuid.uuid4()}.{ext}"

    def upload(self, file_obj: bytes, object_name: str, length: int):
        try:
            data_stream = BytesIO(file_obj)  # wrap bytes in BytesIO to provide .read()
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=data_stream,
                length=length,
                part_size=10 * 1024 * 1024,
            )
        except S3Error as e:
            raise HTTPException(
                status_code=500,
                detail=f"MinIO upload error: {str(e)}"
            )


minio_service = MinioService()
