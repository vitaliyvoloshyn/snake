from urllib.parse import parse_qs


class Request:
    def __init__(self, environ: dict):
        self.build_get_params_dict(environ['QUERY_STRING'])
        self.build_post_data_dict(environ['CONTENT_LENGTH'], environ['wsgi.input'])

    def build_post_data_dict(self, content_length: str, raw_data):
        self.POST = {}
        input_data_length = int(content_length) if content_length else 0
        if input_data_length:
            input_data_str = raw_data.read(input_data_length).decode()
            self.POST = parse_qs(input_data_str)

    def build_get_params_dict(self, raw_params: str) -> None:
        self.GET = parse_qs(raw_params)
        self.GET['raw_query_string'] = raw_params
