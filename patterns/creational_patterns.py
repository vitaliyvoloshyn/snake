from copy import deepcopy
from quopri import decodestring


class IUser:
    """Абстрактный пользователь"""
    pass


class Teacher(IUser):
    """Пользователь"""
    pass


class Student(IUser):
    """Студент"""
    pass


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


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
        self.courses = []
        self.categories = []
        self.create_start_categories()

    def create_start_categories(self):
        for cat in Engine.start_categories:
            self.create_category(cat[0], cat[1])

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    # @staticmethod
    def create_category(self, name: str, path_img: str = ''):
        category_obj = Category(name, path_img)
        self.categories.append(category_obj)

    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    # @staticmethod
    # def create_course(type_, name, category):
    #     return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


if __name__ == '__main__':
    a = Engine()
    print(a.categories)
    print(a.categories[0].course_count())
