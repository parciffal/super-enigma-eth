import aiohttp
from app.tools.token_analitic.api_urls import gopluslabs
import json


class GoPlus:
    ETH_CHAIN_ID = "1"
    ETH_CHAINS = ["eth", "ethereum"]

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def aiohttp_get(self, url: str) -> dict:
        async with self.session.get(
            url,
        ) as response:
            data = await response.text()
        parsed_data = json.loads(data)
        # print(time.time() - start)
        return parsed_data

    async def analyze(self, address: str, data: dict) -> dict:
        try:
            url = await gopluslabs(
                "get_address_info",
                address,
                self.ETH_CHAIN_ID,
            )
            response = await self.aiohttp_get(url)
            if response["result"][address.lower()]:
                data["goplus"] = response["result"][address.lower()]
            else:
                data["goplus"] = None
            return data
        except:
            return data
