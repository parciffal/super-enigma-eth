from typing import Dict, Any
import json

DEXTOOL = {
    "etc": "etc",
    "ethereum": "ether",
    "ethereum goerli": "ethergoerli",
    "ethf": "ethf",
    "ethw": "ethw",
}

DEXTOOL_EMOJI = {
    "bitbucket": "BitBucket",
    "discord": "Discord",
    "facebook": "Facebook",
    "github": "Github",
    "instagram": "Instagram",
    "linkedin": "Linkedin",
    "medium": "Medium",
    "reddit": "Reddit",
    "telegram": "Telegram",
    "tiktok": "TikTok",
    "twitter": "𝕏",
    "website": "Website",
    "youtube": "YouTube",
}


class DexTool:
    CHAIN: str = "ether"

    def __init__(self, session):
        self.session = session

    async def aiohttp_get(self, url: str, dextool_key: str) -> Dict[str, Any]:
        headers = {"accept": "application/json", "X-API-Key": dextool_key}
        async with self.session.get(url, headers=headers) as response:
            data = await response.text()
        parsed_data = json.loads(data)
        # print(time.time() - start)
        return parsed_data

    async def analyze(self, address: str, data: dict, dextool_key: str) -> dict:
        try:
            url = (
                f"https://api.dextools.io/v1/token?chain={self.CHAIN}&address={address}"
            )
            response = await self.aiohttp_get(url, dextool_key)
            data["dextool"] = response['data']
            return data
        except Exception as e:
            data['dextool'] = None
            return data
