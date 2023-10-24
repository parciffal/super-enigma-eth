from pprint import pprint
from typing import Union
from aiogram import Bot
import aiohttp
import time
from datetime import datetime, timezone

from app.config import Config

from app.tools.token_analitic.message_creater import MessageCreater
from app.tools.token_analitic.tools import LINKS
from app.tools.token_analitic.apis import (
    GoPlus,
    DexScreaner,
    DexTool,
    Etherscan,
    GeckoTermianl,
    Moralis,
    QuickIntel,
    CoinMarketCup,
)


async def is_pair_created_within_one_hour(
    pair_created_at: Union[str, int, None]
) -> Union[bool, None]:
    if isinstance(pair_created_at, int):
        pair_crt_at_seconds = pair_created_at / 1000.0
    elif isinstance(pair_created_at, str):
        pair_crt_at_datetime = datetime.fromisoformat(pair_created_at)
        pair_crt_at_datetime = pair_crt_at_datetime.replace(tzinfo=timezone.utc)
        pair_crt_at_seconds = pair_crt_at_datetime.timestamp()
    else:
        return None
    current_timestamp_seconds = datetime.now(timezone.utc).timestamp()
    difference_seconds = current_timestamp_seconds - pair_crt_at_seconds
    print(difference_seconds)
    return difference_seconds < 3600 * 24


class TokenAnalyzer:
    CHAINS = {
        "ethereum": "1",
        "eth": "1",
    }

    def __init__(self, session: Union[aiohttp.ClientSession, None] = None):
        if session:
            self.session = session
        else:
            self.session = aiohttp.ClientSession()
        self.moralis = Moralis(self.session)
        self.geckotermianl = GeckoTermianl(self.session)
        self.dexscreaner = DexScreaner(self.session)
        self.quickintel = QuickIntel(self.session)
        self.coinmarketcup = CoinMarketCup(self.session)
        self.etherscan = Etherscan(self.session)
        self.gopluslab = GoPlus(self.session)
        self.dextool = DexTool(self.session)
        self.message = MessageCreater()

    async def get_button_links(self, address: str):
        keyboards = []
        links = LINKS[self.CHAINS["eth"]]
        keys = {
            "0xSBot:telegram": "🔍 Analyze",
            "sniper:telegram": "🔫 Sniper",
            "dex:link": "⚖️  Dex",
            "scan:link": "🔬 Scan",
        }
        for key in links:
            if key.split(":")[-1] == "link":
                keyboards.append({"name": keys[key], "url": f"{links[key]}{address}"})
            else:
                keyboards.append({"name": keys[key], "url": links[key]})
        return keyboards

    async def get_analytic_data(
        self, address: str, data: dict, quickintel_key: str
    ) -> dict:
        data = await self.gopluslab.analyze(address, data)
        if data.get("goplus") is None:
            data = await self.quickintel.analyze(data, address, quickintel_key)
        return data

    async def analyze(
        self, data: dict, bot: Bot, config: Config, token: str = "", det: bool = True
    ):
        start = time.time()
        dextool_key = config.scanapis.dextool
        quick_intel_key = config.scanapis.quickintel
        if token:
            address = token
        else:
            address = data["token"]["contractAddress"]
        data = await self.moralis.analyze(address, config.scanapis.moralis, data)
        if det:
            if data.get("moralis"):
                check = await is_pair_created_within_one_hour(
                    data["moralis"]["created_at"]
                )
                if check == False:
                    return None, None
        data = await self.geckotermianl.analyze_full(address, data)
        if det:
            if data.get("full"):
                check = await is_pair_created_within_one_hour(
                    data["full"]["attributes"]["pool_created_at"]
                )
                if check == False:
                    return None, None
        data = await self.dexscreaner.get_full_info(address, data)
        if det:
            if data.get("dexscreener"):
                check = await is_pair_created_within_one_hour(
                    data["dexscreener"]["pairCreatedAt"]
                )
                if check == False:
                    return None, None
        # get analytic info
        data = await self.get_analytic_data(address, data, quick_intel_key)
        if not det and data.get("goplus"):
            if data["goplus"].get("holders"):
                addresses = [
                    i.get("address", "").lower() for i in data["goplus"]["holders"]
                ]
                null_addrs = [
                    "0x000000000000000000000000000000000000dead",
                    "0x0000000000000000000000000000000000000000",
                ]
                if not any(addr in null_addrs for addr in addresses):
                    msg: str = "🔥No Burn detected. try again later."
                    kb: list = []
                    return msg, kb
        # get keyboard data
        keyboards = await self.get_button_links(address)
        # dex tool links
        data = await self.dextool.analyze(address, data, dextool_key)
        # get message
        msg = await self.message.message_creater(data, bot, address)
        print("Response Time: ", time.time() - start)
        return msg, keyboards
