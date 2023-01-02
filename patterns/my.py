from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class Component(ABC):
    auto_id = 0

    def __init__(self):
        self._parent = None

    def __str__(self):
        return self.name

    def get_child_by_name(self, name: str) -> Component:
        return self.children.get(name, None)

    @property
    def parent(self) -> Component:
        return self._parent

    @parent.setter
    def parent(self, parent: Component):
        self._parent = parent

    def get_id(self) -> int:
        """возвращает id для новосозданной категории"""
        self.__class__.auto_id += 1
        return self.auto_id


class CourseComponent(Component):
    pass


class CategoryComponent(Component):
    @abstractmethod
    def add(self, component: Component) -> None:
        pass

    @abstractmethod
    def remove(self, component: Component) -> None:
        pass

    @abstractmethod
    def get_course_count(self) -> int:
        pass


class Course_(CourseComponent):
    """
    Класс Лист представляет собой конечные объекты структуры. Лист не может
    иметь вложенных компонентов.
    """

    def __init__(self, name: str):
        self.name = name


class Category_(CategoryComponent):
    """
    Класс Контейнер содержит сложные компоненты, которые могут иметь вложенные
    компоненты.
    """

    def __init__(self):
        self.children: Dict[str: Component] = {}
        self.id = None

    def add(self, component: Component) -> None:
        component.id = self.get_id()
        self.children[component.name] = component
        component.parent = self

    def remove(self, component: Component) -> None:
        self.children.pop(component.name)
        component.parent = None



    def get_course_count(self) -> int:

        results = 0
        for child in self.children.values():
            if isinstance(child, Course_):
                results += 1
            else:
                results += child.get_course_count()
        return results


# def client_code2(component1: Component, component2: Component) -> None:
#     """
#     Благодаря тому, что операции управления потомками объявлены в базовом классе
#     Компонента, клиентский код может работать как с простыми, так и со сложными
#     компонентами, вне зависимости от их конкретных классов.
#     """
#
#     if component1.is_composite():
#         component1.add(component2)
#
#     print(f"RESULT: {component1.get_course_count()}", end="")


# if __name__ == "__main__":
    # Таким образом, клиентский код может поддерживать простые компоненты-
    # листья...

    # kulinary = Category('Кулинария')
    # italy = Category('Italy')
    # kulinary.add(Course('Курс 1'))
    # kulinary.add(Course('Курс 2'))
    # kulinary.add(italy)
    # italy.add(Course('Курс 3'))
    # italy.add(Course('Курс 4'))
    # italy.add(Category('pizza'))
    #
    # print(kulinary.get_course_count())
    # print(italy.get_course_count())
    #
    # course2 = Course('Курс 2')
    # course3 = Course('Курс 3')
