# config.py

import requests

API_KEY = "99af1e52e8b504f480478eda"  
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair"
CODES_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/codes"

def get_supported_currencies():
    try:
        response = requests.get(CODES_URL)
        data = response.json()
        return data["supported_codes"] if data["result"] == "success" else []
    except Exception as e:
        print(f"Failed to fetch supported currencies: {e}")
        return []

SUPPORTED_CURRENCIES = get_supported_currencies()

