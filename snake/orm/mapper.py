from typing import List

from snake.orm.connection import get_connection
from snake.orm.exception import RecordNotFoundException, DbCommitException, DbUpdateException, DbDeleteException
from snake.utils.user_models import get_attr_class


class Query:
    pass


class Mapper:
    """Реализует ORM для моделей.
        Поддерживаемые методы:
        - выборка всех значений из таблицы;
        - выборка по id;
        - выборка данных по условию;
        - создание записи в таблице;
        - редактирование записи в таблице;
        - удаление записи из таблицы"""

    # entity: object = None

    def __init__(self, model):

        self.connection = get_connection()
        self.cursor = self.connection.cursor()
        self.model = model
        self.model_attr: tuple = self._get_model_attr(self.model.__class__)

    def _get_obj_from_data_query(self, data):
        obj = Query()
        attrs = {self.model.pk: data[0]}
        attrs.update({field: value for field, value in zip(self.model_attr, data[1:])})
        obj.__dict__ = attrs
        return obj

    @staticmethod
    def _get_model_attr(model) -> tuple:
        attr = get_attr_class(model)
        return tuple(key for key in attr.keys())

    def all(self) -> List[Query]:
        """Выборка всех значений из таблицы"""
        res: list = []
        statement = f'SELECT * from {self.model.table_name}'
        for data in self.cursor.execute(statement).fetchall():
            res.append(self._get_obj_from_data_query(data))
        return res

    def find_by_id(self, id: int) -> Query:
        """выборка по id"""
        statement = f"SELECT * FROM {self.model.table_name} WHERE {self.model.pk}={id}"
        result = self.cursor.execute(statement).fetchone()
        if result:
            return self._get_obj_from_data_query(result)

        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def filter(self, **kwargs) -> List[Query]:
        """Выборка данных по условию. Принимает словарь - параметр и значение. Принимает только один фильтр"""
        lst: list = []
        param = list(kwargs.keys())[0]
        value = kwargs.get(param)
        statement = f"SELECT * FROM {self.model.table_name} WHERE {param}='{value}'"
        for data in self.cursor.execute(statement).fetchall():
            lst.append(self._get_obj_from_data_query(data))
        return lst

    def insert(self, *args) -> None:
        """Создание записи в таблице"""
        statement = f"INSERT INTO {self.model.table_name} ({', '.join(self.model_attr)}) " \
                    f"VALUES {args if len(args)>1 else '(' + chr(34) + args[0] + chr(34) + ')'}"
        print(statement)
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj_id: int, obj) -> None:
        """Редактирование записи в таблице"""
        statement = f"UPDATE {self.model.table_name} SET first_name=?, last_name=?, email=?, phone=?, course=? Where id=?"

        self.cursor.execute(statement, (obj.first_name, obj.last_name, obj.email, obj.phone, obj.course.name, obj_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, id: int):
        """Удаление записи из таблицы"""
        statement = f"DELETE FROM {self.model.table_name} WHERE {self.model.pk}={id}"
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)
