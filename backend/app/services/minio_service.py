from minio import Minio
from minio.error import S3Error
from fastapi import HTTPException
from app.core.config import settings
import uuid
from io import BytesIO
from io import BytesIO

import logging

logger = logging.getLogger(__name__)

class MinioService:
    def __init__(self):
        logger.info("Initializing MinIO client")
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket_name = settings.MINIO_BUCKET

        # Ensure bucket exists
        if not self.client.bucket_exists(bucket_name=self.bucket_name):
            logger.info("MinIO bucket not found, creating bucket", extra={
                    "bucket": self.bucket_name
                })
            self.client.make_bucket(bucket_name=self.bucket_name)

    def generate_object_name(self, filename: str) -> str:
        ext = filename.split(".")[-1]
    
        object_name = f"{uuid.uuid4()}.{ext}"
        logger.debug(
        "Generated MinIO object name",
        extra={"file_name": filename, "object_name": object_name},
        )
        return object_name


    def upload(self, file_obj: bytes, object_name: str, length: int):

        logger.info(
        "Uploading object to MinIO",
        extra={
            "bucket": self.bucket_name,
            "object_name": object_name,
            "size": length,
        },
        )

        try:
            data_stream = BytesIO(file_obj)  # wrap bytes in BytesIO to provide .read()
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=data_stream,
                length=length,
                part_size=10 * 1024 * 1024,
            )

            logger.info(
                "MinIO upload successful",
                extra={"object_name": object_name},
            )

        except S3Error as e:
            logger.exception(
                "MinIO upload failed",
                extra={"object_name": object_name},
            )
            raise HTTPException(
                status_code=500,
                detail=f"MinIO upload error: {str(e)}"
            )
        
    def list_objects(self) -> list[dict]:
        logger.debug("Listing objects from MinIO", extra={"bucket": self.bucket_name})
        objects = self.client.list_objects(bucket_name=self.bucket_name, recursive=True)
        result = []
        for obj in objects:
            result.append({
                "object_name": obj.object_name,
                "size": obj.size,
                "last_modified": obj.last_modified.isoformat() if obj.last_modified else None,
            })

        logger.info(
            "Listed objects from MinIO",
             extra={"count": len(result)},
        )
        return result
    
    def get_file(self, object_name: str) -> dict:
        logger.debug("Fetching object metadata", extra={"object_name": object_name})
        try:
            obj = self.client.stat_object(bucket_name=self.bucket_name, object_name=object_name)
            return {
                "object_name": obj.object_name,
                "size": obj.size,
                "last_modified": obj.last_modified.isoformat() if obj.last_modified else None,
            }
        except S3Error as e:
            logger.warning(
                "MinIO object not found",
                extra={"object_name": object_name},
            )
            raise HTTPException(status_code=404, detail=f"File '{object_name}' not found")


    def stream(self, object_name: str):
        logger.info("Streaming object from MinIO", extra={"object_name": object_name})
        try:
            response = self.client.get_object(self.bucket_name, object_name)

            def file_iterator():
                for chunk in response.stream(32 * 1024):  # 32 KB chunks
                    yield chunk
                response.close()
                response.release_conn()
                logger.debug(
                    "MinIO stream closed",
                    extra={"object_name": object_name},
                )


            return file_iterator

        except S3Error as e:
            logger.exception(
                "Failed to stream MinIO object",
                extra={"object_name": object_name},
            )
            raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")
    
minio_service = MinioService()
