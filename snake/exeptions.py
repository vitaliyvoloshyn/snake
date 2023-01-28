class Base_Exception(Exception):
    """Базовый клас исключения"""
    code = 404
    text = 'Страница не найдена'

    def __str__(self):
        return f'{self.code} {self.text}'


class NotFound(Base_Exception):
    """Исключение Страница не найдена"""
    code = 404
    text = 'Страница не найдена'


class NotAllowed(Base_Exception):
    """Исключение Неподдерживаемый http метод"""
    code = 405
    text = 'Неподдерживаемый http метод'


class NotUniqueEmail(Exception):
    """Исключение не уникальности email при регистрации"""
    def __init__(self, txt):
        self.txt = txt
