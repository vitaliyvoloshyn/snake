import os

from models import create_start_categories, create_start_course_types, queue_




def create_table(connection) -> None:
    """Создание таблицы в БД"""
    cur = connection.cursor()
    # cur.execute('DROP TABLE IF EXISTS student;')
    # cur.execute('DROP TABLE IF EXISTS course;')
    # cur.execute('DROP TABLE IF EXISTS category;')
    for model in queue_:
        cur.execute(model().get_sql_query_create_table())
    create_start_categories()
    create_start_course_types()
    cur.close()


def _get_sql_query_string(table_name: str, fields: dict) -> str:
    return f'CREATE TABLE IF NOT EXISTS {table_name} ({_get_fields_name_and_types_to_str(fields)});'


def _get_fields_name_and_types_to_str(fields: dict) -> str:
    out_str: str = ''
    for field, type_ in fields.items():
        out_str += f' {field} {type_.sql_query()},'
    return out_str[:-1]

if __name__ == '__main__':
    create_table()
