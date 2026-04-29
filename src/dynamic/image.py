import os
from pathlib import Path

__image_folder_path = Path(os.getcwd()) / "dynamic" / "image"

empty_image = __image_folder_path / "empty.png"
def get_image(path: Path) -> Path:
    return path if path.exists() else empty_image
def create_folder_path_wrapper(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

start_menu_image = get_image(__image_folder_path / "start_menu.png")
status_menu_image = get_image(__image_folder_path / "status_menu.png")
offer_menu_image = get_image(__image_folder_path / "offer_menu.png")