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
    categories: List[Category] = []

    def __init__(self, name: str, path_img: str = ''):
        super().__init__(name)
        self.path_img = path_img
        self.parent = None
        self.children: List[Component] = []
        self.course_count = self.course_count

    @staticmethod
    def create(name: str, parent_category: Category = None, path_img: str = '') -> Category:
        category = Category(name, path_img)
        if parent_category:
            category.parent = parent_category
            parent_category.children.append(category)
        return category

    def course_count(self) -> int:
        course_count = 0
        for child in self.children:
            if isinstance(child, Course):
                course_count += 1
        return course_count

    def subcategories_count(self) -> int:
        subcategories_count = 0
        for child in self.children:
            if isinstance(child, Category):
                subcategories_count += 1
        return subcategories_count


class CourseCopy:
    def clone(self):
        copy_course = deepcopy(self)
        return copy_course

class Course(Component, CourseCopy):
    def __init__(self, name: str, parent_category: Category):
        super().__init__(name)
        self.parent = parent_category
        self.parent.children.append(self)
        self.observers: List[Student] = []

    def add_observer(self, observer: Student) -> None:
        self.observers.append(observer)

    def send_notification(self, notifier: Tuple[Notifier]) -> None:
        for obsrerver in self.observers:
            obsrerver.student_notify(notifier)


class RecordCourse(Course):
    """класс курса в записи"""
    type: str = 'В записи'

    def __init__(self, name: str, parent_category: Category):
        super().__init__(name, parent_category)




class OnlineCourse(Course):
    """класс курса в записи"""

    def __str__(self):
        return 'Онлайн'


class LiveCourse(Course):
    """класс курса вживую"""

    def __str__(self):
        return 'Вживую'


@dataclass
class CoursesTypes:
    online: Course = OnlineCourse
    record: Course = RecordCourse
    live: Course = LiveCourse


class CourseFactory:
    @staticmethod
    def create(type_: Course, name: str, parent_category: Category) -> Course:
        """Фабричный метод"""
        return type_(name, parent_category)


class Student:
    def __init__(self, first_name: str, last_name: str, email: str, phone: str, course: Course):
        self.course = course
        self.phone = phone
        self.email = email
        self.last_name = last_name
        self.first_name = first_name
        self.course.add_observer(self)

    def student_notify(self, notifier: Tuple[Notifier]) -> None:
        for ntfr in notifier:
            ntfr.notify(self)


class Notifier(ABC):
    @classmethod
    @abstractmethod
    def notify(cls, student: Student):
        pass


class EmailNotifier(Notifier):
    @classmethod
    def notify(cls, student: Student):
        print(
            f'Отправлено уведомление студенту {student.last_name} {student.first_name} на электронный адрес {student.email}')


class PhoneNotifier(Notifier):
    @classmethod
    def notify(cls, student: Student):
        print(f'Отправлено уведомление студенту {student.last_name} {student.first_name} на телефон {student.phone}')


class Engine:
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
        for cat in Engine.start_categories:
            self.create_category(cat[0], path_img=cat[1])

    def create_category(self, name: str, parent_category: Category = None, path_img: str = '') -> Category:
        category = Category.create(name, parent_category, path_img)
        self._add_to_category_list(category)
        return category

    def create_course(self, type_: Course, name: str, parent_category: Category) -> Course:
        course = CourseFactory.create(type_, name, parent_category)
        self._add_to_courses_list(course)
        return course

    def clone_course(self, course: Course):
        new_course = course.clone()
        course.parent.children.append(new_course)
        self._add_to_courses_list(new_course)

    def create_student(self, first_name: str, last_name: str, email: str, phone: str, course: Course) -> Student:
        if self._validate_email(email):
            student = Student(first_name, last_name, email, phone, course)
            self._add_to_student_list(student)
            mapper = MapperRegistry.get_current_mapper('student')
            mapper.insert(student)
            return student

    @classmethod
    def _add_to_category_list(cls, category: Category) -> None:
        cls._category_list.append(category)

    @classmethod
    def _add_to_courses_list(cls, course: Course) -> None:
        cls._courses_list.append(course)

    @classmethod
    def _add_to_student_list(cls, student: Student) -> None:
        cls._students_list.append(student)

    @classmethod
    def get_categories(cls) -> List[Category]:
        return cls._category_list

    @classmethod
    def get_categories_without_parents(cls) -> List[Category]:
        return list(filter(lambda x: x.parent is None, cls._category_list))

    @classmethod
    def get_students(cls) -> List[Student]:
        return cls._students_list

    @classmethod
    def get_students(cls, course: Course = None) -> List[Student]:
        if course:
            return list(filter(lambda x: x.course is course, cls._students_list))
        return cls._students_list

    @classmethod
    def count_students(cls, course: Course = None) -> int:
        cnt = len(cls.get_students(course))
        return cnt

    @classmethod
    def get_student_by_email(cls, email: str) -> Union[Student, None]:
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
        for category in cls._category_list:
            if category.name == name:
                return category
        for course in cls._courses_list:
            if course.name == name:
                return course
        return None


