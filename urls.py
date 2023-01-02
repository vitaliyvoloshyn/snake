from snake.urls import Url
from view import HomePageView, DeveloperPageView, AboutPageView, FirstGalleryPageView, SecondGalleryPageView, \
    ThirdGalleryPageView, ContactPageView, LearnCookPageView, DetailCategoryView

"""каждый элемент списка urlpatterns - это экземрляр класса Url (dataclass), содержащий два поля: url и класс View"""

# urlpatterns = [
#     Url('', HomePageView),
#     Url('/about', AboutPageView),
#     Url('/developer', DeveloperPageView),
#     Url('/firstgallery', FirstGalleryPageView),
#     Url('/secondgallery', SecondGalleryPageView),
#     Url('/thirdgallery', ThirdGalleryPageView),
#     Url('/contact', ContactPageView),
#     Url('/learncook', LearnCookPageView),
#     Url('/learncook/category', DetailCategoryView)
# ]
