import aiohttp
import json

from .api_urls import get_api_url


class CoinMarketCup:
    def __init__(self):
        pass

    @staticmethod
    async def get_coin_data(address: str):
        url = await get_api_url("get_coin_data", address)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()
            await session.close()

        parsed_data = json.loads(data)
        return parsed_data

    @staticmethod
    async def get_last_buy(coin_id: str):
        url = await get_api_url("get_coin_data", coin_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()
            await session.close()

        parsed_data = json.loads(data)
        return parsed_data
