import aiohttp
import json


from app.tools.token_analitic.tools import base_info_tamplate
from app.tools.token_analitic.api_urls import coinmarketcap


class CoinMarketCup:

    def __init__(self, session):
        self.session = session

    async def aiohttp_get(self, url) -> dict:
        async with self.session.get(url, ) as response:
            data = await response.text()
        parsed_data = json.loads(data)
        # print(time.time() - start)
        return parsed_data

    async def analyze(self, address):
        url = await coinmarketcap("get_coinmarket_base_info", address)
        data = await self.aiohttp_get(url)
        try:
            if data["status"]["error_code"] in [0, "0"]:
                data["base"] = data["data"]["pairs"][0]
                return data
            else:
                return {"base": None}
        except:
            return {"base": None}
