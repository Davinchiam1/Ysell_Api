import datetime
from Api_connect import Ysell_regu
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, insert, select, exists, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DATETIME, Date, MetaData, Table, text
import pandas as pd
import sqlalchemy
import numpy as np

# создаем сессию
engine = create_engine('postgresql://data_user:12345678@localhost:5432/Aprobation')
Session = sessionmaker(bind=engine)
Base = sqlalchemy.orm.declarative_base()

# session = Session()

def create_table(table_name, columns):
    # Создаем объект таблицы
    metadata = MetaData()
    table = Table(table_name, metadata)
    inspector = inspect(engine)
    for name, data_type in columns.items():
        if name == 'id':
            table.append_column(Column(name, data_type, primary_key=True))
        else:
            table.append_column(Column(name, data_type))
    if not table_name in inspector.get_table_names():
        metadata.create_all(engine)
    return table


def create_colums(frame=pd.DataFrame()):
    columns_dict = {'id': Integer}
    for col, dtype in frame.dtypes.items():
        if dtype == 'int64':
            columns_dict[col] = Integer
        elif dtype == 'float64':
            columns_dict[col] = Float
        elif str(dtype).startswith('object'):
            columns_dict[col] = String
        else:
            columns_dict[col] = String
    return columns_dict


data = Ysell_regu().orders_req(start=151, end=160)
test = create_colums(data)
table_name = 'orders'
orders = create_table(table_name, test)




class Orders(Base):
    __tablename__ = table_name
    __table__ = orders


session = Session()

with engine.connect() as connection:
    # Загрузить данные из датафрейма в список словарей
    data['id']=data.index
    data1 = data.to_dict('records')

    # Обновить или добавить записи в таблицу
    for row in data1:
        orders = Orders(**row)
        session.merge(orders)
session.commit()
session.close()
with engine.connect() as connection:
    result = connection.execute(text('SELECT * FROM ' + table_name))
    df_result = pd.DataFrame(result.fetchall(), columns=result.keys())
    df_result.to_excel('1234.xlsx')
    print(df_result.tail())

# закрытие соединения
engine.dispose()
# Session = sessionmaker(bind=engine)
# session = Session()
#
# handbook = Handbook.__table__
# select_statement = handbook.select()
# result_set = session.execute(select_statement)
#
# for row in result_set:
#     print(row)
