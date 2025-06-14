import requests
import json
import os
from datetime import datetime
from config import BASE_URL, API_KEY

HISTORY_FILE = "currency_history.json"
BASE_CURRENCY = "USD"

def load_currency_data():
    """
    Mengambil semua data nilai tukar dari BASE_CURRENCY ke semua mata uang yang disediakan oleh API.
    Menyimpan hasilnya ke histori lokal.
    """
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{BASE_CURRENCY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["result"] == "success":
            all_data = data["conversion_rates"]
            save_currency_to_history(all_data)
            return all_data
        else:
            print("API response error:", data.get("error-type", "Unknown error"))
            return {}
    except Exception as e:
        print(f"Error loading real-time currency data: {e}")
        return {}

def save_currency_to_history(new_data):
    """
    Simpan data kurs ke file JSON dengan timestamp saat ini.
    """
    timestamp = datetime.now().isoformat(timespec='minutes')

    history = {}
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)

    history[timestamp] = new_data

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=2)

def load_currency_history():
    file_path = os.path.join(os.path.dirname(__file__), "currency_history.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}
