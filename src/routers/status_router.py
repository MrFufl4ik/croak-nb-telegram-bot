from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InputMediaPhoto

from src.core.telegram_bot import get_cached_image
from src.data.bot_user import get_bot_user_by_telegram_id
from src.data.product_user import get_product_user, is_product_user_exists, \
    is_product_user_active
from src.dynamic import image
from src.dynamic.config import localisation_config, main_config
from src.keyboards.status_keyboard import get_keyboard

router = Router()

__status_menu_localisation: dict = localisation_config["status_menu"]
__product_config: dict = main_config["product"]

@router.callback_query(lambda c: c.data == "status_menu")
async def __on_callback(callback: CallbackQuery):
    media = await get_cached_image(image.status_menu_image)
    bot_user = await get_bot_user_by_telegram_id(callback.from_user.id)
    is_active = await is_product_user_active(bot_user)
    default_cost = __product_config.get("default_cost", 100)
    if is_active:
        product_user = await get_product_user(bot_user)
        caption = __status_menu_localisation.get("caption_with_active_product", "error 500")
        expires_dt = product_user.expires_at
        cost = product_user.cost if product_user.cost is not None else default_cost
        caption = caption.format(cost, expires_dt.strftime("%d.%m.%Y"))
    else:
        is_exists = await is_product_user_exists(bot_user)
        caption = __status_menu_localisation.get("caption_without_active_product", "error 500")
        if is_exists:
            product_user = await get_product_user(bot_user)
            cost = product_user.cost if product_user.cost is not None else default_cost
            caption = caption.format(cost)
        else: caption = caption.format(default_cost)

    keyboard = await get_keyboard()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=media,
            caption=caption,
            parse_mode=ParseMode.HTML
        ),
        reply_markup=keyboard
    )