from __future__ import annotations

import importlib
from snake.models_ import Models, CharField, ForeignKey, Integer


class Category(Models):
    name = CharField()
    image = CharField()
    category = ForeignKey()


class Course(Models):
    name = CharField(max_length=60)
    category = ForeignKey('category')


class Student(Models):
    last_name = CharField(60, not_null=True)
    first_name = CharField(60)
    email = CharField(120, not_null=True, unique=True)
    phone = CharField(60)
    course = ForeignKey('course')


if __name__ == '__main__':
    print(Category)
    # module = importlib.import_module('models')
    # classes = [
    #     value
    #     for value in (
    #         getattr(module, name)
    #         for name in dir(module)
    #     )
    #     if isinstance(value, type)
    #        and getattr(value, '__module__', None) == module.__name__
    # ]
    # print(classes[0].__dict__)
