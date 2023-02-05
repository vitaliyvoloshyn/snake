import importlib


# def get_user_models_classes() -> dict:
#     """Возвращает список классов моделей, созданных пользователем в модуле models"""
#     try:
#         module = importlib.import_module('models')
#         print(dir(module))
#         classes = [
#             value
#             for value in (
#                 getattr(module, name)
#                 for name in dir(module)
#             )
#             if isinstance(value, type)
#                and getattr(value, '__module__', None) == module.__name__
#         ]
#         return classes
#     except ModuleNotFoundError:
#         pass
#     return []


def get_attr_class(clas) -> dict:
    """Возвращает словарь аттрибутов пользовательского класса"""

    dct = {key: value for key, value in clas.__dict__.items() if key != '__module__' and key != '__doc__'}
    return dct


if __name__ == '__main__':
    # get_user_models_classes()
    pass