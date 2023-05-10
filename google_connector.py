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

    def load_frame(self, title, data_directory):

        try:
            worksheet = self.table.worksheet(title=title)
        except gspread.WorksheetNotFound:
            self.table.add_worksheet(title=title, rows="150", cols="60")
            worksheet = self.table.worksheet(title)

        loader = Reports_loading()
        data = loader.get_data(data_directory)
        data.fillna('0', inplace=True)
        data = data[data.columns[1:].tolist() + [data.columns[0]]]
        data = [data.columns.values.tolist()] + data.values.tolist()
        worksheet.update('A1', data)
        print('Данные успешно загружены в таблицу.')


table_connect = Table_connest(table_name='Копия Chews_stock_для аналитиков')
table_connect.load_frame(title='Inv/Reserv', data_directory='Z:\\Аналитика\\Amazon\\Update_api\\Amz Stock and Amz Orders')
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
