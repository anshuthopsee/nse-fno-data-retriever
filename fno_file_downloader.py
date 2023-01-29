import os
import io
from datetime import date, time
import requests
import zipfile36

def unzipper(bytes):
    fp = io.BytesIO(bytes)
    with zipfile36.ZipFile(file=fp) as zf:
        fname = zf.namelist()[0]
        with zf.open(fname) as fp_bh:
            return fp_bh.read().decode('utf-8')
    

class NSEFiles:
    def __init__(self):
        self.base_url = "https://archives.nseindia.com/content/"
        self.timeout = 4
        self.session = requests.Session()
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "accept-encoding": "gzip, deflate, br",
            "accept":
            """text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9""",
        }
        self.session.headers.update(self.headers)
        self.routes = {
            "bhavcopy_fo": "historical/DERIVATIVES/{yyyy}/{MMM}/fo{dd}{MMM}{yyyy}bhav.csv.zip",
            "fii_stats": "fo/fii_stats_{dd}-{MMM}-{yyyy}.xls",
            "fao_participant_vol" : "nsccl/fao_participant_vol_{dd}{mm}{yyyy}.csv"
        }

    def get(self, route, **params):
        url = self.base_url + self.routes[route].format(**params)
        print(url)
        self.response = self.session.get(url, timeout=self.timeout)
        return self.response

    def bhavcopy_fo(self, dt):
        try:
            dd = dt.strftime('%d')
            MMM = dt.strftime('%b').upper()
            yyyy = dt.year
            response = self.get("bhavcopy_fo", yyyy=yyyy, MMM=MMM, dd=dd)
            response = unzipper(response.content)
            return response
        except:
            print("Data not available right now. Try again later.")

    def bhavcopy_fo_save(self, dt, dest):
        try:
            fmt = "bhavcopy_fo_%d%b%Y.csv"
            fname = os.path.join(dest, dt.strftime(fmt))
            if os.path.isfile(fname):
                return fname
            file = self.bhavcopy_fo(dt)
            with open(fname, 'w') as f:
                f.write(file)
            return fname
        except:
            return None

    def fii_stats(self, dt):
        try:
            dd = dt.strftime('%d')
            MMM = dt.strftime('%b')
            yyyy = dt.year
            response = self.get("fii_stats", yyyy=yyyy, MMM=MMM, dd=dd)
            return response.content
        except:
            print("Data not available right now. Try again later.")

    def fii_stats_save(self, dt, dest):
        try:
            fmt = "fii_stats_%d%b%Y.xls"
            fname = os.path.join(dest, dt.strftime(fmt))
            if os.path.isfile(fname):
                return fname
            file = self.fii_stats(dt)
            with open(fname, 'wb') as f:
                f.write(file)
            return fname
        except:
            return None

    def fao_participant_vol(self, dt):
        try:
            dd = dt.strftime('%d')
            mm = dt.strftime('%m')
            yyyy = dt.year
            response = self.get("fao_participant_vol", yyyy=yyyy, mm=mm, dd=dd)
            return response.content
        except:
            print("Data not available right now. Try again later.")

    def fao_participant_vol_save(self, dt, dest):
        try:
            fmt = "fao_participant_vol_%d%b%Y.csv"
            fname = os.path.join(dest, dt.strftime(fmt))
            if os.path.isfile(fname):
                return fname
            file = self.fao_participant_vol(dt)
            with open(fname, 'wb') as f:
                f.write(file)
            return fname
        except:
            return None

filepath = "FILE/PATH"

nse = NSEFiles()
nse.bhavcopy_fo_save(date(2023, 1, 27), filepath)
nse.fii_stats_save(date(2023, 1, 27), filepath)
nse.fao_participant_vol_save(date(2023, 1, 27), filepath)
