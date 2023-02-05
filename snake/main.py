import os.path
import pprint
from typing import List, Type
import view
from settings import BASE_DIR, DATABASE

from snake.exeptions import NotFound, NotAllowed
from snake.orm.db import create_table
from snake.request import Request
from snake.response import Response, ResponseStatic
from snake.static import StaticFiles
from snake.urlpatterns import urlpatterns
from snake.urls import Url
from snake.views import NotFound404View, NotAllowed405View
from snake.views import View



class Snake:
    __slots__ = ('urls', 'view', 'request', 'response', 'static_files', 'input_post_data')

    def __init__(self):
        self.urls = urlpatterns



    def __call__(self, environ: dict, start_response):
        # pprint.pprint(environ)
        # сначала проверяем запрос. Если запрос на статику, то формируем ответ и отдаем файл
        request_static_file = StaticFiles().get_static_file(self._get_filename_from_url(environ.get('PATH_INFO')))
        if request_static_file:
            self.response = ResponseStatic(status_code='200 OK', file=request_static_file)
        else:
            # если запрос на HTML, то тянем представление, вытаскиваем query_string, формируем ответ и отдаем данные
            self.view = self._get_view(environ)
            self.view.context = {
                'url': f'{environ["wsgi.url_scheme"]}://{environ["HTTP_HOST"]}'}  # формируем контекст для базового класса View
            self.request = self._get_request(environ)
            self.response = self._get_response(environ, self.view, self.request)
        start_response(str(self.response.status_code), list(self.response.headers.items()))
        return iter([self.response.body])

    @staticmethod
    def _prepare_url(url: str) -> str:
        """Подготовка url - удаляет последний символ ./"""
        if url[-1] == '/':
            return url[:-1]
        return url

    def _find_view(self, raw_url: str) -> Type[View]:
        """Ищет в списке urls совпадение запрашиваемого url и отдает соответствующий класс представления"""
        url = self._prepare_url(raw_url)
        for path in self.urls:
            if path.url == url:
                return path.view
        raise NotFound

    def _get_view(self, environ: dict) -> View:
        """Возвращает экземпляр класса представления"""
        raw_url = environ.get('PATH_INFO')
        try:
            view = self._find_view(raw_url)
        except NotFound as e:
            view = NotFound404View
        return view()  # возвращаем экземпляр соответствеющей View

    @staticmethod
    def _get_request(environ: dict) -> Request:
        """Возвращает объекта класса Request"""
        return Request(environ)

    @staticmethod
    def _get_response(environ: dict, view: View, request: Request) -> Response:
        """Возвращает экземпляр обьекта класса Response определенного представления"""
        method = environ.get('REQUEST_METHOD').lower()
        try:
            if not hasattr(view, method):
                raise NotAllowed
        except NotAllowed as e:
            return NotAllowed405View().get(request)
        return getattr(view, method)(request)

    @staticmethod
    def _get_filename_from_url(url: str) -> str:
        """Определяет и возвращает имя запрашиваемого статического файла из url"""
        try:
            filename = url[url.rfind('/') + 1:]
            return filename
        except:
            return ''
