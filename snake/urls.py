from dataclasses import dataclass
from snake.views import View
from typing import Type


@dataclass
class Url:
    url: str
    view: Type[View]
