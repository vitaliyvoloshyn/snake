class Base_Exception(Exception):
    code = 404
    text = 'Страница не найдена'

    def __str__(self):
        return f'{self.code} {self.text}'


class NotFound(Base_Exception):
    code = 404
    text = 'Страница не найдена'


class NotAllowed(Base_Exception):
    code = 405
    text = 'Неподдерживаемый http метод'
