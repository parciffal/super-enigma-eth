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
from pprint import pprint

import logging


from app.config import Config
from app.filters.is_owner import PrivateChatFilter


router = Router()


@router.message(Command("start"))
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
            f"🚀 Welcome to <b>@{bot_info.username}</b> - The Token Analyzer Bot! 📊\n\n"
            f"🔍 This bot specializes in generating detailed analysis reports for tokens on various chains:\n"
            f"   - <b>Shibarium</b>\n"
            f"   - <b>BSC (Binance Smart Chain)</b>\n"
            f"   - <b>ETH (Ethereum)</b>\n"
            f"   - <b>OKC (OKCoin Chain)</b>\n"
            f"   - <b>Optimism</b>\n"
            f"   - <b>Cronos</b>\n"
            f"   - <b>Polygon</b>\n"
            f"   - <b>Fantom</b>\n"
            f"   - <b>Avalanche</b>\n"
            f"   - <b>Harmony</b>\n"
            f"And more..."
            f"\n📈 <b>How to use the bot?</b>\n"
            f"   Simply send a contract address, and the bot will automatically detect the blockchain it belongs to and generate an in-depth analysis report for you! 📄\n"
            f"\n👥 <b>How to add the bot to your Group?</b>\n"
            f"   To enable group analysis, add @{bot_info.username} as an administrator in your group, and it's ready to assist your community! 💬\n"
            f"\n📢 <b>Stay tuned for updates and new features!</b>\n"
            f"   We're constantly improving to provide you with the best token analysis experience! 🚀\n"
        )

        # Add any more specific details or features you want to highlight here.

        await message.answer(msg, parse_mode="html", reply_markup=reply_markup)
    except Exception as e:
        logging.error(e)


@router.message(Command("help"))
async def help_cmd_handler(message: Message, config: Config, bot: Bot):
    try:
        bot_info = await bot.get_me()
        msg = (
            f"🚀 Welcome to <b>@{bot_info.username}</b> - Your Instant Token Analyzer Bot! 📊\n\n"
            f"🔍 Need a quick token analysis? Look no further! Just send a contract address, and I'll provide you with an instant and fast reply! 💬\n"
            f"\n🌐 <b>Features:</b>\n"
            f"   - Real-time token data 📈\n"
            f"   - Market trends 📉\n"
            f"   - Social media 🗞️\n"
            f"   - Chain support ⛓️\n\n"
            f"💎 Looking to promote your project or product? Contact us for advertisement opportunities! 📣\n"
            f"\n❓ Always remember to DYOR (Do Your Own Research) and make informed decisions on your journey to financial success! 💪💰\n"
            f"\n🤝 Have any questions or need assistance? Feel free to ask anytime. We're here to help! 🙌"
        )

        # You can further customize or add specific details to this message as needed.

        await message.answer(msg)
    except Exception as e:
        logging.error(e)


"""
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

@router.message(F.content_type.in_({ContentType.NEW_CHAT_MEMBERS}))
async def bot_added_as_member(event, bot: Bot):
    try:
        try:
            if event.new_chat_member:
                info = await bot.get_me()
                if event.new_chat_member['id'] == info.id:
                    await bot.send_message(event.chat.id, f"🤖 {info.username} has joined the group!\nTo get started, send /start. \nTo get help send /help🚀👋")
        except:
            pass
    except Exception as e:
        logging.error(e)

