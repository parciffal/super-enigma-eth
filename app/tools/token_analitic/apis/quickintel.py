import aiohttp
import json


class QuickIntel:
    CHAIN = "eth"

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def aiohttp_post(self, url: str, headers: dict, payload: dict) -> dict:
        async with self.session.post(url, headers=headers, json=payload) as resp:
            data = await resp.text()
        parsed_data = json.loads(data)
        # print(time.time() - start)
        return parsed_data

    async def analyze(self, data: dict, token: str, quickintel_key: str):
        url = "https://qpi.quickintel.io/api/getthirdaudit"

        headers = {"api_key": quickintel_key,
                   "Content-Type": "application/json"}
        payload = {
            "chain": self.CHAIN,
            "tokenAddress": token,
            "id": "0xs",
        }
        try:
            data["quick"] = await self.aiohttp_post(url, headers, payload)
        finally:
            return data
