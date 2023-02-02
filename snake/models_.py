from __future__ import annotations
from snake.create_db import models_classes

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
    def __init__(self, model: str = ''):
        classes = models_classes()
        self.model = None
        if classes:
            self.model = classes.get(model, None)()

    def sql_query(self, field_name: str):
        return f'INTEGER, FOREIGN KEY ({field_name}) REFERENCES {self.model.table_name if self.model else "category"} ({self.model.pk_field_name if self.model else "categoryid"})'


class Id:
    def sql_query(self, field_name: str):
        return f'INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE'


class Models:
    """Базовый класс моделей"""

    def __init__(self):
        self.table_name = self.__class__.__name__.lower()  # Имя таблицы - название пользовательского класса в нижнем регистре
        self.set_id_field()

    def set_id_field(self):
        """Формирует аттрибут Primary Key и помещает его в пользовательский класс"""
        self.pk_field_name = f'{self.table_name}id'
        setattr(self.__class__, self.pk_field_name, Id())



if __name__ == '__main__':
    fore = ForeignKey()
