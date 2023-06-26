import os.path
import time
from urllib.parse import urlencode
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

    def __init__(self, url='https://1359.eu11.ysell.pro/api/v1/', token='token.txt'):
        self.url = url
        with open(token, "r", encoding='utf8') as f:
            token = f.readline()
            print(token)
        self.headers = {
            'accept': '*/*',
            'Authorization': token
        }
        self.pages = None
        self.temp_frame = None

    def orders_by_page(self, page=1):
        self.temp_frame = pd.DataFrame()
        sort = '?sort=-purchase_date&'
        pages = 'page=' + str(page)
        url = self.url + 'order' + sort + pages
        response = requests.get(url=url, headers=self.headers, timeout=30)
        json_data = response.json()
        df = pd.json_normalize(json_data)
        if response.status_code != 200:
            print(response.json())
        # применение функции к датафрейму
        df_temp = df['items'].apply(json_to_columns)
        df_temp['items.p_id'] = df_temp['items.p_id'].fillna(0)
        temp_frame = pd.concat([df, df_temp], axis=1)
        temp_frame = temp_frame.drop(['items', 'items.product'], axis=1)
        temp_frame.set_index('id', inplace=True)
        return temp_frame

    def products_by_page(self, page=1):
        self.temp_frame = pd.DataFrame()
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
        error_pages = []  # Список для хранения страниц с ошибками
        total_pages = end - start + 1
        self.temp_frame = pd.DataFrame()

        with tqdm(total=total_pages) as pbar:
            for page in range(start, end + 1):
                try:
                    final_frame = pd.concat([final_frame, self.orders_by_page(page=page)])
                except Exception as e:
                    # Обработка ошибки
                    print(f"Ошибка на странице {page}: {e}")
                    error_pages.append(page)

                pbar.update(1)  # Увеличение прогресса на 1

        # Дополнительный опрос страниц с ошибками
        if len(error_pages) > 0:
            time.sleep(30)
            for page in error_pages:
                try:
                    final_frame = pd.concat([final_frame, self.orders_by_page(page=page)])
                except Exception as e:
                    # Обработка ошибки при повторном опросе страницы
                    print(f"Ошибка при повторном опросе страницы {page}: {e}")

        # final_frame['id']=final_frame.index
        final_frame['shipments'] = final_frame['shipments'].astype(str)
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
# test_data = test.orders_req(start=8300, end=8700)
# test_data.to_excel('test_data.xlsx')
# test.product_req()

class Keepa_req:

    def __init__(self):
        self.url = 'https://api.keepa.com/'
        with open('token_keepa.txt', "r", encoding='utf8') as f:
            token = f.readline()
            print(token)
        self.access_key = token
        self.pages = None
        self.temp_frame = None

    def req(self):
        url = f"{self.url}token?key={self.access_key}"
        response = requests.get(url)
        print(response.text)

    def category_req(self, category=0):
        url = f"{self.url}category?key={self.access_key}&domain={1}&category={category}&parents={0}"
        response = requests.get(url)
        json_data = response.json()['categories']
        df = pd.DataFrame.from_dict(json_data, orient='index')
        df.to_excel('test1.xlsx')

    def category_search(self, search=""):
        url = f"{self.url}search?key={self.access_key}&domain={1}&type=category&term={search}"
        response = requests.get(url)
        json_data = response.json()['categories']
        df = pd.DataFrame.from_dict(json_data, orient='index')
        df.to_excel('test1.xlsx')

    def product_req(self, asin):
        if type(asin) is list:
            asin = ','.join(asin)
        data = {
            'asin': asin,
            'stats': 180,
        }
        encoded_data = urlencode(data)
        url = f"{self.url}product?key={self.access_key}&domain={1}&{encoded_data}"
        response = requests.get(url)
        json_data = response.json()['product']
        df = pd.DataFrame.from_dict(json_data, orient='index')
        df.to_excel('test2.xlsx')

    def product_search(self, search={}):
        encoded_data = urlencode(search)
        url = f"{self.url}search?key={self.access_key}&domain={1}&type=product&term={search}&stats=180"
        response = requests.get(url)
        json_data = response.json()['categories']
        df = pd.DataFrame.from_dict(json_data, orient='index')
        df.to_excel('test1.xlsx')

    def product_finder(self, search={}):
        encoded_data = urlencode(search)
        url = f"{self.url}query?key={self.access_key}&domain={1}&selection={search}"
        response = requests.get(url)
        json_data = response.json()['categories']
        df = pd.DataFrame.from_dict(json_data, orient='index')
        df.to_excel('test1.xlsx')

    def bsr_req(self, category: int = 0, range: int = 30):
        url = f"{self.url}bestsellers?key={self.access_key}&domain={1}&category={category}&range={range}"
        response = requests.get(url)
        json_data = response.json()['categories']
        df = pd.DataFrame.from_dict(json_data, orient='index')
        df.to_excel('test1.xlsx')
# ['categories']
# test2=Keepa_req()
# test2.req()
# # test2.category_req()
# test2.category_search('health')
