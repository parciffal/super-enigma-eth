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


async def coinmarketcap(key, address):
    API_URLS = {
        "get_coinmarket_base_info": f"https://api.coinmarketcap.com/dexer/v3/dexer/search/main-site?keyword={address}&all=false",
        "get_gecko_base_info": f"https://app.geckoterminal.com/api/p1/search?query={address}",
    }
    return API_URLS[key]


async def geckoterminal(key, chain, address):
    API_URLS = {
        "get_full_info": f"https://app.geckoterminal.com/api/p1/{chain}/pools/{address}",
        "get_shibarium_info": f"https://app.geckoterminal.com/api/p1/shibarium/pools/{address}?include=dex%2Cdex.network.explorers%2Cnetwork_link_services%2Ctoken_link_services%2Cdex_link_services%2Cpairs&base_token=0",
    }
    return API_URLS[key]


async def gopluslabs(key, address, chainID):
    API_URLS = {
        "get_address_info": f"https://api.gopluslabs.io/api/v1/token_security/{chainID}?contract_addresses={address}"
    }
    return API_URLS[key]


async def coinbrain(key, address):
    API_URLS = {
        "get_coinbrain_base_info": f"https://api.coinbrain.com/cointoaster/coins?size=100"
    }
    headers = {"Content-Type": "application/json"}
    data = {
        "searchPhrase": address,
        "chainIds": [1, 56, 137, 42161, 43114, 10, 250, 42220, 1313161554],
    }
    return API_URLS[key], headers, data
