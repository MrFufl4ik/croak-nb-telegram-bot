from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InputMediaPhoto

from src.core.telegram_bot import get_cached_image
from src.dynamic import image
from src.dynamic.config import localisation_config
from src.keyboards.prolong_keyboard import get_keyboard

router = Router()

__prolong_menu_localisation: dict = localisation_config["prolong_menu"]

@router.callback_query(lambda c: c.data == "prolong_menu")
async def __on_callback(callback: CallbackQuery):
    media = await get_cached_image(image.prolong_menu_image)

    caption = __prolong_menu_localisation.get("caption", "error 500")

    keyboard = await get_keyboard()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=media,
            caption=caption,
            parse_mode=ParseMode.HTML
        ),
        reply_markup=keyboard
    )