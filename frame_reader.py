import os
import re
import pandas as pd


class Reports_loading:
    def __init__(self):
        self.inventory_frame = None
        self.reserved_frame = None
        self.inventory_list = []
        self.reserved_list = []
        self.result_frame = None

    def _create_lists(self, directory):
        """Finding of all .csv files in directory"""
        if directory is not None:
            for f in os.scandir(directory):
                if f.is_file() and f.path.split('.')[-1].lower() == 'csv':
                    if 'Inventory' in str(f.path):
                        self.inventory_list.append(f.path)
                    if 'Reserved' in str(f.path):
                        self.reserved_list.append(f.path)
        else:
            for f in os.scandir():
                if f.is_file() and f.path.split('.')[-1].lower() == 'csv':
                    if 'Inventory' in str(f.path):
                        self.inventory_list.append(f.path)
                    if 'Reserved' in str(f.path):
                        self.reserved_list.append(f.path)

    def _read_data(self):
        for file in self.inventory_list:
            temp_frame = pd.read_csv(file, delimiter=',',encoding='cp1252')
            self.inventory_frame = pd.concat([self.inventory_frame, temp_frame], ignore_index=True, axis=0)
        for file in self.reserved_list:
            temp_frame_2 = pd.read_csv(file, delimiter=',',encoding='cp1252')
            self.reserved_frame = pd.concat([self.reserved_frame, temp_frame_2], ignore_index=True, axis=0)

    def _concentrate_data(self):
        """Concentrating data into one dataframe"""
        self.result_frame = pd.merge(self.inventory_frame, self.reserved_frame, on='fnsku', how='outer')

    def get_data(self, directory=None):
        self._create_lists(directory=directory)
        self._read_data()
        self._concentrate_data()
        return self.result_frame


# test=Reports_loading()
# frame=test.get_data(directory='./Amz Stock and Amz Orders')
# frame.to_excel('test_file.xlsx', sheet_name='list1')