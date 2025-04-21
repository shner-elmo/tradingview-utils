import os

from tradingview_utils import authenticate, assert_cookies_are_valid

USERNAME = os.environ["TV_USERNAME"]
PASSWORD = os.environ["TV_PASSWORD"]


def test_cookies():
    cookies = authenticate(username=USERNAME, password=PASSWORD)
    assert_cookies_are_valid(cookies=cookies)
