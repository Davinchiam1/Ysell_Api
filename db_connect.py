import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DATETIME, Date
import pandas as pd
import sqlalchemy
import numpy as np

# создаем сессию
engine = create_engine('postgresql://data_user:12345678@localhost:5432/Aprobation')
Session = sessionmaker(bind=engine)
session = Session()

# создаем класс Stats
Base = sqlalchemy.orm.declarative_base()