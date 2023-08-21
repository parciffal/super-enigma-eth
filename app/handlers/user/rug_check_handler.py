from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.text_decorations import html_decoration as hd


import datetime
import logging
from pprint import pprint

from app.config import Config
from app.tools.honeypot import HoneyPot
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


async def honey_pot_template(data: dict) -> str:
    """
    Create a formatted message based on HoneyPot data.

    Args:
        data (dict): Data from HoneyPot analysis.

    Returns:
        str: A formatted message containing HoneyPot analysis details.
    """
    if data["honeypotResult"]["isHoneypot"]:
        is_honeypot = "❗❗❗ <b><i>WARNING</i>: IS HONEYPOT</b> ❗❗❗"
    else:
        is_honeypot = "🎉🎉🎉 <b><i>SUCCESS</i>: IS NOT HONEYPOT</b> 🎉🎉🎉"
    message = (
        f"🚨 <b>{hd.code(data['token']['name'].upper())}</b> 🚨"
        f"| <b>{data['name_link']}</b>\n"
        f"<b>Address</b>: {hd.code(data['token']['address'])}\n\n"
        f"{is_honeypot}\n\n"
        f"📊 <b><i>SIMULATION RESULTS</i></b> 📊\n"
        f"<b>Tax:</b> Buy: {round(data['simulationResult']['buyTax'], 2)}%"
        f" | Sell: {round(data['simulationResult']['sellTax'], 2)}%"
        f" | Transfer: {data['simulationResult']['transferTax']}%\n"
        f"<b>Gas:</b> Buy: {data['simulationResult']['buyGas']} ⛽"
        f"| Sell: {data['simulationResult']['sellGas']} ⛽\n"
        f"<b>Limit:</b> Buy: {data['simulationResult'].get('buyLimit')}"
        f" | Sell: {data['simulationResult'].get('sellLimit')}\n"
        f"<b>Source code:</b> {data['simulationResult'].get('openSource')}\n\n"
        f"📈 <i>RECENT HOLDER ANALYSIS</i> 📈\n"
        f"<b>Holders analyzed:</b> {data['holderAnalysis']['holders']}\n"
        f"<b>Can Sell:</b> {data['holderAnalysis']['successful']} 💰 | "
        f"<b>Can't Sell:</b> {data['holderAnalysis']['failed']} ❌\n"
        f"<b>Siphoned:</b> {data['holderAnalysis']['siphoned']} 💸\n"
        f"<b>Average:</b> Tax: {round(data['holderAnalysis']['averageTax'], 2)}%"
        f" | Gas: {round(data['holderAnalysis']['averageTax'], 2)} ⛽\n"
        f"<b>Highest Tax:</b> {round(data['holderAnalysis']['highestTax'], 2)}%\n"
    )
    return message


@router.message(Command("address"))
async def address_cmd_handler(message: Message, config: Config):
    # try:
    if message.text:
        address = message.text.split(" ")[-1]
        token_data = await HoneyPot().analize_token(address)
        msg = await honey_pot_template(token_data)
        keyboard = await get_link_keyboard(token_data)
        await message.answer(msg, parse_mode="html", reply_markup=keyboard)


# except Exception as e:
#    logging.error(e)
