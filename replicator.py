import requests
import time
from datetime import datetime

PARENT_API_KEY = "b8280d36fc1726ef594ff258b454e265"
PARENT_BEARER = "fbc4e213a2849bf3084ae14087d466e9"

CHILD_ACCOUNTS = [
    {
        "api_key": "cebef84f4a0a11ded64f5222ba857f90",
        "access_token": "d2661ad747b753fa0a9e600b320413e8"
    }
]

def get_headers(api_key, token):
    return {
        "x-api-key": api_key,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def fetch_parent_trades():
    url = "https://api.gwcindia.in/v1/tradebook"
    resp = requests.get(url, headers=get_headers(PARENT_API_KEY, PARENT_BEARER))
    return resp.json().get("data", [])

def place_order(trade, child):
    payload = {
        "tsym": trade["tsym"],
        "exchange": trade["exchange"],
        "trantype": trade["trantype"],
        "validity": "DAY",
        "pricetype": trade["pricetype"],
        "qty": trade["qty"],
        "discqty": "0",
        "price": trade["price"],
        "trgprc": "0",
        "product": trade["product"],
        "amo": "NO"
    }
    url = "https://api.gwcindia.in/v1/placeorder"
    r = requests.post(url, headers=get_headers(child["api_key"], child["access_token"]), json=payload)
    return r.json()

def main():
    seen = set()
    start_time = datetime.now()

    while True:
        trades = fetch_parent_trades()
        for trade in trades:
            exchtime = datetime.strptime(trade["exchtime"], "%d-%m-%Y %H:%M:%S")
            trade_id = trade["nstordno"]
            if exchtime > start_time and trade_id not in seen:
                seen.add(trade_id)
                for child in CHILD_ACCOUNTS:
                    res = place_order(trade, child)
                    print(f"{trade['tsym']} -> {res.get('status')}")

        time.sleep(10)

if __name__ == "__main__":
    main()
