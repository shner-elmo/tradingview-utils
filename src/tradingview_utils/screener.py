from __future__ import annotations

import json
from typing import Literal

import requests
from tradingview_screener import Query

# the `constants` module was removed in version 3.0.0 I believe
try:
    from tradingview_screener.query import HEADERS
except ImportError:
    from tradingview_screener.constants import HEADERS  # noqa


MAX_LIMIT = 1_000_000
# not really the max, but big enough for most cases


def get_data_update_mode(
    cookies, market: str = "america"
) -> dict[str, str]:  # dict[exchange, update_mode]
    """
    Get the update-mode for each exchange
    :param cookies:
    :return:
    """
    _, df = (
        Query()
        .select("exchange", "update_mode")
        .limit(MAX_LIMIT)
        .set_markets(market)
        .get_scanner_data(cookies=cookies)
    )
    return df.groupby("exchange")["update_mode"].value_counts()


def list_indices():
    """
    This is a list of all the indices in the world.
    These can be passed to [`Query.set_index()`](query.html#Query.set_index)
    """
    # for all ETFs: `.order_by('aum', ascending=False, nulls_first=False)`
    _, df = (
        Query()
        .select("name", "description")
        .order_by("index_priority")
        .set_markets("cfd")
        .set_property("preset", "indices_all")
        .limit(MAX_LIMIT)
        .get_scanner_data()
    )
    return list(df.iter_tuples())


def list_screeners(
    cookies,
    screener_type: Literal["stock", "forex", "crypto"],
):
    r = requests.get(
        f"https://www.tradingview.com/screener/settings/?screener_type={screener_type}",
        cookies=cookies,  # pyright: ignore [reportArgumentType]
        headers=HEADERS,
    )
    r.raise_for_status()

    # there are certain values that are stored in a string (serialized JSON), so we un-serialize it.
    rv = r.json()
    for key, lst in rv.items():
        for dct in lst:
            content = dct.get("content")
            if content:
                dct["content"] = json.loads(content)
    return rv


# see issue: https://github.com/shner-elmo/TradingView-Screener/issues/12
def format_technical_rating(rating: float) -> str:
    if rating >= 0.5:
        return "Strong Buy"
    elif rating >= 0.1:
        return "Buy"
    elif rating >= -0.1:
        return "Neutral"
    elif rating >= -0.5:
        return "Sell"
    # elif x >= -0.1:
    else:
        return "Strong Sell"


# def screener_to_query() -> Query:
#     ...
#
#
# def get_earnings(
#     start_date: dt.datetime, end_date: dt.datetime, index: Optional[Iterable[str]]
# ) -> tuple[int, pd.DataFrame]:
#     # {'query': {'types': []}, 'tickers': [], 'groups': [{'type': 'index', 'values': ['DJ:DJU']}]}
#     #
#     # {'left': 'earnings_release_next_trading_date_fq', 'operation': 'in_day_range', 'right': [0, 0]}
#     # [{'left': 'earnings_release_next_trading_date_fq', 'operation': 'in_week_range', 'right': [1, 1]}]
#     # [{'left': 'earnings_release_next_trading_date_fq', 'operation': 'in_month_range', 'right': [0, 0]}]
#     #
#     _, df = (Query()
#      .select('earnings_per_share_forecast_fq', 'earnings_per_share_fq', 'earnings_per_share_basic_ttm')
#      .where(col('earnings_release_next_trading_date_fq').in_day_range([0, 0]))
#      .order_by('market_cap_basic', ascending=False)
#      .limit(MAX_LIMIT)
#      .get_scanner_data()
#     )
#     return df
