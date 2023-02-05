class DbCommitException(Exception):
    """Класс, описывающий исключение при операции вставки данных в таблицу"""
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    """Класс, описывающий исключение при операции вставки данных в таблицу"""
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    """Класс, описывающий исключение при операции удаления данных из таблицы"""
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    """Класс, описывающий исключение при операции выборки данных из таблицы"""
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')