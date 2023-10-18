import pprint
import aiohttp


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
        print("moralis")
        pprint.pprint(data)
        return data.get(0, {})

    async def analyze(self, address: str, moralis_key: str) -> dict:
        try:
            data_r = await self.aiohttp_get(self.CHAIN, address, moralis_key)
            data["moralis"] = data_r
        finally:
            return {"moralis": None}
