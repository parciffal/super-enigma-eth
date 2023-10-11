from typing import Dict, Any

DEXTOOL = {
    "etc": "etc",
    "ethereum": "ether",
    "ethereum goerli": "ethergoerli",
    "ethf": "ethf",
    "ethw": "ethw",
}

DEXTOOL_EMOJI = {
    "bitbucket": "🔗 BitBucket",
    "discord": "💬 Discord",
    "facebook": "📘 Facebook",
    "github": "💻 Github",
    "instagram": "📸 Instagram",
    "linkedin": "🔗 Linkedin",
    "medium": "📰 Medium",
    "reddit": "🔗 Reddit",
    "telegram": "✉️ Telegram",
    "tiktok": "🎵 TikTok",
    "twitter": "🐦 Twitter",
    "website": "🌐 Website",
    "youtube": "🎥 YouTube",
}


class DexTool:

    CHAIN: str = "ethereum"

    def __init__(self, session):
        self.session = session

    async def aiohttp_get(self, url: str, dextool_key: str) -> Dict[str, Any]:
        headers = {"accept": "application/json", "X-API-Key": dextool_key}
        async with self.session.get(url, headers=headers) as response:
            return await response.json()

    async def analyze(self, address: str, data: dict, dextool_key: str) -> dict:
        try:
            url = f"https://api.dextools.io/v1/token?chain={self.CHAIN}&address={address}"
            response = await self.aiohttp_get(url, dextool_key)
            links = {
                key: value
                for key, value in response["data"]["links"].items()
                if value != ""
            }
            if links:
                data["social_links"] = links
            return data
        except Exception as e:
            return data
