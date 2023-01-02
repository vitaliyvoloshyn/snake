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
    def wrapper(g, arg):
        print(f'Вызвана функция - {func.__name__}')
        print(arg)
        time_start = time.perf_counter()
        func(arg)
        print(f'затрачено на выполнение: {time.perf_counter() - time_start} с')

    return wrapper

@debug
def gh(hjhjhhj):
    print(f'this is {hjhjhhj}')

if __name__ == '__main__':
    gh('john')
