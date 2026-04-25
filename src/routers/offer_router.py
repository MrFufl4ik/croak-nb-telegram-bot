from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InputMediaPhoto

from src.core.telegram_bot import get_cached_image
from src.data.bot_user import get_bot_user_by_telegram_id
from src.dynamic import image
from src.dynamic.config import localisation_config
from src.keyboards.offer_keyboard import get_keyboard

router = Router()

__offer_menu_localisation: dict = localisation_config["offer_menu"]

@router.callback_query(lambda c: c.data == "offer_menu")
async def __on_callback(callback: CallbackQuery):
    media = await get_cached_image(image.start_menu_image)
    caption = __offer_menu_localisation.get("caption", "Offer not defined!")

    keyboard = await get_keyboard()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=media,
            caption=caption,
            parse_mode=ParseMode.HTML
        ),
        reply_markup=keyboard
    )