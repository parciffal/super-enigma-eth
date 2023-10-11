from aiogram import Bot
from aiogram.utils.text_decorations import html_decoration as hd
from datetime import datetime
from pprint import pprint

from app.tools.advertize_manager import ads_manager
from app.tools.token_analitic.apis import DEXTOOL, DEXTOOL_EMOJI
from app.tools.token_analitic.tools import *


class MessageCreater:
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
    CHAIN_FULL_NAMES = {
        "ethereum": "Ethereum",
        "eth": "Ethereum",
        "shibarium": "Shibarium",
        "Shibarium": "Shibarium",
        "optimism": "Optimism",
        "cronos": "Cronos",
        "bsc": "Binance Smart Chain",
        "bnb chain": "Binance Smart Chain",
        "okc": "OKExChain",
        "gnosis": "Gnosis Chain",
        "heco": "Huobi Eco Chain",
        "polygon": "Polygon",
        "fantom": "Fantom",
        "kcc": "KuCoin Community Chain",
        "zksync era": "zkSync Era",
        "zksync": "zkSync",
        "ethw": "EtherLite",
        "fon": "Ferrum Network",
        "arbitrum": "Arbitrum",
        "avalanche": "Avalanche",
        "linea mainet": "Linea Mainnet",
        "linea testnet": "Linea Testnet",
        "base": "Basecoin",
        "harmony": "Harmony",
        "tron": "Tron",
    }

    DEXTOOL_CHAINS = DEXTOOL

    BOOL = {"1": False, "0": True}
    CH_BOOL = {"1": True, "0": False}
    MSG_BOOL = {"0": "✅", "1": "🚫"}
    CHECK_BOOL = {"1": "✅", "0": "🚫"}
    QUICK_BOOL = {False: "✅", True: "🚫", None: "🚫", }
    QUICK_REVERSE = {True: "✅", False: "🚫"}

    def __init__(self) -> None:
        pass

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

    async def get_pair(self, data, address):
        pair = ""
        for include in data.get('included', []):
            if include.get('type') == 'pair':
                links = LINKS.get(self.CHAINS.get(
                    data['base']['platformName'].lower(), ""), {})
                url = links.get('browserScanAddress') if links.get(
                    'browserScan') != "" else None
                pair = hd.link("View on Scan", url +
                               include['attributes']['quote_address'])
                return f"<b>🔄 Pair: </b>{pair} \n"

        try:
            address = data['dex']['quoteToken']['address']
            links = LINKS.get(self.CHAINS.get(
                data['base']['platformName'].lower(), ""), {})
            url = links.get('browserScanAddress') if links.get(
                'browserScan') != "" else None
            pair = hd.link("View on Scan", url + address)
        except:
            pass

        if pair == "":
            try:
                pair = data['full']['attributes']['name']
            except:
                return ""

        return f"<b>🔄 Pair: </b>{pair} \n"

    async def get_marketcap(self, data):
        try:
            marketcup = await add_commas_to_float(
                round(float(data["full"]["attributes"]
                      ["fully_diluted_valuation"]))
            )
            return f"<b>📊 Market Cap:</b> {marketcup} $\n"
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
                    try:
                        days = await self.calculate_days_left(i["locked_detail"])
                        if days > 0:
                            return f"<b>🔐 LP Locked: {round(float(i['percent'])*100, 2)} % </b>on <b>{i['tag']}</b>  for <b>{days} Days</b> \n"
                        else:
                            return f"<b>🔐 LP Locked: {round(float(i['percent'])*100, 2)} % </b>on <b>{i['tag']}</b>  <b>Expired for {-1*days} Days</b> \n"
                    except:
                        return f"<b>🔐 LP Locked: {round(float(i['percent'])*100, 2)} % </b>on <b>{i['tag']}</b>\n"
            return ""
        except:
            return ""

    async def get_buy_tax(self, data):
        try:
            buy_tax = round(float(data['data']['buy_tax'])*100, 2)
            msg = f"{buy_tax} %" if buy_tax else 'N\A'
            return f"<b>💰 Buy Tax: </b>{msg}\n"
        except:
            try:
                buy_tax = data['data']['buy_Tax']
                if buy_tax is None:
                    return f"<b>💰 Buy Tax: </b>N\A\n"
                msg = f"{buy_tax} %" if buy_tax else 'N\A'
                return f"<b>💰 Buy Tax: </b>{msg}\n"
            except:
                return ""

    async def get_sell_tax(self, data):
        try:
            sell_tax = round(float(data['data']['sell_tax'])*100, 2)
            msg = f"{sell_tax} %" if sell_tax else 'N\A'
            return f"<b>💸 Sell Tax: </b>{msg}\n"
        except:
            try:
                sell_tax = data['data']['sell_Tax']
                msg = f"{sell_tax} %" if sell_tax else 'N\A '
                return f"<b>💸 Sell Tax: </b>{msg}\n"
            except:
                return ""

    async def get_creator(self, data):
        try:
            creator = data['data']['creator_address']
            return f"<b>🧑‍🎨 Creator: </b>{hd.code(creator)}\n"
        except:
            return ""

    async def get_owner(self, data):
        try:
            owner = data['data']['owner_address']
            return f"<b>👤 Owner: </b>{hd.code(owner)}\n"
        except:
            return ""

    async def get_chain(self, data):
        try:
            chain  = self.CHAIN_FULL_NAMES.get(data['base']['platformName'], data['base']['platformName'])
            return f"<b>🌐 Chain: </b>{hd.code(chain)}\n\n"
        except:
            return ""

    async def get_liquidity(self, data):
        try:
            liquidity = await add_commas_to_float(round(float(data["full"]["attributes"]["reserve_in_usd"]), 2))
        except (KeyError, ValueError):
            try:
                liquidity = await add_commas_to_float(round(float(data['dex']['liquidity']['usd']), 2))
            except (KeyError, ValueError):
                return ""
        return f"<b>💰 Liquidity:</b> {liquidity} $\n"

    async def get_social_links(self, data):
        try:
            msg = "\n🌐<b> Social Media </b>🌐\n\n"
            if data.get("social_links") is None:
                return ""
            else:
                social_links = data['social_links']
                count = 0
                for key, value in social_links.items():
                    if count == 4:
                        count = 0
                        msg += "\n"
                    msg += f"{hd.link(DEXTOOL_EMOJI[key], value)}  "
                    count += 1
                return msg+"\n"
        except:
            return ""

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
                f"<b>🍯Honeypot: </b>{honey_pot}\n"
                f"<b>🖨️Mintable: </b>{mintable}\n"
                f"<b>🔄Proxy: </b>{proxy}\n"
                f"<b>🚫Blacklisted: </b>{blacklisted}\n"
                f"<b>📈In Dex: </b>{in_dex}\n"
                f"<b>🌐Contract Verified: </b>{contract_verified}\n\n"
                f"🧪 <b>{count}/6 Test's passed</b> 🧪\n\n"
            )
        except Exception as e:
            print(e)
            return ""

    async def get_message_analytic(self, data, liquidity):
        try:
            if data.get('data') and data.get("data").get("is_honeypot"):
                count = await self.check_get_message_analytic(data)
                honeypot = self.MSG_BOOL[data['data']['is_honeypot']] if data['data'].get(
                    'is_honeypot') else f"<b>N/A </b>"
                mintable = self.MSG_BOOL[data['data']['is_mintable']] if data['data'].get(
                    'is_mintable') else f"<b>N/A </b>"
                proxy = self.MSG_BOOL[data['data']['is_proxy']] if data['data'].get(
                    'is_proxy') else f"<b>N/A </b>"
                blacklisted = self.MSG_BOOL[data['data']['is_blacklisted']] if data['data'].get(
                    'is_blacklisted') else f"<b>N/A </b>"
                in_dex = self.CHECK_BOOL[data['data']['is_in_dex']] if data['data'].get(
                    'is_in_dex') else f"{self.MSG_BOOL['1']}"
                open_source = self.CHECK_BOOL[data['data']['is_open_source']] if data['data'].get(
                    'is_open_source') else f"{self.MSG_BOOL['1']}"
                return (
                    f"<b>🛡️Safety Test's</b>\n\n"
                    f"<b>🍯Honeypot: </b>{honeypot}\n"
                    f"<b>🖨️Mintable: </b>{mintable}\n"
                    f"<b>🔄Proxy: </b>{proxy}\n"
                    f"<b>🚫Blacklisted: </b>{blacklisted}\n"
                    f"<b>📈In Dex: </b>{in_dex}\n"
                    f"<b>🌐Open Source: </b>{open_source}\n\n"
                    f"🧪 <b>{count}/6 Test's passed</b> 🧪\n\n"
                )
            else:
                return await self.get_quick_message(data, liquidity=liquidity)
        except:
            return ""

    async def get_base_liquidity(self, name, data):
        try:
            return f"<b>🌊 Pooled {name}:</b> {await add_commas_to_float(data['dex']['liquidity']['base'])}\n"
        except:
            return ""

    async def get_name(self, data):
        try:
            return data['full']['attributes']['name']
        except:
            try:
                return data['dex']['baseToken']['name']
            except:
                return data['base']['baseTokenName']

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

    async def get_pair_created_at(self, data, age):
        try:
            return await self.calc_created(data['dex'])
        except:
            return age

    async def get_price(self, data):
        try:
            return f"<b>💲 Price:</b> {data['dex']['priceUsd']} $\n"
        except:
            return ""

    async def get_price_change(self, data):
        try:
            return f"<b>📉 24H Price Change:</b> {data['dex']['priceChange']['h24']}%\n"
        except:
            return ""

    async def get_txns(self, data):
        try:
            txns = f"📈 <b>24H Txns:</b>"
            txns += f"\n       <b>|_🟢 Buy: </b>{data['dex']['txns']['h24']['buys']} "
            txns += f"| <b>🔴 Sell: </b>{data['dex']['txns']['h24']['sells']}\n"
            return txns
        except:
            return ""

    async def collect_info(self, address: str, data: dict, bot: Bot) -> dict:
        msg_data = {}
        msg_data['ads'], msg_data['media'] = await ads_manager.get_ads(bot)
        msg_data['name'] = await self.get_name(data)
        msg_data['age'] = await self.calculate_age(data)
        msg_data['top_holders'] = await self.get_top_holders(data)
        msg_data['pair'] = await self.get_pair(data, address)
        msg_data['marketcap'] = await self.get_marketcap(data)
        msg_data['lp_locked'] = await self.get_lp_locked(data)
        msg_data['buy_tax'] = await self.get_buy_tax(data)
        msg_data['sell_tax'] = await self.get_sell_tax(data)
        msg_data['creator'] = await self.get_creator(data)
        msg_data['owner'] = await self.get_owner(data)
        msg_data['chain'] = await self.get_chain(data)
        msg_data['liquidity'] = await self.get_liquidity(data)
        msg_data['social_links'] = await self.get_social_links(data)
        msg_data['test'] = await self.get_message_analytic(data, msg_data.get('liquidity'))
        msg_data['liquidity_base'] = await self.get_base_liquidity(msg_data['name'], data)
        msg_data['pair_created_at'] = await self.get_pair_created_at(data, msg_data['age'])
        msg_data['price'] = await self.get_price(data)
        msg_data['price_change'] = await self.get_price_change(data)
        msg_data['txns'] = await self.get_txns(data)
        return msg_data
    
    async def market_data_section(self, msg_data: dict) -> str:
        keys = ['pair', 'liquidity', 'liquidity_base', 'marketcap', 'price', 'price_change', "txns", 'lp_locked', 'pair_created_at']
        section = ""
        passed = False
        for key in keys:
            if msg_data.get(key) is not None and msg_data.get(key) != "":
                passed = True
                section += f"{msg_data[key]}"
        if passed:
            section = f"\n<b>💲 Market Data 💲</b>\n\n"+ section
        return section

    async def create(self, address: str, data: dict, bot: Bot):
        bot_info = await bot.get_me()
        msg_data = await self.collect_info(address, data, bot)
        market_data = await self.market_data_section(msg_data)
        message = (
            f"{msg_data['media']}"
            f"@{bot_info.username} | "
            f"your 🔎 0XS RESULTS 🔍 for <b>{hd.code(msg_data['name'].upper())}</b> Token!\n"
            f"<b>🏷️ Name: </b>{hd.code(msg_data['name'])}\n"
            f"<b>🔗 CA: </b>{hd.code(address)}\n"
            f"{msg_data['chain']}"
            f"{msg_data['test']}"
            f"{msg_data['buy_tax']}"
            f"{msg_data['sell_tax']}"
            f"{msg_data['creator']}"
            f"{msg_data['owner']}"
            f"{msg_data['age']}"
            f"{msg_data['top_holders']}"
            f"{market_data}"
            f"{msg_data['social_links']}"
            f"\n{msg_data['ads']}"
        )
        return message
