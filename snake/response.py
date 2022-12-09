from snake.template_engine import Templator


class Response:

    def __init__(self,
                 status_code: int,
                 headers: dict = None,
                 body: str = '',
                 template_name: str = '',
                 context: dict = {}):
        self.status_code = status_code
        self.headers = {}
        self.body = body
        self.template_name = template_name
        self._set_base_headers()
        if headers is not None:
            self._update_headers(headers)
        if template_name:
            self._set_body(self._get_template_as_string(template_name, context))
        else:
            self._set_body(body)

    def _set_base_headers(self):
        self.headers = {
            'Content-Type': 'text/html; charset=utf-8',
            'Content-Length': 0
        }

    def _set_body(self, raw_body: str):
        self.body = raw_body.encode('utf-8')
        self._update_headers({
            'Content-Length': str(len(self.body))
        })

    def _update_headers(self, headers: dict):
        self.headers.update(headers)

    def _get_template_as_string(self, template_name: str, context: dict):
        template = Templator(template_name)
        return template.render(context)
