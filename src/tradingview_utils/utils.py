from __future__ import annotations

import requests

# the `constants` module was removed in version 3.0.0 I believe
try:
    from tradingview_screener.query import HEADERS
except ImportError:
    from tradingview_screener.constants import HEADERS  # noqa


def get_all_symbols(market: str = "america") -> list[str]:
    """
    Get all the symbols of a given market.

    Examples:

    >>> get_all_symbols()
    ['OTC:BMVVF',
     'OTC:BRQL',
     'NYSE:EFC/PA',
     'NASDAQ:NVCR',
     'NASDAQ:OMIC',
     ...

    >>> len(get_all_symbols())
    18060

    The default market is `america`, but you can change it with any market from
    `tradingview_screener.constants.MARKETS`:
    >>> get_all_symbols(market='switzerland')
    ['BX:UN01',
     'BX:XFNT',
     'BX:ZPDE',
     'BX:0QF',
     'BX:BSN',
     ...

    For instance, to get all the crypto tickers:
    >>> get_all_symbols(market='crypto')
    ['KRAKEN:KNCEUR',
     'TRADERJOE:WETHEWAVAX_FE15C2',
     'UNISWAP:DBIWETH_DEDF7B',
     'KUCOIN:DIABTC',
     'QUICKSWAP:WIXSWMATIC_F87B83.USD',
     ...

    >>> len(get_all_symbols(market='futures'))
    75205

    >>> len(get_all_symbols(market='bonds'))
    1090

    >>> len(get_all_symbols(market='germany'))
    13251

    >>> len(get_all_symbols(market='israel'))
    1034

    :param market: any market from `tradingview_screener.constants.MARKETS`, default 'america'
    :return: list of tickers
    """
    r = requests.get(f"https://scanner.tradingview.com/{market}/scan", timeout=60)
    r.raise_for_status()
    data = r.json()[
        "data"
    ]  # [{'s': 'NYSE:HKD', 'd': []}, {'s': 'NASDAQ:ALTY', 'd': []}...]

    return [dct["s"] for dct in data]


# def list_watchlists():
#     ...
#
# def get_watchlist():
#     # to get a watchlist ID:
#     # response = requests.get('https://www.tradingview.com/api/v1/symbols_list/all/', cookies=cookies, headers=headers)
#     ...
#
#
# def search_ticker(s: str) -> list[str]:
#     ...


# TODO: add: markets, indices, and presets to the 'Data' section in the docs.
