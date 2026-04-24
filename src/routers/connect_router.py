from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InputMediaPhoto

from src.core.telegram_bot import get_cached_image
from src.data.bot_user import get_bot_user_by_telegram_id
from src.data.product_user import get_product_user, is_product_user_active
from src.dynamic.config import localisation_config
from src.dynamic.connect_image import get_connect_image
from src.keyboards.connect_keyboard import get_keyboard

router = Router()

__connect_menu_localisation: dict = localisation_config["connect_menu"]

@router.callback_query(lambda c: c.data == "connect_menu")
async def __on_callback(callback: CallbackQuery):
    bot_user = await get_bot_user_by_telegram_id(callback.from_user.id)
    is_active = await is_product_user_active(bot_user)
    if not is_active: return

    product_user = await get_product_user(bot_user)
    connect_image = await get_connect_image(product_user)
    media = await get_cached_image(connect_image)
    caption = __connect_menu_localisation.get("caption", "{0}")
    caption = caption.format(product_user.connect_link)
    keyboard = await get_keyboard()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=media,
            caption=caption,
            parse_mode=ParseMode.HTML
        ),
        reply_markup=keyboard
    )