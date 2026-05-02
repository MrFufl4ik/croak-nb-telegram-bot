import re

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from src.core.telegram_bot import get_cached_image, get_telegram_bot
from src.data.bot_user import get_bot_user_by_telegram_id
from src.dynamic import image
from src.dynamic.config import localisation_config
from src.keyboards.admin_keyboard import get_keyboard, get_userinfo_keyboard

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


@router.message(Command("userinfo"))
async def __on_callback(message: Message):
    bot_user = await get_bot_user_by_telegram_id(message.from_user.id)
    if not bot_user.is_admin: return
    regex_pattern = r"^/userinfo (\d+)$"
    if not re.fullmatch(regex_pattern, message.text): return
    match = re.match(regex_pattern, message.text)
    user_id = match.group(1)
    telegram_bot = get_telegram_bot()
    chat_info = await telegram_bot.get_chat(user_id)
    result = []
    result.append("========================")
    result.append("<u>id</u> | {0}".format(chat_info.id))
    result.append("<u>username</u> | {0}".format(chat_info.username))
    result.append("<u>full name</u> | {0}".format(chat_info.full_name))
    result.append("<u>bio</u> | {0}".format(chat_info.bio))
    if chat_info.birthdate is not None:
        birthdate_caption = "{}.{}.{}".format(
            chat_info.birthdate.day,
            chat_info.birthdate.month,
            chat_info.birthdate.year
        )
        result.append("<u>birthdate</u> | {0}".format(birthdate_caption))

    keyboard = await get_userinfo_keyboard(chat_info)
    await message.answer(
        text='\n'.join(result),
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )