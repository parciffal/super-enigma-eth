import aiohttp
import json
import time
from pprint import pprint
import logging
from datetime import datetime

from aiogram.utils.text_decorations import html_decoration as hd

from app.db.models import GroupModel
from .api_urls import gopluslabs, coinmarketcap, geckoterminal
from app.tools.advertize_manager import ads_manager
from app.keyboards.inline.rug_check_keyboard import get_link_keyboard


class GoPlusLabs:
    ETH = 1
    BTC = 56
    NULLADR = "0x0000000000000000000000000000000000000000"
    CHAINS = {
        "ethereum": "1",
        "eth": "1",
        "shibarium": "1",
        "Shibarium": "1",
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
    BOOL = {"1": False, "0": True}
    CH_BOOL = {"1": True, "0": False}
    MSG_BOOL = {"0": "✅", "1": "🚫"}
    CHECK_BOOL = {"1": "✅", "0": "🚫"}

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def aiohttp_get(self, url) -> dict:
        start = time.time()
        async with self.session.get(url) as response:
            data = await response.text()
        parsed_data = json.loads(data)
        print(time.time() - start)
        return parsed_data

    async def base_info_tamplate(self) -> dict:
        return {
            "baseInfo": {
                "platformId": "",
                "platformName": "",
                "baseTokenSymbol": "",
                "quoteTokenSymbol": "",
                "liquidity": "",
                "pairContractAddress": "",
                "platFormCryptoId": "",
                "exchangeId": "",
                "poolId": "",
                "baseTokenName": "",
                "identifier": "",
                "creation_date": "",
            }
        }

    async def get_token_base_info(self, address) -> dict:
        url = await coinmarketcap("get_coinmarket_base_info", address)
        data = await self.aiohttp_get(url)
        if data["status"]["error_code"] in [0, "0"]:
            data["baseInfo"] = data["data"]["pairs"][0]
            return data
        else:
            return {"baseInfo": None}

    async def get_gecko_base_info(self, address) -> dict:
        url = await coinmarketcap("get_gecko_base_info", address)
        data = await self.aiohttp_get(url)
        template = await self.base_info_tamplate()
        if data["data"]["attributes"]["pools"][0]:
            try:
                kl = data["data"]["attributes"]["pools"][0]
                template["baseInfo"]["platformId"] = self.CHAINS[
                    kl["network"]["identifier"]
                ]
                template["baseInfo"]["platformName"] = kl["network"]["name"]
                template["baseInfo"]["baseTokenName"] = kl["tokens"][0]["name"]
                template["baseInfo"]["baseTokenSymbol"] = kl["tokens"][0]["symbol"]
                template["baseInfo"]["identifier"] = kl["network"]["identifier"]
                return template
            except:
                data = await self.get_token_base_info(address)
                return data
        else:
            return await self.get_token_base_info(address)

    async def get_token_security_info(self, data: dict, address) -> dict:
        url = await gopluslabs(
            "get_address_info",
            address,
            self.CHAINS[data["baseInfo"]["platformName"].lower()],
        )
        data_s = await self.aiohttp_get(url)
        if data_s["result"][address.lower()]:
            data["data"] = data_s["result"][address.lower()]
        else:
            data["data"] = None
        return data

    async def shorten_number(self, number):
        if number >= 1_000_000_000_000:  # Trillions
            return f"{number / 1_000_000_000_000:.2f} <b>TR</b>"
        elif number >= 1_000_000_000:  # Billions
            return f"{number / 1_000_000_000:.2f} <b>B</b>"
        elif number >= 1_000_000:
            return f"{number/ 1_000_000:.2f} <b>M</b>"
        else:
            return str(number)

    async def get_button_links(self, data: dict, chain: str, address: str) -> dict:
        if chain == "bsc":
            data["links"].append(
                {"name": "🔸BSCScan", "url": f"https://bscscan.com/token/{address}"}
            )
        elif chain == "ethereum":
            data["links"].append(
                {"name": "🔹ETHScan", "url": f"https://etherscan.io/token/{address}"}
            )
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
    async def check_get_message_analytic(self, data) -> int:
        count = 0
        if (
            self.BOOL[data["data"]["is_honeypot"]]
            if data["data"].get("is_honeypot")
            else None
        ):
            count += 1
        if (
            self.BOOL[data["data"]["is_mintable"]]
            if data["data"].get("is_mintable")
            else None
        ):
            count += 1
        if (
            self.BOOL[data["data"]["is_proxy"]]
            if data["data"].get("is_proxy")
            else None
        ):
            count += 1
        if (
            self.BOOL[data["data"]["is_blacklisted"]]
            if data["data"].get("is_blacklisted")
            else None
        ):
            count += 1
        if (
            self.CH_BOOL[data["data"]["is_in_dex"]]
            if data["data"].get("is_in_dex")
            else None
        ):
            count += 1
        if (
            self.CH_BOOL[data["data"]["is_open_source"]]
            if data["data"].get("is_open_source")
            else None
        ):
            count += 1

        return count

    async def get_message_analytic(self, data):
        count = await self.check_get_message_analytic(data)
        return (
            f"<b>------------------🛡️Safety Level</b>\n\n"
            f"<b>🍯Honeypot: </b> {self.MSG_BOOL[data['data']['is_honeypot']] if data['data'].get('is_honeypot') else self.MSG_BOOL['1']}    "
            f"<b>🖨️Mintable: </b> {self.MSG_BOOL[data['data']['is_mintable']] if data['data'].get('is_mintable') else self.MSG_BOOL['1']}\n"
            f"<b>🔄Proxy: </b> {self.MSG_BOOL[data['data']['is_proxy']] if data['data'].get('is_proxy') else self.MSG_BOOL['1']}           "
            f"<b>🚫Blacklisted: </b> {self.MSG_BOOL[data['data']['is_blacklisted']] if data['data'].get('is_blacklisted') else self.MSG_BOOL['1']}\n"
            f"<b>📈In Dex: </b> {self.CHECK_BOOL[data['data']['is_in_dex']] if data['data'].get('is_in_dex') else self.MSG_BOOL['1']}          "
            f"<b>🌐Open Source: </b> {self.CHECK_BOOL[data['data']['is_open_source']] if data['data'].get('is_open_source') else self.MSG_BOOL['1']}\n\n"
            f"                     🧪 <b>{count}/6 Test's passed</b> 🧪\n\n"
        )

    async def calculate_days_left(self, locked_detail):
        if not locked_detail:
            return None
        end_time_str = locked_detail[0]["end_time"]
        end_time = datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%S+00:00")
        current_time = datetime.utcnow()
        days_left = (end_time - current_time).days
        return days_left

    async def calculate_age(self, creation_date):
        current_time = datetime.utcnow()
        creation_time = datetime.strptime(creation_date, "%Y-%m-%dT%H:%M:%S.%fZ")

        days_passed = (current_time - creation_time).days
        return days_passed

    async def get_token_liquidity(self, data):
        msg = ""
        if data["data"].get("dex")[0]:
            msg += f"<b>💧Liquidity:</b> {round(float(data['data'].get('dex')[0]['liquidity'])) } $\n"
        else:
            msg.append(f"<b>💧Liquidity:</b> 0$\n")
        if data["data"].get("lp_holders"):
            for i in data["data"]["lp_holders"]:
                if i["is_locked"] == 1:
                    try:
                        days = await self.calculate_days_left(i["locked_detail"])
                        if days > 0:
                            msg += f"<b>🔐LP Locked: {round(float(i['percent'])*100, 2)} % </b> on <b>{i['tag']}</b>  for <b>{days} Days</b> \n"
                        else:
                            msg += f"<b>🔐LP Locked: {round(float(i['percent'])*100, 2)} % </b> on <b>{i['tag']}</b>  <b>Expired for {-1*days} Days</b> \n"

                    except:
                        msg += f"<b>🔐LP Locked: {round(float(i['percent'])*100, 2)} % </b> on <b>{i['tag']}</b>\n"
                    break
        if data["baseInfo"]["creation_date"] != "":
            if data["baseInfo"]["creation_date"] > 0:
                days = data["baseInfo"]["creation_date"]
                msg += f"<b>⌛️ Age: {days} Days</b>\n"
        return msg

    #
    async def get_message(self, data, bot, address) -> str:
        ads = await ads_manager.get_ads(bot)
        test = await self.get_message_analytic(data)
        liquidity = await self.get_token_liquidity(data)
        bot_info = await bot.get_me()
        message = (
            f"@{bot_info.username} |"
            f" 🚨 <b>{hd.code(data['data']['token_name'].upper()) if data['data'].get('token_name') else None}</b> 🚨 |"
            f" <code>{data['baseInfo']['platformName']} </code>\n\n"
            f"<b>---------------📝Base Token Info</b>\n\n"
            f"<b>🏦Address: </b> {hd.code(address)}\n"
            f"<b>👑Owner: </b> {hd.code(data['data']['owner_address'])}\n"
            f"<b>💼Holders:</b> {data['data']['holder_count'] if data['data'].get('holder_count') else None}\n"
            f"<b>💰Total Supply:</b> {await self.shorten_number( float(data['data']['total_supply'] )) if data['data'].get('total_supply') else None}\n"
            f"{liquidity}"
            f"<b>💸Tax: Buy: {round(float(data['data']['buy_tax'])*100, 2) if data['data'].get('buy_tax') else None}% | "
            f"Sell: {round(float(data['data']['sell_tax'])*100, 2) if data['data'].get('sell_tax') else None}%</b>\n\n"
            f"{test}"
            f"{ads}"
        )
        return message

    #
    async def get_creation_time(self, data, address):
        try:
            url = await geckoterminal(
                "get_full_info", data["baseInfo"]["identifier"], address
            )
            response = await self.aiohttp_get(url)
            print(response)
            if response["links"]["top_pool"]:
                response = await self.aiohttp_get(response["links"]["top_pool"])
            creation_date = response["data"]["attributes"]["pool_created_at"]
            days = await self.calculate_age(creation_date)
            data["baseInfo"]["creation_date"] = days
            return data
        except:
            return data

    #
    async def get_token_security(self, address, bot):
        data = await self.get_gecko_base_info(address)
        if data["baseInfo"] is not None:
            data = await self.get_token_security_info(data, address)
            if data["data"] is not None:
                chain = data["baseInfo"]["platformName"].lower()
                data["links"] = []
                data = await self.get_creation_time(data, address)
                data = await self.get_button_links(data, chain, address)
                keyboards = await get_link_keyboard(data)
                msg = await self.get_message(data, bot, address)
                return msg, keyboards
            else:
                msg = "📈 <b>We apologize, but the requested token currently does not possess an available analytic report.</b>"
                keyboards = None
                return msg, keyboards
        else:
            msg = "📵  <b>Apologies, but the token you are inquiring about does not currently have adequate liquidity.  \nPlease try again later.</b>"
            keyboards = None
            return msg, keyboards


gopluslabs_manager = GoPlusLabs()
