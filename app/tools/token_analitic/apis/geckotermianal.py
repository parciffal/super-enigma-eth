from typing import Dict, Any

import aiohttp
import json


from app.tools.token_analitic.tools import base_info_tamplate
from app.tools.token_analitic.api_urls import coinmarketcap, geckoterminal


class GeckoTermianl:
    ETH_CHAIN_ID = "1"

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def aiohttp_get(self, url: str) -> Dict[str, Any]:
        async with self.session.get(url) as response:
            data = await response.text()
        parsed_data: Dict[str, Any] = json.loads(data)
        return parsed_data

    async def analyze_full(self, address: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            url = await geckoterminal("get_full_info", data["base"]["identifier"], address)
            response: Dict[str, Any] = await self.aiohttp_get(url)
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

    async def analyze(self, address: str) -> Dict[str, Any]:
        url = await coinmarketcap("get_gecko_base_info", address)
        data = await self.aiohttp_get(url)
        print(data)
        template = await base_info_tamplate()
        try:
            if data["data"]["attributes"]["pools"][0]:
                kl = data["data"]["attributes"]["pools"][0]
                template["base"]["platformId"] = self.ETH_CHAIN_ID
                template["base"]["platformName"] = "Ethereum"
                template["base"]["baseTokenName"] = kl["tokens"][0]["name"]
                template["base"]["baseTokenSymbol"] = kl["tokens"][0]["symbol"]
                template["base"]["identifier"] = self.ETH_CHAIN_ID
                return template
            else:
                return {"base": None}
        except:
            return {"base": None}
