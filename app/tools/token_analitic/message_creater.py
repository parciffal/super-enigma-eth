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
        "eth": "1"
    }
    CHAIN_FULL_NAMES = {
        "ethereum": "Ethereum",
        "eth": "Ethereum"
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
        links = LINKS[self.CHAINS['eth']]
        if links.get('browserScanAddress') != "":
            url = links.get('browserScanAddress')
        else:
            url = None
        if data.get('goplus'):
            if data['goplus'].get('holders'):
                msg = "⚖️Top holders: "
                for holder in data['goplus']['holders']:
                    if url is not None:
                        percent = str(round(float(holder['percent'])*100))+"%"
                        txt = hd.link(percent, url+holder['address'])
                    else:
                        txt = str(round(float(holder['percent'])*100))+"%"
                    if msg != "⚖️Top holders:":
                        msg += f" | {txt}"
                    else:
                        msg += f"{txt}"
                return msg+"\n"
        return ""

    async def calculate_age(self, data):
        try:
            current_time = datetime.utcnow()
            creation_time = datetime.strptime(
                data['full']["attributes"]["pool_created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            time_difference = current_time - creation_time

            days = time_difference.days
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes = remainder // 60
            if days or hours or minutes:
                age_str = ""
                if days:
                    age_str += f"{days} day{'s' if days != 1 else ''} "
                if hours:
                    age_str += f"{hours} hour{'s' if hours != 1 else ''} "
                if minutes:
                    age_str += f"{minutes} minute{'s' if minutes != 1 else ''}"
                return f"🕔 Age: <b>{age_str}</b>\n"
            else:
                return "Less than a minute"
        except:
            return ""

    async def get_marketcap(self, data):
        try:
            marketcup = await add_commas_to_float(
                round(float(data["full"]["attributes"]
                      ["fully_diluted_valuation"]))
            )
            return f"💰 MC: <b>${marketcup}</b>\n"
        except:
            return ""

    async def get_buy_tax(self, data) -> str:
        try:
            buy_tax = round(float(data['goplus']['buy_tax'])*100, 2)
            return f"{buy_tax}%"
        except:
            try:
                buy_tax = data['quick']['buy_Tax']
                return f"{buy_tax}%"
            except:
                return f"N/A"

    async def get_sell_tax(self, data) -> str:
        try:
            sell_tax = round(float(data['goplus']['sell_tax'])*100, 2)
            return f"{sell_tax}%"
        except:
            try:
                sell_tax = data['quick']['sell_Tax']
                return f"{sell_tax}%"
            except:
                return f"N/A"

    async def get_taxes(self, data) -> str:
        buy_tax = await self.get_buy_tax(data)
        sell_tax = await self.get_sell_tax(data)
        return f"💳 Taxes B/S: <b>{buy_tax} / {sell_tax}</b>\n"

    async def get_creator(self, data):
        try:
            creator = data['goplus']['creator_address']
            return creator
        except:
            return ""

    async def get_owner(self, data):
        try:
            owner = data['goplus']['owner_address']
            return f"<b>👤 Owner: </b>{hd.code(owner)}\n"
        except:
            return ""

    async def get_liquidity(self, data):
        try:
            liquidity = await add_commas_to_float(round(float(data["full"]["attributes"]["reserve_in_usd"]), 2))
            return f"🌊 LP:<b> ${liquidity}</b>\n"
        except:
            try:
                liquidity = await add_commas_to_float(round(float(data['dexscreener']['liquidity']['usd']), 2))
                return f"🌊 LP:<b> ${liquidity}</b>\n"
            except:
                return ""

    async def get_social_links(self, data):
        try:
            msg = "\nSocial: "
            if data.get("dextool", None) is None:
                return ""
            else:
                social_links = data['dextool']['links']
                count = 0
                for key, value in social_links.items():
                    if value != "":
                        if count == 4:
                            count = 0
                            msg += "\n"
                        if msg == "\nSocial: ":
                            msg += f"{hd.link(DEXTOOL_EMOJI[key], value)} "
                        else:
                            msg += f"| {hd.link(DEXTOOL_EMOJI[key], value)} "
                        count += 1
                return msg+"\n"
        except:
            return ""

    async def check_get_message_analytic(self, data) -> str:
        count = 0
        if (
            self.BOOL[data['goplus']["is_honeypot"]]
            if data['goplus'].get("is_honeypot")
            else None
        ):
            count += 1
        if (
            self.BOOL[data['goplus']["is_mintable"]]
            if data['goplus'].get("is_mintable")
            else None
        ):
            count += 1
        if (
            self.BOOL[data['goplus']["is_proxy"]]
            if data['goplus'].get("is_proxy")
            else None
        ):
            count += 1
        if (
            self.BOOL[data['goplus']["is_blacklisted"]]
            if data['goplus'].get("is_blacklisted")
            else None
        ):
            count += 1
        if (
            self.CH_BOOL[data['goplus']["is_in_dex"]]
            if data['goplus'].get("is_in_dex")
            else None
        ):
            count += 1
        if (
            self.CH_BOOL[data['goplus']["is_open_source"]]
            if data['goplus'].get("is_open_source")
            else None
        ):
            count += 1
        if count > 0:
            return "✅"
        return "❌"

    async def check_quick_message(self, data, liquidity) -> str:
        count = 0
        try:
            if (
                data['quick']["is_Honeypot"] == False
            ):
                count += 1
        except:
            pass
        try:
            if (
                data['quick']["is_Mintable"] == False
            ):
                count += 1
        except:
            pass
        try:
            if (
                data['quick']["is_Proxy"] == False
            ):
                count += 1
        except:
            pass
        try:
            if (
                data['quick']["can_Blacklist"] == False
            ):
                count += 1
        except:
            pass
        try:
            if (
                data['quick']["contract_Verified"]
            ):
                count += 1
        except:
            pass

        if liquidity != "":
            count += 1

        if count > 0:
            return "✅"
        return "❌"

    async def get_quick_message(self, data, liquidity):
        try:
            count = await self.check_quick_message(data, liquidity)
            honeypot = self.QUICK_BOOL[data['quick']['is_Honeypot']] if data['quick'].get(
                'is_Honeypot') is not None else f"<b>N/A</b>"
            mintable = self.QUICK_BOOL[data['quick']['is_Mintable']] if data['quick'].get(
                'is_Mintable') is not None else f"<b>N/A</b>"
            proxy = self.QUICK_BOOL[data['quick']['is_Proxy']] if data['quick'].get(
                'is_Proxy') is not None else f"<b>N/A</b>"
            blacklisted = self.QUICK_BOOL[data['quick']['can_Blacklist']] if data['quick'].get(
                'can_Blacklist') is not None else f"<b>N/A</b>"

            in_dex = self.QUICK_BOOL[False] if liquidity != "" else self.QUICK_BOOL[True]
            contract_verified = self.QUICK_REVERSE[data['quick']['contract_Verified']] if data['quick'].get(
                'contract_Verified') is not None else f"{self.QUICK_REVERSE[False]}"

            return (
                f"Contract Verified: {count}\n\n\n"
                f"|-Honeypot: {honeypot}\n"
                f"|-Mintable: {mintable}\n"
                f"|-Proxy: {proxy}\n"
                f"|-Blacklisted: {blacklisted}\n"
                f"|-In Dex: {in_dex}\n"
                f"|-Contract Verified: {contract_verified}\n\n"
            )
        except Exception as e:
            print(e)
            return ""

    async def get_message_analytic(self, data, liquidity):
        try:
            if data.get('goplus') and data.get("goplus").get("is_honeypot") or data.get("goplus").get("honeypot_with_same_creator"):
                count = await self.check_get_message_analytic(data)
                test_msg = f"Contract Verified: {count}\n"
                try:
                    external_call = self.MSG_BOOL[data['goplus']['external_call']] if data['goplus'].get(
                        "external_call") else f"<b>N/A </b>"
                    test_msg += f"|-External calls: {external_call}\n"
                except:
                    pass
                try:
                    is_contract_renounced = self.QUICK_REVERSE[data['dextool']['audit']['is_contract_renounced']] if data['dextool'].get(
                        "audit") else f"<b>N/A </b>"
                    test_msg += f"|-Renounced: {is_contract_renounced}\n"
                except:
                    pass
                try:
                    unlimitedFees = self.QUICK_REVERSE[data['dextool']['audit']['unlimitedFees']] if data['dextool'].get(
                        "audit") else f"<b>N/A </b>"
                    test_msg += f"|-Unlimited Fees: {unlimitedFees}\n"
                except:
                    pass
                try:
                    hidden_owner = self.MSG_BOOL[data['goplus']['hidden_owner']] if data['goplus'].get(
                        "hidden_owner") else f"<b>N/A </b>"
                    test_msg += f"|-Hidden owner: {hidden_owner}\n"
                except:
                    pass
                try:
                    open_source = self.CHECK_BOOL[data['goplus']['is_open_source']] if data['goplus'].get(
                        'is_open_source') else f"{self.MSG_BOOL['1']}"
                    test_msg += f"|-Open source: {open_source}\n"
                except:
                    pass
                try:
                    mintable = self.MSG_BOOL[data['goplus']['is_mintable']] if data['goplus'].get(
                        'is_mintable') else f"<b>N/A </b>"
                    test_msg += f"|-Is Mintable: {mintable}\n"
                except:
                    pass
                try:
                    is_whitelisted = self.CHECK_BOOL[data['goplus']['is_whitelisted']] if data['goplus'].get(
                        "is_whitelisted") else f"<b>N/A </b>"
                    test_msg += f"|-Whitelisted: {is_whitelisted}\n"
                except:
                    pass
                try:
                    blacklisted = self.MSG_BOOL[data['goplus']['is_blacklisted']] if data['goplus'].get(
                        'is_blacklisted') else f"<b>N/A </b>"
                    test_msg += f"|-Blacklisted: {blacklisted}\n"
                except:
                    pass
                try:
                    proxy = self.MSG_BOOL[data['goplus']['is_proxy']] if data['goplus'].get(
                        'is_proxy') else f"<b>N/A </b>"
                    test_msg += f"|-Proxy contract: {proxy}\n"
                except:
                    pass
                try:
                    in_dex = self.CHECK_BOOL[data['goplus']['is_in_dex']] if data['goplus'].get(
                        'is_in_dex') else f"{self.MSG_BOOL['1']}"
                    test_msg += f"|-In Dex: {in_dex}\n"
                except:
                    pass
                try:
                    honeypot = self.MSG_BOOL[data['goplus']['is_honeypot']] if data['goplus'].get(
                        'is_honeypot') else f"<b>N/A </b>"
                    test_msg += f"|-Honeypot: {honeypot}\n"
                except:
                    pass
                test_msg += "\n"
                return test_msg
            else:
                return await self.get_quick_message(data, liquidity=liquidity)
        except:
            return ""

    async def get_base_liquidity(self, data):
        try:
            return f"🌊 LP:<b> ${await add_commas_to_float(data['dexsceener']['liquidity']['base'])}</b>\n"
        except:
            return ""

    async def get_price_change(self, data):
        try:

            return f"⏳ 24h-Vol:<b> ${data['dexscreener']['volume']['h24']}</b>\n"
        except:
            return ""

    async def get_burned(self, data):
        links = LINKS[self.CHAINS['eth']]
        if links.get('browserScanAddress') != "":
            url = links.get('browserScanAddress')
        else:
            url = None
        if data.get('goplus'):
            if data['goplus'].get('holders'):
                for holder in data['goplus']['holders']:
                    print(holder.get("address") in [
                          "0x0000000000000000000000000000000000000000"])
                    if holder.get("address", "").lower() in ["0x000000000000000000000000000000000000dead", "0x0000000000000000000000000000000000000000"]:
                        print(holder)
                        if url is not None:
                            percent = str(
                                round(float(holder['percent'])*100))+"%"
                            return hd.link(percent, url+holder['address'])
                        else:
                            return str(round(float(holder['percent'])*100))+"%"
        if data.get("value_eth"):
            return f"<b>{data['value_eth']} ETH</b>"
        return ""

    async def get_price(self, data):
        try:
            return float(data['dexscreener']['priceUsd'])
        except:
            try:
                return float(data['dextool']['pairs'][0]['price'])
            except:
                try:
                    return float(data['full']['attributes']['price_in_usd'])
                except:
                    return 0

    async def get_creator_balance(self, data):
        price = await self.get_price(data)
        holder_balance = float(data['goplus']['creator_balance'])
        hl = round(price*holder_balance)
        sl = await add_commas_to_float(hl)
        return sl

    async def collect_info(self, data: dict, bot: Bot) -> dict:
        msg_data = {}
        msg_data['ads'], msg_data['media'] = await ads_manager.get_ads(bot)
        msg_data['name'] = data['token']['tokenName'] if data.get(
            "token") else data['goplus']['token_name']
        msg_data['symbol'] = data['token']['tokenSymbol'] if data.get(
            "token") else data['goplus']['token_symbol']
        msg_data['age'] = await self.calculate_age(data)
        msg_data['top_holders'] = await self.get_top_holders(data)
        msg_data['marketcap'] = await self.get_marketcap(data)
        msg_data['taxes'] = await self.get_taxes(data)
        msg_data['creator'] = await self.get_creator(data)
        msg_data['owner'] = await self.get_owner(data)
        msg_data['liquidity'] = await self.get_liquidity(data)
        msg_data['social_links'] = await self.get_social_links(data)
        msg_data['test'] = await self.get_message_analytic(data, msg_data.get('liquidity'))
        msg_data['liquidity_base'] = await self.get_base_liquidity(data)
        msg_data['price_change'] = await self.get_price_change(data)
        msg_data['get_burned'] = await self.get_burned(data)
        msg_data['creator_balance'] = await self.get_creator_balance(data)
        return msg_data

    async def message_creater(self, data: dict, bot: Bot, address: str):
        msg_data = await self.collect_info(data, bot)
        if data.get('token'):
            TX = hd.link(
                'TX', f"https://etherscan.io/tx/{data['token']['hash']}")
        else:
            TX = ""
        Verify = hd.link(
            "Verify", f"https://etherscan.io/address/{msg_data['creator']}")
        DexT = hd.link(
            "DexT", f"https://www.dextools.io/app/en/ether/pair-explorer/{address}")
        DexS = hd.link("DexS", f"https://dexscreener.com/ethereum/{address}")
        Contract = hd.link("Contract", f"https://etherscan.io/token/{address}")
        Holders = hd.link(
            "Holders", f"https://etherscan.io/token/tokenholderchart/{address}")
        message_template = (
            f"{msg_data['media']}"
            f"{msg_data['name']} ({msg_data['symbol']}) burned <b>{msg_data['get_burned']}</b> liquidity!🔥 | {TX}\n"
            f"{msg_data['marketcap']}"
            f"{msg_data['liquidity']}"
            f"{msg_data['taxes']}"
            f"{msg_data['price_change']}"
            f"{msg_data['age']}"
            f"\n➡️ Contract Address: {hd.code(address)}\n\n"
            f"{msg_data['test']}"
            f"{msg_data['top_holders']}\n"
            f"⚖️Deployer balance: <b>${msg_data['creator_balance']}</b> | {Verify}\n"
            f"{msg_data['social_links']}\n"
            f"{DexT} | {DexS} | {Contract} | {Holders}\n"
            f"\n{msg_data['ads']}"
        )
        return message_template
