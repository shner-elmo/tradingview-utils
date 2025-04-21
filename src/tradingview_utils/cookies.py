from __future__ import annotations

from http.cookiejar import CookieJar

import requests
from tradingview_screener import Query

# the `constants` module was removed in version 3.0.0 I believe
try:
    from tradingview_screener.query import HEADERS
except ImportError:
    from tradingview_screener.constants import HEADERS  # noqa


def authenticate(username: str, password: str) -> CookieJar:
    """
    It's always better to use an existing cookie/session rather than creating a new one (beause it
    will disconnect the other one when you try to use both simultaneously)
    """
    session = requests.Session()
    r = session.post(
        "https://www.tradingview.com/accounts/signin/",
        headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.tradingview.com"},
        data={"username": username, "password": password, "remember": "on"},
        timeout=60,
    )
    r.raise_for_status()
    if r.json().get("error"):
        raise Exception(f"Failed to authenticate: \n{r.json()}")
    return session.cookies


def assert_cookies_are_valid(cookies: dict | CookieJar):
    # try a query and make sure that TradingView recognizes the cookies
    _, df = (
        Query()
        .set_markets("america")
        .select("update_mode")
        .set_tickers("NASDAQ:AAPL")
        .get_scanner_data(cookies=cookies)
    )
    if df["update_mode"].iloc[0] != "streaming":
        raise AssertionError("Failed to authenticate")


# def load_cookies(path: str | Path) -> CookieJar: ...
#
#
# def dump_cookies(cookies: CookieJar, path: str | Path): ...
#
#
# def cookies_expired() -> bool: ...
#
#
# def cookies_expiration() -> dt.datetime: ...


# # TODO: does it belong in this module?
# def ping():
#     r = requests.get('https://data.tradingview.com/ping', headers=headers)
#     r.raise_for_status()
#     return r.json().get('ok') is True  # TODO: is this right?
