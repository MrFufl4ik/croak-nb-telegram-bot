from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InputMediaPhoto

from src.core.telegram_bot import get_cached_image
from src.dynamic import image
from src.dynamic.config import localisation_config
from src.keyboards.status_keyboard import get_keyboard

router = Router()

__start_menu_localisation: dict = localisation_config["status_menu"]

@router.callback_query(lambda c: c.data == "status_menu")
async def __on_callback(callback: CallbackQuery):
    media = await get_cached_image(image.start_menu_image)
    caption = __start_menu_localisation.get("caption", "error 500")
    caption = caption.format(200, "10.02.26")
    keyboard = await get_keyboard()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=media,
            caption=caption,
            parse_mode=ParseMode.HTML
        ),
        reply_markup=keyboard
    )