async def get_api_url(key, address, platform_id=14):
    API_URLS = {
        "get_coin_data": f"https://api.coinmarketcap.com/dexer/v3/dexer/pair-list?base-address={address}&start=1&limit=10&platform-id={platform_id}",
        "get_last_buy": f"https://api.coinmarketcap.com/kline/v3/k-line/transactions/14/{address}?reverse-order=false",
        "get_btc_rug_check": f"https://api.moonarch.app/1.0/tokens/BSC/details/{address}",
        "get_eth_rug_check": f"https://api.moonarch.app/1.0/tokens/BSC/details/{address}",
    }
    return API_URLS[key]


async def honey_pot_url(key, address, chainID=56):
    API_URLS = {
        "get_token_info": f"https://api.honeypot.is/v1/TokenInfo?address={address}&chainID={chainID}",
        "get_is_honeypot": f"https://api.honeypot.is/v2/IsHoneypot?address={address}&chainID={chainID}",
        "get_contract_verification": f"https://api.honeypot.is/v1/GetContractVerification?address={address}&chainID={chainID}",
        "get_pairs": f"https://api.honeypot.is/v1/GetPairs?address={address}",
    }
    return API_URLS[key]
