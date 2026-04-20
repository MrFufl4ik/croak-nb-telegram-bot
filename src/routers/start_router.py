from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, User

from src.core.telegram_bot import get_cached_image
from src.dynamic import image
from src.dynamic.config import localisation_config

router = Router()

__start_menu_localisation: dict = localisation_config["start_menu"]

@router.message(CommandStart())
async def start_command_handler(message: Message):
    user = message.from_user
    media = await get_cached_image(image.start_menu_image)
    caption = __start_menu_localisation.get("caption", "error 500")
    caption = caption.format(
        user.full_name, #username
        "16.05.26", #expire date
        200 # nb price
    )
    await message.answer_photo(
        photo=media,
        caption=caption,
        parse_mode=ParseMode.HTML
    )