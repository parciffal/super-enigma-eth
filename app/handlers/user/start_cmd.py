from aiogram import Router, Bot, F
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ContentType,
    Message,
    ChatMemberUpdated,
)
from aiogram.filters import Command
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter,
    IS_NOT_MEMBER,
    MEMBER,
)

import logging


from app.config import Config
from app.filters.is_owner import PrivateChatFilter


router = Router()


@router.message(Command("start"), PrivateChatFilter())
async def token_cmd_handler(message: Message, config: Config, bot: Bot):
    try:
        bot_info = await bot.get_me()
        kl = []
        kl.append(
            [
                KeyboardButton(text="🫂 Social Media"),
                KeyboardButton(text="💎 Advertisement"),
            ]
        )
        kl.append([KeyboardButton(text="⛓️ Chain Support")])
        reply_markup = ReplyKeyboardMarkup(keyboard=kl, resize_keyboard=True)
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
        await message.answer(msg, parse_mode="html", reply_markup=reply_markup)
    except Exception as e:
        logging.error(e)


@router.message(Command("help"), PrivateChatFilter())
async def help_cmd_handler(message: Message, config: Config, bot: Bot):
    try:
        bot_info = await bot.get_me()
        msg = (
            f"🔍 @{bot_info.username} you can analyze token with an instant and fast reply.\n"
            f"\n🫂 Social Media - Check for the updates\n"
            f"💎 Advertisement - Contact for ads\n"
            f"⛓️ Chain Support - List supported chains\n\n"
            f"❓Always DYOR and make yourself rich! 😉"
        )
        await message.answer(msg)
    except Exception as e:
        logging.error(e)


@router.message(F.content_type.in_({ContentType.TEXT}))
async def reply_handler(message: Message, config: Config, bot: Bot):
    try:
        if message.text:
            if message.text == "🫂 Social Media":
                msg = (
                    f"🕊️ X: \nhttps://twitter.com/zeroxsai\n\n"
                    f"🌐 Website: \nhttps://0xs.ai\n\n"
                    f"✈️ Telegram: \nhttps://t.me/zeroxsai\n\n"
                )
                await message.answer(msg)
            elif message.text == "💎 Advertisement":
                msg = f"🗞️Looking got good advertisement?🗞️\n🚀Get in touch with @Botindeed! 🚀"
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
        logging.error(e)

"""
@router.message()
async def bot_added_as_member(event, bot: Bot):
    try:
        from pprint import pprint

        pprint(event)
        try:
            if event.new_chat_member:
                await bot.send_message(event.chat.id, "Bot added to group")
        except:
            pass
    except Exception as e:
        logging.error(e)
"""
