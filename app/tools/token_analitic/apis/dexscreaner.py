from typing import Dict, Any

import aiohttp
import json


from app.tools.token_analitic.tools import base_info_tamplate


class DexScreaner:
    ETH_CHAIN_ID = "1"

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def aiohttp_get(self, url: str) -> Dict[str, Any]:
        async with self.session.get(
            url,
        ) as response:
            data = await response.text()
        parsed_data = json.loads(data)
        return parsed_data

    async def get_full_info(self, address: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={address}"
            response = await self.aiohttp_get(url)
            data["dex"] = response["pairs"][0]
        finally:
            return data

    async def analyze(self, address: str) -> Dict[str, Any]:

        url = f"https://api.dexscreener.com/latest/dex/search?q={address}"

        data = await self.aiohttp_get(url)
        print(data)
        pairs = data.get("pairs", [])
        if pairs:
            pair = pairs[0]
            if pair["chainId"] == self.ETH_CHAIN_ID:
                template = await base_info_tamplate()
                template["base"]["platformId"] = self.ETH_CHAIN_ID
                template["base"]["platformName"] = pair["chainId"]
                template["base"]["baseTokenName"] = pair["baseToken"]["name"]
                template["base"]["baseTokenSymbol"] = pair["baseToken"]["symbol"]
                template["base"]["identifier"] = pair["chainId"]
                return template

        return {"base": None}
