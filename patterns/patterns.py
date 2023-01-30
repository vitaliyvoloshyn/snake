from __future__ import annotations

import os.path
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from sqlite3 import connect
from typing import List, Union, Tuple

from settings import DATABASE, BASE_DIR
from snake.exeptions import NotUniqueEmail


class Component(ABC):
    """Интерфейс для категорий и курсов"""

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<Component {self.__class__.__name__} {self.name}>'


class Category(Component):
    """Объект категории"""
    categories: List[Category] = []

    def __init__(self, name: str, path_img: str = ''):
        super().__init__(name)
        self.path_img = path_img
        self.parent = None
        self.children: List[Component] = []
        self.course_count = self.course_count

    @staticmethod
    def create(name: str, parent_category: Category = None, path_img: str = '') -> Category:
        """Создание категории. Возвращает экземпляр класса Category"""
        category = Category(name, path_img)
        if parent_category:
            category.parent = parent_category
            parent_category.children.append(category)
        return category

    def course_count(self) -> int:
        """Возвращает количество курсов в категории из своего списка дочерних элементов.
        Курсы дочерних подкатегорий не учитываются"""
        course_count = 0
        for child in self.children:
            if isinstance(child, Course):
                course_count += 1
        return course_count

    def subcategories_count(self) -> int:
        """Возвращает количество подкатегорий в категории из своего списка дочерних элементов.
        Подкатегории дочерних подкатегорий не учитываются"""
        subcategories_count = 0
        for child in self.children:
            if isinstance(child, Category):
                subcategories_count += 1
        return subcategories_count


class CourseCopy:
    """Класс, реализующий паттерн Прототип."""
    def clone(self):
        """Копирует объект и возвращает копию"""
        copy_course = deepcopy(self)
        return copy_course


class Course(Component, CourseCopy):
    """Объект Курса"""
    def __init__(self, name: str, parent_category: Category):
        super().__init__(name)
        self.parent = parent_category
        self.parent.children.append(self)
        self.observers: List[Student] = []

    def add_observer(self, observer: Student) -> None:
        """Добавление подписчика (студента)"""
        self.observers.append(observer)

    def send_notification(self, notifier: Tuple[Notifier]) -> None:
        """Информирование подписчиков курса"""
        for observer in self.observers:
            observer.student_notify(notifier)


class RecordCourse(Course):
    """класс курса в записи"""
    type: str = 'В записи'

    def __init__(self, name: str, parent_category: Category):
        super().__init__(name, parent_category)


class OnlineCourse(Course):
    """класс курса в записи"""

    type: str = 'Онлайн'

    def __str__(self):
        return 'Онлайн'


class LiveCourse(Course):
    """класс курса вживую"""
    type: str = 'Вживую'

    def __str__(self):
        return 'Вживую'


@dataclass
class CoursesTypes:
    """Датакласс, хранящий типы курсов"""
    online: Course = OnlineCourse
    record: Course = RecordCourse
    live: Course = LiveCourse


class CourseFactory:
    """Фабрика для создания курсов"""
    @staticmethod
    def create(type_: Course, name: str, parent_category: Category) -> Course:
        """Фабричный метод. Возвращает экземпляр объекта Course"""
        return type_(name, parent_category)


class Student:
    """Объект студент"""
    def __init__(self, student_id: int = 0, first_name: str = '', last_name: str = '', email: str = '', phone: str = '', course: Course = None):
        self.student_id = student_id
        self.course = course
        self.phone = phone
        self.email = email
        self.last_name = last_name
        self.first_name = first_name

    def student_notify(self, notifier: Tuple[Notifier]) -> None:
        """Информирование студентов"""
        for ntfr in notifier:
            ntfr.notify(self)


class Notifier(ABC):
    """Абстрактный класс уведомителя"""
    @classmethod
    @abstractmethod
    def notify(cls, student: Student):
        pass


class EmailNotifier(Notifier):
    """Уведомитель по электронной почте"""
    @classmethod
    def notify(cls, student: Student):
        """Функция уведомления"""
        print(
            f'Отправлено уведомление студенту {student.last_name} {student.first_name} на электронный адрес {student.email}')


class PhoneNotifier(Notifier):
    """Уведомитель по телефону (смс)"""
    @classmethod
    def notify(cls, student: Student):
        """Функция уведомления"""
        print(f'Отправлено уведомление студенту {student.last_name} {student.first_name} на телефон {student.phone}')


