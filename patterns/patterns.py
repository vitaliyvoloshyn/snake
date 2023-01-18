from __future__ import annotations

from abc import ABC
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Union


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


class Engine:
    _category_list: List[Category] = []
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
        return course

    def clone_course(self, course: Course):
        new_course = course.clone()
        course.parent.children.append(new_course)

    @classmethod
    def _add_to_category_list(cls, category: Category) -> None:
        """Добавляет в список только категории без родителей (верхний уровень)"""
        if category.parent is None:
            cls._category_list.append(category)

    @classmethod
    def get_categories(cls) -> List[Category]:
        return cls._category_list


    @classmethod
    def get_component_by_name(cls, name: str) -> Union[Component, None]:
        for category in cls._category_list:
            if category.name == name:
                return category
            else:
                if isinstance(category, Category):
                    res = cls._get_component_by_name_from_children(name, category)
                    if res:
                        return res

        return None

    @classmethod
    def _get_component_by_name_from_children(cls, name: str, parent_category: Category) -> Union[Component, None]:
        for child in parent_category.children:
            if child.name == name:
                return child
            else:
                res = cls._get_component_by_name_from_children(name, child)
                if res:
                    return res

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


if __name__ == '__main__':
    engine = Engine()
