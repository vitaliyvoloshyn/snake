from jinja2 import Environment, FileSystemLoader

from settings import TEMPLATE_DIR_NAME


class Templator:
    def __init__(self, template_name: str):
        self.loader = FileSystemLoader(TEMPLATE_DIR_NAME)
        self.env = Environment(loader=self.loader)
        self.template_name = template_name

    def _get_template(self):
        self.template = self.env.get_template(self.template_name)

    def render(self, context: dict) -> str:
        self._get_template()
        return self.template.render(context)
