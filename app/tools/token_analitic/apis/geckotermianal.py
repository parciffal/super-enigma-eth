import aiohttp
import json


from app.tools.token_analitic.tools import base_info_tamplate
from app.tools.token_analitic.api_urls import coinmarketcap, geckoterminal


class GeckoTermianl:
    NULLADR = "0x0000000000000000000000000000000000000000"
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

    BOOL = {"1": False, "0": True}
    CH_BOOL = {"1": True, "0": False}
    MSG_BOOL = {"0": "✅", "1": "🚫"}
    CHECK_BOOL = {"1": "✅", "0": "🚫"}
    QUICK_BOOL = {False: "✅", True: "🚫", None: "🚫", }
    QUICK_REVERSE = {True: "✅", False: "🚫"}

    def __init__(self, session):
        self.session = session

    async def aiohttp_get(self, url) -> dict:
        async with self.session.get(url, ) as response:
            data = await response.text()
        parsed_data = json.loads(data)
        # print(time.time() - start)
        return parsed_data

    async def analyze_full(self, address: str,  data: dict) -> dict:
        try:
            url = await geckoterminal("get_full_info", data["base"]["identifier"], address)
            response = await self.aiohttp_get(url)
            if response.get("links"):
                response = await self.aiohttp_get(response["links"]["top_pool"])
            if response.get("data"):
                data["full"] = response["data"]
            if response.get("included"):
                data['included'] = response['included']
            else:
                data['included'] = {}
            return data
        except:
            return data

    async def analyze(self, address: str) -> dict:
        url = await coinmarketcap("get_gecko_base_info", address)
        data = await self.aiohttp_get(url)
        template = await base_info_tamplate()
        try:
            if data["data"]["attributes"]["pools"][0]:
                kl = data["data"]["attributes"]["pools"][0]
                template["base"]["platformId"] = self.CHAINS[
                    kl["network"]["identifier"]
                ]
                template["base"]["platformName"] = kl["network"]["name"]
                template["base"]["baseTokenName"] = kl["tokens"][0]["name"]
                template["base"]["baseTokenSymbol"] = kl["tokens"][0]["symbol"]
                template["base"]["identifier"] = kl["network"]["identifier"]
                return template
            else:
                return {"base": None}
        except:
            return {"base": None}
