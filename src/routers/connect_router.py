from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InputMediaPhoto

from src.core.telegram_bot import get_cached_image
from src.data.bot_user import get_bot_user_by_telegram_id
from src.data.product_user import is_product_user_active
from src.dynamic import image
from src.dynamic.config import localisation_config, main_config
from src.keyboards.connect_keyboard import get_keyboard
from src.routers.start_router import init_start_message

router = Router()

__connect_menu_localisation: dict = localisation_config["connect_menu"]
__connect_config: dict = main_config["connect"]

@router.callback_query(lambda c: c.data == "connect_menu")
async def __on_callback(callback: CallbackQuery):
    bot_user = await get_bot_user_by_telegram_id(callback.from_user.id)
    is_active = await is_product_user_active(bot_user)
    if not is_active:
        await init_start_message(callback.from_user, callback.message)
        return

    media = await get_cached_image(image.connect_menu_image)
    caption = __connect_menu_localisation.get("caption", "error 500")
    caption = caption.format(
        __connect_config.get("download_link_windows", "https://google.com"),
        __connect_config.get("download_link_linux", "https://google.com"),
        __connect_config.get("download_link_android", "https://google.com"),
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

@router.callback_query(lambda c: c.data == "inactive_connect_menu")
async def __on_callback(callback: CallbackQuery):
    bot_user = await get_bot_user_by_telegram_id(callback.from_user.id)
    is_active = await is_product_user_active(bot_user)
    if is_active:
        await init_start_message(callback.from_user, callback.message)
        return
    await callback.answer(
        __connect_menu_localisation.get("inactive_answer_message", "Subscription expired!"),
        show_alert=True
    )