from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command


import logging


from app.config import Config
from app.filters.is_owner import PrivateChatFilter


router = Router()


@router.message(Command("start"), PrivateChatFilter())
async def token_cmd_handler(message: Message, config: Config, bot: Bot):
    try:
        bot_info = await bot.get_me()
        msg = (
            f"Welcome to <b>@{bot_info.username}</b> bot \n"
            f"This bot generates an analysis report for <b>BSC, ETH, OKC,"
            f" Optimism, Cronos, HECO, Polygon, Fantom, KCC, Avalanche,"
            f" Harmony</b> chain's token's\n"
            f"\n<b>How to use bot?</b>\n"
            f"Send contract address, the bot will determine which chain it"
            f" is and then generates an analysis report.\n"
            f"\n<b>How to add the bot to Group?</b>\n"
            f"Add @{bot_info.username} to your group and then give it"
            f" admin rights. It is ready to use.\n"
        )
        await message.answer(msg, parse_mode="html")
    except Exception as e:
        logging.error(e)
