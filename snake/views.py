from snake.request import Request
from snake.response import Response


class View:
    status_code: int = 200
    body: str = 'testing page'
    context: dict = {}

    def get(self, request: Request, *args, **kwargs) -> Response:
        return Response(status_code=self.status_code, body=self.body, context=self.get_context())

    def get_context(self) -> dict:
        return self.context


class NotFound404View(View):
    status_code = 404
    body = '<h1>404 Страница не найдена</h1>'


class NotAllowed405View(View):
    status_code = 404
    body = '<h1>405 Not Allowed</h1>'


class TemplateView(View):
    template_name = ''

    def get(self, request: Request, *args, **kwargs) -> Response:
        return Response(status_code=self.status_code, template_name=self.template_name, context=self.get_context())
