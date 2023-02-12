import requests
import ast

headers = {
    "accept": "/",
    "accept-encoding": "gzip, deflate, br",
    "user-agent" :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
}

session = requests.Session()

def get_cookies():
    request = session.get("https://www.nseindia.com", headers=headers, timeout=4)
    return request.cookies

def get_cash_data():
    response = session.get("https://www.nseindia.com/api/fiidiiTradeReact", headers=headers, cookies=get_cookies(), timeout=4)
    data = response.content
    data = ast.literal_eval(data.decode("utf-8"))
    return data

if __name__ == "__main__":
    print(get_cash_data())
