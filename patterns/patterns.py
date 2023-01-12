from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Union


class Component(ABC):
    """Интерфейс для категорий и курсов"""

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def create(name: str, parent_category: Category = None) -> Component:
        raise NotImplementedError

    def __repr__(self):
        return f'<Component {self.__class__.__name__} {self.name}>'


class Category(Component):
    categories: List[Category] = []

    def __init__(self, name: str):
        super().__init__(name)
        self.parent = None
        self.children: List[Component] = []

    @staticmethod
    def create(name: str, parent_category: Category = None) -> Category:
        category = Category(name)
        if parent_category:
            category.parent = parent_category
            parent_category.children.append(category)
        # Category._add_to_categories_list(category)
        return category

    # @staticmethod
    # def _add_to_categories_list(category: Category) -> None:
    #     Category.categories.append(category)


class Course(Component):
    def __init__(self, name: str, parent_category: Category):
        super().__init__(name)
        self.parent = parent_category

    @staticmethod
    def create(name: str, parent_category: Category) -> Course:
        course = Course(name, parent_category)
        parent_category.children.append(course)
        return course


class Engine:
    _category_list: List[Category] = []
    _course_list: List[Course] = []

    def create_category(self, name: str, parent_category: Category = None) -> Category:
        category = Category.create(name, parent_category)
        self._add_to_component_list(category)
        return category

    def create_course(self, name: str, parent_category: Category) -> Course:
        course = Course.create(name, parent_category)
        self._add_to_component_list(course)
        return course

    @classmethod
    def _add_to_component_list(cls, component: Component) -> None:
        if isinstance(component, Category):
            cls._category_list.append(component)
        elif isinstance(component, Course):
            cls._course_list.append(component)

    @classmethod
    def get_categories(cls)-> List[Category]:
        return cls._category_list

    @classmethod
    def get_courses(cls) -> List[Course]:
        return cls._course_list

    @classmethod
    def get_category_by_name(cls, name: str) -> Union[Category, None]:
        for category in cls._category_list:
            if category.name == name:
                return category
        return None

if __name__ == '__main__':
    engine = Engine()
    engine.create_category('fgh')
    print(engine.get_categories())
    print(engine.get_category_by_name('fgh'))
    h = engine.create_course('fishing', engine.get_category_by_name('fgh'))
    print(engine.get_courses())
    print(h.parent)
    engine.create_category('salmo', engine.get_category_by_name('fgh'))
    print(engine.get_category_by_name('fgh').children)

