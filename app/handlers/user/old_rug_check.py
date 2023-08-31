from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command, ContentType
from aiogram.utils.text_decorations import html_decoration as hd


import datetime
import logging
from pprint import pprint

from app.db.models import AdsModel, LinkModel
from app.config import Config
from app.tools.gopluslabs import gopluslabs_manager
from app.tools.honeypot import HoneyPot
from app.tools.advertize_manager import ads_manager
from app.keyboards.inline.rug_check_keyboard import get_link_keyboard

router = Router()


async def get_time_delta(given_timestamp):
    """
    Calculate the time difference between the given timestamp and the current time.

    Args:
        given_timestamp (float): The given timestamp.

    Returns:
        str: A string representing the time difference in days.
    """
    current_timestamp = datetime.datetime.now().timestamp()
    given_datetime = datetime.datetime.fromtimestamp(given_timestamp)
    current_datetime = datetime.datetime.fromtimestamp(current_timestamp)
    time_delta = current_datetime - given_datetime
    days = time_delta.days % 30
    return f"{days} Days"


async def get_simulation_result(data) -> str:
    if data["simulationSuccess"]:
        return (
            f"<b>Tax:</b> Buy: {round(data['simulationResult']['buyTax'], 2)}%"
            f" | Sell: {round(data['simulationResult']['sellTax'], 2)}%"
            f" | Transfer: {data['simulationResult']['transferTax']}%\n"
            f"<b>Gas:</b> Buy: {data['simulationResult']['buyGas']} ⛽"
            f"| Sell: {data['simulationResult']['sellGas']} ⛽\n"
            f"<b>Limit:</b> Buy: {data['simulationResult'].get('buyLimit')}"
            f" | Sell: {data['simulationResult'].get('sellLimit')}\n"
            f"<b>Source code:</b> {data['simulationResult'].get('openSource')}\n\n"
        )
    else:
        return f"\n<b>SIMULATION FAILED\n<i>ERROR: {data['simulationError'].upper()}</i></b>\n\n"


async def get_ads():
    return ""


async def honey_pot_template(data: dict, bot: Bot) -> str:
    """
    Create a formatted message based on HoneyPot data.

    Args:
        data (dict): Data from HoneyPot analysis.

    Returns:
        str: A formatted message containing HoneyPot analysis details.
    """
    try:
        if data["honeypotResult"]["isHoneypot"]:
            is_honeypot = "❗❗❗ <b><i>WARNING</i>: IS HONEYPOT</b> ❗❗❗"
        else:
            is_honeypot = "🎉🎉🎉 <b><i>SUCCESS</i>: IS NOT HONEYPOT</b> 🎉🎉🎉"
    except Exception as e:
        logging.error(e)
        is_honeypot = "<b><i>COULD NOT DETERMINE IF THIS IS A HONEYPOT.</i></b>"
    simulation_result = await get_simulation_result(data)
    if data.get("top_group_link"):
        top_group_link = data.get("top_group_link")
    else:
        top_group_link = ""
    ads = await ads_manager.get_ads(bot)
    message = (
        f"@dsmdslkd_bot 🚨 <b>{hd.code(data['token']['name'].upper())}</b> 🚨"
        f"| <b>{data['name_link']}</b>\n\n"
        f"<b>Address</b>: {hd.code(data['token']['address'])}\n\n"
        f"{is_honeypot}\n\n"
        f"📊 <b><i>SIMULATION RESULTS</i></b> 📊\n"
        f"{simulation_result}"
        f"📈 <i>RECENT HOLDER ANALYSIS</i> 📈\n"
        f"<b>Holders analyzed:</b> {data['holderAnalysis']['holders']}\n"
        f"<b>Can Sell:</b> {data['holderAnalysis']['successful']} 💰 | "
        f"<b>Can't Sell:</b> {data['holderAnalysis']['failed']} ❌\n"
        f"<b>Siphoned:</b> {data['holderAnalysis']['siphoned']} 💸\n"
        f"<b>Average:</b> Tax: {round(data['holderAnalysis']['averageTax'], 2)}%"
        f" | Gas: {round(data['holderAnalysis']['averageGas'], 2)} ⛽\n"
        f"<b>Highest Tax:</b> {round(data['holderAnalysis']['highestTax'], 2)}%\n\n"
        f"{ads}"
    )
    return message


@router.message(F.content_type.in_({ContentType.TEXT}))
async def token_cmd_handler(message: Message, config: Config, bot: Bot):
    try:
        if message.text:
            address = message.text.split(" ")[-1]
            msg, keyboard = await gopluslabs_manager.get_token_security(address, bot)
            await message.answer(msg, parse_mode="html", reply_markup=keyboard)
    except Exception as e:
        await message.answer(
            "📵  The token does not have sufficient liquidity yet. \nPlease try again later."
        )
        logging.error(e)


@router.message(Command("token"))
async def address_cmd_handler(message: Message, config: Config, bot: Bot):
    try:
        if message.text:
            address = message.text.split(" ")[-1]
            token_data = await gopluslabs_manager.get_token_security(address, bot)
            if token_data == 404:
                token_data = await HoneyPot().analize_token(address)
                msg = await honey_pot_template(token_data, bot)
            keyboard = await get_link_keyboard(token_data)
            await message.answer(msg, parse_mode="html", reply_markup=keyboard)

    except Exception as e:
        logging.error(e)
