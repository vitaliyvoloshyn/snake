from wsgiref.simple_server import make_server

from snake.main import Snake
# from view import urlpatterns

app = Snake()

with make_server('', 8080, app) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()
