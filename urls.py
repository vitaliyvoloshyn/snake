from snake.urls import Url
from view import HomePageView, DeveloperPageView

"""каждый элемент списка urlpatterns - это экземрляр класса Url (dataclass), содержащий два поля: url и класс View"""

urlpatterns = [
    Url('', HomePageView),
    Url('/developer', DeveloperPageView)
]
