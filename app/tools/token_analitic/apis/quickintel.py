import aiohttp


class QuickIntel:
    CHAIN = "eth"

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def aiohttp_post(self, url: str, headers: dict, payload: dict) -> dict:
        async with self.session.post(url, headers=headers, json=payload) as resp:
            data = await resp.json()
        from pprint import pprint

        print("Screener")
        pprint(data)
        return data

    async def analyze(self, data: dict, token: str, quickintel_key: str):
        url = "https://qpi.quickintel.io/api/getthirdaudit"

        headers = {"api_key": quickintel_key, "Content-Type": "application/json"}
        payload = {
            "chain": self.CHAIN,
            "tokenAddress": token,
            "id": "0xs",
        }
        try:
            data["quickintel"] = await self.aiohttp_post(url, headers, payload)
        finally:
            return data
