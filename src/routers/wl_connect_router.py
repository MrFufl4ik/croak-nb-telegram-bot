from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InputMediaPhoto

from src.core.telegram_bot import get_cached_image
from src.data.bot_user import get_bot_user_by_telegram_id
from src.data.product_user import is_product_user_active
from src.dynamic.config import localisation_config, main_config
from src.dynamic.connect_image import get_connect_image_by_connect_link
from src.keyboards.simple_connect_keyboard import get_keyboard
from src.routers.start_router import init_start_message

router = Router()

__wl_connect_menu_localisation: dict = localisation_config["wl_connect_menu"]
__wl_connect_config: dict = main_config["wl_connect"]

@router.callback_query(lambda c: c.data == "wl_connect_menu")
async def __on_callback(callback: CallbackQuery):
    bot_user = await get_bot_user_by_telegram_id(callback.from_user.id)
    is_active = await is_product_user_active(bot_user)
    if not is_active:
        await init_start_message(callback.from_user, callback.message)
        return

    connect_link = __wl_connect_config.get("connect_link", "https://google.com")
    connect_image = await get_connect_image_by_connect_link(connect_link)
    media = await get_cached_image(connect_image)
    caption = __wl_connect_menu_localisation.get("caption", "{0}")
    caption = caption.format(
        connect_link
    )
    keyboard = await get_keyboard()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=media,
            caption=caption,
            parse_mode=ParseMode.HTML
        ),
        reply_markup=keyboard
    )