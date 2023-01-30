import importlib
import inspect
import os
import sqlite3
import sys

from models import Models
from settings import DATABASE, BASE_DIR


def create_db():
    """Создание файла БД"""
    if not os.path.exists(os.path.join(BASE_DIR, DATABASE.get('name'))):
        database_file = os.path.join(BASE_DIR, DATABASE.get('name'))
        con = sqlite3.connect(database_file)
        cur = con.cursor()
        with open(os.path.join(BASE_DIR, 'snake', 'create_db.sql'), 'r') as f:
            text = f.read()
        classes = models_classes()
        for clas in classes:
            attrs = get_attr_class(clas)
            cur.execute(create_table(clas.__name__, **attrs))
        cur.executescript(text)
        cur.close()
        con.close()
        print('Создан файл базы данных')


def create_table(tablename: str, **kwargs) -> str:
    tablename = tablename.lower()
    fields_str = ''
    for fild, value_type in kwargs.items():
        fields_str += f'{fild} {value_type.sql_query},'
    statement = (f"""CREATE TABLE IF NOT EXISTS {tablename}(
       {tablename}id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
       {fields_str[:-1]});
   """)
    print(statement)
    return statement
def models_classes() -> list:
    """Возвращает список классов моделей, созданных пользователем в модуле models"""
    try:
        module = importlib.import_module('models')
        classes = [
            value
            for value in (
                getattr(module, name)
                for name in dir(module)
            )
            if isinstance(value, type)
               and getattr(value, '__module__', None) == module.__name__
        ]
        return classes
    except ModuleNotFoundError:
        pass
    return []

def get_attr_class(clas):
    return {key: value for key, value in clas.__dict__.items() if key != '__module__' and key != '__doc__'}

def create_tables():
    classes = models_classes()
    for clas in classes:
        attrs = get_attr_class(clas)
        return create_table(clas.__name__, **attrs)


if __name__ == '__main__':
    create_db()
