import shutil
import os

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_files(file_paths):
    """
    file_paths: list of file paths selected by user
    """
    saved_files = []

    for path in file_paths:
        filename = os.path.basename(path)
        dest = os.path.join(UPLOAD_DIR, filename)
        shutil.copy(path, dest)
        saved_files.append(dest)

    return saved_files