class Engine:
    """Реализует API по созданию категорий, курсов, студентов"""
    _category_list: List[Category] = []
    _students_list: List[Student] = []
    _courses_list: List[Course] = []
    start_categories = [
        ['Кулинарные курсы', 'img/kulinarnie_kursy.jpg'],
        ['Кондитерские курсы', 'img/konditerskie_kursi.jpg'],
        ['Мастер-классы', 'img/master-class.jpg']
    ]

    def __init__(self):
        self.create_start_categories()

    def create_start_categories(self):
        """Создание тестовых категорий при инициализации объекта Engine"""
        for cat in Engine.start_categories:
            self.create_category(cat[0], path_img=cat[1])

    def create_category(self, name: str, parent_category: Category = None, path_img: str = '') -> Category:
        """Создание категории"""
        category = Category.create(name, parent_category, path_img)
        self._add_to_category_list(category)
        return category

    def create_course(self, type_: Course, name: str, parent_category: Category) -> Course:
        """Создание курса"""
        course = CourseFactory.create(type_, name, parent_category)
        self._add_to_courses_list(course)
        return course

    def clone_course(self, course: Course):
        """Копирование существующего курса"""
        new_course = course.clone()
        course.parent.children.append(new_course)
        self._add_to_courses_list(new_course)

    def create_student(self, first_name: str, last_name: str, email: str, phone: str, course: Course) -> Student:
        """Создание студента"""
        if self._validate_email(email):
            student = Student(first_name, last_name, email, phone, course)
            course.add_observer(student)
            self._add_to_student_list(student)
            mapper = MapperRegistry.get_current_mapper('student')
            mapper.insert(student)
            return student

    @classmethod
    def _add_to_category_list(cls, category: Category) -> None:
        """Добавляет категорию в список категорий"""
        cls._category_list.append(category)

    @classmethod
    def _add_to_courses_list(cls, course: Course) -> None:
        """Добавляет курс в список курсов"""
        cls._courses_list.append(course)

    @classmethod
    def _add_to_student_list(cls, student: Student) -> None:
        """Добавляет студента в список студентов"""
        cls._students_list.append(student)

    @classmethod
    def get_categories(cls) -> List[Category]:
        """Возвращает список категорий"""
        return cls._category_list

    @classmethod
    def get_categories_without_parents(cls) -> List[Category]:
        """Возвращает список категорий, не имеющих родителей"""
        return list(filter(lambda x: x.parent is None, cls._category_list))

    @classmethod
    def get_students(cls, course: Course = None) -> List[Student]:
        """Возвращает список студентов"""
        if course:
            return list(filter(lambda x: x.course is course, cls._students_list))
        return cls._students_list

    @classmethod
    def count_students(cls, course: Course = None) -> int:
        """Возвращает количество студентов на курсе"""
        cnt = len(cls.get_students(course))
        return cnt

    @classmethod
    def get_student_by_email(cls, email: str) -> Union[Student, None]:
        """Возвращает объект студента по email"""
        for student in cls._students_list:
            if student.email == email:
                return student
        return None

    @classmethod
    def _validate_email(cls, email: str) -> bool:
        """Проверка уникальности email при регистрации нового пользователя"""
        if cls.get_student_by_email(email):
            raise NotUniqueEmail(f'Пользователь с электронным адресом {email} уже зарегистрирован')
        return True

    @classmethod
    def get_courses(cls) -> List[Union[Course, None]]:
        """Возвращает список всех созданных курсов"""
        return cls._courses_list

    @classmethod
    def get_component_by_name(cls, name: str) -> Union[Component, None]:
        """Возвращает категорию или курс по имени компонента"""
        for category in cls._category_list:
            if category.name == name:
                return category
        for course in cls._courses_list:
            if course.name == name:
                return course
        return None


class Handler:
    """Абстрактный класс обработчика вывода для логгера"""
    def print_(self, text):
        """Функция вывода сообщения"""
        pass


class ConsoleHandler(Handler):
    """Обработчик вывода в консоль"""
    def print_(self, text):
        """Функция вывода сообщения"""
        print(text)


class FileHandler(Handler):
    """Обработчик вывода в файл"""
    def __init__(self, filename: str):
        self._out_file = filename

    def print_(self, text: str):
        """Функция вывода сообщения"""
        with open(self._out_file, 'a') as f:
            f.write(text + '\n')


