import pprint
from aiogram import Bot, types
import aiohttp
import time
import asyncio

from app.config import Config

from app.tools.token_analitic.message_creater import MessageCreater
from app.tools.token_analitic.tools import LINKS
from app.tools.token_analitic.apis import (
    GoPlus, DexScreaner, DexTool, Etherscan, GeckoTermianl,
    Moralis, QuickIntel, CoinMarketCup, DEXTOOL, DEXTOOL_EMOJI)
from app.keyboards.inline.rug_check_keyboard import get_link_keyboard


class TokenAnalyzer:
    CHAINS = {
        "ethereum": "1",
        "eth": "1",
    }

    def __init__(self):
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

    def __del__(self):
        async def close_session():
            await self.session.close()
        asyncio.run(close_session())

    async def get_button_links(self, data: dict, address: str):
        keyboards = []
        links = LINKS[self.CHAINS[data["base"]["platformName"].lower()]]
        keys = {
            "geckoterminal": "🦎 Gecko",
            "dextools": "📈 Dex",
            "browserScanAddress": "📡 Scan",
        }
        for key in links:
            keyboards.append(
                {"name": keys[key], "url": f"{links[key]}{address}"})
        return keyboards

    async def get_base_data(self, address, moralis_key, eth_key) -> dict:
        # data = await self.etherscan.analyze(address, eth_key)
        # if data["base"] is None:
        data = await self.moralis.analyze(address, moralis_key)
        if data["base"] is None:
            data = await self.dexscreaner.analyze(address)
        if data["base"] is None:
            data = await self.coinmarketcup.analyze(address)
        if data["base"] is None:
            data = await self.geckotermianl.analyze(address)
        return data

    async def get_analytic_data(
        self, address: str, data: dict, quickintel_key: str
    ) -> dict:
        data = await self.gopluslab.analyze(address, data)
        if data.get("data") is None:
            data = await self.quickintel.analyze(data, address, quickintel_key)
        return data

    async def send_progress_msg(self, message: types.Message, data: dict, bot: Bot):
        chain = (
            data["base"]["platformName"] if data["base"].get(
                "platformName") else "N\A"
        )
        progress_msg = await bot.send_message(
            message.chat.id, text=f"🔎 0xS Analyzer on <b>{chain}</b> in progress 🔍"
        )
        return progress_msg

    async def analyze(
        self, message: types.Message, address: str, bot: Bot, config: Config
    ):
        eth_key = config.scanapis.ethscan
        print(eth_key)
        moralis_key = config.scanapis.moralis
        dextool_key = config.scanapis.dextool
        quick_intel_key = config.scanapis.quickintel

        start = time.time()

        data = await self.get_base_data(address, moralis_key, eth_key)
        progress_msg = await self.send_progress_msg(message, data, bot)

        if data.get("base") is not None:
            # get full info from geckotermial

            data = await self.geckotermianl.analyze_full(address, data)
            # get analytic info

            data = await self.get_analytic_data(address, data, quick_intel_key)
            # get keyboard data

            keyboards = await self.get_button_links(data, address)
            # dex tool links

            data = await self.dextool.analyze(address, data, dextool_key)

            data = await self.dexscreaner.get_full_info(address, data)
            # get message

            msg = await self.message.create(address, data, bot)
        else:
            msg = "📵  <b>Apologies, but the token you are inquiring about does not currently have adequate liquidity.  \nPlease try again later.</b>"
            keyboards = []
        print("Response Time: ", time.time() - start)
        return msg, keyboards, bot, progress_msg


token_analyzer = TokenAnalyzer()
