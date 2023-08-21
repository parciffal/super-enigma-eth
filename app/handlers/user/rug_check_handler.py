from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.text_decorations import html_decoration as hd
from aiogram.utils.markdown import hide_link


import datetime
import logging
from pprint import pprint

from app.config import Config
from app.tools.monarch_rugcheck import MonarchRugCheck
from app.tools.coinmarketcup import CoinMarketCup
from app.tools.honeypot import HoneyPot

router = Router()


async def get_time_delta(given_timestamp):
    # Get the current timestamp
    current_timestamp = datetime.datetime.now().timestamp()

    # Convert the given timestamp to a datetime object
    given_datetime = datetime.datetime.fromtimestamp(given_timestamp)

    # Convert the current timestamp to a datetime object
    current_datetime = datetime.datetime.fromtimestamp(current_timestamp)
    # Calculate the time difference
    time_delta = current_datetime - given_datetime
    days = time_delta.days % 30
    return f"{days} Days"


async def message_template(data: dict):
    message = f"""
    @BSCSafeSniper  |  {data['token']['name']}  |  🔸{data['network']} Report \n
     🔸 Address: {data['token']['address']} \n 
     👨‍💻 Owner:  {data['token']['creator']} \n
     💧 Liquid: {int(float(data['token']['liq']))}.\n
     👥 Holders:     {data['holders']}\n
     💲 MCap: ${int(data['token']['supply']) * int(float(data['token']['price']))}  BNB:${round(data['token']['mainTokenPrice'])} \n
     💰 Liquidity: {(int(float(data['token']['liq'])) * int(float(data['token']['price'])))/round(data['token']['mainTokenPrice'])} WBNB \n
     🔒 LP Lock:      100.00% locked for {await get_time_delta(data['locks'][0]['end'])} on {data['locks'][0]['source']} \n
     🔖 Fee:              Buy: 9.99%  |  Sell: 13.73%
     📈 Max Buy:   99999999999999.98(0.0001 WBNB)
     🥏 Telegram:  https://t.me/GodFatherBNB
     🌐 WebSite:     www.godfatherbsc.site
     📈 ATH:             TBD

     🔸BSC () 📈Chart () 💠Analyzer ()
     ____________________________
     Always DYOR. Auto rugcheckers can`t detect all scams.
     THIS IS ONE MINUTE DELAYED REPORT.
     JOIN VIP FOR REAL-TIME"""


async def honey_pot_tamplate(data: dict) -> str:
    if data["honeypotResult"]["isHoneypot"]:
        is_honeypot = "❗❗❗ <b><i>WARNING</i>: IS HONEYPOT</b> ❗❗❗"
    else:
        is_honeypot = "🎉🎉🎉 <b><i>SUCCESS</i>: IS NOT HONEYPOT</b> 🎉🎉🎉"
    message = (
        f"🚨 <b>{data['token']['name'].upper()}</b> 🚨 | <b>{data['name_link']}</b>\n"
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
    try:
        print(message.text)
        if message.text:
            address = message.text.split(" ")[-1]
            token_data = await HoneyPot().analize_token(address)
            pprint(token_data)
            msg = await honey_pot_tamplate(token_data)
            await message.answer(msg, parse_mode="html")
    except Exception as e:
        logging.error(e)
