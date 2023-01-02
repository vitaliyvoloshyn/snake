from typing import List, Union

from my import CourseComponent, CategoryComponent, Category_, Course_, Component

class Course(Course_):
    pass

class Category(Category_):
    """Категория"""
    auto_id = 0

    def __init__(self, name: str, path_img: str = ''):
        super().__init__()
        # self.id = self.get_id()
        self.name = name
        self.path_img = path_img
        self.courses = []

    # def _course_count(self) -> int:
    #     return len(self.courses)

    # def get_id(self) -> int:
    #     """возвращает id для новосозданной категории"""
    #     if not self.children:
    #         return 1
    #     lst_obj = self.children.values().id
    #     print(lst_obj)
    #     o = map(lambda x: max(x.id), lst_obj)
    #     return o


    def __repr__(self):
        return self.name

    # @staticmethod
    # def create(name: str, path_img: str = ''):
    #
    #     return Category(name, path_img)


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

    def component(self, name: str) -> Union[Component, None]:
        for cat in self.categories:
            component = cat.get_child_by_name(name)
            if component:
                return component
        return None

    def create_start_categories(self):
        for cat in Engine.start_categories:
            self.create_category(cat[0], cat[1])

    def create_category(self, name: str, path_img: str = '') -> CategoryComponent:
        cat_obj = Category(name, path_img)
        cat_obj.add(cat_obj)
        print(cat_obj.children)
        self._add_component_to_list(cat_obj)
        return cat_obj

    def add_subcategory(self, parent: CategoryComponent, name: str, path_img: str = '') -> CategoryComponent:
        cat_obj = Category(name, path_img)
        parent.add(cat_obj)
        self._add_component_to_list(cat_obj)
        return cat_obj

    def add_course(self, parent: CategoryComponent, name: str) -> CourseComponent:
        course_obj = Course(name)
        parent.add(course_obj)
        self._add_component_to_list(course_obj)
        return course_obj

    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    def _add_component_to_list(self, component: Component):
        self.categories.append(component)

    def text(self, text):
        print(text)


if __name__ == '__main__':
    d = Engine()
    d.create_category('Кулинария')
    my_cat = d.component('Кулинария')
    print(my_cat.id)
    f = d.add_subcategory(d.component('Кулинария'), 'Азиатская')
    print(f.id)
