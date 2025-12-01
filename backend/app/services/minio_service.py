from minio import Minio
from minio.error import S3Error
from fastapi import HTTPException
from app.core.config import settings
import uuid
from io import BytesIO
from typing import List, Dict

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
        
    def list_objects(self) -> list[dict]:
        objects = self.client.list_objects(bucket_name=self.bucket_name, recursive=True)
        result = []
        for obj in objects:
            result.append({
                "object_name": obj.object_name,
                "size": obj.size,
                "last_modified": obj.last_modified.isoformat() if obj.last_modified else None,
            })
        return result
    
    def get_file(self, object_name: str) -> dict:
        try:
            obj = self.client.stat_object(bucket_name=self.bucket_name, object_name=object_name)
            return {
                "object_name": obj.object_name,
                "size": obj.size,
                "last_modified": obj.last_modified.isoformat() if obj.last_modified else None,
            }
        except S3Error as e:
            raise HTTPException(status_code=404, detail=f"File '{object_name}' not found")


minio_service = MinioService()
