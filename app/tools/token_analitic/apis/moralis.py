import aiohttp
import json


from app.tools.token_analitic.tools import base_info_tamplate


class Moralis:
    CHAIN = "eth"

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def aiohttp_get(self, chain: str, address: str, moralis_key: str) -> dict:
        headers = {
            "accept": "application/json",
            "X-API-Key": moralis_key,
        }

        url = f"https://deep-index.moralis.io/api/v2.2/erc20/metadata?chain={chain}&addresses%5B0%5D={address}"
        async with self.session.get(url, headers=headers) as response:
            data = await response.json()
        return data.get(0, {})

    async def analyze(self, address: str, moralis_key: str) -> dict:
        try:
            data = await self.aiohttp_get(self.CHAIN, address, moralis_key)
            print(data)
            if "" not in [data["name"], data["symbol"]] and data:
                template = await base_info_tamplate()
                template["base"]["platformId"] = self.CHAIN
                template["base"]["platformName"] = self.CHAIN
                template["base"]["baseTokenName"] = data["name"]
                template["base"]["baseTokenSymbol"] = data["symbol"]
                template["base"]["identifier"] = self.CHAIN
                template["base"]["created_at"] = data["created_at"]
                return template
        finally:
            return {"base": None}
