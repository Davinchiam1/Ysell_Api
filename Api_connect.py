import os.path
import time

import requests
import json
import pandas as pd
from datetime import datetime
from tqdm import tqdm


class Ysell_regu:

    def __init__(self):
        self.url = 'https://1359.eu11.ysell.pro/api/v1/'
        with open('token.txt', "r", encoding='utf8') as f:
            token = f.readline()
            print(token)
        self.headers = {
            'accept': '*/*',
            'Authorization': token
        }
        self.dates = []
        self.temp_frame = pd.DataFrame()

    def orders_req(self,page=1):
        sort='?sort=-id&'
        pages='page='+str(page)
        url=self.url+'order'+sort+pages
        response = requests.post(url=url, headers=self.headers)
        print(response.status_code)
        json_data = response.json()
        df = pd.json_normalize(json_data)
