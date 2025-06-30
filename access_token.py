import requests
import time
import webbrowser
import threading
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

PARENT = {
    "api_key": "b8280d36fc1726ef594ff258b454e265",
    "api_secret": "e3f3b525b46fd5e3dee47df4e58f4923",
    "port": 8000
}

CHILD_ACCOUNTS = [
    {
        "api_key": "cebef84f4a0a11ded64f5222ba857f90",
        "api_secret": "a419d2e47093d1ec60368fb30acb0ea6",
        "port": 8001
    }
]

class TokenHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        self.server.request_token = query.get("request_token", [None])[0]#type:ignore
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Token received. You can close this tab.")
        threading.Thread(target=self.server.shutdown).start()

def get_bearer_token(api_key, api_secret, port):
    server = HTTPServer(("localhost", port), TokenHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

    login_url = f"https://api.gwcindia.in/v1/login?api_key={api_key}"
    resp = requests.get(login_url, allow_redirects=False)
    redirect_url = resp.headers["Location"].replace("redirect_uri=http://localhost:8000", f"http://localhost:{port}")
    webbrowser.open(redirect_url)

    while not hasattr(server, "request_token"):
        time.sleep(0.5)

    token = server.request_token#type:ignore
    signature = hashlib.sha256((api_key + token + api_secret).encode()).hexdigest()

    res = requests.post("https://api.gwcindia.in/v1/login-response", headers={
        "Content-Type": "application/json"
    }, json={
        "api_key": api_key,
        "request_token": token,
        "signature": signature
    })

    return res.json()["data"]["access_token"]

def get_headers(api_key, token):
    return {
        "x-api-key": api_key,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def fetch_trades(api_key, token):
    resp = requests.get("https://api.gwcindia.in/v1/tradebook", headers=get_headers(api_key, token))
    return resp.json().get("data", [])

def place_order(trade, api_key, token):
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
    resp = requests.post("https://api.gwcindia.in/v1/placeorder", headers=get_headers(api_key, token), json=payload)
    return resp.json()

def main():
    parent_token = get_bearer_token(PARENT["api_key"], PARENT["api_secret"], PARENT["port"])
    children = [
        {
            "api_key": acc["api_key"],
            "token": get_bearer_token(acc["api_key"], acc["api_secret"], acc["port"])
        }
        for acc in CHILD_ACCOUNTS
    ]

    initial_trades = fetch_trades(PARENT["api_key"], parent_token)
    seen = {trade["nstordno"] for trade in initial_trades}
    print(f"✅ Ignoring {len(seen)} existing trades")

    while True:
        try:
            trades = fetch_trades(PARENT["api_key"], parent_token)
            for trade in trades:
                trade_id = trade["nstordno"]
                if trade_id not in seen:
                    seen.add(trade_id)
                    for child in children:
                        result = place_order(trade, child["api_key"], child["token"])
                        print(f"{trade['tsym']} copied → {result.get('status')}")
            time.sleep(10)
        except KeyboardInterrupt:
            print("Stopped by user")
            break
        except Exception as e:
            print("Error:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
