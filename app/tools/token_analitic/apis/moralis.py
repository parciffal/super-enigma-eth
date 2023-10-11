import aiohttp
import json


from app.tools.token_analitic.tools import base_info_tamplate


class Moralis:
    CHAIN_LIST = [
        "eth",
        "bsc",
        "polygon",
        "avalanche",
        "fantom",
        "cronos",
        "arbitrum",
        "goerli",
        "sepolia",
    ]

    def __init__(self, session):
        self.session = session

    async def aiohttp_get(self, chain, address, moralis_key) -> dict:
        headers = {
            "accept": "application/json",
            "X-API-Key": moralis_key,
        }

        url = f"https://deep-index.moralis.io/api/v2.2/erc20/metadata?chain={chain}&addresses%5B0%5D={address}"
        async with self.session.get(url, headers=headers) as response:
            data = await response.text()
        parsed_data = json.loads(data)
        return parsed_data[0]

    async def aiohttp_post(self, url, headers, dt) -> dict:
        async with self.session.post(url, headers=headers, json=dt) as response:
            data = await response.text()
        parsed_data = json.loads(data)

        return parsed_data

    async def analyze(self, token, moralis_key):
        for chain in self.CHAIN_LIST:
            data = await self.aiohttp_get(chain, token, moralis_key)
            if "" not in [data["name"], data["symbol"]]:
                template = await base_info_tamplate()
                template["base"]["platformId"] = chain
                template["base"]["platformName"] = chain
                template["base"]["baseTokenName"] = data["name"]
                template["base"]["baseTokenSymbol"] = data["symbol"]
                template["base"]["identifier"] = chain
                template["base"]["created_at"] = data["created_at"]
                return template
        return {"base": None}
