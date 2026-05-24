import os
from pathlib import Path

default_images_path = Path("data/images/")

class FileManager:
    def __init__(self):
        pass

    def save_file(file, subfolder: str) -> str:
        # Create the folder for the subfolder if it doesn't exist
        images_folder = default_images_path / subfolder
        images_folder.mkdir(parents=True, exist_ok=True)

    # Save the file to the appropriate folder
        file_path = images_folder / file.filename
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        return str(file_path)

    def get_file(file_path: str):
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                return f.read()
        return None

    def delete_file(file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
        return True
