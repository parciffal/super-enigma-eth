import pprint
from aiogram import Bot, types
import aiohttp
import time

from app.config import Config

from app.tools.token_analitic.apis.goplus import GoPlus
from app.tools.token_analitic.message_creater import MessageCreater
from app.tools.token_analitic.tools import LINKS
from app.tools.token_analitic.apis import *
from app.keyboards.inline.rug_check_keyboard import get_link_keyboard


class TokenAnalyzer:
    CHAINS = {
        "ethereum": "1",
        "eth": "1",
        "shibarium": "109",
        "Shibarium": "109",
        "optimism": "10",
        "cronos": "25",
        "bsc": "56",
        "bnb chain": "56",
        "okc": "66",
        "gnosis": "100",
        "heco": "128",
        "polygon": "137",
        "fantom": "250",
        "kcc": "321",
        "zksync era": "324",
        "zksync": "324",
        "ethw": "10001",
        "fon": "201022",
        "arbitrum": "42161",
        "avalanche": "43114",
        "linea mainet": "59144",
        "linea testnet": "59140",
        "base": "8453",
        "harmony": "1666600000",
        "tron": "tron",
    }

    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.moralis = Moralis(self.session)
        self.geckotermianl = GeckoTermianl(self.session)
        self.dexscreaner = DexScreaner(self.session)
        self.quickintel = QuickIntel(self.session)
        self.coinmarketcup = CoinMarketCup(self.session)
        self.shibarium = Shibarium(self.session)
        self.gopluslab = GoPlus(self.session)
        self.dextool = DexTool(self.session)
        self.message = MessageCreater()

    async def __del__(self):
        await self.session.close()

    async def get_button_links(self, data: dict, address: str):
        keyboards = []
        links = LINKS[self.CHAINS[data["base"]["platformName"].lower()]]
        keys = {
            "geckoterminal": "🦎 Gecko",
            "dextools": "📈 Dex",
            "browserScanAddress": "📡 Scan"
        }
        for key in links:
            keyboards.append(
                {
                    "name": keys[key],
                    "url": f"{links[key]}{address}"
                }
            )
        return keyboards

    async def get_base_data(self, address, moralis_key) -> dict:
        data = await self.geckotermianl.analyze(address)
        if data['base'] is None:
            data = await self.coinmarketcup.analyze(address)
        if data['base'] is None:
            data = await self.dexscreaner.analyze(address)
        if data['base'] is None:
            data = await self.moralis.analyze(address, moralis_key)
        if data['base'] is None:
            data = await self.shibarium.analyze(address)
        return data

    async def get_analytic_data(self, address: str, data: dict, quickintel_key: str) -> dict:
        data = await self.gopluslab.analyze(address, data)
        if data.get('data') is None:
            data = await self.quickintel.analyze(data, address, quickintel_key)
        return data

    async def send_progress_msg(self, message: types.Message, data: dict, bot: Bot):
        chain = data['base']['platformName'] if data['base'].get(
            "platformName") else "N\A"
        progress_msg = await bot.send_message(
            message.chat.id, text=f"🔎 0xS Analyzer on <b>{chain}</b> in progress 🔍"
        )
        return progress_msg

    async def analyze(self, message: types.Message, address: str, bot: Bot, config: Config):
        moralis_key = config.scanapis.moralis
        dextool_key = config.scanapis.dextool
        quick_intel_key = config.scanapis.quickintel
        start = time.time()
        data = await self.get_base_data(address, moralis_key)
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
