import datetime
import sys

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
metadata = MetaData()


# session = Session()

def create_table(table_name, frame):
    # Создаем объект таблицы
    inspector = inspect(engine)
    if table_name in inspector.get_table_names():
        table = Table(table_name, metadata, autoload_with=engine)
    else:
        table = Table(table_name, metadata)
        columns = create_colums(frame)
        for name, data_type in columns.items():
            if name == 'id':
                table.append_column(Column(name, data_type, primary_key=True))
            else:
                table.append_column(Column(name, data_type))
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


def update_orders(table_name='orders', start=161, end=163,requ=None):
    data = requ.orders_req(start=start, end=end)
    orders = create_table(table_name, data)
    Base = sqlalchemy.orm.declarative_base()

    class Orders(Base):
        __tablename__ = table_name
        __table__ = orders

    session = Session()

    with engine.connect() as connection:
        # Загрузить данные из датафрейма в список словарей
        data['id'] = data.index
        data1 = data.to_dict('records')

        # Обновить или добавить записи в таблицу
        for row in data1:
            orders = Orders(**row)
            session.merge(orders)
    session.commit()
    session.close()
    # with engine.connect() as connection:
    #     result = connection.execute(text('SELECT * FROM ' + table_name))
    #     df_result = pd.DataFrame(result.fetchall(), columns=result.keys())
    #     df_result.to_excel('1234.xlsx')
    #     print(df_result.tail())
    #
    # # закрытие соединения
    # engine.dispose()


# update_orders(start=1, end=2)

def update_pages(starter=1,ender=100):
    # создаем один объект класса запросов к APi
    requ=Ysell_regu()
    for i in range(starter,ender):
        Base = sqlalchemy.orm.declarative_base()
        update_orders(start=1 + 100 * i, end=100 + 100 * i,requ=requ)



def update_products(table_name='products',requ=None):
    data = Ysell_regu().product_req()
    products = create_table(table_name, data)
    Base = sqlalchemy.orm.declarative_base()
    class Products(Base):
        __tablename__ = table_name
        __table__ = products

    session = Session()

    with engine.connect() as connection:
        # Загрузить данные из датафрейма в список словарей
        data['id'] = data.index
        data1 = data.to_dict('records')

        # Обновить или добавить записи в таблицу
        for row in data1:
            products = Products(**row)
            session.merge(products)
    session.commit()
    session.close()
    print('\n')
# update_products()


update_pages(73,75)