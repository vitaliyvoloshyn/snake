from __future__ import annotations

from snake.orm.mapper import Mapper


class FieldType:
    def __init__(self, not_null: bool = False, unique: bool = False):
        self.unique = Unique(unique)
        self.not_null = NotNull(not_null)

    def sql_query(self, field_name: str = ''):
        return f' {self.not_null.sql_query()} {self.unique.sql_query()}'


class Text(FieldType):
    def sql_query(self, field_name: str = ''):
        return 'TEXT'


class Integer(FieldType):
    def sql_query(self, field_name: str = ''):
        return 'INTEGER'


class CharField(FieldType):
    def __init__(self, max_length: int = 255, not_null: bool = False, unique: bool = False):
        super().__init__(not_null, unique)
        self.string_len = max_length

    def sql_query(self, field_name: str = ''):
        return f'VARCHAR({self.string_len})' + super().sql_query()


class NotNull:
    def __init__(self, not_null: bool):
        self.not_null = not_null

    def sql_query(self, field_name: str = ''):
        return f'{"NOT NULL" if self.not_null else ""}'


class Unique:
    def __init__(self, unique: bool = False):
        self.unique = unique

    def sql_query(self, field_name: str = ''):
        return f'{"UNIQUE" if self.unique else ""}'


class ForeignKey:
    def __init__(self, model=None):
        self.model = None
        if model:
            self.model = model

    def sql_query(self, field_name: str):
        if self.model:
            self.model = self.model()
            return 'INTEGER', f'FOREIGN KEY ({field_name}) REFERENCES {self.model.table_name} ({self.model.pk})'
        else:
            return 'INTEGER', f'FOREIGN KEY ({field_name}) REFERENCES category (categoryId)'


class PrimaryKey:
    def sql_query(self, field_name: str):
        return f'INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE'


class Models:
    """Базовый класс моделей"""

    def __init__(self):
        self.table_name = self.__class__.__name__.lower()  # Имя таблицы - название пользовательского класса в нижнем регистре
        self.set_id_field()
        self.user_model_fields = self._get_attr_user_model_class(self.__class__)
        self.objects = Mapper(self)

    @staticmethod
    def _get_attr_user_model_class(clas) -> dict:
        """Возвращает словарь аттрибутов пользовательского класса"""
        dct = {key: value for key, value in clas.__dict__.items() if
               key != '__module__' and key != '__doc__'}
        return dct

    def set_id_field(self):
        """Формирует аттрибут Primary Key и помещает его в пользовательский класс"""
        self.pk = f'{self.table_name}Id'  # имя поля primary key таблицы

    def get_sql_query_create_table(self):
        query = f'CREATE TABLE IF NOT EXISTS {self.table_name} ' \
                f'({self._get_fields_name_and_types_to_str(self._get_fields_for_sql_query())});'
        print(query)
        return query

    def _get_fields_name_and_types_to_str(self, fields: dict) -> str:
        out_str: str = ''
        foreign_keys_query: str = ''
        for field, type_ in fields.items():
            query = type_.sql_query(field)
            if isinstance(query, str):
                out_str += f' {field} {query},'
            elif isinstance(query,tuple):
                out_str += f' {field} {query[0]},'
                foreign_keys_query += f' {query[1]},'
        out_str += foreign_keys_query
        return out_str[:-1]

    def _get_fields_for_sql_query(self) -> dict:
        out_dict: dict = {self.pk: PrimaryKey()}
        out_dict.update(self.user_model_fields)
        return out_dict


if __name__ == '__main__':
    fore = ForeignKey()
