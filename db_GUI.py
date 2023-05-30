import tkinter as tk
import os
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkinter import messagebox
import db_connect as dbc
from tkcalendar import DateEntry


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.options = ['1359.eu11', 'nemo.eu2']
        selected_option = StringVar()
        selected_option.set(self.options[0])
        self.combobox = Combobox(self, values=self.options, textvariable=selected_option)
        self.combobox_label = tk.Label(self, text="Account:")
        self.combobox_label.grid(row=0, column=0, sticky=tk.W)
        self.combobox.grid(row=0, column=1, sticky=tk.W)

        self.token_label = tk.Label(self, text="Token" + str(self.read_token))
        self.token_label.grid(row=1, column=0, sticky=tk.W)

        self.start_label = tk.Label(self, text="Start:")
        self.start_label.grid(row=2, column=0, sticky=tk.W)
        self.start_entry = tk.Entry(self)
        self.start_entry.grid(row=2, column=1)

        self.end_label = tk.Label(self, text="End:")
        self.end_label.grid(row=2, column=2, sticky=tk.W)
        self.end_entry = tk.Entry(self)
        self.end_entry.grid(row=2, column=3)

        self.orders_update = tk.Button(self, text="Load orders", command=self.update_orders)
        self.orders_update.grid(row=3, column=0)

        self.orders = tk.Button(self, text="Load orders", command=self.load_orders)
        self.orders.grid(row=3, column=1)

        self.products = tk.Button(self, text="Load orders", command=self.load_products)
        self.products.grid(row=3, column=0)



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
        dbc.update_pages(starter=self.start_entry.get(), ender=self.end_entry.get(),
                         link='https://' + self.combobox.get() + '.ysell.pro/api/v1/', tablename=self.orders_name,
                         token=self.token_name)

    def load_orders(self):
        dbc.update_orders(table_name=self.orders_name, start=self.start_entry.get(), end=self.end_entry.get(),
                          link='https://' + self.combobox.get() + '.ysell.pro/api/v1/', token=self.token_name)

    def load_products(self):
        dbc.update_products(table_name=self.orders_name,link='https://' + self.combobox.get() + '.ysell.pro/api/v1/', token=self.token_name)

root = tk.Tk()
root.title("Data Processing App")
root.geometry("550x200")
root.resizable(False, False)
root.columnconfigure(3, minsize=50, weight=1)
root.columnconfigure(1, minsize=50, weight=1)

app = App(master=root)
app.mainloop()
