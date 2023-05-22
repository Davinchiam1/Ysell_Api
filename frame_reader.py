import os
import re
import pandas as pd


class Reports_loading:
    def __init__(self):
        self.inventory_frame = None
        self.reserved_frame = None
        self.orders_frame = None
        self.orders_list=[]
        self.inventory_list = []
        self.reserved_list = []
        self.result_frame = None
        self.orders_stat=[]
        self.orders_stat_frame=None

    def _create_lists(self, directory):
        """Finding of all .csv files in directory"""
        if directory is not None:
            for f in os.scandir(directory):
                if f.is_file() and f.path.split('.')[-1].lower() == 'csv':
                    if 'Inventory' in str(f.path):
                        self.inventory_list.append(f.path)
                    if 'Reserved' in str(f.path):
                        self.reserved_list.append(f.path)
                elif f.is_file() and f.path.split('.')[-1].lower() == 'txt':
                    if 'Order' in str(f.path):
                        self.orders_list.append(f.path)
                    if 'Order1' in str(f.path):
                        self.orders_stat.append(f.path)
        else:
            for f in os.scandir():
                if f.is_file() and f.path.split('.')[-1].lower() == 'csv':
                    if 'Inventory' in str(f.path):
                        self.inventory_list.append(f.path)
                    if 'Reserved' in str(f.path):
                        self.reserved_list.append(f.path)
                elif f.is_file() and f.path.split('.')[-1].lower() == 'txt':
                    if 'Order1М' in str(f.path):
                        self.orders_list.append(f.path)
                    if 'Order1' in str(f.path):
                        self.orders_stat.append(f.path)

    def _read_data(self):
        for file in self.inventory_list:
            temp_frame = pd.read_csv(file, delimiter=',',encoding='cp1252')
            self.inventory_frame = pd.concat([self.inventory_frame, temp_frame], ignore_index=True, axis=0)
        for file in self.reserved_list:
            temp_frame = pd.read_csv(file, delimiter=',',encoding='cp1252')
            self.reserved_frame = pd.concat([self.reserved_frame, temp_frame], ignore_index=True, axis=0)
        for file in self.orders_list:
            temp_frame = pd.read_csv(file, delimiter='\t', encoding='cp1252',low_memory=False)
            temp_frame=temp_frame[['sku','asin','item-status','quantity','currency','item-price']]
            self.orders_frame=pd.concat([self.orders_frame, temp_frame], ignore_index=True, axis=0)
        for file in self.orders_stat:
            temp_frame = pd.read_csv(file, delimiter='\t', encoding='cp1252', low_memory=False)
            temp_frame = temp_frame[['sku', 'asin', 'item-status', 'quantity', 'currency', 'item-price']]
            self.orders_stat_frame = pd.concat([self.orders_stat_frame, temp_frame], ignore_index=True, axis=0)

    def _concentrate_data(self, status='Shipped'):
        """Concentrating data into one dataframe"""
        self.result_frame = pd.merge(self.inventory_frame, self.reserved_frame, on='fnsku', how='outer')
        self.orders_frame = self.orders_frame[self.orders_frame['item-status'] == 'Shipped']
        self.orders_frame = self.orders_frame.groupby('asin').agg({'quantity': 'sum', 'item-price': 'mean'})
        self.orders_frame['avg_per_day']=self.orders_frame['quantity']/30
        self.orders_frame['asin']=self.orders_frame.index
        self.orders_stat_frame = self.orders_stat_frame[self.orders_frame['item-status'] == 'Shipped']
        self.orders_stat_frame = self.orders_stat_frame.groupby('asin').agg({'quantity': 'sum', 'item-price': 'mean'})
        self.orders_stat_frame['quantity']=self.orders_stat_frame['quantity']/3
        self.orders_stat_frame['avg_per_day_3M']=self.orders_stat_frame['quantity']/30
        self.orders_stat_frame['asin']=self.orders_stat_frame.index
        self.orders_frame = pd.merge(self.orders_frame,self.orders_stat_frame,on='asin',how='outer')
        self.result_frame=pd.merge(self.result_frame,self.orders_frame,left_on='asin_x',right_on='asin',how='outer')

    def get_data(self, directory=None):
        self._create_lists(directory=directory)
        self._read_data()
        self._concentrate_data()
        return self.result_frame, self.orders_frame


# test=Reports_loading()
# frame,frame2=test.get_data(directory='Z:\\Аналитика\\Amazon\\Update_api\\Amz Stock and Amz Orders')
# frame.to_excel('test_file.xlsx', sheet_name='list1')
# frame2.to_excel('test_file2.xlsx', sheet_name='list1')