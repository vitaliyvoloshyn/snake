from __future__ import annotations

from abc import ABC, abstractmethod


class Notifier(ABC):
    """Абстрактный класс уведомителя"""
    @classmethod
    @abstractmethod
    def notify(cls, student):
        pass


class EmailNotifier(Notifier):
    """Уведомитель по электронной почте"""

    @classmethod
    def notify(cls, student):
        """Функция уведомления"""
        print(
            f'Отправлено уведомление студенту {student.last_name} {student.first_name} на электронный адрес {student.email}')


class PhoneNotifier(Notifier):
    """Уведомитель по телефону (смс)"""

    @classmethod
    def notify(cls, student):
        """Функция уведомления"""
        print(f'Отправлено уведомление студенту {student.last_name} {student.first_name} на телефон {student.phone}')


class Handler:
    """Абстрактный класс обработчика вывода для логгера"""
    def print_(self, text):
        """Функция вывода сообщения"""
        pass


class ConsoleHandler(Handler):
    """Обработчик вывода в консоль"""
    def print_(self, text):
        """Функция вывода сообщения"""
        print(text)


class FileHandler(Handler):
    """Обработчик вывода в файл"""
    def __init__(self, filename: str):
        self._out_file = filename

    def print_(self, text: str):
        """Функция вывода сообщения"""
        with open(self._out_file, 'a') as f:
            f.write(text + '\n')


class Formatter:
    """Объект форматировщика сообщений для логгера"""
    @staticmethod
    def get_format_text(text):
        """Возвращает отформатированное сообщение"""
        return f'log >>> {text}'


class Log:
    """Класс логгера"""
    _instance: dict = {}

    def __init__(self, name: str):
        self._name = name
        self._handler = ConsoleHandler()
        self._formatter = Formatter()

    def __new__(cls, *args, **kwargs):
        name = args[0] if args else kwargs.get('name', None)
        if not cls._instance.get(name, None):
            cls._instance[name] = super().__new__(cls)
        return cls._instance[name]

    def set_handler(self, handler: Handler):
        """Устанавливает обработчик вывода"""
        if handler.__name__ == 'FileHandler':
            self._handler = handler(f'{self._name}_log.txt')
        elif handler.__name__ == 'ConsoleHandler':
            self._handler = handler

    def set_formatter(self, formatter: Formatter):
        """Устанавливает форматировщик сообщений"""
        self._formatter = formatter

    def log(self, text: str):
        """Логгирование сообщения"""
        self._handler.print_(self._formatter.get_format_text(text))


def get_logger(name: str) -> Log:
    """Возвращает объект логгера"""
    return Log(name)
