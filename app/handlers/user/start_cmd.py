from aiogram import Router, Bot, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType, Message
from aiogram.filters import Command

from pprint import pprint
import logging

from app.config import Config
from app.filters.security_filter import security_decorator


router = Router()


async def message_template(bot_info):
    return (
        f"🚀 Welcome to <b>@{bot_info.username}</b> - The Token Analyzer Bot! 📊\n\n"
        f"🔍 This bot specializes in generating detailed analysis"
        f" reports for tokens on various chains:\n"
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
        f"   Simply send a contract address, and the bot will automatically detect"
        f" the blockchain it belongs to and generate an in-depth analysis report for you! 📄\n"
        f"\n👥 <b>How to add the bot to your Group?</b>\n"
        f"   To enable group analysis, add @{bot_info.username} as an "
        f"administrator in your group, and it's ready to assist your community! 💬\n"
        f"\n📢 <b>Stay tuned for updates and new features!</b>\n"
        f"   We're constantly improving to provide you with the best token analysis experience! 🚀\n"
    )


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
        msg = await message_template(bot_info)

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
            f"🔍 Need a quick token analysis? Look no further!"
            f" Just send a contract address, and I'll provide you with an instant and fast reply! 💬\n"
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


@router.message(F.content_type.in_({ContentType.NEW_CHAT_MEMBERS}))
async def bot_added_as_member(event, bot: Bot):
    try:
        try:
            if event.new_chat_member:
                info = await bot.get_me()
                if event.new_chat_member["id"] == info.id:
                    await bot.send_message(
                        event.chat.id,
                        f"🤖 {info.username} has joined the group!\nTo get started, send /start. \nTo get help send /help🚀👋",
                    )
        except:
            pass
    except Exception as e:
        logging.error(e)
