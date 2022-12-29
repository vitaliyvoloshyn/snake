from patterns.creational_patterns import get_logger
from snake.request import Request
from snake.response import ResponseHTML, Response

logger = get_logger('my_log')


class View:
    status_code: str = '200 OK'
    body = 'testing page'
    context: dict = {}

    def get(self, request: Request = None, *args, **kwargs) -> Response:
        return ResponseHTML(status_code=self.status_code, body=self.body, context=self.get_context())

    def post(self, request: Request = None, *args, **kwargs) -> Response:
        return ResponseHTML(status_code=self.status_code, body=self.body, context=self.get_context())

    def get_context(self) -> dict:
        return self.context


class NotFound404View(View):
    status_code: str = '404 NOT FOUND'
    body = '<h1>404 Страница не найдена</h1>'


class NotAllowed405View(View):
    status_code: str = '405 NOT ALLOWED'
    body = '<h1>405 Not Allowed</h1>'


class TemplateView(View):
    template_name = ''

    def get(self, request: Request = None, *args, **kwargs) -> Response:
        logger.log("принят GET-запрос")
        return ResponseHTML(status_code=self.status_code, template_name=self.template_name, context=self.get_context())

    def post(self, request: Request = None, *args, **kwargs) -> Response:
        logger.log("принят POST-запрос")
        return ResponseHTML(status_code=self.status_code, template_name=self.template_name, context=self.get_context())
