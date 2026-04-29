from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InputMediaPhoto

from src.core.telegram_bot import get_cached_image
from src.data.bot_user import get_bot_user_by_telegram_id
from src.data.product_user import get_product_user, is_product_user_active
from src.dynamic.config import localisation_config, main_config
from src.dynamic.connect_image import get_connect_image
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

    product_user = await get_product_user(bot_user)
    connect_image = await get_connect_image(product_user)
    media = await get_cached_image(connect_image)
    caption = __connect_menu_localisation.get("caption", "{0}")
    caption = caption.format(
        product_user.connect_link,
        __connect_config.get("download_link_windows", "https://google.com"),
        __connect_config.get("download_link_linux", "https://google.com"),
        __connect_config.get("download_link_android", "https://google.com"),
    )
    keyboard = await get_keyboard(product_user.connect_link)
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