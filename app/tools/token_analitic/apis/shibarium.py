import aiohttp
import json


from app.tools.token_analitic.tools import base_info_tamplate
from app.tools.token_analitic.api_urls import coinmarketcap


class Shibarium:
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

    def __init__(self, session):
        self.session = session

    async def aiohttp_get(self, url) -> dict:
        async with self.session.get(url, ) as response:
            data = await response.text()
        parsed_data = json.loads(data)
        return parsed_data

    async def analyze(self, address):
        try:
            url = f"https://www.shibariumscan.io/api?module=token&action=getToken&contractaddress={address}"
            data = await self.aiohttp_get(url=url)
            template = await base_info_tamplate()
            template["base"]["platformId"] = "shibarium"
            template["base"]["platformName"] = "shibarium"
            template["base"]["baseTokenName"] = data["result"]["name"]
            template["base"]["baseTokenSymbol"] = data["result"]["symbol"]
            template["base"]["identifier"] = "shibarium"
            return template
        except:
            return {"base": None}
