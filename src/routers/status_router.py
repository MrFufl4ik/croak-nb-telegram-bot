from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InputMediaPhoto

from src.core.telegram_bot import get_cached_image
from src.data.bot_user import get_bot_user_by_telegram_id
from src.data.product_user import get_product_user, is_product_user_exists, \
    is_product_user_active, get_final_cost_by_bot_user
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
    subscription_day_count = __product_config.get("subscription_day_count", 30)
    if is_active:
        product_user = await get_product_user(bot_user)
        caption = __status_menu_localisation.get("caption_with_active_product", "error 500")
        expires_dt = product_user.expires_at
        cost = await get_final_cost_by_bot_user(bot_user)
        caption = caption.format(cost, subscription_day_count, expires_dt.strftime("%d.%m.%Y"))
    else:
        cost = await get_final_cost_by_bot_user(bot_user)
        caption = __status_menu_localisation.get("caption_without_active_product", "error 500")
        caption = caption.format(cost, subscription_day_count)

    keyboard = await get_keyboard()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=media,
            caption=caption,
            parse_mode=ParseMode.HTML
        ),
        reply_markup=keyboard
    )