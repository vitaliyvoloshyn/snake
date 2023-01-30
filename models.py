import importlib

from snake.models_ import Text, Models


class Student(Models):
    last_name = Text()
    first_name = Text()
    email = Text()
    phone = Text()
    course = Text()

class Category(Models):
    name = Text()

class Course(Models):
    name = Text()
    parent_category = Text()


if __name__ == '__main__':
    module = importlib.import_module('models')
    classes = [
        value
        for value in (
            getattr(module, name)
            for name in dir(module)
        )
        if isinstance(value, type)
           and getattr(value, '__module__', None) == module.__name__
    ]
    print(classes[0].__dict__)