class Formatter:
    """Объект форматировщика сообщений для логгера"""
    @staticmethod
    def get_format_text(text):
        """Возвращает отформатированное сообщение"""
        return f'log >>> {text}'


class Log:
    """Класс логгера"""
    _instance: dict = {}

    def __init__(self, name: str):
        self._name = name
        self._handler = ConsoleHandler()
        self._formatter = Formatter()

    def __new__(cls, *args, **kwargs):
        name = args[0] if args else kwargs.get('name', None)
        if not cls._instance.get(name, None):
            cls._instance[name] = super().__new__(cls)
        return cls._instance[name]

    def set_handler(self, handler: Handler):
        """Устанавливает обработчик вывода"""
        if handler.__name__ == 'FileHandler':
            self._handler = handler(f'{self._name}_log.txt')
        elif handler.__name__ == 'ConsoleHandler':
            self._handler = handler

    def set_formatter(self, formatter: Formatter):
        """Устанавливает форматировщик сообщений"""
        self._formatter = formatter

    def log(self, text: str):
        """Логгирование сообщения"""
        self._handler.print_(self._formatter.get_format_text(text))


def get_logger(name: str) -> Log:
    """Возвращает объект логгера"""
    return Log(name)


class Mapper:
    """Реализует ORM для моделей.
        Поддерживаемые методы:
        - выборка всех значений из таблицы;
        - выборка по id;
        - выборка данных по условию;
        - создание записи в таблице;
        - редактирование записи в таблице;
        - удаление записи из таблицы"""

    table_name: str = ''
    entity: object = None

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def all(self) -> list:
        """Выборка всех значений из таблицы"""
        statement = f'SELECT * from {self.table_name}'
        return self.cursor.execute(statement).fetchall()

    def find_by_id(self, id: int) -> list:
        """выборка по id"""
        statement = f"SELECT * FROM {self.table_name} WHERE id=?"
        result = self.cursor.execute(statement, (id,)).fetchone()
        if result:
            return result
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def filter(self, **kwargs) -> list:
        """Выборка данных по условию. Принимает словарь - параметр и значение. Принимает только один фильтр"""
        param = list(kwargs.keys())[0]
        value = kwargs.get(param)
        statement = f"SELECT * FROM {self.table_name} WHERE {param}='{value}'"
        result = self.cursor.execute(statement).fetchone()
        if result:
            return result
        else:
            raise RecordNotFoundException(f'record with param {param}: {value} not found')

    def insert(self, *args) -> None:
        """Создание записи в таблице"""
        statement = f"INSERT INTO {self.table_name} " \
                    f"VALUES (?,?,?,?,?,?)"
        self.cursor.execute(statement, args)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj_id: int, obj: Student) -> None:
        """Редактирование записи в таблице"""
        statement = f"UPDATE {self.table_name} SET first_name=?, last_name=?, email=?, phone=?, course=? Where id=?"

        self.cursor.execute(statement, (obj.first_name, obj.last_name, obj.email, obj.phone, obj.course.name, obj_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, id: int):
        """Удаление записи из таблицы"""
        statement = f"DELETE FROM {self.table_name} WHERE id={id}"
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)

    def _create_object_instance(self, *args):
        """Создает инстанс сущности объекта"""
        return self.entity(args)


class StudentMapper(Mapper):
    """Реализует ORM для модели студента.
    """
    table_name = 'student'



def get_connection():
    """"""
    return connect(os.path.join(BASE_DIR, DATABASE.get('name')))


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    """Регистр для мапперов различных моделей"""
    mappers = {
        'student': StudentMapper,
    }

    @staticmethod
    def get_current_mapper(name: str) -> StudentMapper:
        """Возвращает маппер по имени"""
        return MapperRegistry.mappers[name](get_connection())


class DbCommitException(Exception):
    """Класс, описывающий исключение при операции вставки данных в таблицу"""
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    """Класс, описывающий исключение при операции вставки данных в таблицу"""
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    """Класс, описывающий исключение при операции удаления данных из таблицы"""
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    """Класс, описывающий исключение при операции выборки данных из таблицы"""
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


if __name__ == '__main__':
    mod = MapperRegistry.get_current_mapper('student')
    res = mod.all()
    print(res)
