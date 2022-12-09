from typing import List, Type

from snake.exeptions import NotFound, NotAllowed
from snake.views import NotFound404View, NotAllowed405View
from snake.request import Request
from snake.response import Response
from snake.urls import Url
from snake.views import View


class Snake:
    __slots__ = ('urls', 'view', 'request', 'response')

    def __init__(self, urls: List[Url]):
        self.urls = urls

    def __call__(self, environ: dict, start_response):
        self.view = self._get_view(environ)
        self.request = self._get_request(environ)
        self.response = self._get_response(environ, self.view, self.request)
        start_response(str(self.response.status_code), self.response.headers.items())
        return iter([self.response.body])

    @staticmethod
    def _prepare_url(url: str) -> str:
        if url[-1] == '/':
            return url[:-1]
        return url

    def _find_view(self, raw_url: str) -> Type[View]:
        url = self._prepare_url(raw_url)
        for path in self.urls:
            if path.url == url:
                return path.view
        raise NotFound

    def _get_view(self, environ: dict) -> View:
        raw_url = environ.get('PATH_INFO')
        try:
            view = self._find_view(raw_url)
        except NotFound as e:
            print(e)
            view = NotFound404View
        return view()  # возвращаем экземпляр соответствеющей View

    @staticmethod
    def _get_request(environ: dict) -> Request:
        return Request(environ)

    @staticmethod
    def _get_response(environ: dict, view: View, request: Request) -> Response:
        method = environ.get('REQUEST_METHOD').lower()
        try:
            if not hasattr(view, method):
                raise NotAllowed
        except NotAllowed as e:
            print(e)
            return NotAllowed405View().get(request)
        return getattr(view, method)(request)
