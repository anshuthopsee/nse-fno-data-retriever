import requests

header = {
    "user-agent" :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "accept-encoding": "gzip, deflate, br",
    "accept": """text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9""",
}

session = requests.Session()
session.headers.update(header)

def get_fii_dii_cash_data():
    response = session.get("https://www.nseindia.com/api/fiidiiTradeReact", timeout=4)
    return response.content

data = get_fii_dii_cash_data()
