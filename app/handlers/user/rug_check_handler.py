from aiogram import Router, Bot, F
from aiogram.types import Message, ContentType

import pprint
import logging

from app.filters.security_filter import security_decorator
from app.config import Config
from app.tools.token_analitic.token_analyzer import token_analyzer, get_link_keyboard

router = Router()


async def change_message(bot, progress_msg, msg, keyboard):
    await progress_msg.delete()
    if keyboard is None:
        await bot.send_message(
            text=msg,
            chat_id=progress_msg.chat.id,
        )
    else:
        keyb = await get_link_keyboard(keyboard)
        await bot.send_message(
            text=msg,
            chat_id=progress_msg.chat.id,
            reply_markup=keyb,
        )


@router.message(F.content_type.in_({ContentType.TEXT}))
@security_decorator(group_id="-1001569965543")
async def token_cmd_handler(message: Message, bot: Bot, config: Config):
    try:
        if message.text:
            if len(message.text) == 42 and message.text.startswith("0"):
                address = message.text
                (
                    msg,
                    keyboard,
                    bot,
                    progress_msg,
                ) = await token_analyzer.analyze(message, address, bot, config)
                await change_message(bot, progress_msg, msg, keyboard)
            elif message.text.startswith("0") and (
                len(message.text) < 42 or len(message.text) > 42
            ):
                await message.answer(
                    "📵 <b> We're sorry, but the token you provided appears to be invalid.</b>"
                )
            elif message.text == "🫂 Social Media":
                msg = (
                    "🕊️ X: \nhttps://twitter.com/zeroxsai\n\n"
                    "🌐 Website: \nhttps://0xs.ai\n\n"
                    "✈️  Telegram: \nhttps://t.me/zeroxsai\n\n"
                )
                await message.answer(msg)
            elif message.text == "💎 Advertisement":
                msg = (
                    "🗞️ Looking got good advertisement? 🗞️\n"
                    "🚀 Get in touch with @Botindeed! 🚀"
                )
                await message.answer(msg)
            elif message.text == "⛓️ Chain Support":
                msg = (
                    "⛓️ <b>Supported Chains</b> ⛓️\n\n"
                    "1. <b>Shibarium (SHIB) 🔗</b>\n"
                    "2. <b>Ethereum (ETH) 🔗</b>\n"
                    "3. <b>Binance Smart Chain (BSC) 🔗</b>\n"
                    "4. <b>Optimism (OL) 🔗</b>\n"
                    "5. <b>Cronos (CRONOS) 🔗</b>\n"
                    "6. <b>OKExChain (OKC) 🔗</b>\n"
                    "7. <b>Gnosis (GNOSIS) 🔗</b>\n"
                    "8. <b>Polygon (MATIC) 🔗</b>\n"
                    "9. <b>Fantom Opera (FTM) 🔗</b>\n"
                    "10. <b>zkSync (zkSYNC) 🔗</b>\n"
                    "11. <b>KCC (KCC) 🔗</b>\n"
                    "12. <b>Avalanche (AVAX) 🔗</b>\n"
                    "13. <b>Arbitrum (ARBITRUM) 🔗</b>\n"
                    "14. <b>Base (BASE) 🔗</b>\n"
                    "15. <b>Harmony (HARMONY) 🔗</b>\n"
                    "16. <b>Ethereum Wanchain (ETHW) 🔗</b>\n"
                    "16. <b>Ethereum Wanchain (ETHW) 🔗</b>\n"
                    "18. <b>Tron (TRON) 🔗</b>\n"
                )
                await message.answer(msg)

    except Exception as e:
        answer_msg = (
            "📵 <b> We're sorry, but the token you provided appears"
            " to be invalid or error appeared.\n Please try again later. </b>"
        )
        await message.answer(answer_msg)
        logging.error(repr(e))
