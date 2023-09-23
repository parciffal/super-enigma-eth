import aiohttp
import json


from app.tools.token_analitic.tools import base_info_tamplate

DEXTOOL = {
    "alvey": "alvey",
    "aptos": "aptos",
    "arbitrum": "arbitrum",
    "arbitrumnova": "arbitrumnova",
    "astar": "astar",
    "aurora": "aurora",
    "avalanche": "avalanche",
    "avax dfk": "dfk",
    "bnb chain": "bsc",
    "base": "base",
    "bitgert": "bitgert",
    "bitrock": "bitrock",
    "boba": "boba",
    "canto": "canto",
    "celo": "celo",
    "conflux": "conflux",
    "core dao": "coredao",
    "cronos": "cronos",
    "cube": "cube",
    "dogechain": "dogechain",
    "echelon": "echelon",
    "elastos": "elastos",
    "energi": "energi",
    "etc": "etc",
    "ethereum": "ether",
    "ethereum goerli": "ethergoerli",
    "ethf": "ethf",
    "ethw": "ethw",
    "evmos": "evmos",
    "exosama": "exosama",
    "fantom": "fantom",
    "filecoin": "filecoin",
    "flare": "flare",
    "fuse": "fuse",
    "fusion": "fusion",
    "gnosis": "gnosis",
    "harmony": "harmony",
    "heco": "heco",
    "hoo": "hoo",
    "iotex": "iotex",
    "kcc": "kucoin",
    "kardia": "kardia",
    "kava": "kava",
    "kek": "kek",
    "klaytn": "klaytn",
    "linea": "linea",
    "mantle": "mantle",
    "meter": "meter",
    "metis": "metis",
    "milkomeda": "milkomeda",
    "moonbeam": "moonbeam",
    "moonriver": "moonriver",
    "muu": "muu",
    "nova network": "nova",
    "okc": "oec",
    "oasis": "oasis",
    "opbnb": "opbnb",
    "optimism": "optimism",
    "polygon": "polygon",
    "polygon zkevm": "polygonzkevm",
    "proof of memes": "pom",
    "pulsechain": "pulse",
    "redlight": "redlight",
    "ronin": "ronin",
    "rsk": "rsk",
    "shib": "shib",
    "shibarium": "shibarium",
    "shibarum": "shibarium",
    "shiden": "shiden",
    "smartbch": "smartbch",
    "solana": "solana",
    "starknet": "starknet",
    "sx": "sx",
    "syscoin": "syscoin",
    "telos": "telos",
    "thundercore": "thundercore",
    "tomb": "tomb",
    "tomo": "tomo",
    "ultron": "ultron",
    "velas": "velas",
    "wan": "wan",
    "zksync": "zksync",
    "elrond": "elrond",
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
    "website": "🌐 WebSite",
    "youtube": "🎥 YouTube",
}


class DexTool:
    def __init__(self, session):
        self.session = session

    async def aiohttp_get(self, chain: str, address: str, url: str, dextool_key: str) -> dict:
        headers = {
            "accept": "application/json",
            "X-API-Key": dextool_key
        }

        async with self.session.get(url, headers=headers) as response:
            data = await response.text()
        parsed_data = json.loads(data)
        return parsed_data

    async def aiohttp_post(self, url, headers, dt) -> dict:
        async with self.session.post(url, headers=headers, json=dt) as response:
            data = await response.text()
        parsed_data = json.loads(data)

        return parsed_data

    async def analyze(self, address: str, data: dict, dextool_key: str) -> dict:
        try:
            if DEXTOOL.get(data['base']['platformName'].lower()) is not None:
                chain = DEXTOOL.get(data['base']['platformName'].lower())
                url = f"https://api.dextools.io/v1/token?chain={chain}&address={address}"
                response = await self.aiohttp_get(chain, address, url, dextool_key)
                links = {key: value for key,
                         value in response['data']['links'].items() if value != ""}
                if links:
                    data['social_links'] = links
            return data
        except Exception as e:
            return data
