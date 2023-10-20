from pprint import pprint
from typing import Dict, Union
from aiogram import Bot, types
import aiohttp
import time
import asyncio
from datetime import datetime, timezone

from app.config import Config

from app.tools.token_analitic.message_creater import MessageCreater
from app.tools.token_analitic.tools import LINKS
from app.tools.token_analitic.apis import (
    GoPlus, DexScreaner, DexTool, Etherscan, GeckoTermianl,
    Moralis, QuickIntel, CoinMarketCup, DEXTOOL, DEXTOOL_EMOJI)
from app.keyboards.inline.rug_check_keyboard import get_link_keyboard


async def is_pair_created_within_one_hour(pair_created_at: Union[str, int, None]) -> Union[bool, None]:
    if isinstance(pair_created_at, int):
        pair_created_at_seconds = pair_created_at / 1000.0
    elif isinstance(pair_created_at, str):
        pair_created_at_datetime = datetime.fromisoformat(pair_created_at)
        pair_created_at_datetime = pair_created_at_datetime.replace(
            tzinfo=timezone.utc)
        pair_created_at_seconds = pair_created_at_datetime.timestamp()
    else:
        return None
    current_timestamp_seconds = datetime.now(timezone.utc).timestamp()
    difference_seconds = current_timestamp_seconds - pair_created_at_seconds
    print(difference_seconds)

    return difference_seconds < 3600*4


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
            "geckoterminal": "🦎 Gecko",
            "dextools": "📈 Dex",
            "browserScanAddress": "📡 Scan",
        }
        for key in links:
            keyboards.append(
                {"name": keys[key], "url": f"{links[key]}{address}"})
        return keyboards

    async def get_analytic_data(
        self, address: str, data: dict, quickintel_key: str
    ) -> dict:
        data = await self.gopluslab.analyze(address, data)
        if data.get("goplus") is None:
            data = await self.quickintel.analyze(data, address, quickintel_key)
        return data

    async def analyze(
        self, data: dict, bot: Bot, config: Config, token: str = ""
    ):
        start = time.time()
        dextool_key = config.scanapis.dextool
        quick_intel_key = config.scanapis.quickintel
        if token:
            address = token
        else:
            address = data['token']['contractAddress']
        data = await self.moralis.analyze(address, config.scanapis.moralis, data)
        if data.get("moralis"):
            check = await is_pair_created_within_one_hour(data["moralis"]['created_at'])
            if check == False:
                return None, None
        data = await self.geckotermianl.analyze_full(address, data)
        if data.get('full'):
            check = await is_pair_created_within_one_hour(data["full"]['attributes']['pool_created_at'])
            if check == False:
                return None, None
        data = await self.dexscreaner.get_full_info(address, data)
        if data.get('dexscreener'):
            check = await is_pair_created_within_one_hour(data["dexscreener"]['pairCreatedAt'])
            if check == False:
                return None, None
        # get analytic info
        data = await self.get_analytic_data(address, data, quick_intel_key)
        # get keyboard data
        keyboards = await self.get_button_links(address)
        # dex tool links
        data = await self.dextool.analyze(address, data, dextool_key)
        # get message
        pprint(data)
        msg = await self.message.message_creater(data, bot, address)
        print("Response Time: ", time.time() - start)
        return msg, keyboards
