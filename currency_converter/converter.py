
# converter.py

import requests
from config import BASE_URL, SUPPORTED_CURRENCIES, API_KEY


def is_currency_supported(currency_code):
    return any(code == currency_code for code, _ in SUPPORTED_CURRENCIES)

