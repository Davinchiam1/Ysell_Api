import os.path
import time

import requests
import json
import pandas as pd
from datetime import datetime
from tqdm import tqdm


def json_to_columns(row):
    # преобразование JSON в словарь
    data = row[0]
    # создание новых столбцов для каждого ключа в JSON
    temp_row = {}
    for key in data:
        temp_row['items.' + key] = data[key]
    return pd.Series(temp_row)


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
        self.pages = None
        self.temp_frame = pd.DataFrame()

    def orders_by_page(self, page=1):
        sort = '?sort=-id&'
        pages = 'page=' + str(page)
        url = self.url + 'order' + sort + pages
        response = requests.get(url=url, headers=self.headers)
        print(response.status_code)
        json_data = response.json()
        df = pd.json_normalize(json_data)

        # применение функции к датафрейму
        df_temp = df['items'].apply(json_to_columns)
        temp_frame = pd.concat([df, df_temp], axis=1)
        temp_frame = temp_frame.drop(['items','items.product'], axis=1)
        temp_frame.set_index('id', inplace=True)
        return temp_frame

    def products_by_page(self, page=1):
        pages = '?page=' + str(page)
        url = self.url + 'product' + pages + '&per-page=50'
        response = requests.get(url=url, headers=self.headers)
        print(response.status_code)
        json_data = response.json()
        df = pd.json_normalize(json_data)
        self.pages = response.headers.get('X-Pagination-Page-Count')

        # применение функции к датафрейму
        temp_frame = df
        temp_frame.set_index('id', inplace=True)
        return temp_frame

    def orders_req(self, start=1, end=10):
        final_frame = pd.DataFrame()
        for page in range(start, end+1):
            final_frame = pd.concat([final_frame, self.orders_by_page(page=page)])
        # final_frame['id']=final_frame.index
        final_frame['shipments']=final_frame['shipments'].astype(str)
        final_frame['services'] = final_frame['services'].astype(str)
        return final_frame

    def product_req(self, load_all=True, start=1, end=3):
        final_frame = pd.DataFrame()
        page = start
        while page <= end:
            final_frame = pd.concat([final_frame, self.products_by_page(page=page)])
            if load_all and page == start:
                end = int(self.pages)
            page += 1
        return final_frame


# test = Ysell_regu()
# test.orders_req()
# test.product_req()
