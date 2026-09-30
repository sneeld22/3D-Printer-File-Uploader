MAX_FILE_SIZE = 50 * 1024 * 1024
ALLOWED_EXTENSIONS = {".stl", ".3mf"}


def normalize_upload_filename(filename: str | None) -> str:
    if not filename:
        raise ValueError("A filename is required")

    name = filename.replace("\\", "/").rsplit("/", 1)[-1]
    if not name or len(name) > 255 or any(ord(char) < 32 for char in name):
        raise ValueError("Invalid filename")
    if not any(name.lower().endswith(extension) for extension in ALLOWED_EXTENSIONS):
        raise ValueError("Only .stl and .3mf files are allowed")
    return name
