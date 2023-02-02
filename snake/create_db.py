import importlib
import os
import sqlite3

from settings import DATABASE, BASE_DIR


def create_db():
    """Создание файла БД"""
    if not os.path.exists(os.path.join(BASE_DIR, DATABASE.get('name'))):
        database_file = os.path.join(BASE_DIR, DATABASE.get('name'))
        con = sqlite3.connect(database_file)
        cur = con.cursor()
        for name, clas in classes.items():
            attrs = get_attr_class(clas)
            cur.execute(create_table(name, **attrs))
        # cur.execute(add_category_foreign_key())
        cur.close()
        con.close()
        print('Создан файл базы данных')

def add_category_foreign_key():
    return f'ALTER table category add Foreign Key (category_id) references category(categoryid);'

def create_table(table_name: str, **kwargs) -> str:
    fields_str = ''
    for field, value_type in kwargs.items():
        fields_str += f'{field} {value_type.sql_query(field)},'
    statement = (f"""CREATE TABLE IF NOT EXISTS {table_name}(
       {fields_str[:-1]});
   """)
    print(statement)
    return statement


def models_classes() -> dict:
    """Возвращает список классов моделей, созданных пользователем в модуле models"""
    try:
        module = importlib.import_module('models')
        classes = {
            value.__name__.lower(): value
            for value in (
                getattr(module, name)
                for name in dir(module)
            )
            if isinstance(value, type)
               and getattr(value, '__module__', None) == module.__name__
        }
        return classes
    except ModuleNotFoundError:
        pass
    return []


def get_attr_class(clas) -> dict:
    """Возвращает словарь аттрибутов инстанса пользовательского класса"""
    from snake.models_ import ForeignKey

    dct = {key: value for key, value in clas().__class__.__dict__.items() if key != '__module__' and key != '__doc__'}
    deleted_keys: list = []
    for key, field_type in dct.items():
        if isinstance(field_type, ForeignKey):
            deleted_keys.append(key)
    for el in deleted_keys:
        value = dct.pop(el)
        dct.update({el + "_id": value})
    return dct


classes: dict = models_classes()

if __name__ == '__main__':
    create_db()
