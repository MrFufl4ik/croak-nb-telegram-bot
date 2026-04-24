from pathlib import Path

import qrcode.constants
from PIL.Image import Image, Resampling
from qrcode.main import QRCode

from src.data.bot_user import get_bot_user_by_id
from src.data.product_user import ProductUser
from src.dynamic.image import create_folder_path_wrapper, __image_folder_path, empty_image

__connect_image_folder_path = create_folder_path_wrapper(__image_folder_path / "connect_image")

async def get_connect_image(product_user: ProductUser) -> Path:
    connect_link: str = product_user.connect_link
    qr = QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=0
    )
    qr.add_data(connect_link)
    qr.make(fit=True)
    img: Image = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((452, 452), Resampling.NEAREST)
    bot_user = await get_bot_user_by_id(product_user.bot_user_id)
    img.save(__connect_image_folder_path / f"{bot_user.telegram_id}.png")

    return empty_image