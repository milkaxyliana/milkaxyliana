import requests
import time
from datetime import datetime, timedelta
import os

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
BASE_URL = "https://api.etherscan.io/api"

def get_last_transactions(address):
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }
    r = requests.get(BASE_URL, params=params)
    data = r.json()
    return data.get("result", [])

def is_sleeping_giant(tx_list, threshold_days=180):
    if len(tx_list) < 2:
        return False
    last_outgoing_time = None
    for tx in reversed(tx_list):
        if tx["from"].lower() == tx["to"].lower():
            continue
        if tx["from"].lower() == tx["to"].lower():
            continue
        if tx["from"].lower() != tx["to"].lower() and tx["from"] != "":
            if tx["from"].lower() == tx["from"].lower() and int(tx["value"]) > 0:
                last_outgoing_time = int(tx["timeStamp"])
                break
    if last_outgoing_time:
        last_tx_date = datetime.utcfromtimestamp(last_outgoing_time)
        return (datetime.utcnow() - last_tx_date).days > threshold_days
    return False

def analyze_addresses(addresses):
    print("🔍 Analyzing potential sleeping giants...")
    for addr in addresses:
        try:
            txs = get_last_transactions(addr)
            if is_sleeping_giant(txs):
                print(f"⚠️ Woke up after sleep: {addr}")
            time.sleep(0.25)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Можно загрузить адреса из файла или API; вот примеры
    sample_addresses = [
        "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",  # Bitfinex Wallet
        "0xfe9e8709d3215310075d67e3ed32a380ccf451c8",  # Giant
        "0xdc76cd25977e0a5ae17155770273ad58648900d3",  # Dormant wallet
    ]
    analyze_addresses(sample_addresses)
