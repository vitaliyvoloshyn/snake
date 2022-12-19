from wsgiref.simple_server import make_server

from snake.main import Snake
from urls import urlpatterns
app = Snake(urls=urlpatterns)
# class Server:
#     __instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if cls.__instance is None:
#             cls.__instance = super().__new__(cls)
#         return cls.__instance
#
#     def __init__(self, host: str = '', port: int = 8080):
#         self.host = host
#         self.port = port
#         self.instance = self
#
#     def run_server(self):
#         with make_server(self.host, self.port, self.app) as httpd:
#             print("Запуск на порту 8080...")
#             httpd.serve_forever()
#
# if __name__ == '__main__':
#     Server()
