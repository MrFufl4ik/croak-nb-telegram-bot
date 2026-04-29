from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InputMediaPhoto

from src.core.telegram_bot import get_cached_image
from src.data.bot_user import get_bot_user_by_telegram_id
from src.dynamic import image
from src.dynamic.config import localisation_config
from src.keyboards.admin_keyboard import get_keyboard

router = Router()

__admin_menu_localisation: dict = localisation_config["admin_menu"]

@router.callback_query(lambda c: c.data == "admin_menu")
async def __on_callback(callback: CallbackQuery):
    bot_user = await get_bot_user_by_telegram_id(callback.from_user.id)
    if not bot_user.is_admin: return

    media = await get_cached_image(image.start_menu_image)
    caption = __admin_menu_localisation.get("caption", "error 500")

    keyboard = await get_keyboard(bot_user)
    await callback.message.edit_media(
        InputMediaPhoto(
            media=media,
            caption=caption,
            parse_mode=ParseMode.HTML
        ),
        reply_markup=keyboard
    )
