from urllib.parse import parse_qs


class Request:
    def __init__(self, environ: dict):
        self.build_get_params_dict(environ['QUERY_STRING'])

    def build_get_params_dict(self, raw_params: str) -> None:
        self.GET = parse_qs(raw_params)
