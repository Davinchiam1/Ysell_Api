import tkinter as tk
import os
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkinter import messagebox
import db_connect as dbc
from tkcalendar import DateEntry
import threading

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.options = ['1359.eu11', 'nemo.eu2']
        self.combobox = Combobox(self, values=self.options)
        self.combobox_label = tk.Label(self, text="Account:")
        self.combobox_label.grid(row=0, column=0, sticky=tk.W)
        self.combobox.grid(row=0, column=1, sticky=tk.W)
        self.combobox.bind("<<ComboboxSelected>>", self.selected)

        self.token_label = tk.Label(self,text='Token:')
        self.token_label.grid(row=1, column=0, sticky=tk.W,columnspan=3)

        self.start_label = tk.Label(self, text="Start:")
        self.start_label.grid(row=2, column=0, sticky=tk.W)
        self.start_entry = tk.Entry(self)
        self.start_entry.grid(row=2, column=1)

        self.end_label = tk.Label(self, text="End:")
        self.end_label.grid(row=2, column=2, sticky=tk.W)
        self.end_entry = tk.Entry(self)
        self.end_entry.grid(row=2, column=3,sticky=tk.W)

        self.orders_update = tk.Button(self, text="Update orders", command=self.update_orders)
        self.orders_update.grid(row=3, column=0,sticky=tk.N)

        self.orders = tk.Button(self, text="Load orders", command=self.load_orders)
        self.orders.grid(row=3, column=1,sticky=tk.N)

        self.products = tk.Button(self, text="Load products", command=self.load_products)
        self.products.grid(row=3, column=2,sticky=tk.N)

    def update_orders_thread(self):
        threading.Thread(target=self.update_orders).start()

    def load_orders_thread(self):
        threading.Thread(target=self.load_orders).start()

    def load_products_thread(self):
        threading.Thread(target=self.load_products).start()

    def selected(self, event):
        # получаем выделенный элемент
        if self.combobox.get() == self.options[0]:
            with open('token.txt', "r", encoding='utf8') as f:
                token = f.readline()
                self.token_name = 'token.txt'
                self.orders_name = 'orders'
                self.prod_table = 'products'
                self.token_label["text"] = f"Token: {token}"
        elif self.combobox.get() == self.options[1]:
            with open('token2.txt', "r", encoding='utf8') as f:
                token = f.readline()
                self.token_name = 'token2.txt'
                self.orders_name = 'orders_v2'
                self.prod_table = 'products_v2'
                self.token_label["text"] = f"Token: {token}"
    def read_token(self):
        if self.combobox.get() == self.options[0]:
            with open('token.txt', "r", encoding='utf8') as f:
                token = f.readline()
                self.token_name = 'token.txt'
                self.orders_name = 'orders'
                self.prod_table = 'products'
                return token
        elif self.combobox.get() == self.options[1]:
            with open('token2.txt', "r", encoding='utf8') as f:
                token = f.readline()
                self.token_name = 'token.txt'
                self.orders_name = 'orders_v2'
                self.prod_table = 'products_v2'
                return token

    def update_orders(self):
        dbc.update_pages(starter=int(self.start_entry.get()), ender=int(self.end_entry.get()),
                         link='https://' + self.combobox.get() + '.ysell.pro/api/v1/', tablename=self.orders_name,
                         token=self.token_name)

    def load_orders(self):
        dbc.update_orders(table_name=self.orders_name, start=int(self.start_entry.get()), end=int(self.end_entry.get()),
                          link='https://' + self.combobox.get() + '.ysell.pro/api/v1/', token=self.token_name)

    def load_products(self):
        dbc.update_products(table_name=self.prod_table,link='https://' + self.combobox.get() + '.ysell.pro/api/v1/', token=self.token_name)

root = tk.Tk()
root.title("Database update App")
root.geometry("450x100")
root.resizable(False, False)
# root.columnconfigure(3, minsize=50, weight=1)
# root.columnconfigure(1, minsize=50, weight=1)

app = App(master=root)
app.mainloop()
