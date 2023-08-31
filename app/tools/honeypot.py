import aiohttp
import json
from pprint import pprint

from app.db.models import GroupModel
from .api_urls import get_api_url, honey_pot_url


class HoneyPot:
    ETH = 1
    BTC = 56
    NULLADR = "0x0000000000000000000000000000000000000000"

    def __init__(self):
        pass

    async def aiohttp_get(self, url) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()
            await session.close()

        parsed_data = json.loads(data)
        return parsed_data

    async def get_button_links(self, data: dict, chain: str = "btc") -> dict:
        address = data["token"]["address"]
        if chain == "btc":
            group = await GroupModel.filter(chain="btc").first()
            data["links"].append(
                {"name": "🔸BSCScan", "url": f"https://bscscan.com/token/{address}"}
            )
        else:
            group = await GroupModel.filter(chain="eth").first()
            data["links"].append(
                {"name": "🔹ETHScan", "url": f"https://etherscan.io/token/{address}"}
            )
        if group:
            data["top_group_link"] = await group.to_link()
        data["links"].append(
            {
                "name": "📈 Chart",
                "url": f"https://www.geckoterminal.com/{chain}/pools/{address}",
            }
        )
        data["links"].append(
            {"name": "💠 Dex", "url": f"https://www.dexanalyzer.io/{chain}/{address}"}
        )
        data["links"].append(
            {"name": "📊 ApeSpace", "url": f"https://apespace.io/{chain}/{address}"}
        )

        return data

    #
    async def analize_token(self, address: str):
        chainId = self.BTC
        chain = "btc"
        data = await self.get_is_honeypot(address=address)
        data["name_link"] = "🔸BSC Report"
        data["links"] = []
        if (
            data is None
            or data.get("code") == 404
            or data["token"]["address"] == self.NULLADR
        ):
            chainId = self.ETH
            data = await self.get_is_honeypot(address=address, chainId=chainId)
            data["name_link"] = "🔹ETH Report"
            data["links"] = []
            chain = "eth"
        data = await self.get_button_links(data, chain)
        pprint(data)
        return data

    #
    async def get_token_info(
        self, address: str, pair: str = "", chainId: int = 56
    ) -> dict:
        url = await honey_pot_url("get_token_info", address, chainId)
        return await self.aiohttp_get(url)

    #
    async def get_is_honeypot(
        self, address: str, pair: str = "", chainId: int = 56
    ) -> dict:
        url = await honey_pot_url("get_is_honeypot", address, chainId)
        return await self.aiohttp_get(url)

    #
    async def get_pairs(self, address: str, pair: str = "", chainId: int = 56) -> dict:
        url = await honey_pot_url("get_pairs", address, chainId)

        return await self.aiohttp_get(url)

    async def get_contract_verification(
        self, address: str, pair: str = "", chainId: int = 56
    ) -> dict:
        url = await honey_pot_url("get_contract_verification", address, chainId)
        return await self.aiohttp_get(url)

    async def get_coin_data(self, address: str):
        url = await get_api_url("get_coin_data", address)
        return await self.aiohttp_get(url)

    async def get_last_buy(self, coin_id: str):
        url = await get_api_url("get_coin_data", coin_id)
        return await self.aiohttp_get(url)
