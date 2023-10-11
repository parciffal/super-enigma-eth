import aiohttp

from app.tools.token_analitic.api_urls import coinmarketcap


class CoinMarketCup:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def aiohttp_get(self, url: str) -> dict:
        async with self.session.get(url) as response:
            data = await response.json()
        return data

    async def analyze(self, address: str) -> dict:
        url = await coinmarketcap("get_coinmarket_base_info", address)
        data = await self.aiohttp_get(url)
        try:
            if data["status"]["error_code"] in [0, "0"]:
                data["base"] = data["data"]["pairs"][0]
                return data
        finally:
            return {"base": None}
