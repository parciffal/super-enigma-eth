from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

# from aiogram.utils.text_decorations import html_decoration as hd

from app.config import Config
from app.keyboards.inline.admin.menu_kb import start_menu

import logging


router = Router()


@router.message(Command("admin"))
async def admin_cmd(message: Message, config: Config):
    try:
        keyboard = await start_menu()
        await message.answer("Select section to edit", reply_markup=keyboard)
    except Exception as e:
        logging.error(e)
