import os
from sqlite3 import connect

from settings import BASE_DIR, DATABASE

DB_FILE = os.path.join(BASE_DIR, DATABASE['name'])

def get_connection():
    """Возвращает объект подключения к БД"""

    if not (os.path.exists(os.path.join(BASE_DIR, DATABASE['name']))):
        from snake.orm.db import create_table
        connection = connect(DB_FILE)
        create_table(connection)
        connection.close()
        print('Файл базы данных создан')
    return connect(DB_FILE)
