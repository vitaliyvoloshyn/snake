import time

from snake.urlpatterns import urlpatterns
from snake.urls import Url
from snake.views import View


class AppRout:

    def __init__(self, url: str):
        self.url = url

    def __call__(self, cls: View):
        urlpatterns.append(Url(self.url, cls))


def debug(func):
    def wrapper(inst, arg):
        print(f'----------debug----------')
        print(f'Вызвана функция - {func.__name__} {inst}')
        time_start = time.perf_counter()
        result = func(inst, arg)
        print(f'затрачено на выполнение: {time.perf_counter() - time_start} с')
        print('-' * 25)
        return result

    return wrapper
