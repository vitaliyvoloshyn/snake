from dataclasses import dataclass
from snake.views import View


@dataclass
class Url:
    url: str
    view: View
