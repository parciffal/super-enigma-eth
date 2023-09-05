from aiogram import Router, Bot, F
from aiogram.types import Message, ContentType


import logging


from app.config import Config
from app.tools.token_analitic import gopluslabs_manager
from app.tools.token_analitic.gopluslabs import get_link_keyboard

router = Router()


@router.message(F.content_type.in_({ContentType.TEXT}))
async def token_cmd_handler(message: Message, config: Config, bot: Bot):
    try:
        if message.text:
            if len(message.text) == 42 and message.text.startswith("0"):
                address = message.text
                msg, keyboard = await gopluslabs_manager.get_token_security(
                    address, bot
                )
                if keyboard is None:
                    await message.answer(msg, parse_mode="html")
                else:
                    keyb = await get_link_keyboard(keyboard)
                    await message.answer(msg, parse_mode="html", reply_markup=keyb)
            if message.text.startswith("0") and (
                len(message.text) < 42 or len(message.text) > 42
            ):
                await message.answer(
                    "📵 <b> We're sorry, but the token you provided appears to be invalid.</b>"
                )
    except Exception as e:
        await message.answer(
            "📵 <b> We're sorry, but the token you provided appears to be invalid or error appeared.\n Please try again later. </b>"
        )
        logging.error(e)
