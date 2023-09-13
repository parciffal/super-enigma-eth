import asyncio
import aiohttp
import json


async def main():
    url = "https://qpi.quickintel.io/api/getthirdaudit"

    headers = {"api_key": "0xs-KUen48jjdHV223ss", "Content-Type": "application/json"}

    data = {
        "chain": "shibarium",
        "tokenAddress": "0x2bc459873c03a8cd2e3d070544cae1e6e184a686",
        "id": "0xs",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as resp:
            print(resp.status)
            print(await resp.json())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())