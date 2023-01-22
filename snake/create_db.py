import os
import sqlite3

from settings import DATABASE, BASE_DIR


def create_db():
    if not os.path.exists(os.path.join(BASE_DIR, DATABASE.get('name'))):
        database_file = os.path.join(BASE_DIR, DATABASE.get('name'))
        con = sqlite3.connect(database_file)
        cur = con.cursor()
        with open(os.path.join(BASE_DIR, 'snake', 'create_db.sql'), 'r') as f:
            text = f.read()
        cur.executescript(text)
        cur.close()
        con.close()
        print('Создан файл базы данных')


if __name__ == '__main__':
    if not os.path.exists(os.path.join(BASE_DIR, DATABASE.get('name'))):
        print('create')
        create_db()
    else:
        print('not create')
