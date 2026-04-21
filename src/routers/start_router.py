from pyexpat.errors import messages

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, User, CallbackQuery, InputMediaPhoto

from src.core.telegram_bot import get_cached_image
from src.dynamic import image
from src.dynamic.config import localisation_config
from src.keyboards.start_keyboard import get_keyboard

router = Router()

__start_menu_localisation: dict = localisation_config["start_menu"]

@router.message(CommandStart())
async def start_command_handler(message: Message):
    user = message.from_user
    media = await get_cached_image(image.start_menu_image)
    caption = __start_menu_localisation.get("caption", "error 500")
    caption = caption.format(user.full_name)
    keyboard = get_keyboard()
    await message.answer_photo(
        photo=media,
        caption=caption,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@router.callback_query(lambda c: c.data == "start_menu")
async def __on_callback(callback: CallbackQuery):
    user = callback.from_user
    media = await get_cached_image(image.start_menu_image)
    caption = __start_menu_localisation.get("caption", "error 500")
    caption = caption.format(user.full_name)
    keyboard = get_keyboard()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=media,
            caption=caption,
            parse_mode=ParseMode.HTML
        ),
        reply_markup=keyboard
    )