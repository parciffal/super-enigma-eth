import aiohttp
from typing import Union
import asyncio
from datetime import datetime
from aiogram import Bot
from pprint import pprint
from app.tools.token_analitic.apis import DexScreaner, GoPlus, QuickIntel, DexTool


def timestamp_to_date(unix_timestamp):
    timestamp = datetime.utcfromtimestamp(int(unix_timestamp))
    formatted_date = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date


class BurnDetector:
    def __init__(
        self,
        bot: Bot,
        api_key: str = "6BPFQFD84EPX6FANACNRDSUTD4SKR4MEIX",
        target_address: str = "0x000000000000000000000000000000000000dEaD",
        api_endpoint: str = "https://api.etherscan.io/api",
    ):
        self.bot = bot
        self.api_key = api_key
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
            "offset": "10",
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

    async def burned(self):
        try:
            while True:
                data = await self.get(self.url, self.params)
                if not data:
                    return None
                if data["status"] == "1":
                    transactions = data["result"]
                    for tx in transactions:
                        try:
                            if (
                                tx["tokenSymbol"] not in ["", "UNI-V2"]
                                and int(tx["timeStamp"]) > self.last_tr_time
                            ):
                                self.last_tr_time = int(tx["timeStamp"])
                                value_wei = int(tx["value"])
                                value_eth = value_wei / 10**18
                                data = {
                                    "chain": "ethereum",
                                    "token": tx,
                                    "value_eth": value_eth,
                                }
                                pprint(data)
                        except KeyError as e:
                            print(f"KeyError: {e}. Skipping transaction.")
                else:
                    print("API request failed:", data.get("message", "None"))

                # Sleep for 5 minutes (300 seconds) before checking again
                await asyncio.sleep(300)

        finally:
            if self.session:
                await self.session.close()

    async def start_burning(self):
        try:
            self.session = aiohttp.ClientSession()
            await self.burned()
        except asyncio.CancelledError:
            print("Burning task was cancelled.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def run(self):
        asyncio.run(self.start_burning())
