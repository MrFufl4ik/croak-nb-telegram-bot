import os
from pathlib import Path

__image_folder_path = Path(os.getcwd()) / "dynamic" / "image"

empty_image = __image_folder_path / "empty.png"
def get_image(path: Path) -> Path:
    return path if path.exists() else empty_image

start_menu_image = get_image(__image_folder_path / "start_menu.png")