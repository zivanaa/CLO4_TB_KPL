# converter.py

import requests
from config import BASE_URL, SUPPORTED_CURRENCIES, API_KEY


def is_currency_supported(currency_code):
    return any(code == currency_code for code, _ in SUPPORTED_CURRENCIES)

def convert_currency(amount, from_currency, to_currency):
    assert amount > 0, "Amount must be greater than 0"
    assert is_currency_supported(from_currency), f"{from_currency} not supported"
    assert is_currency_supported(to_currency), f"{to_currency} not supported"

    url = f"{BASE_URL}/{from_currency}/{to_currency}"
    response = requests.get(url)
    data = response.json()

    if data["result"] == "success":
        return amount * data["conversion_rate"]
    else:
        raise Exception("Conversion failed from API")
