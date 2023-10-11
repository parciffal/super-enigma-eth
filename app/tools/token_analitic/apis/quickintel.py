import aiohttp
import json


from app.tools.token_analitic.tools import base_info_tamplate


class QuickIntel:
    def __init__(self, session):
        self.session = session

    async def aiohttp_post(self, address, chain, data, quickintel_key) -> dict:
        url = "https://qpi.quickintel.io/api/getthirdaudit"

        headers = {"api_key": quickintel_key,
                   "Content-Type": "application/json"}
        payload = {
            "chain": chain,
            "tokenAddress": address,
            "id": "0xs",
        }
        async with self.session.post(url, headers=headers, json=payload) as resp:
            data['data'] = await resp.json()
        parsed_data = json.loads(data)

        return parsed_data

    async def analyze(self, data, token, quickintel_key):
        try:
            chain = data['base']['identifier']
            data['data'] = await self.aiohttp_post(token, chain, data, quickintel_key)
        except:
            pass
        finally:
            return data
