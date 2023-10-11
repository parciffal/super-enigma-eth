LINKS = {
    "1": {
        "geckoterminal": "https://www.geckoterminal.com/eth/pools/",
        "dextools": "https://www.dextools.io/app/en/ether/pair-explorer/",
        "browserScanAddress": "https://etherscan.io/address/",
    },
    "56": {
        "geckoterminal": "https://www.geckoterminal.com/bsc/pools/",
        "dextools": "https://www.dextools.io/app/en/bnb/pair-explorer/",
        "browserScanAddress": "https://bscscan.com/address/",
    },
    "42161": {
        "geckoterminal": "https://www.geckoterminal.com/arbitrum/pools/",
        "dextools": "https://www.dextools.io/app/en/arbitrum/pair-explorer/",
        "browserScanAddress": "https://arbiscan.io/address/",
    },
    "137": {
        "geckoterminal": "https://www.geckoterminal.com/polygon_pos/pools/",
        "dextools": "https://www.dextools.io/app/en/polygon/pair-explorer/",
        "browserScanAddress": "https://polygonscan.com/address/",
    },
    "324": {
        "geckoterminal": "https://www.geckoterminal.com/zksync/pools/",
        "dextools": "https://www.dextools.io/app/en/zksync/pair-explorer/",
        "browserScanAddress": "https://explorer.zksync.io/address/",
    },
    "59144": {
        "geckoterminal": "https://www.geckoterminal.com/linea/pools/",
        "dextools": "https://www.dextools.io/app/en/linea/pair-explorer/",
        "browserScanAddress": "https://explorer.linea.build/address/",
    },
    "59140": {
        "geckoterminal": "",
        "dextools": "",
        "browserScanAddress": "https://explorer.goerli.zkevm.consensys.net/address/",
    },
    "8453": {
        "geckoterminal": "https://www.geckoterminal.com/base/pools/",
        "dextools": "https://www.dextools.io/app/en/base/pair-explorer/",
        "browserScanAddress": "https://basescan.org/address/",
    },
    "5000": {
        "geckoterminal": "",
        "dextools": "",
        "browserScanAddress": "https://explorer.mantle.xyz/address/",
    },
    "534351": {
        "geckoterminal": "",
        "dextools": "",
        "browserScanAddress": "https://sepolia-blockscout.scroll.io/address/",
    },
    "10": {
        "geckoterminal": "https://www.geckoterminal.com/optimism/pools/",
        "dextools": "https://www.dextools.io/app/en/optimism/pair-explorer/",
        "browserScanAddress": "https://optimistic.etherscan.io/address/",
    },
    "43114": {
        "geckoterminal": "https://www.geckoterminal.com/avax/pools/",
        "dextools": "https://www.dextools.io/app/en/avalanche/pair-explorer/",
        "browserScanAddress": "https://snowtrace.io/address/",
    },
    "250": {
        "geckoterminal": "https://www.geckoterminal.com/ftm/pools/",
        "dextools": "",
        "browserScanAddress": "https://ftmscan.com/address/",
    },
    "25": {
        "geckoterminal": "https://www.geckoterminal.com/cro/pools/",
        "dextools": "https://www.dextools.io/app/en/cronos/pair-explorer/",
        "browserScanAddress": "https://cronoscan.com/address/",
    },
    "66": {
        "geckoterminal": "",
        "dextools": "https://www.dextools.io/app/en/okc/pair-explorer/",
        "browserScanAddress": "https://www.oklink.com/okexchain/address/",
    },
    "128": {
        "geckoterminal": "",
        "dextools": "https://www.dextools.io/app/en/heco/pair-explorer/",
        "browserScanAddress": "https://hecoinfo.com/address/",
    },
    "100": {
        "geckoterminal": "https://www.geckoterminal.com/xdai/pools/",
        "dextools": "https://www.dextools.io/app/en/gnosis/pair-explorer/",
        "browserScanAddress": "https://gnosisscan.io/address/",
    },
    "10001": {
        "geckoterminal": "https://www.geckoterminal.com/ethw/pools/",
        "dextools": "https://www.dextools.io/app/en/ethw/pair-explorer/",
        "browserScanAddress": "https://www.oklink.com/en/ethw/address/",
    },
    "tron": {
        "geckoterminal": "",
        "dextools": "",
        "browserScanAddress": "https://tronscan.org/#/token20/",
    },
    "321": {
        "geckoterminal": "https://www.geckoterminal.com/kcc/pools/",
        "dextools": "https://www.dextools.io/app/en/kucoin/pair-explorer/",
        "browserScanAddress": "https://scan.kcc.io/address/",
    },
    "201022": {
        "geckoterminal": "",
        "dextools": "",
        "browserScanAddress": "https://fonscan.io/address/",
    },
    "shibarium": {
        "geckoterminal": "https://www.geckoterminal.com/shibarium/pools/",
        "dextools": "https://www.dextools.io/app/en/shib/pairs-explorer/",
        "browserScanAddress": "https://www.shibariumscan.io/address/",
    },
    "109": {
        "geckoterminal": "https://www.geckoterminal.com/shibarium/pools/",
        "dextools": "https://www.dextools.io/app/en/shib/pairs-explorer/",
        "browserScanAddress": "https://www.shibariumscan.io/address/",
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
