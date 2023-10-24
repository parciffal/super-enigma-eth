from aiogram import Router, Bot, F
from aiogram.types import ContentType, Message
from aiogram.filters import Command

from pprint import pprint
import logging

from app.config import Config
from app.db.models import GroupModel
from app.keyboards.inline.rug_check_keyboard import get_link_keyboard
from app.tools.token_analitic.token_analyzer import TokenAnalyzer

token_analyzer = TokenAnalyzer()
router = Router()


async def message_template(bot_info):
    return (
        f"🔥 Welcome to <b>@{bot_info.username}</b> - The Ethereum Burn Detector Bot! 🔍\n\n"
        f"📊 This bot specializes in detecting and analyzing burn"
        f" events on the Ethereum blockchain.\n"
        f"\n👀 <b>What this bot does:</b>\n"
        f"   - Detects burn events for various ERC-20 tokens on Ethereum\n"
        f"   - Provides detailed analysis and statistics for each burn event\n"
        f"   - Keeps you updated on the latest burn activities\n"
        f"\n📈 <b>How to use the bot?</b>\n"
        f"   Simply add bot to group, and the bot will check for "
        f"recent burn events and provide you with a report! 📄\n"
        f"\n👥 <b>How to add the bot to your Group?</b>\n"
        f"   To enable group analysis, add @{bot_info.username} as an "
        f"administrator in your group, and it's ready to assist your community! 💬\n"
        f"\n📢 <b>Stay tuned for updates and new features!</b>\n"
        f"   We're constantly improving to provide you with "
        f"the best burn detection experience on Ethereum! 🚀\n"
    )


@router.message(Command("start"))
async def start_cmd_handler(message: Message, config: Config, bot: Bot):
    try:
        bot_info = await bot.get_me()
        msg = await message_template(bot_info)
        # Add any more specific details or features you want to highlight here.
        await message.answer(msg, parse_mode="html")
    except Exception as e:
        logging.error(e)


@router.message(Command("help"))
async def help_cmd_handler(message: Message, config: Config, bot: Bot):
    try:
        print(1)
        bot_info = await bot.get_me()
        msg = (
            f"🔥 Welcome to <b>@{bot_info.username}</b> - The Ethereum Burn Detector Bot! 🔍\n\n"
            f"📊 Looking to detect burn events for ERC-20 tokens on the Ethereum blockchain? You're in the right place!\n"
            f"\n👀 <b>How to use the bot:</b>\n"
            f"   Just send a contract address of an ERC-20 token, and I'll detect any recent burn events and provide you with a report! 📄\n"
            f"\n🌐 <b>Features:</b>\n"
            f"   - Real-time burn event detection 🔥\n"
            f"   - Detailed burn event analysis 📉\n"
            f"   - Latest burn event updates 🔄\n"
            f"\n💎 Looking to learn more about token burns or promote your burn-related project? Contact us for collaboration opportunities! 📣\n"
            f"\n❓ Always remember to verify burn events and make informed decisions in the crypto space! 💪💰\n"
            f"\n🤝 Have any questions or need assistance with detecting burns? Feel free to ask anytime. We're here to help you track those burns! 🙌"
        )

        # You can further customize or add specific details to this message as needed.
        await message.answer(msg)
    except Exception as e:
        logging.error(e)


@router.message(Command("autodetect"))
async def autodetect_cmd_handler(message: Message, config: Config, bot: Bot):
    try:
        if message.from_user:
            member = await bot.get_chat_member(message.chat.id, message.from_user.id)
            if member.status in ["creator", "administrator"]:
                group = await GroupModel.get(telegram_id=message.chat.id)
                group.show = not group.show
                await group.save()
                msd = {True: "On", False: "Off"}
                msg = f"Autosend is {msd[group.show]}"
                await message.answer(msg)
    except Exception as e:
        logging.error(repr(e))


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


@router.message(Command("detect"))
async def detect_cmd_handler(message: Message, bot: Bot, config: Config):
    try:
        print(message.text)
        if message.text:
            if message.text == "/detect":
                await message.answer("🚨 <b>Token not provided.</b> 🚨")
            kls = message.text.split(" ")[-1]
            if len(kls) > 1:
                if len(kls) == 42 and kls.startswith("0"):
                    address = kls
                    progress_msg: Message = await message.answer(
                        "🔥Burn Detector in progres on ETH 🔥"
                    )
                    (msg, keyboard) = await token_analyzer.analyze(
                        {}, bot, config, address, False
                    )
                    await change_message(bot, progress_msg, msg, keyboard)
                elif kls.startswith("0") and (len(kls) < 42 or len(kls) > 42):
                    await message.answer("🚨 <b>Invalid token provided.</b> 🚨")
    except Exception as e:
        await message.answer("🚨 <b>Invalid token provided.</b> 🚨")
        logging.error(repr(e))


@router.message(F.content_type.in_({ContentType.LEFT_CHAT_MEMBER}))
async def bot_delete_from_member(event: Message, bot: Bot):
    try:
        if event.left_chat_member:
            info = await bot.get_me()
            if event.left_chat_member.id == info.id:
                group = GroupModel.get(telegram_id=event.chat.id).first()
                if group:
                    await group.delete()
                    logging.info(f"Bot removed from {event.chat.title}")
    except Exception as e:
        logging.error(e)


@router.message(F.content_type.in_({ContentType.NEW_CHAT_MEMBERS}))
async def bot_added_as_member(event: Message, bot: Bot):
    try:
        if event.new_chat_member:
            info = await bot.get_me()
            if event.new_chat_member["id"] == info.id:
                group = GroupModel(telegram_id=event.chat.id, name=event.chat.title)
                await group.save()
                await bot.send_message(
                    event.chat.id,
                    f"🤖 {info.username} has joined the group!\nTo get started, send /start. \nTo get help send /help🚀👋",
                )
    except Exception as e:
        logging.error(repr(e))
