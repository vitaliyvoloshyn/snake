from copy import deepcopy
from dataclasses import dataclass
from typing import List


class CourseCopy:

    def clone(self):
        copy_course = deepcopy(self)
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


if __name__ == '__main__':
    a=Engine()
    a.categories[0].create_course(CoursesTypes.online, 'pizza')
    a.categories[0].clone_course('pizza')
    print(type(list(CoursesTypes().__dict__.keys())[0]))
