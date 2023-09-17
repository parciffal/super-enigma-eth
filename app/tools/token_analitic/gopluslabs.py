from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.markdown import link
import aiohttp
import json
import time
import locale
from pprint import pprint
import logging
from datetime import datetime

from aiogram.utils.text_decorations import html_decoration as hd
from tortoise.fields import relational

from app.db.models import GroupModel
from app.tools.token_analitic.api_urls import gopluslabs, coinmarketcap, geckoterminal
from app.tools.token_analitic.tools import LINKS
from app.tools.advertize_manager import ads_manager
from app.keyboards.inline.rug_check_keyboard import get_link_keyboard


async def base_info_tamplate() -> dict:
    return {
        "base": {
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


async def shorten_number(number):
    suffixes = ["", "K", "M", "B", "TR"]
    suffix_index = 0

    while number >= 1000 and suffix_index < len(suffixes) - 1:
        suffix_index += 1
        number /= 1000.0

    return f"{number:.2f} {suffixes[suffix_index]}"


async def add_commas_to_float(number):
    return "{:,}".format(number)


class GoPlusLabs:
    ETH = 1
    BTC = 56
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
    BOOL = {"1": False, "0": True}
    CH_BOOL = {"1": True, "0": False}
    MSG_BOOL = {"0": "✅", "1": "🚫"}
    CHECK_BOOL = {"1": "✅", "0": "🚫"}
    QUICK_BOOL = {False: "✅", True: "🚫", None: "🚫", }
    QUICK_REVERSE = {True: "✅", False: "🚫"}

    def __init__(self):
        self.session = aiohttp.ClientSession()
        # Set the locale to the user's default locale
        self.locale = locale.setlocale(locale.LC_ALL, "")

    async def aiohttp_get(self, url, headers={}) -> dict:
        # start = time.time()
        async with self.session.get(url, headers=headers) as response:
            data = await response.text()
        parsed_data = json.loads(data)
        # print(time.time() - start)
        return parsed_data

    async def aiohttp_post(self, url, headers, dt) -> dict:
        # start = time.time()
        # print(time.time() - start)
        async with self.session.post(url, headers=headers, json=dt) as response:
            data = await response.text()
        parsed_data = json.loads(data)

        return parsed_data

    async def get_token_base_info_dex(self, address) -> dict:
        data = await self.get_dex_data(address)
        if data:
            template = await base_info_tamplate()
            template["base"]["platformId"] = self.CHAINS[
                data['chainId']
            ]
            template["base"]["platformName"] = data['chainId']
            template["base"]["baseTokenName"] = data['baseToken']['name']
            template["base"]["baseTokenSymbol"] = data['baseToken']["symbol"]
            template["base"]["identifier"] = data['chainId']
            return template
        else:
            return {"base": None}

    async def get_token_base_info(self, address) -> dict:
        url = await coinmarketcap("get_coinmarket_base_info", address)
        data = await self.aiohttp_get(url)
        try:
            if data["status"]["error_code"] in [0, "0"]:
                data["base"] = data["data"]["pairs"][0]
                print(2)
                return data
            else:
                return await self.get_token_base_info_dex(address)
        except:
            return await self.get_token_base_info_dex(address)

    async def get_gecko_base_info(self, address) -> dict:
        url = await coinmarketcap("get_gecko_base_info", address)
        data = await self.aiohttp_get(url)
        template = await base_info_tamplate()
        try:
            if data["data"]["attributes"]["pools"][0]:
                try:
                    kl = data["data"]["attributes"]["pools"][0]
                    template["base"]["platformId"] = self.CHAINS[
                        kl["network"]["identifier"]
                    ]
                    template["base"]["platformName"] = kl["network"]["name"]
                    template["base"]["baseTokenName"] = kl["tokens"][0]["name"]
                    template["base"]["baseTokenSymbol"] = kl["tokens"][0]["symbol"]
                    template["base"]["identifier"] = kl["network"]["identifier"]
                    return template
                except:
                    data = await self.get_token_base_info(address)
                    return data
            else:
                return await self.get_token_base_info(address)
        except:
            return await self.get_token_base_info(address)

    async def get_token_security_info(self, data: dict, address) -> dict:
        url = await gopluslabs(
            "get_address_info",
            address,
            self.CHAINS[data["base"]["platformName"].lower()],
        )
        data_s = await self.aiohttp_get(url)
        if data_s["result"][address.lower()]:
            data["data"] = data_s["result"][address.lower()]
        else:
            data["data"] = None
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

    async def check_quick_message(self, data, liquidity) -> int:
        count = 0
        try:
            if (
                data["data"]["is_Honeypot"] == False
            ):
                count += 1
        except:
            pass
        try:
            if (
                data["data"]["is_Mintable"] == False
            ):
                count += 1
        except:
            pass
        try:
            if (
                data["data"]["is_Proxy"] == False
            ):
                count += 1
        except:
            pass
        try:
            if (
                data["data"]["can_Blacklist"] == False
            ):
                count += 1
        except:
            pass
        try:
            if (
                data["data"]["contract_Verified"]
            ):
                count += 1
        except:
            pass
        if liquidity != "":
            count += 1

        return count

    async def get_quick_message(self, data, liquidity):
        try:
            count = await self.check_quick_message(data, liquidity)
            honey_pot = self.QUICK_BOOL[data['data']['is_Honeypot']] if data['data'].get(
                'is_Honeypot') is not None else f"<b>N/A</b>"
            mintable = self.QUICK_BOOL[data['data']['is_Mintable']] if data['data'].get(
                'is_Mintable') is not None else f"<b>N/A</b>"
            proxy = self.QUICK_BOOL[data['data']['is_Proxy']] if data['data'].get(
                'is_Proxy') is not None else f"<b>N/A</b>"
            blacklisted = self.QUICK_BOOL[data['data']['can_Blacklist']] if data['data'].get(
                'can_Blacklist') is not None else f"<b>N/A</b>"

            in_dex = self.QUICK_BOOL[False] if liquidity != "" else self.QUICK_BOOL[True]
            contract_verified = self.QUICK_REVERSE[data['data']['contract_Verified']] if data['data'].get(
                'contract_Verified') is not None else f"{self.QUICK_REVERSE[False]}"

            return (
                f"<b>🛡️Safety Test's</b>\n\n"
                f"<b>🍯Honeypot: </b> {honey_pot}\n"
                f"<b>🖨️Mintable: </b> {mintable}\n"
                f"<b>🔄Proxy: </b> {proxy}\n"
                f"<b>🚫Blacklisted: </b> {blacklisted}\n"
                f"<b>📈In Dex: </b> {in_dex}\n"
                f"<b>🌐Contract Verified: </b> {contract_verified}\n\n"
                f"🧪 <b>{count}/6 Test's passed</b> 🧪\n\n"
            )
        except Exception as e:
            return ""

    async def get_message_analytic(self, data, liquidity):
        try:
            if data.get('data') and data.get("data").get("is_honeypot"):
                count = await self.check_get_message_analytic(data)
                honeypot = self.MSG_BOOL[data['data']['is_honeypot']] if data['data'].get(
                    'is_honeypot') else f"<b>N/A </b> "
                mintable = self.MSG_BOOL[data['data']['is_mintable']] if data['data'].get(
                    'is_mintable') else f"<b>N/A </b> "
                proxy = self.MSG_BOOL[data['data']['is_proxy']] if data['data'].get(
                    'is_proxy') else f"<b>N/A </b> "
                blacklisted = self.MSG_BOOL[data['data']['is_blacklisted']] if data['data'].get(
                    'is_blacklisted') else f"<b>N/A </b> "
                in_dex = self.CHECK_BOOL[data['data']['is_in_dex']] if data['data'].get(
                    'is_in_dex') else f"{self.MSG_BOOL['1']}"
                open_source = self.CHECK_BOOL[data['data']['is_open_source']] if data['data'].get(
                    'is_open_source') else f"{self.MSG_BOOL['1']}"
                return (
                    f"<b>🛡️Safety Test's</b>\n\n"
                    f"<b>🍯Honeypot: </b> {honeypot}\n"
                    f"<b>🖨️Mintable: </b> {mintable}\n"
                    f"<b>🔄Proxy: </b> {proxy}\n"
                    f"<b>🚫Blacklisted: </b> {blacklisted}\n"
                    f"<b>📈In Dex: </b> {in_dex}\n"
                    f"<b>🌐Open Source: </b> {open_source}\n\n"
                    f"🧪 <b>{count}/6 Test's passed</b> 🧪\n\n"
                )
            else:
                return await self.get_quick_message(data, liquidity=liquidity)
        except:
            return ""

    async def calculate_age(self, data):
        try:
            current_time = datetime.utcnow()
            creation_time = datetime.strptime(data['full']["attributes"]["pool_created_at"],
                                              "%Y-%m-%dT%H:%M:%S.%fZ")
            days = (current_time - creation_time).days
            if days:
                return f"<b>📅 Contract Age:</b> Created {days} days ago\n"
            else:
                return ""
        except:
            return ""

    async def calculate_days_left(self, locked_detail):
        try:
            if not locked_detail:
                return None
            end_time_str = locked_detail[0]["end_time"]
            end_time = datetime.strptime(
                end_time_str, "%Y-%m-%dT%H:%M:%S+00:00")
            current_time = datetime.utcnow()
            days_left = (end_time - current_time).days
            return days_left
        except:
            return None

    async def get_lp_locked(self, data):
        try:
            for i in data["data"]["holders"]:
                if i["is_locked"] == 1:
                    print(i['is_locked'])
                    try:
                        days = await self.calculate_days_left(i["locked_detail"])
                        if days > 0:
                            return f"<b>🔐 LP Locked: {round(float(i['percent'])*100, 2)} % </b> on <b>{i['tag']}</b>  for <b>{days} Days</b> \n"
                        else:
                            return f"<b>🔐 LP Locked: {round(float(i['percent'])*100, 2)} % </b> on <b>{i['tag']}</b>  <b>Expired for {-1*days} Days</b> \n"
                    except:
                        return f"<b>🔐 LP Locked: {round(float(i['percent'])*100, 2)} % </b> on <b>{i['tag']}</b>\n"
            return ""
        except:
            return ""

    async def get_top_holders(self, data):
        links = LINKS[self.CHAINS[data["base"]["platformName"].lower()]]
        if links.get('browserScanAddress') != "":
            url = links.get('browserScanAddress')
        else:
            url = None
        if data.get('data'):
            if data['data'].get('holders'):
                msg = "<b>📊 Top Holders: </b>"
                for holder in data['data']['holders']:
                    if url is not None:
                        percent = str(round(float(holder['percent'])*100))+"%"
                        txt = hd.link(percent, url+holder['address'])
                    else:
                        txt = str(round(float(holder['percent'])*100))+"%"
                    msg += f"{txt} |"
                return msg+"\n"
        return ""

    async def get_pair(self, data):
        for include in data['included']:
            if include['type'] == 'pair':
                links = LINKS[self.CHAINS[data["base"]
                                          ["platformName"].lower()]]
                if links.get('browserScan') != "":
                    url = links.get('browserScanAddress')
                else:
                    url = None
                pair = hd.link("View on Scan", url +
                               include['attributes']['quote_address'])
                return f"<b>🔄 Pair: </b> {pair} \n"
        return ""

    async def get_buy_tax(self, data):
        try:
            buy_tax = round(float(data['data']['buy_tax'])*100, 2)
            msg = f"{buy_tax} %" if buy_tax else ' N\A '
            return f"<b>💰 Buy Tax: </b> {msg}\n"
        except:
            try:
                buy_tax = data['data']['buy_Tax']
                if buy_tax is None:
                    return f"<b>💰 Buy Tax: </b> N\A \n"
                msg = f"{buy_tax} %" if buy_tax else ' N\A '
                return f"<b>💰 Buy Tax: </b> {msg}\n"
            except:
                return ""

    async def get_sell_tax(self, data):
        try:
            sell_tax = round(float(data['data']['sell_tax'])*100, 2)
            msg = f"{sell_tax} %" if sell_tax else ' N\A '
            return f"<b>💸 Sell Tax: </b> {msg}\n"
        except:
            try:
                sell_tax = data['data']['sell_Tax']
                msg = f"{sell_tax} %" if sell_tax else ' N\A '
                return f"<b>💸 Sell Tax: </b> {msg}\n"
            except:
                return ""

    async def get_creator(self, data):
        try:
            creator = data['data']['creator_address']
            return f"<b>🧑‍🎨 Creator:</b> {hd.code(creator)}\n"
        except:
            return ""

    async def get_owner(self, data):
        try:
            owner = data['data']['owner_address']
            return f"<b>👤 Owner: </b> {hd.code(owner)}\n"
        except:
            return ""

    async def get_liquidity(self, data):
        try:
            liquidity = await add_commas_to_float(
                round(float(data["full"]["attributes"]["reserve_in_usd"]), 2)
            )
            print(liquidity)
            return f"<b>💰 Liquidity:</b> {liquidity} $\n"
        except:
            return ""

    async def get_marketcap(self, data):
        try:
            marketcup = await add_commas_to_float(
                round(float(data["full"]["attributes"]
                      ["fully_diluted_valuation"]))
            )
            return f"<b>📊 Market Cap:</b> {marketcup} $\n"
        except:
            return ""

    async def get_pairing(self, data):
        try:
            return f"<b>🔄 Pairing:</b> {data['full']['attributes']['name']}\n"
        except:
            return ""

    async def get_chain(self, data):
        try:
            return f"<b>🌐 Chain:</b> {data['base']['platformName']}\n\n"
        except:
            return ""

    async def get_dex_data(self, address):
        try:
            data = await self.aiohttp_get(f"https://api.dexscreener.com/latest/dex/search?q={address}")
            return data['pairs'][0]
        except:
            return None

    async def calc_created(self, data):
        try:
            current_time = datetime.utcnow()
            creation_timestamp_ms = int(data['pairCreatedAt'])
            creation_time = datetime.utcfromtimestamp(
                creation_timestamp_ms / 1000.0)
            days = (current_time - creation_time).days
            if days:
                return f"<b>📅 Pair Created</b>: {days} Days ago\n"
            else:
                return ""
        except:
            return ""

    async def get_dex_pair(self, data, address):
        try:
            links = LINKS[self.CHAINS[data["base"]
                                      ["platformName"].lower()]]
            if links.get('browserScan') != "":
                url = links.get('browserScanAddress')
            else:
                url = None
            pair = hd.link("View on Scan", url + address)
            return f"<b>👁️ Pair: </b> {pair} \n"
        except:
            return ""

    async def quickintel_audit(self, data, address):
        try:
            start = time.time()
            url = "https://qpi.quickintel.io/api/getthirdaudit"

            headers = {"api_key": "0xs-KUen48jjdHV223ss",
                       "Content-Type": "application/json"}
            payload = {
                "chain": data['base']['identifier'],
                "tokenAddress": address,
                "id": "0xs",
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as resp:
                    # print(resp.status)
                    # print(await resp.json())
                    data['data'] = await resp.json()
            print("Quick Audit: ", time.time() - start)
            return data
        except:
            return data

    async def get_message(self, data, bot, address) -> str:
        ads, media = await ads_manager.get_ads(bot)
        age = await self.calculate_age(data)
        top_holders = await self.get_top_holders(data)
        pair = await self.get_pair(data)
        bot_info = await bot.get_me()
        marketcap = await self.get_marketcap(data)
        lp_locked = await self.get_lp_locked(data)
        buy_tax = await self.get_buy_tax(data)
        sell_tax = await self.get_sell_tax(data)
        creator = await self.get_creator(data)
        owner = await self.get_owner(data)
        pairing = await self.get_pairing(data)
        chain = await self.get_chain(data)
        dex_data = await self.get_dex_data(address)
        liquidity = await self.get_liquidity(data)
        try:
            liquidity = f"<b>💰 Liquidity:</b> {dex_data['liquidity']['usd']} $\n"
        except:
            pass
        test = await self.get_message_analytic(data, liquidity)
        # pprint(data['data'])
        if pair == "":
            try:
                pair = await self.get_dex_pair(data, dex_data['quoteToken']['address'])
            except:
                pass
        try:
            name = data['full']['attributes']['name']
        except:
            try:
                name = dex_data['baseToken']['name']
            except:
                name = data['base']['baseTokenName']

        try:
            liquidity_base = f"<b>🌊 Pooled {name}:</b> {await add_commas_to_float(dex_data['liquidity']['base'])}\n"
        except:
            liquidity_base = ""
        try:
            pair_created_at = await self.calc_created(dex_data)
        except:
            pair_created_at = age

        try:
            price = f"<b>💲 Price:</b> {dex_data['priceUsd']} $\n"
        except:
            price = ""

        try:
            price_change = f"<b>📉 24H Price Change: </b> {dex_data['priceChange']['h24']}%\n"
        except:
            price_change = ""

        try:
            txns = f"📈 <b>24H Txns:</b>"
            txns += f"\n       <b>|_🟢 Buy:</b> {dex_data['txns']['h24']['buys']} "
            txns += f"| <b>🔴 Sell:</b> {dex_data['txns']['h24']['sells']}\n"
        except:
            txns = ""

        message = (
            f"{media}"
            f"@{bot_info.username} | "
            f"your 🔎 0XS RESULTS 🔍 for <b>{hd.code(name.upper())}</b> Token!\n"
            f"<b>🏷️ Name: </b> {hd.code(name)}\n"
            f"<b>🔗 CA: </b> {hd.code(address)}\n"
            f"{chain}"
            f"{test}"
            f"{buy_tax}"
            f"{sell_tax}"
            f"{creator}"
            f"{owner}"
            f"{age}"
            f"{top_holders}"
            f"\n<b>💲 Market Data 💲</b>\n"
            f"{pairing}"
            f"{pair}"
            f"{liquidity}"
            f"{liquidity_base}"
            f"{marketcap}"
            f"{price}"
            f"{price_change}"
            f"{txns}"
            f"{lp_locked}"
            f"{pair_created_at}"
            f"\n{ads}"
        )
        return message

    #
    async def get_gecko_full_info(self, address, data):
        url = await geckoterminal("get_full_info", data["base"]["identifier"], address)
        response = await self.aiohttp_get(url)
        if response.get("links"):
            response = await self.aiohttp_get(response["links"]["top_pool"])
        if response.get("data"):
            data["full"] = response["data"]
        if response.get("included"):
            data['included'] = response['included']
        else:
            data['included'] = {}
        return data

    async def get_button_links(self, data: dict, address: str) -> dict:
        keyboards = []
        links = LINKS[self.CHAINS[data["base"]["platformName"].lower()]]
        for key in links:
            url = f"{links[key]}{address}"
            name = key
            if key == "geckoterminal":
                name = "🦎 Gecko"
            if key == "dextools":
                name = "📈 Dex"
            if key == "browserScanAddress":
                name = "📡 Scan"
            keyboards.append(
                {
                    "name": name,
                    "url": url
                }
            )
        return keyboards

    async def get_token_security(self, message,  address: str, bot: Bot):
        start = time.time()
        data = await self.get_gecko_base_info(address)
        progress_msg = await bot.send_message(
            message.chat.id, text=f"🔎 0xS Analyzer on <b>{data['base']['platformName']}</b> in progress 🔍"
        )
        try:
            data = await self.get_gecko_full_info(address, data)
            try:
                if data["base"]["identifier"] != "shibarium":
                    data = await self.get_token_security_info(data, address)
                else:
                    data = await self.quickintel_audit(data, address)
            except:
                try:
                    data = await self.get_token_security_info(data, address)
                except:
                    data = await self.quickintel_audit(data, address)
            keyboards = await self.get_button_links(data, address)
            msg = await self.get_message(data, bot, address)
            print("Response Time: ", time.time() - start)
            return msg, keyboards, bot, progress_msg
        except:
            msg = "📵  <b>Apologies, but the token you are inquiring about does not currently have adequate liquidity.  \nPlease try again later.</b>"
            keyboards = None
            print("Response Time: ", time.time() - start)
            return msg, keyboards, bot, progress_msg


gopluslabs_manager = GoPlusLabs()
