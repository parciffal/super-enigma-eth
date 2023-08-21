import aiohttp
import json

from .api_urls import get_api_url


class MonarchRugCheck:
    @staticmethod
    async def get_rug_check(address: str, chain="btc"):
        url = await get_api_url(f"get_{chain}_rug_check", address)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()
            await session.close()

        parsed_data = json.loads(data)
        return parsed_data
