from pprint import pprint
from typing import Dict, Any
import json
import aiohttp


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
        # print(time.time() - start)
        return parsed_data

    async def get_full_info(self, address: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={address}"
            response = await self.aiohttp_get(url)
            data["dexscreener"] = response["pairs"][0]
        finally:
            return data

    async def analyze(self, address: str):
        url = f"https://api.dexscreener.com/latest/dex/search?q={address}"
        try:
            response = await self.aiohttp_get(url)
            data = response["pairs"][0]
            return data
        except:
            return None
