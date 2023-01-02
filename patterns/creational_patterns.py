from copy import deepcopy
from dataclasses import dataclass
from typing import List


class CourseCopy:

    def clone(self):
        copy_course = deepcopy(self)
        copy_course.id = self.get_id()
        return copy_course


class Course(CourseCopy):
    auto_id = 0
    """Интерфейс для создания курсов"""

    def __init__(self, name: str):
        self.name = name
        self.id = self.get_id()

    def __repr__(self):
        return self.name

    @classmethod
    def get_id(cls) -> int:
        """возвращает id для новосозданного курса"""
        cls.auto_id += 1
        return cls.auto_id


class RecordCourse(Course):
    """класс курса в записи"""

    def __str__(self):
        return 'В записи'


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
    def create(type_: Course, name: str) -> Course:
        """Фабричный метод"""
        return type_(name)


class Category:
    """Категория"""
    auto_id = 0

    def __init__(self, name: str, path_img: str = ''):
        self.id = self.get_id()
        self.name = name
        self.path_img = path_img
        self.courses = []

    def course_count(self) -> int:
        return len(self.courses)

    @classmethod
    def get_id(cls) -> int:
        """возвращает id для новосозданной категории"""
        cls.auto_id += 1
        return cls.auto_id

    def create_course(self, type_: Course, name: str) -> Course:
        course = CourseFactory.create(type_, name)
        self._add_course_to_list(course)
        return course

    def clone_course(self, course_name: str):
        course: Course = list(filter(lambda x: x.name == course_name, self.courses))
        self._add_course_to_list(course[0].clone())

    def _add_course_to_list(self, course: Course):
        """Добавить новый курс к списку курсов"""
        self.courses.append(course)

    def __repr__(self):
        return self.name


class Engine:
    """основной интерфейс проекта"""
    start_categories = [
        ['Кулинарные курсы', 'img/kulinarnie_kursy.jpg'],
        ['Кондитерские курсы', 'img/konditerskie_kursi.jpg'],
        ['Мастер-классы', 'img/master-class.jpg']
    ]

    def __init__(self):
        self.teachers = []
        self.students = []
        self.categories: List[Category] = []
        self.create_start_categories()

    def create_start_categories(self):
        for cat in Engine.start_categories:
            self.create_category(cat[0], cat[1])

    def create_category(self, name: str, path_img: str = ''):
        category_obj = Category(name, path_img)
        self.categories.append(category_obj)

    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    def text(self, text):
        print(text)


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
