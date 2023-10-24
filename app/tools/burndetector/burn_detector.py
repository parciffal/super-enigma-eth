import logging
import aiohttp
from typing import Union
import asyncio
from datetime import datetime
from aiogram import Bot
from pprint import pprint
from app.config import Config
from app.db.models import GroupModel
from app.tools.token_analitic.token_analyzer import TokenAnalyzer
from app.tools.token_analitic.apis import DexScreaner, Moralis
from app.keyboards.inline.rug_check_keyboard import get_link_keyboard


def timestamp_to_date(unix_timestamp):
    timestamp = datetime.utcfromtimestamp(int(unix_timestamp))
    formatted_date = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date


def is_pair_created_within_one_hour(pair_created_at):
    # Convert the pairCreatedAt timestamp from milliseconds to seconds
    pair_created_at_seconds = pair_created_at / 1000.0

    # Get the current timestamp in seconds
    current_timestamp_seconds = datetime.now().timestamp()

    # Calculate the difference in seconds
    difference_seconds = current_timestamp_seconds - pair_created_at_seconds

    # Check if the difference is less than 1 hour (3600 seconds)
    return difference_seconds < 7200


class BurnDetector:
    def __init__(
        self,
        bot: Bot,
        config: Config,
        target_address: str = "0x000000000000000000000000000000000000dEaD",
        api_endpoint: str = "https://api.etherscan.io/api",
    ):
        self.bot = bot
        self.config: Config = config
        self.api_key = config.scanapis.ethscan
        self.last_tr_time = 0
        self.target_address = target_address
        self.url = api_endpoint
        self.params = {
            "module": "account",
            "action": "tokentx",
            "address": self.target_address,
            "startblock": "0",
            "endblock": "latest",
            "page": "1",
            "offset": "20",
            "sort": "desc",
            "apikey": self.api_key,
        }

    async def get(self, url: str, params: dict = {}) -> Union[None, dict]:
        try:
            async with self.session.get(url=url, params=params) as response:
                response.raise_for_status()  # Raise an exception for non-200 status
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Aiohttp client error: {e}")
            return None

    async def send_message(self, msg, kb):
        groups = await GroupModel.filter(show=True)
        for group in groups:
            await self.bot.send_message(
                text=msg,
                chat_id=group.telegram_id,
                reply_markup=kb,
            )

    async def bot_age(self, contract_address):
        try:
            dt = await self.dex.analyze(contract_address)
            if dt:
                return is_pair_created_within_one_hour(dt["pairCreatedAt"])
            dt = await self.moralis.get_token(
                contract_address, self.config.scanapis.moralis
            )
            if dt:
                pprint(dt)
        except Exception as e:
            print(e)
        finally:
            return None

    async def burned(self):
        try:
            while True:
                data = await self.get(self.url, self.params)
                if not data:
                    return None
                if data["status"] == "1":
                    transactions = data["result"]
                    for tx in transactions:
                        print(tx["contractAddress"])
                        try:
                            if (
                                tx["tokenSymbol"] not in ["", "UNI-V2"]
                                and int(tx["timeStamp"]) > self.last_tr_time
                            ):
                                # check = await self.bot_age(tx['contractAddress'])

                                self.last_tr_time = int(tx["timeStamp"])
                                value_wei = int(tx["value"])
                                value_eth = value_wei / 10**18
                                data = {
                                    "chain": "ethereum",
                                    "token": tx,
                                    "value_eth": value_eth,
                                }
                                msg, kb = await self.token_analyzer.analyze(
                                    data, self.bot, self.config
                                )
                                if msg and kb:
                                    keyb = await get_link_keyboard(kb)
                                    asyncio.create_task(self.send_message(msg, keyb))
                                else:
                                    self.last_tr_time = 0
                            await asyncio.sleep(1)
                        except KeyError as e:
                            print(f"KeyError: {e}. Skipping transaction.")
                else:
                    print("API request failed:", data.get("message", "None"))

                # Sleep for 5 minutes (300 seconds) before checking again
                await asyncio.sleep(10)
        except Exception as e:
            logging.error(f"Burn: {repr(e)}")
        finally:
            if self.session:
                await self.session.close()

    async def start_burning(self):
        try:
            self.session = aiohttp.ClientSession()
            self.dex = DexScreaner(self.session)
            self.moralis = Moralis(self.session)
            self.token_analyzer = TokenAnalyzer(self.session)
            logging.info(f"Start listning {self.target_address} address")
            await self.burned()
        except asyncio.CancelledError:
            print("Burning task was cancelled.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def run(self):
        asyncio.run(self.start_burning())