class Handler:
    def print_(self, text):
        pass


class ConsoleHandler(Handler):
    def print_(self, text):
        print(text)


class FileHandler(Handler):
    def __init__(self, filename: str):
        self._out_file = filename

    def print_(self, text: str):
        with open(self._out_file, 'a') as f:
            f.write(text + '\n')


class Formatter:
    @staticmethod
    def get_format_text(text):
        return f'log >>> {text}'


class Log:
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
        if handler.__name__ == 'FileHandler':
            self._handler = handler(f'{self._name}_log.txt')
        elif handler.__name__ == 'ConsoleHandler':
            self._handler = handler

    def set_formatter(self, formatter: Formatter):
        self._formatter = formatter

    def log(self, text: str):
        self._handler.print_(self._formatter.get_format_text(text))


def get_logger(name: str) -> Log:
    return Log(name)


class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'student'

    def all(self) -> List[Student]:
        statement = f'SELECT * from {self.tablename}'
        result = []
        for item in self.cursor.execute(statement).fetchall():
            id, first_name, last_name, email, phone, course = item
            course = Engine.get_component_by_name(course)
            student = Student(first_name, last_name, email, phone, course)

            result.append(student)
        return result

    def find_by_id(self, id: int) -> List[Student]:
        statement = f"SELECT * FROM {self.tablename} WHERE id=?"
        result = self.cursor.execute(statement, (id,)).fetchone()
        if result:
            id, first_name, last_name, email, phone, course = result
            course = Engine.get_component_by_name(course)
            student = Student(first_name, last_name, email, phone, course)
            return student
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj: Student) -> None:
        statement = f"INSERT INTO {self.tablename} (first_name, last_name, email, phone, course)" \
                    f"VALUES (?,?,?,?,?)"
        self.cursor.execute(statement, (obj.first_name, obj.last_name, obj.email, obj.phone, obj.course.name))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj_id: int, obj: Student) -> None:
        statement = f"UPDATE {self.tablename} SET first_name=?, last_name=?, email=?, phone=?, course=? Where id=?"

        self.cursor.execute(statement, (obj.first_name, obj.last_name, obj.email, obj.phone, obj.course.name, obj_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, id: int):
        statement = f"DELETE FROM {self.tablename} WHERE id={id}"
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)

def get_connection():
    return connect(os.path.join(BASE_DIR, DATABASE.get('name')))


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'student': StudentMapper,
    }

    @staticmethod
    def get_current_mapper(name: str) -> StudentMapper:
        return MapperRegistry.mappers[name](get_connection())


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


if __name__ == '__main__':
    engine = Engine()
    cat1 = engine.get_component_by_name('Кулинарные курсы')
    course1 = engine.create_course(CoursesTypes.record, 'course1', cat1)
    # st1 = engine.create_student('John', 'Connor', 'sdd@sd.c', '+1245780545', course1)
    # st2 = engine.create_student('John', 'Connor', 'zsdd@sd.c', '+1245780545', course1)
    # st3 = engine.create_student('John', 'Connor', 'zzsdd@sd.c', '+1245780545', course1)
    st4 = Student('Johnny_bhbh', 'Connor', 'zzsdd@sd.c', '+1245780545', course1)
    mapp = MapperRegistry.get_current_mapper('student')
    print(mapp.all())
    print(mapp.find_by_id(3))
    mapp.update(4, st4)
    mapp.delete(4)
    mapp.delete(4)

