from pathlib import Path
from typing import Union

from snake.template_engine import Templator


class Response:
    """Базовый клас Ответа"""
    def __init__(self,
                 status_code: str,
                 headers: dict = None,
                 body: Union[str, bytes] = '',
                 ):
        self.status_code = status_code
        self.headers = {}
        self.body = body
        if headers is not None:
            self._update_headers(headers)

    def _set_body(self, raw_body: Union[str, bytes]):
        if isinstance(raw_body, str):
            self.body = raw_body.encode('utf-8')
        else:
            self.body = raw_body
        self._update_headers({
            'Content-Length': str(len(self.body))
        })

    def _update_headers(self, headers: dict):
        self.headers.update(headers)


class ResponseStatic(Response):
    """Класс ответа на запрос статики"""
    types = {
        ('jpg', 'png'): {'Content-Type': 'image/jpeg'},
        ('css'): {'Content-Type': 'text/css'},
        ('js'): {'Content-Type': 'text/javascript'}
    }

    def __init__(self,
                 status_code: str,
                 file: Path,
                 headers: dict = None,
                 ):
        super().__init__(status_code=status_code,
                         headers=headers,
                         )

        body = self._read_file_bytes(file)
        self._set_body(body)
        for type_, header in self.types.items():
            if file.suffix in type_:
                self._update_headers(header)

    def _read_file_bytes(self, file: Path) -> bytes:
        return file.read_bytes()


class ResponseHTML(Response):
    """Класс ответа на запрос html"""
    headers_ = {'Content-Type': 'text/html; charset=utf-8'}

    def __init__(self,
                 status_code: str,
                 template_name: str = '',
                 body: str = '',
                 headers: dict = None,
                 context: dict = {}):

        super().__init__(status_code=status_code,
                         headers=headers,
                         )
        if template_name:

            self._set_body(self._get_template_as_string(template_name, context))
        else:
            self._set_body(body)
        self._update_headers(self.headers_)

    @staticmethod
    def _get_template_as_string(template_name: str, context: dict):
        template = Templator(template_name)
        return template.render(context)

class ResponceRedirect(ResponseHTML):
    """Класс ответа при редиректе"""
    def __init__(self, to: str, context: dict = {}, status_code: str = '302 Found'):
        headers = {'Location': to}
        super().__init__(status_code=status_code, headers=headers, context=context)

