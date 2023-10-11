import aiohttp
import logging


class Etherscan:

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.base_url = "https://api.etherscan.io/api"

    async def aiohttp_get(self, url: str, **params) -> dict:
        """Make a GET request to Etherscan API."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    return await response.json()
        except aiohttp.ClientConnectionError as e:
            logging.error(f"aiohttp client error: {e}")
            return {}

    async def analyze(self, address: str, key: str) -> dict:
        """
        Analyze a token contract address using Etherscan API.

        Args:
            address: The token contract address 
            key: Etherscan API key

        Returns:
            dict: The token info if found, else None
        """
        try:
            params = {
                "module": "token",
                "action": "tokeninfo",
                "contractaddress": address,
                "apikey": key
            }

            data = await self.aiohttp_get(
                self.base_url,
                **params
            )
            base_data = data.get("result", [])[0]
            return {"base": base_data}
        except Exception as e:
            logging.error(f"Error getting token info: {e}")
            return {"base": None}
