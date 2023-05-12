import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from frame_reader import Reports_loading

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


class Table_connest:

    def __init__(self, token='token.json', table_name='123'):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(token, scope)
        self.table_name = table_name
        client = gspread.authorize(self.credentials)
        self.table = client.open(table_name)

    def load_frame(self, title1,title2, data_directory):

        try:
            worksheet = self.table.worksheet(title=title1)
        except gspread.WorksheetNotFound:
            self.table.add_worksheet(title=title1, rows="150", cols="60")
            worksheet = self.table.worksheet(title1)

        loader = Reports_loading()
        data_invres,data_ord = loader.get_data(data_directory)
        data_invres.fillna('0', inplace=True)
        data = data_invres[data_invres.columns[1:].tolist() + [data_invres.columns[0]]]
        data = [data.columns.values.tolist()] + data.values.tolist()
        worksheet.update('A1', data)

        try:
            worksheet = self.table.worksheet(title=title2)
        except gspread.WorksheetNotFound:
            self.table.add_worksheet(title=title2, rows="150", cols="60")
            worksheet = self.table.worksheet(title1)
        columns=data_ord.columns.tolist()
        columns = [columns[-1]] + columns[:-1]
        data_ord=data_ord[columns]
        data = [data_ord.columns.values.tolist()] + data_ord.values.tolist()
        worksheet.update('A1', data)
        print('Данные успешно загружены в таблицу.')


table_connect = Table_connest(table_name='Chews_stock_best deal')
table_connect.load_frame(title1='Inv/Reserv',title2='Ord', data_directory='Z:\\Аналитика\\Amazon\\Update_api\\Amz Stock and Amz Orders')
# # Укажите путь к файлу ключа JSON
# credentials = ServiceAccountCredentials.from_json_keyfile_name('test-table-386307-5f6f43257222.json', scope)
#
# # Авторизуйтесь и получите доступ к Google Таблице
# client = gspread.authorize(credentials)
#
# # Откройте Google Таблицу по ее имени
# spreadsheet = client.open('123')
# # Выберите лист для чтения данных
# worksheet = spreadsheet.sheet1
#
# # Получите все значения из листа
# data = worksheet.get_all_values()
#
# # Преобразуйте данные в датафрейм
# df = pd.DataFrame(data)
#
# # Назначьте первую строку в качестве заголовков столбцов
# df.columns = df.iloc[0]
# df = df[1:]
#
# # Выведите датафрейм
# print(df)
