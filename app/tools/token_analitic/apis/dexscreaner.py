import aiohttp
import json


from app.tools.token_analitic.tools import base_info_tamplate


class DexScreaner:
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

    async def get_full_info(self, address: str, data: dict) -> dict:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={address}"
            response = await self.aiohttp_get(url)
            data['dex'] = response['pairs'][0]
        finally:
            return data

    async def analyze(self, address):
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={address}"
            data = await self.aiohttp_get(url)
            if len(data.get("pairs")) > 0:
                data = data['pairs'][0]
                template = await base_info_tamplate()
                template["base"]["platformId"] = self.CHAINS[
                    data['chainId']
                ]
                template["base"]["platformName"] = data['chainId']
                template["base"]["baseTokenName"] = data['baseToken']['name']
                template["base"]["baseTokenSymbol"] = data['baseToken']["symbol"]
                template["base"]["identifier"] = data['chainId']
                return template
            else:
                return {"base": None}
        except:
            return {"base": None}
