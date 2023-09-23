import aiohttp
import json
from app.tools.token_analitic.api_urls import gopluslabs


from app.tools.token_analitic.tools import base_info_tamplate


class GoPlus:
    NULLADR = "0x0000000000000000000000000000000000000000"
    CHAINS = {
        "ethereum": "1",
        "eth": "1",
        "shibarium": "109",
        "Shibarium": "109",
        "optimism": "10",
        "cronos": "25",
        "bsc": "56",
        "bnb chain": "56",
        "okc": "66",
        "gnosis": "100",
        "heco": "128",
        "polygon": "137",
        "fantom": "250",
        "kcc": "321",
        "zksync era": "324",
        "zksync": "324",
        "ethw": "10001",
        "fon": "201022",
        "arbitrum": "42161",
        "avalanche": "43114",
        "linea mainet": "59144",
        "linea testnet": "59140",
        "base": "8453",
        "harmony": "1666600000",
        "tron": "tron",
    }

    def __init__(self, session):
        self.session = session

    async def aiohttp_get(self, url) -> dict:
        async with self.session.get(url, ) as response:
            data = await response.text()
        parsed_data = json.loads(data)
        # print(time.time() - start)
        return parsed_data

    async def aiohttp_post(self, url, headers, dt) -> dict:
        async with self.session.post(url, headers=headers, json=dt) as response:
            data = await response.text()
        parsed_data = json.loads(data)

        return parsed_data

    async def analyze(self, address: str, data: dict) -> dict:
        try:
            url = await gopluslabs(
                "get_address_info",
                address,
                self.CHAINS[data["base"]["platformName"].lower()],
            )
            response = await self.aiohttp_get(url)
            if response['result'][address.lower()]:
                data['data'] = response['result'][address.lower()]
            else:
                data['data'] = None
            return data
        except:
            return data
