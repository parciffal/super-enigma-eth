LINKS = {
    "1": {
        "0xSBot:telegram": "https://t.me/ZeroXsAnalyzerBot?start",
        "sniper:telegram": "https://t.me/unibotsniper_bot?start",
        "dex:link": "https://www.dextools.io/app/en/ether/pair-explorer/",
        "scan:link": "https://etherscan.io/address/",
    }
}


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
