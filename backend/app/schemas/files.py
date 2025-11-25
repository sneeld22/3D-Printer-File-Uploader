from pydantic import BaseModel

class FileInfo(BaseModel):
    object_name: str
    size: int
    last_modified: str | None = None

class UploadedFileResponse(BaseModel):
    filename: str
    object_name: str
    message: str
