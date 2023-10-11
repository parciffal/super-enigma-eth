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
    # try:
    #     await bot.delete_message(progress_msg.chat.id, progress_msg.message_id)
    # except Exception as e:
    #     logging.error(e)

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
            print(message.chat.id)
            if len(message.text) == 42 and message.text.startswith("0"):
                address = message.text

                # progress_msg: Message = await message.answer("🔎0xS Analyz in progress🔍")
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
                    f"🕊️ X: \nhttps://twitter.com/zeroxsai\n\n"
                    f"🌐 Website: \nhttps://0xs.ai\n\n"
                    f"✈️ Telegram: \nhttps://t.me/zeroxsai\n\n"
                )
                await message.answer(msg)
            elif message.text == "💎 Advertisement":
                msg = f"🗞️ Looking got good advertisement? 🗞️\n🚀 Get in touch with @Botindeed! 🚀"
                await message.answer(msg)
            elif message.text == "⛓️ Chain Support":
                msg = (
                    f"⛓️ <b>Supported Chains</b> ⛓️\n\n"
                    f"1. <b>Shibarium (SHIB) 🔗</b>\n"
                    f"2. <b>Ethereum (ETH) 🔗</b>\n"
                    f"3. <b>Binance Smart Chain (BSC) 🔗</b>\n"
                    f"4. <b>Optimism (OL) 🔗</b>\n"
                    f"5. <b>Cronos (CRONOS) 🔗</b>\n"
                    f"6. <b>OKExChain (OKC) 🔗</b>\n"
                    f"7. <b>Gnosis (GNOSIS) 🔗</b>\n"
                    f"8. <b>Polygon (MATIC) 🔗</b>\n"
                    f"9. <b>Fantom Opera (FTM) 🔗</b>\n"
                    f"10. <b>zkSync (zkSYNC) 🔗</b>\n"
                    f"11. <b>KCC (KCC) 🔗</b>\n"
                    f"12. <b>Avalanche (AVAX) 🔗</b>\n"
                    f"13. <b>Arbitrum (ARBITRUM) 🔗</b>\n"
                    f"14. <b>Base (BASE) 🔗</b>\n"
                    f"15. <b>Harmony (HARMONY) 🔗</b>\n"
                    f"16. <b>Ethereum Wanchain (ETHW) 🔗</b>\n"
                    f"16. <b>Ethereum Wanchain (ETHW) 🔗</b>\n"
                    f"18. <b>Tron (TRON) 🔗</b>\n"
                )
                await message.answer(msg)

    except Exception as e:
        await message.answer(
            "📵 <b> We're sorry, but the token you provided appears to be invalid or error appeared.\n Please try again later. </b>"
        )
        logging.error(repr(e))
