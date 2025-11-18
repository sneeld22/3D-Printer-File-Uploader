import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from minio import Minio
from minio.error import S3Error

app = FastAPI()

# Configure your MinIO client
minio_client = Minio(
    "localhost:9000",  # Replace with your MinIO endpoint
    access_key="minio_access_key",  # Your MinIO access key
    secret_key="minio_secret_key",  # Your MinIO secret key
    secure=False  # True if using HTTPS
)

BUCKET_NAME = "uploads"

# Ensure bucket exists on startup
@app.on_event("startup")
def startup_event():
    found = minio_client.bucket_exists(BUCKET_NAME)
    if not found:
        minio_client.make_bucket(BUCKET_NAME)
        print(f"Created bucket '{BUCKET_NAME}'")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Generate a unique filename
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"

    try:
        # Upload file stream to MinIO
        file_content = await file.read()
        file_size = len(file_content)
        
        minio_client.put_object(
            bucket_name=BUCKET_NAME,
            object_name=unique_filename,
            data=bytes(file_content),
            length=file_size,
            content_type=file.content_type
        )
    except S3Error as err:
        raise HTTPException(status_code=500, detail=f"MinIO error: {err}")

    return {
        "original_filename": file.filename,
        "stored_filename": unique_filename,
        "content_type": file.content_type,
        "size": file_size,
    }
