from pathlib import Path

import qrcode.constants
from PIL import Image
from qrcode.main import QRCode

from src.core.hashing import async_sha256
from src.data.bot_user import get_bot_user_by_id
from src.data.product_user import ProductUser
from src.dynamic.image import create_folder_path_wrapper, __image_folder_path, empty_image, get_image

__connect_image_folder_path = create_folder_path_wrapper(__image_folder_path / "connect_image")
__source_image = get_image(__connect_image_folder_path / "source.png")

async def get_connect_image_by_connect_link(connect_link) -> Path:
    result_image_file_name = "{0}.png"
    result_image_file_name = result_image_file_name.format(await async_sha256(connect_link.encode('utf-8')))
    result_image_path: Path = __connect_image_folder_path / result_image_file_name
    if result_image_path.exists(): return result_image_path

    qr = QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=0
    )
    qr.add_data(connect_link)
    qr.make(fit=True)
    qr_image: Image.Image = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    qr_image = qr_image.resize((452, 453), Image.Resampling.NEAREST)

    background_image: Image.Image = Image.open(__source_image).convert("RGB")
    background_image.paste(qr_image, (197, 236))
    background_image.save(result_image_path)

    return Path(result_image_path)

async def get_connect_image(product_user: ProductUser) -> Path:
    result = await get_connect_image_by_connect_link(product_user.connect_link)
    return result