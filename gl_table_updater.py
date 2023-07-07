import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Combobox
from google_connector import Table_connest

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Загрузка данных в Google Таблицы')
        self.table_names={}

        # Создание элементов интерфейса
        self.lbl_title1 = tk.Label(self.root, text='Выберите таблицу:')
        self.combo_table = Combobox(self.root, values=self.get_table_names(), width=30)
        self.btn_browse = tk.Button(self.root, text='Выбрать папку', command=self.browse_directory)
        self.lbl_path = tk.Label(self.root, text='Выберите папку с файлами:')
        self.btn_upload = tk.Button(self.root, text='Загрузить данные', command=self.upload_data)

        # Размещение элементов на форме
        self.lbl_title1.pack()
        self.combo_table.pack()
        self.btn_browse.pack()
        self.lbl_path.pack()
        self.btn_upload.pack()

        self.data_directory = ''

    def get_table_names(self):
        with open('table_names.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(':')
                    table_name = parts[0].strip()
                    sheet_names = [name.strip() for name in parts[1].split(',')]
                    self.table_names[table_name] = sheet_names

            return list(self.table_names.keys())

    def browse_directory(self):
        self.data_directory = filedialog.askdirectory()
        self.lbl_path.configure(text=f'Выбранная папка: {self.data_directory}')

    def upload_data(self):
        table_name = self.combo_table.get()  # Выбранное имя таблицы

        if table_name == '':
            print('Выберите таблицу')
            return

        if self.data_directory == '':
            print('Выберите папку с файлами')
            return
        table_connect = Table_connest(table_name=table_name)
        table_connect.load_frame(title1=self.table_names[table_name][0], title2=self.table_names[table_name][0],
                                 data_directory=self.data_directory)

    def run(self):
        self.root.mainloop()

# Создание объекта интерфейса и запуск программы
gui = GUI()
gui.run()