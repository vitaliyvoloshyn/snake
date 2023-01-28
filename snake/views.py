from patterns.patterns import get_logger
from snake.request import Request
from snake.response import ResponseHTML, Response

logger = get_logger('my_log')


class View:
    """Базовый класс представления"""
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
    """Класс представления 404 ошибки"""
    status_code: str = '404 NOT FOUND'
    body = '<h1>404 Страница не найдена</h1>'


class NotAllowed405View(View):
    """Класс представления 405 ошибки"""
    status_code: str = '405 NOT ALLOWED'
    body = '<h1>405 Not Allowed</h1>'


class TemplateView(View):
    """Класс шаблонного представления"""
    template_name = ''

    def get(self, request: Request = None, *args, **kwargs) -> Response:
        logger.log("принят GET-запрос")
        obj = ResponseHTML(status_code=self.status_code, template_name=self.template_name, context=self.get_context())
        return obj

    def post(self, request: Request = None, *args, **kwargs) -> Response:
        logger.log("принят POST-запрос")
        return ResponseHTML(status_code=self.status_code, template_name=self.template_name, context=self.get_context())


class ListView(TemplateView):
    """Класс шаблонного представления для отображения списков"""
    model = None
    context_object_name = 'objects_list'
    queryset = []

    def get_queryset(self) -> list:
        self.queryset = self.model.all()
        return self.queryset

    def get_context(self) -> dict:
        return {self.context_object_name: self.get_queryset()}


class DetailView(ListView):
    """Класс шаблонного представления для отображения детализации"""
    context_object_name = 'object'
    object_id: int = 0

    def __init__(self):
        super().__init__()

    def get_queryset(self) -> list:
        self.queryset = self.model.find_by_id(self.object_id)
        return self.queryset

    def get_context(self) -> dict:
        return {self.context_object_name: self.queryset}

    def get(self, request: Request = None, *args, **kwargs) -> Response:
        self.object_id = self._get_object_id(request)
        if not self.object_id:
            return Response(status_code='404 NOT FOUND', body=b'404 NOT FOUND')
        self.get_queryset()
        return super().get(request)

    @staticmethod
    def _get_object_id(request: Request) -> int:
        id_ = request.GET.get('id', 0)
        return id_[0] if id_ else 0

